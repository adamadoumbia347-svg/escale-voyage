import { Env, esc, siteUrl } from "./_lib/common"
import { mailerReady, sendMail, lastMailError } from "./_lib/mail"
import { Month, Point, cacheKey, isLow30, LOW30 } from "./apercu-prix"
import { ROUTES } from "./barometre"
import { deals, whatsappLines } from "./saisir"
// Message WhatsApp de la semaine : chaque lundi matin (tâche quotidienne de wrangler.jsonc), un e-mail avec le message
// des bons plans prêt à copier dans la chaîne WhatsApp. Destinataire : variable DIGEST_TO (Cloudflare > Variables et secrets).
// Prix : relevé du jour (historique KV des pages trajets, mis à jour chaque nuit par src/releve.ts) et dates du cache.
// Aussi envoyable à la demande depuis /admin/ (bouton « Recevoir le message WhatsApp maintenant »). Suivi du bilan de la semaine (weeklyStats).
const CHANNEL = "https://whatsapp.com/channel/0029VbE28kB0LKZN7ypnGj0d"
const DEST: [string, string, string, string, string][] = [
  ["CDG", "DSS", "Dakar", "🇸🇳", "vol-paris-dakar"], ["CDG", "BKO", "Bamako", "🇲🇱", "vol-paris-bamako"],
  ["CDG", "ABJ", "Abidjan", "🇨🇮", "vol-paris-abidjan"], ["CDG", "CKY", "Conakry", "🇬🇳", "vol-paris-conakry"],
  ["CDG", "DLA", "Douala", "🇨🇲", "vol-paris-douala"], ["CDG", "FIH", "Kinshasa", "🇨🇩", "vol-paris-kinshasa"],
  ["CDG", "LFW", "Lomé", "🇹🇬", "vol-paris-lome"], ["CDG", "COO", "Cotonou", "🇧🇯", "vol-paris-cotonou"],
  ["CDG", "OUA", "Ouagadougou", "🇧🇫", "vol-paris-ouagadougou"], ["CDG", "ALG", "Alger", "🇩🇿", "vol-paris-alger"],
  ["CDG", "ORN", "Oran", "🇩🇿", "vol-paris-oran"], ["ORY", "CMN", "Casablanca", "🇲🇦", "vol-paris-casablanca"],
  ["CDG", "RAK", "Marrakech", "🇲🇦", "vol-paris-marrakech"], ["CDG", "TUN", "Tunis", "🇹🇳", "vol-paris-tunis"],
  ["CDG", "DJE", "Djerba", "🇹🇳", "vol-paris-djerba"],
]
const money = (n: number, loc = "fr-FR") => new Intl.NumberFormat(loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n)
const day = (iso: string, loc = "fr-FR") => { const [y, m, d] = iso.split("-").map(Number); return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString(loc, { day: "numeric", month: "short", timeZone: "UTC" }) }

// Textes du message des bons plans dans la langue de l'inscrit (champ « langue » du formulaire)
type Txt = { loc: string; paris: string; head: string; intro: string; from: string; drop: string; ete?: string; baro: string; alert: string; share: string; foot: string;
  subject: string; cta: string; why: string; unsub: string; app: string }
