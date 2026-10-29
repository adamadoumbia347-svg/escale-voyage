import { Ctx, esc, pricesForDates } from "./_lib/common"
// Pages trajets : les prix réels sont écrits directement dans la page, pour les visiteurs comme pour Google
// (avant, ils n'apparaissaient qu'après le chargement, via route-prices.js, et les moteurs de recherche ne les voyaient pas).
// - titre, description et aperçu des liens partagés : « … · dès 389 € »
// - en haut de page : « Aller-retour repéré dès 389 € »
// - section « Prix repérés récemment » : le prix le plus bas pour chacun des 6 prochains mois, avec une phrase de résumé
// Les prix (Travelpayouts) sont gardés 6 heures dans le cache de Cloudflare. Sans réponse rapide, la page part telle quelle
// et route-prices.js prend le relais dans le navigateur. Les chemins concernés sont listés dans wrangler.jsonc (run_worker_first).
const PAGES = /^\/(vol-|vols-pour-|en\/flights-|es\/vuelos-|pt\/voos-|ar\/flights-|it\/voli-)/
const MONTHS = 6
const WAIT_MS = 2500
const CACHE_S = 6 * 3600

export type Month = { month: string; price: number; dep: string; ret: string; transfers: number }

// Historique du prix le plus bas (grands trajets seulement, pour limiter les écritures KV) :
// une valeur par jour au plus, enregistrée quand les prix sont rafraîchis (cache de 6 heures), 120 jours gardés.
// Il sert à dire si le prix du moment est bas, normal ou élevé par rapport aux semaines précédentes.
const TRACKED = new Set(("CDG-DSS CDG-BKO CDG-ABJ CDG-CKY CDG-DLA CDG-NSI CDG-LFW CDG-COO CDG-OUA CDG-FIH CDG-LBV CDG-NKC ORY-CMN CDG-RAK " +
  "CDG-ALG CDG-TUN CDG-YUL CDG-DXB CDG-IST CDG-RUN BRU-FIH BRU-DSS BRU-ABJ BRU-DLA MRS-ALG MRS-TUN MRS-DSS LYS-CMN LYS-DSS LYS-ALG " +
  "GVA-DSS GVA-CMN CDG-PTP CDG-FDF CDG-ORN CDG-DJE CDG-BZV CDG-NDJ CDG-TNR CDG-JED " +
  "LYS-TUN LYS-DJE LYS-AGA LYS-RAK LYS-OUD LYS-FEZ LYS-ORN LYS-CZL LYS-IST LYS-DXB LYS-ABJ LYS-BKO MRS-ORN MRS-CZL MRS-CMN MRS-RAK MRS-DJE MRS-IST MRS-BKO MRS-ABJ " +
  "LIL-ALG LIL-ORN LIL-TUN LIL-OUD GVA-ABJ CDG-MPM BOD-RAK").split(" "))
const HIST_DAYS = 120, HIST_MIN = 7, HIST_WINDOW = 60
export type Point = [string, number] // [date, prix le plus bas des 6 prochains mois]

export async function readHistory(ctx: Ctx, from: string, to: string): Promise<Point[]> {
  if (!ctx.env.ESCALE || !TRACKED.has(`${from}-${to}`)) return []
  try { return ((await ctx.env.ESCALE.get(`hist:${from}-${to}`, "json")) as Point[]) || [] } catch { return [] }
}

async function recordHistory(ctx: Ctx, from: string, to: string, price: number) {
  if (!ctx.env.ESCALE || !TRACKED.has(`${from}-${to}`)) return
  const today = new Date().toISOString().slice(0, 10)
  const hist = await readHistory(ctx, from, to)
  if (hist.length && hist[hist.length - 1][0] === today) return
  hist.push([today, Math.round(price)])
  await ctx.env.ESCALE.put(`hist:${from}-${to}`, JSON.stringify(hist.slice(-HIST_DAYS)))
}

// « Bas », « normal » ou « élevé » : prix du jour comparé à la médiane des 60 derniers jours (au moins 7 jours de données)
function verdict(hist: Point[], price: number) {
  const since = new Date(Date.now() - HIST_WINDOW * 864e5).toISOString().slice(0, 10)
  const today = new Date().toISOString().slice(0, 10)
  const past = hist.filter(([d]) => d >= since && d < today).map(([, p]) => p).sort((a, b) => a - b)
  if (past.length < HIST_MIN) return null
  const median = past[Math.floor(past.length / 2)]
  const diff = Math.round((price / median - 1) * 100)
  return { level: (diff <= -8 ? "low" : diff >= 8 ? "high" : "mid") as "low" | "mid" | "high", diff: Math.abs(diff), median, days: past.length }
}

