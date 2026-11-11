import { lot } from "./lot"
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
// Mêmes pages en anglais (/en/price-index/from/…, /en/price-index/month/…) et en italien (/it/voli-da/…, /it/voli-mese/…).
// Toutes sous des adresses déjà envoyées au serveur (run_worker_first dans wrangler.jsonc). Mise en page : une page existante de la langue.
// Données : historique KV (hist:FROM-TO) et prix par mois (mois:FROM-TO, écrit par src/apercu-prix.ts à chaque relevé).
// Une page sans assez de prix réels porte « noindex » : Google ne voit que les pages qui ont du contenu. Rien n'est inventé.
export type Row = { from: string; to: string; a: string; b: string; path: string; price: number; d7: number | null; level: "low" | "mid" | "high" | null; diff: number; median: number; best: string; months: Month[] }
type Snap = { date: string; rows: Row[] }
const CACHE_S = 3600
const iso = (daysAgo: number) => new Date(Date.now() - daysAgo * 864e5).toISOString().slice(0, 10)
const slug = (s: string) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")
// Les 6 mois couverts par les relevés (mois en cours + 5)
const fenetre = () => { const n = new Date(); return Array.from({ length: 6 }, (_, i) => new Date(Date.UTC(n.getUTCFullYear(), n.getUTCMonth() + i, 1)).toISOString().slice(0, 7)) }

function weekAgo(hist: Point[]) {
  const target = Date.parse(iso(7))
  let best: Point | null = null
  for (const p of hist) { const gap = Math.abs(Date.parse(p[0]) - target) / 864e5; if (gap <= 2 && (!best || gap < Math.abs(Date.parse(best[0]) - target) / 864e5)) best = p }
  return best ? best[1] : null
}

async function compute(env: Env): Promise<Snap> {
  const ctx: Ctx = { request: new Request("https://escale.live/__bonsplans"), env, waitUntil: () => {}, next: () => Promise.resolve(new Response(null, { status: 404 })) }
  const since = iso(2), today = iso(0)
  const L = await lot(ctx) // une seule lecture KV pour tous les trajets (src/lot.ts)
  const rows = (await Promise.all(ROUTES.map(async ([from, to, lab, path]) => {
    const hist = L.h[`${from}-${to}`] || [], saved = L.m[`${from}-${to}`] || null
    const last = hist[hist.length - 1]
    if (!last || last[0] < since) return null
    const v = verdict(hist, last[1]), w = weekAgo(hist), [a, b] = lab.split(" → ")
    // Prix par mois : seulement s'ils datent de moins de 3 jours et pour des mois pas encore passés
    const months = saved && saved.d >= since ? saved.rows.filter((m) => m.month >= today.slice(0, 7) && m.price > 0) : []
    return { from, to, a, b, path, price: last[1], d7: w ? Math.round((last[1] / w - 1) * 100) : null, level: v ? v.level : null, diff: v ? v.diff : 0, median: v ? v.median : 0, best: last[2] || "", months } as Row
  }))).filter(Boolean) as Row[]
  return { date: today, rows }
}

// Le relevé du jour est gardé à deux endroits : le cache Cloudflare (une heure, propre à chaque centre de données) et une seule
// clé KV (snap:v1, lisible partout en une opération). Les pages qui ont peu de marge (pages destination, pages trajets) lisent
// seulement ces copies avec snapshotLeger() ; le calcul complet (une lecture par trajet) est réservé aux pages de bons plans
// et à la tâche du matin.
const SNAP_KEY = "snap:v1"
const cacheReq = () => new Request("https://escale.live/__bonsplans/v4/" + new Date().toISOString().slice(0, 13))
export async function snapshot(ctx: Ctx): Promise<Snap> {
  const cache = (globalThis as any).caches?.default, key = cacheReq()
  if (cache) { const hit = await cache.match(key); if (hit) return hit.json() }
  const kv = ctx.env.ESCALE
  const garde = kv ? ((await kv.get(SNAP_KEY, "json").catch(() => null)) as (Snap & { ts?: number }) | null) : null
  const frais = garde && garde.ts && Date.now() - garde.ts < CACHE_S * 1000
  const s: Snap = frais ? { date: garde!.date, rows: garde!.rows } : await compute(ctx.env)
  if (!frais && kv && s.rows.length) ctx.waitUntil(kv.put(SNAP_KEY, JSON.stringify({ ...s, ts: Date.now() })).catch(() => {}))
  if (cache && s.rows.length) ctx.waitUntil(cache.put(key, new Response(JSON.stringify(s), { headers: { "Cache-Control": `public, max-age=${CACHE_S}` } })))
  return s
}
// Copie déjà prête du relevé (cache, sinon la clé KV si elle date de moins de 26 heures) : deux opérations au plus, jamais de calcul
export async function snapshotLeger(ctx: Ctx): Promise<Snap | null> {
  const cache = (globalThis as any).caches?.default
  if (cache) { const hit = await cache.match(cacheReq()); if (hit) return hit.json() }
  const garde = ctx.env.ESCALE ? ((await ctx.env.ESCALE.get(SNAP_KEY, "json").catch(() => null)) as (Snap & { ts?: number }) | null) : null
  return garde && garde.ts && Date.now() - garde.ts < 26 * 3600e3 ? { date: garde.date, rows: garde.rows } : null
}


