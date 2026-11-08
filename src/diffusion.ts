import { Ctx, esc } from "./_lib/common"
import { rows } from "./barometre"
import { ARCH, Snap, Summary, compute } from "./indice"
import { deals } from "./saisir"
// Diffusion de l'indice des prix hors du site, écrite par le serveur (aucun fichier statique) :
// - flux RSS : /barometre-prix/flux.xml (fr), /en/price-index/feed.xml (en) : les trajets à saisir du jour et les archives mensuelles
// - widget à intégrer (iframe) : /indice-prix/widget/ (fr), /en/price-index/widget/ (en)
// - communiqué du mois, image 1080×1350 prête à poster : /indice-prix/communique/ (mois en cours), /indice-prix/2026-11/communique/ (archive),
//   /en/price-index/press/ et /en/price-index/2026-11/press/ en anglais. Le PNG se fabrique dans le navigateur (bouton), sans service tiers.
type Lang = "fr" | "en"
const SITE = "https://escale.live"
const T = {
  fr: { loc: "fr-FR", index: "/indice-prix/", deals: "/barometre-prix/a-saisir/", feed: "/barometre-prix/flux.xml",
    feedTitle: "Escale · prix des vols Europe – Afrique", feedDesc: "Chaque jour, les trajets sous leur prix habituel ; chaque mois, l'Indice Escale des prix des vols Europe – Afrique.",
    dealsTitle: (n: number, d: string) => `À saisir le ${d} : ${n} trajet${n > 1 ? "s" : ""} sous ${n > 1 ? "leur" : "son"} prix habituel`, noDeals: (d: string) => `${d} : aucun trajet nettement sous son prix habituel`,
    archTitle: (m: string) => `Indice Escale des prix : ${m}`, month: (ym: string) => { const [y, m] = ym.split("-").map(Number); return new Date(Date.UTC(y, m - 1, 1)).toLocaleDateString("fr-FR", { month: "long", year: "numeric", timeZone: "UTC" }) },
    wTitle: "Indice Escale des prix", wSub: (span: string, n: number) => `variation médiane des billets Europe – Afrique sur ${span} · ${n} trajets`, wGo: "Voir l'indice", wWait: "Indice en cours de calcul",
    cTitle: "Indice Escale des prix des vols", cSub: "Europe – Afrique", cBig: (span: string) => `variation médiane sur ${span}`, cN: (n: number, u: number, d: number) => `${n} grands trajets suivis chaque jour · ${u} en hausse · ${d} en baisse`,
    cUp: "Plus fortes hausses", cDown: "Plus fortes baisses", cFoot: "Données libres · escale.live/indice-prix", cFrom: "dès",
    pTitle: (m: string) => `Communiqué : Indice Escale des prix, ${m}`, pLead: "Image prête à poster (1080 × 1350, format portrait) et phrase à citer. Téléchargez le PNG, puis publiez-le sur TikTok, WhatsApp, Facebook ou Instagram avec le texte ci-dessous.",
    pBtn: "⬇️ Télécharger en PNG", pCopy: "📋 Copier le texte", pCopied: "✅ Copié", pBack: "Retour à l'indice", pHash: "#Escale #VolsAfrique #Diaspora #PrixDesBillets", pSource: "Source : Escale," },
  en: { loc: "en-GB", index: "/en/price-index/", deals: "/en/price-index/deals-today/", feed: "/en/price-index/feed.xml",
    feedTitle: "Escale · Europe – Africa air fares", feedDesc: "Every day, the routes below their usual price; every month, the Escale Price Index for Europe – Africa flights.",
    dealsTitle: (n: number, d: string) => `Worth booking on ${d}: ${n} route${n > 1 ? "s" : ""} below ${n > 1 ? "their" : "its"} usual price`, noDeals: (d: string) => `${d}: no route clearly below its usual price`,
    archTitle: (m: string) => `Escale Price Index: ${m}`, month: (ym: string) => { const [y, m] = ym.split("-").map(Number); return new Date(Date.UTC(y, m - 1, 1)).toLocaleDateString("en-GB", { month: "long", year: "numeric", timeZone: "UTC" }) },
    wTitle: "Escale Price Index", wSub: (span: string, n: number) => `median change in Europe – Africa fares over ${span} · ${n} routes`, wGo: "See the index", wWait: "Index being computed",
    cTitle: "Escale Price Index, air fares", cSub: "Europe – Africa", cBig: (span: string) => `median change over ${span}`, cN: (n: number, u: number, d: number) => `${n} major routes tracked daily · ${u} up · ${d} down`,
    cUp: "Biggest rises", cDown: "Biggest drops", cFoot: "Open data · escale.live/en/price-index", cFrom: "from",
    pTitle: (m: string) => `Press kit: Escale Price Index, ${m}`, pLead: "Ready-to-post image (1080 × 1350, portrait) and a sentence to quote. Download the PNG, then post it on TikTok, WhatsApp, Facebook or Instagram with the text below.",
    pBtn: "⬇️ Download PNG", pCopy: "📋 Copy the text", pCopied: "✅ Copied", pBack: "Back to the index", pHash: "#Escale #AfricaFlights #Diaspora #AirFares", pSource: "Source: Escale," },
}
const money = (n: number, loc: string) => new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
const sign = (v: number, lang: Lang) => (v > 0 ? "+" : v < 0 ? "−" : "") + Math.abs(v) + (lang === "fr" ? " %" : "%")
const rfc = (iso: string) => new Date(iso + (iso.length === 10 ? "T06:00:00Z" : "")).toUTCString()
const cdata = (s: string) => `<![CDATA[${s.replace(/]]>/g, "]]]]><![CDATA[>")}]]>`

