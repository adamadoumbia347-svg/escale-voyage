// Accueil : thèmes en onglets (un seul bloc visible à la fois, les photos et les prix d'un bloc ne se chargent qu'à son ouverture)
// et photos animées (lent zoom, seulement quand la carte est à l'écran ; coupé en mode léger et si l'animation est réduite).
(function () {
  "use strict";
  var hub = document.getElementById("hub");
  if (hub) {
    var tabs = [].slice.call(hub.querySelectorAll(".hub-tab"));
    var panels = function (t) { return t.getAttribute("data-p").split(",").map(function (id) { return document.getElementById(id); }).filter(Boolean); };
    var usable = function (t) { return panels(t).some(function (p) { return !p.hidden; }); };
    var KEY = "escale.hub";
    var select = function (t, save) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute("aria-selected", on ? "true" : "false");
        x.tabIndex = on ? 0 : -1;
        panels(x).forEach(function (p) { p.classList.toggle("hub-off", !on); });
      });
      if (save) try { localStorage.setItem(KEY, t.id); } catch (e) {}
      var bar = t.parentNode; if (bar && bar.scrollTo) bar.scrollTo({ left: Math.max(0, t.offsetLeft - bar.offsetLeft - 16), behavior: save ? "smooth" : "auto" });
    };
    var refresh = function () {
      tabs.forEach(function (t) { t.hidden = !usable(t); });
      var cur = tabs.filter(function (t) { return t.getAttribute("aria-selected") === "true"; })[0];
      if (!cur || cur.hidden) { var f = tabs.filter(function (t) { return !t.hidden; })[0]; if (f) select(f); }
    };
    tabs.forEach(function (t) {
      t.addEventListener("click", function () { select(t, true); });
      t.addEventListener("keydown", function (e) {
        var vis = tabs.filter(function (x) { return !x.hidden; }), i = vis.indexOf(t);
        var n = e.key === "ArrowRight" ? vis[i + 1] : e.key === "ArrowLeft" ? vis[i - 1] : null;
        if (n) { e.preventDefault(); select(n, true); n.focus(); }
      });
    });
    // Un bloc peut se cacher tout seul (pas de prix pour « Rentrer au pays », pas d'API) : son onglet aussi
    if ("MutationObserver" in window) {
      var mo = new MutationObserver(refresh);
      tabs.forEach(function (t) { panels(t).forEach(function (p) { mo.observe(p, { attributes: true, attributeFilter: ["hidden"] }); }); });
    }
    // Ouverture : lien /#calculateur, /#fetes… sinon le dernier thème choisi, sinon « Bons plans »
    var openHash = function () {
      var h = (location.hash || "").slice(1); if (h === "calc") h = "calculateur";
      var t = h && tabs.filter(function (x) { return x.id === "ht-" + h || x.getAttribute("data-p").split(",").indexOf(h) >= 0; })[0];
      if (t) { select(t); var el = document.getElementById(h) || hub; setTimeout(function () { el.scrollIntoView({ block: "start" }); }, 50); return true; }
      return false;
    };
    if (!openHash()) {
      var saved = null; try { saved = localStorage.getItem(KEY); } catch (e) {}
      var st = saved && document.getElementById(saved);
      select(st && tabs.indexOf(st) >= 0 ? st : tabs[0]);
    }
    refresh();
    window.addEventListener("hashchange", openHash);
    // Carte « Comparer les hôtels » : passe le moteur sur Hôtels et remonte
    hub.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[data-tab]"); if (!a) return;
      e.preventDefault();
      location.hash = a.getAttribute("data-tab");
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  // Photos animées
  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || root.classList.contains("lite") || !("IntersectionObserver" in window)) return;
  root.classList.add("kb-on");
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { e.target.classList.toggle("kb-run", e.isIntersecting); });
  }, { threshold: 0.2 });
  document.querySelectorAll(".inspi-card, .city-card").forEach(function (c) { io.observe(c); });
})();
