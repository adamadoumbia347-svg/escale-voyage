import { Ctx, esc, pricesForDates } from "./_lib/common"
// Pages trajets : les prix réels sont écrits directement dans la page, pour les visiteurs comme pour Google
// (avant, ils n'apparaissaient qu'après le chargement, via route-prices.js, et les moteurs de recherche ne les voyaient pas).
// - titre, description et aperçu des liens partagés : « … · dès 389 € »
// - en haut de page : « Aller-retour repéré dès 389 € »
// - section « Prix repérés récemment » : le prix le plus bas pour chacun des 6 prochains mois, avec une phrase de résumé
// Les prix (Travelpayouts) sont gardés 6 heures dans le cache de Cloudflare. Sans réponse rapide, la page part telle quelle
// et route-prices.js prend le relais dans le navigateur. Les chemins concernés sont listés dans wrangler.jsonc (run_worker_first).
const PAGES = /^\/(vol-|en\/flights-|es\/vuelos-|pt\/voos-|ar\/flights-)/
const MONTHS = 6
const WAIT_MS = 2500
const CACHE_S = 6 * 3600

type Month = { month: string; price: number; dep: string; ret: string; transfers: number }

const L: Record<string, { loc: string; from: string; hero: string; direct: string; one: string; many: string; best: string; go: string
  summary: string; updated: string }> = {
  fr: { loc: "fr-FR", from: "dès", hero: "Aller-retour repéré dès", direct: "vol direct", one: "1 escale", many: " escales", best: "Le moins cher", go: "Voir ces dates",
    summary: "Mois le moins cher en ce moment : {m}, dès {p} l’aller-retour. Sur les {n} prochains mois, les prix repérés vont de {p} à {max}.", updated: "Prix mis à jour le {d}." },
  en: { loc: "en-GB", from: "from", hero: "Round trip found from", direct: "direct", one: "1 stop", many: " stops", best: "Cheapest", go: "See these dates",
    summary: "Cheapest month right now: {m}, from {p} return. Over the next {n} months, prices found range from {p} to {max}.", updated: "Prices updated on {d}." },
  es: { loc: "es-ES", from: "desde", hero: "Ida y vuelta desde", direct: "vuelo directo", one: "1 escala", many: " escalas", best: "El más barato", go: "Ver estas fechas",
    summary: "Mes más barato ahora mismo: {m}, desde {p} ida y vuelta. En los próximos {n} meses, los precios encontrados van de {p} a {max}.", updated: "Precios actualizados el {d}." },
  pt: { loc: "pt-PT", from: "desde", hero: "Ida e volta desde", direct: "voo direto", one: "1 escala", many: " escalas", best: "O mais barato", go: "Ver estas datas",
    summary: "Mês mais barato neste momento: {m}, desde {p} ida e volta. Nos próximos {n} meses, os preços encontrados vão de {p} a {max}.", updated: "Preços atualizados a {d}." },
  ar: { loc: "ar-u-nu-latn", from: "من", hero: "ذهاب وعودة ابتداءً من", direct: "رحلة مباشرة", one: "توقف واحد", many: " توقفات", best: "الأرخص", go: "اعرض هذه التواريخ",
    summary: "أرخص شهر حاليًا: {m}، من {p} ذهابًا وعودة. خلال الأشهر الـ{n} القادمة، تتراوح الأسعار بين {p} و{max}.", updated: "آخر تحديث للأسعار: {d}." },
}

// Prix le plus bas par mois de départ (6 prochains mois), depuis le cache Cloudflare ou Travelpayouts.
// null = service indisponible (rien n'est gardé en cache) ; [] = aucun prix connu pour ce trajet.
async function routeMonths(ctx: Ctx, from: string, to: string): Promise<Month[] | null> {
  const cache = (globalThis as any).caches?.default
  const key = new Request(`https://escale.live/__prix-trajet/${from}-${to}`)
  if (cache) {
    const hit = await cache.match(key)
    if (hit) return hit.json()
  }
  const token = ctx.env.TRAVELPAYOUTS_TOKEN!
  const now = new Date(), today = now.toISOString().slice(0, 10)
  const months = Array.from({ length: MONTHS }, (_, i) => new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + i, 1)).toISOString().slice(0, 7))
  const rows = await Promise.all(months.map((m) => pricesForDates(token, { origin: from, destination: to, departure_at: m, one_way: "false", sorting: "price", currency: "eur", limit: "5" }, 6000)))
  if (rows.every((r) => r === null)) return null
  const out: Month[] = []
  rows.forEach((data, i) => {
    const t = (data ?? []).filter((x: any) => x.price && String(x.departure_at || "").slice(0, 10) >= today).sort((a: any, b: any) => a.price - b.price)[0]
    if (t) out.push({ month: months[i], price: t.price, dep: String(t.departure_at).slice(0, 10), ret: t.return_at ? String(t.return_at).slice(0, 10) : "", transfers: t.transfers ?? 0 })
  })
  if (cache) ctx.waitUntil(cache.put(key, new Response(JSON.stringify(out), { headers: { "Content-Type": "application/json", "Cache-Control": `public, max-age=${CACHE_S}` } })))
  return out
}

