/* « Que visiter » : comparer deux pays côte à côte (prix du vol depuis la ville du visiteur, lieux à voir).
   Les prix viennent de /api/ruban (aller-retour le plus bas repéré récemment) ; sans prix repéré, rien n'est affiché. Dépend de visiter.js (window.VX). */
(function () {
  "use strict";
  var VX = window.VX, out = document.getElementById("vx-cmp"), A = document.getElementById("vc-a"), B = document.getElementById("vc-b"), F = document.getElementById("vc-from"); if (!VX || !out || !A || !B || !F) return;
  var T = { fr: { des: "{v} dès {p}", ar: "aller-retour", sans: "Pas de prix repéré pour l'instant", choisir: "Écrivez votre ville ou votre aéroport de départ pour voir les prix.", lieux: "{n} lieux à voir", voir: "Voir le pays", vols: "Voir les vols", moins: "Le moins cher" },
    en: { des: "{v} from {p}", ar: "return", sans: "No price spotted yet", choisir: "Type your departure city or airport to see prices.", lieux: "{n} places to see", voir: "See the country", vols: "See flights", moins: "Cheapest" },
    it: { des: "{v} da {p}", ar: "andata e ritorno", sans: "Nessun prezzo rilevato per ora", choisir: "Scrivi la tua città o il tuo aeroporto di partenza per vedere i prezzi.", lieux: "{n} luoghi da vedere", voir: "Vedi il paese", vols: "Vedi i voli", moins: "Il meno caro" } }[VX.lang];
  var e = VX.esc, pays = {}, P = {}, dep = ""; // dep : code de la ville ou de l'aéroport écrit par le visiteur
  var q = new URLSearchParams(location.search);
  var col = function (p, autre) {
    var x = P[p.cc], y = autre && P[autre.cc], moins = x && y && x.price < y.price;
    return '<article class="vc-col"><div class="vc-ph"><img src="/img/visiter/' + e(p.lieux[0].k) + '-640.webp" alt="" width="640" height="427" loading="lazy">' + (moins ? '<span class="vc-badge">' + e(T.moins) + "</span>" : "") + "</div>" +
      "<h2>" + p.flag + " " + e(p.nom) + '</h2><p class="vc-prix">' + (x && x.price > 0 ? "<strong>" + e(VX.fmt(T.des, { v: p.ville, p: VX.money(x.price) })) + "</strong> " + e(T.ar) + (x.ret ? "<br><small>" + e(VX.jour(x.dep)) + " → " + e(VX.jour(x.ret)) + "</small>" : "")
        : "<small>" + e(dep ? T.sans : T.choisir) + "</small>") + '</p><p class="vc-n">' + e(VX.fmt(T.lieux, { n: p.lieux.length })) + "</p><ul>" +
      p.lieux.map(function (l) { return '<li><a href="' + e(VX.base + p.slug + "/#" + l.k) + '">' + e(l.n) + "</a></li>"; }).join("") + '</ul><p class="vc-btn"><a class="btn" href="' + e(VX.base + p.slug + "/") + '">' + e(T.voir) +
      '</a><a class="btn ghost" href="' + e(VX.lienVols(dep || "PAR", p.air, x)) + '">' + e(T.vols) + "</a></p></article>";
  };
  var rendre = function () {
    var a = pays[A.value], b = pays[B.value]; if (!a || !b) return;
    out.innerHTML = col(a, b) + col(b, a);
    try { history.replaceState(null, "", location.pathname + "?a=" + a.cc + "&b=" + b.cc); } catch (err) {}
  };
  var prix = function () { if (!dep) { P = {}; return rendre(); } var d0 = dep; VX.prix(dep).then(function (x) { if (dep !== d0) return; P = x; rendre(); }); };
  VX.data().then(function (d) {
    d.pays.forEach(function (p) { pays[p.cc] = p; });
    var a = pays[q.get("a")] ? q.get("a") : d.pays[0].cc, b = pays[q.get("b")] && q.get("b") !== a ? q.get("b") : (d.pays.filter(function (p) { return p.cc !== a; })[0] || d.pays[0]).cc;
    A.value = a; B.value = b; rendre();
    var der = VX.dernierDepart(); if (der) { F.value = der[1] + " (" + der[0] + ")"; F.dataset.code = der[0]; dep = der[0]; prix(); }
  });
  A.addEventListener("change", rendre); B.addEventListener("change", rendre);
  VX.champDepart(F, function (code) { dep = code; prix(); });
})();
