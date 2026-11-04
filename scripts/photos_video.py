"""Photos plein écran pour les vidéos (motion design) : images libres de Wikimedia Commons.

Lancé par GitHub Actions (.github/workflows/photos-video.yml) :
  python3 scripts/photos_video.py bali
Chaque photo est recadrée en 1080x1920 (vertical) et enregistrée en WebP dans video/photos/<série>/<n>.webp.
Auteurs et licences dans video/photos/<série>/credits.json (à citer dans la vidéo ou la légende).
"""
import io
import json
import pathlib
import re
import sys
import time
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from photos import UA, OK_LICENSE, info, search  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
BAD = re.compile(r"map|flag|logo|plan|diagram|stamp|poster|interior|inside|portrait|painting|night|crowd|construction|\.svg|\.png|\.gif|\.tif", re.I)

SERIES = {
    "bali": [
        ("kelingking", ["Kelingking beach Nusa Penida", "Kelingking Nusa Penida", "Nusa Penida cliff"], "kelingking|nusa penida"),
        ("tanahlot", ["Tanah Lot temple sunset", "Tanah Lot temple", "Pura Tanah Lot"], "tanah lot"),
        ("riziere", ["Tegallalang rice terraces", "Tegalalang rice terrace", "Jatiluwih rice terraces"], "tegal+alang|jatiluwih|rice terrace"),
        ("ulundanu", ["Pura Ulun Danu Bratan", "Ulun Danu Beratan temple", "Ulun Danu Bratan"], "ulun danu"),
        ("uluwatu", ["Uluwatu temple cliff", "Pura Luhur Uluwatu", "Uluwatu Bali"], "uluwatu"),
        ("lempuyang", ["Pura Lempuyang gate Agung", "Lempuyang temple", "Pura Penataran Agung Lempuyang"], "lempuyang"),
        ("batur", ["Mount Batur sunrise", "Gunung Batur", "Mount Batur caldera lake"], "batur"),
        ("tirtagangga", ["Tirta Gangga water palace", "Tirta Gangga Bali", "Taman Ujung water palace"], "tirta gangga|taman ujung|ujung"),
        ("plage", ["Padang Padang beach Bali", "Bali beach Nusa Dua", "Dreamland beach Bali", "Balangan beach"], "padang|nusa dua|dreamland|balangan|bali"),
        ("singe", ["Ubud Monkey Forest macaque", "Sacred Monkey Forest Sanctuary Ubud", "Ubud monkey forest"], "monkey forest|ubud|macaque"),
        ("cascade", ["Tegenungan waterfall", "Sekumpul waterfall", "Gitgit waterfall Bali", "Tukad Cepung waterfall"], "tegenungan|sekumpul|gitgit|cepung|waterfall"),
    ],
    "monde": [
        ("tokyo", ["Chureito Pagoda Mount Fuji", "Mount Fuji Chureito Pagoda", "Mount Fuji Lake Kawaguchi"], "fuji|chureito"),
        ("newyork", ["Manhattan skyline", "Lower Manhattan skyline", "Midtown Manhattan skyline"], "manhattan|new york"),
        ("maldives", ["Maldives water villas", "Maldives island aerial view", "Maldives lagoon"], "maldiv"),
        ("marrakech", ["Koutoubia Marrakech", "Jemaa el-Fnaa", "Marrakech medina"], "marrak|koutoubia|jemaa"),
        ("lisbonne", ["Lisbon Alfama", "Lisbon tram 28", "Lisbon panorama"], "lisbo|alfama"),
        ("rome", ["Colosseum Rome", "Colosseo Roma", "Trevi Fountain Rome"], "colosse|colosseo|colosseum|trevi"),
        ("istanbul", ["Hagia Sophia exterior", "Blue Mosque Istanbul", "Istanbul Bosphorus skyline"], "hagia|sophia|blue mosque|sultan ahmed|istanbul"),
        ("dubai", ["Burj Khalifa", "Dubai Marina", "Downtown Dubai"], "burj|dubai"),
        ("bangkok", ["Wat Arun", "Wat Arun Bangkok", "Grand Palace Bangkok"], "wat arun|grand palace|bangkok"),
        ("phuket", ["Phang Nga Bay", "Phi Phi islands", "Maya Bay"], "phang nga|phi phi|maya bay|phuket"),
        ("cancun", ["Cancún beach", "Tulum ruins beach", "Isla Mujeres beach"], "canc[uú]n|tulum|mujeres"),
        ("guadeloupe", ["Grande Anse Deshaies Guadeloupe", "Plage Guadeloupe", "Guadeloupe beach"], "guadeloupe|deshaies"),
        ("maurice", ["Le Morne Brabant", "Mauritius lagoon", "Île aux Cerfs Mauritius"], "mauritius|maurice|le morne|cerfs"),
        ("barcelone", ["Sagrada Família", "Park Güell Barcelona", "Barcelona panorama"], "sagrada|g[uü]ell|barcelon"),
        ("londres", ["Tower Bridge London", "Big Ben Westminster", "London skyline Thames"], "tower bridge|big ben|westminster|london"),
        ("islande", ["Skógafoss", "Seljalandsfoss", "Jökulsárlón"], "sk[oó]gafoss|seljalandsfoss|j[oö]kuls"),
        ("athenes", ["Acropolis of Athens", "Parthenon Athens"], "acropol|parthenon|athen"),
        ("abidjan", ["Abidjan Plateau skyline", "Abidjan lagune Ebrié", "Abidjan Plateau"], "abidjan"),
        ("zanzibar", ["Nungwi beach Zanzibar", "Kendwa beach Zanzibar", "Zanzibar beach"], "zanzibar|nungwi|kendwa|paje"),
        ("puntacana", ["Bávaro beach", "Punta Cana beach", "Playa Bávaro"], "punta cana|b[aá]varo"),
        ("avion", ["Airplane wing above clouds", "Aircraft wing clouds", "Airbus A350 takeoff"], "wing|clouds|a350|a380|takeoff|airliner|aircraft|airplane"),
    ],
    "japon": [
        ("fuji", ["Chureito Pagoda Mount Fuji", "Mount Fuji Lake Kawaguchi"], "fuji|chureito"),
        ("fushimi", ["Fushimi Inari-taisha torii", "Fushimi Inari torii gates"], "fushimi|inari"),
        ("kinkakuji", ["Kinkaku-ji", "Kinkakuji Golden Pavilion"], "kinkaku"),
        ("shibuya", ["Shibuya Crossing", "Shibuya scramble crossing"], "shibuya"),
        ("sakura", ["Himeji Castle cherry blossoms", "Meguro River cherry blossoms", "cherry blossoms Kyoto"], "himeji|meguro|cherry|sakura"),
        ("nara", ["Nara Park deer", "Sika deer Nara"], "nara"),
        ("osaka", ["Osaka Castle", "Dotonbori Osaka"], "osaka|dotonbori"),
        ("shinkansen", ["Shinkansen Mount Fuji", "Shinkansen N700", "Shinkansen E5"], "shinkansen"),
        ("bambou", ["Arashiyama bamboo grove", "Sagano bamboo forest"], "arashiyama|bamboo|sagano"),
        ("sensoji", ["Senso-ji Asakusa", "Sensō-ji"], "sens[oō]-?ji|asakusa"),
        ("tokyotour", ["Tokyo Tower", "Tokyo skyline Tokyo Tower"], "tokyo"),
    ],
    "tendances": [
        ("bishkek", ["Issyk-Kul lake mountains", "Song-Kol lake yurts", "Ala Archa gorge", "Kyrgyzstan mountains yurt"], "kyrgyz|issyk|ala.?archa|song.?k[oö]l|bishkek|tian shan", "File:Issyk kul Lake mountains.jpg"),
        ("hurghada", ["Giftun island beach", "Hurghada coral reef", "Makadi Bay", "El Gouna lagoon", "Hurghada beach"], "hurghada|giftun|makadi|gouna|sahl hasheesh", "File:Makadi Bay pano.jpg"),
        ("malmo", ["Turning Torso", "Malmö Västra hamnen", "Malmö Stortorget", "Øresund Bridge aerial"], "malm|turning torso|[oø]resund", "File:2026-07-28-Turning Torso-060888.jpg"),
        ("trapani", ["Saline di Trapani", "Trapani salt pans windmill", "San Vito Lo Capo beach", "Favignana", "Erice Sicily"], "trapani|saline|marsala|san vito|favignana|erice", "File:Erice Chiesa di San Giovanni Battista BW 2025-04-30 12-31-24.jpg"),
        ("chongqing", ["Hongyadong", "Chongqing skyline Yangtze", "Chongqing Jiefangbei", "Chongqing skyline"], "chongqing|hongyadong", "File:The skyscrapers of Chongqing CBD with Hongya Cave at sunset.jpeg"),
        ("danang", ["Golden Bridge Ba Na Hills", "Dragon Bridge Da Nang", "My Khe beach Da Nang"], "golden bridge|ba na|da nang|đà nẵng|dragon bridge|my khe"),
        ("sal", ["Santa Maria beach Sal Cape Verde", "Sal island Cape Verde beach", "Ilha do Sal"], "sal|santa maria|cabo verde|cape verde"),
        ("quebec", ["Château Frontenac", "Château Frontenac Québec", "Old Quebec"], "frontenac|qu[eé]bec"),
        ("redwoods", ["Redwood National and State Parks", "Jedediah Smith Redwoods", "Muir Woods", "Avenue of the Giants", "Prairie Creek Redwoods"], "redwood national|jedediah|muir woods|avenue of the giants|humboldt redwoods|prairie creek", "File:Redwood National and State Parks - panoramio (1).jpg"),
        ("venetie", ["Tre Cime di Lavaredo", "Venice Grand Canal", "Dolomites Veneto"], "lavaredo|venezia|venice|dolomit|veneto"),
        ("sibenik", ["Šibenik panorama", "St. Nicholas Fortress Šibenik", "Skradinski buk Krka", "Šibenik harbour"], "[sš]ibenik|krka|skradin", "File:Skradinski buk waterfall – NP Krka – 2016.jpg"),
        ("rabat", ["Hassan Tower Rabat", "Kasbah of the Udayas", "Rabat Morocco"], "rabat|hassan tower|oudaya|udaya"),
        ("okinawa", ["Kouri Bridge Okinawa", "Okinawa beach", "Shuri Castle"], "okinawa|shuri|kouri|ishigaki|miyako|kerama"),
    ],
    "argent": [
        ("inde", ["Taj Mahal", "Taj Mahal Agra", "Taj Mahal sunrise"], "taj mahal"),
        ("tunisie", ["Sidi Bou Said", "Sidi Bou Saïd village", "Sidi Bou Said blue door"], "sidi.?bou"),
        ("suisse", ["Matterhorn Zermatt", "Matterhorn", "Lauterbrunnen valley"], "matterhorn|zermatt|lauterbrunnen|cervin"),
        ("dakar", ["Dakar Corniche", "Dakar Senegal city", "African Renaissance Monument"], "dakar|renaissance"),
    ],
}


