// « Ce billet est-il vrai ? » : compare un prix proposé (agent, WhatsApp, réseaux sociaux) avec les vrais prix
// trouvés récemment pour le même trajet et le même mois (/api/calendar, converti en euros via /api/fx).
(function () {
  "use strict";
  var f = document.getElementById("ar-form");
  if (!f || !window.EscaleAC) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2), loc = lang === "fr" ? "fr-FR" : "en-GB";
  var T = JSON.parse(f.getAttribute("data-t")), out = document.getElementById("ar-out");
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var eur = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var from = window.EscaleAC.attach(f.querySelector("#ar-from")); window.EscaleAC.attach(f.querySelector("#ar-to"));
  if (window.ESCALE_FETE_FROM) window.ESCALE_FETE_FROM.then(function (x) { window.EscaleAC.ready.then(function () { if (!f.querySelector("#ar-from").value) from.set(x.code === "CDG" ? "PAR" : x.code); }); });
  var fx = get("/api/fx?all=1");
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var a = f.querySelector("#ar-from").dataset.code, b = f.querySelector("#ar-to").dataset.code, mo = f.querySelector("#ar-month").value;
    var price = Number(f.querySelector("#ar-price").value), cur = f.querySelector("#ar-cur").value;
    if (!a || !b || a === b || !/^\d{4}-\d{2}$/.test(mo) || !(price > 0)) { out.innerHTML = '<p class="tc-err">' + esc(T.err) + "</p>"; return; }
    out.innerHTML = '<p class="pr-wait">' + esc(T.loading) + "</p>";
    Promise.all([fx, get("/api/calendar?from=" + a + "&to=" + b + "&month=" + mo)]).then(function (r) {
      var rates = r[0] && r[0].rates || { EUR: 1 }, cal = r[1], days = cal && cal.available && cal.days ? cal.days : {};
      var p = price / (cur === "EUR" ? 1 : (rates[cur] || NaN));
      var vals = Object.keys(days).map(function (k) { return days[k].price; }).sort(function (x, y) { return x - y; });
      if (!(p > 0) || !vals.length) { out.innerHTML = '<p class="tc-err">' + esc(T.none) + "</p>"; return; }
      var min = vals[0], ratio = p / min;
      var v = ratio < 0.6 ? ["bad", T.v_bad] : ratio < 0.9 ? ["mid", T.v_mid] : ["good", T.v_good];
      out.innerHTML = '<div class="tc-res tc-' + v[0] + '"><p class="tc-v">' + esc(v[1]) + "</p>" +
        "<ul><li>" + esc(T.l_offer.replace("{p}", eur(p))) + "</li><li>" + esc(T.l_min.replace("{p}", eur(min))) + "</li></ul>" +
        '<p class="tc-diff">' + esc(v[0] === "bad" ? T.t_bad : v[0] === "mid" ? T.t_mid : T.t_good) + "</p>" +
        '<p class="small">' + esc(T.note) + "</p></div>";
    });
  });
})();
