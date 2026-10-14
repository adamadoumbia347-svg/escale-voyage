import { Ctx, json, lastApiError, IATA, MONTH, currencyOf, pricesForDates, edgeCached } from "../_lib/common"
// Destinations les moins chères depuis un aéroport, pour un mois. GET /api/explore?from=CDG&month=2026-11&currency=EUR
export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 3600, async () => {
  const token = ctx.env.TRAVELPAYOUTS_TOKEN
  if (!token) return json({ available: false, reason: "cle-absente" })
  const q = new URL(ctx.request.url).searchParams
  const from = (q.get("from") || "").toUpperCase(), month = q.get("month") || ""
  let currency = currencyOf(q.get("currency"))
  if (!IATA.test(from) || !MONTH.test(month)) return json({ error: "Paramètres invalides" }, { status: 400 })
  const ask = (cur: string) => pricesForDates(token, { origin: from, departure_at: month, unique: "true", one_way: "false", sorting: "price", currency: cur.toLowerCase(), limit: "30" })
  let data = await ask(currency)
  if (!data && currency !== "EUR") { currency = "EUR"; data = await ask(currency) }
  if (!data) return json({ available: false, reason: lastApiError || "inconnue" })
  const today = new Date().toISOString().slice(0, 10)
  const seen = new Set<string>()
  const items = data
    .filter((d: any) => d && d.price && String(d.departure_at || "").slice(0, 10) >= today)
    .sort((a: any, b: any) => a.price - b.price)
    .filter((d: any) => { const k = d.destination_airport || d.destination; if (seen.has(k)) return false; seen.add(k); return true })
    .map((d: any) => ({ to: d.destination_airport || d.destination, city_code: d.destination, price: d.price, transfers: d.transfers, departure_at: d.departure_at, return_at: d.return_at ?? null }))
  return json({ available: true, currency, items })
})
