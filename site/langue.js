// Langue automatique sur toutes les pages : si la page existe dans la langue du navigateur (liens hreflang), on y va tout seul.
// - le choix fait à la main (sélecteur de langue, liens FR · EN · ES…) est gardé dans « escale.lang » et toujours respecté ;
// - pas de page dans la langue du visiteur : version anglaise, sauf s'il lit le français ;
// - jamais pour les robots des moteurs de recherche ni les aperçus de liens (chaque page reste indexée dans sa langue).
(function () {
  "use strict";
  try {
    var d = document, html = d.documentElement;
    var here = (html.getAttribute("lang") || "fr").slice(0, 2).toLowerCase();
    var get = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } };
    var set = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
    var alt = {};
    [].forEach.call(d.querySelectorAll('link[rel="alternate"][hreflang]'), function (l) {
      var h = l.getAttribute("hreflang").slice(0, 2).toLowerCase();
      if (h !== "x-" && !alt[h]) alt[h] = l.getAttribute("href");
    });
    // Choix à la main : un lien vers une autre langue de la page, ou ?lang=xx
    var norm = function (u) { try { var x = new URL(u, location.href); return x.pathname.replace(/\/index\.html$/, "/"); } catch (e) { return ""; } };
    var byPath = {}; Object.keys(alt).forEach(function (k) { byPath[norm(alt[k])] = k; });
    d.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[href]"); if (!a) return;
      var k = a.getAttribute("hreflang") || byPath[norm(a.getAttribute("href"))];
      if (k && norm(a.getAttribute("href")) !== norm(location.href)) set("escale.lang", k.slice(0, 2));
    }, true);
    var qp = new URLSearchParams(location.search).get("lang");
    if (qp) { set("escale.lang", qp.slice(0, 2)); return; }

    var ua = navigator.userAgent || "";
    if (/bot|crawl|spider|slurp|google|bing|yandex|baidu|duckduck|facebookexternalhit|whatsapp|telegram|twitter|linkedin|preview|lighthouse|pagespeed|headless/i.test(ua)) return;
    if (!Object.keys(alt).length) return;

    // Langue voulue : choix enregistré, sinon langues du navigateur dans l'ordre
    var chosen = get("escale.lang");
    var nav = (navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ""])
      .map(function (l) { return String(l).slice(0, 2).toLowerCase(); });
    var want = null;
    if (chosen) want = alt[chosen] ? chosen : (chosen !== "fr" && here !== "en" && alt.en ? "en" : null);
    else {
      for (var i = 0; i < nav.length; i++) { if (nav[i] === here) return; if (alt[nav[i]]) { want = nav[i]; break; } }
      if (!want && nav.indexOf("fr") < 0 && here !== "en" && alt.en) want = "en";
    }
    if (!want || want === here) return;
    var target = norm(alt[want]);  // même site (adresse relative)
    if (norm(target) === norm(location.href)) return;
    // Une seule redirection par page et par visite (évite toute boucle)
    var key = "escale.lr." + location.pathname;
    try { if (sessionStorage.getItem(key)) return; sessionStorage.setItem(key, "1"); } catch (e) { return; }
    location.replace(target + location.search.replace(/([?&])lang=[^&]*/g, "$1") + location.hash);
  } catch (e) {}
})();
