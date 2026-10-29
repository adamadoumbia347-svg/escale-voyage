// Point d'entrée du Worker Cloudflare d'Escale.
// - /api/* : fonctions serveur (prix, calendrier, bons plans, position, alertes, formulaires, admin, tâches)
// - pages trajets : prix réels écrits dans la page (titre, haut de page, prix par mois), pour les visiteurs et Google
// - /barometre-prix/ : tableau des prix et de leur évolution, écrit dans la page
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
import * as populaires from "./api/populaires"
import * as apercu from "./apercu-prix"
import * as barometre from "./barometre"

const API: Record<string, any> = { prix, explore, calendar, deals, geo, alert, form, admin, cron, populaires }

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
    return apercu.onRequest(c)
  },
  // Chaque matin (voir « triggers » dans wrangler.jsonc) : vérification des alertes prix
  async scheduled(_event: unknown, env: Env, ctx: { waitUntil: (p: Promise<any>) => void }) {
    ctx.waitUntil(cron.checkAlerts(env).then((r) => console.log("alertes", JSON.stringify(r))))
  },
}