const TXT: Record<string, Txt> = {
  fr: { loc: "fr-FR", paris: "Paris", head: "✈️ *Bons plans Escale* · semaine du {d}", intro: "Allers-retours les moins chers repérés au départ de *Paris* :", from: "dès", drop: "en 7 jours",
    ete: "☀️ Été 2027 : les premiers prix de juillet-août → {b}/vols-ete-2027/", baro: "📊 Baromètre des prix : {b}/barometre-prix/",
    alert: "🔔 Alerte prix gratuite : choisissez votre trajet sur {b} et recevez un e-mail quand le prix baisse.", share: "📢 Partagez la chaîne à vos proches : {c}",
    foot: "_Prix repérés récemment, par personne. Le tarif exact s'affiche sur le site de réservation._", subject: "✈️ Les bons plans vols de la semaine",
    cta: "Comparer les prix en direct", why: "Vous recevez cet e-mail car vous vous êtes inscrit aux bons plans d'Escale.", unsub: "Se désinscrire en un clic", app: "" },
  en: { loc: "en-GB", paris: "Paris", head: "✈️ *Escale deals* · week of {d}", intro: "Cheapest round trips found from *Paris*:", from: "from", drop: "in 7 days",
    baro: "📊 Price barometer: {b}/barometre-prix/", alert: "🔔 Free price alert: pick your route on {b} and get an email when the price drops.",
    share: "📢 Share the channel with your family: {c}", foot: "_Prices found recently, per person. The exact fare is shown on the booking site._",
    subject: "✈️ This week's flight deals", cta: "Compare live prices", why: "You are receiving this email because you signed up for Escale deals.", unsub: "Unsubscribe in one click", app: "en" },
  es: { loc: "es-ES", paris: "París", head: "✈️ *Ofertas Escale* · semana del {d}", intro: "Idas y vueltas más baratas encontradas desde *París*:", from: "desde", drop: "en 7 días",
    baro: "📊 Barómetro de precios: {b}/barometre-prix/", alert: "🔔 Alerta de precio gratuita: elige tu ruta en {b} y recibe un correo cuando baje el precio.",
    share: "📢 Comparte el canal con tu familia: {c}", foot: "_Precios encontrados recientemente, por persona. La tarifa exacta aparece en el sitio de reserva._",
    subject: "✈️ Las ofertas de vuelos de la semana", cta: "Comparar precios en directo", why: "Recibes este correo porque te suscribiste a las ofertas de Escale.", unsub: "Darse de baja en un clic", app: "es" },
  pt: { loc: "pt-PT", paris: "Paris", head: "✈️ *Promoções Escale* · semana de {d}", intro: "Idas e voltas mais baratas encontradas a partir de *Paris*:", from: "desde", drop: "em 7 dias",
    baro: "📊 Barómetro de preços: {b}/barometre-prix/", alert: "🔔 Alerta de preço gratuito: escolha a rota em {b} e receba um e-mail quando o preço baixar.",
    share: "📢 Partilhe o canal com a família: {c}", foot: "_Preços encontrados recentemente, por pessoa. A tarifa exata aparece no site de reserva._",
    subject: "✈️ As promoções de voos da semana", cta: "Comparar preços ao vivo", why: "Recebe este e-mail porque se inscreveu nas promoções da Escale.", unsub: "Cancelar a inscrição num clique", app: "pt" },
  ar: { loc: "ar-u-nu-latn", paris: "باريس", head: "✈️ *عروض Escale* · أسبوع {d}", intro: "أرخص رحلات الذهاب والعودة التي وُجدت من *باريس*:", from: "من", drop: "خلال 7 أيام",
    baro: "📊 مؤشر الأسعار: {b}/barometre-prix/", alert: "🔔 تنبيه سعر مجاني: اختر رحلتك على {b} واستلم بريدًا عندما ينخفض السعر.",
    share: "📢 شارك القناة مع عائلتك: {c}", foot: "_أسعار وُجدت مؤخرًا للشخص الواحد. يظهر السعر الدقيق على موقع الحجز._",
    subject: "✈️ عروض الطيران لهذا الأسبوع", cta: "قارن الأسعار مباشرة", why: "تصلك هذه الرسالة لأنك اشتركت في عروض Escale.", unsub: "إلغاء الاشتراك بنقرة واحدة", app: "ar" },
  it: { loc: "it-IT", paris: "Parigi", head: "✈️ *Offerte Escale* · settimana del {d}", intro: "Andata e ritorno più economici trovati da *Parigi*:", from: "da", drop: "in 7 giorni",
    baro: "📊 Barometro dei prezzi: {b}/barometre-prix/", alert: "🔔 Avviso prezzo gratuito: scegli la tratta su {b} e ricevi un'e-mail quando il prezzo scende.",
    share: "📢 Condividi il canale con la famiglia: {c}", foot: "_Prezzi trovati di recente, a persona. La tariffa esatta appare sul sito di prenotazione._",
    subject: "✈️ Le offerte voli della settimana", cta: "Confronta i prezzi in diretta", why: "Ricevi questa e-mail perché ti sei iscritto alle offerte di Escale.", unsub: "Annulla l'iscrizione con un clic", app: "it" },
  de: { loc: "de-DE", paris: "Paris", head: "✈️ *Escale-Angebote* · Woche vom {d}", intro: "Günstigste Hin- und Rückflüge ab *Paris*:", from: "ab", drop: "in 7 Tagen",
    baro: "📊 Preisbarometer: {b}/barometre-prix/", alert: "🔔 Kostenloser Preisalarm: Wähle deine Strecke auf {b} und erhalte eine E-Mail, wenn der Preis fällt.",
    share: "📢 Teile den Kanal mit deiner Familie: {c}", foot: "_Kürzlich gefundene Preise pro Person. Der genaue Tarif erscheint auf der Buchungsseite._",
    subject: "✈️ Die Flugangebote der Woche", cta: "Live-Preise vergleichen", why: "Du erhältst diese E-Mail, weil du dich für die Angebote von Escale angemeldet hast.", unsub: "Mit einem Klick abmelden", app: "de" },
  nl: { loc: "nl-NL", paris: "Parijs", head: "✈️ *Escale-deals* · week van {d}", intro: "Goedkoopste retourvluchten gevonden vanuit *Parijs*:", from: "vanaf", drop: "in 7 dagen",
    baro: "📊 Prijsbarometer: {b}/barometre-prix/", alert: "🔔 Gratis prijsalert: kies je route op {b} en ontvang een e-mail als de prijs daalt.",
    share: "📢 Deel het kanaal met je familie: {c}", foot: "_Onlangs gevonden prijzen, per persoon. Het exacte tarief zie je op de boekingssite._",
    subject: "✈️ De vluchtdeals van de week", cta: "Live prijzen vergelijken", why: "Je ontvangt deze e-mail omdat je je hebt aangemeld voor de deals van Escale.", unsub: "Met één klik afmelden", app: "en" },
}

