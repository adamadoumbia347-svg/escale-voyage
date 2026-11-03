import { Ctx, json, edgeCached } from "../_lib/common"
// Taux de change de l'euro, pour afficher à côté des prix en euros un équivalent dans la monnaie du visiteur (site/fx.js).
// Source : ExchangeRate-API (open.er-api.com, gratuit, attribution affichée par fx.js), sinon la BCE (frankfurter.app).
// Le franc CFA (XOF, XAF) a une parité fixe avec l'euro. Gardé 12 heures. GET /api/fx
// Avec ?all=1 : toutes les monnaies du monde (accueil : prix affichés dans la monnaie du pays du visiteur).
const WANT = ["GBP", "USD", "CAD", "CHF", "MAD", "DZD", "TND", "EGP", "NGN", "GHS", "KES", "ZAR", "AED", "SAR", "QAR", "ETB", "RWF",
  "CDF", "GNF", "MRU", "GMD", "CVE", "AOA", "MZN", "TZS", "UGX", "SEK", "NOK", "DKK", "PLN", "TRY", "BRL", "HTG"]
const CFA = 655.957

export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 43200, async () => {
  const all = new URL(ctx.request.url).searchParams.get("all") === "1"
  const pick = (r: Record<string, number>) => {
    const out: Record<string, number> = { XOF: CFA, XAF: CFA }
    for (const c of all ? Object.keys(r) : WANT) if (/^[A-Z]{3}$/.test(c) && c !== "XOF" && c !== "XAF" && typeof r[c] === "number" && r[c] > 0) out[c] = r[c]
    return out
  }
  try {
    const r = await fetch("https://open.er-api.com/v6/latest/EUR")
    if (r.ok) {
      const d: any = await r.json()
      if (d?.result === "success" && d.rates?.USD) return json({ base: "EUR", source: "er-api", updated: d.time_last_update_utc || null, rates: pick(d.rates) })
    }
  } catch (_) { /* source de secours */ }
  try {
    const r = await fetch("https://api.frankfurter.app/latest?from=EUR")
    if (r.ok) {
      const d: any = await r.json()
      if (d?.rates?.USD) return json({ base: "EUR", source: "ecb", updated: d.date || null, rates: pick(d.rates) })
    }
  } catch (_) { /* rien */ }
  return json({ base: "EUR", source: "fixed", updated: null, rates: { XOF: CFA, XAF: CFA } })
})
