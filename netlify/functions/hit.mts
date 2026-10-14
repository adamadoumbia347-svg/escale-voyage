import type { Config } from "@netlify/functions"
import { getStore } from "@netlify/blobs"

// Mesure d'audience anonyme : aucune adresse IP, aucun cookie, aucun identifiant de visiteur n'est enregistré.
// Chaque visite est un petit événement séparé (pas de compteur partagé), regroupé chaque nuit par stats-rollup.
const BOTS = /bot|crawl|spider|slurp|preview|facebookexternalhit|whatsapp|headless|lighthouse|pingdom|curl|wget/i
const clean = (v: unknown, n: number) => String(v ?? "").replace(/[^\p{L}\p{N}\-._/~]/gu, "").slice(0, n)

export default async (req: Request) => {
  if (req.method !== "POST") return new Response(null, { status: 405 })
  if (BOTS.test(req.headers.get("user-agent") || "")) return new Response(null, { status: 204 })
  let e: any
  try { e = JSON.parse(await req.text()) } catch { return new Response(null, { status: 400 }) }
  const ev = {
    k: e.k === "click" ? "click" : "view",
    p: clean(e.p, 120) || "/",
    l: ["fr", "en", "es", "pt", "ar"].includes(e.l) ? e.l : "",
    r: clean(e.r, 60).toLowerCase(),
    t: clean(e.t, 60).toLowerCase(),
  }
  const day = new Date().toISOString().slice(0, 10)
  await getStore("stats-events").setJSON(`${day}/${crypto.randomUUID()}`, ev)
  return new Response(null, { status: 204 })
}

export const config: Config = {
  path: "/api/hit",
  rateLimit: { windowLimit: 60, windowSize: 60, aggregateBy: ["ip", "domain"] },
}
