import { Ctx, Env, esc } from "./_lib/common"
import { ROUTES } from "./barometre"
import { Point, readHistory, verdict } from "./apercu-prix"
import { label } from "./indice"
// « À saisir aujourd'hui » (/a-saisir/ en français, /en/deals-today/ en anglais) : les grands trajets dont le prix du jour est
// nettement sous leur prix habituel (verdict « bon prix » : au moins 8 % sous la médiane des 60 derniers relevés).
// Recalculé chaque heure à partir de l'historique KV (relevé quotidien, src/releve.ts). Sert aussi au bandeau de l'accueil
// et au message WhatsApp (src/digest.ts). Page écrite par le serveur sur la mise en page du baromètre (fichier statique).
export type Deal = { label: string; path: string; from: string; to: string; price: number; diff: number; median: number; d7: number | null; days: number }
export type Deals = { date: string; total: number; items: Deal[] }
const CACHE_S = 3600
const iso = (daysAgo: number) => new Date(Date.now() - daysAgo * 864e5).toISOString().slice(0, 10)

function weekAgo(hist: Point[]) {
  const target = Date.parse(iso(7))
  let best: Point | null = null
  for (const p of hist) { const gap = Math.abs(Date.parse(p[0]) - target) / 864e5; if (gap <= 2 && (!best || gap < Math.abs(Date.parse(best[0]) - target) / 864e5)) best = p }
  return best ? best[1] : null
}

async function compute(env: Env): Promise<Deals> {
  const ctx: Ctx = { request: new Request("https://escale.live/__saisir"), env, waitUntil: () => {}, next: () => Promise.resolve(new Response(null, { status: 404 })) }
  const since = iso(1)
  let total = 0
  const items = (await Promise.all(ROUTES.map(async ([from, to, lab, path]) => {
    const hist = await readHistory(ctx, from, to)
    const last = hist[hist.length - 1]
    if (!last || last[0] < since) return null
    total++
    const v = verdict(hist, last[1])
    if (!v || v.level !== "low") return null
    const w = weekAgo(hist)
    return { label: lab, path, from, to, price: last[1], diff: v.diff, median: v.median, d7: w ? Math.round((last[1] / w - 1) * 100) : null, days: v.days } as Deal
  }))).filter(Boolean) as Deal[]
  items.sort((a, b) => b.diff - a.diff)
  return { date: iso(0), total, items }
}

// Résultat gardé une heure dans le cache Cloudflare (une seule clé pour toutes les langues)
export async function deals(env: Env, waitUntil: (p: Promise<any>) => void = () => {}): Promise<Deals> {
  const cache = (globalThis as any).caches?.default
  const key = new Request("https://escale.live/__saisir/v1/" + new Date().toISOString().slice(0, 13))
  if (cache) { const hit = await cache.match(key); if (hit) return hit.json() }
  const d = await compute(env)
  if (cache && d.total) waitUntil(cache.put(key, new Response(JSON.stringify(d), { headers: { "Cache-Control": `public, max-age=${CACHE_S}` } })))
  return d
}

