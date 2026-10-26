import { Ctx, json, IATA, currencyOf, pricesForDates, edgeCached } from "../_lib/common"
// Destinations populaires depuis un aéroport : les trajets les plus recherchés par les voyageurs (classement Aviasales,
// « sorting=route »), avec le prix aller-retour le plus bas repéré le mois prochain.
// Gardé 12 heures (cache Cloudflare + espace KV ESCALE). GET /api/populaires?from=CDG&currency=EUR
const TTL = 43200
// Le classement vient d'Aviasales, très utilisé par les voyageurs russophones : on écarte la Russie et la Biélorussie,
// qui ne reflètent pas les recherches du public d'Escale (et ne sont pas desservies depuis l'Union européenne).
const EXCLUDED = new Set(("MOW DME SVO VKO ZIA LED AER KZN SVX OVB KRR MRV UFA KUF ROV MCX IKT KGD VVO KHV OMS PEE GOJ TJM CEK VOG " +
  "BAX KJA AAQ NBC MMK ARH SGC NUX NJC YKS UUD CSY ABA OGZ GRV NAL IJK ASF STW KXK PKC UUS PES MSQ GME VTB BQT").split(" "))

export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 3600, async () => {
  const token = ctx.env.TRAVELPAYOUTS_TOKEN
  if (!token) return json({ available: false, reason: "cle-absente" })
  const q = new URL(ctx.request.url).searchParams
  const from = (q.get("from") || "").toUpperCase(), currency = currencyOf(q.get("currency"))
  if (!IATA.test(from)) return json({ error: "Paramètres invalides" }, { status: 400 })
  const kv = ctx.env.ESCALE, key = `cache:pop:${from}:${currency}`
  if (kv) {
    const saved = await kv.get(key, "json")
    if (saved) return json(saved)
  }
  const d = new Date(), today = d.toISOString().slice(0, 10)
  const month = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 1)).toISOString().slice(0, 7)
  const data = await pricesForDates(token, { origin: from, departure_at: month, unique: "true", one_way: "false", sorting: "route", currency: currency.toLowerCase(), limit: "30" })
  if (!data) return json({ available: false })
  const seen = new Set<string>()
  const routes = []
  for (const t of data) {
    const to = t.destination_airport || t.destination, dep = String(t.departure_at || "").slice(0, 10)
    if (!to || seen.has(to) || to === from || !t.price || dep < today || EXCLUDED.has(to) || EXCLUDED.has(t.destination)) continue
    seen.add(to)
    routes.push({ to, city: t.destination, price: t.price, transfers: t.transfers ?? null })
    if (routes.length === 8) break
  }
  const out = { available: true, from, currency, updated: new Date().toISOString(), routes }
  if (kv && routes.length) ctx.waitUntil(kv.put(key, JSON.stringify(out), { expirationTtl: TTL }))
  return json(out)
})
