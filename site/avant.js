// « Avant de partir » (eSIM Airalo, location de voiture, transfert, activités, assurance, indemnisation…) sur les pages
// Recherche en direct et Hôtels en direct. Liens partenaires réglés dans /data/partners.json (comme l'ancienne recherche de l'accueil).
(function () {
  "use strict";
  var box = document.getElementById("avant-partir");
  if (!box) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var T = { fr: ["Avant de partir", "Les services utiles pour votre voyage", "Les services utiles pour votre voyage à {c}", "Voir l’offre"],
    en: ["Before you go", "Useful services for your trip", "Useful services for your trip to {c}", "See offer"],
    es: ["Antes de salir", "Servicios útiles para tu viaje", "Servicios útiles para tu viaje a {c}", "Ver oferta"],
    pt: ["Antes de partir", "Serviços úteis para a sua viagem", "Serviços úteis para a sua viagem a {c}", "Ver oferta"],
    ar: ["قبل السفر", "خدمات مفيدة لرحلتك", "خدمات مفيدة لرحلتك إلى {c}", "اعرض العرض"],
    it: ["Prima di partire", "Servizi utili per il tuo viaggio", "Servizi utili per il tuo viaggio a {c}", "Vedi l’offerta"],
    de: ["Vor der Reise", "Nützliche Services für deine Reise", "Nützliche Services für deine Reise nach {c}", "Zum Angebot"],
    nl: ["Voor vertrek", "Handige diensten voor je reis", "Handige diensten voor je reis naar {c}", "Bekijk aanbod"] }[lang] || null;
  if (!T) return;
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var P = new URLSearchParams(location.search), fs = (P.get("flightSearch") || "").match(/^[A-Z]{3}\d{4}([A-Z]{3})/);
  var code = fs ? fs[1] : "", city0 = (P.get("ville") || "").trim().slice(0, 80);
  var cityP = code ? fetch("/data/airports.json").then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; })
    .then(function (db) { var a = (db || []).filter(function (x) { return x[0] === code; })[0]; return a ? a[1] : ""; }) : Promise.resolve(city0);
  Promise.all([fetch("/data/partners.json").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }), cityP]).then(function (res) {
    var cfg = res[0], city = res[1];
    if (!cfg || !cfg.services) return;
    var list = cfg.services.filter(function (p) { return p.key !== "hotel"; }); // les hôtels sont déjà sur ces pages
    box.innerHTML = "<h2>" + esc(T[0]) + "</h2><p class=\"small\">" + esc(city ? T[2].replace("{c}", city) : T[1]) + "</p><ul class=\"avant-list\">" +
      list.map(function (p) {
        var url = p.url.replace("{city}", encodeURIComponent(city)).replace("{code}", code);
        return "<li><span class=\"av-logo\" style=\"background:" + esc(p.color) + "\" aria-hidden=\"true\">" + esc(p.name[0]) + "</span>" +
          "<div><strong>" + esc(p.title[lang] || p.title.en) + "</strong><span>" + esc(p.desc[lang] || p.desc.en) + "</span></div>" +
          "<a href=\"" + esc(url) + "\" target=\"_blank\" rel=\"sponsored noopener noreferrer\">" + esc(T[3]) + " · " + esc(p.name) + "</a></li>";
      }).join("") + "</ul>";
    box.hidden = false;
  });
})();
