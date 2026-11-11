import { Ctx, esc, keysOf } from "./_lib/common"
import { Row, rows } from "./barometre"
import { shareBlock } from "./diffusion"
// Indice Escale des prix (/indice-prix/ en français, /en/price-index/ en anglais) : à partir des prix relevés chaque jour pour le
// baromètre (historique KV), la variation médiane sur 30 et 7 jours, par grande région, les plus fortes hausses et baisses,
// et une phrase prête à citer. Aucun chiffre inventé : sans assez de relevés, la page le dit. Écrit par le serveur, en cache une journée.

type Lang = "fr" | "en"
const T = {
  fr: {
    loc: "fr-FR", url: "https://escale.live/indice-prix/", short: "escale.live/indice-prix",
    regions: ["Afrique de l'Ouest", "Afrique centrale", "Maghreb et Égypte", "Afrique de l'Est, australe et océan Indien"],
    origins: ["Depuis la France et la Belgique", "Depuis Londres", "Depuis l'Italie"],
    days: (n: number) => `${n} jours`, wait: (d: string) => `Relevé du ${d} : pas encore assez de relevés pour calculer l'indice. Il s'affiche dès que les prix de chaque trajet ont au moins une semaine d'historique.`,
    up: (m: number) => `ont augmenté de ${m} %`, down: (m: number) => `ont baissé de ${m} %`, flat: (s: string) => `sont restés stables (${s})`,
    quote: (d: string, tr: string, span: string, n: number) => `Selon l'Indice Escale des prix du ${d}, les prix des billets d'avion entre l'Europe et l'Afrique ${tr} sur ${span} (médiane de ${n} grands trajets suivis chaque jour).`,
    hi: (l: string, s: string, p: string) => ` La plus forte hausse concerne ${l} (${s}, dès ${p} aller-retour).`, lo: (l: string, s: string, p: string) => ` La plus forte baisse concerne ${l} (${s}, dès ${p}).`,
    lead: (d: string) => `Relevé du ${d}`, big: (span: string) => `variation médiane des prix sur ${span}`,
    counts: (n: number, d: number, u: number, s: number) => `${n} trajets · ${d} en baisse · ${u} en hausse · ${s} stables`,
    source: "Source : Escale,", copy: "📋 Copier la phrase et la source", byRegion: "Par région d'arrivée", byOrigin: "Par pays de départ",
    th: (span: string) => [`Variation sur ${span}`, "Prix médian aller-retour", "Trajets"], ups: "Les plus fortes hausses", downs: "Les plus fortes baisses",
    cheap: "Les trajets les moins chers du moment", from: "dès",
  },
  en: {
    loc: "en-GB", url: "https://escale.live/en/price-index/", short: "escale.live/en/price-index",
    regions: ["West Africa", "Central Africa", "North Africa and Egypt", "East and Southern Africa, Indian Ocean"],
    origins: ["From France and Belgium", "From London", "From Italy"],
    days: (n: number) => `${n} days`, wait: (d: string) => `Data as of ${d}: not enough price records yet to compute the index. It appears as soon as each route has at least one week of price history.`,
    up: (m: number) => `rose by ${m}%`, down: (m: number) => `fell by ${m}%`, flat: (s: string) => `stayed stable (${s})`,
    quote: (d: string, tr: string, span: string, n: number) => `According to the Escale Price Index of ${d}, air fares between Europe and Africa ${tr} over ${span} (median of ${n} major routes tracked daily).`,
    hi: (l: string, s: string, p: string) => ` The biggest rise is on ${l} (${s}, from ${p} round trip).`, lo: (l: string, s: string, p: string) => ` The biggest drop is on ${l} (${s}, from ${p}).`,
    lead: (d: string) => `Data as of ${d}`, big: (span: string) => `median change in fares over ${span}`,
    counts: (n: number, d: number, u: number, s: number) => `${n} routes · ${d} down · ${u} up · ${s} stable`,
    source: "Source: Escale,", copy: "📋 Copy the sentence and the source", byRegion: "By arrival region", byOrigin: "By departure country",
    th: (span: string) => [`Change over ${span}`, "Median round-trip fare", "Routes"], ups: "Biggest rises", downs: "Biggest drops",
    cheap: "Cheapest routes right now", from: "from",
  },
}
const REGIONS: string[][] = [
  ["DSS", "BKO", "ABJ", "CKY", "LFW", "COO", "OUA", "NKC", "NIM", "OXB", "BJL", "RAI", "ACC", "LOS", "ABV"],
  ["DLA", "NSI", "FIH", "BZV", "LBV", "NDJ", "LAD"],
  ["ALG", "ORN", "CMN", "RAK", "TUN", "DJE", "CAI"],
  ["ADD", "NBO", "JNB", "KGL", "TNR", "MPM", "DAR", "MRU"],
]
const ORIG: string[][] = [["CDG", "ORY", "LYS", "MRS", "BRU"], ["LHR"], ["MXP", "FCO"]]
// Noms des villes en anglais (les libellés du baromètre sont en français)
const EN: Record<string, string> = { Genève: "Geneva", Francfort: "Frankfurt", Lisbonne: "Lisbon", Barcelone: "Barcelona", Montréal: "Montreal", Londres: "London", "Le Caire": "Cairo", "Addis-Abeba": "Addis Ababa", Alger: "Algiers", Bruxelles: "Brussels", Maurice: "Mauritius",
  "N’Djamena": "N'Djamena", Yaoundé: "Yaoundé", Lomé: "Lomé", Marrakech: "Marrakesh" }
