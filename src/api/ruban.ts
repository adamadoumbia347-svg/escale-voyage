import { Ctx, json, IATA, pricesForDates, edgeCached } from "../_lib/common"
// Ruban de pays de l'accueil : pour la ville de départ du visiteur, le prix aller-retour le plus bas repéré (mois prochain et
// suivant) vers la grande ville de chaque pays de la rubrique « Que visiter ». GET /api/ruban?from=CDG  (prix en euros)
// Sert aussi aux pages pays, à la carte et au comparateur de la rubrique (site/visiter*.js).
// Deux demandes groupées à Travelpayouts (toutes les destinations du mois), puis une demande par pays resté sans prix.
// Rien n'est inventé : un pays sans prix repéré n'affiche rien. Gardé 12 heures dans le cache de Cloudflare (aucune écriture KV).
// Liste à garder en accord avec scripts/visiter.py (codes pays → villes d'arrivée, la première sert au lien de recherche).
// Premier code : aéroport connu du moteur d'Escale (lien de recherche). Deuxième : code demandé à Travelpayouts (ville quand elle existe).
const PAYS: Record<string, string[]> = {
  ci: ["ABJ", "ABJ"], sn: ["DSS", "DKR"], cm: ["DLA", "DLA", "YAO", "NSI"], gh: ["ACC", "ACC"], ma: ["RAK", "RAK", "CAS", "CMN"], tn: ["TUN", "TUN"], eg: ["CAI", "CAI"],
  ke: ["NBO", "NBO"], tz: ["ZNZ", "ZNZ", "DAR"], za: ["CPT", "CPT", "JNB"], fr: ["CDG", "PAR", "ORY"], it: ["FCO", "ROM", "MIL", "MXP"], es: ["BCN", "BCN", "MAD"], pt: ["LIS", "LIS"],
  gr: ["ATH", "ATH"], nl: ["AMS", "AMS"], tr: ["IST", "IST"], ae: ["DXB", "DXB"], jp: ["NRT", "TYO", "HND"], th: ["BKK", "BKK"], id: ["DPS", "DPS"], us: ["JFK", "NYC", "EWR"],
  mx: ["MEX", "MEX"], br: ["GIG", "RIO"],
  gn: ["CKY", "CKY"], bj: ["COO", "COO"], tg: ["LFW", "LFW"], ga: ["LBV", "LBV"], ng: ["LOS", "LOS", "ABV"],
}
type Prix = { to: string; price: number; dep: string; ret: string | null; v?: string }  // v : ville ou aéroport du prix trouvé (accueil, « Vers l'Afrique »)

export const onRequestGet = (ctx: Ctx) => edgeCached(ctx, 43200, async () => {
  const token = ctx.env.TRAVELPAYOUTS_TOKEN
  if (!token) return json({ available: false, reason: "cle-absente" })
  const from = (new URL(ctx.request.url).searchParams.get("from") || "").toUpperCase()
  if (!IATA.test(from)) return json({ error: "Paramètres invalides" }, { status: 400 })
  const d = new Date(), today = d.toISOString().slice(0, 10)
  const mois = [1, 2].map((i) => new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + i, 1)).toISOString().slice(0, 7))
  const out: Record<string, Prix> = {}
  const garder = (cc: string, t: any) => {
    const dep = String(t?.departure_at || "").slice(0, 10)
    if (!t?.price || dep < today) return
    if (!out[cc] || t.price < out[cc].price) out[cc] = { to: PAYS[cc][0], price: Math.round(t.price), dep, ret: t.return_at ? String(t.return_at).slice(0, 10) : null, v: String(t.destination || PAYS[cc][1]) }
  }
  const lots = await Promise.all(mois.map((m) => pricesForDates(token, { origin: from, departure_at: m, unique: "true", one_way: "false", sorting: "price", currency: "eur", limit: "1000" })))
  for (const data of lots) for (const t of data || []) {
    for (const cc in PAYS) if (PAYS[cc].includes(t.destination) || PAYS[cc].includes(t.destination_airport)) garder(cc, t)
  }
  // Pays restés sans prix : une demande chacun (sauf le pays de départ lui-même)
  const manquants = Object.keys(PAYS).filter((cc) => !out[cc] && !PAYS[cc].includes(from))
  await Promise.all(manquants.map(async (cc) => {
    const data = await pricesForDates(token, { origin: from, destination: PAYS[cc][1], departure_at: mois[0], one_way: "false", sorting: "price", currency: "eur", limit: "1" }, 6000)
    if (data && data[0]) garder(cc, data[0])
  }))
  for (const cc in PAYS) if (PAYS[cc].includes(from)) delete out[cc]
  if (!Object.keys(out).length) return json({ available: false, reason: "aucun-prix" })
  return json({ available: true, from, currency: "EUR", updated: new Date().toISOString(), prix: out })
})
