// « Le vrai budget du voyage en famille » : billets réels (meilleur aller-retour du mois, /api/calendar) × voyageurs,
// + bagages, visa et assurance saisis par le visiteur (aucun montant inventé), total en euros et en francs CFA.
(function () {
  "use strict";
  var f = document.getElementById("bf-form");
  if (!f || !window.EscaleAC) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2), loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "en-GB";
  var T = JSON.parse(f.getAttribute("data-t")), out = document.getElementById("bf-out");
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var eur = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var cfa = function (n) { return Math.round(n * 655.957).toLocaleString(loc) + " F CFA"; };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { day: "numeric", month: "long" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var num = function (id) { var v = Number(f.querySelector(id).value); return v > 0 ? v : 0; };
  var from = window.EscaleAC.attach(f.querySelector("#bf-from")), to = window.EscaleAC.attach(f.querySelector("#bf-to"));
  if (window.ESCALE_FETE_FROM) window.ESCALE_FETE_FROM.then(function (x) { window.EscaleAC.ready.then(function () { if (!f.querySelector("#bf-from").value) from.set(x.code === "CDG" ? "PAR" : x.code); }); });
  // Mois : les 6 prochains
  var sel = f.querySelector("#bf-month"), d = new Date();
  for (var i = 0; i < 6; i++) { var m = new Date(d.getFullYear(), d.getMonth() + i, 1), v = m.getFullYear() + "-" + ("0" + (m.getMonth() + 1)).slice(-2), o = document.createElement("option");
    o.value = v; o.textContent = m.toLocaleDateString(loc, { month: "long", year: "numeric" }); if (i === 1) o.selected = true; sel.appendChild(o); }
  // Bouton « visa Schengen » : remplit les montants officiels (90 € adulte, 45 € de 6 à 12 ans)
  var sch = f.querySelector("#bf-sch");
  if (sch) sch.addEventListener("click", function () { f.querySelector("#bf-visa-a").value = 90; f.querySelector("#bf-visa-c").value = 45; });
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var a = f.querySelector("#bf-from").dataset.code, b = f.querySelector("#bf-to").dataset.code;
    var ad = Math.max(1, num("#bf-ad")), ch = num("#bf-ch"), bb = num("#bf-bb"), bags = num("#bf-bags"), bagp = num("#bf-bagp");
    var va = num("#bf-visa-a"), vc = num("#bf-visa-c"), ins = num("#bf-ins");
    if (!a || !b || a === b) { out.innerHTML = '<p class="tc-err">' + esc(T.err) + "</p>"; return; }
    out.innerHTML = '<p class="pr-wait">' + esc(T.loading) + "</p>";
    get("/api/calendar?from=" + a + "&to=" + b + "&month=" + sel.value).then(function (cal) {
      var best = null, days = cal && cal.available && cal.days ? cal.days : {};
      Object.keys(days).forEach(function (k) { if (!best || days[k].price < best.p) best = { p: days[k].price, d: k, r: days[k].ret }; });
      if (!best) { out.innerHTML = '<p class="tc-err">' + esc(T.none) + "</p>"; return; }
      var seats = ad + ch, tickets = best.p * seats, bagT = bags * seats * bagp, visaT = va * ad + vc * ch, insT = ins * (seats + bb);
      var total = tickets + bagT + visaT + insT;
      var rows = [[T.r_tickets.replace("{n}", seats).replace("{p}", eur(best.p)), tickets]];
      if (bagT) rows.push([T.r_bags.replace("{n}", bags * seats).replace("{p}", eur(bagp)), bagT]);
      if (visaT) rows.push([T.r_visa, visaT]);
      if (insT) rows.push([T.r_ins.replace("{n}", seats + bb), insT]);
      var name = window.EscaleAC.name;
      var msg = T.wa.replace("{a}", name(a)).replace("{b}", name(b)).replace("{n}", seats + bb).replace("{t}", eur(total)).replace("{c}", cfa(total)) + " " + location.origin + location.pathname;
      out.innerHTML = '<div class="bf-res"><h2>' + esc(name(a)) + " → " + esc(name(b)) + '</h2><p class="small">' + esc(T.dates.replace("{d}", day(best.d)).replace("{r}", best.r ? day(best.r) : "")) + "</p>" +
        '<table class="bf-table">' + rows.map(function (r) { return "<tr><th scope=\"row\">" + esc(r[0]) + "</th><td>" + esc(eur(r[1])) + "</td></tr>"; }).join("") +
        '<tr class="bf-tot"><th scope="row">' + esc(T.total) + "</th><td>" + esc(eur(total)) + "<small>" + esc(cfa(total)) + "</small></td></tr></table>" +
        '<p class="bf-per">' + esc(T.per.replace("{p}", eur(total / (seats + bb)))) + "</p>" +
        (bb ? '<p class="small">👶 ' + esc(T.baby.replace("{n}", bb)) + "</p>" : "") + (ch ? '<p class="small">🧒 ' + esc(T.child) + "</p>" : "") +
        (!bagp && bags ? '<p class="small">🧳 ' + T.bag_hint + "</p>" : "") +
        '<div class="pr-btns"><a class="btn" href="/recherche/?flightSearch=' + a + ddmm(best.d) + b + (best.r ? ddmm(best.r) : "") + ad + '">' + esc(T.see) + "</a>" +
        '<a class="btn wa-btn" target="_blank" rel="noopener" href="https://wa.me/?text=' + encodeURIComponent(msg) + '">📲 ' + esc(T.share) + "</a></div>" +
        '<p class="small">' + esc(T.note) + "</p></div>";
    });
  });
})();
