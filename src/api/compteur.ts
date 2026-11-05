import { Ctx, json, edgeCached } from "../_lib/common"
// Compteur public de l'accueil : nombre de recherches et comparaisons lancées sur Escale ces 7 derniers jours
// (somme des clics anonymes vers le moteur et les sites partenaires, voir api/clic.ts). Gardé 1 heure.
// Seul un total est rendu : ni détail, ni donnée personnelle (le compteur n'en enregistre aucune).
const SEARCH = /^(moteur-|aviasales|trajet-populaire|tripcom|stay22|skyscanner|kayak|momondo|booking|agoda|klook|tp-media|economybookings|airalo|kiwitaxi|compensair)/
export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 3600, async () => {
  const env = ctx.env
  if (!env.ESCALE) return json({ available: false })
  const days = [...Array(7).keys()].map((i) => new Date(Date.now() - i * 864e5).toISOString().slice(0, 10))
  const rows = await Promise.all(days.map((d) => env.ESCALE.get("clics:" + d, "json") as Promise<Record<string, number> | null>))
  let n = 0
  rows.forEach((day) => { if (day) for (const [id, v] of Object.entries(day)) if (SEARCH.test(id.split("|")[0])) n += v })
  return json({ available: true, week: n })
})
