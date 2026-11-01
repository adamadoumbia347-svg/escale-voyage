"""Pages en néerlandais : trajets au départ des Pays-Bas et de Flandre (Amsterdam, Eindhoven, Rotterdam, Bruxelles)
vers l'Afrique, le Maghreb et le Suriname (grandes diasporas marocaine, ghanéenne, nigériane et surinamienne).

Même principe que scripts/italia.py et scripts/deutsch.py : page d'accueil /nl/, rubriques du menu en anglais,
recherche en anglais. Durées ESTIMÉES d'après la distance (« ca. »). Entrée : résumé prudent pour un passeport
néerlandais ou belge, avec renvoi vers les reisadviezen officiels. Vérifié : novembre 2026.
"""
import html

import build_i18n as B
from italia import est
from deutsch import slug

E = html.escape

B.UI["nl"] = dict(
    flight_slug="vluchten", app_lang="en", arrow="→",
    home="Vluchten, hotels en huurauto's vergelijken", legal="Juridische informatie (FR)", privacy="Privacy (FR)", cookies="Cookies beheren",
    disclaimer="Escale verkoopt geen tickets en bepaalt geen prijzen. De getoonde prijzen zijn echte prijzen die onlangs zijn gevonden: het exacte tarief zie je op de boekingssite.",
)
B.NAMES["nl"] = "Nederlands"
B.LOCALE["nl"] = "nl_NL"

ORIG = {
    "AMS": ("Amsterdam", "Vanuit Amsterdam kun je ook Eindhoven (EIN) en Rotterdam (RTM) vergelijken, of Brussel en Düsseldorf: met de trein snel bereikbaar en soms veel goedkoper."),
    "EIN": ("Eindhoven", "Vanuit Eindhoven vliegen veel prijsvechters naar Marokko: vergelijk ook Amsterdam (AMS) en Düsseldorf (DUS) voor vluchten met een overstap."),
    "RTM": ("Rotterdam", "Rotterdam The Hague Airport is klein: vergelijk ook Amsterdam (AMS), Eindhoven (EIN) en Brussel (BRU) voor meer keuze."),
    "BRU": ("Brussel", "Vanuit Brussel vergelijk je ook Charleroi (CRL), waar prijsvechters vliegen, en Amsterdam (AMS) voor intercontinentale vluchten."),
}
DEST = {
    "CMN": ("Casablanca", "Marokko", "Luchthaven Mohammed V", "de zomervakantie, de kerstvakantie en het einde van de ramadan",
            "Met een Nederlands of Belgisch paspoort heb je voor een vakantie tot 90 dagen geen visum nodig. Vergelijk ook Nador, Tanger, Al Hoceima en Marrakech."),
    "NDR": ("Nador", "Marokko", "Luchthaven Nador Al Aaroui", "juli, augustus en het Offerfeest",
            "Nador is in de zomer erg gevraagd: boek vroeg en vergelijk ook Al Hoceima (AHU), Oujda (OUD) en Tanger. Geen visum nodig voor een vakantie tot 90 dagen."),
    "TNG": ("Tanger", "Marokko", "Luchthaven Tanger Ibn Battuta", "juli, augustus en het einde van de ramadan",
            "In de zomer is de veerboot via Spanje een alternatief als je met de auto reist. Geen visum nodig voor een vakantie tot 90 dagen."),
    "RAK": ("Marrakech", "Marokko", "Luchthaven Marrakech Menara", "de herfst-, kerst- en voorjaarsvakantie",
            "Veel prijsvechters vliegen op Marrakech: controleer de bagageregels voordat je prijzen vergelijkt."),
    "AGA": ("Agadir", "Marokko", "Luchthaven Agadir Al Massira", "de winterzon (december tot maart) en de zomervakantie",
            "Agadir is populair voor winterzon: boek de kerstvakantie ruim op tijd."),
    "TUN": ("Tunis", "Tunesië", "Luchthaven Tunis-Carthago", "juli, augustus en het einde van de ramadan",
            "Met een Nederlands of Belgisch paspoort heb je voor een vakantie geen visum nodig. Vergelijk ook Monastir, Enfidha en Djerba."),
    "CAI": ("Caïro", "Egypte", "Internationale luchthaven van Caïro", "de kerst- en voorjaarsvakantie",
            "Het visum voor Egypte vraag je online aan of koop je bij aankomst: controleer de actuele voorwaarden voordat je boekt."),
    "ACC": ("Accra", "Ghana", "Kotoka International Airport", "Kerstmis en de zomervakantie",
            "Voor Ghana heb je een visum nodig dat je vóór vertrek aanvraagt. Een gelekoortsvaccinatie is verplicht."),
    "LOS": ("Lagos", "Nigeria", "Murtala Muhammed International Airport", "Kerstmis en de zomervakantie",
            "Voor Nigeria heb je een visum nodig dat je vóór vertrek aanvraagt. Een gelekoortsvaccinatie is verplicht."),
    "DSS": ("Dakar", "Senegal", "Luchthaven Blaise Diagne", "Kerstmis, augustus en Tabaski",
            "Met een Nederlands of Belgisch paspoort heb je voor een verblijf tot 90 dagen geen visum nodig. De luchthaven ligt in Diass, ca. 45 km van Dakar."),
    "ABJ": ("Abidjan", "Ivoorkust", "Luchthaven Félix Houphouët-Boigny", "Kerstmis en de zomervakantie",
            "Het visum voor Ivoorkust vraag je online aan (e-visum) vóór vertrek. Een gelekoortsvaccinatie is verplicht."),
    "ADD": ("Addis Abeba", "Ethiopië", "Bole International Airport", "Kerstmis en Timkat (januari)",
            "Addis Abeba is ook een grote overstapluchthaven voor de rest van Afrika: vergelijk overstapvluchten naar je eindbestemming. E-visum online."),
    "NBO": ("Nairobi", "Kenia", "Jomo Kenyatta International Airport", "juli tot september en Kerstmis",
            "Voor Kenia heb je vóór vertrek een elektronische reistoestemming (eTA) nodig."),
    "PBM": ("Paramaribo", "Suriname", "Johan Adolf Pengel International Airport", "de zomervakantie en de kerstvakantie",
            "Voor Suriname heb je met een Nederlands of Belgisch paspoort een e-visum of een toeristenkaart nodig, online aan te vragen vóór vertrek. De luchthaven ligt in Zanderij, ca. 45 km van Paramaribo."),
}
DEST_EN = {"CMN": "Casablanca", "NDR": "Nador", "TNG": "Tangier", "RAK": "Marrakech", "AGA": "Agadir", "TUN": "Tunis", "CAI": "Cairo", "ACC": "Accra",
           "LOS": "Lagos", "DSS": "Dakar", "ABJ": "Abidjan", "ADD": "Addis Ababa", "NBO": "Nairobi", "PBM": "Paramaribo"}
