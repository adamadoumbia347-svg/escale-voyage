/* Rubrique « Que visiter » (français, anglais, italien) : envies gardées dans le téléphone, recherche d'un pays ou d'un lieu,
   prix du vol depuis la ville du visiteur, budget du voyage, carte postale à partager, alerte prix depuis les envies, partage.
   Rien n'est envoyé sans geste du visiteur : les envies restent dans le navigateur ; l'alerte prix n'envoie que l'e-mail saisi.
   Ce fichier expose aussi window.VX (langue, villes de départ, prix) pour la carte, le jeu et le comparateur. */
(function () {
  "use strict";
  var lang = (document.documentElement.lang || "fr").slice(0, 2); if (!/^(fr|en|it)$/.test(lang)) lang = "fr";
  var T = {
    fr: { add: "Ajouter à mes envies", rm: "Retirer de mes envies", retirer: "Retirer", cherche: "Recherche du prix du moment…", aucun: "Pas de prix repéré depuis {v} pour l'instant : lancez la recherche pour voir les vols.",
      prix: "{a} → {b} : dès {p} aller-retour", dates: "({d1} → {d2})", note: "Prix repéré récemment, il peut changer.", n1: "{n} pays correspond", nx: "{n} pays correspondent", n0: "Aucun pays pour cette recherche pour l'instant.",
      tot: "Total : {t} · {pp} par personne", det: "Vols {a} + logement {b} + sur place {c}", pc_top: "PROCHAINE ESCALE", pc_share: "Partager", pc_dl: "Télécharger l'image", pc_x: "Fermer", pc_txt: "Ma prochaine escale : {n} ({p})",
      al_btn: "🔔 M'alerter si le vol pour {v} baisse", al_h: "Alerte prix : {v}", al_p: "Recevez un e-mail quand l'aller-retour passe sous votre budget. Gratuit, désinscription en un clic.", al_from: "Je pars de", al_email: "Votre e-mail",
      al_max: "Budget maximum (€)", al_consent: "J'accepte de recevoir des e-mails pour cette alerte. Mon adresse ne sert qu'à cela.", al_go: "Créer mon alerte", al_ok: "C'est noté : ouvrez l'e-mail envoyé à {e} pour confirmer l'alerte.",
      al_err: "Vérifiez la ville de départ, l'e-mail, le budget, et cochez la case.", al_fail: "L'alerte n'a pas pu être créée. Réessayez plus tard.", al_vu: "Prix repéré récemment : {p}.", choisir: "choisir une ville" },
    en: { add: "Add to my wishlist", rm: "Remove from my wishlist", retirer: "Remove", cherche: "Looking for the current price…", aucun: "No price spotted from {v} yet: run the search to see flights.",
      prix: "{a} → {b}: from {p} return", dates: "({d1} → {d2})", note: "Price spotted recently, it can change.", n1: "{n} country matches", nx: "{n} countries match", n0: "No country matches this search yet.",
      tot: "Total: {t} · {pp} per person", det: "Flights {a} + accommodation {b} + spending {c}", pc_top: "NEXT STOP", pc_share: "Share", pc_dl: "Download the image", pc_x: "Close", pc_txt: "My next stop: {n} ({p})",
      al_btn: "🔔 Alert me if flights to {v} get cheaper", al_h: "Price alert: {v}", al_p: "Get an email when the return fare drops below your budget. Free, one-click unsubscribe.", al_from: "I'm leaving from", al_email: "Your email",
      al_max: "Maximum budget (€)", al_consent: "I agree to receive emails for this alert. My address is used for nothing else.", al_go: "Create my alert", al_ok: "Done: open the email sent to {e} to confirm the alert.",
      al_err: "Check the departure city, the email, the budget, and tick the box.", al_fail: "The alert could not be created. Try again later.", al_vu: "Price spotted recently: {p}.", choisir: "choose a city" },
    it: { add: "Aggiungi ai miei desideri", rm: "Togli dai miei desideri", retirer: "Togli", cherche: "Cerco il prezzo del momento…", aucun: "Nessun prezzo rilevato da {v} per ora: avvia la ricerca per vedere i voli.",
      prix: "{a} → {b}: da {p} andata e ritorno", dates: "({d1} → {d2})", note: "Prezzo rilevato di recente, può cambiare.", n1: "{n} paese corrisponde", nx: "{n} paesi corrispondono", n0: "Nessun paese per questa ricerca, per ora.",
      tot: "Totale: {t} · {pp} a persona", det: "Voli {a} + alloggio {b} + sul posto {c}", pc_top: "PROSSIMO SCALO", pc_share: "Condividi", pc_dl: "Scarica l'immagine", pc_x: "Chiudi", pc_txt: "Il mio prossimo scalo: {n} ({p})",
      al_btn: "🔔 Avvisami se il volo per {v} scende", al_h: "Avviso prezzo: {v}", al_p: "Ricevi un'e-mail quando l'andata e ritorno scende sotto il tuo budget. Gratis, cancellazione in un clic.", al_from: "Parto da", al_email: "La tua e-mail",
      al_max: "Budget massimo (€)", al_consent: "Accetto di ricevere e-mail per questo avviso. Il mio indirizzo serve solo a questo.", al_go: "Crea il mio avviso", al_ok: "Fatto: apri l'e-mail inviata a {e} per confermare l'avviso.",
      al_err: "Controlla la città di partenza, l'e-mail, il budget e spunta la casella.", al_fail: "Non è stato possibile creare l'avviso. Riprova più tardi.", al_vu: "Prezzo rilevato di recente: {p}.", choisir: "scegli una città" }
  }[lang];
  var KEY = "escale.envies", $ = function (s, r) { return (r || document).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var fmt = function (s, o) { return s.replace(/\{(\w+)\}/g, function (_, k) { return o[k]; }); };
  var lget = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, lset = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
  var loc = { fr: "fr-FR", en: "en-GB", it: "it-IT" }[lang];
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var jour = function (d) { try { return new Date(d + "T12:00:00").toLocaleDateString(loc, { day: "numeric", month: "long" }); } catch (e) { return d; } };
  var root = $("[data-vx-base]"), base = root ? root.dataset.vxBase : "/visiter/", dataUrl = root ? root.dataset.vxData : "/data/visiter-fr.json";

  // ---- Villes de départ proposées (code de ville → nom dans la langue) et aéroport utilisé pour les prix et les liens
  var NOMS = { PAR: ["Paris", "Paris", "Parigi"], LYS: ["Lyon", "Lyon", "Lione"], MRS: ["Marseille", "Marseille", "Marsiglia"], NCE: ["Nice", "Nice", "Nizza"], TLS: ["Toulouse", "Toulouse", "Tolosa"],
    BRU: ["Bruxelles", "Brussels", "Bruxelles"], GVA: ["Genève", "Geneva", "Ginevra"], MIL: ["Milan", "Milan", "Milano"], ROM: ["Rome", "Rome", "Roma"], VCE: ["Venise", "Venice", "Venezia"], BLQ: ["Bologne", "Bologna", "Bologna"],
    LON: ["Londres", "London", "Londra"], MAD: ["Madrid", "Madrid", "Madrid"], AMS: ["Amsterdam", "Amsterdam", "Amsterdam"], FRA: ["Francfort", "Frankfurt", "Francoforte"], YMQ: ["Montréal", "Montreal", "Montréal"], NYC: ["New York", "New York", "New York"] };
  var VILLES = {}; Object.keys(NOMS).forEach(function (c) { VILLES[c] = NOMS[c][{ fr: 0, en: 1, it: 2 }[lang]]; });
  var AERO = { PAR: "CDG", MIL: "MXP", ROM: "FCO", LON: "LHR", YMQ: "YUL", NYC: "JFK" };
  var aero = function (c) { return AERO[c] || c; };
  var PAYS_DEP = { FR: "PAR", BE: "BRU", CH: "GVA", IT: "MIL", GB: "LON", ES: "MAD", NL: "AMS", DE: "FRA", CA: "YMQ", US: "NYC", LU: "BRU" };
  var depart = function (cb) { // ville mémorisée, sinon déduite du pays du visiteur (sans cookie)
    var m = lget("escale.depart"); if (m && VILLES[m]) return cb(m);
    fetch("/api/geo").then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; }).then(function (g) { cb(PAYS_DEP[g.country] || "PAR"); });
  };
  var cachePrix = {};
  var prix = function (ville) { // prix aller-retour les plus bas repérés vers chaque pays, depuis cette ville (/api/ruban)
    if (!cachePrix[ville]) cachePrix[ville] = fetch("/api/ruban?v=2&from=" + aero(ville)).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; })
      .then(function (j) { return (j && j.available && j.prix) || {}; });
    return cachePrix[ville];
  };
  var remplirVilles = function (sel, sauf) { Object.keys(VILLES).forEach(function (c) { if (aero(c) !== sauf) { var o = document.createElement("option"); o.value = c; o.textContent = VILLES[c]; sel.appendChild(o); } }); };
  var donnees = null, charger = function () { if (!donnees) donnees = fetch(dataUrl).then(function (r) { return r.json(); }).catch(function () { return { pays: [] }; }); return donnees; };
  var lienVols = function (ville, air, x) { return "/?type=vols&from=" + aero(ville) + "&to=" + air + (x ? "&dep=" + x.dep + (x.ret ? "&ret=" + x.ret : "") : "") + (lang === "fr" ? "" : "&lang=" + lang); };
  window.VX = { lang: lang, T: T, VILLES: VILLES, aero: aero, depart: depart, prix: prix, money: money, jour: jour, esc: esc, fmt: fmt, base: base, data: charger, remplirVilles: remplirVilles, lienVols: lienVols,
    setDepart: function (c) { lset("escale.depart", c); } };

  // ---- 1. Envies : cœur sur chaque lieu, liste, alerte prix par pays
  function lire() { try { var v = JSON.parse(lget(KEY) || "[]"); return Array.isArray(v) ? v.filter(function (x) { return x && x.k && x.n && x.u; }).slice(0, 200) : []; } catch (e) { return []; } }
  function maj() {
    var L = lire(), ks = L.map(function (x) { return x.k; });
    $$(".vx-like").forEach(function (b) { var on = ks.indexOf(b.dataset.k) >= 0; b.setAttribute("aria-pressed", on ? "true" : "false"); b.title = on ? T.rm : T.add; });
    $$("[data-envies-n]").forEach(function (e) { e.textContent = L.length; e.hidden = !L.length; });
    var box = $("#vx-envies"); if (!box) return;
    box.hidden = !L.length;
    var ul = $("ul", box);
    if (ul) ul.innerHTML = L.map(function (x) {
      return '<li><a href="' + esc(x.u) + '"><img src="/img/visiter/' + esc(x.k) + '-640.webp" alt="" width="64" height="64" loading="lazy"><span><b>' + esc(x.n) + "</b><small>" + esc(x.p || "") +
        '</small></span></a><button type="button" class="vx-rm" data-k="' + esc(x.k) + '" aria-label="' + esc(T.retirer + " " + x.n) + '">×</button></li>';
    }).join("");
    var al = $("#vx-alertes", box); if (!al) return;
    var ccs = []; L.forEach(function (x) { var c = x.k.slice(0, 2); if (ccs.indexOf(c) < 0) ccs.push(c); });
    if (!ccs.length) { al.innerHTML = ""; return; }
    charger().then(function (d) {
      var done = []; try { done = JSON.parse(lget("escale.envies-alertes") || "[]"); } catch (e) {}
      al.innerHTML = ccs.slice(0, 6).map(function (c) { var p = d.pays.filter(function (y) { return y.cc === c; })[0]; if (!p || done.indexOf(c) >= 0) return "";
        return '<button type="button" class="vx-al" data-cc="' + c + '" data-air="' + esc(p.air) + '" data-ville="' + esc(p.ville) + '">' + esc(fmt(T.al_btn, { v: p.ville })) + "</button>"; }).join("");
    });
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".vx-like, .vx-rm");
    if (!b) return;
    var L = lire(), k = b.dataset.k, i = L.map(function (x) { return x.k; }).indexOf(k);
    if (i >= 0) L.splice(i, 1);
    else if (b.classList.contains("vx-like") && /^[a-z]{2}-[a-z0-9]+$/.test(k)) { L.unshift({ k: k, n: b.dataset.n, p: b.dataset.p, u: location.pathname + "#" + k }); b.classList.remove("pop"); void b.offsetWidth; b.classList.add("pop"); }
    lset(KEY, JSON.stringify(L)); maj();
  });
  maj();

  // Alerte prix depuis les envies : petit formulaire (ville de départ, e-mail, budget), envoyé à /api/alert
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".vx-al"); if (!b) return;
    var old = $(".vx-alform"); if (old) old.remove();
    var f = document.createElement("form"); f.className = "vx-alform"; f.noValidate = true;
    f.innerHTML = "<h3>" + esc(fmt(T.al_h, { v: b.dataset.ville })) + "</h3><p class='small'>" + esc(T.al_p) + "</p>" +
      "<label><span>" + esc(T.al_from) + "</span><select name='from'><option value=''>" + esc(T.choisir) + "</option></select></label>" +
      "<label><span>" + esc(T.al_email) + "</span><input type='email' name='email' autocomplete='email' required></label>" +
      "<label><span>" + esc(T.al_max) + "</span><input type='number' name='max' min='1' step='1' inputmode='numeric' required></label><p class='small vx-alvu' hidden></p>" +
      "<label class='vx-alc'><input type='checkbox' name='consent' required> <span>" + esc(T.al_consent) + "</span></label>" +
      "<p><button type='submit' class='btn'>" + esc(T.al_go) + "</button></p><p class='small vx-almsg' role='status'></p>";
    b.insertAdjacentElement("afterend", f);
    remplirVilles(f.from, b.dataset.air);
    var proposer = function () {
      if (!f.from.value) return;
      prix(f.from.value).then(function (P) { var x = P[b.dataset.cc], vu = $(".vx-alvu", f);
        if (x && x.price > 0) { vu.textContent = fmt(T.al_vu, { p: money(x.price) }); vu.hidden = false; if (!f.max.value || f.max.dataset.auto) { f.max.value = Math.max(1, Math.floor(x.price * 0.9 / 10) * 10); f.max.dataset.auto = "1"; } }
        else vu.hidden = true; });
    };
    f.max.addEventListener("input", function () { delete f.max.dataset.auto; });
    f.from.addEventListener("change", function () { if (f.from.value) lset("escale.depart", f.from.value); proposer(); });
    depart(function (c) { if (VILLES[c] && aero(c) !== b.dataset.air) { f.from.value = c; proposer(); } });
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = $(".vx-almsg", f), email = f.email.value.trim(), max = Number(f.max.value);
      if (!f.from.value || !/^\S+@\S+\.\S+$/.test(email) || !(max > 0) || !f.consent.checked) { msg.textContent = T.al_err; return; }
      var go = f.querySelector("button"); go.disabled = true;
      fetch("/api/alert", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, max: max, from: aero(f.from.value), to: b.dataset.air, lang: lang, currency: "EUR", consent: true }) })
        .then(function (r) { return r.ok; }).catch(function () { return false; }).then(function (ok) {
          if (!ok) { msg.textContent = T.al_fail; go.disabled = false; return; }
          var done = []; try { done = JSON.parse(lget("escale.envies-alertes") || "[]"); } catch (e2) {}
          done.push(b.dataset.cc); lset("escale.envies-alertes", JSON.stringify(done.slice(-40)));
          f.innerHTML = "<p class='vx-alok'>" + esc(fmt(T.al_ok, { e: email })) + "</p>"; b.remove();
        });
    });
    f.email.focus();
  });

  // ---- 2. Recherche sur le sommaire (pays ou lieu)
  var q = $("#vx-q");
  if (q) {
    var norm = function (t) { return t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
    q.addEventListener("input", function () {
      var v = norm(q.value.trim()), n = 0;
      $$(".vx-hub a[data-mots]").forEach(function (a) { var ok = !v || norm(a.dataset.mots).indexOf(v) >= 0; a.hidden = !ok; if (ok) n++; });
      $$(".vx-reg").forEach(function (h) { var g = h.nextElementSibling; h.hidden = !g || !$$("a:not([hidden])", g).length; });
      var m = $("#vx-q-msg"); if (m) m.textContent = v ? (n ? fmt(n > 1 ? T.nx : T.n1, { n: n }) : T.n0) : "";
    });
  }

  // ---- 3. Page d'un pays : prix du vol depuis la ville du visiteur, puis budget du voyage
  var cta = $(".vx-cta[data-air]");
  if (cta && "IntersectionObserver" in window) {
    // Le visiteur écrit lui-même sa ville ou son aéroport de départ (3 200 aéroports, liste chargée quand il touche le champ) :
    // jusqu'au 13 novembre 2026, c'était une liste fermée de 17 villes.
    var out = $(".vx-prix", cta), inp = $(".vx-from", cta), air = cta.dataset.air, cc = cta.dataset.cc, vol = $("#vb-vol", cta), cur = "";
    var afficher = function (from, nom) {
      cur = from;
      if (!from || aero(from) === air) { out.textContent = ""; return; }
      out.textContent = T.cherche;
      prix(from).then(function (P) {
        if (cur !== from) return;
        var x = P[cc], a = $("a.btn", cta);
        if (!x || !(x.price > 0)) { out.textContent = fmt(T.aucun, { v: nom }); if (a) a.href = lienVols(from, air); return; }
        out.innerHTML = "<strong>" + esc(fmt(T.prix, { a: nom, b: cta.dataset.ville, p: money(x.price) })) + "</strong> " + (x.ret ? esc(fmt(T.dates, { d1: jour(x.dep), d2: jour(x.ret) })) + " " : "") + esc(T.note);
        if (a) a.href = lienVols(from, air, x);
        if (vol && (!vol.value || vol.dataset.auto)) { vol.value = Math.round(x.price); vol.dataset.auto = "1"; budget(); }
      });
    };
    var acP = null, ac = function () { // recherche de ville ou d'aéroport (site/ac-mini.js), chargée une seule fois
      if (!acP) acP = new Promise(function (ok) {
        if (window.EscaleAC) return ok();
        var sc = document.createElement("script"); sc.src = "/ac-mini.js"; sc.onload = ok; sc.onerror = ok; document.head.appendChild(sc);
      }).then(function () { return window.EscaleAC ? window.EscaleAC.ready : null; }).then(function () {
        if (!window.EscaleAC) return;
        window.EscaleAC.attach(inp, function (code, nom) { lset("escale.aeroport", code + "|" + nom); if (VILLES[code]) lset("escale.depart", code); afficher(code, nom); });
        if (inp.value.trim().length >= 2 && !inp.dataset.code) inp.dispatchEvent(new Event("input")); // ce qui a été tapé pendant le chargement
      });
      return acP;
    };
    if (inp) {
      inp.addEventListener("focus", ac); inp.addEventListener("input", function () { ac(); if (!inp.value.trim()) afficher("", ""); });
      var io = new IntersectionObserver(function (es) {
        if (!es[0].isIntersecting) return; io.disconnect();
        var m = (lget("escale.aeroport") || "").split("|"); // dernier départ écrit par ce visiteur (reste dans son appareil)
        if (/^[A-Z]{3}$/.test(m[0]) && m[1] && aero(m[0]) !== air) { inp.value = m[1] + " (" + m[0] + ")"; inp.dataset.code = m[0]; afficher(m[0], m[1]); }
      }, { rootMargin: "500px 0px" });
      io.observe(cta);
    }
  }
  function budget() {
    var g = function (id) { var e = document.getElementById(id); return e ? Math.max(0, Number(e.value) || 0) : 0; }, tot = document.getElementById("vb-tot"); if (!tot) return;
    var pers = Math.max(1, Math.round(g("vb-pers"))), nuits = Math.round(g("vb-nuits")), a = g("vb-vol") * pers, b = g("vb-log") * nuits, c = g("vb-jour") * nuits * pers, t = a + b + c;
    tot.innerHTML = t > 0 ? "<strong>" + esc(fmt(T.tot, { t: money(t), pp: money(t / pers) })) + "</strong><br><small>" + esc(fmt(T.det, { a: money(a), b: money(b), c: money(c) })) + "</small>" : "";
  }
  $$(".vx-budget input").forEach(function (i) { i.addEventListener("input", function () { if (i.id === "vb-vol") delete i.dataset.auto; budget(); }); });

  // ---- 4. Carte postale : image 1080 × 1920 fabriquée dans le téléphone (photo créditée), à partager ou à télécharger
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".vx-pc"); if (!b) return;
    var d = b.dataset, im = new Image();
    im.onload = function () {
      var W = 1080, H = 1920, c = document.createElement("canvas"); c.width = W; c.height = H; var x = c.getContext("2d");
      x.fillStyle = "#061a1f"; x.fillRect(0, 0, W, H);
      var ph = 1240, s = Math.max(W / im.width, ph / im.height), w = im.width * s, h = im.height * s; x.drawImage(im, (W - w) / 2, (ph - h) / 2, w, h);
      var g = x.createLinearGradient(0, ph - 420, 0, ph); g.addColorStop(0, "rgba(6,26,31,0)"); g.addColorStop(1, "#061a1f"); x.fillStyle = g; x.fillRect(0, ph - 420, W, 421);
      var serif = '"Fraunces", Georgia, serif', sans = '"Nunito", "Segoe UI", system-ui, sans-serif';
      x.textBaseline = "alphabetic"; x.fillStyle = "#7ff3de"; x.font = "800 44px " + sans; x.fillText(T.pc_top, 70, ph + 70);
      var size = 150; x.fillStyle = "#fff"; do { x.font = "600 " + size + "px " + serif; size -= 6; } while (x.measureText(d.n).width > W - 140 && size > 60);
      x.fillText(d.n, 70, ph + 70 + size + 40);
      x.font = "700 64px " + sans; x.fillStyle = "#e6f6f3"; x.fillText(d.p + " " + d.f, 70, ph + 70 + size + 150);
      x.fillStyle = "#19c7b1"; x.fillRect(70, H - 250, 120, 8);
      x.font = "italic 600 76px " + serif; x.fillStyle = "#fff"; x.fillText("escale", 70, H - 150); var ew = x.measureText("escale").width; x.fillStyle = "#7ff3de"; x.fillText(".live", 70 + ew, H - 150);
      x.font = "500 28px " + sans; x.fillStyle = "rgba(255,255,255,.72)"; x.fillText("Photo : " + d.a + ", " + d.l + ", Wikimedia Commons", 70, H - 70, W - 140);
      var ov = document.createElement("div"); ov.className = "vx-pcov"; ov.setAttribute("role", "dialog"); ov.setAttribute("aria-modal", "true");
      ov.innerHTML = '<div class="vx-pcbox"><p class="vx-pcbtn"><button type="button" class="btn" data-a="s" hidden>' + esc(T.pc_share) + '</button><a class="btn ghost" data-a="d" download="escale-' + esc(d.k) + '.jpg">' + esc(T.pc_dl) +
        '</a><button type="button" class="btn ghost" data-a="x">' + esc(T.pc_x) + "</button></p></div>";
      c.className = "vx-pccan"; ov.firstChild.insertBefore(c, ov.firstChild.firstChild); document.body.appendChild(ov);
      var fermer = function () { ov.remove(); document.removeEventListener("keydown", esc2); }, esc2 = function (ev) { if (ev.key === "Escape") fermer(); };
      document.addEventListener("keydown", esc2);
      ov.addEventListener("click", function (ev) { if (ev.target === ov || (ev.target.dataset && ev.target.dataset.a === "x")) fermer(); });
      c.toBlob(function (blob) {
        if (!blob) return;
        $('[data-a="d"]', ov).href = URL.createObjectURL(blob);
        var file = null; try { file = new File([blob], "escale-" + d.k + ".jpg", { type: "image/jpeg" }); } catch (err) {}
        var sh = $('[data-a="s"]', ov);
        if (file && navigator.canShare && navigator.canShare({ files: [file] })) { sh.hidden = false; sh.onclick = function () { navigator.share({ files: [file], text: fmt(T.pc_txt, { n: d.n, p: d.p }) + " · escale.live" }).catch(function () {}); }; }
      }, "image/jpeg", 0.9);
    };
    var lancer = function () { im.src = "/img/visiter/" + d.k + ".webp"; };
    if (document.fonts && document.fonts.load) Promise.all([document.fonts.load('600 100px "Fraunces"'), document.fonts.load('italic 600 76px "Fraunces"'), document.fonts.load('800 44px "Nunito"')]).then(lancer, lancer); else lancer();
  });

  // ---- 5. Partage de la page
  var sh = $("#vx-share");
  if (sh) sh.addEventListener("click", function () {
    var d = { title: document.title, text: sh.dataset.t, url: location.origin + location.pathname };
    if (navigator.share) navigator.share(d).catch(function () {});
    else window.open("https://wa.me/?text=" + encodeURIComponent(d.text + " " + d.url), "_blank", "noopener");
  });
})();
