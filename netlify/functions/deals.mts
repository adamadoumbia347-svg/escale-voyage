import type { Config } from "@netlify/functions"

// Bons plans : destinations les moins chères depuis plusieurs grandes villes, sur les deux prochains mois.
// Résultat mis en cache par le CDN de Netlify (rafraîchi toutes les 6 heures).
// GET /api/deals?currency=EUR
const ORIGINS = ["CDG", "BRU", "LYS", "MRS", "GVA", "LHR", "JFK", "YUL"]
const CURRENCIES = ["EUR", "USD", "GBP", "CAD", "CHF", "XOF", "MAD"]

function monthsAhead() {
  const d = new Date(), out: string[] = []
  for (let i = 1; i <= 2; i++) {
    const m = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + i, 1))
    out.push(m.toISOString().slice(0, 7))
  }
  return out
}

async function cheapest(token: string, origin: string, month: string, currency: string) {
  const api = new URL("https://api.travelpayouts.com/aviasales/v3/prices_for_dates")
  api.search = new URLSearchParams({
    origin, departure_at: month, unique: "true", one_way: "false", sorting: "price",
    currency: currency.toLowerCase(), limit: "30", token,
  }).toString()
  try {
    const res = await fetch(api, { headers: { "Accept-Encoding": "gzip" } })
    if (!res.ok) return []
    const body = await res.json()
    return body?.success === false ? [] : body?.data ?? []
  } catch { return [] }
}

export default async (req: Request) => {
  const token = Netlify.env.get("TRAVELPAYOUTS_TOKEN")
  if (!token) return Response.json({ available: false })
  let currency = (new URL(req.url).searchParams.get("currency") || "EUR").toUpperCase()
  if (!CURRENCIES.includes(currency)) currency = "EUR"
  const months = monthsAhead()
  const today = new Date().toISOString().slice(0, 10)
  const results = await Promise.all(ORIGINS.flatMap((o) => months.map((m) => cheapest(token, o, m, currency).then((d) => [o, d] as const))))
  const origins: Record<string, any[]> = {}
  for (const [o, list] of results) {
    const best: Record<string, any> = origins[o] ? Object.fromEntries(origins[o].map((x) => [x.to, x])) : {}
    for (const t of list) {
      const to = t.destination_airport || t.destination
      const dep = String(t.departure_at || "").slice(0, 10)
      if (!to || !t.price || dep < today) continue
      if (!best[to] || t.price < best[to].price) {
        best[to] = { to, price: t.price, transfers: t.transfers, dep, ret: t.return_at ? String(t.return_at).slice(0, 10) : null }
      }
    }
    origins[o] = Object.values(best).sort((a, b) => a.price - b.price).slice(0, 12)
  }
  return Response.json({ available: true, currency, updated: new Date().toISOString(), origins }, {
    headers: { "Cache-Control": "public, max-age=900", "Netlify-CDN-Cache-Control": "public, durable, s-maxage=21600, stale-while-revalidate=86400" },
  })
}

export const config: Config = { path: "/api/deals" }
