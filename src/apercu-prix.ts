import { Ctx, esc, pricesForDates } from "./_lib/common"
import * as paye from "./paye"
import * as partage from "./partage"
import * as autresVilles from "./autres-villes"
import { readPaid } from "./api/paye"
// Pages trajets : les prix réels sont écrits directement dans la page, pour les visiteurs comme pour Google
// (avant, ils n'apparaissaient qu'après le chargement, via route-prices.js, et les moteurs de recherche ne les voyaient pas).
// - titre, description et aperçu des liens partagés : « … · dès 389 € »
// - en haut de page : « Aller-retour repéré dès 389 € »
// - section « Prix repérés récemment » : le prix le plus bas pour chacun des 6 prochains mois, avec une phrase de résumé
// Les prix (Travelpayouts) sont gardés 6 heures dans le cache de Cloudflare. Sans réponse rapide, la page part telle quelle
// et route-prices.js prend le relais dans le navigateur. Les chemins concernés sont listés dans wrangler.jsonc (run_worker_first).
const PAGES = /^\/(vol-|vols-pour-|en\/flights-|es\/vuelos-|pt\/voos-|ar\/flights-|it\/voli-|de\/fluege-|nl\/vluchten-)/
const MONTHS = 6
const WAIT_MS = 1200
const CACHE_S = 6 * 3600

export type Month = { month: string; price: number; dep: string; ret: string; transfers: number }

// Historique du prix le plus bas (grands trajets seulement, pour limiter les écritures KV) :
// une valeur par jour au plus, enregistrée quand les prix sont rafraîchis (cache de 6 heures), 120 jours gardés.
// Il sert à dire si le prix du moment est bas, normal ou élevé par rapport aux semaines précédentes.
const TRACKED = new Set(("CDG-DSS CDG-BKO CDG-ABJ CDG-CKY CDG-DLA CDG-NSI CDG-LFW CDG-COO CDG-OUA CDG-FIH CDG-LBV CDG-NKC ORY-CMN CDG-RAK " +
  "CDG-ALG CDG-TUN CDG-YUL CDG-DXB CDG-IST CDG-RUN BRU-FIH BRU-DSS BRU-ABJ BRU-DLA MRS-ALG MRS-TUN MRS-DSS LYS-CMN LYS-DSS LYS-ALG " +
  "GVA-DSS GVA-CMN CDG-PTP CDG-FDF CDG-ORN CDG-DJE CDG-BZV CDG-NDJ CDG-TNR CDG-JED " +
  "LYS-TUN LYS-DJE LYS-AGA LYS-RAK LYS-OUD LYS-FEZ LYS-ORN LYS-CZL LYS-IST LYS-DXB LYS-ABJ LYS-BKO MRS-ORN MRS-CZL MRS-CMN MRS-RAK MRS-DJE MRS-IST MRS-BKO MRS-ABJ " +
  "LIL-ALG LIL-ORN LIL-TUN LIL-OUD GVA-ABJ CDG-MPM BOD-RAK MXP-ABJ MXP-DSS FCO-DSS MXP-CMN MXP-LOS MXP-ACC " +
  "CDG-NIM CDG-NDJ CDG-OXB CDG-BJL CDG-RAI CDG-ACC CDG-LOS CDG-ADD CDG-NBO CDG-JNB CDG-KGL CDG-CAI CDG-TNR CDG-LAD CDG-MPM CDG-DAR CDG-MRU MXP-TUN MXP-CAI MXP-ADD MXP-ALG FCO-CMN FCO-TUN FCO-CAI FCO-LOS FCO-ADD FCO-ALG FCO-ACC FCO-ABJ " +
  "LHR-LOS LHR-ACC LHR-ABV LHR-NBO LHR-JNB LHR-ADD LHR-CAI LHR-CMN LHR-RAK LHR-ALG LHR-DSS LHR-ABJ LHR-FIH LHR-TUN").split(" "))
const HIST_DAYS = 400, HIST_MIN = 7, HIST_WINDOW = 60 // 400 jours : permet « le prix il y a un an »
export type Point = [string, number, string?] // [date, prix le plus bas des 6 prochains mois]

