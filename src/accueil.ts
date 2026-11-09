import { Ctx, json, esc, IATA } from "./_lib/common"
import { Month, Point, cacheKey, readHistory } from "./apercu-prix"
import { banner, deals } from "./saisir"
import { ANIM } from "./accueil-anim"
// Accueil : les boutons « Trajets populaires » (sous le moteur) reçoivent le prix aller-retour le plus bas déjà connu
// (cache des pages trajets, sinon dernier relevé de l'historique KV, mis à jour chaque nuit par src/releve.ts)
// et une flèche de tendance sur 7 jours (↓ baisse, ↑ hausse, à partir de 3 %).
// Rien n'est demandé à Travelpayouts ici : la page reste rapide (jamais plus de 400 ms d'attente). Prix gardés 1 heure dans le cache de Cloudflare.
// GET /api/connus?r=CDG-DSS,ORY-CMN : mêmes prix, pour le bloc « Vos trajets » (trajets consultés, gardés dans le navigateur).
const CHIP = /<b class="pr" data-r="([A-Z]{3})-([A-Z]{3})"><\/b>/g
const H1_FR = "Les billets pas chers <em>pour toutes les destinations</em></h1>"
const H1_NEW = `<span class="hero-badge" style="display:table;margin:0 0 10px;padding:6px 13px;border-radius:999px;background:rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.5);color:#fff;font-weight:700;font-size:14px;letter-spacing:0;line-height:1.2">🌍 Le comparateur de la diaspora africaine</span> Les billets pas chers <em>pour rentrer au pays</em></h1>`
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
  await Promise.all(pairs.map(async ([from, to]) => {
    const c = cache ? await cache.match(cacheKey(from, to)) : null
    const months: Month[] = c ? await c.json() : []
    const hist: Point[] = await readHistory(ctx, from, to)
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
    if (bn) out = out.replace('<section class="block" id="recent-block"', bn + '<section class="block" id="recent-block"')
    // Adresses de recherche (/?type=vols&from=…) : même page que l'accueil, pas à indexer (Search Console les listait par milliers
    // en « autre page avec balise canonique correcte »). La balise canonique vers / reste ; on ajoute noindex, follow.
    // Titre de l'accueil en français : Escale se présente comme le comparateur de la diaspora africaine. L'étiquette est dans le h1
    // (lue par Google avec le titre) ; les autres langues gardent leur titre traduit (data-en-html, site/i18n.js), et la fin du
    // titre reste animée par site/hero-anim.js (« pour rentrer au pays » → « pour Abidjan » → « pour Dakar »…).
    out = out.replace(H1_FR, H1_NEW)
    // Animation du titre (destinations qui défilent, Afrique d'abord) : la version du serveur remplace le fichier site/hero-anim.js
    out = out.replace(/<script src="\/hero-anim\.js[^"]*" defer><\/script>/, () => `<script>document.addEventListener("DOMContentLoaded",function(){${ANIM}});</script>`)
    // Message de saison (« Noël au pays… ») posé sur la photo : fond blanc et texte foncé, lisible quelle que soit la photo
    out = out.replace("</head>", `<style>.has-hero .band .hero-season a{background:#fff;color:#08303a;border-color:transparent;-webkit-backdrop-filter:none;backdrop-filter:none;border-radius:16px;box-shadow:0 10px 30px -14px rgb(0 0 0/.5)}</style></head>`)
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
