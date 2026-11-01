// Pages en anglais : à côté des prix en euros, un équivalent approximatif en livres et en dollars
// (« ≈ £372 · $466 »), taux de la Banque centrale européenne (/api/fx). Les prix restent comparés en euros.
(function () {
  "use strict";
  var SEL = ".hub-price strong, #hero-price strong, .price-val";
  var rates = null;
  var fmt = function (n, c) {
    try { return new Intl.NumberFormat(c === "GBP" ? "en-GB" : "en-US", { style: "currency", currency: c, maximumFractionDigits: 0 }).format(n); }
    catch (e) { return c + " " + Math.round(n); }
  };
  var apply = function () {
    if (!rates) return;
    document.querySelectorAll(SEL).forEach(function (s) {
      if (s.getAttribute("data-fx")) return;
      var eur = parseInt(String(s.textContent).replace(/[^\d]/g, ""), 10);
      if (!eur) return;
      s.setAttribute("data-fx", "1");
      var x = document.createElement("span");
      x.className = "fx";
      x.textContent = " ≈ " + fmt(eur * rates.GBP, "GBP") + " · " + fmt(eur * rates.USD, "USD");
      s.insertAdjacentElement("afterend", x);
    });
  };
  fetch("/api/fx").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (d) {
    if (!d || !d.rates || !d.rates.GBP) return;
    rates = d.rates;
    apply();
    // Prix remplis plus tard par hub.js / route-prices.js
    new MutationObserver(apply).observe(document.body, { childList: true, subtree: true });
  });
})();