// ---------- langues ----------
export type Lang = "fr" | "en" | "it"
const LANGS: Lang[] = ["fr", "en", "it"]
const CFG: Record<Lang, { loc: string; base: string; ville: string; mois: string; tpl: string; og: string; noms: string[] }> = {
  fr: { loc: "fr-FR", base: "/barometre-prix", ville: "depuis", mois: "mois", tpl: "/barometre-prix/", og: "fr_FR", noms: ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"] },
  en: { loc: "en-GB", base: "/en/price-index", ville: "from", mois: "month", tpl: "/en/price-index/", og: "en_GB", noms: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] },
  it: { loc: "it-IT", base: "/it", ville: "voli-da", mois: "voli-mese", tpl: "/it/comprare-o-aspettare/", og: "it_IT", noms: ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"] },
}
// Noms de villes qui changent selon la langue (les autres restent identiques)
const VILLES: Record<string, { en?: string; it?: string }> = { Genève: { en: "Geneva", it: "Ginevra" }, Francfort: { en: "Frankfurt", it: "Francoforte" }, Lisbonne: { en: "Lisbon", it: "Lisbona" }, Barcelone: { en: "Barcelona", it: "Barcellona" }, Montréal: { en: "Montreal" },
  Londres: { en: "London", it: "Londra" }, Milan: { it: "Milano" }, Rome: { it: "Roma" }, Bruxelles: { en: "Brussels" }, Marseille: { it: "Marsiglia" }, Lyon: { it: "Lione" }, Paris: { it: "Parigi" },
  Alger: { en: "Algiers", it: "Algeri" }, "Le Caire": { en: "Cairo", it: "Il Cairo" }, Tunis: { it: "Tunisi" }, "Addis-Abeba": { en: "Addis Ababa", it: "Addis Abeba" }, Marrakech: { en: "Marrakesh" }, Oran: { it: "Orano" }, Djerba: { it: "Gerba" },
  Tanger: { en: "Tangier", it: "Tangeri" }, Le: {}, "Le Cap": { en: "Cape Town", it: "Città del Capo" }, Maurice: { en: "Mauritius", it: "Mauritius" }, "La Réunion": { en: "Réunion", it: "Riunione" }, Yaoundé: {}, Lomé: {}, Djeddah: { en: "Jeddah", it: "Gedda" } }
const nom = (v: string, l: Lang) => (l === "fr" ? v : VILLES[v]?.[l] || v)
const money = (n: number, l: Lang) => new Intl.NumberFormat(CFG[l].loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
const mslug = (ym: string, l: Lang) => slug(CFG[l].noms[Number(ym.slice(5, 7)) - 1])
const moisSeul = (ym: string, l: Lang) => CFG[l].noms[Number(ym.slice(5, 7)) - 1]
const moisNom = (ym: string, l: Lang) => `${moisSeul(ym, l)} ${ym.slice(0, 4)}`
const jour = (d: string, l: Lang) => { const [y, m, j] = d.split("-").map(Number); return new Date(Date.UTC(y, m - 1, j)).toLocaleDateString(CFG[l].loc, { day: "numeric", month: "short", timeZone: "UTC" }) }
const dateL = (l: Lang) => new Date().toLocaleDateString(CFG[l].loc, { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Paris" })
// Adresses
const uListeVilles = (l: Lang) => `${CFG[l].base}/${CFG[l].ville}/`
const uVille = (l: Lang, v: string) => `${CFG[l].base}/${CFG[l].ville}/${slug(nom(v, l))}/`
const uListeMois = (l: Lang) => `${CFG[l].base}/${CFG[l].mois}/`
const uMois = (l: Lang, i: number) => `${CFG[l].base}/${CFG[l].mois}/${slug(CFG[l].noms[i])}/`
const uDest = (l: Lang, i: number, d: string) => `${CFG[l].base}/${CFG[l].mois}/${slug(CFG[l].noms[i])}/${slug(nom(d, l))}/`
const alts = (f: (l: Lang) => string) => Object.fromEntries(LANGS.map((l) => [l, f(l)])) as Record<Lang, string>

// ---------- textes ----------
const TX = {
  fr: { jour: "Mis à jour chaque jour", parMois: "Bons plans par mois", releve: "Relevé du", niv: { low: "Bon prix", mid: "Dans la moyenne", high: "Plutôt élevé" }, direct: "Direct", escale: (n: number) => (n === 1 ? "1 escale" : `${n} escales`),
    depuis: (v: string) => `Depuis ${v}`, ouPartir: (m: string) => `Où partir en ${m}`, en: (m: string) => `en ${m}`, destEn: (d: string, m: string) => `${d} en ${m}`, moinsCher: "Le mois le moins cher", parRapport: (p: number, m: string) => `+${p} % par rapport à ${m}`,
    thVille: ["Trajet", "Aller-retour dès", "Niveau du prix", "Sur 7 jours", "Mois le moins cher"], thMois: (m: string) => ["Trajet", `Aller-retour en ${m}, dès`, "Dates repérées", "Par rapport aux autres mois"], thDest: (m: string) => ["Trajet", `Aller-retour en ${m}, dès`, "Dates repérées", "Vol"],
    thListeV: ["Ville de départ", "Destinations relevées", "Prix le plus bas", "Sous leur prix habituel"], thListeM: ["Mois", "Trajets avec un prix", "Prix le plus bas"],
    enBref: "En bref", autresVilles: "Autres villes de départ", autresMois: "Les autres mois", parVille: "Par ville de départ", parMoisT: "Par mois", voirAussi: "Voir aussi", moisParMois: (v: string) => `Partir de ${v} mois par mois`, enMoisParDest: (m: string) => `En ${m}, par destination`, destAutres: (d: string) => `${d}, les autres mois`,
    methT: "D'où viennent ces prix", meth: "Chaque nuit, Escale relève le prix aller-retour le plus bas des 6 prochains mois pour les grands trajets entre l'Europe et l'Afrique, auprès de dizaines de compagnies et d'agences. Cette page se met à jour toute seule à partir de ces relevés. Les prix sont indicatifs, par personne : le tarif exact dépend des dates et des bagages, et se confirme sur le site de réservation.",
    vTitle: (v: string) => `Vols pas chers depuis ${v} vers l'Afrique : prix du jour | Escale`, vH1: (v: string) => `Vols pas chers au départ de ${v}`, vDesc: (v: string, n: number) => `Les prix aller-retour du jour au départ de ${v} vers ${n} destinations d'Afrique et du Maghreb, du moins cher au plus cher, avec le mois le moins cher de chaque trajet.`,
    vLead: (d: string, n: number, v: string, p1: string, b1: string, p2: string, b2: string, k: number) => `Relevé du ${d} : ${n} destination${n > 1 ? "s" : ""} au départ de ${v}, de ${p1} (${b1}) à ${p2} (${b2}) l'aller-retour.${k ? ` ${k} ${k > 1 ? "sont" : "est"} sous ${k > 1 ? "leur" : "son"} prix habituel.` : ""}`,
    q1: (v: string) => `Quel est le vol le moins cher au départ de ${v} vers l'Afrique ?`, r1: (d: string, t: string, p: string) => `Au relevé du ${d}, c'est ${t}, à partir de ${p} l'aller-retour.`,
    q2: (v: string) => `Quels trajets au départ de ${v} sont de bonnes affaires aujourd'hui ?`, r2item: (t: string, p: string, x: number) => `${t} (${p}, ${x} % sous son prix habituel)`, r2none: "Aucun n'est nettement sous son prix habituel aujourd'hui. Une alerte prix sur la page du trajet prévient quand ça baisse.",
    q3: (v: string) => `Quel mois partir de ${v} pour payer moins cher ?`, r3: (m: string, k: number, n: number) => `En ce moment, ${m} est le mois le moins cher pour ${k} des ${n} destinations relevées. Le mois le moins cher de chaque trajet est indiqué dans le tableau.`,
    mTitle: (m: string) => `Où partir en ${m} pas cher : vols Europe – Afrique | Escale`, mH1: (m: string) => `Où partir en ${m}`, mDesc: (m: string) => `Les prix aller-retour repérés pour ${m} entre l'Europe et l'Afrique, du moins cher au plus cher, avec les dates et la comparaison aux autres mois.`,
    mLead: (d: string, n: number, m: string, p: string, t: string, c: number, ms: string) => `Relevé du ${d} : ${n} trajet${n > 1 ? "s" : ""} avec un prix repéré pour ${m}, à partir de ${p} l'aller-retour (${t}).${c ? ` Pour ${c} d'entre eux, ${ms} est le mois le moins cher des six prochains mois.` : ""}`,
    mVide: (m: string) => `Aucun prix n'a encore été relevé pour ${m}. Revenez demain : les relevés se font chaque nuit.`, mHors: (m: string) => `Les relevés d'Escale couvrent les 6 prochains mois. Les prix pour ${m} apparaîtront ici dès que ce mois entrera dans cette période.`, mHorsDesc: (m: string) => `Les prix pour ${m} ne sont pas encore relevés : Escale suit les 6 prochains mois. Voici les mois disponibles.`,
    dTitle: (d: string, m: string, n: number) => `Vols pour ${d} en ${m} : prix depuis ${n > 1 ? `${n} villes` : "l'Europe"} | Escale`, dH1: (d: string, m: string) => `Vols pour ${d} en ${m}`, dDesc: (d: string, m: string) => `Les prix aller-retour repérés pour ${d} en ${m}, au départ de chaque ville relevée par Escale, avec les dates et le nombre d'escales.`,
    dLead: (dt: string, d: string, m: string, p1: string, v1: string, p2: string, v2: string) => `Relevé du ${dt} : pour ${d} en ${m}, le prix aller-retour le plus bas repéré est ${p1} au départ de ${v1}${p2 ? `, et ${p2} au départ de ${v2}` : ""}.`, dBest: (d: string, m: string, p: string, v: string) => ` En ce moment, le mois le moins cher pour ${d} est ${m} (dès ${p} depuis ${v}).`,
    dVide: (d: string, m: string) => `Aucun prix n'est relevé pour ${d} en ${m} pour le moment. Les relevés couvrent les 6 prochains mois et se font chaque nuit.`, tousEn: (m: string) => `Tous les trajets en ${m}`, lienVilles: "Les prix par ville de départ", lienSaisir: "Les trajets à saisir aujourd'hui",
    lvTitle: "Vols pas chers vers l'Afrique par ville de départ : prix du jour | Escale", lvH1: "Les bons plans par ville de départ", lvDesc: "Choisissez votre ville de départ : les prix aller-retour du jour vers l'Afrique et le Maghreb, du moins cher au plus cher.", lvLead: (d: string, n: number, v: number) => `Relevé du ${d} : ${n} trajets suivis au départ de ${v} villes d'Europe.`,
    lmTitle: "Où partir pas cher, mois par mois : vols Europe – Afrique | Escale", lmH1: "Les bons plans mois par mois", lmDesc: "Pour chacun des six prochains mois, les prix aller-retour repérés entre l'Europe et l'Afrique, du moins cher au plus cher.", lmLead: (d: string) => `Relevé du ${d}. Escale suit les six prochains mois.` },
  en: { jour: "Updated daily", parMois: "Deals by month", releve: "Data as of", niv: { low: "Good price", mid: "Typical", high: "On the high side" }, direct: "Direct", escale: (n: number) => (n === 1 ? "1 stop" : `${n} stops`),
    depuis: (v: string) => `From ${v}`, ouPartir: (m: string) => `Where to go in ${m}`, en: (m: string) => `in ${m}`, destEn: (d: string, m: string) => `${d} in ${m}`, moinsCher: "The cheapest month", parRapport: (p: number, m: string) => `+${p}% compared with ${m}`,
    thVille: ["Route", "Round trip from", "Price level", "Over 7 days", "Cheapest month"], thMois: (m: string) => ["Route", `Round trip in ${m}, from`, "Dates found", "Compared with other months"], thDest: (m: string) => ["Route", `Round trip in ${m}, from`, "Dates found", "Flight"],
    thListeV: ["Departure city", "Destinations tracked", "Lowest fare", "Below usual price"], thListeM: ["Month", "Routes with a fare", "Lowest fare"],
    enBref: "In short", autresVilles: "Other departure cities", autresMois: "Other months", parVille: "By departure city", parMoisT: "By month", voirAussi: "See also", moisParMois: (v: string) => `Flying from ${v}, month by month`, enMoisParDest: (m: string) => `In ${m}, by destination`, destAutres: (d: string) => `${d}, other months`,
    methT: "Where these fares come from", meth: "Every night, Escale records the lowest round-trip fare over the next 6 months for the main routes between Europe and Africa, across dozens of airlines and agencies. This page updates itself from those records. Fares are indicative, per person: the exact fare depends on dates and baggage, and is confirmed on the booking site.",
    vTitle: (v: string) => `Cheap flights from ${v} to Africa: today's fares | Escale`, vH1: (v: string) => `Cheap flights from ${v}`, vDesc: (v: string, n: number) => `Today's round-trip fares from ${v} to ${n} destinations in Africa and the Maghreb, cheapest first, with the cheapest month for each route.`,
    vLead: (d: string, n: number, v: string, p1: string, b1: string, p2: string, b2: string, k: number) => `Data as of ${d}: ${n} destination${n > 1 ? "s" : ""} from ${v}, from ${p1} (${b1}) to ${p2} (${b2}) round trip.${k ? ` ${k} ${k > 1 ? "are" : "is"} below ${k > 1 ? "their" : "its"} usual price.` : ""}`,
    q1: (v: string) => `What is the cheapest flight from ${v} to Africa?`, r1: (d: string, t: string, p: string) => `As of ${d}, it is ${t}, from ${p} round trip.`,
    q2: (v: string) => `Which routes from ${v} are good deals today?`, r2item: (t: string, p: string, x: number) => `${t} (${p}, ${x}% below its usual price)`, r2none: "None is clearly below its usual price today. A price alert on the route page tells you when it drops.",
    q3: (v: string) => `Which month is cheapest to fly from ${v}?`, r3: (m: string, k: number, n: number) => `Right now, ${m} is the cheapest month for ${k} of the ${n} destinations tracked. The cheapest month for each route is shown in the table.`,
    mTitle: (m: string) => `Where to go in ${m} on a budget: Europe – Africa flights | Escale`, mH1: (m: string) => `Where to go in ${m}`, mDesc: (m: string) => `Round-trip fares found for ${m} between Europe and Africa, cheapest first, with dates and a comparison with other months.`,
    mLead: (d: string, n: number, m: string, p: string, t: string, c: number, ms: string) => `Data as of ${d}: ${n} route${n > 1 ? "s" : ""} with a fare found for ${m}, from ${p} round trip (${t}).${c ? ` For ${c} of them, ${ms} is the cheapest of the next six months.` : ""}`,
    mVide: (m: string) => `No fare has been recorded for ${m} yet. Check back tomorrow: fares are recorded every night.`, mHors: (m: string) => `Escale's records cover the next 6 months. Fares for ${m} will appear here once that month enters this window.`, mHorsDesc: (m: string) => `Fares for ${m} are not recorded yet: Escale tracks the next 6 months. Here are the months available.`,
    dTitle: (d: string, m: string, n: number) => `Flights to ${d} in ${m}: fares from ${n > 1 ? `${n} cities` : "Europe"} | Escale`, dH1: (d: string, m: string) => `Flights to ${d} in ${m}`, dDesc: (d: string, m: string) => `Round-trip fares found for ${d} in ${m}, from each departure city tracked by Escale, with dates and number of stops.`,
    dLead: (dt: string, d: string, m: string, p1: string, v1: string, p2: string, v2: string) => `Data as of ${dt}: for ${d} in ${m}, the lowest round-trip fare found is ${p1} from ${v1}${p2 ? `, and ${p2} from ${v2}` : ""}.`, dBest: (d: string, m: string, p: string, v: string) => ` Right now, the cheapest month for ${d} is ${m} (from ${p} out of ${v}).`,
    dVide: (d: string, m: string) => `No fare is recorded for ${d} in ${m} at the moment. Records cover the next 6 months and are made every night.`, tousEn: (m: string) => `All routes in ${m}`, lienVilles: "Fares by departure city", lienSaisir: "Routes worth booking today",
    lvTitle: "Cheap flights to Africa by departure city: today's fares | Escale", lvH1: "Deals by departure city", lvDesc: "Pick your departure city: today's round-trip fares to Africa and the Maghreb, cheapest first.", lvLead: (d: string, n: number, v: number) => `Data as of ${d}: ${n} routes tracked from ${v} European cities.`,
    lmTitle: "Where to go on a budget, month by month: Europe – Africa flights | Escale", lmH1: "Deals month by month", lmDesc: "For each of the next six months, the round-trip fares found between Europe and Africa, cheapest first.", lmLead: (d: string) => `Data as of ${d}. Escale tracks the next six months.` },
  it: { jour: "Aggiornato ogni giorno", parMois: "Offerte per mese", releve: "Rilevazione del", niv: { low: "Buon prezzo", mid: "Nella media", high: "Piuttosto alto" }, direct: "Diretto", escale: (n: number) => (n === 1 ? "1 scalo" : `${n} scali`),
    depuis: (v: string) => `Da ${v}`, ouPartir: (m: string) => `Dove andare a ${m}`, en: (m: string) => `a ${m}`, destEn: (d: string, m: string) => `${d} a ${m}`, moinsCher: "Il mese più economico", parRapport: (p: number, m: string) => `+${p} % rispetto a ${m}`,
    thVille: ["Tratta", "Andata e ritorno da", "Livello del prezzo", "In 7 giorni", "Mese più economico"], thMois: (m: string) => ["Tratta", `Andata e ritorno a ${m}, da`, "Date trovate", "Rispetto agli altri mesi"], thDest: (m: string) => ["Tratta", `Andata e ritorno a ${m}, da`, "Date trovate", "Volo"],
    thListeV: ["Città di partenza", "Destinazioni rilevate", "Prezzo più basso", "Sotto il prezzo abituale"], thListeM: ["Mese", "Tratte con un prezzo", "Prezzo più basso"],
    enBref: "In breve", autresVilles: "Altre città di partenza", autresMois: "Gli altri mesi", parVille: "Per città di partenza", parMoisT: "Per mese", voirAussi: "Vedi anche", moisParMois: (v: string) => `Partire da ${v}, mese per mese`, enMoisParDest: (m: string) => `A ${m}, per destinazione`, destAutres: (d: string) => `${d}, gli altri mesi`,
    methT: "Da dove vengono questi prezzi", meth: "Ogni notte Escale rileva il prezzo andata e ritorno più basso dei prossimi 6 mesi per le principali tratte tra l'Europa e l'Africa, presso decine di compagnie e agenzie. Questa pagina si aggiorna da sola a partire da queste rilevazioni. I prezzi sono indicativi, a persona: la tariffa esatta dipende dalle date e dai bagagli, e si conferma sul sito di prenotazione.",
    vTitle: (v: string) => `Voli economici da ${v} per l'Africa: prezzi di oggi | Escale`, vH1: (v: string) => `Voli economici da ${v}`, vDesc: (v: string, n: number) => `I prezzi andata e ritorno di oggi da ${v} verso ${n} destinazioni in Africa e nel Maghreb, dal più economico al più caro, con il mese più conveniente per ogni tratta.`,
    vLead: (d: string, n: number, v: string, p1: string, b1: string, p2: string, b2: string, k: number) => `Rilevazione del ${d}: ${n} destinazion${n > 1 ? "i" : "e"} da ${v}, da ${p1} (${b1}) a ${p2} (${b2}) andata e ritorno.${k ? ` ${k} ${k > 1 ? "sono" : "è"} sotto il prezzo abituale.` : ""}`,
    q1: (v: string) => `Qual è il volo più economico da ${v} per l'Africa?`, r1: (d: string, t: string, p: string) => `Alla rilevazione del ${d} è ${t}, da ${p} andata e ritorno.`,
    q2: (v: string) => `Quali tratte da ${v} sono un buon affare oggi?`, r2item: (t: string, p: string, x: number) => `${t} (${p}, ${x} % sotto il prezzo abituale)`, r2none: "Nessuna è nettamente sotto il prezzo abituale oggi. Un avviso prezzo sulla pagina della tratta ti avverte quando scende.",
    q3: (v: string) => `In quale mese conviene partire da ${v}?`, r3: (m: string, k: number, n: number) => `In questo momento ${m} è il mese più economico per ${k} delle ${n} destinazioni rilevate. Il mese più conveniente di ogni tratta è indicato nella tabella.`,
    mTitle: (m: string) => `Dove andare a ${m} spendendo poco: voli Europa – Africa | Escale`, mH1: (m: string) => `Dove andare a ${m}`, mDesc: (m: string) => `I prezzi andata e ritorno trovati per ${m} tra l'Europa e l'Africa, dal più economico al più caro, con le date e il confronto con gli altri mesi.`,
    mLead: (d: string, n: number, m: string, p: string, t: string, c: number, ms: string) => `Rilevazione del ${d}: ${n} tratt${n > 1 ? "e" : "a"} con un prezzo trovato per ${m}, da ${p} andata e ritorno (${t}).${c ? ` Per ${c} di queste, ${ms} è il mese più economico dei prossimi sei.` : ""}`,
    mVide: (m: string) => `Nessun prezzo è stato ancora rilevato per ${m}. Torna domani: le rilevazioni si fanno ogni notte.`, mHors: (m: string) => `Le rilevazioni di Escale coprono i prossimi 6 mesi. I prezzi per ${m} compariranno qui quando il mese entrerà in questo periodo.`, mHorsDesc: (m: string) => `I prezzi per ${m} non sono ancora rilevati: Escale segue i prossimi 6 mesi. Ecco i mesi disponibili.`,
    dTitle: (d: string, m: string, n: number) => `Voli per ${d} a ${m}: prezzi da ${n > 1 ? `${n} città` : "tutta Europa"} | Escale`, dH1: (d: string, m: string) => `Voli per ${d} a ${m}`, dDesc: (d: string, m: string) => `I prezzi andata e ritorno trovati per ${d} a ${m}, da ogni città di partenza rilevata da Escale, con le date e il numero di scali.`,
    dLead: (dt: string, d: string, m: string, p1: string, v1: string, p2: string, v2: string) => `Rilevazione del ${dt}: per ${d} a ${m}, il prezzo andata e ritorno più basso trovato è ${p1} da ${v1}${p2 ? `, e ${p2} da ${v2}` : ""}.`, dBest: (d: string, m: string, p: string, v: string) => ` In questo momento il mese più economico per ${d} è ${m} (da ${p} partendo da ${v}).`,
    dVide: (d: string, m: string) => `Nessun prezzo è rilevato per ${d} a ${m} per ora. Le rilevazioni coprono i prossimi 6 mesi e si fanno ogni notte.`, tousEn: (m: string) => `Tutte le tratte a ${m}`, lienVilles: "I prezzi per città di partenza", lienSaisir: "Le tratte da prendere oggi",
    lvTitle: "Voli economici per l'Africa per città di partenza: prezzi di oggi | Escale", lvH1: "Le offerte per città di partenza", lvDesc: "Scegli la tua città di partenza: i prezzi andata e ritorno di oggi per l'Africa e il Maghreb, dal più economico al più caro.", lvLead: (d: string, n: number, v: number) => `Rilevazione del ${d}: ${n} tratte seguite da ${v} città europee.`,
    lmTitle: "Dove andare spendendo poco, mese per mese: voli Europa – Africa | Escale", lmH1: "Le offerte mese per mese", lmDesc: "Per ognuno dei prossimi sei mesi, i prezzi andata e ritorno trovati tra l'Europa e l'Africa, dal più economico al più caro.", lmLead: (d: string) => `Rilevazione del ${d}. Escale segue i prossimi sei mesi.` },
}
const SAISIR: Record<Lang, string> = { fr: "/barometre-prix/a-saisir/", en: "/en/price-index/deals-today/", it: "/barometre-prix/a-saisir/" }

// ---------- éléments communs ----------
const niveau = (r: Row, l: Lang) => (r.level ? `<span class="${r.level === "low" ? "bt-down" : r.level === "high" ? "bt-up" : "bt-flat"}">${TX[l].niv[r.level]}${r.level === "low" ? ` (−${r.diff}${l === "en" ? "%" : " %"})` : ""}</span>` : `<span class="bt-na">—</span>`)
const tendance = (v: number | null, l: Lang) => (v === null ? `<span class="bt-na">—</span>` : `<span class="${v <= -3 ? "bt-down" : v >= 3 ? "bt-up" : "bt-flat"}">${v > 0 ? "+" : v < 0 ? "−" : ""}${Math.abs(v)}${l === "en" ? "%" : " %"}</span>`)
const table = (th: string[], lignes: string[]) => `<div class="bt-wrap"><table class="bt-table"><thead><tr>${th.map((h) => `<th scope="col">${esc(h)}</th>`).join("")}</tr></thead><tbody>${lignes.join("")}</tbody></table></div>`
const liste = (items: [string, string][]) => `<ul>${items.map(([u, t]) => `<li><a href="${u}">${esc(t)}</a></li>`).join("")}</ul>`
const puces = (items: [string, string][]) => `<p class="bp-puces">${items.map(([u, t]) => `<a href="${u}">${esc(t)}</a>`).join("")}</p>`
const STYLE = `<style>.bp-puces{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}.bp-puces a{padding:7px 13px;border-radius:999px;border:1px solid var(--line,#e3e7ee);background:var(--surface,#fff);text-decoration:none;font-weight:600;font-size:.92rem;color:inherit}.bp-qr dt{font-weight:700;margin-top:14px}.bp-qr dd{margin:4px 0 0;color:var(--muted,#5b6474)}</style>`
// Villes de départ et destinations (noms français, ceux des relevés)
const villes = (s: Snap) => [...new Set(s.rows.map((r) => r.a))].sort((x, y) => x.localeCompare(y, "fr"))
const destinations = (s: Snap) => [...new Set(s.rows.map((r) => r.b))]
const trajet = (r: Row, l: Lang) => `${nom(r.a, l)} → ${nom(r.b, l)}`
const lienTrajet = (r: Row, l: Lang) => `<a href="/${r.path}/">${esc(trajet(r, l))}</a>`
const prixDuMois = (r: Row, ym: string) => r.months.find((m) => m.month === ym) || null
const idx = (ym: string) => Number(ym.slice(5, 7)) - 1
const pucesVilles = (s: Snap, l: Lang, sauf = "") => puces(villes(s).filter((v) => v !== sauf).map((v) => [uVille(l, v), TX[l].depuis(nom(v, l))]))

// Liens vers ces pages, ajoutés au baromètre et à « À saisir aujourd'hui »
export const LIENS = `<section><h2>Bons plans par ville de départ et par mois</h2>${STYLE}${puces([["/barometre-prix/depuis/", "Par ville de départ"], ["/barometre-prix/mois/", "Par mois"], ["/barometre-prix/a-saisir/", "À saisir aujourd'hui"], ["/barometre-prix/actus/", "Les actus de la semaine"]])}</section>`

export type Page = { path: string; title: string; desc: string; eyebrow: string; h1: string; body: string; index: boolean; article?: boolean; lang?: Lang; alt?: Record<Lang, string> }
export async function shell(ctx: Ctx, p: Page): Promise<Response> {
  const l: Lang = p.lang || "fr"
  const base = await ctx.env.ASSETS?.fetch(new Request("https://escale.live" + CFG[l].tpl))
  if (!base || !base.ok) return ctx.next()
  const main = `<main>\n<div class="board"><div class="wrap">\n  <p class="eyebrow">${esc(p.eyebrow)}</p><h1>${esc(p.h1)}</h1><p class="hero-lead">${esc(p.desc)}</p>\n</div></div>\n<div class="wrap">\n${STYLE}${p.body}${p.article ? "" : `<section><h2>${esc(TX[l].methT)}</h2><p>${esc(TX[l].meth)}</p></section>`}</div>\n</main>`
  let html = await base.text()
  html = html.slice(0, html.indexOf("<main>")) + main + html.slice(html.indexOf("</main>") + 7)
  const hre = p.alt ? LANGS.map((x) => `<link rel="alternate" hreflang="${x}" href="https://escale.live${p.alt![x]}">`).join("") + `<link rel="alternate" hreflang="x-default" href="https://escale.live${p.alt.fr}">` : ""
  // Sélecteur de langue de l'en-tête : il pointe vers la même page dans les autres langues (et non vers celles du gabarit)
  const TITRES: Record<Lang, string> = { fr: "Français", en: "English", it: "Italiano" }
  const nav = p.alt ? `<nav class="lang-nav" aria-label="Langue / Language">${LANGS.map((x) => `<a href="${p.alt![x]}" hreflang="${x}" lang="${x}" title="${TITRES[x]}"${x === l ? ' aria-current="page"' : ""}>${x.toUpperCase()}</a>`).join("")}</nav>` : ""
  html = /<nav class="lang-nav"[\s\S]*?<\/nav>/.test(html) ? html.replace(/<nav class="lang-nav"[\s\S]*?<\/nav>/, nav) : nav ? html.replace("</div></header>", nav + "</div></header>") : html
  html = html
    .replace(/<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*/g, "")
    .replace(/<script type="application\/ld\+json">[\s\S]*?<\/script>\s*/g, "")
    .replace(/<script src="\/attendre\.js[^"]*"[^>]*><\/script>/, "")
    .replace(/<title>[^<]*<\/title>/, `<title>${esc(p.title)}</title>${p.index ? "" : '<meta name="robots" content="noindex, follow">'}${hre}`)
    .replace(/(<meta name="description" content=")[^"]*(")/, `$1${esc(p.desc)}$2`)
    .replace(/(<meta property="og:title" content=")[^"]*(")/, `$1${esc(p.title.replace(/ \| Escale$/, ""))}$2`)
    .replace(/(<meta property="og:description" content=")[^"]*(")/, `$1${esc(p.desc)}$2`)
    .replace(/(<meta property="og:url" content=")[^"]*(")/, `$1https://escale.live${p.path}$2`)
    .replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="https://escale.live${p.path}">`)
  const headers = new Headers(base.headers)
  headers.delete("content-length")
  headers.set("Cache-Control", "public, max-age=1800")
  return new Response(html, { status: 200, headers })
}

// ---------- 1. par ville de départ ----------
function pageDepuis(s: Snap, l: Lang, vs: string): Page | null {
  const ville = villes(s).find((v) => slug(nom(v, l)) === vs)
  if (!ville) return null
  const t = TX[l], rows = s.rows.filter((r) => r.a === ville).sort((x, y) => x.price - y.price), V = nom(ville, l)
  const min = rows[0], max = rows[rows.length - 1], bons = rows.filter((r) => r.level === "low")
  const lignes = rows.map((r) => `<tr><th scope="row">${lienTrajet(r, l)}</th><td><strong>${esc(money(r.price, l))}</strong></td><td>${niveau(r, l)}</td><td>${tendance(r.d7, l)}</td><td>${r.best ? esc(moisNom(r.best, l)) : "—"}</td></tr>`)
  const moisDispo = fenetre().filter((ym) => rows.some((r) => prixDuMois(r, ym)))
  const compte = new Map<string, number>()
  rows.forEach((r) => { if (r.best) compte.set(r.best, (compte.get(r.best) || 0) + 1) })
  const top = [...compte.entries()].sort((x, y) => y[1] - x[1])[0]
  const qr: [string, string][] = [[t.q1(V), t.r1(dateL(l), trajet(min, l), money(min.price, l))], [t.q2(V), bons.length ? bons.map((r) => t.r2item(trajet(r, l), money(r.price, l), r.diff)).join(" ; ") + "." : t.r2none], ...(top ? [[t.q3(V), t.r3(moisNom(top[0], l), top[1], rows.length)] as [string, string]] : [])]
  const body = `<section><p class="bt-lead">${esc(t.vLead(dateL(l), rows.length, V, money(min.price, l), nom(min.b, l), money(max.price, l), nom(max.b, l), bons.length))}</p>${table(t.thVille, lignes)}</section>` +
    `<section><h2>${esc(t.enBref)}</h2><dl class="bp-qr">${qr.map(([q, r]) => `<dt>${esc(q)}</dt><dd>${esc(r)}</dd>`).join("")}</dl></section>` +
    (moisDispo.length ? `<section><h2>${esc(t.moisParMois(V))}</h2>${puces(moisDispo.map((ym) => [uMois(l, idx(ym)), t.ouPartir(moisNom(ym, l))]))}</section>` : "") +
    `<section><h2>${esc(t.autresVilles)}</h2>${pucesVilles(s, l, ville)}</section>`
  return { lang: l, path: uVille(l, ville), alt: alts((x) => uVille(x, ville)), title: t.vTitle(V), eyebrow: t.jour, h1: t.vH1(V), desc: t.vDesc(V, rows.length), body, index: rows.length >= 2 }
}

// ---------- 2. par mois ----------
function pageMois(s: Snap, l: Lang, ms: string): Page | null {
  const i = CFG[l].noms.map(slug).indexOf(ms)
  if (i < 0) return null
  const t = TX[l], ym = fenetre().find((x) => idx(x) === i) || null, seul = CFG[l].noms[i]
  const autres = `<section><h2>${esc(t.autresMois)}</h2>${puces(fenetre().filter((x) => x !== ym).map((x) => [uMois(l, idx(x)), moisNom(x, l)]))}</section><section><h2>${esc(t.parVille)}</h2>${pucesVilles(s, l)}</section>`
  const commun = { lang: l, path: uMois(l, i), alt: alts((x) => uMois(x, i)), eyebrow: t.parMois }
  if (!ym) return { ...commun, title: t.mTitle(seul), h1: t.mH1(seul), desc: t.mHorsDesc(seul), body: `<section><p class="bt-lead">${esc(t.mHors(seul))}</p></section>` + autres, index: false }
  const M = moisNom(ym, l)
  // Mois le moins cher de chaque trajet : pris dans les mêmes prix par mois (et non dans l'historique), pour comparer ce qui est comparable
  const moinsCher = (r: Row) => r.months.reduce((a, c) => (c.price < a.price ? c : a))
  const avec = s.rows.map((r) => ({ r, m: prixDuMois(r, ym) })).filter((x) => x.m) as { r: Row; m: Month }[]
  const liste2 = avec.length ? avec.map(({ r, m }) => ({ r, prix: m.price, dep: m.dep, ret: m.ret, mini: moinsCher(r).price, mm: moinsCher(r).month })) : s.rows.filter((r) => r.best === ym).map((r) => ({ r, prix: r.price, dep: "", ret: "", mini: r.price, mm: ym }))
  liste2.sort((x, y) => x.prix - y.prix)
  const lignes = liste2.map(({ r, prix, dep, ret, mini, mm }) => `<tr><th scope="row">${lienTrajet(r, l)}</th><td><strong>${esc(money(prix, l))}</strong></td><td>${dep && ret ? `${esc(jour(dep, l))} → ${esc(jour(ret, l))}` : "—"}</td>` +
    `<td>${prix <= mini ? `<span class="bt-down">${esc(t.moinsCher)}</span>` : `<span class="bt-flat">${esc(t.parRapport(Math.round((prix / mini - 1) * 100), moisNom(mm, l)))}</span>`}</td></tr>`)
  const dests = destinations(s).map((d) => ({ d, c: avec.filter((x) => x.r.b === d).length })).filter((x) => x.c >= 2).sort((x, y) => nom(x.d, l).localeCompare(nom(y.d, l), CFG[l].loc))
  const min = liste2[0], champions = liste2.filter((x) => x.prix <= x.mini).length
  const body = (liste2.length ? `<section><p class="bt-lead">${esc(t.mLead(dateL(l), liste2.length, M, money(min.prix, l), trajet(min.r, l), champions, seul))}</p>${table(t.thMois(seul), lignes)}</section>` : `<section><p class="bt-lead">${esc(t.mVide(M))}</p></section>`) +
    (dests.length ? `<section><h2>${esc(t.enMoisParDest(seul))}</h2>${puces(dests.map((x) => [uDest(l, i, x.d), t.destEn(nom(x.d, l), seul)]))}</section>` : "") + autres
  return { ...commun, title: t.mTitle(M), h1: t.mH1(M), desc: t.mDesc(M), body, index: liste2.length >= 3 }
}

// ---------- 3. une destination, un mois ----------
function pageDestMois(s: Snap, l: Lang, ms: string, ds: string): Page | null {
  const i = CFG[l].noms.map(slug).indexOf(ms), dest = destinations(s).find((d) => slug(nom(d, l)) === ds)
  if (i < 0 || !dest) return null
  const t = TX[l], tous = s.rows.filter((r) => r.b === dest), ym = fenetre().find((x) => idx(x) === i) || null, seul = CFG[l].noms[i], D = nom(dest, l), M = ym ? moisNom(ym, l) : seul
  const rows = ym ? (tous.map((r) => ({ r, m: prixDuMois(r, ym) })).filter((x) => x.m) as { r: Row; m: Month }[]).sort((x, y) => x.m.price - y.m.price) : []
  const tousMois = tous.flatMap((r) => r.months.map((m) => ({ r, m }))).sort((x, y) => x.m.price - y.m.price)[0]
  const lignes = rows.map(({ r, m }) => `<tr><th scope="row">${lienTrajet(r, l)}</th><td><strong>${esc(money(m.price, l))}</strong></td><td>${m.dep && m.ret ? `${esc(jour(m.dep, l))} → ${esc(jour(m.ret, l))}` : "—"}</td><td>${m.transfers === 0 ? t.direct : t.escale(m.transfers)}</td></tr>`)
  const autresMois = ym ? fenetre().filter((x) => x !== ym && tous.filter((r) => prixDuMois(r, x)).length >= 2) : []
  const der = rows[rows.length - 1]
  const body = (rows.length ? `<section><p class="bt-lead">${esc(t.dLead(dateL(l), D, M, money(rows[0].m.price, l), nom(rows[0].r.a, l), rows.length > 1 ? money(der.m.price, l) : "", rows.length > 1 ? nom(der.r.a, l) : "") + (tousMois ? t.dBest(D, moisNom(tousMois.m.month, l), money(tousMois.m.price, l), nom(tousMois.r.a, l)) : ""))}</p>${table(t.thDest(seul), lignes)}</section>` : `<section><p class="bt-lead">${esc(t.dVide(D, M))}</p></section>`) +
    (autresMois.length ? `<section><h2>${esc(t.destAutres(D))}</h2>${puces(autresMois.map((x) => [uDest(l, idx(x), dest), t.destEn(D, moisNom(x, l))]))}</section>` : "") +
    `<section><h2>${esc(t.voirAussi)}</h2>${liste([[uMois(l, i), t.tousEn(M)], [uListeVilles(l), t.lienVilles], [SAISIR[l], t.lienSaisir]])}</section>`
  return { lang: l, path: uDest(l, i, dest), alt: alts((x) => uDest(x, i, dest)), title: t.dTitle(D, M, rows.length), eyebrow: t.parMois, h1: t.dH1(D, M), desc: t.dDesc(D, M), body, index: rows.length >= 2 }
}

// ---------- listes ----------
function pageListeVilles(s: Snap, l: Lang): Page {
  const t = TX[l]
  const lignes = villes(s).map((v) => { const rows = s.rows.filter((r) => r.a === v).sort((x, y) => x.price - y.price); return `<tr><th scope="row"><a href="${uVille(l, v)}">${esc(t.depuis(nom(v, l)))}</a></th><td>${rows.length}</td><td><strong>${esc(money(rows[0].price, l))}</strong> (${esc(nom(rows[0].b, l))})</td><td>${rows.filter((r) => r.level === "low").length}</td></tr>` })
  return { lang: l, path: uListeVilles(l), alt: alts(uListeVilles), title: t.lvTitle, eyebrow: t.jour, h1: t.lvH1, desc: t.lvDesc, index: true,
    body: `<section><p class="bt-lead">${esc(t.lvLead(dateL(l), s.rows.length, villes(s).length))}</p>${table(t.thListeV, lignes)}</section><section><h2>${esc(t.parMoisT)}</h2>${puces(fenetre().map((ym) => [uMois(l, idx(ym)), t.ouPartir(moisNom(ym, l))]))}</section>` }
}
function pageListeMois(s: Snap, l: Lang): Page {
  const t = TX[l]
  const lignes = fenetre().map((ym) => { const x = s.rows.map((r) => ({ r, m: prixDuMois(r, ym) })).filter((y) => y.m).sort((a, b) => a.m!.price - b.m!.price)
    return `<tr><th scope="row"><a href="${uMois(l, idx(ym))}">${esc(moisNom(ym, l))}</a></th><td>${x.length || "—"}</td><td>${x.length ? `<strong>${esc(money(x[0].m!.price, l))}</strong> (${esc(trajet(x[0].r, l))})` : "—"}</td></tr>` })
  return { lang: l, path: uListeMois(l), alt: alts(uListeMois), title: t.lmTitle, eyebrow: t.jour, h1: t.lmH1, desc: t.lmDesc, index: true,
    body: `<section><p class="bt-lead">${esc(t.lmLead(dateL(l)))}</p>${table(t.thListeM, lignes)}</section><section><h2>${esc(t.parVille)}</h2>${pucesVilles(s, l)}</section>` }
}

// Autres pages écrites par le serveur à ajouter au plan (les actus, src/actus.ts)
export const AUTRES: ((ctx: Ctx) => Promise<string[]>)[] = []
// Adresses à faire connaître aux moteurs : seulement les pages qui ont assez de prix réels, dans les trois langues
export async function urls(ctx: Ctx): Promise<string[]> {
  const s = await snapshot(ctx), out: string[] = []
  for (const l of LANGS) {
    out.push(uListeVilles(l), uListeMois(l))
    for (const v of villes(s)) { const p = pageDepuis(s, l, slug(nom(v, l))); if (p?.index) out.push(p.path) }
    for (const ym of fenetre()) { const ms = mslug(ym, l), p = pageMois(s, l, ms); if (p?.index) out.push(p.path)
      for (const d of destinations(s)) { const q = pageDestMois(s, l, ms, slug(nom(d, l))); if (q?.index) out.push(q.path) } }
  }
  for (const f of AUTRES) { try { out.push(...(await f(ctx))) } catch {} }
  return out.map((u) => "https://escale.live" + u)
}

// Adresses servies par ce module (à tester avant les autres pages du même préfixe)
export const ROUTE = /^\/(?:barometre-prix\/(?:depuis|mois)|en\/price-index\/(?:from|month)|it\/(?:voli-da|voli-mese))(?:\/|$)/

export const onRequest = async (ctx: Ctx): Promise<Response> => {
  const path = new URL(ctx.request.url).pathname
  if (path === "/barometre-prix/plan.xml") {
    const list = await urls(ctx), day = iso(0)
    return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${list.map((u) => `<url><loc>${u}</loc><lastmod>${day}</lastmod></url>`).join("\n")}\n</urlset>\n`, { headers: { "Content-Type": "application/xml; charset=utf-8", "Cache-Control": "public, max-age=3600" } })
  }
  let hit: { l: Lang; ville: boolean; a?: string; b?: string } | null = null
  for (const l of LANGS) {
    const base = CFG[l].base.replace(/\//g, "\\/"), m = path.match(new RegExp(`^${base}\\/(${CFG[l].ville}|${CFG[l].mois})(?:\\/([a-z0-9-]+))?(?:\\/([a-z0-9-]+))?\\/?$`))
    if (m) { hit = { l, ville: m[1] === CFG[l].ville, a: m[2], b: m[3] }; break }
  }
  if (!hit) return ctx.next()
  // Adresse sans barre finale : renvoi vers l'adresse officielle
  if (!path.endsWith("/")) return Response.redirect(new URL(path + "/", ctx.request.url).toString(), 301)
  const s = await snapshot(ctx), { l } = hit
  // Relevés illisibles pour l'instant (quota de lectures atteint, panne) : « réessayez plus tard » plutôt que « page introuvable »,
  // pour que Google ne retire pas ces pages de son index
  if (!s.rows.length) return new Response("Relevés momentanément indisponibles. Réessayez dans une heure.", { status: 503, headers: { "Retry-After": "3600", "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" } })
  const p = hit.ville ? (hit.b ? null : hit.a ? pageDepuis(s, l, hit.a) : pageListeVilles(s, l)) : hit.b ? pageDestMois(s, l, hit.a!, hit.b) : hit.a ? pageMois(s, l, hit.a) : pageListeMois(s, l)
  return p ? shell(ctx, p) : ctx.next()
}
