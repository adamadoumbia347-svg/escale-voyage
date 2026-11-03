// Pages « Vols pour les fêtes » : prix aller-retour repérés pour les dates de la fête, trajet par trajet (/api/prix).
(function () {
  "use strict";
  var t = document.querySelector(".fete-table");
  if (!t) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn" }[lang] || "fr-FR";
  var dep = t.getAttribute("data-dep"), ret = t.getAttribute("data-ret");
  var label = t.getAttribute("data-from-label"), none = t.getAttribute("data-none");
  var money = function (n, cur) {
    try { return new Intl.NumberFormat(loc, { style: "currency", currency: cur || "EUR", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " " + (cur || "EUR"); }
  };
  t.querySelectorAll("tbody tr").forEach(function (tr) {
    var cell = tr.querySelector(".fp");
    var url = "/api/prix?from=" + tr.getAttribute("data-from") + "&to=" + tr.getAttribute("data-to") + "&dep=" + dep + "&ret=" + ret + "&currency=EUR";
    fetch(url).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (d) {
      if (d && d.available && d.price) { cell.innerHTML = "<strong></strong>"; cell.firstChild.textContent = label + " " + money(d.price, d.currency); }
      else cell.textContent = none;
    });
  });
})();

// « Le jour le moins cher pour partir » : calendrier des prix réels (/api/calendar) autour de la fête, comparé au jour le plus demandé
(function () {
  "use strict";
  var box = document.querySelector(".best-day");
  if (!box) return;
  var lang = box.getAttribute("data-lang") || "fr";
  var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn" }[lang] || "fr-FR";
  var start = box.getAttribute("data-start"), end = box.getAttribute("data-end"), ref = box.getAttribute("data-ref"), from = box.getAttribute("data-from");
  var names = JSON.parse(box.getAttribute("data-names") || "{}"), L = JSON.parse(box.getAttribute("data-t") || "[]");
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { weekday: "short", day: "numeric", month: "short" }); } catch (e) { return s; } };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var months = [start.slice(0, 7)]; if (end.slice(0, 7) !== months[0]) months.push(end.slice(0, 7));
  var tpl = box.querySelector("[data-tpl]");
  tpl.textContent = tpl.getAttribute("data-tpl").replace("{a}", day(start)).replace("{b}", day(end)).replace("{c}", day(ref));
  var list = box.querySelector(".bd-list"), shown = 0;
  (box.getAttribute("data-routes") || "").split(",").filter(Boolean).forEach(function (to) {
    Promise.all(months.map(function (m) {
      return fetch("/api/calendar?from=" + from + "&to=" + to + "&month=" + m + "&currency=EUR").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
    })).then(function (res) {
      var days = {};
      res.forEach(function (d) { if (d && d.available && d.days) Object.keys(d.days).forEach(function (k) { days[k] = d.days[k]; }); });
      var best = null;
      Object.keys(days).forEach(function (k) { if (k >= start && k <= end && (!best || days[k].price < days[best].price)) best = k; });
      if (!best) return;
      var b = days[best], r = days[ref], li = document.createElement("li");
      var href = "/recherche/?flightSearch=" + from + best.slice(8, 10) + best.slice(5, 7) + to + (b.ret ? b.ret.slice(8, 10) + b.ret.slice(5, 7) : "") + "1";
      var html = "<a href=\"" + esc(href) + "\"><strong>" + esc(names[to] || to) + "</strong></a>" + (lang === "fr" ? " : " : ": ") + esc(L[0]) + " " + esc(day(best)) +
        (b.ret ? " (" + esc(L[4]) + " " + esc(day(b.ret)) + ")" : "") + " · <strong>" + esc(money(b.price)) + "</strong>";
      if (r && best !== ref && r.price > b.price) html += " " + esc(L[1]) + " " + esc(money(r.price)) + ", " + esc(L[2]) + " <strong class=\"bd-save\">" + esc(money(r.price - b.price)) + " " + esc(L[3]) + "</strong>";
      li.innerHTML = html; list.appendChild(li); shown++;
      box.hidden = false;
    });
  });
})();