export const label = (l: string, lang: Lang) => lang === "fr" ? l : l.split(" → ").map((x) => EN[x] || x).join(" → ")

// Indice par pays d'arrivée (/indice-prix/pays/cote-d-ivoire/, /en/price-index/country/ivory-coast/) : mêmes relevés, filtrés
// sur les aéroports du pays. Les médias d'un pays citent un chiffre qui parle de leur pays.
export const PAYS: { fr: string; en: string; nom: string; name: string; codes: string[] }[] = [
  { fr: "cote-d-ivoire", en: "ivory-coast", nom: "Côte d'Ivoire", name: "Ivory Coast", codes: ["ABJ"] },
  { fr: "senegal", en: "senegal", nom: "Sénégal", name: "Senegal", codes: ["DSS"] },
  { fr: "mali", en: "mali", nom: "Mali", name: "Mali", codes: ["BKO"] },
  { fr: "guinee", en: "guinea", nom: "Guinée", name: "Guinea", codes: ["CKY"] },
  { fr: "cameroun", en: "cameroon", nom: "Cameroun", name: "Cameroon", codes: ["DLA", "NSI"] },
  { fr: "rd-congo", en: "dr-congo", nom: "RD Congo", name: "DR Congo", codes: ["FIH"] },
  { fr: "togo", en: "togo", nom: "Togo", name: "Togo", codes: ["LFW"] },
  { fr: "benin", en: "benin", nom: "Bénin", name: "Benin", codes: ["COO"] },
  { fr: "burkina-faso", en: "burkina-faso", nom: "Burkina Faso", name: "Burkina Faso", codes: ["OUA"] },
  { fr: "ghana", en: "ghana", nom: "Ghana", name: "Ghana", codes: ["ACC"] },
  { fr: "nigeria", en: "nigeria", nom: "Nigeria", name: "Nigeria", codes: ["LOS", "ABV"] },
  { fr: "maroc", en: "morocco", nom: "Maroc", name: "Morocco", codes: ["CMN", "RAK"] },
  { fr: "algerie", en: "algeria", nom: "Algérie", name: "Algeria", codes: ["ALG", "ORN"] },
  { fr: "tunisie", en: "tunisia", nom: "Tunisie", name: "Tunisia", codes: ["TUN", "DJE"] },
  { fr: "egypte", en: "egypt", nom: "Égypte", name: "Egypt", codes: ["CAI"] },
  { fr: "ethiopie", en: "ethiopia", nom: "Éthiopie", name: "Ethiopia", codes: ["ADD"] },
  { fr: "kenya", en: "kenya", nom: "Kenya", name: "Kenya", codes: ["NBO"] },
  { fr: "afrique-du-sud", en: "south-africa", nom: "Afrique du Sud", name: "South Africa", codes: ["JNB"] },
]
// « vers la Côte d'Ivoire », « vers le Maroc », « vers Madagascar »…
const VERS: Record<string, string> = { "cote-d-ivoire": "la Côte d'Ivoire", senegal: "le Sénégal", mali: "le Mali", guinee: "la Guinée", cameroun: "le Cameroun", "rd-congo": "la RD Congo", togo: "le Togo", benin: "le Bénin", "burkina-faso": "le Burkina Faso", ghana: "le Ghana", nigeria: "le Nigeria", maroc: "le Maroc", algerie: "l'Algérie", tunisie: "la Tunisie", egypte: "l'Égypte", ethiopie: "l'Éthiopie", kenya: "le Kenya", "afrique-du-sud": "l'Afrique du Sud" }
const PT = {
  fr: { base: "/indice-prix/pays/", eyebrow: "Indice par pays · mis à jour chaque jour", h1: (n: string) => `Indice Escale <span>${esc(n)}</span>`, title: (n: string) => `Prix des vols vers ${VERS[n] || n} : l'indice Escale du jour | Escale`,
    desc: (n: string) => `Les billets d'avion depuis l'Europe vers ${VERS[n] || n} montent-ils ou baissent-ils ? Variation médiane des prix sur les trajets suivis chaque jour par Escale, plus fortes hausses et baisses, prix les plus bas.`,
    few: (n: string, k: number) => `${k} trajet${k > 1 ? "s" : ""} vers ${VERS[n] || n} suivi${k > 1 ? "s" : ""} chaque jour : encore trop peu pour un indice fiable. Voici les prix du moment.`, routes: "Trajets suivis", all: "Tous les pays", back: "Indice Europe – Afrique" },
  en: { base: "/en/price-index/country/", eyebrow: "Country index · updated daily", h1: (n: string) => `Escale Price Index <span>${esc(n)}</span>`, title: (n: string) => `Air fares to ${n}: today's Escale index | Escale`,
    desc: (n: string) => `Are flights from Europe to ${n} getting cheaper or dearer? Median change in fares on the routes Escale tracks daily, biggest rises and drops, lowest fares.`,
    few: (n: string, k: number) => `${k} route${k > 1 ? "s" : ""} to ${n} tracked daily: not enough yet for a reliable index. Here are today's fares.`, routes: "Tracked routes", all: "All countries", back: "Europe – Africa index" },
}
export function countryList(lang: Lang, skip = ""): string {
  const t = PT[lang]
  return `<h2>${esc(lang === "fr" ? "Indice par pays d'arrivée" : "Index by arrival country")}</h2><ul class="ix-list ix-pays">${PAYS.filter((p) => p[lang] !== skip).map((p) => `<li><a href="${t.base}${p[lang]}/">${esc(lang === "fr" ? p.nom : p.name)}</a></li>`).join("")}</ul>`
}

