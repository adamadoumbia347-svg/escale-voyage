/* Animations du site (motion design) : apparition au défilement, cartes en relief, photo d'ouverture en parallaxe,
   barre de progression de lecture. Rien ne s'anime si l'appareil demande moins d'animations ou économise les données.
   Sans JavaScript, tout le contenu reste visible : les éléments ne sont masqués qu'une fois ce script lancé. */
(function () {
  "use strict";
  var mq = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: true };
  var conn = navigator.connection || {};
  if (mq.matches || conn.saveData || !("IntersectionObserver" in window)) return;
  var root = document.documentElement, vh = window.innerHeight || 800;
  root.classList.add("mo");

  // 1. Apparition au défilement : seulement pour ce qui est sous l'écran au chargement (pas de saut, pas de retard sur le haut de page)
  var sel = "[data-rv], main .wrap > section, main .wrap > article, section.block, .vx-card, .vx-hub a, .tool-card, .guide-card";
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("rv-in"); io.unobserve(e.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
  var n = 0;
  document.querySelectorAll(sel).forEach(function (el) {
    if (el.closest(".rv")) return; // pas d'animation imbriquée
    var r = el.getBoundingClientRect();
    if (r.top < vh * 0.92) return;
    el.classList.add("rv"); el.style.setProperty("--rv-d", (n++ % 3) * 70 + "ms"); io.observe(el);
  });

  // 2. Barre de progression de lecture (pages longues)
  var bar = null;
  if (document.body.scrollHeight > vh * 2.2) {
    bar = document.createElement("div"); bar.className = "mo-bar"; bar.setAttribute("aria-hidden", "true"); document.body.appendChild(bar);
  }

  // 3. Parallaxe de la photo d'ouverture et des photos de cartes (transform uniquement : aucun recalcul de mise en page)
  var hero = document.querySelector(".vx-hero img"), cards = [].slice.call(document.querySelectorAll(".vx-card .vx-ph img")), tick = false;
  function frame() {
    tick = false;
    var y = window.scrollY || 0;
    if (bar) bar.style.transform = "scaleX(" + Math.min(1, y / Math.max(1, document.documentElement.scrollHeight - vh)) + ")";
    if (hero && y < vh * 1.2) hero.style.transform = "translate3d(0," + (y * 0.18).toFixed(1) + "px,0) scale(" + (1.06 + y / 6000).toFixed(4) + ")";
    for (var i = 0; i < cards.length; i++) {
      var r = cards[i].parentNode.getBoundingClientRect();
      if (r.bottom < -50 || r.top > vh + 50) continue;
      var k = (r.top + r.height / 2 - vh / 2) / vh; // -0.5 … 0.5
      cards[i].style.transform = "translate3d(0," + (-k * 26).toFixed(1) + "px,0) scale(1.12)";
    }
  }
  window.addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });
  frame();

  // 4. Cartes en relief : elles s'inclinent sous le pointeur (souris ou stylet, pas au doigt)
  if (window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.querySelectorAll(".vx-card, .vx-hub a, .vz-row a").forEach(function (c) {
      c.addEventListener("pointermove", function (e) {
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        c.style.transform = "perspective(900px) rotateY(" + (x * 7).toFixed(2) + "deg) rotateX(" + (-y * 6).toFixed(2) + "deg) translateZ(0)";
        c.style.setProperty("--gx", ((x + 0.5) * 100).toFixed(0) + "%"); c.style.setProperty("--gy", ((y + 0.5) * 100).toFixed(0) + "%");
      });
      c.addEventListener("pointerleave", function () { c.style.transform = ""; });
    });
  }
})();
