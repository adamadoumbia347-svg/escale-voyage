// Chargement du moteur de recherche en direct (White Label Travelpayouts n° 24006), sur l'accueil et sur /recherche/.
// Ville de départ : le champ « Depuis » est laissé vide dans Travelpayouts (White Label → Contenu), et le moteur
// propose alors lui-même l'aéroport le plus proche du visiteur (vérifié le 29/10/2026). Le paramètre « origin » seul est ignoré.
(function () {
  "use strict";
  var s = document.createElement("script"); s.async = 1; s.type = "module";
  s.src = "https://tpemb.com/wl_web/main.js?wl_id=24006"; document.head.appendChild(s);
})();