export async function readHistory(ctx: Ctx, from: string, to: string): Promise<Point[]> {
  if (!ctx.env.ESCALE || !TRACKED.has(`${from}-${to}`)) return []
  try { return ((await ctx.env.ESCALE.get(`hist:${from}-${to}`, "json")) as Point[]) || [] } catch { return [] }
}

// Prix par mois (mois:FROM-TO) : gardés une fois par jour pour les trajets suivis, pour les pages « bons plans par mois »
// (src/bonsplans.ts). Écrit au relevé de la nuit, ou à la première visite du jour d'une page trajet.
export type Saved = { d: string; rows: Month[] }
export async function readMonths(env: any, from: string, to: string): Promise<Saved | null> {
  if (!env?.ESCALE || !TRACKED.has(`${from}-${to}`)) return null
  try { return (await env.ESCALE.get(`mois:${from}-${to}`, "json")) as Saved | null } catch { return null }
}
export async function saveMonths(env: any, from: string, to: string, rows: Month[], check = true) {
  if (!env?.ESCALE || !rows.length || !TRACKED.has(`${from}-${to}`)) return
  const today = new Date().toISOString().slice(0, 10)
  if (check) { const cur = await readMonths(env, from, to); if (cur && cur.d === today) return }
  await env.ESCALE.put(`mois:${from}-${to}`, JSON.stringify({ d: today, rows }), { expirationTtl: 14 * 86400 })
}

// Le mois le moins cher est gardé avec le prix : le baromètre lit tout dans KV, sans ouvrir le cache de chaque trajet
async function recordHistory(ctx: Ctx, from: string, to: string, price: number, month: string) {
  if (!ctx.env.ESCALE || !TRACKED.has(`${from}-${to}`)) return
  const today = new Date().toISOString().slice(0, 10)
  const hist = await readHistory(ctx, from, to)
  const last = hist[hist.length - 1]
  if (last && last[0] === today) { if (last[2]) return; last[2] = month } // relevé du jour déjà fait (on complète le mois s'il manquait)
  else hist.push([today, Math.round(price), month])
  await ctx.env.ESCALE.put(`hist:${from}-${to}`, JSON.stringify(hist.slice(-HIST_DAYS)))
}

// « Plus bas depuis 30 jours » : le prix du jour est inférieur ou égal à tous les prix relevés les 30 jours précédents (au moins 14 jours de relevés)
export function isLow30(hist: Point[], price: number) {
  const since = new Date(Date.now() - 30 * 864e5).toISOString().slice(0, 10), today = new Date().toISOString().slice(0, 10)
  const past = hist.filter(([d]) => d >= since && d < today).map(([, v]) => v)
  return past.length >= 14 && price <= Math.min(...past)
}
export const LOW30: Record<string, string> = { fr: "Prix le plus bas relevé depuis 30 jours", en: "Lowest price recorded in 30 days", es: "El precio más bajo registrado en 30 días", pt: "O preço mais baixo registado em 30 dias",
  ar: "أدنى سعر مسجّل منذ 30 يومًا", it: "Il prezzo più basso rilevato da 30 giorni", de: "Niedrigster erfasster Preis seit 30 Tagen", nl: "Laagste gemeten prijs in 30 dagen" }

