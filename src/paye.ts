import { esc } from "./_lib/common"
// « Prix payés par de vrais voyageurs » : sur chaque page trajet, les visiteurs indiquent le prix réellement payé (aller-retour,
// par personne), la compagnie et le mois du voyage. Rien de nominatif. La page affiche seulement des chiffres agrégés
// (« 12 voyageurs ont payé entre 520 € et 690 € ») dès 3 déclarations, après écart des valeurs aberrantes.
// Données : clé KV paye:FROM-TO = liste [{p, c, m, at}] (500 dernières). API : src/api/paye.ts. Bloc écrit par le serveur (apercu-prix.ts).
export type Paid = { p: number; c: string; m: string; at: string }
export type Stats = { n: number; min: number; max: number; med: number; airlines: [string, number][]; recent: number }
export const KEY = (from: string, to: string) => `paye:${from}-${to}`
export const MAX_KEEP = 500

const median = (a: number[]) => { const s = a.slice().sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2) }

// Agrégat : médiane de toutes les déclarations, puis min/max sur celles comprises entre 0,4 et 2,5 fois la médiane
export function stats(list: Paid[]): Stats | null {
  if (list.length < 3) return null
  const med = median(list.map((x) => x.p))
  const kept = list.filter((x) => x.p >= med * 0.4 && x.p <= med * 2.5)
  if (kept.length < 3) return null
  const by: Record<string, number> = {}
  for (const x of kept) if (x.c) by[x.c] = (by[x.c] || 0) + 1
  const airlines = Object.entries(by).filter(([, n]) => n >= 2).sort((a, b) => b[1] - a[1]).slice(0, 3) as [string, number][]
  const year = new Date(Date.now() - 365 * 864e5).toISOString().slice(0, 7)
  return { n: kept.length, min: Math.min(...kept.map((x) => x.p)), max: Math.max(...kept.map((x) => x.p)), med: median(kept.map((x) => x.p)), airlines, recent: kept.filter((x) => x.m >= year).length }
}

