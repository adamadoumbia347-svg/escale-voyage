/* Accueil : prix des vols dans le ruban de pays. Pour la ville de départ du visiteur, chaque pastille reçoit le prix
   aller-retour le plus bas repéré vers la grande ville du pays (/api/ruban), et mène alors à la recherche à ces dates.
   Sans prix repéré, la pastille reste telle quelle (elle mène à la page du pays). Chargé après l'affichage de la page. */
(function () {
  "use strict";
  var rb = document.querySelector(".hero .ruban"); if (!rb) return;
  var code = function () { var f = document.getElementById("f-from"), m = f && /\(([A-Z]{3})\)\s*$/.exec(f.value || ""); return m ? m[1] : ""; };
  var money = function (n) { if (window.ESCALE_MONEY) return window.ESCALE_MONEY(n, "EUR"); try { return new Intl.NumberFormat(document.documentElement.lang || "fr", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var en = (document.documentElement.lang || "fr").slice(0, 2) !== "fr", fait = "";
  var remplir = function () {
    var from = code(); if (!from || from === fait) return; fait = from;
    fetch("/api/ruban?from=" + from).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (j) {
      if (code() !== from) return;
      var P = (j && j.available && j.prix) || {};
      [].forEach.call(rb.querySelectorAll("a[data-cc]"), function (a) {
        var x = P[a.dataset.cc], b = a.querySelector("b");
        if (!a.dataset.h) a.dataset.h = a.getAttribute("href");
        if (!x || !(x.price > 0)) { if (b) b.remove(); a.setAttribute("href", a.dataset.h); a.removeAttribute("title"); return; }
        if (!b) { b = document.createElement("b"); a.appendChild(b); }
        b.textContent = a.dataset.ville + " " + (en ? "from " : "dès ") + money(x.price);
        a.title = (en ? "Lowest round-trip price spotted recently, it can change" : "Aller-retour le plus bas repéré récemment, il peut changer");
        a.setAttribute("href", "/?type=vols&from=" + from + "&to=" + x.to + "&dep=" + x.dep + (x.ret ? "&ret=" + x.ret : ""));
      });
      rb.classList.toggle("prix", Object.keys(P).length > 0);
    });
  };
  var go = function () { remplir(); var f = document.getElementById("f-from"); if (f) { f.addEventListener("change", function () { setTimeout(remplir, 300); }); f.addEventListener("blur", function () { setTimeout(remplir, 300); }); } };
  // Après l'affichage : le moteur a eu le temps de proposer l'aéroport du visiteur
  if ("requestIdleCallback" in window) setTimeout(function () { requestIdleCallback(go, { timeout: 2500 }); }, 1800); else setTimeout(go, 3000);
})();
