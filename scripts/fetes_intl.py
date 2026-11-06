"""« Christmas flights 2026 » (anglais, diaspora du Royaume-Uni) et « Voli per Natale 2026 » (italien, diaspora en Italie), par destination.

Même principe que fetes_dest.py (pages françaises) : prix repérés par période et par aéroport de départ (site/ete.js, /api/prix),
quand partir et réserver, alerte prix. Aucun prix écrit. Dates des vacances scolaires : variables selon les écoles ou les régions,
la page le dit. À mettre à jour chaque année.
"""
import html
import json

import build_i18n as B

E = html.escape

CONF = {
    "en": dict(
        base="en/christmas-flights-2026", hero="LHR", origins=[("LHR", "London Heathrow"), ("LGW", "London Gatwick"), ("MAN", "Manchester"), ("BHX", "Birmingham")],
        dests=["LOS", "ACC", "ABV", "NBO", "JNB", "ADD", "HRE", "FIH", "DSS", "ABJ", "CMN"],
        dates="Christmas Day falls on Friday 25 December 2026. Most UK schools break up around 18 December 2026 and go back around 4-5 January 2027, but dates vary by council and school: check yours.",
        periods=[("2026-12", "2027-01", "2026-12-19", "2027-01-03", "School holidays: 19 Dec → 3 Jan", "The busiest dates."),
                 ("2026-12", "2027-01", "2026-12-12", "2027-01-02", "Leave mid-December, back early January", "Leaving a week before the holidays is often cheaper."),
                 ("2026-12", "2027-01", "2026-12-26", "2027-01-10", "Leave after Christmas, back mid-January", "Boxing Day departures and returns after 5 January are often quieter.")],
        dep="2026-12-19", ret="2027-01-03", month="2026-12",
        busy="Around Christmas, departures on the first weekend of the school holidays and returns on the last weekend (2-3 January) are the most expensive.",
        book="As early as possible: a few weeks before Christmas, fares rise almost every week. If it is too expensive, move your departure by a few days or compare another UK airport.",
        bags="Travelling with gifts? Compare fares that include two checked bags: they often cost less than a basic fare plus extra luggage.",
        arrive="Flights land at {ap} ({code}). If you arrive late, book your transfer or your first night before you leave.",
        t_title="{c} flights for Christmas 2026: prices and dates | Escale",
        t_desc="Flights to {c} for Christmas 2026 (Friday 25 December): fares found from London, Manchester and Birmingham, when to leave and when to book.",
        eyebrow="Christmas 2026 · {country}", h1="Flights to {c} for Christmas 2026", lead="Christmas 2026 is on Friday 25 December: fares found to fly home to {c}, the best time to leave and to book.",
        cta="Compare Christmas flights", when_h="When is Christmas 2026?", leave_h="When to leave?", th_p="Period (from London Heathrow)", th_o="Route (leaving and returning in December-January)",
        th_price="Fare found", see="See flights", from_h="Which UK airport?", know_h="Good to know for Christmas 2026", bookh="When to book?",
        note="Lowest round-trip fare recently found for each period, per person. The dates shown are those of the flight found; the exact fare is confirmed on the booking site. No price yet means few travellers have searched these dates: set an alert to be told.",
        wa_h="Deals every week", wa_p="The lowest fares to {c} and Africa, every week on WhatsApp, for free.",
        faq=[("When is Christmas 2026?", "{dates}"), ("When should I book a flight to {c} for Christmas 2026?", "{book}")],
        hub_t="Christmas 2026 flights home: prices by destination | Escale", hub_d="Flights for Christmas 2026 from the UK to Lagos, Accra, Abuja, Nairobi, Johannesburg, Addis Ababa, Harare and more: fares found and when to book.",
        hub_h1="Fly home for Christmas 2026", hub_lead="Christmas 2026 is on Friday 25 December. For each destination: fares found from the UK, the best time to leave and to book.",
        hub_pick="Pick your destination", others="Other destinations for Christmas", link="🎄 Christmas 2026: fares and dates for {c} →",
        flex="Turn on flexible dates (±3 days) in the search: moving your departure by a few days often changes the price a lot."),
    "it": dict(
        base="it/voli-natale-2026", hero="MXP", origins=[("MXP", "Milano Malpensa"), ("BGY", "Bergamo"), ("FCO", "Roma Fiumicino"), ("VCE", "Venezia"), ("BLQ", "Bologna"), ("NAP", "Napoli")],
        dests=["DSS", "ABJ", "LOS", "ACC", "OUA", "BKO", "DLA", "CMN", "TUN"],
        dates="Natale cade venerdì 25 dicembre 2026. Le vacanze scolarie di Natale vanno di solito dal 23 dicembre all'Epifania (mercoledì 6 gennaio 2027), con differenze tra regioni: controlla il calendario della tua.",
        periods=[("2026-12", "2027-01", "2026-12-20", "2027-01-06", "Vacanze di Natale: 20 dic → 6 gen", "Le date più richieste."),
                 ("2026-12", "2027-01", "2026-12-13", "2027-01-03", "Partenza a metà dicembre, ritorno a inizio gennaio", "Partire una settimana prima delle vacanze costa spesso meno."),
                 ("2026-12", "2027-01", "2026-12-27", "2027-01-10", "Partenza dopo Natale, ritorno a metà gennaio", "Le partenze dopo il 26 dicembre e i ritorni dopo l'Epifania sono spesso più tranquilli.")],
        dep="2026-12-20", ret="2027-01-06", month="2026-12",
        busy="A Natale, le partenze del primo fine settimana delle vacanze e i ritorni intorno all'Epifania sono i più cari.",
        book="Il prima possibile: a poche settimane da Natale i prezzi salgono quasi ogni settimana. Se è troppo caro, sposta la partenza di qualche giorno o confronta un altro aeroporto italiano.",
        bags="Viaggi con i regali? Confronta le tariffe con due bagagli in stiva inclusi: spesso costano meno di una tariffa base con i bagagli in più.",
        arrive="I voli arrivano all'aeroporto {ap} ({code}). Se arrivi tardi, prenota il transfer o la prima notte prima di partire.",
        t_title="Voli per {c} a Natale 2026: prezzi e date | Escale",
        t_desc="Voli per {c} per Natale 2026 (venerdì 25 dicembre): prezzi trovati da Milano, Bergamo, Roma, Venezia, Bologna e Napoli, quando partire e prenotare.",
        eyebrow="Natale 2026 · {country}", h1="Voli per {c} a Natale 2026", lead="Natale 2026 cade venerdì 25 dicembre: i prezzi trovati per tornare a {c}, il momento migliore per partire e per prenotare.",
        cta="Confronta i voli di Natale", when_h="Quando cade Natale 2026?", leave_h="Quando partire?", th_p="Periodo (da Milano Malpensa)", th_o="Tratta (andata e ritorno tra dicembre e gennaio)",
        th_price="Prezzo trovato", see="Vedi i voli", from_h="Da quale aeroporto partire?", know_h="Da sapere per Natale 2026", bookh="Quando prenotare?",
        note="Prezzo andata e ritorno più basso trovato di recente per ogni periodo, a persona. Le date sono quelle del volo trovato; la tariffa esatta si conferma sul sito di prenotazione. Se non c'è ancora un prezzo, pochi viaggiatori hanno cercato queste date: crea un avviso.",
        wa_h="Le offerte ogni settimana", wa_p="I prezzi più bassi per {c} e l'Africa, ogni settimana su WhatsApp, gratis.",
        faq=[("Quando cade Natale 2026?", "{dates}"), ("Quando prenotare un volo per {c} per Natale 2026?", "{book}")],
        hub_t="Natale 2026 a casa: prezzi dei voli per destinazione | Escale", hub_d="Voli per Natale 2026 dall'Italia per Dakar, Abidjan, Lagos, Accra, Ouagadougou, Bamako, Douala, Casablanca e Tunisi: prezzi trovati e quando prenotare.",
        hub_h1="Tornare a casa per Natale 2026", hub_lead="Natale 2026 cade venerdì 25 dicembre. Per ogni destinazione: i prezzi trovati dall'Italia, il momento migliore per partire e per prenotare.",
        hub_pick="Scegli la tua destinazione", others="Altre destinazioni per Natale", link="🎄 Natale 2026: prezzi e date per {c} →",
        flex="Attiva le date flessibili (±3 giorni) nella ricerca: spostare la partenza di qualche giorno cambia spesso molto il prezzo."),
}
NAMES_IT = {"DSS": "Dakar", "ABJ": "Abidjan", "LOS": "Lagos", "ACC": "Accra", "OUA": "Ouagadougou", "BKO": "Bamako", "DLA": "Douala", "CMN": "Casablanca", "TUN": "Tunisi"}
COUNTRY = {"LOS": ("Nigeria", "Nigeria"), "ACC": ("Ghana", "Ghana"), "ABV": ("Nigeria", "Nigeria"), "NBO": ("Kenya", "Kenya"), "JNB": ("South Africa", "Sudafrica"),
           "ADD": ("Ethiopia", "Etiopia"), "HRE": ("Zimbabwe", "Zimbabwe"), "FIH": ("DR Congo", "RD Congo"), "DSS": ("Senegal", "Senegal"), "ABJ": ("Côte d'Ivoire", "Costa d'Avorio"),
           "CMN": ("Morocco", "Marocco"), "OUA": ("Burkina Faso", "Burkina Faso"), "BKO": ("Mali", "Mali"), "DLA": ("Cameroon", "Camerun"), "TUN": ("Tunisia", "Tunisia")}