ROUTES = [("AMS", d) for d in ("CMN", "NDR", "TNG", "RAK", "AGA", "TUN", "CAI", "ACC", "LOS", "DSS", "ABJ", "ADD", "NBO", "PBM")] + \
         [("EIN", d) for d in ("CMN", "NDR", "TNG", "RAK", "AGA")] + [("RTM", d) for d in ("NDR", "TNG", "CMN")] + \
         [("BRU", d) for d in ("CMN", "NDR", "TNG", "ACC", "LOS", "DSS", "ABJ")]
GOV = "https://www.nederlandwereldwijd.nl/reisadvies"


def path(r):
    return f"nl/vluchten-{slug(ORIG[r[0]][0])}-{slug(DEST[r[1]][0])}"


def build(site, ctx):
    airports = ctx["airports"]
    urls = []
    for r in ROUTES:
        fr_, to = r
        a, otip = ORIG[fr_]
        b, country, airport, peak, dtip = DEST[to]
        d, km = est(airports, fr_, to)
        dur = f"ca. {d} zonder overstap (geschat op basis van de afstand van {km:,} km)".replace(",", ".").replace(" h ", " u ").replace(" h", " u")
        dd = d.replace(" h ", " u ").replace(" h", " u")
        p = path(r)
        faq = [
            (f"Hoe lang duurt een vlucht van {a} naar {b}?", f"Ongeveer {dd} zonder overstap (schatting op basis van de afstand). Met een overstap duurt de reis vaak enkele uren langer, afhankelijk van de aansluiting."),
            (f"Wanneer boek je een goedkope vlucht {a} – {b}?", f"Meestal twee tot drie maanden voor vertrek. Tijdens {peak} stijgen de prijzen sterk: boek voor die periodes eerder."),
            (f"Op welke luchthaven kom je aan in {b}?", f"De vluchten landen op {airport} ({to})."),
            (f"Heb ik een visum nodig voor {country}?", dtip if "visum" in dtip.lower() else "Dat hangt af van je nationaliteit: controleer vóór het boeken het officiële reisadvies."),
            ("Is bagage inbegrepen?", "Niet altijd. De goedkoopste tarieven bevatten soms alleen handbagage: controleer de ruimbagage voordat je betaalt."),
        ]
        others = [o for o in ROUTES if o != r and (o[0] == fr_ or o[1] == to)]
        hero = f"""<p class="eyebrow">{E(country)}</p>
  <h1>Goedkope vluchten {E(a)} <span>→</span> {E(b)}</h1>
  <p class="codes" dir="ltr">{fr_} → {to}</p>
  <p class="hero-price" id="hero-price" hidden></p>
  <div class="cta-row"><a class="btn" href="{E(B.av_link(fr_, to))}" data-av="{fr_}-{to}" target="_blank" rel="sponsored noopener">Prijzen bekijken op Aviasales</a><a class="btn ghost" href="/recherche/" data-wl="{fr_}-{to}">Live prijzen</a>{B.alert_btn("nl")}</div>"""
        body = f"""<dl class="facts">
  <div><dt>Vluchtduur</dt><dd>{E(dur[0].upper() + dur[1:])}</dd></div>
  <div><dt>Aankomst</dt><dd>{E(airport)} ({to})</dd></div>
  <div><dt>Duurste periodes</dt><dd>{E(peak[0].upper() + peak[1:])}</dd></div>
</dl>
<section id="route-prices" data-from="{fr_}" data-to="{to}" hidden><h2>Onlangs gevonden prijzen</h2>
<p class="small">Laagste retourprijzen die reizigers de afgelopen dagen hebben gevonden, per vertrekmaand. Het exacte tarief zie je op de boekingssite.</p>
<ul class="price-list"></ul></section>
<script src="/route-prices.js" defer></script>
{B.calendar_html("nl", fr_, to)}
<section><h2>Onze tips voor deze route</h2><ul><li>{E(otip)}</li><li>{E(dtip)} Inreisregels veranderen: bekijk vóór het boeken het <a href="{GOV}" target="_blank" rel="noopener">officiële reisadvies</a>.</li></ul></section>
<section><h2>Zo betaal je minder</h2>
<ol class="steps">
<li><strong>Gebruik flexibele data.</strong> Een of twee dagen eerder of later vertrekken verandert de prijs vaak meer dan de keuze van de site.</li>
<li><strong>Vergelijk vluchten met een overstap.</strong> Via Istanbul, Casablanca, Lissabon of Addis Abeba is het vaak goedkoper dan rechtstreeks.</li>
<li><strong>Let op de bagage.</strong> Tel de koffer mee voordat je twee tarieven vergelijkt.</li>
<li><strong>Stel een prijsalert in</strong> als je pas over een paar maanden vertrekt: je krijgt een e-mail zodra de prijs daalt.</li>
</ol>
<p><a class="btn" href="{E(B.av_link(fr_, to))}" data-av="{fr_}-{to}" target="_blank" rel="sponsored noopener">{E(a)} → {E(b)} zoeken op Aviasales</a></p>
</section>
{B.extras_html(site, "nl", b, DEST_EN[to], to)}
<section class="faq"><h2>Veelgestelde vragen</h2>
{"".join(f"<details><summary>{E(q)}</summary><p>{E(ans)}</p></details>" for q, ans in faq)}
</section>
<section><h2>Andere routes</h2><ul class="route-links">{"".join(f'<li><a href="/{path(o)}/">{E(ORIG[o[0]][0])} → {E(DEST[o[1]][0])}</a></li>' for o in others)}</ul></section>"""
        urls.append(B.write(site, p, "nl", f"Goedkope vluchten {a} {b}: prijzen vergelijken",
                            f"Goedkope vlucht {a} – {b} ({fr_} → {to}): vluchtduur, wanneer boeken, visum en echte prijzen die onlangs op Aviasales zijn gevonden.",
                            hero, body, B.faq_ld(faq), {"nl": p}, ctx))
    groups = {}
    for r in ROUTES:
        groups.setdefault(r[0], []).append(r)
    body = "".join(
        f'<section><h2>Vluchten vanuit {E(ORIG[o][0])}</h2><ul class="route-links">' + "".join(
            f'<li><a href="/{path(r)}/">{E(ORIG[r[0]][0])} → {E(DEST[r[1]][0])}</a></li>' for r in rs) + "</ul></section>"
        for o, rs in groups.items())
    body += f'<section><h2>Elke week de beste deals</h2><p>De laagste prijzen naar Afrika, de Maghreb en Suriname, elke week gratis op WhatsApp.</p>{B.wa_btn("nl")}</section>'
    hero = ('<h1>Goedkope vluchten naar Afrika, Marokko en Suriname</h1><p class="hero-lead">Vanuit Amsterdam, Eindhoven, Rotterdam en Brussel: '
            'vluchtduur, wanneer boeken en echte prijzen die onlangs zijn gevonden, route per route.</p>')
    urls.append(B.write(site, "nl", "nl", "Goedkope vluchten naar Afrika, Marokko en Suriname | Escale",
                        "Goedkope vluchten vanuit Amsterdam, Eindhoven, Rotterdam en Brussel naar Nador, Casablanca, Tanger, Accra, Lagos, Paramaribo: echte prijzen.",
                        hero, body, "", {"nl": "nl"}, ctx))
    return urls
