// Pages trajets : « Pour toute la famille » sous le prix du haut. Estimation = prix par personne × voyageurs,
// et bouton pour partager ce budget sur WhatsApp. Chargé par route-prices.js.
(function () {
  "use strict";
  var hero = document.getElementById("hero-price");
  if (!hero) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var L = {
    fr: ["👨‍👩‍👧‍👦 Pour toute la famille", "Adultes", "Enfants", "≈ {t} aller-retour", "Partager sur WhatsApp", "{r} pour {a} adulte(s) et {c} enfant(s) : environ {t} aller-retour (dès {p} par personne). Compare les dates gratuitement :", "Estimation : prix par personne × nombre de voyageurs. Les enfants paient souvent un peu moins."],
    en: ["👨‍👩‍👧‍👦 For the whole family", "Adults", "Children", "≈ {t} return", "Share on WhatsApp", "{r} for {a} adult(s) and {c} child(ren): about {t} return (from {p} per person). Compare dates for free:", "Estimate: price per person × travellers. Children often pay a little less."],
    es: ["👨‍👩‍👧‍👦 Para toda la familia", "Adultos", "Niños", "≈ {t} ida y vuelta", "Compartir en WhatsApp", "{r} para {a} adulto(s) y {c} niño(s): unos {t} ida y vuelta (desde {p} por persona). Compara fechas gratis:", "Estimación: precio por persona × viajeros. Los niños suelen pagar algo menos."],
    pt: ["👨‍👩‍👧‍👦 Para toda a família", "Adultos", "Crianças", "≈ {t} ida e volta", "Partilhar no WhatsApp", "{r} para {a} adulto(s) e {c} criança(s): cerca de {t} ida e volta (desde {p} por pessoa). Compare datas grátis:", "Estimativa: preço por pessoa × viajantes. As crianças pagam muitas vezes um pouco menos."],
    ar: ["👨‍👩‍👧‍👦 لكل العائلة", "البالغون", "الأطفال", "≈ {t} ذهاب وعودة", "مشاركة على واتساب", "{r} لـ {a} بالغ و{c} طفل: حوالي {t} ذهابًا وعودة (من {p} للشخص). قارن التواريخ مجانًا:", "تقدير: سعر الشخص × عدد المسافرين. غالبًا ما يدفع الأطفال أقل قليلًا."],
    it: ["👨‍👩‍👧‍👦 Per tutta la famiglia", "Adulti", "Bambini", "≈ {t} andata e ritorno", "Condividi su WhatsApp", "{r} per {a} adulto/i e {c} bambino/i: circa {t} andata e ritorno (da {p} a persona). Confronta le date gratis:", "Stima: prezzo a persona × viaggiatori. I bambini spesso pagano un po' meno."]
  }[lang] || null;
  if (!L) return;
  var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn", it: "it-IT" }[lang];
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var tries = 0;
  var start = function () {
    var s = hero.querySelector("strong");
    var p = s && !hero.hidden ? parseInt(s.textContent.replace(/[^\d]/g, ""), 10) : 0;
    if (!p) { if (++tries < 20) setTimeout(start, 500); return; }
    var route = (document.querySelector("h1") || {}).textContent || "";
    var opt = function (n, sel) { var h = ""; for (var i = 0; i <= n; i++) h += "<option" + (i === sel ? " selected" : "") + ">" + i + "</option>"; return h; };
    var box = document.createElement("div"); box.className = "fam";
    box.innerHTML = "<p class=\"fam-h\"></p><div class=\"fam-row\"><label><span></span><select class=\"fam-a\">" + opt(8, 2).replace("<option>0</option>", "") + "</select></label>" +
      "<label><span></span><select class=\"fam-c\">" + opt(8, 2) + "</select></label><strong class=\"fam-t\"></strong></div>" +
      "<a class=\"fam-wa\" target=\"_blank\" rel=\"noopener\" data-k=\"partage-famille\"></a><p class=\"fam-n small\"></p>";
    box.querySelector(".fam-h").textContent = L[0];
    var spans = box.querySelectorAll("label span"); spans[0].textContent = L[1]; spans[1].textContent = L[2];
    box.querySelector(".fam-wa").textContent = L[4]; box.querySelector(".fam-n").textContent = L[6];
    var upd = function () {
      var a = +box.querySelector(".fam-a").value, c = +box.querySelector(".fam-c").value, t = money(p * (a + c));
      box.querySelector(".fam-t").textContent = L[3].replace("{t}", t);
      var msg = L[5].replace("{r}", route.trim()).replace("{a}", a).replace("{c}", c).replace("{t}", t).replace("{p}", money(p)) + " " + location.origin + location.pathname;
      box.querySelector(".fam-wa").href = "https://wa.me/?text=" + encodeURIComponent(msg);
    };
    box.addEventListener("change", upd); upd();
    hero.parentNode.insertBefore(box, hero.nextSibling);
  };
  start();
})();
