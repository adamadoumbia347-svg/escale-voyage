// Favoris sans compte : trajets, hôtels et recherches gardés dans ce navigateur (localStorage), jamais envoyés au serveur.
(function () {
  "use strict";
  var KEY = "escale.favs", MAX = 60;
  var L = {
    fr: { save: "Ajouter aux favoris", saved: "Dans vos favoris", short: "Favori", shortOn: "Enregistré", remove: "Retirer", open: "Ouvrir",
      empty: "Aucun favori pour l’instant. Touchez l’étoile sur un trajet, un hôtel ou une recherche pour le retrouver ici.",
      kinds: { vol: "Recherche de vol", route: "Trajet", hotel: "Hôtels", deal: "Bon plan" }, added: "Ajouté le", clear: "Tout effacer", confirm: "Effacer tous les favoris ?" },
    en: { save: "Add to favorites", saved: "In your favorites", short: "Save", shortOn: "Saved", remove: "Remove", open: "Open",
      empty: "No favorites yet. Tap the star on a route, a hotel page or a search to find it here.",
      kinds: { vol: "Flight search", route: "Route", hotel: "Hotels", deal: "Deal" }, added: "Added on", clear: "Clear all", confirm: "Delete all favorites?" },
    es: { save: "Añadir a favoritos", saved: "En tus favoritos", short: "Favorito", shortOn: "Guardado", remove: "Quitar", open: "Abrir",
      empty: "Aún no tienes favoritos. Toca la estrella en una ruta, un hotel o una búsqueda para encontrarlo aquí.",
      kinds: { vol: "Búsqueda de vuelo", route: "Ruta", hotel: "Hoteles", deal: "Oferta" }, added: "Añadido el", clear: "Borrar todo", confirm: "¿Borrar todos los favoritos?" },
    pt: { save: "Adicionar aos favoritos", saved: "Nos seus favoritos", short: "Favorito", shortOn: "Guardado", remove: "Remover", open: "Abrir",
      empty: "Ainda não tem favoritos. Toque na estrela de uma rota, de um hotel ou de uma pesquisa para a encontrar aqui.",
      kinds: { vol: "Pesquisa de voo", route: "Rota", hotel: "Hotéis", deal: "Promoção" }, added: "Adicionado a", clear: "Apagar tudo", confirm: "Apagar todos os favoritos?" },
    ar: { save: "أضف إلى المفضلة", saved: "في المفضلة", short: "المفضلة", shortOn: "محفوظ", remove: "إزالة", open: "فتح",
      empty: "لا توجد عناصر مفضلة بعد. المس النجمة في صفحة رحلة أو فندق أو بحث لتجده هنا.",
      kinds: { vol: "بحث عن رحلة", route: "رحلة", hotel: "فنادق", deal: "عرض" }, added: "أضيف في", clear: "حذف الكل", confirm: "حذف كل العناصر المفضلة؟" },
    it: { save: "Aggiungi ai preferiti", saved: "Nei tuoi preferiti", short: "Preferito", shortOn: "Salvato", remove: "Rimuovi", open: "Apri",
      empty: "Ancora nessun preferito. Tocca la stella su una tratta, un hotel o una ricerca per ritrovarla qui.",
      kinds: { vol: "Ricerca voli", route: "Tratta", hotel: "Hotel", deal: "Offerta" }, added: "Aggiunto il", clear: "Cancella tutto", confirm: "Cancellare tutti i preferiti?" },
    de: { save: "Zu Favoriten hinzufügen", saved: "In deinen Favoriten", short: "Merken", shortOn: "Gemerkt", remove: "Entfernen", open: "Öffnen",
      empty: "Noch keine Favoriten. Tippe auf den Stern bei einer Strecke, einem Hotel oder einer Suche, um sie hier wiederzufinden.",
      kinds: { vol: "Flugsuche", route: "Strecke", hotel: "Hotels", deal: "Angebot" }, added: "Hinzugefügt am", clear: "Alle löschen", confirm: "Alle Favoriten löschen?" },
    nl: { save: "Toevoegen aan favorieten", saved: "In je favorieten", short: "Bewaren", shortOn: "Bewaard", remove: "Verwijderen", open: "Openen",
      empty: "Nog geen favorieten. Tik op de ster bij een route, hotel of zoekopdracht om die hier terug te vinden.",
      kinds: { vol: "Vluchtzoekopdracht", route: "Route", hotel: "Hotels", deal: "Aanbieding" }, added: "Toegevoegd op", clear: "Alles wissen", confirm: "Alle favorieten wissen?" }
  };
  var lang = function () { var l = (document.documentElement.lang || "fr").slice(0, 2); return L[l] ? l : "fr"; };
  var esc = function (t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  function read() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v.filter(function (f) { return f && typeof f.u === "string" && f.u.charAt(0) === "/"; }) : []; }
    catch (e) { return []; }
  }
  function write(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list.slice(0, MAX))); } catch (e) {}
    sync();
  }
  var has = function (list, u) { return list.some(function (f) { return f.u === u; }); };

  function sync() {
    var list = read(), l = L[lang()];
    document.querySelectorAll("[data-fav]").forEach(function (b) {
      var on = has(list, b.getAttribute("data-fav"));
      b.setAttribute("aria-pressed", String(on));
      var s = b.querySelector("span");
      if (s) s.textContent = b.classList.contains("go") ? (on ? l.shortOn : l.short) : (on ? l.saved : l.save);
    });
    document.querySelectorAll("[data-fav-count]").forEach(function (c) { c.textContent = String(list.length); c.hidden = !list.length; });
    var box = document.getElementById("fav-list");
    if (box) paint(box, list, l);
  }

  function paint(box, list, l) {
    var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn", it: "it-IT", de: "de-DE", nl: "nl-NL" }[lang()];
    var clear = document.getElementById("fav-clear");
    if (clear) clear.hidden = !list.length;
    if (!list.length) { box.innerHTML = '<p class="fav-empty">' + esc(l.empty) + "</p>"; return; }
    box.innerHTML = '<ul class="fav-list">' + list.map(function (f) {
      var when = "";
      try { when = f.at ? l.added + " " + new Date(f.at).toLocaleDateString(loc, { day: "numeric", month: "short" }) : ""; } catch (e) {}
      return '<li class="fav-item"><a class="fav-main" href="' + esc(f.u) + '"><span class="fav-kind">' + esc(l.kinds[f.k] || "") + "</span>" +
        "<strong><bdi>" + esc(f.t) + "</bdi></strong>" + (f.s ? '<span class="fav-sub">' + esc(f.s) + "</span>" : "") +
        (when ? '<span class="fav-sub">' + esc(when) + "</span>" : "") + "</a>" +
        '<button type="button" class="fav-remove" data-unfav="' + esc(f.u) + '" aria-label="' + esc(l.remove + " : " + f.t) + '">' + esc(l.remove) + "</button></li>";
    }).join("") + "</ul>";
  }

  document.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest("[data-fav]");
    if (b) {
      ev.preventDefault();
      var u = b.getAttribute("data-fav"), list = read();
      if (has(list, u)) list = list.filter(function (f) { return f.u !== u; });
      else list.unshift({ u: u, t: b.getAttribute("data-fav-title") || document.title, s: b.getAttribute("data-fav-sub") || "", k: b.getAttribute("data-fav-kind") || "route", at: Date.now() });
      write(list);
      return;
    }
    var r = ev.target.closest && ev.target.closest("[data-unfav]");
    if (r) { var v = r.getAttribute("data-unfav"); write(read().filter(function (f) { return f.u !== v; })); return; }
    if (ev.target.closest && ev.target.closest("#fav-clear") && window.confirm(L[lang()].confirm)) write([]);
  });

  // Retrouver ses favoris sur un autre appareil, sans compte : un lien qui contient la liste (dans la partie après #, jamais envoyée au serveur).
  // Ouvert sur l'autre appareil, il ajoute les favoris à ceux qui y sont déjà.
  var M = {
    fr: { h: "📲 Retrouver mes favoris sur un autre appareil", p: "Envoyez-vous ce lien (WhatsApp, e-mail) et ouvrez-le sur l’autre téléphone ou ordinateur : vos favoris s’y ajoutent. Aucun compte, rien n’est gardé sur nos serveurs.", wa: "WhatsApp", mail: "E-mail", copy: "Copier le lien", copied: "Lien copié", txt: "Mes favoris Escale :", ok: "{n} favori(s) ajouté(s) sur cet appareil.", none: "Ces favoris sont déjà sur cet appareil." },
    en: { h: "📲 Get my favorites on another device", p: "Send yourself this link (WhatsApp, email) and open it on the other phone or computer: your favorites are added there. No account, nothing is kept on our servers.", wa: "WhatsApp", mail: "Email", copy: "Copy link", copied: "Link copied", txt: "My Escale favorites:", ok: "{n} favorite(s) added on this device.", none: "These favorites are already on this device." },
    es: { h: "📲 Recuperar mis favoritos en otro dispositivo", p: "Envíate este enlace (WhatsApp, correo) y ábrelo en el otro teléfono u ordenador: tus favoritos se añaden allí. Sin cuenta, nada se guarda en nuestros servidores.", wa: "WhatsApp", mail: "Correo", copy: "Copiar enlace", copied: "Enlace copiado", txt: "Mis favoritos de Escale:", ok: "{n} favorito(s) añadido(s) en este dispositivo.", none: "Estos favoritos ya están en este dispositivo." },
    pt: { h: "📲 Recuperar os meus favoritos noutro dispositivo", p: "Envie este link para si (WhatsApp, e-mail) e abra-o no outro telemóvel ou computador: os seus favoritos são adicionados. Sem conta, nada fica nos nossos servidores.", wa: "WhatsApp", mail: "E-mail", copy: "Copiar link", copied: "Link copiado", txt: "Os meus favoritos Escale:", ok: "{n} favorito(s) adicionado(s) neste dispositivo.", none: "Estes favoritos já estão neste dispositivo." },
    ar: { h: "📲 استرجاع المفضلة على جهاز آخر", p: "أرسل هذا الرابط لنفسك (واتساب، بريد إلكتروني) وافتحه على الهاتف أو الحاسوب الآخر: تُضاف مفضلتك هناك. بدون حساب، ولا شيء يُحفظ على خوادمنا.", wa: "واتساب", mail: "بريد إلكتروني", copy: "نسخ الرابط", copied: "تم نسخ الرابط", txt: "مفضلتي على Escale:", ok: "تمت إضافة {n} إلى المفضلة على هذا الجهاز.", none: "هذه العناصر موجودة بالفعل على هذا الجهاز." },
    it: { h: "📲 Ritrovare i miei preferiti su un altro dispositivo", p: "Inviati questo link (WhatsApp, e-mail) e aprilo sull’altro telefono o computer: i tuoi preferiti vengono aggiunti. Nessun account, niente resta sui nostri server.", wa: "WhatsApp", mail: "E-mail", copy: "Copia il link", copied: "Link copiato", txt: "I miei preferiti Escale:", ok: "{n} preferito/i aggiunto/i su questo dispositivo.", none: "Questi preferiti sono già su questo dispositivo." },
    de: { h: "📲 Meine Favoriten auf einem anderen Gerät", p: "Schick dir diesen Link (WhatsApp, E-Mail) und öffne ihn auf dem anderen Handy oder Computer: Deine Favoriten werden dort hinzugefügt. Kein Konto, nichts wird auf unseren Servern gespeichert.", wa: "WhatsApp", mail: "E-Mail", copy: "Link kopieren", copied: "Link kopiert", txt: "Meine Escale-Favoriten:", ok: "{n} Favorit(en) auf diesem Gerät hinzugefügt.", none: "Diese Favoriten sind schon auf diesem Gerät." },
    nl: { h: "📲 Mijn favorieten op een ander apparaat", p: "Stuur jezelf deze link (WhatsApp, e-mail) en open hem op de andere telefoon of computer: je favorieten worden daar toegevoegd. Geen account, niets blijft op onze servers.", wa: "WhatsApp", mail: "E-mail", copy: "Link kopiëren", copied: "Link gekopieerd", txt: "Mijn Escale-favorieten:", ok: "{n} favoriet(en) toegevoegd op dit apparaat.", none: "Deze favorieten staan al op dit apparaat." }
  };
  var b64 = function (t) { return btoa(unescape(encodeURIComponent(t))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); };
  var unb64 = function (t) { return decodeURIComponent(escape(atob(t.replace(/-/g, "+").replace(/_/g, "/")))); };
  var cut = function (v, n) { return String(v == null ? "" : v).slice(0, n); };
  function lien() {
    var data = read().slice(0, 40).map(function (x) { return [x.u, cut(x.t, 80), cut(x.s, 60), x.k || "route"]; });
    return location.origin + location.pathname + "#f=" + b64(JSON.stringify(data));
  }
  function recevoir() {
    var m = /^#f=([\w-]+)$/.exec(location.hash || ""); if (!m) return null;
    var n = 0;
    try {
      var data = JSON.parse(unb64(m[1])), list = read();
      if (Array.isArray(data)) data.slice(0, 40).forEach(function (x) {
        if (!Array.isArray(x) || typeof x[0] !== "string" || x[0].charAt(0) !== "/" || x[0].charAt(1) === "/" || x[0].length > 300 || has(list, x[0])) return;
        list.push({ u: x[0], t: cut(x[1], 80), s: cut(x[2], 60), k: /^(vol|route|hotel|deal)$/.test(x[3]) ? x[3] : "route", at: Date.now() }); n++;
      });
      if (n) write(list);
    } catch (e) { return null; }
    try { history.replaceState(null, "", location.pathname); } catch (e) {}
    return n;
  }
  function transfert() {
    var box = document.getElementById("fav-list"); if (!box || !box.parentNode) return;
    var recu = recevoir(), m = M[lang()], d = document.getElementById("fav-move");
    if (!d) { d = document.createElement("div"); d.id = "fav-move"; d.className = "fav-move"; box.parentNode.appendChild(d); }
    var some = read().length > 0;
    d.hidden = !some && recu === null;
    d.innerHTML = (recu !== null ? '<p class="ok" role="status">' + esc(recu ? m.ok.replace("{n}", recu) : m.none) + "</p>" : "") +
      (some ? "<h2>" + esc(m.h) + "</h2><p>" + esc(m.p) + '</p><div class="btns"><a class="btn" data-mv="wa" target="_blank" rel="noopener">' + esc(m.wa) + '</a><a class="btn ghost" data-mv="mail">' + esc(m.mail) + '</a><button type="button" class="btn ghost" data-mv="copy">' + esc(m.copy) + "</button></div>" : "");
    if (!some) return;
    var maj = function () { var u = lien(); d.querySelector('[data-mv="wa"]').href = "https://wa.me/?text=" + encodeURIComponent(m.txt + " " + u); d.querySelector('[data-mv="mail"]').href = "mailto:?subject=" + encodeURIComponent(m.txt) + "&body=" + encodeURIComponent(u); return u; };
    maj();
    d.querySelector('[data-mv="copy"]').addEventListener("click", function () {
      var b = this, u = maj();
      (navigator.clipboard ? navigator.clipboard.writeText(u) : Promise.reject()).then(function () { b.textContent = m.copied; }, function () { window.prompt(m.copy, u); });
    });
    d.addEventListener("click", function (e) { if (e.target.closest && e.target.closest("[data-mv]")) maj(); }, true);
  }
  // Mise à jour si les favoris changent dans un autre onglet
  window.addEventListener("storage", function (e) { if (e.key === KEY) sync(); });
  window.EscaleFavs = { sync: sync };
  sync();
  transfert();
  window.addEventListener("hashchange", transfert);
})();
