import { Ctx, esc } from "./_lib/common"
import { snapshot, Row } from "./bonsplans"
// Pages trajets : « Depuis une autre ville » — le prix du jour vers la même destination au départ des autres villes relevées
// chaque nuit (Abidjan : Paris, Milan, Rome, Bruxelles…), avec l'écart par rapport au trajet de la page. Aide à voir d'un coup
// d'œil si un autre aéroport de départ fait baisser le prix. Données : relevés du jour (src/bonsplans.ts, gardés une heure).
// Bloc écrit par src/apercu-prix.ts, seulement pour les trajets suivis et quand au moins une autre ville a un prix.
type T = { loc: string; title: string; lead: string; less: string; more: string; same: string; note: string }
const L: Record<string, T> = {
  fr: { loc: "fr-FR", title: "Vers {b} depuis une autre ville", lead: "Prix aller-retour du jour vers {b}, au départ des autres villes suivies par Escale.", less: "{x} de moins que depuis {a}", more: "{x} de plus que depuis {a}", same: "même prix que depuis {a}", note: "Prix relevés aujourd'hui, par personne. Pensez au trajet jusqu'à l'autre aéroport avant de comparer." },
  en: { loc: "en-GB", title: "To {b} from another city", lead: "Today's round-trip fares to {b} from the other cities tracked by Escale.", less: "{x} less than from {a}", more: "{x} more than from {a}", same: "same price as from {a}", note: "Fares recorded today, per person. Count the trip to the other airport before comparing." },
  es: { loc: "es-ES", title: "A {b} desde otra ciudad", lead: "Precios de ida y vuelta de hoy a {b} desde las otras ciudades que sigue Escale.", less: "{x} menos que desde {a}", more: "{x} más que desde {a}", same: "mismo precio que desde {a}", note: "Precios registrados hoy, por persona. Cuenta el trayecto hasta el otro aeropuerto antes de comparar." },
  pt: { loc: "pt-PT", title: "Para {b} a partir de outra cidade", lead: "Preços de ida e volta de hoje para {b} a partir das outras cidades seguidas pela Escale.", less: "{x} a menos do que de {a}", more: "{x} a mais do que de {a}", same: "mesmo preço que de {a}", note: "Preços registados hoje, por pessoa. Conte a deslocação até ao outro aeroporto antes de comparar." },
  ar: { loc: "ar-u-nu-latn", title: "إلى {b} من مدينة أخرى", lead: "أسعار الذهاب والعودة اليوم إلى {b} من المدن الأخرى التي يتابعها Escale.", less: "أقل بـ {x} من {a}", more: "أعلى بـ {x} من {a}", same: "نفس السعر من {a}", note: "أسعار مسجّلة اليوم للشخص الواحد. احسب تكلفة الوصول إلى المطار الآخر قبل المقارنة." },
  it: { loc: "it-IT", title: "Per {b} da un'altra città", lead: "Prezzi andata e ritorno di oggi per {b} dalle altre città seguite da Escale.", less: "{x} in meno rispetto a {a}", more: "{x} in più rispetto a {a}", same: "stesso prezzo che da {a}", note: "Prezzi rilevati oggi, a persona. Considera il tragitto fino all'altro aeroporto prima di confrontare." },
  de: { loc: "de-DE", title: "Nach {b} ab einer anderen Stadt", lead: "Heutige Preise für Hin- und Rückflug nach {b} ab den anderen Städten, die Escale beobachtet.", less: "{x} weniger als ab {a}", more: "{x} mehr als ab {a}", same: "gleicher Preis wie ab {a}", note: "Heute erfasste Preise pro Person. Rechne die Anreise zum anderen Flughafen mit ein." },
  nl: { loc: "nl-NL", title: "Naar {b} vanuit een andere stad", lead: "Retourprijzen van vandaag naar {b} vanuit de andere steden die Escale volgt.", less: "{x} minder dan vanuit {a}", more: "{x} meer dan vanuit {a}", same: "zelfde prijs als vanuit {a}", note: "Vandaag gemeten prijzen, per persoon. Reken de reis naar het andere vliegveld mee." },
}
const fill = (s: string, o: Record<string, string>) => s.replace(/\{(\w+)\}/g, (_, k) => o[k])

export async function render(ctx: Ctx, lang: string, from: string, to: string): Promise<string> {
  const s = await snapshot(ctx)
  const ici = s.rows.find((r) => r.from === from && r.to === to)
  if (!ici) return ""
  // Une ligne par autre ville (Paris a deux aéroports : on garde le moins cher)
  const par = new Map<string, Row>()
  for (const r of s.rows) if (r.to === to && r.a !== ici.a && (!par.has(r.a) || r.price < par.get(r.a)!.price)) par.set(r.a, r)
  const autres = [...par.values()].sort((x, y) => x.price - y.price)
  if (!autres.length) return ""
  const t = L[lang] || L.fr
  const money = (n: number) => { try { return new Intl.NumberFormat(t.loc, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n) } catch { return Math.round(n) + " €" } }
  const lignes = autres.map((r) => { const d = r.price - ici.price
    const ecart = Math.abs(d) < 3 ? `<span class="av-eq">${esc(fill(t.same, { a: ici.a }))}</span>` : d < 0 ? `<span class="av-dn">${esc(fill(t.less, { x: money(-d), a: ici.a }))}</span>` : `<span class="av-up">${esc(fill(t.more, { x: money(d), a: ici.a }))}</span>`
    return `<li><a href="/${r.path}/">${esc(r.a)} → ${esc(r.b)}</a><strong>${esc(money(r.price))}</strong>${ecart}</li>` }).join("")
  const style = `<style>.av{margin:22px 0 8px;padding:16px 18px;border:1px solid var(--line,#e5e7eb);border-radius:16px;background:var(--surface,#fff)}.av h2{margin:0 0 6px;font-size:1.15rem}.av p{margin:0 0 10px;color:var(--muted,#5b6474);font-size:.92rem}.av ul{list-style:none;margin:0;padding:0}.av li{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;padding:10px 0;border-top:1px solid var(--line,#e5e7eb)}.av li a{font-weight:700}.av li strong{font-size:1.05rem}.av li span{font-size:.88rem;font-weight:600;margin-inline-start:auto}.av-dn{color:#18794e}.av-up{color:#b42318}.av-eq{color:var(--muted,#5b6474)}.av .av-note{margin:10px 0 0;font-size:.8rem}</style>`
  return `${style}<section class="av" id="autres-villes" dir="${lang === "ar" ? "rtl" : "ltr"}"><h2>${esc(fill(t.title, { b: ici.b }))}</h2><p>${esc(fill(t.lead, { b: ici.b }))}</p><ul>${lignes}</ul><p class="av-note">${esc(t.note)}</p></section>`
}
