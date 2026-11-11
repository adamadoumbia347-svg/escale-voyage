import { Ctx, esc, keysOf } from "./_lib/common"
import { shell, AUTRES } from "./bonsplans"
// « Les actus de la semaine » : articles publiés sans remise en ligne des fichiers du site.
//   /barometre-prix/actus/          → liste des articles, du plus récent au plus ancien
//   /barometre-prix/actus/<slug>/   → un article
// Chaque article est une valeur KV (clé actu:<slug>) : { slug, title, desc, date (AAAA-MM-JJ), body (HTML), maj? }.
// Ils sont écrits depuis l'extérieur (API Cloudflare), à partir des relevés réels du site : aucun prix inventé.
// Les adresses sont ajoutées au plan /barometre-prix/plan.xml et signalées chaque matin à IndexNow (src/bonsplans.ts).
export type Actu = { slug: string; title: string; desc: string; date: string; body: string; maj?: string }
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/
const dateFr = (d: string) => { const [y, m, j] = d.split("-").map(Number); return new Date(Date.UTC(y, m - 1, j)).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" }) }

export async function liste(ctx: Ctx): Promise<Actu[]> {
  const kv = ctx.env.ESCALE
  if (!kv) return []
  const cache = (globalThis as any).caches?.default
  const key = new Request("https://escale.live/__actus/v1/" + Math.floor(Date.now() / 600000)) // gardé 10 minutes
  if (cache) { const hit = await cache.match(key); if (hit) return hit.json() }
  const names = (await keysOf(ctx.env, "actu:", (p) => ctx.waitUntil(p), 200)).slice(0, 200)
  const all = (await Promise.all(names.map((k) => kv.get(k, "json").catch(() => null)))).filter((a: any) => a && SLUG.test(a.slug || "") && a.title && a.body && /^\d{4}-\d{2}-\d{2}$/.test(a.date || "")) as Actu[]
  all.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : a.slug.localeCompare(b.slug)))
  if (cache && all.length) ctx.waitUntil(cache.put(key, new Response(JSON.stringify(all), { headers: { "Cache-Control": "public, max-age=600" } })))
  return all
}

AUTRES.push(async (ctx) => { const l = await liste(ctx); return l.length ? ["/barometre-prix/actus/", ...l.map((a) => `/barometre-prix/actus/${a.slug}/`)] : [] })

// Dernier article, pour le lien de l'accueil
export async function dernier(ctx: Ctx): Promise<Actu | null> { try { return (await liste(ctx))[0] || null } catch { return null } }

export const onRequest = async (ctx: Ctx): Promise<Response> => {
  const path = new URL(ctx.request.url).pathname
  const m = path.match(/^\/barometre-prix\/actus(?:\/([a-z0-9-]+))?\/?$/)
  if (!m) return ctx.next()
  if (!path.endsWith("/")) return Response.redirect(new URL(path + "/", ctx.request.url).toString(), 301)
  const all = await liste(ctx)
  if (!m[1]) {
    const body = all.length ? `<section>${all.map((a) => `<article style="margin:0 0 22px"><h2 style="margin:0 0 4px;font-size:1.2rem"><a href="/barometre-prix/actus/${a.slug}/">${esc(a.title)}</a></h2><p style="margin:0;color:var(--muted,#5b6474);font-size:.9rem">${esc(dateFr(a.date))}</p><p style="margin:6px 0 0">${esc(a.desc)}</p></article>`).join("")}</section>` : `<section><p class="bt-lead">Le premier article arrive bientôt.</p></section>`
    return shell(ctx, { path: "/barometre-prix/actus/", title: "Les actus des vols Europe – Afrique : prix et bons plans | Escale", eyebrow: "Chaque semaine", h1: "Les actus de la semaine",
      desc: "Chaque semaine, ce qui bouge sur les prix des vols entre l'Europe et l'Afrique, d'après les relevés quotidiens d'Escale.", body, index: all.length > 0, article: true })
  }
  const a = all.find((x) => x.slug === m[1])
  if (!a) return ctx.next()
  const autres = all.filter((x) => x.slug !== a.slug).slice(0, 5)
  const ld = { "@context": "https://schema.org", "@type": "Article", headline: a.title, description: a.desc, datePublished: a.date, dateModified: a.maj || a.date, inLanguage: "fr",
    mainEntityOfPage: `https://escale.live/barometre-prix/actus/${a.slug}/`, author: { "@type": "Organization", name: "Escale", url: "https://escale.live/" }, publisher: { "@type": "Organization", name: "Escale", url: "https://escale.live/" } }
  const body = `<article class="actu"><p style="color:var(--muted,#5b6474);font-size:.9rem;margin:0 0 14px">Publié le ${esc(dateFr(a.date))}${a.maj && a.maj !== a.date ? `, mis à jour le ${esc(dateFr(a.maj))}` : ""}</p>${a.body}</article>` +
    `<script type="application/ld+json">${JSON.stringify(ld).replace(/</g, "\\u003c")}</script>` +
    (autres.length ? `<section><h2>Autres actus</h2><ul>${autres.map((x) => `<li><a href="/barometre-prix/actus/${x.slug}/">${esc(x.title)}</a></li>`).join("")}</ul></section>` : "") +
    `<section><h2>Voir aussi</h2><p class="bp-puces"><a href="/barometre-prix/actus/">Toutes les actus</a><a href="/barometre-prix/a-saisir/">À saisir aujourd'hui</a><a href="/barometre-prix/depuis/">Par ville de départ</a><a href="/barometre-prix/mois/">Par mois</a></p></section>`
  return shell(ctx, { path: `/barometre-prix/actus/${a.slug}/`, title: `${a.title} | Escale`, eyebrow: "Les actus de la semaine", h1: a.title, desc: a.desc, body, index: true, article: true })
}