// E-mail de bienvenue envoyé dès l'inscription aux bons plans : [objet, première ligne]
const WELCOME: Record<string, [string, string]> = {
  fr: ["Bienvenue sur Escale ✈️", "Bienvenue ! Voici les bons plans du moment. Le prochain message arrive lundi."],
  en: ["Welcome to Escale ✈️", "Welcome! Here are the current deals. The next message arrives on Monday."],
  es: ["Bienvenido a Escale ✈️", "¡Bienvenido! Estas son las ofertas del momento. El próximo mensaje llega el lunes."],
  pt: ["Bem-vindo à Escale ✈️", "Bem-vindo! Aqui estão as promoções do momento. A próxima mensagem chega na segunda-feira."],
  ar: ["مرحبًا بك في Escale ✈️", "مرحبًا! هذه عروض اللحظة. الرسالة القادمة تصل يوم الاثنين."],
  it: ["Benvenuto su Escale ✈️", "Benvenuto! Ecco le offerte del momento. Il prossimo messaggio arriva lunedì."],
  de: ["Willkommen bei Escale ✈️", "Willkommen! Hier sind die aktuellen Angebote. Die nächste Nachricht kommt am Montag."],
  nl: ["Welkom bij Escale ✈️", "Welkom! Dit zijn de deals van dit moment. Het volgende bericht komt maandag."],
}
// Villes de départ proposées dans les bons plans : celles qui ont assez de trajets relevés chaque nuit (src/barometre.ts). Paris par défaut.
const ORIGINS = ["LHR", "MXP", "FCO"]
export const originOf = (code: unknown) => (ORIGINS.includes(String(code || "").toUpperCase()) ? String(code).toUpperCase() : "CDG")
const FLAGS: Record<string, string> = { LOS: "🇳🇬", ABV: "🇳🇬", ACC: "🇬🇭", NBO: "🇰🇪", ADD: "🇪🇹", CAI: "🇪🇬", JNB: "🇿🇦", CPT: "🇿🇦", CMN: "🇲🇦", DSS: "🇸🇳", ABJ: "🇨🇮", TUN: "🇹🇳", ALG: "🇩🇿", RAK: "🇲🇦", DLA: "🇨🇲", FIH: "🇨🇩", BKO: "🇲🇱", CKY: "🇬🇳", EBB: "🇺🇬", DAR: "🇹🇿", KGL: "🇷🇼", LAD: "🇦🇴", FNA: "🇸🇱", BJL: "🇬🇲", HRE: "🇿🇼", LUN: "🇿🇲", MRU: "🇲🇺", ZNZ: "🇹🇿", TNG: "🇲🇦", AGA: "🇲🇦", FEZ: "🇲🇦", ORN: "🇩🇿", DJE: "🇹🇳" }
// Noms de villes qui changent selon la langue (les autres restent identiques)
const CITY_L: Record<string, Record<string, string>> = {
  Alger: { en: "Algiers", es: "Argel", pt: "Argel", ar: "الجزائر", it: "Algeri", de: "Algier", nl: "Algiers" },
  Tunis: { es: "Túnez", pt: "Tunes", ar: "تونس", it: "Tunisi" }, Dakar: { ar: "داكار" }, Abidjan: { ar: "أبيدجان", es: "Abiyán" },
  Casablanca: { ar: "الدار البيضاء" }, Marrakech: { ar: "مراكش", de: "Marrakesch", en: "Marrakesh" }, Oran: { ar: "وهران", es: "Orán", it: "Orano" },
  "Le Caire": { en: "Cairo", es: "El Cairo", pt: "Cairo", ar: "القاهرة", it: "Il Cairo", de: "Kairo", nl: "Caïro" },
  "Addis-Abeba": { en: "Addis Ababa", es: "Adís Abeba", pt: "Adis Abeba", ar: "أديس أبابا", it: "Addis Abeba", de: "Addis Abeba", nl: "Addis Abeba" },
  Johannesburg: { es: "Johannesburgo", pt: "Joanesburgo", ar: "جوهانسبرغ" }, Lagos: { ar: "لاغوس" }, Accra: { ar: "أكرا" }, Nairobi: { ar: "نيروبي" }, Abuja: { ar: "أبوجا", es: "Abuya" },
  Londres: { en: "London", ar: "لندن", it: "Londra", de: "London", nl: "Londen" }, Milan: { es: "Milán", pt: "Milão", ar: "ميلانو", it: "Milano", de: "Mailand", nl: "Milaan" },
  Rome: { es: "Roma", pt: "Roma", ar: "روما", it: "Roma", de: "Rom" },
  Bamako: { ar: "باماكو" }, Kinshasa: { ar: "كينشاسا", es: "Kinsasa" }, Djerba: { ar: "جربة", es: "Yerba", it: "Gerba" },
}

