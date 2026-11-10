import { Ctx, Env, esc } from "./_lib/common"
import { ROUTES } from "./barometre"
import { Month, Point, readHistory, readMonths, verdict } from "./apercu-prix"
// Pages de bons plans écrites par le serveur à partir des relevés quotidiens (aucun fichier statique, aucune page écrite à la main) :
//   /barometre-prix/depuis/                 → liste des villes de départ
//   /barometre-prix/depuis/milan/           → « Vols pas chers au départ de Milan » : toutes les destinations relevées, prix du jour
//   /barometre-prix/mois/                   → liste des mois
//   /barometre-prix/mois/fevrier/           → « Où partir en février » : tous les trajets, prix repéré pour ce mois
//   /barometre-prix/mois/decembre/abidjan/  → « Vols pour Abidjan en décembre » : prix depuis chaque ville de départ
//   /barometre-prix/plan.xml                → plan de ces pages pour les moteurs de recherche
// Toutes sous /barometre-prix/, déjà envoyé au serveur (run_worker_first dans wrangler.jsonc). Mise en page : celle du baromètre.
// Données : historique KV (hist:FROM-TO) et prix par mois (mois:FROM-TO, écrit par src/apercu-prix.ts à chaque relevé).
// Une page sans assez de prix réels porte « noindex » : Google ne voit que les pages qui ont du contenu. Rien n'est inventé.
type Row = { from: string; to: string; a: string; b: string; path: string; price: number; d7: number | null; level: "low" | "mid" | "high" | null; diff: number; median: number; best: string; months: Month[] }
type Snap = { date: string; rows: Row[] }
const CACHE_S = 3600
const iso = (daysAgo: number) => new Date(Date.now() - daysAgo * 864e5).toISOString().slice(0, 10)
const slug = (s: string) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")
const money = (n: number) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
const MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
const MSLUG = MOIS.map(slug)
const moisNom = (ym: string) => `${MOIS[Number(ym.slice(5, 7)) - 1]} ${ym.slice(0, 4)}`
const jour = (d: string) => { const [y, m, j] = d.split("-").map(Number); return new Date(Date.UTC(y, m - 1, j)).toLocaleDateString("fr-FR", { day: "numeric", month: "short", timeZone: "UTC" }) }
// Les 6 mois couverts par les relevés (mois en cours + 5)
const fenetre = () => { const n = new Date(); return Array.from({ length: 6 }, (_, i) => new Date(Date.UTC(n.getUTCFullYear(), n.getUTCMonth() + i, 1)).toISOString().slice(0, 7)) }
const ymDe = (ms: string) => fenetre().find((ym) => MSLUG[Number(ym.slice(5, 7)) - 1] === ms) || null

function weekAgo(hist: Point[]) {
  const target = Date.parse(iso(7))
  let best: Point | null = null
  for (const p of hist) { const gap = Math.abs(Date.parse(p[0]) - target) / 864e5; if (gap <= 2 && (!best || gap < Math.abs(Date.parse(best[0]) - target) / 864e5)) best = p }
  return best ? best[1] : null
}

async function compute(env: Env): Promise<Snap> {
  const ctx: Ctx = { request: new Request("https://escale.live/__bonsplans"), env, waitUntil: () => {}, next: () => Promise.resolve(new Response(null, { status: 404 })) }
  const since = iso(2), today = iso(0)
  const rows = (await Promise.all(ROUTES.map(async ([from, to, lab, path]) => {
    const [hist, saved] = await Promise.all([readHistory(ctx, from, to), readMonths(env, from, to)])
    const last = hist[hist.length - 1]
    if (!last || last[0] < since) return null
    const v = verdict(hist, last[1]), w = weekAgo(hist), [a, b] = lab.split(" → ")
    // Prix par mois : seulement s'ils datent de moins de 3 jours et pour des mois pas encore passés
    const months = saved && saved.d >= since ? saved.rows.filter((m) => m.month >= today.slice(0, 7) && m.price > 0) : []
    return { from, to, a, b, path, price: last[1], d7: w ? Math.round((last[1] / w - 1) * 100) : null, level: v ? v.level : null, diff: v ? v.diff : 0, median: v ? v.median : 0, best: last[2] || "", months } as Row
  }))).filter(Boolean) as Row[]
  return { date: today, rows }
}

