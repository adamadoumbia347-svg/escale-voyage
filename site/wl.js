// Chargement du moteur de recherche en direct (White Label Travelpayouts n° 24006), sur l'accueil et sur /recherche/.
// Le moteur n'accepte pas qu'on lui donne seulement l'aéroport de départ (paramètre « origin » ignoré, testé le 29/10/2026) :
// la ville de départ par défaut se règle dans Travelpayouts (White Label → Contenu → « Depuis »).
(function () {
  "use strict";
  var s = document.createElement("script"); s.async = 1; s.type = "module";
  s.src = "https://tpemb.com/wl_web/main.js?wl_id=24006"; document.head.appendChild(s);
})();