export async function buildMessage(env: Env, lang = "fr", origin = "CDG") {
  const t = TXT[lang] || TXT.fr
  // Paris : la liste historique ; Londres, Milan, Rome : les trajets relevés chaque nuit au départ de cette ville
  const paris = origin === "CDG"
  const list: [string, string, string, string, string][] = paris ? DEST : ROUTES.filter((r) => r[0] === origin).map(([from, to, label, path]) => [from, to, label.split(" → ")[1] || to, FLAGS[to] || "✈️", path])
  const homeFr = ROUTES.find((r) => r[0] === origin)?.[2].split(" → ")[0] || origin
  const home = paris ? t.paris : ((CITY_L[homeFr] || {})[lang] || homeFr)
  const cache = (globalThis as any).caches?.default
  const since = new Date(Date.now() - 3 * 864e5).toISOString().slice(0, 10)
  const rows = (await Promise.all(list.map(async ([from, to, city, flag, path]) => {
    const hist = ((await env.ESCALE?.get(`hist:${from}-${to}`, "json")) as Point[] | null) || []
    const last = hist.length ? hist[hist.length - 1] : null
    const hit = cache ? await cache.match(cacheKey(from, to)) : null
    const months: Month[] = hit ? await hit.json() : []
    const best = months.length ? months.reduce((a, b) => (b.price < a.price ? b : a)) : null
    const price = best ? best.price : last && last[0] >= since ? last[1] : null
    if (!price) return null
    const week = hist.find(([d]) => d >= new Date(Date.now() - 8 * 864e5).toISOString().slice(0, 10))
    const trend = week && week[1] && week[0] < since ? Math.round((price / week[1] - 1) * 100) : null
    return { city, flag, path, price, best, trend, from, to, low: isLow30(hist, price) }
  }))).filter(Boolean).sort((a: any, b: any) => a.price - b.price) as any[]
  const today = new Date().toLocaleDateString(t.loc, { day: "numeric", month: "long", timeZone: "Europe/Paris" })
  const base = siteUrl(env).replace(/^https?:\/\//, "")
  const sep = lang === "fr" ? " : " : ": "
  const lines = [t.head.replace("{d}", today), "", t.intro.replace(`*${t.paris}*`, `*${home}*`), ""]
  for (const r of rows) {
    const dates = r.best && r.best.ret ? ` (${day(r.best.dep, t.loc)} → ${day(r.best.ret, t.loc)})` : ""
    const tr = r.trend !== null && r.trend <= -5 ? ` 📉 ${r.trend} % ${t.drop}` : ""
    const city = (CITY_L[r.city] || {})[lang] || r.city
    // En français : la page trajet ; dans les autres langues : la recherche, déjà dans la bonne langue
    const { from, to } = r
    const link = lang === "fr" && paris ? `${base}/${r.path}/` : `${base}/?type=vols&from=${from}&to=${to}${t.app ? "&lang=" + t.app : ""}`
    const low = r.low ? ` 🏆 ${LOW30[lang] || LOW30.fr}` : ""
    lines.push(`${r.flag} ${home} → ${city}${sep}*${t.from} ${money(r.price, t.loc)}*${dates}${tr}${low}`, `   👉 ${link}`)
  }
  // Trajets nettement sous leur prix habituel (src/saisir.ts), en français seulement
  if (lang === "fr") { try { lines.push("", ...whatsappLines(await deals(env), base).slice(0, -1)) } catch {} }
  lines.push("", ...(t.ete ? [t.ete.replace("{b}", base)] : []), t.baro.replace("{b}", base), t.alert.replace("{b}", base), t.share.replace("{c}", CHANNEL), "", t.foot)
  return { count: rows.length, text: lines.join("\n") }
}

// Bilan de la semaine (ajouté à l'e-mail du lundi) : clics des 7 derniers jours comparés aux 7 précédents (compteur anonyme
// de site/clics.js, clés clics:AAAA-MM-JJ), pages d'où partent les clics, inscrits aux bons plans et alertes prix actives.
const LINKS: Record<string, string> = { "moteur-resultat": "Vols choisis dans la recherche en direct", "moteur-lien": "Ouvertures de la recherche en direct",
  "trajet-populaire": "Trajets populaires (accueil)", "bandeau-saison": "Bandeau de saison", aviasales: "Aviasales", stay22: "Hôtels (Stay22)", tripcom: "Trip.com (vols et hôtels)", "tripcom-package": "Vol + hôtel (Trip.com)",
  whatsapp: "Chaîne WhatsApp", "whatsapp-bulle": "Bulle WhatsApp", "partage-whatsapp": "Partages sur WhatsApp", booking: "Booking", google: "Google Hôtels / Vols",
  airbnb: "Airbnb", agoda: "Agoda", kayak: "Kayak", skyscanner: "Skyscanner", momondo: "momondo", "autre-site": "Autres sites" }
const PAGES: Record<string, string> = { accueil: "Accueil", recherche: "Recherche en direct", trajet: "Pages trajets", destination: "Pages destinations", ete: "Pages été 2027", autre: "Autres pages" }

async function countKeys(env: Env, prefix: string) {
  let n = 0, cursor: string | undefined
  do { const page: any = await env.ESCALE.list({ prefix, cursor, limit: 1000 }); n += page.keys.length; cursor = page.list_complete ? undefined : page.cursor } while (cursor && n < 50000)
  return n
}

export async function weeklyStats(env: Env) {
  if (!env.ESCALE) return null
  const days = Array.from({ length: 14 }, (_, i) => new Date(Date.now() - (i + 1) * 864e5).toISOString().slice(0, 10))
  const rows = await Promise.all(days.map((d) => env.ESCALE.get("clics:" + d, "json")))
  const links: Record<string, [number, number]> = {}, pages: Record<string, number> = {}
  let now = 0, before = 0
  rows.forEach((r: any, i) => { for (const [id, n] of Object.entries(r || {})) {
    const [k, p] = id.split("|"), v = n as number, o = links[k] || (links[k] = [0, 0])
    if (i < 7) { o[0] += v; now += v; pages[p] = (pages[p] || 0) + v } else { o[1] += v; before += v }
  } })
  const [subs, alerts] = await Promise.all([countKeys(env, "form:bons-plans:"), countKeys(env, "alert:")])
  return { now, before, links, pages, subs, alerts, from: days[6], to: days[0] }
}

function statsHtml(s: NonNullable<Awaited<ReturnType<typeof weeklyStats>>>) {
  const evo = (a: number, b: number) => !b ? (a ? "nouveau" : "–") : `${a >= b ? "+" : ""}${Math.round((a / b - 1) * 100)} %`
  const td = "padding:6px 10px;border-bottom:1px solid #e3e8ef"
  const top = Object.entries(s.links).filter(([, v]) => v[0] || v[1]).sort((a, b) => b[1][0] - a[1][0]).slice(0, 10)
  const pg = Object.entries(s.pages).sort((a, b) => b[1] - a[1]).slice(0, 5)
  return `<h2 style="margin:28px 0 6px">Bilan de la semaine</h2><p style="color:#5b6b80;margin:0 0 10px">Du ${day(s.from)} au ${day(s.to)}, comparé aux 7 jours précédents.</p>` +
    `<p style="font-size:17px"><strong>${s.now} clics</strong> vers les partenaires et la recherche (${evo(s.now, s.before)}) · <strong>${s.subs}</strong> inscrits aux bons plans · <strong>${s.alerts}</strong> alertes prix actives</p>` +
    (top.length ? `<table style="border-collapse:collapse;width:100%;font-size:14px"><tr><th style="${td};text-align:left">Lien</th><th style="${td};text-align:right">7 jours</th><th style="${td};text-align:right">Évolution</th></tr>` +
      top.map(([k, v]) => `<tr><td style="${td}">${esc(LINKS[k] || k)}</td><td style="${td};text-align:right">${v[0]}</td><td style="${td};text-align:right">${evo(v[0], v[1])}</td></tr>`).join("") + `</table>` : `<p>Aucun clic enregistré cette semaine.</p>`) +
    (pg.length ? `<p style="margin-top:12px"><strong>Pages d'où partent les clics :</strong> ${pg.map(([p, n]) => `${esc(PAGES[p] || p)} (${n})`).join(" · ")}</p>` : "") +
    `<p style="color:#5b6b80;font-size:13px">Visiteurs et pages vues : Cloudflare › Web Analytics. Ventes : Travelpayouts et Stay22.</p>`
}

export async function sendDigest(env: Env) {
  const to = ((env as any).DIGEST_TO || "").trim()
  if (!to) return { sent: false, reason: "DIGEST_TO absent" }
  if (!mailerReady(env)) return { sent: false, reason: "envoi d'e-mails non configuré" }
  const m = await buildMessage(env)
  if (!m.count) return { sent: false, reason: "aucun prix relevé" }
  const st = await weeklyStats(env).catch(() => null)
  const html = `<div style="font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:640px;color:#0d1b2e">` +
    `<h2 style="margin:0 0 8px">Message WhatsApp à coller dans la chaîne</h2>` +
    `<p>1. Sélectionnez le texte dans le cadre et copiez-le.<br>2. WhatsApp → Actualités → chaîne Escale → collez → envoyez.</p>` +
    `<pre style="white-space:pre-wrap;font:15px/1.5 system-ui,sans-serif;background:#f3f6fa;border:1px solid #dde3ec;border-radius:10px;padding:14px">${esc(m.text)}</pre>` +
    `<p><a href="${CHANNEL}">Ouvrir la chaîne WhatsApp</a> · <a href="${siteUrl(env)}/outils/whatsapp/">Préparer un autre message (Lyon, Marseille, Bruxelles…)</a></p>` +
    (st ? statsHtml(st) : "") +
    `<p style="color:#5b6b80;font-size:13px">E-mail automatique d'Escale, envoyé chaque lundi et jeudi à ${esc(to)}.</p></div>`
  const ok = await sendMail(env, to, `Message WhatsApp et bilan de la semaine${st ? ` (${st.now} clics)` : ""}`, html)
  return { sent: ok, to, count: m.count, ...(ok ? {} : { detail: lastMailError }) }
}

// E-mail des bons plans aux inscrits (formulaire « Recevez les bons plans » : clés form:bons-plans:… avec e-mail et consentement).
// Envoyé le lundi avec la tâche quotidienne, au plus une fois tous les 6 jours par personne, 40 envois au plus par passage
// (le reste part au passage suivant). Chaque e-mail contient un lien de désinscription en un clic (/api/form?action=desinscription).
export async function unsubToken(env: Env, id: string) {
  const secret = (env.ADMIN_KEY || env.CRON_KEY || "escale") + ":desinscription"
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"])
  const sig = await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(id))
  return [...new Uint8Array(sig)].slice(0, 16).map((b) => b.toString(16).padStart(2, "0")).join("")
}