type T = { title: string; have: string; none: string; airlines: string; cta: string; price: string; airline: string; month: string; send: string; thanks: string; error: string; note: string; loc: string }
const L: Record<string, T> = {
  fr: { loc: "fr-FR", title: "Ce que les voyageurs ont vraiment payé", have: "{n} voyageurs ont déclaré leur billet aller-retour : entre {min} et {max}, le plus souvent autour de {med}.", none: "Personne n’a encore partagé le prix de son billet sur ce trajet. Soyez le premier : ça aide toute la communauté.",
    airlines: "Compagnies les plus citées : {a}.", cta: "Vous avez déjà fait ce trajet ? Dites-nous combien vous avez payé (anonyme, 20 secondes).", price: "Prix payé, aller-retour par personne (€)", airline: "Compagnie", month: "Mois du voyage", send: "Partager mon prix", thanks: "Merci ! Votre prix a été ajouté.", error: "Impossible d’envoyer pour le moment. Réessayez plus tard.", note: "Prix déclarés par des visiteurs, non vérifiés. À titre indicatif." },
  en: { loc: "en-GB", title: "What travellers actually paid", have: "{n} travellers reported their round-trip fare: between {min} and {max}, most often around {med}.", none: "Nobody has shared what they paid on this route yet. Be the first: it helps the whole community.",
    airlines: "Most mentioned airlines: {a}.", cta: "Flown this route? Tell us what you paid (anonymous, 20 seconds).", price: "Price paid, round trip per person (€)", airline: "Airline", month: "Month of travel", send: "Share my fare", thanks: "Thank you! Your fare has been added.", error: "Could not send right now. Please try again later.", note: "Fares reported by visitors, not verified. For guidance only." },
  es: { loc: "es-ES", title: "Lo que realmente pagaron los viajeros", have: "{n} viajeros indicaron su billete de ida y vuelta: entre {min} y {max}, casi siempre alrededor de {med}.", none: "Nadie ha compartido aún el precio de su billete en esta ruta. Sé el primero: ayuda a toda la comunidad.",
    airlines: "Aerolíneas más citadas: {a}.", cta: "¿Ya hiciste este viaje? Dinos cuánto pagaste (anónimo, 20 segundos).", price: "Precio pagado, ida y vuelta por persona (€)", airline: "Aerolínea", month: "Mes del viaje", send: "Compartir mi precio", thanks: "¡Gracias! Tu precio se ha añadido.", error: "No se pudo enviar ahora. Inténtalo más tarde.", note: "Precios declarados por visitantes, sin verificar. Solo orientativos." },
  pt: { loc: "pt-PT", title: "O que os viajantes pagaram de verdade", have: "{n} viajantes indicaram o bilhete de ida e volta: entre {min} e {max}, quase sempre à volta de {med}.", none: "Ninguém partilhou ainda o preço do bilhete nesta rota. Seja o primeiro: ajuda toda a comunidade.",
    airlines: "Companhias mais citadas: {a}.", cta: "Já fez esta viagem? Diga-nos quanto pagou (anónimo, 20 segundos).", price: "Preço pago, ida e volta por pessoa (€)", airline: "Companhia", month: "Mês da viagem", send: "Partilhar o meu preço", thanks: "Obrigado! O seu preço foi adicionado.", error: "Não foi possível enviar agora. Tente mais tarde.", note: "Preços declarados por visitantes, não verificados. Apenas indicativos." },
  ar: { loc: "ar-u-nu-latn", title: "ما دفعه المسافرون فعلًا", have: "أفاد {n} مسافرًا بسعر تذكرة الذهاب والعودة: بين {min} و{max}، وغالبًا حوالي {med}.", none: "لم يشارك أحد بعد سعر تذكرته على هذا الخط. كن الأول: هذا يساعد المجتمع كله.",
    airlines: "أكثر شركات الطيران ذكرًا: {a}.", cta: "سافرت على هذا الخط؟ أخبرنا كم دفعت (دون اسم، 20 ثانية).", price: "السعر المدفوع، ذهابًا وعودة للشخص (€)", airline: "شركة الطيران", month: "شهر السفر", send: "مشاركة سعري", thanks: "شكرًا! تمت إضافة سعرك.", error: "تعذر الإرسال الآن. حاول لاحقًا.", note: "أسعار صرّح بها الزوار وغير متحقق منها. للاسترشاد فقط." },
  it: { loc: "it-IT", title: "Quanto hanno pagato davvero i viaggiatori", have: "{n} viaggiatori hanno indicato il loro biglietto andata e ritorno: tra {min} e {max}, più spesso intorno a {med}.", none: "Nessuno ha ancora condiviso il prezzo del biglietto su questa rotta. Sii il primo: aiuta tutta la comunità.",
    airlines: "Compagnie più citate: {a}.", cta: "Hai già fatto questo viaggio? Dicci quanto hai pagato (anonimo, 20 secondi).", price: "Prezzo pagato, andata e ritorno a persona (€)", airline: "Compagnia", month: "Mese del viaggio", send: "Condividi il mio prezzo", thanks: "Grazie! Il tuo prezzo è stato aggiunto.", error: "Invio impossibile al momento. Riprova più tardi.", note: "Prezzi dichiarati dai visitatori, non verificati. Solo indicativi." },
  de: { loc: "de-DE", title: "Was Reisende wirklich bezahlt haben", have: "{n} Reisende haben ihren Hin- und Rückflug gemeldet: zwischen {min} und {max}, meist um {med}.", none: "Noch niemand hat den Preis seines Tickets auf dieser Strecke geteilt. Sei die erste Person: das hilft der ganzen Community.",
    airlines: "Meistgenannte Airlines: {a}.", cta: "Schon geflogen? Sag uns, was du bezahlt hast (anonym, 20 Sekunden).", price: "Bezahlter Preis, hin und zurück pro Person (€)", airline: "Airline", month: "Reisemonat", send: "Meinen Preis teilen", thanks: "Danke! Dein Preis wurde hinzugefügt.", error: "Senden gerade nicht möglich. Bitte später erneut versuchen.", note: "Von Besuchern gemeldete Preise, nicht geprüft. Nur zur Orientierung." },
  nl: { loc: "nl-NL", title: "Wat reizigers echt betaalden", have: "{n} reizigers meldden hun retourticket: tussen {min} en {max}, meestal rond {med}.", none: "Nog niemand deelde de prijs van zijn ticket op deze route. Wees de eerste: het helpt de hele community.",
    airlines: "Meest genoemde maatschappijen: {a}.", cta: "Deze route al gevlogen? Vertel ons wat je betaalde (anoniem, 20 seconden).", price: "Betaalde prijs, retour per persoon (€)", airline: "Maatschappij", month: "Reismaand", send: "Mijn prijs delen", thanks: "Bedankt! Je prijs is toegevoegd.", error: "Versturen lukt nu niet. Probeer het later opnieuw.", note: "Door bezoekers gemelde prijzen, niet gecontroleerd. Ter indicatie." },
}
const AIRLINES = ["Air France", "Air Côte d'Ivoire", "Air Sénégal", "Royal Air Maroc", "Corsair", "Brussels Airlines", "Turkish Airlines", "Ethiopian Airlines", "Kenya Airways", "ASKY", "Tunisair", "Air Algérie", "EgyptAir", "Qatar Airways", "Emirates", "British Airways", "ITA Airways", "Lufthansa", "KLM", "TAP", "Iberia", "Transavia", "easyJet", "Ryanair", "Vueling", "Air Europa", "Air Mauritius", "Rwandair", "Air Peace", "Mauritania Airlines"]

