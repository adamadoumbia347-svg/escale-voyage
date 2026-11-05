// « As-tu payé ton billet trop cher ? » : compare le prix payé avec les vrais prix trouvés récemment
// (calendrier des prix /api/calendar : même jour de départ et meilleur jour du mois), convertis en euros (/api/fx).
(function () {
  "use strict";
  var f = document.getElementById("tc-form");
  if (!f || !window.EscaleAC) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2), loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "en-GB";
  var T = JSON.parse(f.getAttribute("data-t")), out = document.getElementById("tc-out");
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { day: "numeric", month: "long" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var from = window.EscaleAC.attach(f.querySelector("#tc-from")), to = window.EscaleAC.attach(f.querySelector("#tc-to"));
  if (window.ESCALE_FETE_FROM) window.ESCALE_FETE_FROM.then(function (x) { window.EscaleAC.ready.then(function () { if (!f.querySelector("#tc-from").value) from.set(x.code === "CDG" ? "PAR" : x.code); }); });
  var fx = get("/api/fx?all=1");
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var a = f.querySelector("#tc-from").dataset.code, b = f.querySelector("#tc-to").dataset.code, dep = f.querySelector("#tc-dep").value, paid = Number(f.querySelector("#tc-paid").value), cur = f.querySelector("#tc-cur").value;
    var pax = Math.max(1, Number(f.querySelector("#tc-pax").value) || 1);
    if (!a || !b || a === b || !/^\d{4}-\d{2}-\d{2}$/.test(dep) || !(paid > 0)) { out.innerHTML = '<p class="tc-err">' + esc(T.err) + "</p>"; return; }
    out.innerHTML = '<p class="pr-wait">' + esc(T.loading) + "</p>";
    Promise.all([fx, get("/api/calendar?from=" + a + "&to=" + b + "&month=" + dep.slice(0, 7))]).then(function (r) {
      var rates = r[0] && r[0].rates || { EUR: 1 }, cal = r[1];
      var per = (paid / pax) / (cur === "EUR" ? 1 : (rates[cur] || NaN));
      if (!(per > 0)) { out.innerHTML = '<p class="tc-err">' + esc(T.err) + "</p>"; return; }
      var days = cal && cal.available && cal.days ? cal.days : {};
      var same = days[dep] ? days[dep].price : null, best = null;
      Object.keys(days).forEach(function (k) { if (!best || days[k].price < best.p) best = { p: days[k].price, d: k, r: days[k].ret }; });
      if (!same && !best) { out.innerHTML = '<p class="tc-err">' + esc(T.none) + "</p>"; return; }
      var ref = same || best.p, diff = Math.round(per - ref), pct = ref ? diff / ref : 0;
      var v = pct <= 0.05 ? ["good", T.v_good] : pct <= 0.2 ? ["mid", T.v_mid] : ["bad", T.v_bad];
      var lines = (same ? "<li>" + esc(T.l_same.replace("{d}", day(dep)).replace("{p}", money(same))) + "</li>" : "") +
        (best ? "<li>" + esc(T.l_best.replace("{d}", day(best.d)).replace("{p}", money(best.p))) + "</li>" : "") +
        "<li>" + esc(T.l_paid.replace("{p}", money(per))) + "</li>";
      var msg = (diff > 0 ? T.share_bad.replace("{x}", money(diff)) : T.share_good) + " " + location.origin + location.pathname;
      out.innerHTML = '<div class="tc-res tc-' + v[0] + '"><p class="tc-v">' + esc(v[1]) + "</p>" +
        '<p class="tc-diff">' + esc(diff > 0 ? T.more.replace("{x}", money(diff)) : T.less.replace("{x}", money(-diff))) + "</p><ul>" + lines + "</ul>" +
        '<div class="pr-btns"><a class="btn wa-btn" target="_blank" rel="noopener" href="https://wa.me/?text=' + encodeURIComponent(msg) + '">📲 ' + esc(T.share) + "</a>" +
        (best ? '<a class="btn ghost" href="/recherche/?flightSearch=' + a + ddmm(best.d) + b + (best.r ? ddmm(best.r) : "") + '1">' + esc(T.see) + "</a>" : "") + "</div>" +
        '<p class="small">' + esc(T.note) + "</p></div>";
      var box = document.getElementById("price-alert"); if (box) { box.setAttribute("data-from", a); box.setAttribute("data-to", b); }
    });
  });
})();
