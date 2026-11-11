import { Ctx, Env } from "./_lib/common"
import { ROUTES } from "./barometre"
import { Point, Saved, readHistory, readMonths } from "./apercu-prix"
// Copie groupée des relevés des trajets suivis (historique des 70 derniers jours + prix par mois), dans UNE clé KV (lot:v1).
// Pourquoi : le baromètre, « à saisir », l'indice, les bons plans et l'accueil lisaient chacun une clé par trajet (90 à 180 lectures
// par calcul, refait chaque heure dans chaque centre Cloudflare) ; le 11 novembre 2026, le plafond gratuit de 100 000 lectures par
// jour a été dépassé. Avec cette copie, un calcul coûte une lecture.
// Les relevés ne changent qu'entre 3 h et 6 h UTC (src/releve.ts) : la copie est refaite par la tâche de 6 h UTC (src/worker.ts)
// et reste valable jusqu'au lendemain 6 h. (Depuis le 11 novembre 2026, chaque envoi sur GitHub publie le site tout seul : .github/workflows/deploiement.yml.) Si la tâche n'a pas tourné, la première visite après 6 h la refait.
export type Lot = { ts: number; h: Record<string, Point[]>; m: Record<string, Saved | null> }
const KEY = "lot:v1", GARDE = 70
const cacheReq = () => new Request("https://escale.live/__lot/v1/" + new Date().toISOString().slice(0, 13))
// Dernier « 6 h UTC » passé : une copie plus ancienne est à refaire
const limite = (now = Date.now()) => { const d = new Date(now), six = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), 6); return now >= six ? six : six - 864e5 }

export async function buildLot(env: Env): Promise<Lot> {
  const ctx: Ctx = { request: new Request("https://escale.live/__lot"), env, waitUntil: () => {}, next: () => Promise.resolve(new Response(null, { status: 404 })) }
  const lot: Lot = { ts: Date.now(), h: {}, m: {} }
  await Promise.all(ROUTES.map(async ([from, to]) => {
    const [hist, saved] = await Promise.all([readHistory(ctx, from, to), readMonths(env, from, to)])
    lot.h[`${from}-${to}`] = hist.slice(-GARDE); lot.m[`${from}-${to}`] = saved
  }))
  // On n'enregistre pas une copie vide (lectures refusées, quota atteint) : elle masquerait les vrais relevés toute la journée
  if ((env as any).ESCALE && Object.values(lot.h).some((h) => h.length)) await (env as any).ESCALE.put(KEY, JSON.stringify(lot)).catch(() => {})
  return lot
}

// Mémoire du processus : une copie déjà lue sert aux visites suivantes (10 minutes), et deux calculs lancés par la même page
// (accueil : offres + prix populaires + petits prix) partagent la même lecture au lieu de la refaire chacun.
let memo: { l: Lot; at: number } | null = null, enCours: Promise<Lot> | null = null
const plein = (l: Lot | null | undefined) => !!l && Object.values(l.h).some((h) => h.length)
export async function lot(ctx: Ctx): Promise<Lot> {
  if (memo && Date.now() - memo.at < 600e3 && (memo.l.ts >= limite() || !plein(memo.l))) return memo.l
  if (enCours) return enCours
  enCours = (async () => {
    const cache = (globalThis as any).caches?.default, key = cacheReq()
    if (cache) { const hit = await cache.match(key).catch(() => null); if (hit) return (await hit.json()) as Lot }
    const kv = (ctx.env as any).ESCALE
    const garde = kv ? ((await kv.get(KEY, "json").catch(() => null)) as Lot | null) : null
    let l = garde && garde.ts >= limite() ? garde : await buildLot(ctx.env)
    if (!plein(l) && plein(garde)) l = garde as Lot // lectures refusées : on garde la copie de la veille plutôt que rien
    if (cache && plein(l)) ctx.waitUntil(cache.put(key, new Response(JSON.stringify(l), { headers: { "Cache-Control": "public, max-age=3600" } })))
    return l
  })().then((l) => { memo = { l, at: Date.now() }; return l }).finally(() => { enCours = null })
  return enCours
}
// Historique d'un trajet : dans la copie groupée s'il est suivi, sinon lecture directe de sa clé
export async function histDe(ctx: Ctx, from: string, to: string, l?: Lot): Promise<Point[]> {
  const k = `${from}-${to}`, L = l || (await lot(ctx))
  return k in L.h ? L.h[k] : readHistory(ctx, from, to)
}
