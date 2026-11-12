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
  return { status: r.status, text: (await r.text()).slice(0, 60000) }
}
const depuis = (j: number) => new Date(Date.now() - j * 864e5).toISOString().slice(0, 10)

// Exploration : réponses brutes de l'API dans une clé de diagnostic, pour connaître les vrais champs
export async function diag(env: Env) {
  const out: Record<string, unknown> = { ts: Date.now() }
  out.champs = await appel(env, "/get_fields_list")
  out.agreges = await appel(env, "/get_fields_list?data_type=aggregated")
  out.q100 = await appel(env, "/execute_query", { fields: ["action_id", "sub_id", "price_usd", "paid_profit_usd", "state", "date"], filters: [{ field: "type", op: "eq", value: "action" }, { field: "campaign_id", op: "eq", value: 100 }, { field: "date", op: "ge", value: depuis(45) }], sort: [{ field: "date", order: "asc" }], offset: 0, limit: 200 })
  out.qtout = await appel(env, "/execute_query", { fields: ["action_id", "campaign_id", "sub_id", "price_usd", "paid_profit_usd", "state", "date"], filters: [{ field: "date", op: "ge", value: depuis(45) }], sort: [{ field: "date", order: "asc" }], offset: 0, limit: 200 })
  await env.ESCALE.put("gains:diag", JSON.stringify(out), { expirationTtl: 86400 })
  return { ok: true }
}

export const onRequest = async (ctx: Ctx) => {
  const k = new URL(ctx.request.url).searchParams.get("k") || ""
  if (!k || (await sha(k)) !== EMPREINTE) return json({ error: "unauthorized" }, { status: 401 })
  if (!ctx.env.ESCALE || !ctx.env.TRAVELPAYOUTS_TOKEN) return json({ error: "non configuré" }, { status: 503 })
  return json(await diag(ctx.env))
}
