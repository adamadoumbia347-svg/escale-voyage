// Page « Destinations tendance 2027 » : meilleur aller-retour des deux prochains mois depuis l'aéroport du visiteur
// (window.ESCALE_FETE_FROM, voir fetes.js), via le calendrier des prix (/api/calendar). Aucun prix n'est écrit dans la page.
(function () {
  "use strict";
  var cfg = document.getElementById("tr-cfg");
  if (!cfg || !window.ESCALE_FETE_FROM) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB" }[lang] || "fr-FR";
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var money = function (n, cur) {
    try { return new Intl.NumberFormat(loc, { style: "currency", currency: cur || "EUR", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " " + (cur || "EUR"); }
  };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { day: "numeric", month: "short" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var months = (function () { var d = new Date(), out = []; for (var i = 1; i <= 2; i++) { var m = new Date(d.getFullYear(), d.getMonth() + i, 1); out.push(m.getFullYear() + "-" + ("0" + (m.getMonth() + 1)).slice(-2)); } return out; })();
  var best = function (from, to) {
    return Promise.all(months.map(function (m) { return get("/api/calendar?from=" + from + "&to=" + to + "&month=" + m); })).then(function (rs) {
      var b = null;
      rs.forEach(function (r) {
        if (!r || !r.available || !r.days) return;
        Object.keys(r.days).forEach(function (k) { var x = r.days[k]; if (x && x.price && (!b || x.price < b.price)) b = { price: x.price, dep: k, ret: x.ret, cur: r.currency, to: to }; });
      });
      return b;
    });
  };
  var cards = [].slice.call(document.querySelectorAll(".tr-card[data-to]"));
  cards.forEach(function (c) { var p = c.querySelector(".tr-price"); if (p) p.textContent = cfg.getAttribute("data-loading"); });
  window.ESCALE_FETE_FROM.then(function (f) {
    var from = f.code === "CDG" ? "PAR" : f.code;
    var fc = document.querySelector(".tr-from");
    if (fc) { fc.querySelector(".tr-from-city").textContent = f.name || "Paris"; fc.hidden = false; }
    var go = function (c) {
      var codes = c.getAttribute("data-to").split(","), p = c.querySelector(".tr-price"), a = c.querySelector(".tr-link");
      if (codes.indexOf(f.code) >= 0) { c.remove(); return; }
      a.href = a.getAttribute("href").replace(/([?&]type=vols)/, "$1&from=" + from);
      var tryNext = function (i) {
        if (i >= codes.length) { p.textContent = cfg.getAttribute("data-none"); return; }
        best(from, codes[i]).then(function (b) {
          if (!b) return tryNext(i + 1);
          p.innerHTML = "<b></b> <span></span>";
          p.firstChild.textContent = cfg.getAttribute("data-from") + " " + money(b.price, b.cur);
          p.lastChild.textContent = "· " + day(b.dep);
          a.href = "/recherche/?flightSearch=" + from + ddmm(b.dep) + b.to + (b.ret ? ddmm(b.ret) : "") + "1";
        });
      };
      tryNext(0);
    };
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); go(e.target); } }); }, { rootMargin: "300px" });
      cards.forEach(function (c) { io.observe(c); });
    } else cards.forEach(go);
  });
})();
