// Chargement du moteur de recherche en direct (White Label Travelpayouts n° 24006), sur l'accueil et sur /recherche/.
// Ville de départ : le champ « Depuis » est laissé vide dans Travelpayouts (White Label → Contenu), et le moteur
// propose alors lui-même l'aéroport le plus proche du visiteur (vérifié le 29/10/2026). Le paramètre « origin » seul est ignoré.
(function () {
  "use strict";
  // Le moteur lit « locale » dans l'adresse (vérifié le 3/11/2026 : &locale=en l'affiche en anglais ; sans, il reste en français).
  // Langue : celle choisie sur Escale, sinon celle du navigateur (toutes les langues sont activées dans le moteur
  // depuis le 3/11/2026 : japonais, turc, chinois… aussi). Monnaie : celle choisie sur Escale (testé : USD, GBP, XOF).
  try {
    var u = new URL(location.href), changed = false;
    var lang = (localStorage.getItem("escale.lang") || (navigator.language || "fr").slice(0, 2)).toLowerCase();
    if (!u.searchParams.get("locale") && /^[a-z]{2}$/.test(lang) && lang !== "fr") { u.searchParams.set("locale", lang); changed = true; }
    var cur = (localStorage.getItem("escale.cur") || "").toUpperCase();
    if (!u.searchParams.get("currency") && /^(USD|GBP|CAD|CHF|XOF|XAF|MAD)$/.test(cur)) { u.searchParams.set("currency", cur.toLowerCase()); changed = true; }
    if (changed) history.replaceState(history.state, "", u.pathname + u.search + u.hash);
  } catch (e) {}
  var s = document.createElement("script"); s.async = 1; s.type = "module";
  s.src = "https://tpemb.com/wl_web/main.js?wl_id=24006"; document.head.appendChild(s);
})();
