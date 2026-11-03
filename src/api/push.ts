import { Ctx, json, IATA, CURRENCIES } from "../_lib/common"
import { vapidKeys, endpointId } from "../_lib/webpush"
// Alertes prix par notification sur le téléphone (Web Push). Rien de personnel n'est demandé : seulement l'adresse technique
// d'abonnement donnée par le navigateur (« endpoint »), avec l'accord du visiteur (fenêtre d'autorisation du navigateur).
//  GET  /api/push?action=key                     -> { key } clé publique VAPID
//  POST /api/push {endpoint, from, to, max, lang, currency} -> alerte créée (clé KV palert:<id>, 1 an)
//  GET  /api/push?action=msg&e=<endpoint>        -> dernier message à afficher (lu par site/sw.js)
//  POST /api/push {endpoint, action: "stop"}     -> supprime toutes les alertes de cet abonnement
const LANGS = ["fr", "en", "es", "pt", "ar", "it", "de", "nl"]
const PUSH_HOST = /^https:\/\/([a-z0-9-]+\.)*(googleapis\.com|mozilla\.com|mozaws\.net|push\.apple\.com|notify\.windows\.com|push\.services\.mozilla\.com)\//

export const onRequest = async (ctx: Ctx) => {
  const { request, env } = ctx, kv = env.ESCALE
  if (!kv) return json({ error: "unavailable" }, { status: 503 })
  const url = new URL(request.url), action = url.searchParams.get("action")
  if (request.method === "GET" && action === "key") return json({ key: (await vapidKeys(kv)).publicKey }, { headers: { "Cache-Control": "public, max-age=3600" } })
  if (request.method === "GET" && action === "msg") {
    const e = url.searchParams.get("e") || ""
    const m = PUSH_HOST.test(e) ? await kv.get(`pmsg:${await endpointId(e)}`, "json") : null
    return json(m || { title: "Escale", body: "", url: "/" }, { headers: { "Cache-Control": "no-store" } })
  }
  if (request.method !== "POST") return json({ error: "Méthode non autorisée" }, { status: 405 })
  let b: any
  try { b = await request.json() } catch { return json({ error: "invalid" }, { status: 400 }) }
  const endpoint = String(b.endpoint || "")
  if (!PUSH_HOST.test(endpoint) || endpoint.length > 1000) return json({ error: "invalid" }, { status: 400 })
  const eid = await endpointId(endpoint)
  const idx: string[] = (await kv.get(`pidx:${eid}`, "json")) || []
  if (b.action === "stop") {
    await Promise.all(idx.map((id) => kv.delete(`palert:${id}`)))
    await kv.delete(`pidx:${eid}`)
    return json({ ok: true })
  }
  const from = String(b.from || "").toUpperCase(), to = String(b.to || "").toUpperCase(), max = Math.round(Number(b.max))
  const lang = LANGS.includes(b.lang) ? b.lang : "fr"
  const currency = CURRENCIES.includes(String(b.currency).toUpperCase()) ? String(b.currency).toUpperCase() : "EUR"
  if (!IATA.test(from) || !IATA.test(to) || !(max > 0 && max < 10_000_000)) return json({ error: "invalid" }, { status: 400 })
  if (idx.length >= 10) return json({ error: "too_many" }, { status: 429 })
  const id = crypto.randomUUID()
  await kv.put(`palert:${id}`, JSON.stringify({ endpoint, eid, from, to, max, currency, lang, created: new Date().toISOString(), lastSent: null }), { expirationTtl: 366 * 86400 })
  idx.push(id)
  await kv.put(`pidx:${eid}`, JSON.stringify(idx), { expirationTtl: 366 * 86400 })
  return json({ ok: true })
}
