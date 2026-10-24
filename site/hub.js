// Pages « destination » : prix aller-retour le plus bas repéré pour chaque ville de départ (le mois prochain).
// Les cases déjà remplies par le serveur (src/apercu-prix.ts, data-ssr) ne sont pas redemandées.
(function () {
  "use strict";
  var cells = document.querySelectorAll(".hub-price:not([data-ssr])");
  if (!cells.length) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn" }[lang] || "fr-FR";
  var money = function (n) {
    try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " €"; }
  };
  var d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + 1);
  var month = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-01";
  cells.forEach(function (td) {
    fetch("/api/prix?from=" + td.getAttribute("data-from") + "&to=" + td.getAttribute("data-to") + "&dep=" + month + "&rt=1")
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; })
      .then(function (p) {
        if (p && p.available && p.price) td.innerHTML = td.getAttribute("data-label") + " <strong>" + money(p.price) + "</strong>";
        else td.textContent = "—";
      });
  });
})();
