import { Ctx, esc } from "./_lib/common"
import { Month, Point, cacheKey, readHistory } from "./apercu-prix"
// Accueil : les boutons « Trajets populaires » (sous le moteur) reçoivent le prix aller-retour le plus bas déjà connu
// (cache des pages trajets, sinon dernier relevé de l'historique KV, mis à jour chaque matin par releve-prix.yml).
// Rien n'est demandé à Travelpayouts ici : la page reste rapide. Prix gardés 1 heure dans le cache de Cloudflare.
const CHIP = /<b class="pr" data-r="([A-Z]{3})-([A-Z]{3})"><\/b>/g
const CACHE_S = 3600

const money = (n: number) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)

async function prices(ctx: Ctx, pairs: [string, string][]) {
  const cache = (globalThis as any).caches?.default
  const key = new Request("https://escale.live/__accueil-prix/" + new Date().toISOString().slice(0, 13))
  const hit = cache ? await cache.match(key) : null
  if (hit) return (await hit.json()) as Record<string, number>
  const since = new Date(Date.now() - 3 * 864e5).toISOString().slice(0, 10)
  const out: Record<string, number> = {}
  await Promise.all(pairs.map(async ([from, to]) => {
    const c = cache ? await cache.match(cacheKey(from, to)) : null
    const months: Month[] = c ? await c.json() : []
    if (months.length) { out[`${from}-${to}`] = Math.min(...months.map((m) => m.price)); return }
    const hist: Point[] = await readHistory(ctx, from, to)
    const last = hist[hist.length - 1]
    if (last && last[0] >= since) out[`${from}-${to}`] = last[1]
  }))
  if (cache && Object.keys(out).length) ctx.waitUntil(cache.put(key, new Response(JSON.stringify(out), { headers: { "Cache-Control": `public, max-age=${CACHE_S}` } })))
  return out
}

export const onRequest = async (ctx: Ctx) => {
  const response = await ctx.next()
  if (ctx.request.method !== "GET" || !response.ok || !(response.headers.get("content-type") || "").includes("text/html")) return response
  try {
    const html = await response.text()
    const pairs = [...html.matchAll(CHIP)].map((m) => [m[1], m[2]] as [string, string])
    const map = pairs.length ? await prices(ctx, pairs) : {}
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    return new Response(html.replace(CHIP, (all, f, t) => (map[`${f}-${t}`] ? `<b class="pr" data-r="${f}-${t}">${esc(money(map[`${f}-${t}`]))}</b>` : all)),
      { status: response.status, headers })
  } catch {
    return response
  }
}
