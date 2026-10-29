// Page « Recherche en direct » avec une recherche déjà lancée (?flightSearch=CDG1911DSS26111) : comme sur Skyscanner,
// le grand titre et le formulaire laissent la place à une barre compacte (trajet, passagers, dates avec ‹ ›).
// Toucher la barre rouvre le formulaire du moteur pour modifier la recherche.
(function () {
  "use strict";
  var bar = document.getElementById("rs-bar"), form = document.querySelector(".wl-form");
  var fs = new URLSearchParams(location.search).get("flightSearch") || "";
  var m = fs.match(/^([A-Z]{3})(\d{2})(\d{2})([A-Z]{3})(?:(\d{2})(\d{2}))?(\d)?(\d)?(\d)?$/);
  if (!bar || !form || !m) return;
  var from = m[1], to = m[4], ad = +(m[7] || 1), ch = +(m[8] || 0) + +(m[9] || 0);
  var today = new Date(); today.setHours(0, 0, 0, 0);
  var dateOf = function (d, mo) { // prochaine date à venir pour ce jour et ce mois
    var t = new Date(today.getFullYear(), +mo - 1, +d);
    if (t < today) t.setFullYear(t.getFullYear() + 1);
    return t;
  };
  var dep = dateOf(m[2], m[3]), ret = m[5] ? dateOf(m[5], m[6]) : null;
  if (ret && ret < dep) ret.setFullYear(ret.getFullYear() + 1);
  var dd = function (d) { return String(d.getDate()).padStart(2, "0") + String(d.getMonth() + 1).padStart(2, "0"); };
  var shift = function (d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; };
  var link = function (a, b) { return "/recherche/?flightSearch=" + from + dd(a) + to + (b ? dd(b) : "") + (m[7] ? m.slice(7).join("") : "1"); };
  var day = function (d) { return d.toLocaleDateString("fr-FR", { weekday: "short", day: "numeric", month: "short" }); };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var arrow = function (href, label, txt, off) {
    return off ? '<span class="rs-arr" aria-hidden="true">' + txt + "</span>" : '<a class="rs-arr" href="' + href + '" aria-label="' + label + '">' + txt + "</a>";
  };
  var group = function (d, isRet) {
    var prev = shift(d, -1), next = shift(d, 1);
    var pHref = isRet ? link(dep, prev) : link(prev, ret && ret < prev ? prev : ret);
    var nHref = isRet ? link(dep, next) : link(next, ret && ret < next ? next : ret);
    var pOff = isRet ? prev < dep : prev < today;
    return '<div class="rs-date">' + arrow(pHref, (isRet ? "Retour" : "Aller") + " un jour plus tôt", "‹", pOff) +
      "<span>" + esc(day(d)) + "</span>" + arrow(nHref, (isRet ? "Retour" : "Aller") + " un jour plus tard", "›", false) + "</div>";
  };
  var pax = ad + (ad > 1 ? " adultes" : " adulte") + (ch ? ", " + ch + (ch > 1 ? " enfants" : " enfant") : "") + ", Économie";
  var paint = function (a, b) {
    bar.innerHTML = '<button type="button" class="rs-sum" aria-expanded="false" aria-controls="tpwl-search">' +
      '<span class="rs-ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path fill="currentColor" d="M10 2a8 8 0 0 1 6.3 12.9l5.4 5.4-1.4 1.4-5.4-5.4A8 8 0 1 1 10 2zm0 2a6 6 0 1 0 0 12 6 6 0 0 0 0-12z"/></svg></span>' +
      '<span class="rs-txt"><strong>' + esc(a) + " – " + esc(b) + "</strong><small>" + esc(pax) + "</small></span>" +
      '<span class="rs-edit">Modifier</span></button>' +
      '<div class="rs-dates">' + group(dep, false) + (ret ? group(ret, true) : "") + "</div>";
    bar.querySelector(".rs-sum").addEventListener("click", function () {
      var open = form.classList.toggle("open");
      this.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) form.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  };
  paint(from, to);
  fetch("/data/airports.json").then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; }).then(function (db) {
    var name = function (c) { var a = (db || []).filter(function (x) { return x[0] === c; })[0]; return a ? a[1] + " (" + c + ")" : c; };
    var open = form.classList.contains("open");
    paint(name(from), name(to));
    if (open) bar.querySelector(".rs-sum").setAttribute("aria-expanded", "true");
  });
})();
