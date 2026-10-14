import type { Config } from "@netlify/functions"
import { getStore } from "@netlify/blobs"
import { addEvent, emptyDay, merge } from "../lib/stats.mts"

// Tableau de bord : GET /api/stats?days=30 avec l'en-tête « x-stats-key: <STATS_KEY> ».
function same(a: string, b: string) {
  if (!a || !b || a.length !== b.length) return false
  let r = 0
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i)
  return r === 0
}

export default async (req: Request) => {
  const key = Netlify.env.get("STATS_KEY") || ""
  if (!same(req.headers.get("x-stats-key") || "", key)) return Response.json({ error: "unauthorized" }, { status: 401 })
  const n = Math.min(365, Math.max(1, Number(new URL(req.url).searchParams.get("days")) || 30))
  const daysStore = getStore("stats-days"), events = getStore("stats-events")
  const out: Record<string, any> = {}
  const d0 = new Date()
  for (let i = n - 1; i >= 1; i--) {
    const d = new Date(d0.getTime() - i * 864e5).toISOString().slice(0, 10)
    out[d] = (await daysStore.get(d, { type: "json" })) || emptyDay()
  }
  // Aujourd'hui (et les jours pas encore regroupés) : calcul direct à partir des événements
  const today = d0.toISOString().slice(0, 10)
  const live: Record<string, any> = {}
  const { blobs } = await events.list()
  for (const { key: k } of blobs) {
    const d = k.slice(0, 10)
    if (!live[d]) live[d] = emptyDay()
    const e = await events.get(k, { type: "json" })
    if (e) addEvent(live[d], e)
  }
  for (const d in live) if (out[d] || d === today) out[d] = out[d] ? merge(out[d], live[d]) : live[d]
  if (!out[today]) out[today] = emptyDay()
  return Response.json({ days: out }, { headers: { "Cache-Control": "no-store" } })
}

export const config: Config = { path: "/api/stats" }
