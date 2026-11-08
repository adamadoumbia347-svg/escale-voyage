// IndexNow (Bing, Yandex, Seznam…) : chaque matin, signale les pages modifiées depuis 2 jours (date « lastmod » du plan du site).
// Remplace l'envoi qui se faisait depuis GitHub à chaque mise en ligne. La clé publique est le fichier site/58b4cc1ae82fde85a120e07836308d90.txt.
const KEY = "58b4cc1ae82fde85a120e07836308d90"

export async function indexNow(env: any, now = Date.now()) {
  const r = env.ASSETS ? await env.ASSETS.fetch(new Request("https://escale.live/sitemap.xml")) : null
  if (!r || !r.ok) return { erreur: r ? r.status : "assets" }
  const xml = await r.text(), since = now - 2 * 864e5, urls: string[] = []
  for (const m of xml.matchAll(/<loc>([^<]+)<\/loc>\s*<lastmod>([^<]+)<\/lastmod>/g)) if (Date.parse(m[2]) >= since) urls.push(m[1])
  if (!urls.length) return { envoyees: 0 }
  const res = await fetch("https://api.indexnow.org/indexnow", {
    method: "POST", headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({ host: "escale.live", key: KEY, keyLocation: `https://escale.live/${KEY}.txt`, urlList: urls.slice(0, 10000) }),
  })
  return { envoyees: Math.min(urls.length, 10000), statut: res.status }
}
