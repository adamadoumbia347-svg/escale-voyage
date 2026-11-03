// Diagnostic : langue affichée par le moteur en direct (White Label Travelpayouts) selon l'adresse et la langue du navigateur.
// Lancé par .github/workflows/diag-wl-langue.yml
const { chromium } = require('playwright');
const base = 'https://escale.live/recherche/?flightSearch=CDG1012DSS20121';
const tests = (process.env.TESTS || '&locale=en').split(' ').map((x) => ['fr-FR', x === '-' ? '' : x]);
(async () => { const b = await chromium.launch();
  for (const [loc, extra] of tests) {
    const c = await b.newContext({ locale: loc, viewport: { width: 1280, height: 900 } }); const p = await c.newPage();
    await p.goto(base + extra, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {}); await p.waitForTimeout(8000);
    const txt = await p.evaluate(() => { const out = []; const walk = (n) => { if (!n) return; if (n.nodeType === 3) { const t = n.textContent.trim(); if (t) out.push(t); return; }
      if (n.tagName === 'STYLE' || n.tagName === 'SCRIPT') return; if (n.shadowRoot) walk(n.shadowRoot); n.childNodes && n.childNodes.forEach(walk); };
      walk(document.querySelector('#tpwl-search')); walk(document.querySelector('#tpwl-tickets')); return out.join(' | ').slice(0, 300); });
    console.log(`[${loc}] ${extra || '(rien)'} => ${txt}`);
    await c.close(); }
  await b.close(); })();
