import { lot, histDe } from "./lot"
import { ROUTES as BARO } from "./barometre"
import { Ctx, json, esc, IATA } from "./_lib/common"
import { Month, Point, cacheKey, readHistory } from "./apercu-prix"
import { banner, deals, Deals } from "./saisir"
import { ANIM } from "./accueil-anim"
import { dernier } from "./actus"
import { snapshotLeger } from "./bonsplans"
// Accueil : les boutons « Trajets populaires » (sous le moteur) reçoivent le prix aller-retour le plus bas déjà connu
// (cache des pages trajets, sinon dernier relevé de l'historique KV, mis à jour chaque nuit par src/releve.ts)
// et une flèche de tendance sur 7 jours (↓ baisse, ↑ hausse, à partir de 3 %).
// Rien n'est demandé à Travelpayouts ici : la page reste rapide (jamais plus de 400 ms d'attente). Prix gardés 1 heure dans le cache de Cloudflare.
// GET /api/connus?r=CDG-DSS,ORY-CMN : mêmes prix, pour le bloc « Vos trajets » (trajets consultés, gardés dans le navigateur).
const CHIP = /<b class="pr" data-r="([A-Z]{3})-([A-Z]{3})"><\/b>/g
const CACHE_S = 3600
const WAIT_MS = 400
type Known = { price: number; d7: number | null }

const money = (n: number) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
const iso = (daysAgo: number) => new Date(Date.now() - daysAgo * 864e5).toISOString().slice(0, 10)

// Prix relevé il y a environ 7 jours (à ± 2 jours), pour la tendance
function weekAgo(hist: Point[]) {
  const target = Date.parse(iso(7))
  let best: Point | null = null
  for (const p of hist) {
    const gap = Math.abs(Date.parse(p[0]) - target) / 864e5
    if (gap <= 2 && (!best || gap < Math.abs(Date.parse(best[0]) - target) / 864e5)) best = p
  }
  return best ? best[1] : null
}

export async function knownPrices(ctx: Ctx, pairs: [string, string][]) {
  const cache = (globalThis as any).caches?.default
  const since = iso(3)
  const out: Record<string, Known> = {}
  const L = await lot(ctx).catch(() => undefined) // trajets suivis : une seule lecture KV (src/lot.ts)
  await Promise.all(pairs.map(async ([from, to]) => {
    const c = cache ? await cache.match(cacheKey(from, to)) : null
    const months: Month[] = c ? await c.json() : []
    const hist: Point[] = await histDe(ctx, from, to, L)
    const last = hist[hist.length - 1]
    const price = months.length ? Math.min(...months.map((m) => m.price)) : last && last[0] >= since ? last[1] : null
    if (!price) return
    const w = weekAgo(hist)
    out[`${from}-${to}`] = { price, d7: w ? Math.round((price / w - 1) * 100) : null }
  }))
  return out
}

async function homePrices(ctx: Ctx, pairs: [string, string][]) {
  const cache = (globalThis as any).caches?.default
  const key = new Request("https://escale.live/__accueil-prix/v2/" + new Date().toISOString().slice(0, 13))
  const hit = cache ? await cache.match(key) : null
  if (hit) return (await hit.json()) as Record<string, Known>
  const job = knownPrices(ctx, pairs).then((out) => {
    if (cache && Object.keys(out).length) return cache.put(key, new Response(JSON.stringify(out), { headers: { "Cache-Control": `public, max-age=${CACHE_S}` } })).then(() => out)
    return out
  })
  ctx.waitUntil(job.catch(() => {}))
  // La page part au plus tard après WAIT_MS : sans prix cette fois, avec prix pour les visiteurs suivants (cache rempli en arrière-plan)
  return (await Promise.race([job, new Promise<null>((ok) => setTimeout(() => ok(null), WAIT_MS))])) || {}
}

const arrow = (d: number | null) => d === null || Math.abs(d) < 3 ? "" : d < 0 ? ` <i class="tr dn" title="${-d} % en 7 jours">↓</i>` : ` <i class="tr up" title="+${d} % en 7 jours">↑</i>`

