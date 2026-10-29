// Sur toutes les pages : bulle « Bons plans sur WhatsApp » (en bas à droite) et compteur de clics anonyme.
// Le compteur n'utilise aucun cookie et n'enregistre ni adresse IP ni identifiant : seulement « tel lien, tel jour, tel type de page »,
// pour savoir ce qui sert vraiment (Aviasales, moteur en direct, hôtels, WhatsApp…). Résultats dans /admin/.
(function () {
  "use strict";
  var path = location.pathname;
  if (/^\/(admin|outils)\//.test(path)) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var CHANNEL = "https://whatsapp.com/channel/0029VbE28kB0LKZN7ypnGj0d";
  var L = { fr: "Bons plans sur WhatsApp", en: "Deals on WhatsApp", es: "Ofertas en WhatsApp", pt: "Promoções no WhatsApp", ar: "العروض على واتساب", it: "Offerte su WhatsApp" }[lang] || "Bons plans sur WhatsApp";

  // Bulle WhatsApp (masquable pour la visite)
  var closed = false; try { closed = sessionStorage.getItem("escale.wa") === "0"; } catch (e) {}
  if (!closed) {
    var w = document.createElement("div");
    w.className = "wa-float";
    w.innerHTML = '<a href="' + CHANNEL + '" target="_blank" rel="noopener" data-k="whatsapp-bulle"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8 0-1.3.7-2 1-2.3.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.7-.1l.9-1.1c.2-.3.4-.2.7-.1l1.9.9c.3.1.5.2.5.3.1.2.1.6-.1 1.2z"/></svg><span>' + L + '</span></a>' +
      '<button type="button" aria-label="×">×</button>';
    w.querySelector("button").addEventListener("click", function () { w.remove(); try { sessionStorage.setItem("escale.wa", "0"); } catch (e) {} });
    var add = function () { document.body.appendChild(w); };
    if (document.body) add(); else document.addEventListener("DOMContentLoaded", add);
  }

  // Compteur de clics
  var page = path === "/" ? "accueil" : /^\/recherche\//.test(path) ? "recherche" : /^\/vols-ete-/.test(path) ? "ete"
    : /^\/(vol-|(en|es|pt|ar)\/(flights|vuelos|voos)-|it\/voli-)/.test(path) ? "trajet" : /^\/vols-pour-|\/(flights|vuelos|voos)-(to|a|para)-/.test(path) ? "destination" : "autre";
  var kind = function (a) {
    if (a.dataset && a.dataset.k) return a.dataset.k;
    if (a.classList.contains("pop-chip")) return "trajet-populaire";
    if (a.classList.contains("season")) return "bandeau-saison";
    var h; try { h = new URL(a.href, location.href); } catch (e) { return null; }
    if (h.host === location.host) return /^\/recherche\//.test(h.pathname) ? "moteur-lien" : null;
    var host = h.host.replace(/^www\./, "");
    if (/aviasales\./.test(host)) return "aviasales";
    if (/stay22\./.test(host)) return "stay22";
    if (/\.tpm\.lv$/.test(host)) return host.split(".")[0];
    if (/whatsapp\.com$/.test(host)) return "whatsapp";
    if (/^wa\.me$/.test(host)) return "partage-whatsapp";
    var m = host.match(/(skyscanner|kayak|momondo|booking|google|airbnb|agoda|safetywing)/);
    return m ? m[1] : "autre-site";
  };
  var send = function (k) {
    var body = JSON.stringify({ k: k, p: page });
    try { if (navigator.sendBeacon && navigator.sendBeacon("/api/clic", body)) return; } catch (e) {}
    try { fetch("/api/clic", { method: "POST", body: body, keepalive: true }); } catch (e) {}
  };
  document.addEventListener("click", function (ev) {
    var t = ev.target;
    if (t && t.closest && t.closest("#tpwl-tickets")) { send("moteur-resultat"); return; }
    var a = t && t.closest && t.closest("a[href]");
    if (!a) return;
    var k = kind(a);
    if (k) send(k);
  }, true);
})();
