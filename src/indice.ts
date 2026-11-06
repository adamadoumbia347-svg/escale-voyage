import { Ctx, esc } from "./_lib/common"
import { Row, rows } from "./barometre"
// Indice Escale des prix (/indice-prix/) : à partir des prix relevés chaque jour pour le baromètre (historique KV),
// la variation médiane sur 30 et 7 jours, par grande région, les plus fortes hausses et baisses, et une phrase prête à citer.
// Aucun chiffre inventé : sans assez de relevés, la page le dit. Écrit par le serveur (lisible par Google), en cache une journée.

const REGIONS: [string, string[]][] = [
  ["Afrique de l'Ouest", ["DSS", "BKO", "ABJ", "CKY", "LFW", "COO", "OUA", "NKC", "NIM", "OXB", "BJL", "RAI", "ACC", "LOS", "ABV"]],
  ["Afrique centrale", ["DLA", "NSI", "FIH", "BZV", "LBV", "NDJ", "LAD"]],
  ["Maghreb et Égypte", ["ALG", "ORN", "CMN", "RAK", "TUN", "DJE", "CAI"]],
  ["Afrique de l'Est, australe et océan Indien", ["ADD", "NBO", "JNB", "KGL", "TNR", "MPM", "DAR", "MRU"]],
]
const ORIG: [string, string[]][] = [["Depuis la France et la Belgique", ["CDG", "ORY", "LYS", "MRS", "BRU"]], ["Depuis Londres", ["LHR"]], ["Depuis l'Italie", ["MXP", "FCO"]]]

const money = (n: number) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
const today = () => new Date().toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Paris" })
const median = (a: number[]) => { if (!a.length) return null; const s = a.slice().sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2) }
const sign = (v: number) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v) + " %"
const cls = (v: number) => (v <= -3 ? "bt-down" : v >= 3 ? "bt-up" : "bt-flat")

export function render(list: Row[]) {
  const d = today()
  const use30 = list.filter((r) => r.d30 !== null).length >= 5
  const key = use30 ? "d30" : "d7"
  const span = use30 ? "30 jours" : "7 jours"
  const with_ = list.filter((r) => r[key] !== null)
  if (with_.length < 3) {
    return `<p class="bt-lead">Relevé du ${esc(d)} : pas encore assez de relevés pour calculer l'indice. Il s'affiche dès que les prix de chaque trajet ont au moins une semaine d'historique.</p>`
  }
  const vals = with_.map((r) => r[key] as number)
  const med = median(vals)!
  const down = vals.filter((v) => v <= -3).length, up = vals.filter((v) => v >= 3).length
  const sorted = with_.slice().sort((a, b) => (a[key] as number) - (b[key] as number))
  const bottom = sorted.slice(0, 5).filter((r) => (r[key] as number) <= -3), top = sorted.slice(-5).reverse().filter((r) => (r[key] as number) >= 3)
  const trend = med >= 3 ? `ont augmenté de ${med} %` : med <= -3 ? `ont baissé de ${Math.abs(med)} %` : `sont restés stables (${sign(med)})`
  let quote = `Selon l'Indice Escale des prix du ${d}, les prix des billets d'avion entre l'Europe et l'Afrique ${trend} sur ${span} (médiane de ${with_.length} grands trajets suivis chaque jour).`
  if (top[0]) quote += ` La plus forte hausse concerne ${top[0].label} (${sign(top[0][key] as number)}, dès ${money(top[0].price)} aller-retour).`
  if (bottom[0]) quote += ` La plus forte baisse concerne ${bottom[0].label} (${sign(bottom[0][key] as number)}, dès ${money(bottom[0].price)}).`
  const block = (title: string, codes: string[], by: "to" | "from") => {
    const g = with_.filter((r) => codes.includes(r[by]))
    const m = median(g.map((r) => r[key] as number)), p = median(g.map((r) => r.price))
    return g.length >= 2 && m !== null ? `<tr><th scope="row">${esc(title)}</th><td><span class="${cls(m)}">${sign(m)}</span></td><td>${p ? esc(money(p)) : "—"}</td><td>${g.length}</td></tr>` : ""
  }
  const rowsHtml = (rs: Row[]) => rs.map((r) => `<li><a href="/${r.path}/">${esc(r.label)}</a> : <span class="${cls(r[key] as number)}">${sign(r[key] as number)}</span>, dès <strong>${esc(money(r.price))}</strong></li>`).join("")
  const regions = REGIONS.map(([t, c]) => block(t, c, "to")).join(""), origins = ORIG.map(([t, c]) => block(t, c, "from")).join("")
  const thead = `<thead><tr><th scope="col"></th><th scope="col">Variation sur ${span}</th><th scope="col">Prix médian aller-retour</th><th scope="col">Trajets</th></tr></thead>`
  return `<p class="bt-lead">Relevé du ${esc(d)}</p>` +
    `<div class="ix-big"><span class="ix-num ${cls(med)}">${sign(med)}</span><span class="ix-lab">variation médiane des prix sur ${span}<br><small>${with_.length} trajets · ${down} en baisse · ${up} en hausse · ${with_.length - down - up} stables</small></span></div>` +
    `<blockquote class="ix-quote"><p id="ix-q">${esc(quote)}</p><footer>Source : Escale, <a href="https://escale.live/indice-prix/">escale.live/indice-prix</a></footer></blockquote>` +
    `<p><button type="button" class="btn ghost" id="ix-copy">📋 Copier la phrase et la source</button></p>` +
    (regions ? `<h2>Par région d'arrivée</h2><div class="bt-wrap"><table class="bt-table">${thead}<tbody>${regions}</tbody></table></div>` : "") +
    (origins ? `<h2>Par pays de départ</h2><div class="bt-wrap"><table class="bt-table">${thead}<tbody>${origins}</tbody></table></div>` : "") +
    (top.length ? `<h2>Les plus fortes hausses</h2><ul class="ix-list">${rowsHtml(top)}</ul>` : "") +
    (bottom.length ? `<h2>Les plus fortes baisses</h2><ul class="ix-list">${rowsHtml(bottom)}</ul>` : "") +
    `<h2>Les trajets les moins chers du moment</h2><ul class="ix-list">${rowsHtml(list.slice().sort((a, b) => a.price - b.price).slice(0, 5).filter((r) => r[key] !== null))}</ul>`
}

export const onRequest = async (ctx: Ctx) => {
  const response = await ctx.next()
  if (ctx.request.method !== "GET" || !response.ok) return response
  const cache = (globalThis as any).caches?.default
  const key = new Request("https://escale.live/__indice/v1/" + new Date().toISOString().slice(0, 10))
  try {
    let block = ""
    const hit = cache ? await cache.match(key) : null
    if (hit) block = await hit.text()
    else {
      const list = await rows(ctx)
      if (list.length) {
        block = render(list)
        if (cache) ctx.waitUntil(cache.put(key, new Response(block, { headers: { "Cache-Control": "public, max-age=3600" } })))
      }
    }
    if (!block) return response
    const html = (await response.text()).replace(/<div id="indice">[\s\S]*?<\/div><!-- \/indice -->/, `<div id="indice" data-ssr="1">${block}</div><!-- /indice -->`)
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    return new Response(html, { status: response.status, headers })
  } catch {
    return response
  }
}