// « Offres du jour » au-dessus du titre : les trajets les plus en dessous de leur prix habituel (src/saisir.ts), un à la fois.
// Les jours sans bonne affaire, les plus petits prix des trajets populaires prennent la place. Rien n'est affiché sans prix réel.
type Offre = { label: string; price: number; diff: number | null; href: string }
// Pays des aéroports de départ relevés chaque nuit : les offres au départ du pays du visiteur passent en premier
const PAYS_DEPART: Record<string, string> = { CDG: "FR", ORY: "FR", LYS: "FR", MRS: "FR", BRU: "BE", LHR: "GB", MXP: "IT", FCO: "IT",
  GVA: "CH", MAD: "ES", BCN: "ES", FRA: "DE", LIS: "PT", YUL: "CA" }
// Pays où Escale suit des départs : le visiteur n'y voit que les offres au départ de son pays (demande de Dobam, 11 novembre 2026).
// Ailleurs (Suisse, Espagne, Afrique…), toutes les offres restent affichées.
const PAYS_SUIVIS = new Set(Object.values(PAYS_DEPART))
function offres(d: Deals | null, map: Record<string, Known>, html: string, pays = "", petits: Offre[] = []): string {
  // « local » : on a de quoi montrer quelque chose pour ce pays (une offre ou un petit prix) ; sinon toutes les offres, comme ailleurs
  const local = PAYS_SUIVIS.has(pays) && (petits.length > 0 || (d?.items || []).some((r) => PAYS_DEPART[r.from] === pays))
  let list: Offre[] = (d?.items || []).filter((r) => !local || PAYS_DEPART[r.from] === pays).sort((a, b) => b.diff - a.diff).slice(0, 5)
    .map((r) => ({ label: r.label, price: r.price, diff: r.diff, href: `/?type=vols&from=${r.from}&to=${r.to}` }))
  const deal = list.length > 0
  // Aucune offre au départ de ce pays aujourd'hui : ses petits prix du jour (relevé de la nuit), sans pourcentage
  if (!deal && local && petits.length) list = petits
  else if (!deal) {
    list = [...html.matchAll(/<span>([^<]+)<\/span><b class="pr" data-r="([A-Z]{3})-([A-Z]{3})">/g)]
      .map((m) => ({ label: m[1], k: map[`${m[2]}-${m[3]}`], from: m[2], to: m[3] })).filter((x) => x.k)
      .sort((a, b) => a.k.price - b.k.price).slice(0, 4)
      .map((x) => ({ label: x.label, price: x.k.price, diff: null, href: `/?type=vols&from=${x.from}&to=${x.to}` }))
  }
  if (!list.length) return ""
  const tag = deal ? `<b data-en="🔥 Deal of the day">🔥 Offre du jour</b>` : `<b data-en="✈️ Low fare today">✈️ Petit prix du jour</b>`
  const items = list.map((o, i) => `<a href="${o.href}"${i ? "" : ' class="on"'}>${tag}<span>${esc(o.label)}</span><strong>${esc(money(o.price))}</strong>${o.diff ? `<i>−${o.diff} %</i>` : ""}</a>`).join("")
  const css = `<style>.band .hero>.hero-offres:not(.hero-bg){order:0;align-self:flex-start;margin:16px 0 -6px;max-width:100%}.hero-offres{display:grid;margin:0 0 12px}.hero-offres a{grid-area:1/1;display:flex;flex-wrap:wrap;align-items:center;gap:2px 10px;padding:9px 16px 10px;border-radius:18px;background:#fff;color:#08303a;text-decoration:none;font:700 17px/1.2 var(--f-body,system-ui);box-shadow:0 12px 32px -14px rgb(0 0 0/.6);max-width:100%;opacity:0;visibility:hidden;transform:translateY(60%);transition:transform .5s cubic-bezier(.2,.8,.2,1),opacity .4s ease,visibility .4s}.hero-offres a.on{opacity:1;visibility:visible;transform:none}.hero-offres a.out{transform:translateY(-60%)}.hero-offres b{flex:0 0 100%;font-weight:800;font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:#b45309}.hero-offres span{white-space:nowrap}.hero-offres strong{font-weight:800;font-size:19px;color:#0b8577;white-space:nowrap}.hero-offres i{font-style:normal;font-weight:800;font-size:13px;color:#fff;background:#12a150;border-radius:7px;padding:3px 7px;white-space:nowrap}@media(max-width:360px){.hero-offres a{font-size:15px;padding:8px 13px 9px}.hero-offres strong{font-size:17px}}</style>`
  const js = list.length > 1 ? `<script>(function(){var a=document.querySelectorAll(".hero-offres a"),i=0;if(a.length<2||(window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches))return;setInterval(function(){var c=a[i];i=(i+1)%a.length;var n=a[i];c.classList.remove("on");c.classList.add("out");n.classList.remove("out");void n.offsetWidth;n.classList.add("on");setTimeout(function(){c.classList.remove("out")},600)},3400)})()</script>` : ""
  return `${css}<p class="hero-offres">${items}</p>${js}`
}

