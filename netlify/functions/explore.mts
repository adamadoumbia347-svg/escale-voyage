import type { Config } from "@netlify/functions"

// Destinations les moins chères depuis un aéroport, pour un mois donné (données en cache Aviasales via Travelpayouts).
// GET /api/explore?from=CDG&month=2026-11&currency=EUR
const IATA = /^[A-Z]{3}$/
const MONTH = /^\d{4}-\d{2}$/
const CURRENCIES = ["EUR", "USD", "GBP", "CAD", "CHF", "XOF", "MAD"]

async function query(token: string, from: string, month: string, currency: string) {
  const api = new URL("https://api.travelpayouts.com/aviasales/v3/prices_for_dates")
  api.search = new URLSearchParams({
    origin: from,
    departure_at: month,
    unique: "true",
    one_way: "false",
    sorting: "price",
    currency: currency.toLowerCase(),
    limit: "30",
    token,
  }).toString()
  const res = await fetch(api, { headers: { "Accept-Encoding": "gzip" } })
  if (!res.ok) return null
  const body = await res.json()
  return body?.success === false ? null : body?.data ?? null
}

export default async (req: Request) => {
  const token = Netlify.env.get("TRAVELPAYOUTS_TOKEN")
  if (!token) return Response.json({ available: false })

  const q = new URL(req.url).searchParams
  const from = (q.get("from") || "").toUpperCase()
  const month = q.get("month") || ""
  let currency = (q.get("currency") || "EUR").toUpperCase()
  if (!IATA.test(from) || !MONTH.test(month)) return Response.json({ error: "Paramètres invalides" }, { status: 400 })
  if (!CURRENCIES.includes(currency)) currency = "EUR"

  try {
    let data = await query(token, from, month, currency)
    if (!data && currency !== "EUR") { currency = "EUR"; data = await query(token, from, month, currency) }
    if (!data) return Response.json({ available: false })
    const items = data
      .filter((d: any) => d && d.price)
      .map((d: any) => ({
        to: d.destination_airport || d.destination,
        city_code: d.destination,
        price: d.price,
        transfers: d.transfers,
        departure_at: d.departure_at,
        return_at: d.return_at ?? null,
      }))
    return Response.json({ available: true, currency, items }, { headers: { "Cache-Control": "public, max-age=3600" } })
  } catch {
    return Response.json({ available: false })
  }
}

export const config: Config = { path: "/api/explore" }
