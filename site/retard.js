// « Vol retardé ou annulé : combien la compagnie te doit ? » (règlement européen 261/2004 et règle britannique UK261).
// Montant selon la distance (calculée entre les aéroports) : 250 € jusqu'à 1 500 km, 400 € jusqu'à 3 500 km (ou vol intra-UE plus long),
// 600 € au-delà ; Royaume-Uni : 220 £ / 350 £ / 520 £. Estimation : les « circonstances extraordinaires » sont exclues.
(function () {
  "use strict";
  var f = document.getElementById("rt-form");
  if (!f || !window.EscaleAC) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2), loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "en-GB";
  var T = JSON.parse(f.getAttribute("data-t")), out = document.getElementById("rt-out"), claim = f.getAttribute("data-claim");
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var EU = /^(AT|BE|BG|HR|CY|CZ|DK|EE|FI|FR|DE|GR|HU|IE|IT|LV|LT|LU|MT|NL|PL|PT|RO|SK|SI|ES|SE|IS|NO|CH|GP|MQ|GF|RE|YT|MF)$/;
  var AC = window.EscaleAC; AC.attach(f.querySelector("#rt-from")); AC.attach(f.querySelector("#rt-to"));
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var a = f.querySelector("#rt-from").dataset.code, b = f.querySelector("#rt-to").dataset.code;
    var carrier = f.querySelector("#rt-carrier").value, what = f.querySelector("#rt-what").value;
    if (!a || !b || a === b) { out.innerHTML = '<p class="tc-err">' + esc(T.err) + "</p>"; return; }
    var ca = AC.cc(a), cb = AC.cc(b), km = AC.km(a, b), depEU = EU.test(ca), arrEU = EU.test(cb), depUK = ca === "GB", arrUK = cb === "GB";
    var euCar = carrier === "eu", unk = carrier === "unknown";
    var scheme = null;
    if (depEU || (arrEU && euCar)) scheme = "eu"; else if (depUK || (arrUK && (euCar || carrier === "uk"))) scheme = "uk";
    var maybe = !scheme && unk && (arrEU || arrUK);
    var ok = what === "delay3" || what === "cancel" || what === "denied";
    var msg;
    if (!ok) msg = '<p class="tc-v">' + esc(T.no_event) + "</p>";
    else if (!scheme && !maybe) msg = '<p class="tc-v">' + esc(T.no_rule) + "</p><p>" + esc(T.no_rule_txt) + "</p>";
    else {
      var intra = depEU && arrEU, band = km == null ? 2 : km <= 1500 ? 0 : (km <= 3500 || (scheme === "eu" && intra)) ? 1 : 2;
      var amt = (scheme === "uk" ? [220, 350, 520] : [250, 400, 600])[band];
      var money = new Intl.NumberFormat(loc, { style: "currency", currency: scheme === "uk" ? "GBP" : "EUR", maximumFractionDigits: 0 }).format(amt);
      msg = '<p class="tc-v">' + esc((maybe ? T.maybe : T.yes).replace("{x}", money)) + "</p>" +
        "<ul><li>" + esc(T.l_km.replace("{k}", km == null ? "?" : km.toLocaleString(loc))) + "</li><li>" + esc(scheme === "uk" ? T.l_uk : T.l_eu) + "</li></ul>" +
        '<p class="small">' + esc(T.except) + "</p>" +
        '<div class="pr-btns"><a class="btn" href="' + esc(claim) + '" target="_blank" rel="noopener sponsored">' + esc(T.claim) + "</a></div>" +
        '<p class="small">' + esc(T.free) + "</p>";
    }
    out.innerHTML = '<div class="tc-res ' + (ok && (scheme || maybe) ? "tc-good" : "tc-mid") + '">' + msg + "</div>";
  });
})();
