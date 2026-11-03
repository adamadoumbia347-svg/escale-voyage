"""Liens partenaires Trip.com (hôtels) : identifiants de ville Trip.com vérifiés sur les pages « …-hotels-list-ID » du site Trip.com."""
import urllib.parse

AFF = {"Allianceid": "11233048", "SID": "335082259", "trip_sub1": "escale"}
# Code d'aéroport (ou de ville) -> identifiant de ville Trip.com
IDS = {"ABJ": 3265, "DSS": 856, "DKR": 856, "CMN": 809, "CAS": 809, "RAK": 1360, "CAI": 332, "LOS": 783, "ACC": 1274, "NBO": 825,
       "DXB": 220, "IST": 532, "BKK": 359, "HND": 228, "NRT": 228, "TYO": 228, "DPS": 723, "SIN": 73, "HKT": 725, "CDG": 192, "PAR": 192, "ORY": 192}

LABEL = {"fr": "Hôtels à {c} sur Trip.com", "en": "Hotels in {c} on Trip.com", "es": "Hoteles en {c} en Trip.com", "pt": "Hotéis em {c} na Trip.com",
         "ar": "فنادق {c} على Trip.com", "it": "Hotel a {c} su Trip.com", "de": "Hotels in {c} bei Trip.com", "nl": "Hotels in {c} op Trip.com"}


def link(code, sub="site"):
    cid = IDS.get((code or "").upper())
    if not cid:
        return None
    return "https://www.trip.com/hotels/list?" + urllib.parse.urlencode({"city": cid, **AFF, "trip_sub2": sub})


def li(code, city, lang, sub):
    u = link(code, sub)
    if not u:
        return ""
    import html
    return f'<li><a href="{html.escape(u)}" target="_blank" rel="sponsored noopener noreferrer">{html.escape(LABEL.get(lang, LABEL["en"]).format(c=city))}</a></li>'
