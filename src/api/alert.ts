import { Ctx, json, IATA, CURRENCIES, siteUrl, esc } from "../_lib/common"
import { mailerReady, sendMail, lastMailError } from "../_lib/mail"
import { TXT, fill, page } from "../_lib/alert-texts"
// Alertes prix par e-mail (stockées dans l'espace KV ESCALE, clé alert:<id>).
//  GET  /api/alert?action=status                    -> { enabled }
//  POST /api/alert {email, from, to, max, lang, currency, consent} -> alerte « en attente » + e-mail de confirmation
//  GET  /api/alert?action=confirm&id=…&token=…      -> active l'alerte
//  GET  /api/alert?action=unsubscribe&id=…&token=…  -> supprime l'alerte et l'adresse
const EMAIL = /^[^\s@]{1,64}@[^\s@]{1,190}\.[a-z]{2,24}$/i
const LANGS = ["fr", "en", "es", "pt", "ar"]

export const onRequest = async (ctx: Ctx) => {
  const { request, env } = ctx
  const url = new URL(request.url)
  const action = url.searchParams.get("action")
  const kv = env.ESCALE
  if (request.method === "GET" && action === "status") return json({ enabled: mailerReady(env) })

  if (request.method === "GET" && (action === "confirm" || action === "unsubscribe")) {
    const id = url.searchParams.get("id") || "", token = url.searchParams.get("token") || ""
    const rec: any = kv && /^[a-f0-9-]{36}$/.test(id) ? await kv.get(`alert:${id}`, "json") : null
    const lang = rec && LANGS.includes(rec.lang) ? rec.lang : "fr"
    if (!rec || rec.token !== token) return page(lang, TXT[lang].invalid)
    if (action === "unsubscribe") { await kv.delete(`alert:${id}`); return page(lang, TXT[lang].unsubscribed) }
    rec.status = "active"; rec.confirmed = new Date().toISOString()
    await kv.put(`alert:${id}`, JSON.stringify(rec), { expirationTtl: 366 * 86400 })
    return page(lang, TXT[lang].confirmed)
  }

  if (request.method !== "POST") return json({ error: "Méthode non autorisée" }, { status: 405 })
  if (!mailerReady(env)) return json({ error: "unavailable" }, { status: 503 })
  let body: any
  try { body = await request.json() } catch { return json({ error: "invalid" }, { status: 400 }) }
  const email = String(body.email || "").trim().toLowerCase()
  const from = String(body.from || "").toUpperCase(), to = String(body.to || "").toUpperCase()
  const max = Math.round(Number(body.max))
  const lang = LANGS.includes(body.lang) ? body.lang : "fr"
  const currency = CURRENCIES.includes(String(body.currency).toUpperCase()) ? String(body.currency).toUpperCase() : "EUR"
  if (!EMAIL.test(email) || !IATA.test(from) || !IATA.test(to) || !(max > 0 && max < 10_000_000) || body.consent !== true) {
    return json({ error: "invalid" }, { status: 400 })
  }
  // Limite simple contre les abus : une demande par adresse et par heure
  const lim = `alertlimit:${email}`
  if (await kv.get(lim)) return json({ error: "later" }, { status: 429 })
  await kv.put(lim, "1", { expirationTtl: 3600 })
  const id = crypto.randomUUID(), token = crypto.randomUUID().replace(/-/g, "")
  // En attente : effacée automatiquement après 7 jours sans confirmation
  await kv.put(`alert:${id}`, JSON.stringify({ email, from, to, max, currency, lang, token, status: "pending", created: new Date().toISOString(), lastSent: null }), { expirationTtl: 7 * 86400 })
  const base = siteUrl(env, request)
  const money = new Intl.NumberFormat(lang === "ar" ? "ar-u-nu-latn" : lang, { style: "currency", currency, maximumFractionDigits: 0 }).format(max)
  const t = TXT[lang]
  const v = { a: from, b: to, max: money, link: `${base}/api/alert?action=confirm&id=${id}&token=${token}`, unsub: `${base}/api/alert?action=unsubscribe&id=${id}&token=${token}` }
  const ok = await sendMail(env, email, fill(t.confirmSubject, v), fill(t.confirmBody, v) + fill(t.footer, v))
  if (!ok) { await kv.delete(`alert:${id}`); await kv.delete(lim); return json({ error: "mail", detail: lastMailError }, { status: 502 }) }
  return json({ ok: true, email: esc(email) })
}
