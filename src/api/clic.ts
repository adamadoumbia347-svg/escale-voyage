import { Ctx, json } from "../_lib/common"
// Compteur de clics anonyme (site/clics.js) : POST /api/clic {k, p, u?} -> +1 dans « clics:AAAA-MM-JJ » (espace KV ESCALE),
// et pour les liens partenaires, +1 pour la page u dans « pages:AAAA-MM-JJ ».
// Ni cookie, ni adresse IP, ni identifiant : seulement le type de lien (k) et le type de page (p). Gardé 400 jours.
const OK = /^[a-z0-9-]{1,30}$/
export const onRequestPost = async ({ request, env }: Ctx) => {
  if (!env.ESCALE) return json({ ok: false }, { status: 503 })
  let b: any = null
  try { b = JSON.parse(await request.text()) } catch { b = null }
  const k = String(b?.k || ""), p = String(b?.p || "autre")
  if (!OK.test(k) || !OK.test(p)) return json({ ok: false }, { status: 400 })
  const key = "clics:" + new Date().toISOString().slice(0, 10)
  const day: Record<string, number> = ((await env.ESCALE.get(key, "json")) as any) || {}
  const id = `${k}|${p}`
  if (!(id in day) && Object.keys(day).length > 300) return json({ ok: false }, { status: 429 }) // garde-fou
  day[id] = (day[id] || 0) + 1
  await env.ESCALE.put(key, JSON.stringify(day), { expirationTtl: 400 * 86400 })
  // Clics vers un partenaire : on compte aussi l'adresse de la page (chemin seul, sans paramètres) dans « pages:AAAA-MM-JJ »
  const u = String(b?.u || "").toLowerCase()
  if (u && /^\/[a-z0-9\-\/._]{0,90}$/.test(u)) {
    const pk = "pages:" + new Date().toISOString().slice(0, 10)
    const pages: Record<string, number> = ((await env.ESCALE.get(pk, "json")) as any) || {}
    if (u in pages || Object.keys(pages).length < 600) {
      pages[u] = (pages[u] || 0) + 1
      await env.ESCALE.put(pk, JSON.stringify(pages), { expirationTtl: 400 * 86400 })
    }
  }
  return json({ ok: true })
}
