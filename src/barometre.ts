import { Ctx, esc } from "./_lib/common"
import { Month, Point, cacheKey, readHistory, routeMonths } from "./apercu-prix"
// Baromètre des prix (/barometre-prix/) : pour les grands trajets de la diaspora, le prix aller-retour le plus bas des
// 6 prochains mois, son évolution sur 7 et 30 jours (historique gardé dans KV par apercu-prix.ts) et le mois le moins cher.
// Le tableau est écrit dans la page par le serveur (lisible par Google). Les prix viennent du cache des pages trajets ;
// le relevé quotidien (.github/workflows/releve-prix.yml) ouvre chaque page trajet listée ici pour tenir les prix à jour.
const ROUTES: [string, string, string, string][] = [
  ["CDG", "DSS", "Paris → Dakar", "vol-paris-dakar"], ["CDG", "BKO", "Paris → Bamako", "vol-paris-bamako"],
  ["CDG", "ABJ", "Paris → Abidjan", "vol-paris-abidjan"], ["CDG", "CKY", "Paris → Conakry", "vol-paris-conakry"],
  ["CDG", "DLA", "Paris → Douala", "vol-paris-douala"], ["CDG", "NSI", "Paris → Yaoundé", "vol-paris-yaounde"],
  ["CDG", "FIH", "Paris → Kinshasa", "vol-paris-kinshasa"], ["CDG", "BZV", "Paris → Brazzaville", "vol-paris-brazzaville"],
  ["CDG", "LBV", "Paris → Libreville", "vol-paris-libreville"], ["CDG", "LFW", "Paris → Lomé", "vol-paris-lome"],
  ["CDG", "COO", "Paris → Cotonou", "vol-paris-cotonou"], ["CDG", "OUA", "Paris → Ouagadougou", "vol-paris-ouagadougou"],
  ["CDG", "NKC", "Paris → Nouakchott", "vol-paris-nouakchott"], ["CDG", "ALG", "Paris → Alger", "vol-paris-alger"],
  ["CDG", "ORN", "Paris → Oran", "vol-paris-oran"], ["ORY", "CMN", "Paris → Casablanca", "vol-paris-casablanca"],
  ["CDG", "RAK", "Paris → Marrakech", "vol-paris-marrakech"], ["CDG", "TUN", "Paris → Tunis", "vol-paris-tunis"],
  ["CDG", "DJE", "Paris → Djerba", "vol-paris-djerba"], ["LYS", "ALG", "Lyon → Alger", "vol-lyon-alger"],
  ["MRS", "ALG", "Marseille → Alger", "vol-marseille-alger"], ["MRS", "TUN", "Marseille → Tunis", "vol-marseille-tunis"],
  ["BRU", "FIH", "Bruxelles → Kinshasa", "vol-bruxelles-kinshasa"], ["BRU", "DSS", "Bruxelles → Dakar", "vol-bruxelles-dakar"],
]
const CACHE_S = 3600
const STABLE = 3 // variation de ±3 % ou moins : « stable »

const money = (n: number) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
const iso = (daysAgo: number) => new Date(Date.now() - daysAgo * 864e5).toISOString().slice(0, 10)
const frDate = (d: string, o: Intl.DateTimeFormatOptions) => { const [y, m, j] = d.split("-").map(Number); return new Date(Date.UTC(y, m - 1, j || 1)).toLocaleDateString("fr-FR", { ...o, timeZone: "UTC" }) }

// Prix relevé il y a environ n jours (le relevé le plus proche, à ± marge jours)
function ago(hist: Point[], n: number, margin: number) {
  const target = Date.parse(iso(n))
  let best: Point | null = null
  for (const p of hist) {
    const gap = Math.abs(Date.parse(p[0]) - target) / 864e5
    if (gap <= margin && (!best || gap < Math.abs(Date.parse(best[0]) - target) / 864e5)) best = p
  }
  return best ? best[1] : null
}
const pct = (now: number, then: number | null) => (then ? Math.round((now / then - 1) * 100) : null)

type Row = { label: string; path: string; from: string; to: string; price: number; d7: number | null; d30: number | null; month: Month | null }