// « Bas », « normal » ou « élevé » : prix du jour comparé à la médiane des 60 derniers jours (au moins 7 jours de données)
export function verdict(hist: Point[], price: number) {
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
  de: { loc: "de-DE", from: "ab", hero: "Hin- und Rückflug gefunden ab", direct: "Direktflug", one: "1 Stopp", many: " Stopps", best: "Am günstigsten", go: "Diese Daten ansehen",
    summary: "Günstigster Monat derzeit: {m}, ab {p} hin und zurück. In den nächsten {n} Monaten liegen die gefundenen Preise zwischen {p} und {max}.", updated: "Preise aktualisiert am {d}.",
    low: "Derzeit ein guter Preis", mid: "Durchschnittlicher Preis", high: "Derzeit eher teuer",
    lowTxt: "{p}, also {x} % günstiger als üblich (Medianpreis {avg} in den letzten {n} erfassten Tagen).",
    midTxt: "{p}, nah am üblichen Preis ({avg}, Median der letzten {n} erfassten Tage).",
    highTxt: "{p}, also {x} % teurer als üblich ({avg}, Median der letzten {n} erfassten Tage). Wenn du warten kannst, erstelle einen Preisalarm.",
    chart: "Niedrigster Preis nach Abflugmonat" },
  nl: { loc: "nl-NL", from: "vanaf", hero: "Retour gevonden vanaf", direct: "rechtstreeks", one: "1 overstap", many: " overstappen", best: "Goedkoopst", go: "Bekijk deze data",
    summary: "Goedkoopste maand op dit moment: {m}, vanaf {p} retour. In de komende {n} maanden liggen de gevonden prijzen tussen {p} en {max}.", updated: "Prijzen bijgewerkt op {d}.",
    low: "Nu een goede prijs", mid: "Gemiddelde prijs", high: "Nu eerder duur",
    lowTxt: "{p}, dus {x} % goedkoper dan normaal (mediaanprijs {avg} over de laatste {n} gemeten dagen).",
    midTxt: "{p}, dicht bij de normale prijs ({avg}, mediaan van de laatste {n} gemeten dagen).",
    highTxt: "{p}, dus {x} % duurder dan normaal ({avg}, mediaan van de laatste {n} gemeten dagen). Kun je wachten, stel dan een prijsalert in.",
    chart: "Laagste prijs per vertrekmaand" },
}

