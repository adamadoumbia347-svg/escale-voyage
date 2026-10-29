import { Env, esc, siteUrl } from "./_lib/common"
import { mailerReady, sendMail, lastMailError } from "./_lib/mail"
import { Month, Point, cacheKey } from "./apercu-prix"
// Message WhatsApp de la semaine : chaque lundi matin (tâche quotidienne de wrangler.jsonc), un e-mail avec le message
// des bons plans prêt à copier dans la chaîne WhatsApp. Destinataire : variable DIGEST_TO (Cloudflare > Variables et secrets).
// Prix : relevé du jour (historique KV des pages trajets, mis à jour chaque matin par releve-prix.yml) et dates du cache.
// Aussi envoyable à la demande depuis /admin/ (bouton « Recevoir le message WhatsApp maintenant »).
const CHANNEL = "https://whatsapp.com/channel/0029VbE28kB0LKZN7ypnGj0d"
const DEST: [string, string, string, string, string][] = [
  ["CDG", "DSS", "Dakar", "🇸🇳", "vol-paris-dakar"], ["CDG", "BKO", "Bamako", "🇲🇱", "vol-paris-bamako"],
  ["CDG", "ABJ", "Abidjan", "🇨🇮", "vol-paris-abidjan"], ["CDG", "CKY", "Conakry", "🇬🇳", "vol-paris-conakry"],
  ["CDG", "DLA", "Douala", "🇨🇲", "vol-paris-douala"], ["CDG", "FIH", "Kinshasa", "🇨🇩", "vol-paris-kinshasa"],
  ["CDG", "LFW", "Lomé", "🇹🇬", "vol-paris-lome"], ["CDG", "COO", "Cotonou", "🇧🇯", "vol-paris-cotonou"],
  ["CDG", "OUA", "Ouagadougou", "🇧🇫", "vol-paris-ouagadougou"], ["CDG", "ALG", "Alger", "🇩🇿", "vol-paris-alger"],
  ["CDG", "ORN", "Oran", "🇩🇿", "vol-paris-oran"], ["ORY", "CMN", "Casablanca", "🇲🇦", "vol-paris-casablanca"],
  ["CDG", "RAK", "Marrakech", "🇲🇦", "vol-paris-marrakech"], ["CDG", "TUN", "Tunis", "🇹🇳", "vol-paris-tunis"],
  ["CDG", "DJE", "Djerba", "🇹🇳", "vol-paris-djerba"],
]
const money = (n: number) => new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
const day = (iso: string) => { const [y, m, d] = iso.split("-").map(Number); return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString("fr-FR", { day: "numeric", month: "short", timeZone: "UTC" }) }

export async function buildMessage(env: Env) {
  const cache = (globalThis as any).caches?.default
  const since = new Date(Date.now() - 3 * 864e5).toISOString().slice(0, 10)
  const rows = (await Promise.all(DEST.map(async ([from, to, city, flag, path]) => {
    const hist = ((await env.ESCALE?.get(`hist:${from}-${to}`, "json")) as Point[] | null) || []
    const last = hist.length ? hist[hist.length - 1] : null
    const hit = cache ? await cache.match(cacheKey(from, to)) : null
    const months: Month[] = hit ? await hit.json() : []
    const best = months.length ? months.reduce((a, b) => (b.price < a.price ? b : a)) : null
    const price = best ? best.price : last && last[0] >= since ? last[1] : null
    if (!price) return null
    const week = hist.find(([d]) => d >= new Date(Date.now() - 8 * 864e5).toISOString().slice(0, 10))
    const trend = week && week[1] && week[0] < since ? Math.round((price / week[1] - 1) * 100) : null
    return { city, flag, path, price, best, trend }
  }))).filter(Boolean).sort((a: any, b: any) => a.price - b.price) as any[]
  const today = new Date().toLocaleDateString("fr-FR", { day: "numeric", month: "long", timeZone: "Europe/Paris" })
  const base = siteUrl(env).replace(/^https?:\/\//, "")
  const lines = [`✈️ *Bons plans Escale* · semaine du ${today}`, "", "Allers-retours les moins chers repérés au départ de *Paris* :", ""]
  for (const r of rows) {
    const dates = r.best && r.best.ret ? ` (${day(r.best.dep)} → ${day(r.best.ret)})` : ""
    const tr = r.trend !== null && r.trend <= -5 ? ` 📉 ${r.trend} % en 7 jours` : ""
    lines.push(`${r.flag} Paris → ${r.city} : *dès ${money(r.price)}*${dates}${tr}`, `   👉 ${base}/${r.path}/`)
  }
  lines.push("", `☀️ Été 2027 : les premiers prix de juillet-août → ${base}/vols-ete-2027/`,
    `📊 Baromètre des prix : ${base}/barometre-prix/`,
    `🔔 Alerte prix gratuite : choisissez votre trajet sur ${base} et recevez un e-mail quand le prix baisse.`,
    `📢 Partagez la chaîne à vos proches : ${CHANNEL}`,
    "", "_Prix repérés récemment, par personne. Le tarif exact s'affiche sur le site de réservation._")
  return { count: rows.length, text: lines.join("\n") }
}

export async function sendDigest(env: Env) {
  const to = ((env as any).DIGEST_TO || "").trim()
  if (!to) return { sent: false, reason: "DIGEST_TO absent" }
  if (!mailerReady(env)) return { sent: false, reason: "envoi d'e-mails non configuré" }
  const m = await buildMessage(env)
  if (!m.count) return { sent: false, reason: "aucun prix relevé" }
  const html = `<div style="font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:640px;color:#0d1b2e">` +
    `<h2 style="margin:0 0 8px">Message WhatsApp de la semaine</h2>` +
    `<p>1. Sélectionnez le texte dans le cadre et copiez-le.<br>2. WhatsApp → Actualités → chaîne Escale → collez → envoyez.</p>` +
    `<pre style="white-space:pre-wrap;font:15px/1.5 system-ui,sans-serif;background:#f3f6fa;border:1px solid #dde3ec;border-radius:10px;padding:14px">${esc(m.text)}</pre>` +
    `<p><a href="${CHANNEL}">Ouvrir la chaîne WhatsApp</a> · <a href="${siteUrl(env)}/outils/whatsapp/">Préparer un autre message (Lyon, Marseille, Bruxelles…)</a></p>` +
    `<p style="color:#5b6b80;font-size:13px">E-mail automatique d'Escale, envoyé chaque lundi à ${esc(to)}.</p></div>`
  const ok = await sendMail(env, to, `Message WhatsApp de la semaine (${m.count} destinations)`, html)
  return { sent: ok, to, count: m.count, ...(ok ? {} : { detail: lastMailError }) }
}
