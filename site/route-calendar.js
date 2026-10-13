// Pages trajets : calendrier des prix (prix aller-retour le plus bas par jour de départ), coloré du moins cher au plus cher.
// Données : /api/calendar (Travelpayouts). Sans données, la section reste masquée.
(function () {
  "use strict";
  var box = document.getElementById("route-calendar");
  if (!box) return;
  var from = box.getAttribute("data-from"), to = box.getAttribute("data-to");
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var L = {
    fr: { loc: "fr-FR", cheap: "Moins cher", dear: "Plus cher", none: "Pas de prix connu ce jour-là", empty: "Pas encore de prix connus pour ce mois.", app: "fr", stops: ["direct", "1 escale", " escales"] },
    en: { loc: "en-GB", cheap: "Cheaper", dear: "More expensive", none: "No known price that day", empty: "No known prices for this month yet.", app: "en", stops: ["direct", "1 stop", " stops"] },
    es: { loc: "es-ES", cheap: "Más barato", dear: "Más caro", none: "Sin precio conocido ese día", empty: "Aún no hay precios para este mes.", app: "es", stops: ["directo", "1 escala", " escalas"] },
    pt: { loc: "pt-PT", cheap: "Mais barato", dear: "Mais caro", none: "Sem preço conhecido nesse dia", empty: "Ainda não há preços para este mês.", app: "pt", stops: ["direto", "1 escala", " escalas"] },
    ar: { loc: "ar-u-nu-latn", cheap: "أرخص", dear: "أغلى", none: "لا يوجد سعر معروف لهذا اليوم", empty: "لا توجد أسعار معروفة لهذا الشهر بعد.", app: "ar", stops: ["مباشرة", "توقف واحد", " توقفات"] }
  }[lang] || null;
  if (!L) return;
  var monthsEl = box.querySelector(".cal-months"), gridEl = box.querySelector(".cal-grid"), legendEl = box.querySelector(".cal-legend");
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var pad = function (n) { return String(n).padStart(2, "0"); };
  var money = function (n, cur) {
    try { return new Intl.NumberFormat(L.loc, { style: "currency", currency: cur, currencyDisplay: "narrowSymbol", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " " + cur; }
  };
  var compact = function (n) { return n >= 10000 ? Math.round(n / 1000) + "k" : String(Math.round(n)); };
  var now = new Date(), today = now.getFullYear() + "-" + pad(now.getMonth() + 1) + "-" + pad(now.getDate());
  var months = [0, 1, 2].map(function (i) { var d = new Date(now.getFullYear(), now.getMonth() + i, 1); return d.getFullYear() + "-" + pad(d.getMonth() + 1); });
  var cache = {}, current = months[0];

  function load(m) {
    if (!cache[m]) cache[m] = fetch("/api/calendar?from=" + from + "&to=" + to + "&month=" + m).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
    return cache[m];
  }
  function paintMonths() {
    monthsEl.innerHTML = months.map(function (m) {
      var p = m.split("-");
      var label = new Date(+p[0], +p[1] - 1, 1).toLocaleDateString(L.loc, { month: "long" });
      return '<button type="button" data-m="' + m + '" aria-pressed="' + (m === current) + '">' + esc(label) + "</button>";
    }).join("");
  }
  function render(m, data) {
    var p = m.split("-"), y = +p[0], mo = +p[1] - 1;
    var first = new Date(y, mo, 1), nDays = new Date(y, mo + 1, 0).getDate();
    var offset = (first.getDay() + 6) % 7; // lundi en premier
    var days = (data && data.days) || {}, prices = Object.keys(days).filter(function (d) { return d >= today; }).map(function (d) { return days[d].price; });
    var min = Math.min.apply(null, prices), max = Math.max.apply(null, prices);
    var heads = [];
    for (var i = 0; i < 7; i++) heads.push(new Date(2024, 0, 1 + i).toLocaleDateString(L.loc, { weekday: "narrow" }));
    var cells = heads.map(function (h) { return '<span class="cal-head" aria-hidden="true">' + esc(h) + "</span>"; });
    for (var k = 0; k < offset; k++) cells.push('<span class="cal-empty"></span>');
    for (var d = 1; d <= nDays; d++) {
      var iso = m + "-" + pad(d), info = days[iso];
      if (iso < today || !info) {
        cells.push('<span class="cal-day off" title="' + esc(L.none) + '"><b>' + d + "</b></span>");
        continue;
      }
      // 0 = le moins cher, 4 = le plus cher
      var tier = max > min ? Math.min(4, Math.floor(((info.price - min) / (max - min)) * 5)) : 0;
      var href = "/?type=vols&from=" + from + "&to=" + to + "&dep=" + iso + (info.ret ? "&ret=" + info.ret : "") + (L.app !== "fr" ? "&lang=" + L.app : "");
      var st = info.transfers === 0 ? L.stops[0] : info.transfers === 1 ? L.stops[1] : info.transfers + L.stops[2];
      cells.push('<a class="cal-day t' + tier + '" href="' + esc(href) + '" title="' + esc(money(info.price, data.currency) + " · " + st) + '"><b>' + d + "</b><span>" + esc(compact(info.price)) + "</span></a>");
    }
    gridEl.innerHTML = cells.join("");
    legendEl.innerHTML = prices.length
      ? esc(L.cheap) + ' <span class="cal-scale" aria-hidden="true"><i class="t0"></i><i class="t1"></i><i class="t2"></i><i class="t3"></i><i class="t4"></i></span> ' + esc(L.dear) +
        " · " + esc(money(min, data.currency)) + " – " + esc(money(max, data.currency))
      : esc(L.empty);
  }
  function show(m) {
    current = m; paintMonths();
    load(m).then(function (data) { if (current === m) render(m, data && data.available ? data : null); });
  }
  monthsEl.addEventListener("click", function (ev) { var b = ev.target.closest("button[data-m]"); if (b) show(b.getAttribute("data-m")); });

  // N'affiche la section que si au moins un des 3 mois a des prix ; commence par le premier mois qui en a
  Promise.all(months.map(load)).then(function (all) {
    var idx = all.findIndex(function (d) { return d && d.available && Object.keys(d.days || {}).some(function (k) { return k >= today; }); });
    if (idx < 0) return;
    box.hidden = false;
    show(months[idx]);
  });
})();
