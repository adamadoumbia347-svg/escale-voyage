// Page « Partage des frais du voyage » : qui a payé quoi, qui doit combien à qui.
// Tout est calculé dans le navigateur et gardé sur l'appareil (localStorage). Rien n'est envoyé à Escale.
// Le lien de partage contient le compte lui-même (après le #), pour que le groupe voie les mêmes chiffres.
(function () {
  "use strict";
  var root = document.getElementById("pf");
  if (!root) return;
  var T = JSON.parse(root.dataset.t), lang = document.documentElement.lang || "fr", KEY = "escale-frais";
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var fill = function (s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); };
  var CURS = ["EUR", "USD", "GBP", "CAD", "CHF", "XOF", "XAF", "MAD", "DZD", "TND"];
  var vide = function () { return { cur: "EUR", next: 1, people: [], exp: [] }; };

  // ---- état : { cur, next, people: [{ id, n }], exp: [{ l, a (centimes), by (id), f: [id…] }] }
  function valide(s) {
    if (!s || !Array.isArray(s.people) || !Array.isArray(s.exp)) return null;
    var ids = {}, out = vide();
    if (CURS.indexOf(s.cur) !== -1) out.cur = s.cur;
    s.people.slice(0, 30).forEach(function (p) {
      var id = +p.id, n = String(p.n || "").trim().slice(0, 24);
      if (id > 0 && n && !ids[id]) { ids[id] = 1; out.people.push({ id: id, n: n }); out.next = Math.max(out.next, id + 1); }
    });
    s.exp.slice(0, 200).forEach(function (e) {
      var a = Math.round(+e.a), f = (Array.isArray(e.f) ? e.f : []).map(Number).filter(function (i, k, t) { return ids[i] && t.indexOf(i) === k; });
      if (a > 0 && a < 1e11 && ids[+e.by] && f.length) out.exp.push({ l: String(e.l || "").slice(0, 40), a: a, by: +e.by, f: f });
    });
    return out;
  }
  var enc = function (s) { return btoa(unescape(encodeURIComponent(JSON.stringify(s)))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); };
  var dec = function (h) { try { return valide(JSON.parse(decodeURIComponent(escape(atob(h.replace(/-/g, "+").replace(/_/g, "/")))))); } catch (e) { return null; } };
  function lire() { try { return valide(JSON.parse(localStorage.getItem(KEY))); } catch (e) { return null; } }
  function garder() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }

  var S = lire() || vide();
  var m = /^#d=([\w-]+)$/.exec(location.hash);
  if (m) {
    var recu = dec(m[1]);
    // Un compte reçu par lien remplace le compte de l'appareil seulement après accord, s'il y en avait déjà un différent
    if (recu && (!S.people.length || enc(S) === enc(recu) || confirm(T.replace))) { S = recu; garder(); }
    history.replaceState(null, "", location.pathname + location.search);
  }

  var argent = function (c) {
    try { return new Intl.NumberFormat(lang, { style: "currency", currency: S.cur, maximumFractionDigits: c % 100 ? 2 : 0 }).format(c / 100); }
    catch (e) { return (c / 100).toFixed(2) + " " + S.cur; }
  };
  var nom = function (id) { for (var i = 0; i < S.people.length; i++) if (S.people[i].id === id) return S.people[i].n; return "?"; };

  // ---- calcul : solde de chacun (payé − part), puis le moins de virements possible (le plus gros débiteur paie le plus gros créancier)
  function soldes() {
    var b = {}; S.people.forEach(function (p) { b[p.id] = { paye: 0, part: 0 }; });
    S.exp.forEach(function (e) {
      b[e.by].paye += e.a;
      var q = Math.floor(e.a / e.f.length), r = e.a - q * e.f.length;
      e.f.forEach(function (id, i) { b[id].part += q + (i < r ? 1 : 0); });   // les centimes restants vont aux premiers
    });
    return b;
  }
  function virements(b) {
    var d = [], c = [], out = [];
    S.people.forEach(function (p) { var s = b[p.id].paye - b[p.id].part; if (s < 0) d.push({ id: p.id, v: -s }); else if (s > 0) c.push({ id: p.id, v: s }); });
    var tri = function (a, z) { return z.v - a.v; };
    while (d.length && c.length) {
      d.sort(tri); c.sort(tri);
      var x = Math.min(d[0].v, c[0].v);
      out.push({ de: d[0].id, a: c[0].id, v: x });
      d[0].v -= x; c[0].v -= x;
      if (!d[0].v) d.shift();
      if (!c[0].v) c.shift();
    }
    return out;
  }
  window.EscaleFrais = { soldes: soldes, virements: virements, etat: function () { return S; } };   // pour les contrôles

  // ---- affichage
  function dessiner() {
    var cur = $("pf-cur");
    if (!cur.options.length) cur.innerHTML = CURS.map(function (c) { return "<option>" + c + "</option>"; }).join("");
    cur.value = S.cur;
    $("pf-people").innerHTML = S.people.map(function (p) {
      return '<li><span>' + esc(p.n) + '</span><button type="button" data-del-p="' + p.id + '" aria-label="' + esc(fill(T.del, { n: p.n })) + '">×</button></li>';
    }).join("");
    var assez = S.people.length >= 2;
    $("pf-eform").hidden = !assez; $("pf-need").hidden = assez;
    var by = $("pf-by"), garde = +by.value;
    by.innerHTML = S.people.map(function (p) { return '<option value="' + p.id + '">' + esc(p.n) + "</option>"; }).join("");
    if (garde && S.people.some(function (p) { return p.id === garde; })) by.value = garde;
    var coches = {}; [].forEach.call(document.querySelectorAll("#pf-for input"), function (i) { coches[i.value] = i.checked; });
    $("pf-for").innerHTML = S.people.map(function (p) {
      return '<label><input type="checkbox" value="' + p.id + '"' + (coches[p.id] === false ? "" : " checked") + "><span>" + esc(p.n) + "</span></label>";
    }).join("");
    $("pf-exp").innerHTML = S.exp.map(function (e, i) {
      var pour = e.f.length === S.people.length ? T.all : e.f.map(nom).join(", ");
      return "<li><div><strong>" + esc(e.l || T.expense) + "</strong><small>" + esc(fill(T.paidby, { n: nom(e.by), f: pour })) + "</small></div><b>" + argent(e.a) +
        '</b><button type="button" data-del-e="' + i + '" aria-label="' + esc(fill(T.del, { n: e.l || T.expense })) + '">×</button></li>';
    }).join("");
    var res = $("pf-res");
    res.hidden = !S.exp.length;
    if (!S.exp.length) return;
    var b = soldes(), v = virements(b), total = S.exp.reduce(function (t, e) { return t + e.a; }, 0);
    var lignes = S.people.map(function (p) {
      var s = b[p.id].paye - b[p.id].part;
      return "<tr><th scope=\"row\">" + esc(p.n) + "</th><td>" + argent(b[p.id].paye) + "</td><td>" + argent(b[p.id].part) + '</td><td class="' + (s < 0 ? "pf-neg" : s > 0 ? "pf-pos" : "") + '">' +
        '<span dir="ltr">' + (s > 0 ? "+" : "") + argent(s) + "</span></td></tr>";
    }).join("");
    $("pf-out").innerHTML = '<p class="pf-total">' + esc(T.total) + " <strong>" + argent(total) + "</strong></p>" +
      (v.length ? '<ul class="pf-pay">' + v.map(function (x) { return "<li>" + fill(esc(T.owes), { a: "<strong>" + esc(nom(x.de)) + "</strong>", b: "<strong>" + esc(nom(x.a)) + "</strong>", x: '<b dir="ltr">' + argent(x.v) + "</b>" }) + "</li>"; }).join("") + "</ul>"
                : '<p class="pf-ok">' + esc(T.even) + "</p>") +
      '<div class="pf-scroll"><table class="pf-table"><thead><tr><td></td><th scope="col">' + esc(T.c_paid) + '</th><th scope="col">' + esc(T.c_share) + '</th><th scope="col">' + esc(T.c_bal) + "</th></tr></thead><tbody>" + lignes + "</tbody></table></div>";
    var lien = location.origin + location.pathname + "#d=" + enc(S);
    var texte = T.wa_head + "\n" + fill(T.wa_total, { t: argent(total) }) + "\n" +
      (v.length ? v.map(function (x) { return "• " + fill(T.owes, { a: nom(x.de), b: nom(x.a), x: argent(x.v) }); }).join("\n") : T.even) + "\n\n" + T.wa_link + " " + lien;
    $("pf-wa").href = "https://wa.me/?text=" + encodeURIComponent(texte);
    $("pf-copy").dataset.lien = lien;
  }
  function maj() { garder(); dessiner(); }
  var dire = function (id, t) { $(id).textContent = t || ""; };

  $("pf-pform").addEventListener("submit", function (e) {
    e.preventDefault();
    var i = $("pf-name"), n = i.value.trim().slice(0, 24);
    if (!n) return;
    if (S.people.some(function (p) { return p.n.toLowerCase() === n.toLowerCase(); })) { dire("pf-pmsg", T.dup); return; }
    if (S.people.length >= 30) return;
    S.people.push({ id: S.next++, n: n }); i.value = ""; dire("pf-pmsg"); maj(); i.focus();
  });
  $("pf-cur").addEventListener("change", function () { S.cur = this.value; maj(); });
  $("pf-eform").addEventListener("submit", function (e) {
    e.preventDefault();
    var a = Math.round(parseFloat(String($("pf-amount").value).replace(",", ".")) * 100);
    var f = [].filter.call(document.querySelectorAll("#pf-for input"), function (i) { return i.checked; }).map(function (i) { return +i.value; });
    if (!(a > 0) || a >= 1e11) { dire("pf-emsg", T.e_amount); return; }
    if (!f.length) { dire("pf-emsg", T.e_for); return; }
    if (S.exp.length >= 200) return;
    S.exp.push({ l: $("pf-label").value.trim().slice(0, 40), a: a, by: +$("pf-by").value, f: f });
    $("pf-label").value = ""; $("pf-amount").value = ""; dire("pf-emsg");
    [].forEach.call(document.querySelectorAll("#pf-for input"), function (i) { i.checked = true; });
    maj(); $("pf-label").focus();
  });
  root.addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    if (b.dataset.delE) { S.exp.splice(+b.dataset.delE, 1); maj(); }
    if (b.dataset.delP) {
      var id = +b.dataset.delP;
      if (S.exp.some(function (x) { return x.by === id || x.f.indexOf(id) !== -1; })) { dire("pf-pmsg", fill(T.used, { n: nom(id) })); return; }
      S.people = S.people.filter(function (p) { return p.id !== id; }); dire("pf-pmsg"); maj();
    }
  });
  $("pf-copy").addEventListener("click", function () {
    var b = this, l = b.dataset.lien, fait = function () { var o = b.textContent; b.textContent = T.copied; setTimeout(function () { b.textContent = o; }, 1800); };
    if (navigator.clipboard) navigator.clipboard.writeText(l).then(fait, function () { prompt(T.copy, l); }); else prompt(T.copy, l);
  });
  $("pf-reset").addEventListener("click", function () {
    if (!confirm(T.reset_q)) return;
    S = vide(); try { localStorage.removeItem(KEY); } catch (e) {} dessiner();
  });
  dessiner();
})();
