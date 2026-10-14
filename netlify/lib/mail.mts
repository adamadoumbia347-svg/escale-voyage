// Envoi d'e-mails : Resend (RESEND_API_KEY) ou Brevo (BREVO_API_KEY). Expéditeur : ALERT_FROM (adresse validée chez le fournisseur).
export function mailerReady(): boolean {
  return Boolean((Netlify.env.get("RESEND_API_KEY") || Netlify.env.get("BREVO_API_KEY")) && Netlify.env.get("ALERT_FROM"))
}

export async function sendMail(to: string, subject: string, html: string): Promise<boolean> {
  const from = Netlify.env.get("ALERT_FROM") || ""
  const resend = Netlify.env.get("RESEND_API_KEY"), brevo = Netlify.env.get("BREVO_API_KEY")
  try {
    if (resend) {
      const r = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${resend}`, "Content-Type": "application/json" },
        body: JSON.stringify({ from: `Escale <${from}>`, to: [to], subject, html }),
      })
      return r.ok
    }
    if (brevo) {
      const r = await fetch("https://api.brevo.com/v3/smtp/email", {
        method: "POST",
        headers: { "api-key": brevo, "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ sender: { name: "Escale", email: from }, to: [{ email: to }], subject, htmlContent: html }),
      })
      return r.ok
    }
  } catch { /* l'erreur est signalée par le retour false */ }
  return false
}

// Prix aller-retour le plus bas sur les 3 prochains mois (cache Aviasales via Travelpayouts)
export async function cheapestRoundTrip(from: string, to: string, currency = "EUR"): Promise<number | null> {
  const token = Netlify.env.get("TRAVELPAYOUTS_TOKEN")
  if (!token) return null
  const now = new Date(), today = now.toISOString().slice(0, 10)
  const months = [0, 1, 2].map((i) => new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() + i, 1)).toISOString().slice(0, 7))
  const prices = await Promise.all(months.map(async (m) => {
    const api = new URL("https://api.travelpayouts.com/aviasales/v3/prices_for_dates")
    api.search = new URLSearchParams({ origin: from, destination: to, departure_at: m, one_way: "false", sorting: "price",
      currency: currency.toLowerCase(), limit: "5", token }).toString()
    try {
      const r = await fetch(api)
      if (!r.ok) return null
      const b = await r.json()
      const ok = (b?.data ?? []).filter((t: any) => t.price && String(t.departure_at || "").slice(0, 10) >= today)
      return ok.length ? Math.min(...ok.map((t: any) => t.price)) : null
    } catch { return null }
  }))
  const valid = prices.filter((p): p is number => typeof p === "number")
  return valid.length ? Math.min(...valid) : null
}

export const esc = (t: string) => String(t).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" } as any)[c])
