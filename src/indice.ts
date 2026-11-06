import { Ctx, esc } from "./_lib/common"
import { Row, rows } from "./barometre"
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
const EN: Record<string, string> = { Londres: "London", "Le Caire": "Cairo", "Addis-Abeba": "Addis Ababa", Alger: "Algiers", Bruxelles: "Brussels", Maurice: "Mauritius",
  "N’Djamena": "N'Djamena", Yaoundé: "Yaoundé", Lomé: "Lomé", Marrakech: "Marrakesh" }
const label = (l: string, lang: Lang) => lang === "fr" ? l : l.split(" → ").map((x) => EN[x] || x).join(" → ")

const median = (a: number[]) => { if (!a.length) return null; const s = a.slice().sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2) }
const cls = (v: number) => (v <= -3 ? "bt-down" : v >= 3 ? "bt-up" : "bt-flat")

export function render(list: Row[], lang: Lang = "fr") {
  const t = T[lang]
  const money = (n: number) => new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
  const sign = (v: number) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v) + (lang === "fr" ? " %" : "%")
  const d = new Date().toLocaleDateString(t.loc, { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Paris" })
  const use30 = list.filter((r) => r.d30 !== null).length >= 5
  const key = use30 ? "d30" : "d7"
  const span = t.days(use30 ? 30 : 7)
  const with_ = list.filter((r) => r[key] !== null)
  if (with_.length < 3) return `<p class="bt-lead">${esc(t.wait(d))}</p>`
  const v = (r: Row) => r[key] as number
  const vals = with_.map(v)
  const med = median(vals)!
  const down = vals.filter((x) => x <= -3).length, up = vals.filter((x) => x >= 3).length
  const sorted = with_.slice().sort((a, b) => v(a) - v(b))
  const bottom = sorted.slice(0, 5).filter((r) => v(r) <= -3), top = sorted.slice(-5).reverse().filter((r) => v(r) >= 3)
  const trend = med >= 3 ? t.up(med) : med <= -3 ? t.down(Math.abs(med)) : t.flat(sign(med))
  let quote = t.quote(d, trend, span, with_.length)
  if (top[0]) quote += t.hi(label(top[0].label, lang), sign(v(top[0])), money(top[0].price))
  if (bottom[0]) quote += t.lo(label(bottom[0].label, lang), sign(v(bottom[0])), money(bottom[0].price))
  const block = (title: string, codes: string[], by: "to" | "from") => {
    const g = with_.filter((r) => codes.includes(r[by]))
    const m = median(g.map(v)), p = median(g.map((r) => r.price))
    return g.length >= 2 && m !== null ? `<tr><th scope="row">${esc(title)}</th><td><span class="${cls(m)}">${sign(m)}</span></td><td>${p ? esc(money(p)) : "—"}</td><td>${g.length}</td></tr>` : ""
  }
  const li = (rs: Row[]) => rs.map((r) => `<li><a href="/${r.path}/">${esc(label(r.label, lang))}</a>${lang === "fr" ? " : " : ": "}<span class="${cls(v(r))}">${sign(v(r))}</span>, ${t.from} <strong>${esc(money(r.price))}</strong></li>`).join("")
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

export const onRequest = async (ctx: Ctx) => {
  const response = await ctx.next()
  if (ctx.request.method !== "GET" || !response.ok) return response
  const lang: Lang = new URL(ctx.request.url).pathname.startsWith("/en/") ? "en" : "fr"
  const cache = (globalThis as any).caches?.default
  const key = new Request(`https://escale.live/__indice/v2/${lang}/` + new Date().toISOString().slice(0, 10))
  try {
    let block = ""
    const hit = cache ? await cache.match(key) : null
    if (hit) block = await hit.text()
    else {
      const list = await rows(ctx)
      if (list.length) {
        block = render(list, lang)
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