const linkify = (t: string) => esc(t).replace(/(https?:\/\/[^\s<]+|escale\.live\/[^\s<]*)/g, (u) => `<a href="${u.startsWith("http") ? u : "https://" + u}">${u}</a>`)
  .replace(/\*([^*\n]+)\*/g, "<strong>$1</strong>").replace(/_([^_\n]+)_/g, "<em>$1</em>").replace(/\n/g, "<br>")

// Ligne « ton trajet » en tête des bons plans : le trajet de la page où la personne s'est inscrite, s'il est relevé chaque nuit
const MINE: Record<string, string> = {"fr": "🎯 Ton trajet", "en": "🎯 Your route", "es": "🎯 Tu ruta", "pt": "🎯 O seu trajeto", "ar": "🎯 رحلتك", "it": "🎯 La tua tratta", "de": "🎯 Deine Strecke", "nl": "🎯 Jouw route"}
export async function routeLine(env: Env, lang: string, from: unknown, to: unknown) {
  const f = String(from || "").toUpperCase(), d = String(to || "").toUpperCase()
  const r = ROUTES.find((x) => x[0] === f && x[1] === d)
  if (!r || !env.ESCALE) return ""
  const hist = ((await env.ESCALE.get(`hist:${f}-${d}`, "json").catch(() => null)) as Point[] | null) || []
  const last = hist[hist.length - 1]
  if (!last || last[0] < new Date(Date.now() - 3 * 864e5).toISOString().slice(0, 10)) return ""
  const t = TXT[lang] || TXT.fr, [a, b] = r[2].split(" → ").map((c) => (CITY_L[c] || {})[lang] || c)
  const week = hist.find(([day]) => day >= new Date(Date.now() - 8 * 864e5).toISOString().slice(0, 10))
  const trend = week && week[1] && week[0] < last[0] ? Math.round((last[1] / week[1] - 1) * 100) : null
  const tr = trend !== null && trend <= -5 ? ` 📉 ${trend} % ${t.drop}` : ""
  const low = isLow30(hist, last[1]) ? ` 🏆 ${LOW30[lang] || LOW30.fr}` : ""
  const base = siteUrl(env).replace(/^https?:\/\//, "")
  return `${MINE[lang] || MINE.fr}${lang === "fr" ? " : " : ": "}${a} → ${b}, *${t.from} ${money(last[1], t.loc)}*${tr}${low}\n   👉 ${base}/?type=vols&from=${f}&to=${d}${t.app ? "&lang=" + t.app : ""}`
}
// Place la ligne « ton trajet » juste après le titre du message
const withMine = (text: string, mine: string) => (mine ? text.replace("\n\n", `\n\n${mine}\n\n`) : text)

// Corps HTML commun aux bons plans du lundi et à l'e-mail de bienvenue
async function dealsHtml(env: Env, name: string, lang: string, text: string, top = "") {
  const t = TXT[lang] || TXT.fr, base = siteUrl(env)
  const unsub = `${base}/api/form?action=desinscription&id=${encodeURIComponent(name)}&t=${await unsubToken(env, name)}`
  const home = lang === "fr" ? `${base}/` : `${base}/?lang=${t.app}`
  return `<div dir="${lang === "ar" ? "rtl" : "ltr"}" lang="${lang}" style="font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:620px;color:#0d1b2e;font-size:15px;line-height:1.55">` +
    (top ? `<p style="font-weight:700">${esc(top)}</p>` : "") +
    `<p>${linkify(text)}</p>` +
    `<p style="margin-top:24px"><a href="${home}" style="background:#1a56db;color:#fff;padding:10px 18px;border-radius:999px;text-decoration:none;font-weight:700">${esc(t.cta)}</a></p>` +
    `<p style="color:#5b6b80;font-size:12px;margin-top:28px">${esc(t.why)} ` +
    `<a href="${unsub}" style="color:#5b6b80">${esc(t.unsub)}</a>.</p></div>`
}
const langOf = (rec: any) => (TXT[String(rec?.fields?.langue || "").slice(0, 2)] ? String(rec.fields.langue).slice(0, 2) : "fr")

// E-mail de bienvenue : envoyé dès l'inscription (src/api/form.ts), avec les bons plans du moment au départ de la ville de l'inscrit
export async function sendWelcome(env: Env, name: string) {
  if (!mailerReady(env) || !env.ESCALE) return false
  const rec: any = await env.ESCALE.get(name, "json")
  const email = rec?.fields?.email
  if (!email || !/^\S+@\S+\.\S+$/.test(email) || !rec.fields.consent || rec.unsubscribed || rec.welcomed) return false
  const lang = langOf(rec), origin = originOf(rec.fields.depart)
  let m = await buildMessage(env, lang, origin)
  if (!m.count && origin !== "CDG") m = await buildMessage(env, lang)
  if (!m.count) return false
  const w = WELCOME[lang] || WELCOME.fr
  const mine = await routeLine(env, lang, rec.fields.depart, rec.fields.arrivee)
  if (!(await sendMail(env, email, w[0], await dealsHtml(env, name, lang, withMine(m.text, mine), w[1])))) return false
  rec.welcomed = new Date().toISOString()
  await env.ESCALE.put(name, JSON.stringify(rec))
  return true
}

export async function sendNewsletter(env: Env) {
  if (!mailerReady(env) || !env.ESCALE) return { sent: 0, reason: "envoi d'e-mails non configuré" }
  const msgs: Record<string, Awaited<ReturnType<typeof buildMessage>>> = {}
  const msg = async (l: string, o = "CDG") => (msgs[l + o] ||= await buildMessage(env, l, o))
  if (!(await msg("fr")).count) return { sent: 0, reason: "aucun prix relevé" }
  const now = Date.now()
  let sent = 0, cursor: string | undefined
  do {
    const page: any = await env.ESCALE.list({ prefix: "form:bons-plans:", cursor, limit: 1000 })
    for (const { name } of page.keys) {
      if (sent >= 40) return { sent, more: true }
      const rec: any = await env.ESCALE.get(name, "json")
      const email = rec?.fields?.email, consent = rec?.fields?.consent
      if (!email || !/^\S+@\S+\.\S+$/.test(email) || !consent || rec.unsubscribed) continue
      if (rec.lastNewsletter && now - Date.parse(rec.lastNewsletter) < 6 * 864e5) continue
      // Inscrit depuis moins de 2 jours : il vient de recevoir les mêmes prix dans l'e-mail de bienvenue
      if (rec.welcomed && now - Date.parse(rec.welcomed) < 2 * 864e5) continue
      // Langue et ville de départ de l'inscrit (page où il s'est inscrit) ; français et Paris par défaut
      const lang = langOf(rec), t = TXT[lang], origin = originOf(rec.fields.depart)
      let m = await msg(lang, origin)
      if (!m.count) m = await msg(lang)
      const mine = await routeLine(env, lang, rec.fields.depart, rec.fields.arrivee)
      if (await sendMail(env, email, t.subject, await dealsHtml(env, name, lang, withMine(m.text, mine)))) {
        rec.lastNewsletter = new Date().toISOString()
        await env.ESCALE.put(name, JSON.stringify(rec))
        sent++
      }
    }
    cursor = page.list_complete ? undefined : page.cursor
  } while (cursor)
  return { sent }
}
