import { Env, pricesForDates } from "./common"
// Envoi d'e-mails : Resend (RESEND_API_KEY) ou Brevo (BREVO_API_KEY). Expéditeur : ALERT_FROM (adresse validée chez le fournisseur).
export const mailerReady = (env: Env) => Boolean((env.RESEND_API_KEY || env.BREVO_API_KEY) && env.ALERT_FROM && env.ESCALE)

export async function sendMail(env: Env, to: string, subject: string, html: string): Promise<boolean> {
  const from = env.ALERT_FROM || ""
  try {
    if (env.RESEND_API_KEY) {
      const r = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
        body: JSON.stringify({ from: `Escale <${from}>`, to: [to], subject, html }),
      })
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
  } catch { /* l'erreur est signalée par le retour false */ }
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
