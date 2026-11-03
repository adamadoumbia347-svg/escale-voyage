// Accueil : « Vos trajets » (trajets consultés, gardés dans ce navigateur, avec l'évolution du prix depuis la dernière visite),
// photo de destination derrière le titre, et « Partez ce mois-ci » (destinations les moins chères depuis Paris, /api/deals).
(function () {
  "use strict";
  var lang = (document.documentElement.lang || "fr").slice(0, 2);
  var T = function (fr, en) { return lang === "fr" ? fr : en; };
  var loc = { fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn" }[lang] || "fr-FR";
  var money = function (n) { try { return new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n); } catch (e) { return Math.round(n) + " €"; } };
  var esc = function (t) { return String(t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var get = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } };
  var set = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
  var dd = function (n) { var d = new Date(Date.now() + n * 864e5); return String(d.getDate()).padStart(2, "0") + String(d.getMonth() + 1).padStart(2, "0"); };

  // 1. Vos trajets
  var list = []; try { list = JSON.parse(get("escale.trajets") || "[]"); } catch (e) { list = []; }
  var box = document.getElementById("my-routes"), row = document.getElementById("my-row");
  if (box && row && list.length) {
    var link = function (x) { return x.u || ("/recherche/?flightSearch=" + x.f + dd(45) + x.t + dd(52) + "1"); };
    var paint = function (prices) {
      row.innerHTML = list.map(function (x) {
        var k = prices[x.f + "-" + x.t], now = k && k.price, diff = now && x.p ? now - x.p : 0;
        var d = !diff ? "" : diff < 0 ? ' <i class="tr dn">↓ ' + esc(money(-diff)) + "</i>" : ' <i class="tr up">↑ ' + esc(money(diff)) + "</i>";
        return '<a class="pop-chip" href="' + esc(link(x)) + '"><span>' + esc(x.l) + "</span>" + (now ? '<b class="pr">' + esc(money(now)) + d + "</b>" : "") + "</a>";
      }).join("");
      box.hidden = false;
      // Le prix d'aujourd'hui devient la référence de la prochaine visite
      list.forEach(function (x) { var k = prices[x.f + "-" + x.t]; if (k && k.price) x.p = k.price; });
      set("escale.trajets", JSON.stringify(list));
    };
    fetch("/api/connus?r=" + list.map(function (x) { return x.f + "-" + x.t; }).join(","))
      .then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; })
      .then(function (j) { paint((j && j.prix) || {}); });
  }

  // 2. Photo de destination derrière le titre (une ville différente à chaque visite), chargée au premier geste du visiteur
  // (défilement, toucher, clic, clavier) : elle ne retarde jamais l'affichage de la page ni du moteur de recherche.
  var PHOTOS = ["dakar", "marrakech", "abidjan", "casablanca", "tunis", "djerba", "alger", "le-caire", "tanger", "accra", "lisbonne", "istanbul"];
  var EV = ["scroll", "pointerdown", "touchstart", "keydown"], photoDone = false;
  var photo = function () {
    if (photoDone) return; photoDone = true;
    EV.forEach(function (e) { removeEventListener(e, photo, { passive: true }); });
    var band = document.querySelector(".band");
    if (!band || matchMedia("(prefers-reduced-data: reduce)").matches || document.documentElement.classList.contains("lite")) return;
    var n = (+(get("escale.photo") || 0) + 1) % PHOTOS.length; set("escale.photo", String(n));
    var img = new Image();
    img.onload = function () { band.style.setProperty("--hero-img", "url(" + img.src + ")"); band.classList.add("has-photo"); };
    img.src = "/img/villes/" + PHOTOS[n] + (innerWidth > 700 ? ".webp" : "-480.webp");
  };
  EV.forEach(function (e) { addEventListener(e, photo, { passive: true }); });

  // 3. Partez ce mois-ci : chargé quand la section approche de l'écran
  var sec = document.getElementById("partez"), grid = document.getElementById("partez-grid");
  if (!sec || !grid) return;
  // Photos des villes (site/data/photos.json) ; les aéroports d'une même ville prennent la photo de la ville
  var ALIAS = { LHR: "LON", LGW: "LON", STN: "LON", LTN: "LON", LCY: "LON", MXP: "MIL", LIN: "MIL", BGY: "MIL", FCO: "ROM", CIA: "ROM", TSF: "VCE",
    ARN: "STO", BMA: "STO", KEF: "REK", TFS: "TCI", TFN: "TCI", NYC: "JFK", EWR: "JFK", LGA: "JFK", SAW: "IST", YUL: "YMQ", TYO: "HND", NRT: "HND", CAS: "CMN", DKR: "DSS",
    BUH: "OTP", PAR: "CDG", MOW: "SVO", ROM: "ROM" };
  var slugOf = function (img) { var m = /\/img\/villes\/([a-z0-9-]+)\.webp$/.exec(img || ""); return m ? m[1] : null; };
  var day = function (s) { var p = s.split("-"); return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString(loc, { day: "numeric", month: "short" }); };
  var ddmm = function (s) { return s.slice(8, 10) + s.slice(5, 7); };
  var go = function () {
    Promise.all([
      fetch("/api/deals?currency=EUR").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }),
      (window.ESCALE_AIRPORTS = window.ESCALE_AIRPORTS || fetch("/data/airports.json").then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; })),
      fetch("/data/photos.json").then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; })
    ]).then(function (res) {
      var d = res[0], names = {}, IMG = {};
      (res[2] || []).forEach(function (p) { var sl = slugOf(p.img); if (sl) IMG[p.code] = sl; });
      (res[1] || []).forEach(function (a) { if (!names[a[0]]) names[a[0]] = a[1]; });
      var deals = d && d.origins && d.origins.CDG ? d.origins.CDG.filter(function (x) { return x.dep && x.ret; }).slice(0, 8) : [];
      if (!deals.length) return;
      grid.innerHTML = deals.map(function (x) {
        var city = names[x.to] || x.to, img = document.documentElement.classList.contains("lite") ? null : (IMG[x.to] || IMG[ALIAS[x.to]]);  // mode léger : sans photo
        var href = "/recherche/?flightSearch=CDG" + ddmm(x.dep) + x.to + ddmm(x.ret) + "1";
        return '<a class="city-card' + (img ? "" : " no-img") + '" href="' + esc(href) + '">' +
          (img ? '<img src="/img/villes/' + img + '-480.webp" width="480" height="360" alt="" loading="lazy" decoding="async">' : "") +
          '<span class="city-info"><strong>' + esc(city) + '</strong><small>' + esc(day(x.dep) + " → " + day(x.ret)) + '</small><b class="city-price">' + esc(T("dès ", "from ") + money(x.price)) + "</b></span></a>";
      }).join("");
      sec.hidden = false;
    });
  };
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (e) { if (e.some(function (x) { return x.isIntersecting; })) { io.disconnect(); go(); } }, { rootMargin: "600px" });
    io.observe(document.getElementById("fetes") || document.querySelector("main")); // la section est cachée tant qu'elle est vide : on observe la suivante
  } else go();
})();