export const onRequest = async (ctx: Ctx) => {
  const response = await ctx.next()
  if (ctx.request.method !== "GET" || !response.ok || !(response.headers.get("content-type") || "").includes("text/html")) return response
  try {
    const html = await response.text()
    const pairs = [...html.matchAll(CHIP)].map((m) => [m[1], m[2]] as [string, string])
    // Bandeau « trajets sous leur prix habituel » (src/saisir.ts) : jamais plus de 400 ms d'attente, sinon la page part sans lui
    const dealsJob = deals(ctx.env, ctx.waitUntil).catch(() => null)
    const [map, d] = await Promise.all([pairs.length ? homePrices(ctx, pairs) : ({} as Record<string, Known>), Promise.race([dealsJob, new Promise<null>((ok) => setTimeout(() => ok(null), WAIT_MS))])])
    if (!d) ctx.waitUntil(dealsJob)
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    let out = html.replace(CHIP, (all, f, t) => {
      const k = map[`${f}-${t}`]
      return k ? `<b class="pr" data-r="${f}-${t}">${esc(money(k.price))}${arrow(k.d7)}</b>` : all
    })
    const bn = d ? banner(d, "fr") : ""
    // Dernier article des actus de la semaine (src/actus.ts) : un lien discret au-dessus des blocs de l'accueil
    const act = await Promise.race([dernier(ctx), new Promise<null>((ok) => setTimeout(() => ok(null), WAIT_MS))])
    if (act) out = out.replace('<section class="block" id="recent-block"', `<div class="wrap mini-srv"><p style="margin:0 auto 14px;padding:10px 16px;border-radius:14px;border:1px solid var(--line,#e3e7ee);background:var(--surface,#fff);font-size:.95rem">📰 <strong>Actu de la semaine :</strong> <a href="/barometre-prix/actus/${act.slug}/">${esc(act.title)}</a></p></div><section class="block" id="recent-block"`)
    // Accueil épuré : ces deux encarts sont rangés dans la rubrique « Idées » (classe mini-srv, voir site/mini.js)
    if (bn) out = out.replace('<section class="block" id="recent-block"', '<div class="mini-srv">' + bn + '</div><section class="block" id="recent-block"')
    // Adresses de recherche (/?type=vols&from=…) : même page que l'accueil, pas à indexer (Search Console les listait par milliers
    // en « autre page avec balise canonique correcte »). La balise canonique vers / reste ; on ajoute noindex, follow.
    // Pays du visiteur (donné par Cloudflare, sans cookie) : ordre des villes du titre animé et des offres du jour
    const pays = String(((ctx.request as any).cf || {}).country || "")
    // Offres du jour juste au-dessus du titre (à la place de l'étiquette « comparateur de la diaspora »)
    // Trajets populaires (ruban sous le titre) : pour un visiteur d'un pays où Escale suit des départs (hors France, déjà la liste de départ),
    // les trajets de son pays avec leur prix du jour remplacent ceux de Paris (demande de Dobam, 11 novembre 2026)
    if (PAYS_SUIVIS.has(pays) && pays !== "FR") {
      // Villes de départ du pays à tour de rôle (Milan, Rome, Milan, Rome…) pour qu'aucune ne remplisse la liste à elle seule
      const parVille: Record<string, typeof BARO> = {}
      for (const r of BARO) if (PAYS_DEPART[r[0]] === pays) (parVille[r[0]] ||= []).push(r)
      const files = Object.values(parVille), loc: typeof BARO = []
      for (let i = 0; loc.length < 12 && files.some((f) => f[i]); i++) for (const f of files) if (f[i] && loc.length < 12) loc.push(f[i])
      const prix = await Promise.race([knownPrices(ctx, loc.map((r) => [r[0], r[1]] as [string, string])).catch(() => ({} as Record<string, Known>)), new Promise<Record<string, Known>>((ok) => setTimeout(() => ok({}), WAIT_MS))])
      const chips = loc.filter((r) => prix[`${r[0]}-${r[1]}`]).map((r) => { const k = prix[`${r[0]}-${r[1]}`]
        return `<a class="pop-chip" href="/recherche/" data-wl="${r[0]}-${r[1]}"><span>${esc(r[2])}</span><b class="pr" data-r="${r[0]}-${r[1]}">${esc(money(k.price))}${arrow(k.d7)}</b></a>` })
      // Depuis le 14 novembre 2026, ces trajets défilent sous le titre (ruban) : étiquette + trajets, écrits deux fois pour que la boucle soit continue
      const lab = (cache: boolean) => `<span class="rb-t"${cache ? ' aria-hidden="true"' : ' id="pop-hero-h"'} data-en="✈️ Popular routes, round trip from">✈️ Trajets populaires, aller-retour dès</span>`
      const tous = chips.join("")
      if (chips.length >= 2) out = out.replace(/(<div class="piste" id="pop-hero-row">)[\s\S]*?(<\/div>)/, (_m, a, z) => a + lab(false) + tous + lab(true) + tous.replace(/<a /g, '<a tabindex="-1" aria-hidden="true" ') + z)
    }
    let petits: Offre[] = []
    if (PAYS_SUIVIS.has(pays) && !(d?.items || []).some((r) => PAYS_DEPART[r.from] === pays)) {
      const snap = await Promise.race([snapshotLeger(ctx).catch(() => null), new Promise<null>((ok) => setTimeout(() => ok(null), WAIT_MS))])
      petits = (snap?.rows || []).filter((r) => PAYS_DEPART[r.from] === pays && r.price > 0).sort((x, y) => x.price - y.price).slice(0, 4)
        .map((r) => ({ label: `${r.a} → ${r.b}`, price: r.price, diff: null, href: `/?type=vols&from=${r.from}&to=${r.to}` }))
    }
    out = out.replace(/<h1 data-en-html="Cheap flights/, () => offres(d, map, html, pays, petits) + '<h1 data-en-html="Cheap flights')
    // Animation du titre (destinations qui défilent, Afrique d'abord) : la version du serveur remplace le fichier site/hero-anim.js
    out = out.replace(/<script src="\/hero-anim\.js[^"]*" defer><\/script>/, () => `<script>window.ESCALE_PAYS=${JSON.stringify(/^[A-Z]{2}$/.test(pays) ? pays : "")};document.addEventListener("DOMContentLoaded",function(){${ANIM}});</script>`)
    // Message de saison (« Noël au pays… ») posé sur la photo : fond blanc et texte foncé, lisible quelle que soit la photo
    out = out.replace("</head>", `<style>.has-hero .band .hero-season a{background:#fff;color:#08303a;border-color:transparent;-webkit-backdrop-filter:none;backdrop-filter:none;border-radius:16px;box-shadow:0 10px 30px -14px rgb(0 0 0/.5)}</style></head>`)
    // Noms du site déclarés à Google : « Escale Live » est ce que les vidéos demandent de taper
    out = out.replace('"alternateName":["Escale Comparateur","Escale Voyage"]', '"alternateName":["Escale Live","escale.live","Escale Comparateur","Escale Voyage"]')
    if (new URL(ctx.request.url).searchParams.has("type")) out = out.replace("<head>", '<head>\n<meta name="robots" content="noindex, follow">')
    return new Response(out, { status: response.status, headers })
  } catch {
    return response
  }
}

export const onRequestGet = async (ctx: Ctx) => {
  const r = (new URL(ctx.request.url).searchParams.get("r") || "").toUpperCase().split(",").slice(0, 6)
  const pairs = r.map((x) => x.split("-")).filter((p) => p.length === 2 && IATA.test(p[0]) && IATA.test(p[1])) as [string, string][]
  const out = pairs.length ? await knownPrices(ctx, pairs) : {}
  return json({ prix: out }, { headers: { "Cache-Control": "public, max-age=900" } })
}