type Lang = "fr" | "en"
const T = {
  fr: { loc: "fr-FR", path: "/a-saisir/", other: "/en/deals-today/", eyebrow: "Mis à jour chaque heure", h1: "À saisir aujourd'hui", title: "Vols à saisir aujourd'hui : les trajets sous leur prix habituel | Escale",
    desc: "Chaque jour, les trajets Europe – Afrique dont le prix aller-retour est nettement sous son niveau habituel, d'après les relevés quotidiens d'Escale. Mis à jour chaque heure.",
    lead: (n: number, t: number, d: string) => n ? `Relevé du ${d} : ${n} trajet${n > 1 ? "s" : ""} sur ${t} suivis ${n > 1 ? "sont" : "est"} nettement sous ${n > 1 ? "leur" : "son"} prix habituel.` : `Relevé du ${d} : aucun des ${t} trajets suivis n'est nettement sous son prix habituel aujourd'hui. Revenez demain, ou créez une alerte prix.`,
    th: ["Trajet", "Aller-retour dès", "Sous le prix habituel", "Prix habituel", "Sur 7 jours"], how: "Comment c'est calculé",
    howTxt: "Chaque nuit, Escale relève le prix aller-retour le plus bas des 6 prochains mois pour 70 grands trajets de la diaspora. Un trajet apparaît ici quand ce prix est au moins 8 % sous la médiane de ses 60 derniers relevés (au moins 7 jours d'historique). C'est un signal, pas une promesse : le tarif exact dépend des dates et se confirme sur le site de réservation.",
    more: "Voir aussi", baro: "Le baromètre des prix (tous les trajets)", indice: "L'indice Escale des prix", alert: "Acheter maintenant ou attendre ? Le guide", since: (n: number) => `${n} jours de relevés`, go: "Voir ce trajet",
    banner: (n: number) => `🟢 ${n} trajet${n > 1 ? "s" : ""} sous ${n > 1 ? "leur" : "son"} prix habituel aujourd'hui`, bannerGo: "Voir lesquels" },
  en: { loc: "en-GB", path: "/en/deals-today/", other: "/a-saisir/", eyebrow: "Updated hourly", h1: "Worth booking today", title: "Flights worth booking today: routes below their usual price | Escale",
    desc: "Every day, the Europe – Africa routes whose round-trip fare is clearly below its usual level, based on Escale's daily price records. Updated hourly.",
    lead: (n: number, t: number, d: string) => n ? `Data as of ${d}: ${n} of ${t} tracked routes ${n > 1 ? "are" : "is"} clearly below ${n > 1 ? "their" : "its"} usual price.` : `Data as of ${d}: none of the ${t} tracked routes is clearly below its usual price today. Check back tomorrow, or set a price alert.`,
    th: ["Route", "Round trip from", "Below usual price", "Usual price", "Over 7 days"], how: "How it is computed",
    howTxt: "Every night, Escale records the lowest round-trip fare over the next 6 months for 70 major diaspora routes. A route appears here when that fare is at least 8% below the median of its last 60 records (at least 7 days of history). It is a signal, not a promise: the exact fare depends on dates and is confirmed on the booking site.",
    more: "See also", baro: "The price barometer (all routes)", indice: "The Escale Price Index", alert: "Buy now or wait? The guide", since: (n: number) => `${n} days of records`, go: "See this route",
    banner: (n: number) => `🟢 ${n} route${n > 1 ? "s" : ""} below ${n > 1 ? "their" : "its"} usual price today`, bannerGo: "See which" },
}

