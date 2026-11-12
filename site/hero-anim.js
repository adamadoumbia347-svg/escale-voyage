// Accueil : les avantages défilent un par un sous le titre, le titre, lui, ne change plus.
// Sous le titre, un ruban de pays défile (CSS). // a demandé moins d'animations ou en mode léger ; le texte d'origine reste dans la page pour Google et les lecteurs d'écran.
// Ce fichier est aussi écrit dans la page par le serveur (src/accueil-anim.ts) : garder les deux identiques.
(function () {
  "use strict";
  var root = document.documentElement;
  // La liste des avantages est déjà en mode « un à la fois » dans la page (rien ne bouge au chargement) ;
  // sans animation (mode léger, moins d'animations demandé), on réaffiche la liste complète.
  var ul = document.querySelector(".hero .perks");
  if (root.classList.contains("lite") || (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches)) {
    if (ul) ul.classList.remove("ticker");
    return;
  }

  // 1. Avantages : un à la fois, qui montent
  // Les animations démarrent quelques secondes après l'ouverture : la page s'affiche d'abord, stable (plus rapide et plus lisible)
  if (ul && ul.children.length > 1) {
    var items = Array.prototype.slice.call(ul.children), i = 0;
    setTimeout(function () { setInterval(function () {
      var cur = items[i]; i = (i + 1) % items.length; var nxt = items[i];
      cur.classList.remove("on"); cur.classList.add("out");
      nxt.classList.remove("out"); void nxt.offsetWidth; nxt.classList.add("on");
      setTimeout(function () { cur.classList.remove("out"); }, 600);
    }, 2800); }, 4000);
  }

  // 2. Le titre reste fixe : sous lui, un ruban de pays défile (écrit dans la page par scripts/build_pages.py, animé en CSS).
})();
