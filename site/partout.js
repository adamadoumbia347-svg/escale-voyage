// Page « Partout » : carte du monde avec les prix aller-retour les moins chers depuis la ville choisie (données /api/explore).
(function () {
  "use strict";
  var root = document.getElementById("anywhere");
  if (!root) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var L = {
    fr: { loc: "fr-FR", from: "dès", load: "Recherche des meilleurs prix…", none: "Pas encore de prix pour ce mois depuis cette ville. Essayez un autre mois.",
      count: "{n} destinations, du moins cher au plus cher", over: "{n} destinations au-dessus de votre budget sont masquées.", stops: ["direct", "1 escale", "{n} escales"], see: "Voir les vols", any: "Tous budgets" },
    en: { loc: "en-GB", from: "from", load: "Looking for the best prices…", none: "No prices yet for this month from this city. Try another month.",
      count: "{n} destinations, cheapest first", over: "{n} destinations above your budget are hidden.", stops: ["direct", "1 stop", "{n} stops"], see: "See flights", any: "Any budget" },
    es: { loc: "es-ES", from: "desde", load: "Buscando los mejores precios…", none: "Aún no hay precios para este mes desde esta ciudad. Prueba otro mes.",
      count: "{n} destinos, del más barato al más caro", over: "{n} destinos por encima de tu presupuesto están ocultos.", stops: ["directo", "1 escala", "{n} escalas"], see: "Ver vuelos", any: "Cualquier presupuesto" },
    pt: { loc: "pt-PT", from: "desde", load: "A procurar os melhores preços…", none: "Ainda não há preços para este mês a partir desta cidade. Experimente outro mês.",
      count: "{n} destinos, do mais barato ao mais caro", over: "{n} destinos acima do seu orçamento estão ocultos.", stops: ["direto", "1 escala", "{n} escalas"], see: "Ver voos", any: "Qualquer orçamento" },
    ar: { loc: "ar-u-nu-latn", from: "من", load: "جارٍ البحث عن أفضل الأسعار…", none: "لا توجد أسعار بعد لهذا الشهر من هذه المدينة. جرّب شهرًا آخر.",
      count: "{n} وجهة، من الأرخص إلى الأغلى", over: "تم إخفاء {n} وجهة تتجاوز ميزانيتك.", stops: ["مباشرة", "توقف واحد", "{n} توقفات"], see: "اعرض الرحلات", any: "أي ميزانية" }
  }[lang] || null;
  if (!L) return;
  var W = 2000, K = W / 360, TOP = 84;
  var X = function (lon) { return (lon + 180) * K; }, Y = function (lat) { return (TOP - lat) * K; };
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var fmt = function (s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); };
  var flag = function (cc) { return cc && cc.length === 2 ? String.fromCodePoint.apply(null, cc.toUpperCase().split("").map(function (c) { return 127397 + c.charCodeAt(0); })) : "✈"; };
  var names; try { names = new Intl.DisplayNames([lang], { type: "region" }); } catch (e) { names = null; }
  var country = function (cc) { try { return names && cc ? names.of(cc) : cc || ""; } catch (e) { return cc || ""; } };
  var cur = "EUR";
  try { var c0 = localStorage.getItem("escale.cur"); if (c0) cur = c0; } catch (e) {}
  var money = function (n, c) {
    try { return new Intl.NumberFormat(L.loc, { style: "currency", currency: c, currencyDisplay: "narrowSymbol", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " " + c; }
  };
  var iso = function (d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0"); };

  var sel = $("any-from"), months = $("any-months"), range = $("any-max"), out = $("any-max-out");
  var svg = $("any-dots"), tip = $("any-tip"), list = $("any-list"), status = $("any-status"), scroller = $("any-scroll");
  var ap = {}, items = [], currency = cur, month = null, max = Infinity, req = 0;

  // Mois : celui en cours et les cinq suivants (le mois prochain par défaut)
  var ms = [];
  for (var i = 0; i < 6; i++) { var d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + i); ms.push(iso(d)); }
  month = ms[1];
  months.innerHTML = ms.map(function (m) {
    var p = m.split("-"), label = new Date(+p[0], +p[1] - 1, 1).toLocaleDateString(L.loc, { month: "short", year: "numeric" });
    return '<button type="button" data-m="' + m + '" aria-pressed="' + (m === month) + '">' + esc(label) + "</button>";
  }).join("");
  months.addEventListener("click", function (ev) {
    var b = ev.target.closest("button[data-m]"); if (!b) return;
    month = b.getAttribute("data-m");
    months.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
    load();
  });

  // Ville de départ : dernier choix, sinon la ville la plus proche (pays du visiteur), sinon Paris
  var codes = [].map.call(sel.options, function (o) { return o.value; });
  var BY_COUNTRY = { FR: "CDG", BE: "BRU", LU: "BRU", CH: "GVA", GB: "LHR", IE: "LHR", US: "JFK", CA: "YUL", NL: "AMS", DE: "FRA", AT: "FRA", ES: "MAD", PT: "LIS", IT: "FCO" };
  var saved = null;
  try { saved = localStorage.getItem("escale.any.from") || ((localStorage.getItem("escale.from") || "").match(/\(([A-Z]{3})\)/) || [])[1]; } catch (e) {}
  if (saved && codes.indexOf(saved) >= 0) sel.value = saved;
  sel.addEventListener("change", function () { try { localStorage.setItem("escale.any.from", sel.value); } catch (e) {} load(); });

  range.addEventListener("input", function () {
    var vmax = +range.max;
    max = +range.value >= vmax ? Infinity : +range.value;
    out.textContent = max === Infinity ? L.any : "≤ " + money(max, currency);
    paint();
  });

  function load() {
    var id = ++req, from = sel.value;
    status.textContent = L.load;
    root.setAttribute("aria-busy", "true");
    fetch("/api/explore?from=" + from + "&month=" + month + "&currency=" + cur).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (data) {
      if (id !== req) return;
      root.removeAttribute("aria-busy");
      currency = data && data.currency || cur;
      items = (data && data.available && data.items || []).filter(function (it) { return ap[it.to] && ap[it.to][5] != null; });
      var prices = items.map(function (it) { return it.price; });
      if (prices.length) {
        var lo = Math.floor(Math.min.apply(null, prices)), hi = Math.ceil(Math.max.apply(null, prices));
        range.min = String(lo); range.max = String(hi); range.step = String(Math.max(1, Math.round((hi - lo) / 40)));
        range.value = String(hi); max = Infinity; out.textContent = L.any;
      }
      range.disabled = !prices.length;
      paint();
    });
  }

  function tier(p, lo, hi) { return hi > lo ? Math.min(4, Math.floor(((p - lo) / (hi - lo)) * 5)) : 0; }
  function href(it) {
    var q = "type=vols&from=" + sel.value + "&to=" + it.to + "&dep=" + String(it.departure_at).slice(0, 10) + (it.return_at ? "&ret=" + String(it.return_at).slice(0, 10) : "");
    return "/?" + q + (lang !== "fr" ? "&lang=" + lang : "");
  }
  function stopsText(n) { return n === 0 ? L.stops[0] : n === 1 ? L.stops[1] : fmt(L.stops[2], { n: n }); }
  function paint() {
    var o = ap[sel.value], ox = o ? X(o[6]) : 0, oy = o ? Y(o[5]) : 0;
    var shown = items.filter(function (it) { return it.price <= max; });
    var prices = items.map(function (it) { return it.price; }), lo = Math.min.apply(null, prices), hi = Math.max.apply(null, prices);
    var dots = shown.slice().reverse().map(function (it) {
      var a = ap[it.to], x = X(a[6]).toFixed(1), y = Y(a[5]).toFixed(1);
      var label = a[1] + " (" + it.to + ") : " + L.from + " " + money(it.price, currency);
      return '<a href="' + esc(href(it)) + '" class="any-dot t' + tier(it.price, lo, hi) + '" data-to="' + it.to + '" aria-label="' + esc(label) + '">' +
        '<circle cx="' + x + '" cy="' + y + '" r="26" class="hit"/><circle cx="' + x + '" cy="' + y + '" r="13" class="pt"/></a>';
    }).join("");
    svg.innerHTML = '<path id="any-arc" class="any-arc" d=""/>' + dots +
      (o ? '<g class="any-origin"><circle cx="' + ox.toFixed(1) + '" cy="' + oy.toFixed(1) + '" r="30" class="ring"/><circle cx="' + ox.toFixed(1) + '" cy="' + oy.toFixed(1) + '" r="12" class="core"/></g>' : "");
    if (!items.length) {
      status.textContent = L.none; list.innerHTML = ""; list.setAttribute("data-done", ""); return;
    }
    status.textContent = fmt(L.count, { n: shown.length }) + (shown.length < items.length ? " " + fmt(L.over, { n: items.length - shown.length }) : "");
    list.innerHTML = shown.map(function (it) {
      var a = ap[it.to], dep = String(it.departure_at).slice(0, 10), ret = it.return_at ? String(it.return_at).slice(0, 10) : "";
      var day = function (s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString(L.loc, { day: "numeric", month: "short" }); };
      return '<li><a class="any-item" href="' + esc(href(it)) + '" data-to="' + it.to + '"><span class="any-flag" aria-hidden="true">' + flag(a[3]) + "</span>" +
        '<span class="any-name"><strong>' + esc(a[1]) + '</strong><small>' + esc(country(a[3])) + " · " + esc(day(dep)) + (ret ? " → " + esc(day(ret)) : "") + " · " + esc(stopsText(it.transfers)) + "</small></span>" +
        '<span class="any-price t' + tier(it.price, lo, hi) + '">' + esc(money(it.price, currency)) + "</span></a></li>";
    }).join("");
    if (o && scroller && scroller.scrollWidth > scroller.clientWidth && !scroller.dataset.done) {
      scroller.dataset.done = "1";
      scroller.scrollLeft = Math.max(0, ox / W * scroller.scrollWidth - scroller.clientWidth / 2);
    }
  }

  // Survol ou focus d'une destination : trajet en arc depuis la ville de départ et bulle avec le prix
  function show(code, anchor) {
    var it = items.filter(function (x) { return x.to === code; })[0], a = ap[code], o = ap[sel.value];
    if (!it || !a || !o) return hide();
    var x1 = X(o[6]), y1 = Y(o[5]), x2 = X(a[6]), y2 = Y(a[5]);
    var mx = (x1 + x2) / 2, my = Math.min(y1, y2) - Math.hypot(x2 - x1, y2 - y1) * 0.22;
    var arc = $("any-arc"); if (arc) arc.setAttribute("d", "M" + x1.toFixed(1) + " " + y1.toFixed(1) + "Q" + mx.toFixed(1) + " " + my.toFixed(1) + " " + x2.toFixed(1) + " " + y2.toFixed(1));
    svg.querySelectorAll(".any-dot").forEach(function (d) { d.classList.toggle("on", d.getAttribute("data-to") === code); });
    list.querySelectorAll(".any-item").forEach(function (d) { d.classList.toggle("on", d.getAttribute("data-to") === code); });
    if (!anchor) { tip.hidden = true; return; }
    var box = svg.getBoundingClientRect(), wrap = tip.parentNode.getBoundingClientRect();
    tip.innerHTML = '<strong>' + esc(a[1]) + "</strong> " + esc(L.from) + " <b>" + esc(money(it.price, currency)) + "</b>";
    tip.style.left = (box.left - wrap.left + (x2 / W) * box.width) + "px";
    tip.style.top = (box.top - wrap.top + (y2 / (789)) * box.height) + "px";
    tip.hidden = false;
  }
  function hide() {
    tip.hidden = true;
    var arc = $("any-arc"); if (arc) arc.setAttribute("d", "");
    svg.querySelectorAll(".any-dot.on").forEach(function (d) { d.classList.remove("on"); });
    list.querySelectorAll(".any-item.on").forEach(function (d) { d.classList.remove("on"); });
  }
  svg.addEventListener("pointerover", function (ev) { var a = ev.target.closest(".any-dot"); if (a) show(a.getAttribute("data-to"), a); });
  svg.addEventListener("pointerleave", hide);
  svg.addEventListener("focusin", function (ev) { var a = ev.target.closest(".any-dot"); if (a) show(a.getAttribute("data-to"), a); });
  svg.addEventListener("focusout", hide);
  list.addEventListener("pointerover", function (ev) { var a = ev.target.closest(".any-item"); if (a) show(a.getAttribute("data-to"), null); });
  list.addEventListener("pointerleave", hide);

  fetch("/data/airports.json").then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; }).then(function (rows) {
    (rows || []).forEach(function (a) { ap[a[0]] = a; });
    if (saved && codes.indexOf(saved) >= 0) return load();
    fetch("/api/geo").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (g) {
      var c = g && BY_COUNTRY[g.country];
      if (c && codes.indexOf(c) >= 0) sel.value = c;
      load();
    });
  });
})();
