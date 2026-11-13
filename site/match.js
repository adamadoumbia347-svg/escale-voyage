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

  // ---- Départ écrit par le visiteur : son aéroport entre dans le match avec le prix le plus bas des six prochains mois
  // (/api/calendar, la même définition que les relevés des trajets suivis). Sans prix repéré, on le dit, sans rien inventer.
  var lget = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, lset = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
  var inp = document.getElementById("mh-from"), msg = document.getElementById("mh-me"), dep = "", depNom = "", mine = {};
  var VILLE = { PAR: ["CDG", "ORY"], MIL: ["MXP", "LIN", "BGY"], ROM: ["FCO", "CIA"], LON: ["LHR", "LGW", "STN", "LTN"] }; // code de ville → aéroports suivis
  var meme = function (a, b) { return a === b || (VILLE[a] && VILLE[a].indexOf(b) >= 0) || (VILLE[b] && VILLE[b].indexOf(a) >= 0); };
  var pad = function (n) { return String(n).padStart(2, "0"); };
  function monPrix(from, to) {
    var k = from + "-" + to;
    if (!mine[k]) {
      var now = new Date(), today = now.getFullYear() + "-" + pad(now.getMonth() + 1) + "-" + pad(now.getDate()), mois = [];
      for (var i = 0; i < 6; i++) { var d = new Date(now.getFullYear(), now.getMonth() + i, 1); mois.push(d.getFullYear() + "-" + pad(d.getMonth() + 1)); }
      mine[k] = Promise.all(mois.map(function (m) { return fetch("/api/calendar?from=" + from + "&to=" + to + "&month=" + m).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); }))
        .then(function (all) {
          var best = null;
          all.forEach(function (d) { if (!d || !d.available) return; Object.keys(d.days || {}).forEach(function (day) { var x = d.days[day];
            if (day >= today && x.price > 0 && d.currency === "EUR" && (!best || x.price < best.price)) best = { price: Math.round(x.price), dep: day, ret: x.ret }; }); });
          return best;
        });
    }
    return mine[k];
  }

  function show(to) {
    var g = groups[to];
    if (!g) return;
    current = to;
    Array.prototype.forEach.call(chips.querySelectorAll("button"), function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-to") === to)); });
    paint(to, null);
    if (msg) msg.textContent = "";
    if (!dep || meme(dep, to)) return;
    if (g.rows.some(function (r) { return meme(dep, r.from); })) return; // déjà dans le classement : la ligne est marquée « Votre départ »
    var d0 = dep, n0 = depNom;
    if (msg) msg.textContent = "Recherche du prix depuis " + n0 + "…";
    monPrix(d0, to).then(function (best) {
      if (current !== to || dep !== d0) return;
      if (!best) { if (msg) msg.innerHTML = "Pas de prix repéré depuis " + esc(n0) + " vers " + esc(g.name) + " pour l’instant. <a rel=\"nofollow\" href=\"/?type=vols&amp;from=" + d0 + "&amp;to=" + to + "\">Lancer la recherche</a>"; return; }
      if (msg) msg.textContent = "";
      paint(to, { from: d0, city: n0, price: best.price, href: "/?type=vols&from=" + d0 + "&to=" + to + "&dep=" + best.dep + (best.ret ? "&ret=" + best.ret : "") });
    });
  }

  function paint(to, extra) {
    var g = groups[to];
    var rows = g.rows.concat(extra ? [extra] : []).sort(function (a, b) { return a.price - b.price; });
    var min = rows[0].price, max = rows[rows.length - 1].price;
    var html = '<ol class="mh-list">' + rows.map(function (r, i) {
      var w = Math.round(28 + 72 * (max > min ? (r.price - min) / (max - min) : 0));
      var diff = r.price - min, moi = !!dep && (r === extra || meme(dep, r.from));
      return '<li class="mh-row' + (i === 0 ? " mh-win" : "") + (moi ? " mh-me" : "") + '"><a ' + (r.href ? 'rel="nofollow" href="' + esc(r.href) + '"' : 'href="/' + esc(r.path) + '/"') + ">" +
        '<span class="mh-rank" aria-hidden="true">' + (i === 0 ? "🏆" : i + 1) + "</span>" +
        '<span class="mh-main"><strong>' + esc(r.city) + (moi ? ' <em class="mh-tag">Votre départ</em>' : "") + '</strong><span class="mh-bar"><i style="width:' + w + '%"></i></span>' +
        "<small>" + (i === 0 ? "Vainqueur du match" : "+ " + esc(money(diff)) + " par rapport à " + esc(rows[0].city)) + "</small></span>" +
        '<b class="mh-price">' + esc(money(r.price)) + "</b></a></li>";
    }).join("") + "</ol>";
    if (rows.length > 1 && max > min) {
      html = '<p class="mh-sum">Pour <strong>' + esc(g.name) + "</strong>, partir de <strong>" + esc(rows[0].city) + "</strong> coûte <strong>" + esc(money(max - min)) +
        "</strong> de moins que de " + esc(rows[rows.length - 1].city) + ".</p>" + html;
    }
    box.innerHTML = html;
    var last = g.rows.map(function (r) { return r.date; }).sort().pop();
    if (note && dateEl && last) { dateEl.textContent = day(last); note.hidden = false; }
    if (share) share.hidden = false;
    try { history.replaceState(null, "", "?to=" + to); } catch (e) { /* sans importance */ }
  }

  // Champ « Je pars de » : suggestions de site/ac-mini.js, chargé au premier toucher ; le choix reste dans l'appareil
  if (inp) {
    var partir = function (code, nom) { dep = code || ""; depNom = nom || ""; if (current) show(current); };
    var acP = null, ac = function () {
      if (acP) return;
      acP = new Promise(function (ok) { if (window.EscaleAC) return ok(); var sc = document.createElement("script"); sc.src = "/ac-mini.js"; sc.onload = ok; sc.onerror = ok; document.head.appendChild(sc); })
        .then(function () { return window.EscaleAC ? window.EscaleAC.ready : null; }).then(function () {
          if (!window.EscaleAC) return;
          var actif = document.activeElement === inp; // attach déplace le champ : il perdrait la saisie en cours
          window.EscaleAC.attach(inp, function (code, nom) { lset("escale.aeroport", code + "|" + nom); partir(code, nom); });
          if (actif) { inp.focus(); try { inp.setSelectionRange(inp.value.length, inp.value.length); } catch (e) {} }
          if (inp.value.trim().length >= 2 && !inp.dataset.code) inp.dispatchEvent(new Event("input"));
        });
    };
    inp.addEventListener("focus", ac); inp.addEventListener("input", function () { ac(); if (!inp.value.trim()) partir("", ""); });
    var m = (lget("escale.aeroport") || "").split("|");
    if (/^[A-Z]{3}$/.test(m[0]) && m[1]) { inp.value = m[1] + " (" + m[0] + ")"; inp.dataset.code = m[0]; dep = m[0]; depNom = m[1]; }
  }

  fetch("/api/verdict").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (d) {
    var items = (d && d.items) || [];
    items.forEach(function (it) {
      var parts = String(it.label).split(" → ");
      if (parts.length !== 2 || !(it.price > 0)) return;
      if (!groups[it.to]) { groups[it.to] = { name: parts[1], rows: [] }; order.push(it.to); }
      groups[it.to].rows.push({ from: it.from, city: parts[0], price: it.price, path: it.path, date: it.date });
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
