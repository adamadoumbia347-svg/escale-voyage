// Pages trajets : courbe « prix selon la date de départ » sur les 3 prochains mois (prix aller-retour le plus bas par jour).
// Données : /api/calendar (mêmes réponses que le calendrier des prix). Une seule série : pas de légende, le titre la nomme.
// Survol / toucher : repère vertical et bulle (date, prix) ; clic : lance la recherche à cette date. Le calendrier sert de vue tableau.
(function () {
  "use strict";
  var box = document.getElementById("price-curve");
  if (!box) return;
  var from = box.getAttribute("data-from"), to = box.getAttribute("data-to");
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var L = {
    fr: { loc: "fr-FR", h: "Prix selon la date de départ", p: "Prix aller-retour le plus bas trouvé récemment, jour par jour, sur les 3 prochains mois. Touchez la courbe pour voir un jour, puis lancez la recherche.", min: "le moins cher", go: "Rechercher", app: "fr" },
    en: { loc: "en-GB", h: "Price by departure date", p: "Lowest round-trip price found recently, day by day, over the next 3 months. Tap the curve to see a day, then start the search.", min: "cheapest", go: "Search", app: "en" },
    es: { loc: "es-ES", h: "Precio según la fecha de salida", p: "Precio de ida y vuelta más bajo encontrado recientemente, día a día, en los próximos 3 meses. Toca la curva para ver un día y busca.", min: "el más barato", go: "Buscar", app: "es" },
    pt: { loc: "pt-PT", h: "Preço conforme a data de partida", p: "Preço de ida e volta mais baixo encontrado recentemente, dia a dia, nos próximos 3 meses. Toque na curva para ver um dia e pesquise.", min: "o mais barato", go: "Pesquisar", app: "pt" },
    ar: { loc: "ar-u-nu-latn", h: "السعر حسب تاريخ المغادرة", p: "أقل سعر ذهاب وعودة وُجد مؤخرًا، يومًا بيوم، خلال الأشهر الثلاثة القادمة. المس المنحنى لرؤية يوم ثم ابدأ البحث.", min: "الأرخص", go: "بحث", app: "ar" },
    it: { loc: "it-IT", h: "Prezzo in base alla data di partenza", p: "Prezzo andata e ritorno più basso trovato di recente, giorno per giorno, nei prossimi 3 mesi. Tocca la curva per vedere un giorno, poi avvia la ricerca.", min: "il più economico", go: "Cerca", app: "it" },
    de: { loc: "de-DE", h: "Preis nach Abflugdatum", p: "Niedrigster Preis für Hin- und Rückflug, kürzlich gefunden, Tag für Tag in den nächsten 3 Monaten. Tippe auf die Kurve, um einen Tag zu sehen, und starte die Suche.", min: "am günstigsten", go: "Suchen", app: "de" }
  }[lang] || null;
  if (!L) return;
  var pad = function (n) { return String(n).padStart(2, "0"); };
  var now = new Date(), today = now.getFullYear() + "-" + pad(now.getMonth() + 1) + "-" + pad(now.getDate());
  var months = [0, 1, 2].map(function (i) { var d = new Date(now.getFullYear(), now.getMonth() + i, 1); return d.getFullYear() + "-" + pad(d.getMonth() + 1); });
  var NS = "http://www.w3.org/2000/svg";
  var el = function (n, a) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); return e; };
  var dayMs = function (s) { var p = s.split("-"); return Date.UTC(+p[0], +p[1] - 1, +p[2]); };
  var label = function (s, o) { return new Date(dayMs(s)).toLocaleDateString(L.loc, Object.assign({ timeZone: "UTC" }, o)); };

  Promise.all(months.map(function (m) {
    return fetch("/api/calendar?from=" + from + "&to=" + to + "&month=" + m).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
  })).then(function (res) {
    var pts = [], cur = "EUR";
    res.forEach(function (d) {
      if (!d || !d.available) return;
      cur = d.currency || cur;
      Object.keys(d.days || {}).forEach(function (day) { if (day >= today && d.days[day].price) pts.push({ day: day, p: d.days[day].price, ret: d.days[day].ret }); });
    });
    pts.sort(function (a, b) { return a.day < b.day ? -1 : 1; });
    if (pts.length < 5) return;  // trop peu de jours connus : la section reste masquée
    draw(pts, cur);
  });

  function draw(pts, cur) {
    box.hidden = false;  // visible avant de mesurer la largeur
    var money = function (n) {
      try { return new Intl.NumberFormat(L.loc, { style: "currency", currency: cur, currencyDisplay: "narrowSymbol", maximumFractionDigits: 0 }).format(n); }
      catch (e) { return Math.round(n) + " " + cur; }
    };
    var W = Math.round(Math.max(300, Math.min(640, box.clientWidth || 640))), H = 200, ml = 4, mr = 4, mt = 26, mb = 26;  // largeur réelle : texte à sa vraie taille
    var x0 = dayMs(today), x1 = dayMs(months[2] + "-28") + 3 * 864e5;
    var ps = pts.map(function (q) { return q.p; }), lo = Math.min.apply(null, ps), hi = Math.max.apply(null, ps);
    var span = Math.max(hi - lo, hi * 0.1), y0 = Math.max(0, lo - span * 0.15), y1 = hi + span * 0.1;
    var X = function (s) { return ml + (dayMs(s) - x0) / (x1 - x0) * (W - ml - mr); };
    var Y = function (p) { return mt + (1 - (p - y0) / (y1 - y0)) * (H - mt - mb); };
    box.innerHTML = "<h2></h2><p class='small'></p><div class='pc-plot'></div>";
    box.querySelector("h2").textContent = L.h;
    box.querySelector("p").textContent = L.p;
    var svg = el("svg", { viewBox: "0 0 " + W + " " + H, class: "pc-svg", role: "img", "aria-label": L.h + " : " + money(lo) + " – " + money(hi) });
    // Grille horizontale discrète (bas et haut de l'échelle), axe des mois
    [lo, hi].forEach(function (v) {
      svg.appendChild(el("line", { x1: ml, x2: W - mr, y1: Y(v), y2: Y(v), class: "pc-grid" }));
      var t = el("text", { x: W - mr, y: Y(v) - 5, "text-anchor": "end", class: "pc-axis" }); t.textContent = money(v); svg.appendChild(t);
    });
    months.forEach(function (m, i) {
      var s = i === 0 ? today : m + "-01", x = X(s);
      if (i > 0) svg.appendChild(el("line", { x1: x, x2: x, y1: mt - 6, y2: H - mb, class: "pc-grid" }));
      var t = el("text", { x: x + 4, y: H - 8, class: "pc-axis" }); t.textContent = label(m + "-01", { month: "long" }); svg.appendChild(t);
    });
    var d = pts.map(function (q, i) { return (i ? "L" : "M") + X(q.day).toFixed(1) + " " + Y(q.p).toFixed(1); }).join(" ");
    svg.appendChild(el("path", { d: d, class: "pc-line" }));
    // Point le moins cher : marqueur et étiquette directe (une seule, pas un chiffre sur chaque point)
    var best = pts.reduce(function (a, b) { return b.p < a.p ? b : a; });
    svg.appendChild(el("circle", { cx: X(best.day), cy: Y(best.p), r: 5, class: "pc-min" }));
    var bt = el("text", { x: X(best.day), y: Y(best.p) + 18, "text-anchor": X(best.day) > W - 70 ? "end" : X(best.day) < 70 ? "start" : "middle", class: "pc-label" });
    bt.textContent = money(best.p) + " · " + label(best.day, { day: "numeric", month: "short" });
    svg.appendChild(bt);
    // Couche de survol : repère vertical + marqueur + bulle
    var cross = el("line", { y1: mt - 6, y2: H - mb, class: "pc-cross", visibility: "hidden" });
    var dot = el("circle", { r: 5, class: "pc-dot", visibility: "hidden" });
    svg.appendChild(cross); svg.appendChild(dot);
    var hit = el("rect", { x: 0, y: 0, width: W, height: H, fill: "transparent", class: "pc-hit" });
    svg.appendChild(hit);
    var plot = box.querySelector(".pc-plot");
    plot.appendChild(svg);
    var tip = document.createElement("a");
    tip.className = "pc-tip"; tip.hidden = true;
    plot.appendChild(tip);
    var app = L.app !== "fr" ? "&lang=" + L.app : "";
    var pick = function (ev) {
      var r = svg.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width * W;
      var q = pts.reduce(function (a, b) { return Math.abs(X(b.day) - x) < Math.abs(X(a.day) - x) ? b : a; });
      var cx = X(q.day), cy = Y(q.p);
      cross.setAttribute("x1", cx); cross.setAttribute("x2", cx); cross.setAttribute("visibility", "visible");
      dot.setAttribute("cx", cx); dot.setAttribute("cy", cy); dot.setAttribute("visibility", "visible");
      tip.innerHTML = "<span></span><strong></strong><em></em>";
      tip.children[0].textContent = label(q.day, { weekday: "short", day: "numeric", month: "short" });
      tip.children[1].textContent = money(q.p) + (q === best ? " · " + L.min : "");
      tip.children[2].textContent = L.go + " →";
      tip.href = "/?type=vols&from=" + from + "&to=" + to + "&dep=" + q.day + (q.ret ? "&ret=" + q.ret : "") + app;
      tip.hidden = false;
      var left = cx / W * r.width, tw = tip.offsetWidth;
      tip.style.left = Math.max(0, Math.min(r.width - tw, left - tw / 2)) + "px";
      tip.style.top = Math.max(0, cy / H * r.height - tip.offsetHeight - 12) + "px";
    };
    hit.addEventListener("pointermove", pick);
    hit.addEventListener("pointerdown", pick);
    plot.addEventListener("pointerleave", function (ev) {
      if (ev.pointerType === "mouse") { cross.setAttribute("visibility", "hidden"); dot.setAttribute("visibility", "hidden"); tip.hidden = true; }
    });
    box.hidden = false;
  }
})();
