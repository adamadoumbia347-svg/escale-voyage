"""Pages en italien (test) : trajets au départ de l'Italie (Milan, Rome, Bologne, Turin) vers l'Afrique et le Maghreb.

Les Italiens ne cherchent pas « Paris → Dakar » mais « Milano → Dakar » : ces pages ne traduisent pas les trajets français,
ce sont des trajets propres à l'Italie, avec leur page d'accueil /it/. Les rubriques du menu (offres, guides…) renvoient
vers les pages en anglais, et la recherche s'ouvre en anglais (le comparateur n'existe pas encore en italien).
Durées : ESTIMÉES d'après la distance (préfixe « circa ») ; on ne prétend pas qu'un vol direct existe.
"""
import html
import math
import urllib.parse

import build_i18n as B

E = html.escape

B.UI["it"] = dict(
    flight_slug="voli", app_lang="en", arrow="→",
    home="Confronta voli, hotel e auto", legal="Note legali (FR)", privacy="Privacy (FR)", cookies="Gestisci i cookie",
    disclaimer="Escale non vende biglietti e non fissa alcun prezzo. I prezzi mostrati sono prezzi reali trovati di recente: la tariffa esatta appare sul sito di prenotazione.",
)

# Villes de départ (code, nom italien, aéroports voisins à comparer)
ORIG = {
    "MXP": ("Milano", "Da Milano confronta anche Bergamo Orio al Serio (BGY), servito da molte compagnie low cost, e Linate (LIN)."),
    "FCO": ("Roma", "Da Roma confronta anche Ciampino (CIA), servito da compagnie low cost: a volte il risparmio è notevole."),
    "BLQ": ("Bologna", "Da Bologna confronta anche le partenze da Milano e da Venezia: con uno scalo in più, il prezzo può scendere."),
    "TRN": ("Torino", "Da Torino confronta anche Milano Malpensa (MXP), a circa un'ora e mezza: l'offerta di voli è molto più ampia."),
}
# Destinations (code, nom italien, pays, aéroport, périodes chères, conseil)
DEST = {
    "DSS": ("Dakar", "Senegal", "Aeroporto internazionale Blaise Diagne", "Natale, agosto e la Tabaski",
            "L'aeroporto Blaise Diagne si trova a Diass, a circa 45 km dal centro di Dakar: prevedi il trasferimento nel budget, soprattutto per un arrivo di notte."),
    "CMN": ("Casablanca", "Marocco", "Aeroporto Mohammed V", "agosto, Natale e la fine del Ramadan",
            "Confronta anche Marrakech, Rabat, Tangeri, Fès e Nador: a seconda della tua destinazione finale, un altro aeroporto può costare meno."),
    "TUN": ("Tunisi", "Tunisia", "Aeroporto di Tunisi-Cartagine", "luglio, agosto e la fine del Ramadan",
            "Confronta anche Monastir, Enfidha e Djerba. D'estate il traghetto è un'alternativa se viaggi in auto."),
    "CAI": ("Il Cairo", "Egitto", "Aeroporto internazionale del Cairo", "le vacanze di Natale e di Pasqua",
            "Per i cittadini italiani il visto si ottiene online prima della partenza o all'arrivo: verifica le condizioni aggiornate prima di prenotare."),
    "LOS": ("Lagos", "Nigeria", "Aeroporto internazionale Murtala Muhammed", "Natale e le vacanze estive",
            "Per la Nigeria serve un visto da richiedere prima della partenza, e la vaccinazione contro la febbre gialla è obbligatoria."),
    "ACC": ("Accra", "Ghana", "Aeroporto internazionale Kotoka", "Natale e le vacanze estive",
            "Per il Ghana serve un visto da richiedere prima della partenza, e la vaccinazione contro la febbre gialla è obbligatoria."),
    "ABJ": ("Abidjan", "Costa d'Avorio", "Aeroporto Félix Houphouët-Boigny", "Natale e le vacanze estive",
            "Il visto per la Costa d'Avorio si richiede online (e-visa) prima della partenza, e la vaccinazione contro la febbre gialla è obbligatoria."),
    "ADD": ("Addis Abeba", "Etiopia", "Aeroporto internazionale di Bole", "Natale e il Timkat (gennaio)",
            "Addis Abeba è anche un grande scalo per il resto dell'Africa: confronta i voli con coincidenza verso la tua destinazione finale."),
    "ALG": ("Algeri", "Algeria", "Aeroporto Houari Boumediene", "luglio, agosto e la fine del Ramadan",
            "Per l'Algeria serve un visto da richiedere prima della partenza (salvo per chi ha la cittadinanza algerina)."),
}
ROUTES = [("MXP", d) for d in ("DSS", "CMN", "LOS", "ACC", "ABJ", "CAI", "TUN")] + \
         [("FCO", d) for d in ("DSS", "CMN", "TUN", "CAI", "LOS", "ADD", "ALG")] + \
         [("BLQ", d) for d in ("CMN", "DSS")] + [("TRN", d) for d in ("CMN", "DSS")]