// « Le bon moment pour acheter » : conseil clair déduit des relevés (prix du jour vs médiane 60 jours, et tendance sur 7 jours).
// Jamais une promesse : les textes restent prudents et renvoient vers l'alerte prix quand il vaut mieux attendre.
type Advice = { buy: string; wait: string; hold: string; up: string; down: string; flat: string; hist: string; min: string; max: string }
const ADV: Record<string, Advice> = {
  fr: { buy: "Notre conseil : c’est un bon moment pour réserver.", wait: "Notre conseil : si vos dates sont souples, attendez et créez une alerte prix.", hold: "Notre conseil : pas d’urgence, mais pas de raison d’attendre non plus.",
    up: "Le prix a augmenté de {x} % en une semaine.", down: "Le prix a baissé de {x} % en une semaine.", flat: "Le prix est stable depuis une semaine.", hist: "Prix le plus bas relevé chaque jour, {n} derniers jours", min: "min.", max: "max." },
  en: { buy: "Our advice: this is a good time to book.", wait: "Our advice: if your dates are flexible, wait and set a price alert.", hold: "Our advice: no rush, but no reason to wait either.",
    up: "The price rose {x}% over the past week.", down: "The price fell {x}% over the past week.", flat: "The price has been stable for a week.", hist: "Lowest price recorded each day, last {n} days", min: "min", max: "max" },
  es: { buy: "Nuestro consejo: es un buen momento para reservar.", wait: "Nuestro consejo: si tus fechas son flexibles, espera y crea una alerta de precio.", hold: "Nuestro consejo: sin prisa, pero tampoco hay motivo para esperar.",
    up: "El precio subió un {x} % en una semana.", down: "El precio bajó un {x} % en una semana.", flat: "El precio está estable desde hace una semana.", hist: "Precio más bajo registrado cada día, últimos {n} días", min: "mín.", max: "máx." },
  pt: { buy: "O nosso conselho: é um bom momento para reservar.", wait: "O nosso conselho: se as datas forem flexíveis, espere e crie um alerta de preço.", hold: "O nosso conselho: sem pressa, mas também sem razão para esperar.",
    up: "O preço subiu {x} % numa semana.", down: "O preço desceu {x} % numa semana.", flat: "O preço está estável há uma semana.", hist: "Preço mais baixo registado cada dia, últimos {n} dias", min: "mín.", max: "máx." },
  ar: { buy: "نصيحتنا: هذا وقت جيد للحجز.", wait: "نصيحتنا: إن كانت مواعيدك مرنة، انتظر وأنشئ تنبيهًا بالسعر.", hold: "نصيحتنا: لا عجلة، ولا سبب للانتظار أيضًا.",
    up: "ارتفع السعر بنسبة {x}٪ خلال أسبوع.", down: "انخفض السعر بنسبة {x}٪ خلال أسبوع.", flat: "السعر مستقر منذ أسبوع.", hist: "أدنى سعر مسجل كل يوم، آخر {n} يومًا", min: "الأدنى", max: "الأعلى" },
  it: { buy: "Il nostro consiglio: è un buon momento per prenotare.", wait: "Il nostro consiglio: se le date sono flessibili, aspetta e crea un avviso prezzo.", hold: "Il nostro consiglio: nessuna fretta, ma nemmeno motivo di aspettare.",
    up: "Il prezzo è salito del {x} % in una settimana.", down: "Il prezzo è sceso del {x} % in una settimana.", flat: "Il prezzo è stabile da una settimana.", hist: "Prezzo più basso rilevato ogni giorno, ultimi {n} giorni", min: "min.", max: "max." },
  de: { buy: "Unser Tipp: ein guter Zeitpunkt zum Buchen.", wait: "Unser Tipp: Bei flexiblen Daten lieber warten und einen Preisalarm anlegen.", hold: "Unser Tipp: keine Eile, aber auch kein Grund zu warten.",
    up: "Der Preis ist in einer Woche um {x} % gestiegen.", down: "Der Preis ist in einer Woche um {x} % gesunken.", flat: "Der Preis ist seit einer Woche stabil.", hist: "Täglich erfasster Tiefstpreis, letzte {n} Tage", min: "Min.", max: "Max." },
  nl: { buy: "Ons advies: een goed moment om te boeken.", wait: "Ons advies: zijn je data flexibel, wacht dan en stel een prijsalert in.", hold: "Ons advies: geen haast, maar ook geen reden om te wachten.",
    up: "De prijs steeg {x} % in een week.", down: "De prijs daalde {x} % in een week.", flat: "De prijs is al een week stabiel.", hist: "Laagste prijs per dag gemeten, laatste {n} dagen", min: "min.", max: "max." },
}
const SPARK_DAYS = 30
// Variation du prix du jour par rapport au relevé d'il y a environ 7 jours (à ± 2 jours près)
function weekChange(hist: Point[], price: number): number | null {
  const target = Date.now() - 7 * 864e5
  let best: Point | null = null
  for (const p of hist) { const gap = Math.abs(Date.parse(p[0]) - target) / 864e5; if (gap <= 2 && (!best || gap < Math.abs(Date.parse(best[0]) - target) / 864e5)) best = p }
  return best ? Math.round((price / best[1] - 1) * 100) : null
}
// Courbe des 30 derniers relevés (SVG écrit dans la page, sans script) : la tendance se voit d'un coup d'œil
function sparkline(hist: Point[], a: Advice, money: (n: number) => string): string {
  const since = new Date(Date.now() - SPARK_DAYS * 864e5).toISOString().slice(0, 10)
  const pts = hist.filter(([d]) => d >= since)
  if (pts.length < 5) return ""
  const vals = pts.map((p) => p[1]), lo = Math.min(...vals), hi = Math.max(...vals)
  const W = 320, H = 72, PAD = 6
  const x = (i: number) => PAD + (i * (W - 2 * PAD)) / Math.max(1, pts.length - 1)
  const y = (v: number) => hi === lo ? H / 2 : PAD + ((hi - v) * (H - 2 * PAD - 16)) / (hi - lo) // le minimum reste à 16 px du bord : la courbe se voit même quand elle est plate
  const line = pts.map((p, i) => `${x(i).toFixed(1)},${y(p[1]).toFixed(1)}`).join(" ")
  const area = `${PAD},${H - PAD} ${line} ${x(pts.length - 1).toFixed(1)},${H - PAD}`
  const last = pts[pts.length - 1]
  const style = `<style>.ph-wrap{margin:14px 0 4px}.ph-wrap figcaption{font-size:.85rem;color:var(--muted,#5b6474);margin-bottom:6px}.ph-svg{display:block;width:100%;height:auto;color:var(--teal-d,#0b8577)}.ph-legend{display:flex;justify-content:space-between;font-size:.8rem;color:var(--muted,#5b6474);margin-top:2px}</style>`
  return style + `<figure class="ph-wrap"><figcaption>${esc(a.hist.replace("{n}", String(SPARK_DAYS)))}</figcaption>` +
    `<svg class="ph-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(a.hist.replace("{n}", String(SPARK_DAYS)))}">` +
    `<polygon points="${area}" fill="currentColor" opacity=".12"/><polyline points="${line}" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>` +
    `<circle cx="${x(pts.length - 1).toFixed(1)}" cy="${y(last[1]).toFixed(1)}" r="3.5" fill="currentColor"/></svg>` +
    `<div class="ph-legend"><span>${esc(pts[0][0].slice(8, 10) + "/" + pts[0][0].slice(5, 7))} · ${esc(a.min)} ${esc(money(lo))}</span><span>${esc(a.max)} ${esc(money(hi))} · ${esc(last[0].slice(8, 10) + "/" + last[0].slice(5, 7))}</span></div></figure>`
}
// Conseil : « bon moment pour réserver » si le prix est bas ou s'il monte, « attendez » s'il est élevé ou s'il baisse nettement
function advice(level: "low" | "mid" | "high", wk: number | null, a: Advice): string {
  const trend = wk === null ? "" : wk >= 5 ? a.up.replace("{x}", String(wk)) : wk <= -5 ? a.down.replace("{x}", String(Math.abs(wk))) : a.flat
  const tip = level === "low" ? a.buy : level === "high" ? a.wait : wk !== null && wk >= 5 ? a.buy : wk !== null && wk <= -5 ? a.wait : a.hold
  return `<p class="price-advice"><strong>${esc(tip)}</strong>${trend ? " " + esc(trend) : ""}</p>`
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
  if (cache) ctx.waitUntil(cache.put(key, new Response(JSON.stringify(out), { headers: { "Content-Type": "application/json", "Cache-Control": `public, max-age=${CACHE_S}`, "X-At": String(Date.now()) } })))
  if (out.length) { const b = out.reduce((a, c) => (c.price < a.price ? c : a)); ctx.waitUntil(recordHistory(ctx, from, to, b.price, b.month).catch(() => {})) }
  if (out.length) ctx.waitUntil(saveMonths(ctx.env, from, to, out, false).catch(() => {}))
  return out
}