export function render(lang: string, from: string, to: string, s: Stats | null): string {
  const t = L[lang] || L.fr
  const money = (n: number) => { try { return new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n) } catch { return Math.round(n) + " €" } }
  const fill = (x: string, o: Record<string, string>) => x.replace(/\{(\w+)\}/g, (_, k) => o[k])
  const now = new Date(), maxMonth = now.toISOString().slice(0, 7), minMonth = new Date(Date.UTC(now.getUTCFullYear() - 2, now.getUTCMonth(), 1)).toISOString().slice(0, 7)
  const summary = s ? `<p class="pp-have"><strong>${esc(fill(t.have, { n: String(s.n), min: money(s.min), max: money(s.max), med: money(s.med) }))}</strong>` +
    (s.airlines.length ? ` ${esc(fill(t.airlines, { a: s.airlines.map(([a, n]) => `${a} (${n})`).join(", ") }))}` : "") + `</p>` : `<p class="pp-none">${esc(t.none)}</p>`
  const style = `<style>.pp{margin:22px 0 8px;padding:16px 18px;border:1px solid var(--line,#e5e7eb);border-radius:16px;background:var(--surface,#fff)}.pp h2{margin:0 0 8px;font-size:1.15rem}.pp-have strong{color:var(--ink,#0b1b2b)}.pp-none,.pp-cta,.pp-note{color:var(--muted,#5b6474)}.pp-cta{margin:10px 0 8px}.pp-form{display:grid;gap:10px;grid-template-columns:1fr 1fr;align-items:end}.pp-form label{display:grid;gap:4px;font-size:.85rem;color:var(--muted,#5b6474)}.pp-form input{font:inherit;padding:9px 10px;border:1px solid var(--line,#e5e7eb);border-radius:10px;background:var(--surface,#fff);color:inherit;min-width:0}.pp-form .pp-wide{grid-column:1/-1}.pp-form button{font:inherit;font-weight:700;padding:11px 16px;border:0;border-radius:999px;background:var(--teal-d,#0b8577);color:#fff;cursor:pointer;grid-column:1/-1}.pp-note{font-size:.8rem;margin:10px 0 0}.pp-ok{color:#18794e;font-weight:600}.pp-ko{color:#b42318}@media(max-width:480px){.pp-form{grid-template-columns:1fr}}</style>`
  const form = `<p class="pp-cta">${esc(t.cta)}</p><form class="pp-form" data-from="${from}" data-to="${to}" action="/api/paye" method="post">` +
    `<label>${esc(t.price)}<input type="number" name="prix" min="30" max="4000" step="1" inputmode="numeric" required></label>` +
    `<label>${esc(t.month)}<input type="month" name="mois" min="${minMonth}" max="${maxMonth}" required></label>` +
    `<label class="pp-wide">${esc(t.airline)}<input type="text" name="compagnie" list="pp-airlines" maxlength="40" autocomplete="off"></label><datalist id="pp-airlines">${AIRLINES.map((a) => `<option value="${esc(a)}">`).join("")}</datalist>` +
    `<input type="text" name="site-web" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">` +
    `<input type="hidden" name="from" value="${from}"><input type="hidden" name="to" value="${to}"><input type="hidden" name="lang" value="${esc(lang)}">` +
    `<button type="submit">${esc(t.send)}</button><p class="pp-msg pp-wide" role="status" hidden></p></form>`
  const script = `<script>(function(){var f=document.querySelector(".pp-form");if(!f)return;f.addEventListener("submit",function(e){e.preventDefault();var b=f.querySelector("button"),m=f.querySelector(".pp-msg");b.disabled=true;var d={};new FormData(f).forEach(function(v,k){d[k]=v});fetch("/api/paye",{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify(d)}).then(function(r){return r.ok?r.json():Promise.reject()}).then(function(){m.textContent=${JSON.stringify(t.thanks)};m.className="pp-msg pp-wide pp-ok";m.hidden=false;f.querySelectorAll("label,button").forEach(function(x){x.hidden=true});try{(window.escaleSend||function(){})("prix-paye")}catch(x){}}).catch(function(){m.textContent=${JSON.stringify(t.error)};m.className="pp-msg pp-wide pp-ko";m.hidden=false;b.disabled=false})})})()</script>`
  return `${style}<section class="pp" id="prix-payes"><h2>${esc(t.title)}</h2>${summary}${form}<p class="pp-note">${esc(t.note)}</p></section>${script}`
}
