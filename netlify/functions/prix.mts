import type { Config } from "@netlify/functions"

// Prix indicatif le plus bas trouvé récemment pour un trajet (données en cache Aviasales via Travelpayouts).
// Inactif tant que la variable d'environnement TRAVELPAYOUTS_TOKEN n'est pas définie dans Netlify.
// GET /api/prix?from=CDG&to=BKO&dep=2026-11-03&ret=2026-11-10
// GET /api/prix?from=CDG&to=BKO&dep=2026-11-01&rt=1   (aller-retour, date de retour libre)
// GET /api/prix?...&list=1[&direct=1]                   (jusqu'à 30 offres du mois : compagnie, horaires, durée, escales, lien)

const IATA = /^[A-Z]{3}$/
const DATE = /^\d{4}-\d{2}-\d{2}$/
const CURRENCIES = ["EUR", "USD", "GBP", "CAD", "CHF", "XOF", "MAD"]

export default async (req: Request) => {
  const token = Netlify.env.get("TRAVELPAYOUTS_TOKEN")
  if (!token) return Response.json({ available: false }, { status: 200 })

  const q = new URL(req.url).searchParams
  const from = (q.get("from") || "").toUpperCase()
  const to = (q.get("to") || "").toUpperCase()
  const dep = q.get("dep") || ""
  const ret = q.get("ret") || ""
  const roundTrip = Boolean(ret) || q.get("rt") === "1"
  const list = q.get("list") === "1"
  const direct = q.get("direct") === "1"
  let currency = (q.get("currency") || "EUR").toUpperCase()
  if (!CURRENCIES.includes(currency)) currency = "EUR"
  if (!IATA.test(from) || !IATA.test(to) || !DATE.test(dep) || (ret && !DATE.test(ret))) {
    return Response.json({ error: "Paramètres invalides" }, { status: 400 })
  }

  const ask = async (cur: string) => {
    const api = new URL("https://api.travelpayouts.com/aviasales/v3/prices_for_dates")
    api.search = new URLSearchParams({
      origin: from,
      destination: to,
      departure_at: dep.slice(0, 7), // le mois entier : plus de résultats en cache
      ...(ret ? { return_at: ret.slice(0, 7) } : {}),
      one_way: roundTrip ? "false" : "true",
      sorting: "price",
      ...(direct ? { direct: "true" } : {}),
      currency: cur.toLowerCase(),
      limit: list ? "30" : "1",
      token,
    }).toString()
    const res = await fetch(api, { headers: { "Accept-Encoding": "gzip" } })
    if (!res.ok) return null
    const body = await res.json()
    return body?.success === false ? null : body
  }

  try {
    let body = await ask(currency)
    if (!body && currency !== "EUR") { currency = "EUR"; body = await ask(currency) }
    if (!body) return Response.json({ available: false }, { status: 200 })
    const best = body?.data?.[0]
    if (!best) return Response.json({ available: true, price: null, currency, offers: [] }, { status: 200, headers: cache() })
    const offers = list ? (body.data as any[]).slice(0, 30).map((o) => ({
      price: o.price, airline: o.airline, flight_number: o.flight_number,
      departure_at: o.departure_at, return_at: o.return_at ?? null,
      origin_airport: o.origin_airport, destination_airport: o.destination_airport,
      transfers: o.transfers, return_transfers: o.return_transfers ?? null,
      duration_to: o.duration_to ?? o.duration ?? null, duration_back: o.duration_back ?? null,
      link: typeof o.link === "string" && o.link.startsWith("/") ? o.link : null,
    })) : undefined
    return Response.json({
      available: true,
      price: best.price,
      currency,
      airline: best.airline,
      transfers: best.transfers,
      departure_at: best.departure_at,
      return_at: best.return_at ?? null,
      ...(offers ? { offers } : {}),
    }, { status: 200, headers: cache() })
  } catch {
    return Response.json({ available: false }, { status: 200 })
  }
}

const cache = () => ({ "Cache-Control": "public, max-age=3600" })

export const config: Config = { path: "/api/prix" }
