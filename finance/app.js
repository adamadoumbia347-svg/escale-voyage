// Marché Facile : widgets TradingView + données CoinGecko / Alternative.me traduites en mots simples.
(() => {
  const $ = (s) => document.querySelector(s);
  const root = document.documentElement;
  const etat = { symbole: "FOREXCOM:SPXUSD", devise: "eur", flux: { feedMode: "market", market: "stock" } };

  // ---------- Thème ----------
  try { const t = localStorage.getItem("theme"); if (t) root.dataset.theme = t; } catch (e) {}
  const theme = () => root.dataset.theme;
  $("#theme").addEventListener("click", () => {
    root.dataset.theme = theme() === "dark" ? "light" : "dark";
    try { localStorage.setItem("theme", theme()); } catch (e) {}
    widgets();
  });

  // ---------- Widgets TradingView ----------
  function tv(id, nom, config) {
    const el = document.getElementById(id);
    el.innerHTML = '<div class="tradingview-widget-container" style="height:100%;width:100%"><div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div></div>';
    const s = document.createElement("script");
    s.src = `https://s3.tradingview.com/external-embedding/embed-widget-${nom}.js`;
    s.async = true;
    s.innerHTML = JSON.stringify({ locale: "fr", colorTheme: theme(), ...config });
    s.onerror = () => { el.innerHTML = '<div class="tv-erreur">Impossible de charger ce module (connexion ou bloqueur de publicité).</div>'; };
    el.firstChild.appendChild(s);
  }

  const graphique = () => tv("chart", "advanced-chart", {
    autosize: true, symbol: etat.symbole, interval: "D", timezone: "Europe/Paris",
    theme: theme(), style: "1", allow_symbol_change: true, support_host: "https://www.tradingview.com",
  });
  const avis = () => tv("tech", "technical-analysis", {
    interval: "1D", width: "100%", height: "100%", isTransparent: true, symbol: etat.symbole,
    showIntervalTabs: true, displayMode: "single",
  });
  const actus = () => tv("news", "timeline", {
    ...etat.flux, isTransparent: true, displayMode: "regular", width: "100%", height: "100%",
  });

  function widgets() {
    tv("tape", "ticker-tape", {
      symbols: [
        { proName: "FOREXCOM:SPXUSD", title: "S&P 500" },
        { proName: "FOREXCOM:NSXUSD", title: "Nasdaq 100" },
        { proName: "EURONEXT:PX1", title: "CAC 40" },
        { proName: "XETR:DAX", title: "DAX" },
        { proName: "FX:EURUSD", title: "EUR/USD" },
        { proName: "BITSTAMP:BTCUSD", title: "Bitcoin" },
        { proName: "BITSTAMP:ETHUSD", title: "Ethereum" },
        { proName: "OANDA:XAUUSD", title: "Or" },
        { proName: "TVC:USOIL", title: "Pétrole" },
      ],
      showSymbolLogo: true, isTransparent: true, displayMode: "adaptive",
    });
    graphique();
    avis();
    tv("overview", "market-overview", {
      dateRange: "1D", showChart: true, width: "100%", height: "100%", isTransparent: true, showSymbolLogo: true,
      tabs: [
        { title: "Indices", symbols: [
          { s: "FOREXCOM:SPXUSD", d: "S&P 500 (USA)" }, { s: "FOREXCOM:NSXUSD", d: "Nasdaq 100 (USA)" },
          { s: "FOREXCOM:DJI", d: "Dow Jones (USA)" }, { s: "EURONEXT:PX1", d: "CAC 40 (France)" },
          { s: "XETR:DAX", d: "DAX (Allemagne)" }, { s: "INDEX:NKY", d: "Nikkei (Japon)" } ] },
        { title: "Devises", symbols: [
          { s: "FX:EURUSD", d: "Euro / Dollar" }, { s: "FX:GBPUSD", d: "Livre / Dollar" },
          { s: "FX:USDJPY", d: "Dollar / Yen" }, { s: "FX_IDC:EURXOF", d: "Euro / Franc CFA" },
          { s: "FX:USDCHF", d: "Dollar / Franc suisse" } ] },
        { title: "Matières premières", symbols: [
          { s: "OANDA:XAUUSD", d: "Or" }, { s: "OANDA:XAGUSD", d: "Argent" },
          { s: "TVC:USOIL", d: "Pétrole WTI" }, { s: "TVC:UKOIL", d: "Pétrole Brent" },
          { s: "NYMEX:NG1!", d: "Gaz naturel" } ] },
        { title: "Obligations", symbols: [
          { s: "TVC:US10Y", d: "Taux USA 10 ans" }, { s: "TVC:DE10Y", d: "Taux Allemagne 10 ans" },
          { s: "TVC:FR10Y", d: "Taux France 10 ans" } ] },
      ],
    });
    tv("heatmap", "stock-heatmap", {
      dataSource: "SPX500", grouping: "sector", blockSize: "market_cap_basic", blockColor: "change",
      hasTopBar: false, isDataSetEnabled: false, isZoomEnabled: true, hasSymbolTooltip: true,
      isMonoSize: false, width: "100%", height: "100%",
    });
    actus();
    tv("events", "events", {
      isTransparent: true, width: "100%", height: "100%",
      importanceFilter: "0,1", countryFilter: "us,eu,fr,de,gb,cn,jp",
    });
  }

  function chips(id, onClick) {
    $(id).addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      $(id).querySelectorAll("button").forEach((x) => x.classList.toggle("actif", x === b));
      onClick(b.dataset);
    });
  }
  chips("#symboles", (d) => { etat.symbole = d.s; graphique(); avis(); });
  chips("#flux", (d) => { etat.flux = d.f === "all" ? { feedMode: "all_symbols" } : { feedMode: "market", market: d.m }; actus(); });
  chips("#devise", (d) => { etat.devise = d.d; cryptos(); });

  // ---------- Mise en forme ----------
  const nf = (n, opt) => new Intl.NumberFormat("fr-FR", opt).format(n);
  const prix = (n, dev) => nf(n, { style: "currency", currency: dev.toUpperCase(), maximumFractionDigits: n < 1 ? 4 : n < 100 ? 2 : 0 });
  const gros = (n, dev) => nf(n, { style: "currency", currency: dev.toUpperCase(), notation: "compact", maximumFractionDigits: 2 });
  const pct = (n) => (n == null ? "—" : `${n > 0 ? "+" : ""}${nf(n, { maximumFractionDigits: 2 })} %`);
  const sens = (n) => (n > 0 ? "up" : n < 0 ? "down" : "");

  // Traduction d'une variation en mots simples
  function enClair(j, s) {
    if (j == null) return ["Pas de données", ""];
    if (j >= 8) return ["🚀 S'envole", "up"];
    if (j >= 3) return ["📈 Forte hausse", "up"];
    if (j >= 0.5) return [s < -5 ? "↗️ Rebondit" : "↗️ Monte doucement", "up"];
    if (j > -0.5) return ["➖ Stable", ""];
    if (j > -3) return [s > 5 ? "↘️ Petite pause" : "↘️ Baisse légère", "down"];
    if (j > -8) return ["📉 Forte baisse", "down"];
    return ["⚠️ Chute brutale", "down"];
  }

  function humeur(v) {
    if (v <= 24) return ["Peur extrême", "Les investisseurs paniquent et vendent. Historiquement, ce sont souvent des moments où les prix sont bas.", "#e5484d"];
    if (v <= 44) return ["Peur", "Les investisseurs sont inquiets et prudents.", "#f76b15"];
    if (v <= 55) return ["Neutre", "Ni panique, ni euphorie : le marché hésite.", "#c9a800"];
    if (v <= 75) return ["Avidité", "Les investisseurs sont confiants et achètent.", "#8ac926"];
    return ["Avidité extrême", "Euphorie générale : attention, les prix peuvent être gonflés et corriger brusquement.", "#26a69a"];
  }

  async function json(url) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }

  // ---------- Données ----------
  const donnees = { global: null, fg: null, coins: null };

  async function peurAvidite() {
    try {
      const { data } = await json("https://api.alternative.me/fng/?limit=8");
      donnees.fg = data;
      const v = +data[0].value;
      const [label, explic, couleur] = humeur(v);
      $("#fg-val").textContent = v;
      $("#fg-val").style.color = couleur;
      $("#fg-label").textContent = `/ 100 · ${label}`;
      $("#fg-explic").textContent = explic;
      $("#aiguille").style.transform = `rotate(${(v / 100) * 180 - 90}deg)`;
      const hier = +data[1].value, sem = +data[7].value;
      $("#fg-hier").textContent = `Hier : ${hier} (${humeur(hier)[0].toLowerCase()}) · Il y a 7 jours : ${sem} (${humeur(sem)[0].toLowerCase()})`;
    } catch (e) {
      $("#fg-explic").textContent = "Indice indisponible pour le moment.";
    }
  }

  async function global() {
    try {
      const { data } = await json("https://api.coingecko.com/api/v3/global");
      donnees.global = data;
      const v = data.market_cap_change_percentage_24h_usd;
      $("#k-cap").textContent = gros(data.total_market_cap.eur, "eur");
      $("#k-var").textContent = pct(v);
      $("#k-var").className = sens(v);
      $("#k-vol").textContent = gros(data.total_volume.eur, "eur");
      $("#k-btc").textContent = `${nf(data.market_cap_percentage.btc, { maximumFractionDigits: 1 })} %`;
    } catch (e) {
      $("#k-cap").textContent = "indisponible";
    }
  }

  async function cryptos() {
    const dev = etat.devise;
    try {
      const coins = await json(`https://api.coingecko.com/api/v3/coins/markets?vs_currency=${dev}&order=market_cap_desc&per_page=15&page=1&sparkline=true&price_change_percentage=24h,7d`);
      donnees.coins = coins;
      $("#cryptos").innerHTML = coins.map((c, i) => {
        const j = c.price_change_percentage_24h_in_currency, s = c.price_change_percentage_7d_in_currency;
        const [mot, cl] = enClair(j, s);
        return `<tr>
          <td class="muted">${i + 1}</td>
          <td><img src="${c.image}" alt="" loading="lazy">${esc(c.name)}<span class="sym">${esc(c.symbol)}</span></td>
          <td class="num">${prix(c.current_price, dev)}</td>
          <td class="num ${sens(j)}">${pct(j)}</td>
          <td class="num ${sens(s)}">${pct(s)}</td>
          <td class="cacher-mobile">${sparkline(c.sparkline_in_7d?.price, s)}</td>
          <td><span class="badge ${cl}">${mot}</span></td>
        </tr>`;
      }).join("");
    } catch (e) {
      $("#cryptos").innerHTML = '<tr><td colspan="7" class="muted">Données crypto indisponibles pour le moment (limite de requêtes atteinte ?). Réessayez dans une minute.</td></tr>';
    }
  }

  function sparkline(p, s) {
    if (!p || p.length < 2) return "";
    const pts = p.filter((_, i) => i % 4 === 0);
    const min = Math.min(...pts), max = Math.max(...pts), w = 120, h = 32;
    const d = pts.map((v, i) => `${(i / (pts.length - 1)) * w},${h - ((v - min) / (max - min || 1)) * h}`).join(" ");
    return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><polyline points="${d}" fill="none" stroke="var(--${s >= 0 ? "up" : "down"})" stroke-width="1.6"/></svg>`;
  }

  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // Phrase de résumé construite à partir des données disponibles
  function resume() {
    const { global: g, fg, coins } = donnees;
    const morceaux = [];
    if (g) {
      const v = g.market_cap_change_percentage_24h_usd;
      const ton = v >= 3 ? "une <b class=up>très bonne journée</b>" : v >= 0.5 ? "une <b class=up>bonne journée</b>"
        : v > -0.5 ? "une journée <b>calme</b>" : v > -3 ? "une <b class=down>journée difficile</b>" : "une <b class=down>très mauvaise journée</b>";
      morceaux.push(`Les cryptomonnaies vivent ${ton} : leur valeur totale a ${v >= 0 ? "pris" : "perdu"} <b class="${sens(v)}">${nf(Math.abs(v), { maximumFractionDigits: 1 })} %</b> en 24 h.`);
    }
    if (coins && coins.length) {
      const btc = coins.find((c) => c.id === "bitcoin");
      if (btc) morceaux.push(`Le Bitcoin vaut <b>${prix(btc.current_price, etat.devise)}</b> (${pct(btc.price_change_percentage_24h_in_currency)} aujourd'hui, ${pct(btc.price_change_percentage_7d_in_currency)} sur la semaine).`);
      const tri = [...coins].filter((c) => c.price_change_percentage_24h_in_currency != null)
        .sort((a, b) => b.price_change_percentage_24h_in_currency - a.price_change_percentage_24h_in_currency);
      const top = tri[0], flop = tri[tri.length - 1];
      if (top && flop && top !== flop) morceaux.push(`Meilleure performance : <b>${esc(top.name)}</b> (<span class="up">${pct(top.price_change_percentage_24h_in_currency)}</span>). Plus forte baisse : <b>${esc(flop.name)}</b> (<span class="down">${pct(flop.price_change_percentage_24h_in_currency)}</span>).`);
    }
    if (fg) {
      const v = +fg[0].value, avant = +fg[7].value;
      const [label] = humeur(v);
      const evol = v - avant >= 10 ? "nettement plus confiants qu'il y a une semaine" : v - avant <= -10 ? "nettement plus inquiets qu'il y a une semaine"
        : "à peu près aussi confiants que la semaine dernière";
      morceaux.push(`Humeur des investisseurs : <b>${label.toLowerCase()}</b> (${v}/100), ${evol}.`);
    }
    morceaux.push("Pour les actions, devises et matières premières, regardez le graphique et la vue d'ensemble ci-dessous : <span class=up>vert</span> = hausse, <span class=down>rouge</span> = baisse.");
    $("#resume").innerHTML = morceaux.join(" ");
    $("#maj").textContent = new Date().toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
  }

  async function charger() {
    await Promise.allSettled([peurAvidite(), global(), cryptos()]);
    resume();
  }
  $("#refresh").addEventListener("click", charger);

  // ---------- Lexique ----------
  const LEXIQUE = [
    ["Action", "Un petit morceau d'une entreprise. Si l'entreprise gagne de la valeur, l'action aussi."],
    ["Indice boursier", "Un panier d'actions qui résume la santé d'un marché (ex. CAC 40 = 40 grandes entreprises françaises)."],
    ["Marché haussier (bull)", "Période où les prix montent pendant longtemps. Le taureau frappe de bas en haut avec ses cornes."],
    ["Marché baissier (bear)", "Période où les prix baissent d'au moins 20 %. L'ours frappe de haut en bas avec ses pattes."],
    ["Volatilité", "L'ampleur des mouvements de prix. Forte volatilité = ça monte et descend beaucoup, donc plus risqué."],
    ["Volume", "La quantité échangée. Un mouvement de prix avec beaucoup de volume est plus « sérieux »."],
    ["Capitalisation", "Prix d'une action × nombre d'actions : la valeur totale d'une entreprise ou d'une crypto en bourse."],
    ["Bougie (chandelier)", "Un rectangle qui montre le prix d'ouverture, de clôture, le plus haut et le plus bas d'une période. Verte = hausse, rouge = baisse."],
    ["Support", "Un niveau de prix où l'actif a souvent arrêté de baisser, comme un plancher."],
    ["Résistance", "Un niveau de prix où l'actif a souvent arrêté de monter, comme un plafond."],
    ["Tendance", "La direction générale des prix : haussière, baissière ou sans direction (« range »)."],
    ["Moyenne mobile", "Le prix moyen des X derniers jours, tracé en ligne. Elle lisse les mouvements pour voir la tendance."],
    ["RSI", "Un indicateur de 0 à 100. Au-dessus de 70 : l'actif a peut-être trop monté. Sous 30 : il a peut-être trop baissé."],
    ["Dividende", "Une part des bénéfices qu'une entreprise reverse à ses actionnaires, souvent une fois par an."],
    ["Taux directeur", "Le taux auquel les banques centrales prêtent aux banques. S'il monte, emprunter coûte plus cher et la bourse souffre souvent."],
    ["Inflation", "La hausse générale des prix. Une inflation élevée pousse les banques centrales à monter les taux."],
    ["Obligation", "Un prêt fait à un État ou une entreprise, qui vous verse des intérêts."],
    ["ETF (tracker)", "Un fonds qui copie un indice. Acheter un ETF CAC 40, c'est acheter un peu des 40 entreprises d'un coup."],
    ["Crypto-monnaie", "Une monnaie numérique sans banque centrale (Bitcoin, Ethereum…). Très volatile."],
    ["Stablecoin", "Une crypto dont la valeur est accrochée au dollar ou à l'euro (ex. USDT, USDC)."],
    ["Peur & Avidité", "Un indice de 0 à 100 qui mesure l'humeur des investisseurs, de la panique à l'euphorie."],
    ["Correction", "Une baisse de 10 à 20 % après une hausse. C'est normal et fréquent."],
    ["Krach", "Une chute très brutale et rapide des marchés."],
    ["Diversifier", "Ne pas mettre tous ses œufs dans le même panier : répartir son argent sur plusieurs placements."],
    ["Paire de devises", "Le prix d'une monnaie dans une autre. EUR/USD = 1,08 veut dire 1 € = 1,08 $."],
    ["Spread", "L'écart entre le prix d'achat et le prix de vente : c'est en partie le coût de la transaction."],
    ["Levier", "Emprunter pour investir plus. Les gains ET les pertes sont multipliés : très risqué."],
  ];
  function lexique(filtre = "") {
    const f = filtre.trim().toLowerCase();
    $("#mots").innerHTML = LEXIQUE.filter(([m, d]) => !f || (m + d).toLowerCase().includes(f))
      .map(([m, d]) => `<div><dt>${m}</dt><dd>${d}</dd></div>`).join("") || '<p class="muted">Aucun mot trouvé.</p>';
  }
  $("#recherche").addEventListener("input", (e) => lexique(e.target.value));

  // ---------- Démarrage ----------
  lexique();
  widgets();
  charger();
  setInterval(charger, 5 * 60 * 1000);
})();
