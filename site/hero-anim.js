// Accueil : les avantages défilent un par un sous le titre, et la fin du titre tape des destinations
// (« pour toutes les destinations » → « pour Abidjan » → « pour Bangkok »…). Rien ne bouge si le visiteur a demandé moins
// d'animations ou en mode léger ; le texte d'origine reste dans la page pour Google et les lecteurs d'écran.
(function () {
  "use strict";
  var root = document.documentElement;
  if (root.classList.contains("lite") || (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches)) return;

  // 1. Avantages : un à la fois, qui montent
  var ul = document.querySelector(".hero .perks");
  if (ul && ul.children.length > 1) {
    var items = Array.prototype.slice.call(ul.children), i = 0;
    ul.classList.add("ticker"); items[0].classList.add("on");
    setInterval(function () {
      var cur = items[i]; i = (i + 1) % items.length; var nxt = items[i];
      cur.classList.remove("on"); cur.classList.add("out");
      nxt.classList.remove("out"); void nxt.offsetWidth; nxt.classList.add("on");
      setTimeout(function () { cur.classList.remove("out"); }, 600);
    }, 2800);
  }

  // 2. Titre : effet machine à écrire sur la fin (français et anglais)
  var em = document.querySelector(".hero h1 em"), h1 = em && em.parentNode;
  var lang = (root.lang || "fr").slice(0, 2);
  var W = { fr: ["pour Abidjan", "pour Dakar", "pour Bangkok", "pour New York", "pour Marrakech", "pour Tokyo", "pour Zanzibar"],
    en: ["to Abidjan", "to Lagos", "to Bangkok", "to New York", "to Marrakech", "to Tokyo", "to Zanzibar"] }[lang];
  if (!em || !W) return;
  var first = em.textContent, words = [first].concat(W), k = 0;
  h1.setAttribute("aria-label", h1.textContent);
  Array.prototype.forEach.call(h1.childNodes, function (n) { if (n.nodeType === 1) n.setAttribute("aria-hidden", "true"); });
  h1.style.minHeight = h1.offsetHeight + "px"; h1.style.textWrap = "wrap"; // le titre garde sa hauteur et sa coupure : la page ne saute pas
  em.classList.add("typing");
  var type = function (txt, done) { var n = 0; (function step() { em.textContent = txt.slice(0, ++n); n < txt.length ? setTimeout(step, 55) : done(); })(); };
  var erase = function (done) { (function step() { var t = em.textContent; if (!t) return done(); em.textContent = t.slice(0, -1); setTimeout(step, 28); })(); };
  var loop = function () {
    setTimeout(function () {
      erase(function () { k = (k + 1) % words.length; type(words[k], loop); });
    }, k === 0 ? 3200 : 1700);
  };
  loop();
})();
