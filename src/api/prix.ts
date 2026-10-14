import { Ctx, json, IATA, DATE, currencyOf, pricesForDates, edgeCached } from "../_lib/common"
// Prix repérés récemment pour un trajet (cache Aviasales via Travelpayouts).
// GET /api/prix?from=CDG&to=BKO&dep=2026-11-03&ret=2026-11-10[&list=1][&direct=1]
export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 3600, async () => {
  const token = ctx.env.TRAVELPAYOUTS_TOKEN
  if (!token) return json({ available: false })
  const q = new URL(ctx.request.url).searchParams
  const from = (q.get("from") || "").toUpperCase(), to = (q.get("to") || "").toUpperCase()
  const dep = q.get("dep") || "", ret = q.get("ret") || ""
  const roundTrip = Boolean(ret) || q.get("rt") === "1"
  const list = q.get("list") === "1", direct = q.get("direct") === "1"
  let currency = currencyOf(q.get("currency"))
  if (!IATA.test(from) || !IATA.test(to) || !DATE.test(dep) || (ret && !DATE.test(ret))) return json({ error: "Paramètres invalides" }, { status: 400 })
  const ask = (cur: string) => pricesForDates(token, {
    origin: from, destination: to, departure_at: dep.slice(0, 7), ...(ret ? { return_at: ret.slice(0, 7) } : {}),
    one_way: roundTrip ? "false" : "true", sorting: "price", ...(direct ? { direct: "true" } : {}),
    currency: cur.toLowerCase(), limit: list ? "30" : "1",
  })
  let data = await ask(currency)
  if (!data && currency !== "EUR") { currency = "EUR"; data = await ask(currency) }
  if (!data) return json({ available: false })
  const best = data[0]
  if (!best) return json({ available: true, price: null, currency, offers: [] })
  const offers = list ? data.slice(0, 30).map((o: any) => ({
    price: o.price, airline: o.airline, flight_number: o.flight_number,
    departure_at: o.departure_at, return_at: o.return_at ?? null,
    origin_airport: o.origin_airport, destination_airport: o.destination_airport,
    transfers: o.transfers, return_transfers: o.return_transfers ?? null,
    duration_to: o.duration_to ?? o.duration ?? null, duration_back: o.duration_back ?? null,
  })) : undefined
  return json({ available: true, price: best.price, currency, airline: best.airline, transfers: best.transfers,
    departure_at: best.departure_at, return_at: best.return_at ?? null, ...(offers ? { offers } : {}) })
})
