// « Acheter maintenant ou attendre ? » : verdict des grands trajets du baromètre (/api/verdict) : dernier prix relevé
// comparé à la médiane des 60 derniers jours, avec une mini-courbe des 45 derniers relevés.
(function () {
  "use strict";
  var box = document.getElementById("aa-list");
  if (!box) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2), loc = lang === "fr" ? "fr-FR" : "en-GB";
  var T = JSON.parse(box.getAttribute("data-t"));
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var spark = function (s) {
    if (!s || s.length < 2) return "";
    var mn = Math.min.apply(null, s), mx = Math.max.apply(null, s), w = 120, h = 34;
    var pts = s.map(function (v, i) { return (i / (s.length - 1) * w).toFixed(1) + "," + (mx === mn ? h / 2 : h - (v - mn) / (mx - mn) * h).toFixed(1); }).join(" ");
    return '<svg class="aa-spark" viewBox="0 0 ' + w + " " + h + '" aria-hidden="true"><polyline points="' + pts + '" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/></svg>';
  };
  var filter = document.getElementById("aa-filter");
  fetch("/api/verdict").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (d) {
    var items = d && d.items || [];
    if (!items.length) { box.innerHTML = '<li class="pr-wait">' + esc(T.none) + "</li>"; return; }
    var order = { low: 0, mid: 1, high: 2 };
    items.sort(function (a, b) { return (order[a.level] == null ? 3 : order[a.level]) - (order[b.level] == null ? 3 : order[b.level]); });
    var render = function () {
      var q = (filter && filter.value || "").toLowerCase();
      box.innerHTML = items.filter(function (it) { return !q || it.label.toLowerCase().indexOf(q) >= 0; }).map(function (it) {
        var lv = it.level || "na", lab = it.level ? T[it.level] : T.na;
        var txt = it.level === "low" ? T.lowTxt : it.level === "high" ? T.highTxt : it.level === "mid" ? T.midTxt : T.naTxt;
        txt = txt.replace("{x}", it.diff == null ? "" : it.diff).replace("{avg}", it.median ? money(it.median) : "").replace("{n}", it.days || "");
        return '<li class="aa-item aa-' + lv + '"><a href="/' + esc(it.path) + '/"><span class="aa-top"><strong>' + esc(it.label) + '</strong><span class="aa-badge">' + esc(lab) + "</span></span>" +
          '<span class="aa-mid"><b>' + esc(T.from + " " + money(it.price)) + "</b>" + spark(it.series) + "</span><small>" + esc(txt) + "</small></a></li>";
      }).join("");
    };
    render(); if (filter) filter.addEventListener("input", render);
  });
})();
