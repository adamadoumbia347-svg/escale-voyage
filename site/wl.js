// Chargement du moteur de recherche en direct (White Label Travelpayouts n° 24006), sur l'accueil et sur /recherche/.
// Ville de départ : le champ « Depuis » est laissé vide dans Travelpayouts (White Label → Contenu), et le moteur
// propose alors lui-même l'aéroport le plus proche du visiteur (vérifié le 29/10/2026). Le paramètre « origin » seul est ignoré.
(function () {
  "use strict";
  // Langue du moteur = langue choisie sur Escale (ou celle du navigateur) : le moteur lit « locale » dans l'adresse
  // (vérifié le 3/11/2026 : &locale=en affiche le moteur en anglais ; sans ce paramètre il reste en français).
  // Langues activées dans le moteur : fr, en, es, pt, ar, it (vérifié le 3/11/2026) ; allemand et néerlandais → anglais.
  // Monnaie : celle choisie sur Escale (testé : USD, GBP, XOF), sinon celle réglée dans le moteur (EUR).
  try {
    var u = new URL(location.href), ok = { en: 1, es: 1, pt: 1, ar: 1, it: 1, de: "en", nl: "en" }, changed = false;
    var lang = (localStorage.getItem("escale.lang") || (navigator.language || "fr").slice(0, 2)).toLowerCase();
    if (!u.searchParams.get("locale") && ok[lang]) { u.searchParams.set("locale", ok[lang] === 1 ? lang : ok[lang]); changed = true; }
    var cur = (localStorage.getItem("escale.cur") || "").toUpperCase();
    if (!u.searchParams.get("currency") && /^(USD|GBP|CAD|CHF|XOF|XAF|MAD)$/.test(cur)) { u.searchParams.set("currency", cur.toLowerCase()); changed = true; }
    if (changed) history.replaceState(history.state, "", u.pathname + u.search + u.hash);
  } catch (e) {}
  var s = document.createElement("script"); s.async = 1; s.type = "module";
  s.src = "https://tpemb.com/wl_web/main.js?wl_id=24006"; document.head.appendChild(s);
})();
