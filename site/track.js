// Mesure d'audience anonyme d'Escale : page vue, langue, site d'origine et clics vers les sites partenaires.
// Aucun cookie, aucun identifiant, aucune donnée personnelle. Désactivée si le navigateur demande « Do Not Track ».
(function () {
  "use strict";
  if (navigator.webdriver || navigator.doNotTrack === "1" || !/^https?:$/.test(location.protocol) || location.pathname.indexOf("/stats/") === 0) return;
  var send = function (data) {
    data.l = (document.documentElement.lang || "").slice(0, 2);
    var body = JSON.stringify(data);
    try {
      if (navigator.sendBeacon && navigator.sendBeacon("/api/hit", new Blob([body], { type: "application/json" }))) return;
    } catch (e) {}
    try { fetch("/api/hit", { method: "POST", body: body, keepalive: true }); } catch (e) {}
  };
  var ref = "";
  try { var r = document.referrer ? new URL(document.referrer).hostname : ""; ref = r && r !== location.hostname ? r.replace(/^www\./, "") : ""; } catch (e) {}
  send({ k: "view", p: location.pathname, r: ref });
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a[href^='http']");
    if (!a) return;
    try { var h = new URL(a.href).hostname; if (h !== location.hostname) send({ k: "click", p: location.pathname, t: h.replace(/^www\./, "") }); } catch (e) {}
  }, true);
})();
