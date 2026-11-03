"""Noms des villes dans chaque langue du site, pour les aéroports de site/data/airports.json (le nom de base est en français).

Source : Wikidata (licence CC0), lancé par GitHub Actions (.github/workflows/noms-villes.yml), qui a accès à Internet :
  python3 scripts/noms_villes.py
Pour chaque aéroport : la ville desservie (propriété P931) et son nom en anglais, espagnol, portugais, arabe, italien, allemand
et néerlandais. On ne garde la ville que si son nom français correspond à celui du site (ou son nom anglais), pour ne jamais
remplacer « Paris-Beauvais » par un village voisin. Résultat : site/data/noms/<langue>.json = {code : nom}, seulement quand le nom diffère.
"""
import json
import re
import pathlib
import time
import unicodedata
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = json.loads((ROOT / "site" / "data" / "airports.json").read_text(encoding="utf-8"))
OUT = ROOT / "site" / "data" / "noms"
LANGS = ["en", "es", "pt", "ar", "it", "de", "nl"]
UA = "EscaleNoms/1.0 (https://escale.live; comparateur de vols)"


def norm(t):
    t = unicodedata.normalize("NFD", t or "")
    return "".join(c for c in t if unicodedata.category(c) != "Mn").lower().replace("-", " ").replace("’", "'").strip()


SUFFIX = re.compile(r"\s*(,\s*D\.C\.|Municipality|Municipio|Kommune|kommun|City|Province|Provinz|Provincia|governorate|Governorate|County|District|"
                    r"Upazila|Island|First Nation|-shi|-machi|-shi|Landkreis)$", re.I)
KEEP = {"Mexico City", "Quebec City", "Kuwait City", "Panama City", "Guatemala City", "Ho Chi Minh City", "Cape Town"}
BAD = {"Luperon pto pta"}  # libellés Wikidata erronés


def clean(base, label):
    """Nom traduit débarrassé des mots administratifs ; le nom du site si la traduction n'apporte rien."""
    if label in KEEP:
        return label
    if label in BAD:
        return base
    v = re.sub(r"\s*\([^)]*\)$", "", label)  # « Altái (Sinkiang) »
    for _ in range(2):
        v = SUFFIX.sub("", v).strip(" ,")
    v = re.sub(r"^(Heroica|Municipio de|Comune di)\s+", "", v)
    nb, nv = norm(base), norm(v)
    if not v or nv == nb:
        return v if v and len(v) == len(base) else base  # mêmes lettres : on garde les accents de la traduction si même longueur
    if nb in nv and len(v) > len(base):  # « Tapachula de Córdova y Ordóñez » : une précision, pas une traduction
        return base
    return v


def sparql(codes):
    vals = " ".join(f'"{c}"' for c in codes)
    q = f"""SELECT ?iata ?city ?lang ?l WHERE {{ VALUES ?iata {{ {vals} }} ?ap wdt:P238 ?iata . ?ap wdt:P931 ?city .
      ?city rdfs:label ?l . BIND(LANG(?l) AS ?lang) FILTER(?lang IN ("fr","en","es","pt","ar","it","de","nl")) }}"""
    url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q, "format": "json"})
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/sparql-results+json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)["results"]["bindings"]
        except Exception as e:  # noqa: BLE001
            print("  nouvel essai :", e)
            time.sleep(5 * (attempt + 1))
    return []


def main():
    names = {a[0]: a[1] for a in DB}
    found = {}  # code -> {ville wikidata -> {langue: nom}}
    codes = list(names)
    for i in range(0, len(codes), 250):
        for b in sparql(codes[i:i + 250]):
            found.setdefault(b["iata"]["value"], {}).setdefault(b["city"]["value"], {})[b["lang"]["value"]] = b["l"]["value"]
        print(f"{min(i + 250, len(codes))}/{len(codes)}")
        time.sleep(1)
    out = {l: {} for l in LANGS}
    kept = 0
    for code, cities in found.items():
        base = norm(names[code])
        good = [lab for lab in cities.values() if base in (norm(lab.get("fr")), norm(lab.get("en")))]
        if not good:
            continue
        lab = max(good, key=len)
        kept += 1
        for l in LANGS:
            v = lab.get(l) and clean(names[code], lab.get(l))
            if v and v != names[code]:
                out[l][code] = v
    OUT.mkdir(parents=True, exist_ok=True)
    for l in LANGS:
        (OUT / f"{l}.json").write_text(json.dumps(dict(sorted(out[l].items())), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(l, len(out[l]), "noms")
    print("aéroports avec une ville reconnue :", kept, "/", len(codes))


if __name__ == "__main__":
    main()
