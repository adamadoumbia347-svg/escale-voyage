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

  // Grande photo du haut : diaporama lent (une photo toutes les 7 s), chargé après la page, en pause hors écran
  var bg = document.getElementById("hero-bg"), cap = document.getElementById("hero-cap");
  if (bg && document.documentElement.classList.contains("has-hero")) {
    var SL = [["zanzibar", "ZNZ", "Zanzibar"], ["bali", "DPS", "Bali"], ["marrakech", "RAK", "Marrakech", "Marrakesh"], ["dakar", "DSS", "Dakar", null, 1],
      ["tokyo", "HND", "Tokyo"], ["maldives", "MLE", "Maldives"]];
    var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var imgs = [bg.querySelector("img")], k = 0, visible = true, timer = null;
    var start = function () {
      SL.slice(1).forEach(function (x) {
        var im = document.createElement("img"); im.alt = ""; im.decoding = "async"; im.width = 1280; im.height = 960;
        im.srcset = "/img/villes/" + x[0] + ".webp 800w" + (x[4] ? "" : ", /img/villes/" + x[0] + "-1280.webp 1280w"); im.sizes = "100vw";
        im.src = "/img/villes/" + x[0] + ".webp"; bg.appendChild(im); imgs.push(im);
      });
      timer = setInterval(function () {
        if (!visible || document.hidden) return;
        var n = (k + 1) % imgs.length; if (!imgs[n].complete) return;
        imgs[k].classList.remove("on"); imgs[n].classList.add("on"); k = n;
        if (cap) {
          cap.classList.add("fade");
          setTimeout(function () {
            var x = SL[k], en = (document.documentElement.lang || "fr").slice(0, 2) !== "fr";
            cap.querySelector(".hc-city").textContent = en && x[3] ? x[3] : x[2];
            cap.setAttribute("href", "/?type=vols&to=" + x[1]); cap.classList.remove("fade");
          }, 450);
        }
      }, 7000);
    };
    if (!still) {
      var later = function () { (window.requestIdleCallback || function (f) { setTimeout(f, 1500); })(start, { timeout: 4000 }); };
      if (document.readyState === "complete") later(); else window.addEventListener("load", later);
      if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(bg);
    }
  }

  // Photos animées
  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || root.classList.contains("lite") || !("IntersectionObserver" in window)) return;
  root.classList.add("kb-on");
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { e.target.classList.toggle("kb-run", e.isIntersecting); });
  }, { threshold: 0.2 });
  var watch = function () { document.querySelectorAll(".inspi-card, .city-card, .ex-card").forEach(function (c) { if (!c.kbw) { c.kbw = 1; io.observe(c); } }); };
  watch();
  var eg = document.getElementById("ex-grid"); if (eg && "MutationObserver" in window) new MutationObserver(watch).observe(eg, { childList: true });
})();
