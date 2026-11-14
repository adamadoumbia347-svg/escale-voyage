// Accueil : « Vers l'Afrique depuis <ville du visiteur> », une ligne de trajets sous le moteur de recherche, avec les dates et le prix
// aller-retour le plus bas repéré (mois prochain et suivant). Une seule demande : /api/ruban?from=XXX (gardée 12 h par Cloudflare).
// Rien n'est inventé : un pays sans prix repéré n'apparaît pas ; sans aucun prix, le bloc reste caché.
(function () {
  "use strict";
  var sec = document.getElementById("af"), row = document.getElementById("af-row"), city = document.getElementById("af-city");
  if (!sec || !row) return;
  var lang = function () { return (document.documentElement.lang || "fr").slice(0, 2); };
  var LOC = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn" };
  var FROM = { fr: "dès ", en: "from ", it: "da ", de: "ab ", es: "desde ", pt: "desde ", ar: "من " };
  // pays (clé de /api/ruban) → drapeau ; code de ville ou d'aéroport → [aéroport du moteur, nom fr, nom en]
  var PAYS = { ci: "🇨🇮", sn: "🇸🇳", cm: "🇨🇲", gh: "🇬🇭", ma: "🇲🇦", tn: "🇹🇳", eg: "🇪🇬", ke: "🇰🇪", tz: "🇹🇿", za: "🇿🇦", gn: "🇬🇳", bj: "🇧🇯", tg: "🇹🇬", ga: "🇬🇦", ng: "🇳🇬" };
  var V = { ABJ: ["ABJ", "Abidjan"], DSS: ["DSS", "Dakar"], DKR: ["DSS", "Dakar"], DLA: ["DLA", "Douala"], YAO: ["NSI", "Yaoundé"], NSI: ["NSI", "Yaoundé"], ACC: ["ACC", "Accra"],
    RAK: ["RAK", "Marrakech"], CAS: ["CMN", "Casablanca"], CMN: ["CMN", "Casablanca"], TUN: ["TUN", "Tunis"], CAI: ["CAI", "Le Caire", "Cairo"], NBO: ["NBO", "Nairobi"],
    ZNZ: ["ZNZ", "Zanzibar"], DAR: ["DAR", "Dar es Salaam"], CPT: ["CPT", "Le Cap", "Cape Town"], JNB: ["JNB", "Johannesburg"], CKY: ["CKY", "Conakry"], COO: ["COO", "Cotonou"],
    LFW: ["LFW", "Lomé"], LBV: ["LBV", "Libreville"], LOS: ["LOS", "Lagos"], ABV: ["ABV", "Abuja"] };
  var VILLE = { CDG: "PAR", ORY: "PAR", BVA: "PAR", FCO: "ROM", CIA: "ROM", MXP: "MIL", LIN: "MIL", BGY: "MIL", LHR: "LON", LGW: "LON", STN: "LON", LTN: "LON" };
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var money = function (n) { if (window.ESCALE_MONEY) return window.ESCALE_MONEY(n, "EUR"); return Math.round(n) + " €"; };
  var jour = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(LOC[lang()] || "en-GB", { day: "numeric", month: "short" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var cur = null, token = 0, last = null;
  var paint = function (j) {
    var from = cur.code, name = cur.name || from, fr = lang() === "fr";
    var list = Object.keys((j && j.prix) || {}).filter(function (cc) { return PAYS[cc]; }).map(function (cc) {
      var x = j.prix[cc], v = V[x.v] || V[x.to]; if (!v || !x.price || !x.dep) return null;
      return { f: PAYS[cc], to: v[0], n: fr ? v[1] : (v[2] || v[1]), p: x.price, dep: x.dep, ret: x.ret };
    }).filter(Boolean).sort(function (a, b) { return a.p - b.p; }).slice(0, 10);
    if (!list.length) { sec.hidden = true; return; }
    if (city) city.textContent = name;
    row.innerHTML = list.map(function (x) {
      return '<a href="/recherche/?flightSearch=' + from + ddmm(x.dep) + x.to + (x.ret ? ddmm(x.ret) : "") + '1"><b>' + esc(name) + " → " + esc(x.n) + " " + x.f + "</b><small>" +
        esc(jour(x.dep)) + (x.ret ? " → " + esc(jour(x.ret)) : "") + "</small><em>" + esc((FROM[lang()] || "from ") + money(x.p)) + "</em></a>";
    }).join("");
    row.scrollLeft = 0; sec.hidden = false;
  };
  var load = function () {
    var t = ++token, q = VILLE[cur.code] || cur.code;
    fetch("/api/ruban?from=" + q).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (j) {
      if (t !== token) return;
      last = j; paint(j);
    });
  };
  var set = function (d) { if (!d || !d.code) return; if (cur && cur.code === d.code) { if (last) paint(last); return; } cur = { code: d.code, name: d.name }; load(); };
  window.addEventListener("escale:from", function (e) { set(e.detail); });
  window.addEventListener("escale:lang", function () { if (cur && last) paint(last); });
  window.addEventListener("escale:cur", function () { if (cur && last) paint(last); });
  var start = function () {
    if (window.ESCALE_FROM) set(window.ESCALE_FROM);
    // Ville du visiteur inconnue au bout de 3 s : Paris
    setTimeout(function () { if (!cur) set({ code: "CDG", name: "Paris" }); }, 3000);
  };
  if (document.readyState === "complete") start(); else window.addEventListener("load", start);
})();
