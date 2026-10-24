"""Accueil « Explorer le monde » : cartes photo des villes (photos libres de site/data/photos.json, voir scripts/photos.py)."""
import html
import json

import translations as TR

E = html.escape
LANGS = ["en", "es", "pt", "ar"]
# Noms des villes absentes des tables de traduction (en, es, pt, ar)
EXTRA_NAMES = {
    "Lisbonne": ("Lisbon", "Lisboa", "Lisboa", "لشبونة"),
    "Barcelone": ("Barcelona", "Barcelona", "Barcelona", "برشلونة"),
    "New York": ("New York", "Nueva York", "Nova Iorque", "نيويورك"),
    "Le Caire": ("Cairo", "El Cairo", "Cairo", "القاهرة"),
    "Djerba": ("Djerba", "Yerba", "Djerba", "جربة"),
    "Tanger": ("Tangier", "Tánger", "Tânger", "طنجة"),
    "Accra": ("Accra", "Acra", "Acra", "أكرا"),
}
COUNTRY_FR = {"SN": "Sénégal", "MA": "Maroc", "CI": "Côte d’Ivoire", "TN": "Tunisie", "DZ": "Algérie", "TR": "Turquie", "AE": "Émirats arabes unis",
              "PT": "Portugal", "ES": "Espagne", "US": "États-Unis", "EG": "Égypte", "ML": "Mali", "GH": "Ghana"}


def names(city):
    v = TR.CITIES.get(city) or EXTRA_NAMES.get(city)
    return {l: (v[i] if v else city) for i, l in enumerate(LANGS)}


def photos(site):
    p = site / "data" / "photos.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def cards(site, hubs, airports):
    out = []
    for p in photos(site):
        code, city = p["code"], p["city"]
        hp = hubs.get(city)
        hrefs = {l: (f"/{hp[l]}/" if hp else f"/?type=vols&to={code}" + ("" if l == "fr" else f"&lang={l}")) for l in ["fr"] + LANGS}
        cc = (airports.get(code) or [None, None, None, ""])[3]
        big, small = p["img"], p["img_small"]
        out.append(
            f'<a class="city-card" href="{E(hrefs["fr"])}" data-hrefs="{E(json.dumps(hrefs, ensure_ascii=False))}">'
            f'<img src="{small}" srcset="{small} 480w, {big} 800w" sizes="(max-width: 600px) 46vw, 230px" width="480" height="360" alt="" loading="lazy" decoding="async">'
            f'<span class="city-info"><strong data-names="{E(json.dumps(names(city), ensure_ascii=False))}">{E(city)}</strong>'
            f'<small class="city-country" data-cc="{cc}">{E(COUNTRY_FR.get(cc, ""))}</small>'
            f'<b class="city-price" data-to="{code}"></b></span></a>')
    return '<div class="city-grid">' + "".join(out) + "</div>"


def dest_photos(site):
    """{code aéroport : petite photo} pour les cartes « Destinations populaires »."""
    return {p["code"]: p["img_small"] for p in photos(site)}


def credits_body(site):
    rows = "".join(
        f'<li><strong>{E(p["city"])}</strong> : <a href="{E(p["page"])}" rel="noopener">{E(p["file"].replace("File:", ""))}</a>, '
        f'{E(p["author"])}, ' + (f'<a href="{E(p["license_url"])}" rel="noopener license">{E(p["license"])}</a>' if p.get("license_url") else E(p["license"]))
        + " (recadrée et redimensionnée)</li>" for p in photos(site))
    return (f'<section><p>Les photos des villes viennent de <a href="https://commons.wikimedia.org/">Wikimedia Commons</a>, '
            f'sous licence libre. Merci à leurs auteurs.</p><ul class="links">{rows}</ul></section>')

