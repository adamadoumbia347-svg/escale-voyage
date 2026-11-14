// Accueil épuré : six rubriques sous le moteur de recherche. Chaque bouton montre les blocs de sa rubrique (ils restent dans la page,
// simplement repliés) ; un deuxième toucher la referme. Un lien /#faq, /#newsletter, /#calculateur… ouvre la bonne rubrique.
(function () {
  "use strict";
  var nav = document.getElementById("mini-nav");
  if (!nav || !document.documentElement.classList.contains("mini")) return;
  var PAYS = ".hero > .ruban:not(.pop-ruban):not(.nv-hero)";
  // rubrique → blocs à montrer, et onglet du bloc à thèmes (hub.js) à ouvrir
  var G = {
    idees: { s: [".mini-srv", "#hero-deal", "#budget-hook", "#inspi", "#hub", ".saison-bas"], t: "ht-deals" },
    explorer: { s: [PAYS, "#hub", "#nouveautes"], t: "ht-monde" },
    outils: { s: ["#hub"], t: "ht-outils" },
    guides: { s: [".how-mini", "#guides", "#hub"], t: "ht-astuces" },
    bons: { s: ["#newsletter", ".hero > .nv-hero"] },
    questions: { s: ["#faq", ".hero > .hero-meta"] }
  };
  // ancre → rubrique (les blocs à thèmes sont tous dans #hub)
  var H = { outils: "outils", astuces: "guides", checklist: "guides", calculateur: "guides", calc: "guides", world: "explorer", monde: "explorer",
    "sur-place": "explorer", explore: "idees", deals: "idees", fetes: "idees", "home-run": "idees", pays: "idees" };
  var btns = [].slice.call(nav.querySelectorAll("button[data-g]")), cur = null;
  var all = function (f) { Object.keys(G).forEach(function (k) { G[k].s.forEach(function (q) { [].forEach.call(document.querySelectorAll(q), f); }); }); };
  var show = function (g, tab) {
    all(function (e) { e.classList.remove("mini-on"); });
    btns.forEach(function (b) { b.setAttribute("aria-expanded", b.getAttribute("data-g") === g ? "true" : "false"); });
    cur = g;
    if (!g) return;
    G[g].s.forEach(function (q) { [].forEach.call(document.querySelectorAll(q), function (e) { e.classList.add("mini-on"); }); });
    if (tab && G[g].t) { var t = document.getElementById(G[g].t); if (t && !t.hidden) t.click(); }
  };
  btns.forEach(function (b) {
    b.addEventListener("click", function () {
      var g = b.getAttribute("data-g");
      if (cur === g) { show(null); return; }
      show(g, true);
      var y = nav.getBoundingClientRect().top + window.pageYOffset - 70;
      window.scrollTo({ top: Math.max(0, y), behavior: "smooth" });
    });
  });
  var fromHash = function () {
    var h = decodeURIComponent((location.hash || "").slice(1)); if (!h || !/^[\w-]+$/.test(h)) return;
    var g = H[h] || H[h.replace(/^ht-/, "")];
    if (!g) {
      var el = document.getElementById(h); if (!el) return;
      Object.keys(G).some(function (k) { return G[k].s.some(function (q) { var m = el.closest(q); if (m) { g = k; return true; } return false; }); });
      if (!g) return;
      show(g, false);
      setTimeout(function () { el.scrollIntoView({ block: "start" }); }, 60);
      return;
    }
    show(g, false);   // hub.js choisit l'onglet et fait défiler
  };
  fromHash();
  window.addEventListener("hashchange", fromHash);
  // Lien interne vers un bloc replié (même ancre que l'adresse en cours : pas d'événement hashchange)
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"], a[href^="/#"]'); if (!a) return;
    setTimeout(fromHash, 0);
  });
})();
