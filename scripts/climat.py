"""Climat et saisons, mois par mois, pour les 30 pages « Meilleur mois pour partir » (fr, en, it, de).

Données de climatologie générale (saisons sèches et des pluies, chaleur, froid) et périodes de forte demande
(vacances scolaires européennes, fêtes, retours de la diaspora). Ce sont des tendances moyennes, pas une prévision :
la page le dit et renvoie vers la météo officielle avant le départ. Aucun prix écrit ici.

Météo, une lettre par mois (janv. → déc.) : S sec et agréable, M variable ou doux avec quelques pluies,
P saison des pluies (ou cyclones), C très chaud, F froid ou frais.
Saison, une lettre par mois : H haute saison (prix plus hauts), m moyenne, b basse (souvent moins cher).
"""
import html
import json

E = html.escape

#        météo           saison          particularités
DATA = {
    "DSS": ("SSSSSSPPPPSS", "HmmmmmHHbbmH", ["diaspora", "rain_late"]),
    "ABJ": ("SSSMPPPMMPPS", "HmmmmbHHbbmH", ["diaspora", "two_rains"]),
    "RAK": ("FFSSSCCCSSSF", "bbmHmbHHbmmH", ["heat", "cold_nights"]),
    "CMN": ("MMMSSSSSSSMM", "bbbmmmHHbbbH", ["diaspora"]),
    "TUN": ("FFMSSSCCSSMF", "bbbmmmHHmbbm", ["diaspora"]),
    "DJE": ("FFMSSSCCSSMF", "bbbmmmHHmmbb", []),
    "AGA": ("SSSSSSSSSSSS", "mHmHbbHHbmmH", ["winter_sun"]),
    "CAI": ("SSSSCCCCCSSS", "HmmHbbbbbmmH", ["heat"]),
    "HRG": ("SSSSSCCCCSSS", "bmmHbbHHbHmH", ["heat", "winter_sun"]),
    "ZNZ": ("SSMPPSSSSSMS", "HmbbbmHHmmbH", ["long_rains"]),
    "NBO": ("SSMPPSSSSSPM", "HmbbbmHHmmbH", ["long_rains", "safari"]),
    "MRU": ("PPPMSSSSSSSM", "bbbmmmHHmHHH", ["cyclones"]),
    "RUN": ("PPPMSSSSSSSM", "bbbmbbHHbmmH", ["cyclones"]),
    "IST": ("FFFSSSCCSSMF", "bbbmHHHHHmbm", []),
    "DXB": ("SSSSCCCCCSSS", "HHHmbbbbbmHH", ["heat"]),
    "LIS": ("MMSSSSSSSSMM", "bbbmmHHHHmbm", []),
    "BCN": ("MMMSSSCCSSMM", "bbbmmHHHmmbm", []),
    "ROM": ("MMMSSSCCSSMM", "bbbmmHHHmmbm", []),
    "ATH": ("MMMSSCCCSSMM", "bbbmmHHHmmbb", ["heat"]),
    "LON": ("FFFMSSSSMMFF", "bbbmmHHHmmbH", ["rain_any"]),
    "NYC": ("FFFSSSCCSSMF", "bbbmmHHHmmmH", ["snow"]),
    "MIA": ("SSSSMPPPPMSS", "HHHmbbmbbbmH", ["hurricanes"]),
    "YMQ": ("FFFMSSSSSMFF", "bbbbmHHHmmbH", ["snow"]),
    "PTP": ("SSSSSMMPPPMS", "HHmHbbHHbbmH", ["hurricanes"]),
    "FDF": ("SSSSSMMPPPMS", "HHmHbbHHbbmH", ["hurricanes"]),
    "PUJ": ("SSSSMMMPPPMS", "HHHmbbmmbbmH", ["hurricanes", "sargassum"]),
    "CUN": ("SSSSMPMPPPSS", "HHHmbbmmbbmH", ["hurricanes", "sargassum"]),
    "BKK": ("SSCCCPPPPPSS", "HHmbbbmmbbmH", ["monsoon"]),
    "DPS": ("PPPSSSSSSSMP", "bbbmmmHHmmbH", ["monsoon"]),
    "TYO": ("FFMSSPCCMSSF", "bbHHmbHHbmHm", ["sakura", "tsuyu"]),
}

