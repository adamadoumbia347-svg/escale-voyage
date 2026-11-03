// « Escale malin » (pages trajets) : quand un vol avec escale est nettement moins cher que le vol direct, on le montre,
// avec le temps de voyage en plus. Prix réels repérés le mois prochain (/api/prix, liste des offres et offres directes).
(function () {
  "use strict";
  var box = document.getElementById("route-prices");
  if (!box) return;
  var from = box.getAttribute("data-from"), to = box.getAttribute("data-to");
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var L = {
    fr: ["Escale malin", "Avec {n} : {p} au lieu de {d} en vol direct, soit {s} de moins pour {h} de voyage en plus.", "1 escale", "{k} escales", "Voir ces vols", "loc fr-FR"],
    en: ["Smart stopover", "With {n}: {p} instead of {d} for a direct flight, {s} less for {h} more travel time.", "1 stop", "{k} stops", "See these flights", "loc en-GB"],
    es: ["Escala inteligente", "Con {n}: {p} en vez de {d} en vuelo directo, {s} menos por {h} más de viaje.", "1 escala", "{k} escalas", "Ver estos vuelos", "loc es-ES"],
    pt: ["Escala inteligente", "Com {n}: {p} em vez de {d} em voo direto, {s} a menos por mais {h} de viagem.", "1 escala", "{k} escalas", "Ver estes voos", "loc pt-PT"],
    ar: ["توقف ذكي", "مع {n}: {p} بدلًا من {d} للرحلة المباشرة، أي أقل بـ{s} مقابل {h} إضافية من السفر.", "توقف واحد", "{k} توقفات", "اعرض هذه الرحلات", "loc ar"],
    it: ["Scalo furbo", "Con {n}: {p} invece di {d} con volo diretto, {s} in meno per {h} di viaggio in più.", "1 scalo", "{k} scali", "Vedi questi voli", "loc it-IT"],
    de: ["Clever umsteigen", "Mit {n}: {p} statt {d} im Direktflug, {s} weniger für {h} mehr Reisezeit.", "1 Stopp", "{k} Stopps", "Diese Flüge ansehen", "loc de-DE"]
  }[lang] || null;
  if (!L) return;
  var loc = L[5].slice(4);
  var money = function (n, c) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: c || "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var hours = function (m) { var h = Math.round(m / 60); return h + " h"; };
  var d0 = new Date(); d0.setMonth(d0.getMonth() + 1, 10);
  var iso = function (d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
  var d1 = new Date(d0.getTime() + 7 * 864e5), q = "from=" + from + "&to=" + to + "&dep=" + iso(d0) + "&ret=" + iso(d1) + "&currency=EUR";
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  Promise.all([get("/api/prix?" + q + "&list=1"), get("/api/prix?" + q + "&direct=1&list=1")]).then(function (res) {
    var all = (res[0] && res[0].offers) || [], dir = ((res[1] && res[1].offers) || []).filter(function (o) { return o.transfers === 0; });
    var stop = all.filter(function (o) { return o.transfers > 0 && o.duration_to; }).sort(function (a, b) { return a.price - b.price; })[0];
    var direct = dir.concat(all.filter(function (o) { return o.transfers === 0; })).sort(function (a, b) { return a.price - b.price; })[0];
    if (!stop || !direct || !direct.duration_to) return;
    var save = direct.price - stop.price;
    if (save < 40 || save / direct.price < 0.15) return;  // écart trop faible : pas la peine de conseiller une escale
    var extra = Math.max(60, (stop.duration_to - direct.duration_to) + ((stop.duration_back || stop.duration_to) - (direct.duration_back || direct.duration_to)));
    var n = stop.transfers === 1 ? L[2] : L[3].replace("{k}", stop.transfers);
    var dd = function (s) { return s ? String(s).slice(8, 10) + String(s).slice(5, 7) : ""; };
    var href = "/recherche/?flightSearch=" + from + dd(stop.departure_at) + to + dd(stop.return_at) + "1";
    var sec = document.createElement("section"); sec.className = "escale-malin";
    sec.innerHTML = "<h2></h2><p></p><p><a class=\"btn ghost\"></a></p>";
    sec.querySelector("h2").textContent = "💡 " + L[0];
    sec.querySelector("p").textContent = L[1].replace("{n}", n).replace("{p}", money(stop.price)).replace("{d}", money(direct.price)).replace("{s}", money(save)).replace("{h}", hours(extra));
    var a = sec.querySelector("a"); a.href = href; a.textContent = L[4] + " →";
    // Plus bas dans la page (avant l'alerte prix) : rien ne bouge en haut pendant le chargement
    var at = document.getElementById("price-alert") || box.nextSibling;
    at.parentNode.insertBefore(sec, at);
  });
})();
