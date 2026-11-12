// Vol à plusieurs étapes (/vol-plusieurs-etapes/) : 2 à 4 allers simples enchaînés. Pour chaque étape, un lien vers la recherche en direct
// et le prix le plus bas repéré récemment pour ce mois (/api/prix, par personne), quand il est connu. Rien n'est gardé ni envoyé ailleurs.
(function () {
  "use strict";
  var f = document.getElementById("et-form"), out = document.getElementById("et-out"), more = document.getElementById("et-more");
  if (!f || !window.EscaleAC) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var T = ({
    fr: { loc: "fr-FR", leg: "Étape {i} : départ", to: "Arrivée", date: "Date", ph: "Ville ou aéroport", e1: "Étape {i} : choisissez le départ et l'arrivée dans la liste, puis une date.", e2: "Étape {i} : le départ et l'arrivée sont identiques.",
      e3: "Étape {i} : la date est avant celle de l'étape précédente.", e4: "Saisissez au moins deux étapes.", h: "Vos {n} recherches", ow: "aller simple", wait: "Recherche du prix repéré…", cmp: "Comparer",
      from: "repéré dès <strong>{p} €</strong> ce mois-là", none: "Pas de prix repéré récemment : ouvrez la recherche.", total: "Total repéré pour les {n} étapes : <strong>dès {p} €</strong> par personne",
      note: "Prix les plus bas repérés récemment pour le mois de chaque étape, par personne : le tarif exact dépend du jour et se confirme en ouvrant la recherche. Billets séparés : gardez une marge large entre deux étapes." },
    en: { loc: "en-GB", leg: "Leg {i}: from", to: "To", date: "Date", ph: "City or airport", e1: "Leg {i}: pick the departure and arrival from the list, then a date.", e2: "Leg {i}: departure and arrival are the same.",
      e3: "Leg {i}: the date is before the previous leg.", e4: "Enter at least two legs.", h: "Your {n} searches", ow: "one way", wait: "Looking for the spotted price…", cmp: "Compare",
      from: "spotted from <strong>€{p}</strong> that month", none: "No price spotted recently: open the search.", total: "Total spotted for the {n} legs: <strong>from €{p}</strong> per person",
      note: "Lowest prices recently spotted for the month of each leg, per person: the exact fare depends on the day and is confirmed when you open the search. Separate tickets: leave a wide margin between two legs." },
    it: { loc: "it-IT", leg: "Tappa {i}: partenza", to: "Arrivo", date: "Data", ph: "Città o aeroporto", e1: "Tappa {i}: scegli partenza e arrivo dall'elenco, poi una data.", e2: "Tappa {i}: partenza e arrivo sono uguali.",
      e3: "Tappa {i}: la data è prima di quella della tappa precedente.", e4: "Inserisci almeno due tappe.", h: "Le tue {n} ricerche", ow: "sola andata", wait: "Ricerca del prezzo rilevato…", cmp: "Confronta",
      from: "rilevato da <strong>{p} €</strong> quel mese", none: "Nessun prezzo rilevato di recente: apri la ricerca.", total: "Totale rilevato per le {n} tappe: <strong>da {p} €</strong> a persona",
      note: "Prezzi più bassi rilevati di recente per il mese di ogni tappa, a persona: la tariffa esatta dipende dal giorno e si conferma aprendo la ricerca. Biglietti separati: tieni un margine ampio tra due tappe." }
  })[lang] || null;
  if (!T) return;
  var R = function (t, o) { return t.replace(/\{(\w)\}/g, function (_, k) { return o[k]; }); };
  var msg = document.getElementById("et-msg"), MAX = 4;
  var esc = function (t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var ddmm = function (d) { return d.slice(8, 10) + d.slice(5, 7); };
  var jour = function (d) { try { return new Date(d + "T12:00:00").toLocaleDateString(T.loc, { weekday: "short", day: "numeric", month: "long" }); } catch (e) { return d; } };
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
    d.innerHTML = '<div class="tool-grid"><label><span>' + esc(R(T.leg, { i: n + 1 })) + '</span><input class="et-from" placeholder="' + esc(T.ph) + '" autocomplete="off"></label>' +
      '<label><span>' + esc(T.to) + '</span><input class="et-to" placeholder="' + esc(T.ph) + '" autocomplete="off"></label><label><span>' + esc(T.date) + '</span><input class="et-date" type="date"></label></div>';
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
      if (!a || !b || !d) { bad = bad || R(T.e1, { i: i + 1 }); return; }
      if (a === b) { bad = bad || R(T.e2, { i: i + 1 }); return; }
      if (legs.length && d < legs[legs.length - 1].d) { bad = bad || R(T.e3, { i: i + 1 }); return; }
      legs.push({ a: a, b: b, d: d });
    });
    if (bad || legs.length < 2) { msg.textContent = bad || T.e4; out.innerHTML = ""; return; }
    msg.textContent = "";
    var N = window.EscaleAC.name;
    out.innerHTML = '<h3>' + esc(R(T.h, { n: legs.length })) + '</h3><ol class="et-list">' + legs.map(function (l, i) {
      return '<li><div><strong>' + esc(N(l.a)) + " → " + esc(N(l.b)) + '</strong><span class="small">' + esc(jour(l.d)) + ' · ' + esc(T.ow) + '</span><span class="et-prix small" data-i="' + i + '">' + esc(T.wait) + '</span></div>' +
        '<a class="btn" href="/recherche/?flightSearch=' + l.a + ddmm(l.d) + l.b + pax + '" target="_blank" rel="noopener">' + esc(T.cmp) + '</a></li>';
    }).join("") + '</ol><p id="et-total" class="et-total" hidden></p>' +
      '<p class="small">' + esc(T.note) + '</p>';
    out.scrollIntoView({ behavior: "smooth", block: "start" });
    var prix = new Array(legs.length), reste = legs.length;
    legs.forEach(function (l, i) {
      fetch("/api/prix?from=" + l.a + "&to=" + l.b + "&dep=" + l.d + "&currency=EUR").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (j) {
        var el = out.querySelector('.et-prix[data-i="' + i + '"]'), p = j && j.available && j.price;
        if (p && (!j.currency || j.currency === "EUR")) { prix[i] = p; el.innerHTML = R(T.from, { p: Math.round(p).toLocaleString(T.loc) }); }
        else el.textContent = T.none;
        if (--reste === 0 && prix.filter(Boolean).length === legs.length) {
          var t = prix.reduce(function (s, x) { return s + x; }, 0), box = document.getElementById("et-total");
          box.hidden = false; box.innerHTML = R(T.total, { n: legs.length, p: Math.round(t).toLocaleString(T.loc) });
        }
      });
    });
  });
})();
