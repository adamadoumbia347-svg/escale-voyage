// Accueil : prix du jour (baromètre), compteur de recherches de la semaine, « Ta prochaine escale » et « Le bon plan du jour ».
// Tout vient de vraies données : /api/verdict (prix relevés chaque jour), /api/compteur (clics anonymes des 7 derniers jours),
// les trajets gardés dans ce navigateur (escale.trajets) et la grille des idées de voyage (#ex-grid). Rien n'est inventé :
// sans donnée, le bloc reste caché.
(function () {
  "use strict";
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var W = {
    fr: { deal: "Bon prix aujourd'hui", vs: "sous le prix habituel", seen: "relevé le {d}", count: "{n} recherches comparées cette semaine sur Escale",
          next: "Ta prochaine escale", since: "depuis ta dernière visite", go: "Voir les vols", top: "Le bon plan du jour", topGo: "Voir ce vol", rt: "aller-retour" },
    en: { deal: "Good price today", vs: "below the usual price", seen: "checked on {d}", count: "{n} searches compared on Escale this week",
          next: "Your next trip", since: "since your last visit", go: "See flights", top: "Deal of the day", topGo: "See this flight", rt: "round trip" },
    es: { deal: "Buen precio hoy", vs: "por debajo del precio habitual", seen: "visto el {d}", count: "{n} búsquedas comparadas esta semana en Escale",
          next: "Tu próximo viaje", since: "desde tu última visita", go: "Ver vuelos", top: "La oferta del día", topGo: "Ver este vuelo", rt: "ida y vuelta" },
    pt: { deal: "Bom preço hoje", vs: "abaixo do preço habitual", seen: "visto a {d}", count: "{n} pesquisas comparadas esta semana no Escale",
          next: "A tua próxima viagem", since: "desde a tua última visita", go: "Ver voos", top: "A promoção do dia", topGo: "Ver este voo", rt: "ida e volta" },
    ar: { deal: "سعر جيد اليوم", vs: "أقل من السعر المعتاد", seen: "سُجّل في {d}", count: "{n} عملية بحث ومقارنة هذا الأسبوع على Escale",
          next: "رحلتك القادمة", since: "منذ زيارتك الأخيرة", go: "عرض الرحلات", top: "عرض اليوم", topGo: "عرض هذه الرحلة", rt: "ذهاب وعودة" },
    it: { deal: "Buon prezzo oggi", vs: "sotto il prezzo abituale", seen: "rilevato il {d}", count: "{n} ricerche confrontate questa settimana su Escale",
          next: "Il tuo prossimo viaggio", since: "dalla tua ultima visita", go: "Vedi i voli", top: "L'offerta del giorno", topGo: "Vedi questo volo", rt: "andata e ritorno" },
    de: { deal: "Guter Preis heute", vs: "unter dem üblichen Preis", seen: "erfasst am {d}", count: "{n} verglichene Suchen diese Woche bei Escale",
          next: "Deine nächste Reise", since: "seit deinem letzten Besuch", go: "Flüge ansehen", top: "Angebot des Tages", topGo: "Diesen Flug ansehen", rt: "hin und zurück" }
  }[lang] || null;
  if (!W) return;
  var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn", it: "it-IT", de: "de-DE" }[lang];
  var f = function (s, o) { return s.replace(/\{(\w+)\}/g, function (m, k) { return k in o ? o[k] : m; }); };
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var money = function (n) { if (window.ESCALE_MONEY) return window.ESCALE_MONEY(n, "EUR"); try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var day = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(loc, { day: "numeric", month: "short" }); } catch (e) { return s; } };
  var get = function (u) { return fetch(u).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); };
  // Noms des villes dans la langue de la page : liste des aéroports d'app.js (chargée juste après l'affichage), 8 s au plus
  var ready = new Promise(function (res) {
    var t0 = Date.now();
    (function wait() {
      if (window.ESCALE_DB_READY) return window.ESCALE_DB_READY.then(function () { return window.ESCALE_AIRPORTS; }).then(res, function () { res(null); });
      if (Date.now() - t0 > 8000) return res(null);
      setTimeout(wait, 200);
    })();
  });
  var names = function () { return lang === "fr" ? Promise.resolve({}) : ready.then(function (list) { var m = {}; (list || []).forEach(function (a) { m[a[0]] = a[1]; }); return m; }).catch(function () { return {}; }); };
  var PAR = /^(CDG|ORY|BVA|PAR)$/;
  var same = function (a, b) { return a === b || (PAR.test(a) && PAR.test(b)); };

  // 1. Prix du jour : le trajet du baromètre le plus en baisse, de préférence au départ de la ville du visiteur
  var deal = document.getElementById("hero-deal");
  if (deal) get("/api/verdict").then(function (d) {
    var it = (d && d.items || []).filter(function (x) { return x.level === "low" && x.price && x.diff >= 8; });
    if (!it.length) return;
    var from = (window.ESCALE_FROM && window.ESCALE_FROM.code) || "CDG";
    var mine = it.filter(function (x) { return same(x.from, from); });
    var x = (mine.length ? mine : it).sort(function (a, b) { return b.diff - a.diff; })[0];
    names().then(function (n) {
      var a = lang === "fr" ? x.label.split(" → ")[0] : (n[x.from] || x.label.split(" → ")[0]);
      var b = lang === "fr" ? x.label.split(" → ")[1] : (n[x.to] || x.label.split(" → ")[1]);
      deal.innerHTML = '<a href="/' + esc(x.path) + '/"><b class="hd-h">🔥 ' + esc(W.deal) + '</b><span class="hd-r"><bdi>' + esc(a + " → " + b) + "</bdi> <strong>" + esc(money(x.price)) + "</strong>"
        + ' <span class="hd-pct">−' + Math.round(x.diff) + ' %</span> →</span><small>' + esc(W.vs) + " · " + esc(f(W.seen, { d: day(x.date) })) + "</small></a>";
      deal.classList.add("on");
    });
  });

  // 2. Compteur de la semaine : affiché seulement à partir de 100 (un petit chiffre ferait peur plus qu'il ne rassure)
  var cnt = document.getElementById("hero-count");
  if (cnt) get("/api/compteur").then(function (d) {
    if (!d || !d.available || !(d.week >= 100)) return;
    var n = new Intl.NumberFormat(loc).format(d.week);
    cnt.textContent = "🔎 " + f(W.count, { n: n }); cnt.hidden = false;
    var meta = cnt.closest(".hero-meta"); if (meta) meta.classList.add("has-count");
  });

  // 3. Ta prochaine escale : le dernier trajet consulté, avec l'évolution du prix depuis la dernière visite (accueil.js garde les prix)
  var nx = document.getElementById("next-escale");
  var list = []; try { list = JSON.parse(localStorage.getItem("escale.trajets") || "[]"); } catch (e) { list = []; }
  if (nx && list.length) {
    var x = list[0], before = x.p;
    var dd = function (n) { var d = new Date(Date.now() + n * 864e5); return String(d.getDate()).padStart(2, "0") + String(d.getMonth() + 1).padStart(2, "0"); };
    get("/api/connus?r=" + x.f + "-" + x.t).then(function (j) {
      var k = j && j.prix && j.prix[x.f + "-" + x.t], now = k && k.price;
      names().then(function (n) {
        var label = lang === "fr" ? x.l : ((n[x.f] || x.f) + " → " + (n[x.t] || x.t));
        var diff = now && before ? now - before : 0;
        var trend = !diff ? "" : '<span class="ne-tr ' + (diff < 0 ? "dn" : "up") + '">' + (diff < 0 ? "↓ " : "↑ ") + esc(money(Math.abs(diff))) + " " + esc(W.since) + "</span>";
        var href = x.u || ("/recherche/?flightSearch=" + x.f + dd(45) + x.t + dd(52) + "1");
        nx.innerHTML = '<span class="ne-h">✈️ ' + esc(W.next) + '</span><bdi class="ne-r">' + esc(label) + "</bdi>" + (now ? '<strong class="ne-p">' + esc(money(now)) + "</strong>" : "") + trend + '<span class="ne-go">' + esc(W.go) + " →</span>";
        nx.href = href; nx.hidden = false;
      });
    });
  }

  // 4. Le bon plan du jour : la destination la moins chère de la grille des idées de voyage, en grand, avec sa photo
  var grid = document.getElementById("ex-grid"), top = document.getElementById("ex-top");
  if (grid && top && "MutationObserver" in window) {
    var paint = function () {
      var c = grid.querySelector(".ex-card:not([hidden])");
      if (!c) { top.hidden = true; return; }
      var img = c.querySelector(".ex-ph img"), name = c.querySelector(".ex-name"), meta = c.querySelector(".ex-meta"), pr = c.querySelector(".ex-price"), fl = c.querySelector(".ex-flag");
      top.innerHTML = '<button type="button" class="ext-card">' + (img ? '<span class="ext-ph"><img src="' + esc(img.getAttribute("src").replace("-480.webp", ".webp")) + '" alt="" width="800" height="600" loading="lazy" decoding="async"></span>' : "")
        + '<span class="ext-body"><span class="ext-h">⭐ ' + esc(W.top) + '</span><strong class="ext-n">' + (fl ? fl.textContent + " " : "") + esc(name ? name.textContent : "") + "</strong>"
        + '<span class="ext-m">' + esc(meta ? meta.textContent : "") + '</span><span class="ext-p">' + esc(pr ? pr.textContent : "") + " <small>" + esc(W.rt) + '</small></span><span class="btn ext-go">' + esc(W.topGo) + " →</span></span></button>";
      top.querySelector(".ext-card").onclick = function () { c.click(); };
      top.hidden = false;
    };
    new MutationObserver(paint).observe(grid, { childList: true, subtree: true, attributes: true, attributeFilter: ["hidden"] });
  }
})();
