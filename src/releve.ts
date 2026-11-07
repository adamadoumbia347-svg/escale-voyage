import { Ctx, Env } from "./_lib/common"
import { ROUTES } from "./barometre"
import { cacheKey, routeMonths } from "./apercu-prix"
// Relevé quotidien des prix, fait par Cloudflare lui-même (avant : .github/workflows/releve-prix.yml, qui ouvrait chaque page).
// Pour chaque trajet du baromètre : on vide le cache du trajet, puis routeMonths() redemande les prix des 6 prochains mois
// à Travelpayouts, remet le cache à jour et ajoute le prix du jour à l'historique KV (baromètre, indice, verdict « bon prix »).
// Une exécution ne peut pas faire plus d'une cinquantaine d'appels réseau (formule gratuite) : le travail est découpé
// en tranches de 5 trajets, une toutes les 10 minutes entre 3 h et 6 h UTC (voir « crons » dans wrangler.jsonc).
export const PER_RUN = 5
export const SLOT_MIN = 10
export const START_HOUR = 3

export function sliceFor(date: Date): number {
  return Math.floor(((date.getUTCHours() - START_HOUR) * 60 + date.getUTCMinutes()) / SLOT_MIN)
}

export async function releve(env: Env, when = new Date()) {
  const slice = sliceFor(when)
  const routes = ROUTES.slice(slice * PER_RUN, slice * PER_RUN + PER_RUN)
  if (slice < 0 || !routes.length || !env.TRAVELPAYOUTS_TOKEN) return { slice, trajets: 0 }
  const pending: Promise<any>[] = []
  const ctx: Ctx = {
    request: new Request("https://escale.live/__releve"), env,
    waitUntil: (p) => { pending.push(p) },
    next: () => Promise.resolve(new Response(null, { status: 404 })),
  }
  const cache = (globalThis as any).caches?.default
  const out: string[] = []
  for (const [from, to] of routes) {
    try {
      if (cache) await cache.delete(cacheKey(from, to))
      const rows = await routeMonths(ctx, from, to)
      out.push(`${from}-${to}:${rows === null ? "indisponible" : rows.length ? Math.min(...rows.map((r) => r.price)) : "aucun prix"}`)
    } catch (e) { out.push(`${from}-${to}:erreur`) }
  }
  await Promise.allSettled(pending)
  return { slice, trajets: routes.length, prix: out }
}
