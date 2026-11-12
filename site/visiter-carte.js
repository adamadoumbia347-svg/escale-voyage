/* « Que visiter » : carte du monde des pays (sommaire). Les points sont déjà dans la page (liens vers chaque pays) ;
   ce script ajoute le zoom par région, le prix du vol depuis la ville du visiteur et une fiche au toucher d'un point.
   Même projection que la carte « Partout » (site/partout.js, img/world.svg). Dépend de visiter.js (window.VX). */
(function () {
  "use strict";
  var VX = window.VX, map = document.getElementById("vx-map"); if (!VX || !map) return;
  var T = { fr: { voir: "Voir le pays", vols: "Voir les vols", des: "{v} : dès {p} aller-retour depuis {a}", sans: "Pas de prix repéré depuis {a} pour l'instant.", lieux: "{n} lieux à voir" },
    en: { voir: "See the country", vols: "See flights", des: "{v}: from {p} return from {a}", sans: "No price spotted from {a} yet.", lieux: "{n} places to see" },
    it: { voir: "Vedi il paese", vols: "Vedi i voli", des: "{v}: da {p} andata e ritorno da {a}", sans: "Nessun prezzo rilevato da {a} per ora.", lieux: "{n} luoghi da vedere" } }[VX.lang];
  var W = 2000, K = W / 360, TOP = 84, Hm = 789, inner = map.querySelector(".vx-map-in"), card = document.getElementById("vx-map-card");
  // lonMin, lonMax, latMin, latMax de chaque vue : monde, Afrique, Europe, Asie, Amériques
  var VUES = [[-128, 152, -42, 64], [-22, 54, -37, 39], [-13, 43, 32, 57], [24, 148, -13, 48], [-128, -30, -32, 52]], vue = 1;
  var cadrer = function () {
    var b = VUES[vue], cw = map.clientWidth, s = cw / ((b[1] - b[0]) * K), h = (b[3] - b[2]) * K * s, hmax = Math.min(520, Math.max(260, window.innerHeight * 0.72)), dx = 0;
    if (h > hmax) { s *= hmax / h; h = hmax; dx = (cw - (b[1] - b[0]) * K * s) / 2; } // vue trop haute : on réduit et on centre
    map.style.aspectRatio = "auto"; map.style.height = Math.round(h) + "px";
    inner.style.width = (W * s) + "px"; inner.style.height = (Hm * s) + "px";
    inner.style.transform = "translate(" + (dx - (b[0] + 180) * K * s).toFixed(1) + "px," + (-(TOP - b[3]) * K * s).toFixed(1) + "px)";
  };
  [].forEach.call(document.querySelectorAll(".vx-zoom button"), function (bt) {
    bt.addEventListener("click", function () {
      vue = +bt.dataset.z; [].forEach.call(document.querySelectorAll(".vx-zoom button"), function (o) { o.setAttribute("aria-pressed", o === bt ? "true" : "false"); });
      map.classList.add("anim"); cadrer();
    });
  });
  cadrer(); window.addEventListener("resize", cadrer);
  var P = {}, ville = "", pays = {};
  VX.data().then(function (d) { d.pays.forEach(function (p) { pays[p.cc] = p; }); });
  VX.depart(function (c) { ville = c; VX.prix(c).then(function (x) { P = x; [].forEach.call(map.querySelectorAll(".vx-pin"), function (a) { a.classList.toggle("has", !!P[a.dataset.cc]); }); }); });
  map.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".vx-pin"); if (!a) return;
    var p = pays[a.dataset.cc]; if (!p) return; // sans les données, le lien ouvre simplement la page du pays
    e.preventDefault();
    [].forEach.call(map.querySelectorAll(".vx-pin.on"), function (o) { o.classList.remove("on"); }); a.classList.add("on");
    var x = P[p.cc], nomV = VX.VILLES[ville] || "";
    card.innerHTML = '<img src="/img/visiter/' + VX.esc(p.lieux[0].k) + '-640.webp" alt="" width="96" height="96" loading="lazy"><div><h3>' + p.flag + " " + VX.esc(p.nom) + "</h3><p>" +
      (x && x.price > 0 ? "<strong>" + VX.esc(VX.fmt(T.des, { v: p.ville, p: VX.money(x.price), a: nomV })) + "</strong>" + (x.ret ? " (" + VX.esc(VX.jour(x.dep)) + " → " + VX.esc(VX.jour(x.ret)) + "). " : ". ") + VX.esc(VX.T.note)
        : (nomV ? VX.esc(VX.fmt(T.sans, { a: nomV })) : "")) + '</p><p class="small">' + VX.esc(VX.fmt(T.lieux, { n: p.lieux.length })) + " : " + VX.esc(p.lieux.slice(0, 4).map(function (l) { return l.n; }).join(", ")) + "…</p>" +
      '<p><a class="btn" href="' + a.getAttribute("href") + '">' + VX.esc(T.voir) + '</a> <a class="btn ghost" href="' + VX.esc(VX.lienVols(ville || "PAR", p.air, x)) + '">' + VX.esc(T.vols) + "</a></p></div>";
    card.classList.add("on");
  });
})();
