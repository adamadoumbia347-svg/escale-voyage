// Vidéo TikTok du jour : lit les prix du baromètre (escale.live/barometre-prix/), choisit le format du jour,
// fabrique la vidéo (Playwright + ffmpeg, 1080 × 1920) et l'envoie par e-mail via /api/admin?action=video.
// Lancé chaque jour par .github/workflows/video-du-jour.yml. Variables : ADMIN_KEY (secret GitHub), FORMAT (facultatif, pour tester).
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const { chromium } = require('playwright');
const SITE = 'https://escale.live', DIR = __dirname, OUT = path.join(DIR, 'out');

const FLAGS = { Dakar: '🇸🇳', Bamako: '🇲🇱', Abidjan: '🇨🇮', Conakry: '🇬🇳', Douala: '🇨🇲', 'Yaoundé': '🇨🇲', Kinshasa: '🇨🇩', Brazzaville: '🇨🇬',
  Libreville: '🇬🇦', 'Lomé': '🇹🇬', Cotonou: '🇧🇯', Ouagadougou: '🇧🇫', Nouakchott: '🇲🇷', Alger: '🇩🇿', Oran: '🇩🇿', Casablanca: '🇲🇦', Marrakech: '🇲🇦', Tunis: '🇹🇳', Djerba: '🇹🇳' };
const TAGS = { '🇸🇳': '#senegal #dakar', '🇲🇱': '#mali #bamako', '🇨🇮': '#cotedivoire #abidjan', '🇬🇳': '#guinee #conakry', '🇨🇲': '#cameroun', '🇨🇩': '#rdc #kinshasa', '🇨🇬': '#congo',
  '🇬🇦': '#gabon', '🇹🇬': '#togo', '🇧🇯': '#benin', '🇧🇫': '#burkinafaso', '🇲🇷': '#mauritanie', '🇩🇿': '#algerie', '🇲🇦': '#maroc', '🇹🇳': '#tunisie' };
const MAGHREB = new Set(['🇩🇿', '🇲🇦', '🇹🇳']);
const TIPS = [
  ['Décale ton départ d\'un ou deux jours', 'Le calendrier des prix montre les jours les moins chers', 'Même trajet, même mois… mais pas le même prix'],
  ['Compare le prix AVEC la valise', 'Le billet le moins cher n\'inclut pas toujours la soute', 'Ajoute le prix du bagage avant de comparer'],
  ['Regarde les vols avec escale', 'Casablanca, Istanbul, Addis-Abeba…', 'souvent moins chers que le vol direct'],
  ['Compare plusieurs aéroports', 'Orly, Beauvais, Bruxelles, Lyon…', 'un autre départ peut coûter bien moins cher'],
  ['Réserve tôt pour les fêtes', 'Noël, l\'été, la Tabaski…', 'les prix montent à l\'approche des dates'],
  ['Crée une alerte prix gratuite', 'Tu choisis ton budget', 'tu reçois un e-mail quand le billet baisse'],
  ['Vérifie la durée totale du trajet', 'Un vol pas cher avec 17 h d\'escale…', 'ça vaut le coup de comparer'],
];

// Captures du site sur téléphone (vraies pages du jour) et position des éléments que le doigt touche (px CSS de la page)
async function capture(b, url, name, sels, maxH, wait) {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, locale: 'fr-FR', isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  await ctx.addInitScript(() => { try { sessionStorage.setItem('escale.wa', '0'); sessionStorage.setItem('escale.v', '1'); localStorage.setItem('escale.visites', '0');
    localStorage.setItem('escale.lang', 'fr'); localStorage.setItem('escale.cur', 'EUR'); localStorage.setItem('escale.from', 'Paris (CDG)'); } catch (e) {} });
  const p = await ctx.newPage();
  await p.goto(url, { waitUntil: 'load', timeout: 60000 }).catch(() => {});
  const bar = await p.$$('.cc-bar button'); if (bar.length) await bar[0].click().catch(() => {});
  await p.waitForTimeout(wait);
  const boxes = await p.evaluate((sels) => { const o = {}; for (const [k, q] of Object.entries(sels)) { const e = document.querySelector(q); if (!e) continue;
    e.scrollIntoView && 0; const r = e.getBoundingClientRect(); o[k] = { x: r.left + r.width / 2, y: r.top + scrollY, top: r.top + scrollY, h: r.height }; } return o; }, sels);
  const H = Math.min(maxH, await p.evaluate(() => document.documentElement.scrollHeight));
  const file = path.join(OUT, name + '.jpg');
  await p.screenshot({ path: file, type: 'jpeg', quality: 72, fullPage: true, clip: { x: 0, y: 0, width: 390, height: H } });
  await ctx.close();
  return { src: name + '.jpg', w: 390, h: H, boxes };
}

