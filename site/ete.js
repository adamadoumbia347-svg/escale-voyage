// Pages « Vacances d'été » : prix aller-retour le plus bas repéré pour chaque période / aéroport (/api/prix cherche au mois).
// Affiche aussi les dates du vol trouvé et met ces dates dans le lien « Voir les vols ».
(function () {
  "use strict";
  var tables = document.querySelectorAll(".ete-table");
  if (!tables.length) return;
  var L = (document.documentElement.lang || "fr").slice(0, 2);
  var W = { fr: ["fr-FR", "Pas encore de prix", "dès ", "Aller-retour depuis Paris repéré dès "], en: ["en-GB", "No price yet", "from ", "Round trip from London found from "],
            it: ["it-IT", "Ancora nessun prezzo", "da ", "Andata e ritorno da Milano trovato da "] }[L] || ["fr-FR", "Pas encore de prix", "dès ", "Aller-retour repéré dès "];
  var heroFrom = tables[0].getAttribute("data-hero") || "CDG";
  var money = function (n, cur) {
    try { return new Intl.NumberFormat(W[0], { style: "currency", currency: cur || "EUR", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " " + (cur || "EUR"); }
  };
  var day = function (iso) { return new Date(iso.slice(0, 10) + "T12:00:00").toLocaleDateString(W[0], { day: "numeric", month: "short" }); };
  var best = null, today = new Date().toISOString().slice(0, 10);
  Array.prototype.forEach.call(tables, function (t) {
    Array.prototype.forEach.call(t.querySelectorAll("tbody tr"), function (tr) {
      var cell = tr.querySelector(".fp"), link = tr.querySelector("a.price-go");
      var url = "/api/prix?from=" + tr.getAttribute("data-from") + "&to=" + tr.getAttribute("data-to") +
        "&dep=" + tr.getAttribute("data-dep") + "-01&ret=" + tr.getAttribute("data-ret") + "-01&currency=EUR";
      fetch(url).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (d) {
        var dep = d && (d.departure_at || "").slice(0, 10), ret = d && (d.return_at || "").slice(0, 10);
        if (!d || !d.available || !d.price || !dep || dep < today) { cell.textContent = W[1]; return; }
        cell.innerHTML = "<strong></strong><span class=\"small ete-note\"></span>";
        cell.firstChild.textContent = W[2] + money(d.price, d.currency);
        cell.lastChild.textContent = day(dep) + (ret ? " → " + day(ret) : "");
        if (link && ret) link.href = link.href.replace(/dep=[0-9-]+/, "dep=" + dep).replace(/ret=[0-9-]+/, "ret=" + ret);
        // Prix le plus bas de la page, affiché en haut (et proposé comme budget de l'alerte)
        if (tr.getAttribute("data-from") === heroFrom && (best === null || d.price < best)) {
          best = d.price;
          var h = document.getElementById("hero-price");
          if (h) { h.innerHTML = ""; h.appendChild(document.createTextNode(W[3])); h.appendChild(document.createElement("strong")); h.lastChild.textContent = money(d.price, d.currency); h.hidden = false; }
        }
      });
    });
  });
})();
