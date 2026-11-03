// Diagnostic : texte visible de pages externes (langue, monnaie), navigateur en français. Lancé par .github/workflows/diag-pages.yml
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch();
  for (const url of (process.env.URLS || '').split(' ').filter(Boolean)) {
    const c = await b.newContext({ locale: 'fr-FR', viewport: { width: 1280, height: 900 } }); const p = await c.newPage();
    await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {}); await p.waitForTimeout(7000);
    const txt = await p.evaluate(() => document.body ? document.body.innerText.replace(/\s+/g, ' ').slice(0, 400) : '');
    console.log('### ' + url + '\n    ' + txt + '\n    → ' + p.url().slice(0, 160));
    await c.close(); }
  await b.close(); })();
