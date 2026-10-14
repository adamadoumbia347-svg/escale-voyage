// Génère une image de partage (1200x630, JPEG) par trajet dans site/og/ORIG-DEST.jpg.
// Usage : node scripts/make_og.js   (nécessite Playwright ; les images existantes sont conservées)
const fs = require("fs"), path = require("path");
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) { ({ chromium } = require(path.join(process.env.NPM_G || "", "playwright"))); }
const root = path.join(__dirname, "..", "site");
const routes = JSON.parse(fs.readFileSync(path.join(root, "data", "routes.json"), "utf8"));
const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const page = (a, b, ca, cb) => `<!doctype html><html><head><meta charset="utf-8"><style>
  body{margin:0;width:1200px;height:630px;background:#18202c;color:#f3f5f8;font-family:"DejaVu Sans",Arial,sans-serif;display:flex;flex-direction:column;justify-content:space-between;padding:64px 72px;box-sizing:border-box}
  .brand{display:flex;align-items:center;gap:18px;font-size:34px;font-weight:700}
  .mark{background:#ffcc1a;color:#18202c;padding:10px 14px;border-radius:10px;font-weight:800}
  .codes{display:flex;align-items:center;gap:28px;font-family:"DejaVu Sans Mono",monospace;font-weight:700;font-size:150px;letter-spacing:6px}
  .codes span{color:#ffcc1a;font-size:110px}
  .cities{font-size:52px;font-weight:700;margin-top:6px}
  .foot{white-space:nowrap;display:flex;justify-content:space-between;align-items:center;font-size:30px;color:#c9d1dd}
  .cta{background:#ffcc1a;color:#18202c;font-weight:800;padding:16px 26px;border-radius:12px}
</style></head><body>
  <div class="brand"><span class="mark">ESC</span>Escale</div>
  <div><div class="codes">${esc(a)}<span>→</span>${esc(b)}</div><div class="cities">${esc(ca)} → ${esc(cb)}</div></div>
  <div class="foot"><span>Google Flights · Skyscanner · Kayak</span><span class="cta">Comparer les prix</span></div>
</body></html>`;
(async () => {
  fs.mkdirSync(path.join(root, "og"), { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  let made = 0;
  for (const [a, bb, ca, cb] of routes) {
    const out = path.join(root, "og", `${a}-${bb}.jpg`);
    if (fs.existsSync(out)) continue;
    await p.setContent(page(a, bb, ca, cb));
    await p.screenshot({ path: out, type: "jpeg", quality: 82 });
    made++;
  }
  await b.close();
  console.log(`${made} images créées, ${routes.length} trajets au total`);
})();
