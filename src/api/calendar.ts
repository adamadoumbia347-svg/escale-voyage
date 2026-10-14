import { Ctx, json, IATA, MONTH, currencyOf, pricesForDates, edgeCached } from "../_lib/common"
// Prix aller-retour le plus bas par jour de départ sur un mois. GET /api/calendar?from=CDG&to=DSS&month=2026-11&currency=EUR
export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 10800, async () => {
  const token = ctx.env.TRAVELPAYOUTS_TOKEN
  if (!token) return json({ available: false })
  const q = new URL(ctx.request.url).searchParams
  const from = (q.get("from") || "").toUpperCase(), to = (q.get("to") || "").toUpperCase(), month = q.get("month") || ""
  let currency = currencyOf(q.get("currency"))
  if (!IATA.test(from) || !IATA.test(to) || !MONTH.test(month)) return json({ error: "Paramètres invalides" }, { status: 400 })
  const ask = (cur: string) => pricesForDates(token, { origin: from, destination: to, departure_at: month, one_way: "false", unique: "false", sorting: "price", currency: cur.toLowerCase(), limit: "1000" })
  let data = await ask(currency)
  if (!data && currency !== "EUR") { currency = "EUR"; data = await ask(currency) }
  if (!data) return json({ available: false })
  const days: Record<string, { price: number; ret: string | null; transfers: number }> = {}
  for (const t of data) {
    const day = String(t.departure_at || "").slice(0, 10)
    if (!day.startsWith(month) || !t.price) continue
    if (!days[day] || t.price < days[day].price) days[day] = { price: t.price, ret: t.return_at ? String(t.return_at).slice(0, 10) : null, transfers: t.transfers }
  }
  return json({ available: true, currency, month, days })
})
