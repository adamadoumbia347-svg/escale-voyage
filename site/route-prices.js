// Pages trajets : affiche le prix aller-retour le plus bas repéré récemment pour les 3 prochains mois.
// Les données viennent de /api/prix (Travelpayouts). Sans réponse, la section reste masquée.
(function () {
  "use strict";
  // Lien Aviasales (partenaire rémunéré) : ouvre directement une recherche datée, départ dans 45 jours, retour 7 jours après
  var pad2 = function (n) { return String(n).padStart(2, "0"); };
  var ddmm = function (dt) { return pad2(dt.getDate()) + pad2(dt.getMonth() + 1); };
  Array.prototype.forEach.call(document.querySelectorAll("a[data-av]"), function (a) {
    var p = a.getAttribute("data-av").split("-"), m = (a.href.match(/marker=(\d+)/) || [])[1];
    if (!m || p.length !== 2) return;
    var dep = new Date(Date.now() + 45 * 864e5), ret = new Date(dep.getTime() + 7 * 864e5);
    a.href = "https://www.aviasales.com/search/" + p[0] + ddmm(dep) + p[1] + ddmm(ret) + "1?marker=" + m + "&currency=eur";
  });
  var box = document.getElementById("route-prices");
  // Prix déjà écrits dans la page par le serveur (src/apercu-prix.ts) : rien à faire
  if (!box || box.hasAttribute("data-ssr")) return;
  var from = box.getAttribute("data-from"), to = box.getAttribute("data-to");
  var heroPrice = document.getElementById("hero-price");
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var L = {
    fr: { loc: "fr-FR", hero: "Aller-retour repéré dès", from: "dès", direct: "vol direct", one: "1 escale", many: " escales", best: "Le moins cher", go: "Voir ces dates", app: "fr" },
    en: { loc: "en-GB", hero: "Round trip found from", from: "from", direct: "direct", one: "1 stop", many: " stops", best: "Cheapest", go: "See these dates", app: "en" },
    es: { loc: "es-ES", hero: "Ida y vuelta desde", from: "desde", direct: "vuelo directo", one: "1 escala", many: " escalas", best: "El más barato", go: "Ver estas fechas", app: "es" },
    pt: { loc: "pt-PT", hero: "Ida e volta desde", from: "desde", direct: "voo direto", one: "1 escala", many: " escalas", best: "O mais barato", go: "Ver estas datas", app: "pt" },
    ar: { loc: "ar", hero: "ذهاب وعودة ابتداءً من", from: "من", direct: "رحلة مباشرة", one: "توقف واحد", many: " توقفات", best: "الأرخص", go: "اعرض هذه التواريخ", app: "ar" },
    it: { loc: "it-IT", hero: "Andata e ritorno trovato da", from: "da", direct: "volo diretto", one: "1 scalo", many: " scali", best: "Il più economico", go: "Vedi queste date", app: "en" }
  }[lang] || null;
  if (!L) return;
  var money = function (n) {
    try { return new Intl.NumberFormat(L.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " €"; }
  };

  var now = new Date(), months = [];
  for (var i = 0; i < 3; i++) {
    var d = new Date(now.getFullYear(), now.getMonth() + i, 1);
    months.push(d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-01");
  }
  var label = function (iso) {
    var p = iso.split("-");
    return new Date(+p[0], +p[1] - 1, 1).toLocaleDateString(L.loc, { month: "long", year: "numeric" });
  };
  var day = function (iso) {
    return iso ? new Date(iso).toLocaleDateString(L.loc, { day: "numeric", month: "short" }) : "";
  };
  var esc = function (t) {
    return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  };

  Promise.all(months.map(function (m) {
    return fetch("/api/prix?from=" + from + "&to=" + to + "&dep=" + m + "&rt=1")
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; })
      .then(function (d) { return { month: m, data: d }; });
  })).then(function (rows) {
    var today = new Date().toISOString().slice(0, 10);
    var found = rows.filter(function (r) {
      return r.data && r.data.available && r.data.price && (r.data.departure_at || "").slice(0, 10) >= today;
    });
    if (!found.length) return;
    var best = Math.min.apply(null, found.map(function (r) { return r.data.price; }));
    if (heroPrice) {
      heroPrice.innerHTML = esc(L.hero) + " <strong>" + esc(money(best)) + "</strong>";
      heroPrice.hidden = false;
    }
    var list = found.map(function (r) {
      var d = r.data, dep = (d.departure_at || "").slice(0, 10), ret = (d.return_at || "").slice(0, 10);
      var stops = d.transfers === 0 ? L.direct : d.transfers === 1 ? L.one : d.transfers + L.many;
      var href = "/?type=vols&from=" + from + "&to=" + to + (dep ? "&dep=" + dep : "") + (ret ? "&ret=" + ret : "") + (L.app !== "fr" ? "&lang=" + L.app : "");
      var cheapest = d.price === best ? ' <span class="pill-best">' + esc(L.best) + "</span>" : "";
      return '<li class="price-row"><div><span class="price-month">' + esc(label(r.month)) + cheapest + "</span>" +
        '<span class="price-meta">' + esc(dep ? day(dep) + (ret ? " → " + day(ret) : "") + " · " + stops : stops) + "</span></div>" +
        '<strong class="price-val">' + esc(L.from + " " + money(d.price)) + "</strong>" +
        '<a class="price-go" href="' + esc(href) + '">' + esc(L.go) + "</a></li>";
    }).join("");
    box.querySelector(".price-list").innerHTML = list;
    box.hidden = false;
  });
})();
