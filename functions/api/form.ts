import { Ctx, json } from "../_lib/common"
// Formulaires du site (contact, inscription aux bons plans), enregistrés dans l'espace KV ESCALE.
// Les messages se lisent sur /admin/ (clé ADMIN_KEY). Champ piège « site-web » contre les robots.
const FORMS: Record<string, string[]> = { contact: ["nom", "email", "message"], "bons-plans": ["email", "whatsapp", "langue", "consent"] }
const MAX = 3000

export const onRequestPost = async ({ request, env }: Ctx) => {
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
