// Page « Quiz destination » : 5 questions, un score par destination (étiquettes dans data-cfg, voir scripts/quiz_pages.py),
// puis le vrai prix aller-retour du mois prochain depuis l'aéroport du visiteur (/api/prix) ; on garde 3 destinations dans le budget.
(function () {
  "use strict";
  var box = document.getElementById("qz");
  if (!box) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "fr-FR";
  var C = JSON.parse(box.getAttribute("data-cfg")), T = C.t, Q = C.q, D = C.d;
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n, cur) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: cur || "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { day: "numeric", month: "short" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var country = function (cc) { try { return new Intl.DisplayNames([lang], { type: "region" }).of(cc); } catch (e) { return cc; } };
  var ym = function (k) { var d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + k); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-01"; };
  var ALIAS = { TFS: "TCI", KEF: "REK", CPT: "CPT", FNC: "FNC", JFK: "NYC", DPS: "DPS" };
  var db = Promise.all([get("/data/airports.json"), get("/data/photos.json"), lang === "fr" ? Promise.resolve({}) : get("/data/noms/" + lang + ".json")]);
  var from = window.ESCALE_FETE_FROM ? window.ESCALE_FETE_FROM.then(function (f) { return { code: f.code === "PAR" ? "CDG" : f.code, name: f.name || (f.code === "CDG" || f.code === "PAR" ? "Paris" : f.code) }; }) : Promise.resolve({ code: "CDG", name: "Paris" });
  var ans = [];

  function ask(i) {
    var q = Q[i];
    box.innerHTML = '<div class="qz-q"><div class="qz-bar" aria-hidden="true"><span style="width:' + Math.round(i / Q.length * 100) + '%"></span></div>' +
      '<p class="qz-step">' + esc(T.step.replace("{i}", i + 1).replace("{n}", Q.length)) + "</p>" +
      '<h2 class="qz-h" tabindex="-1">' + esc(q[0]) + '</h2><div class="qz-opts">' +
      q[1].map(function (o, k) { return '<button type="button" class="qz-opt" data-k="' + k + '">' + esc(o[0]) + "</button>"; }).join("") + "</div>" +
      (i ? '<button type="button" class="qz-back">' + esc(T.back) + "</button>" : "") + "</div>";
    var h = box.querySelector(".qz-h"); if (h) h.focus();
    box.querySelectorAll(".qz-opt").forEach(function (b) {
      b.addEventListener("click", function () { ans[i] = q[1][+b.getAttribute("data-k")][1]; if (i + 1 < Q.length) ask(i + 1); else result(); });
    });
    var bk = box.querySelector(".qz-back"); if (bk) bk.addEventListener("click", function () { ask(i - 1); });
  }

  function score() {
    var a = {}; ans.forEach(function (x) { var p = x.split(":"); a[p[0]] = p[1]; });
    return { want: a, list: D.map(function (d) {
      var s = 0, types = d[1], dist = d[2];
      if (types.indexOf(a.t) === 0) s += 6; else if (types.indexOf(a.t) > 0) s += 4;
      if (a.d === "s") s += dist === "s" ? 3 : dist === "m" ? -1 : -4;
      if (a.d === "m") s += dist === "l" ? 0 : 2;
      if (a.d === "l") s += dist === "l" ? 3 : dist === "m" ? 1 : -1;
      if (a.v === d[3]) s += 2;
      if (a.w === "fam" && d[4] === "f") s += 2;
      if (a.w === "amis" && d[3] === "a") s += 1;
      if (a.w === "duo" && d[3] === "q") s += 1;
      return { d: d, s: s + Math.random() * 0.5 };
    }).sort(function (x, y) { return y.s - x.s; }) };
  }

  function result() {
    var sc = score(), max = +sc.want.p || 0, top = sc.list.slice(0, 8);
    box.innerHTML = '<p class="qz-wait">' + esc(T.load) + "</p>";
    Promise.all([db, from]).then(function (r) {
      var rows = r[0][0] || [], photos = r[0][1] || [], names = r[0][2] || {}, f = r[1];
      var ap = {}; rows.forEach(function (x) { ap[x[0]] = x; });
      var ph = {}; photos.forEach(function (p) { ph[p.code] = p; });
      var price = function (to) {
        var u = function (k) { return "/api/prix?from=" + f.code + "&to=" + to + "&dep=" + ym(k) + "&rt=1&currency=EUR"; };
        return get(u(1)).then(function (x) { return x && x.price ? x : get(u(2)); });
      };
      return Promise.all(top.map(function (t) { return t.d[0] === f.code ? Promise.resolve(null) : price(t.d[0]); })).then(function (ps) {
        var all = top.map(function (t, k) { return { d: t.d, p: ps[k] && ps[k].price ? ps[k] : null }; }).filter(function (x) { return x.d[0] !== f.code; });
        var fit = all.filter(function (x) { return x.p && (!max || x.p.price <= max); });
        var pick = fit.slice(0, 3);
        all.forEach(function (x) { if (pick.length < 3 && pick.indexOf(x) < 0) pick.push(x); });
        var first = pick[0], fn = names[first.d[0]] || (ap[first.d[0]] || [])[1] || first.d[0];
        var txt = T.share_txt.replace("{c}", fn) + " " + location.origin + location.pathname;
        box.innerHTML = '<h2 class="qz-res-h">' + esc(T.res_h) + "</h2>" +
          '<p class="small">' + esc(T.from_l) + " <strong>" + esc(f.name) + "</strong></p>" +
          '<ol class="qz-res">' + pick.map(function (x, k) {
            var c = x.d[0], a = ap[c], p = ph[c] || ph[ALIAS[c]], n = names[c] || (a ? a[1] : c);
            var tags = (x.d[1].split("").concat([x.d[2]], x.d[4] ? ["f"] : [])).map(function (g) { return T.tags[g] ? '<span class="qz-tag">' + esc(T.tags[g]) + "</span>" : ""; }).join("");
            var pr = x.p, dep = pr && pr.departure_at ? String(pr.departure_at).slice(0, 10) : "", ret = pr && pr.return_at ? String(pr.return_at).slice(0, 10) : "";
            var href = dep && ret ? "/recherche/?flightSearch=" + f.code + ddmm(dep) + c + ddmm(ret) + "1" : "/?type=vols&to=" + c + (lang !== "fr" ? "&lang=" + lang : "");
            var priceH = pr ? '<b class="qz-price">' + esc(money(pr.price, pr.currency)) + "</b>" + (max && pr.price > max ? '<small class="qz-over">' + esc(T.over) + "</small>" : "") + (dep && ret ? "<small>" + esc(day(dep)) + " → " + esc(day(ret)) + "</small>" : "") : '<small>' + esc(T.none_price) + "</small>";
            return '<li class="qz-card' + (k === 0 ? " first" : "") + '"><a href="' + esc(href) + '">' +
              (p ? '<img src="' + esc(k === 0 ? (p.img || p.img_small) : (p.img_small || p.img)) + '" alt="" width="480" height="360" loading="lazy" decoding="async">' : '<span class="we-noimg" aria-hidden="true">✈️</span>') +
              '<span class="qz-txt"><span class="qz-rank">' + (k + 1) + '</span><strong>' + esc(n) + "</strong><small>" + esc(a ? country(a[3]) : "") + '</small><span class="qz-tags">' + tags + "</span>" +
              '<span class="qz-pr">' + priceH + '</span><span class="qz-go">' + esc(T.book) + " →</span></span></a></li>";
          }).join("") + "</ol>" +
          '<div class="qz-actions"><a class="btn wa-btn" target="_blank" rel="noopener" href="https://wa.me/?text=' + encodeURIComponent(txt) + '">' + esc(T.share) + '</a>' +
          '<button type="button" class="btn qz-again" id="qz-again">' + esc(T.again) + "</button></div>";
        document.getElementById("qz-again").addEventListener("click", function () { ans = []; ask(0); });
        var h = box.querySelector(".qz-res-h"); if (h) { h.setAttribute("tabindex", "-1"); h.focus(); }
      });
    });
  }
  document.getElementById("qz-start").addEventListener("click", function () { ask(0); });
})();
