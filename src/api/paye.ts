import { Ctx, IATA, MONTH, json, keysOf } from "../_lib/common"
import { KEY, MAX_KEEP, Paid, stats } from "../paye"
// Prix réellement payés par les voyageurs (bloc « Ce que les voyageurs ont vraiment payé » des pages trajets, src/paye.ts).
// POST /api/paye {from,to,prix,compagnie,mois} : ajoute une déclaration anonyme (1 par jour et par adresse IP pour un même trajet).
// GET  /api/paye?from=CDG&to=ABJ : chiffres agrégés seulement, jamais la liste brute.
const PRICE_MIN = 30, PRICE_MAX = 4000

async function ipKey(request: Request, from: string, to: string) {
  const ip = request.headers.get("CF-Connecting-IP") || "0"
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(`${ip}|${from}-${to}|${new Date().toISOString().slice(0, 10)}`))
  return "payeip:" + Array.from(new Uint8Array(buf)).slice(0, 12).map((b) => b.toString(16).padStart(2, "0")).join("")
}

export async function readPaid(env: any, from: string, to: string): Promise<Paid[]> {
  if (!env?.ESCALE) return []
  try { return ((await env.ESCALE.get(KEY(from, to), "json")) as Paid[]) || [] } catch { return [] }
}

// Trajets qui ont au moins une déclaration. Liste gardée 10 minutes (mémoire du processus, puis cache du centre de données) et tirée
// de l'inventaire des clés « paye: » (keysOf : une clé KV, refaite toutes les 6 heures). Avant le 13 novembre 2026, chaque visite
// d'une page trajet lisait la clé paye:FROM-TO, presque toujours vide : environ 9 000 lectures KV par jour, surtout des robots.
let declares: { s: Set<string>; at: number } | null = null
export async function trajetsDeclares(ctx: Ctx): Promise<Set<string>> {
  if (declares && Date.now() - declares.at < 600e3) return declares.s
  const cache = (globalThis as any).caches?.default, req = new Request("https://escale.live/__paye/idx/v1")
  let keys: string[] | null = null
  if (cache) { const hit = await cache.match(req).catch(() => null); if (hit) keys = (await hit.json().catch(() => null)) as string[] | null }
  if (!Array.isArray(keys)) {
    keys = await keysOf(ctx.env, "paye:", ctx.waitUntil)
    if (cache) ctx.waitUntil(Promise.resolve(cache.put(req, new Response(JSON.stringify(keys), { headers: { "Cache-Control": "public, max-age=600" } }))).catch(() => {}))
  }
  declares = { s: new Set(keys), at: Date.now() }
  return declares.s
}
// Déclarations d'un trajet pour sa page : lecture KV seulement s'il figure dans la liste (en cas de doute, lecture directe)
export async function readPaidPage(ctx: Ctx, from: string, to: string): Promise<Paid[]> {
  const connus = await trajetsDeclares(ctx).catch(() => null)
  return !connus || connus.has(KEY(from, to)) ? readPaid(ctx.env, from, to) : []
}
// Nouvelle déclaration : le trajet est ajouté tout de suite à l'inventaire (sinon son bloc n'apparaîtrait qu'au prochain inventaire)
async function noterDeclare(env: any, key: string) {
  const ik = "idx:paye:", cur = (await env.ESCALE.get(ik, "json").catch(() => null)) as { ts: number; keys: string[] } | null
  if (cur && Array.isArray(cur.keys) && !cur.keys.includes(key)) await env.ESCALE.put(ik, JSON.stringify({ ts: cur.ts, keys: [...cur.keys, key] })).catch(() => {})
  declares = null
}

export const onRequestGet = async ({ request, env }: Ctx) => {
  const q = new URL(request.url).searchParams
  const from = (q.get("from") || "").toUpperCase(), to = (q.get("to") || "").toUpperCase()
  if (!IATA.test(from) || !IATA.test(to)) return json({ error: "Paramètres invalides" }, { status: 400 })
  const s = stats(await readPaid(env, from, to))
  return json({ from, to, stats: s }, { headers: { "Cache-Control": "public, max-age=600" } })
}

export const onRequestPost = async ({ request, env, waitUntil }: Ctx) => {
  let d: Record<string, string> = {}
  try {
    if ((request.headers.get("content-type") || "").includes("application/json")) d = await request.json() as Record<string, string>
    else { const f = await request.formData(); f.forEach((v, k) => { d[k] = String(v) }) }
  } catch { return json({ ok: false }, { status: 400 }) }
  if (String(d["site-web"] || "")) return json({ ok: true }) // robot : on fait semblant d'accepter
  const from = String(d.from || "").toUpperCase(), to = String(d.to || "").toUpperCase()
  const prix = Math.round(Number(d.prix)), mois = String(d.mois || "").slice(0, 7)
  const compagnie = String(d.compagnie || "").replace(/[^\p{L}\p{N} '’.&-]/gu, "").replace(/\s+/g, " ").trim().slice(0, 40)
  const now = new Date(), maxMonth = now.toISOString().slice(0, 7), minMonth = new Date(Date.UTC(now.getUTCFullYear() - 2, now.getUTCMonth(), 1)).toISOString().slice(0, 7)
  if (!IATA.test(from) || !IATA.test(to) || from === to || !Number.isFinite(prix) || prix < PRICE_MIN || prix > PRICE_MAX || !MONTH.test(mois) || mois < minMonth || mois > maxMonth)
    return json({ ok: false, error: "Paramètres invalides" }, { status: 400 })
  if (!env.ESCALE) return json({ ok: false }, { status: 503 })
  const ik = await ipKey(request, from, to)
  if (await env.ESCALE.get(ik)) return json({ ok: true, deja: true }) // déjà une déclaration aujourd'hui pour ce trajet
  const list = await readPaid(env, from, to)
  list.push({ p: prix, c: compagnie, m: mois, at: now.toISOString().slice(0, 10) })
  await Promise.all([
    env.ESCALE.put(KEY(from, to), JSON.stringify(list.slice(-MAX_KEEP))),
    env.ESCALE.put(ik, "1", { expirationTtl: 86400 }),
  ])
  waitUntil(noterDeclare(env, KEY(from, to)).catch(() => {}))
  return json({ ok: true, n: list.length })
}