async function archives(env: any): Promise<[string, Snap][]> {
  if (!env?.ESCALE) return []
  try {
    const { keys } = await env.ESCALE.list({ prefix: ARCH, limit: 60 })
    const months = keys.map((k: any) => k.name.slice(ARCH.length)).filter((m: string) => /^\d{4}-\d{2}$/.test(m)).sort().reverse().slice(0, 12)
    const snaps = await Promise.all(months.map((m: string) => env.ESCALE.get(ARCH + m, "json").catch(() => null)))
    return months.map((m: string, i: number) => [m, snaps[i]] as [string, Snap]).filter((x: [string, Snap]) => x[1])
  } catch { return [] }
}

// ---- Flux RSS ----
export async function rss(ctx: Ctx, lang: Lang): Promise<Response> {
  const t = T[lang]
  const cache = (globalThis as any).caches?.default
  const key = new Request(`${SITE}/__rss/v1/${lang}/` + new Date().toISOString().slice(0, 13))
  if (cache) { const hit = await cache.match(key); if (hit) return hit }
  const [d, arch] = await Promise.all([deals(ctx.env, ctx.waitUntil).catch(() => null), archives(ctx.env)])
  const items: string[] = []
  if (d && d.total) {
    const day = new Date().toLocaleDateString(t.loc, { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Paris" })
    const body = d.items.length ? `<ul>${d.items.slice(0, 10).map((r) => `<li><a href="${SITE}/${r.path}/">${esc(r.label)}</a>: ${esc(money(r.price, t.loc))} (−${r.diff}${lang === "fr" ? " %" : "%"})</li>`).join("")}</ul>` : ""
    items.push(`<item><title>${esc(d.items.length ? t.dealsTitle(d.items.length, day) : t.noDeals(day))}</title><link>${SITE}${t.deals}</link><guid isPermaLink="false">escale-deals-${d.date}</guid><pubDate>${rfc(d.date)}</pubDate><description>${cdata(body || esc(t.noDeals(day)))}</description></item>`)
  }
  for (const [m, s] of arch) {
    const sum = s.sum?.[lang]
    const body = sum ? `<p>${esc(sum.quote)}</p>` : ""
    items.push(`<item><title>${esc(t.archTitle(t.month(m)))}</title><link>${SITE}${t.index}${m}/</link><guid isPermaLink="true">${SITE}${t.index}${m}/</guid><pubDate>${rfc(s.date)}</pubDate><description>${cdata(body)}</description></item>`)
  }
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>${esc(t.feedTitle)}</title><link>${SITE}${t.index}</link><description>${esc(t.feedDesc)}</description><language>${lang === "fr" ? "fr-FR" : "en-GB"}</language><atom:link href="${SITE}${t.feed}" rel="self" type="application/rss+xml"/><lastBuildDate>${new Date().toUTCString()}</lastBuildDate>${items.join("")}</channel></rss>`
  const res = new Response(xml, { headers: { "Content-Type": "application/rss+xml; charset=utf-8", "Cache-Control": "public, max-age=3600" } })
  if (cache) ctx.waitUntil(cache.put(key, res.clone()))
  return res
}

// ---- Widget (iframe) ----
export async function widget(ctx: Ctx, lang: Lang): Promise<Response> {
  const t = T[lang]
  const cache = (globalThis as any).caches?.default
  const key = new Request(`${SITE}/__widget-indice/v1/${lang}/` + new Date().toISOString().slice(0, 10))
  if (cache) { const hit = await cache.match(key); if (hit) return hit }
  const list = await rows(ctx)
  const s = list.length ? compute(list, lang) : null
  const color = s ? (s.med <= -3 ? "#0b8a4a" : s.med >= 3 ? "#c2410c" : "#5a6474") : "#5a6474"
  const html = `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>${esc(t.wTitle)}</title>` +
    `<style>:root{--bg:#fff;--ink:#141a24;--muted:#5a6474;--line:#d9dee6;--teal:#0b8577}@media(prefers-color-scheme:dark){:root{--bg:#171e28;--ink:#e9edf3;--muted:#9aa5b5;--line:#2a3442;--teal:#3ec1ae}}*{box-sizing:border-box}html,body{margin:0;height:100%}body{font:14px/1.35 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg)}` +
    `a.card{display:flex;flex-direction:column;justify-content:space-between;gap:6px;height:100%;padding:12px 14px;border:1px solid var(--line);border-radius:12px;color:inherit;text-decoration:none}a.card:hover{border-color:var(--teal)}.top{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--muted)}.mark{background:var(--teal);color:#fff;font:800 11px/1 system-ui,sans-serif;padding:4px 6px;border-radius:4px}` +
    `.num{font:800 40px/1 system-ui,sans-serif;letter-spacing:-.02em}.sub{font-size:12px;color:var(--muted)}.go{align-self:flex-start;background:var(--teal);color:#fff;font-weight:700;font-size:12px;padding:6px 10px;border-radius:999px}</style></head><body>` +
    `<a class="card" href="${SITE}${t.index}?utm_source=widget&utm_medium=iframe" target="_blank" rel="noopener"><span class="top"><span class="mark">escale</span>${esc(t.wTitle)}${s ? ` · ${esc(s.date)}` : ""}</span>` +
    (s ? `<span class="num" style="color:${color}">${esc(sign(s.med, lang))}</span><span class="sub">${esc(t.wSub(s.span, s.n))}</span>` : `<span class="sub">${esc(t.wWait)}</span>`) +
    `<span class="go">${esc(t.wGo)} →</span></a></body></html>`
  const res = new Response(html, { headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "public, max-age=3600", "X-Robots-Tag": "noindex" } })
  if (cache && s) ctx.waitUntil(cache.put(key, res.clone()))
  return res
}

// ---- Communiqué du mois (image SVG → PNG dans le navigateur) ----
function svg(s: Summary, lang: Lang, monthLabel: string): string {
  const t = T[lang]
  const W = 1080, H = 1350
  const color = s.med <= -3 ? "#1f9d61" : s.med >= 3 ? "#e0633a" : "#5f6b7a"
  const line = (items: Summary["top"], y0: number, title: string, c: string) => {
    if (!items.length) return ""
    let out = `<text x="80" y="${y0}" font-size="30" font-weight="700" fill="#0b1b2b">${esc(title)}</text>`
    items.slice(0, 3).forEach((r, i) => {
      const y = y0 + 52 + i * 50
      out += `<text x="80" y="${y}" font-size="30" fill="#0b1b2b">${esc(r.label)}</text><text x="1000" y="${y}" font-size="30" font-weight="700" fill="${c}" text-anchor="end">${esc(sign(r.v, lang))}  <tspan font-weight="500" fill="#5f6b7a" font-size="24">${esc(t.cFrom)} ${esc(money(r.price, t.loc))}</tspan></text>`
    })
    return out
  }
  const f = `font-family="Instrument Sans, Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif"`
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" ${f}>` +
    `<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9faf5"/><stop offset="1" stop-color="#ffffff"/></linearGradient></defs>` +
    `<rect width="${W}" height="${H}" fill="url(#bg)"/><rect x="0" y="0" width="${W}" height="14" fill="#0b8577"/>` +
    `<g transform="translate(80 90)"><rect width="64" height="64" rx="16" fill="#0b8577"/><path transform="translate(10 10) scale(1.85)" d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" fill="#fff"/></g>` +
    `<text x="164" y="118" font-size="30" font-weight="700" fill="#0b1b2b">escale</text><text x="164" y="150" font-size="22" fill="#5f6b7a">${esc(t.cFoot)}</text>` +
    `<text x="80" y="260" font-size="44" font-weight="800" fill="#0b1b2b">${esc(t.cTitle)}</text><text x="80" y="310" font-size="34" fill="#5f6b7a">${esc(t.cSub)} · ${esc(monthLabel)}</text>` +
    `<text x="80" y="520" font-size="190" font-weight="800" fill="${color}" letter-spacing="-6">${esc(sign(s.med, lang))}</text>` +
    `<text x="80" y="585" font-size="32" fill="#0b1b2b">${esc(t.cBig(s.span))}</text><text x="80" y="628" font-size="26" fill="#5f6b7a">${esc(t.cN(s.n, s.up, s.down))}</text>` +
    `<line x1="80" y1="690" x2="1000" y2="690" stroke="#cfe3dd" stroke-width="2"/>` +
    line(s.top, 760, t.cUp, "#e0633a") + line(s.bottom, 1000, t.cDown, "#1f9d61") +
    `<text x="80" y="1290" font-size="24" fill="#5f6b7a">${esc(s.date)} · ${esc(t.cFoot)}</text></svg>`
}

export async function communique(ctx: Ctx, lang: Lang, ym: string | null): Promise<Response> {
  const t = T[lang]
  let s: Summary | null = null, monthLabel = ""
  if (ym) {
    const snap: Snap | null = ctx.env.ESCALE ? await ctx.env.ESCALE.get(ARCH + ym, "json").catch(() => null) : null
    s = snap?.sum?.[lang] || null; monthLabel = t.month(ym)
  } else {
    const list = await rows(ctx); s = list.length ? compute(list, lang) : null; monthLabel = t.month(new Date().toISOString().slice(0, 7))
  }
  if (!s) return ctx.next()
  const img = svg(s, lang, monthLabel)
  const text = `${s.quote}\n\n${t.pSource} ${SITE}${t.index}\n${t.pHash}`
  const html = `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>${esc(t.pTitle(monthLabel))} | Escale</title>` +
    `<style>body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#0b1b2b;background:#f4f6f8}main{max-width:720px;margin:0 auto;padding:24px 16px 60px}h1{font-size:1.5rem;margin:0 0 8px}.lead{color:#5f6b7a}.card{background:#fff;border:1px solid #e5e7eb;border-radius:16px;padding:12px;margin:16px 0}svg{display:block;width:100%;height:auto;border-radius:10px}.row{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0}button,a.btn{font:inherit;font-weight:700;padding:11px 18px;border:0;border-radius:999px;background:#0b8577;color:#fff;cursor:pointer;text-decoration:none}a.btn.ghost,button.ghost{background:#fff;color:#0b8577;border:1px solid #0b8577}pre{white-space:pre-wrap;font:15px/1.5 system-ui,sans-serif;background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:14px}</style></head><body><main>` +
    `<h1>${esc(t.pTitle(monthLabel))}</h1><p class="lead">${esc(t.pLead)}</p><div class="card" id="card">${img}</div>` +
    `<div class="row"><button type="button" id="dl">${esc(t.pBtn)}</button><button type="button" class="ghost" id="cp">${esc(t.pCopy)}</button><a class="btn ghost" href="${t.index}${ym ? ym + "/" : ""}">${esc(t.pBack)}</a></div>` +
    `<pre id="txt">${esc(text)}</pre>` +
    `<script>(function(){var s=document.querySelector("#card svg"),b=document.getElementById("dl");b.addEventListener("click",function(){var x=new XMLSerializer().serializeToString(s),u=URL.createObjectURL(new Blob([x],{type:"image/svg+xml;charset=utf-8"})),im=new Image();im.onload=function(){var c=document.createElement("canvas");c.width=1080;c.height=1350;var g=c.getContext("2d");g.drawImage(im,0,0,1080,1350);URL.revokeObjectURL(u);c.toBlob(function(bl){var a=document.createElement("a");a.href=URL.createObjectURL(bl);a.download="indice-escale-${esc(ym || new Date().toISOString().slice(0, 7))}.png";document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},1000)},"image/png")};im.src=u});` +
    `document.getElementById("cp").addEventListener("click",function(e){var t=document.getElementById("txt").textContent;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){e.target.textContent=${JSON.stringify(t.pCopied)}},function(){prompt("",t)})})})()</script></main></body></html>`
  return new Response(html, { headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "public, max-age=3600", "X-Robots-Tag": "noindex" } })
}

// Bloc « Diffuser l'indice » ajouté sous l'indice (flux RSS, widget, communiqué)
export function shareBlock(lang: Lang, ym: string | null = null): string {
  const t = T[lang]
  const embed = `<iframe src="${SITE}${lang === "fr" ? "/indice-prix/widget/" : "/en/price-index/widget/"}" title="${esc(t.wTitle)}" width="320" height="170" loading="lazy" style="border:0;max-width:100%"></iframe>`
  const L = lang === "fr" ? { h: "Diffuser l'indice", press: "Image du mois prête à poster (communiqué)", feed: "Flux RSS (trajets à saisir et archives)", widget: "Intégrer l'indice sur votre site : copiez ce code" }
    : { h: "Spread the index", press: "Ready-to-post monthly image (press kit)", feed: "RSS feed (deals of the day and archives)", widget: "Embed the index on your site: copy this code" }
  return `<h2>${esc(L.h)}</h2><ul class="ix-list"><li><a href="${t.index}${ym ? ym + "/" : ""}${lang === "fr" ? "communique" : "press"}/">${esc(L.press)}</a></li><li><a href="${t.feed}">${esc(L.feed)}</a></li></ul>` +
    `<p class="small">${esc(L.widget)}</p><pre class="small" style="white-space:pre-wrap;word-break:break-all;background:var(--soft,#f4f6f8);border-radius:10px;padding:10px 12px">${esc(embed)}</pre><p>${embed}</p>`
}
