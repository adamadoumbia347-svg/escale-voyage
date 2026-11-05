// Départ du visiteur pour les pages des fêtes : l'aéroport choisi sur Escale (« escale.from »), sinon le plus proche
// d'après sa position approximative (/api/geo), sinon Paris. Les deux blocs ci-dessous l'attendent (window.ESCALE_FETE_FROM).
(function () {
  "use strict";
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var paris = { code: "CDG", name: null };
  var stored = null; try { stored = ((localStorage.getItem("escale.from.m") ? localStorage.getItem("escale.from") : "") || "").match(/^(.*?)\s*\(([A-Z]{3})\)$/); } catch (e) {}
  var names = lang === "fr" ? Promise.resolve({}) : get("/data/noms/" + lang + ".json").then(function (m) { return m || {}; });
  var pick = function (db, lat, lon, cc) {
    var rad = Math.PI / 180, best = null, bd = 1e9, home = null, hd = 1e9;
    (db || []).forEach(function (a) {
      if (!a[4] || a[5] == null) return;
      var dl = (a[5] - lat) * rad, dn = (a[6] - lon) * rad, h = Math.pow(Math.sin(dl / 2), 2) + Math.cos(lat * rad) * Math.cos(a[5] * rad) * Math.pow(Math.sin(dn / 2), 2), d = 12742 * Math.asin(Math.sqrt(h));
      if (d < bd) { bd = d; best = a; } if (cc && a[3] === cc && d < hd) { hd = d; home = a; }
    });
    return home && hd < 250 ? home : bd < 400 ? best : null;
  };
  window.ESCALE_FETE_FROM = (stored ? Promise.resolve({ code: stored[2], name: stored[1] }) : get("/api/geo").then(function (g) {
    if (!g || g.lat == null) return paris;
    return get("/data/airports.json").then(function (db) { var a = pick(db, g.lat, g.lon, g.country); return a ? { code: a[0], name: a[1] } : paris; });
  })).then(function (f) {
    if (/^(CDG|ORY|BVA|PAR)$/.test(f.code)) return paris;  // Paris : la page est déjà prête
    return names.then(function (m) { return { code: f.code, name: (m && m[f.code]) || f.name }; });
  }).catch(function () { return paris; });
})();

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
  window.ESCALE_FETE_FROM.then(function (f) {
  if (f.name) {
    // Titre du tableau et lignes : depuis la ville du visiteur (le lien « Alerte prix » mène à une page Paris : retiré)
    var h = t.parentNode.querySelector("h2"); if (h) h.textContent = h.textContent.replace(/Paris|París|باريس/, f.name);
    t.querySelectorAll("tbody tr").forEach(function (tr) {
      if (tr.getAttribute("data-to") === f.code) { tr.remove(); return; }
      tr.setAttribute("data-from", f.code);
      var b = tr.querySelector("th bdi"); if (b) b.textContent = b.textContent.replace(/^.*?(\s→\s)/, f.name + "$1");
      var go = tr.querySelector(".price-go"); if (go) go.href = go.getAttribute("href").replace(/from=[A-Z]{3}/, "from=" + f.code);
      var al = tr.querySelector(".fete-alert"); if (al) al.remove();
    });
  }
  t.querySelectorAll("tbody tr").forEach(function (tr) {
    var cell = tr.querySelector(".fp");
    var url = "/api/prix?from=" + tr.getAttribute("data-from") + "&to=" + tr.getAttribute("data-to") + "&dep=" + dep + "&ret=" + ret + "&currency=EUR";
    fetch(url).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (d) {
      if (d && d.available && d.price) { cell.innerHTML = "<strong></strong>"; cell.firstChild.textContent = label + " " + money(d.price, d.currency); }
      else cell.textContent = none;
    });
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
  window.ESCALE_FETE_FROM.then(function (f) {
  var start = box.getAttribute("data-start"), end = box.getAttribute("data-end"), ref = box.getAttribute("data-ref"), from = f.code;
  var names = JSON.parse(box.getAttribute("data-names") || "{}"), L = JSON.parse(box.getAttribute("data-t") || "[]");
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { weekday: "short", day: "numeric", month: "short" }); } catch (e) { return s; } };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var months = [start.slice(0, 7)]; if (end.slice(0, 7) !== months[0]) months.push(end.slice(0, 7));
  var tpl = box.querySelector("[data-tpl]");
  tpl.textContent = tpl.getAttribute("data-tpl").replace("{a}", day(start)).replace("{b}", day(end)).replace("{c}", day(ref));
  var list = box.querySelector(".bd-list"), shown = 0;
  (box.getAttribute("data-routes") || "").split(",").filter(function (x) { return x && x !== from; }).forEach(function (to) {
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
  });
})();
