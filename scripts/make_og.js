// Génère une image de partage (1200x630, JPEG) par trajet dans site/og/ORIG-DEST.jpg.
// Usage : node scripts/make_og.js [--all]   (nécessite Playwright ; sans --all, les images existantes sont conservées)
const fs = require("fs"), path = require("path");
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) { ({ chromium } = require(path.join(process.env.NPM_G || "", "playwright"))); }
const root = path.join(__dirname, "..", "site");
const routes = JSON.parse(fs.readFileSync(path.join(root, "data", "routes.json"), "utf8"));
const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
// Aux couleurs du site (vert Escale) avec le logo ; aucune marque tierce. Texte neutre (codes, villes, escale.live) : sert à toutes les langues.
const ICON = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#19c7b1"/><stop offset="1" stop-color="#0b8577"/></linearGradient></defs><rect width="64" height="64" rx="15" fill="url(#g)"/><g transform="translate(32 32) rotate(45) translate(-17 -17) scale(1.4167)"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z" fill="#fff"/></g></svg>`.replace("<svg ", '<svg width="96" height="96" ');
const page = (a, b, ca, cb) => `<!doctype html><html><head><meta charset="utf-8"><style>
  body{margin:0;width:1200px;height:630px;background:linear-gradient(135deg,#0b8577 0%,#0a5d58 55%,#08303a 100%);color:#fff;font-family:"DejaVu Sans",Arial,sans-serif;display:flex;flex-direction:column;justify-content:space-between;padding:60px 72px;box-sizing:border-box;position:relative;overflow:hidden}
  body:after{content:"";position:absolute;right:-120px;top:-120px;width:520px;height:520px;border-radius:50%;background:rgba(255,255,255,.06)}
  .brand{display:flex;align-items:center;gap:22px;font-size:46px;font-weight:700;letter-spacing:-1px}
  .brand b{color:#7ff3de;font-weight:700}
  .codes{display:flex;align-items:center;gap:30px;font-weight:700;font-size:148px;letter-spacing:4px;line-height:1}
  .codes span{color:#7ff3de;font-size:112px}
  .cities{font-size:54px;font-weight:700;margin-top:18px;opacity:.95}
  .foot{display:flex;justify-content:space-between;align-items:center;font-size:30px}
  .foot i{font-style:normal;opacity:.85}
  .cta{background:#fff;color:#0a5d58;font-weight:800;padding:16px 28px;border-radius:999px;font-size:32px}
</style></head><body>
  <div class="brand">${ICON}<span>escale<b>.live</b></span></div>
  <div><div class="codes">${esc(a)}<span>→</span>${esc(b)}</div><div class="cities">${esc(ca)} → ${esc(cb)}</div></div>
  <div class="foot"><i>✈ 🏨 🚗</i><span class="cta">escale.live</span></div>
</body></html>`;
const FORCE = process.argv.includes("--all");
(async () => {
  fs.mkdirSync(path.join(root, "og"), { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  let made = 0;
  for (const [a, bb, ca, cb] of routes) {
    const out = path.join(root, "og", `${a}-${bb}.jpg`);
    if (!FORCE && fs.existsSync(out)) continue;
    await p.setContent(page(a, bb, ca, cb));
    await p.screenshot({ path: out, type: "jpeg", quality: 72 });
    made++;
  }
  await b.close();
  console.log(`${made} images créées, ${routes.length} trajets au total`);
})();
