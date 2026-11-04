import { Ctx, json, IATA, currencyOf, pricesForDates, edgeCached } from "../_lib/common"
// Week-ends pas chers : pour chacun des 8 prochains week-ends (départ vendredi ou samedi, retour dimanche ou lundi),
// les destinations aller-retour les moins chères trouvées récemment depuis un aéroport (cache Aviasales, prix réels).
// GET /api/weekends?from=CDG&max=100&currency=EUR -> { items: [{ to, price, dep, ret, transfers }] } (une ligne par destination, la moins chère)
// Gardé 6 heures en périphérie.
const ymd = (d: Date) => d.toISOString().slice(0, 10)
export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 21600, async () => {
  const token = ctx.env.TRAVELPAYOUTS_TOKEN
  if (!token) return json({ available: false, reason: "cle-absente" })
  const q = new URL(ctx.request.url).searchParams
  const from = (q.get("from") || "").toUpperCase()
  const max = Math.min(2000, Math.max(20, Number(q.get("max")) || 100))
  const currency = currencyOf(q.get("currency"))
  if (!IATA.test(from)) return json({ error: "Paramètres invalides" }, { status: 400 })
  // Vendredis des 8 prochains week-ends (au moins 3 jours à l'avance)
  const d = new Date(Date.now() + 3 * 86400000)
  d.setUTCDate(d.getUTCDate() + ((5 - d.getUTCDay() + 7) % 7))
  const fridays = Array.from({ length: 8 }, (_, i) => new Date(d.getTime() + i * 7 * 86400000))
  // Un appel par mois concerné (2 ou 3), puis on garde les vrais week-ends
  const months = [...new Set(fridays.map((f) => ymd(f).slice(0, 7)))]
  const lists = await Promise.all(months.map((m) => pricesForDates(token, {
    origin: from, departure_at: m, unique: "false", one_way: "false", sorting: "price", currency: currency.toLowerCase(), limit: "1000" }, 9000)))
  const rows: any[] = lists.flatMap((r) => r || [])
  const okPair = new Set<string>()
  for (const f of fridays) {
    const fri = ymd(f), sat = ymd(new Date(f.getTime() + 86400000)), sun = ymd(new Date(f.getTime() + 2 * 86400000)), mon = ymd(new Date(f.getTime() + 3 * 86400000))
    for (const a of [fri, sat]) for (const b of [sun, mon]) okPair.add(a + b)
  }
  const best = new Map<string, any>()
  for (const t of rows) {
    const dep = String(t.departure_at || "").slice(0, 10), ret = String(t.return_at || "").slice(0, 10)
    if (!t.price || t.price > max || !okPair.has(dep + ret)) continue
    const to = t.destination_airport || t.destination
    const cur = best.get(to)
    if (!cur || t.price < cur.price) best.set(to, { to, city: t.destination, price: t.price, dep, ret, transfers: t.transfers })
  }
  if (!rows.length) return json({ available: false, reason: "aucune-donnee" })
  const items = [...best.values()].sort((a, b) => a.price - b.price).slice(0, 40)
  return json({ available: true, currency, from, max, items })
})
