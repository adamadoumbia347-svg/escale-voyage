// Pages « Meilleur mois pour partir à… » : prix aller-retour le plus bas de chacun des 12 prochains mois,
// depuis l'aéroport du visiteur (window.ESCALE_FETE_FROM, voir fetes.js), via le calendrier des prix (/api/calendar).
// Aucun prix n'est écrit dans la page ; un mois sans prix trouvé reste vide.
(function () {
  "use strict";
  var box = document.getElementById("mm-chart");
  if (!box || !window.ESCALE_FETE_FROM) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "fr-FR";
  var T = JSON.parse(box.getAttribute("data-t")), to = box.getAttribute("data-to");
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var money = function (n, cur) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: cur || "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var mname = function (m) { try { return new Date(m + "-15T12:00:00").toLocaleDateString(loc, { month: "long", year: "numeric" }); } catch (e) { return m; } };
  var mshort = function (m) { try { return new Date(m + "-15T12:00:00").toLocaleDateString(loc, { month: "short" }); } catch (e) { return m.slice(5); } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var months = (function () { var d = new Date(), out = []; for (var i = 0; i < 12; i++) { var m = new Date(d.getFullYear(), d.getMonth() + i, 1); out.push(m.getFullYear() + "-" + ("0" + (m.getMonth() + 1)).slice(-2)); } return out; })();
  box.innerHTML = '<p class="mm-wait">' + T.loading + "</p>";
  window.ESCALE_FETE_FROM.then(function (f) {
    var from = f.code === "CDG" ? "PAR" : f.code;
    var fc = document.querySelector(".mm-from"); if (fc) fc.textContent = f.name || "Paris";
    if (from === to) { box.innerHTML = '<p class="mm-wait">' + T.same + "</p>"; return; }
    Promise.all(months.map(function (m) { return get("/api/calendar?from=" + from + "&to=" + to + "&month=" + m); })).then(function (rs) {
      var rows = months.map(function (m, i) {
        var r = rs[i], b = null;
        if (r && r.available && r.days) Object.keys(r.days).forEach(function (k) { var x = r.days[k]; if (x && x.price && (!b || x.price < b.price)) b = { price: x.price, dep: k, ret: x.ret, cur: r.currency }; });
        return { m: m, b: b };
      });
      var got = rows.filter(function (r) { return r.b; });
      if (!got.length) { box.innerHTML = '<p class="mm-wait">' + T.none + "</p>"; return; }
      var max = Math.max.apply(null, got.map(function (r) { return r.b.price; }));
      var best = got.reduce(function (a, r) { return r.b.price < a.b.price ? r : a; });
      var dear = got.reduce(function (a, r) { return r.b.price > a.b.price ? r : a; });
      var link = function (r) { return "/recherche/?flightSearch=" + from + ddmm(r.b.dep) + to + (r.b.ret ? ddmm(r.b.ret) : "") + "1"; };
      box.innerHTML = '<ol class="mm-bars">' + rows.map(function (r) {
        if (!r.b) return '<li class="mm-empty"><span class="mm-bar" style="--h:6%"></span><b>–</b><small>' + mshort(r.m) + "</small></li>";
        var h = Math.max(12, Math.round(r.b.price / max * 100));
        return '<li class="' + (r === best ? "mm-best" : "") + '"><a href="' + link(r) + '" aria-label="' + mname(r.m) + " : " + money(r.b.price, r.b.cur) + '"><span class="mm-bar" style="--h:' + h + '%"></span><b>' + money(r.b.price, r.b.cur) + "</b><small>" + mshort(r.m) + "</small></a></li>";
      }).join("") + "</ol>";
      var s = document.getElementById("mm-summary");
      if (s) {
        s.innerHTML = "<p><strong></strong></p><p></p>";
        s.firstChild.firstChild.textContent = T.best.replace("{m}", mname(best.m)).replace("{p}", money(best.b.price, best.b.cur));
        s.lastChild.textContent = got.length > 1 && dear !== best ? T.dear.replace("{m}", mname(dear.m)).replace("{p}", money(dear.b.price, dear.b.cur)) : "";
        var go = document.getElementById("mm-go"); if (go) { go.href = link(best); go.hidden = false; }
      }
    });
  });
})();
