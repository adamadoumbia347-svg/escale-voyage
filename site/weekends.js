// Page « Week-ends pas chers » : week-ends aller-retour (vendredi/samedi → dimanche/lundi) des 8 prochaines semaines,
// au départ de l'aéroport du visiteur (window.ESCALE_FETE_FROM, voir fetes.js), prix réels via /api/weekends.
(function () {
  "use strict";
  var box = document.getElementById("we-list");
  if (!box || !window.ESCALE_FETE_FROM) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "fr-FR";
  var T = JSON.parse(box.getAttribute("data-t"));
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n, cur) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: cur || "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { weekday: "short", day: "numeric", month: "short" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var country = function (cc) { try { return new Intl.DisplayNames([lang], { type: "region" }).of(cc); } catch (e) { return cc; } };
  var ALIAS = { LHR: "LON", LGW: "LON", STN: "LON", LTN: "LON", LCY: "LON", MXP: "MIL", LIN: "MIL", BGY: "MIL", FCO: "ROM", CIA: "ROM", TSF: "VCE", ARN: "STO", BMA: "STO", KEF: "REK",
    TFS: "TCI", TFN: "TCI", EWR: "JFK", LGA: "JFK", SAW: "IST", YUL: "YMQ", NRT: "HND", DKR: "DSS", PAR: "CDG", ORY: "CDG", BVA: "CDG", BCN: "BCN", OPO: "OPO" };
  var data = Promise.all([get("/data/airports.json"), get("/data/photos.json"), lang === "fr" ? Promise.resolve({}) : get("/data/noms/" + lang + ".json")]);
  var budget = Number(box.getAttribute("data-max")) || 100, from = null;
  var render = function () {
    box.innerHTML = '<p class="we-wait">' + esc(T.loading) + "</p>";
    Promise.all([data, get("/api/weekends?from=" + from.code + "&max=" + budget + "&currency=EUR")]).then(function (r) {
      var db = r[0][0] || [], photos = r[0][1] || [], names = r[0][2] || {}, d = r[1];
      var ap = {}; db.forEach(function (a) { ap[a[0]] = a; });
      var ph = {}; photos.forEach(function (p) { ph[p.code] = p; });
      if (!d || !d.available || !d.items || !d.items.length) { box.innerHTML = '<p class="we-wait">' + esc(T.none) + "</p>"; return; }
      box.innerHTML = d.items.map(function (it) {
        var a = ap[it.to] || ap[it.city] || null, name = names[it.to] || names[it.city] || (a ? a[1] : it.city || it.to);
        var p = ph[it.to] || ph[ALIAS[it.to]] || ph[it.city] || ph[ALIAS[it.city]];
        var href = "/recherche/?flightSearch=" + from.code + ddmm(it.dep) + it.to + ddmm(it.ret) + "1";
        return '<li class="we-card"><a href="' + href + '">' + (p ? '<img src="' + esc(p.img_small || p.img) + '" alt="" width="480" height="360" loading="lazy" decoding="async">' : '<span class="we-noimg" aria-hidden="true">✈️</span>') +
          '<span class="we-txt"><strong>' + esc(name) + "</strong><small>" + esc(a ? country(a[3]) : "") + "</small>" +
          '<span class="we-dates">' + esc(day(it.dep)) + " → " + esc(day(it.ret)) + " · " + esc(it.transfers ? T.stop : T.direct) + "</span>" +
          '<b class="we-price">' + esc(money(it.price, d.currency)) + "</b></span></a></li>";
      }).join("");
    });
  };
  document.querySelectorAll(".we-budget button").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".we-budget button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      budget = Number(b.getAttribute("data-max")); if (from) render();
    });
  });
  window.ESCALE_FETE_FROM.then(function (f) {
    from = { code: f.code === "CDG" ? "PAR" : f.code, name: f.name || "Paris" };
    var c = document.querySelector(".we-from"); if (c) c.textContent = from.name;
    render();
  });
})();
