import { Ctx, json, sameKey, esc } from "../_lib/common"
import { mailerReady, sendMail, lastMailError } from "../_lib/mail"
import { sendDigest } from "../digest"
// Lecture des messages et inscriptions pour la page /admin/ (en-tête « x-admin-key: <ADMIN_KEY> »).
//  GET    /api/admin?form=contact|bons-plans   -> liste (les plus récents d'abord)
//  DELETE /api/admin?key=form:…                -> supprime une entrée (désinscription, message traité)
//  GET    /api/admin?action=clics              -> clics des 30 derniers jours (compteur anonyme, site/clics.js)
//  POST   /api/admin?action=digest             -> envoie tout de suite l'e-mail « message WhatsApp de la semaine »
//  POST   /api/admin?action=video              -> envoie à DIGEST_TO la vidéo TikTok du jour (fabriquée par .github/workflows/video-du-jour.yml)
export const onRequest = async ({ request, env }: Ctx) => {
  if (!sameKey(request.headers.get("x-admin-key") || "", env.ADMIN_KEY || "")) return json({ error: "unauthorized" }, { status: 401 })
  if (!env.ESCALE) return json({ error: "no-storage" }, { status: 503 })
  const url = new URL(request.url)
  if (request.method === "POST" && url.searchParams.get("action") === "digest") return json(await sendDigest(env))
  if (request.method === "POST" && url.searchParams.get("action") === "video") {
    // Corps : { title, caption, filename, video (mp4 en base64) }. Destinataire fixe : DIGEST_TO.
    const to = ((env as any).DIGEST_TO || "").trim()
    if (!to || !mailerReady(env)) return json({ sent: false, reason: "DIGEST_TO ou envoi d'e-mails non configuré" }, { status: 503 })
    const b: any = await request.json().catch(() => null)
    if (!b || typeof b.video !== "string" || b.video.length > 20e6 || !/^[\w.-]+\.mp4$/.test(b.filename || "")) return json({ error: "invalid" }, { status: 400 })
    const title = String(b.title || "Vidéo du jour").slice(0, 120), caption = String(b.caption || "").slice(0, 2200)
    const html = `<div style="font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:640px;color:#0d1b2e">` +
      `<h2 style="margin:0 0 8px">🎬 ${esc(title)}</h2><p>La vidéo est en pièce jointe. Enregistre-la sur ton téléphone, puis TikTok › + › Importer, ajoute un son tendance et colle la légende :</p>` +
      `<pre style="white-space:pre-wrap;font:15px/1.5 system-ui,sans-serif;background:#f3f6fa;border:1px solid #dde3ec;border-radius:10px;padding:14px">${esc(caption)}</pre>` +
      `<p style="color:#5b6b80;font-size:13px">Vidéo fabriquée automatiquement chaque jour avec les prix du baromètre d'Escale. Meilleure heure pour publier : 19 h – 21 h.</p></div>`
    const ok = await sendMail(env, to, `🎬 Vidéo TikTok du jour : ${title}`, html, [{ filename: b.filename, content: b.video }])
    return json({ sent: ok, ...(ok ? {} : { detail: lastMailError }) })
  }
  if (url.searchParams.get("action") === "clics") {
    // Clics des 30 derniers jours : total par lien, sur 7 et 30 jours, et détail par type de page
    const days = Array.from({ length: 30 }, (_, i) => new Date(Date.now() - i * 864e5).toISOString().slice(0, 10))
    const rows = await Promise.all(days.map((d) => env.ESCALE.get("clics:" + d, "json")))
    const out: Record<string, { j7: number; j30: number; pages: Record<string, number> }> = {}
    rows.forEach((r: any, i) => { for (const [id, n] of Object.entries(r || {})) {
      const [k, p] = id.split("|"); const o = out[k] || (out[k] = { j7: 0, j30: 0, pages: {} })
      o.j30 += n as number; if (i < 7) o.j7 += n as number; o.pages[p] = (o.pages[p] || 0) + (n as number) } })
    return json({ depuis: days[29], clics: out }, { headers: { "Cache-Control": "no-store" } })
  }
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