def slug(t):
    return B.slugify(t)


def path(r):
    return f"it/voli-{slug(ORIG[r[0]][0])}-{slug(DEST[r[1]][0])}"


def est(airports, a, b):
    """Durée estimée sans escale (distance / 800 km/h + 30 min, au quart d'heure), comme routes_extra.py."""
    x, y = airports[a], airports[b]
    r = math.pi / 180
    h = math.sin((y[5] - x[5]) * r / 2) ** 2 + math.cos(x[5] * r) * math.cos(y[5] * r) * math.sin((y[6] - x[6]) * r / 2) ** 2
    km = 12742 * math.asin(math.sqrt(h))
    minutes = round((km / 800 + 0.5) * 60 / 15) * 15
    hh, mm = divmod(minutes, 60)
    return (f"{hh} h {mm:02d}" if mm else f"{hh} h"), int(round(km, -1))


def build(site, ctx):
    airports = ctx["airports"]
    urls = []
    for r in ROUTES:
        fr_, to = r
        a, otip = ORIG[fr_]
        b, country, airport, peak, dtip = DEST[to]
        d, km = est(airports, fr_, to)
        dur = f"circa {d} senza scalo (stima in base alla distanza di {km:,} km)".replace(",", ".")
        p = path(r)
        app = "/?" + urllib.parse.urlencode({"type": "vols", "from": fr_, "to": to, "lang": "en"})
        faq = [
            (f"Quanto dura un volo da {a} a {b}?", f"Circa {d} con un volo senza scalo (stima in base alla distanza). Con uno scalo, il viaggio dura spesso diverse ore in più a seconda della coincidenza."),
            (f"Quando prenotare un volo economico {a} – {b}?", f"In genere due o tre mesi prima della partenza. I prezzi salgono molto durante {peak}: per questi periodi prenota prima."),
            (f"In quale aeroporto si arriva a {b}?", f"I voli arrivano all'{airport} ({to})."),
            ("Il bagaglio è incluso?", "Non sempre. Le tariffe più basse a volte includono solo un bagaglio piccolo: verifica la franchigia del bagaglio in stiva prima di pagare."),
        ]
        others = [o for o in ROUTES if o != r and (o[0] == fr_ or o[1] == to)]
        hero = f"""<p class="eyebrow">{E(country)}</p>
  <h1>Voli economici {E(a)} <span>→</span> {E(b)}</h1>
  <p class="codes" dir="ltr">{fr_} → {to}</p>
  <p class="hero-price" id="hero-price" hidden></p>
  <div class="cta-row"><a class="btn" href="{E(B.av_link(fr_, to))}" data-av="{fr_}-{to}" target="_blank" rel="sponsored noopener">Vedi i prezzi su Aviasales</a><a class="btn ghost" href="{E(app)}">Confronta i siti</a>{B.alert_btn("it")}</div>"""
        body = f"""<dl class="facts">
  <div><dt>Durata del volo</dt><dd>{E(dur[0].upper() + dur[1:])}</dd></div>
  <div><dt>Arrivo</dt><dd>{E(airport)} ({to})</dd></div>
  <div><dt>Periodi più cari</dt><dd>{E(peak[0].upper() + peak[1:])}</dd></div>
</dl>
<section id="route-prices" data-from="{fr_}" data-to="{to}" hidden><h2>Prezzi trovati di recente</h2>
<p class="small">Prezzi andata e ritorno più bassi trovati dai viaggiatori negli ultimi giorni, per mese di partenza. La tariffa esatta appare sul sito di prenotazione.</p>
<ul class="price-list"></ul></section>
<script src="/route-prices.js" defer></script>
{B.calendar_html("it", fr_, to)}
<section><h2>I nostri consigli per questa tratta</h2><ul><li>{E(otip)}</li><li>{E(dtip)}</li></ul></section>
<section><h2>Come pagare di meno</h2>
<ol class="steps">
<li><strong>Usa le date flessibili.</strong> Spostare la partenza di un giorno o due cambia spesso il prezzo più della scelta del sito.</li>
<li><strong>Confronta i voli con scalo.</strong> Casablanca, Istanbul, Tunisi o Addis Abeba sono spesso più economici del volo diretto.</li>
<li><strong>Controlla il bagaglio.</strong> Aggiungi il prezzo della valigia prima di confrontare due tariffe.</li>
<li><strong>Attiva un avviso prezzo</strong> se parti tra qualche mese: ricevi un'e-mail quando il prezzo scende.</li>
</ol>
<p><a class="btn" href="{E(B.av_link(fr_, to))}" data-av="{fr_}-{to}" target="_blank" rel="sponsored noopener">Cerca {E(a)} → {E(b)} su Aviasales</a></p>
</section>
{B.extras_html(site, "it", b, DEST_EN[to], to)}
<section class="faq"><h2>Domande frequenti</h2>
{"".join(f"<details><summary>{E(q)}</summary><p>{E(ans)}</p></details>" for q, ans in faq)}
</section>
<section><h2>Altre tratte</h2><ul class="route-links">{"".join(f'<li><a href="/{path(o)}/">{E(ORIG[o[0]][0])} → {E(DEST[o[1]][0])}</a></li>' for o in others)}</ul></section>"""
        urls.append(B.write(site, p, "it", f"Voli economici {a} {b}: confronta i prezzi",
                            f"Volo economico {a} – {b} ({fr_} → {to}): durata del volo, quando prenotare e prezzi reali trovati di recente su Aviasales.",
                            hero, body, B.faq_ld(faq), {"it": p}, ctx))
    groups = {}
    for r in ROUTES:
        groups.setdefault(r[0], []).append(r)
    body = "".join(
        f'<section><h2>Voli da {E(ORIG[o][0])}</h2><ul class="route-links">' + "".join(
            f'<li><a href="/{path(r)}/">{E(ORIG[r[0]][0])} → {E(DEST[r[1]][0])}</a></li>' for r in rs) + "</ul></section>"
        for o, rs in groups.items())
    body += f'<section><h2>Le offerte ogni settimana</h2><p>I prezzi più bassi verso l\'Africa e il Maghreb, ogni settimana su WhatsApp, gratis.</p>{B.wa_btn("it")}</section>'
    hero = ('<h1>Voli economici verso l\'Africa e il Maghreb</h1><p class="hero-lead">Da Milano, Roma, Bologna e Torino: durata del volo, '
            'quando prenotare e prezzi reali trovati di recente, tratta per tratta.</p>')
    urls.append(B.write(site, "it", "it", "Voli economici verso l'Africa e il Maghreb | Escale",
                        "Voli economici da Milano, Roma, Bologna e Torino verso Dakar, Casablanca, Tunisi, Il Cairo, Lagos, Accra, Abidjan: prezzi reali e consigli.",
                        hero, body, "", {"it": "it"}, ctx))
    return urls


DEST_EN = {"DSS": "Dakar", "CMN": "Casablanca", "TUN": "Tunis", "CAI": "Cairo", "LOS": "Lagos", "ACC": "Accra", "ABJ": "Abidjan", "ADD": "Addis Ababa", "ALG": "Algiers"}
