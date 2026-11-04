// Page « Fais venir un proche / Paye pour moi » (toutes langues, tous pays) :
//  - mode choix : départ, arrivée (n'importe quel aéroport du monde, recherche par ville) et mois → 3 meilleurs vols réels (/api/calendar),
//    puis « Envoyer pour paiement » ouvre WhatsApp avec un lien vers ce vol précis ;
//  - mode paiement (?v=ABJ-PAR-20261209-20261223-421) : la personne qui paie voit ce vol, le prix actuel (/api/prix) et réserve.
// Escale ne touche jamais à l'argent : la réservation se fait chez le partenaire, comme partout sur le site.
(function () {
  "use strict";
  var app = document.getElementById("pr-app");
  if (!app) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", it: "it-IT", de: "de-DE" }[lang] || "en-GB";
  var T = JSON.parse(app.getAttribute("data-t"));
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { weekday: "short", day: "numeric", month: "long" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var ymd = function (s) { return s.slice(0, 4) + "-" + s.slice(4, 6) + "-" + s.slice(6, 8); };
  var engine = function (f, t, dep, ret) { return "/recherche/?flightSearch=" + f + ddmm(dep) + t + (ret ? ddmm(ret) : "") + "1"; };
  var country = function (cc) { try { return new Intl.DisplayNames([lang], { type: "region" }).of(cc); } catch (e) { return cc; } };
  // Codes de ville (plusieurs aéroports) : nom et pays
  var CITY = { PAR: ["Paris", "FR"], LON: ["London", "GB"], MIL: ["Milano", "IT"], ROM: ["Roma", "IT"], NYC: ["New York", "US"], TYO: ["Tokyo", "JP"], STO: ["Stockholm", "SE"],
    BUH: ["București", "RO"], MOW: ["Moskva", "RU"], YMQ: ["Montréal", "CA"], YTO: ["Toronto", "CA"], WAS: ["Washington", "US"], CHI: ["Chicago", "US"], SAO: ["São Paulo", "BR"], BUE: ["Buenos Aires", "AR"], BJS: ["Beijing", "CN"], SEL: ["Seoul", "KR"], OSA: ["Osaka", "JP"] };
  var CITYN = { fr: { LON: "Londres", MIL: "Milan", ROM: "Rome", MOW: "Moscou", BUH: "Bucarest", BJS: "Pékin", SEL: "Séoul" }, en: { MIL: "Milan", ROM: "Rome", BUH: "Bucharest", MOW: "Moscow" },
    es: { PAR: "París", LON: "Londres", MIL: "Milán", ROM: "Roma", NYC: "Nueva York", MOW: "Moscú", BUH: "Bucarest", BJS: "Pekín", SEL: "Seúl" }, pt: { LON: "Londres", MIL: "Milão", ROM: "Roma", NYC: "Nova Iorque", MOW: "Moscovo", BJS: "Pequim" },
    it: { PAR: "Parigi", LON: "Londra", MOW: "Mosca", BUH: "Bucarest", BJS: "Pechino" }, de: { LON: "London", MIL: "Mailand", ROM: "Rom", MOW: "Moskau", BUH: "Bukarest", BJS: "Peking" } }[lang] || {};
  var SCH = /^(AT|BE|BG|CH|CZ|DE|DK|EE|ES|FI|FR|GR|HR|HU|IS|IT|LI|LT|LU|LV|MT|NL|NO|PL|PT|RO|SE|SI|SK)$/;
  var MERGE = { CDG: "PAR", ORY: "PAR", BVA: "PAR", MXP: "MIL", LIN: "MIL", BGY: "MIL", FCO: "ROM", CIA: "ROM", LHR: "LON", LGW: "LON", STN: "LON", LTN: "LON", LCY: "LON", JFK: "NYC", EWR: "NYC", LGA: "NYC", YUL: "YMQ" };
  var db = {}, list = [];
  var dbReady = Promise.all([get("/data/airports.json"), lang === "fr" ? Promise.resolve({}) : get("/data/noms/" + lang + ".json")]).then(function (r) {
    var names = r[1] || {};
    (r[0] || []).forEach(function (a) { db[a[0]] = { n: names[a[0]] || a[1], cc: a[3], big: a[4] }; });
    Object.keys(CITY).forEach(function (k) { db[k] = { n: CITYN[k] || names[k] || CITY[k][0], cc: CITY[k][1], big: 1, city: 1 }; });
    list = Object.keys(db).map(function (k) { return [k, db[k]]; });
  });
  var name = function (c) { return (db[c] && db[c].n) || c; };
  var norm = function (s) { return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
  var visaLink = function (c) { var cc = db[c] && db[c].cc; return (lang === "fr" ? "/visa/" : "/en/visa/") + (cc ? "?d=" + (SCH.test(cc) ? "SCH" : cc) : ""); };

  // ---------- Mode paiement ----------
  var v = (new URLSearchParams(location.search).get("v") || "").match(/^([A-Z]{3})-([A-Z]{3})-(\d{8})-(\d{8})-(\d{1,5})$/);
  if (v) {
    var f = v[1], t = v[2], dep = ymd(v[3]), ret = ymd(v[4]), seen = +v[5];
    document.querySelectorAll(".pr-choose-only").forEach(function (e) { e.hidden = true; });
    var box = document.getElementById("price-alert"); if (box) { box.setAttribute("data-from", f); box.setAttribute("data-to", t); }
    dbReady.then(function () {
      app.innerHTML = '<div class="pr-pay"><p class="eyebrow">' + esc(T.pay_eyebrow) + "</p><h2>" + esc(name(f)) + " → " + esc(name(t)) + "</h2>" +
        '<p class="pr-dates">✈️ ' + esc(day(dep)) + "<br>↩️ " + esc(day(ret)) + "</p>" +
        '<p class="pr-seen">' + esc(T.seen.replace("{p}", money(seen))) + '</p><p class="pr-now" aria-live="polite">' + esc(T.checking) + "</p>" +
        '<a class="btn pr-book" href="' + engine(f, t, dep, ret) + '">' + esc(T.book) + "</a>" +
        '<p class="small">' + esc(T.book_note) + ' <a href="' + visaLink(t) + '">' + esc(T.visa_link) + "</a></p></div>";
      get("/api/prix?from=" + f + "&to=" + t + "&dep=" + dep + "&ret=" + ret + "&currency=EUR").then(function (d) {
        var now = app.querySelector(".pr-now");
        if (d && d.available && d.price) { now.innerHTML = "<strong></strong>"; now.firstChild.textContent = T.now.replace("{p}", money(d.price)); if (d.price < seen) now.classList.add("pr-down"); }
        else now.textContent = T.now_none;
      });
    });
    return;
  }

  // ---------- Mode choix ----------
  var FROMS = JSON.parse(app.getAttribute("data-from")), TOS = JSON.parse(app.getAttribute("data-to"));
  var months = (function () { var d = new Date(), out = []; for (var i = 0; i < 6; i++) { var m = new Date(d.getFullYear(), d.getMonth() + i, 1); out.push(m.getFullYear() + "-" + ("0" + (m.getMonth() + 1)).slice(-2)); } return out; })();
  var mname = function (m) { try { return new Date(m + "-15T12:00:00").toLocaleDateString(loc, { month: "long" }); } catch (e) { return m; } };
  var st = { f: FROMS[0], t: TOS[0], m: months[1] };
  var field = function (key, q, sugg) {
    return '<div class="pr-step" data-k="' + key + '"><h2>' + esc(q) + '</h2><div class="pr-pick"><input type="search" class="pr-in" autocomplete="off" placeholder="' + esc(T.ph) + '" aria-label="' + esc(q) + '">' +
      '<ul class="pr-sug" role="listbox" hidden></ul></div><div class="pr-chips" role="group">' + sugg.map(function (c) {
        return '<button type="button" data-v="' + c + '" aria-pressed="' + (st[key] === c) + '">' + esc(name(c)) + "</button>";
      }).join("") + "</div></div>";
  };
  var setVal = function (step, c) {
    var key = step.getAttribute("data-k"); st[key] = c;
    var g = step.querySelector(".pr-chips");
    if (!g.querySelector('[data-v="' + c + '"]')) { var b = document.createElement("button"); b.type = "button"; b.setAttribute("data-v", c); b.textContent = name(c); g.insertBefore(b, g.firstChild); }
    g.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-v") === c ? "true" : "false"); });
    step.querySelector(".pr-in").value = ""; step.querySelector(".pr-sug").hidden = true;
    search();
  };
  var draw = function () {
    app.innerHTML = field("f", "1. " + T.q_from, FROMS) + field("t", "2. " + T.q_to, TOS) +
      '<div class="pr-step"><h2>3. ' + esc(T.q_month) + '</h2><div class="pr-chips pr-months" role="group">' + months.map(function (m) {
        return '<button type="button" data-v="' + m + '" aria-pressed="' + (st.m === m) + '">' + esc(mname(m)) + "</button>"; }).join("") + "</div></div>" +
      '<div class="pr-res" id="pr-res" aria-live="polite"></div>';
    app.querySelectorAll(".pr-step[data-k]").forEach(function (step) {
      var inp = step.querySelector(".pr-in"), ul = step.querySelector(".pr-sug");
      step.querySelector(".pr-chips").addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) setVal(step, b.getAttribute("data-v")); });
      inp.addEventListener("input", function () {
        var q = norm(inp.value.trim());
        if (q.length < 2) { ul.hidden = true; return; }
        var up = inp.value.trim().toUpperCase();
        var hits = list.filter(function (x) { return x[0] === up || norm(x[1].n).indexOf(q) === 0; })
          .sort(function (a, b) { return (b[0] === up) - (a[0] === up) || (b[1].city || 0) - (a[1].city || 0) || (b[1].big || 0) - (a[1].big || 0); }).slice(0, 7);
        ul.innerHTML = hits.map(function (x) { return '<li role="option" data-v="' + x[0] + '">' + esc(x[1].n) + " <small>" + esc(country(x[1].cc)) + " · " + x[0] + "</small></li>"; }).join("");
        ul.hidden = !hits.length;
      });
      ul.addEventListener("click", function (e) { var li = e.target.closest("li"); if (li) setVal(step, li.getAttribute("data-v")); });
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); var li = ul.querySelector("li"); if (li) setVal(step, li.getAttribute("data-v")); } });
    });
    app.querySelector(".pr-months").addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return; st.m = b.getAttribute("data-v");
      this.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); search();
    });
    search();
  };
  var tok = 0;
  var search = function () {
    var t0 = ++tok, res = document.getElementById("pr-res");
    if (st.f === st.t) { res.innerHTML = ""; return; }
    res.innerHTML = '<p class="pr-wait">' + esc(T.loading) + "</p>";
    var box = document.getElementById("price-alert"); if (box) { box.setAttribute("data-from", st.f); box.setAttribute("data-to", st.t); }
    var vl = document.getElementById("pr-visa"); if (vl) vl.href = visaLink(st.t);
    get("/api/calendar?from=" + st.f + "&to=" + st.t + "&month=" + st.m).then(function (r) {
      if (t0 !== tok) return;
      var days = r && r.available && r.days ? Object.keys(r.days).map(function (k) { return { dep: k, ret: r.days[k].ret, p: r.days[k].price, s: r.days[k].transfers }; }).filter(function (x) { return x.p && x.ret; }) : [];
      days.sort(function (a, b) { return a.p - b.p; });
      if (!days.length) { res.innerHTML = '<p class="pr-wait">' + esc(T.none) + "</p>"; return; }
      res.innerHTML = "<h2>" + esc(T.best_h.replace("{a}", name(st.f)).replace("{b}", name(st.t))) + "</h2>" + days.slice(0, 3).map(function (x, i) {
        var link = location.origin + location.pathname + "?v=" + st.f + "-" + st.t + "-" + x.dep.replace(/-/g, "") + "-" + x.ret.replace(/-/g, "") + "-" + Math.round(x.p);
        var msg = T.wa.replace("{a}", name(st.f)).replace("{b}", name(st.t)).replace("{d}", day(x.dep)).replace("{r}", day(x.ret)).replace("{p}", money(x.p)).replace("{u}", link);
        return '<div class="pr-offer' + (i === 0 ? " pr-best" : "") + '">' + (i === 0 ? '<span class="pr-tag">' + esc(T.cheapest) + "</span>" : "") +
          '<p class="pr-price">' + esc(money(x.p)) + " <small>" + esc(T.rt) + "</small></p>" +
          '<p class="pr-dates">✈️ ' + esc(day(x.dep)) + "<br>↩️ " + esc(day(x.ret)) + " · " + esc(x.s ? (x.s === 1 ? T.stop1 : T.stops.replace("{n}", x.s)) : T.direct) + "</p>" +
          '<div class="pr-btns"><a class="btn wa-btn" target="_blank" rel="noopener" href="https://wa.me/?text=' + encodeURIComponent(msg) + '">📲 ' + esc(T.send) + "</a>" +
          '<a class="btn ghost" href="' + engine(st.f, st.t, x.dep, x.ret) + '">' + esc(T.self) + "</a></div></div>";
      }).join("") + '<p class="small">' + esc(T.note) + "</p>";
    });
  };
  // Arrivée par défaut : l'aéroport du visiteur, où qu'il soit (sinon la première suggestion)
  dbReady.then(function () {
    if (!window.ESCALE_FETE_FROM) return draw();
    window.ESCALE_FETE_FROM.then(function (fr) {
      var c = MERGE[fr.code] || fr.code;
      if (c && db[c]) { st.t = c; if (TOS.indexOf(c) >= 0) TOS.splice(TOS.indexOf(c), 1); TOS.unshift(c); if (st.f === c) st.f = FROMS.filter(function (x) { return x !== c; })[0]; }
      draw();
    }, draw);
  });
})();
