// Gains réels Travelpayouts (réservations et commissions) pour le bilan du lundi.
// API de statistiques : https://api.travelpayouts.com/statistics/v1 (jeton dans l'en-tête X-Access-Token, le même que pour les prix).
// Le résumé est rangé dans la clé KV « gains:v1 » (aucun jeton, aucune donnée personnelle) ; rien n'est renvoyé sur une adresse publique.
// Lancé chaque matin par la tâche de 6 h UTC (src/worker.ts) ; /api/gains?k=<clé> le relance à la main (seule l'empreinte de la clé est ici).
import { Ctx, Env, json } from "./_lib/common"

const BASE = "https://api.travelpayouts.com/statistics/v1"
const EMPREINTE = "3e92cf742363ad768986d9964944c878ef353b74308996955593c401f9d41263"

async function sha(s: string) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s))
  return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, "0")).join("")
}
const appel = async (env: Env, chemin: string, corps?: unknown) => {
  const r = await fetch(BASE + chemin, { method: corps ? "POST" : "GET", headers: { "X-Access-Token": env.TRAVELPAYOUTS_TOKEN || "", "Content-Type": "application/json" }, body: corps ? JSON.stringify(corps) : undefined })
  return { status: r.status, text: await r.text() }
}
const depuis = (j: number) => new Date(Date.now() - j * 864e5).toISOString().slice(0, 10)

// Résumé des réservations des 90 derniers jours, par programme et par semaine (lundi), toutes marques confondues.
// Une seule requête par jour. États : paid (commission acquise), processing (en attente), cancelled (annulée).
export type Gains = { ts: number; monnaie: "USD"; depuis: string; lignes: { semaine: string; programme: string; id: number; reservations: number; annulees: number; ventes: number; payees: number; attente: number }[] }
export async function gains(env: Env): Promise<{ ok: boolean; status?: number; lignes?: number }> {
  const r = await appel(env, "/execute_query", { fields: ["campaign_id", "campaign_name_en", "date", "price_usd", "paid_profit_usd", "processing_profit_usd", "state"],
    filters: [{ field: "type", op: "eq", value: "action" }, { field: "date", op: "ge", value: depuis(90) }], sort: [{ field: "date", order: "asc" }], offset: 0, limit: 2000 })
  if (r.status !== 200) return { ok: false, status: r.status }
  let rows: any[]
  try { rows = JSON.parse(r.text).results || [] } catch { return { ok: false, status: 0 } }
  const map: Record<string, Gains["lignes"][number]> = {}
  for (const x of rows) {
    const d = new Date(String(x.date) + "T00:00:00Z"); if (isNaN(+d)) continue
    d.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7))
    const semaine = d.toISOString().slice(0, 10), id = Number(x.campaign_id) || 0, k = semaine + "|" + id
    const l = (map[k] ||= { semaine, programme: String(x.campaign_name_en || id).slice(0, 40), id, reservations: 0, annulees: 0, ventes: 0, payees: 0, attente: 0 })
    if (x.state === "cancelled") { l.annulees++; continue }
    l.reservations++; l.ventes += Number(x.price_usd) || 0; l.payees += Number(x.paid_profit_usd) || 0; l.attente += Number(x.processing_profit_usd) || 0
  }
  const lignes = Object.values(map).sort((a, b) => a.semaine.localeCompare(b.semaine) || a.id - b.id)
  for (const l of lignes) { l.ventes = Math.round(l.ventes * 100) / 100; l.payees = Math.round(l.payees * 100) / 100; l.attente = Math.round(l.attente * 100) / 100 }
  const out: Gains = { ts: Date.now(), monnaie: "USD", depuis: depuis(90), lignes }
  await env.ESCALE.put("gains:v1", JSON.stringify(out))
  return { ok: true, lignes: lignes.length }
}

export const onRequest = async (ctx: Ctx) => {
  const k = new URL(ctx.request.url).searchParams.get("k") || ""
  if (!k || (await sha(k)) !== EMPREINTE) return json({ error: "unauthorized" }, { status: 401 })
  if (!ctx.env.ESCALE || !ctx.env.TRAVELPAYOUTS_TOKEN) return json({ error: "non configuré" }, { status: 503 })
  return json(await gains(ctx.env))
}
