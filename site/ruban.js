/* Accueil : prix des vols dans le ruban de pays. Pour la ville de départ du visiteur, chaque pastille reçoit le prix
   aller-retour le plus bas repéré vers la grande ville du pays (/api/ruban), et mène alors à la recherche à ces dates.
   Sans prix repéré, la pastille reste telle quelle (elle mène à la page du pays). Chargé après l'affichage de la page.
   En italien, ce script pose aussi les noms des pays (attribut data-it) : app.js ne connaît que le français et l'anglais. */
(function () {
  "use strict";
  var root = document.documentElement, rb = document.querySelector(".hero .ruban");
  var lg = function () { return (root.lang || "fr").slice(0, 2); };
  var italien = function () { if (lg() === "it") [].forEach.call(document.querySelectorAll("[data-it]"), function (e) { if (e.textContent !== e.dataset.it) e.textContent = e.dataset.it; }); };
  italien();
  if (window.MutationObserver) new MutationObserver(function () { setTimeout(italien, 0); peindre(); }).observe(root, { attributes: true, attributeFilter: ["lang"] });
  if (!rb) return;
  var code = function () { var f = document.getElementById("f-from"), m = f && /\(([A-Z]{3})\)\s*$/.exec(f.value || ""); return m ? m[1] : ""; };
  var money = function (n) { if (window.ESCALE_MONEY) return window.ESCALE_MONEY(n, "EUR"); try { return new Intl.NumberFormat(lg(), { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var MOT = { fr: ["dès ", "Aller-retour le plus bas repéré récemment, il peut changer"], en: ["from ", "Lowest return fare spotted recently, it can change"], it: ["da ", "Andata e ritorno più basso rilevato di recente, può cambiare"],
    es: ["desde ", "Ida y vuelta más barato visto recientemente, puede cambiar"], pt: ["desde ", "Ida e volta mais barata vista recentemente, pode mudar"], de: ["ab ", "Günstigster Hin- und Rückflug, kürzlich gesehen; kann sich ändern"] };
  var fait = "", P = {}, de = "";
  function peindre() {
    if (!rb || !de) return;
    var l = lg(), m = MOT[l] || MOT.en;
    [].forEach.call(rb.querySelectorAll("a[data-cc]"), function (a) {
      var x = P[a.dataset.cc], b = a.querySelector("b");
      if (!x || !(x.price > 0)) { if (b) b.remove(); a.removeAttribute("title"); if (a.dataset.h) { a.setAttribute("href", a.dataset.h); delete a.dataset.h; } return; }
      if (!b) { b = document.createElement("b"); a.appendChild(b); }
      b.textContent = (a.getAttribute("data-ville-" + l) || (l === "fr" ? a.dataset.ville : a.getAttribute("data-ville-en")) || a.dataset.ville) + " " + m[0] + money(x.price);
      a.title = m[1];
      if (!a.dataset.h) a.dataset.h = a.getAttribute("href");
      a.setAttribute("href", "/?type=vols&from=" + de + "&to=" + x.to + "&dep=" + x.dep + (x.ret ? "&ret=" + x.ret : "") + (l === "fr" ? "" : "&lang=" + l));
    });
  }
  var remplir = function () {
    var from = code(); if (!from || from === fait) return; fait = from;
    fetch("/api/ruban?from=" + from).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (j) {
      if (code() !== from) return;
      P = (j && j.available && j.prix) || {}; de = from; peindre();
    });
  };
  var go = function () { remplir(); var f = document.getElementById("f-from"); if (f) { f.addEventListener("change", function () { setTimeout(remplir, 300); }); f.addEventListener("blur", function () { setTimeout(remplir, 300); }); } };
  // Après l'affichage : le moteur a eu le temps de proposer l'aéroport du visiteur
  if ("requestIdleCallback" in window) setTimeout(function () { requestIdleCallback(go, { timeout: 2500 }); }, 1800); else setTimeout(go, 3000);
})();
