"""Pages « Meilleur mois pour partir à… » (30 destinations, fr et en) + page d'index.

Aucun prix écrit : site/meilleur-mois.js lit le calendrier des prix (/api/calendar) des 12 prochains mois depuis
l'aéroport du visiteur et montre le mois le moins cher. Photos : site/data/photos.json (Wikimedia Commons, auteurs cités).
"""
import html
import json

import build_i18n as B

E = html.escape


def hero_src(site, img):
    """Grande photo (-1280) si elle existe, sinon la photo normale."""
    big = img.replace(".webp", "-1280.webp")
    return big if (site / big.lstrip("/")).exists() else img

# code de destination (calendrier), code de la photo (photos.json), slug fr, slug en, nom fr, nom en
DESTS = [
    ("DSS", "DSS", "dakar", "dakar", "Dakar", "Dakar"), ("ABJ", "ABJ", "abidjan", "abidjan", "Abidjan", "Abidjan"),
    ("RAK", "RAK", "marrakech", "marrakech", "Marrakech", "Marrakech"), ("CMN", "CMN", "casablanca", "casablanca", "Casablanca", "Casablanca"),
    ("TUN", "TUN", "tunis", "tunis", "Tunis", "Tunis"), ("DJE", "DJE", "djerba", "djerba", "Djerba", "Djerba"),
    ("AGA", "AGA", "agadir", "agadir", "Agadir", "Agadir"), ("CAI", "CAI", "le-caire", "cairo", "Le Caire", "Cairo"),
    ("HRG", "HRG", "hurghada", "hurghada", "Hurghada", "Hurghada"), ("ZNZ", "ZNZ", "zanzibar", "zanzibar", "Zanzibar", "Zanzibar"),
    ("NBO", "NBO", "nairobi", "nairobi", "Nairobi", "Nairobi"), ("MRU", "MRU", "ile-maurice", "mauritius", "l'île Maurice", "Mauritius"),
    ("RUN", "RUN", "la-reunion", "reunion", "La Réunion", "Réunion"), ("IST", "IST", "istanbul", "istanbul", "Istanbul", "Istanbul"),
    ("DXB", "DXB", "dubai", "dubai", "Dubaï", "Dubai"), ("LIS", "LIS", "lisbonne", "lisbon", "Lisbonne", "Lisbon"),
    ("BCN", "BCN", "barcelone", "barcelona", "Barcelone", "Barcelona"), ("ROM", "ROM", "rome", "rome", "Rome", "Rome"),
    ("ATH", "ATH", "athenes", "athens", "Athènes", "Athens"), ("LON", "LON", "londres", "london", "Londres", "London"),
    ("NYC", "JFK", "new-york", "new-york", "New York", "New York"), ("MIA", "MIA", "miami", "miami", "Miami", "Miami"),
    ("YMQ", "YMQ", "montreal", "montreal", "Montréal", "Montreal"), ("PTP", "PTP", "guadeloupe", "guadeloupe", "la Guadeloupe", "Guadeloupe"),
    ("FDF", "FDF", "martinique", "martinique", "la Martinique", "Martinique"), ("PUJ", "PUJ", "punta-cana", "punta-cana", "Punta Cana", "Punta Cana"),
    ("CUN", "CUN", "cancun", "cancun", "Cancún", "Cancún"), ("BKK", "BKK", "bangkok", "bangkok", "Bangkok", "Bangkok"),
    ("DPS", "DPS", "bali", "bali", "Bali", "Bali"), ("TYO", "HND", "tokyo", "tokyo", "Tokyo", "Tokyo"),
]
PRE = {"l'île Maurice": "à", "La Réunion": "à", "la Guadeloupe": "en", "la Martinique": "en"}

