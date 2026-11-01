"""Pages en allemand : trajets au départ de l'Allemagne, de l'Autriche et de la Suisse alémanique vers l'Afrique et le Maghreb.

Même principe que scripts/italia.py : les Allemands cherchent « Frankfurt → Accra », pas « Paris → Accra ». Ce sont des trajets
propres à ces pays, avec leur page d'accueil /de/. Les rubriques du menu (offres, guides…) renvoient vers les pages en anglais,
et la recherche s'ouvre en anglais (le comparateur n'existe pas encore en allemand).
Durées : ESTIMÉES d'après la distance (« ca. ») ; on ne prétend pas qu'un vol direct existe.
Règles d'entrée : résumé prudent pour les passeports allemands, toujours avec un renvoi vers l'Auswärtiges Amt. Vérifié : novembre 2026.
"""
import html
import urllib.parse

import build_i18n as B
from italia import est

E = html.escape

B.UI["de"] = dict(
    flight_slug="fluege", app_lang="de", arrow="→",
    home="Flüge, Hotels und Mietwagen vergleichen", legal="Impressum (FR)", privacy="Datenschutz (FR)", cookies="Cookies verwalten",
    disclaimer="Escale verkauft keine Tickets und legt keine Preise fest. Die angezeigten Preise sind echte, kürzlich gefundene Preise: Der genaue Tarif erscheint auf der Buchungsseite.",
)

# Villes de départ (code, nom allemand, aéroports voisins à comparer)
ORIG = {
    "FRA": ("Frankfurt", "Von Frankfurt aus lohnt sich auch ein Blick auf Köln/Bonn (CGN) und Düsseldorf (DUS): mit dem ICE schnell erreichbar, manchmal deutlich günstiger."),
    "BER": ("Berlin", "Von Berlin aus fliegen viele Verbindungen über Istanbul, Paris, Brüssel oder Addis Abeba: Vergleiche die Umsteigeflüge, oft sind sie günstiger."),
    "MUC": ("München", "Von München aus vergleiche auch Abflüge ab Wien (VIE), Zürich (ZRH) oder Memmingen (FMM) mit Billigfliegern."),
    "DUS": ("Düsseldorf", "Von Düsseldorf aus vergleiche auch Köln/Bonn (CGN), Amsterdam (AMS) und Brüssel (BRU): Brüssel hat viele Afrika-Verbindungen."),
    "HAM": ("Hamburg", "Von Hamburg aus vergleiche auch Abflüge ab Berlin, Amsterdam oder Kopenhagen: Mit einem Umstieg mehr kann der Preis sinken."),
    "CGN": ("Köln", "Von Köln/Bonn aus vergleiche auch Düsseldorf (DUS), Frankfurt (FRA) und Brüssel (BRU), das viele Afrika-Verbindungen hat."),
    "STR": ("Stuttgart", "Von Stuttgart aus vergleiche auch Frankfurt (FRA), München (MUC) und Zürich (ZRH): Dort ist das Flugangebot viel größer."),
    "VIE": ("Wien", "Von Wien aus vergleiche auch Bratislava (BTS) und Budapest (BUD), die von Billigfliegern angeflogen werden."),
}
# Destinations (code, nom allemand, pays, aéroport, périodes chères, conseil / entrée pour les passeports allemands)
DEST = {
    "ACC": ("Accra", "Ghana", "Kotoka International Airport", "Weihnachten und die Sommerferien",
            "Für Ghana brauchst du ein Visum, das vor der Abreise beantragt wird. Eine Gelbfieberimpfung ist Pflicht."),
    "LOS": ("Lagos", "Nigeria", "Murtala Muhammed International Airport", "Weihnachten und die Sommerferien",
            "Für Nigeria brauchst du ein Visum, das vor der Abreise beantragt wird. Eine Gelbfieberimpfung ist Pflicht."),
    "ABV": ("Abuja", "Nigeria", "Nnamdi Azikiwe International Airport", "Weihnachten und die Sommerferien",
            "Vergleiche Abuja mit Lagos: Je nach Ziel in Nigeria kann der andere Flughafen günstiger sein. Visum und Gelbfieberimpfung sind Pflicht."),
    "DLA": ("Douala", "Kamerun", "Flughafen Douala", "Weihnachten und die Sommerferien",
            "Für Kamerun brauchst du ein Visum vor der Abreise und eine Gelbfieberimpfung. Vergleiche auch Yaoundé (NSI)."),
    "CMN": ("Casablanca", "Marokko", "Flughafen Mohammed V", "der Sommer, Weihnachten und das Ende des Ramadan",
            "Mit deutschem Pass brauchst du für einen Urlaub bis 90 Tage kein Visum. Vergleiche auch Marrakesch, Agadir, Tanger, Fès und Nador."),
    "TUN": ("Tunis", "Tunesien", "Flughafen Tunis-Karthago", "Juli, August und das Ende des Ramadan",
            "Mit deutschem Pass brauchst du für einen Urlaub kein Visum. Vergleiche auch Monastir, Enfidha und Djerba."),
    "CAI": ("Kairo", "Ägypten", "Internationaler Flughafen Kairo", "die Weihnachts- und Osterferien",
            "Mit deutschem Pass gibt es das Visum online vor der Reise oder bei der Ankunft: Prüfe die aktuellen Bedingungen vor der Buchung."),
    "ADD": ("Addis Abeba", "Äthiopien", "Bole International Airport", "Weihnachten und Timkat (Januar)",
            "Addis Abeba ist auch ein großes Drehkreuz für den Rest Afrikas: Vergleiche Umsteigeflüge zu deinem Endziel. Visum online (e-Visa)."),
    "DSS": ("Dakar", "Senegal", "Flughafen Blaise Diagne", "Weihnachten, August und Tabaski",
            "Mit deutschem Pass brauchst du für bis zu 90 Tage kein Visum. Der Flughafen liegt in Diass, etwa 45 km vom Zentrum Dakars."),
    "ABJ": ("Abidjan", "Elfenbeinküste", "Flughafen Félix Houphouët-Boigny", "Weihnachten und die Sommerferien",
            "Das Visum für die Elfenbeinküste wird online (e-Visa) vor der Abreise beantragt. Eine Gelbfieberimpfung ist Pflicht."),
    "NBO": ("Nairobi", "Kenia", "Jomo Kenyatta International Airport", "Juli bis September und Weihnachten",
            "Für Kenia brauchst du vor der Abreise eine elektronische Einreisegenehmigung (eTA)."),
    "ALG": ("Algier", "Algerien", "Flughafen Houari Boumediene", "Juli, August und das Ende des Ramadan",
            "Für Algerien brauchst du ein Visum, das vor der Abreise beantragt wird (außer mit algerischer Staatsangehörigkeit)."),
}
DEST_EN = {"ACC": "Accra", "LOS": "Lagos", "ABV": "Abuja", "DLA": "Douala", "CMN": "Casablanca", "TUN": "Tunis", "CAI": "Cairo",
           "ADD": "Addis Ababa", "DSS": "Dakar", "ABJ": "Abidjan", "NBO": "Nairobi", "ALG": "Algiers"}