export function renderList(d: Deals, lang: Lang): string {
  const t = T[lang]
  const money = (n: number) => new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
  const date = new Date().toLocaleDateString(t.loc, { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Paris" })
  const sign = (v: number | null) => v === null ? `<span class="bt-na">—</span>` : `<span class="${v <= -3 ? "bt-down" : v >= 3 ? "bt-up" : "bt-flat"}">${v > 0 ? "+" : v < 0 ? "−" : ""}${Math.abs(v)}${lang === "fr" ? " %" : "%"}</span>`
  const rows = d.items.map((r) => `<tr><th scope="row"><a href="/${r.path}/">${esc(label(r.label, lang))}</a><br><small>${esc(t.since(r.days))}</small></th>` +
    `<td><strong>${esc(money(r.price))}</strong></td><td><span class="bt-down">−${r.diff}${lang === "fr" ? " %" : "%"}</span></td><td>${esc(money(r.median))}</td><td>${sign(r.d7)}</td></tr>`).join("")
  return `<p class="bt-lead">${esc(t.lead(d.items.length, d.total, date))}</p>` +
    (rows ? `<div class="bt-wrap"><table class="bt-table"><thead><tr>${t.th.map((h) => `<th scope="col">${esc(h)}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div>` : "")
}

// Bandeau de l'accueil (vide s'il n'y a rien à saisir)
export function banner(d: Deals, lang: Lang = "fr"): string {
  if (!d.items.length) return ""
  const t = T[lang]
  const top = d.items.slice(0, 3).map((r) => `${label(r.label, lang)} −${r.diff}${lang === "fr" ? " %" : "%"}`).join(" · ")
  return `<style>.sz{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;margin:0 auto 14px;padding:10px 16px;border-radius:14px;background:#edf8f1;border:1px solid #bfe3cd;color:#0f5132}.sz strong{font-weight:700}.sz small{color:#2b6a45}.sz a{margin-inline-start:auto;font-weight:700;color:#0b8577;white-space:nowrap}:root:not([data-theme="light"]) .sz{background:rgb(24 121 78/.18);border-color:rgb(24 121 78/.4);color:#bfe3cd}:root:not([data-theme="light"]) .sz small{color:#9ccfb0}</style>` +
    `<div class="wrap"><p class="sz"><strong>${esc(t.banner(d.items.length))}</strong><small>${esc(top)}</small><a href="${t.path}">${esc(t.bannerGo)} →</a></p></div>`
}

// Lignes pour le message WhatsApp (src/digest.ts) : au plus 5 trajets, en français
export function whatsappLines(d: Deals, base: string): string[] {
  if (!d.items.length) return []
  const money = (n: number) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
  return ["🟢 *Sous leur prix habituel aujourd'hui :*", ...d.items.slice(0, 5).map((r) => `• ${r.label} : *${money(r.price)}* (−${r.diff} % vs habituel)`), `   👉 ${base}/a-saisir/`, ""]
}

// Page complète : mise en page du baromètre (fichier statique), contenu remplacé
export async function page(ctx: Ctx, lang: Lang): Promise<Response> {
  const t = T[lang]
  const base = await ctx.env.ASSETS?.fetch(new Request("https://escale.live/barometre-prix/"))
  if (!base || !base.ok) return ctx.next()
  const d = await deals(ctx.env, ctx.waitUntil)
  const main = `<main>\n<div class="board"><div class="wrap">\n  <p class="eyebrow">${esc(t.eyebrow)}</p><h1>${esc(t.h1)}</h1><p class="hero-lead">${esc(t.desc)}</p>\n</div></div>\n<div class="wrap">\n` +
    `<section><div id="saisir" data-ssr="1">${renderList(d, lang)}</div></section>` +
    `<section><h2>${esc(t.how)}</h2><p>${esc(t.howTxt)}</p></section>` +
    `<section><h2>${esc(t.more)}</h2><ul><li><a href="/barometre-prix/">${esc(t.baro)}</a></li><li><a href="${lang === "fr" ? "/indice-prix/" : "/en/price-index/"}">${esc(t.indice)}</a></li><li><a href="/${lang === "fr" ? "acheter-ou-attendre" : "en/buy-or-wait"}/">${esc(t.alert)}</a></li></ul></section>` +
    `</div>\n</main>`
  let html = await base.text()
  html = html.slice(0, html.indexOf("<main>")) + main + html.slice(html.indexOf("</main>") + 7)
  html = html
    .replace(/<html lang="[a-z]{2}"/, `<html lang="${lang}"`)
    .replace(/<title>[^<]*<\/title>/, `<title>${esc(t.title)}</title>`)
    .replace(/(<meta name="description" content=")[^"]*(")/, `$1${esc(t.desc)}$2`)
    .replace(/(<meta property="og:title" content=")[^"]*(")/, `$1${esc(t.title.replace(/ \| Escale$/, ""))}$2`)
    .replace(/(<meta property="og:description" content=")[^"]*(")/, `$1${esc(t.desc)}$2`)
    .replace(/(<meta property="og:locale" content=")[^"]*(")/, `$1${lang === "fr" ? "fr_FR" : "en_GB"}$2`)
    .replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="https://escale.live${t.path}">`)
    .replace(/<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*/g, "")
    .replace(/<\/title>/, `</title><link rel="alternate" hreflang="fr" href="https://escale.live/a-saisir/"><link rel="alternate" hreflang="en" href="https://escale.live/en/deals-today/"><link rel="alternate" hreflang="x-default" href="https://escale.live/a-saisir/">`)
    .replace(/<script type="application\/ld\+json">\{"@context": "https:\/\/schema.org", "@type": "Dataset"[\s\S]*?<\/script>/, "")
  const headers = new Headers(base.headers)
  headers.delete("content-length")
  headers.set("Cache-Control", "public, max-age=1800")
  return new Response(html, { status: 200, headers })
}