async function prices() {
  const html = process.env.BARO_FILE ? fs.readFileSync(process.env.BARO_FILE, 'utf8') : await (await fetch(SITE + '/barometre-prix/')).text(); // BARO_FILE : test hors ligne
  const rows = [...html.matchAll(/<tr><th scope="row"><a href="\/([^/]+)\/">([^<]+)<\/a><\/th><td><strong>([^<]+)<\/strong><\/td><td>(.*?)<\/td><td>(.*?)<\/td><td>([^<]*)<\/td><\/tr>/g)]
    .map(([, p, label, price, d7, , month]) => {
      const lab = label.replace(/&#x27;|&#39;/g, "'").replace(/&amp;/g, '&'), city = lab.split('→')[1].trim();
      const dv = (d7.match(/([+−-]?)(\d+) %/) || []), d = dv[2] ? (dv[1] === '+' ? 1 : -1) * +dv[2] : null;
      return { path: p, route: lab, city, flag: FLAGS[city] || '✈️', price: +price.replace(/[^\d]/g, ''), d7: dv[1] === '' && dv[2] ? 0 : d, month: month.trim() };
    }).filter((r) => r.price > 0).sort((a, b) => a.price - b.price);
  if (rows.length < 6) throw new Error('baromètre illisible (' + rows.length + ' lignes)');
  return rows;
}

const day = () => new Date(new Date().toLocaleString('en-US', { timeZone: 'Europe/Paris' }));
const today = () => day().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long' });
const doy = () => { const d = day(); return Math.floor((d - new Date(d.getFullYear(), 0, 0)) / 864e5); };
const tags = (list) => [...new Set(list.map((r) => TAGS[r.flag]).filter(Boolean).join(' ').split(' '))].slice(0, 6).join(' ');
const card = (r, extra) => ({ flag: r.flag, route: r.route, price: r.price, extra: extra || 'aller-retour dès' });
const OUTRO = { note: 'Prix aller-retour les plus bas repérés pour un départ<br>dans les 6 prochains mois. Ils changent chaque jour.', ask: 'Ta ville n\'est pas dans le top ?<br><span class="y">Écris-la en commentaire 👇</span>', cta: 'Tous les prix, chaque jour 👆' };

function build(rows, fmt) {
  const mag = rows.filter((r) => MAGHREB.has(r.flag)), afr = rows.filter((r) => !MAGHREB.has(r.flag));
  const base = '#billetdavion #volpascher #diaspora #bonplan';
  const date = today();
  if (fmt === 'top') return { title: 'Top des prix de la semaine', data: { hook: { emoji: '🔥✈️', title: 'Les vols <b>les moins chers</b><br>vers l\'Afrique<br>cette semaine', sub: `Prix repérés le ${date}` },
      sections: [{ chip: 'Top 3 Maghreb', title: 'Depuis la France 🇫🇷', cards: mag.slice(0, 3).map((r) => card(r)) }, { chip: 'Top 3 Afrique', title: 'De l\'Ouest et du Centre 🌍', cards: afr.slice(0, 3).map((r) => card(r)) }], outro: OUTRO },
    route: afr[0].path, caption: `Les vols les moins chers vers l'Afrique cette semaine 🔥 ${mag[0].route} dès ${mag[0].price} €, ${afr[0].route} dès ${afr[0].price} € aller-retour ✈️ Ta ville ? Dis-le en commentaire 👇 ${base} ${tags([...mag.slice(0, 3), ...afr.slice(0, 3)])}` };
  if (fmt === 'afrique' || fmt === 'maghreb') { const L = (fmt === 'afrique' ? afr : mag).slice(0, 5), nom = fmt === 'afrique' ? 'l\'Afrique de l\'Ouest et du Centre' : 'le Maghreb';
    return { title: `Top 5 ${fmt === 'afrique' ? 'Afrique' : 'Maghreb'}`, data: { hook: { emoji: fmt === 'afrique' ? '🌍✈️' : '🌴✈️', title: `Top 5 des vols<br><b>les moins chers</b><br>vers ${nom}`, sub: `Aller-retour, prix repérés le ${date}` },
        sections: [{ chip: `Top 5 ${fmt === 'afrique' ? 'Afrique' : 'Maghreb'}`, title: 'Depuis la France et la Belgique', cards: L.map((r) => card(r)) }], outro: OUTRO },
      route: L[0].path, caption: `Top 5 des vols les moins chers vers ${nom} 🔥 n°1 : ${L[0].route} dès ${L[0].price} € aller-retour ✈️ Ta ville ? Dis-le en commentaire 👇 ${base} ${tags(L)}` }; }
  if (fmt === 'focus') { const pool = afr.length ? afr : rows, r = pool[doy() % pool.length];
    return { title: `${r.route} dès ${r.price} €`, data: { hook: { emoji: r.flag + '✈️', title: `Combien coûte<br><b>${r.route}</b><br>en ce moment ?`, sub: 'La réponse va te surprendre 👀' },
        sections: [{ chip: 'Prix du moment', title: r.route, cards: [card(r, r.month ? `aller-retour dès · le moins cher en ${r.month}` : 'aller-retour dès')] }], outro: { note: OUTRO.note, ask: 'Tu pars quand ?<br><span class="y">Dis-le en commentaire 👇</span>', cta: 'Compare tes dates gratuitement 👆' } },
      route: r.path, caption: `${r.route} : aller-retour dès ${r.price} € en ce moment ✈️${r.month ? ` Mois le moins cher : ${r.month}.` : ''} Compare tes dates gratuitement sur escale.live ${base} ${tags([r])}` }; }
  if (fmt === 'baisse') { const down = rows.filter((r) => r.d7 !== null && r.d7 <= -3).sort((a, b) => a.d7 - b.d7).slice(0, 3);
    if (!down.length) return build(rows, 'maghreb');
    return { title: 'Ça baisse cette semaine', data: { hook: { emoji: '📉✈️', title: 'Les prix qui <b>baissent</b><br>cette semaine', sub: `Comparé à il y a 7 jours · ${date}` },
        sections: [{ chip: 'En baisse', title: 'Sur 7 jours', cards: down.map((r) => card(r, `${r.d7} % en 7 jours`)) }], outro: OUTRO },
      route: down[0].path, caption: `Les prix des vols qui baissent cette semaine 📉 ${down.map((r) => `${r.route} ${r.d7} %`).join(', ')} ✈️ ${base} ${tags(down)}` }; }
  if (fmt === 'quiz') { const pool = rows.filter((r) => r.price > 60), r = pool[(doy() * 7) % pool.length];
    const opts = [r.price, Math.round(r.price * 1.45 / 5) * 5, Math.round(r.price * 0.65 / 5) * 5], order = [[0, 1, 2], [1, 0, 2], [2, 1, 0]][doy() % 3];
    return { title: `Devine le prix : ${r.route}`, data: { hook: { emoji: '🤔💸', title: 'Devine le prix<br>de ce billet', sub: 'Réponds avant la fin du compte à rebours !' },
        quiz: { flag: r.flag, route: r.route, options: order.map((i) => opts[i]), answer: order.indexOf(0) }, outro: { ask: 'Tu avais trouvé ?<br><span class="y">Dis-le en commentaire 👇</span>', cta: 'Tous les prix sur escale.live 👆' } },
      route: r.path, caption: `Devine le prix 🤔 ${r.route} aller-retour : A, B ou C ? Réponse dans la vidéo 👀 ${base} ${tags([r])}` }; }
  // astuce
  const k = doy() % TIPS.length, [l1, l2, l3] = TIPS[k];
  return { title: `Astuce : ${l1}`, data: { hook: { emoji: '💡✈️', title: 'L\'astuce du jour<br>pour payer ton billet<br><b>moins cher</b>', sub: 'Garde-la pour ton prochain voyage 📌' },
      tip: { label: 'Astuce n°' + (k + 1), lines: [l1, `<small>${l2}</small>`, `<span class="y">${l3}</span>`] }, outro: { ask: 'Tu la connaissais ?<br><span class="y">Dis-le en commentaire 👇</span>', cta: 'Abonne-toi pour d\'autres astuces 👆' } },
    caption: `Astuce du jour 💡 ${l1} : ${l2.toLowerCase()}, ${l3}. Compare gratuitement sur escale.live ✈️ #astuce ${base}` };
}

// Scène « téléphone » : baromètre puis page du trajet mis en avant (calendrier, alerte), avec le doigt qui touche
async function phoneScene(b, fmt, v) {
  const route = v.route || 'vol-paris-dakar';
  const R = await capture(b, `${SITE}/${route}/`, 'trajet', { hero: '#hero-price', cal: '#route-calendar', day: '#route-calendar .cal-day.t0', alert: '#price-alert', alertBtn: '#price-alert button[type=submit]' }, 7200, 7000);
  const shots = [], cal = R.boxes.cal, day = R.boxes.day, al = R.boxes.alert, btn = R.boxes.alertBtn;
  if (['top', 'afrique', 'maghreb', 'baisse'].includes(fmt)) {
    const Bp = await capture(b, `${SITE}/barometre-prix/`, 'barometre', { table: '#barometre table', row: `#barometre a[href="/${route}/"]` }, 6000, 4000);
    const ty = Bp.boxes.table ? Bp.boxes.table.top - 110 : 500, row = Bp.boxes.row;
    shots.push({ src: Bp.src, w: Bp.w, steps: [[0, 0], [.9, 0], [2.6, ty], [4.6, ty]], taps: row ? [[3.4, row.x, row.y, ty]] : [], dur: 4.6 });
  }
  const steps = [[0, 0], [1.4, 0]], taps = [];
  let t = 1.4;
  if (R.boxes.hero) taps.push([.9, 200, R.boxes.hero.y, 0]);
  if (cal) { const y = cal.top - 70; steps.push([t + 1.8, y]); t += 1.8; if (day) { taps.push([t + .8, day.x, day.y, y]); } steps.push([t + 2.2, y]); t += 2.2; }
  if (al && (fmt === 'focus' || fmt === 'astuce')) { const y = al.top - 60; steps.push([t + 1.4, y]); t += 1.4; if (btn) taps.push([t + .8, btn.x, btn.y, y]); steps.push([t + 2, y]); t += 2; }
  shots.push({ src: R.src, w: R.w, steps, taps, dur: t + .3 });
  v.data.phone = { caption: fmt === 'focus' ? 'Les jours les moins chers en un coup d\'œil 📅' : fmt === 'astuce' ? 'Tout ça, gratuitement, sur escale.live 👇' : 'Tous ces prix en direct sur escale.live 👇',
    sub: 'Calendrier des prix · alerte gratuite · prix en direct', shots };
}

(async () => {
  const rows = await prices();
  const week = ['quiz', 'top', 'focus', 'astuce', 'afrique', 'baisse', 'maghreb']; // dimanche → samedi
  const fmt = process.env.FORMAT || week[day().getDay()];
  const v = build(rows, fmt);
  console.log('Format :', fmt, '·', v.title);
  fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(path.join(OUT, 'f'), { recursive: true });
  const b = await chromium.launch();
  if (!process.env.NO_PHONE) await phoneScene(b, fmt, v).catch((e) => console.log('Captures impossibles, vidéo sans téléphone :', e.message));
  for (const f of ['template.html', 'font.woff2']) fs.copyFileSync(path.join(DIR, f), path.join(OUT, f));
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.addInitScript((d) => { window.DATA = d; }, v.data);
  await p.goto('file://' + path.join(OUT, 'template.html')); await p.waitForFunction(() => [...document.images].every((i) => i.complete)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.evaluate(() => document.getAnimations().forEach((a) => a.pause()));
  const end = await p.evaluate(() => window.__end), fps = 30, n = Math.ceil(end * fps);
  const probe = process.env.PROBE ? process.env.PROBE.split(',').map((s) => Math.round(+s * fps)) : null; // test : quelques images seulement
  for (const i of probe || [...Array(n).keys()]) {
    await p.evaluate((ms) => { document.getAnimations().forEach((a) => (a.currentTime = ms)); window.__tick(ms / 1000); }, i * 1000 / fps);
    await p.screenshot({ path: path.join(OUT, 'f', String(i).padStart(4, '0') + '.png') });
  }
  await b.close();
  if (probe) return console.log('Images de test :', probe.length, '· durée', end.toFixed(1), 's');
  const name = `escale-${new Date().toISOString().slice(0, 10)}-${fmt}.mp4`, mp4 = path.join(OUT, name);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', path.join(OUT, 'f', '%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'medium', '-movflags', '+faststart', mp4]);
  console.log('Vidéo :', name, (fs.statSync(mp4).size / 1e6).toFixed(1), 'Mo,', end.toFixed(1), 's');
  if (process.env.NO_SEND) return;
  const r = await fetch(SITE + '/api/admin?action=video', { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-admin-key': process.env.ADMIN_KEY || '' },
    body: JSON.stringify({ title: v.title, caption: v.caption, filename: name, video: fs.readFileSync(mp4).toString('base64') }) });
  const j = await r.text(); console.log('Envoi :', r.status, j.slice(0, 200));
  if (!r.ok || !/"sent":true/.test(j)) process.exit(1);
})().catch((e) => { console.error(e); process.exit(1); });
