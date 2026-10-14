import type { Config } from "@netlify/functions"
import { getStore } from "@netlify/blobs"
import { addEvent, emptyDay, merge, type Day } from "../lib/stats.mts"

// Chaque nuit à 0 h 30 UTC : regroupe les événements des jours passés en un total par jour, puis supprime les événements.
// Seule cette tâche écrit dans « stats-days » : pas d'écriture concurrente.
export default async () => {
  const events = getStore("stats-events"), days = getStore("stats-days")
  const today = new Date().toISOString().slice(0, 10)
  const { blobs } = await events.list()
  const byDay = new Map<string, string[]>()
  for (const { key } of blobs) {
    const d = key.slice(0, 10)
    if (d < today) byDay.set(d, [...(byDay.get(d) || []), key])
  }
  for (const [d, keys] of byDay) {
    const agg = emptyDay()
    for (const k of keys) { const e = await events.get(k, { type: "json" }); if (e) addEvent(agg, e) }
    const prev = (await days.get(d, { type: "json" })) as Day | null
    await days.setJSON(d, prev ? merge(prev, agg) : agg)
    for (const k of keys) await events.delete(k)
  }
}

export const config: Config = { schedule: "30 0 * * *" }
