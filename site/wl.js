// Chargement du moteur de recherche en direct (White Label Travelpayouts n° 24006), sur l'accueil et sur /recherche/.
// Sans trajet dans l'adresse, l'aéroport de départ est prérempli avec le grand aéroport le plus proche du visiteur
// (position approximative donnée par Cloudflare via /api/geo, rien n'est enregistré). Au plus 1,5 s d'attente.
(function () {
  "use strict";
  var load = function () {
    var s = document.createElement("script"); s.async = 1; s.type = "module";
    s.src = "https://tpemb.com/wl_web/main.js?wl_id=24006"; document.head.appendChild(s);
  };
  var q = new URLSearchParams(location.search);
  if (q.has("flightSearch") || q.has("origin") || q.has("origin_iata")) { load(); return; }
  var done = false, finish = function (code) {
    if (done) return; done = true;
    if (code) { try { q.set("origin", code); history.replaceState(history.state, "", location.pathname + "?" + q.toString() + location.hash); } catch (e) {} }
    load();
  };
  setTimeout(function () { finish(null); }, 1500);
  var cached = null;
  try { cached = sessionStorage.getItem("escale.near"); } catch (e) {}
  if (cached) { finish(cached === "-" ? null : cached); return; }
  Promise.all([
    fetch("/api/geo").then(function (r) { return r.ok ? r.json() : null; }),
    fetch("/data/airports.json").then(function (r) { return r.ok ? r.json() : null; })
  ]).then(function (res) {
    var g = res[0], db = res[1], best = null, bestD = 400; // au-delà de 400 km, on ne propose rien
    if (g && g.lat != null && g.lon != null && db) {
      var rad = Math.PI / 180;
      db.forEach(function (a) {
        if (!a[4] || a[5] == null) return; // grands aéroports seulement
        var dLat = (a[5] - g.lat) * rad, dLon = (a[6] - g.lon) * rad;
        var h = Math.pow(Math.sin(dLat / 2), 2) + Math.cos(g.lat * rad) * Math.cos(a[5] * rad) * Math.pow(Math.sin(dLon / 2), 2);
        var d = 12742 * Math.asin(Math.sqrt(h));
        if (d < bestD) { bestD = d; best = a[0]; }
      });
    }
    try { sessionStorage.setItem("escale.near", best || "-"); } catch (e) {}
    finish(best);
  }).catch(function () { finish(null); });
})();