const L: Record<string, { loc: string; from: string; hero: string; direct: string; one: string; many: string; best: string; go: string
  summary: string; updated: string; low: string; mid: string; high: string; lowTxt: string; midTxt: string; highTxt: string; chart: string }> = {
  fr: { loc: "fr-FR", from: "dès", hero: "Aller-retour repéré dès", direct: "vol direct", one: "1 escale", many: " escales", best: "Le moins cher", go: "Voir ces dates",
    summary: "Mois le moins cher en ce moment : {m}, dès {p} l’aller-retour. Sur les {n} prochains mois, les prix repérés vont de {p} à {max}.", updated: "Prix mis à jour le {d}.",
    low: "Bon prix en ce moment", mid: "Prix dans la moyenne", high: "Prix plutôt élevé en ce moment",
    lowTxt: "{p}, soit {x} % de moins que d’habitude (prix médian de {avg} sur les {n} derniers jours relevés).",
    midTxt: "{p}, proche du prix habituel ({avg}, médiane des {n} derniers jours relevés).",
    highTxt: "{p}, soit {x} % de plus que d’habitude ({avg}, médiane des {n} derniers jours relevés). Si vous pouvez attendre, créez une alerte prix.",
    chart: "Prix le plus bas par mois de départ" },
  en: { loc: "en-GB", from: "from", hero: "Round trip found from", direct: "direct", one: "1 stop", many: " stops", best: "Cheapest", go: "See these dates",
    summary: "Cheapest month right now: {m}, from {p} return. Over the next {n} months, prices found range from {p} to {max}.", updated: "Prices updated on {d}.",
    low: "Good price right now", mid: "Typical price", high: "Price is on the high side",
    lowTxt: "{p}, {x}% below usual (median price {avg} over the last {n} days tracked).",
    midTxt: "{p}, close to the usual price ({avg}, median over the last {n} days tracked).",
    highTxt: "{p}, {x}% above usual ({avg}, median over the last {n} days tracked). If you can wait, set a price alert.",
    chart: "Lowest price by departure month" },
  es: { loc: "es-ES", from: "desde", hero: "Ida y vuelta desde", direct: "vuelo directo", one: "1 escala", many: " escalas", best: "El más barato", go: "Ver estas fechas",
    summary: "Mes más barato ahora mismo: {m}, desde {p} ida y vuelta. En los próximos {n} meses, los precios encontrados van de {p} a {max}.", updated: "Precios actualizados el {d}.",
    low: "Buen precio ahora mismo", mid: "Precio habitual", high: "Precio más bien alto ahora mismo",
    lowTxt: "{p}, un {x} % menos de lo habitual (precio mediano de {avg} en los últimos {n} días registrados).",
    midTxt: "{p}, cerca del precio habitual ({avg}, mediana de los últimos {n} días registrados).",
    highTxt: "{p}, un {x} % más de lo habitual ({avg}, mediana de los últimos {n} días registrados). Si puedes esperar, crea una alerta de precio.",
    chart: "Precio más bajo por mes de salida" },
  pt: { loc: "pt-PT", from: "desde", hero: "Ida e volta desde", direct: "voo direto", one: "1 escala", many: " escalas", best: "O mais barato", go: "Ver estas datas",
    summary: "Mês mais barato neste momento: {m}, desde {p} ida e volta. Nos próximos {n} meses, os preços encontrados vão de {p} a {max}.", updated: "Preços atualizados a {d}.",
    low: "Bom preço neste momento", mid: "Preço habitual", high: "Preço algo elevado neste momento",
    lowTxt: "{p}, {x} % abaixo do habitual (preço mediano de {avg} nos últimos {n} dias registados).",
    midTxt: "{p}, perto do preço habitual ({avg}, mediana dos últimos {n} dias registados).",
    highTxt: "{p}, {x} % acima do habitual ({avg}, mediana dos últimos {n} dias registados). Se puder esperar, crie um alerta de preço.",
    chart: "Preço mais baixo por mês de partida" },
  ar: { loc: "ar-u-nu-latn", from: "من", hero: "ذهاب وعودة ابتداءً من", direct: "رحلة مباشرة", one: "توقف واحد", many: " توقفات", best: "الأرخص", go: "اعرض هذه التواريخ",
    summary: "أرخص شهر حاليًا: {m}، من {p} ذهابًا وعودة. خلال الأشهر الـ{n} القادمة، تتراوح الأسعار بين {p} و{max}.", updated: "آخر تحديث للأسعار: {d}.",
    low: "سعر جيد حاليًا", mid: "سعر معتاد", high: "السعر مرتفع نسبيًا حاليًا",
    lowTxt: "{p}، أي أقل من المعتاد بنسبة {x}٪ (السعر الوسيط {avg} خلال آخر {n} يومًا مسجلًا).",
    midTxt: "{p}، قريب من السعر المعتاد ({avg}، الوسيط خلال آخر {n} يومًا مسجلًا).",
    highTxt: "{p}، أي أعلى من المعتاد بنسبة {x}٪ ({avg}، الوسيط خلال آخر {n} يومًا مسجلًا). إن استطعت الانتظار، أنشئ تنبيهًا بالسعر.",
    chart: "أدنى سعر حسب شهر المغادرة" },
  it: { loc: "it-IT", from: "da", hero: "Andata e ritorno trovato da", direct: "volo diretto", one: "1 scalo", many: " scali", best: "Il più economico", go: "Vedi queste date",
    summary: "Mese più economico al momento: {m}, da {p} andata e ritorno. Nei prossimi {n} mesi, i prezzi trovati vanno da {p} a {max}.", updated: "Prezzi aggiornati il {d}.",
    low: "Buon prezzo al momento", mid: "Prezzo nella media", high: "Prezzo piuttosto alto al momento",
    lowTxt: "{p}, cioè il {x} % in meno del solito (prezzo mediano di {avg} negli ultimi {n} giorni rilevati).",
    midTxt: "{p}, vicino al prezzo abituale ({avg}, mediana degli ultimi {n} giorni rilevati).",
    highTxt: "{p}, cioè il {x} % in più del solito ({avg}, mediana degli ultimi {n} giorni rilevati). Se puoi aspettare, crea un avviso prezzo.",
    chart: "Prezzo più basso per mese di partenza" },
}