async function snapshot(ctx: Ctx): Promise<Snap> {
  const cache = (globalThis as any).caches?.default
  const key = new Request("https://escale.live/__bonsplans/v2/" + new Date().toISOString().slice(0, 13))
  if (cache) { const hit = await cache.match(key); if (hit) return hit.json() }
  const s = await compute(ctx.env)
  if (cache && s.rows.length) ctx.waitUntil(cache.put(key, new Response(JSON.stringify(s), { headers: { "Cache-Control": `public, max-age=${CACHE_S}` } })))
  return s
}

// ---------- éléments communs ----------
const NIVEAU = { low: ["bt-down", "Bon prix"], mid: ["bt-flat", "Dans la moyenne"], high: ["bt-up", "Plutôt élevé"] } as const
const niveau = (r: Row) => (r.level ? `<span class="${NIVEAU[r.level][0]}">${NIVEAU[r.level][1]}${r.level === "low" ? ` (−${r.diff} %)` : ""}</span>` : `<span class="bt-na">—</span>`)
const tendance = (v: number | null) => (v === null ? `<span class="bt-na">—</span>` : `<span class="${v <= -3 ? "bt-down" : v >= 3 ? "bt-up" : "bt-flat"}">${v > 0 ? "+" : v < 0 ? "−" : ""}${Math.abs(v)} %</span>`)
const table = (th: string[], lignes: string[]) => `<div class="bt-wrap"><table class="bt-table"><thead><tr>${th.map((h) => `<th scope="col">${esc(h)}</th>`).join("")}</tr></thead><tbody>${lignes.join("")}</tbody></table></div>`
const liste = (items: [string, string][]) => `<ul>${items.map(([u, t]) => `<li><a href="${u}">${esc(t)}</a></li>`).join("")}</ul>`
const puces = (items: [string, string][]) => `<p class="bp-puces">${items.map(([u, t]) => `<a href="${u}">${esc(t)}</a>`).join("")}</p>`
const STYLE = `<style>.bp-puces{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}.bp-puces a{padding:7px 13px;border-radius:999px;border:1px solid var(--line,#e3e7ee);background:var(--surface,#fff);text-decoration:none;font-weight:600;font-size:.92rem;color:inherit}.bp-qr dt{font-weight:700;margin-top:14px}.bp-qr dd{margin:4px 0 0;color:var(--muted,#5b6474)}</style>`
const METHODE = `<section><h2>D'où viennent ces prix</h2><p>Chaque nuit, Escale relève le prix aller-retour le plus bas des 6 prochains mois pour les grands trajets entre l'Europe et l'Afrique, auprès de dizaines de compagnies et d'agences. Cette page se met à jour toute seule à partir de ces relevés. Les prix sont indicatifs, par personne : le tarif exact dépend des dates et des bagages, et se confirme sur le site de réservation.</p></section>`
const villes = (s: Snap) => [...new Map(s.rows.map((r) => [slug(r.a), r.a])).entries()].sort((x, y) => x[1].localeCompare(y[1], "fr"))
const destinations = (s: Snap) => [...new Map(s.rows.map((r) => [slug(r.b), r.b])).entries()]
const lienTrajet = (r: Row, texte: string) => `<a href="/${r.path}/">${esc(texte)}</a>`
const dateFr = () => new Date().toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Paris" })
const prixDuMois = (r: Row, ym: string) => r.months.find((m) => m.month === ym) || null

// Liens vers ces pages, ajoutés au baromètre et à « À saisir aujourd'hui »
export const LIENS = `<section><h2>Bons plans par ville de départ et par mois</h2>${STYLE}${puces([["/barometre-prix/depuis/", "Par ville de départ"], ["/barometre-prix/mois/", "Par mois"], ["/barometre-prix/a-saisir/", "À saisir aujourd'hui"], ["/barometre-prix/actus/", "Les actus de la semaine"]])}</section>`