// Âge des prix (heure de mise en cache, en-tête X-At) : « vérifiés il y a 2 h »
export async function priceAge(from: string, to: string): Promise<number | null> {
  const cache = (globalThis as any).caches?.default
  if (!cache) return null
  const hit = await cache.match(cacheKey(from, to)).catch(() => null)
  const at = hit ? Number(hit.headers.get("X-At")) : NaN
  return Number.isFinite(at) && at > 0 ? Math.max(0, Date.now() - at) : null
}
const AGO: Record<string, [string, string, string]> = { fr: ["Prix vérifiés il y a moins d’une heure.", "Prix vérifiés il y a {h} h.", "Prix vérifiés il y a {d} j."], en: ["Prices checked less than an hour ago.", "Prices checked {h} h ago.", "Prices checked {d} d ago."],
  es: ["Precios comprobados hace menos de una hora.", "Precios comprobados hace {h} h.", "Precios comprobados hace {d} d."], pt: ["Preços verificados há menos de uma hora.", "Preços verificados há {h} h.", "Preços verificados há {d} d."],
  ar: ["تم التحقق من الأسعار منذ أقل من ساعة.", "تم التحقق من الأسعار منذ {h} س.", "تم التحقق من الأسعار منذ {d} ي."], it: ["Prezzi verificati meno di un’ora fa.", "Prezzi verificati {h} h fa.", "Prezzi verificati {d} g fa."],
  de: ["Preise vor weniger als einer Stunde geprüft.", "Preise vor {h} Std. geprüft.", "Preise vor {d} T. geprüft."], nl: ["Prijzen minder dan een uur geleden gecontroleerd.", "Prijzen {h} u geleden gecontroleerd.", "Prijzen {d} d geleden gecontroleerd."] }
