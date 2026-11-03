import { Env, esc, siteUrl } from "./_lib/common"
import { mailerReady, sendMail, lastMailError } from "./_lib/mail"
import { Month, Point, cacheKey } from "./apercu-prix"
// Message WhatsApp de la semaine : chaque lundi matin (tâche quotidienne de wrangler.jsonc), un e-mail avec le message
// des bons plans prêt à copier dans la chaîne WhatsApp. Destinataire : variable DIGEST_TO (Cloudflare > Variables et secrets).
// Prix : relevé du jour (historique KV des pages trajets, mis à jour chaque matin par releve-prix.yml) et dates du cache.
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
// Noms de villes qui changent selon la langue (les autres restent identiques)
const CITY_L: Record<string, Record<string, string>> = {
  Alger: { en: "Algiers", es: "Argel", pt: "Argel", ar: "الجزائر", it: "Algeri", de: "Algier", nl: "Algiers" },
  Tunis: { es: "Túnez", pt: "Tunes", ar: "تونس", it: "Tunisi" }, Dakar: { ar: "داكار" }, Abidjan: { ar: "أبيدجان", es: "Abiyán" },
  Casablanca: { ar: "الدار البيضاء" }, Marrakech: { ar: "مراكش", de: "Marrakesch", en: "Marrakesh" }, Oran: { ar: "وهران", es: "Orán", it: "Orano" },
  Bamako: { ar: "باماكو" }, Kinshasa: { ar: "كينشاسا", es: "Kinsasa" }, Djerba: { ar: "جربة", es: "Yerba", it: "Gerba" },
}