def ok(x, must):
    return (x["mime"] == "image/jpeg" and x["width"] >= 1200 and x["height"] >= 900
            and OK_LICENSE.match(x["license"] or "") and not BAD.search(x["title"]) and re.search(must, x["title"], re.I))


def pick(queries, must, used):
    for quality in (True, False):
        for q in queries:
            try:
                titles = [t for t in search(q, quality) if t not in used]
            except Exception as e:  # noqa: BLE001
                print("  recherche ratée", q, e); continue
            for i in range(0, len(titles), 10):
                for x in info(titles[i:i + 10]):
                    if ok(x, must):
                        return x
            time.sleep(0.5)
    return None


def vertical(data):
    im = Image.open(io.BytesIO(data)).convert("RGB")
    W, H = 1080, 1920
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))


def candidates(name, key, queries, must):
    """Mode choix : jusqu'à 6 photos possibles par lieu, en petit, dans video/photos/_choix/<série>/."""
    out = ROOT / "video" / "photos" / "_choix" / name
    out.mkdir(parents=True, exist_ok=True)
    seen, n, titles = set(), 0, {}
    for quality in (True, False):
        for q in queries:
            try:
                found = [t for t in search(q, quality) if t not in seen]
            except Exception:  # noqa: BLE001
                continue
            seen.update(found)
            for i in range(0, len(found), 10):
                for x in info(found[i:i + 10]):
                    if n < 6 and ok(x, must):
                        data = urllib.request.urlopen(urllib.request.Request(x["thumb"], headers={"User-Agent": UA}), timeout=60).read()
                        vertical(data).resize((360, 640)).save(out / f"{key}-{n}.webp", "WEBP", quality=70)
                        titles[f"{key}-{n}"] = x["title"]; n += 1
            time.sleep(0.5)
    p = out / "titres.json"
    old = json.loads(p.read_text()) if p.exists() else {}
    old.update(titles); p.write_text(json.dumps(old, ensure_ascii=False, indent=1))
    print(key, n, "candidates")