NAMES_EN = {"LOS": "Lagos", "ACC": "Accra", "ABV": "Abuja", "NBO": "Nairobi", "JNB": "Johannesburg", "ADD": "Addis Ababa", "HRE": "Harare", "FIH": "Kinshasa",
            "DSS": "Dakar", "ABJ": "Abidjan", "CMN": "Casablanca"}


def slug(c):
    return B.slugify(c)


def build(site, ctx):
    urls, links = [], {}
    airports = ctx["airports"]
    for lang, t in CONF.items():
        names = NAMES_EN if lang == "en" else NAMES_IT
        paths_of = {code: f'{t["base"]}-{slug(names[code])}' for code in t["dests"]}
        th = '<thead><tr><th scope="col">{}</th><th scope="col">' + E(t["th_price"]) + '</th><th scope="col"><span class="sr-only">' + E(t["see"]) + "</span></th></tr></thead>"
        q = "&amp;lang=" + lang
        for code in t["dests"]:
            c = names[code]
            country = COUNTRY[code][0 if lang == "en" else 1]
            ap = airports.get(code, [code, c, c])[2]
            h0 = t["hero"]
            rows = "".join(
                f'<tr data-from="{h0}" data-to="{code}" data-dep="{a}" data-ret="{b}"><th scope="row">{E(lab)}<span class="small ete-note">{E(note)}</span></th><td class="fp" aria-live="polite">…</td>'
                f'<td><a class="price-go" href="/?type=vols&amp;from={h0}&amp;to={code}&amp;dep={d1}&amp;ret={d2}{q}">{E(t["see"])}</a></td></tr>' for a, b, d1, d2, lab, note in t["periods"])
            orig = "".join(
                f'<tr data-from="{o}" data-to="{code}" data-dep="{t["month"]}" data-ret="2027-01"><th scope="row">{E(on)} → {E(c)}</th><td class="fp" aria-live="polite">…</td>'
                f'<td><a class="price-go" href="/?type=vols&amp;from={o}&amp;to={code}&amp;dep={t["dep"]}&amp;ret={t["ret"]}{q}">{E(t["see"])}</a></td></tr>' for o, on in t["origins"])
            hero = (f'<p class="eyebrow">{E(t["eyebrow"].format(country=country))}</p><h1>{E(t["h1"].format(c=c))}</h1><p class="hero-lead">{E(t["lead"].format(c=c))}</p>'
                    f'<p class="hero-price" id="hero-price" hidden></p><div class="cta-row"><a class="btn" href="/?type=vols&amp;from={h0}&amp;to={code}&amp;dep={t["dep"]}&amp;ret={t["ret"]}{q}">{E(t["cta"])}</a>{B.alert_btn(lang)}</div>')
            faq = [(a.format(c=c), b.format(dates=t["dates"], book=t["book"])) for a, b in t["faq"]]
            body = (f'<section><h2>{E(t["when_h"])}</h2><p>{E(t["dates"])}</p></section>'
                    f'<section><h2>{E(t["leave_h"])}</h2><table class="fete-table ete-table" data-hero="{h0}">{th.format(E(t["th_p"]))}<tbody>{rows}</tbody></table><p class="small">{E(t["note"])}</p></section>'
                    f'<section><h2>{E(t["from_h"])}</h2><table class="fete-table ete-table">{th.format(E(t["th_o"]))}<tbody>{orig}</tbody></table></section>'
                    f'<section id="price-alert" class="price-alert" data-from="{h0}" data-to="{code}" hidden></section>'
                    f'<section><h2>{E(t["know_h"])}</h2><ul><li>{E(t["busy"])}</li><li>{E(t["arrive"].format(ap=ap, code=code))}</li><li>{E(t["bags"])}</li></ul></section>'
                    f'<section><h2>{E(t["bookh"])}</h2><p>{E(t["book"])} {E(t["flex"])}</p></section>'
                    f'<section><h2>{E(t["wa_h"])}</h2><p>{E(t["wa_p"].format(c=c))}</p>{B.wa_btn(lang)}</section>'
                    f'<section class="faq"><h2>{"Frequently asked questions" if lang == "en" else "Domande frequenti"}</h2>' + "".join(f"<details><summary>{E(a)}</summary><p>{E(b)}</p></details>" for a, b in faq) + "</section>"
                    + f'<section><h2>{E(t["others"])}</h2><ul class="links">' + "".join(f'<li><a href="/{paths_of[o]}/">{E(names[o])}</a></li>' for o in t["dests"] if o != code) + "</ul></section>"
                    + '<script src="/ete.js" defer></script><script src="/alerts.js" defer></script>')
            urls.append(B.write(site, paths_of[code], lang, t["t_title"].format(c=c), t["t_desc"].format(c=c), hero, body, B.faq_ld(faq), {lang: paths_of[code]}, ctx))
            links[(lang, code)] = (paths_of[code], t["link"].format(c=c))
        items = "".join(f'<li><a href="/{paths_of[c]}/"><strong>{E(names[c])}</strong></a> · <span class="small">{E(COUNTRY[c][0 if lang == "en" else 1])}</span></li>' for c in t["dests"])
        hero = f'<p class="eyebrow">🎄 {"Christmas" if lang == "en" else "Natale"} 2026</p><h1>{E(t["hub_h1"])}</h1><p class="hero-lead">{E(t["hub_lead"])}</p>'
        body = (f'<section><h2>{E(t["hub_pick"])}</h2><ul class="route-links">{items}</ul></section><section><h2>{E(t["when_h"])}</h2><p>{E(t["dates"])}</p><p>{E(t["busy"])} {E(t["book"])}</p></section>'
                + B.wa_btn(lang))
        urls.append(B.write(site, t["base"], lang, t["hub_t"], t["hub_d"], hero, body, "", {lang: t["base"]}, ctx))
    return urls, links


