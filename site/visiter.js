/* Rubrique « Que visiter » : envies gardées dans le téléphone (sans compte), recherche d'un pays ou d'un lieu,
   prix du moment depuis la ville du visiteur, partage. Rien n'est envoyé : les envies restent dans le navigateur. */
(function () {
  "use strict";
  var KEY = "escale.envies", $ = function (s, r) { return (r || document).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  function lire() { try { var v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v.filter(function (x) { return x && x.k && x.n && x.u; }).slice(0, 200) : []; } catch (e) { return []; } }
  function ecrire(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} }
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };

  // ---- 1. Cœur sur chaque lieu
  function maj() {
    var L = lire(), ks = L.map(function (x) { return x.k; });
    $$(".vx-like").forEach(function (b) { var on = ks.indexOf(b.dataset.k) >= 0; b.setAttribute("aria-pressed", on ? "true" : "false"); b.title = on ? "Retirer de mes envies" : "Ajouter à mes envies"; });
    $$("[data-envies-n]").forEach(function (e) { e.textContent = L.length; e.hidden = !L.length; });
    var box = $("#vx-envies");
    if (box) {
      box.hidden = !L.length;
      var ul = $("ul", box);
      if (ul) ul.innerHTML = L.map(function (x) {
        return '<li><a href="' + esc(x.u) + '"><img src="/img/visiter/' + esc(x.k) + '-640.webp" alt="" width="64" height="64" loading="lazy"><span><b>' + esc(x.n) + "</b><small>" + esc(x.p || "") +
          '</small></span></a><button type="button" class="vx-rm" data-k="' + esc(x.k) + '" aria-label="Retirer ' + esc(x.n) + '">×</button></li>';
      }).join("");
    }
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".vx-like, .vx-rm");
    if (!b) return;
    var L = lire(), k = b.dataset.k, i = L.map(function (x) { return x.k; }).indexOf(k);
    if (i >= 0) L.splice(i, 1);
    else if (b.classList.contains("vx-like") && /^[a-z]{2}-[a-z0-9]+$/.test(k)) { L.unshift({ k: k, n: b.dataset.n, p: b.dataset.p, u: location.pathname + "#" + k }); b.classList.remove("pop"); void b.offsetWidth; b.classList.add("pop"); }
    ecrire(L); maj();
  });
  maj();

  // ---- 2. Recherche sur le sommaire (pays ou lieu)
  var q = $("#vx-q");
  if (q) {
    var norm = function (t) { return t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
    q.addEventListener("input", function () {
      var v = norm(q.value.trim()), n = 0;
      $$(".vx-hub a[data-mots]").forEach(function (a) { var ok = !v || norm(a.dataset.mots).indexOf(v) >= 0; a.hidden = !ok; if (ok) n++; });
      $$(".vx-reg").forEach(function (h) { var g = h.nextElementSibling; h.hidden = !g || !$$("a:not([hidden])", g).length; });
      var m = $("#vx-q-msg"); if (m) m.textContent = v ? (n ? n + " pays correspond" + (n > 1 ? "ent" : "") : "Aucun pays pour cette recherche pour l'instant.") : "";
    });
  }

  // ---- 3. Prix du moment depuis la ville du visiteur (chargé quand le bloc approche de l'écran)
  var cta = $(".vx-cta[data-air]");
  if (cta && "IntersectionObserver" in window) {
    var VILLES = { PAR: "Paris", LYS: "Lyon", MRS: "Marseille", NCE: "Nice", TLS: "Toulouse", BRU: "Bruxelles", GVA: "Genève", MIL: "Milan", ROM: "Rome", LON: "Londres", MAD: "Madrid", AMS: "Amsterdam", FRA: "Francfort", YMQ: "Montréal", NYC: "New York" };
    var AERO = { PAR: "CDG", MIL: "MXP", ROM: "FCO", LON: "LHR", YMQ: "YUL", NYC: "JFK" }; // aéroport connu du moteur, pour le lien de recherche
    var PAYS = { FR: "PAR", BE: "BRU", CH: "GVA", IT: "MIL", GB: "LON", ES: "MAD", NL: "AMS", DE: "FRA", CA: "YMQ", US: "NYC", LU: "BRU" };
    var out = $(".vx-prix", cta), sel = $("select", cta), air = cta.dataset.air, MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
    var jour = function (d) { var p = d.split("-"); return +p[2] + " " + MOIS[+p[1] - 1]; };
    Object.keys(VILLES).forEach(function (c) { if ((AERO[c] || c) !== air) { var o = document.createElement("option"); o.value = c; o.textContent = VILLES[c]; sel.appendChild(o); } });
    var charger = function (from) {
      if (!from || (AERO[from] || from) === air) { out.textContent = ""; return; }
      out.textContent = "Recherche du prix du moment…";
      var d = new Date(), mois = [1, 2, 3].map(function (i) { var x = new Date(d.getFullYear(), d.getMonth() + i, 1); return x.getFullYear() + "-" + ("0" + (x.getMonth() + 1)).slice(-2); });
      Promise.all(mois.map(function (m) { return fetch("/api/calendar?from=" + from + "&to=" + air + "&month=" + m + "&currency=EUR").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); })).then(function (rs) {
        var best = null;
        rs.forEach(function (j) { if (!j || !j.days || (j.currency && j.currency !== "EUR")) return; Object.keys(j.days).forEach(function (k) { var x = j.days[k]; if (x && x.price > 0 && x.ret && (!best || x.price < best.price)) best = { price: x.price, dep: k, ret: x.ret }; }); });
        if (!best) { out.textContent = "Pas de prix repéré depuis " + VILLES[from] + " pour l'instant : lancez la recherche pour voir les vols."; return; }
        out.innerHTML = "<strong>" + esc(VILLES[from]) + " → " + esc(cta.dataset.ville) + " : dès " + Math.round(best.price).toLocaleString("fr-FR") + " € aller-retour</strong> (" + jour(best.dep) + " → " + jour(best.ret) +
          "). Prix repéré récemment, il peut changer.";
        var a = $("a.btn", cta); if (a) a.href = "/?type=vols&from=" + (AERO[from] || from) + "&to=" + air + "&dep=" + best.dep + "&ret=" + best.ret;
      });
    };
    sel.addEventListener("change", function () { try { localStorage.setItem("escale.depart", sel.value); } catch (e) {} charger(sel.value); });
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; io.disconnect();
      var memo = null; try { memo = localStorage.getItem("escale.depart"); } catch (e) {}
      var go = function (c) { if (c && VILLES[c] && (AERO[c] || c) !== air) { sel.value = c; charger(c); } };
      if (memo) return go(memo);
      fetch("/api/geo").then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; }).then(function (g) { go(PAYS[g.country] || "PAR"); });
    }, { rootMargin: "500px 0px" });
    io.observe(cta);
  }

  // ---- 4. Partage
  var sh = $("#vx-share");
  if (sh) sh.addEventListener("click", function () {
    var d = { title: document.title, text: sh.dataset.t, url: location.origin + location.pathname };
    if (navigator.share) navigator.share(d).catch(function () {});
    else window.open("https://wa.me/?text=" + encodeURIComponent(d.text + " " + d.url), "_blank", "noopener");
  });
})();
