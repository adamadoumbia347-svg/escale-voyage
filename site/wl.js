// Chargement du moteur de recherche en direct (White Label Travelpayouts n° 24006), sur l'accueil et sur /recherche/.
// Ville de départ : le champ « Depuis » est laissé vide dans Travelpayouts (White Label → Contenu), et le moteur
// propose alors lui-même l'aéroport le plus proche du visiteur (vérifié le 29/10/2026). Le paramètre « origin » seul est ignoré.
(function () {
  "use strict";
  // Le moteur lit « locale » dans l'adresse (vérifié le 3/11/2026 : &locale=en l'affiche en anglais ; sans, il reste en français).
  // Langue : celle choisie sur Escale, sinon celle du navigateur (langues activées dans Travelpayouts le 3/11/2026). Monnaie : celle choisie sur Escale (testé : USD, GBP, XOF).
  try {
    var u = new URL(location.href), changed = false;
    var lang = (localStorage.getItem("escale.lang") || (navigator.language || "fr").slice(0, 2)).toLowerCase();
    // Langues vérifiées dans le moteur (3/11/2026) ; les autres en anglais (le chinois « zh », par exemple, retombait en français)
    var OK = { en: 1, es: 1, pt: 1, ar: 1, it: 1, de: 1, nl: 1, ja: 1, tr: 1 };
    if (!u.searchParams.get("locale") && lang !== "fr") { u.searchParams.set("locale", OK[lang] ? lang : "en"); changed = true; }
    var cur = (localStorage.getItem("escale.cur") || "").toUpperCase();
    if (!u.searchParams.get("currency") && /^(USD|GBP|CAD|CHF|XOF|XAF|MAD)$/.test(cur)) { u.searchParams.set("currency", cur.toLowerCase()); changed = true; }
    if (changed) history.replaceState(history.state, "", u.pathname + u.search + u.hash);
  } catch (e) {}
  // Place réservée au formulaire (pages.css, min-height) : libérée dès que le moteur est affiché. Sinon, quand le moteur
  // replie son formulaire en simple loupe après une recherche, un grand espace vide reste au-dessus des résultats.
  (function () {
    var el = document.getElementById("tpwl-search"), n = 0;
    if (!el) return;
    var t = setInterval(function () {
      var r = el.shadowRoot || el;
      if ((r.childElementCount || (r.children && r.children.length)) && el.getBoundingClientRect().height > 0) { el.style.minHeight = "0"; clearInterval(t); }
      else if (++n > 100) clearInterval(t);
    }, 250);
  })();
  var s = document.createElement("script"); s.async = 1; s.type = "module";
  s.src = "https://tpemb.com/wl_web/main.js?wl_id=24006"; document.head.appendChild(s);
})();
