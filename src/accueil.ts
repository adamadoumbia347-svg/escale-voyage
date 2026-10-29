import { Ctx, json, esc, IATA } from "./_lib/common"
import { Month, Point, cacheKey, readHistory } from "./apercu-prix"
// Accueil : les boutons « Trajets populaires » (sous le moteur) reçoivent le prix aller-retour le plus bas déjà connu
// (cache des pages trajets, sinon dernier relevé de l'historique KV, mis à jour chaque matin par releve-prix.yml)
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
    const map = pairs.length ? await homePrices(ctx, pairs) : {}
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    return new Response(html.replace(CHIP, (all, f, t) => {
      const k = map[`${f}-${t}`]
      return k ? `<b class="pr" data-r="${f}-${t}">${esc(money(k.price))}${arrow(k.d7)}</b>` : all
    }), { status: response.status, headers })
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
