// Escale : comparateur de vols, hôtels et voitures.
// Recherche d'aéroports dans le monde entier, interface FR/EN, devises, idées de voyage avec prix réels.
(function () {
  "use strict";

  // ---------- Réglages : identifiants partenaires ----------
  // Laissés vides, les liens restent des liens normaux (voir CROISSANCE.md).
  const AFFILIATE = {
    booking_aid: "",      // Booking.com -> paramètre aid
    agoda_cid: "",        // Agoda Partners -> paramètre cid
    kayak_affid: "",      // Kayak / momondo -> paramètre affid
    skyscanner_wrap: "",  // Lien de suivi Skyscanner (Impact) ; l'URL de recherche est ajoutée à la fin
    travelpayouts_marker: "789659" // Identifiant Travelpayouts -> ajouté aux liens Aviasales (paramètre marker)
  };
  function tag(k, url) {
    const add = (u, key, val) => val ? u + (u.includes("?") ? "&" : "?") + key + "=" + encodeURIComponent(val) : u;
    if (k === "booking") return add(url, "aid", AFFILIATE.booking_aid);
    if (k === "agoda") return add(url, "cid", AFFILIATE.agoda_cid);
    if (k === "kayak" || k === "momondo") return add(url, "affid", AFFILIATE.kayak_affid);
    if (k === "sky" && AFFILIATE.skyscanner_wrap) return AFFILIATE.skyscanner_wrap + encodeURIComponent(url);
    return url;
  }

  const $ = (id) => document.getElementById(id);
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  const esc = (t) => String(t).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const q = (o) => Object.entries(o).filter(([, v]) => v !== "" && v != null).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join("&");
  const enc = encodeURIComponent;
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isLive = /^https?:$/.test(location.protocol) && window.top === window;

  // ---------- Langue ----------
  const LANGS = ["fr", "en", "es", "pt", "ar"];
  const urlLang = new URLSearchParams(location.search).get("lang");
  if (LANGS.includes(urlLang)) { try { localStorage.setItem("escale.lang", urlLang); } catch (e) {} }
  const navLang = (navigator.language || "fr").slice(0, 2).toLowerCase();
  let LANG = store.get("escale.lang") || (LANGS.includes(navLang) ? navLang : "en");
  if (!LANGS.includes(LANG)) LANG = "fr";
  // Français et anglais écrits dans le code ; espagnol, portugais et arabe dans i18n.js (clé = texte anglais)
  const DICT = window.ESCALE_I18N || {};
  const COL = { es: 0, pt: 1, ar: 2 };
  const tr = (en) => (DICT[en] && DICT[en][COL[LANG]]) || en;
  const T = (fr, en) => (LANG === "fr" ? fr : LANG === "en" ? en : tr(en));
  const fmt = (str, vars) => str.replace(/\{(\w+)\}/g, (m, k) => (k in vars ? vars[k] : m));
  const locale = () => ({ fr: "fr-FR", en: "en-GB", es: "es-ES", pt: "pt-PT", ar: "ar-u-nu-latn" })[LANG];

  function applyLang() {
    document.documentElement.lang = LANG;
    document.documentElement.dir = LANG === "ar" ? "rtl" : "ltr";
    document.querySelectorAll("[data-en]").forEach((el) => {
      if (el.dataset.fr == null) el.dataset.fr = el.textContent;
      el.textContent = T(el.dataset.fr, el.dataset.en);
    });
    document.querySelectorAll("[data-en-html]").forEach((el) => {
      if (el.dataset.frHtml == null) el.dataset.frHtml = el.innerHTML;
      el.innerHTML = T(el.dataset.frHtml, el.dataset.enHtml);
    });
    document.querySelectorAll("[data-en-ph]").forEach((el) => {
      if (el.dataset.frPh == null) el.dataset.frPh = el.placeholder;
      el.placeholder = T(el.dataset.frPh, el.dataset.enPh);
    });
    document.querySelectorAll("[data-en-aria]").forEach((el) => {
      if (el.dataset.frAria == null) el.dataset.frAria = el.getAttribute("aria-label");
      el.setAttribute("aria-label", T(el.dataset.frAria, el.dataset.enAria));
    });
    $("lang").value = LANG;
    const dealsPath = { fr: "/bons-plans/", en: "/en/deals/", es: "/es/ofertas/", pt: "/pt/promocoes/", ar: "/ar/deals/" }[LANG];
    document.querySelectorAll("#deals-link, .deals-href").forEach((a) => { a.href = dealsPath; });
    document.querySelectorAll(".about-href").forEach((a) => { a.href = { fr: "/a-propos/", en: "/en/about/", es: "/es/acerca-de/", pt: "/pt/sobre/", ar: "/ar/about/" }[LANG]; });
    document.querySelectorAll(".guides-href").forEach((a) => { a.href = { fr: "/guides/", en: "/en/guides/", es: "/es/guias/", pt: "/pt/guias/", ar: "/ar/guides/" }[LANG]; });
    countryNames = null;
  }

  // ---------- Devise ----------
  const CURRENCIES = ["EUR", "USD", "GBP", "CAD", "CHF", "XOF", "MAD"];
  const COUNTRY_CUR = { US: "USD", GB: "GBP", CA: "CAD", CH: "CHF", MA: "MAD",
    SN: "XOF", ML: "XOF", CI: "XOF", BF: "XOF", NE: "XOF", TG: "XOF", BJ: "XOF", GW: "XOF" };
  let CUR = store.get("escale.cur") || "EUR";
  if (!CURRENCIES.includes(CUR)) CUR = "EUR";
  const money = (n, cur) => {
    try { return new Intl.NumberFormat(locale(), { style: "currency", currency: cur || CUR, currencyDisplay: "narrowSymbol", maximumFractionDigits: 0 }).format(n); }
    catch (e) { return Math.round(n) + " " + (cur || CUR); }
  };

  // ---------- Aéroports du monde ----------
  // Liste intégrée (affichage immédiat), complétée par /data/airports.json : [code, ville, nom, pays, grand, lat, lon]
  const BUILTIN = [
    ["CDG","Paris","Charles de Gaulle","FR",1],["ORY","Paris","Orly","FR",1],["BVA","Paris-Beauvais","Beauvais","FR",0],
    ["LYS","Lyon","Saint-Exupéry","FR",1],["MRS","Marseille","Provence","FR",1],["NCE","Nice","Côte d'Azur","FR",1],
    ["BRU","Bruxelles","Brussels Airport","BE",1],["GVA","Genève","Geneva Airport","CH",1],["LHR","Londres","Heathrow","GB",1],
    ["BKO","Bamako","Modibo Keïta","ML",1],["DSS","Dakar","Blaise Diagne","SN",1],["ABJ","Abidjan","Félix-Houphouët-Boigny","CI",1],
    ["CMN","Casablanca","Mohammed V","MA",1],["ALG","Alger","Houari Boumediene","DZ",1],["TUN","Tunis","Carthage","TN",1],
    ["FIH","Kinshasa","N'djili","CD",1],["DLA","Douala","Douala","CM",1],["DXB","Dubaï","Dubai International","AE",1],
    ["IST","Istanbul","Istanbul Airport","TR",1],["JFK","New York","John F. Kennedy","US",1],["YUL","Montréal","Trudeau","CA",1]
  ];
  let DB = BUILTIN, byCode = new Map(BUILTIN.map((a) => [a[0], a])), dbLoaded = false, dbPromise = null;
  const norm = (t) => String(t || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[’'`-]/g, " ").trim();
  let countryNames = null;
  function countryName(cc) {
    try {
      if (!countryNames) countryNames = new Intl.DisplayNames([LANG], { type: "region" });
      return countryNames.of(cc) || cc;
    } catch (e) { return cc; }
  }
  const flag = (cc) => (cc && cc.length === 2 ? String.fromCodePoint(...[...cc.toUpperCase()].map((c) => 127397 + c.charCodeAt(0))) : "✈");
  let index = null; // [entrée, ville normalisée, nom normalisé]
  function buildIndex() { index = DB.map((a) => [a, norm(a[1]), norm(a[2])]); }
  function loadDB() {
    if (dbPromise) return dbPromise;
    dbPromise = fetch("/data/airports.json").then((r) => (r.ok ? r.json() : null)).then((list) => {
      if (!Array.isArray(list) || !list.length) return;
      DB = list; byCode = new Map(list.map((a) => [a[0], a])); dbLoaded = true; buildIndex();
      // Remplace les codes nus (ex. « BKO » venu d'un lien) par « Bamako (BKO) »
      document.querySelectorAll('input[data-ac="airport"]').forEach((el) => {
        if (/^[A-Z]{3}$/.test(el.value.trim()) && byCode.has(el.value.trim())) el.value = labelOf(el.value.trim());
      });
      paintDests();
    }).catch(() => {});
    return dbPromise;
  }
  buildIndex();
  const labelOf = (code) => { const a = byCode.get(code); return a ? `${a[1]} (${code})` : code; };

  function searchAirports(text, max) {
    const t = norm(text);
    if (!t) return [];
    const up = text.trim().toUpperCase();
    const out = [];
    for (const [a, city, name] of index) {
      let s = 0;
      if (a[0] === up) s = 1000;
      else if (city === t) s = 600;
      else if (city.startsWith(t)) s = 400;
      else if (name.startsWith(t)) s = 250;
      else if (t.length >= 3 && (city.includes(" " + t) || name.includes(t))) s = 120;
      else if (t.length >= 3 && norm(countryName(a[3])).startsWith(t)) s = 80;
      if (s) out.push([s + (a[4] ? 50 : 0), a]);
    }
    out.sort((x, y) => y[0] - x[0] || x[1][1].localeCompare(y[1][1]));
    return out.slice(0, max || 8).map((x) => x[1]);
  }
  function searchCities(text, max) {
    const seen = new Set(), res = [];
    for (const a of searchAirports(text, 40)) {
      const k = a[1] + "|" + a[3];
      if (seen.has(k)) continue;
      seen.add(k); res.push(a);
      if (res.length >= (max || 8)) break;
    }
    return res;
  }

  // Liste déroulante accessible (combobox) pour les champs aéroport et ville
  let acCount = 0;
  function attachAutocomplete(input) {
    const kind = input.dataset.ac;
    const wrap = input.parentElement; wrap.classList.add("ac");
    const list = document.createElement("ul");
    list.className = "ac-list"; list.id = "ac-" + (++acCount); list.setAttribute("role", "listbox"); list.hidden = true;
    wrap.appendChild(list);
    input.setAttribute("role", "combobox"); input.setAttribute("aria-autocomplete", "list");
    input.setAttribute("aria-expanded", "false"); input.setAttribute("aria-controls", list.id);
    let items = [], active = -1;
    const close = () => { list.hidden = true; input.setAttribute("aria-expanded", "false"); input.removeAttribute("aria-activedescendant"); active = -1; };
    const pick = (i) => {
      const a = items[i]; if (!a) return;
      input.value = kind === "city" ? a[1] : labelOf(a[0]);
      close();
      input.dispatchEvent(new Event("change", { bubbles: true }));
    };
    const highlight = (i) => {
      active = i;
      [...list.children].forEach((li, j) => li.setAttribute("aria-selected", String(j === i)));
      if (i >= 0) { input.setAttribute("aria-activedescendant", list.id + "-" + i); list.children[i].scrollIntoView({ block: "nearest" }); }
    };
    const render = () => {
      const v = input.value.trim();
      if (/\([A-Z]{3}\)$/.test(v) || !v) { close(); return; }
      items = kind === "city" ? searchCities(v) : searchAirports(v);
      if (!items.length) {
        list.innerHTML = `<li class="ac-empty" role="option" aria-disabled="true">${esc(dbLoaded ? T("Aucun aéroport trouvé. Essayez le nom de la ville ou le code à 3 lettres.", "No airport found. Try the city name or the 3-letter code.") : T("Chargement des aéroports du monde…", "Loading airports worldwide…"))}</li>`;
      } else {
        list.innerHTML = items.map((a, i) => kind === "city"
          ? `<li role="option" id="${list.id}-${i}" data-i="${i}"><span class="ac-flag" aria-hidden="true">${flag(a[3])}</span><span class="ac-main">${esc(a[1])}</span><span class="ac-sub">${esc(countryName(a[3]))}</span></li>`
          : `<li role="option" id="${list.id}-${i}" data-i="${i}"><span class="ac-flag" aria-hidden="true">${flag(a[3])}</span><span class="ac-main">${esc(a[1])}</span><span class="ac-code">${a[0]}</span><span class="ac-sub">${esc(a[2])} · ${esc(countryName(a[3]))}</span></li>`).join("");
      }
      list.hidden = false; input.setAttribute("aria-expanded", "true"); active = -1;
    };
    input.addEventListener("focus", () => { loadDB().then(() => { if (document.activeElement === input && input.value.trim() && !/\([A-Z]{3}\)$/.test(input.value)) render(); }); });
    input.addEventListener("input", () => { render(); if (!dbLoaded) loadDB().then(() => { if (document.activeElement === input) render(); }); });
    input.addEventListener("keydown", (ev) => {
      if (list.hidden) { if (ev.key === "ArrowDown") render(); return; }
      if (ev.key === "ArrowDown") { ev.preventDefault(); highlight(Math.min(items.length - 1, active + 1)); }
      else if (ev.key === "ArrowUp") { ev.preventDefault(); highlight(Math.max(0, active - 1)); }
      else if (ev.key === "Enter" && items.length) { ev.preventDefault(); pick(active >= 0 ? active : 0); }
      else if (ev.key === "Escape") close();
    });
    input.addEventListener("blur", () => setTimeout(close, 120));
    list.addEventListener("mousedown", (ev) => { const li = ev.target.closest("li[data-i]"); if (li) { ev.preventDefault(); pick(+li.dataset.i); } });
  }
  document.querySelectorAll("input[data-ac]").forEach(attachAutocomplete);

  // « Paris (CDG) », « CDG » ou « Bamako » -> { code, name }
  function place(raw) {
    const v = (raw || "").trim();
    if (!v) return null;
    const m = v.match(/\(([A-Za-z]{3})\)\s*$/) || v.match(/^([A-Za-z]{3})$/);
    if (m) {
      const code = m[1].toUpperCase(), a = byCode.get(code);
      return { code, name: a ? a[1] : code, cc: a ? a[3] : null };
    }
    const hit = searchAirports(v, 1)[0];
    if (hit && norm(hit[1]) === norm(v)) return { code: hit[0], name: hit[1], cc: hit[3] };
    return { code: null, name: v, cc: null };
  }

  // ---------- Champs : valeurs par défaut ----------
  const fill = (sel, from, to, def, fmt) => { for (let i = from; i <= to; i++) { const o = new Option(fmt ? fmt(i) : String(i), String(i)); if (i === def) o.selected = true; sel.add(o); } };
  fill($("f-adults"), 1, 9, 1); fill($("f-children"), 0, 8, 0);
  fill($("h-adults"), 1, 10, 2); fill($("h-rooms"), 1, 5, 1);
  fill($("c-t1"), 6, 22, 10, (h) => String(h).padStart(2, "0") + ":00");
  fill($("c-t2"), 6, 22, 10, (h) => String(h).padStart(2, "0") + ":00");

  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const parse = (s) => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
  const addDays = (s, n) => { const d = parse(s); d.setDate(d.getDate() + n); return iso(d); };
  const today = iso(new Date());
  const nights = (a, b) => Math.round((parse(b) - parse(a)) / 86400000);
  const human = (s) => parse(s).toLocaleDateString(locale(), { weekday: "short", day: "numeric", month: "short" });
  const short = (s) => parse(s).toLocaleDateString(locale(), { day: "numeric", month: "short" });
  const yymmdd = (s) => s.slice(2).replace(/-/g, "");

  [["f-dep", 21], ["f-ret", 28], ["h-in", 21], ["h-out", 25], ["c-d1", 21], ["c-d2", 28]].forEach(([id, n]) => {
    $(id).value = addDays(today, n); $(id).min = today;
  });
  // Recherche par mois : 12 prochains mois, durée du séjour en nuits
  function paintMonthOptions() {
    const keep = $("f-month").value, keepStay = $("f-stay").value || "7";
    $("f-month").innerHTML = Array.from({ length: 12 }, (_, i) => { const d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + i); return iso(d).slice(0, 7); })
      .map((m) => `<option value="${m}">${esc(parse(m + "-01").toLocaleDateString(locale(), { month: "long", year: "numeric" }))}</option>`).join("");
    if (keep) $("f-month").value = keep; else $("f-month").selectedIndex = 1;
    $("f-stay").innerHTML = [3, 5, 7, 10, 14, 21, 28].map((n) => `<option value="${n}">${esc(fmt(T("{n} nuits", "{n} nights"), { n }))}</option>`).join("");
    $("f-stay").value = keepStay;
  }
  paintMonthOptions();
  const DEFAULT_FROM = "Paris (CDG)";
  $("f-from").value = store.get("escale.from") || DEFAULT_FROM;
  $("f-to").value = "Bamako (BKO)";
  $("h-dest").value = "Dakar";
  $("c-pick").value = "Casablanca (CMN)";
  const link = (a, b, gap) => $(a).addEventListener("change", () => {
    $(b).min = $(a).value;
    if (!$(b).value || $(b).value <= $(a).value) $(b).value = addDays($(a).value, gap);
  });
  link("f-dep", "f-ret", 7); link("h-in", "h-out", 3); link("c-d1", "c-d2", 7);

  // ---------- Sites comparés ----------
  const COLORS = { google: "#1a73e8", sky: "#0062e3", kayak: "#ff690f", momondo: "#d1006e", booking: "#003580",
    hotels: "#d32f2f", agoda: "#5c2d91", airbnb: "#e0475b", rental: "#00897b", discover: "#2e7d32", aviasales: "#0c73fe" };
  const SITES = {
    fr: { kayak: "www.kayak.fr", momondo: "www.momondo.fr", sky: "www.skyscanner.fr/transport/vols", booking: "searchresults.fr.html",
          hotels: "fr.hotels.com", agoda: "fr-fr", airbnb: "www.airbnb.fr", rental: "fr", discover: "fr" },
    en: { kayak: "www.kayak.com", momondo: "www.momondo.com", sky: "www.skyscanner.net/transport/flights", booking: "searchresults.en-gb.html",
          hotels: "www.hotels.com", agoda: "en-gb", airbnb: "www.airbnb.com", rental: "en", discover: "" },
    es: { kayak: "www.kayak.es", momondo: "www.momondo.es", sky: "www.skyscanner.net/transport/flights", booking: "searchresults.es.html",
          hotels: "es.hotels.com", agoda: "es-es", airbnb: "www.airbnb.es", rental: "es", discover: "es" },
    pt: { kayak: "www.kayak.com", momondo: "www.momondo.com", sky: "www.skyscanner.net/transport/flights", booking: "searchresults.pt-pt.html",
          hotels: "www.hotels.com", agoda: "pt-pt", airbnb: "www.airbnb.pt", rental: "pt", discover: "pt" },
    ar: { kayak: "www.kayak.com", momondo: "www.momondo.com", sky: "www.skyscanner.net/transport/flights", booking: "searchresults.ar.html",
          hotels: "www.hotels.com", agoda: "ar-ae", airbnb: "www.airbnb.com", rental: "en", discover: "" }
  };
  const D = () => SITES[LANG];

  function flightLinks(s) {
    const d = D();
    const F = s.from.code.toLowerCase(), Tt = s.to && s.to.code ? s.to.code.toLowerCase() : null;
    const cabinSky = { economy: "economy", premium: "premiumeconomy", business: "business", first: "first" }[s.cabin];
    const cabinKayak = { economy: "", premium: "/premium", business: "/business", first: "/first" }[s.cabin];
    const cabinG = { economy: "", premium: " premium economy", business: " business class", first: " first class" }[s.cabin];
    const pax = s.adults > 1 ? `/${s.adults}adults` : "";
    const kids = s.children > 0 ? "/children" + "-11".repeat(s.children) : "";
    const flex = s.flex ? "-flexible-3days" : "";
    const kDates = `/${s.dep}${flex}` + (s.ret ? `/${s.ret}${flex}` : "");
    const kParams = "?" + q({ sort: "price_a", fs: s.direct ? "stops=0" : "" });
    const list = [];
    if (!Tt) {
      list.push({ k: "google", name: "Google Flights Explore", desc: T("Carte des destinations les moins chères depuis votre aéroport.", "Map of the cheapest destinations from your airport."), best: true,
        url: `https://www.google.com/travel/explore?${q({ q: `Flights from ${s.from.code}`, hl: LANG, curr: CUR })}` });
      list.push({ k: "sky", name: T("Skyscanner « Partout »", "Skyscanner “Everywhere”"), desc: T("Toutes les destinations triées par prix.", "Every destination sorted by price."),
        url: `https://${d.sky}/${F}/anywhere/${yymmdd(s.dep)}/` + (s.ret ? `${yymmdd(s.ret)}/` : "") + "?" + q({ adultsv2: s.adults, cabinclass: cabinSky, rtn: s.ret ? 1 : 0 }) });
      list.push({ k: "kayak", name: "Kayak Explore", desc: T("Destinations selon votre budget et vos dates.", "Destinations by budget and dates."),
        url: `https://${d.kayak}/explore/${s.from.code}-anywhere` });
      return list;
    }
    const gq = `Flights to ${s.to.code} from ${s.from.code} on ${s.dep}` + (s.ret ? ` through ${s.ret}` : " one way") +
      (s.adults > 1 ? ` ${s.adults} adults` : "") + (s.children ? ` ${s.children} children` : "") + cabinG + (s.direct ? " nonstop" : "");
    list.push({ k: "google", name: "Google Flights", desc: T("Graphique et calendrier des prix pour repérer le jour le moins cher.", "Price graph and calendar to spot the cheapest day."), best: true,
      url: `https://www.google.com/travel/flights?${q({ q: gq, hl: LANG, curr: CUR })}` });
    list.push({ k: "sky", name: "Skyscanner", desc: T("Très bon sur les compagnies low-cost et les agences en ligne.", "Great for low-cost airlines and online agencies."), best: true,
      url: `https://${d.sky}/${F}/${Tt}/${yymmdd(s.dep)}/` + (s.ret ? `${yymmdd(s.ret)}/` : "") + "?" +
        q({ adultsv2: s.adults, childrenv2: s.children ? Array(s.children).fill(8).join("|") : "", cabinclass: cabinSky,
            rtn: s.ret ? 1 : 0, preferdirects: s.direct ? "true" : "", sortby: "cheapest" }) });
    list.push({ k: "kayak", name: "Kayak", desc: s.flex ? T("Recherche ±3 jours autour de vos dates, triée par prix.", "Searches ±3 days around your dates, sorted by price.") : T("Compare des centaines de sites, tri par prix.", "Compares hundreds of sites, sorted by price."),
      url: `https://${d.kayak}/flights/${s.from.code}-${s.to.code}${kDates}${cabinKayak}${pax}${kids}${kParams}` });
    if (AFFILIATE.travelpayouts_marker) {
      const ddmm = (x) => x.slice(8, 10) + x.slice(5, 7);
      const paxAv = String(s.adults) + (s.children ? String(s.children) : "");
      list.push({ k: "aviasales", name: "Aviasales", desc: T("Compare des centaines de compagnies et d’agences, souvent très bon sur les vols avec escale.", "Compares hundreds of airlines and agencies, often great for flights with stops."),
        url: `https://www.aviasales.com/search/${s.from.code}${ddmm(s.dep)}${s.to.code}${s.ret ? ddmm(s.ret) : ""}${paxAv}?` + q({ marker: AFFILIATE.travelpayouts_marker, currency: CUR.toLowerCase() }) });
    }
    list.push({ k: "momondo", name: "momondo", desc: T("Souvent des tarifs d’agences que les autres n’affichent pas.", "Often shows agency fares others don’t."),
      url: `https://${d.momondo}/flight-search/${s.from.code}-${s.to.code}${kDates}${cabinKayak}${pax}${kids}${kParams}` });
    return list;
  }

  function hotelLinks(s) {
    const d = D(), x = s.dest;
    return [
      { k: "booking", name: "Booking.com", desc: T("Le plus grand choix d’hébergements, souvent annulables gratuitement.", "The widest choice of stays, often with free cancellation."), best: true,
        url: `https://www.booking.com/${d.booking}?${q({ ss: x, checkin: s.in, checkout: s.out, group_adults: s.adults, no_rooms: s.rooms, group_children: 0, order: "price", selected_currency: CUR })}` },
      { k: "google", name: T("Google Hôtels", "Google Hotels"), desc: T("Compare les prix de plusieurs agences pour le même hôtel.", "Compares prices from several agencies for the same hotel."), best: true,
        url: `https://www.google.com/travel/search?${q({ q: T(`hôtels ${x} du ${s.in} au ${s.out}`, `hotels in ${x} from ${s.in} to ${s.out}`), hl: LANG, curr: CUR })}` },
      { k: "kayak", name: T("Kayak Hôtels", "Kayak Hotels"), desc: T("Agrège Booking, Expedia, Hotels.com et d’autres, tri par prix.", "Aggregates Booking, Expedia, Hotels.com and more, sorted by price."),
        url: `https://${d.kayak}/hotels/${enc(x)}/${s.in}/${s.out}/${s.adults}adults` + (s.rooms > 1 ? `/${s.rooms}rooms` : "") + "?sort=price_a" },
      { k: "hotels", name: "Hotels.com", desc: T("Programme de fidélité : des nuits offertes après plusieurs séjours.", "Loyalty programme: free nights after several stays."),
        url: `https://${d.hotels}/Hotel-Search?${q({ destination: x, startDate: s.in, endDate: s.out, adults: s.adults, rooms: s.rooms, sort: "PRICE_LOW_TO_HIGH" })}` },
      { k: "agoda", name: "Agoda", desc: T("Souvent le moins cher en Asie, en Afrique et au Moyen-Orient.", "Often cheapest in Asia, Africa and the Middle East."),
        url: `https://www.agoda.com/${d.agoda}/search?${q({ textToSearch: x, checkIn: s.in, checkOut: s.out, adults: s.adults, rooms: s.rooms, sort: "priceLowToHigh" })}` },
      { k: "airbnb", name: "Airbnb", desc: T("Appartements et maisons, intéressant pour les familles et les longs séjours.", "Apartments and homes, good for families and long stays."),
        url: `https://${d.airbnb}/s/${enc(x)}/homes?${q({ checkin: s.in, checkout: s.out, adults: s.adults })}` }
    ];
  }

  function carLinks(s) {
    const d = D();
    const P = s.pick.code || s.pick.name, Dr = s.drop ? (s.drop.code || s.drop.name) : null;
    const h = (n) => String(n).padStart(2, "0") + "h";
    const path = `${enc(P)}` + (Dr ? `/${enc(Dr)}` : "") + `/${s.d1}-${h(s.t1)}/${s.d2}-${h(s.t2)}`;
    return [
      { k: "kayak", name: T("Kayak Voitures", "Kayak Cars"), desc: T("Compare les loueurs et les courtiers, tri par prix.", "Compares rental companies and brokers, sorted by price."), best: true,
        url: `https://${d.kayak}/cars/${path}?sort=price_a` },
      { k: "momondo", name: T("momondo Voitures", "momondo Cars"), desc: T("Bon complément de Kayak, avec d’autres partenaires.", "A good complement to Kayak, with other partners."),
        url: `https://${d.momondo}/carsearch/${path}?sort=price_a` },
      { k: "google", name: T("Recherche Google", "Google search"), desc: T("Loueurs locaux et agences indépendantes, souvent moins chers hors aéroport.", "Local and independent agencies, often cheaper away from the airport."),
        url: `https://www.google.com/search?${q({ q: T(`location voiture pas cher ${s.pick.name} ${s.d1}`, `cheap car rental ${s.pick.name} ${s.d1}`), hl: LANG })}` },
      { k: "rental", name: "Rentalcars", desc: T("Courtier connu, assurance « franchise zéro » proposée.", "Well-known broker with full-protection cover."), manual: true,
        url: `https://www.rentalcars.com/${d.rental}/` },
      { k: "discover", name: "Discover Cars", desc: T("Souvent bien placé sur les petites agences locales.", "Often strong on small local agencies."), manual: true,
        url: `https://www.discovercars.com/${d.discover}` }
    ];
  }

  // ---------- Affichage des résultats ----------
  function providerList(items) {
    return `<ul class="providers">` + items.map((p, i) => `
      <li class="prov" style="--i:${i}">
        <span class="logo" style="background:${COLORS[p.k]}" aria-hidden="true">${esc(p.name[0].toUpperCase())}</span>
        <div class="prov-body">
          <div class="prov-name">${esc(p.name)}${p.best ? ` <span class="pill best">${T("Recommandé", "Recommended")}</span>` : ""}${p.manual ? ` <span class="pill manual">${T("Saisie sur le site", "Enter on site")}</span>` : ""}</div>
          <div class="prov-desc">${esc(p.desc)}</div>
        </div>
        <a class="go" href="${esc(tag(p.k, p.url))}" target="_blank" rel="noopener noreferrer">${T("Voir les prix", "See prices")} →</a>
      </li>`).join("") + `</ul>`;
  }
  function pass(codes, meta, stubBig, stubSmall) {
    return `<div class="pass"><div class="pass-main"><div class="pass-codes" dir="ltr">${codes}</div>${meta.map(([l, v]) =>
      `<div class="pass-meta"><span>${esc(l)}</span><strong>${esc(v)}</strong></div>`).join("")}</div>
      <div class="pass-stub"><b>${esc(stubBig)}</b>${esc(stubSmall)}</div></div>`;
  }
  let booting = true;
  function show(html) {
    const r = $("results"); r.innerHTML = html;
    if (!booting) r.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
  }
  const stopsText = (n) => n === 0 ? T("vol direct", "direct") : n === 1 ? T("1 escale", "1 stop") : fmt(T("{n} escales", "{n} stops"), { n });

  function renderFlights(s) {
    const toCode = s.to && s.to.code ? s.to.code : "ANY";
    const pax = s.adults + s.children;
    const head = `<div class="results-head"><h2><bdi dir="ltr">${esc(s.from.name)} → ${esc(s.to ? s.to.name : T("Partout", "Anywhere"))}</bdi></h2>
      <span class="summary">${T("Ouvrez 2 ou 3 sites et comparez le prix final", "Open 2 or 3 sites and compare the final price")}</span></div>`;
    const card = pass(`${esc(s.from.code)} <small>→</small> ${esc(toCode)}`,
      [[T("Aller", "Depart"), human(s.dep)], [T("Retour", "Return"), s.ret ? human(s.ret) : T("Aller simple", "One way")],
       [T("Voyageurs", "Travellers"), `${pax} · ${$("f-cabin").selectedOptions[0].text}`]],
      s.ret ? `${nights(s.dep, s.ret)} ${T("J", "D")}` : T("1 VOL", "1 WAY"), s.ret ? T("séjour", "trip") : T("aller simple", "one way"));
    let flexHtml = "";
    if (s.flex && s.to && s.to.code) {
      const len = s.ret ? nights(s.dep, s.ret) : 0;
      const cells = [-3, -2, -1, 0, 1, 2, 3].map((o) => {
        const d = addDays(s.dep, o);
        if (d < today) return "";
        const r = s.ret ? addDays(d, len) : null;
        const u = flightLinks({ ...s, dep: d, ret: r, flex: false })[0].url;
        return `<a href="${esc(u)}" target="_blank" rel="noopener noreferrer" class="${o === 0 ? "cur" : ""}"><small>${o === 0 ? T("Vos dates", "Your dates") : (o > 0 ? "+" : "") + o + T(" j", " d")}</small><strong>${esc(human(d))}</strong></a>`;
      }).join("");
      flexHtml = `<h3 class="sub-h">${T("Comparer jour par jour sur Google Flights", "Compare day by day on Google Flights")}</h3><div class="flex-grid">${cells}</div>`;
    }
    const priceSlot = isLive && s.to && s.to.code ? '<div class="price-hint" id="price-hint" hidden></div>' : "";
    const anywhere = !s.to ? `<h3 class="sub-h">${T("Destinations les moins chères repérées", "Cheapest destinations found")}</h3><div class="ex-grid" id="res-explore"></div>` : "";
    const extras = s.to && s.to.code ? extrasSlot(s.to.name) : "";
    show(head + card + priceSlot + shareBar("vols", fmt(T("Vols {a} → {b}", "Flights {a} → {b}"), { a: s.from.name, b: s.to ? s.to.name : T("partout", "anywhere") })) + providerList(flightLinks(s)) + flexHtml + anywhere + extras);
    if (extras) fillExtras(s.to.name, s.to.code);
    if (priceSlot) loadPrice(s);
    if (!s.to) renderExplore($("res-explore"), s.from.code, s.dep.slice(0, 7));
  }
  let priceReq = 0;
  async function loadPrice(s) {
    const id = ++priceReq;
    try {
      const r = await fetch("/api/prix?" + q({ from: s.from.code, to: s.to.code, dep: s.dep, ret: s.ret || "", currency: CUR }));
      if (!r.ok || id !== priceReq) return;
      const d = await r.json();
      const box = $("price-hint");
      if (!d.available || !d.price || !box) return;
      const month = parse(s.dep).toLocaleDateString(locale(), { month: "long" });
      box.innerHTML = fmt(T("Prix repéré récemment pour {month} : <strong>dès {price}</strong> ({stops}, {kind}). Le tarif exact et disponible s’affiche sur les sites ci-dessous.",
        "Recently found for {month}: <strong>from {price}</strong> ({stops}, {kind}). The exact available fare is shown on the sites below."),
        { month: esc(month), price: esc(money(d.price, d.currency)), stops: esc(stopsText(d.transfers)), kind: s.ret ? T("aller-retour", "round trip") : T("aller simple", "one way") });
      box.hidden = false;
    } catch (e) { /* prix indisponibles : rien n'est affiché */ }
  }
  function renderHotels(s) {
    const n = nights(s.in, s.out);
    show(`<div class="results-head"><h2>${T("Hôtels à", "Hotels in")} ${esc(s.dest)}</h2><span class="summary">${T("Tri du moins cher au plus cher", "Sorted from cheapest")}</span></div>` +
      pass(`${esc(s.dest.slice(0, 3).toUpperCase())}`, [[T("Arrivée", "Check-in"), human(s.in)], [T("Départ", "Check-out"), human(s.out)],
        [T("Voyageurs", "Guests"), `${s.adults} ${s.adults > 1 ? T("adultes", "adults") : T("adulte", "adult")} · ${s.rooms} ${T("ch.", "rm")}`]],
        `${n} ${T("N", "N")}`, n > 1 ? T("nuits", "nights") : T("nuit", "night")) +
      shareBar("hotels", fmt(T("Hôtels à {c}", "Hotels in {c}"), { c: s.dest })) + providerList(hotelLinks(s)) + extrasSlot(s.dest));
    fillExtras(s.dest, "");
  }
  function renderCars(s) {
    const days = Math.max(1, Math.ceil(nights(s.d1, s.d2) + (s.t2 > s.t1 ? 1 : 0)));
    const code = s.pick.code || s.pick.name.slice(0, 3).toUpperCase();
    show(`<div class="results-head"><h2>${T("Location à", "Car rental in")} ${esc(s.pick.name)}</h2><span class="summary">${T("Vérifiez franchise et politique carburant", "Check the excess and fuel policy")}</span></div>` +
      pass(`${esc(code)}${s.drop ? ` <small>→</small> ${esc(s.drop.code || s.drop.name.slice(0, 3).toUpperCase())}` : ""}`,
        [[T("Prise en charge", "Pick-up"), `${human(s.d1)} · ${s.t1}h`], [T("Restitution", "Drop-off"), `${human(s.d2)} · ${s.t2}h`], [T("Conducteur", "Driver"), $("c-age").selectedOptions[0].text]],
        `${days} ${T("J", "D")}`, T("de location", "rental")) +
      shareBar("voitures", fmt(T("Location de voiture à {c}", "Car rental in {c}"), { c: s.pick.name })) + providerList(carLinks(s)));
  }

  // ---------- Avant de partir (eSIM, assurance, transfert, activités) : liens réglés dans /data/partners.json ----------
  let partnersP = null;
  const extrasSlot = (city) => `<div id="res-extras-wrap"><h3 class="sub-h">${esc(T("Avant de partir", "Before you go"))}</h3>
    <p class="summary">${esc(fmt(T("Les services utiles pour votre voyage à {c}.", "Useful services for your trip to {c}."), { c: city }))}</p>
    <ul class="extras-res providers" id="res-extras"></ul></div>`;
  function fillExtras(city, code) {
    if (!partnersP) partnersP = fetch("/data/partners.json").then((r) => (r.ok ? r.json() : null)).catch(() => null);
    partnersP.then((cfg) => {
      const ul = $("res-extras");
      if (!ul) return;
      if (!cfg) { $("res-extras-wrap").remove(); return; }
      ul.innerHTML = cfg.services.map((p, i) => {
        const url = p.url.replace("{city}", enc(city)).replace("{code}", code || "");
        return `<li class="extra prov" style="--i:${i}"><span class="logo" style="background:${esc(p.color)}" aria-hidden="true">${esc(p.name[0])}</span>
          <div><strong>${esc(p.title[LANG] || p.title.en)}</strong><span>${esc(p.desc[LANG] || p.desc.en)}</span></div>
          <a class="go" href="${esc(url)}" target="_blank" rel="sponsored noopener noreferrer">${esc(T("Voir l’offre", "See offer"))} · ${esc(p.name)}</a></li>`;
      }).join("");
    });
  }

  // ---------- Recherche par mois : calendrier des prix dans les résultats ----------
  let monthReq = 0;
  function renderMonth(s) {
    const d = D(), [y, mo] = s.month.split("-").map(Number);
    const monthName = parse(s.month + "-01").toLocaleDateString(locale(), { month: "long", year: "numeric" });
    const yymm = s.month.slice(2).replace("-", "");
    const retMonth = (() => { const x = new Date(y, mo - 1, 1); x.setDate(x.getDate() + 32); return iso(x).slice(2, 7).replace("-", ""); })();
    const sky = `https://${d.sky}/${s.from.code.toLowerCase()}/${s.to.code.toLowerCase()}/${yymm}/` + (s.ow ? "" : `${s.stay > 20 ? retMonth : yymm}/`) + "?" + q({ adultsv2: s.adults, rtn: s.ow ? 0 : 1 });
    const gf = `https://www.google.com/travel/flights?${q({ q: `Flights from ${s.from.code} to ${s.to.code} in ${parse(s.month + "-01").toLocaleDateString("en-GB", { month: "long", year: "numeric" })}`, hl: LANG, curr: CUR })}`;
    const head = `<div class="results-head"><h2><bdi dir="ltr">${esc(s.from.name)} → ${esc(s.to.name)}</bdi> · ${esc(monthName)}</h2>
      <span class="summary">${esc(fmt(T("Séjour de {n} nuits · cliquez sur un jour pour lancer la recherche", "{n}-night trip · click a day to search"), { n: s.stay || 1 }))}</span></div>`;
    const links = providerList([
      { k: "sky", name: T("Skyscanner : le mois entier", "Skyscanner: whole month"), desc: T("Vue du mois avec le prix de chaque jour.", "Month view with the price of each day."), best: true, url: sky },
      { k: "google", name: "Google Flights", desc: T("Graphique des prix sur le mois.", "Price graph for the month."), url: gf }
    ]);
    show(head + `<div id="month-cal"><p class="lead">${esc(T("Chargement des prix du mois…", "Loading prices for the month…"))}</p></div>` + links);
    const id = ++monthReq;
    if (!isLive) { $("month-cal").innerHTML = ""; return; }
    fetch("/api/calendar?" + q({ from: s.from.code, to: s.to.code, month: s.month, currency: CUR })).then((r) => (r.ok ? r.json() : null)).catch(() => null).then((data) => {
      if (id !== monthReq || !$("month-cal")) return;
      const days = data && data.available ? data.days || {} : {};
      const keys = Object.keys(days).filter((k) => k >= today);
      if (!keys.length) { $("month-cal").innerHTML = `<p class="lead">${esc(T("Pas encore de prix connus pour ce mois. Utilisez les liens ci-dessous.", "No known prices for this month yet. Use the links below."))}</p>`; return; }
      const prices = keys.map((k) => days[k].price), min = Math.min(...prices), max = Math.max(...prices);
      const first = new Date(y, mo - 1, 1), nDays = new Date(y, mo, 0).getDate(), offset = (first.getDay() + 6) % 7;
      const cells = [];
      for (let i = 0; i < 7; i++) cells.push(`<span class="cal-head" aria-hidden="true">${esc(new Date(2024, 0, 1 + i).toLocaleDateString(locale(), { weekday: "narrow" }))}</span>`);
      for (let k = 0; k < offset; k++) cells.push("<span></span>");
      for (let dd = 1; dd <= nDays; dd++) {
        const day = `${s.month}-${String(dd).padStart(2, "0")}`, info = days[day];
        if (day < today || !info) { cells.push(`<span class="cal-day off"><b>${dd}</b></span>`); continue; }
        const tier = max > min ? Math.min(4, Math.floor(((info.price - min) / (max - min)) * 5)) : 0;
        const p = money(info.price, data.currency);
        cells.push(`<button type="button" class="cal-day t${tier}" data-day="${day}" title="${esc(p + " · " + stopsText(info.transfers))}" aria-label="${esc(short(day) + " : " + p)}"><b>${dd}</b><span>${esc(String(Math.round(info.price)))}</span></button>`);
      }
      $("month-cal").innerHTML = `<h3 class="sub-h">${esc(fmt(T("Jours les moins chers en {m}", "Cheapest days in {m}"), { m: monthName }))}</h3>
        <div class="cal-grid" dir="ltr">${cells.join("")}</div>
        <p class="summary">${esc(T("Moins cher", "Cheaper"))} <span class="cal-scale" aria-hidden="true"><i class="t0"></i><i class="t1"></i><i class="t2"></i><i class="t3"></i><i class="t4"></i></span> ${esc(T("Plus cher", "More expensive"))} · ${esc(money(min, data.currency))} – ${esc(money(max, data.currency))}</p>`;
      $("month-cal").onclick = (ev) => {
        const b = ev.target.closest("button[data-day]"); if (!b) return;
        $("f-monthmode").checked = false;
        $("f-dep").value = b.dataset.day;
        if (!s.ow) { $("trip-rt").checked = true; $("f-ret").value = addDays(b.dataset.day, s.stay); }
        syncTrip();
        $("form-vols").requestSubmit();
      };
    });
  }

  // ---------- Filtre de budget sur les idées de voyage ----------
  function setupBudget(items, currency) {
    const box = $("ex-budget"), range = $("ex-max");
    if (!items.length) { box.hidden = true; return; }
    const prices = items.map((it) => Math.round(it.price)), min = Math.min(...prices), max = Math.max(...prices);
    if (max <= min) { box.hidden = true; return; }
    range.min = String(min); range.max = String(max); range.step = "1";
    range.value = String(max);
    const apply = () => {
      const v = +range.value;
      let n = 0;
      $("ex-grid").querySelectorAll(".ex-card").forEach((c) => { const ok = +c.dataset.price <= v; c.hidden = !ok; if (ok) n++; });
      $("ex-max-out").textContent = `${money(v, currency)} · ${fmt(T("{n} destinations", "{n} destinations"), { n })}`;
    };
    range.oninput = apply;
    apply();
    box.hidden = false;
  }

  // ---------- Calculateur du vrai prix ----------
  function calc() {
    const pax = Math.max(1, +$("calc-pax").value || 1), need = Math.max(0, +$("calc-bags").value || 0);
    const totals = ["a", "b", "c"].map((k) => {
      const price = $(`calc-${k}-price`).value;
      if (price === "") return null;
      const incl = +$(`calc-${k}-incl`).value || 0, bag = +$(`calc-${k}-bag`).value || 0, fees = +$(`calc-${k}-fees`).value || 0;
      return (+price + fees + Math.max(0, need - incl) * bag) * pax;
    });
    const valid = totals.filter((t) => t != null), best = valid.length ? Math.min(...valid) : null;
    ["a", "b", "c"].forEach((k, i) => {
      const o = $(`calc-${k}-out`), t = totals[i];
      o.textContent = t == null ? "–" : money(t);
      o.classList.toggle("best", t != null && valid.length > 1 && t === best);
    });
    if (valid.length > 1) {
      const order = totals.map((t, i) => [t, "ABC"[i]]).filter((x) => x[0] != null).sort((x, y) => x[0] - y[0]);
      $("calc-verdict").textContent = fmt(T("L’offre {w} est la moins chère : {d} d’économie sur l’offre {l}.", "Offer {w} is the cheapest: {d} less than offer {l}."),
        { w: order[0][1], l: order[order.length - 1][1], d: money(order[order.length - 1][0] - order[0][0]) });
    } else $("calc-verdict").textContent = "";
  }
  $("calc").addEventListener("input", calc);
  $("calc").addEventListener("submit", (ev) => ev.preventDefault());
  calc();

  // ---------- Idées de voyage (prix réels) ----------
  const exploreCache = new Map();
  function fetchExplore(from, month) {
    const key = from + month + CUR;
    if (!exploreCache.has(key)) {
      exploreCache.set(key, fetch("/api/explore?" + q({ from, month, currency: CUR }))
        .then((r) => (r.ok ? r.json() : null)).catch(() => null));
    }
    return exploreCache.get(key);
  }
  async function renderExplore(grid, from, month) {
    if (!grid) return false;
    if (!isLive) { grid.innerHTML = ""; return false; }
    grid.innerHTML = Array(8).fill('<div class="ex-skel"></div>').join("");
    const [data] = await Promise.all([fetchExplore(from, month), loadDB()]);
    const items = data && data.available && Array.isArray(data.items) ? data.items.filter((it) => it.departure_at && it.departure_at.slice(0, 10) >= today) : [];
    if (!items.length) {
      if (grid.id === "ex-grid") $("ex-budget").hidden = true;
      grid.innerHTML = `<p class="lead" style="grid-column:1/-1">${T("Pas encore de prix repérés pour ce mois. Essayez un autre mois ou les liens ci-dessus.", "No prices found yet for this month. Try another month or the links above.")}</p>`;
      return false;
    }
    grid.innerHTML = items.slice(0, 16).map((it, i) => {
      const a = byCode.get(it.to) || byCode.get(it.city_code);
      const city = a ? a[1] : it.to, cc = a ? a[3] : "";
      const dep = it.departure_at.slice(0, 10), ret = it.return_at ? it.return_at.slice(0, 10) : "";
      return `<button type="button" class="ex-card" style="--i:${i}" data-price="${Math.round(it.price)}" data-to="${esc(a ? a[0] : it.to)}" data-dep="${dep}" data-ret="${ret}" data-from="${esc(from)}">
        <span class="ex-top"><span aria-hidden="true">${flag(cc)}</span><b>${esc(a ? a[0] : it.to)}</b></span>
        <span class="ex-name">${esc(city)}</span>
        <span class="ex-meta">${esc(cc ? countryName(cc) : "")}${ret ? ` · ${esc(short(dep))} → ${esc(short(ret))}` : ""} · ${esc(stopsText(it.transfers))}</span>
        <span class="ex-price">${T("dès", "from")} ${esc(money(it.price, data.currency))}</span>
      </button>`;
    }).join("");
    if (grid.id === "ex-grid") { feedFlap(from, items); setupBudget(items.slice(0, 16), data.currency); }
    return true;
  }
  document.addEventListener("click", (ev) => {
    const c = ev.target.closest(".ex-card"); if (!c) return;
    selectTab("vols");
    $("f-from").value = labelOf(c.dataset.from);
    $("f-to").value = labelOf(c.dataset.to);
    if (c.dataset.ret) { $("trip-rt").checked = true; $("f-ret").value = c.dataset.ret; } else { $("trip-ow").checked = true; }
    $("f-dep").value = c.dataset.dep; syncTrip();
    $("form-vols").requestSubmit();
  });
  const monthsAhead = () => [0, 1, 2].map((i) => { const d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + i); return iso(d).slice(0, 7); });
  let exploreFrom = null, exploreMonth = null;
  function paintExploreMonths() {
    $("ex-months").innerHTML = monthsAhead().map((m) => `<button type="button" data-m="${m}" aria-pressed="${m === exploreMonth}">${esc(parse(m + "-01").toLocaleDateString(locale(), { month: "long" }))}</button>`).join("");
  }
  async function showHomeExplore(from) {
    if (!isLive || !from) return;
    exploreFrom = from; exploreMonth = exploreMonth || monthsAhead()[1];
    await loadDB();
    const a = byCode.get(from);
    $("ex-city").textContent = a ? a[1] : from;
    paintExploreMonths();
    $("explore").hidden = false;
    const ok = await renderExplore($("ex-grid"), from, exploreMonth);
    if (!ok && exploreMonth === monthsAhead()[1]) { /* garde la section visible avec son message */ }
  }
  $("ex-months").addEventListener("click", (ev) => {
    const b = ev.target.closest("button[data-m]"); if (!b) return;
    exploreMonth = b.dataset.m; paintExploreMonths();
    renderExplore($("ex-grid"), exploreFrom, exploreMonth);
  });

  // ---------- Panneau des départs (lettres qui basculent) ----------
  const FLAP_LEN = 22;
  let flapRows = [["CDG", "BKO"], ["ORY", "DSS"], ["BRU", "ABJ"], ["LYS", "CMN"], ["CDG", "JFK"], ["GVA", "DXB"]].map(([a, b]) => `${a} → ${b}`);
  let flapIdx = 0, flapTimer = null;
  function setFlap(text) {
    const el = $("flap"); const t = text.padEnd(FLAP_LEN).slice(0, FLAP_LEN);
    if (el.children.length !== FLAP_LEN) el.innerHTML = Array(FLAP_LEN).fill("<i></i>").join("");
    [...t].forEach((ch, i) => {
      const cell = el.children[i];
      if (cell.textContent === ch) return;
      // Les 9 premiers caractères forment le trajet (« CDG → BKO ») ; la suite (le prix) est surlignée
      const apply = () => { cell.textContent = ch; cell.className = ch === " " ? "sp" : i >= 10 ? "hl" : ""; };
      if (reduceMotion) { apply(); return; }
      setTimeout(() => { cell.classList.remove("flip"); void cell.offsetWidth; cell.classList.add("flip"); setTimeout(apply, 140); }, i * 28);
    });
  }
  function startFlap() {
    setFlap(flapRows[0]);
    clearInterval(flapTimer);
    flapTimer = setInterval(() => { if (document.hidden) return; flapIdx = (flapIdx + 1) % flapRows.length; setFlap(flapRows[flapIdx]); }, 3600);
  }
  function feedFlap(from, items) {
    const rows = items.slice(0, 8).map((it) => {
      // Panneau en caractères latins quelle que soit la langue
      let p;
      try { p = new Intl.NumberFormat("en", { style: "currency", currency: CUR, currencyDisplay: "narrowSymbol", maximumFractionDigits: 0 }).format(it.price).replace(/\s/g, ""); }
      catch (e) { p = Math.round(it.price) + CUR; }
      return `${from} → ${(byCode.get(it.to) || [it.to])[0]} ${p}`;
    });
    if (rows.length) { flapRows = rows; flapIdx = 0; startFlap(); }
  }

  // ---------- Destinations populaires ----------
  const DESTS = [
    ["CDG", "BKO", "Souvent avec une escale, environ 8 à 12 h", "Usually with a stop, about 8–12 h"],
    ["CDG", "DSS", "Vols directs, environ 5 h 30", "Direct flights, about 5 h 30"],
    ["CDG", "ABJ", "Vols directs, environ 6 h 30", "Direct flights, about 6 h 30"],
    ["BRU", "FIH", "Vols directs, environ 8 h", "Direct flights, about 8 h"],
    ["ORY", "CMN", "Low-cost possibles, environ 3 h", "Low-cost options, about 3 h"],
    ["LHR", "LOS", "Vols directs, environ 6 h 30", "Direct flights, about 6 h 30"],
    ["CDG", "YUL", "Nombreux vols directs, environ 7 h 30", "Many direct flights, about 7 h 30"],
    ["JFK", "DSS", "Vols directs, environ 8 h", "Direct flights, about 8 h"]
  ];
  function paintDests() {
    $("dests").innerHTML = DESTS.map(([a, b, dfr, den], i) => {
      const dsc = T(dfr, den);
      const A = byCode.get(a), B = byCode.get(b);
      const title = `${A ? A[1] : a} → ${B ? B[1] : b}`;
      return `<button type="button" class="dest" data-i="${i}"><span class="codes">${a} <span>→</span> ${b}</span><strong>${esc(title)}</strong><small>${esc(dsc)}</small></button>`;
    }).join("");
  }
  $("dests").addEventListener("click", (ev) => {
    const b = ev.target.closest(".dest"); if (!b) return;
    const [a, c] = DESTS[+b.dataset.i];
    selectTab("vols");
    $("f-from").value = labelOf(a); $("f-to").value = labelOf(c);
    $("trip-rt").checked = true; syncTrip();
    $("f-dep").value = addDays(today, 21); $("f-ret").value = addDays(today, 35);
    $("form-vols").requestSubmit();
  });

  // ---------- FAQ ----------
  const FAQ = [
    ["Escale est-il gratuit ?", "Oui. Escale ne demande ni inscription ni paiement. Vous payez uniquement votre réservation, directement sur le site choisi.",
     "Is Escale free?", "Yes. No sign-up, no fees. You only pay for your booking, directly on the site you choose."],
    ["Puis-je chercher n’importe quelle destination ?", "Oui : plus de 3 200 aéroports dans 234 pays sont proposés, et la recherche d’hôtels accepte n’importe quelle ville du monde. Laissez l’arrivée vide pour voir les destinations les moins chères.",
     "Can I search any destination?", "Yes: over 3,200 airports in 234 countries, and hotel search accepts any city in the world. Leave the destination empty to see the cheapest places to go."],
    ["Comment trouver le vol le moins cher ?", "Activez les dates flexibles, comparez au moins trois sites (Google Flights, Skyscanner, Kayak) et regardez la grille jour par jour : décaler le départ d’un ou deux jours fait souvent baisser le prix.",
     "How do I find the cheapest flight?", "Turn on flexible dates, compare at least three sites (Google Flights, Skyscanner, Kayak) and check the day-by-day grid: moving your departure by a day or two often lowers the price."],
    ["D’où viennent les prix affichés ?", "Ce sont des prix réels trouvés récemment par des voyageurs sur Aviasales. Le tarif exact et disponible s’affiche ensuite sur les sites de réservation.",
     "Where do the prices come from?", "They are real prices recently found by travellers on Aviasales. The exact available fare is then shown on the booking sites."],
    ["Les prix incluent-ils les bagages ?", "Pas toujours. Les tarifs les plus bas incluent parfois seulement un petit sac. Vérifiez la franchise bagage avant de payer.",
     "Do prices include baggage?", "Not always. The lowest fares sometimes include only a small bag. Check the baggage allowance before paying."],
    ["Comment payer moins cher une location de voiture ?", "Réservez tôt, choisissez la politique carburant « plein/plein » et comparez une prise en charge en ville avec l’aéroport, souvent plus cher.",
     "How can I pay less for a rental car?", "Book early, choose a full-to-full fuel policy and compare picking up in town with the airport, which is often more expensive."]
  ];
  function paintFaq() {
    $("faq-list").innerHTML = FAQ.map(([qf, af, qe, ae]) => `<details><summary>${esc(T(qf, qe))}</summary><p>${esc(T(af, ae))}</p></details>`).join("");
  }
  const ld = $("faq-ld");
  if (ld) ld.textContent = JSON.stringify({ "@context": "https://schema.org", "@type": "FAQPage",
    mainEntity: FAQ.map(([qf, af]) => ({ "@type": "Question", name: qf, acceptedAnswer: { "@type": "Answer", text: af } })) });

  // ---------- Liens partageables (?type=vols&from=CDG&to=BKO...) ----------
  const URLKEYS = {
    vols: { from: "f-from", to: "f-to", dep: "f-dep", ret: "f-ret", ad: "f-adults", ch: "f-children", cab: "f-cabin", ow: "trip-ow", flex: "f-flex", dir: "f-direct" },
    hotels: { dest: "h-dest", in: "h-in", out: "h-out", ad: "h-adults", ro: "h-rooms" },
    voitures: { pick: "c-pick", drop: "c-drop", other: "c-other", d1: "c-d1", t1: "c-t1", d2: "c-d2", t2: "c-t2", age: "c-age" }
  };
  const isBool = (el) => el.type === "checkbox" || el.type === "radio";
  function shareUrl(tab) {
    const params = new URLSearchParams({ type: tab });
    Object.entries(URLKEYS[tab]).forEach(([k, id]) => {
      const el = $(id); const v = isBool(el) ? (el.checked ? "1" : "") : el.value;
      if (v) params.set(k, v.replace(/^.*\(([A-Z]{3})\)$/, "$1"));
    });
    return location.origin + location.pathname + "?" + params.toString();
  }
  let urlHadParams = false;
  function applyUrl() {
    if (!isLive) return null;
    const p = new URLSearchParams(location.search), tab = p.get("type");
    if (!URLKEYS[tab]) return null;
    urlHadParams = true;
    Object.entries(URLKEYS[tab]).forEach(([k, id]) => {
      if (!p.has(k)) return;
      const el = $(id), v = p.get(k);
      if (isBool(el)) el.checked = v === "1";
      else el.value = /^[A-Z]{3}$/.test(v) && el.dataset.ac === "airport" ? labelOf(v) : v;
    });
    if (tab === "vols" && !$("trip-ow").checked) $("trip-rt").checked = true;
    return tab;
  }
  function shareBar(tab, text) {
    if (!isLive) return "";
    const url = shareUrl(tab);
    if (!booting) { try { history.replaceState(null, "", url); } catch (e) {} }
    const wa = "https://wa.me/?text=" + encodeURIComponent(text + " : " + url);
    return `<div class="share"><button type="button" class="go" id="copy-link" data-url="${esc(url)}">${T("Copier le lien de cette recherche", "Copy link to this search")}</button>
      <a class="go" href="${esc(wa)}" target="_blank" rel="noopener noreferrer">${T("Partager sur WhatsApp", "Share on WhatsApp")}</a><span class="ok" id="copy-ok" role="status"></span></div>`;
  }
  $("results").addEventListener("click", async (ev) => {
    const b = ev.target.closest("#copy-link"); if (!b) return;
    try { await navigator.clipboard.writeText(b.dataset.url); $("copy-ok").textContent = T("Lien copié", "Link copied"); }
    catch (e) { $("copy-ok").textContent = b.dataset.url; }
  });

  // ---------- Historique ----------
  const KEY = "escale.recent.v1";
  const load = () => { try { return JSON.parse(store.get(KEY)) || []; } catch (e) { return []; } };
  function remember(entry) {
    if (booting) return;
    const list = load().filter((e) => e.label !== entry.label);
    list.unshift(entry);
    store.set(KEY, JSON.stringify(list.slice(0, 6)));
    paintRecent();
  }
  function paintRecent() {
    const list = load();
    $("recent-block").hidden = list.length === 0;
    $("recent").innerHTML = list.map((e, i) => `<button type="button" class="chip" data-i="${i}">${esc(e.label)}</button>`).join("");
  }
  $("recent").addEventListener("click", (ev) => {
    const b = ev.target.closest(".chip"); if (!b) return;
    const e = load()[+b.dataset.i]; if (!e) return;
    Object.entries(e.fields).forEach(([id, v]) => { const el = $(id); if (!el) return; if (isBool(el)) el.checked = v; else el.value = v; });
    selectTab(e.tab); syncTrip(); syncDrop();
    $("form-" + e.tab).requestSubmit();
  });
  const snapshot = (ids) => Object.fromEntries(ids.map((id) => [id, isBool($(id)) ? $(id).checked : $(id).value]));

  // ---------- Formulaires ----------
  function syncTrip() {
    const month = $("f-monthmode").checked, ow = $("trip-ow").checked;
    $("f-dep-wrap").hidden = month;
    $("f-ret-wrap").hidden = ow || month;
    $("f-month-wrap").hidden = !month;
    $("f-stay-wrap").hidden = !month || ow;
    $("f-dep").required = !month;
  }
  $("f-monthmode").addEventListener("change", syncTrip);
  document.querySelectorAll('input[name="trip"]').forEach((r) => r.addEventListener("change", syncTrip));
  function syncDrop() { $("c-drop-wrap").hidden = !$("c-other").checked; }
  $("c-other").addEventListener("change", syncDrop);
  $("f-swap").addEventListener("click", () => { const a = $("f-from").value; $("f-from").value = $("f-to").value; $("f-to").value = a; });

  $("form-vols").addEventListener("submit", (ev) => {
    ev.preventDefault();
    const err = $("f-err"); err.textContent = "";
    const from = place($("f-from").value), to = place($("f-to").value);
    const ow = $("trip-ow").checked;
    if (!from) return (err.textContent = T("Indiquez un aéroport de départ.", "Enter a departure airport."));
    if (!from.code) return (err.textContent = T("Choisissez l’aéroport de départ dans la liste ou tapez son code à 3 lettres (ex. CDG).", "Pick the departure airport from the list or type its 3-letter code (e.g. JFK)."));
    if (to && !to.code) return (err.textContent = T("Choisissez l’aéroport d’arrivée dans la liste ou tapez son code à 3 lettres (ex. BKO).", "Pick the destination airport from the list or type its 3-letter code (e.g. LHR)."));
    if (to && to.code === from.code) return (err.textContent = T("Le départ et l’arrivée sont identiques.", "Origin and destination are the same."));
    if ($("f-monthmode").checked) {
      if (!to) return (err.textContent = T("Choisissez une destination pour voir les prix du mois entier.", "Choose a destination to see prices for the whole month."));
      renderMonth({ from, to, month: $("f-month").value, stay: ow ? 0 : +$("f-stay").value, ow,
        adults: +$("f-adults").value, children: +$("f-children").value, cabin: $("f-cabin").value });
      if (!booting) store.set("escale.from", labelOf(from.code));
      return;
    }
    const dep = $("f-dep").value, ret = ow ? null : $("f-ret").value;
    if (!dep) return (err.textContent = T("Choisissez une date d’aller.", "Choose a departure date."));
    if (dep < today) return (err.textContent = T("La date d’aller est déjà passée.", "The departure date is in the past."));
    if (!ow && (!ret || ret < dep)) return (err.textContent = T("La date de retour doit être après l’aller.", "The return date must be after departure."));
    const s = { from, to, dep, ret, adults: +$("f-adults").value, children: +$("f-children").value, cabin: $("f-cabin").value,
      flex: $("f-flex").checked, direct: $("f-direct").checked };
    renderFlights(s);
    if (!booting) store.set("escale.from", labelOf(from.code));
    remember({ tab: "vols", label: `✈ ${from.code}→${to ? to.code : "?"} · ${dep.slice(5)}`,
      fields: snapshot(["f-from", "f-to", "f-dep", "f-ret", "f-adults", "f-children", "f-cabin", "f-flex", "f-direct", "trip-rt", "trip-ow"]) });
  });

  $("form-hotels").addEventListener("submit", (ev) => {
    ev.preventDefault();
    const err = $("h-err"); err.textContent = "";
    const dest = $("h-dest").value.trim();
    if (!dest) return (err.textContent = T("Indiquez une destination.", "Enter a destination."));
    const a = $("h-in").value, b = $("h-out").value;
    if (!a || !b || b <= a) return (err.textContent = T("La date de départ doit être après la date d’arrivée.", "Check-out must be after check-in."));
    if (a < today) return (err.textContent = T("La date d’arrivée est déjà passée.", "The check-in date is in the past."));
    const s = { dest, in: a, out: b, adults: +$("h-adults").value, rooms: +$("h-rooms").value };
    renderHotels(s);
    remember({ tab: "hotels", label: `🛏 ${dest} · ${a.slice(5)}`, fields: snapshot(["h-dest", "h-in", "h-out", "h-adults", "h-rooms"]) });
  });

  $("form-voitures").addEventListener("submit", (ev) => {
    ev.preventDefault();
    const err = $("c-err"); err.textContent = "";
    const pick = place($("c-pick").value), drop = $("c-other").checked ? place($("c-drop").value) : null;
    if (!pick) return (err.textContent = T("Indiquez un lieu de prise en charge.", "Enter a pick-up location."));
    if ($("c-other").checked && !drop) return (err.textContent = T("Indiquez le lieu de restitution.", "Enter a drop-off location."));
    const d1 = $("c-d1").value, d2 = $("c-d2").value, t1 = +$("c-t1").value, t2 = +$("c-t2").value;
    if (!d1 || !d2 || d2 < d1 || (d2 === d1 && t2 <= t1)) return (err.textContent = T("La restitution doit être après la prise en charge.", "Drop-off must be after pick-up."));
    if (d1 < today) return (err.textContent = T("La date de prise en charge est déjà passée.", "The pick-up date is in the past."));
    const s = { pick, drop, d1, d2, t1, t2 };
    renderCars(s);
    remember({ tab: "voitures", label: `🚗 ${pick.code || pick.name} · ${d1.slice(5)}`, fields: snapshot(["c-pick", "c-drop", "c-other", "c-d1", "c-t1", "c-d2", "c-t2", "c-age"]) });
  });

  // ---------- Onglets ----------
  const TABS = ["vols", "hotels", "voitures"];
  let currentTab = "vols";
  function rerender() {
    const was = booting; booting = true;
    $("form-" + currentTab).dispatchEvent(new Event("submit", { cancelable: true }));
    booting = was;
  }
  function selectTab(name) {
    if (!TABS.includes(name)) name = "vols";
    currentTab = name;
    TABS.forEach((t) => {
      $("tab-" + t).setAttribute("aria-selected", String(t === name));
      $("tab-" + t).tabIndex = t === name ? 0 : -1;
      $("panel-" + t).hidden = t !== name;
    });
    store.set("escale.tab", name);
    rerender();
  }
  document.querySelector(".tabs").addEventListener("click", (ev) => { const b = ev.target.closest(".tab"); if (b) selectTab(b.dataset.tab); });
  document.querySelector(".tabs").addEventListener("keydown", (ev) => {
    if (ev.key !== "ArrowRight" && ev.key !== "ArrowLeft") return;
    const cur = TABS.indexOf(currentTab);
    const next = TABS[(cur + (ev.key === "ArrowRight" ? 1 : TABS.length - 1)) % TABS.length];
    selectTab(next); $("tab-" + next).focus();
  });

  // ---------- Langue et devise : changements ----------
  $("lang").addEventListener("change", () => {
    LANG = $("lang").value; store.set("escale.lang", LANG);
    countryNames = null; paintMonthOptions(); calc();
    applyLang(); paintDests(); paintFaq(); paintRecent(); rerender();
    if (!$("explore").hidden) { paintExploreMonths(); renderExplore($("ex-grid"), exploreFrom, exploreMonth); }
  });
  $("cur").addEventListener("change", () => {
    CUR = $("cur").value; store.set("escale.cur", CUR);
    rerender();
    if (!$("explore").hidden) renderExplore($("ex-grid"), exploreFrom, exploreMonth);
  });

  // ---------- Position du visiteur : aéroport le plus proche et devise ----------
  function nearestAirport(lat, lon) {
    const rad = Math.PI / 180;
    let best = null, bestD = Infinity;
    for (const a of DB) {
      if (!a[4] || a[5] == null) continue;
      const dLat = (a[5] - lat) * rad, dLon = (a[6] - lon) * rad;
      const h = Math.sin(dLat / 2) ** 2 + Math.cos(lat * rad) * Math.cos(a[5] * rad) * Math.sin(dLon / 2) ** 2;
      const dist = 12742 * Math.asin(Math.sqrt(h));
      if (dist < bestD) { bestD = dist; best = a; }
    }
    return bestD < 400 ? best : null;
  }
  async function useGeo() {
    if (!isLive) return null;
    try {
      const g = await fetch("/api/geo").then((r) => (r.ok ? r.json() : null));
      if (!g) return null;
      if (!store.get("escale.cur") && COUNTRY_CUR[g.country]) { CUR = COUNTRY_CUR[g.country]; $("cur").value = CUR; }
      if (g.lat == null || g.lon == null) return null;
      await loadDB();
      if (!dbLoaded) return null;
      return nearestAirport(g.lat, g.lon);
    } catch (e) { return null; }
  }

  // ---------- Démarrage ----------
  $("cur").value = CUR;
  applyLang(); paintDests(); paintFaq();
  let start = applyUrl() || (location.hash || "").slice(1);
  if (!TABS.includes(start)) start = store.get("escale.tab") || "vols";
  selectTab(start);
  syncTrip(); syncDrop(); paintRecent();
  booting = false;
  startFlap();

  if (isLive) {
    (window.requestIdleCallback || ((f) => setTimeout(f, 300)))(() => loadDB());
    useGeo().then((near) => {
      const userChose = urlHadParams || store.get("escale.from");
      if (near && !userChose && $("f-from").value === DEFAULT_FROM) {
        $("f-from").value = labelOf(near[0]);
        if (currentTab === "vols") rerender();
      }
      const from = place($("f-from").value);
      showHomeExplore(from && from.code ? from.code : "CDG");
      if (CUR !== "EUR" && currentTab !== "vols") rerender();
    });
  }
})();