function render(html: string, from: string, to: string, rows: Month[]) {
  const lang = (html.match(/<html lang="([a-z]{2})"/) || [])[1] || "fr"
  const t = L[lang] || L.fr
  const money = (n: number) => { try { return new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n) } catch { return Math.round(n) + " €" } }
  const date = (iso: string, o: Intl.DateTimeFormatOptions) => { const [y, m, d] = iso.split("-").map(Number); try { return new Date(Date.UTC(y, m - 1, d || 1)).toLocaleDateString(t.loc, { ...o, timeZone: "UTC" }) } catch { return iso } }
  const fill = (s: string, o: Record<string, string>) => s.replace(/\{(\w+)\}/g, (_, k) => o[k])
  const prices = rows.map((r) => r.price), best = Math.min(...prices), max = Math.max(...prices)
  const bestRow = rows.find((r) => r.price === best)!
  const label = `${t.from} ${money(best)}`
  const lead = label.charAt(0).toUpperCase() + label.slice(1)
  const app = lang === "fr" ? "" : "&lang=" + lang
  const items = rows.map((r) => {
    const stops = r.transfers === 0 ? t.direct : r.transfers === 1 ? t.one : r.transfers + t.many
    const when = date(r.dep, { day: "numeric", month: "short" }) + (r.ret ? " → " + date(r.ret, { day: "numeric", month: "short" }) : "")
    const href = `/?type=vols&from=${from}&to=${to}&dep=${r.dep}` + (r.ret ? `&ret=${r.ret}` : "") + app
    return `<li class="price-row"><div><span class="price-month">${esc(date(r.month, { month: "long", year: "numeric" }))}` +
      (r.price === best ? ` <span class="pill-best">${esc(t.best)}</span>` : "") + `</span>` +
      `<span class="price-meta">${esc(when + " · " + stops)}</span></div>` +
      `<strong class="price-val">${esc(t.from + " " + money(r.price))}</strong><a class="price-go" href="${esc(href)}">${esc(t.go)}</a></li>`
  }).join("")
  const summary = fill(t.summary, { m: date(bestRow.month, { month: "long", year: "numeric" }), p: money(best), max: money(max), n: String(MONTHS) }) +
    " " + fill(t.updated, { d: date(new Date().toISOString().slice(0, 10), { day: "numeric", month: "long", year: "numeric" }) })
  return html
    .replace(/(<title>)([^<]*?)( \| Escale)?(<\/title>)/, (_m, a, s, b, c) => a + s + ` · ${label}` + (b || "") + c)
    .replace(/(<meta property="og:title" content=")([^"]*)(")/, (_m, a, s, b) => a + s + ` · ${label}` + b)
    .replace(/(<meta name="description" content=")([^"]*)(")/, (_m, a, s, b) => a + esc(lead) + " — " + s + b)
    .replace(/(<meta property="og:description" content=")([^"]*)(")/, (_m, a, s, b) => a + esc(lead) + " — " + s + b)
    .replace(/<p class="hero-price" id="hero-price" hidden><\/p>/, `<p class="hero-price" id="hero-price">${esc(t.hero)} <strong>${esc(money(best))}</strong></p>`)
    .replace(/(<section id="route-prices" data-from="[A-Z]{3}" data-to="[A-Z]{3}") hidden>/, `$1 data-ssr="1">`)
    .replace(/<ul class="price-list"><\/ul>/, `<p class="price-summary">${esc(summary)}</p><ul class="price-list">${items}</ul>`)
}

export const onRequest = async (ctx: Ctx) => {
  const { request, env } = ctx
  const path = new URL(request.url).pathname
  if (request.method !== "GET" || !PAGES.test(path) || !env.TRAVELPAYOUTS_TOKEN) return ctx.next()
  const response = await ctx.next()
  try {
    if (!response.ok || !(response.headers.get("content-type") || "").includes("text/html")) return response
    const html = await response.text()
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    const route = html.match(/id="route-prices" data-from="([A-Z]{3})" data-to="([A-Z]{3})"/)
    if (!route) return new Response(html, { status: response.status, headers })
    const job = routeMonths(ctx, route[1], route[2]).catch(() => null)
    const rows = await Promise.race([job, new Promise<undefined>((ok) => setTimeout(() => ok(undefined), WAIT_MS))])
    if (rows === undefined) ctx.waitUntil(job) // trop lent : la page part sans les prix, le cache se remplit pour la visite suivante
    if (!rows || !rows.length) return new Response(html, { status: response.status, headers })
    return new Response(render(html, route[1], route[2], rows), { status: response.status, headers })
  } catch {
    return response
  }
}
