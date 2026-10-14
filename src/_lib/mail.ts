import { Env, pricesForDates } from "./common"
// Envoi d'e-mails : Resend (RESEND_API_KEY) ou Brevo (BREVO_API_KEY). Expéditeur : ALERT_FROM (adresse validée chez le fournisseur).
// Adresse d'expéditeur : ALERT_FROM si défini, sinon MAIL_FROM (écrit dans wrangler.jsonc)
const sender = (env: Env) => (env.ALERT_FROM || (env as any).MAIL_FROM || "").trim()
export const mailerReady = (env: Env) => Boolean((env.RESEND_API_KEY || env.BREVO_API_KEY) && sender(env) && env.ESCALE)

// Dernière erreur d'envoi (sans la clé), renvoyée dans le champ « detail » pour faciliter le diagnostic
export let lastMailError = ""
export async function sendMail(env: Env, to: string, subject: string, html: string): Promise<boolean> {
  lastMailError = ""
  // Accepte « alertes@escale.live » comme « Escale <alertes@escale.live> »
  const raw = sender(env)
  const from = (raw.match(/<([^>]+)>/)?.[1] || raw).trim()
  try {
    if (env.RESEND_API_KEY) {
      const r = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${env.RESEND_API_KEY.trim()}`, "Content-Type": "application/json" },
        body: JSON.stringify({ from: `Escale <${from}>`, to: [to], subject, html }),
      })
      if (!r.ok) lastMailError = `resend-${r.status}: ${(await r.text()).slice(0, 200)}`
      return r.ok
    }
    if (env.BREVO_API_KEY) {
      const r = await fetch("https://api.brevo.com/v3/smtp/email", {
        method: "POST",
        headers: { "api-key": env.BREVO_API_KEY, "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ sender: { name: "Escale", email: from }, to: [{ email: to }], subject, htmlContent: html }),
      })
      return r.ok
    }
  } catch (e) { lastMailError = `reseau: ${String((e as any)?.message || e).slice(0, 120)}` }
  return false
}

// Prix aller-retour le plus bas sur les 3 prochains mois
export async function cheapestRoundTrip(token: string | undefined, from: string, to: string, currency = "EUR", timeoutMs = 8000): Promise<number | null> {
  if (!token) return null
  const now = new Date(), today = now.toISOString().slice(0, 10)
  const months = [0, 1, 2].map((i) => new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + i, 1)).toISOString().slice(0, 7))
  const prices = await Promise.all(months.map(async (m) => {
    const data = await pricesForDates(token, { origin: from, destination: to, departure_at: m, one_way: "false", sorting: "price", currency: currency.toLowerCase(), limit: "5" }, timeoutMs)
    const ok = (data ?? []).filter((t: any) => t.price && String(t.departure_at || "").slice(0, 10) >= today)
    return ok.length ? Math.min(...ok.map((t: any) => t.price)) : null
  }))
  const valid = prices.filter((p): p is number => typeof p === "number")
  return valid.length ? Math.min(...valid) : null
}