MONTHS = {
    "fr": ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "it": ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"],
    "de": ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."],
}
ICON = {"S": "☀️", "M": "🌤️", "P": "🌧️", "C": "🔥", "F": "❄️"}

T = {
    "fr": dict(
        h="Climat et saisons {a}, mois par mois", legend={"S": "sec et agréable", "M": "variable, quelques pluies", "P": "saison des pluies", "C": "très chaud", "F": "frais ou froid"},
        season={"H": "haute saison", "m": "saison moyenne", "b": "basse saison"}, weather="Météo", demand="Demande",
        best="Les plus beaux mois pour la météo : {x}.", rain="Saison des pluies : {x}.", hot="Fortes chaleurs : {x}.", cold="Mois frais ou froids : {x}.",
        high="Haute saison, prix souvent plus hauts : {x}.", low="Mois plus calmes, souvent moins chers : {x}.",
        deal="Le meilleur compromis entre météo et prix : {x}.", nodeal="Pas de mois idéal à la fois beau et calme : vise le début ou la fin de la belle saison.",
        note="Ce sont des tendances moyennes, pas une prévision : regarde la météo officielle quelques jours avant le départ.",
        tips={"diaspora": "Décembre et juillet-août sont les mois des retours au pays : les vols s'y remplissent vite, réserve 3 à 4 mois avant.",
              "rain_late": "Les pluies arrivent en général en juillet et culminent en août-septembre, avec une chaleur humide.",
              "two_rains": "Deux saisons des pluies : la grande de mai à juillet, la petite vers octobre-novembre.",
              "heat": "En plein été, la chaleur dépasse souvent 40 °C : préfère le printemps ou l'automne pour visiter.",
              "cold_nights": "En hiver, les journées sont douces mais les nuits sont froides : prévois un pull.",
              "winter_sun": "Une destination de soleil d'hiver : les vacances de février et de Noël font monter les prix.",
              "long_rains": "Les grandes pluies tombent surtout en avril-mai : beaucoup d'hôtels baissent leurs prix à cette période.",
              "safari": "La grande migration des gnous au Masai Mara a lieu en général de juillet à octobre : la période la plus demandée pour les safaris.",
              "cyclones": "De janvier à mars, chaleur humide et risque de cyclones : une assurance annulation est utile.",
              "rain_any": "Il peut pleuvoir toute l'année : un parapluie ne quitte jamais la valise.",
              "snow": "L'hiver est très froid, avec de la neige : les prix des vols baissent souvent en janvier-février.",
              "hurricanes": "La saison des ouragans va de juin à novembre, avec un pic d'août à octobre : regarde la météo et prends une assurance.",
              "sargassum": "Des algues sargasses arrivent souvent sur les plages au printemps et en été, selon les années.",
              "monsoon": "Pendant la mousson, les averses sont fortes mais souvent courtes, plutôt en fin de journée.",
              "sakura": "Les cerisiers fleurissent en général fin mars – début avril : la période la plus demandée, réserve tôt.",
              "tsuyu": "Juin est la saison des pluies (tsuyu), juillet-août sont chauds et humides, septembre peut connaître des typhons."},
        faq_q="Quel est le meilleur mois pour partir {a} ?", faq_q2="Quand les billets pour {n} sont-ils les moins chers ?",
        faq_a2="Les prix suivent la demande. {x} Le calendrier en haut de cette page montre le prix aller-retour le plus bas de chaque mois depuis ton aéroport."),
    "en": dict(
        h="{n} weather and seasons, month by month", legend={"S": "dry and pleasant", "M": "mixed, some rain", "P": "rainy season", "C": "very hot", "F": "cool or cold"},
        season={"H": "high season", "m": "shoulder season", "b": "low season"}, weather="Weather", demand="Demand",
        best="Best months for the weather: {x}.", rain="Rainy season: {x}.", hot="Very hot: {x}.", cold="Cool or cold months: {x}.",
        high="High season, prices often higher: {x}.", low="Quieter months, often cheaper: {x}.",
        deal="Best balance of weather and price: {x}.", nodeal="No month is both sunny and quiet: aim for the start or the end of the good season.",
        note="These are average trends, not a forecast: check the official weather a few days before you leave.",
        tips={"diaspora": "December and July-August are the months for going home to visit family: flights fill up fast, book 3 to 4 months ahead.",
              "rain_late": "The rains usually start in July and peak in August-September, with humid heat.",
              "two_rains": "Two rainy seasons: the long one from May to July, the short one around October-November.",
              "heat": "In high summer the heat often goes above 40 °C: spring or autumn are better for sightseeing.",
              "cold_nights": "In winter the days are mild but the nights are cold: pack a jumper.",
              "winter_sun": "A winter sun destination: February half-term and Christmas push prices up.",
              "long_rains": "The long rains fall mostly in April-May: many hotels lower their prices then.",
              "safari": "The great wildebeest migration in the Masai Mara usually runs from July to October: the busiest time for safaris.",
              "cyclones": "January to March is hot and humid, with a risk of cyclones: cancellation insurance is useful.",
              "rain_any": "It can rain at any time of year: always pack an umbrella.",
              "snow": "Winter is very cold, with snow: flight prices often drop in January-February.",
              "hurricanes": "Hurricane season runs from June to November, peaking from August to October: check the weather and get insurance.",
              "sargassum": "Sargassum seaweed often reaches the beaches in spring and summer, depending on the year.",
              "monsoon": "During the monsoon, showers are heavy but often short, mostly late in the day.",
              "sakura": "Cherry blossoms usually bloom in late March – early April: the busiest period, book early.",
              "tsuyu": "June is the rainy season (tsuyu), July-August are hot and humid, and September can bring typhoons."},
        faq_q="What is the best month to visit {n}?", faq_q2="When are flights to {n} cheapest?",
        faq_a2="Prices follow demand. {x} The calendar at the top of this page shows the lowest round-trip price for each month from your airport."),
    "it": dict(
        h="Clima e stagioni {a}, mese per mese", legend={"S": "secco e piacevole", "M": "variabile, qualche pioggia", "P": "stagione delle piogge", "C": "molto caldo", "F": "fresco o freddo"},
        season={"H": "alta stagione", "m": "media stagione", "b": "bassa stagione"}, weather="Meteo", demand="Domanda",
        best="I mesi migliori per il meteo: {x}.", rain="Stagione delle piogge: {x}.", hot="Caldo forte: {x}.", cold="Mesi freschi o freddi: {x}.",
        high="Alta stagione, prezzi spesso più alti: {x}.", low="Mesi più tranquilli, spesso più economici: {x}.",
        deal="Il miglior compromesso tra meteo e prezzo: {x}.", nodeal="Nessun mese è insieme bello e tranquillo: punta all'inizio o alla fine della bella stagione.",
        note="Sono tendenze medie, non una previsione: controlla il meteo ufficiale qualche giorno prima della partenza.",
        tips={"diaspora": "Dicembre e luglio-agosto sono i mesi dei ritorni a casa: i voli si riempiono presto, prenota 3-4 mesi prima.",
              "rain_late": "Le piogge arrivano di solito a luglio e sono più forti ad agosto-settembre, con caldo umido.",
              "two_rains": "Due stagioni delle piogge: la grande da maggio a luglio, la piccola verso ottobre-novembre.",
              "heat": "In piena estate il caldo supera spesso i 40 °C: meglio la primavera o l'autunno per visitare.",
              "cold_nights": "In inverno le giornate sono miti ma le notti fredde: porta un maglione.",
              "winter_sun": "Una meta di sole d'inverno: le vacanze di Natale e di febbraio fanno salire i prezzi.",
              "long_rains": "Le grandi piogge cadono soprattutto ad aprile-maggio: molti hotel abbassano i prezzi in quel periodo.",
              "safari": "La grande migrazione degli gnu nel Masai Mara va di solito da luglio a ottobre: il periodo più richiesto per i safari.",
              "cyclones": "Da gennaio a marzo caldo umido e rischio di cicloni: un'assicurazione annullamento è utile.",
              "rain_any": "Può piovere tutto l'anno: l'ombrello non lascia mai la valigia.",
              "snow": "L'inverno è molto freddo, con neve: i prezzi dei voli calano spesso a gennaio-febbraio.",
              "hurricanes": "La stagione degli uragani va da giugno a novembre, con un picco da agosto a ottobre: controlla il meteo e assicurati.",
              "sargassum": "Le alghe sargasso arrivano spesso sulle spiagge in primavera e in estate, a seconda degli anni.",
              "monsoon": "Durante il monsone gli acquazzoni sono forti ma spesso brevi, soprattutto a fine giornata.",
              "sakura": "I ciliegi fioriscono di solito tra fine marzo e inizio aprile: il periodo più richiesto, prenota presto.",
              "tsuyu": "Giugno è la stagione delle piogge (tsuyu), luglio-agosto sono caldi e umidi, settembre può portare tifoni."},
        faq_q="Qual è il mese migliore per andare {a}?", faq_q2="Quando i voli {a} costano meno?",
        faq_a2="I prezzi seguono la domanda. {x} Il calendario in cima a questa pagina mostra il prezzo andata e ritorno più basso di ogni mese dal tuo aeroporto."),
    "de": dict(
        h="Klima und Reisezeit {n}, Monat für Monat", legend={"S": "trocken und angenehm", "M": "wechselhaft, etwas Regen", "P": "Regenzeit", "C": "sehr heiß", "F": "kühl oder kalt"},
        season={"H": "Hochsaison", "m": "Zwischensaison", "b": "Nebensaison"}, weather="Wetter", demand="Nachfrage",
        best="Die besten Monate fürs Wetter: {x}.", rain="Regenzeit: {x}.", hot="Große Hitze: {x}.", cold="Kühle oder kalte Monate: {x}.",
        high="Hochsaison, Preise oft höher: {x}.", low="Ruhigere Monate, oft günstiger: {x}.",
        deal="Der beste Kompromiss aus Wetter und Preis: {x}.", nodeal="Kein Monat ist zugleich sonnig und ruhig: Ziele auf den Anfang oder das Ende der guten Saison.",
        note="Das sind Durchschnittswerte, keine Vorhersage: Prüfe ein paar Tage vor dem Abflug den offiziellen Wetterbericht.",
        tips={"diaspora": "Dezember und Juli-August sind die Monate der Heimreisen: Die Flüge sind schnell voll, buche 3 bis 4 Monate vorher.",
              "rain_late": "Der Regen beginnt meist im Juli und ist im August-September am stärksten, bei feuchter Hitze.",
              "two_rains": "Zwei Regenzeiten: die große von Mai bis Juli, die kleine um Oktober-November.",
              "heat": "Im Hochsommer steigt die Hitze oft über 40 °C: Frühling oder Herbst sind für Besichtigungen besser.",
              "cold_nights": "Im Winter sind die Tage mild, die Nächte aber kalt: Pack einen Pullover ein.",
              "winter_sun": "Ein Ziel für Wintersonne: Die Weihnachts- und Winterferien treiben die Preise nach oben.",
              "long_rains": "Der große Regen fällt vor allem im April-Mai: Viele Hotels senken dann ihre Preise.",
              "safari": "Die große Gnu-Wanderung in der Masai Mara findet meist von Juli bis Oktober statt: die gefragteste Zeit für Safaris.",
              "cyclones": "Von Januar bis März ist es heiß und feucht, mit Zyklon-Risiko: Eine Reiserücktrittsversicherung ist sinnvoll.",
              "rain_any": "Regnen kann es das ganze Jahr: Der Schirm gehört immer in den Koffer.",
              "snow": "Der Winter ist sehr kalt, mit Schnee: Die Flugpreise sinken oft im Januar-Februar.",
              "hurricanes": "Die Hurrikansaison dauert von Juni bis November, mit dem Höhepunkt von August bis Oktober: Prüfe das Wetter und versichere dich.",
              "sargassum": "Sargassum-Algen erreichen je nach Jahr oft im Frühling und Sommer die Strände.",
              "monsoon": "Während des Monsuns sind die Schauer heftig, aber oft kurz, meist am späten Nachmittag.",
              "sakura": "Die Kirschblüte ist meist Ende März bis Anfang April: die gefragteste Zeit, buche früh.",
              "tsuyu": "Der Juni ist Regenzeit (Tsuyu), Juli-August sind heiß und schwül, im September kann es Taifune geben."},
        faq_q="Was ist der beste Monat für eine Reise nach {n}?", faq_q2="Wann sind Flüge nach {n} am günstigsten?",
        faq_a2="Die Preise folgen der Nachfrage. {x} Der Kalender oben auf dieser Seite zeigt den niedrigsten Hin- und Rückflugpreis jedes Monats ab deinem Flughafen."),
}
AND = {"fr": " et ", "en": " and ", "it": " e ", "de": " und "}


