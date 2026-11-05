"""Page « Destinations tendance 2027 » (fr, en).

Sources vérifiées en novembre 2026 :
- Skyscanner Travel Trends 2027 (skyscanner.net) : hausse des recherches de vols aller-retour (1er janvier - 17 juin 2026 comparé à 2025).
- Lonely Planet Best in Travel 2027 : sélection de destinations (pas de classement officiel repris ici).
Les prix ne sont jamais écrits dans la page : site/tendances.js les charge en direct (/api/calendar) depuis l'aéroport du visiteur.
Photos : Wikimedia Commons, licences libres (site/data/tendances-photos.json, auteurs affichés sous chaque photo).
"""
import html
import json

import build_i18n as B

E = html.escape
SKY = "https://www.skyscanner.net/travel-trends/destinations"
LP = "https://www.lonelyplanet.com/best-in-travel"

# clé photo, codes d'aéroport (essayés dans l'ordre), nom fr, nom en, pays fr, pays en, hausse des recherches
SKYSCANNER = [
    ("bishkek", "FRU", "Bichkek", "Bishkek", "Kirghizistan", "Kyrgyzstan", 501),
    ("hurghada", "HRG", "Hurghada", "Hurghada", "Égypte", "Egypt", 186),
    ("malmo", "MMX,CPH", "Malmö", "Malmö", "Suède", "Sweden", 103),
    ("trapani", "TPS,PMO", "Trapani", "Trapani", "Sicile, Italie", "Sicily, Italy", 95),
    ("chongqing", "CKG", "Chongqing", "Chongqing", "Chine", "China", 70),
    ("danang", "DAD", "Da Nang", "Da Nang", "Vietnam", "Vietnam", 68),
    ("sal", "SID", "Sal", "Sal", "Cap-Vert", "Cape Verde", 67),
]
# clé photo, codes, nom fr, nom en, pays fr, pays en, pourquoi (fr, en)
LONELY = [
    ("quebec", "YQB,YMQ", "Québec", "Québec City", "Canada", "Canada", ("Le Vieux-Québec, ville fortifiée classée à l'UNESCO.", "Old Québec, a walled city listed by UNESCO.")),
    ("redwoods", "SFO", "Les séquoias de Californie", "California's coast redwoods", "États-Unis", "USA", ("Les arbres les plus hauts du monde, au bord du Pacifique.", "The tallest trees on Earth, by the Pacific.")),
    ("venetie", "VCE", "La Vénétie", "Veneto", "Italie", "Italy", ("Venise, les Dolomites et le lac de Garde.", "Venice, the Dolomites and Lake Garda.")),
    ("sibenik", "SPU,ZAD", "Šibenik", "Šibenik", "Croatie", "Croatia", ("Deux sites UNESCO et les cascades de Krka tout près.", "Two UNESCO sites, with the Krka waterfalls nearby.")),
    ("rabat", "RBA", "Rabat", "Rabat", "Maroc", "Morocco", ("La capitale du Maroc, classée à l'UNESCO depuis 2012.", "Morocco's capital, a UNESCO site since 2012.")),
    ("okinawa", "OKA", "Okinawa", "Okinawa", "Japon", "Japan", ("Plages subtropicales et culture ryūkyū.", "Subtropical beaches and Ryukyuan culture.")),
    ("maldives", "MLE", "Fulidhoo, Maldives", "Fulidhoo, Maldives", "Maldives", "Maldives", ("Une île de pêcheurs, alternative aux grands resorts.", "A fishing island, an alternative to big resorts.")),
]
NEAR = {"MMX,CPH": ("vol pour Copenhague, puis 20 min de train", "fly to Copenhagen, then 20 min by train"),
        "TPS,PMO": ("ou vol pour Palerme", "or fly to Palermo"), "SPU,ZAD": ("vol pour Split ou Zadar", "fly to Split or Zadar"),
        "SFO": ("vol pour San Francisco", "fly to San Francisco"), "YQB,YMQ": ("ou vol pour Montréal", "or fly to Montréal")}

