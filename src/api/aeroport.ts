import { Ctx, MONTH, json } from "../_lib/common"
import { CODES, KEY, MAX_KEEP, Visit, WAITS, aggregate, readVisits } from "../aeroport"
// Témoignages d'arrivée à l'aéroport (bloc « L'aéroport vu par les voyageurs », src/aeroport.ts).
// POST /api/aeroport {code, attente, taxi, sim, mois} : une déclaration anonyme (1 par jour et par adresse pour un même aéroport).
// GET  /api/aeroport?code=ABJ : chiffres agrégés seulement.
const VALID = new Set(Object.values(CODES))

async function ipKey(request: Request, code: string) {
  const ip = request.headers.get("CF-Connecting-IP") || "0"
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(`${ip}|aero:${code}|${new Date().toISOString().slice(0, 10)}`))
  return "aeroip:" + Array.from(new Uint8Array(buf)).slice(0, 12).map((b) => b.toString(16).padStart(2, "0")).join("")
}

export const onRequestGet = async ({ request, env }: Ctx) => {
  const code = (new URL(request.url).searchParams.get("code") || "").toUpperCase()
  if (!VALID.has(code)) return json({ error: "Paramètres invalides" }, { status: 400 })
  return json({ code, stats: aggregate(await readVisits(env, code)) }, { headers: { "Cache-Control": "public, max-age=600" } })
}

export const onRequestPost = async ({ request, env }: Ctx) => {
  let d: Record<string, string> = {}
  try {
    if ((request.headers.get("content-type") || "").includes("application/json")) d = await request.json() as Record<string, string>
    else { const f = await request.formData(); f.forEach((v, k) => { d[k] = String(v) }) }
  } catch { return json({ ok: false }, { status: 400 }) }
  if (String(d["site-web"] || "")) return json({ ok: true })
  const code = String(d.code || "").toUpperCase(), w = Number(d.attente), mois = String(d.mois || "").slice(0, 7)
  const taxi = d.taxi === "" || d.taxi === undefined || d.taxi === null ? null : Math.round(Number(d.taxi))
  const sim = d.sim === "1" ? 1 : d.sim === "0" ? 0 : null
  const now = new Date(), maxMonth = now.toISOString().slice(0, 7), minMonth = new Date(Date.UTC(now.getUTCFullYear() - 2, now.getUTCMonth(), 1)).toISOString().slice(0, 7)
  if (!VALID.has(code) || !WAITS.includes(w) || !MONTH.test(mois) || mois < minMonth || mois > maxMonth || (taxi !== null && (!Number.isFinite(taxi) || taxi < 1 || taxi > 300)))
    return json({ ok: false, error: "Paramètres invalides" }, { status: 400 })
  if (!env.ESCALE) return json({ ok: false }, { status: 503 })
  const ik = await ipKey(request, code)
  if (await env.ESCALE.get(ik)) return json({ ok: true, deja: true })
  const list = await readVisits(env, code)
  list.push({ w, taxi, sim, m: mois, at: now.toISOString().slice(0, 10) } as Visit)
  await Promise.all([env.ESCALE.put(KEY(code), JSON.stringify(list.slice(-MAX_KEEP))), env.ESCALE.put(ik, "1", { expirationTtl: 86400 })])
  return json({ ok: true, n: list.length })
}