ROUTES = [("FRA", d) for d in ("ACC", "LOS", "ABV", "DLA", "CMN", "TUN", "CAI", "ADD", "DSS", "ABJ", "NBO", "ALG")] + \
         [("BER", d) for d in ("ACC", "LOS", "DLA", "CMN", "TUN", "CAI", "ADD", "NBO")] + \
         [("MUC", d) for d in ("ACC", "LOS", "CMN", "TUN", "CAI", "ADD", "NBO")] + \
         [("DUS", d) for d in ("ACC", "LOS", "DLA", "CMN", "TUN", "CAI")] + \
         [("HAM", d) for d in ("ACC", "LOS", "CMN", "TUN", "CAI")] + \
         [("CGN", d) for d in ("CMN", "TUN", "ACC")] + [("STR", d) for d in ("CMN", "TUN", "ACC")] + \
         [("VIE", d) for d in ("LOS", "ACC", "CMN", "TUN", "CAI", "ADD")]
GOV = "https://www.auswaertiges-amt.de/de/ReiseUndSicherheit/reise-und-sicherheitshinweise"


def slug(t):
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue")):
        t = t.replace(a, b)
    return B.slugify(t)


def path(r):
    return f"de/fluege-{slug(ORIG[r[0]][0])}-{slug(DEST[r[1]][0])}"


