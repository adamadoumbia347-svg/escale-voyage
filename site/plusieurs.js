// Page « Partir à plusieurs » : pour une destination et des dates, le prix aller-retour repéré depuis chaque grande ville
// de départ en Europe (/api/prix, un appel par ville), classé du moins cher au plus cher, avec le total pour le groupe.
(function () {
  "use strict";
  var form = document.getElementById("pl-form");
  if (!form) return;
  var L = (document.documentElement.lang || "fr").slice(0, 2);
  var W = { fr: ["fr-FR", "Pas de prix repéré", "Voir les vols", "pour {n} personnes", "Le moins cher", "Recherche en cours…", "par personne"],
            en: ["en-GB", "No price found", "See flights", "for {n} people", "Cheapest", "Searching…", "per person"] }[L] || ["fr-FR", "Pas de prix repéré", "Voir les vols", "pour {n} personnes", "Le moins cher", "Recherche en cours…", "par personne"];
  var ORIG = JSON.parse(form.getAttribute("data-origins") || "[]");
  var out = document.getElementById("pl-out");
  var money = function (n) { try { return new Intl.NumberFormat(W[0], { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (iso) { return iso ? new Date(iso.slice(0, 10) + "T12:00:00").toLocaleDateString(W[0], { day: "numeric", month: "short" }) : ""; };
  var app = L === "fr" ? "" : "&lang=" + L;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var to = form.elements.to.value, dep = form.elements.dep.value, ret = form.elements.ret.value, n = Math.max(1, Math.min(9, Number(form.elements.n.value) || 1));
    if (!to || !dep) return;
    out.hidden = false;
    out.innerHTML = '<p class="small" aria-live="polite">' + W[5] + "</p>";
    var rows = [];
    Promise.all(ORIG.map(function (o) {
      var u = "/api/prix?from=" + o[0] + "&to=" + to + "&dep=" + dep + (ret ? "&ret=" + ret : "&rt=0") + "&currency=EUR";
      return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (d) {
        rows.push({ code: o[0], city: o[1], d: d && d.available && d.price ? d : null });
      });
    })).then(function () {
      rows.sort(function (a, b) { return (a.d ? a.d.price : 1e9) - (b.d ? b.d.price : 1e9); });
      var best = rows[0] && rows[0].d ? rows[0].d.price : null;
      var html = '<table class="fete-table"><thead><tr><th scope="col">' + (L === "fr" ? "Départ de" : "From") + '</th><th scope="col">' + W[6] + "</th><th scope=\"col\">" + W[3].replace("{n}", n) + '</th><th scope="col"><span class="sr-only">' + W[2] + "</span></th></tr></thead><tbody>";
      rows.forEach(function (r) {
        var d = r.d;
        var dates = d ? '<span class="small ete-note">' + day(d.departure_at) + (d.return_at ? " → " + day(d.return_at) : "") + (d.transfers === 0 ? (L === "fr" ? " · direct" : " · direct") : "") + "</span>" : "";
        var href = "/?type=vols&from=" + r.code + "&to=" + to + "&dep=" + (d ? d.departure_at.slice(0, 10) : dep) + (ret ? "&ret=" + (d && d.return_at ? d.return_at.slice(0, 10) : ret) : "") + app;
        html += "<tr><th scope=\"row\">" + r.city + (d && d.price === best ? ' <span class="pill-best">' + W[4] + "</span>" : "") + dates + "</th>" +
          '<td class="fp">' + (d ? "<strong>" + money(d.price) + "</strong>" : '<span class="small">' + W[1] + "</span>") + "</td>" +
          "<td>" + (d ? "<strong>" + money(d.price * n) + "</strong>" : "—") + "</td>" +
          '<td><a class="price-go" href="' + href + '">' + W[2] + "</a></td></tr>";
      });
      html += "</tbody></table>";
      if (best) {
        var worst = rows.filter(function (r) { return r.d; }).slice(-1)[0];
        if (worst && worst.d.price > best) html += '<p class="small">' + (L === "fr" ? "Écart entre la ville la moins chère et la plus chère : " : "Gap between the cheapest and the most expensive city: ") + "<strong>" + money((worst.d.price - best) * n) + "</strong> " + W[3].replace("{n}", n) + ".</p>";
      }
      out.innerHTML = html;
      try { (window.escaleSend || function () {})("partir-a-plusieurs"); } catch (x) {}
    });
  });
  // Dates par défaut : dans 6 semaines, retour 2 semaines plus tard
  var d0 = new Date(Date.now() + 42 * 864e5), d1 = new Date(Date.now() + 56 * 864e5);
  if (!form.elements.dep.value) form.elements.dep.value = d0.toISOString().slice(0, 10);
  if (!form.elements.ret.value) form.elements.ret.value = d1.toISOString().slice(0, 10);
  form.elements.dep.min = new Date().toISOString().slice(0, 10);
  // Destination dans l'adresse (?to=ABJ) : lance tout de suite
  var q = new URLSearchParams(location.search).get("to");
  if (q && form.elements.to.querySelector('option[value="' + q + '"]')) { form.elements.to.value = q; form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event("submit")); }
})();
