// « Où partir sans visa avec mon passeport ? » : destinations sans visa ou avec visa électronique / à l'arrivée
// (règles de l'outil visa, scripts/visa.py), avec le meilleur aller-retour du mois prochain depuis l'aéroport du visiteur.
(function () {
  "use strict";
  var box = document.getElementById("sv-app");
  if (!box) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2), loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "en-GB";
  var D = JSON.parse(box.getAttribute("data-d")), T = JSON.parse(box.getAttribute("data-t"));
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var sel = document.getElementById("sv-pass"), grid = document.getElementById("sv-grid");
  var col = lang === "fr" ? 0 : 1, from = "PAR", fromName = "Paris", tok = 0;
  var d0 = new Date(), m1 = new Date(d0.getFullYear(), d0.getMonth() + 1, 1), month = m1.getFullYear() + "-" + ("0" + (m1.getMonth() + 1)).slice(-2);
  var draw = function () {
    var p = sel.value, t0 = ++tok;
    try { localStorage.setItem("escale.visa.p", p); } catch (e) {}
    var list = Object.keys(D.d).filter(function (k) { var st = D.r[p + "-" + k]; return (st === 0 || st === 1) && k !== p; });
    list.sort(function (a, b) { return (D.r[p + "-" + a] - D.r[p + "-" + b]); });
    document.querySelector(".sv-from").textContent = fromName;
    if (!list.length) { grid.innerHTML = '<p class="pr-wait">' + esc(T.none) + "</p>"; return; }
    grid.innerHTML = list.map(function (k) {
      var x = D.d[k], st = D.r[p + "-" + k];
      return '<li class="sv-card" data-k="' + k + '"><span class="sv-flag" aria-hidden="true">' + x[2] + "</span><strong>" + esc(x[col]) + "</strong>" +
        '<span class="sv-st sv-st' + st + '">' + esc(st === 0 ? T.s0 : T.s1) + '</span><span class="sv-pr"></span>' +
        '<span class="sv-links"><a class="sv-go" href="/?type=vols&amp;from=' + from + "&amp;to=" + x[3] + '">' + esc(T.flights) + '</a> · <a href="' + (lang === "fr" ? "/visa/" : "/en/visa/") + "?p=" + p + "&amp;d=" + k + '">' + esc(T.details) + "</a></span></li>";
    }).join("");
    grid.querySelectorAll(".sv-card").forEach(function (c) {
      var k = c.getAttribute("data-k"), to = D.d[k][3];
      if (to === from) { c.querySelector(".sv-pr").textContent = ""; return; }
      get("/api/calendar?from=" + from + "&to=" + to + "&month=" + month).then(function (r) {
        if (t0 !== tok) return;
        var b = null; if (r && r.available && r.days) Object.keys(r.days).forEach(function (d) { var y = r.days[d]; if (y.price && (!b || y.price < b.p)) b = { p: y.price, d: d, r: y.ret }; });
        if (!b) return;
        c.querySelector(".sv-pr").textContent = T.from + " " + money(b.p);
        c.querySelector(".sv-go").href = "/recherche/?flightSearch=" + from + ddmm(b.d) + to + (b.r ? ddmm(b.r) : "") + "1";
      });
    });
  };
  // Passeport par défaut : celui choisi avant, sinon le pays du visiteur (/api/geo) s'il est dans la liste
  var saved = null; try { saved = localStorage.getItem("escale.visa.p"); } catch (e) {}
  var q = new URLSearchParams(location.search).get("p");
  Promise.all([get("/api/geo"), window.ESCALE_FETE_FROM || Promise.resolve(null)]).then(function (r) {
    var g = r[0], fr = r[1];
    var pick = q && D.p[q] ? q : saved && D.p[saved] ? saved : g && g.country && D.p[g.country] ? g.country : sel.value;
    sel.value = pick;
    if (fr) { from = /^(CDG|ORY|BVA)$/.test(fr.code) ? "PAR" : fr.code; fromName = fr.name || "Paris"; }
    draw();
  });
  sel.addEventListener("change", draw);
})();
