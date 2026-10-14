// Après chaque mise en ligne réussie (événement Netlify « deploy-succeeded ») :
// envoie toutes les adresses du sitemap à IndexNow (Bing, Yandex, Seznam…) pour qu'elles soient explorées vite.
const KEY = "58b4cc1ae82fde85a120e07836308d90" // publique : doit correspondre au fichier site/<KEY>.txt

export default async () => {
  if (Netlify.env.get("CONTEXT") && Netlify.env.get("CONTEXT") !== "production") return new Response("skip")
  const base = (Netlify.env.get("URL") || "https://escale-voyage.netlify.app").replace(/\/$/, "")
  try {
    const xml = await (await fetch(`${base}/sitemap.xml`)).text()
    const urlList = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]).slice(0, 10000)
    const r = await fetch("https://api.indexnow.org/indexnow", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({ host: new URL(base).host, key: KEY, keyLocation: `${base}/${KEY}.txt`, urlList }),
    })
    console.log("IndexNow", r.status, urlList.length)
  } catch (e) {
    console.log("IndexNow erreur", String(e))
  }
  return new Response("ok")
}
