import { Ctx, json, sameKey } from "../_lib/common"
import { sendDigest } from "../digest"
// Lecture des messages et inscriptions pour la page /admin/ (en-tête « x-admin-key: <ADMIN_KEY> »).
//  GET    /api/admin?form=contact|bons-plans   -> liste (les plus récents d'abord)
//  DELETE /api/admin?key=form:…                -> supprime une entrée (désinscription, message traité)
//  POST   /api/admin?action=digest             -> envoie tout de suite l'e-mail « message WhatsApp de la semaine »
export const onRequest = async ({ request, env }: Ctx) => {
  if (!sameKey(request.headers.get("x-admin-key") || "", env.ADMIN_KEY || "")) return json({ error: "unauthorized" }, { status: 401 })
  if (!env.ESCALE) return json({ error: "no-storage" }, { status: 503 })
  const url = new URL(request.url)
  if (request.method === "POST" && url.searchParams.get("action") === "digest") return json(await sendDigest(env))
  if (request.method === "DELETE") {
    const key = url.searchParams.get("key") || ""
    if (!key.startsWith("form:")) return json({ error: "invalid" }, { status: 400 })
    await env.ESCALE.delete(key)
    return json({ ok: true })
  }
  const form = url.searchParams.get("form") === "contact" ? "contact" : "bons-plans"
  const items: any[] = []
  let cursor: string | undefined
  do {
    const page: any = await env.ESCALE.list({ prefix: `form:${form}:`, cursor, limit: 1000 })
    for (const k of page.keys) {
      const v = await env.ESCALE.get(k.name, "json")
      if (v) items.push({ key: k.name, ...v })
    }
    cursor = page.list_complete ? undefined : page.cursor
  } while (cursor && items.length < 2000)
  items.sort((a, b) => (a.at < b.at ? 1 : -1))
  return json({ form, items }, { headers: { "Cache-Control": "no-store" } })
}
