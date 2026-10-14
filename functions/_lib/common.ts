// Outils communs aux fonctions Cloudflare Pages d'Escale.
// Variables (Cloudflare > Workers & Pages > escale-voyage > Settings > Variables and Secrets) :
//   TRAVELPAYOUTS_TOKEN  prix réels (Travelpayouts / Aviasales)
//   ADMIN_KEY            accès à la page /admin/ (messages et inscriptions)
//   RESEND_API_KEY ou BREVO_API_KEY + ALERT_FROM   envoi des alertes prix par e-mail
//   CRON_KEY             appel quotidien de /api/cron (vérification des alertes)
//   SITE_URL             adresse publique du site (par défaut https://escale-voyage.pages.dev)
// Stockage (Settings > Bindings) : espace KV nommé ESCALE (formulaires, alertes, cache des bons plans).
export type Env = {
  TRAVELPAYOUTS_TOKEN?: string; ADMIN_KEY?: string; CRON_KEY?: string; SITE_URL?: string
  RESEND_API_KEY?: string; BREVO_API_KEY?: string; ALERT_FROM?: string
  ESCALE?: any // KVNamespace
}
export type Ctx = { request: Request; env: Env; waitUntil: (p: Promise<any>) => void; next: () => Promise<Response> }

export const json = (data: unknown, init: ResponseInit = {}) =>
  new Response(JSON.stringify(data), { ...init, headers: { "Content-Type": "application/json; charset=utf-8", ...(init.headers || {}) } })

export const IATA = /^[A-Z]{3}$/
export const MONTH = /^\d{4}-\d{2}$/
export const DATE = /^\d{4}-\d{2}-\d{2}$/
export const CURRENCIES = ["EUR", "USD", "GBP", "CAD", "CHF", "XOF", "MAD"]
export const currencyOf = (v: string | null) => { const c = (v || "EUR").toUpperCase(); return CURRENCIES.includes(c) ? c : "EUR" }
export const siteUrl = (env: Env, req?: Request) => (env.SITE_URL || (req ? new URL(req.url).origin : "") || "https://escale-voyage.pages.dev").replace(/\/$/, "")

// API Travelpayouts « prices_for_dates » (prix en cache Aviasales)
export async function pricesForDates(token: string, params: Record<string, string>, timeoutMs = 8000): Promise<any[] | null> {
  const api = new URL("https://api.travelpayouts.com/aviasales/v3/prices_for_dates")
  api.search = new URLSearchParams({ ...params, token }).toString()
  try {
    const res = await fetch(api.toString(), { headers: { "Accept-Encoding": "gzip" }, signal: AbortSignal.timeout(timeoutMs) })
    if (!res.ok) return null
    const body: any = await res.json()
    return body?.success === false ? null : body?.data ?? null
  } catch { return null }
}

// Cache de la périphérie Cloudflare (Cache API) : évite d'interroger Travelpayouts à chaque visite.
export async function edgeCached(ctx: Ctx, seconds: number, produce: () => Promise<Response>): Promise<Response> {
  const cache = (globalThis as any).caches?.default
  const key = new Request(new URL(ctx.request.url).toString(), { method: "GET" })
  if (cache) {
    const hit = await cache.match(key)
    if (hit) return hit
  }
  const res = await produce()
  if (cache && res.ok) {
    const copy = new Response(res.clone().body, res)
    copy.headers.set("Cache-Control", `public, max-age=${seconds}`)
    ctx.waitUntil(cache.put(key, copy))
  }
  return res
}

export const esc = (t: string) => String(t).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" } as any)[c])

export function sameKey(a: string, b: string) {
  if (!a || !b || a.length !== b.length) return false
  let r = 0
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i)
  return r === 0
}