def link_pages(site, links):
    """Lien « Christmas 2026 / Natale 2026 » sur les pages trajets anglaises et italiennes vers ces destinations, et sur les pages fêtes."""
    import re
    n = 0
    for f in list(site.glob("en/*/index.html")) + list(site.glob("it/*/index.html")):
        s = f.read_text(encoding="utf-8")
        if "xmas-link" in s:
            continue
        m = re.search(r'<html lang="(en|it)"', s[:400])
        c = re.search(r'data-to="([A-Z]{3})"', s)
        k = s.find('<section class="faq"')
        if not m or not c or k < 0 or (m.group(1), c.group(1)) not in links:
            continue
        p, label = links[(m.group(1), c.group(1))]
        if f"/{p}/" in str(f):
            continue
        s = s[:k] + f'<p class="xmas-link mm-link"><a href="/{p}/">{E(label)}</a></p>' + s[k:]
        f.write_text(s, encoding="utf-8")
        n += 1
    hubs = {"en": (site / "en" / "holiday-flights" / "index.html", "en/christmas-flights-2026", "🎄 Christmas 2026: fares by destination from the UK →"),
            "it": (site / "it" / "index.html", "it/voli-natale-2026", "🎄 Natale 2026: i prezzi dei voli per destinazione dall'Italia →")}
    for lang, (f, p, label) in hubs.items():
        if f.exists():
            s = f.read_text(encoding="utf-8")
            if f'href="/{p}/"' not in s and "</main>" in s:
                k = s.find("<section")
                k = k if k > 0 else s.find("</main>")
                s = s[:k] + f'<p class="xmas-link mm-link"><a href="/{p}/">{E(label)}</a></p>' + s[k:]
                f.write_text(s, encoding="utf-8")
    return n
