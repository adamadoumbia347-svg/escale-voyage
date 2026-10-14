// Agrégation des statistiques : chaque événement = { k: "view" | "click", p: chemin, l: langue, r: site d'origine, t: site partenaire }
export type Day = { views: number; clicks: number; pages: Record<string, number>; langs: Record<string, number>; refs: Record<string, number>; partners: Record<string, number> }
export const emptyDay = (): Day => ({ views: 0, clicks: 0, pages: {}, langs: {}, refs: {}, partners: {} })
const inc = (o: Record<string, number>, k: string) => { if (k) o[k] = (o[k] || 0) + 1 }
export function addEvent(d: Day, e: any) {
  if (e.k === "click") { d.clicks++; inc(d.partners, e.t) }
  else { d.views++; inc(d.pages, e.p); inc(d.langs, e.l); inc(d.refs, e.r || "direct") }
}
export function merge(a: Day, b: Day): Day {
  const m = (x: Record<string, number>, y: Record<string, number>) => { for (const k in y) x[k] = (x[k] || 0) + y[k]; return x }
  return { views: a.views + b.views, clicks: a.clicks + b.clicks, pages: m(a.pages, b.pages), langs: m(a.langs, b.langs), refs: m(a.refs, b.refs), partners: m(a.partners, b.partners) }
}
