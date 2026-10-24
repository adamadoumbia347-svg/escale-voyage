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
      kinds: { vol: "بحث عن رحلة", route: "رحلة", hotel: "فنادق", deal: "عرض" }, added: "أضيف في", clear: "حذف الكل", confirm: "حذف كل العناصر المفضلة؟" }
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
    var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn" }[lang()];
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
  // Mise à jour si les favoris changent dans un autre onglet
  window.addEventListener("storage", function (e) { if (e.key === KEY) sync(); });
  window.EscaleFavs = { sync: sync };
  sync();
})();
