"""Photos des villes (accueil « Explorer le monde ») : images libres de droits de Wikimedia Commons.

Lancé par GitHub Actions (.github/workflows/photos.yml), qui a accès à Internet :
  python3 scripts/photos.py
Pour chaque ville : une photo en paysage, sous licence libre (domaine public, CC0, CC BY, CC BY-SA),
recadrée en 4:3 et enregistrée en WebP (site/img/villes/<ville>.webp et <ville>-480.webp).
Les auteurs et licences sont notés dans site/data/photos.json (affichés sur le site, comme l'exigent les licences).
Pour imposer une photo précise, renseigner « file » (nom du fichier sur Commons, sans « File: »).
"""
import html
import io
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "img" / "villes"
DATA = ROOT / "site" / "data" / "photos.json"
API = "https://commons.wikimedia.org/w/api.php"
UA = "EscalePhotos/1.0 (https://escale.live; comparateur de vols)"

# code aéroport, nom (fr), recherches Commons (de la plus précise à la plus large),
# mots obligatoires dans le titre de la photo (évite les photos d'un autre lieu), fichier imposé (facultatif)
CITIES = [
    ("DSS", "Dakar", ["Dakar Corniche", "Dakar Senegal city"], "dakar|gor[ée]e", ""),
    ("RAK", "Marrakech", ["Koutoubia Marrakech", "Jemaa el-Fnaa"], "marrak|koutoubia|jemaa", ""),
    ("CMN", "Casablanca", ["Hassan II Mosque", "Mosquée Hassan II Casablanca", "Casablanca corniche"], "hassan|casablanca", ""),
    ("ABJ", "Abidjan", ["Abidjan Plateau skyline", "Cathédrale Saint-Paul Abidjan", "Abidjan lagune Ebrié"], "abidjan|plateau|saint-paul", ""),
    ("TUN", "Tunis", ["Sidi Bou Said view", "Sidi Bou Said blue", "Tunis medina"], "sidi.?bou|tunis", ""),
    ("ALG", "Alger", ["Algiers bay", "Notre-Dame d'Afrique Algiers"], "alg|afrique", ""),
    ("IST", "Istanbul", ["Hagia Sophia exterior", "Blue Mosque Istanbul", "Galata Tower Istanbul", "Istanbul skyline"], "hagia|sophia|ayasofya|blue mosque|sultan ahmed|galata|istanbul", ""),
    ("DXB", "Dubaï", ["Burj Khalifa", "Dubai Marina skyline", "Dubai skyline"], "burj|dubai", ""),
    ("LIS", "Lisbonne", ["Lisbon Alfama", "Lisbon tram"], "lisbo|alfama", ""),
    ("BCN", "Barcelone", ["Sagrada Familia exterior", "Barcelona panorama", "Park Güell"], "sagrada|barcelon|g[uü]ell", ""),
    ("JFK", "New York", ["Manhattan skyline", "New York City skyline"], "manhattan|new york", ""),
    ("CAI", "Le Caire", ["Giza pyramids", "Cairo skyline"], "giza|pyramid|cairo", ""),
    ("BKO", "Bamako", ["Bamako skyline", "Pont des Martyrs Bamako", "Grande Mosquée de Bamako", "Bamako Niger"], "bamako", ""),
    ("DJE", "Djerba", ["Djerba beach", "Djerba plage", "Houmt Souk Djerba", "Djerba mosque"], "djerba|jerba|houmt", ""),
    ("TNG", "Tanger", ["Tangier kasbah", "Tanger médina vue", "Tangier bay", "Cap Spartel"], "tang[ie]|spartel|kasbah", ""),
    ("ACC", "Accra", ["Accra Independence Square", "Accra Ghana city"], "accra|independence", ""),
]
OK_LICENSE = re.compile(r"^(public domain|pd|cc0|cc by(-sa)?( \d\.\d)?)", re.I)
BAD_WORDS = re.compile(r"map|flag|logo|plan|coat of arms|diagram|stamp|banknote|poster|interior|inside|ceiling|vault|nave|portrait|ferry|ship|boat|bateau|autoroute|motorway|highway|night|nuit|\.svg|\.png|\.gif|\.tif", re.I)