function agoText(lang: string, ms: number | null) {
  if (ms === null) return ""
  const a = AGO[lang] || AGO.fr, h = Math.floor(ms / 36e5)
  return h < 1 ? a[0] : h < 48 ? a[1].replace("{h}", String(h)) : a[2].replace("{d}", String(Math.floor(h / 24)))
}

function render(html: string, from: string, to: string, rows: Month[], hist: Point[] = [], ageMs: number | null = null) {
  const lang = (html.match(/<html lang="([a-z]{2})"/) || [])[1] || "fr"
  const t = L[lang] || L.fr
  const money = (n: number) => { try { return new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n) } catch { return Math.round(n) + " €" } }
  const date = (iso: string, o: Intl.DateTimeFormatOptions) => { const [y, m, d] = iso.split("-").map(Number); try { return new Date(Date.UTC(y, m - 1, d || 1)).toLocaleDateString(t.loc, { ...o, timeZone: "UTC" }) } catch { return iso } }
  const fill = (s: string, o: Record<string, string>) => s.replace(/\{(\w+)\}/g, (_, k) => o[k])
  const prices = rows.map((r) => r.price), best = Math.min(...prices), max = Math.max(...prices)
  const bestRow = rows.find((r) => r.price === best)!
  const label = `${t.from} ${money(best)}`
  html = html.replace(partage.PRICE_SLOT, `data-prix="${esc(money(best))}" data-n="${Math.round(best)}" data-r="${from}-${to}"`)
  const lead = label.charAt(0).toUpperCase() + label.slice(1)
  const app = lang === "fr" ? "" : "&lang=" + (lang === "nl" ? "en" : lang)
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
  const a = ADV[lang] || ADV.fr
  const badge = v ? `<div class="price-verdict pv-${v.level}"><strong>${esc(t[v.level])}</strong><span>${esc(fill(t[(v.level + "Txt") as "lowTxt"], { p: money(best), x: String(v.diff), avg: money(v.median), n: String(v.days) }))}</span>${advice(v.level, weekChange(hist, best), a)}</div>` : ""
  const spark = v ? sparkline(hist, a, money) : ""
  const summary = fill(t.summary, { m: date(bestRow.month, { month: "long", year: "numeric" }), p: money(best), max: money(max), n: String(MONTHS) }) +
    " " + fill(t.updated, { d: date(new Date().toISOString().slice(0, 10), { day: "numeric", month: "long", year: "numeric" }) })
  const ago = agoText(lang, ageMs)
  const low30 = isLow30(hist, best) ? `<p class="price-low30" style="margin:0 0 10px;font-weight:700;color:#18794e">🏆 ${esc(LOW30[lang] || LOW30.fr)}</p>` : ""
  const badge2 = ago ? `<p class="price-age" style="margin:-4px 0 10px;font-size:.85rem;color:var(--muted,#5b6474)">✅ ${esc(ago)}</p>` : ""
  return html
    .replace(/(<title>)([^<]*?)( \| Escale)?(<\/title>)/, (_m, a, s, b, c) => a + s + ` · ${label}` + (b || "") + c)
    // Aperçu du lien partagé (WhatsApp, Facebook) : prix du jour et verdict (« Bon prix en ce moment »…)
    .replace(/(<meta property="og:title" content=")([^"]*)(")/, (_m, a, s, b) => a + s + ` · ${label}` + (v ? ` · ${esc(t[v.level])}` : "") + b)
    .replace(/(<meta name="description" content=")([^"]*)(")/, (_m, a, s, b) => a + esc(lead) + " — " + s + b)
    .replace(/(<meta property="og:description" content=")([^"]*)(")/, (_m, a, s, b) => a + esc(lead) + " — " + s + b)
    .replace(/<p class="hero-price" id="hero-price" hidden><\/p>/, `<p class="hero-price" id="hero-price">${esc(t.hero)} <strong>${esc(money(best))}</strong></p>`)
    .replace(/(<section id="route-prices" data-from="[A-Z]{3}" data-to="[A-Z]{3}") hidden>/, `$1 data-ssr="1">`)
    .replace(/<ul class="price-list"><\/ul>/, `${badge2}${low30}${badge}${spark}<p class="price-summary">${esc(summary)}</p>${bars}<ul class="price-list">${items}</ul>`)
}

// Pages « destination » (tous les vols vers une ville) : chaque ligne reçoit le prix déjà connu du trajet (cache des pages trajets).
// Les trajets pas encore en cache sont préparés en arrière-plan (3 par visite) ; hub.js complète dans le navigateur.
const t2 = (lang: string) => ({ fr: "dès", en: "from", es: "desde", pt: "desde", ar: "من", it: "da", de: "ab", nl: "vanaf" } as Record<string, string>)[lang] || "dès"
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
  // Prix le plus bas de la page dans le titre (onglet, Google, aperçu des liens partagés) : « Cheap flights to Tunis from €74 – … »
  const all = found.flat().filter(Boolean) as Month[]
  if (all.length) {
    const best = money(Math.min(...all.map((r) => r.price)))
    const add = (t: string) => lang === "en" && / – /.test(t) ? t.replace(" – ", ` from ${best} – `) : t.replace(/ \| Escale$/, "") + ` · ${t2(lang)} ${best}` + (/ \| Escale$/.test(t) ? " | Escale" : "")
    html = html.replace(/<title>([^<]*)<\/title>/, (_m, t) => `<title>${add(t)}</title>`)
      .replace(/(<meta property="og:title" content=")([^"]*)(")/, (_m, a, t, c) => a + add(t) + c)
  }
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
    let html = await response.text()
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    const route = html.match(/id="route-prices" data-from="([A-Z]{3})" data-to="([A-Z]{3})"/)
    if (!route) return new Response(await fillHub(ctx, html), { status: response.status, headers })
    // « Ce que les voyageurs ont vraiment payé » (src/paye.ts), juste après la section des prix
    const lang = (html.match(/<html lang="([a-z]{2})"/) || [])[1] || "fr"
    const paid = paye.render(lang, route[1], route[2], paye.stats(await readPaid(env, route[1], route[2])))
    const at = html.indexOf("</section>", html.indexOf('id="route-prices"'))
    // puis « Envoyer ce prix à la famille » et l'inscription aux bons plans du lundi (src/partage.ts)
    // « Depuis une autre ville » (src/autres-villes.ts) : jamais plus de 300 ms d'attente, sinon la page part sans ce bloc
    const av = await Promise.race([autresVilles.render(ctx, lang, route[1], route[2]).catch(() => ""), new Promise<string>((ok) => setTimeout(() => ok(""), 300))])
    if (at > 0) html = html.slice(0, at + 10) + paid + av + partage.render(lang, route[1], route[2]) + html.slice(at + 10)
    const job = routeMonths(ctx, route[1], route[2]).catch(() => null)
    const rows = await Promise.race([job, new Promise<undefined>((ok) => setTimeout(() => ok(undefined), WAIT_MS))])
    if (rows === undefined) ctx.waitUntil(job) // trop lent : la page part sans les prix, le cache se remplit pour la visite suivante
    if (!rows || !rows.length) return new Response(html, { status: response.status, headers })
    // Prix par mois du jour pour les pages « bons plans » (une écriture par trajet et par jour au plus)
    ctx.waitUntil(saveMonths(env, route[1], route[2], rows).catch(() => {}))
    const [hist, age] = await Promise.all([readHistory(ctx, route[1], route[2]), priceAge(route[1], route[2])])
    return new Response(render(html, route[1], route[2], rows, hist, age), { status: response.status, headers })
  } catch {
    return response
  }
}