T = {
    "fr": dict(base="meilleur-mois-pour-partir", title="Meilleur mois pour partir {a} {n} : le mois le moins cher en avion | Escale",
               desc="Quel est le mois le moins cher pour aller {a} {n} ? Le prix aller-retour le plus bas de chacun des 12 prochains mois, en direct depuis votre aéroport.",
               h1="Le meilleur mois pour partir <span>{a} {n}</span>", lead="Le prix aller-retour le plus bas trouvé pour chacun des 12 prochains mois, depuis votre aéroport. Cliquez sur un mois pour voir les vols.",
               from_l="Départ de", loading="Lecture du calendrier des prix…", none="Pas encore assez de prix pour ce trajet depuis votre aéroport. Essayez une recherche directe.",
               same="Vous êtes déjà sur place : choisissez un autre aéroport de départ sur l'accueil.",
               best="Le mois le moins cher : {m}, dès {p} aller-retour.", dear="Le plus cher : {m} (dès {p}).", go="Voir les vols du mois le moins cher",
               how_h="Comment lire ce graphique", how=["Chaque barre est le meilleur prix aller-retour trouvé récemment pour un départ ce mois-là (calendrier des prix de notre partenaire Aviasales).",
                   "Les mois lointains ont souvent moins de prix connus : un mois vide ne veut pas dire qu'il n'y a pas de vol.",
                   "Les vacances scolaires et les fêtes font monter les prix : partir quelques jours avant ou après change beaucoup."],
               idx_title="Meilleur mois pour partir : le mois le moins cher pour 30 destinations | Escale",
               idx_desc="Le mois le moins cher pour partir à Dakar, Abidjan, Marrakech, New York, Bali, Tokyo et 24 autres destinations, en direct depuis votre aéroport.",
               idx_h1="Le meilleur mois <span>pour partir</span>", idx_lead="Choisissez une destination : vous verrez le prix aller-retour le plus bas de chaque mois, depuis votre aéroport.",
               other="Autres destinations", change="Changer d'aéroport", photo="Photo"),
    "en": dict(base="en/best-time-to-fly", title="Cheapest month to fly to {n}: best time to book | Escale",
               desc="What is the cheapest month to fly to {n}? The lowest round-trip price for each of the next 12 months, live from your airport.",
               h1="The cheapest month to fly to <span>{n}</span>", lead="The lowest round-trip price found for each of the next 12 months, from your airport. Click a month to see the flights.",
               from_l="Leaving from", loading="Reading the price calendar…", none="Not enough prices yet for this route from your airport. Try a direct search.",
               same="You are already there: pick another departure airport on the home page.",
               best="Cheapest month: {m}, from {p} round trip.", dear="Most expensive: {m} (from {p}).", go="See flights for the cheapest month",
               how_h="How to read this chart", how=["Each bar is the best round-trip price recently found for a departure that month (price calendar of our partner Aviasales).",
                   "Months far ahead often have fewer known prices: an empty month does not mean there are no flights.",
                   "School holidays and festive seasons push prices up: leaving a few days earlier or later makes a big difference."],
               idx_title="Cheapest month to fly: best time to go for 30 destinations | Escale",
               idx_desc="The cheapest month to fly to Dakar, Abidjan, Marrakech, New York, Bali, Tokyo and 24 more destinations, live from your airport.",
               idx_h1="The cheapest month <span>to fly</span>", idx_lead="Pick a destination: you will see the lowest round-trip price for each month, from your airport.",
               other="Other destinations", change="Change airport", photo="Photo"),
}


def build(site, ctx):
    photos = {p["code"]: p for p in json.loads((site / "data" / "photos.json").read_text(encoding="utf-8"))}
    urls = []
    idx_paths = {l: T[l]["base"] for l in T}
    for code, pcode, sfr, sen, nfr, nen in DESTS:
        paths = {"fr": f'{T["fr"]["base"]}/{sfr}', "en": f'{T["en"]["base"]}/{sen}'}
        for lang, t in T.items():
            n = nfr if lang == "fr" else nen
            a = PRE.get(n, "à") if lang == "fr" else ""
            q = "" if lang == "fr" else "?lang=en"
            p = photos.get(pcode)
            img = (f'<img class="pv-hero" src="{hero_src(site, p["img"])}" alt="{E(n)}" width="1280" height="960" fetchpriority="high">'
                   f'<p class="pv-cred small">{E(t["photo"])} : {E(p["author"][:50])}, {E(p["license"])}</p>') if p else ""
            tj = E(json.dumps({k: t[k] for k in ("loading", "none", "same", "best", "dear")}, ensure_ascii=False))
            others = "".join(f'<li><a href="/{T[lang]["base"]}/{(d[2] if lang == "fr" else d[3])}/">{E(d[4] if lang == "fr" else d[5])}</a></li>' for d in DESTS if d[0] != code)
            body = (f'<p>{E(t["from_l"])} <strong class="mm-from">…</strong> · <a href="/{q}">{E(t["change"])}</a></p>'
                    f'<div id="mm-chart" class="mm-chart" data-to="{code}" data-t="{tj}"></div>'
                    f'<div id="mm-summary" class="mm-summary" aria-live="polite"></div><p><a id="mm-go" class="btn" href="/{q}" hidden>{E(t["go"])}</a></p>'
                    f'<section><h2>{E(t["how_h"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["how"]) + "</ul></section>"
                    f'<section><h2>{E(t["other"])}</h2><ul class="pv-other">{others}</ul></section>'
                    '<script src="/fetes.js" defer></script><script src="/meilleur-mois.js" defer></script>')
            hero = f'<h1>{t["h1"].format(a=a, n=E(n))}</h1><p class="hero-lead">{E(t["lead"])}</p>{img}'
            title = t["title"].format(a=a, n=n).replace("  ", " ")
            desc = t["desc"].format(a=a, n=n).replace("  ", " ")
            urls.append(B.write(site, paths[lang], lang, title, desc, hero, body, "", paths, ctx))
    for lang, t in T.items():
        cards = "".join(
            f'<li class="tr-card"><a class="tr-link" href="/{t["base"]}/{(d[2] if lang == "fr" else d[3])}/">'
            + (f'<img src="{photos[d[1]]["img_small"]}" alt="" width="480" height="360" loading="lazy" decoding="async">' if d[1] in photos else "")
            + f'<span class="tr-info"><strong>{E(d[4] if lang == "fr" else d[5])}</strong></span></a></li>' for d in DESTS)
        hero = f'<h1>{t["idx_h1"]}</h1><p class="hero-lead">{E(t["idx_lead"])}</p>'
        urls.append(B.write(site, t["base"], lang, t["idx_title"], t["idx_desc"], hero, f'<ul class="tr-grid mm-idx">{cards}</ul>', "", idx_paths, ctx))
    return urls
