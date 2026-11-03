// Diagnostic : éléments qui bougent pendant le chargement (CLS) sur le site en ligne, profil téléphone. Lancé par .github/workflows/diag-cls.yml
const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const c = await b.newContext({ ...devices['Moto G4'] || {}, viewport: { width: 412, height: 823 }, deviceScaleFactor: 1.75, isMobile: true, hasTouch: true });
  for (const u of process.argv.slice(2)) { const p = await c.newPage();
    const cdp = await c.newCDPSession(p); await cdp.send('Network.enable'); await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6e6 / 8, uploadThroughput: 750e3 / 8 }); await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
    await p.addInitScript(() => { window.__ls = []; new PerformanceObserver((l) => l.getEntries().forEach((e) => { if (!e.hadRecentInput) window.__ls.push({ v: +e.value.toFixed(4), t: Math.round(e.startTime), src: e.sources.map((s) => { const n = s.node; return n ? (n.nodeType === 1 ? n.tagName.toLowerCase() + (n.id ? '#' + n.id : '') + '.' + String(n.className).slice(0, 25) : '#text:' + n.textContent.slice(0, 30)) + ' ' + JSON.stringify([Math.round(s.previousRect.y), Math.round(s.currentRect.y), Math.round(s.previousRect.height), Math.round(s.currentRect.height)]) : '?'; }) }); })).observe({ type: 'layout-shift', buffered: true }); });

    await p.goto('https://escale.live' + u); await p.waitForTimeout(6000);
    const ls = await p.evaluate(() => window.__ls); console.log(u, 'CLS', ls.reduce((a, x) => a + x.v, 0).toFixed(3)); ls.forEach((x) => console.log('  ', x.v, x.t + 'ms', x.src.join(' ; ')));
    await p.close(); }
  await b.close(); })();
