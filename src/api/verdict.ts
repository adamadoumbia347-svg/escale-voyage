import { Ctx, json, edgeCached } from "../_lib/common"
import { readHistory, verdict } from "../apercu-prix"
import { ROUTES } from "../barometre"
// « Acheter maintenant ou attendre ? » : pour chaque grand trajet du baromètre, le dernier prix relevé (le plus bas des
// 6 prochains mois), comparé à la médiane des 60 derniers jours (verdict d'apercu-prix.ts) + les 45 derniers relevés.
// GET /api/verdict — gardé 1 heure.
export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 3600, async () => {
  const items = (await Promise.all(ROUTES.map(async ([from, to, label, path]) => {
    const hist = await readHistory(ctx, from, to)
    if (!hist.length) return null
    const last = hist[hist.length - 1]
    const v = verdict(hist, last[1])
    return { from, to, label, path, price: last[1], date: last[0], month: last[2] || null, level: v ? v.level : null, diff: v ? v.diff : null,
      median: v ? v.median : null, days: v ? v.days : null, series: hist.slice(-45).map((p) => p[1]) }
  }))).filter(Boolean)
  return json({ available: items.length > 0, items })
})