# Noms et pays en italien / allemand (clé photo -> (nom it, pays it, nom de, pays de)), raisons et accès
ITDE = {
    "bishkek": ("Biškek", "Kirghizistan", "Bischkek", "Kirgisistan"), "hurghada": ("Hurghada", "Egitto", "Hurghada", "Ägypten"),
    "malmo": ("Malmö", "Svezia", "Malmö", "Schweden"), "trapani": ("Trapani", "Sicilia, Italia", "Trapani", "Sizilien, Italien"),
    "chongqing": ("Chongqing", "Cina", "Chongqing", "China"), "danang": ("Da Nang", "Vietnam", "Da Nang", "Vietnam"),
    "sal": ("Sal", "Capo Verde", "Sal", "Kap Verde"), "quebec": ("Québec", "Canada", "Québec", "Kanada"),
    "redwoods": ("Le sequoie della California", "Stati Uniti", "Die Küstenmammutbäume Kaliforniens", "USA"),
    "venetie": ("Il Veneto", "Italia", "Venetien", "Italien"), "sibenik": ("Šibenik (Sebenico)", "Croazia", "Šibenik", "Kroatien"),
    "rabat": ("Rabat", "Marocco", "Rabat", "Marokko"), "okinawa": ("Okinawa", "Giappone", "Okinawa", "Japan"),
    "maldives": ("Fulidhoo, Maldive", "Maldive", "Fulidhoo, Malediven", "Malediven"),
}
WHY_ITDE = {
    "quebec": ("La Vecchia Québec, città fortificata patrimonio UNESCO.", "Die Altstadt von Québec, eine befestigte Stadt und UNESCO-Welterbe."),
    "redwoods": ("Gli alberi più alti del mondo, sul Pacifico.", "Die höchsten Bäume der Welt, am Pazifik."),
    "venetie": ("Venezia, le Dolomiti e il lago di Garda.", "Venedig, die Dolomiten und der Gardasee."),
    "sibenik": ("Due siti UNESCO e le cascate di Krka a due passi.", "Zwei UNESCO-Stätten, die Krka-Wasserfälle ganz in der Nähe."),
    "rabat": ("La capitale del Marocco, patrimonio UNESCO dal 2012.", "Marokkos Hauptstadt, seit 2012 UNESCO-Welterbe."),
    "okinawa": ("Spiagge subtropicali e cultura delle Ryūkyū.", "Subtropische Strände und Ryūkyū-Kultur."),
    "maldives": ("Un'isola di pescatori, alternativa ai grandi resort.", "Eine Fischerinsel, eine Alternative zu großen Resorts."),
}
NEAR_ITDE = {"MMX,CPH": ("volo per Copenaghen, poi 20 min di treno", "Flug nach Kopenhagen, dann 20 Min. mit dem Zug"),
             "TPS,PMO": ("oppure volo per Palermo", "oder Flug nach Palermo"), "SPU,ZAD": ("volo per Spalato o Zara", "Flug nach Split oder Zadar"),
             "SFO": ("volo per San Francisco", "Flug nach San Francisco"), "YQB,YMQ": ("oppure volo per Montréal", "oder Flug nach Montreal")}

