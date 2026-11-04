// Recherche de ville ou d'aéroport (3 200 aéroports, noms dans la langue de la page), partagée par les outils Escale.
// EscaleAC.attach(input, onPick(code, name)) ; EscaleAC.name(code) ; EscaleAC.ready (promesse) ; EscaleAC.cc(code) (pays).
(function () {
  "use strict";
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var CITY = { PAR: ["Paris", "FR"], LON: ["London", "GB"], MIL: ["Milano", "IT"], ROM: ["Roma", "IT"], NYC: ["New York", "US"], TYO: ["Tokyo", "JP"], STO: ["Stockholm", "SE"],
    YMQ: ["Montréal", "CA"], YTO: ["Toronto", "CA"], WAS: ["Washington", "US"], CHI: ["Chicago", "US"], SAO: ["São Paulo", "BR"], BUE: ["Buenos Aires", "AR"], MOW: ["Moskva", "RU"], BUH: ["București", "RO"] };
  var CITYN = { fr: { LON: "Londres", MIL: "Milan", ROM: "Rome", MOW: "Moscou", BUH: "Bucarest" }, en: { MIL: "Milan", ROM: "Rome", MOW: "Moscow", BUH: "Bucharest" },
    es: { PAR: "París", LON: "Londres", MIL: "Milán", NYC: "Nueva York" }, pt: { LON: "Londres", MIL: "Milão", NYC: "Nova Iorque" }, it: { PAR: "Parigi", LON: "Londra" }, de: { LON: "London", MIL: "Mailand", ROM: "Rom" } }[lang] || {};
  var db = {}, list = [];
  var norm = function (s) { return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var country = function (cc) { try { return new Intl.DisplayNames([lang], { type: "region" }).of(cc); } catch (e) { return cc; } };
  var ready = Promise.all([get("/data/airports.json"), lang === "fr" ? Promise.resolve({}) : get("/data/noms/" + lang + ".json")]).then(function (r) {
    var names = r[1] || {};
    (r[0] || []).forEach(function (a) { db[a[0]] = { n: names[a[0]] || a[1], cc: a[3], big: a[4] }; });
    Object.keys(CITY).forEach(function (k) { db[k] = { n: CITYN[k] || names[k] || CITY[k][0], cc: CITY[k][1], big: 1, city: 1 }; });
    list = Object.keys(db).map(function (k) { return [k, db[k]]; });
  });
  var attach = function (inp, onPick) {
    var wrap = document.createElement("div"); wrap.className = "ac-wrap"; inp.parentNode.insertBefore(wrap, inp); wrap.appendChild(inp);
    var ul = document.createElement("ul"); ul.className = "ac-sug"; ul.hidden = true; ul.setAttribute("role", "listbox"); wrap.appendChild(ul);
    inp.setAttribute("autocomplete", "off");
    var pick = function (c) { inp.value = db[c] ? db[c].n + " (" + c + ")" : c; inp.dataset.code = c; ul.hidden = true; if (onPick) onPick(c, db[c] ? db[c].n : c); };
    inp.addEventListener("input", function () {
      inp.dataset.code = "";
      var q = norm(inp.value.trim()), up = inp.value.trim().toUpperCase();
      if (q.length < 2) { ul.hidden = true; return; }
      var hits = list.filter(function (x) { return x[0] === up || norm(x[1].n).indexOf(q) === 0; })
        .sort(function (a, b) { return (b[0] === up) - (a[0] === up) || (b[1].city || 0) - (a[1].city || 0) || (b[1].big || 0) - (a[1].big || 0); }).slice(0, 7);
      ul.innerHTML = hits.map(function (x) { return '<li role="option" data-v="' + x[0] + '">' + esc(x[1].n) + " <small>" + esc(country(x[1].cc)) + " · " + x[0] + "</small></li>"; }).join("");
      ul.hidden = !hits.length;
    });
    ul.addEventListener("mousedown", function (e) { var li = e.target.closest("li"); if (li) { e.preventDefault(); pick(li.getAttribute("data-v")); } });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { var li = ul.querySelector("li"); if (li && !ul.hidden) { e.preventDefault(); pick(li.getAttribute("data-v")); } } });
    inp.addEventListener("blur", function () { setTimeout(function () { ul.hidden = true; }, 150); });
    return { set: pick };
  };
  window.EscaleAC = { attach: attach, ready: ready, name: function (c) { return (db[c] && db[c].n) || c; }, cc: function (c) { return db[c] && db[c].cc; } };
})();
