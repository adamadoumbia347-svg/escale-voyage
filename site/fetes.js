// Pages « Vols pour les fêtes » : prix aller-retour repérés pour les dates de la fête, trajet par trajet (/api/prix).
(function () {
  "use strict";
  var t = document.querySelector(".fete-table");
  if (!t) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn" }[lang] || "fr-FR";
  var dep = t.getAttribute("data-dep"), ret = t.getAttribute("data-ret");
  var label = t.getAttribute("data-from-label"), none = t.getAttribute("data-none");
  var money = function (n, cur) {
    try { return new Intl.NumberFormat(loc, { style: "currency", currency: cur || "EUR", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " " + (cur || "EUR"); }
  };
  t.querySelectorAll("tbody tr").forEach(function (tr) {
    var cell = tr.querySelector(".fp");
    var url = "/api/prix?from=" + tr.getAttribute("data-from") + "&to=" + tr.getAttribute("data-to") + "&dep=" + dep + "&ret=" + ret + "&currency=EUR";
    fetch(url).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (d) {
      if (d && d.available && d.price) { cell.innerHTML = "<strong></strong>"; cell.firstChild.textContent = label + " " + money(d.price, d.currency); }
      else cell.textContent = none;
    });
  });
})();
