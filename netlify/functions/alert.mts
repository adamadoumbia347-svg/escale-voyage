import type { Config, Context } from "@netlify/functions"
import { getStore } from "@netlify/blobs"
import { mailerReady, sendMail, esc } from "../lib/mail.mts"
import { TXT, fill, page } from "../lib/alert-texts.mts"

// Alertes prix par e-mail.
//  GET  /api/alert?action=status                 -> { enabled }
//  POST /api/alert {email, from, to, max, lang, currency, consent}  -> crée une alerte « en attente » et envoie l'e-mail de confirmation
//  GET  /api/alert?action=confirm&id=…&token=…   -> active l'alerte
//  GET  /api/alert?action=unsubscribe&id=…&token=… -> supprime l'alerte et l'adresse
const IATA = /^[A-Z]{3}$/
const EMAIL = /^[^\s@]{1,64}@[^\s@]{1,190}\.[a-z]{2,24}$/i
const LANGS = ["fr", "en", "es", "pt", "ar"]
const CURRENCIES = ["EUR", "USD", "GBP", "CAD", "CHF", "XOF", "MAD"]

export default async (req: Request, context: Context) => {
  const url = new URL(req.url)
  const store = getStore("alerts")
  const action = url.searchParams.get("action")

  if (req.method === "GET" && action === "status") return Response.json({ enabled: mailerReady() })

  if (req.method === "GET" && (action === "confirm" || action === "unsubscribe")) {
    const id = url.searchParams.get("id") || "", token = url.searchParams.get("token") || ""
    const rec: any = /^[a-f0-9-]{36}$/.test(id) ? await store.get(id, { type: "json", consistency: "strong" }) : null
    const lang = rec && LANGS.includes(rec.lang) ? rec.lang : "fr"
    if (!rec || rec.token !== token) return page(lang, TXT[lang].invalid)
    if (action === "unsubscribe") { await store.delete(id); return page(lang, TXT[lang].unsubscribed) }
    rec.status = "active"; rec.confirmed = new Date().toISOString()
    await store.setJSON(id, rec)
    return page(lang, TXT[lang].confirmed)
  }

  if (req.method !== "POST") return Response.json({ error: "Méthode non autorisée" }, { status: 405 })
  if (!mailerReady()) return Response.json({ error: "unavailable" }, { status: 503 })
  let body: any
  try { body = await req.json() } catch { return Response.json({ error: "invalid" }, { status: 400 }) }
  const email = String(body.email || "").trim().toLowerCase()
  const from = String(body.from || "").toUpperCase(), to = String(body.to || "").toUpperCase()
  const max = Math.round(Number(body.max))
  const lang = LANGS.includes(body.lang) ? body.lang : "fr"
  const currency = CURRENCIES.includes(String(body.currency).toUpperCase()) ? String(body.currency).toUpperCase() : "EUR"
  if (!EMAIL.test(email) || !IATA.test(from) || !IATA.test(to) || !(max > 0 && max < 10_000_000) || body.consent !== true) {
    return Response.json({ error: "invalid" }, { status: 400 })
  }
  const id = crypto.randomUUID(), token = crypto.randomUUID().replace(/-/g, "")
  await store.setJSON(id, { email, from, to, max, currency, lang, token, status: "pending", created: new Date().toISOString(), lastSent: null })
  const base = context.site?.url || url.origin
  const money = new Intl.NumberFormat(lang === "ar" ? "ar-u-nu-latn" : lang, { style: "currency", currency, maximumFractionDigits: 0 }).format(max)
  const t = TXT[lang]
  const v = { a: from, b: to, max: money, link: `${base}/api/alert?action=confirm&id=${id}&token=${token}`, unsub: `${base}/api/alert?action=unsubscribe&id=${id}&token=${token}` }
  const ok = await sendMail(email, fill(t.confirmSubject, v), fill(t.confirmBody, v) + fill(t.footer, v))
  if (!ok) { await store.delete(id); return Response.json({ error: "mail" }, { status: 502 }) }
  return Response.json({ ok: true, email: esc(email) })
}

export const config: Config = {
  path: "/api/alert",
  rateLimit: { windowLimit: 10, windowSize: 60, aggregateBy: ["ip", "domain"] },
}
