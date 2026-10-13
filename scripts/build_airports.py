#!/usr/bin/env python3
"""Génère site/data/airports.json : tous les aéroports avec code IATA et vols réguliers (moyens et grands).

Source : OurAirports (domaine public), via le paquet npm « airports-json ».
Usage : npm pack airports-json && tar xzf airports-json-*.tgz
        python3 scripts/build_airports.py package/data/airports.json
Format de sortie : [code IATA, ville, nom de l'aéroport, code pays ISO, 1 si grand aéroport, latitude, longitude]
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Noms de villes en français (prioritaires sur les noms anglais de la source)
FR = {
    "CDG": "Paris", "ORY": "Paris", "BVA": "Paris-Beauvais", "BRU": "Bruxelles", "CRL": "Bruxelles-Charleroi", "GVA": "Genève",
    "LHR": "Londres", "LGW": "Londres", "STN": "Londres", "LTN": "Londres", "LCY": "Londres", "FRA": "Francfort", "MUC": "Munich",
    "BCN": "Barcelone", "LIS": "Lisbonne", "FCO": "Rome", "CIA": "Rome", "MXP": "Milan", "LIN": "Milan", "VCE": "Venise", "NAP": "Naples",
    "ATH": "Athènes", "CPH": "Copenhague", "VIE": "Vienne", "PRG": "Prague", "WAW": "Varsovie", "MOW": "Moscou", "SVO": "Moscou",
    "CAI": "Le Caire", "ALG": "Alger", "ADD": "Addis-Abeba", "CPT": "Le Cap", "RUN": "La Réunion", "MRU": "Maurice", "NSI": "Yaoundé",
    "NDJ": "N’Djamena", "LFW": "Lomé", "SEZ": "Seychelles", "DXB": "Dubaï", "JED": "Djeddah", "RUH": "Riyad", "MED": "Médine",
    "PEK": "Pékin", "PKX": "Pékin", "SIN": "Singapour", "HND": "Tokyo", "NRT": "Tokyo", "YUL": "Montréal", "YQB": "Québec",
    "PTP": "Pointe-à-Pitre", "FDF": "Fort-de-France", "CAY": "Cayenne", "NOU": "Nouméa", "PPT": "Papeete", "SAW": "Istanbul",
    "IST": "Istanbul", "MEX": "Mexico", "HAV": "La Havane", "BOG": "Bogota", "LIM": "Lima", "FIH": "Kinshasa", "NIM": "Niamey",
    "DSS": "Dakar", "TNR": "Antananarivo", "BZV": "Brazzaville", "PNR": "Pointe-Noire", "ZNZ": "Zanzibar", "DJE": "Djerba",
    "TNG": "Tanger", "FEZ": "Fès", "AGA": "Agadir", "OUD": "Oujda", "ESU": "Essaouira", "TLV": "Tel-Aviv", "BEY": "Beyrouth",
    "AMM": "Amman", "SSH": "Charm el-Cheikh", "HRG": "Hurghada", "CMN": "Casablanca", "RAK": "Marrakech", "DOH": "Doha",
}

def main(src):
    data = json.loads(pathlib.Path(src).read_text(encoding="utf-8"))
    out, seen = [], set()
    for r in data:
        code = (r.get("iata_code") or "").strip().upper()
        if len(code) != 3 or r.get("scheduled_service") != "yes" or code in seen:
            continue
        seen.add(code)
        city = FR.get(code) or (r.get("municipality") or "").split(",")[0].strip() or r["name"]
        name = r["name"].replace("  ", " ").strip()
        out.append([code, city, name, r["iso_country"], 1 if r["type"] == "large_airport" else 0,
                    round(float(r["latitude_deg"]), 2), round(float(r["longitude_deg"]), 2)])
    out.sort(key=lambda a: (-a[4], a[1]))
    dest = ROOT / "site" / "data" / "airports.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(out)} aéroports, {len({a[3] for a in out})} pays -> {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} Ko)")

if __name__ == "__main__":
    main(sys.argv[1])
