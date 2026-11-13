#!/usr/bin/env python3
"""Photos libres de Wikimedia Commons pour les vidéos « Un pays en 40 secondes ».

Lancé par GitHub (.github/workflows/photos-pays.yml) : les machines de GitHub ont leur propre réseau, alors que la session
qui fabrique les vidéos voit la moitié de ses téléchargements refusés par Wikimedia.

Entrée : video/demandes/photos-pays.json
  { "code": "rdcongo", "lieux": { "kinshasa": "Kinshasa skyline", "zongo": "Zongo Falls", … } }
  (clé = nom court du lieu, valeur = mots à chercher sur Commons, en anglais ou en français)
Sortie : photos-pays/<code>/<lieu>/01.jpg … (1280 px de large, ou 1920 avec "largeur": 1920 ; 6 au plus par lieu, ou "max") et photos-pays/<code>/index.json avec,
pour chaque photo : titre du fichier, auteur, licence, description, catégories, taille d'origine.
Seules les licences libres sont gardées (CC0, domaine public, CC BY, CC BY-SA)."""
import json, os, re, sys, time, html, urllib.parse, urllib.request

UA = "EscaleVideos/1.0 (https://escale.live/contact/)"
API = "https://commons.wikimedia.org/w/api.php"
LIBRE = re.compile(r"^(cc0|public domain|pd|cc[ -]by(-sa)?[ -]\d)", re.I)


def get(url, binaire=False, essais=4):
    for i in range(essais):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                d = r.read()
                return d if binaire else d.decode("utf-8")
        except Exception as e:  # réseau, 429… : on attend un peu et on réessaie
            print("  nouvel essai :", str(e)[:80], flush=True)
            time.sleep(5 * (i + 1))
    return None


def texte(v):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", v or ""))).strip()


def chercher(mots, n=14, largeur=1280):
    q = {"action": "query", "format": "json", "generator": "search", "gsrsearch": mots + " filetype:bitmap", "gsrnamespace": 6, "gsrlimit": n,
         "prop": "imageinfo|categories", "cllimit": 50, "iiprop": "url|size|extmetadata|mime", "iiurlwidth": largeur}
    d = json.loads(get(API + "?" + urllib.parse.urlencode(q)) or "{}")
    return sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0))


def main():
    dem = json.load(open("video/demandes/photos-pays.json", encoding="utf-8"))
    code = re.sub(r"[^a-z0-9-]", "", dem["code"].lower())
    # Facultatif dans la demande : "largeur" (1280 par défaut ; 1920 pour une photo affichée en grand) et "max" (photos gardées par lieu, 6 par défaut)
    largeur = 1920 if dem.get("largeur") == 1920 else 1280
    maxi = min(6, max(1, int(dem.get("max", 6))))
    base = f"photos-pays/{code}"
    os.makedirs(base, exist_ok=True)
    index = {}
    for lieu, mots in dem["lieux"].items():
        lieu = re.sub(r"[^a-z0-9-]", "", lieu.lower())
        os.makedirs(f"{base}/{lieu}", exist_ok=True)
        gardees = []
        for p in chercher(mots, largeur=largeur):
            ii = (p.get("imageinfo") or [{}])[0]
            m = ii.get("extmetadata", {})
            lic = texte(m.get("LicenseShortName", {}).get("value"))
            if ii.get("mime") != "image/jpeg" or ii.get("width", 0) < max(1500, largeur) or not LIBRE.match(lic) or not ii.get("thumburl"):
                continue
            img = get(ii["thumburl"], binaire=True)
            if (not img or img[:3] != b"\xff\xd8\xff") and largeur != 1280:  # taille refusée : on se rabat sur 1280 px
                img = get(ii["thumburl"].replace(f"/{largeur}px-", "/1280px-"), binaire=True, essais=2)
            if not img or img[:3] != b"\xff\xd8\xff":
                continue
            nom = f"{len(gardees) + 1:02d}.jpg"
            open(f"{base}/{lieu}/{nom}", "wb").write(img)
            gardees.append({"image": f"{lieu}/{nom}", "fichier": p["title"], "auteur": texte(m.get("Artist", {}).get("value"))[:120], "licence": lic,
                            "description": texte(m.get("ImageDescription", {}).get("value"))[:300], "largeur": ii["width"], "hauteur": ii["height"],
                            "categories": [c["title"].replace("Category:", "") for c in p.get("categories", [])][:12], "page": ii.get("descriptionurl", "")})
            time.sleep(1)
            if len(gardees) == maxi:
                break
        index[lieu] = {"recherche": mots, "photos": gardees}
        print(f"{lieu} : {len(gardees)} photo(s)", flush=True)
        time.sleep(2)
    json.dump({"code": code, "lieux": index}, open(f"{base}/index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if not any(v["photos"] for v in index.values()):
        sys.exit("Aucune photo trouvée")


if __name__ == "__main__":
    main()
