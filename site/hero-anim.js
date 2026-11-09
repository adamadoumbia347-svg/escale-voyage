// Accueil : les avantages défilent un par un sous le titre, et la fin du titre fait défiler des destinations
// (« pour rentrer au pays » → « pour Abidjan 🇨🇮 » → « pour Dakar 🇸🇳 »…) : les villes d'Afrique d'abord, puis le reste du monde.
// Chaque destination monte et remplace la précédente dans une pastille (plus de machine à écrire). Rien ne bouge si le visiteur
// a demandé moins d'animations ou en mode léger ; le texte d'origine reste dans la page pour Google et les lecteurs d'écran.
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

  // 2. Titre : les destinations défilent dans une pastille (français et anglais), Afrique d'abord
  var em = document.querySelector(".hero h1 em"), h1 = em && em.parentNode;
  var lang = (root.lang || "fr").slice(0, 2);
  var AFR = [["Abidjan", "🇨🇮"], ["Dakar", "🇸🇳"], ["Bamako", "🇲🇱"], ["Douala", "🇨🇲"], ["Kinshasa", "🇨🇩"], ["Conakry", "🇬🇳"], ["Lomé", "🇹🇬"], ["Cotonou", "🇧🇯"],
    ["Casablanca", "🇲🇦"], [lang === "en" ? "Algiers" : "Alger", "🇩🇿"], ["Tunis", "🇹🇳"], ["Lagos", "🇳🇬"], ["Accra", "🇬🇭"], ["Nairobi", "🇰🇪"]];
  var MONDE = [["Istanbul", "🇹🇷"], [lang === "en" ? "Dubai" : "Dubaï", "🇦🇪"], ["New York", "🇺🇸"], ["Bangkok", "🇹🇭"], ["Tokyo", "🇯🇵"]];
  // Selon le pays du visiteur (donné par le serveur, sans cookie), les villes des communautés les plus présentes passent en premier
  var PRIO = { IT: ["🇲🇦", "🇸🇳", "🇨🇮", "🇳🇬", "🇹🇳", "🇬🇭"], BE: ["🇨🇩", "🇲🇦", "🇨🇲", "🇬🇳", "🇸🇳"], GB: ["🇳🇬", "🇬🇭", "🇰🇪"], DE: ["🇬🇭", "🇳🇬", "🇲🇦", "🇹🇳", "🇨🇲"],
    NL: ["🇲🇦", "🇬🇭", "🇳🇬"], ES: ["🇲🇦", "🇸🇳", "🇩🇿"], CH: ["🇨🇲", "🇨🇩", "🇹🇳"], US: ["🇳🇬", "🇬🇭", "🇰🇪"], CA: ["🇲🇦", "🇩🇿", "🇨🇲", "🇨🇮"] }[window.ESCALE_PAYS || ""];
  if (PRIO) AFR.sort(function (a, b) { var x = PRIO.indexOf(a[1]), y = PRIO.indexOf(b[1]); return (x < 0 ? 99 : x) - (y < 0 ? 99 : y); });
  if (!em || (lang !== "fr" && lang !== "en")) return;
  setTimeout(function () {
    var full = em.textContent.trim(), cut = full.indexOf(" ");
    if (cut < 1) return;
    var lead = full.slice(0, cut), first = full.slice(cut + 1);
    // Windows n'affiche pas les drapeaux (il montre deux lettres) : on les retire sur ces ordinateurs
    var flags = !/Windows/.test(navigator.userAgent || "");
    var words = [first].concat(AFR.concat(MONDE).map(function (w) { return flags ? w[0] + " " + w[1] : w[0]; })), k = 0;
    h1.setAttribute("aria-label", h1.textContent);
    Array.prototype.forEach.call(h1.childNodes, function (n) { if (n.nodeType === 1) n.setAttribute("aria-hidden", "true"); });
    h1.style.minHeight = h1.offsetHeight + "px"; h1.style.textWrap = "wrap"; // le titre garde sa hauteur et sa coupure : la page ne saute pas
    var st = document.createElement("style");
    st.textContent = ".hero h1 em.roll{white-space:nowrap}.hero h1 em.roll .rl{display:inline-grid;vertical-align:bottom;overflow:hidden;margin-inline-start:.22em;padding:.07em .28em;margin-block:-.07em;border-radius:.3em;background:rgb(127 243 222/.2);box-shadow:inset 0 0 0 1px rgb(127 243 222/.45)}" +
      ".hero h1 em.roll .rl>span{grid-area:1/1;justify-self:start;color:#fff;transition:transform .55s cubic-bezier(.2,.8,.2,1),opacity .4s ease,filter .4s ease}.hero h1 em.roll .rl>span.in{transform:translateY(105%);opacity:0;filter:blur(4px)}.hero h1 em.roll .rl>span.out{transform:translateY(-105%);opacity:0;filter:blur(4px)}" +
      "html:not(.has-hero) .hero h1 em.roll .rl{background:rgb(11 133 119/.1);box-shadow:inset 0 0 0 1px rgb(11 133 119/.25)}html:not(.has-hero) .hero h1 em.roll .rl>span{color:inherit}";
    document.head.appendChild(st);
    em.textContent = lead;
    var rl = document.createElement("span"); rl.className = "rl";
    var cur = document.createElement("span"); cur.textContent = first; rl.appendChild(cur); em.appendChild(rl); em.classList.add("roll");
    var next = function () {
      k = (k + 1) % words.length;
      var nw = document.createElement("span"); nw.className = "in"; nw.textContent = words[k]; rl.appendChild(nw);
      void nw.offsetWidth; nw.className = ""; cur.className = "out";
      var old = cur; cur = nw;
      setTimeout(function () { if (old.parentNode) old.parentNode.removeChild(old); }, 600);
      setTimeout(next, k === 0 ? 3600 : 2100);
    };
    setTimeout(next, 600);
  }, 3000);
})();