def ranges(idx, lang):
    """[0,1,2,6,7] -> « janv. – mars, juil. et août » (en passant d'une année à l'autre : nov. – févr.)."""
    m, s = MONTHS[lang], set(idx)
    if not s:
        return ""
    if len(s) == 12:
        return {"fr": "toute l'année", "en": "all year round", "it": "tutto l'anno", "de": "das ganze Jahr"}[lang]
    start = next(i for i in range(12) if i in s and (i - 1) % 12 not in s)
    runs, cur = [], []
    for k in range(12):
        i = (start + k) % 12
        if i in s:
            cur.append(i)
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    out = []
    for r in runs:
        a, b = m[r[0]], m[r[-1]]
        out.append(a if len(r) == 1 else (f"{a}{AND[lang]}{b}" if len(r) == 2 else f"{a} – {b}"))
    return ", ".join(out)


def render(code, lang, name, a=""):
    """(html, faq_ld_items) pour une destination, ou ("", []) si pas de données."""
    if code not in DATA or lang not in T:
        return "", []
    w, s, tips = DATA[code]
    t = T[lang]
    pick = lambda txt, ch: [i for i in range(12) if txt[i] in ch]
    good = pick(w, "S")
    deal = [i for i in good if s[i] in "bm"] or [i for i in pick(w, "SM") if s[i] == "b"]
    lines = [t["best"].format(x=ranges(good or pick(w, "SM"), lang))]
    for key, ch in (("rain", "P"), ("hot", "C"), ("cold", "F")):
        if pick(w, ch):
            lines.append(t[key].format(x=ranges(pick(w, ch), lang)))
    lines.append(t["high"].format(x=ranges(pick(s, "H"), lang)))
    lines.append(t["low"].format(x=ranges(pick(s, "b"), lang)))
    lines.append(t["deal"].format(x=ranges(deal, lang)) if deal else t["nodeal"])
    lines = [x.replace("..", ".") for x in lines]
    m = MONTHS[lang]
    cells = "".join(
        f'<li class="cl-m cl-{s[i]}"><b>{E(m[i])}</b><span class="cl-i" role="img" aria-label="{E(t["legend"][w[i]])}">{ICON[w[i]]}</span>'
        f'<small>{E(t["season"][s[i]])}</small></li>' for i in range(12))
    legend = " · ".join(f"{ICON[k]} {E(v)}" for k, v in t["legend"].items())
    head = t["h"].format(a=a or name, n=name)
    body = (f'<section class="climat"><h2>{E(head)}</h2><ol class="cl-grid">{cells}</ol><p class="small cl-leg">{legend}</p>'
            + "<ul>" + "".join(f"<li>{E(x)}</li>" for x in lines) + "</ul>"
            + "".join(f"<p>{E(t['tips'][k])}</p>" for k in tips if k in t["tips"])
            + f'<p class="small">{E(t["note"])}</p></section>')
    qn = dict(a=a or name, n=name)
    ans1 = " ".join([lines[0], lines[-1]] + [t["tips"][k] for k in tips[:1] if k in t["tips"]])
    ans2 = " ".join([lines[-3], lines[-2]])
    faq = [(t["faq_q"].format(**qn), ans1), (t["faq_q2"].format(**qn), t["faq_a2"].format(x=ans2))]
    return body, [(q, r.replace("..", ".")) for q, r in faq]


def faq_ld(items):
    return '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in items]},
        ensure_ascii=False) + "</script>"


def faq_html(items, lang):
    h = {"fr": "Questions fréquentes", "en": "Frequently asked questions", "it": "Domande frequenti", "de": "Häufige Fragen"}[lang]
    return f'<section class="faq"><h2>{E(h)}</h2>' + "".join(f"<details><summary>{E(q)}</summary><p>{E(r)}</p></details>" for q, r in items) + "</section>"
