// Outil « Visa selon mon passeport » (/visa/, /en/visa/) : données dans la page (scripts/visa.py), choix gardés sur l'appareil.
(function () {
  "use strict";
  var el = document.getElementById("visa-data");
  if (!el) return;
  var D = JSON.parse(el.textContent), P = document.getElementById("visa-p"), Q = document.getElementById("visa-d");
  var res = document.getElementById("visa-res"), all = document.getElementById("visa-all");
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var st = function (p, d) { var v = D.r[p + "-" + d]; return v === undefined ? 9 : v; };
  var note = function (p, d, s) {
    if (d === "CA" && p === "MA") return D.n["CA-MA"];
    if (s === 1 && D.n[d + "-1"]) return D.n[d + "-1"];
    if (d === "SCH" && s === 0 && D.west.indexOf(p) >= 0 && D.eu.indexOf(p) < 0) return D.n["SCH-W"];
    if (s === 0 && D.ecowas.indexOf(p) >= 0 && D.ecowas.indexOf(d) >= 0 && p !== d) return D.n.ECOWAS;
    if (s === 0 && D.cemac.indexOf(p) >= 0 && D.cemac.indexOf(d) >= 0 && p !== d) return D.n.CEMAC;
    return "";
  };
  var badge = function (s) { return '<span class="visa-badge v' + s + '">' + esc(D.st[s]) + "</span>"; };
  var get = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } };
  var set = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
  var u = new URLSearchParams(location.search);
  if (u.get("p") && D.p[u.get("p")]) P.value = u.get("p"); else if (get("escale.visa.p") && D.p[get("escale.visa.p")]) P.value = get("escale.visa.p");
  if (u.get("d") && D.d[u.get("d")]) Q.value = u.get("d");
  function show() {
    var p = P.value, d = Q.value, s = st(p, d), n = note(p, d, s), dest = D.d[d];
    set("escale.visa.p", p);
    res.innerHTML = '<div class="visa-card"><p class="visa-head">' + esc(D.p[p][1] + " " + D.p[p][0]) + " → " + esc(dest[1] + " " + dest[0]) + "</p>" + badge(s) +
      "<p>" + esc(D.sl[s]) + (n ? " " + esc(n) : "") + '</p><p class="visa-links"><a href="' + esc(dest[2]) + '" target="_blank" rel="noopener">' + esc(D.official) + " ↗</a></p></div>";
    all.innerHTML = Object.keys(D.d).filter(function (k) { return k !== p; }).map(function (k) {
      var x = D.d[k], s2 = st(p, k);
      return '<li><button type="button" data-d="' + k + '"><span>' + esc(x[1] + " " + x[0]) + "</span>" + badge(s2) + "</button></li>";
    }).join("");
  }
  P.addEventListener("change", show); Q.addEventListener("change", show);
  all.addEventListener("click", function (ev) { var b = ev.target.closest("button[data-d]"); if (!b) return; Q.value = b.getAttribute("data-d"); show(); res.scrollIntoView({ behavior: "smooth", block: "center" }); });
  show();
})();
