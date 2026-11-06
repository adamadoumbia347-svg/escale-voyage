// Page « Surprends-moi » : tire au sort une destination aller-retour sous le budget, sur les 3 prochains mois,
// au départ de la ville choisie (prix réels via /api/explore?wide=1). Petit effet « roulette » avant le résultat.
(function () {
  "use strict";
  var box = document.getElementById("sp-box");
  if (!box) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "fr-FR";
  var T = JSON.parse(box.getAttribute("data-t"));
  var $ = function (id) { return document.getElementById(id); };
  var sel = $("sp-from"), chips = $("sp-budget"), go = $("sp-go"), stage = $("sp-stage");
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n, cur) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: cur || "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { weekday: "short", day: "numeric", month: "short" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var country = function (cc) { try { return new Intl.DisplayNames([lang], { type: "region" }).of(cc); } catch (e) { return cc; } };
  var flag = function (cc) { return cc && cc.length === 2 ? String.fromCodePoint.apply(null, cc.toUpperCase().split("").map(function (c) { return 127397 + c.charCodeAt(0); })) : "✈️"; };
  var iso = function (d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0"); };
  var calm = false; try { calm = matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
  var ALIAS = { LHR: "LON", LGW: "LON", STN: "LON", LTN: "LON", MXP: "MIL", LIN: "MIL", BGY: "MIL", FCO: "ROM", CIA: "ROM", ORY: "CDG", BVA: "CDG", SAW: "IST", EWR: "JFK", DKR: "DSS" };
  var db = Promise.all([get("/data/airports.json"), get("/data/photos.json"), lang === "fr" ? Promise.resolve({}) : get("/data/noms/" + lang + ".json")]);
  var months = []; for (var i = 0; i < 3; i++) { var d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + i); months.push(iso(d)); }

  // Ville : ?from=, sinon la dernière choisie sur Escale, sinon Paris
  var q = new URLSearchParams(location.search), saved = null;
  try { saved = localStorage.getItem("escale.any.from"); } catch (e) {}
  var f0 = (q.get("from") || saved || "CDG").toUpperCase();
  if ([].some.call(sel.options, function (o) { return o.value === f0; })) sel.value = f0;
  sel.addEventListener("change", function () { try { localStorage.setItem("escale.any.from", sel.value); } catch (e) {} });
  var max = 200, qm = +q.get("max");
  if (qm > 0) max = qm;
  var mark = function () { chips.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", String(+b.getAttribute("data-max") === max)); }); };
  if (![].some.call(chips.querySelectorAll("button"), function (b) { return +b.getAttribute("data-max") === max; })) max = 200;
  mark();
  chips.addEventListener("click", function (ev) { var b = ev.target.closest("button[data-max]"); if (!b) return; max = +b.getAttribute("data-max"); mark(); });

  // Prix des 3 mois, gardés en mémoire par ville (un seul appel par ville et par visite)
  var cache = {};
  var pool = function (from) {
    if (!cache[from]) cache[from] = Promise.all(months.map(function (m) { return get("/api/explore?from=" + from + "&month=" + m + "&currency=EUR&wide=1"); })).then(function (rs) {
      var best = {}, cur = "EUR";
      rs.forEach(function (r) { if (!r || !r.available || !r.items) return; cur = r.currency || cur; r.items.forEach(function (it) {
        if (!it.return_at) return; var k = it.city_code || it.to; if (!best[k] || it.price < best[k].price) best[k] = it; }); });
      return { cur: cur, items: Object.keys(best).map(function (k) { return best[k]; }) };
    });
    return cache[from];
  };
  var last = null;
  function draw() {
    var from = sel.value;
    go.disabled = true;
    stage.innerHTML = '<p class="sp-wait">' + esc(T.load) + "</p>";
    Promise.all([db, pool(from)]).then(function (r) {
      var rows = r[0][0] || [], photos = r[0][1] || [], names = r[0][2] || {}, P = r[1];
      var ap = {}; rows.forEach(function (a) { ap[a[0]] = a; });
      var ph = {}; photos.forEach(function (p) { ph[p.code] = p; });
      var nm = function (it) { var a = ap[it.to] || ap[it.city_code]; return names[it.to] || names[it.city_code] || (a ? a[1] : it.city_code || it.to); };
      var ok = P.items.filter(function (it) { return !max || it.price <= max; });
      if (!ok.length) { stage.innerHTML = '<p class="sp-wait">' + esc(T.none) + "</p>"; go.disabled = false; return; }
      var pick = ok[Math.floor(Math.random() * ok.length)];
      if (ok.length > 1 && last && pick.to === last) pick = ok.filter(function (x) { return x.to !== last; })[Math.floor(Math.random() * (ok.length - 1))];
      last = pick.to;
      var show = function () {
        var a = ap[pick.to] || ap[pick.city_code], p = ph[pick.to] || ph[ALIAS[pick.to]] || ph[pick.city_code] || ph[ALIAS[pick.city_code]];
        var dep = String(pick.departure_at).slice(0, 10), ret = String(pick.return_at).slice(0, 10), name = nm(pick), price = money(pick.price, P.cur);
        var href = "/recherche/?flightSearch=" + from + ddmm(dep) + pick.to + ddmm(ret) + "1";
        var txt = T.share_txt.replace("{c}", name).replace("{p}", price) + " " + location.origin + location.pathname + "?from=" + from + "&max=" + max;
        stage.innerHTML = '<article class="sp-card">' + (p ? '<img src="' + esc(p.img || p.img_small) + '" alt="" width="960" height="720" decoding="async">' : '<span class="sp-noimg" aria-hidden="true">✈️</span>') +
          '<div class="sp-txt"><p class="sp-name"><span aria-hidden="true">' + flag(a && a[3]) + "</span> <strong>" + esc(name) + "</strong></p>" +
          "<p class=\"sp-meta\">" + esc(a ? country(a[3]) : "") + " · " + esc(day(dep)) + " → " + esc(day(ret)) + " · " + esc(pick.transfers ? T.stop : T.direct) + "</p>" +
          '<p class="sp-price">' + esc(price) + "</p>" +
          '<div class="sp-actions"><a class="btn" href="' + esc(href) + '">' + esc(T.book) + " →</a>" +
          '<button type="button" class="btn sp-again" id="sp-again">' + esc(T.again) + "</button>" +
          '<a class="btn wa-btn" target="_blank" rel="noopener" href="https://wa.me/?text=' + encodeURIComponent(txt) + '">' + esc(T.share) + "</a></div></div></article>";
        $("sp-again").addEventListener("click", draw);
        go.disabled = false;
      };
      if (calm || ok.length < 2) return show();
      // Roulette : les noms défilent de plus en plus lentement, puis le résultat s'affiche
      stage.innerHTML = '<p class="sp-roll" id="sp-roll"></p>';
      var roll = $("sp-roll"), n = 0, steps = 16;
      (function tick() {
        var x = ok[Math.floor(Math.random() * ok.length)], a = ap[x.to] || ap[x.city_code];
        roll.textContent = flag(a && a[3]) + " " + nm(x);
        if (++n < steps) setTimeout(tick, 50 + n * n * 1.6); else setTimeout(show, 250);
      })();
    });
  }
  go.addEventListener("click", draw);
})();
