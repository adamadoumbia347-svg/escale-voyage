// Service worker d'Escale : rend le site installable comme une appli et utilisable hors connexion pour les pages déjà vues.
// - pages : réseau d'abord (prix à jour), copie gardée en secours si la connexion coupe ;
// - fichiers du site (CSS, JS, polices, images) : copie locale d'abord, mise à jour en arrière-plan ;
// - jamais de cache pour /api/ ni pour les autres sites (moteur Travelpayouts, partenaires).
const VERSION = "escale-v1"
const PAGES = VERSION + "-pages", FILES = VERSION + "-files"

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(PAGES).then((c) => c.addAll(["/", "/recherche/"])).catch(() => {}).then(() => self.skipWaiting()))
})
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => !k.startsWith(VERSION)).map((k) => caches.delete(k)))).then(() => self.clients.claim()))
})
self.addEventListener("fetch", (e) => {
  const req = e.request, url = new URL(req.url)
  if (req.method !== "GET" || url.origin !== location.origin || url.pathname.startsWith("/api/") || url.pathname.startsWith("/admin")) return
  if (req.mode === "navigate") {
    e.respondWith(fetch(req).then((res) => {
      if (res.ok) { const copy = res.clone(); caches.open(PAGES).then((c) => c.put(req, copy)).catch(() => {}) }
      return res
    }).catch(() => caches.match(req).then((r) => r || caches.match("/"))))
    return
  }
  if (/\.(css|js|woff2|webp|png|svg|ico|json|webmanifest)$/.test(url.pathname)) {
    e.respondWith(caches.open(FILES).then((c) => c.match(req).then((hit) => {
      const net = fetch(req).then((res) => { if (res.ok) c.put(req, res.clone()).catch(() => {}); return res }).catch(() => hit)
      return hit || net
    })))
  }
})
