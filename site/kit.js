// « Kit voyage hors ligne » : infos du voyage gardées dans ce navigateur (rien n'est envoyé), page et guide d'arrivée
// mis en cache pour être lus sans internet (service worker sw.js).
(function () {
  "use strict";
  var f = document.getElementById("kit-form");
  if (!f) return;
  var T = JSON.parse(f.getAttribute("data-t"));
  var K = "escale.kit";
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var fields = [].slice.call(f.querySelectorAll("[name]"));
  var data = {}; try { data = JSON.parse(localStorage.getItem(K) || "{}"); } catch (e) {}
  fields.forEach(function (x) { if (data[x.name] != null) { if (x.type === "checkbox") x.checked = !!data[x.name]; else x.value = data[x.name]; } });
  var card = document.getElementById("kit-card"), msg = document.getElementById("kit-msg");
  var show = function () {
    var g = function (n) { return data[n] ? esc(data[n]) : ""; };
    var rows = [["✈️", T.flight, g("flight") + (g("code") ? " · " + T.code + " " + g("code") : "")], ["📅", T.when, g("dates")], ["🏠", T.addr, g("addr")],
      ["📞", T.contact, g("contact")], ["🚨", T.emerg, g("emerg")], ["📝", T.notes, g("notes")]].filter(function (r) { return r[2]; });
    card.hidden = !rows.length;
    card.innerHTML = rows.length ? "<h2>" + esc(T.card) + (data.dest ? " · " + esc(data.dest) : "") + "</h2><dl>" + rows.map(function (r) { return "<dt>" + r[0] + " " + esc(r[1]) + "</dt><dd>" + r[2].replace(/\n/g, "<br>") + "</dd>"; }).join("") + "</dl>" : "";
  };
  show();
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    fields.forEach(function (x) { data[x.name] = x.type === "checkbox" ? x.checked : x.value.trim(); });
    try { localStorage.setItem(K, JSON.stringify(data)); } catch (e2) {}
    show();
    var urls = [location.pathname, "/"], g = f.querySelector('[name="guide"]');
    if (g && g.value) urls.push(g.value);
    var done = function (ok) { if (msg) msg.textContent = ok ? T.saved_off : T.saved; };
    if ("serviceWorker" in navigator && window.caches) {
      navigator.serviceWorker.register("/sw.js").then(function () { return caches.open("escale-v3-pages"); })
        .then(function (c) { return Promise.all(urls.map(function (u) { return c.add(u).catch(function () {}); })); }).then(function () { done(true); }, function () { done(false); });
    } else done(false);
  });
  var clr = document.getElementById("kit-clear");
  if (clr) clr.addEventListener("click", function () { if (!confirm(T.confirm)) return; try { localStorage.removeItem(K); } catch (e) {} data = {}; f.reset(); show(); if (msg) msg.textContent = ""; });
})();