async function rows(ctx: Ctx): Promise<Row[]> {
  const cache = (globalThis as any).caches?.default
  const out = await Promise.all(ROUTES.map(async ([from, to, label, path]) => {
    const hist = await readHistory(ctx, from, to)
    const hit = cache ? await cache.match(cacheKey(from, to)) : null
    const months: Month[] = hit ? await hit.json() : []
    const last = hist.length ? hist[hist.length - 1] : null
    const price = months.length ? Math.min(...months.map((m) => m.price)) : last && last[0] >= iso(3) ? last[1] : null
    if (!price) return { missing: [from, to] as const }
    const month = months.length ? months.reduce((a, b) => (b.price < a.price ? b : a)) : null
    return { row: { label, path, from, to, price, d7: pct(price, ago(hist, 7, 2)), d30: pct(price, ago(hist, 30, 5)), month } as Row }
  }))
  // Trajets sans prix en cache : préparés en arrière-plan (3 par visite) pour la visite suivante
  const missing = out.filter((o: any) => o.missing).slice(0, 3).map((o: any) => o.missing)
  if (missing.length) ctx.waitUntil(Promise.all(missing.map(([f, t]: string[]) => routeMonths(ctx, f, t).catch(() => null))))
  return out.filter((o: any) => o.row).map((o: any) => o.row)
}

const trend = (v: number | null) => v === null ? `<span class="bt-na">—</span>`
  : `<span class="${v <= -STABLE ? "bt-down" : v >= STABLE ? "bt-up" : "bt-flat"}">${v > 0 ? "+" : v < 0 ? "−" : ""}${Math.abs(v)} %</span>`

function render(list: Row[]) {
  const today = frDate(iso(0), { day: "numeric", month: "long", year: "numeric" })
  const with7 = list.filter((r) => r.d7 !== null)
  let lead = `Relevé du ${today} : ${list.length} grands trajets suivis chaque jour.`
  if (with7.length >= 3) {
    const down = with7.filter((r) => r.d7! <= -STABLE).length, up = with7.filter((r) => r.d7! >= STABLE).length
    const min = with7.reduce((a, b) => (b.d7! < a.d7! ? b : a)), max = with7.reduce((a, b) => (b.d7! > a.d7! ? b : a))
    lead += ` Sur 7 jours, ${down} trajet${down > 1 ? "s" : ""} en baisse, ${up} en hausse et ${with7.length - down - up} stable${with7.length - down - up > 1 ? "s" : ""}.`
    if (min.d7! <= -STABLE) lead += ` Plus forte baisse : ${min.label} (${min.d7} %, dès ${money(min.price)}).`
    if (max.d7! >= STABLE) lead += ` Plus forte hausse : ${max.label} (+${max.d7} %, dès ${money(max.price)}).`
  } else {
    lead += " Les évolutions sur 7 et 30 jours s'affichent dès qu'il y a assez de relevés pour chaque trajet."
  }
  const cheapest = list.slice().sort((a, b) => a.price - b.price)
  const body = cheapest.map((r) => `<tr><th scope="row"><a href="/${r.path}/">${esc(r.label)}</a></th>` +
    `<td><strong>${esc(money(r.price))}</strong></td><td>${trend(r.d7)}</td><td>${trend(r.d30)}</td>` +
    `<td>${r.month ? esc(frDate(r.month.month, { month: "long", year: "numeric" })) : "—"}</td></tr>`).join("")
  return `<p class="bt-lead">${esc(lead)}</p>` +
    `<div class="bt-wrap"><table class="bt-table"><thead><tr><th scope="col">Trajet</th><th scope="col">Aller-retour dès</th>` +
    `<th scope="col">Sur 7 jours</th><th scope="col">Sur 30 jours</th><th scope="col">Mois le moins cher</th></tr></thead><tbody>${body}</tbody></table></div>`
}

export const onRequest = async (ctx: Ctx) => {
  const response = await ctx.next()
  if (ctx.request.method !== "GET" || !response.ok) return response
  const cache = (globalThis as any).caches?.default
  const key = new Request("https://escale.live/__barometre/" + iso(0))
  try {
    let block = ""
    const hit = cache ? await cache.match(key) : null
    if (hit) block = await hit.text()
    else {
      const list = await rows(ctx)
      if (list.length) {
        block = render(list)
        if (cache) ctx.waitUntil(cache.put(key, new Response(block, { headers: { "Cache-Control": `public, max-age=${CACHE_S}` } })))
      }
    }
    if (!block) return response
    const html = (await response.text()).replace(/<div id="barometre">[\s\S]*?<\/div><!-- \/barometre -->/, `<div id="barometre" data-ssr="1">${block}</div><!-- /barometre -->`)
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    return new Response(html, { status: response.status, headers })
  } catch {
    return response
  }
}

// Liste des pages trajets du baromètre (pour le relevé quotidien et la page statique)
export const PAGES = ROUTES.map((r) => r[3])
