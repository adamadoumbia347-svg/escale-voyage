// Accueil : « Vers l'Afrique depuis <ville du visiteur> », une ligne de trajets sous le moteur de recherche, avec les dates et le prix
// aller-retour le plus bas repéré (mois prochain et suivant). Une seule demande : /api/ruban?from=XXX (gardée 12 h par Cloudflare).
// Rien n'est inventé : un pays sans prix repéré n'apparaît pas ; sans aucun prix, le bloc reste caché.
(function () {
  "use strict";
  var sec = document.getElementById("af"), row = document.getElementById("af-row"), city = document.getElementById("af-city");
  if (!sec || !row) return;
  var lang = function () { return (document.documentElement.lang || "fr").slice(0, 2); };
  var LOC = { fr: "fr-FR", en: "en-GB", it: "it-IT", de: "de-DE", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn" };
  var FROM = { fr: "dès ", en: "from ", it: "da ", de: "ab ", es: "desde ", pt: "desde ", ar: "من " };
  // pays (clé de /api/ruban) → drapeau ; code de ville ou d'aéroport → [aéroport du moteur, nom fr, nom en]
  var PAYS = { ci: "🇨🇮", sn: "🇸🇳", cm: "🇨🇲", gh: "🇬🇭", ma: "🇲🇦", tn: "🇹🇳", eg: "🇪🇬", ke: "🇰🇪", tz: "🇹🇿", za: "🇿🇦", gn: "🇬🇳", bj: "🇧🇯", tg: "🇹🇬", ga: "🇬🇦", ng: "🇳🇬" };
  var V = { ABJ: ["ABJ", "Abidjan"], DSS: ["DSS", "Dakar"], DKR: ["DSS", "Dakar"], DLA: ["DLA", "Douala"], YAO: ["NSI", "Yaoundé"], NSI: ["NSI", "Yaoundé"], ACC: ["ACC", "Accra"],
    RAK: ["RAK", "Marrakech"], CAS: ["CMN", "Casablanca"], CMN: ["CMN", "Casablanca"], TUN: ["TUN", "Tunis"], CAI: ["CAI", "Le Caire", "Cairo"], NBO: ["NBO", "Nairobi"],
    ZNZ: ["ZNZ", "Zanzibar"], DAR: ["DAR", "Dar es Salaam"], CPT: ["CPT", "Le Cap", "Cape Town"], JNB: ["JNB", "Johannesburg"], CKY: ["CKY", "Conakry"], COO: ["COO", "Cotonou"],
    LFW: ["LFW", "Lomé"], LBV: ["LBV", "Libreville"], LOS: ["LOS", "Lagos"], ABV: ["ABV", "Abuja"] };
  var VILLE = { CDG: "PAR", ORY: "PAR", BVA: "PAR", FCO: "ROM", CIA: "ROM", MXP: "MIL", LIN: "MIL", BGY: "MIL", LHR: "LON", LGW: "LON", STN: "LON", LTN: "LON" };
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var money = function (n) { if (window.ESCALE_MONEY) return window.ESCALE_MONEY(n, "EUR"); return Math.round(n) + " €"; };
  var jour = function (s) { try { return new Date(s + "T12:00:00").toLocaleDateString(LOC[lang()] || "en-GB", { day: "numeric", month: "short" }); } catch (e) { return s; } };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var cur = null, token = 0, last = null;
  var paint = function (j) {
    var from = cur.code, name = cur.name || from, fr = lang() === "fr";
    var list = Object.keys((j && j.prix) || {}).filter(function (cc) { return PAYS[cc]; }).map(function (cc) {
      var x = j.prix[cc], v = V[x.v] || V[x.to]; if (!v || !x.price || !x.dep) return null;
      return { f: PAYS[cc], to: v[0], n: fr ? v[1] : (v[2] || v[1]), p: x.price, dep: x.dep, ret: x.ret };
    }).filter(Boolean).sort(function (a, b) { return a.p - b.p; }).slice(0, 10);
    if (!list.length) { sec.hidden = true; return; }
    if (city) city.textContent = name;
    row.innerHTML = list.map(function (x) {
      return '<div class="af-c"><a href="/recherche/?flightSearch=' + from + ddmm(x.dep) + x.to + (x.ret ? ddmm(x.ret) : "") + '1"><b>' + esc(name) + " → " + esc(x.n) + " " + x.f + "</b><small>" +
        esc(jour(x.dep)) + (x.ret ? " → " + esc(jour(x.ret)) : "") + "</small><em>" + esc((FROM[lang()] || "from ") + money(x.p)) + "</em></a>" +
        (alertes ? '<button type="button" class="af-bell" data-to="' + x.to + '" data-n="' + esc(x.n) + '" data-p="' + x.p + '" aria-label="' + esc(tx().bell) + " " + esc(name) + " → " + esc(x.n) + '">🔔</button>' : "") + "</div>";
    }).join("");
    row.scrollLeft = 0; sec.hidden = false;
    ailleurs(j);
  };

  // ---------- Cloche : alerte prix pour un trajet, sans passer par la recherche (e-mail + budget, /api/alert) ----------
  var TX = {
    fr: { bell: "Alerte prix", h: "🔔 Alerte prix : {a} → {b}", l: "Préviens-moi par e-mail si l’aller-retour passe sous", mail: "Ton e-mail", ok: "Créer l’alerte", c: "J’accepte de recevoir des e-mails pour cette alerte (désinscription en un clic).", bad: "Vérifie l’e-mail, le budget et la case à cocher.", done: "C’est presque fini : confirme ton alerte avec le lien envoyé à {e}.", ko: "L’alerte n’a pas pu être créée. Réessaie plus tard.", x: "Fermer", less: "{b} : {s} de moins depuis {c}", inst: "au lieu de" },
    en: { bell: "Price alert", h: "🔔 Price alert: {a} → {b}", l: "Email me when the round trip drops below", mail: "Your email", ok: "Create alert", c: "I agree to receive emails for this alert (one-click unsubscribe).", bad: "Check the email, the budget and the box.", done: "Almost done: confirm your alert with the link sent to {e}.", ko: "The alert could not be created. Please try again later.", x: "Close", less: "{b}: {s} less from {c}", inst: "instead of" },
    it: { bell: "Avviso prezzo", h: "🔔 Avviso prezzo: {a} → {b}", l: "Avvisami via e-mail se l’andata e ritorno scende sotto", mail: "La tua e-mail", ok: "Crea l’avviso", c: "Accetto di ricevere e-mail per questo avviso (disiscrizione con un clic).", bad: "Controlla l’e-mail, il budget e la casella.", done: "Ci siamo quasi: conferma l’avviso con il link inviato a {e}.", ko: "Non è stato possibile creare l’avviso. Riprova più tardi.", x: "Chiudi", less: "{b}: {s} in meno da {c}", inst: "invece di" },
    es: { bell: "Alerta de precio", h: "🔔 Alerta de precio: {a} → {b}", l: "Avísame por correo si la ida y vuelta baja de", mail: "Tu correo", ok: "Crear alerta", c: "Acepto recibir correos para esta alerta (baja con un clic).", bad: "Revisa el correo, el presupuesto y la casilla.", done: "Ya casi está: confirma tu alerta con el enlace enviado a {e}.", ko: "No se pudo crear la alerta. Inténtalo más tarde.", x: "Cerrar", less: "{b}: {s} menos desde {c}", inst: "en lugar de" },
    pt: { bell: "Alerta de preço", h: "🔔 Alerta de preço: {a} → {b}", l: "Avise-me por e-mail se a ida e volta descer abaixo de", mail: "O seu e-mail", ok: "Criar alerta", c: "Aceito receber e-mails para este alerta (cancelamento com um clique).", bad: "Verifique o e-mail, o orçamento e a caixa.", done: "Quase lá: confirme o alerta com o link enviado para {e}.", ko: "Não foi possível criar o alerta. Tente mais tarde.", x: "Fechar", less: "{b}: {s} a menos a partir de {c}", inst: "em vez de" },
    de: { bell: "Preisalarm", h: "🔔 Preisalarm: {a} → {b}", l: "Schreib mir, wenn Hin- und Rückflug günstiger wird als", mail: "Deine E-Mail", ok: "Alarm erstellen", c: "Ich bin einverstanden, E-Mails zu diesem Alarm zu erhalten (Abmeldung mit einem Klick).", bad: "Prüfe E-Mail, Budget und das Kästchen.", done: "Fast fertig: Bestätige den Alarm über den Link an {e}.", ko: "Der Alarm konnte nicht erstellt werden. Versuch es später erneut.", x: "Schließen", less: "{b}: {s} günstiger ab {c}", inst: "statt" }
  };
  var tx = function () { return TX[lang()] || TX.en; };
  var alertes = false;
  fetch("/api/alert?action=status").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (j) {
    alertes = !!(j && j.enabled); if (alertes && cur && last) paint(last);
  });
  var fermer = function () { var d = document.getElementById("af-sheet"); if (d) d.remove(); };
  row.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest(".af-bell"); if (!b || !cur) return;
    ev.preventDefault(); fermer();
    var T = tx(), to = b.getAttribute("data-to"), p = +b.getAttribute("data-p"), max = Math.max(10, Math.floor((p * 0.9) / 10) * 10);
    var d = document.createElement("div"); d.id = "af-sheet"; d.className = "af-sheet"; d.setAttribute("role", "dialog"); d.setAttribute("aria-modal", "true");
    d.innerHTML = '<form class="af-form" novalidate><button type="button" class="af-x" aria-label="' + esc(T.x) + '">×</button><p class="af-t">' +
      esc(T.h.replace("{a}", cur.name || cur.code).replace("{b}", b.getAttribute("data-n"))) + '</p><label class="af-max"><span>' + esc(T.l) + '</span><span class="af-in"><input type="number" name="max" min="1" inputmode="numeric" required value="' + max + '"> €</span></label>' +
      '<input type="email" name="email" required autocomplete="email" placeholder="' + esc(T.mail) + '" aria-label="' + esc(T.mail) + '">' +
      '<label class="af-ck"><input type="checkbox" name="consent" required><span>' + esc(T.c) + '</span></label><button class="btn" type="submit">' + esc(T.ok) + '</button><p class="af-msg" role="status"></p></form>';
    document.body.appendChild(d);
    var f = d.querySelector("form"), msg = d.querySelector(".af-msg");
    d.addEventListener("click", function (e) { if (e.target === d || (e.target.closest && e.target.closest(".af-x"))) fermer(); });
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var email = f.email.value.trim(), m = Number(f.max.value);
      if (!/^\S+@\S+\.\S+$/.test(email) || !(m > 0) || !f.consent.checked) { msg.textContent = T.bad; return; }
      var bt = f.querySelector("button[type=submit]"); bt.disabled = true;
      fetch("/api/alert", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: email, max: m, from: cur.code, to: to, lang: lang(), currency: "EUR", consent: true }) })
        .then(function (r) { return r.ok; }).catch(function () { return false; }).then(function (ok) {
          if (ok) { msg.textContent = T.done.replace("{e}", email); bt.hidden = true; if (window.ESCALE_CLIC) try { window.ESCALE_CLIC("alerte-accueil"); } catch (x) {} }
          else { msg.textContent = T.ko; bt.disabled = false; }
        });
    });
    try { f.email.focus(); } catch (e) {}
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") fermer(); });

  // ---------- « Moins cher depuis une autre ville » : même relevé (/api/ruban) pour les grandes villes proches du visiteur ----------
  // Une ligne seulement, et seulement si l'écart est réel : au moins 12 % de moins et au moins 60 € (ou 0,40 € par km de distance
  // entre les deux villes, pour que l'économie vaille le déplacement), pour la même ville d'arrivée.
  var HUBS = [["PAR", "CDG"], ["LYS", "LYS"], ["MRS", "MRS"], ["NCE", "NCE"], ["TLS", "TLS"], ["BOD", "BOD"], ["NTE", "NTE"], ["BRU", "BRU"], ["LUX", "LUX"], ["GVA", "GVA"], ["ZRH", "ZRH"],
    ["MIL", "MXP"], ["ROM", "FCO"], ["VCE", "VCE"], ["BLQ", "BLQ"], ["NAP", "NAP"], ["TRN", "TRN"], ["MAD", "MAD"], ["BCN", "BCN"], ["LIS", "LIS"], ["OPO", "OPO"],
    ["FRA", "FRA"], ["MUC", "MUC"], ["DUS", "DUS"], ["BER", "BER"], ["AMS", "AMS"], ["LON", "LHR"]];
  var km = function (a, b) { var R = Math.PI / 180, x = (b[1] - a[1]) * R * Math.cos((a[0] + b[0]) * R / 2), y = (b[0] - a[0]) * R; return Math.sqrt(x * x + y * y) * 6371; };
  var tip = document.getElementById("af-tip"), tok2 = 0;
  var ailleurs = function (j) {
    if (!tip) return; tip.hidden = true;
    var t = ++tok2, mine = (j && j.prix) || {}, me = VILLE[cur.code] || cur.code, name = cur.name || cur.code;
    window.ESCALE_AIRPORTS = window.ESCALE_AIRPORTS || fetch("/data/airports-lite.json").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
    window.ESCALE_AIRPORTS.then(function (db) {
      if (!db || t !== tok2) return;
      var by = {}; db.forEach(function (a) { by[a[0]] = a; });
      var here = by[cur.code]; if (!here || here[5] == null) return;
      var near = HUBS.filter(function (h) { return h[0] !== me && by[h[1]] && (h[0] === "LON") === (here[3] === "GB"); })
        .map(function (h) { return { q: h[0], a: by[h[1]], d: km([here[5], here[6]], [by[h[1]][5], by[h[1]][6]]) }; })
        .filter(function (h) { return h.d > 40 && h.d <= 400; }).sort(function (a, b) { return a.d - b.d; }).slice(0, 3);
      if (!near.length) return;
      Promise.all(near.map(function (h) { return fetch("/api/ruban?from=" + h.q).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); })).then(function (res) {
        if (t !== tok2) return;
        var best = null;
        res.forEach(function (r, i) {
          Object.keys((r && r.prix) || {}).forEach(function (cc) {
            var o = r.prix[cc], m = mine[cc]; if (!PAYS[cc] || !m || !o || !o.price || !m.price || !o.dep) return;
            var v = V[o.v] || V[o.to], vm = V[m.v] || V[m.to]; if (!v || !vm || v[0] !== vm[0]) return;   // même ville d'arrivée des deux côtés
            var s = m.price - o.price; if (s < Math.max(60, near[i].d * 0.4) || s < m.price * 0.12) return;   // l'écart doit valoir le déplacement
            if (!best || s > best.s) best = { s: s, o: o, m: m, v: v, h: near[i] };
          });
        });
        if (!best) return;
        var T = tx(), fr = lang() === "fr", dest = fr ? best.v[1] : (best.v[2] || best.v[1]), alt = best.h.a[1];
        var href = fr ? "/match-des-aeroports/?to=" + best.v[0] : "/recherche/?flightSearch=" + best.h.a[0] + ddmm(best.o.dep) + best.v[0] + (best.o.ret ? ddmm(best.o.ret) : "") + "1";
        tip.innerHTML = '<a href="' + href + '">💡 <b>' + esc(T.less.replace("{b}", dest).replace("{s}", money(best.s)).replace("{c}", alt)) + "</b> <small>" + esc(money(best.o.price)) + " " + esc(T.inst) + " " + esc(money(best.m.price)) +
          " · " + esc(jour(best.o.dep)) + (best.o.ret ? " → " + esc(jour(best.o.ret)) : "") + "</small> →</a>";
        tip.hidden = false;
      });
    });
  };
  var load = function () {
    var t = ++token, q = VILLE[cur.code] || cur.code;
    fetch("/api/ruban?from=" + q).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }).then(function (j) {
      if (t !== token) return;
      last = j; paint(j);
    });
  };
  var set = function (d) { if (!d || !d.code) return; if (cur && cur.code === d.code) { if (last) paint(last); return; } cur = { code: d.code, name: d.name }; load(); };
  window.addEventListener("escale:from", function (e) { set(e.detail); });
  window.addEventListener("escale:lang", function () { if (cur && last) paint(last); });
  window.addEventListener("escale:cur", function () { if (cur && last) paint(last); });
  var start = function () {
    if (window.ESCALE_FROM) set(window.ESCALE_FROM);
    // Ville du visiteur inconnue au bout de 3 s : Paris
    setTimeout(function () { if (!cur) set({ code: "CDG", name: "Paris" }); }, 3000);
  };
  if (document.readyState === "complete") start(); else window.addEventListener("load", start);
})();
