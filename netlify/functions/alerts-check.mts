import type { Config } from "@netlify/functions"
import { getStore } from "@netlify/blobs"
import { mailerReady, sendMail, cheapestRoundTrip } from "../lib/mail.mts"
import { TXT, fill } from "../lib/alert-texts.mts"

// Tous les jours à 6 h UTC (7 h ou 8 h à Paris selon l'heure d'été) : vérifie les alertes actives et prévient par e-mail
// quand le prix passe sous le seuil. Au plus un e-mail tous les 3 jours par alerte. Les alertes en attente de plus
// de 7 jours et les alertes de plus d'un an sont supprimées.
export default async () => {
  if (!mailerReady()) return
  const store = getStore("alerts")
  const base = Netlify.env.get("URL") || "https://escale-voyage.netlify.app"
  const now = Date.now(), cache = new Map<string, number | null>()
  const { blobs } = await store.list()
  for (const { key } of blobs.slice(0, 500)) {
    const rec: any = await store.get(key, { type: "json" })
    if (!rec) continue
    const age = now - Date.parse(rec.created)
    if ((rec.status === "pending" && age > 7 * 864e5) || age > 365 * 864e5) { await store.delete(key); continue }
    if (rec.status !== "active") continue
    if (rec.lastSent && now - Date.parse(rec.lastSent) < 3 * 864e5) continue
    const ck = `${rec.from}-${rec.to}-${rec.currency}`
    if (!cache.has(ck)) cache.set(ck, await cheapestRoundTrip(rec.from, rec.to, rec.currency))
    const price = cache.get(ck)
    if (price == null || price > rec.max) continue
    const fmtM = (n: number) => new Intl.NumberFormat(rec.lang === "ar" ? "ar-u-nu-latn" : rec.lang, { style: "currency", currency: rec.currency, maximumFractionDigits: 0 }).format(n)
    const t = TXT[rec.lang] || TXT.fr
    const v = { a: rec.from, b: rec.to, price: fmtM(price), max: fmtM(rec.max),
      search: `${base}/?type=vols&from=${rec.from}&to=${rec.to}${rec.lang === "fr" ? "" : "&lang=" + rec.lang}`,
      unsub: `${base}/api/alert?action=unsubscribe&id=${key}&token=${rec.token}` }
    if (await sendMail(rec.email, fill(t.dropSubject, v), fill(t.dropBody, v) + fill(t.footer, v))) {
      rec.lastSent = new Date().toISOString(); rec.lastPrice = price
      await store.setJSON(key, rec)
    }
  }
}

export const config: Config = { schedule: "0 6 * * *" }
