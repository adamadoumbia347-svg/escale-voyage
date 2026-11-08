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
import * as clic from "./api/clic"
import * as fx from "./api/fx"
import * as grille from "./api/grille"
import * as weekends from "./api/weekends"
import * as verdictApi from "./api/verdict"
import * as compteur from "./api/compteur"
import * as paye from "./api/paye"
import * as apercu from "./apercu-prix"
import * as barometre from "./barometre"
import * as indice from "./indice"
import * as accueil from "./accueil"
import * as saisir from "./saisir"
import { sendDigest, sendNewsletter } from "./digest"
import { indexNow } from "./indexnow"

const API: Record<string, any> = { push, prix, explore, calendar, deals, geo, alert, form, admin, cron, populaires, clic, fx, grille, weekends, verdict: verdictApi, connus: accueil, compteur, paye }

export default {
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
    if (path === "/barometre-prix/" || path === "/barometre-prix") return barometre.onRequest(c)
    // Indice des prix : page du jour et archives mensuelles (/indice-prix/2026-11/)
    if (/^\/(en\/price-index|indice-prix)(\/(\d{4}-\d{2}\/?)?)?$/.test(path)) return indice.onRequest(c)
    if (path === "/") return accueil.onRequest(c)
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
    ctx.waitUntil(cron.checkAlerts(env).then((r) => console.log("alertes", JSON.stringify(r))))
    // Archive du mois de l'indice des prix (src/indice.ts) : le relevé du jour remplace celui de la veille, puis le mois reste figé
    ctx.waitUntil(indice.archiveIndice(env).then((r) => console.log("indice archive", JSON.stringify(r))).catch((e) => console.log("indice archive erreur", String(e))))
    // IndexNow : pages modifiées depuis 2 jours signalées aux moteurs de recherche (src/indexnow.ts)
    ctx.waitUntil(indexNow(env).then((r) => console.log("IndexNow", JSON.stringify(r))).catch((e) => console.log("IndexNow erreur", String(e))))
    // Lundi et jeudi : e-mail avec le message WhatsApp des bons plans, prêt à coller dans la chaîne (src/digest.ts)
    const day = new Date().getUTCDay()
    if (day === 1 || day === 4) ctx.waitUntil(sendDigest(env).then((r) => console.log("message WhatsApp", JSON.stringify(r))))
    // Le lundi seulement : e-mail des bons plans aux inscrits (une fois par semaine au plus)
    if (day === 1) ctx.waitUntil(sendNewsletter(env).then((r) => console.log("bons plans par e-mail", JSON.stringify(r))))
  },
}
