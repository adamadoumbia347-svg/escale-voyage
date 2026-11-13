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
// Copie de secours, gardée 30 heures dans le cache de chaque centre de données (hors KV, sans quota). Le 11 novembre 2026, les
// lectures KV ont été refusées de 15 h 32 UTC à minuit : les pages « bons plans » et « à saisir » ont répondu 503 et Google a
// signalé des « erreurs serveur (5xx) ». Avec cette copie, ces pages continuent d'afficher le relevé du matin (le même que
// celui de KV, puisqu'il ne change qu'entre 3 h et 6 h UTC) tant que le centre de données l'a vue dans les 30 dernières heures.
const secoursReq = () => new Request("https://escale.live/__lot/v1/secours")
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
let memo: { l: Lot; at: number; secours?: boolean } | null = null, enCours: Promise<Lot> | null = null
const plein = (l: Lot | null | undefined) => !!l && Object.values(l.h).some((h) => h.length)
export async function lot(ctx: Ctx): Promise<Lot> {
  if (memo && Date.now() - memo.at < 600e3 && (memo.l.ts >= limite() || !plein(memo.l) || memo.secours)) return memo.l
  if (enCours) return enCours
  let secours = false
  enCours = (async () => {
    const cache = (globalThis as any).caches?.default, key = cacheReq()
    if (cache) { const hit = await cache.match(key).catch(() => null); if (hit) return (await hit.json()) as Lot }
    const kv = (ctx.env as any).ESCALE
    const garde = kv ? ((await kv.get(KEY, "json").catch(() => null)) as Lot | null) : null
    let l = garde && garde.ts >= limite() ? garde : await buildLot(ctx.env)
    if (!plein(l) && plein(garde)) l = garde as Lot // lectures refusées : on garde la copie de la veille plutôt que rien
    if (!plein(l) && cache) { // KV illisible (quota du jour atteint) : copie de secours du centre de données
      const hit = await cache.match(secoursReq()).catch(() => null), s = hit ? ((await hit.json().catch(() => null)) as Lot | null) : null
      if (plein(s)) { secours = true; return s as Lot }
    }
    if (cache && plein(l)) {
      const corps = JSON.stringify(l)
      ctx.waitUntil(cache.put(key, new Response(corps, { headers: { "Cache-Control": "public, max-age=3600" } })))
      ctx.waitUntil(Promise.resolve(cache.put(secoursReq(), new Response(corps, { headers: { "Cache-Control": "public, max-age=108000" } }))).catch(() => {}))
    }
    return l
  })().then((l) => { memo = { l, at: Date.now(), secours }; return l }).finally(() => { enCours = null })
  return enCours
}
// Historique d'un trajet : dans la copie groupée s'il est suivi, sinon lecture directe de sa clé
export async function histDe(ctx: Ctx, from: string, to: string, l?: Lot): Promise<Point[]> {
  const k = `${from}-${to}`, L = l || (await lot(ctx))
  return k in L.h ? L.h[k] : readHistory(ctx, from, to)
}