T = {
    "fr": dict(path="tendances-2027", title="Destinations tendance 2027 : où partir en 2027 (Skyscanner, Lonely Planet) | Escale",
               desc="Les destinations qui montent en 2027 selon Skyscanner et Lonely Planet : Hurghada, Da Nang, Cap-Vert, Québec, Vénétie, Rabat… avec le prix des vols en direct depuis chez vous.",
               h1="Où partir <span>en 2027</span> ?", lead="Les destinations qui montent, d'après les recherches de vols Skyscanner et la sélection Lonely Planet. Le prix affiché est le meilleur aller-retour trouvé en ce moment depuis votre aéroport.",
               sky_h="Les destinations qui explosent sur Skyscanner", sky_p="Hausse des recherches de vols aller-retour sur Skyscanner (skyscanner.net), du 1er janvier au 17 juin 2026, comparé à la même période en 2025.",
               lp_h="Les coups de cœur de Lonely Planet", lp_p="Sélection extraite de Lonely Planet Best in Travel 2027 (l'ordre ci-dessous n'est pas un classement).",
               more="Sources", src_sky="Skyscanner Travel Trends 2027", src_lp="Lonely Planet Best in Travel 2027",
               searches="de recherches", from_l="dès", loading="Prix en cours…", none="Comparer les prix", photo="Photo",
               note="Prix aller-retour en direct (calendrier des prix Escale), pour une date précise : ils changent tous les jours. Les tendances viennent des sources citées, vérifiées en novembre 2026.",
               cta="Chercher un autre vol", from_txt="Prix depuis", bell="Alerte prix", alert_for="Alerte pour :"),
    "en": dict(path="en/trending-2027", title="Trending destinations 2027: where to travel in 2027 (Skyscanner, Lonely Planet) | Escale",
               desc="The destinations on the rise in 2027 according to Skyscanner and Lonely Planet: Hurghada, Da Nang, Cape Verde, Québec, Veneto, Rabat… with live flight prices from your airport.",
               h1="Where to go <span>in 2027</span>?", lead="The destinations on the rise, from Skyscanner flight searches and Lonely Planet's picks. The price shown is the best round trip found right now from your airport.",
               sky_h="Skyscanner's fastest-rising destinations", sky_p="Increase in round-trip flight searches on Skyscanner (skyscanner.net), 1 January to 17 June 2026 compared with the same period in 2025.",
               lp_h="Lonely Planet's picks", lp_p="A selection from Lonely Planet Best in Travel 2027 (the order below is not a ranking).",
               more="Sources", src_sky="Skyscanner Travel Trends 2027", src_lp="Lonely Planet Best in Travel 2027",
               searches="searches", from_l="from", loading="Loading price…", none="Compare prices", photo="Photo",
               note="Live round-trip prices (Escale price calendar), for a specific date: they change every day. Trends come from the sources cited, checked in November 2026.",
               cta="Search another flight", from_txt="Prices from", bell="Price alert", alert_for="Alert for:"),
    "it": dict(path="it/tendenze-2027", title="Destinazioni di tendenza 2027: dove andare nel 2027 (Skyscanner, Lonely Planet) | Escale",
               desc="Le destinazioni in ascesa nel 2027 secondo Skyscanner e Lonely Planet: Hurghada, Da Nang, Capo Verde, Québec, Veneto, Rabat… con i prezzi dei voli in diretta dal tuo aeroporto.",
               h1="Dove andare <span>nel 2027</span>?", lead="Le destinazioni in ascesa, secondo le ricerche di voli su Skyscanner e la selezione di Lonely Planet. Il prezzo mostrato è il miglior andata e ritorno trovato ora dal tuo aeroporto.",
               sky_h="Le destinazioni che crescono di più su Skyscanner", sky_p="Aumento delle ricerche di voli andata e ritorno su Skyscanner (skyscanner.net), dal 1° gennaio al 17 giugno 2026 rispetto allo stesso periodo del 2025.",
               lp_h="I preferiti di Lonely Planet", lp_p="Selezione tratta da Lonely Planet Best in Travel 2027 (l'ordine qui sotto non è una classifica).",
               more="Fonti", src_sky="Skyscanner Travel Trends 2027", src_lp="Lonely Planet Best in Travel 2027",
               searches="di ricerche", from_l="da", loading="Prezzo in arrivo…", none="Confronta i prezzi", photo="Foto",
               note="Prezzi andata e ritorno in diretta (calendario prezzi di Escale), per una data precisa: cambiano ogni giorno. Le tendenze vengono dalle fonti citate, verificate a novembre 2026.",
               cta="Cerca un altro volo", from_txt="Prezzi da", bell="Avviso prezzo", alert_for="Avviso per:"),
    "de": dict(path="de/trendziele-2027", title="Trendziele 2027: wohin reisen 2027 (Skyscanner, Lonely Planet) | Escale",
               desc="Die Reiseziele im Aufwind 2027 laut Skyscanner und Lonely Planet: Hurghada, Da Nang, Kap Verde, Québec, Venetien, Rabat… mit Live-Flugpreisen ab deinem Flughafen.",
               h1="Wohin <span>2027</span>?", lead="Die Reiseziele im Aufwind, nach Flugsuchen bei Skyscanner und der Auswahl von Lonely Planet. Der angezeigte Preis ist der beste Hin- und Rückflug, der gerade ab deinem Flughafen gefunden wurde.",
               sky_h="Die am stärksten wachsenden Ziele bei Skyscanner", sky_p="Zuwachs der Suchen nach Hin- und Rückflügen bei Skyscanner (skyscanner.net), 1. Januar bis 17. Juni 2026 im Vergleich zum Vorjahreszeitraum.",
               lp_h="Die Favoriten von Lonely Planet", lp_p="Auswahl aus Lonely Planet Best in Travel 2027 (die Reihenfolge unten ist keine Rangliste).",
               more="Quellen", src_sky="Skyscanner Travel Trends 2027", src_lp="Lonely Planet Best in Travel 2027",
               searches="Suchen", from_l="ab", loading="Preis wird geladen…", none="Preise vergleichen", photo="Foto",
               note="Live-Preise für Hin- und Rückflug (Preiskalender von Escale), für ein bestimmtes Datum: Sie ändern sich täglich. Die Trends stammen aus den genannten Quellen, geprüft im November 2026.",
               cta="Einen anderen Flug suchen", from_txt="Preise ab", bell="Preisalarm", alert_for="Alarm für:"),
}


