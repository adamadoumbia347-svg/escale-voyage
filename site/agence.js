// Page d'une agence partenaire : recherche de vols (moteur Escale) depuis la ville de l'agence, bons plans du mois
// (/api/explore) et bouton WhatsApp vers l'agence avec le trajet choisi. Escale ne touche jamais à l'argent.
(function () {
  "use strict";
  var box = document.getElementById("ag-app");
  if (!box || !window.EscaleAC) return;
  var A = JSON.parse(box.getAttribute("data-a")), T = JSON.parse(box.getAttribute("data-t"));
  var lang = (document.documentElement.lang || "fr").slice(0, 2), loc = lang === "fr" ? "fr-FR" : "en-GB";
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var cfa = function (n) { return Math.round(n * 655.957).toLocaleString(loc) + " F CFA"; };
  var day = function (s) { try { return new Date(String(s).slice(0, 10) + "T12:00:00").toLocaleDateString(loc, { day: "numeric", month: "short" }); } catch (e) { return ""; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var wa = function (txt) { return A.whatsapp ? "https://wa.me/" + A.whatsapp.replace(/[^0-9]/g, "") + "?text=" + encodeURIComponent(txt) : null; };
  var f = document.getElementById("ag-form"), from = window.EscaleAC.attach(f.querySelector("#ag-from")), to = window.EscaleAC.attach(f.querySelector("#ag-to"));
  window.EscaleAC.ready.then(function () { from.set(A.aeroport); });
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var a = f.querySelector("#ag-from").dataset.code, b = f.querySelector("#ag-to").dataset.code, dep = f.querySelector("#ag-dep").value, ret = f.querySelector("#ag-ret").value, n = f.querySelector("#ag-pax").value || "1";
    if (!a || !b || !dep) { document.getElementById("ag-msg").textContent = T.err; return; }
    location.href = "/recherche/?flightSearch=" + a + ddmm(dep) + b + (ret ? ddmm(ret) : "") + n;
  });
  // Contacter l'agence avec le trajet saisi
  var wb = document.getElementById("ag-wa");
  if (wb) wb.addEventListener("click", function (e) {
    var a = f.querySelector("#ag-from").value, b = f.querySelector("#ag-to").value, dep = f.querySelector("#ag-dep").value;
    var u = wa(T.wa_trip.replace("{a}", a || "…").replace("{b}", b || "…").replace("{d}", dep || "…"));
    if (u) { e.preventDefault(); window.open(u, "_blank", "noopener"); }
  });
  // Bons plans du mois prochain depuis la ville de l'agence
  var grid = document.getElementById("ag-deals"), d = new Date(), m = new Date(d.getFullYear(), d.getMonth() + 1, 1), month = m.getFullYear() + "-" + ("0" + (m.getMonth() + 1)).slice(-2);
  Promise.all([fetch("/api/explore?from=" + A.aeroport + "&month=" + month + "&currency=EUR").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }), window.EscaleAC.ready]).then(function (r) {
    var items = (r[0] && r[0].available && r[0].items || []).slice(0, 8);
    if (!items.length) { grid.innerHTML = '<li class="pr-wait">' + esc(T.none) + "</li>"; return; }
    grid.innerHTML = items.map(function (it) {
      var name = window.EscaleAC.name(it.to), dep = String(it.departure_at).slice(0, 10), ret = it.return_at ? String(it.return_at).slice(0, 10) : "";
      var w = wa(T.wa_deal.replace("{a}", window.EscaleAC.name(A.aeroport)).replace("{b}", name).replace("{d}", day(dep)).replace("{p}", money(it.price)));
      return '<li class="ag-deal"><strong>' + esc(name) + "</strong><small>" + esc(day(dep) + (ret ? " → " + day(ret) : "")) + "</small>" +
        '<b>' + esc(money(it.price)) + "</b><small>" + esc(cfa(it.price)) + "</small>" +
        '<span class="ag-btns"><a class="btn ghost" href="/recherche/?flightSearch=' + A.aeroport + ddmm(dep) + it.to + (ret ? ddmm(ret) : "") + '1">' + esc(T.online) + "</a>" +
        (w ? '<a class="btn wa-btn" target="_blank" rel="noopener" href="' + esc(w) + '">' + esc(T.agency) + "</a>" : "") + "</span></li>";
    }).join("");
  });
})();
