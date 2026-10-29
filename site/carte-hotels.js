// Carte des hôtels en direct (Stay22, identifiant escalelive) : Booking, Expedia, Hotels.com, Agoda, Vrbo… sur une carte, avec les prix.
// - pages hôtels : la carte se charge au clic sur « Afficher la carte » (page plus rapide, rien n'est chargé sans action du visiteur) ;
// - page « Recherche en direct » : sous les vols, la carte de la ville d'arrivée pour les mêmes dates.
(function () {
  "use strict";
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var L = { fr: ["Hôtels à {c} pour vos dates", "Prix en direct de Booking, Expedia, Agoda, Hotels.com… Cliquez sur un hôtel pour voir l’offre."],
    en: ["Hotels in {c} for your dates", "Live prices from Booking, Expedia, Agoda, Hotels.com… Click a hotel to see the deal."],
    es: ["Hoteles en {c} para tus fechas", "Precios en directo de Booking, Expedia, Agoda, Hotels.com… Haz clic en un hotel para ver la oferta."],
    pt: ["Hotéis em {c} para as suas datas", "Preços ao vivo da Booking, Expedia, Agoda, Hotels.com… Clique num hotel para ver a oferta."],
    ar: ["فنادق {c} لتواريخك", "أسعار مباشرة من بوكينغ وإكسبيديا وأغودا… انقر على فندق لعرض العرض."],
    it: ["Hotel a {c} per le tue date", "Prezzi in diretta di Booking, Expedia, Agoda, Hotels.com… Clicca su un hotel per vedere l’offerta."] }[lang] || null;
  var url = function (address, checkin, checkout) {
    return "https://www.stay22.com/embed/gm?" + new URLSearchParams(Object.assign({ aid: "escalelive", address: address, maincolor: "1A56DB", currency: "EUR" },
      checkin && checkout ? { checkin: checkin, checkout: checkout } : {})).toString();
  };
  var frame = function (src, title) {
    var f = document.createElement("iframe");
    f.src = src; f.title = title; f.loading = "lazy"; f.className = "s22-frame"; f.setAttribute("allow", "geolocation");
    return f;
  };
  window.EscaleHotelMap = { url: url, frame: frame };

  // Pages hôtels : bouton « Afficher la carte »
  Array.prototype.forEach.call(document.querySelectorAll(".s22-map[data-address]"), function (box) {
    var btn = box.querySelector("button");
    if (!btn) return;
    btn.addEventListener("click", function () {
      box.querySelector(".s22-ph").replaceWith(frame(url(box.getAttribute("data-address")), box.getAttribute("data-title") || "Stay22"));
    });
  });

  // Page « Recherche en direct » : carte de la ville d'arrivée, pour les dates de la recherche
  var fs = new URLSearchParams(location.search).get("flightSearch"), slot = document.getElementById("wl-hotels");
  var m = fs && fs.match(/^[A-Z]{3}(\d{2})(\d{2})([A-Z]{3})(?:(\d{2})(\d{2}))?/);
  if (!slot || !m || !L) return;
  var dateOf = function (d, mo) { // prochaine date à venir pour ce jour et ce mois
    var now = new Date(), y = now.getFullYear(), t = new Date(y, +mo - 1, +d);
    if (t < new Date(now.getFullYear(), now.getMonth(), now.getDate())) t = new Date(y + 1, +mo - 1, +d);
    return t.getFullYear() + "-" + mo + "-" + d;
  };
  var inD = dateOf(m[1], m[2]), outD = m[4] ? dateOf(m[4], m[5]) : null;
  if (outD && outD <= inD) outD = null;
  fetch("/data/airports.json").then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; }).then(function (db) {
    var a = (db || []).filter(function (x) { return x[0] === m[3]; })[0];
    if (!a) return;
    var city = a[1], cc = a[3], country = "";
    try { country = new Intl.DisplayNames(["en"], { type: "region" }).of(cc); } catch (e) {}
    slot.querySelector("h2").textContent = L[0].replace("{c}", city);
    slot.querySelector("p").textContent = L[1];
    slot.appendChild(frame(url(city + (country ? ", " + country : ""), inD, outD || null), L[0].replace("{c}", city)));
    slot.hidden = false;
  });
})();