def card(site_photos, lang, key, codes, name, country, badge, why, near):
    c = site_photos.get(key, {})
    fq = "" if lang == "fr" else f"&lang={lang}"
    first = codes.split(",")[0]
    return (f'<li class="tr-card" data-to="{codes}"><a class="tr-link" href="/?type=vols&amp;to={first}{fq}">'
            f'<img src="/img/tendances/{key}.webp" alt="{E(name)}, {E(country)}{(". " + E(why)) if why else ""}" width="480" height="640" loading="lazy" decoding="async">'
            + (f'<span class="tr-badge">{E(badge)}</span>' if badge else "") +
            f'<span class="tr-info"><strong>{E(name)}</strong><small>{E(country)}</small>'
            + (f'<em class="tr-why">{E(why)}</em>' if why else "") +
            f'<span class="tr-price" aria-live="polite"></span>' + (f'<small class="tr-near">{E(near)}</small>' if near else "") + '</span></a>'
            f'<button type="button" class="tr-bell alert-cta" hidden data-name="{E(name)}">🔔 {E(T[lang]["bell"])}</button>'
            f'<p class="tr-credit">{E(T[lang]["photo"])} : <a href="{E(c.get("page", ""))}" target="_blank" rel="noopener">{E(c.get("author", "Wikimedia Commons")[:60])}</a>, {E(c.get("license", ""))}</p></li>')


def build(site, ctx):
    photos = json.loads((site / "data" / "tendances-photos.json").read_text(encoding="utf-8"))
    paths = {l: T[l]["path"] for l in T}
    urls = []
    for lang, t in T.items():
        col = 0 if lang == "fr" else 1
        x = {"it": 0, "de": 1}.get(lang)
        nm = lambda k, fr, en: ITDE[k][2 * x] if x is not None else (fr if lang == "fr" else en)
        ct = lambda k, pf, pe: ITDE[k][2 * x + 1] if x is not None else (pf if lang == "fr" else pe)
        nr = lambda codes: NEAR_ITDE.get(codes, ("", ""))[x] if x is not None else NEAR.get(codes, ("", ""))[col]
        sky = "".join(card(photos, lang, k, codes, nm(k, fr, en), ct(k, pf, pe), f"#{i + 1} · +{pct} %", "", nr(codes))
                      for i, (k, codes, fr, en, pf, pe, pct) in enumerate(SKYSCANNER))
        lp = "".join(card(photos, lang, k, codes, nm(k, fr, en), ct(k, pf, pe), "Lonely Planet 2027", WHY_ITDE[k][x] if x is not None else why[col], nr(codes))
                     for k, codes, fr, en, pf, pe, why in LONELY)
        q = "" if lang == "fr" else f"?lang={lang}"
        body = (f'<p class="tr-from small" hidden>{E(t["from_txt"])} <strong class="tr-from-city"></strong></p>'
                f'<section><h2>{E(t["sky_h"])}</h2><p class="small">{E(t["sky_p"])}</p><ul class="tr-grid">{sky}</ul></section>'
                f'<section><h2>{E(t["lp_h"])}</h2><p class="small">{E(t["lp_p"])}</p><ul class="tr-grid">{lp}</ul></section>'
                f'<section id="price-alert" class="price-alert" data-from="PAR" data-to="HRG" data-for="{E(t["alert_for"])}" hidden></section>'
                f'<section><h2>{E(t["more"])}</h2><ul><li><a href="{SKY}" target="_blank" rel="noopener">{E(t["src_sky"])}</a></li>'
                f'<li><a href="{LP}" target="_blank" rel="noopener">{E(t["src_lp"])}</a></li></ul><p class="small">{E(t["note"])}</p></section>'
                f'<p><a class="btn" href="/{q}">{E(t["cta"])}</a></p>'
                f'<div id="tr-cfg" hidden data-from="{E(t["from_l"])}" data-loading="{E(t["loading"])}" data-none="{E(t["none"])}"></div>'
                '<script src="/fetes.js" defer></script><script src="/tendances.js" defer></script><script src="/alerts.js" defer></script>')
        hero = f'<p class="eyebrow">2027</p><h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": t["title"].split(" | ")[0],
                                                                   "description": t["desc"], "inLanguage": lang, "dateModified": "2026-11-04",
                                                                   "author": {"@type": "Organization", "name": "Escale"}}, ensure_ascii=False) + "</script>"
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, ld, paths, ctx, og="og-image.png"))
    return urls
