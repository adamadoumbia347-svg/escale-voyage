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
  var cc = "";
  var cityP = code ? fetch("/data/airports.json").then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; })
    .then(function (db) { var a = (db || []).filter(function (x) { return x[0] === code; })[0]; cc = a ? a[3] : ""; return a ? a[1] : ""; }) : Promise.resolve(city0);
  // Pack selon la destination : d'abord les infos Escale (visa selon le passeport, guide d'arrivée à l'aéroport), puis l'essentiel
  // (eSIM, transfert, assurance), puis le reste
  var ARR = { ABJ: "abidjan", DSS: "dakar", LOS: "lagos", ACC: "accra", DLA: "douala", CMN: "casablanca", FIH: "kinshasa", BKO: "bamako", CKY: "conakry",
    ALG: ["alger", "algiers"], TUN: "tunis", LFW: "lome" };
  var ORDER = ["esim", "transfer", "insurance", "car", "tours", "activities", "bike", "claim"];
  var X = { fr: ["Votre pack pour {c}", "Faut-il un visa ?", "La réponse selon votre passeport, avec le lien officiel.", "Arriver à l’aéroport de {c}", "Taxi, change, carte SIM : ce qu’il faut savoir en arrivant.", "Vérifier"],
    en: ["Your pack for {c}", "Do you need a visa?", "The answer for your passport, with the official link.", "Arriving at {c} airport", "Taxis, money, SIM card: what to know when you land.", "Check"],
    es: ["Tu pack para {c}", "¿Necesitas visado?", "La respuesta según tu pasaporte, con el enlace oficial.", "Llegar al aeropuerto de {c}", "Taxi, cambio, tarjeta SIM: lo que hay que saber al llegar.", "Comprobar"],
    pt: ["O seu pack para {c}", "Precisa de visto?", "A resposta segundo o seu passaporte, com o link oficial.", "Chegar ao aeroporto de {c}", "Táxi, câmbio, cartão SIM: o que saber ao chegar.", "Verificar"],
    ar: ["حزمتك إلى {c}", "هل تحتاج إلى تأشيرة؟", "الإجابة حسب جواز سفرك مع الرابط الرسمي.", "الوصول إلى مطار {c}", "سيارات الأجرة والصرف وشريحة الاتصال: ما يجب معرفته عند الوصول.", "تحقّق"],
    it: ["Il tuo pacchetto per {c}", "Serve il visto?", "La risposta in base al tuo passaporto, con il link ufficiale.", "Arrivare all’aeroporto di {c}", "Taxi, cambio, SIM: cosa sapere all’arrivo.", "Verifica"],
    de: ["Dein Paket für {c}", "Brauchst du ein Visum?", "Die Antwort für deinen Pass, mit offiziellem Link.", "Ankunft am Flughafen {c}", "Taxi, Geld, SIM-Karte: was du bei der Ankunft wissen musst.", "Prüfen"],
    nl: ["Je pakket voor {c}", "Heb je een visum nodig?", "Het antwoord voor je paspoort, met de officiële link.", "Aankomst op de luchthaven van {c}", "Taxi, geld, simkaart: wat je moet weten bij aankomst.", "Bekijken"] }[lang];
  Promise.all([fetch("/data/partners.json").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }), cityP]).then(function (res) {
    var cfg = res[0], city = res[1];
    if (!cfg || !cfg.services) return;
    var list = cfg.services.filter(function (p) { return p.key !== "hotel"; }); // les hôtels sont déjà sur ces pages
    list.sort(function (a, b) { var i = ORDER.indexOf(a.key), j = ORDER.indexOf(b.key); return (i < 0 ? 99 : i) - (j < 0 ? 99 : j); });
    var own = "";
    if (city && X) {
      var en = lang !== "fr", item = function (icon, t, d, href) { return "<li><span class=\"av-logo\" style=\"background:#1a56db\" aria-hidden=\"true\">" + icon + "</span><div><strong>" + esc(t) + "</strong><span>" + esc(d) + "</span></div><a href=\"" + esc(href) + "\">" + esc(X[5]) + " →</a></li>"; };
      var SCH = /^(AT|BE|BG|HR|CZ|DK|EE|FI|FR|DE|GR|HU|IS|IT|LV|LI|LT|LU|MT|NL|NO|PL|PT|RO|SK|SI|ES|SE|CH)$/;
      if (cc) own += item("🛂", X[1], X[2], (en ? "/en/visa/" : "/visa/") + "?d=" + (SCH.test(cc) ? "SCH" : cc));
      var g = ARR[code]; if (g) { var slug = Array.isArray(g) ? g[en ? 1 : 0] : g; own += item("🛬", X[3].replace("{c}", city), X[4], en ? "/en/arriving-at-" + slug + "-airport/" : "/arriver-aeroport-" + slug + "/"); }
    }
    box.innerHTML = "<h2>" + esc(city && X ? X[0].replace("{c}", city) : T[0]) + "</h2><p class=\"small\">" + esc(city ? T[2].replace("{c}", city) : T[1]) + "</p><ul class=\"avant-list\">" + own +
      list.map(function (p) {
        var url = p.url.replace("{city}", encodeURIComponent(city)).replace("{code}", code);
        // Klook : page de la ville si on l'a (partners.json → klook.villes), lien partenaire au format Travelpayouts
        if (p.key === "tours" && cfg.klook && cfg.klook.villes && cfg.klook.villes[code]) url = cfg.klook.format.replace("{url}", encodeURIComponent(cfg.klook.villes[code]));
        if (/stay22\.com/.test(url)) url += "&lang=" + lang;  // page Stay22 dans la langue de la page
        return "<li><span class=\"av-logo\" style=\"background:" + esc(p.color) + "\" aria-hidden=\"true\">" + esc(p.name[0]) + "</span>" +
          "<div><strong>" + esc(p.title[lang] || p.title.en) + "</strong><span>" + esc(p.desc[lang] || p.desc.en) + "</span></div>" +
          "<a href=\"" + esc(url) + "\" target=\"_blank\" rel=\"sponsored noopener noreferrer\">" + esc(T[3]) + " · " + esc(p.name) + "</a></li>";
      }).join("") + "</ul>";
    box.hidden = false;
  });
})();
