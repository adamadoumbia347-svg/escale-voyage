// « Contrôle avant le vol » : nom sur le billet, validité du passeport selon la destination, pages libres, visa.
// Règles prudentes (vérifiées en novembre 2026) : Schengen = passeport valable 3 mois après le retour et délivré il y a moins
// de 10 ans ; Royaume-Uni, États-Unis, Canada = valable tout le séjour ; ailleurs = 6 mois après l'arrivée (souvent exigé).
(function () {
  "use strict";
  var f = document.getElementById("cv-form");
  if (!f) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2), loc = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE" }[lang] || "en-GB";
  var T = JSON.parse(f.getAttribute("data-t")), out = document.getElementById("cv-out");
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var D = function (s) { return s ? new Date(s + "T12:00:00") : null; };
  var addM = function (d, m) { var x = new Date(d); x.setMonth(x.getMonth() + m); return x; };
  var day = function (d) { return d.toLocaleDateString(loc, { day: "numeric", month: "long", year: "numeric" }); };
  f.addEventListener("submit", function (e) {
    e.preventDefault();
    var dest = f.querySelector("#cv-dest").value, pass = f.querySelector("#cv-pass").value, dep = D(f.querySelector("#cv-dep").value), ret = D(f.querySelector("#cv-ret").value) || dep;
    var exp = D(f.querySelector("#cv-exp").value), iss = D(f.querySelector("#cv-iss").value), pages = Number(f.querySelector("#cv-pages").value), name = f.querySelector("#cv-name").value;
    if (!dep || !exp) { out.innerHTML = '<p class="tc-err">' + esc(T.err) + "</p>"; return; }
    var rows = [], bad = 0, warn = 0;
    var add = function (lvl, txt) { rows.push('<li class="cv-' + lvl + '">' + (lvl === "ok" ? "✅ " : lvl === "warn" ? "⚠️ " : "❌ ") + esc(txt) + "</li>"); if (lvl === "bad") bad++; if (lvl === "warn") warn++; };
    // Nom
    if (name === "yes") add("ok", T.name_ok); else if (name === "no") add("bad", T.name_bad); else add("warn", T.name_warn);
    // Validité
    var need, rule;
    if (dest === "SCH") { need = addM(ret, 3); rule = T.r_sch; }
    else if (/^(GB|US|CA)$/.test(dest)) { need = ret; rule = T.r_whole; }
    else { need = addM(dep, 6); rule = T.r_six; }
    if (exp >= need) add("ok", T.exp_ok.replace("{d}", day(exp)).replace("{r}", rule));
    else add("bad", T.exp_bad.replace("{d}", day(exp)).replace("{n}", day(need)).replace("{r}", rule));
    if (dest === "SCH" && iss) { if (addM(iss, 120) >= dep) add("ok", T.iss_ok); else add("bad", T.iss_bad); }
    // Pages
    if (pages >= 2) add("ok", T.pages_ok); else if (pages === 1) add("warn", T.pages_warn); else add("bad", T.pages_bad);
    // Visa
    var vlink = (lang === "fr" ? "/visa/" : "/en/visa/") + "?p=" + encodeURIComponent(pass) + "&d=" + encodeURIComponent(dest);
    var v = bad ? ["bad", T.v_bad] : warn ? ["mid", T.v_mid] : ["good", T.v_good];
    out.innerHTML = '<div class="tc-res tc-' + v[0] + '"><p class="tc-v">' + esc(v[1]) + '</p><ul class="cv-list">' + rows.join("") + "</ul>" +
      '<p><a class="btn ghost" href="' + vlink + '">🛂 ' + esc(T.visa) + "</a></p><p class=\"small\">" + esc(T.note) + "</p></div>";
  });
})();
