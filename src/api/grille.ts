import { Ctx, json, IATA, DATE, currencyOf, edgeCached } from "../_lib/common"
// Grille des prix aller × retour (comme la « grille de dates » de Google Flights) : 7 jours de départ × 7 jours de retour
// autour des dates choisies, prix aller-retour le plus bas trouvé récemment (API Travelpayouts « week-matrix », cache Aviasales).
// GET /api/grille?from=CDG&to=DSS&dep=2026-12-20&ret=2027-01-03&currency=EUR — gardé 3 heures.
export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 10800, async () => {
  const token = ctx.env.TRAVELPAYOUTS_TOKEN
  if (!token) return json({ available: false, reason: "cle-absente" })
  const q = new URL(ctx.request.url).searchParams
  const from = (q.get("from") || "").toUpperCase(), to = (q.get("to") || "").toUpperCase()
  const dep = q.get("dep") || "", ret = q.get("ret") || ""
  const currency = currencyOf(q.get("currency"))
  if (!IATA.test(from) || !IATA.test(to) || from === to || !DATE.test(dep) || !DATE.test(ret) || ret <= dep) return json({ error: "Paramètres invalides" }, { status: 400 })
  const api = new URL("https://api.travelpayouts.com/v2/prices/week-matrix")
  api.search = new URLSearchParams({ origin: from, destination: to, depart_date: dep, return_date: ret, currency: currency.toLowerCase(),
    show_to_affiliates: "true", token: token.trim() }).toString()
  try {
    const r = await fetch(api.toString(), { headers: { "Accept-Encoding": "gzip" }, signal: AbortSignal.timeout(8000) })
    if (!r.ok) return json({ available: false, reason: `travelpayouts-http-${r.status}` })
    const body: any = await r.json()
    if (body?.success === false || !Array.isArray(body?.data)) return json({ available: false, reason: "travelpayouts-refus" })
    const cells: Record<string, { price: number; stops: number | null }> = {}
    for (const t of body.data) {
      const d = String(t.depart_date || "").slice(0, 10), b = String(t.return_date || "").slice(0, 10), p = Number(t.value)
      if (!DATE.test(d) || !DATE.test(b) || !p) continue
      const k = `${d}|${b}`
      if (!cells[k] || p < cells[k].price) cells[k] = { price: p, stops: t.number_of_changes ?? null }
    }
    return json({ available: true, currency, dep, ret, cells })
  } catch (e) {
    return json({ available: false, reason: "travelpayouts-reseau" })
  }
})
