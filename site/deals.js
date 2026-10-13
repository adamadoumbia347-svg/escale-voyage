// Page « Bons plans » : destinations les moins chères depuis plusieurs grandes villes (données /api/deals, rafraîchies toutes les 6 heures).
(function () {
  "use strict";
  var root = document.getElementById("deals");
  if (!root) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var L = {
    fr: { loc: "fr-FR", from: "dès", updated: "Mis à jour le", empty: "Les bons plans arrivent : revenez dans quelques minutes.", share: "Partager sur WhatsApp", stops: ["direct", "1 escale", " escales"], app: "fr", msg: "Bon plan : {a} → {b} dès {p} sur Escale" },
    en: { loc: "en-GB", from: "from", updated: "Updated on", empty: "Deals are on their way: check back in a few minutes.", share: "Share on WhatsApp", stops: ["direct", "1 stop", " stops"], app: "en", msg: "Deal: {a} → {b} from {p} on Escale" },
    es: { loc: "es-ES", from: "desde", updated: "Actualizado el", empty: "Las ofertas están llegando: vuelve en unos minutos.", share: "Compartir en WhatsApp", stops: ["directo", "1 escala", " escalas"], app: "es", msg: "Oferta: {a} → {b} desde {p} en Escale" },
    pt: { loc: "pt-PT", from: "desde", updated: "Atualizado a", empty: "As promoções estão a chegar: volte daqui a alguns minutos.", share: "Partilhar no WhatsApp", stops: ["direto", "1 escala", " escalas"], app: "pt", msg: "Promoção: {a} → {b} desde {p} na Escale" },
    ar: { loc: "ar-u-nu-latn", from: "من", updated: "آخر تحديث", empty: "العروض في الطريق: عد بعد دقائق.", share: "شارك على واتساب", stops: ["مباشرة", "توقف واحد", " توقفات"], app: "ar", msg: "عرض: {a} → {b} من {p} على Escale" }
  }[lang] || null;
  if (!L) return;
  var chips = document.getElementById("deal-origins"), grid = document.getElementById("deal-grid"), upd = document.getElementById("deal-updated");
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var flag = function (cc) { return cc && cc.length === 2 ? String.fromCodePoint.apply(null, cc.toUpperCase().split("").map(function (c) { return 127397 + c.charCodeAt(0); })) : "✈"; };
  var names; try { names = new Intl.DisplayNames([lang], { type: "region" }); } catch (e) { names = null; }
  var country = function (cc) { try { return names ? names.of(cc) : cc; } catch (e) { return cc; } };
  var money = function (n, cur) {
    try { return new Intl.NumberFormat(L.loc, { style: "currency", currency: cur, currencyDisplay: "narrowSymbol", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " " + cur; }
  };
  var day = function (iso) { var p = iso.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString(L.loc, { day: "numeric", month: "short" }); };
  var cur = "EUR";
  try { var c = localStorage.getItem("escale.cur"); if (c) cur = c; } catch (e) {}

  Promise.all([
    fetch("/api/deals?currency=" + cur).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }),
    fetch("/data/airports.json").then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; })
  ]).then(function (res) {
    var data = res[0], ap = {};
    (res[1] || []).forEach(function (a) { ap[a[0]] = a; });
    var origins = data && data.available ? Object.keys(data.origins).filter(function (o) { return data.origins[o].length; }) : [];
    if (!origins.length) { grid.innerHTML = '<p class="small">' + esc(L.empty) + "</p>"; return; }
    if (upd && data.updated) upd.textContent = L.updated + " " + new Date(data.updated).toLocaleString(L.loc, { day: "numeric", month: "long", hour: "2-digit", minute: "2-digit" });
    var cityOf = function (code) { return ap[code] ? ap[code][1] : code; };
    var active = origins[0];
    function paint() {
      chips.innerHTML = origins.map(function (o) {
        return '<button type="button" data-o="' + o + '" aria-pressed="' + (o === active) + '">' + esc(cityOf(o)) + " <b>" + o + "</b></button>";
      }).join("");
      grid.innerHTML = data.origins[active].map(function (d, i) {
        var a = ap[d.to], cc = a ? a[3] : "";
        var st = d.transfers === 0 ? L.stops[0] : d.transfers === 1 ? L.stops[1] : d.transfers + L.stops[2];
        var price = money(d.price, data.currency);
        var href = "/?type=vols&from=" + active + "&to=" + d.to + "&dep=" + d.dep + (d.ret ? "&ret=" + d.ret : "") + (L.app !== "fr" ? "&lang=" + L.app : "");
        var text = L.msg.replace("{a}", cityOf(active)).replace("{b}", cityOf(d.to)).replace("{p}", price) + " " + location.origin + href;
        return '<article class="deal" style="--i:' + i + '">' +
          '<a class="deal-main" href="' + esc(href) + '"><span class="deal-top"><span aria-hidden="true">' + flag(cc) + '</span><b dir="ltr">' + active + " → " + esc(d.to) + "</b></span>" +
          '<span class="deal-city">' + esc(cityOf(d.to)) + '</span><span class="deal-meta">' + esc(cc ? country(cc) : "") +
          (d.ret ? " · " + esc(day(d.dep)) + " → " + esc(day(d.ret)) : "") + " · " + esc(st) + "</span>" +
          '<span class="deal-price">' + esc(L.from) + " " + esc(price) + "</span></a>" +
          '<a class="deal-share" href="https://wa.me/?text=' + encodeURIComponent(text) + '" target="_blank" rel="noopener noreferrer">' + esc(L.share) + "</a></article>";
      }).join("");
    }
    chips.addEventListener("click", function (ev) { var b = ev.target.closest("button[data-o]"); if (b) { active = b.getAttribute("data-o"); paint(); } });
    paint();
  });
})();
