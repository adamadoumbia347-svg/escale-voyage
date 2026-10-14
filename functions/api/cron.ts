import { Ctx, json, sameKey, siteUrl } from "../_lib/common"
import { mailerReady, sendMail, cheapestRoundTrip } from "../_lib/mail"
import { TXT, fill } from "../_lib/alert-texts"
// Vérification quotidienne des alertes prix, appelée par GitHub Actions (.github/workflows/quotidien.yml)
// avec l'en-tête « x-cron-key: <CRON_KEY> ». Au plus un e-mail tous les 3 jours par alerte.
export const onRequestPost = async ({ request, env }: Ctx) => {
  if (!sameKey(request.headers.get("x-cron-key") || "", env.CRON_KEY || "")) return json({ error: "unauthorized" }, { status: 401 })
  if (!mailerReady(env)) return json({ ok: true, skipped: "mail not configured" })
  const kv = env.ESCALE, base = siteUrl(env)
  const now = Date.now(), cache = new Map<string, number | null>()
  let sent = 0, checked = 0
  const { keys } = await kv.list({ prefix: "alert:", limit: 500 })
  for (const { name } of keys) {
    const rec: any = await kv.get(name, "json")
    if (!rec || rec.status !== "active") continue
    checked++
    if (rec.lastSent && now - Date.parse(rec.lastSent) < 3 * 864e5) continue
    const ck = `${rec.from}-${rec.to}-${rec.currency}`
    if (!cache.has(ck)) cache.set(ck, await cheapestRoundTrip(env.TRAVELPAYOUTS_TOKEN, rec.from, rec.to, rec.currency))
    const price = cache.get(ck)
    if (price == null || price > rec.max) continue
    const fmtM = (n: number) => new Intl.NumberFormat(rec.lang === "ar" ? "ar-u-nu-latn" : rec.lang, { style: "currency", currency: rec.currency, maximumFractionDigits: 0 }).format(n)
    const t = TXT[rec.lang] || TXT.fr
    const id = name.slice("alert:".length)
    const v = { a: rec.from, b: rec.to, price: fmtM(price), max: fmtM(rec.max),
      search: `${base}/?type=vols&from=${rec.from}&to=${rec.to}${rec.lang === "fr" ? "" : "&lang=" + rec.lang}`,
      unsub: `${base}/api/alert?action=unsubscribe&id=${id}&token=${rec.token}` }
    if (await sendMail(env, rec.email, fill(t.dropSubject, v), fill(t.dropBody, v) + fill(t.footer, v))) {
      rec.lastSent = new Date().toISOString(); rec.lastPrice = price
      const left = Math.max(86400, Math.round((Date.parse(rec.created) + 365 * 864e5 - now) / 1000))
      await kv.put(name, JSON.stringify(rec), { expirationTtl: left })
      sent++
    }
  }
  return json({ ok: true, checked, sent })
}
