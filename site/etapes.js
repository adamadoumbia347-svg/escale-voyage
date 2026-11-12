// Vol à plusieurs étapes (/vol-plusieurs-etapes/) : 2 à 4 allers simples enchaînés. Pour chaque étape, un lien vers la recherche en direct
// et le prix le plus bas repéré récemment pour ce mois (/api/prix, par personne), quand il est connu. Rien n'est gardé ni envoyé ailleurs.
(function () {
  "use strict";
  var f = document.getElementById("et-form"), out = document.getElementById("et-out"), more = document.getElementById("et-more");
  if (!f || !window.EscaleAC) return;
  var msg = document.getElementById("et-msg"), MAX = 4;
  var esc = function (t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var ddmm = function (d) { return d.slice(8, 10) + d.slice(5, 7); };
  var jour = function (d) { try { return new Date(d + "T12:00:00").toLocaleDateString("fr-FR", { weekday: "short", day: "numeric", month: "long" }); } catch (e) { return d; } };
  var rows = function () { return [].slice.call(f.querySelectorAll(".et-row")); };
  var today = new Date().toISOString().slice(0, 10);
  function wire(row) {
    var from = row.querySelector(".et-from"), to = row.querySelector(".et-to"), date = row.querySelector(".et-date");
    date.min = today;
    window.EscaleAC.attach(from);
    // L'arrivée choisie devient le départ de l'étape suivante, si celui-ci est encore vide
    window.EscaleAC.attach(to, function (code) {
      var all = rows(), nx = all[all.indexOf(row) + 1];
      if (nx) { var nf = nx.querySelector(".et-from"); if (!nf.dataset.code) { nf.value = to.value; nf.dataset.code = code; } }
    });
    date.addEventListener("change", function () { var all = rows(), nx = all[all.indexOf(row) + 1]; if (nx && date.value) nx.querySelector(".et-date").min = date.value; });
  }
  rows().forEach(wire);
  document.getElementById("et-add").addEventListener("click", function () {
    var n = rows().length; if (n >= MAX) return;
    var d = document.createElement("div"); d.className = "et-row"; d.dataset.i = String(n + 1);
    d.innerHTML = '<div class="tool-grid"><label><span>Étape ' + (n + 1) + ' : départ</span><input class="et-from" placeholder="Ville ou aéroport" autocomplete="off"></label>' +
      '<label><span>Arrivée</span><input class="et-to" placeholder="Ville ou aéroport" autocomplete="off"></label><label><span>Date</span><input class="et-date" type="date"></label></div>';
    more.appendChild(d); wire(d);
    var prev = rows()[n - 1], pt = prev.querySelector(".et-to");
    if (pt.dataset.code) { var nf = d.querySelector(".et-from"); nf.value = pt.value; nf.dataset.code = pt.dataset.code; }
    if (n + 1 >= MAX) this.hidden = true;
  });
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var pax = document.getElementById("et-pax").value || "1", legs = [], bad = "";
    rows().forEach(function (r, i) {
      var a = r.querySelector(".et-from").dataset.code, b = r.querySelector(".et-to").dataset.code, d = r.querySelector(".et-date").value;
      if (!a && !b && !d && i >= 2) return; // étape ajoutée puis laissée vide
      if (!a || !b || !d) { bad = bad || "Étape " + (i + 1) + " : choisissez le départ et l'arrivée dans la liste, puis une date."; return; }
      if (a === b) { bad = bad || "Étape " + (i + 1) + " : le départ et l'arrivée sont identiques."; return; }
      if (legs.length && d < legs[legs.length - 1].d) { bad = bad || "Étape " + (i + 1) + " : la date est avant celle de l'étape précédente."; return; }
      legs.push({ a: a, b: b, d: d });
    });
    if (bad || legs.length < 2) { msg.textContent = bad || "Saisissez au moins deux étapes."; out.innerHTML = ""; return; }
    msg.textContent = "";
    var N = window.EscaleAC.name;
    out.innerHTML = '<h3>Vos ' + legs.length + ' recherches</h3><ol class="et-list">' + legs.map(function (l, i) {
      return '<li><div><strong>' + esc(N(l.a)) + " → " + esc(N(l.b)) + '</strong><span class="small">' + esc(jour(l.d)) + ' · aller simple</span><span class="et-prix small" data-i="' + i + '">Recherche du prix repéré…</span></div>' +
        '<a class="btn" href="/recherche/?flightSearch=' + l.a + ddmm(l.d) + l.b + pax + '" target="_blank" rel="noopener">Comparer</a></li>';
    }).join("") + '</ol><p id="et-total" class="et-total" hidden></p>' +
      '<p class="small">Prix les plus bas repérés récemment pour le mois de chaque étape, par personne : le tarif exact dépend du jour et se confirme en ouvrant la recherche. Billets séparés : gardez une marge large entre deux étapes.</p>';
    out.scrollIntoView({ behavior: "smooth", block: "start" });
    var prix = new Array(legs.length), reste = legs.length;
    legs.forEach(function (l, i) {
      fetch("/api/prix?from=" + l.a + "&to=" + l.b + "&dep=" + l.d + "&currency=EUR").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (j) {
        var el = out.querySelector('.et-prix[data-i="' + i + '"]'), p = j && j.available && j.price;
        if (p && (!j.currency || j.currency === "EUR")) { prix[i] = p; el.innerHTML = "repéré dès <strong>" + Math.round(p).toLocaleString("fr-FR") + " €</strong> ce mois-là"; }
        else el.textContent = "Pas de prix repéré récemment : ouvrez la recherche.";
        if (--reste === 0 && prix.filter(Boolean).length === legs.length) {
          var t = prix.reduce(function (s, x) { return s + x; }, 0), box = document.getElementById("et-total");
          box.hidden = false; box.innerHTML = "Total repéré pour les " + legs.length + " étapes : <strong>dès " + Math.round(t).toLocaleString("fr-FR") + " €</strong> par personne";
        }
      });
    });
  });
})();