CAND = False
ONLY = []


def main():
    global CAND, ONLY
    args = sys.argv[1:]
    if "--choix" in args:
        CAND = True; args.remove("--choix")
    ONLY = [a.split("=", 1)[1].split(",") for a in args if a.startswith("--lieux=")]
    ONLY = ONLY[0] if ONLY else []
    args = [a for a in args if not a.startswith("--lieux=")]
    names = args or list(SERIES)
    for name in names:
        out = ROOT / "video" / "photos" / name
        out.mkdir(parents=True, exist_ok=True)
        credits, used = {}, set()
        only = set(ONLY)
        for key, queries, must, *forced in SERIES[name]:
            if only and key not in only:
                continue
            if CAND:
                candidates(name, key, queries, must); continue
            x = (info([forced[0]]) or [None])[0] if forced else pick(queries, must, used)
            if not x:
                print("AUCUNE photo pour", key); continue
            used.add(x["title"])
            w = min(x["width"], 3200)
            big = x["thumb"].replace("/1600px-", f"/{w}px-") if x["width"] > 1600 else x["thumb"]
            req = urllib.request.Request(big, headers={"User-Agent": UA})
            try:
                data = urllib.request.urlopen(req, timeout=60).read()
            except Exception:  # noqa: BLE001
                data = urllib.request.urlopen(urllib.request.Request(x["thumb"], headers={"User-Agent": UA}), timeout=60).read()
            vertical(data).save(out / f"{key}.webp", "WEBP", quality=82)
            credits[key] = {k: x[k] for k in ("title", "page", "author", "license", "license_url")}
            print("OK", key, "<-", x["title"], "|", x["author"], "|", x["license"])
            time.sleep(0.5)
        if CAND:
            continue
        p = out / "credits.json"
        if only and p.exists():
            credits = {**json.loads(p.read_text()), **credits}
        p.write_text(json.dumps(credits, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
