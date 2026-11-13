/* Accueil : choix du départ, de l'arrivée et des dates en plein écran (13 novembre 2026, demande de Dobam).
   1. Sur téléphone, toucher « Départ » ou « Arrivée » ouvre un écran entier : on écrit, les villes sortent avec leurs aéroports dessous.
   2. Toucher une date ouvre un calendrier de 12 mois avec, sous chaque jour, le prix aller-retour le plus bas repéré (/api/calendar).
   Les champs du formulaire restent la référence (app.js lit leurs valeurs) : ce script les remplit et déclenche leurs événements.
   Sans ce script, le formulaire fonctionne comme avant (liste déroulante et sélecteur de date du téléphone). */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var fFrom = $("f-from"), fTo = $("f-to"), fDep = $("f-dep"), fRet = $("f-ret");
  if (!fFrom || !fTo || !fDep || !fRet) return;
  var lang = function () { return (document.documentElement.lang || "fr").slice(0, 2); };
  var TXT = {
    fr: { back: "Retour", from: "D’où pars-tu ?", to: "Où vas-tu ?", near: "Aéroport le plus proche", popFrom: "Départs fréquents", popTo: "Destinations populaires", none: "Aucun aéroport trouvé. Essaie le nom de la ville ou le code à 3 lettres.",
      load: "Chargement des aéroports…", all: "Tous les aéroports", dep: "Départ", ret: "Retour", pick: "Choisir", reset: "Réinitialiser", ok: "OK", clear: "Effacer",
      note: "Prix aller-retour le plus bas repéré pour un départ ce jour-là, par personne. Il peut changer.", noteNo: "Choisis le départ et l’arrivée pour voir les prix par jour.", dates: "Choisir les dates" },
    en: { back: "Back", from: "Where from?", to: "Where to?", near: "Nearest airport", popFrom: "Frequent departures", popTo: "Popular destinations", none: "No airport found. Try the city name or the 3-letter code.",
      load: "Loading airports…", all: "All airports", dep: "Depart", ret: "Return", pick: "Choose", reset: "Reset", ok: "OK", clear: "Clear",
      note: "Lowest return fare spotted for a departure that day, per person. It can change.", noteNo: "Choose where from and where to, to see prices by day.", dates: "Choose dates" },
    es: { back: "Volver", from: "¿Desde dónde sales?", to: "¿Adónde vas?", near: "Aeropuerto más cercano", popFrom: "Salidas frecuentes", popTo: "Destinos populares", none: "Ningún aeropuerto encontrado. Prueba con la ciudad o el código de 3 letras.",
      load: "Cargando aeropuertos…", all: "Todos los aeropuertos", dep: "Ida", ret: "Vuelta", pick: "Elegir", reset: "Restablecer", ok: "OK", clear: "Borrar",
      note: "Ida y vuelta más barato visto para una salida ese día, por persona. Puede cambiar.", noteNo: "Elige origen y destino para ver los precios por día.", dates: "Elegir fechas" },
    pt: { back: "Voltar", from: "De onde partes?", to: "Para onde vais?", near: "Aeroporto mais próximo", popFrom: "Partidas frequentes", popTo: "Destinos populares", none: "Nenhum aeroporto encontrado. Tenta a cidade ou o código de 3 letras.",
      load: "A carregar aeroportos…", all: "Todos os aeroportos", dep: "Ida", ret: "Volta", pick: "Escolher", reset: "Repor", ok: "OK", clear: "Apagar",
      note: "Ida e volta mais barata vista para uma partida nesse dia, por pessoa. Pode mudar.", noteNo: "Escolhe a origem e o destino para ver os preços por dia.", dates: "Escolher datas" },
    it: { back: "Indietro", from: "Da dove parti?", to: "Dove vai?", near: "Aeroporto più vicino", popFrom: "Partenze frequenti", popTo: "Destinazioni popolari", none: "Nessun aeroporto trovato. Prova con la città o il codice di 3 lettere.",
      load: "Caricamento degli aeroporti…", all: "Tutti gli aeroporti", dep: "Andata", ret: "Ritorno", pick: "Scegli", reset: "Reimposta", ok: "OK", clear: "Cancella",
      note: "Andata e ritorno più basso rilevato per una partenza quel giorno, a persona. Può cambiare.", noteNo: "Scegli partenza e arrivo per vedere i prezzi per giorno.", dates: "Scegli le date" },
    de: { back: "Zurück", from: "Von wo?", to: "Wohin?", near: "Nächster Flughafen", popFrom: "Häufige Abflugorte", popTo: "Beliebte Ziele", none: "Kein Flughafen gefunden. Versuche den Stadtnamen oder den 3-Buchstaben-Code.",
      load: "Flughäfen werden geladen…", all: "Alle Flughäfen", dep: "Hinflug", ret: "Rückflug", pick: "Wählen", reset: "Zurücksetzen", ok: "OK", clear: "Löschen",
      note: "Günstigster Hin- und Rückflug für einen Abflug an diesem Tag, pro Person. Kann sich ändern.", noteNo: "Wähle Abflug und Ziel, um die Preise pro Tag zu sehen.", dates: "Daten wählen" },
    ar: { back: "رجوع", from: "من أين تسافر؟", to: "إلى أين؟", near: "أقرب مطار", popFrom: "مدن مغادرة شائعة", popTo: "وجهات شائعة", none: "لم يُعثر على مطار. جرّب اسم المدينة أو الرمز المكوّن من 3 أحرف.",
      load: "جارٍ تحميل المطارات…", all: "كل المطارات", dep: "الذهاب", ret: "العودة", pick: "اختر", reset: "إعادة ضبط", ok: "موافق", clear: "مسح",
      note: "أدنى سعر ذهاب وعودة شوهد لمغادرة في ذلك اليوم، للشخص الواحد. قد يتغير.", noteNo: "اختر المغادرة والوصول لرؤية الأسعار حسب اليوم.", dates: "اختر التواريخ" }
  };
  var T = function () { return TXT[lang()] || TXT.en; };
  var LOC = function () { return { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", it: "it-IT", de: "de-DE", ar: "ar-u-nu-latn", nl: "nl-NL" }[lang()] || "en-GB"; };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var norm = function (s) { return String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9 ]+/g, " ").trim(); };
  var pad = function (n) { return String(n).padStart(2, "0"); };
  var isoOf = function (d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); };
  var parse = function (s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); };
  var fire = function (el, types) { types.forEach(function (t) { el.dispatchEvent(new Event(t, { bubbles: true })); }); };
  var petit = function () { return matchMedia("(max-width: 700px)").matches; };

  // ---------- Styles (dans les couleurs du site : variables de thème de l'accueil)
  var st = document.createElement("style");
  st.textContent =
    ".rp{position:fixed;inset:0;z-index:1000;background:var(--bg,#fff);color:var(--ink,#0f172a);display:flex;flex-direction:column;font-family:var(--f-body,system-ui)}" +
    ".rp[hidden]{display:none}.rp-top{display:flex;align-items:center;gap:8px;padding:10px 12px;border-bottom:1px solid var(--line,#e2e8f0);padding-top:calc(10px + env(safe-area-inset-top,0px))}" +
    ".rp-back,.rp-x{appearance:none;border:0;background:none;color:inherit;width:44px;height:44px;border-radius:50%;font-size:24px;line-height:1;cursor:pointer;flex:none}.rp-back:hover,.rp-x:hover{background:var(--soft,#f1f5f9)}" +
    "[dir=rtl] .rp-back{transform:scaleX(-1)}" +
    ".rp .rp-in,.rp .rp-in:focus{border:0;outline:0;box-shadow:none}.rp-in{flex:1;min-width:0;background:none;color:inherit;font:600 19px/1.3 var(--f-body,system-ui);padding:10px 4px}" +
    ".rp-list{flex:1;overflow:auto;-webkit-overflow-scrolling:touch;padding:6px 8px calc(24px + env(safe-area-inset-bottom,0px))}" +
    ".rp-h{margin:14px 10px 4px;font:700 12px/1.2 var(--f-body,system-ui);letter-spacing:.06em;text-transform:uppercase;color:var(--muted,#64748b)}" +
    ".rp-row{display:flex;align-items:center;gap:12px;width:100%;text-align:start;appearance:none;border:0;background:none;color:inherit;padding:11px 10px;border-radius:12px;cursor:pointer;font:inherit}" +
    ".rp-row:hover,.rp-row:focus-visible{background:var(--soft,#f1f5f9)}.rp-row .i{flex:none;width:28px;text-align:center;font-size:18px}.rp-row .m{flex:1;min-width:0}.rp-row b{display:block;font-weight:700;font-size:16px}" +
    ".rp-row small{display:block;color:var(--muted,#64748b);font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.rp-row .c{flex:none;font:700 12px/1 var(--f-mono,monospace);color:var(--muted,#64748b);border:1px solid var(--line,#e2e8f0);border-radius:6px;padding:4px 6px}" +
    ".rp-row.sub{padding-inline-start:34px}.rp-row.sub b{font-weight:600;font-size:15px}.rp-empty{padding:18px 12px;color:var(--muted,#64748b)}" +
    ".rp-tabs{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:8px}.rp-tabs.one{grid-template-columns:1fr}.rp-tab{appearance:none;border:2px solid var(--line,#e2e8f0);background:var(--surface,#fff);color:inherit;border-radius:12px;padding:7px 12px;text-align:start;cursor:pointer;font:inherit}" +
    ".rp-tab small{display:block;font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted,#64748b)}.rp-tab b{display:block;font-size:15px;white-space:nowrap}.rp-tab[aria-pressed=true]{border-color:var(--teal-d,#0b8577)}" +
    ".rp-week{display:grid;grid-template-columns:repeat(7,1fr);padding:8px 10px 6px;border-bottom:1px solid var(--line,#e2e8f0);font:700 12px/1 var(--f-body,system-ui);color:var(--muted,#64748b);text-align:center}" +
    ".rp-cal{flex:1;overflow:auto;-webkit-overflow-scrolling:touch;padding:0 10px 10px}.rp-cal h3{margin:18px 0 8px;text-align:center;font:700 17px/1.2 var(--f-display,var(--f-body,system-ui));text-transform:capitalize}" +
    ".rp-grid{display:grid;grid-template-columns:repeat(7,1fr);row-gap:4px}.rp-d{appearance:none;border:0;background:none;color:inherit;height:52px;border-radius:999px;cursor:pointer;font:inherit;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:0}" +
    ".rp-d b{font-weight:600;font-size:15px;line-height:1}.rp-d small{font-size:10px;line-height:1;color:var(--muted,#64748b);min-height:10px}.rp-d.cheap small{color:#0f7a4a;font-weight:700}.rp-d:disabled{opacity:.3;cursor:default}" +
    ".rp-d.in{background:color-mix(in srgb,var(--teal,#12b3a0) 16%,transparent);border-radius:0}.rp-d.a,.rp-d.b{background:var(--teal-fond,#0b8577);color:var(--teal-ink,#fff)}.rp-d.a small,.rp-d.b small{color:inherit}" +
    ".rp-d.a.has-b{border-start-end-radius:0;border-end-end-radius:0}.rp-d.b{border-start-start-radius:0;border-end-start-radius:0}.rp-d.a.b{border-radius:999px}" +
    ".rp-foot{display:flex;align-items:center;gap:10px;padding:10px 14px calc(10px + env(safe-area-inset-bottom,0px));border-top:1px solid var(--line,#e2e8f0)}.rp-foot p{flex:1;margin:0;font-size:11.5px;line-height:1.35;color:var(--muted,#64748b)}" +
    ".rp-reset{appearance:none;border:0;background:none;color:var(--teal-d,#0b8577);font:700 14px/1 var(--f-body,system-ui);padding:12px 8px;cursor:pointer}.rp-ok{appearance:none;border:0;border-radius:999px;background:var(--teal-fond,#0b8577);color:var(--teal-ink,#fff);font:700 15px/1 var(--f-body,system-ui);padding:14px 24px;cursor:pointer}" +
    ".rp-date-btn{position:absolute;inset:0;z-index:2;appearance:none;border:0;background:transparent;cursor:pointer;border-radius:12px}.rp-date-btn:focus-visible{outline:2px solid var(--focus,#12b3a0);outline-offset:2px}" +
    "@media (min-width:701px){.rp{inset:auto;top:50%;left:50%;transform:translate(-50%,-50%);width:440px;max-width:94vw;height:min(680px,92vh);border-radius:20px;box-shadow:0 30px 80px -20px rgb(0 0 0 / .5);overflow:hidden}.rp-voile{position:fixed;inset:0;z-index:999;background:rgb(3 18 28 / .45)}}" +
    "@media (max-width:700px){.rp-voile{display:none}}.rp-voile[hidden]{display:none}";
  document.head.appendChild(st);

  // ---------- Fenêtre commune
  var box = document.createElement("div"); box.className = "rp"; box.hidden = true; box.setAttribute("role", "dialog"); box.setAttribute("aria-modal", "true");
  var voile = document.createElement("div"); voile.className = "rp-voile"; voile.hidden = true;
  document.body.appendChild(voile); document.body.appendChild(box);
  var ouvert = false, pousse = false, retour = null, gardeScroll = "";
  function ouvrir(html, label, focusBack) {
    box.innerHTML = html; box.setAttribute("aria-label", label); box.hidden = false; voile.hidden = false; ouvert = true; retour = focusBack || null;
    gardeScroll = document.documentElement.style.overflow; document.documentElement.style.overflow = "hidden";
    try { history.pushState({ rp: 1 }, ""); pousse = true; } catch (e) { pousse = false; } // le bouton « retour » du téléphone ferme la fenêtre
  }
  function fermer(depuisRetour) {
    if (!ouvert) return;
    ouvert = false; box.hidden = true; voile.hidden = true; box.innerHTML = ""; document.documentElement.style.overflow = gardeScroll;
    if (pousse && !depuisRetour) { pousse = false; try { history.back(); } catch (e) {} }
    pousse = false;
  }
  addEventListener("popstate", function () { if (ouvert) fermer(true); });
  voile.addEventListener("click", function () { fermer(); });
  document.addEventListener("keydown", function (e) { if (ouvert && e.key === "Escape") fermer(); });

  // ---------- 1. Départ et arrivée : villes et aéroports
  var DB = null, dbP = null;
  function base() {
    if (!dbP) {
      window.ESCALE_AIRPORTS = window.ESCALE_AIRPORTS || fetch("/data/airports-lite.json").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
      dbP = window.ESCALE_AIRPORTS.then(function (l) { DB = Array.isArray(l) ? l : []; return DB; });
    }
    return dbP;
  }
  var pays = function (cc) { try { return new Intl.DisplayNames([lang()], { type: "region" }).of(cc) || cc; } catch (e) { return cc; } };
  var drapeau = function (cc) { return cc && cc.length === 2 ? String.fromCodePoint.apply(null, cc.toUpperCase().split("").map(function (c) { return 127397 + c.charCodeAt(0); })) : "✈"; };
  var etiquette = function (a) { return a[1] + " (" + a[0] + ")"; };
  function chercher(txt) { // groupes [ville, pays, [aéroports]] du plus pertinent au moins pertinent
    var t = norm(txt), up = txt.trim().toUpperCase(), notes = [];
    if (!t || !DB) return [];
    DB.forEach(function (a) {
      var v = norm(a[1]), fr = a[7] && a[7] !== a[1] ? norm(a[7]) : "", n = norm(a[2]), s = 0;
      if (a[0] === up) s = 1000; else if (v === t || fr === t) s = 600; else if (v.indexOf(t) === 0 || (fr && fr.indexOf(t) === 0)) s = 400;
      else if (n.indexOf(t) === 0) s = 250; else if (t.length >= 3 && (v.indexOf(" " + t) >= 0 || n.indexOf(" " + t) >= 0)) s = 120; // début de mot seulement
      else if (t.length >= 3 && norm(pays(a[3])).indexOf(t) === 0) s = 80;
      if (s) notes.push([s + (a[4] ? 50 : 0), a]);
    });
    notes.sort(function (x, y) { return y[0] - x[0] || x[1][1].localeCompare(y[1][1]); });
    var groupes = [], vus = {};
    notes.slice(0, 60).forEach(function (x) {
      var a = x[1], k = a[1] + "|" + a[3];
      if (!vus[k]) { if (groupes.length >= 7) return; vus[k] = { ville: a[1], cc: a[3], air: [] }; groupes.push(vus[k]); }
      if (vus[k].air.length < 5) vus[k].air.push(a);
    });
    // tous les aéroports d'une ville trouvée, même ceux dont le nom ne contient pas le texte tapé (Milan : Malpensa, Linate, Bergame)
    groupes.forEach(function (g) { DB.forEach(function (a) { if (a[1] === g.ville && a[3] === g.cc && g.air.indexOf(a) < 0 && g.air.length < 5) g.air.push(a); });
      g.air.sort(function (a, b) { return (b[4] || 0) - (a[4] || 0); }); });
    return groupes;
  }
  var nomAero = function (a) { return a[2] || a[1]; };
  function rendreGroupes(gs) {
    return gs.map(function (g) {
      if (g.air.length === 1) { var a = g.air[0];
        return '<button type="button" class="rp-row" data-code="' + a[0] + '"><span class="i" aria-hidden="true">' + drapeau(g.cc) + '</span><span class="m"><b>' + esc(g.ville) + "</b><small>" + esc(nomAero(a)) + " · " + esc(pays(g.cc)) + '</small></span><span class="c">' + a[0] + "</span></button>"; }
      return '<button type="button" class="rp-row" data-code="' + g.air[0][0] + '"><span class="i" aria-hidden="true">' + drapeau(g.cc) + '</span><span class="m"><b>' + esc(g.ville) + "</b><small>" + esc(pays(g.cc)) + "</small></span></button>" +
        g.air.map(function (a) { return '<button type="button" class="rp-row sub" data-code="' + a[0] + '"><span class="i" aria-hidden="true">✈</span><span class="m"><b>' + esc(nomAero(a)) + '</b></span><span class="c">' + a[0] + "</span></button>"; }).join("");
    }).join("");
  }
  var POP = { from: ["CDG", "LYS", "MRS", "BRU", "GVA", "MXP", "FCO", "LHR", "MAD", "YUL"], to: ["DSS", "ABJ", "CMN", "ALG", "TUN", "CKY", "DLA", "RAK", "LOS", "ACC", "IST", "DXB"] };
  function lieu(champ, quoi) {
    var t = T();
    ouvrir('<div class="rp-top"><button type="button" class="rp-back" aria-label="' + esc(t.back) + '">←</button>' +
      '<input class="rp-in" type="text" inputmode="search" enterkeyhint="search" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" placeholder="' + esc(quoi === "from" ? t.from : t.to) + '" aria-label="' + esc(quoi === "from" ? t.from : t.to) + '">' +
      '<button type="button" class="rp-x" aria-label="' + esc(t.clear) + '">×</button></div><div class="rp-list" role="listbox"></div>', quoi === "from" ? t.from : t.to);
    var inp = box.querySelector(".rp-in"), liste = box.querySelector(".rp-list");
    champ.dispatchEvent(new Event("focus")); // app.js charge alors les noms officiels des aéroports dans la liste partagée
    var peindre = function () {
      var v = inp.value.trim();
      if (!DB) { liste.innerHTML = '<p class="rp-empty">' + esc(t.load) + "</p>"; return; }
      if (!v) {
        var par = {}; DB.forEach(function (a) { par[a[0]] = a; });
        liste.innerHTML = (quoi === "from" && $("f-near") ? '<button type="button" class="rp-row" data-near="1"><span class="i" aria-hidden="true">📍</span><span class="m"><b>' + esc(t.near) + "</b></span></button>" : "") +
          '<p class="rp-h">' + esc(quoi === "from" ? t.popFrom : t.popTo) + "</p>" +
          POP[quoi].filter(function (c) { return par[c]; }).map(function (c) { var a = par[c];
            return '<button type="button" class="rp-row" data-code="' + c + '"><span class="i" aria-hidden="true">' + drapeau(a[3]) + '</span><span class="m"><b>' + esc(a[1]) + "</b><small>" + esc(pays(a[3])) + '</small></span><span class="c">' + c + "</span></button>"; }).join("");
        return;
      }
      var gs = chercher(v);
      liste.innerHTML = gs.length ? rendreGroupes(gs) : '<p class="rp-empty">' + esc(t.none) + "</p>";
      liste.scrollTop = 0;
    };
    inp.addEventListener("input", peindre);
    box.querySelector(".rp-back").addEventListener("click", function () { fermer(); });
    box.querySelector(".rp-x").addEventListener("click", function () { inp.value = ""; peindre(); inp.focus(); });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { var b = liste.querySelector(".rp-row[data-code]"); if (b && inp.value.trim()) { e.preventDefault(); b.click(); } } });
    liste.addEventListener("click", function (e) {
      var b = e.target.closest(".rp-row"); if (!b) return;
      if (b.dataset.near) { fermer(); setTimeout(function () { $("f-near").click(); }, 60); return; }
      var a = null; DB.forEach(function (x) { if (x[0] === b.dataset.code) a = x; }); if (!a) return;
      champ.value = etiquette(a); fermer(); fire(champ, ["input", "change"]);
    });
    peindre(); base().then(peindre); setTimeout(peindre, 900); // 900 ms : les noms officiels sont arrivés entre-temps
    setTimeout(function () { inp.focus(); }, 30);
  }
  [[fFrom, "from"], [fTo, "to"]].forEach(function (x) {
    x[0].addEventListener("focus", function (e) { if (!petit() || ouvert || !e.isTrusted) return; x[0].blur(); lieu(x[0], x[1]); });
  });

  // ---------- 2. Dates : calendrier de 12 mois avec le prix sous chaque jour
  var prixMois = {};
  var codeDe = function (el) { var m = /\(([A-Za-z]{3})\)\s*$/.exec(el.value || "") || /^([A-Za-z]{3})$/.exec((el.value || "").trim()); return m ? m[1].toUpperCase() : ""; };
  var argent = function (n) { if (window.ESCALE_MONEY) { try { return String(window.ESCALE_MONEY(n, "EUR")).replace(/\s/g, " "); } catch (e) {} } return Math.round(n) + " €"; };
  function dates(quoi) {
    var t = T(), loc = LOC(), today = isoOf(new Date());
    var aller = $("trip-ow") && $("trip-ow").checked, dep = fDep.value >= today ? fDep.value : "", ret = !aller && fRet.value > dep ? fRet.value : "", actif = aller ? "dep" : quoi;
    var from = codeDe(fFrom), to = codeDe(fTo);
    var jour = function (s) { return s ? parse(s).toLocaleDateString(loc, { weekday: "short", day: "numeric", month: "short" }) : t.pick; };
    var sem = []; for (var i = 0; i < 7; i++) sem.push("<span>" + esc(new Date(2024, 0, 1 + i).toLocaleDateString(loc, { weekday: "narrow" })) + "</span>");
    var mois = [], now = new Date();
    for (var k = 0; k < 12; k++) { var d = new Date(now.getFullYear(), now.getMonth() + k, 1); mois.push(d.getFullYear() + "-" + pad(d.getMonth() + 1)); }
    var corps = mois.map(function (m) {
      var p = m.split("-"), y = +p[0], mo = +p[1] - 1, n = new Date(y, mo + 1, 0).getDate(), off = (new Date(y, mo, 1).getDay() + 6) % 7, c = "";
      for (var e = 0; e < off; e++) c += "<span></span>";
      for (var j = 1; j <= n; j++) { var iso = m + "-" + pad(j); c += '<button type="button" class="rp-d" data-d="' + iso + '"' + (iso < today ? " disabled" : "") + "><b>" + j + "</b><small></small></button>"; }
      return '<section data-m="' + m + '"><h3>' + esc(new Date(y, mo, 1).toLocaleDateString(loc, y === now.getFullYear() ? { month: "long" } : { month: "long", year: "numeric" })) + '</h3><div class="rp-grid">' + c + "</div></section>";
    }).join("");
    ouvrir('<div class="rp-top"><button type="button" class="rp-back" aria-label="' + esc(t.back) + '">←</button><div class="rp-tabs' + (aller ? " one" : "") + '">' +
      '<button type="button" class="rp-tab" data-k="dep"><small>' + esc(t.dep) + "</small><b></b></button>" + (aller ? "" : '<button type="button" class="rp-tab" data-k="ret"><small>' + esc(t.ret) + "</small><b></b></button>") + "</div></div>" +
      '<div class="rp-week" aria-hidden="true">' + sem.join("") + '</div><div class="rp-cal">' + corps + "</div>" +
      '<div class="rp-foot"><p>' + esc(from && to ? t.note : t.noteNo) + '</p><button type="button" class="rp-reset">' + esc(t.reset) + '</button><button type="button" class="rp-ok">' + esc(t.ok) + "</button></div>", t.dates);
    var cal = box.querySelector(".rp-cal");
    var marquer = function () {
      [].forEach.call(box.querySelectorAll(".rp-tab"), function (b) { b.setAttribute("aria-pressed", String(b.dataset.k === actif)); b.querySelector("b").textContent = jour(b.dataset.k === "dep" ? dep : ret); });
      [].forEach.call(cal.querySelectorAll(".rp-d"), function (b) { var d = b.dataset.d;
        b.classList.toggle("a", d === dep); b.classList.toggle("b", !!ret && d === ret); b.classList.toggle("has-b", d === dep && !!ret && ret !== dep); b.classList.toggle("in", !!dep && !!ret && d > dep && d < ret); });
    };
    cal.addEventListener("click", function (e) {
      var b = e.target.closest(".rp-d"); if (!b || b.disabled) return; var d = b.dataset.d;
      if (aller) { dep = d; }
      else if (actif === "dep" || !dep || d < dep) { dep = d; if (ret && ret <= dep) ret = ""; actif = "ret"; }
      else { ret = d; }
      marquer();
    });
    [].forEach.call(box.querySelectorAll(".rp-tab"), function (b) { b.addEventListener("click", function () { actif = b.dataset.k; marquer(); }); });
    box.querySelector(".rp-back").addEventListener("click", function () { fermer(); });
    box.querySelector(".rp-reset").addEventListener("click", function () { dep = ""; ret = ""; actif = "dep"; marquer(); });
    box.querySelector(".rp-ok").addEventListener("click", function () {
      if (dep) { fDep.value = dep; fire(fDep, ["input", "change"]); if (!aller && ret) { fRet.value = ret; fire(fRet, ["input", "change"]); } }
      fermer();
    });
    // Prix : un appel par mois, seulement pour les mois qui passent à l'écran (réponses gardées 3 h par le serveur)
    if (from && to && from !== to && "IntersectionObserver" in window) {
      var peindreMois = function (sec, data) {
        if (!data || !data.available || data.currency !== "EUR") return;
        var vals = []; Object.keys(data.days || {}).forEach(function (d) { if (d >= today) vals.push(data.days[d].price); });
        if (!vals.length) return; vals.sort(function (a, b) { return a - b; });
        var seuil = vals[Math.max(0, Math.ceil(vals.length * 0.25) - 1)];
        [].forEach.call(sec.querySelectorAll(".rp-d"), function (b) { var x = data.days[b.dataset.d]; if (!x || b.disabled) return;
          b.querySelector("small").textContent = argent(x.price); b.classList.toggle("cheap", x.price <= seuil); });
      };
      var io = new IntersectionObserver(function (es) { es.forEach(function (en) {
        if (!en.isIntersecting) return; io.unobserve(en.target);
        var m = en.target.dataset.m, cle = from + "-" + to + "-" + m;
        if (!prixMois[cle]) prixMois[cle] = fetch("/api/calendar?from=" + from + "&to=" + to + "&month=" + m).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
        prixMois[cle].then(function (data) { if (ouvert && en.target.isConnected) peindreMois(en.target, data); });
      }); }, { root: cal, rootMargin: "200px 0px" });
      [].forEach.call(cal.querySelectorAll("section"), function (s) { io.observe(s); });
    }
    marquer();
    var cible = cal.querySelector('section[data-m="' + ((actif === "ret" && ret ? ret : dep) || today).slice(0, 7) + '"]');
    if (cible) cal.scrollTop = Math.max(0, cible.offsetTop - cal.offsetTop - 4);
  }
  [[fDep, "dep"], [fRet, "ret"]].forEach(function (x) {
    var wrap = x[0].parentElement; if (!wrap) return;
    if (getComputedStyle(wrap).position === "static") wrap.style.position = "relative";
    var b = document.createElement("button"); b.type = "button"; b.className = "rp-date-btn";
    var lab = wrap.querySelector("label"); b.setAttribute("aria-label", (lab ? lab.textContent + " : " : "") + T().dates);
    b.addEventListener("click", function () { dates(x[1]); });
    wrap.appendChild(b); x[0].tabIndex = -1; // le bouton remplace le sélecteur de date du téléphone ; le champ garde sa valeur
  });
})();
