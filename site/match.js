// « Match des aéroports » : pour une destination, les villes de départ suivies classées du prix relevé le plus bas au plus haut.
// Données : /api/verdict (dernier relevé de chaque grand trajet). Aucun prix n'est écrit dans la page.
(function () {
  "use strict";
  var box = document.getElementById("mh-box"), chips = document.getElementById("mh-dest");
  if (!box || !chips) return;
  var note = document.getElementById("mh-note"), dateEl = document.getElementById("mh-date"), share = document.getElementById("mh-share");
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n) { try { return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" }); };
  var groups = {}, order = [], current = null;

  function show(to) {
    var g = groups[to];
    if (!g) return;
    current = to;
    Array.prototype.forEach.call(chips.querySelectorAll("button"), function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-to") === to)); });
    var rows = g.rows.slice().sort(function (a, b) { return a.price - b.price; });
    var min = rows[0].price, max = rows[rows.length - 1].price;
    var html = '<ol class="mh-list">' + rows.map(function (r, i) {
      var w = Math.round(28 + 72 * (max > min ? (r.price - min) / (max - min) : 0));
      var diff = r.price - min;
      return '<li class="mh-row' + (i === 0 ? " mh-win" : "") + '"><a href="/' + esc(r.path) + '/">' +
        '<span class="mh-rank" aria-hidden="true">' + (i === 0 ? "🏆" : i + 1) + "</span>" +
        '<span class="mh-main"><strong>' + esc(r.city) + '</strong><span class="mh-bar"><i style="width:' + w + '%"></i></span>' +
        "<small>" + (i === 0 ? "Vainqueur du match" : "+ " + esc(money(diff)) + " par rapport à " + esc(rows[0].city)) + "</small></span>" +
        '<b class="mh-price">' + esc(money(r.price)) + "</b></a></li>";
    }).join("") + "</ol>";
    if (rows.length > 1 && max > min) {
      html = '<p class="mh-sum">Pour <strong>' + esc(g.name) + "</strong>, partir de <strong>" + esc(rows[0].city) + "</strong> coûte <strong>" + esc(money(max - min)) +
        "</strong> de moins que de " + esc(rows[rows.length - 1].city) + ".</p>" + html;
    }
    box.innerHTML = html;
    var last = rows.map(function (r) { return r.date; }).sort().pop();
    if (note && dateEl && last) { dateEl.textContent = day(last); note.hidden = false; }
    if (share) share.hidden = false;
    try { history.replaceState(null, "", "?to=" + to); } catch (e) { /* sans importance */ }
  }

  fetch("/api/verdict").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (d) {
    var items = (d && d.items) || [];
    items.forEach(function (it) {
      var parts = String(it.label).split(" → ");
      if (parts.length !== 2 || !(it.price > 0)) return;
      if (!groups[it.to]) { groups[it.to] = { name: parts[1], rows: [] }; order.push(it.to); }
      groups[it.to].rows.push({ city: parts[0], price: it.price, path: it.path, date: it.date });
    });
    order = order.filter(function (to) { return groups[to].rows.length >= 2; }).sort(function (a, b) { return groups[b].rows.length - groups[a].rows.length; });
    if (!order.length) { box.innerHTML = '<p class="pr-wait">Les prix sont en cours de relevé : revenez dans quelques heures.</p>'; return; }
    chips.innerHTML = order.map(function (to) { return '<button type="button" data-to="' + esc(to) + '" aria-pressed="false">' + esc(groups[to].name) + "</button>"; }).join("");
    chips.addEventListener("click", function (ev) { var b = ev.target.closest("button[data-to]"); if (b) show(b.getAttribute("data-to")); });
    var want = (/[?&]to=([A-Z]{3})/.exec(location.search) || [])[1];
    show(groups[want] && order.indexOf(want) >= 0 ? want : (order.indexOf("DSS") >= 0 ? "DSS" : order[0]));
  });

  if (share) share.addEventListener("click", function () {
    var g = groups[current];
    if (!g) return;
    var url = "https://escale.live/match-des-aeroports/?to=" + current, text = "Match des aéroports pour " + g.name + " : de quelle ville partir pour payer moins cher ?";
    if (navigator.share) { navigator.share({ title: "Match des aéroports", text: text, url: url }).catch(function () {}); }
    else { window.open("https://wa.me/?text=" + encodeURIComponent(text + " " + url), "_blank", "noopener"); }
  });
})();
