// Point d'entrée du Worker Cloudflare d'Escale.
// - /api/* : fonctions serveur (prix, calendrier, bons plans, position, alertes, formulaires, admin, tâches)
// - pages trajets : prix réels écrits dans la page (titre, haut de page, prix par mois), pour les visiteurs et Google
// - /barometre-prix/ : tableau des prix et de leur évolution, écrit dans la page
// - / (accueil) : prix des boutons « Trajets populaires »
// - tout le reste : fichiers du dossier site/ (servis directement par Cloudflare, sans passer par ce code)
import { Ctx, Env, json } from "./_lib/common"
import * as prix from "./api/prix"
import * as explore from "./api/explore"
import * as calendar from "./api/calendar"
import * as deals from "./api/deals"
import * as geo from "./api/geo"
import * as alert from "./api/alert"
import * as form from "./api/form"
import * as admin from "./api/admin"
import * as cron from "./api/cron"
import { releve } from "./releve"
import * as push from "./api/push"
import * as populaires from "./api/populaires"
import * as ruban from "./api/ruban"
import * as clic from "./api/clic"
import * as fx from "./api/fx"
import * as grille from "./api/grille"
import * as weekends from "./api/weekends"
import * as verdictApi from "./api/verdict"
import * as compteur from "./api/compteur"
import * as paye from "./api/paye"
import * as aeroApi from "./api/aeroport"
import * as aeroport from "./aeroport"
import * as apercu from "./apercu-prix"
import * as barometre from "./barometre"
import * as indice from "./indice"
import * as accueil from "./accueil"
import * as saisir from "./saisir"
import * as bonsplans from "./bonsplans"
import * as actus from "./actus"
import * as diffusion from "./diffusion"
import * as compagnie from "./compagnie"
import { sendDigest, sendNewsletter } from "./digest"
import { buildLot } from "./lot"
import { indexNow } from "./indexnow"
import * as gains from "./gains"

const API: Record<string, any> = { push, prix, explore, calendar, deals, geo, alert, form, admin, cron, populaires, ruban, clic, fx, grille, weekends, verdict: verdictApi, connus: accueil, compteur, paye, aeroport: aeroApi, gains }

