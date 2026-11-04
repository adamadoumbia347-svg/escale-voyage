// Page « Fais venir un proche / Paye pour moi » :
//  - mode choix : la personne au pays (ou qui organise) choisit départ, arrivée, mois → 3 meilleurs vols réels (/api/calendar),
//    puis « Envoyer pour paiement » ouvre WhatsApp avec un lien vers ce vol précis ;
//  - mode paiement (?v=ABJ-PAR-20261209-20261223-421) : la personne qui paie voit ce vol, le prix actuel (/api/prix) et réserve.
// Escale ne touche jamais à l'argent : la réservation se fait chez le partenaire, comme partout sur le site.
(function () {
  "use strict";
  var app = document.getElementById("pr-app");
  if (!app) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2), loc = lang === "fr" ? "fr-FR" : "en-GB";
  var T = JSON.parse(app.getAttribute("data-t"));
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { weekday: "short", day: "numeric", month: "long" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var ymd = function (s) { return s.slice(0, 4) + "-" + s.slice(4, 6) + "-" + s.slice(6, 8); };
  var FROM = JSON.parse(app.getAttribute("data-from")), TO = JSON.parse(app.getAttribute("data-to"));
  var names = {}; FROM.concat(TO).forEach(function (x) { names[x[0]] = x[1]; });
  var name = function (c) { return names[c] || c; };
  var engine = function (f, t, dep, ret) { return "/recherche/?flightSearch=" + f + ddmm(dep) + t + (ret ? ddmm(ret) : "") + "1"; };

  // ---------- Mode paiement ----------
  var v = (new URLSearchParams(location.search).get("v") || "").match(/^([A-Z]{3})-([A-Z]{3})-(\d{8})-(\d{8})-(\d{1,5})$/);
  if (v) {
    var f = v[1], t = v[2], dep = ymd(v[3]), ret = ymd(v[4]), seen = +v[5];
    document.querySelectorAll(".pr-choose-only").forEach(function (e) { e.hidden = true; });
    app.innerHTML = '<div class="pr-pay"><p class="eyebrow">' + esc(T.pay_eyebrow) + "</p><h2>" + esc(name(f)) + " → " + esc(name(t)) + "</h2>" +
      '<p class="pr-dates">✈️ ' + esc(day(dep)) + "<br>↩️ " + esc(day(ret)) + "</p>" +
      '<p class="pr-seen">' + esc(T.seen.replace("{p}", money(seen))) + '</p><p class="pr-now" aria-live="polite">' + esc(T.checking) + "</p>" +
      '<a class="btn pr-book" href="' + engine(f, t, dep, ret) + '">' + esc(T.book) + "</a>" +
      '<p class="small">' + esc(T.book_note) + "</p></div>";
    var box = document.getElementById("price-alert"); if (box) { box.setAttribute("data-from", f); box.setAttribute("data-to", t); box.hidden = true; }
    get("/api/prix?from=" + f + "&to=" + t + "&dep=" + dep + "&ret=" + ret + "&currency=EUR").then(function (d) {
      var now = app.querySelector(".pr-now");
      if (d && d.available && d.price) {
        now.innerHTML = "<strong></strong>"; now.firstChild.textContent = T.now.replace("{p}", money(d.price));
        if (d.price < seen) now.classList.add("pr-down");
      } else now.textContent = T.now_none;
    });
    return;
  }

  // ---------- Mode choix ----------
  var months = (function () { var d = new Date(), out = []; for (var i = 0; i < 6; i++) { var m = new Date(d.getFullYear(), d.getMonth() + i, 1); out.push(m.getFullYear() + "-" + ("0" + (m.getMonth() + 1)).slice(-2)); } return out; })();
  var mname = function (m) { try { return new Date(m + "-15T12:00:00").toLocaleDateString(loc, { month: "long" }); } catch (e) { return m; } };
  var st = { f: FROM[0][0], t: TO[0][0], m: months[1] };
  var chips = function (key, list) {
    return '<div class="pr-chips" role="group" data-k="' + key + '">' + list.map(function (x) {
      return '<button type="button" data-v="' + x[0] + '" aria-pressed="' + (st[key] === x[0]) + '">' + esc(x[2] ? x[2] + " " : "") + esc(x[1]) + "</button>";
    }).join("") + "</div>";
  };
  var draw = function () {
    app.innerHTML = '<div class="pr-step"><h2>1. ' + esc(T.q_from) + "</h2>" + chips("f", FROM) + "</div>" +
      '<div class="pr-step"><h2>2. ' + esc(T.q_to) + "</h2>" + chips("t", TO) + "</div>" +
      '<div class="pr-step"><h2>3. ' + esc(T.q_month) + "</h2>" + chips("m", months.map(function (m) { return [m, mname(m)]; })) + "</div>" +
      '<div class="pr-res" id="pr-res" aria-live="polite"></div>';
    app.querySelectorAll(".pr-chips").forEach(function (g) {
      g.addEventListener("click", function (e) {
        var b = e.target.closest("button"); if (!b) return;
        st[g.getAttribute("data-k")] = b.getAttribute("data-v");
        g.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        search();
      });
    });
    search();
  };
  var tok = 0;
  var search = function () {
    var t0 = ++tok, res = document.getElementById("pr-res");
    if (st.f === st.t) { res.innerHTML = ""; return; }
    res.innerHTML = '<p class="pr-wait">' + esc(T.loading) + "</p>";
    get("/api/calendar?from=" + st.f + "&to=" + st.t + "&month=" + st.m).then(function (r) {
      if (t0 !== tok) return;
      var days = r && r.available && r.days ? Object.keys(r.days).map(function (k) { return { dep: k, ret: r.days[k].ret, p: r.days[k].price, s: r.days[k].transfers }; }).filter(function (x) { return x.p && x.ret; }) : [];
      days.sort(function (a, b) { return a.p - b.p; });
      if (!days.length) { res.innerHTML = '<p class="pr-wait">' + esc(T.none) + "</p>"; return; }
      res.innerHTML = '<h2>' + esc(T.best_h.replace("{a}", name(st.f)).replace("{b}", name(st.t))) + "</h2>" + days.slice(0, 3).map(function (x, i) {
        var link = location.origin + location.pathname + "?v=" + st.f + "-" + st.t + "-" + x.dep.replace(/-/g, "") + "-" + x.ret.replace(/-/g, "") + "-" + Math.round(x.p);
        var msg = T.wa.replace("{a}", name(st.f)).replace("{b}", name(st.t)).replace("{d}", day(x.dep)).replace("{r}", day(x.ret)).replace("{p}", money(x.p)).replace("{u}", link);
        return '<div class="pr-offer' + (i === 0 ? " pr-best" : "") + '">' + (i === 0 ? '<span class="pr-tag">' + esc(T.cheapest) + "</span>" : "") +
          '<p class="pr-price">' + esc(money(x.p)) + ' <small>' + esc(T.rt) + "</small></p>" +
          '<p class="pr-dates">✈️ ' + esc(day(x.dep)) + "<br>↩️ " + esc(day(x.ret)) + " · " + esc(x.s ? (x.s === 1 ? T.stop1 : T.stops.replace("{n}", x.s)) : T.direct) + "</p>" +
          '<div class="pr-btns"><a class="btn wa-btn" target="_blank" rel="noopener" href="https://wa.me/?text=' + encodeURIComponent(msg) + '">📲 ' + esc(T.send) + "</a>" +
          '<a class="btn ghost" href="' + engine(st.f, st.t, x.dep, x.ret) + '">' + esc(T.self) + "</a></div></div>";
      }).join("") + '<p class="small">' + esc(T.note) + "</p>";
      var box = document.getElementById("price-alert"); if (box) { box.setAttribute("data-from", st.f); box.setAttribute("data-to", st.t); }
    });
  };
  // Arrivée par défaut : l'aéroport du visiteur s'il est dans la liste (sinon Paris)
  var start = function () { draw(); };
  if (window.ESCALE_FETE_FROM) window.ESCALE_FETE_FROM.then(function (fr) {
    var CITY = { CDG: "PAR", ORY: "PAR", BVA: "PAR", MXP: "MIL", LIN: "MIL", BGY: "MIL", FCO: "ROM", CIA: "ROM", CRL: "BRU", LHR: "LON", LGW: "LON", STN: "LON", LTN: "LON", LCY: "LON", ORY2: "" };
    var c = CITY[fr.code] || fr.code;
    if (TO.some(function (x) { return x[0] === c; })) st.t = c;
    if (FROM.some(function (x) { return x[0] === c; })) st.f = c;
    start();
  }); else start();
})();
