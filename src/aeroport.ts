import { Ctx, esc } from "./_lib/common"
// « L'aéroport vu par les voyageurs » : sur les guides « Arriver à l'aéroport de … » (/arriver-aeroport-abidjan/, /en/arriving-at-abidjan-airport/),
// les visiteurs déclarent, anonymement, leur attente à l'immigration, le prix payé pour le taxi vers le centre et s'ils ont acheté
// une carte SIM à l'aéroport. La page affiche des chiffres agrégés dès 3 déclarations (médianes, pourcentage). Données : clé KV aero:CODE.
// API : src/api/aeroport.ts. Bloc écrit par le serveur (src/worker.ts → onRequest ci-dessous). Rien d'inventé : sans déclaration, le bloc invite seulement à témoigner.
export type Visit = { w: number; taxi: number | null; sim: number | null; m: string; at: string } // w = attente en minutes (borne haute de la tranche), taxi en €, sim : 1 oui / 0 non
export type Agg = { n: number; wait: number; taxi: number | null; taxiN: number; simPct: number | null; simN: number; recent: number }
export const KEY = (code: string) => `aero:${code}`
export const MAX_KEEP = 500
export const CODES: Record<string, string> = { abidjan: "ABJ", accra: "ACC", alger: "ALG", algiers: "ALG", bamako: "BKO", casablanca: "CMN", conakry: "CKY", dakar: "DSS", douala: "DLA", kinshasa: "FIH", lagos: "LOS", lome: "LFW", tunis: "TUN" }
export const WAITS = [15, 30, 60, 120] // tranches : moins de 15 min, 15-30, 30-60, plus d'une heure

const median = (a: number[]) => { const s = a.slice().sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2) }

export function aggregate(list: Visit[]): Agg | null {
  if (list.length < 3) return null
  const taxis = list.map((v) => v.taxi).filter((x): x is number => typeof x === "number" && x > 0)
  const tmed = taxis.length ? median(taxis) : null
  const kept = tmed ? taxis.filter((x) => x >= tmed * 0.3 && x <= tmed * 3) : []
  const sims = list.map((v) => v.sim).filter((x): x is number => x === 0 || x === 1)
  const year = new Date(Date.now() - 365 * 864e5).toISOString().slice(0, 7)
  return { n: list.length, wait: median(list.map((v) => v.w)), taxi: kept.length >= 3 ? median(kept) : null, taxiN: kept.length, simPct: sims.length >= 3 ? Math.round((100 * sims.filter((x) => x === 1).length) / sims.length) : null, simN: sims.length, recent: list.filter((v) => v.m >= year).length }
}

type T = { loc: string; title: string; none: string; have: string; taxi: string; sim: string; cta: string; wait: string; waitOpts: string[]; taxiL: string; simL: string; simOpts: [string, string]; month: string; send: string; thanks: string; error: string; note: string }
const L: Record<string, T> = {
  fr: { loc: "fr-FR", title: "L'aéroport vu par les voyageurs", none: "Personne n'a encore raconté son arrivée ici. Soyez le premier : trois réponses suffisent pour afficher des chiffres utiles à tous.",
    have: "{n} voyageurs ont raconté leur arrivée : attente à l'immigration le plus souvent {w}.", taxi: " Taxi jusqu'au centre : environ {t} ({k} réponses).", sim: " {p} % ont acheté une carte SIM à l'aéroport.",
    cta: "Vous êtes passé par cet aéroport ? Racontez en 20 secondes, sans vous identifier.", wait: "Attente à l'immigration", waitOpts: ["Moins de 15 min", "15 à 30 min", "30 min à 1 h", "Plus d'une heure"], taxiL: "Taxi jusqu'au centre, prix payé (€ environ)", simL: "Carte SIM achetée à l'aéroport ?", simOpts: ["Oui", "Non"], month: "Mois de l'arrivée", send: "Partager mon arrivée", thanks: "Merci ! Votre témoignage a été ajouté.", error: "Impossible d'envoyer pour le moment. Réessayez plus tard.", note: "Chiffres déclarés par des visiteurs, non vérifiés. À titre indicatif : l'attente et les prix varient selon l'heure et la saison." },
  en: { loc: "en-GB", title: "The airport, as travellers saw it", none: "Nobody has shared their arrival here yet. Be the first: three answers are enough to show useful figures to everyone.",
    have: "{n} travellers shared their arrival: immigration wait most often {w}.", taxi: " Taxi to the centre: about {t} ({k} answers).", sim: " {p}% bought a SIM card at the airport.",
    cta: "Been through this airport? Tell us in 20 seconds, anonymously.", wait: "Immigration wait", waitOpts: ["Under 15 min", "15 to 30 min", "30 min to 1 h", "Over an hour"], taxiL: "Taxi to the centre, price paid (approx. €)", simL: "Bought a SIM card at the airport?", simOpts: ["Yes", "No"], month: "Month of arrival", send: "Share my arrival", thanks: "Thank you! Your report has been added.", error: "Could not send right now. Please try again later.", note: "Figures reported by visitors, unverified. For guidance: waits and prices vary with time of day and season." },
}
const waitLabel = (w: number, t: T) => t.waitOpts[Math.max(0, WAITS.indexOf(w))] || t.waitOpts[3]