const escale = {
  async fetch(request: Request, env: Env & { ASSETS: { fetch: (r: Request) => Promise<Response> } }, ctx: { waitUntil: (p: Promise<any>) => void }) {
    const c: Ctx = { request, env, waitUntil: (p) => ctx.waitUntil(p), next: () => env.ASSETS.fetch(request) }
    const path = new URL(request.url).pathname
    if (path.startsWith("/api/")) {
      const mod = API[path.slice(5).replace(/\/$/, "")]
      if (!mod) return json({ error: "not found" }, { status: 404 })
      const m = request.method.charAt(0) + request.method.slice(1).toLowerCase()
      const handler = mod[`onRequest${m}`] || mod.onRequest
      if (!handler) return json({ error: "Méthode non autorisée" }, { status: 405 })
      return handler(c)
    }
    // Adresse courte d'une recherche préremplie, pour les messages WhatsApp : /v/LYS-ALG (ou /v/LYS-ALG-en) -> /?type=vols&from=LYS&to=ALG
    const court = path.match(/^\/v\/([A-Za-z]{3})-([A-Za-z]{3})(?:-([a-z]{2}))?\/?$/)
    if (court) return new Response(null, { status: 302, headers: { Location: `/?type=vols&from=${court[1].toUpperCase()}&to=${court[2].toUpperCase()}${court[3] ? "&lang=" + court[3] : ""}`, "X-Robots-Tag": "noindex", "Cache-Control": "public, max-age=3600" } })
    // Bons plans par ville de départ et par mois (src/bonsplans.ts) : pages écrites par le serveur à partir des relevés
    if (/^\/barometre-prix\/actus(\/|$)/.test(path)) return actus.onRequest(c)
    if (bonsplans.ROUTE.test(path) || path === "/barometre-prix/plan.xml") return bonsplans.onRequest(c)
    if (path === "/barometre-prix/" || path === "/barometre-prix") {
      const r = await barometre.onRequest(c)
      if (!r.ok || !(r.headers.get("content-type") || "").includes("text/html")) return r
      const h = new Headers(r.headers); h.delete("content-length")
      return new Response((await r.text()).replace("</main>", `<div class="wrap">${bonsplans.LIENS}</div></main>`), { status: r.status, headers: h })
    }
    // Diffusion de l'indice (src/diffusion.ts) : flux RSS, widget, communiqué du mois
    if (path === "/barometre-prix/flux.xml") return diffusion.rss(c, "fr")
    if (path === "/en/price-index/feed.xml") return diffusion.rss(c, "en")
    if (/^\/indice-prix\/widget\/?$/.test(path)) return diffusion.widget(c, "fr")
    if (/^\/en\/price-index\/widget\/?$/.test(path)) return diffusion.widget(c, "en")
    const com = path.match(/^\/(indice-prix|en\/price-index)\/(?:(\d{4}-\d{2})\/)?(communique|press)\/?$/)
    if (com) return diffusion.communique(c, com[1] === "indice-prix" ? "fr" : "en", com[2] || null)
    if (path === "/indice-prix/donnees.csv" || path === "/en/price-index/data.csv") return indice.donneesCsv(c) // série quotidienne en données libres
    // Indice des prix : page du jour et archives mensuelles (/indice-prix/2026-11/)
    if (/^\/(en\/price-index|indice-prix)(\/(\d{4}-\d{2}\/?|(pays|country)\/[a-z-]+\/?)?)?$/.test(path)) return indice.onRequest(c)
    if (path === "/") return accueil.onRequest(c)
    // Guides « Arriver à l'aéroport » : bloc « l'aéroport vu par les voyageurs » (src/aeroport.ts)
    if (/^\/(arriver-aeroport-|en\/arriving-at-)/.test(path)) return aeroport.onRequest(c)
    // Pages compagnies : bloc « ce que les voyageurs ont payé » (src/compagnie.ts)
    if (/^\/(en\/airline|compagnie)\//.test(path)) return compagnie.onRequest(c)
    // « À saisir aujourd'hui » : page écrite par le serveur (pas de fichier statique)
    if (path === "/barometre-prix/a-saisir/" || path === "/barometre-prix/a-saisir") return saisir.page(c, "fr")
    if (path === "/en/price-index/deals-today/" || path === "/en/price-index/deals-today") return saisir.page(c, "en")
    return apercu.onRequest(c)
  },
  // Chaque matin à 6 h UTC (voir « triggers » dans wrangler.jsonc) : vérification des alertes prix ; lundi et jeudi, message WhatsApp à coller
  async scheduled(event: { cron?: string }, env: Env, ctx: { waitUntil: (p: Promise<any>) => void }) {
    // Toutes les 10 minutes entre 3 h et 6 h UTC : relevé des prix du baromètre, par tranches (src/releve.ts)
    if (event?.cron && event.cron !== "0 6 * * *") {
      ctx.waitUntil(releve(env).then((r) => console.log("relevé des prix", JSON.stringify(r))))
      return
    }
    // Copie groupée des relevés (src/lot.ts) : refaite une fois par jour, juste après le relevé de la nuit
    ctx.waitUntil(buildLot(env).then((l) => console.log("copie groupée des relevés", Object.keys(l.h).length)).catch((e) => console.log("copie groupée erreur", String(e))))
    // Gains réels Travelpayouts pour le bilan du lundi (src/gains.ts) : une requête par jour, résumé dans la clé gains:v1
    ctx.waitUntil(gains.gains(env).then((r) => console.log("gains", JSON.stringify(r))).catch((e) => console.log("gains erreur", String(e))))
    ctx.waitUntil(cron.checkAlerts(env).then((r) => console.log("alertes", JSON.stringify(r))))
    // Archive du mois de l'indice des prix (src/indice.ts) : le relevé du jour remplace celui de la veille, puis le mois reste figé
    ctx.waitUntil(indice.archiveIndice(env).then((r) => console.log("indice archive", JSON.stringify(r))).catch((e) => console.log("indice archive erreur", String(e))))
    // IndexNow : pages modifiées depuis 2 jours signalées aux moteurs de recherche (src/indexnow.ts)
    const cx: Ctx = { request: new Request("https://escale.live/__cron"), env, waitUntil: (p) => ctx.waitUntil(p), next: () => Promise.resolve(new Response(null, { status: 404 })) }
    ctx.waitUntil(bonsplans.urls(cx).catch(() => [] as string[]).then((extra) => indexNow(env, Date.now(), extra)).then((r) => console.log("IndexNow", JSON.stringify(r))).catch((e) => console.log("IndexNow erreur", String(e))))
    // Lundi et jeudi : e-mail avec le message WhatsApp des bons plans, prêt à coller dans la chaîne (src/digest.ts)
    const day = new Date().getUTCDay()
    if (day === 1 || day === 4) ctx.waitUntil(sendDigest(env).then((r) => console.log("message WhatsApp", JSON.stringify(r))))
    // Le lundi seulement : e-mail des bons plans aux inscrits (une fois par semaine au plus)
    if (day === 1) ctx.waitUntil(sendNewsletter(env).then((r) => console.log("bons plans par e-mail", JSON.stringify(r))))
  },
}

// Diagnostic de consommation : une requête envoyée avec l'en-tête « X-Escale-Diag: 1 » reçoit en retour, dans « X-Escale-KV »,
// le nombre d'opérations KV qu'elle a coûtées (lectures, écritures, listes, suppressions), tâches de fond comprises.
// Sans cet en-tête, rien ne change. Sert à savoir quelles pages consomment le quota gratuit de KV (100 000 lectures par jour).
export default {
  async fetch(request: Request, env: any, ctx: { waitUntil: (p: Promise<any>) => void }) {
    if (request.headers.get("X-Escale-Diag") !== "1" || !env.ESCALE) return escale.fetch(request, env, ctx)
    const n: Record<string, number> = { get: 0, put: 0, list: 0, delete: 0 }, fond: Promise<any>[] = []
    const cles: Record<string, number> = {}
    const kv = new Proxy(env.ESCALE, { get: (t: any, k: string) => (typeof t[k] === "function" ? (...a: any[]) => { if (k in n) { n[k]++; const c = k + " " + String(a[0]?.prefix ?? a[0]).split(":")[0]; cles[c] = (cles[c] || 0) + 1 } return t[k](...a) } : t[k]) })
    const r = await escale.fetch(request, { ...env, ESCALE: kv }, { waitUntil: (p) => { fond.push(Promise.resolve(p).catch(() => {})); ctx.waitUntil(p) } })
    await Promise.race([Promise.all(fond), new Promise((ok) => setTimeout(ok, 8000))])
    const h = new Headers(r.headers)
    h.set("X-Escale-KV", `get=${n.get} put=${n.put} list=${n.list} delete=${n.delete}` + (Object.keys(cles).length ? " (" + Object.entries(cles).map(([c, v]) => `${c} x${v}`).join(", ").replace(/[^\x20-\x7e]/g, "?").slice(0, 300) + ")" : ""))
    return new Response(r.body, { status: r.status, headers: h })
  },
  scheduled: escale.scheduled,
}