const median = (a: number[]) => { if (!a.length) return null; const s = a.slice().sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2) }
const cls = (v: number) => (v <= -3 ? "bt-down" : v >= 3 ? "bt-up" : "bt-flat")

// Chiffres de l'indice (partagés avec le flux RSS, le widget et le communiqué : src/diffusion.ts)
export type Summary = { date: string; span: string; spanDays: number; n: number; med: number; up: number; down: number; quote: string
  top: { label: string; v: number; price: number; path: string }[]; bottom: { label: string; v: number; price: number; path: string }[] }
export function compute(list: Row[], lang: Lang = "fr"): Summary | null {
  const t = T[lang]
  const money = (n: number) => new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
  const sign = (v: number) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v) + (lang === "fr" ? " %" : "%")
  const d = new Date().toLocaleDateString(t.loc, { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Paris" })
  const use30 = list.filter((r) => r.d30 !== null).length >= 5
  const key = use30 ? "d30" : "d7"
  const with_ = list.filter((r) => r[key] !== null)
  if (with_.length < 3) return null
  const v = (r: Row) => r[key] as number
  const vals = with_.map(v)
  const med = median(vals)!
  const down = vals.filter((x) => x <= -3).length, up = vals.filter((x) => x >= 3).length
  const sorted = with_.slice().sort((a, b) => v(a) - v(b))
  const bottom = sorted.slice(0, 5).filter((r) => v(r) <= -3), top = sorted.slice(-5).reverse().filter((r) => v(r) >= 3)
  const span = t.days(use30 ? 30 : 7)
  const trend = med >= 3 ? t.up(med) : med <= -3 ? t.down(Math.abs(med)) : t.flat(sign(med))
  let quote = t.quote(d, trend, span, with_.length)
  if (top[0]) quote += t.hi(label(top[0].label, lang), sign(v(top[0])), money(top[0].price))
  if (bottom[0]) quote += t.lo(label(bottom[0].label, lang), sign(v(bottom[0])), money(bottom[0].price))
  const pick = (r: Row) => ({ label: label(r.label, lang), v: v(r), price: r.price, path: r.path })
  return { date: d, span, spanDays: use30 ? 30 : 7, n: with_.length, med, up, down, quote, top: top.map(pick), bottom: bottom.map(pick) }
}

export function render(list: Row[], lang: Lang = "fr") {
  const t = T[lang]
  const money = (n: number) => new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
  const sign = (v: number) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v) + (lang === "fr" ? " %" : "%")
  const d = new Date().toLocaleDateString(t.loc, { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Paris" })
  const s = compute(list, lang)
  if (!s) return `<p class="bt-lead">${esc(t.wait(d))}</p>`
  const key = s.spanDays === 30 ? "d30" : "d7"
  const with_ = list.filter((r) => r[key] !== null)
  const v = (r: Row) => r[key] as number
  const { med, up, down, span, quote } = s
  const block = (title: string, codes: string[], by: "to" | "from") => {
    const g = with_.filter((r) => codes.includes(r[by]))
    const m = median(g.map(v)), p = median(g.map((r) => r.price))
    return g.length >= 2 && m !== null ? `<tr><th scope="row">${esc(title)}</th><td><span class="${cls(m)}">${sign(m)}</span></td><td>${p ? esc(money(p)) : "—"}</td><td>${g.length}</td></tr>` : ""
  }
  const li = (rs: Row[]) => rs.map((r) => `<li><a href="/${r.path}/">${esc(label(r.label, lang))}</a>${lang === "fr" ? " : " : ": "}<span class="${cls(v(r))}">${sign(v(r))}</span>, ${t.from} <strong>${esc(money(r.price))}</strong></li>`).join("")
  const top = s.top.map((x) => with_.find((r) => r.path === x.path)!), bottom = s.bottom.map((x) => with_.find((r) => r.path === x.path)!)
  const regions = REGIONS.map((c, i) => block(t.regions[i], c, "to")).join(""), origins = ORIG.map((c, i) => block(t.origins[i], c, "from")).join("")
  const [h1, h2, h3] = t.th(span)
  const thead = `<thead><tr><th scope="col"></th><th scope="col">${esc(h1)}</th><th scope="col">${esc(h2)}</th><th scope="col">${esc(h3)}</th></tr></thead>`
  return `<p class="bt-lead">${esc(t.lead(d))}</p>` +
    `<div class="ix-big"><span class="ix-num ${cls(med)}">${sign(med)}</span><span class="ix-lab">${esc(t.big(span))}<br><small>${esc(t.counts(with_.length, down, up, with_.length - down - up))}</small></span></div>` +
    `<blockquote class="ix-quote"><p id="ix-q">${esc(quote)}</p><footer>${esc(t.source)} <a href="${t.url}">${t.short}</a></footer></blockquote>` +
    `<p><button type="button" class="btn ghost" id="ix-copy">${esc(t.copy)}</button></p>` +
    (regions ? `<h2>${esc(t.byRegion)}</h2><div class="bt-wrap"><table class="bt-table">${thead}<tbody>${regions}</tbody></table></div>` : "") +
    (origins ? `<h2>${esc(t.byOrigin)}</h2><div class="bt-wrap"><table class="bt-table">${thead}<tbody>${origins}</tbody></table></div>` : "") +
    (top.length ? `<h2>${esc(t.ups)}</h2><ul class="ix-list">${li(top)}</ul>` : "") +
    (bottom.length ? `<h2>${esc(t.downs)}</h2><ul class="ix-list">${li(bottom)}</ul>` : "") +
    `<h2>${esc(t.cheap)}</h2><ul class="ix-list">${li(list.slice().sort((a, b) => a.price - b.price).slice(0, 5).filter((r) => r[key] !== null))}</ul>`
}

// ---- Archives mensuelles (/indice-prix/2026-11/, /en/price-index/2026-11/) ----
// Chaque matin à 6 h UTC (après le relevé des prix), le bloc de l'indice est enregistré dans KV sous la clé du mois en cours :
// la page du mois montre donc le dernier relevé du mois, puis reste figée quand le mois est fini. Ces pages donnent un
// historique citable (« les prix de novembre 2026 ») que les médias et les moteurs de recherche peuvent reprendre.
export type Snap = { date: string; fr: string; en: string; med: number | null; n: number; sum?: { fr: Summary | null; en: Summary | null } }
export const ARCH = "indice:archive:"
const A = {
  fr: { title: (m: string) => `Indice Escale des prix des vols Europe – Afrique : ${m}`, h1: (m: string) => `Indice Escale <span>${esc(m)}</span>`, eyebrow: "Archive mensuelle · données libres",
    desc: (m: string) => `Les prix des billets d'avion Europe – Afrique en ${m} : variation médiane, par région d'arrivée et pays de départ, plus fortes hausses et baisses. Indice Escale, calculé chaque jour.`,
    archives: "Archives mensuelles", current: "Voir l'indice du jour", month: (y: number, m: number) => new Date(Date.UTC(y, m - 1, 1)).toLocaleDateString("fr-FR", { month: "long", year: "numeric", timeZone: "UTC" }), base: "/indice-prix/" },
  en: { title: (m: string) => `Escale Price Index, Europe – Africa flights: ${m}`, h1: (m: string) => `Escale Price Index <span>${esc(m)}</span>`, eyebrow: "Monthly archive · open data",
    desc: (m: string) => `Europe – Africa air fares in ${m}: median change, by arrival region and departure country, biggest rises and drops. Escale Price Index, computed daily.`,
    archives: "Monthly archives", current: "See today's index", month: (y: number, m: number) => new Date(Date.UTC(y, m - 1, 1)).toLocaleDateString("en-GB", { month: "long", year: "numeric", timeZone: "UTC" }), base: "/en/price-index/" },
}
const monthName = (ym: string, lang: Lang) => { const [y, m] = ym.split("-").map(Number); return A[lang].month(y, m) }

async function archiveList(env: any, lang: Lang, skip = ""): Promise<string> {
  if (!env?.ESCALE) return ""
  try {
    const keys = await keysOf(env, ARCH)
    const months = keys.map((k) => k.slice(ARCH.length)).filter((m: string) => /^\d{4}-\d{2}$/.test(m) && m !== skip).sort().reverse()
    if (!months.length) return ""
    return `<h2>${esc(A[lang].archives)}</h2><ul class="ix-list ix-arch">${months.map((m: string) => `<li><a href="${A[lang].base}${m}/">${esc(monthName(m, lang))}</a></li>`).join("")}</ul>`
  } catch { return "" }
}

// Appelé par le cron de 6 h UTC (src/worker.ts) : calcule l'indice du jour et le range dans l'archive du mois
export async function archiveIndice(env: any, now = new Date()) {
  if (!env?.ESCALE) return { erreur: "kv" }
  const pending: Promise<any>[] = []
  const ctx: Ctx = { request: new Request("https://escale.live/__indice-archive"), env, waitUntil: (p) => { pending.push(p) }, next: () => Promise.resolve(new Response(null, { status: 404 })) }
  const list = await rows(ctx)
  await Promise.allSettled(pending)
  const with_ = list.filter((r) => r.d30 !== null).length >= 5 ? list.filter((r) => r.d30 !== null) : list.filter((r) => r.d7 !== null)
  if (with_.length < 3) return { ignore: "pas assez de relevés", trajets: list.length }
  const ym = now.toISOString().slice(0, 7)
  const snap: Snap = { date: now.toISOString().slice(0, 10), fr: render(list, "fr"), en: render(list, "en"), med: median(with_.map((r) => (r.d30 ?? r.d7) as number)), n: with_.length, sum: { fr: compute(list, "fr"), en: compute(list, "en") } }
  await env.ESCALE.put(ARCH + ym, JSON.stringify(snap))
  return { mois: ym, trajets: snap.n, mediane: snap.med }
}

// Page d'un mois : la mise en page de la page de l'indice (fichier statique), avec le bloc archivé à la place du bloc du jour
async function archivePage(ctx: Ctx, lang: Lang, ym: string): Promise<Response> {
  const snap: Snap | null = ctx.env.ESCALE ? await ctx.env.ESCALE.get(ARCH + ym, "json").catch(() => null) : null
  const base = await ctx.env.ASSETS?.fetch(new Request(`https://escale.live${A[lang].base}`))
  if (!snap || !base || !base.ok) return ctx.next()
  const a = A[lang], m = monthName(ym, lang)
  const block = snap[lang] + `<p><a class="btn ghost" href="${a.base}">${esc(a.current)}</a></p>` + (await archiveList(ctx.env, lang, ym)) + shareBlock(lang, ym)
  const html = (await base.text())
    .replace(/<title>[^<]*<\/title>/, `<title>${esc(a.title(m))}</title>`)
    .replace(/(<meta name="description" content=")[^"]*(")/, `$1${esc(a.desc(m))}$2`)
    .replace(/(<meta property="og:title" content=")[^"]*(")/, `$1${esc(a.title(m))}$2`)
    .replace(/(<meta property="og:description" content=")[^"]*(")/, `$1${esc(a.desc(m))}$2`)
    .replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="https://escale.live${a.base}${ym}/">`)
    .replace(/(<link rel="alternate" hreflang="[^"]*" href="https:\/\/escale\.live\/(?:en\/price-index|indice-prix)\/)(">)/g, `$1${ym}/$2`)
    .replace(/<p class="eyebrow">[^<]*<\/p>(\s*<h1>)[\s\S]*?<\/h1>/, `<p class="eyebrow">${esc(a.eyebrow)}</p>$1${a.h1(m)}</h1>`)
    .replace(/<div id="indice">[\s\S]*?<\/div><!-- \/indice -->/, `<div id="indice" data-ssr="1" data-archive="${ym}">${block}</div><!-- /indice -->`)
  const headers = new Headers(base.headers)
  headers.delete("content-length")
  headers.set("Cache-Control", "public, max-age=3600")
  return new Response(html, { status: 200, headers })
}

async function countryPage(ctx: Ctx, lang: Lang, slug: string): Promise<Response> {
  const p = PAYS.find((x) => x[lang] === slug)
  const base = p ? await ctx.env.ASSETS?.fetch(new Request(`https://escale.live${lang === "fr" ? "/indice-prix/" : "/en/price-index/"}`)) : null
  if (!p || !base || !base.ok) return ctx.next()
  const t = PT[lang], name = lang === "fr" ? p.nom : p.name, key = lang === "fr" ? p.fr : p.name
  const all = await rows(ctx)
  const sub = all.filter((r) => p.codes.includes(r.to))
  const money = (n: number) => new Intl.NumberFormat(T[lang].loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
  let block: string
  if (sub.filter((r) => r.d7 !== null).length >= 3) block = render(sub, lang)
  else block = `<p class="bt-lead">${esc(t.few(key, sub.length))}</p>` + (sub.length ? `<ul class="ix-list">${sub.slice().sort((a, b) => a.price - b.price).map((r) => `<li><a href="/${r.path}/">${esc(label(r.label, lang))}</a>${lang === "fr" ? " : " : ": "}${T[lang].from} <strong>${esc(money(r.price))}</strong></li>`).join("")}</ul>` : "")
  block += `<p><a class="btn ghost" href="${lang === "fr" ? "/indice-prix/" : "/en/price-index/"}">${esc(t.back)}</a></p>` + countryList(lang, slug)
  const html = (await base.text())
    .replace(/<title>[^<]*<\/title>/, `<title>${esc(t.title(key))}</title>`)
    .replace(/(<meta name="description" content=")[^"]*(")/, `$1${esc(t.desc(key))}$2`)
    .replace(/(<meta property="og:title" content=")[^"]*(")/, `$1${esc(t.title(key).replace(/ \| Escale$/, ""))}$2`)
    .replace(/(<meta property="og:description" content=")[^"]*(")/, `$1${esc(t.desc(key))}$2`)
    .replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="https://escale.live${t.base}${slug}/">`)
    .replace(/(<link rel="alternate" hreflang="fr" href=")[^"]*(")/, `$1https://escale.live${PT.fr.base}${p.fr}/$2`)
    .replace(/(<link rel="alternate" hreflang="en" href=")[^"]*(")/, `$1https://escale.live${PT.en.base}${p.en}/$2`)
    .replace(/(<link rel="alternate" hreflang="x-default" href=")[^"]*(")/, `$1https://escale.live${PT.fr.base}${p.fr}/$2`)
    .replace(/<p class="eyebrow">[^<]*<\/p>(\s*<h1>)[\s\S]*?<\/h1>/, `<p class="eyebrow">${esc(t.eyebrow)}</p>$1${t.h1(name)}</h1>`)
    .replace(/<div id="indice">[\s\S]*?<\/div><!-- \/indice -->/, `<div id="indice" data-ssr="1" data-pays="${esc(slug)}">${block}</div><!-- /indice -->`)
  const headers = new Headers(base.headers)
  headers.delete("content-length")
  headers.set("Cache-Control", "public, max-age=3600")
  return new Response(html, { status: 200, headers })
}

export const onRequest = async (ctx: Ctx) => {
  const path = new URL(ctx.request.url).pathname
  const lang: Lang = path.startsWith("/en/") ? "en" : "fr"
  const pays = path.match(/\/(?:pays|country)\/([a-z-]+)\/?$/)
  if (ctx.request.method === "GET" && pays) { try { return await countryPage(ctx, lang, pays[1]) } catch { return ctx.next() } }
  const arch = path.match(/\/(\d{4}-\d{2})\/?$/)
  if (ctx.request.method === "GET" && arch) { try { return await archivePage(ctx, lang, arch[1]) } catch { return ctx.next() } }
  const response = await ctx.next()
  if (ctx.request.method !== "GET" || !response.ok) return response
  const cache = (globalThis as any).caches?.default
  const key = new Request(`https://escale.live/__indice/v5/${lang}/` + new Date().toISOString().slice(0, 10))
  try {
    let block = ""
    const hit = cache ? await cache.match(key) : null
    if (hit) block = await hit.text()
    else {
      const list = await rows(ctx)
      if (list.length) {
        block = render(list, lang) + countryList(lang) + (await archiveList(ctx.env, lang)) + shareBlock(lang)
        if (cache) ctx.waitUntil(cache.put(key, new Response(block, { headers: { "Cache-Control": "public, max-age=3600" } })))
      }
    }
    if (!block) return response
    const feed = lang === "fr" ? "/barometre-prix/flux.xml" : "/en/price-index/feed.xml"
    const html = (await response.text()).replace(/<div id="indice">[\s\S]*?<\/div><!-- \/indice -->/, `<div id="indice" data-ssr="1">${block}</div><!-- /indice -->`)
      .replace("</title>", `</title><link rel="alternate" type="application/rss+xml" title="Escale" href="https://escale.live${feed}">`)
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    return new Response(html, { status: response.status, headers })
  } catch {
    return response
  }
}
