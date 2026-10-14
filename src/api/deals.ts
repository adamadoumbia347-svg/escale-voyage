import { Ctx, json, currencyOf, pricesForDates, edgeCached } from "../_lib/common"
// Bons plans : destinations les moins chères depuis plusieurs grandes villes, sur les deux prochains mois.
// Gardé 6 heures (cache Cloudflare + espace KV ESCALE s'il est relié). GET /api/deals?currency=EUR
const ORIGINS = ["CDG", "BRU", "LYS", "MRS", "GVA", "LHR", "JFK", "YUL"]
const TTL = 21600

async function build(token: string, currency: string) {
  const d = new Date()
  const months = [1, 2].map((i) => new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + i, 1)).toISOString().slice(0, 7))
  const today = d.toISOString().slice(0, 10)
  const results = await Promise.all(ORIGINS.flatMap((o) => months.map((m) =>
    pricesForDates(token, { origin: o, departure_at: m, unique: "true", one_way: "false", sorting: "price", currency: currency.toLowerCase(), limit: "30" })
      .then((data) => [o, data ?? []] as const))))
  const origins: Record<string, any[]> = {}
  for (const [o, list] of results) {
    const best: Record<string, any> = origins[o] ? Object.fromEntries(origins[o].map((x) => [x.to, x])) : {}
    for (const t of list) {
      const to = t.destination_airport || t.destination, dep = String(t.departure_at || "").slice(0, 10)
      if (!to || !t.price || dep < today) continue
      if (!best[to] || t.price < best[to].price) best[to] = { to, price: t.price, transfers: t.transfers, dep, ret: t.return_at ? String(t.return_at).slice(0, 10) : null }
    }
    origins[o] = Object.values(best).sort((a, b) => a.price - b.price).slice(0, 12)
  }
  return { available: true, currency, updated: new Date().toISOString(), origins }
}

export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 900, async () => {
  const token = ctx.env.TRAVELPAYOUTS_TOKEN
  if (!token) return json({ available: false })
  const currency = currencyOf(new URL(ctx.request.url).searchParams.get("currency"))
  const kv = ctx.env.ESCALE, key = `cache:deals:${currency}`
  if (kv) {
    const saved = await kv.get(key, "json")
    if (saved) return json(saved)
  }
  const data = await build(token, currency)
  if (kv && Object.values(data.origins).some((l) => l.length)) ctx.waitUntil(kv.put(key, JSON.stringify(data), { expirationTtl: TTL }))
  return json(data)
})
