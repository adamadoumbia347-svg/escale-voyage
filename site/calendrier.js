// « Calendrier des prix de la diaspora » : pour un pays, le prix aller-retour le plus bas de chacun des 12 prochains mois
// (vers la capitale, depuis l'aéroport du visiteur, /api/calendar) et les fêtes qui font monter les prix.
(function () {
  "use strict";
  var box = document.getElementById("cal-app");
  if (!box || !window.ESCALE_FETE_FROM) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2), loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "en-GB";
  var C = JSON.parse(box.getAttribute("data-c")), E = JSON.parse(box.getAttribute("data-e")), T = JSON.parse(box.getAttribute("data-t"));
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var mname = function (m) { try { return new Date(m + "-15T12:00:00").toLocaleDateString(loc, { month: "long", year: "numeric" }); } catch (e) { return m; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var sel = document.getElementById("cal-c"), chart = document.getElementById("cal-chart"), tip = document.getElementById("cal-tip");
  var months = (function () { var d = new Date(), o = []; for (var i = 0; i < 12; i++) { var m = new Date(d.getFullYear(), d.getMonth() + i, 1); o.push(m.getFullYear() + "-" + ("0" + (m.getMonth() + 1)).slice(-2)); } return o; })();
  var from = "PAR", fromName = "Paris", tok = 0;
  var draw = function () {
    var cc = sel.value, c = C[cc], to = c[1], t0 = ++tok;
    document.querySelector(".cal-from").textContent = fromName;
    chart.innerHTML = '<p class="pr-wait">' + esc(T.loading) + "</p>"; tip.innerHTML = "";
    Promise.all(months.map(function (m) { return get("/api/calendar?from=" + from + "&to=" + to + "&month=" + m); })).then(function (rs) {
      if (t0 !== tok) return;
      var rows = months.map(function (m, i) { var r = rs[i], b = null; if (r && r.available && r.days) Object.keys(r.days).forEach(function (d) { var x = r.days[d]; if (x.price && (!b || x.price < b.p)) b = { p: x.price, d: d, r: x.ret }; }); return { m: m, b: b }; });
      var got = rows.filter(function (r) { return r.b; });
      var ev = E.filter(function (e) { return e.c.indexOf("*") >= 0 || e.c.indexOf(cc) >= 0; });
      var evOf = function (m) { return ev.filter(function (e) { return e.m.indexOf(m.slice(5, 7)) >= 0; }).map(function (e) { return e.n; }); };
      if (!got.length) { chart.innerHTML = '<p class="pr-wait">' + esc(T.none) + "</p>"; return; }
      var ps = got.map(function (r) { return r.b.p; }).sort(function (a, b) { return a - b; }), med = ps[Math.floor(ps.length / 2)], max = ps[ps.length - 1];
      var best = got.reduce(function (a, r) { return r.b.p < a.b.p ? r : a; });
      chart.innerHTML = '<ol class="mm-bars">' + rows.map(function (r) {
        var evs = evOf(r.m), tag = evs.length ? '<em class="cal-ev">' + esc(evs.join(" · ")) + "</em>" : "";
        if (!r.b) return '<li class="mm-empty"><span class="mm-bar" style="--h:6%"></span><b>–</b><small>' + esc(mname(r.m).split(" ")[0]) + "</small>" + tag + "</li>";
        var peak = r.b.p > med * 1.15;
        return '<li class="' + (r === best ? "mm-best" : peak ? "cal-peak" : "") + '"><a href="/recherche/?flightSearch=' + from + ddmm(r.b.d) + to + (r.b.r ? ddmm(r.b.r) : "") + '1"><span class="mm-bar" style="--h:' + Math.max(12, Math.round(r.b.p / max * 100)) + '%"></span><b>' + esc(money(r.b.p)) + "</b><small>" + esc(mname(r.m).split(" ")[0]) + "</small>" + tag + "</a></li>";
      }).join("") + "</ol>";
      var peaks = got.filter(function (r) { return r.b.p > med * 1.15; });
      tip.innerHTML = "<p><strong></strong></p><p></p>";
      tip.firstChild.firstChild.textContent = T.best.replace("{m}", mname(best.m)).replace("{p}", money(best.b.p));
      tip.lastChild.textContent = peaks.length ? T.peaks.replace("{m}", peaks.map(function (r) { return mname(r.m).split(" ")[0]; }).join(", ")) : T.flat;
    });
  };
  window.ESCALE_FETE_FROM.then(function (f) { from = /^(CDG|ORY|BVA)$/.test(f.code) ? "PAR" : f.code; fromName = f.name || "Paris"; draw(); });
  sel.addEventListener("change", draw);
})();
