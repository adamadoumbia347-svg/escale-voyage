// Carte des hôtels en direct (Stay22, identifiant escalelive) : Booking, Expedia, Hotels.com, Agoda, Vrbo… sur une carte, avec les prix.
// - pages hôtels : la carte se charge au clic sur « Afficher la carte » (page plus rapide, rien n'est chargé sans action du visiteur) ;
// - page « Recherche en direct » : sous les vols, la carte de la ville d'arrivée pour les mêmes dates ;
// - page « Hôtels en direct » : la recherche d'hôtels de l'accueil, en grand.
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

  // Page « Hôtels en direct » (/hotels-en-direct/?ville=Dakar&arrivee=2026-12-10&depart=2026-12-15&adultes=2&lang=fr) :
  // la recherche d'hôtels de l'accueil arrive ici, comme les vols arrivent sur /recherche/
  var hl = document.getElementById("hl-form");
  if (hl) {
    var P = new URLSearchParams(location.search), lg = P.get("lang") || "";
    if (!/^(fr|en|es|pt|ar|it)$/.test(lg)) lg = "fr";
    var H = {
      fr: { title: "Hôtels à {c}", sum: "{a} → {b} · {n} nuit(s) · {p} adulte(s). Prix en direct de Booking, Expedia, Agoda, Hotels.com… Cliquez sur un hôtel pour voir l’offre." },
      en: { eyebrow: "Live prices", title: "Hotels in {c}", lead: "Real-time prices from Booking, Expedia, Agoda, Hotels.com and more, on a map. Click a hotel to see the deal and book on the partner’s site.",
        city: "Destination", in: "Check-in", out: "Check-out", adults: "Adults", go: "Search", cmp_h: "Also compare on",
        note: "Map provided by our partner Stay22. Escale does not sell hotel nights: the final price and conditions are shown on the booking site. Escale may earn a commission if you book, at no cost to you.",
        sum: "{a} → {b} · {n} night(s) · {p} adult(s). Live prices from Booking, Expedia, Agoda, Hotels.com… Click a hotel to see the deal.", list: "Hotel list", map: "View on map" },
      es: { eyebrow: "Precios en directo", title: "Hoteles en {c}", lead: "Precios en tiempo real de Booking, Expedia, Agoda, Hotels.com y otros, en un mapa. Haz clic en un hotel para ver la oferta.",
        city: "Destino", in: "Llegada", out: "Salida", adults: "Adultos", go: "Buscar", cmp_h: "Comparar también en",
        note: "Mapa de nuestro socio Stay22. Escale no vende noches de hotel: el precio final aparece en el sitio de reserva. Escale puede recibir una comisión, sin coste para ti.",
        sum: "{a} → {b} · {n} noche(s) · {p} adulto(s). Precios en directo de Booking, Expedia, Agoda, Hotels.com… Haz clic en un hotel para ver la oferta.", list: "Lista de hoteles", map: "Ver en el mapa" },
      pt: { eyebrow: "Preços ao vivo", title: "Hotéis em {c}", lead: "Preços em tempo real da Booking, Expedia, Agoda, Hotels.com e outros, num mapa. Clique num hotel para ver a oferta.",
        city: "Destino", in: "Entrada", out: "Saída", adults: "Adultos", go: "Pesquisar", cmp_h: "Comparar também em",
        note: "Mapa do nosso parceiro Stay22. A Escale não vende noites de hotel: o preço final aparece no site de reserva. A Escale pode receber uma comissão, sem custo para si.",
        sum: "{a} → {b} · {n} noite(s) · {p} adulto(s). Preços ao vivo da Booking, Expedia, Agoda, Hotels.com… Clique num hotel para ver a oferta.", list: "Lista de hotéis", map: "Ver no mapa" },
      ar: { eyebrow: "أسعار مباشرة", title: "فنادق {c}", lead: "أسعار مباشرة من بوكينغ وإكسبيديا وأغودا وغيرها على خريطة. انقر على فندق لعرض العرض.",
        city: "الوجهة", in: "الوصول", out: "المغادرة", adults: "البالغون", go: "بحث", cmp_h: "قارن أيضاً على",
        note: "خريطة من شريكنا Stay22. لا تبيع Escale ليالي الفنادق: يظهر السعر النهائي على موقع الحجز. قد تحصل Escale على عمولة دون أي تكلفة عليك.",
        sum: "{a} ← {b} · {n} ليلة · {p} بالغ. أسعار مباشرة من بوكينغ وإكسبيديا وأغودا… انقر على فندق لعرض العرض.", list: "قائمة الفنادق", map: "عرض على الخريطة" },
      it: { eyebrow: "Prezzi in diretta", title: "Hotel a {c}", lead: "Prezzi in tempo reale di Booking, Expedia, Agoda, Hotels.com e altri, su una mappa. Clicca su un hotel per vedere l’offerta.",
        city: "Destinazione", in: "Arrivo", out: "Partenza", adults: "Adulti", go: "Cerca", cmp_h: "Confronta anche su",
        note: "Mappa fornita dal nostro partner Stay22. Escale non vende notti d’hotel: il prezzo finale appare sul sito di prenotazione. Escale può ricevere una commissione, senza costi per te.",
        sum: "{a} → {b} · {n} notte/i · {p} adulto/i. Prezzi in diretta di Booking, Expedia, Agoda, Hotels.com… Clicca su un hotel per vedere l’offerta.", list: "Elenco degli hotel", map: "Vedi sulla mappa" }
    }[lg];
    if (lg !== "fr") {
      document.documentElement.lang = lg; if (lg === "ar") document.documentElement.dir = "rtl";
      Array.prototype.forEach.call(document.querySelectorAll("[data-h]"), function (el) { var k = el.getAttribute("data-h"); if (H[k] && k !== "title") el.textContent = H[k]; });
    }
    var iso = function (d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
    var plus = function (n) { var d = new Date(); d.setDate(d.getDate() + n); return iso(d); };
    var ok = function (x) { return /^\d{4}-\d{2}-\d{2}$/.test(x || ""); };
    var city = (P.get("ville") || "").trim().slice(0, 120), ad = Math.min(8, Math.max(1, parseInt(P.get("adultes"), 10) || 2));
    var inD = P.get("arrivee"), outD = P.get("depart");
    if (!ok(inD) || inD < iso(new Date())) inD = plus(21);
    if (!ok(outD) || outD <= inD) { var d2 = new Date(inD + "T12:00:00"); d2.setDate(d2.getDate() + 4); outD = iso(d2); }
    var f = function (id) { return document.getElementById(id); };
    f("hl-ville").value = city; f("hl-in").value = inD; f("hl-out").value = outD; f("hl-ad").value = String(ad); f("hl-lang").value = lg;
    f("hl-in").min = iso(new Date());
    f("hl-in").addEventListener("change", function () { if (f("hl-out").value <= f("hl-in").value) { var x = new Date(f("hl-in").value + "T12:00:00"); x.setDate(x.getDate() + 4); f("hl-out").value = iso(x); } });
    if (city) {
      var nights = Math.round((new Date(outD + "T12:00:00") - new Date(inD + "T12:00:00")) / 864e5);
      var fmtD = function (x) { try { return new Date(x + "T12:00:00").toLocaleDateString(lg, { day: "numeric", month: "short" }); } catch (e) { return x; } };
      var title = (H.title || "Hôtels à {c}").replace("{c}", city);
      document.querySelector("h1").textContent = title;
      var lead = document.querySelector(".hero-lead"); if (lead) lead.hidden = true; // la carte d’abord (surtout sur téléphone)
      document.title = title + " : prix en direct | Escale";
      var box = f("hl-live");
      f("hl-sum").textContent = H.sum.replace("{a}", fmtD(inD)).replace("{b}", fmtD(outD)).replace("{n}", nights).replace("{p}", ad);
      // Liste des hôtels d'abord (viewmode=listview), bouton pour passer à la carte (viewmode=map)
      var base = url(city, inD, outD) + "&adults=" + ad, fr = frame(base + "&viewmode=listview", title);
      fr.loading = "eager"; fr.className += " big";
      var sw = document.createElement("div"); sw.className = "hl-switch"; sw.setAttribute("role", "group");
      [["listview", H.list || "Liste des hôtels"], ["map", H.map || "Voir sur la carte"]].forEach(function (v, i) {
        var b = document.createElement("button"); b.type = "button"; b.textContent = v[1];
        b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
        b.addEventListener("click", function () {
          if (b.getAttribute("aria-pressed") === "true") return;
          Array.prototype.forEach.call(sw.children, function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
          fr.src = base + "&viewmode=" + v[0];
        });
        sw.appendChild(b);
      });
      box.appendChild(sw); box.appendChild(fr); box.hidden = false;
      f("hl-cmp-a").href = "/?" + new URLSearchParams({ type: "hotels", dest: city, in: inD, out: outD, ad: String(ad), cmp: "1" }).toString();
      f("hl-cmp").hidden = false;
    } else f("hl-ville").focus();
    return;
  }

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
