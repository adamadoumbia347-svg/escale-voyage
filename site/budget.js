// Pages « Où partir avec X € ? » : destinations aller-retour sous le budget de la page (data-max), sur les 3 prochains mois,
// au départ de l'aéroport du visiteur (window.ESCALE_FETE_FROM, voir fetes.js), prix réels via /api/explore.
(function () {
  "use strict";
  var box = document.getElementById("bu-list");
  if (!box || !window.ESCALE_FETE_FROM) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "fr-FR";
  var T = JSON.parse(box.getAttribute("data-t"));
  var max = Number(box.getAttribute("data-max")) || 100;
  var count = document.getElementById("bu-count");
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n, cur) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: cur || "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { day: "numeric", month: "short" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var country = function (cc) { try { return new Intl.DisplayNames([lang], { type: "region" }).of(cc); } catch (e) { return cc; } };
  var iso = function (d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0"); };
  var months = [];
  for (var i = 0; i < 3; i++) { var d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + i); months.push(iso(d)); }
  var ALIAS = { LHR: "LON", LGW: "LON", STN: "LON", LTN: "LON", MXP: "MIL", LIN: "MIL", BGY: "MIL", FCO: "ROM", CIA: "ROM", ORY: "CDG", BVA: "CDG", SAW: "IST", EWR: "JFK", DKR: "DSS" };
  var data = Promise.all([get("/data/airports.json"), get("/data/photos.json"), lang === "fr" ? Promise.resolve({}) : get("/data/noms/" + lang + ".json")]);

  box.innerHTML = '<p class="we-wait">' + esc(T.loading) + "</p>";
  window.ESCALE_FETE_FROM.then(function (f) {
    var code = f.code === "PAR" ? "CDG" : f.code;
    var c = document.querySelector(".we-from"); if (c) c.textContent = f.name || (code === "CDG" ? "Paris" : code);
    var calls = months.map(function (m) { return get("/api/explore?from=" + code + "&month=" + m + "&currency=EUR"); });
    return Promise.all([data, Promise.all(calls)]).then(function (r) {
      var db = r[0][0] || [], photos = r[0][1] || [], names = r[0][2] || {};
      var ap = {}; db.forEach(function (a) { ap[a[0]] = a; });
      var ph = {}; photos.forEach(function (p) { ph[p.code] = p; });
      // Meilleur prix par ville sur les 3 mois, sous le budget
      var best = {}, cur = "EUR";
      r[1].forEach(function (d) {
        if (!d || !d.available || !d.items) return;
        cur = d.currency || cur;
        d.items.forEach(function (it) {
          if (!(it.price <= max) || !it.return_at) return;
          var k = it.city_code || it.to;
          if (!best[k] || it.price < best[k].price) best[k] = it;
        });
      });
      var items = Object.keys(best).map(function (k) { return best[k]; }).sort(function (a, b) { return a.price - b.price; });
      if (!items.length) { box.innerHTML = '<p class="we-wait">' + esc(T.none) + "</p>"; if (count) count.textContent = ""; return; }
      if (count) count.textContent = T.count.replace("{c}", items.length);
      box.innerHTML = items.map(function (it) {
        var dep = String(it.departure_at).slice(0, 10), ret = String(it.return_at).slice(0, 10);
        var a = ap[it.to] || ap[it.city_code] || null, name = names[it.to] || names[it.city_code] || (a ? a[1] : it.city_code || it.to);
        var p = ph[it.to] || ph[ALIAS[it.to]] || ph[it.city_code] || ph[ALIAS[it.city_code]];
        var href = "/recherche/?flightSearch=" + code + ddmm(dep) + it.to + ddmm(ret) + "1";
        return '<li class="we-card"><a href="' + href + '">' + (p ? '<img src="' + esc(p.img_small || p.img) + '" alt="" width="480" height="360" loading="lazy" decoding="async">' : '<span class="we-noimg" aria-hidden="true">✈️</span>') +
          '<span class="we-txt"><strong>' + esc(name) + "</strong><small>" + esc(a ? country(a[3]) : "") + "</small>" +
          '<span class="we-dates">' + esc(day(dep)) + " → " + esc(day(ret)) + " · " + esc(it.transfers ? T.stop : T.direct) + "</span>" +
          '<b class="we-price">' + esc(money(it.price, cur)) + "</b></span></a></li>";
      }).join("");
    });
  });
})();
