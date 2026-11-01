import { Ctx, json, edgeCached } from "../_lib/common"
// Taux de change de l'euro (Banque centrale européenne, via frankfurter.app) pour afficher sur les pages anglaises
// un équivalent approximatif en livres et en dollars. Gardé 12 heures. GET /api/fx
const FALLBACK = { GBP: 0.86, USD: 1.08, CAD: 1.5 }

export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 43200, async () => {
  try {
    const r = await fetch("https://api.frankfurter.app/latest?from=EUR&to=GBP,USD,CAD", { cf: { cacheTtl: 43200 } } as RequestInit)
    if (r.ok) {
      const d: any = await r.json()
      if (d?.rates?.GBP && d?.rates?.USD) return json({ base: "EUR", date: d.date, rates: d.rates })
    }
  } catch (_) { /* taux de secours ci-dessous */ }
  return json({ base: "EUR", date: null, rates: FALLBACK })
})