export function render(lang: string, code: string, a: Agg | null): string {
  const t = L[lang] || L.fr
  const money = (n: number) => { try { return new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n) } catch { return Math.round(n) + " €" } }
  const fill = (x: string, o: Record<string, string>) => x.replace(/\{(\w+)\}/g, (_, k) => o[k])
  const now = new Date(), maxMonth = now.toISOString().slice(0, 7), minMonth = new Date(Date.UTC(now.getUTCFullYear() - 2, now.getUTCMonth(), 1)).toISOString().slice(0, 7)
  const summary = a ? `<p class="ap-have"><strong>${esc(fill(t.have, { n: String(a.n), w: waitLabel(a.wait, t).toLowerCase() }))}</strong>` +
    (a.taxi ? esc(fill(t.taxi, { t: money(a.taxi), k: String(a.taxiN) })) : "") + (a.simPct !== null ? esc(fill(t.sim, { p: String(a.simPct) })) : "") + `</p>` : `<p class="ap-none">${esc(t.none)}</p>`
  const style = `<style>.ap{margin:22px 0 8px;padding:16px 18px;border:1px solid var(--line,#e5e7eb);border-radius:16px;background:var(--surface,#fff)}.ap h2{margin:0 0 8px;font-size:1.15rem}.ap-none,.ap-cta,.ap-note{color:var(--muted,#5b6474)}.ap-cta{margin:10px 0 8px}.ap-form{display:grid;gap:10px;grid-template-columns:1fr 1fr;align-items:end}.ap-form label{display:grid;gap:4px;font-size:.85rem;color:var(--muted,#5b6474)}.ap-form input,.ap-form select{font:inherit;padding:9px 10px;border:1px solid var(--line,#e5e7eb);border-radius:10px;background:var(--surface,#fff);color:inherit;min-width:0}.ap-form button{font:inherit;font-weight:700;padding:11px 16px;border:0;border-radius:999px;background:var(--teal-d,#0b8577);color:#fff;cursor:pointer;grid-column:1/-1}.ap-note{font-size:.8rem;margin:10px 0 0}.ap-ok{color:#18794e;font-weight:600}.ap-ko{color:#b42318}@media(max-width:480px){.ap-form{grid-template-columns:1fr}}</style>`
  const form = `<p class="ap-cta">${esc(t.cta)}</p><form class="ap-form" data-code="${code}" action="/api/aeroport" method="post">` +
    `<label>${esc(t.wait)}<select name="attente" required>${WAITS.map((w, i) => `<option value="${w}">${esc(t.waitOpts[i])}</option>`).join("")}</select></label>` +
    `<label>${esc(t.month)}<input type="month" name="mois" min="${minMonth}" max="${maxMonth}" required></label>` +
    `<label>${esc(t.taxiL)}<input type="number" name="taxi" min="1" max="300" step="1" inputmode="numeric"></label>` +
    `<label>${esc(t.simL)}<select name="sim"><option value="">—</option><option value="1">${esc(t.simOpts[0])}</option><option value="0">${esc(t.simOpts[1])}</option></select></label>` +
    `<input type="text" name="site-web" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true"><input type="hidden" name="code" value="${code}">` +
    `<button type="submit">${esc(t.send)}</button><p class="ap-msg" style="grid-column:1/-1" role="status" hidden></p></form>`
  const script = `<script>(function(){var f=document.querySelector(".ap-form");if(!f)return;f.addEventListener("submit",function(e){e.preventDefault();var b=f.querySelector("button"),m=f.querySelector(".ap-msg");b.disabled=true;var d={};new FormData(f).forEach(function(v,k){d[k]=v});fetch("/api/aeroport",{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify(d)}).then(function(r){return r.ok?r.json():Promise.reject()}).then(function(){m.textContent=${JSON.stringify(t.thanks)};m.className="ap-msg ap-ok";m.hidden=false;f.querySelectorAll("label,button").forEach(function(x){x.hidden=true})}).catch(function(){m.textContent=${JSON.stringify(t.error)};m.className="ap-msg ap-ko";m.hidden=false;b.disabled=false})})})()</script>`
  return `${style}<section class="ap" id="aeroport-voyageurs"><h2>${esc(t.title)}</h2>${summary}${form}<p class="ap-note">${esc(t.note)}</p></section>${script}`
}

export async function readVisits(env: any, code: string): Promise<Visit[]> {
  if (!env?.ESCALE) return []
  try { return ((await env.ESCALE.get(KEY(code), "json")) as Visit[]) || [] } catch { return [] }
}

// Pages « Arriver à l'aéroport de … » : le bloc est inséré avant la section « Pièges à éviter » (fr) / « Pitfalls » (en), sinon avant le dernier h2
export const onRequest = async (ctx: Ctx) => {
  const response = await ctx.next()
  if (ctx.request.method !== "GET" || !response.ok || !(response.headers.get("content-type") || "").includes("text/html")) return response
  try {
    const path = new URL(ctx.request.url).pathname
    const m = path.match(/^\/(?:arriver-aeroport-([a-z-]+)|en\/arriving-at-([a-z-]+)-airport)\/?$/)
    const slug = m ? (m[1] || m[2]) : ""
    const code = CODES[slug]
    if (!code) return response
    const lang = path.startsWith("/en/") ? "en" : "fr"
    const html = await response.text()
    const block = render(lang, code, aggregate(await readVisits(ctx.env, code)))
    const anchor = html.search(/<section>\s*<h2>(Pièges|Pitfalls|Traps|Scams|Things to avoid)/)
    const at = anchor >= 0 ? anchor : html.lastIndexOf("<section>")
    const out = at >= 0 ? html.slice(0, at) + block + html.slice(at) : html
    const headers = new Headers(response.headers)
    headers.delete("content-length")
    return new Response(out, { status: response.status, headers })
  } catch {
    return response
  }
}