def build(site, ctx):
    airports = ctx["airports"]
    urls = []
    for r in ROUTES:
        fr_, to = r
        a, otip = ORIG[fr_]
        b, country, airport, peak, dtip = DEST[to]
        d, km = est(airports, fr_, to)
        dur = f"ca. {d} ohne Umstieg (geschätzt nach der Entfernung von {km:,} km)".replace(",", ".").replace(" h ", " Std. ").replace(" h", " Std.")
        dd = d.replace(" h ", " Std. ").replace(" h", " Std.")
        p = path(r)
        faq = [
            (f"Wie lange dauert ein Flug von {a} nach {b}?", f"Etwa {dd} ohne Umstieg (Schätzung nach der Entfernung). Mit Umstieg dauert die Reise je nach Anschluss oft mehrere Stunden länger."),
            (f"Wann sollte man einen günstigen Flug {a} – {b} buchen?", f"Meist zwei bis drei Monate vor dem Abflug. In der Hauptsaison ({peak}) steigen die Preise stark: Buche für diese Zeiten früher."),
            (f"An welchem Flughafen kommt man in {b} an?", f"Die Flüge landen am {airport} ({to})."),
            (f"Brauche ich ein Visum für {country}?", dtip if "Visum" in dtip else f"Das hängt von deiner Staatsangehörigkeit ab: Prüfe vor der Buchung die Reise- und Sicherheitshinweise des Auswärtigen Amts."),
            ("Ist Gepäck inklusive?", "Nicht immer. Die günstigsten Tarife enthalten manchmal nur ein kleines Handgepäck: Prüfe das Freigepäck, bevor du bezahlst."),
        ]
        others = [o for o in ROUTES if o != r and (o[0] == fr_ or o[1] == to)]
        hero = f"""<p class="eyebrow">{E(country)}</p>
  <h1>Günstige Flüge {E(a)} <span>→</span> {E(b)}</h1>
  <p class="codes" dir="ltr">{fr_} → {to}</p>
  <p class="hero-price" id="hero-price" hidden></p>
  <div class="cta-row"><a class="btn" href="{E(B.av_link(fr_, to))}" data-av="{fr_}-{to}" target="_blank" rel="sponsored noopener">Preise auf Aviasales ansehen</a><a class="btn ghost" href="/recherche/" data-wl="{fr_}-{to}">Live-Preise</a>{B.alert_btn("de")}</div>"""
        body = f"""<dl class="facts">
  <div><dt>Flugdauer</dt><dd>{E(dur[0].upper() + dur[1:])}</dd></div>
  <div><dt>Ankunft</dt><dd>{E(airport)} ({to})</dd></div>
  <div><dt>Teuerste Zeiten</dt><dd>{E(peak[0].upper() + peak[1:])}</dd></div>
</dl>
<section id="route-prices" data-from="{fr_}" data-to="{to}" hidden><h2>Kürzlich gefundene Preise</h2>
<p class="small">Niedrigste Preise für Hin- und Rückflug, die Reisende in den letzten Tagen gefunden haben, nach Abflugmonat. Der genaue Tarif erscheint auf der Buchungsseite.</p>
<ul class="price-list"></ul></section>
<script src="/route-prices.js" defer></script>
{B.calendar_html("de", fr_, to)}
<section><h2>Unsere Tipps für diese Strecke</h2><ul><li>{E(otip)}</li><li>{E(dtip)} Einreisebestimmungen ändern sich: Prüfe vor der Buchung die <a href="{GOV}" target="_blank" rel="noopener">Reise- und Sicherheitshinweise des Auswärtigen Amts</a>.</li></ul></section>
<section><h2>So zahlst du weniger</h2>
<ol class="steps">
<li><strong>Nutze flexible Daten.</strong> Ein oder zwei Tage früher oder später abzufliegen ändert den Preis oft mehr als die Wahl der Buchungsseite.</li>
<li><strong>Vergleiche Umsteigeflüge.</strong> Über Istanbul, Casablanca, Brüssel oder Addis Abeba ist es oft günstiger als direkt.</li>
<li><strong>Achte auf das Gepäck.</strong> Rechne den Koffer ein, bevor du zwei Tarife vergleichst.</li>
<li><strong>Stelle einen Preisalarm ein,</strong> wenn du erst in einigen Monaten fliegst: Du bekommst eine E-Mail, sobald der Preis fällt.</li>
</ol>
<p><a class="btn" href="{E(B.av_link(fr_, to))}" data-av="{fr_}-{to}" target="_blank" rel="sponsored noopener">{E(a)} → {E(b)} auf Aviasales suchen</a></p>
</section>
{B.extras_html(site, "de", b, DEST_EN[to], to)}
<section class="faq"><h2>Häufige Fragen</h2>
{"".join(f"<details><summary>{E(q)}</summary><p>{E(ans)}</p></details>" for q, ans in faq)}
</section>
<section><h2>Weitere Strecken</h2><ul class="route-links">{"".join(f'<li><a href="/{path(o)}/">{E(ORIG[o[0]][0])} → {E(DEST[o[1]][0])}</a></li>' for o in others)}</ul></section>"""
        urls.append(B.write(site, p, "de", f"Günstige Flüge {a} {b}: Preise vergleichen",
                            f"Günstiger Flug {a} – {b} ({fr_} → {to}): Flugdauer, wann buchen, Visum und echte Preise, kürzlich auf Aviasales gefunden.",
                            hero, body, B.faq_ld(faq), {"de": p}, ctx))
    groups = {}
    for r in ROUTES:
        groups.setdefault(r[0], []).append(r)
    body = "".join(
        f'<section><h2>Flüge ab {E(ORIG[o][0])}</h2><ul class="route-links">' + "".join(
            f'<li><a href="/{path(r)}/">{E(ORIG[r[0]][0])} → {E(DEST[r[1]][0])}</a></li>' for r in rs) + "</ul></section>"
        for o, rs in groups.items())
    body += f'<section><h2>Jede Woche die besten Angebote</h2><p>Die günstigsten Preise nach Afrika und in den Maghreb, jede Woche kostenlos auf WhatsApp.</p>{B.wa_btn("de")}</section>'
    hero = ('<h1>Günstige Flüge nach Afrika und in den Maghreb</h1><p class="hero-lead">Ab Frankfurt, Berlin, München, Düsseldorf, Hamburg, Köln, '
            'Stuttgart und Wien: Flugdauer, wann buchen und echte, kürzlich gefundene Preise, Strecke für Strecke.</p>')
    urls.append(B.write(site, "de", "de", "Günstige Flüge nach Afrika und in den Maghreb | Escale",
                        "Günstige Flüge ab Frankfurt, Berlin, München, Düsseldorf, Hamburg und Wien nach Accra, Lagos, Douala, Casablanca, Tunis, Kairo: echte Preise.",
                        hero, body, "", {"de": "de"}, ctx))
    return urls
