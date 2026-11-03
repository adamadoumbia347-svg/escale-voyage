// Page « Recherche en direct » avec une recherche déjà lancée (?flightSearch=CDG1911DSS26111) : comme sur Skyscanner,
// le grand titre et le formulaire laissent la place à une barre compacte (trajet, passagers, dates avec ‹ ›).
// Toucher la barre rouvre le formulaire du moteur pour modifier la recherche.
(function () {
  "use strict";
  var bar = document.getElementById("rs-bar"), form = document.querySelector(".wl-form");
  var fs = new URLSearchParams(location.search).get("flightSearch") || "";
  var m = fs.match(/^([A-Z]{3})(\d{2})(\d{2})([A-Z]{3})(?:(\d{2})(\d{2}))?(\d)?(\d)?(\d)?$/);
  if (!bar || !form || !m) return;
  var from = m[1], to = m[4], ad = +(m[7] || 1), ch = +(m[8] || 0) + +(m[9] || 0);
  var today = new Date(); today.setHours(0, 0, 0, 0);
  var dateOf = function (d, mo) { // prochaine date à venir pour ce jour et ce mois
    var t = new Date(today.getFullYear(), +mo - 1, +d);
    if (t < today) t.setFullYear(t.getFullYear() + 1);
    return t;
  };
  var dep = dateOf(m[2], m[3]), ret = m[5] ? dateOf(m[5], m[6]) : null;
  if (ret && ret < dep) ret.setFullYear(ret.getFullYear() + 1);
  var dd = function (d) { return String(d.getDate()).padStart(2, "0") + String(d.getMonth() + 1).padStart(2, "0"); };
  var shift = function (d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; };
  var link = function (a, b) { return "/recherche/?flightSearch=" + from + dd(a) + to + (b ? dd(b) : "") + (m[7] ? m.slice(7).join("") : "1"); };
  // Langue choisie sur Escale (ou du navigateur) : barre et textes de la page dans cette langue, comme le moteur (wl.js)
  var LG = "fr"; try { LG = (localStorage.getItem("escale.lang") || (navigator.language || "fr").slice(0, 2)).toLowerCase(); } catch (e) {}
  var W = { en: ["adult", "adults", "child", "children", "Economy", "Edit", "Outbound", "Return", "one day earlier", "one day later", "Live prices", "Live flight search",
      "Provided by our partner Travelpayouts (Aviasales). Escale does not sell tickets: the final price and conditions (baggage, changes) are shown on the booking site. Escale may earn a commission if you book, at no cost to you."],
    es: ["adulto", "adultos", "niño", "niños", "Turista", "Modificar", "Ida", "Vuelta", "un día antes", "un día después", "Precios en directo", "Búsqueda de vuelos en directo",
      "Buscador de nuestro socio Travelpayouts (Aviasales). Escale no vende billetes: el precio final y las condiciones aparecen en el sitio de reserva. Escale puede recibir una comisión, sin coste para ti."],
    pt: ["adulto", "adultos", "criança", "crianças", "Económica", "Alterar", "Ida", "Volta", "um dia antes", "um dia depois", "Preços ao vivo", "Pesquisa de voos ao vivo",
      "Motor do nosso parceiro Travelpayouts (Aviasales). A Escale não vende bilhetes: o preço final e as condições aparecem no site de reserva. A Escale pode receber uma comissão, sem custo para si."],
    it: ["adulto", "adulti", "bambino", "bambini", "Economy", "Modifica", "Andata", "Ritorno", "un giorno prima", "un giorno dopo", "Prezzi in diretta", "Ricerca voli in diretta",
      "Motore del nostro partner Travelpayouts (Aviasales). Escale non vende biglietti: il prezzo finale e le condizioni appaiono sul sito di prenotazione. Escale può ricevere una commissione, senza costi per te."],
    de: ["Erwachsener", "Erwachsene", "Kind", "Kinder", "Economy", "Ändern", "Hinflug", "Rückflug", "einen Tag früher", "einen Tag später", "Live-Preise", "Live-Flugsuche",
      "Suchmaschine unseres Partners Travelpayouts (Aviasales). Escale verkauft keine Tickets: Endpreis und Bedingungen erscheinen auf der Buchungsseite. Escale erhält eventuell eine Provision, ohne Kosten für dich."],
    ar: ["بالغ", "بالغين", "طفل", "أطفال", "اقتصادية", "تعديل", "الذهاب", "العودة", "يوماً قبل", "يوماً بعد", "أسعار مباشرة", "بحث مباشر عن الرحلات",
      "محرك من شريكنا Travelpayouts (Aviasales). لا تبيع Escale التذاكر: يظهر السعر النهائي والشروط على موقع الحجز. قد تحصل Escale على عمولة دون أي تكلفة عليك."] }[LG];
  var LOC = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", it: "it-IT", de: "de-DE", ar: "ar" }[LG] || "fr-FR";
  if (W) {
    document.documentElement.lang = LG; if (LG === "ar") document.documentElement.dir = "rtl";
    var setT = function (sel, t) { var e = document.querySelector(sel); if (e) e.textContent = t; };
    setT(".hero .eyebrow, .eyebrow", W[10]); setT("h1", W[11]);
    Array.prototype.forEach.call(document.querySelectorAll("p.small"), function (p) { if (/Travelpayouts/.test(p.textContent)) p.textContent = W[12]; });
  }
  var day = function (d) { return d.toLocaleDateString(LOC, { weekday: "short", day: "numeric", month: "short" }); };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var arrow = function (href, label, txt, off) {
    return off ? '<span class="rs-arr" aria-hidden="true">' + txt + "</span>" : '<a class="rs-arr" href="' + href + '" aria-label="' + label + '">' + txt + "</a>";
  };
  var group = function (d, isRet) {
    var prev = shift(d, -1), next = shift(d, 1);
    var pHref = isRet ? link(dep, prev) : link(prev, ret && ret < prev ? prev : ret);
    var nHref = isRet ? link(dep, next) : link(next, ret && ret < next ? next : ret);
    var pOff = isRet ? prev < dep : prev < today;
    var lab = W ? W[isRet ? 7 : 6] : (isRet ? "Retour" : "Aller"), early = W ? W[8] : "un jour plus tôt", late = W ? W[9] : "un jour plus tard";
    return '<div class="rs-date">' + arrow(pHref, lab + " " + early, "‹", pOff) +
      "<span>" + esc(day(d)) + "</span>" + arrow(nHref, lab + " " + late, "›", false) + "</div>";
  };
  var pax = W ? ad + " " + W[ad > 1 ? 1 : 0] + (ch ? ", " + ch + " " + W[ch > 1 ? 3 : 2] : "") + ", " + W[4]
    : ad + (ad > 1 ? " adultes" : " adulte") + (ch ? ", " + ch + (ch > 1 ? " enfants" : " enfant") : "") + ", Économie";
  var paint = function (a, b) {
    bar.innerHTML = '<button type="button" class="rs-sum" aria-expanded="false" aria-controls="tpwl-search">' +
      '<span class="rs-ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M10 2a8 8 0 0 1 6.3 12.9l5.4 5.4-1.4 1.4-5.4-5.4A8 8 0 1 1 10 2zm0 2a6 6 0 1 0 0 12 6 6 0 0 0 0-12z"/></svg></span>' +
      '<span class="rs-txt"><strong>' + esc(a) + " – " + esc(b) + "</strong><small>" + esc(pax) + "</small></span>" +
      '<span class="rs-edit">' + (W ? W[5] : "Modifier") + '</span></button>' +
      '<div class="rs-dates">' + group(dep, false) + (ret ? group(ret, true) : "") + "</div>";
    bar.querySelector(".rs-sum").addEventListener("click", function () {
      var open = form.classList.toggle("open");
      this.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) form.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  };
  // Partenaire Trip.com (lien rémunéré) : même trajet et mêmes dates ; juste sous la barre vers l'Asie et le Moyen-Orient, sous les résultats ailleurs
  var tripButton = function (cc) {
    var CITY = { CDG: "par", ORY: "par", BVA: "par", LHR: "lon", LGW: "lon", STN: "lon", LTN: "lon", LCY: "lon", FCO: "rom", CIA: "rom", MXP: "mil", LIN: "mil", BGY: "mil",
      JFK: "nyc", EWR: "nyc", LGA: "nyc", HND: "tyo", NRT: "tyo", SAW: "ist", IST: "ist", DSS: "dkr", CMN: "cas", YUL: "ymq", IAD: "was", DCA: "was", ORD: "chi", DMK: "bkk", BKK: "bkk" };
    var cityOf = function (c) { return (CITY[c] || c).toLowerCase(); }, ap = function (c) { return CITY[c] && CITY[c].toUpperCase() !== c ? c.toLowerCase() : ""; };
    var iso = function (d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
    var lg = (document.documentElement.lang || "fr").slice(0, 2), asia = /^(TH|JP|ID|SG|MY|VN|KH|PH|KR|CN|HK|TW|IN|LK|MV|AE|QA|OM|SA|BH|KW|JO)$/.test(cc);
    var TL = { fr: ["Voir aussi ce vol sur Trip.com", "souvent moins cher vers l’Asie"], en: ["Also see this flight on Trip.com", "often cheaper to Asia"] }[lg === "fr" ? "fr" : "en"];
    var o = { dcity: cityOf(from), acity: cityOf(to), dairport: ap(from), aairport: ap(to), ddate: iso(dep), rdate: ret ? iso(ret) : "", triptype: ret ? "rt" : "ow", "class": "y",
      quantity: String(ad + ch), nonstoponly: "off", searchboxarg: "t", locale: lg === "en" ? "en-GB" : "fr-FR", curr: "EUR",
      Allianceid: "11233048", SID: "335082259", trip_sub1: "escale", trip_sub2: "recherche-en-direct" }, qs = [];
    for (var k in o) if (o[k]) qs.push(k + "=" + encodeURIComponent(o[k]));
    var p = document.createElement("p"); p.className = "hl-trip" + (asia ? " top" : "");
    var a = document.createElement("a"); a.className = "btn ghost"; a.target = "_blank"; a.rel = "sponsored noopener noreferrer"; a.dataset.k = "tripcom";
    a.href = "https://www.trip.com/flights/showfarefirst?" + qs.join("&"); a.textContent = "✈️ " + TL[0]; p.appendChild(a);
    if (asia) { var n = document.createElement("span"); n.className = "small"; n.textContent = " " + TL[1]; p.appendChild(n); }
    // Vol + hôtel Trip.com (même trajet, mêmes dates) pour les villes dont on connaît l'identifiant Trip.com
    var HID = { ABJ: 3265, DSS: 856, CMN: 809, RAK: 1360, CAI: 332, LOS: 783, ACC: 1274, NBO: 825, DXB: 220, IST: 532, SAW: 532, BKK: 359, DMK: 359,
      HND: 228, NRT: 228, DPS: 723, SIN: 73, HKT: 725, CDG: 192, ORY: 192 };
    var NM = { ABJ: "Abidjan", DSS: "Dakar", CMN: "Casablanca", RAK: "Marrakech", CAI: "Le Caire", LOS: "Lagos", ACC: "Accra", NBO: "Nairobi", DXB: "Dubaï", IST: "Istanbul", SAW: "Istanbul",
      BKK: "Bangkok", DMK: "Bangkok", HND: "Tokyo", NRT: "Tokyo", DPS: "Bali", SIN: "Singapour", HKT: "Phuket", CDG: "Paris", ORY: "Paris" };
    if (ret && HID[to]) {
      var o2 = { adult: String(ad), child: String(ch), infants: "0", aCityCode: cityOf(to).toUpperCase(), dCityCode: cityOf(from).toUpperCase(), tripWay: "round-trip", classType: "ys",
        dDate: iso(dep), rDate: iso(ret), hCity: String(HID[to]), iDate: iso(dep), oDate: iso(ret), room: "1", curr: "EUR", destinationName: NM[to], isOversea: "true",
        locale: lg === "en" ? "en-GB" : "fr-FR", Allianceid: "11233048", SID: "335082259", trip_sub1: "escale", trip_sub2: "recherche-vol-hotel" }, q2 = [];
      for (var k2 in o2) q2.push(k2 + "=" + encodeURIComponent(o2[k2]));
      var b2 = document.createElement("a"); b2.className = "btn ghost"; b2.target = "_blank"; b2.rel = "sponsored noopener noreferrer"; b2.dataset.k = "tripcom-package";
      b2.href = "https://www.trip.com/packages/list?" + q2.join("&"); b2.textContent = "✈️+🏨 " + (lg === "en" ? "Flight + hotel on Trip.com" : "Vol + hôtel sur Trip.com");
      p.appendChild(document.createTextNode(" ")); p.insertBefore(b2, p.children[1] || null);
    }
    var res = document.getElementById("tpwl-tickets");
    if (asia || !res) bar.parentNode.insertBefore(p, bar.nextSibling); else res.parentNode.insertBefore(p, res.nextSibling);
  };
  paint(from, to);
  fetch("/data/airports.json").then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; }).then(function (db) {
    var name = function (c) { var a = (db || []).filter(function (x) { return x[0] === c; })[0]; return a ? a[1] + " (" + c + ")" : c; };
    var open = form.classList.contains("open");
    paint(name(from), name(to));
    if (open) bar.querySelector(".rs-sum").setAttribute("aria-expanded", "true");
    tripButton(((db || []).filter(function (x) { return x[0] === to; })[0] || [])[3] || "");
  });
})();
