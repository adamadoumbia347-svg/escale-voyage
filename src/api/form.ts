import { Ctx, json, sameKey } from "../_lib/common"
import { unsubToken } from "../digest"
// Formulaires du site (contact, inscription aux bons plans), enregistrés dans l'espace KV ESCALE.
// Les messages se lisent sur /admin/ (clé ADMIN_KEY). Champ piège « site-web » contre les robots.
const FORMS: Record<string, string[]> = { contact: ["nom", "email", "message"], "bons-plans": ["email", "whatsapp", "langue", "consent"] }
const MAX = 3000

export const onRequestGet = (ctx: Ctx) => unsubscribe(ctx)

export const onRequestPost = async (ctx: Ctx) => {
  if (new URL(ctx.request.url).searchParams.get("action") === "desinscription") return unsubscribe(ctx)
  const { request, env } = ctx
  const wantsJson = (request.headers.get("accept") || "").includes("application/json")
  const done = (ok: boolean, form: string) => wantsJson ? json({ ok }, { status: ok ? 200 : 400 })
    : Response.redirect(new URL(ok && form === "contact" ? "/contact/merci/" : "/contact/", request.url).toString(), 303)
  let data: FormData
  try { data = await request.formData() } catch { return done(false, "") }
  const form = String(data.get("form-name") || "")
  if (!FORMS[form]) return done(false, form)
  if (String(data.get("site-web") || "")) return done(true, form) // robot : on fait semblant d'accepter
  const fields: Record<string, string> = {}
  for (const k of FORMS[form]) fields[k] = String(data.get(k) || "").slice(0, MAX)
  if (form === "contact" && (!fields.message.trim() || !/^\S+@\S+\.\S+$/.test(fields.email))) return done(false, form)
  if (form === "bons-plans" && ((!/^\S+@\S+\.\S+$/.test(fields.email) && !/^\+?[0-9 ]{8,20}$/.test(fields.whatsapp)) || !fields.consent)) return done(false, form)
  if (!env.ESCALE) return done(false, form)
  const at = new Date().toISOString()
  await env.ESCALE.put(`form:${form}:${at}:${crypto.randomUUID().slice(0, 8)}`, JSON.stringify({ form, at, fields }))
  return done(true, form)
}

// Désinscription des bons plans (lien en bas de chaque e-mail) : GET /api/form?action=desinscription&id=…&t=… affiche un bouton, POST désinscrit
export const unsubscribe = async ({ request, env }: Ctx) => {
  const q = new URL(request.url).searchParams
  const page = (msg: string) => new Response(`<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">` +
    `<title>Escale</title><body style="font-family:system-ui,sans-serif;max-width:520px;margin:60px auto;padding:0 16px;color:#0d1b2e"><h1 style="font-size:22px">${msg}</h1><p><a href="/">Retour à Escale</a></p></body></html>`,
    { headers: { "content-type": "text/html; charset=utf-8" } })
  if (q.get("action") !== "desinscription" || !env.ESCALE) return page("Lien invalide.")
  const id = q.get("id") || ""
  if (!id.startsWith("form:bons-plans:") || !sameKey(q.get("t") || "", await unsubToken(env, id))) return page("Lien invalide ou expiré.")
  // Confirmation par un bouton : les logiciels qui ouvrent les liens des e-mails pour les vérifier ne désinscrivent personne
  if (request.method !== "POST") return page(`Se désinscrire des bons plans d’Escale ?</h1><form method="post"><button style="font:inherit;font-weight:700;padding:10px 18px;border:0;border-radius:999px;background:#1a56db;color:#fff;cursor:pointer">Oui, me désinscrire</button></form><h1 hidden>`)
  await env.ESCALE.delete(id)
  return page("C’est fait : vous ne recevrez plus les bons plans d’Escale.")
}