export type Page = { path: string; title: string; desc: string; eyebrow: string; h1: string; body: string; index: boolean; article?: boolean }
export async function shell(ctx: Ctx, p: Page): Promise<Response> {
  const base = await ctx.env.ASSETS?.fetch(new Request("https://escale.live/barometre-prix/"))
  if (!base || !base.ok) return ctx.next()
  const main = `<main>\n<div class="board"><div class="wrap">\n  <p class="eyebrow">${esc(p.eyebrow)}</p><h1>${esc(p.h1)}</h1><p class="hero-lead">${esc(p.desc)}</p>\n</div></div>\n<div class="wrap">\n${STYLE}${p.body}${p.article ? "" : METHODE}</div>\n</main>`
  let html = await base.text()
  html = html.slice(0, html.indexOf("<main>")) + main + html.slice(html.indexOf("</main>") + 7)
  html = html
    .replace(/<title>[^<]*<\/title>/, `<title>${esc(p.title)}</title>${p.index ? "" : '<meta name="robots" content="noindex, follow">'}`)
    .replace(/(<meta name="description" content=")[^"]*(")/, `$1${esc(p.desc)}$2`)
    .replace(/(<meta property="og:title" content=")[^"]*(")/, `$1${esc(p.title.replace(/ \| Escale$/, ""))}$2`)
    .replace(/(<meta property="og:description" content=")[^"]*(")/, `$1${esc(p.desc)}$2`)
    .replace(/(<meta property="og:url" content=")[^"]*(")/, `$1https://escale.live${p.path}$2`)
    .replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="https://escale.live${p.path}">`)
    .replace(/<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*/g, "")
    .replace(/<script type="application\/ld\+json">\{"@context": "https:\/\/schema.org", "@type": "Dataset"[\s\S]*?<\/script>/, "")
  const headers = new Headers(base.headers)
  headers.delete("content-length")
  headers.set("Cache-Control", "public, max-age=1800")
  return new Response(html, { status: 200, headers })
}

// ---------- 1. par ville de départ ----------
function pageDepuis(s: Snap, vs: string): Page | null {
  const rows = s.rows.filter((r) => slug(r.a) === vs).sort((x, y) => x.price - y.price)
  if (!rows.length) return null
  const ville = rows[0].a, min = rows[0], max = rows[rows.length - 1], bons = rows.filter((r) => r.level === "low")
  const lignes = rows.map((r) => `<tr><th scope="row">${lienTrajet(r, `${r.a} → ${r.b}`)}</th><td><strong>${esc(money(r.price))}</strong></td><td>${niveau(r)}</td><td>${tendance(r.d7)}</td><td>${r.best ? esc(moisNom(r.best)) : "—"}</td></tr>`)
  const moisDispo = fenetre().filter((ym) => rows.some((r) => prixDuMois(r, ym)))
  // Mois le plus souvent le moins cher au départ de cette ville
  const compte = new Map<string, number>()
  rows.forEach((r) => { if (r.best) compte.set(r.best, (compte.get(r.best) || 0) + 1) })
  const top = [...compte.entries()].sort((x, y) => y[1] - x[1])[0]
  const qr: [string, string][] = [
    [`Quel est le vol le moins cher au départ de ${ville} vers l'Afrique ?`, `Au relevé du ${dateFr()}, c'est ${ville} → ${min.b}, à partir de ${money(min.price)} l'aller-retour.`],
    [`Quels trajets au départ de ${ville} sont de bonnes affaires aujourd'hui ?`, bons.length ? `${bons.map((r) => `${r.a} → ${r.b} (${money(r.price)}, ${r.diff} % sous son prix habituel)`).join(" ; ")}.` : `Aucun n'est nettement sous son prix habituel aujourd'hui. Une alerte prix sur la page du trajet prévient quand ça baisse.`],
    ...(top ? [[`Quel mois partir de ${ville} pour payer moins cher ?`, `En ce moment, ${moisNom(top[0])} est le mois le moins cher pour ${top[1]} des ${rows.length} destinations relevées. Le mois le moins cher de chaque trajet est indiqué dans le tableau.`] as [string, string]] : []),
  ]
  const body = `<section><p class="bt-lead">Relevé du ${esc(dateFr())} : ${rows.length} destination${rows.length > 1 ? "s" : ""} au départ de ${esc(ville)}, de ${esc(money(min.price))} (${esc(min.b)}) à ${esc(money(max.price))} (${esc(max.b)}) l'aller-retour. ${bons.length ? `${bons.length} ${bons.length > 1 ? "sont" : "est"} sous ${bons.length > 1 ? "leur" : "son"} prix habituel.` : ""}</p>` +
    table(["Trajet", "Aller-retour dès", "Niveau du prix", "Sur 7 jours", "Mois le moins cher"], lignes) + `</section>` +
    `<section><h2>En bref</h2><dl class="bp-qr">${qr.map(([q, r]) => `<dt>${esc(q)}</dt><dd>${esc(r)}</dd>`).join("")}</dl></section>` +
    (moisDispo.length ? `<section><h2>Partir de ${esc(ville)} mois par mois</h2>${puces(moisDispo.map((ym) => [`/barometre-prix/mois/${MSLUG[Number(ym.slice(5, 7)) - 1]}/`, `Où partir en ${moisNom(ym)}`]))}</section>` : "") +
    `<section><h2>Autres villes de départ</h2>${puces(villes(s).filter(([v]) => v !== vs).map(([v, n]) => [`/barometre-prix/depuis/${v}/`, `Depuis ${n}`]))}</section>`
  return { path: `/barometre-prix/depuis/${vs}/`, title: `Vols pas chers depuis ${ville} vers l'Afrique : prix du jour | Escale`, eyebrow: "Mis à jour chaque jour",
    h1: `Vols pas chers au départ de ${ville}`, desc: `Les prix aller-retour du jour au départ de ${ville} vers ${rows.length} destinations d'Afrique et du Maghreb, du moins cher au plus cher, avec le mois le moins cher de chaque trajet.`, body, index: rows.length >= 2 }
}

// ---------- 2. par mois ----------
function pageMois(s: Snap, ms: string): Page | null {
  const idx = MSLUG.indexOf(ms)
  if (idx < 0) return null
  const ym = ymDe(ms), nom = MOIS[idx]
  const autres = `<section><h2>Les autres mois</h2>${puces(fenetre().filter((x) => x !== ym).map((x) => [`/barometre-prix/mois/${MSLUG[Number(x.slice(5, 7)) - 1]}/`, moisNom(x)]))}</section>` +
    `<section><h2>Par ville de départ</h2>${puces(villes(s).map(([v, n]) => [`/barometre-prix/depuis/${v}/`, `Depuis ${n}`]))}</section>`
  if (!ym) return { path: `/barometre-prix/mois/${ms}/`, title: `Où partir en ${nom} pas cher : vols Europe – Afrique | Escale`, eyebrow: "Bons plans par mois", h1: `Où partir en ${nom}`,
    desc: `Les prix pour ${nom} ne sont pas encore relevés : Escale suit les 6 prochains mois. Voici les mois disponibles.`, body: `<section><p class="bt-lead">Les relevés d'Escale couvrent les 6 prochains mois. Les prix pour ${esc(nom)} apparaîtront ici dès que ce mois entrera dans cette période.</p></section>` + autres, index: false }
  // Prix du mois pour chaque trajet ; à défaut de prix par mois, les trajets dont c'est le mois le moins cher
  const avec = s.rows.map((r) => ({ r, m: prixDuMois(r, ym) })).filter((x) => x.m) as { r: Row; m: Month }[]
  // Mois le moins cher de chaque trajet : pris dans les mêmes prix par mois (et non dans l'historique), pour comparer ce qui est comparable
  const moinsCher = (r: Row) => r.months.reduce((a, c) => (c.price < a.price ? c : a))
  const liste2 = avec.length ? avec.map(({ r, m }) => ({ r, prix: m.price, dep: m.dep, ret: m.ret, mini: moinsCher(r).price, mm: moinsCher(r).month })) : s.rows.filter((r) => r.best === ym).map((r) => ({ r, prix: r.price, dep: "", ret: "", mini: r.price, mm: ym }))
  liste2.sort((x, y) => x.prix - y.prix)
  const lignes = liste2.map(({ r, prix, dep, ret, mini, mm }) => `<tr><th scope="row">${lienTrajet(r, `${r.a} → ${r.b}`)}</th><td><strong>${esc(money(prix))}</strong></td><td>${dep && ret ? `${esc(jour(dep))} → ${esc(jour(ret))}` : "—"}</td>` +
    `<td>${prix <= mini ? `<span class="bt-down">Le mois le moins cher</span>` : `<span class="bt-flat">+${Math.round((prix / mini - 1) * 100)} % par rapport à ${esc(moisNom(mm))}</span>`}</td></tr>`)
  const dests = destinations(s).map(([d, n]) => ({ d, n, c: avec.filter((x) => slug(x.r.b) === d).length })).filter((x) => x.c >= 2).sort((x, y) => x.n.localeCompare(y.n, "fr"))
  const min = liste2[0], champions = liste2.filter((x) => x.prix <= x.mini).length
  const body = (liste2.length ? `<section><p class="bt-lead">Relevé du ${esc(dateFr())} : ${liste2.length} trajet${liste2.length > 1 ? "s" : ""} avec un prix repéré pour ${esc(moisNom(ym))}, à partir de ${esc(money(min.prix))} l'aller-retour (${esc(min.r.a)} → ${esc(min.r.b)}). ${champions ? `Pour ${champions} d'entre eux, ${esc(nom)} est le mois le moins cher des six prochains mois.` : ""}</p>` +
    table(["Trajet", `Aller-retour en ${nom}, dès`, "Dates repérées", "Par rapport aux autres mois"], lignes) + `</section>` : `<section><p class="bt-lead">Aucun prix n'a encore été relevé pour ${esc(moisNom(ym))}. Revenez demain : les relevés se font chaque nuit.</p></section>`) +
    (dests.length ? `<section><h2>En ${esc(nom)}, par destination</h2>${puces(dests.map((x) => [`/barometre-prix/mois/${ms}/${x.d}/`, `${x.n} en ${nom}`]))}</section>` : "") + autres
  return { path: `/barometre-prix/mois/${ms}/`, title: `Où partir en ${moisNom(ym)} pas cher : vols Europe – Afrique | Escale`, eyebrow: "Bons plans par mois", h1: `Où partir en ${moisNom(ym)}`,
    desc: `Les prix aller-retour repérés pour ${moisNom(ym)} entre l'Europe et l'Afrique, du moins cher au plus cher, avec les dates et la comparaison aux autres mois.`, body, index: liste2.length >= 3 }
}

// ---------- 3. une destination, un mois ----------
function pageDestMois(s: Snap, ms: string, ds: string): Page | null {
  const idx = MSLUG.indexOf(ms), tous = s.rows.filter((r) => slug(r.b) === ds)
  if (idx < 0 || !tous.length) return null
  const ym = ymDe(ms), nom = MOIS[idx], dest = tous[0].b
  const rows = ym ? (tous.map((r) => ({ r, m: prixDuMois(r, ym) })).filter((x) => x.m) as { r: Row; m: Month }[]).sort((x, y) => x.m.price - y.m.price) : []
  const path = `/barometre-prix/mois/${ms}/${ds}/`, titreMois = ym ? moisNom(ym) : nom
  // Mois le moins cher pour cette destination, toutes villes de départ confondues
  const tousMois = tous.flatMap((r) => r.months.map((m) => ({ r, m }))).sort((x, y) => x.m.price - y.m.price)[0]
  const lignes = rows.map(({ r, m }) => `<tr><th scope="row">${lienTrajet(r, `${r.a} → ${r.b}`)}</th><td><strong>${esc(money(m.price))}</strong></td><td>${m.dep && m.ret ? `${esc(jour(m.dep))} → ${esc(jour(m.ret))}` : "—"}</td><td>${m.transfers === 0 ? "Direct" : m.transfers === 1 ? "1 escale" : `${m.transfers} escales`}</td></tr>`)
  const autresMois = ym ? fenetre().filter((x) => x !== ym && tous.filter((r) => prixDuMois(r, x)).length >= 2) : []
  const body = (rows.length ? `<section><p class="bt-lead">Relevé du ${esc(dateFr())} : pour ${esc(dest)} en ${esc(titreMois)}, le prix aller-retour le plus bas repéré est ${esc(money(rows[0].m.price))} au départ de ${esc(rows[0].r.a)}${rows.length > 1 ? `, et ${esc(money(rows[rows.length - 1].m.price))} au départ de ${esc(rows[rows.length - 1].r.a)}` : ""}.` +
    `${tousMois ? ` En ce moment, le mois le moins cher pour ${esc(dest)} est ${esc(moisNom(tousMois.m.month))} (dès ${esc(money(tousMois.m.price))} depuis ${esc(tousMois.r.a)}).` : ""}</p>` +
    table(["Trajet", `Aller-retour en ${nom}, dès`, "Dates repérées", "Vol"], lignes) + `</section>` : `<section><p class="bt-lead">Aucun prix n'est relevé pour ${esc(dest)} en ${esc(titreMois)} pour le moment. Les relevés couvrent les 6 prochains mois et se font chaque nuit.</p></section>`) +
    (autresMois.length ? `<section><h2>${esc(dest)}, les autres mois</h2>${puces(autresMois.map((x) => [`/barometre-prix/mois/${MSLUG[Number(x.slice(5, 7)) - 1]}/${ds}/`, `${dest} en ${moisNom(x)}`]))}</section>` : "") +
    `<section><h2>Voir aussi</h2>${liste([[`/barometre-prix/mois/${ms}/`, `Tous les trajets en ${titreMois}`], ["/barometre-prix/depuis/", "Les prix par ville de départ"], ["/barometre-prix/a-saisir/", "Les trajets à saisir aujourd'hui"]])}</section>`
  return { path, title: `Vols pour ${dest} en ${titreMois} : prix depuis ${rows.length > 1 ? `${rows.length} villes` : "l'Europe"} | Escale`, eyebrow: "Bons plans par mois", h1: `Vols pour ${dest} en ${titreMois}`,
    desc: `Les prix aller-retour repérés pour ${dest} en ${titreMois}, au départ de chaque ville relevée par Escale, avec les dates et le nombre d'escales.`, body, index: rows.length >= 2 }
}

// ---------- listes ----------
function pageListeVilles(s: Snap): Page {
  const lignes = villes(s).map(([v, n]) => { const rows = s.rows.filter((r) => slug(r.a) === v).sort((x, y) => x.price - y.price); return `<tr><th scope="row"><a href="/barometre-prix/depuis/${v}/">Depuis ${esc(n)}</a></th><td>${rows.length}</td><td><strong>${esc(money(rows[0].price))}</strong> (${esc(rows[0].b)})</td><td>${rows.filter((r) => r.level === "low").length}</td></tr>` })
  return { path: "/barometre-prix/depuis/", title: "Vols pas chers vers l'Afrique par ville de départ : prix du jour | Escale", eyebrow: "Mis à jour chaque jour", h1: "Les bons plans par ville de départ",
    desc: "Choisissez votre ville de départ : les prix aller-retour du jour vers l'Afrique et le Maghreb, du moins cher au plus cher.", index: true,
    body: `<section><p class="bt-lead">Relevé du ${esc(dateFr())} : ${s.rows.length} trajets suivis au départ de ${villes(s).length} villes d'Europe.</p>${table(["Ville de départ", "Destinations relevées", "Prix le plus bas", "Sous leur prix habituel"], lignes)}</section><section><h2>Par mois</h2>${puces(fenetre().map((ym) => [`/barometre-prix/mois/${MSLUG[Number(ym.slice(5, 7)) - 1]}/`, `Où partir en ${moisNom(ym)}`]))}</section>` }
}
function pageListeMois(s: Snap): Page {
  const lignes = fenetre().map((ym) => { const l = s.rows.map((r) => ({ r, m: prixDuMois(r, ym) })).filter((x) => x.m).sort((x, y) => x.m!.price - y.m!.price); const ms = MSLUG[Number(ym.slice(5, 7)) - 1]
    return `<tr><th scope="row"><a href="/barometre-prix/mois/${ms}/">${esc(moisNom(ym))}</a></th><td>${l.length || "—"}</td><td>${l.length ? `<strong>${esc(money(l[0].m!.price))}</strong> (${esc(l[0].r.a)} → ${esc(l[0].r.b)})` : "—"}</td></tr>` })
  return { path: "/barometre-prix/mois/", title: "Où partir pas cher, mois par mois : vols Europe – Afrique | Escale", eyebrow: "Mis à jour chaque jour", h1: "Les bons plans mois par mois",
    desc: "Pour chacun des six prochains mois, les prix aller-retour repérés entre l'Europe et l'Afrique, du moins cher au plus cher.", index: true,
    body: `<section><p class="bt-lead">Relevé du ${esc(dateFr())}. Escale suit les six prochains mois.</p>${table(["Mois", "Trajets avec un prix", "Prix le plus bas"], lignes)}</section><section><h2>Par ville de départ</h2>${puces(villes(s).map(([v, n]) => [`/barometre-prix/depuis/${v}/`, `Depuis ${n}`]))}</section>` }
}

// Autres pages écrites par le serveur à ajouter au plan (les actus, src/actus.ts)
export const AUTRES: ((ctx: Ctx) => Promise<string[]>)[] = []
// Adresses à faire connaître aux moteurs : seulement les pages qui ont assez de prix réels
export async function urls(ctx: Ctx): Promise<string[]> {
  const s = await snapshot(ctx), out = ["/barometre-prix/depuis/", "/barometre-prix/mois/"]
  for (const [v] of villes(s)) { const p = pageDepuis(s, v); if (p?.index) out.push(p.path) }
  for (const ym of fenetre()) { const ms = MSLUG[Number(ym.slice(5, 7)) - 1], p = pageMois(s, ms); if (p?.index) out.push(p.path)
    for (const [d] of destinations(s)) { const q = pageDestMois(s, ms, d); if (q?.index) out.push(q.path) } }
  for (const f of AUTRES) { try { out.push(...(await f(ctx))) } catch {} }
  return out.map((u) => "https://escale.live" + u)
}

export const onRequest = async (ctx: Ctx): Promise<Response> => {
  const path = new URL(ctx.request.url).pathname
  if (path === "/barometre-prix/plan.xml") {
    const list = await urls(ctx), day = iso(0)
    return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${list.map((u) => `<url><loc>${u}</loc><lastmod>${day}</lastmod></url>`).join("\n")}\n</urlset>\n`, { headers: { "Content-Type": "application/xml; charset=utf-8", "Cache-Control": "public, max-age=3600" } })
  }
  const m = path.match(/^\/barometre-prix\/(depuis|mois)(?:\/([a-z0-9-]+))?(?:\/([a-z0-9-]+))?\/?$/)
  if (!m) return ctx.next()
  // Adresse sans barre finale : renvoi vers l'adresse officielle
  if (!path.endsWith("/")) return Response.redirect(new URL(path + "/", ctx.request.url).toString(), 301)
  const s = await snapshot(ctx)
  const p = m[1] === "depuis" ? (m[3] ? null : m[2] ? pageDepuis(s, m[2]) : pageListeVilles(s)) : m[3] ? pageDestMois(s, m[2], m[3]) : m[2] ? pageMois(s, m[2]) : pageListeMois(s)
  return p ? shell(ctx, p) : ctx.next()
}
