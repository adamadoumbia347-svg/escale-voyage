import { Ctx, esc, keysOf } from "./_lib/common"
import { Paid } from "./paye"
import { ROUTES } from "./barometre"
// Pages compagnies (/compagnie/air-france/, /en/airline/air-france/) : le bloc « ce que les voyageurs ont payé » est rempli
// par le serveur à partir des déclarations anonymes des pages trajets (clés KV paye:FROM-TO, src/api/paye.ts).
// Agrégat par compagnie recalculé au plus une fois par heure (cache Cloudflare) : nombre de déclarations, prix médian,
// et les trajets les plus cités. Rien n'est affiché sous 3 déclarations.
type Agg = Record<string, { n: number; med: number; routes: { key: string; n: number; med: number }[] }>
const median = (a: number[]) => { const s = a.slice().sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2) }
const norm = (s: string) => s.toLowerCase().replace(/airlines?|air lines|compagnie|\s+/g, "").replace(/[^a-z0-9]/g, "")
const LABEL: Record<string, string> = Object.fromEntries(ROUTES.map(([f, t, l]) => [`${f}-${t}`, l]))

async function aggregate(env: any): Promise<Agg> {
  const out: Record<string, { all: number[]; routes: Record<string, number[]> }> = {}
  if (!env?.ESCALE) return {}
  const keys = await keysOf(env, "paye:")
  const lists = await Promise.all(keys.map((k) => env.ESCALE.get(k, "json").catch(() => null) as Promise<Paid[] | null>))
  keys.forEach((k, i) => {
    const route = k.slice(5)
    for (const p of lists[i] || []) {
      if (!p.c) continue
      const a = norm(p.c)
      if (!a) continue
      const o = (out[a] ||= { all: [], routes: {} })
      o.all.push(p.p); (o.routes[route] ||= []).push(p.p)
    }
  })
  const agg: Agg = {}
  for (const [a, o] of Object.entries(out)) {
    if (o.all.length < 3) continue
    agg[a] = { n: o.all.length, med: median(o.all), routes: Object.entries(o.routes).map(([key, v]) => ({ key, n: v.length, med: median(v) })).sort((x, y) => y.n - x.n).slice(0, 8) }
  }
  return agg
}

async function cached(ctx: Ctx): Promise<Agg> {
  const cache = (globalThis as any).caches?.default
  const key = new Request("https://escale.live/__paye-compagnies/v1/" + new Date().toISOString().slice(0, 13))
  if (cache) { const hit = await cache.match(key); if (hit) return hit.json() }
  const agg = await aggregate(ctx.env)
  if (cache) ctx.waitUntil(cache.put(key, new Response(JSON.stringify(agg), { headers: { "Cache-Control": "public, max-age=3600" } })))
  return agg
}

const T = {
  fr: { loc: "fr-FR", have: (n: number, m: string, c: string) => `${n} voyageurs ont déclaré un billet aller-retour avec ${c} : prix médian ${m}.`, by: "Par trajet", th: ["Trajet", "Prix médian déclaré", "Déclarations"], note: "Prix déclarés par des visiteurs sur les pages de trajets, non vérifiés. À titre indicatif." },
  en: { loc: "en-GB", have: (n: number, m: string, c: string) => `${n} travellers reported a round-trip fare with ${c}: median fare ${m}.`, by: "By route", th: ["Route", "Median reported fare", "Reports"], note: "Fares reported by visitors on route pages, unverified. For guidance only." },
}

export const onRequest = async (ctx: Ctx) => {
  const response = await ctx.next()
  if (ctx.request.method !== "GET" || !response.ok || !(response.headers.get("content-type") || "").includes("text/html")) return response
  try {
    const html = await response.text()
    const m = html.match(/<div id="cie-paye" data-cie="([^"]*)" data-lang="(fr|en)">[\s\S]*?<\/div>/)
    if (!m) return new Response(html, response)
    const name = m[1].replace(/&#39;/g, "'").replace(/&amp;/g, "&"), lang = m[2] as "fr" | "en", t = T[lang]
    const agg = await cached(ctx)
    const a = agg[norm(name)]
    if (!a) return new Response(html, response)
    const money = (n: number) => new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
    const rows = a.routes.map((r) => `<tr><th scope="row">${esc(LABEL[r.key] || r.key.replace("-", " → "))}</th><td><strong>${esc(money(r.med))}</strong></td><td>${r.n}</td></tr>`).join("")
    const block = `<div id="cie-paye" data-cie="${esc(name)}" data-lang="${lang}" data-ssr="1"><p><strong>${esc(t.have(a.n, money(a.med), name))}</strong></p>` +
      (rows ? `<h3>${esc(t.by)}</h3><div class="bt-wrap"><table class="bt-table"><thead><tr>${t.th.map((h) => `<th scope="col">${esc(h)}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div>` : "") +
      `<p class="small">${esc(t.note)}</p></div>`
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    return new Response(html.replace(m[0], block), { status: response.status, headers })
  } catch {
    return response
  }
}