// Prix le plus bas par mois de départ (6 prochains mois), depuis le cache Cloudflare ou Travelpayouts.
// null = service indisponible (rien n'est gardé en cache) ; [] = aucun prix connu pour ce trajet.
export const cacheKey = (from: string, to: string) => new Request(`https://escale.live/__prix-trajet/${from}-${to}`)

export async function routeMonths(ctx: Ctx, from: string, to: string): Promise<Month[] | null> {
  const cache = (globalThis as any).caches?.default
  const key = cacheKey(from, to)
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
  if (out.length) ctx.waitUntil(recordHistory(ctx, from, to, Math.min(...out.map((r) => r.price))).catch(() => {}))
  return out
}

function render(html: string, from: string, to: string, rows: Month[], hist: Point[] = []) {
  const lang = (html.match(/<html lang="([a-z]{2})"/) || [])[1] || "fr"
  const t = L[lang] || L.fr
  const money = (n: number) => { try { return new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n) } catch { return Math.round(n) + " €" } }
  const date = (iso: string, o: Intl.DateTimeFormatOptions) => { const [y, m, d] = iso.split("-").map(Number); try { return new Date(Date.UTC(y, m - 1, d || 1)).toLocaleDateString(t.loc, { ...o, timeZone: "UTC" }) } catch { return iso } }
  const fill = (s: string, o: Record<string, string>) => s.replace(/\{(\w+)\}/g, (_, k) => o[k])
  const prices = rows.map((r) => r.price), best = Math.min(...prices), max = Math.max(...prices)
  const bestRow = rows.find((r) => r.price === best)!
  const label = `${t.from} ${money(best)}`
  const lead = label.charAt(0).toUpperCase() + label.slice(1)
  const app = lang === "fr" ? "" : "&lang=" + (lang === "it" ? "en" : lang)
  const items = rows.map((r) => {
    const stops = r.transfers === 0 ? t.direct : r.transfers === 1 ? t.one : r.transfers + t.many
    const when = date(r.dep, { day: "numeric", month: "short" }) + (r.ret ? " → " + date(r.ret, { day: "numeric", month: "short" }) : "")
    const href = `/?type=vols&from=${from}&to=${to}&dep=${r.dep}` + (r.ret ? `&ret=${r.ret}` : "") + app
    return `<li class="price-row"><div><span class="price-month">${esc(date(r.month, { month: "long", year: "numeric" }))}` +
      (r.price === best ? ` <span class="pill-best">${esc(t.best)}</span>` : "") + `</span>` +
      `<span class="price-meta">${esc(when + " · " + stops)}</span></div>` +
      `<strong class="price-val">${esc(t.from + " " + money(r.price))}</strong><a class="price-go" href="${esc(href)}">${esc(t.go)}</a></li>`
  }).join("")
  // Mini-graphique : une barre par mois, verte si nettement sous la médiane des mois, rouge si nettement au-dessus
  const sorted = [...prices].sort((a, b) => a - b), mMed = sorted[Math.floor(sorted.length / 2)]
  const bars = rows.length > 1 ? `<figure class="price-chart" aria-hidden="true"><figcaption>${esc(t.chart)}</figcaption><div class="pc-bars">` + rows.map((r) => {
    const cls = r.price <= mMed * 0.92 ? "pc-low" : r.price >= mMed * 1.08 ? "pc-high" : "pc-mid"
    const h = max > best ? Math.round(30 + 70 * (r.price - best) / (max - best)) : 60 // hauteur relative : l'écart entre les mois se voit mieux
    return `<div class="pc-col"><span class="pc-val">${esc(money(r.price))}</span><span class="pc-bar ${cls}" style="height:${h}%"></span><span class="pc-m">${esc(date(r.month, { month: "short" }))}</span></div>`
  }).join("") + `</div></figure>` : ""
  const v = verdict(hist, best)
  const badge = v ? `<div class="price-verdict pv-${v.level}"><strong>${esc(t[v.level])}</strong><span>${esc(fill(t[(v.level + "Txt") as "lowTxt"], { p: money(best), x: String(v.diff), avg: money(v.median), n: String(v.days) }))}</span></div>` : ""
  const summary = fill(t.summary, { m: date(bestRow.month, { month: "long", year: "numeric" }), p: money(best), max: money(max), n: String(MONTHS) }) +
    " " + fill(t.updated, { d: date(new Date().toISOString().slice(0, 10), { day: "numeric", month: "long", year: "numeric" }) })
  return html
    .replace(/(<title>)([^<]*?)( \| Escale)?(<\/title>)/, (_m, a, s, b, c) => a + s + ` · ${label}` + (b || "") + c)
    .replace(/(<meta property="og:title" content=")([^"]*)(")/, (_m, a, s, b) => a + s + ` · ${label}` + b)
    .replace(/(<meta name="description" content=")([^"]*)(")/, (_m, a, s, b) => a + esc(lead) + " — " + s + b)
    .replace(/(<meta property="og:description" content=")([^"]*)(")/, (_m, a, s, b) => a + esc(lead) + " — " + s + b)
    .replace(/<p class="hero-price" id="hero-price" hidden><\/p>/, `<p class="hero-price" id="hero-price">${esc(t.hero)} <strong>${esc(money(best))}</strong></p>`)
    .replace(/(<section id="route-prices" data-from="[A-Z]{3}" data-to="[A-Z]{3}") hidden>/, `$1 data-ssr="1">`)
    .replace(/<ul class="price-list"><\/ul>/, `${badge}<p class="price-summary">${esc(summary)}</p>${bars}<ul class="price-list">${items}</ul>`)
}

// Pages « destination » (tous les vols vers une ville) : chaque ligne reçoit le prix déjà connu du trajet (cache des pages trajets).
// Les trajets pas encore en cache sont préparés en arrière-plan (3 par visite) ; hub.js complète dans le navigateur.
async function fillHub(ctx: Ctx, html: string) {
  const cache = (globalThis as any).caches?.default
  const cells = [...html.matchAll(/<td class="hub-price" data-from="([A-Z]{3})" data-to="([A-Z]{3})" data-label="([^"]*)"><\/td>/g)]
  if (!cells.length || !cache) return html
  const lang = (html.match(/<html lang="([a-z]{2})"/) || [])[1] || "fr"
  const t = L[lang] || L.fr
  const money = (n: number) => { try { return new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n) } catch { return Math.round(n) + " €" } }
  const found = await Promise.all(cells.map(async (m) => { const hit = await cache.match(cacheKey(m[1], m[2])); return hit ? (await hit.json()) as Month[] : null }))
  const missing = cells.filter((_, i) => found[i] === null).slice(0, 3)
  if (missing.length) ctx.waitUntil(Promise.all(missing.map((m) => routeMonths(ctx, m[1], m[2]).catch(() => null))))
  let i = 0
  return html.replace(/<td class="hub-price" data-from="([A-Z]{3})" data-to="([A-Z]{3})" data-label="([^"]*)"><\/td>/g, (all, _f, _t, label) => {
    const rows = found[i++]
    if (!rows || !rows.length) return all
    return all.replace('"></td>', `" data-ssr="1">${label} <strong>${esc(money(Math.min(...rows.map((r) => r.price))))}</strong></td>`)
  })
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
    if (!route) return new Response(await fillHub(ctx, html), { status: response.status, headers })
    const job = routeMonths(ctx, route[1], route[2]).catch(() => null)
    const rows = await Promise.race([job, new Promise<undefined>((ok) => setTimeout(() => ok(undefined), WAIT_MS))])
    if (rows === undefined) ctx.waitUntil(job) // trop lent : la page part sans les prix, le cache se remplit pour la visite suivante
    if (!rows || !rows.length) return new Response(html, { status: response.status, headers })
    const hist = await readHistory(ctx, route[1], route[2])
    return new Response(render(html, route[1], route[2], rows, hist), { status: response.status, headers })
  } catch {
    return response
  }
}