export async function buildMessage(env: Env, lang = "fr") {
  const t = TXT[lang] || TXT.fr
  const cache = (globalThis as any).caches?.default
  const since = new Date(Date.now() - 3 * 864e5).toISOString().slice(0, 10)
  const rows = (await Promise.all(DEST.map(async ([from, to, city, flag, path]) => {
    const hist = ((await env.ESCALE?.get(`hist:${from}-${to}`, "json")) as Point[] | null) || []
    const last = hist.length ? hist[hist.length - 1] : null
    const hit = cache ? await cache.match(cacheKey(from, to)) : null
    const months: Month[] = hit ? await hit.json() : []
    const best = months.length ? months.reduce((a, b) => (b.price < a.price ? b : a)) : null
    const price = best ? best.price : last && last[0] >= since ? last[1] : null
    if (!price) return null
    const week = hist.find(([d]) => d >= new Date(Date.now() - 8 * 864e5).toISOString().slice(0, 10))
    const trend = week && week[1] && week[0] < since ? Math.round((price / week[1] - 1) * 100) : null
    return { city, flag, path, price, best, trend }
  }))).filter(Boolean).sort((a: any, b: any) => a.price - b.price) as any[]
  const today = new Date().toLocaleDateString(t.loc, { day: "numeric", month: "long", timeZone: "Europe/Paris" })
  const base = siteUrl(env).replace(/^https?:\/\//, "")
  const sep = lang === "fr" ? " : " : ": "
  const lines = [t.head.replace("{d}", today), "", t.intro, ""]
  for (const r of rows) {
    const dates = r.best && r.best.ret ? ` (${day(r.best.dep, t.loc)} → ${day(r.best.ret, t.loc)})` : ""
    const tr = r.trend !== null && r.trend <= -5 ? ` 📉 ${r.trend} % ${t.drop}` : ""
    const city = (CITY_L[r.city] || {})[lang] || r.city
    // En français : la page trajet ; dans les autres langues : la recherche, déjà dans la bonne langue
    const [from, to] = DEST.find((d) => d[4] === r.path)!.slice(0, 2)
    const link = lang === "fr" ? `${base}/${r.path}/` : `${base}/?type=vols&from=${from}&to=${to}&lang=${t.app}`
    lines.push(`${r.flag} ${t.paris} → ${city}${sep}*${t.from} ${money(r.price, t.loc)}*${dates}${tr}`, `   👉 ${link}`)
  }
  lines.push("", ...(t.ete ? [t.ete.replace("{b}", base)] : []), t.baro.replace("{b}", base), t.alert.replace("{b}", base), t.share.replace("{c}", CHANNEL), "", t.foot)
  return { count: rows.length, text: lines.join("\n") }
}

// Bilan de la semaine (ajouté à l'e-mail du lundi) : clics des 7 derniers jours comparés aux 7 précédents (compteur anonyme
// de site/clics.js, clés clics:AAAA-MM-JJ), pages d'où partent les clics, inscrits aux bons plans et alertes prix actives.
const LINKS: Record<string, string> = { "moteur-resultat": "Vols choisis dans la recherche en direct", "moteur-lien": "Ouvertures de la recherche en direct",
  "trajet-populaire": "Trajets populaires (accueil)", "bandeau-saison": "Bandeau de saison", aviasales: "Aviasales", stay22: "Hôtels (Stay22)", tripcom: "Hôtels (Trip.com)",
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
    `<h2 style="margin:0 0 8px">Message WhatsApp de la semaine</h2>` +
    `<p>1. Sélectionnez le texte dans le cadre et copiez-le.<br>2. WhatsApp → Actualités → chaîne Escale → collez → envoyez.</p>` +
    `<pre style="white-space:pre-wrap;font:15px/1.5 system-ui,sans-serif;background:#f3f6fa;border:1px solid #dde3ec;border-radius:10px;padding:14px">${esc(m.text)}</pre>` +
    `<p><a href="${CHANNEL}">Ouvrir la chaîne WhatsApp</a> · <a href="${siteUrl(env)}/outils/whatsapp/">Préparer un autre message (Lyon, Marseille, Bruxelles…)</a></p>` +
    (st ? statsHtml(st) : "") +
    `<p style="color:#5b6b80;font-size:13px">E-mail automatique d'Escale, envoyé chaque lundi à ${esc(to)}.</p></div>`
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

export async function sendNewsletter(env: Env) {
  if (!mailerReady(env) || !env.ESCALE) return { sent: 0, reason: "envoi d'e-mails non configuré" }
  const msgs: Record<string, Awaited<ReturnType<typeof buildMessage>>> = {}
  const msg = async (l: string) => (msgs[l] ||= await buildMessage(env, l))
  if (!(await msg("fr")).count) return { sent: 0, reason: "aucun prix relevé" }
  const base = siteUrl(env), now = Date.now()
  let sent = 0, cursor: string | undefined
  do {
    const page: any = await env.ESCALE.list({ prefix: "form:bons-plans:", cursor, limit: 1000 })
    for (const { name } of page.keys) {
      if (sent >= 40) return { sent, more: true }
      const rec: any = await env.ESCALE.get(name, "json")
      const email = rec?.fields?.email, consent = rec?.fields?.consent
      if (!email || !/^\S+@\S+\.\S+$/.test(email) || !consent || rec.unsubscribed) continue
      if (rec.lastNewsletter && now - Date.parse(rec.lastNewsletter) < 6 * 864e5) continue
      // Langue de l'inscrit (page où il s'est inscrit) ; français par défaut
      const lang = TXT[String(rec?.fields?.langue || "").slice(0, 2)] ? String(rec.fields.langue).slice(0, 2) : "fr", t = TXT[lang], m = await msg(lang)
      const unsub = `${base}/api/form?action=desinscription&id=${encodeURIComponent(name)}&t=${await unsubToken(env, name)}`
      const home = lang === "fr" ? `${base}/` : `${base}/?lang=${t.app}`
      const html = `<div dir="${lang === "ar" ? "rtl" : "ltr"}" lang="${lang}" style="font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:620px;color:#0d1b2e;font-size:15px;line-height:1.55">` +
        `<p>${linkify(m.text)}</p>` +
        `<p style="margin-top:24px"><a href="${home}" style="background:#1a56db;color:#fff;padding:10px 18px;border-radius:999px;text-decoration:none;font-weight:700">${esc(t.cta)}</a></p>` +
        `<p style="color:#5b6b80;font-size:12px;margin-top:28px">${esc(t.why)} ` +
        `<a href="${unsub}" style="color:#5b6b80">${esc(t.unsub)}</a>.</p></div>`
      if (await sendMail(env, email, t.subject, html)) {
        rec.lastNewsletter = new Date().toISOString()
        await env.ESCALE.put(name, JSON.stringify(rec))
        sent++
      }
    }
    cursor = page.list_complete ? undefined : page.cursor
  } while (cursor)
  return { sent }
}
