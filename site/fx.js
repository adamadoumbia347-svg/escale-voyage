// À côté des prix en euros (pages trajets et destinations), un équivalent approximatif dans la monnaie du visiteur :
// « dès 432 € ≈ 283 400 F CFA ». Monnaie : celle choisie sur l'accueil (escale.cur), sinon celle du pays du visiteur (/api/geo).
// Sur les pages en anglais sans monnaie connue : livres et dollars. Taux : /api/fx (12 h). Les prix restent comparés en euros.
(function () {
  "use strict";
  var SEL = ".hub-price strong, #hero-price strong, .price-val";
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn", it: "it-IT", de: "de-DE", nl: "nl-NL" }[lang] || "fr-FR";
  var BY_COUNTRY = { GB: "GBP", US: "USD", CA: "CAD", CH: "CHF", MA: "MAD", DZ: "DZD", TN: "TND", EG: "EGP", NG: "NGN", GH: "GHS",
    KE: "KES", ZA: "ZAR", AE: "AED", SA: "SAR", QA: "QAR", ET: "ETB", RW: "RWF", CD: "CDF", GN: "GNF", MR: "MRU", GM: "GMD", CV: "CVE",
    AO: "AOA", MZ: "MZN", TZ: "TZS", UG: "UGX", SE: "SEK", NO: "NOK", DK: "DKK", PL: "PLN", TR: "TRY", BR: "BRL", HT: "HTG",
    SN: "XOF", ML: "XOF", CI: "XOF", BF: "XOF", NE: "XOF", TG: "XOF", BJ: "XOF", GW: "XOF",
    CM: "XAF", GA: "XAF", CG: "XAF", TD: "XAF", CF: "XAF", GQ: "XAF" };
  var NOTE = { fr: "Équivalent indicatif, les prix sont comparés en euros.", en: "Approximate equivalent: prices are compared in euros.",
    es: "Equivalente aproximado: los precios se comparan en euros.", pt: "Equivalente aproximado: os preços são comparados em euros.",
    ar: "قيمة تقريبية: تُقارن الأسعار باليورو.", it: "Equivalente indicativo: i prezzi sono confrontati in euro.",
    de: "Ungefährer Gegenwert: Die Preise werden in Euro verglichen.", nl: "Indicatieve tegenwaarde: de prijzen worden in euro vergeleken." }[lang] || "";
  var store = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } };
  var sget = function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } };
  var sset = function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} };
  var getJSON = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };

  function currencies() {
    // Page « pays » (/ci/, /ng/…) : la monnaie de la page ; sinon celle choisie sur l'accueil ou celle du pays du visiteur
    var forced = document.querySelector('meta[name="escale-cur"]');
    if (forced) return Promise.resolve([forced.content]);
    var c = store("escale.cur") || sget("escale.fxcur");
    if (c) return Promise.resolve(c === "EUR" ? [] : [c]);
    return getJSON("/api/geo").then(function (g) {
      var cc = g && g.country, cur = (cc && BY_COUNTRY[cc]) || (cc ? "EUR" : "");
      if (cur) sset("escale.fxcur", cur);
      if (cur && cur !== "EUR") return [cur];
      return !cur && lang === "en" ? ["GBP", "USD"] : [];
    });
  }
  var fmt = function (n, c) {
    var big = n >= 1000;
    try { return new Intl.NumberFormat(loc, { style: "currency", currency: c, currencyDisplay: "narrowSymbol", maximumFractionDigits: 0, maximumSignificantDigits: big ? 3 : undefined }).format(n); }
    catch (e) { return Math.round(n) + " " + c; }
  };

  currencies().then(function (curs) {
    if (!curs.length) return;
    return getJSON("/api/fx").then(function (d) {
      if (!d || !d.rates) return;
      curs = curs.filter(function (c) { return d.rates[c]; });
      if (!curs.length) return;
      var noted = false;
      var apply = function () {
        document.querySelectorAll(SEL).forEach(function (s) {
          if (s.getAttribute("data-fx")) return;
          var eur = parseInt(String(s.textContent).replace(/[^\d]/g, ""), 10);
          if (!eur) return;
          s.setAttribute("data-fx", "1");
          var x = document.createElement("span");
          x.className = "fx";
          x.textContent = " ≈ " + curs.map(function (c) { return fmt(eur * d.rates[c], c); }).join(" · ");
          s.insertAdjacentElement("afterend", x);
          if (!noted) {
            noted = true;
            var box = s.closest("#route-prices, .hub, .board");
            var target = box && box.id === "route-prices" ? box : document.querySelector(".hub") || box;
            if (target) {
              var p = document.createElement("p");
              p.className = "small fx-note";
              p.textContent = "≈ " + NOTE + " ";
              if (d.source === "er-api") {
                var a = document.createElement("a");
                a.href = "https://www.exchangerate-api.com"; a.target = "_blank"; a.rel = "noopener"; a.textContent = "Rates By Exchange Rate API";
                p.appendChild(a);
              }
              target.appendChild(p);
            }
          }
        });
      };
      apply();
      // Prix remplis plus tard par hub.js / route-prices.js
      var mo = new MutationObserver(apply);
      mo.observe(document.body, { childList: true, subtree: true });
      setTimeout(function () { mo.disconnect(); }, 30000);
    });
  });
})();