def api(params):
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def text(v):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", v or ""))).strip()


def info(titles):
    """Infos (taille, licence, auteur, vignette 1600 px) pour une liste de « File:… »."""
    d = api({"action": "query", "titles": "|".join(titles), "prop": "imageinfo",
             "iiprop": "url|size|mime|extmetadata", "iiurlwidth": "1600"})
    out = []
    for p in d.get("query", {}).get("pages", []):
        ii = (p.get("imageinfo") or [None])[0]
        if not ii:
            continue
        m = ii.get("extmetadata", {})
        out.append(dict(title=p["title"], width=ii["width"], height=ii["height"], mime=ii.get("mime", ""),
                        thumb=ii.get("thumburl") or ii["url"], page=ii.get("descriptionurl", ""),
                        license=text(m.get("LicenseShortName", {}).get("value", "")),
                        license_url=text(m.get("LicenseUrl", {}).get("value", "")),
                        author=text(m.get("Artist", {}).get("value", "")) or "Wikimedia Commons"))
    order = {t: i for i, t in enumerate(titles)}
    return sorted(out, key=lambda x: order.get(x["title"], 99))


def acceptable(x, must):
    ratio = x["width"] / max(1, x["height"])
    return (x["mime"] == "image/jpeg" and x["width"] >= 1600 and 1.25 <= ratio <= 2.2
            and OK_LICENSE.match(x["license"] or "") and not BAD_WORDS.search(x["title"]) and re.search(must, x["title"], re.I))


def search(q, quality):
    s = f'{q} filetype:bitmap' + (' incategory:"Quality_images"' if quality else "")
    d = api({"action": "query", "list": "search", "srsearch": s, "srnamespace": "6", "srlimit": "20"})
    return [r["title"] for r in d.get("query", {}).get("search", [])]


def pick(queries, must, pinned):
    if pinned:
        got = info(["File:" + pinned])
        if got and OK_LICENSE.match(got[0]["license"] or ""):
            return got[0]
        print("  fichier imposé refusé ou introuvable :", pinned)
    for quality in (True, False):
        for q in queries:
            titles = search(q, quality)
            if titles:
                for x in info(titles):
                    if acceptable(x, must):
                        return x
            time.sleep(0.5)
    return None


def save(x, slug):
    req = urllib.request.Request(x["thumb"], headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        im = Image.open(io.BytesIO(r.read())).convert("RGB")
    w, h = im.size
    tw = min(w, int(h * 4 / 3))
    th = int(tw * 3 / 4)
    left, top = (w - tw) // 2, (h - th) // 2
    im = im.crop((left, top, left + tw, top + th))
    OUT.mkdir(parents=True, exist_ok=True)
    for size, suffix, q in ((800, "", 70), (480, "-480", 68)):
        im.resize((size, size * 3 // 4), Image.LANCZOS).save(OUT / f"{slug}{suffix}.webp", "WEBP", quality=q, method=6)


def slugify(t):
    t = t.lower()
    for a, b in (("é", "e"), ("è", "e"), ("ï", "i"), ("à", "a"), ("ô", "o")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def main():
    only = set(sys.argv[1:])
    old = {p["code"]: p for p in json.loads(DATA.read_text(encoding="utf-8"))} if DATA.exists() else {}
    res = dict(old)
    for code, city, queries, must, pinned in CITIES:
        if only and code not in only:
            continue
        try:
            x = pick(queries, must, pinned)
        except Exception as e:  # noqa: BLE001
            print(f"{code} {city} : erreur {e}")
            continue
        if not x:
            print(f"{code} {city} : aucune photo libre trouvée")
            continue
        slug = slugify(city)
        save(x, slug)
        res[code] = dict(code=code, city=city, img=f"/img/villes/{slug}.webp", img_small=f"/img/villes/{slug}-480.webp",
                         file=x["title"], page=x["page"], author=x["author"][:120], license=x["license"], license_url=x["license_url"])
        print(f"{code} {city} : {x['title']} — {x['author'][:60]} — {x['license']}")
        time.sleep(0.5)
    DATA.write_text(json.dumps([res[c] for c, *_ in CITIES if c in res], ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
