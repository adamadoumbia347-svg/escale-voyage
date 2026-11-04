// Sur toutes les pages : bulle « Bons plans sur WhatsApp » (en bas à droite) et compteur de clics anonyme.
// Le compteur n'utilise aucun cookie et n'enregistre ni adresse IP ni identifiant : seulement « tel lien, tel jour, tel type de page »,
// pour savoir ce qui sert vraiment (Aviasales, moteur en direct, hôtels, WhatsApp…). Résultats dans /admin/.
(function () {
  "use strict";
  var path = location.pathname;
  if (/^\/(admin|outils)\//.test(path)) return;
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var CHANNEL = "https://whatsapp.com/channel/0029VbE28kB0LKZN7ypnGj0d";
  // Bas de page : passer en version légère (moins de données) ou revenir à la version complète (scripts/build_pages.py, lite_mode)
  (function () {
    var foot = document.querySelector("footer");
    if (!foot) return;
    var lite = document.documentElement.classList.contains("lite");
    var T = {
      fr: ["Version légère (moins de données) · Afficher la version complète", "Passer en version légère (moins de données)"],
      en: ["Light version (less data) · Show the full version", "Switch to the light version (less data)"],
      es: ["Versión ligera (menos datos) · Ver la versión completa", "Pasar a la versión ligera (menos datos)"],
      pt: ["Versão leve (menos dados) · Ver a versão completa", "Mudar para a versão leve (menos dados)"],
      ar: ["النسخة الخفيفة (بيانات أقل) · اعرض النسخة الكاملة", "انتقل إلى النسخة الخفيفة (بيانات أقل)"],
      it: ["Versione leggera (meno dati) · Mostra la versione completa", "Passa alla versione leggera (meno dati)"],
      de: ["Leichte Version (weniger Daten) · Vollständige Version anzeigen", "Zur leichten Version wechseln (weniger Daten)"],
      nl: ["Lichte versie (minder data) · Volledige versie tonen", "Naar de lichte versie (minder data)"]
    }[lang] || ["Version légère · Afficher la version complète", "Passer en version légère"];
    var p = document.createElement("p"), b = document.createElement("button");
    b.type = "button"; b.className = "lite-toggle"; b.textContent = lite ? T[0] : T[1];
    b.addEventListener("click", function () { try { localStorage.setItem("escale.lite", lite ? "0" : "1"); } catch (e) {} location.reload(); });
    p.className = "small"; p.appendChild(b); foot.appendChild(p);
  })();
  var L = { fr: "Bons plans sur WhatsApp", en: "Deals on WhatsApp", es: "Ofertas en WhatsApp", pt: "Promoções no WhatsApp", ar: "العروض على واتساب", it: "Offerte su WhatsApp", de: "Angebote auf WhatsApp", nl: "Deals op WhatsApp" }[lang] || "Bons plans sur WhatsApp";

  // Bulle WhatsApp (masquable pour la visite)
  var closed = false; try { closed = sessionStorage.getItem("escale.wa") === "0"; } catch (e) {}
  if (!closed) {
    var w = document.createElement("div");
    w.className = "wa-float";
    w.innerHTML = '<a href="' + CHANNEL + '" target="_blank" rel="noopener" data-k="whatsapp-bulle" aria-label="' + L + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8 0-1.3.7-2 1-2.3.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.7-.1l.9-1.1c.2-.3.4-.2.7-.1l1.9.9c.3.1.5.2.5.3.1.2.1.6-.1 1.2z"/></svg><span>' + L + '</span></a>' +
      '<button type="button" aria-label="×">×</button>';
    w.querySelector("button").addEventListener("click", function () { w.remove(); try { sessionStorage.setItem("escale.wa", "0"); } catch (e) {} });
    var add = function () { document.body.appendChild(w); };
    if (document.body) add(); else document.addEventListener("DOMContentLoaded", add);
  }

  // Appli installable : service worker + message « Installer Escale » à partir de la 2e visite
  if ("serviceWorker" in navigator) addEventListener("load", function () { navigator.serviceWorker.register("/sw.js").catch(function () {}); });
  var I = { fr: ["Installer Escale sur votre téléphone : les prix en un clic, comme une appli.", "Installer", "Sur iPhone : touchez Partager puis « Sur l’écran d’accueil »."],
    en: ["Install Escale on your phone: prices in one tap, like an app.", "Install", "On iPhone: tap Share, then “Add to Home Screen”."],
    es: ["Instala Escale en tu móvil: los precios en un toque, como una app.", "Instalar", "En iPhone: toca Compartir y luego «Añadir a pantalla de inicio»."],
    pt: ["Instale a Escale no telemóvel: os preços num toque, como uma app.", "Instalar", "No iPhone: toque em Partilhar e depois «Adicionar ao ecrã principal»."],
    ar: ["ثبّت Escale على هاتفك: الأسعار بلمسة واحدة مثل التطبيق.", "تثبيت", "على آيفون: اضغط مشاركة ثم «إضافة إلى الشاشة الرئيسية»."],
    it: ["Installa Escale sul telefono: i prezzi con un tocco, come un’app.", "Installa", "Su iPhone: tocca Condividi e poi «Aggiungi alla schermata Home»."],
    de: ["Installiere Escale auf dem Handy: die Preise mit einem Fingertipp, wie eine App.", "Installieren", "Auf dem iPhone: Tippe auf Teilen und dann auf „Zum Home-Bildschirm“."],
    nl: ["Installeer Escale op je telefoon: de prijzen met één tik, als een app.", "Installeren", "Op iPhone: tik op Delen en dan op ‘Zet op beginscherm’."] }[lang] || null;
  var store = function (k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } };
  var visits = +(store("escale.visites") || 0);
  try { if (!sessionStorage.getItem("escale.v")) { sessionStorage.setItem("escale.v", "1"); store("escale.visites", String(++visits)); } } catch (e) {}
  var standalone = matchMedia("(display-mode: standalone)").matches || navigator.standalone;
  var deferred = null;
  addEventListener("beforeinstallprompt", function (ev) { ev.preventDefault(); deferred = ev; });
  var ios = /iphone|ipad|ipod/i.test(navigator.userAgent) && !/crios|fxios/i.test(navigator.userAgent);
  if (I && visits >= 2 && !standalone && !store("escale.install.non") && !/^\/recherche\//.test(path)) {
    setTimeout(function () {
      if (document.querySelector(".cc-bar") || (!deferred && !ios)) return; // bandeau des cookies affiché, ou installation impossible
      var b = document.createElement("div");
      b.className = "inst-bar";
      b.innerHTML = '<img src="/icon-192.png" alt="" width="36" height="36"><p></p>' + (deferred ? '<button type="button" class="inst-go"></button>' : "") + '<button type="button" class="inst-x" aria-label="×">×</button>';
      b.querySelector("p").textContent = ios && !deferred ? I[0] + " " + I[2] : I[0];
      if (deferred) b.querySelector(".inst-go").textContent = I[1];
      b.addEventListener("click", function (ev) {
        if (ev.target.closest(".inst-go") && deferred) { deferred.prompt(); send("installer-appli"); deferred = null; b.remove(); }
        if (ev.target.closest(".inst-x")) { store("escale.install.non", "1"); b.remove(); }
      });
      document.body.appendChild(b);
    }, 4000);
  }

  // « Vos trajets » : les trajets consultés sont gardés dans ce navigateur (rien n'est envoyé), pour les retrouver sur l'accueil
  var remember = function (f, t, label, url, price) {
    var list = []; try { list = JSON.parse(store("escale.trajets") || "[]"); } catch (e) { list = []; }
    var old = list.filter(function (x) { return x.f === f && x.t === t; })[0];
    list = list.filter(function (x) { return !(x.f === f && x.t === t); });
    list.unshift({ f: f, t: t, l: label || (old && old.l) || f + " → " + t, u: url || (old && old.u) || "", p: old ? old.p : price || null, ts: Date.now() });
    store("escale.trajets", JSON.stringify(list.slice(0, 6)));
  };
  addEventListener("load", function () {
    var rp = document.getElementById("route-prices");
    if (rp && rp.getAttribute("data-from")) {
      var h1 = document.querySelector("h1"), label = h1 ? h1.textContent.replace(/^\s*(Vol pas cher|Cheap flights?|Vuelos? baratos?|Voos? baratos?|Voli economici)\s*/i, "").replace(/\s+/g, " ").trim() : "";
      var st = document.querySelector("#hero-price strong"), price = st ? Number(st.textContent.replace(/[^0-9]/g, "")) || null : null;
      remember(rp.getAttribute("data-from"), rp.getAttribute("data-to"), label, path, price);
    }
    var fs = new URLSearchParams(location.search).get("flightSearch");
    var m = fs && fs.match(/^([A-Z]{3})\d{4}([A-Z]{3})/);
    if (m) remember(m[1], m[2], null, "/recherche/?flightSearch=" + fs, null);
  });

  // Compteur de clics
  var page = path === "/" ? "accueil" : /^\/recherche\//.test(path) ? "recherche" : /^\/vols-ete-/.test(path) ? "ete"
    : /^\/(vol-|(en|es|pt|ar)\/(flights|vuelos|voos)-|it\/voli-)/.test(path) ? "trajet" : /^\/vols-pour-|\/(flights|vuelos|voos)-(to|a|para)-/.test(path) ? "destination" : "autre";
  var kind = function (a) {
    if (a.dataset && a.dataset.k) return a.dataset.k;
    if (a.classList.contains("pop-chip")) return "trajet-populaire";
    if (a.classList.contains("season")) return "bandeau-saison";
    var h; try { h = new URL(a.href, location.href); } catch (e) { return null; }
    if (h.host === location.host) return /^\/recherche\//.test(h.pathname) ? "moteur-lien" : null;
    var host = h.host.replace(/^www\./, "");
    if (/aviasales\./.test(host)) return "aviasales";
    if (/stay22\./.test(host)) return "stay22";
    if (/(^|\.)trip\.com$/.test(host)) return "tripcom";
    if (/\.tpm\.lv$/.test(host)) return host.split(".")[0];
    if (host === "tp.media") return /campaign_id=137\b/.test(h.search) ? "klook" : "tp-media";
    if (/whatsapp\.com$/.test(host)) return "whatsapp";
    if (/^wa\.me$/.test(host)) return "partage-whatsapp";
    var m = host.match(/(skyscanner|kayak|momondo|booking|google|airbnb|agoda|safetywing)/);
    return m ? m[1] : "autre-site";
  };
  var send = function (k) {
    var body = JSON.stringify({ k: k, p: page });
    try { if (navigator.sendBeacon && navigator.sendBeacon("/api/clic", body)) return; } catch (e) {}
    try { fetch("/api/clic", { method: "POST", body: body, keepalive: true }); } catch (e) {}
  };
  document.addEventListener("click", function (ev) {
    var t = ev.target;
    if (t && t.closest && t.closest("#tpwl-tickets")) { send("moteur-resultat"); return; }
    var a = t && t.closest && t.closest("a[href]");
    if (!a) return;
    var k = kind(a);
    if (k) send(k);
  }, true);
})();
