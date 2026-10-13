// Bandeau de consentement aux cookies (Escale).
// Les scripts marqués <script type="text/plain" data-consent="marketing"> ne s'exécutent
// qu'après un clic sur « Accepter ». Le choix est gardé 6 mois, puis redemandé (recommandation CNIL).
(function () {
  "use strict";
  var KEY = "escale.consent.v1";
  var MAX_AGE = 1000 * 60 * 60 * 24 * 182; // environ 6 mois

  function read() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY));
      if (v && (v.choice === "accept" || v.choice === "refuse") && Date.now() - v.ts < MAX_AGE) return v.choice;
    } catch (e) {}
    return null;
  }
  function save(choice) {
    try { localStorage.setItem(KEY, JSON.stringify({ choice: choice, ts: Date.now() })); } catch (e) {}
  }

  var activated = false;
  function activate() {
    if (activated) return;
    activated = true;
    var blocked = document.querySelectorAll('script[type="text/plain"][data-consent="marketing"]');
    for (var i = 0; i < blocked.length; i++) {
      var old = blocked[i], s = document.createElement("script");
      for (var j = 0; j < old.attributes.length; j++) {
        var a = old.attributes[j];
        if (a.name !== "type" && a.name !== "data-consent") s.setAttribute(a.name, a.value);
      }
      s.text = old.text;
      old.parentNode.replaceChild(s, old);
    }
  }

  var css = "" +
    ".cc-bar{position:fixed;left:0;right:0;bottom:0;z-index:1000;padding:16px 16px calc(16px + env(safe-area-inset-bottom,0px));" +
    "background:var(--surface,#fff);color:var(--ink,#141a24);border-top:1px solid var(--line,#d9dee6);box-shadow:0 -10px 30px -20px rgba(0,0,0,.4);" +
    "font:400 14px/1.5 var(--f-body,system-ui,sans-serif)}" +
    ".cc-in{max-width:980px;margin:0 auto;display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between}" +
    ".cc-txt{flex:1 1 420px;min-width:0;margin:0}" +
    ".cc-txt strong{display:block;font-size:15px;margin-bottom:2px}" +
    ".cc-btns{display:flex;gap:10px;flex-wrap:wrap}" +
    ".cc-btn{appearance:none;cursor:pointer;font:700 15px/1 var(--f-body,system-ui,sans-serif);padding:12px 18px;border-radius:10px;" +
    "border:1px solid var(--ink,#141a24);background:var(--surface,#fff);color:var(--ink,#141a24);min-width:120px}" +
    ".cc-btn:hover{background:var(--ink,#141a24);color:var(--surface,#fff)}" +
    ".cc-btn:focus-visible{outline:3px solid var(--focus,#0b5cd6);outline-offset:2px}";

  var bar = null;
  function show() {
    if (bar) { bar.hidden = false; bar.querySelector("button").focus(); return; }
    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);
    bar = document.createElement("div");
    bar.className = "cc-bar";
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-label", "Cookies");
    var lang = (document.documentElement.lang || "fr").slice(0, 2);
    var M = {
      fr: ["Cookies partenaires", "Avec votre accord, notre partenaire Travelpayouts utilise des cookies pour savoir que vous venez d’Escale quand vous réservez. Cela nous permet de rester gratuits. Refuser ne change rien aux recherches.", "En savoir plus", "Refuser", "Accepter"],
      en: ["Partner cookies", "With your consent, our partner Travelpayouts uses cookies to know you came from Escale when you book. This keeps the site free. Declining changes nothing for your searches.", "Learn more", "Decline", "Accept"],
      es: ["Cookies de socios", "Con tu consentimiento, nuestro socio Travelpayouts usa cookies para saber que vienes de Escale cuando reservas. Así el sitio sigue siendo gratuito. Rechazar no cambia nada en tus búsquedas.", "Más información", "Rechazar", "Aceptar"],
      pt: ["Cookies de parceiros", "Com o seu consentimento, o nosso parceiro Travelpayouts usa cookies para saber que veio da Escale quando reserva. Isto mantém o site gratuito. Recusar não muda nada nas pesquisas.", "Saber mais", "Recusar", "Aceitar"],
      ar: ["ملفات تعريف الارتباط للشركاء", "بموافقتك، يستخدم شريكنا Travelpayouts ملفات تعريف الارتباط ليعرف أنك جئت من Escale عند الحجز. هذا ما يبقي الموقع مجانيًا. الرفض لا يغيّر شيئًا في عمليات البحث.", "اعرف المزيد", "رفض", "قبول"]
    }[lang] || null;
    if (!M) M = ["Cookies partenaires", "Avec votre accord, notre partenaire Travelpayouts utilise des cookies pour savoir que vous venez d’Escale quand vous réservez. Cela nous permet de rester gratuits. Refuser ne change rien aux recherches.", "En savoir plus", "Refuser", "Accepter"];
    bar.setAttribute("aria-label", M[0]);
    bar.innerHTML =
      '<div class="cc-in"><p class="cc-txt"><strong>' + M[0] + "</strong>" + M[1] + " " +
      '<a href="/confidentialite/">' + M[2] + "</a></p>" +
      '<div class="cc-btns"><button type="button" class="cc-btn" data-cc="refuse">' + M[3] + "</button>" +
      '<button type="button" class="cc-btn" data-cc="accept">' + M[4] + "</button></div></div>";
    bar.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-cc]");
      if (!b) return;
      var choice = b.getAttribute("data-cc"), wasActive = activated;
      save(choice);
      bar.hidden = true;
      if (choice === "accept") activate();
      // Retrait du consentement : recharger la page pour arrêter le script déjà chargé
      else if (wasActive) location.reload();
    });
    document.body.appendChild(bar);
  }

  // Lien « Gérer les cookies » présent dans le pied de page
  document.addEventListener("click", function (ev) {
    var l = ev.target.closest("[data-open-consent]");
    if (!l) return;
    ev.preventDefault();
    show();
  });

  function start() {
    var c = read();
    if (c === "accept") activate();
    else if (c === null) show();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
