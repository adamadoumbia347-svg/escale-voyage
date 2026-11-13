/* Accueil : ruban de pays. En italien, ce script pose les noms des pays (attribut data-it) : app.js ne connaît que le français
   et l'anglais. Les prix « dès … » qui s'ajoutaient aux pastilles ont été retirés le 13 novembre 2026, à la demande de Dobam :
   chaque pastille montre seulement le pays et mène à sa page. */
(function () {
  "use strict";
  var root = document.documentElement;
  var lg = function () { return (root.lang || "fr").slice(0, 2); };
  var italien = function () { if (lg() === "it") [].forEach.call(document.querySelectorAll("[data-it]"), function (e) { if (e.textContent !== e.dataset.it) e.textContent = e.dataset.it; }); };
  italien();
  if (window.MutationObserver) new MutationObserver(function () { setTimeout(italien, 0); }).observe(root, { attributes: true, attributeFilter: ["lang"] });
})();
