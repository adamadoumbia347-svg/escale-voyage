import type { Config } from "@netlify/functions"

// Calendrier des prix : prix aller-retour le plus bas par jour de départ sur un mois (cache Aviasales via Travelpayouts).
// GET /api/calendar?from=CDG&to=DSS&month=2026-11&currency=EUR
const IATA = /^[A-Z]{3}$/
const MONTH = /^\d{4}-\d{2}$/
const CURRENCIES = ["EUR", "USD", "GBP", "CAD", "CHF", "XOF", "MAD"]

async function query(token: string, from: string, to: string, month: string, currency: string) {
  const api = new URL("https://api.travelpayouts.com/aviasales/v3/prices_for_dates")
  api.search = new URLSearchParams({
    origin: from, destination: to, departure_at: month, one_way: "false", unique: "false",
    sorting: "price", currency: currency.toLowerCase(), limit: "1000", token,
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
  const from = (q.get("from") || "").toUpperCase(), to = (q.get("to") || "").toUpperCase(), month = q.get("month") || ""
  let currency = (q.get("currency") || "EUR").toUpperCase()
  if (!IATA.test(from) || !IATA.test(to) || !MONTH.test(month)) return Response.json({ error: "Paramètres invalides" }, { status: 400 })
  if (!CURRENCIES.includes(currency)) currency = "EUR"
  try {
    let data = await query(token, from, to, month, currency)
    if (!data && currency !== "EUR") { currency = "EUR"; data = await query(token, from, to, month, currency) }
    if (!data) return Response.json({ available: false })
    // Le prix le plus bas pour chaque jour de départ du mois
    const days: Record<string, { price: number; ret: string | null; transfers: number }> = {}
    for (const t of data) {
      const day = String(t.departure_at || "").slice(0, 10)
      if (!day.startsWith(month) || !t.price) continue
      if (!days[day] || t.price < days[day].price) {
        days[day] = { price: t.price, ret: t.return_at ? String(t.return_at).slice(0, 10) : null, transfers: t.transfers }
      }
    }
    return Response.json({ available: true, currency, month, days }, {
      headers: { "Cache-Control": "public, max-age=1800", "Netlify-CDN-Cache-Control": "public, durable, s-maxage=10800, stale-while-revalidate=86400" },
    })
  } catch {
    return Response.json({ available: false })
  }
}

export const config: Config = { path: "/api/calendar" }
