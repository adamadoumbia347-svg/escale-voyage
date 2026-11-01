// Pages trajets : grille des prix aller × retour (7 jours de départ × 7 jours de retour), comme la grille de dates de Google Flights.
// Données : /api/grille (Travelpayouts, prix trouvés récemment). La section reste masquée tant qu'aucun prix n'est connu.
(function () {
  "use strict";
  var box = document.getElementById("price-grid");
  if (!box) return;
  var from = box.getAttribute("data-from"), to = box.getAttribute("data-to");
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var L = {
    fr: { loc: "fr-FR", h: "Grille des prix aller × retour", p: "Prix aller-retour le plus bas trouvé récemment pour chaque combinaison de dates. Touchez une case pour lancer la recherche.",
      dep: "Aller", ret: "Retour", stay: "Séjour", wk: ["1 sem.", "2 sem.", "3 sem.", "4 sem."], prev: "‹ Plus tôt", next: "Plus tard ›", empty: "Pas encore de prix connus autour de ces dates. Essayez d'autres dates.", best: "Le moins cher", app: "fr" },
    en: { loc: "en-GB", h: "Price grid: departure × return", p: "Lowest round-trip price found recently for each pair of dates. Tap a cell to start the search.",
      dep: "Depart", ret: "Return", stay: "Stay", wk: ["1 wk", "2 wks", "3 wks", "4 wks"], prev: "‹ Earlier", next: "Later ›", empty: "No known prices around these dates yet. Try other dates.", best: "Cheapest", app: "en" },
    es: { loc: "es-ES", h: "Cuadrícula de precios ida × vuelta", p: "Precio de ida y vuelta más bajo encontrado recientemente para cada combinación de fechas. Toca una casilla para buscar.",
      dep: "Ida", ret: "Vuelta", stay: "Estancia", wk: ["1 sem.", "2 sem.", "3 sem.", "4 sem."], prev: "‹ Antes", next: "Después ›", empty: "Aún no hay precios conocidos en torno a estas fechas. Prueba otras fechas.", best: "El más barato", app: "es" },
    pt: { loc: "pt-PT", h: "Grelha de preços ida × volta", p: "Preço de ida e volta mais baixo encontrado recentemente para cada combinação de datas. Toque numa casa para pesquisar.",
      dep: "Ida", ret: "Volta", stay: "Estadia", wk: ["1 sem.", "2 sem.", "3 sem.", "4 sem."], prev: "‹ Mais cedo", next: "Mais tarde ›", empty: "Ainda não há preços conhecidos à volta destas datas. Experimente outras datas.", best: "O mais barato", app: "pt" },
    ar: { loc: "ar-u-nu-latn", h: "جدول الأسعار: الذهاب × العودة", p: "أقل سعر ذهاب وعودة وُجد مؤخرًا لكل تركيبة تواريخ. المس خانة لبدء البحث.",
      dep: "الذهاب", ret: "العودة", stay: "مدة الإقامة", wk: ["أسبوع", "أسبوعان", "3 أسابيع", "4 أسابيع"], prev: "أبكر ›", next: "‹ لاحقًا", empty: "لا توجد أسعار معروفة حول هذه التواريخ بعد. جرّب تواريخ أخرى.", best: "الأرخص", app: "ar" },
    it: { loc: "it-IT", h: "Griglia dei prezzi andata × ritorno", p: "Prezzo andata e ritorno più basso trovato di recente per ogni combinazione di date. Tocca una casella per avviare la ricerca.",
      dep: "Andata", ret: "Ritorno", stay: "Soggiorno", wk: ["1 sett.", "2 sett.", "3 sett.", "4 sett."], prev: "‹ Prima", next: "Dopo ›", empty: "Ancora nessun prezzo noto intorno a queste date. Prova altre date.", best: "Il più economico", app: "it" },
    de: { loc: "de-DE", h: "Preistabelle: Hinflug × Rückflug", p: "Niedrigster Preis für Hin- und Rückflug, kürzlich gefunden, für jede Datumskombination. Tippe auf ein Feld, um die Suche zu starten.",
      dep: "Hinflug", ret: "Rückflug", stay: "Aufenthalt", wk: ["1 Wo.", "2 Wo.", "3 Wo.", "4 Wo."], prev: "‹ Früher", next: "Später ›", empty: "Noch keine bekannten Preise rund um diese Daten. Versuche andere Daten.", best: "Am günstigsten", app: "de" }
  }[lang] || null;
  if (!L) return;
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var pad = function (n) { return String(n).padStart(2, "0"); };
  var iso = function (d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); };
  var add = function (s, n) { var p = s.split("-"); var d = new Date(+p[0], +p[1] - 1, +p[2] + n); return iso(d); };
  var short = function (s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString(L.loc, { weekday: "short", day: "numeric", month: "short" }); };
  var compact = function (n) { return n >= 10000 ? Math.round(n / 1000) + "k" : String(Math.round(n)); };
  var money = function (n, c) {
    try { return new Intl.NumberFormat(L.loc, { style: "currency", currency: c, currencyDisplay: "narrowSymbol", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " " + c; }
  };
  var today = iso(new Date());
  var dep = add(today, 30), weeks = 2, req = 0, shown = false, cache = {};

  box.innerHTML = '<h2>' + esc(L.h) + '</h2><p class="small">' + esc(L.p) + '</p>' +
    '<div class="pg-ctrl"><div class="chips pg-stay" role="group" aria-label="' + esc(L.stay) + '">' +
    L.wk.map(function (w, i) { return '<button type="button" data-w="' + (i + 1) + '" aria-pressed="' + (i + 1 === weeks) + '">' + esc(w) + "</button>"; }).join("") +
    '</div><div class="pg-nav"><button type="button" class="btn ghost" data-shift="-7">' + esc(L.prev) + '</button><button type="button" class="btn ghost" data-shift="7">' + esc(L.next) + "</button></div></div>" +
    '<div class="pg-wrap"><table class="pg-table"></table></div><p class="small pg-status" role="status"></p>';
  var table = box.querySelector(".pg-table"), status = box.querySelector(".pg-status");

  box.addEventListener("click", function (ev) {
    var w = ev.target.closest("button[data-w]"), s = ev.target.closest("button[data-shift]");
    if (w) { weeks = +w.getAttribute("data-w"); box.querySelectorAll("button[data-w]").forEach(function (b) { b.setAttribute("aria-pressed", String(b === w)); }); load(); }
    if (s) { var nd = add(dep, +s.getAttribute("data-shift")); if (add(nd, -3) > today) { dep = nd; load(); } }
  });

  function load() {
    var id = ++req, ret = add(dep, weeks * 7), key = dep + ret;
    box.setAttribute("aria-busy", "true");
    var p = cache[key] || (cache[key] = fetch("/api/grille?from=" + from + "&to=" + to + "&dep=" + dep + "&ret=" + ret)
      .then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }));
    p.then(function (d) {
      if (id !== req) return;
      box.removeAttribute("aria-busy");
      render(d, ret);
    });
  }

  function render(d, ret) {
    var deps = [-3, -2, -1, 0, 1, 2, 3].map(function (i) { return add(dep, i); });
    var rets = [-3, -2, -1, 0, 1, 2, 3].map(function (i) { return add(ret, i); });
    var cells = (d && d.available && d.cells) || {}, cur = (d && d.currency) || "EUR";
    var prices = Object.keys(cells).map(function (k) { return cells[k].price; }).sort(function (a, b) { return a - b; });
    if (!prices.length) {
      if (!shown) return;  // rien à montrer : la section reste masquée
      table.innerHTML = ""; status.textContent = L.empty; return;
    }
    shown = true; box.hidden = false;
    var min = prices[0], q = function (p) { var i = prices.indexOf(p); return Math.min(4, Math.floor(i / prices.length * 5)); };
    var app = L.app !== "fr" ? "&lang=" + L.app : "";
    var head = '<thead><tr><th scope="col" class="pg-corner"><span>' + esc(L.ret) + " ↓</span><span>" + esc(L.dep) + " →</span></th>" +
      deps.map(function (x) { return '<th scope="col">' + esc(short(x)) + "</th>"; }).join("") + "</tr></thead>";
    var body = "<tbody>" + rets.map(function (r) {
      return '<tr><th scope="row">' + esc(short(r)) + "</th>" + deps.map(function (x) {
        if (r <= x || x < today) return '<td class="pg-off"></td>';
        var c = cells[x + "|" + r];
        if (!c) return '<td class="pg-none">·</td>';
        var lab = money(c.price, cur) + " · " + short(x) + " → " + short(r) + (c.price === min ? " · " + L.best : "");
        return '<td><a class="pg-cell t' + q(c.price) + (c.price === min ? " pg-min" : "") + '" href="/?type=vols&from=' + from + "&to=" + to + "&dep=" + x + "&ret=" + r + app +
          '" aria-label="' + esc(lab) + '" title="' + esc(lab) + '">' + esc(compact(c.price)) + "</a></td>";
      }).join("") + "</tr>";
    }).join("") + "</tbody>";
    table.innerHTML = head + body;
    status.textContent = L.best + (lang === "fr" ? " : " : ": ") + money(min, cur);
  }
  load();
})();
