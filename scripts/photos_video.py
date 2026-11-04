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


def main():
    names = sys.argv[1:] or list(SERIES)
    for name in names:
        out = ROOT / "video" / "photos" / name
        out.mkdir(parents=True, exist_ok=True)
        credits, used = {}, set()
        for key, queries, must in SERIES[name]:
            x = pick(queries, must, used)
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
        (out / "credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
