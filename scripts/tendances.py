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

T = {
    "fr": dict(path="tendances-2027", title="Destinations tendance 2027 : où partir en 2027 (Skyscanner, Lonely Planet) | Escale",
               desc="Les destinations qui montent en 2027 selon Skyscanner et Lonely Planet : Hurghada, Da Nang, Cap-Vert, Québec, Vénétie, Rabat… avec le prix des vols en direct depuis chez vous.",
               h1="Où partir <span>en 2027</span> ?", lead="Les destinations qui montent, d'après les recherches de vols Skyscanner et la sélection Lonely Planet. Le prix affiché est le meilleur aller-retour trouvé en ce moment depuis votre aéroport.",
               sky_h="Les destinations qui explosent sur Skyscanner", sky_p="Hausse des recherches de vols aller-retour sur Skyscanner (skyscanner.net), du 1er janvier au 17 juin 2026, comparé à la même période en 2025.",
               lp_h="Les coups de cœur de Lonely Planet", lp_p="Sélection extraite de Lonely Planet Best in Travel 2027 (l'ordre ci-dessous n'est pas un classement).",
               more="Sources", src_sky="Skyscanner Travel Trends 2027", src_lp="Lonely Planet Best in Travel 2027",
               searches="de recherches", from_l="dès", loading="Prix en cours…", none="Comparer les prix", photo="Photo",
               note="Prix aller-retour en direct (calendrier des prix Escale), pour une date précise : ils changent tous les jours. Les tendances viennent des sources citées, vérifiées en novembre 2026.",
               cta="Chercher un autre vol", from_txt="Prix depuis"),
    "en": dict(path="en/trending-2027", title="Trending destinations 2027: where to travel in 2027 (Skyscanner, Lonely Planet) | Escale",
               desc="The destinations on the rise in 2027 according to Skyscanner and Lonely Planet: Hurghada, Da Nang, Cape Verde, Québec, Veneto, Rabat… with live flight prices from your airport.",
               h1="Where to go <span>in 2027</span>?", lead="The destinations on the rise, from Skyscanner flight searches and Lonely Planet's picks. The price shown is the best round trip found right now from your airport.",
               sky_h="Skyscanner's fastest-rising destinations", sky_p="Increase in round-trip flight searches on Skyscanner (skyscanner.net), 1 January to 17 June 2026 compared with the same period in 2025.",
               lp_h="Lonely Planet's picks", lp_p="A selection from Lonely Planet Best in Travel 2027 (the order below is not a ranking).",
               more="Sources", src_sky="Skyscanner Travel Trends 2027", src_lp="Lonely Planet Best in Travel 2027",
               searches="searches", from_l="from", loading="Loading price…", none="Compare prices", photo="Photo",
               note="Live round-trip prices (Escale price calendar), for a specific date: they change every day. Trends come from the sources cited, checked in November 2026.",
               cta="Search another flight", from_txt="Prices from"),
}


def card(site_photos, lang, key, codes, name, country, badge, why, near):
    c = site_photos.get(key, {})
    fq = "" if lang == "fr" else "&lang=en"
    first = codes.split(",")[0]
    return (f'<li class="tr-card" data-to="{codes}"><a class="tr-link" href="/?type=vols&amp;to={first}{fq}">'
            f'<img src="/img/tendances/{key}.webp" alt="{E(name)}, {E(country)}{(". " + E(why)) if why else ""}" width="480" height="640" loading="lazy" decoding="async">'
            + (f'<span class="tr-badge">{E(badge)}</span>' if badge else "") +
            f'<span class="tr-info"><strong>{E(name)}</strong><small>{E(country)}</small>'
            + (f'<em class="tr-why">{E(why)}</em>' if why else "") +
            f'<span class="tr-price" aria-live="polite"></span>' + (f'<small class="tr-near">{E(near)}</small>' if near else "") + '</span></a>'
            f'<p class="tr-credit">{E(T[lang]["photo"])} : <a href="{E(c.get("page", ""))}" target="_blank" rel="noopener">{E(c.get("author", "Wikimedia Commons")[:60])}</a>, {E(c.get("license", ""))}</p></li>')


def build(site, ctx):
    photos = json.loads((site / "data" / "tendances-photos.json").read_text(encoding="utf-8"))
    paths = {l: T[l]["path"] for l in T}
    urls = []
    for lang, t in T.items():
        col = 0 if lang == "fr" else 1
        sky = "".join(card(photos, lang, k, codes, (fr if lang == "fr" else en), (pf if lang == "fr" else pe), f"#{i + 1} · +{pct} %", "", NEAR.get(codes, ("", ""))[col])
                      for i, (k, codes, fr, en, pf, pe, pct) in enumerate(SKYSCANNER))
        lp = "".join(card(photos, lang, k, codes, (fr if lang == "fr" else en), (pf if lang == "fr" else pe), "Lonely Planet 2027", why[col], NEAR.get(codes, ("", ""))[col])
                     for k, codes, fr, en, pf, pe, why in LONELY)
        q = "" if lang == "fr" else "?lang=en"
        body = (f'<p class="tr-from small" hidden>{E(t["from_txt"])} <strong class="tr-from-city"></strong></p>'
                f'<section><h2>{E(t["sky_h"])}</h2><p class="small">{E(t["sky_p"])}</p><ul class="tr-grid">{sky}</ul></section>'
                f'<section><h2>{E(t["lp_h"])}</h2><p class="small">{E(t["lp_p"])}</p><ul class="tr-grid">{lp}</ul></section>'
                f'<section><h2>{E(t["more"])}</h2><ul><li><a href="{SKY}" target="_blank" rel="noopener">{E(t["src_sky"])}</a></li>'
                f'<li><a href="{LP}" target="_blank" rel="noopener">{E(t["src_lp"])}</a></li></ul><p class="small">{E(t["note"])}</p></section>'
                f'<p><a class="btn" href="/{q}">{E(t["cta"])}</a></p>'
                f'<div id="tr-cfg" hidden data-from="{E(t["from_l"])}" data-loading="{E(t["loading"])}" data-none="{E(t["none"])}"></div>'
                '<script src="/fetes.js" defer></script><script src="/tendances.js" defer></script>')
        hero = f'<p class="eyebrow">2027</p><h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": t["title"].split(" | ")[0],
                                                                   "description": t["desc"], "inLanguage": lang, "dateModified": "2026-11-04",
                                                                   "author": {"@type": "Organization", "name": "Escale"}}, ensure_ascii=False) + "</script>"
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, ld, paths, ctx, og="og-image.png"))
    return urls
