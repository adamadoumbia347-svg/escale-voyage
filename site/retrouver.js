// Page « On se retrouve où ? » : deux villes de départ, un mois ; on croise /api/explore (wide=1) des deux villes
// et on classe les destinations communes par prix total (aller-retour de chacun additionnés).
(function () {
  "use strict";
  var form = document.getElementById("mt-form");
  if (!form) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "fr-FR";
  var T = JSON.parse(form.getAttribute("data-t"));
  var SHARE = { fr: "Partager sur WhatsApp", en: "Share on WhatsApp", it: "Condividi su WhatsApp", de: "Auf WhatsApp teilen" }[lang] || "WhatsApp";
  var $ = function (id) { return document.getElementById(id); };
  var A = $("mt-a"), Bs = $("mt-b"), months = $("mt-months"), status = $("mt-status"), list = $("mt-list"), visit = $("mt-visit");
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n, cur) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: cur || "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { day: "numeric", month: "short" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var country = function (cc) { try { return new Intl.DisplayNames([lang], { type: "region" }).of(cc); } catch (e) { return cc; } };
  var iso = function (d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0"); };
  var label = function (sel) { return (sel.options[sel.selectedIndex] || {}).textContent.replace(/\s*\([A-Z]{3}\)$/, ""); };
  // Code « ville » d'un aéroport de départ, pour reconnaître « l'un rend visite à l'autre »
  var CITY = { CDG: "PAR", LHR: "LON", FCO: "ROM", MXP: "MIL", JFK: "NYC", IAD: "WAS", YUL: "YMQ", YYZ: "YTO", DSS: "DKR", BER: "BER", IAH: "HOU", CMN: "CAS" };
  var city = function (c) { return CITY[c] || c; };
  var ALIAS = { LHR: "LON", LGW: "LON", STN: "LON", LTN: "LON", MXP: "MIL", LIN: "MIL", BGY: "MIL", FCO: "ROM", CIA: "ROM", ORY: "CDG", BVA: "CDG", SAW: "IST", EWR: "JFK", DKR: "DSS" };
  var db = Promise.all([get("/data/airports.json"), get("/data/photos.json"), lang === "fr" ? Promise.resolve({}) : get("/data/noms/" + lang + ".json")]);

  // Mois : le mois prochain par défaut, sur 6 mois
  var ms = [], month;
  for (var i = 0; i < 6; i++) { var d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + i); ms.push(iso(d)); }
  var q = new URLSearchParams(location.search);
  month = ms.indexOf(q.get("m")) >= 0 ? q.get("m") : ms[1];
  var paint = function () {
    months.innerHTML = ms.map(function (m) {
      var p = m.split("-"), l = new Date(+p[0], +p[1] - 1, 1).toLocaleDateString(loc, { month: "short", year: "numeric" });
      return '<button type="button" data-m="' + m + '" aria-pressed="' + (m === month) + '">' + esc(l) + "</button>";
    }).join("");
  };
  paint();
  months.addEventListener("click", function (ev) { var b = ev.target.closest("button[data-m]"); if (!b) return; month = b.getAttribute("data-m"); paint(); run(); });

  // Villes : adresse partagée (?a=CDG&b=DSS), sinon la dernière ville de départ choisie sur Escale, et Dakar pour l'autre
  var has = function (sel, c) { return [].some.call(sel.options, function (o) { return o.value === c; }); };
  var saved = null; try { saved = localStorage.getItem("escale.any.from"); } catch (e) {}
  var a0 = (q.get("a") || saved || "CDG").toUpperCase(), b0 = (q.get("b") || "").toUpperCase();
  if (has(A, a0)) A.value = a0;
  Bs.value = has(Bs, b0) ? b0 : (A.value === "DSS" ? "CDG" : "DSS");

  var req = 0;
  function run() {
    var a = A.value, b = Bs.value, id = ++req;
    visit.hidden = true; visit.innerHTML = "";
    if (a === b) { status.textContent = T.same; list.innerHTML = ""; return; }
    try { history.replaceState(null, "", location.pathname + "?a=" + a + "&b=" + b + "&m=" + month + (lang !== "fr" && /[?&]lang=/.test(location.search) ? "&lang=" + lang : "")); } catch (e) {}
    status.textContent = T.load; list.innerHTML = "";
    var call = function (c) { return get("/api/explore?from=" + c + "&month=" + month + "&currency=EUR&wide=1"); };
    Promise.all([db, call(a), call(b)]).then(function (r) {
      if (id !== req) return;
      var rows = r[0][0] || [], photos = r[0][1] || [], names = r[0][2] || {};
      var ap = {}; rows.forEach(function (x) { ap[x[0]] = x; });
      var ph = {}; photos.forEach(function (p) { ph[p.code] = p; });
      var ok = function (d) { return d && d.available && d.items ? d.items.filter(function (it) { return it.return_at; }) : []; };
      var ia = ok(r[1]), ib = ok(r[2]), cur = (r[1] && r[1].currency) || "EUR";
      var key = function (it) { return it.city_code || it.to; };
      var best = function (items) { var m = {}; items.forEach(function (it) { var k = key(it); if (!m[k] || it.price < m[k].price) m[k] = it; }); return m; };
      var ma = best(ia), mb = best(ib);
      var nm = function (it) { var x = ap[it.to] || ap[it.city_code]; return names[it.to] || names[it.city_code] || (x ? x[1] : it.city_code || it.to); };
      var href = function (from, it) { return "/recherche/?flightSearch=" + from + ddmm(String(it.departure_at).slice(0, 10)) + it.to + ddmm(String(it.return_at).slice(0, 10)) + "1"; };
      var span = function (it) { return day(String(it.departure_at).slice(0, 10)) + " → " + day(String(it.return_at).slice(0, 10)); };

      // L'un rend visite à l'autre (si le trajet direct entre les deux villes fait partie des résultats)
      var ab = ma[city(b)] || ma[b], ba = mb[city(a)] || mb[a], v = [];
      if (ab) v.push('<a href="' + esc(href(a, ab)) + '">' + esc(T.visit_ab.replace("{a}", label(A)).replace("{b}", label(Bs))) + " <b>" + esc(money(ab.price, cur)) + "</b></a>");
      if (ba) v.push('<a href="' + esc(href(b, ba)) + '">' + esc(T.visit_ab.replace("{a}", label(Bs)).replace("{b}", label(A))) + " <b>" + esc(money(ba.price, cur)) + "</b></a>");
      if (v.length) { visit.innerHTML = "<strong>" + esc(T.visit) + "</strong> " + v.join(" "); visit.hidden = false; }

      var skip = {}; [a, b, city(a), city(b)].forEach(function (c) { skip[c] = 1; });
      var both = Object.keys(ma).filter(function (k) { return mb[k] && !skip[k] && !skip[ma[k].to]; }).map(function (k) {
        var x = ma[k], y = mb[k];
        var s = Math.max(Date.parse(String(x.departure_at).slice(0, 10)), Date.parse(String(y.departure_at).slice(0, 10)));
        var e = Math.min(Date.parse(String(x.return_at).slice(0, 10)), Date.parse(String(y.return_at).slice(0, 10)));
        return { k: k, x: x, y: y, total: x.price + y.price, days: e >= s ? Math.round((e - s) / 864e5) + 1 : 0 };
      }).sort(function (p, q2) { return p.total - q2.total; }).slice(0, 24);
      if (!both.length) { status.textContent = T.none; return; }
      status.textContent = T.count.replace("{n}", both.length);
      list.innerHTML = both.map(function (m) {
        var x = ap[m.x.to] || ap[m.x.city_code], p = ph[m.x.to] || ph[ALIAS[m.x.to]] || ph[m.k] || ph[ALIAS[m.k]];
        return '<li class="mt-card">' + (p ? '<img src="' + esc(p.img_small || p.img) + '" alt="" width="480" height="360" loading="lazy" decoding="async">' : '<span class="we-noimg" aria-hidden="true">✈️</span>') +
          '<div class="mt-body"><div class="mt-top"><span><strong>' + esc(nm(m.x)) + "</strong><small>" + esc(x ? country(x[3]) : "") + "</small></span>" +
          '<span class="mt-total"><b>' + esc(money(m.total, cur)) + "</b><small>" + esc(T.total) + "</small></span></div>" +
          '<span class="mt-badge' + (m.days ? " on" : "") + '">' + esc(m.days ? (m.days === 1 ? T.together.replace(/jours|days|giorni|Tage/, function (w) { return { jours: "jour", days: "day", giorni: "giorno", Tage: "Tag" }[w]; }) : T.together).replace("{n}", m.days) : T.adjust) + "</span>" +
          '<a class="mt-leg" href="' + esc(href(a, m.x)) + '"><span>' + esc(T.you) + " · " + esc(label(A)) + "<small>" + esc(span(m.x)) + "</small></span><b>" + esc(money(m.x.price, cur)) + "</b></a>" +
          '<a class="mt-leg" href="' + esc(href(b, m.y)) + '"><span>' + esc(T.them) + " · " + esc(label(Bs)) + "<small>" + esc(span(m.y)) + "</small></span><b>" + esc(money(m.y.price, cur)) + "</b></a>" +
          "</div></li>";
      }).join("") + '<li class="mt-share"><a class="btn wa-btn" target="_blank" rel="noopener" href="https://wa.me/?text=' + encodeURIComponent(document.title.split(" | ")[0] + " " + location.href) + '">' + esc(SHARE) + "</a></li>";
    });
  }
  form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
  A.addEventListener("change", run); Bs.addEventListener("change", run);
  run();
})();
