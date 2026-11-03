// Service worker d'Escale : rend le site installable comme une appli et utilisable hors connexion pour les pages déjà vues.
// - pages : réseau d'abord (prix à jour), copie gardée en secours si la connexion coupe ;
// - fichiers du site (CSS, JS, polices, images) : copie locale d'abord, mise à jour en arrière-plan ;
// - jamais de cache pour /api/ ni pour les autres sites (moteur Travelpayouts, partenaires).
const VERSION = "escale-v3"
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

// Alertes prix par notification : le serveur réveille le téléphone sans contenu (src/_lib/webpush.ts),
// on va chercher le message (prix, trajet) puis on l'affiche ; un toucher ouvre la recherche du trajet.
self.addEventListener("push", (e) => {
  e.waitUntil(self.registration.pushManager.getSubscription()
    .then((sub) => fetch("/api/push?action=msg&e=" + encodeURIComponent(sub ? sub.endpoint : "")).then((r) => r.json()))
    .catch(() => ({ title: "Escale", body: "", url: "/" }))
    .then((m) => self.registration.showNotification(m.title || "Escale", { body: m.body || "", icon: "/icon-192.png", badge: "/icon-192.png", data: { url: m.url || "/" }, tag: "escale-prix" })))
})
self.addEventListener("notificationclick", (e) => {
  e.notification.close()
  const url = (e.notification.data && e.notification.data.url) || "/"
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((list) => {
    for (const c of list) if ("focus" in c) { c.navigate(url); return c.focus() }
    return self.clients.openWindow(url)
  }))
})
