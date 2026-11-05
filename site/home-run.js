// Accueil : « Rentrer au pays » (meilleur aller-retour du mois prochain vers les grandes villes d'Afrique, depuis la ville
// du visiteur : événement escale:from d'app.js, Paris par défaut), bouton « Options » sur téléphone, les thèmes sont gérés par hub.js.
(function () {
  "use strict";
  // Bouton « Options » : montre la classe de voyage sur téléphone
  var ob = document.getElementById("opt-btn"), gf = document.getElementById("form-vols");
  if (ob && gf) ob.addEventListener("click", function () { var on = gf.classList.toggle("opts"); ob.setAttribute("aria-expanded", on ? "true" : "false"); });

  // « Voir les 24 destinations » (sur téléphone, seules les 8 premières sont affichées)
  var wm = document.getElementById("world-more");
  if (wm) wm.addEventListener("click", function () { var w = document.getElementById("world"); if (w) w.classList.add("all"); });

  // Rentrer au pays
  var d = new Date();
  var sec = document.getElementById("home-run"), row = document.getElementById("hr-row");
  if (!sec || !row) return;
  var lang = function () { return (document.documentElement.lang || "fr").slice(0, 2); };
  var D = [["ABJ", "🇨🇮", "Abidjan"], ["DSS", "🇸🇳", "Dakar"], ["DLA", "🇨🇲", "Douala"], ["BKO", "🇲🇱", "Bamako"], ["CMN", "🇲🇦", "Casablanca"],
    ["ALG", "🇩🇿", "Alger", "Algiers"], ["TUN", "🇹🇳", "Tunis"], ["FIH", "🇨🇩", "Kinshasa"], ["OUA", "🇧🇫", "Ouagadougou"], ["LFW", "🇹🇬", "Lomé"],
    ["COO", "🇧🇯", "Cotonou"], ["CKY", "🇬🇳", "Conakry"], ["LOS", "🇳🇬", "Lagos"], ["ACC", "🇬🇭", "Accra"]];
  var money = function (n, cur) { if (window.ESCALE_MONEY) return window.ESCALE_MONEY(n, cur || "EUR"); return Math.round(n) + " €"; };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var month = (function () { var x = new Date(d.getFullYear(), d.getMonth() + 1, 1); return x.getFullYear() + "-" + ("0" + (x.getMonth() + 1)).slice(-2); })();
  var cur = { code: "PAR", name: "Paris" }, seen = false, token = 0;
  var render = function () {
    var t = ++token, from = cur.code === "CDG" || cur.code === "ORY" ? "PAR" : cur.code;
    var c = sec.querySelector(".hr-city"); if (c) c.textContent = cur.name || from;
    var list = D.filter(function (x) { return x[0] !== from; });
    row.innerHTML = list.map(function (x) {
      var name = lang() === "fr" ? x[2] : (x[3] || x[2]);
      return '<a class="hr-chip" data-to="' + x[0] + '" href="/?type=vols&amp;from=' + from + "&amp;to=" + x[0] + '"><b>' + x[1] + " " + name + '</b><span class="pr"></span><small></small></a>';
    }).join("");
    row.querySelectorAll(".hr-chip").forEach(function (a) {
      var to = a.getAttribute("data-to");
      fetch("/api/calendar?from=" + from + "&to=" + to + "&month=" + month).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (r) {
        if (t !== token) return;
        var b = null;
        if (r && r.available && r.days) Object.keys(r.days).forEach(function (k) { var x = r.days[k]; if (x && x.price && (!b || x.price < b.price)) b = { p: x.price, dep: k, ret: x.ret, c: r.currency }; });
        if (!b) { a.remove(); if (!row.children.length) sec.hidden = true; return; }
        a.querySelector(".pr").textContent = (lang() === "fr" ? "dès " : "from ") + money(b.p, b.c);
        try { a.querySelector("small").textContent = new Date(b.dep + "T12:00:00").toLocaleDateString(lang() === "fr" ? "fr-FR" : "en-GB", { day: "numeric", month: "short" }); } catch (e) {}
        a.href = "/recherche/?flightSearch=" + from + ddmm(b.dep) + to + (b.ret ? ddmm(b.ret) : "") + "1";
        a.setAttribute("data-p", b.p);
        // Trier du moins cher au plus cher
        var kids = [].slice.call(row.children).sort(function (x, y) { return (+x.getAttribute("data-p") || 1e9) - (+y.getAttribute("data-p") || 1e9); });
        kids.forEach(function (k) { row.appendChild(k); });
      });
    });
  };
  window.addEventListener("escale:from", function (e) { if (e.detail && e.detail.code) { cur = { code: e.detail.code, name: e.detail.name }; if (seen) render(); } });
  if (window.ESCALE_FROM) cur = { code: window.ESCALE_FROM.code, name: window.ESCALE_FROM.name };
  var go = function () { seen = true; render(); };
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { if (es.some(function (x) { return x.isIntersecting; })) { io.disconnect(); go(); } }, { rootMargin: "300px" });
    io.observe(sec);
  } else go();
})();
