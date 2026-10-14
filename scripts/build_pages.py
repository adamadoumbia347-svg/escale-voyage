#!/usr/bin/env python3
"""Génère les pages trajets, les pages légales, le sitemap et la liste des guides de la page d'accueil.

Lancer : python3 scripts/build_pages.py   (Netlify le lance aussi à chaque déploiement)
"""
import datetime
import html
import os
import pathlib
import re
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_i18n  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
# Adresse du site. Sur Netlify, la variable URL contient l'adresse principale : dès qu'un nom de domaine
# est défini comme domaine principal, toutes les adresses (canonical, sitemap, hreflang, image de partage) le suivent.
DEFAULT_DOMAIN = "https://escale-voyage.netlify.app"
DOMAIN = (os.environ.get("URL") or DEFAULT_DOMAIN).rstrip("/")
if not DOMAIN.startswith("https://"):
    DOMAIN = DEFAULT_DOMAIN
TODAY = datetime.date.today().isoformat()

# from, to, ville départ, ville arrivée, pays, aéroport arrivée, durée directe (ou None), haute saison, note
ROUTES = [
    ("CDG", "BKO", "Paris", "Bamako", "Mali", "Aéroport international Modibo-Keïta", None,
     "juillet-août, les fêtes de fin d'année et la Tabaski",
     "Les vols directs depuis Paris sont rares ou suspendus selon les périodes : la plupart des trajets passent par Casablanca, Alger, Tunis, Istanbul ou Addis-Abeba. Comparez la durée totale, pas seulement le prix."),
    ("CDG", "DSS", "Paris", "Dakar", "Sénégal", "Aéroport international Blaise-Diagne (AIBD), à environ 45 km de Dakar", "5 h 30",
     "juillet-août, les fêtes de fin d'année, la Tabaski et le Magal de Touba",
     "Des vols partent aussi d'Orly : cochez les deux aéroports parisiens dans les comparateurs pour élargir le choix."),
    ("CDG", "ABJ", "Paris", "Abidjan", "Côte d'Ivoire", "Aéroport international Félix-Houphouët-Boigny", "6 h 30",
     "juillet-août et les fêtes de fin d'année",
     "Plusieurs compagnies desservent la ligne depuis Roissy et Orly : la concurrence fait souvent baisser les prix en basse saison."),
    ("CDG", "CKY", "Paris", "Conakry", "Guinée", "Aéroport international de Conakry-Gbessia", "6 h",
     "juillet-août et les fêtes de fin d'année",
     "Les vols avec escale à Casablanca, Dakar ou Bruxelles sont parfois nettement moins chers que le direct."),
    ("CDG", "DLA", "Paris", "Douala", "Cameroun", "Aéroport international de Douala", "6 h 30",
     "juillet-août et les fêtes de fin d'année",
     "Pensez aussi à Yaoundé-Nsimalen (NSI) si votre destination finale est dans le centre du pays."),
    ("CDG", "LFW", "Paris", "Lomé", "Togo", "Aéroport international Gnassingbé-Eyadéma", "6 h",
     "juillet-août et les fêtes de fin d'année",
     "Comparez avec un vol vers Cotonou (COO) ou Accra (ACC), puis la route : c'est parfois moins cher."),
    ("CDG", "COO", "Paris", "Cotonou", "Bénin", "Aéroport international Cardinal-Bernardin-Gantin de Cotonou-Cadjehoun", "6 h",
     "juillet-août et les fêtes de fin d'année",
     "Comparez avec Lomé (LFW) : les deux villes sont proches et les prix varient beaucoup."),
    ("CDG", "OUA", "Paris", "Ouagadougou", "Burkina Faso", "Aéroport international de Ouagadougou", None,
     "juillet-août et les fêtes de fin d'année",
     "L'offre de vols directs varie selon la situation : les trajets avec escale via Abidjan, Casablanca, Alger ou Istanbul sont fréquents."),
    ("BRU", "FIH", "Bruxelles", "Kinshasa", "RD Congo", "Aéroport international de N'djili", "8 h",
     "juillet-août et les fêtes de fin d'année",
     "Depuis Paris, comparez avec un départ de Bruxelles : il est souvent plus avantageux, même en ajoutant le train."),
    ("ORY", "CMN", "Paris", "Casablanca", "Maroc", "Aéroport Mohammed-V", "3 h",
     "juillet-août, les vacances scolaires et l'Aïd",
     "Les compagnies low-cost desservent aussi Marrakech, Rabat et Tanger : regardez la ville la plus proche de votre destination."),
    ("CDG", "ALG", "Paris", "Alger", "Algérie", "Aéroport Houari-Boumédiène", "2 h 15",
     "juillet-août, l'Aïd et les vacances scolaires",
     "Comparez avec Lyon, Marseille ou Bordeaux si vous pouvez partir d'une autre ville : les prix d'été changent beaucoup d'un aéroport à l'autre."),
    ("CDG", "TUN", "Paris", "Tunis", "Tunisie", "Aéroport international de Tunis-Carthage", "2 h 15",
     "juillet-août et l'Aïd",
     "Pensez aussi à Djerba (DJE) et Monastir (MIR), souvent desservis par des vols moins chers en été."),
    ("CDG", "YUL", "Paris", "Montréal", "Canada", "Aéroport international Montréal-Trudeau", "7 h 30",
     "juillet-août et les fêtes de fin d'année",
     "Une autorisation de voyage électronique (AVE) est exigée pour la plupart des voyageurs : vérifiez avant de réserver."),
    ("CDG", "DXB", "Paris", "Dubaï", "Émirats arabes unis", "Aéroport international de Dubaï", "6 h 45",
     "de novembre à mars, quand il fait moins chaud",
     "Dubaï est aussi une escale pratique vers l'Asie et l'Afrique de l'Est : un stop de quelques jours ne coûte parfois rien de plus."),
    ("CDG", "FIH", "Paris", "Kinshasa", "RD Congo", "Aéroport international de N'djili", "8 h",
     "juillet-août et les fêtes de fin d'année",
     "Comparez avec un départ de Bruxelles, historiquement très bien relié à Kinshasa : l'écart de prix peut couvrir le train Paris–Bruxelles."),
    ("CDG", "LBV", "Paris", "Libreville", "Gabon", "Aéroport international Léon-Mba", "6 h 30",
     "juillet-août et les fêtes de fin d'année",
     "Peu de compagnies desservent la ligne en direct : réservez tôt pour l'été et regardez aussi les escales via Casablanca, Addis-Abeba ou Douala."),
    ("CDG", "NSI", "Paris", "Yaoundé", "Cameroun", "Aéroport international de Yaoundé-Nsimalen", "6 h 30",
     "juillet-août et les fêtes de fin d'année",
     "Comparez avec Douala (DLA) : selon les dates, arriver à Douala puis prendre la route ou un vol intérieur peut revenir moins cher."),
    ("CDG", "NKC", "Paris", "Nouakchott", "Mauritanie", "Aéroport international de Nouakchott-Oumtounsy", None,
     "juillet-août et les fêtes de fin d'année",
     "Les trajets avec escale à Casablanca, Tunis ou Dakar sont fréquents : comparez la durée de correspondance."),
    ("CDG", "NIM", "Paris", "Niamey", "Niger", "Aéroport international Diori-Hamani", None,
     "juillet-août et les fêtes de fin d'année",
     "L'offre de vols change selon la situation : passez par les comparateurs pour voir les escales disponibles (Casablanca, Alger, Istanbul, Addis-Abeba…)."),
    ("CDG", "RAK", "Paris", "Marrakech", "Maroc", "Aéroport Marrakech-Ménara", "3 h 15",
     "les vacances scolaires, Noël et Pâques",
     "Beaucoup de vols low-cost partent d'Orly et de Beauvais : vérifiez les trois aéroports parisiens."),
    ("CDG", "IST", "Paris", "Istanbul", "Turquie", "Aéroport d'Istanbul", "3 h 20",
     "juillet-août et les vacances de printemps",
     "Pensez aussi à l'aéroport Sabiha-Gökçen (SAW), côté asiatique, souvent desservi par des compagnies moins chères."),
    ("CDG", "JED", "Paris", "Djeddah", "Arabie saoudite", "Aéroport international Roi-Abdelaziz", "6 h",
     "le Ramadan, le Hajj et les vacances scolaires",
     "Pour la Omra, réservez le plus tôt possible avant le Ramadan : les prix montent fortement. Médine (MED) est une alternative d'arrivée."),
    ("CDG", "PTP", "Paris", "Pointe-à-Pitre", "Guadeloupe", "Aéroport Guadeloupe – Pôle Caraïbes", "8 h 30",
     "juillet-août, Noël et le carnaval",
     "Les vols partent de Roissy et d'Orly : comparez les deux, les écarts sont fréquents."),
    ("CDG", "RUN", "Paris", "La Réunion", "La Réunion", "Aéroport de La Réunion Roland-Garros", "11 h",
     "juillet-août et décembre-janvier",
     "Comparez aussi l'arrivée à Saint-Pierre Pierrefonds (ZSE) si vous allez dans le sud de l'île."),
    ("MRS", "ALG", "Marseille", "Alger", "Algérie", "Aéroport Houari-Boumédiène", "1 h 45",
     "juillet-août, l'Aïd et les vacances scolaires",
     "L'été, les prix grimpent très vite : réservez dès le printemps et comparez avec un départ de Lyon ou Montpellier."),
    ("MRS", "TUN", "Marseille", "Tunis", "Tunisie", "Aéroport international de Tunis-Carthage", "1 h 30",
     "juillet-août et l'Aïd",
     "Comparez avec Djerba (DJE) et Monastir (MIR) selon votre destination finale."),
    ("MRS", "DSS", "Marseille", "Dakar", "Sénégal", "Aéroport international Blaise-Diagne (AIBD)", None,
     "juillet-août, les fêtes de fin d'année et la Tabaski",
     "Comparez un départ de Marseille avec escale et un train jusqu'à Paris suivi d'un vol direct : le second est parfois moins cher."),
    ("LYS", "CMN", "Lyon", "Casablanca", "Maroc", "Aéroport Mohammed-V", "2 h 45",
     "juillet-août, les vacances scolaires et l'Aïd",
     "Regardez aussi les vols Lyon–Marrakech et Lyon–Oujda selon votre destination finale."),
    ("LYS", "DSS", "Lyon", "Dakar", "Sénégal", "Aéroport international Blaise-Diagne (AIBD)", None,
     "juillet-août, les fêtes de fin d'année et la Tabaski",
     "Comparez avec un départ de Genève, à moins de 2 heures de Lyon : l'offre est parfois plus large."),
    ("BRU", "DSS", "Bruxelles", "Dakar", "Sénégal", "Aéroport international Blaise-Diagne (AIBD)", "6 h",
     "juillet-août, les fêtes de fin d'année et la Tabaski",
     "Depuis le nord de la France, comparez avec Paris : la différence de prix couvre souvent le train."),
    ("BRU", "ABJ", "Bruxelles", "Abidjan", "Côte d'Ivoire", "Aéroport international Félix-Houphouët-Boigny", "6 h 30",
     "juillet-août et les fêtes de fin d'année",
     "Comparez avec un départ de Paris : la concurrence y est plus forte et les promotions plus fréquentes."),
    ("BRU", "DLA", "Bruxelles", "Douala", "Cameroun", "Aéroport international de Douala", None,
     "juillet-août et les fêtes de fin d'année",
     "Comparez la durée totale : certains vols font une escale technique en Afrique de l'Ouest ou centrale."),
    ("GVA", "CMN", "Genève", "Casablanca", "Maroc", "Aéroport Mohammed-V", "3 h",
     "juillet-août, les vacances scolaires et l'Aïd",
     "Si vous habitez en France voisine, comparez avec Lyon : les deux aéroports sont à moins de 2 heures."),
    ("GVA", "DSS", "Genève", "Dakar", "Sénégal", "Aéroport international Blaise-Diagne (AIBD)", None,
     "juillet-août, les fêtes de fin d'année et la Tabaski",
     "Les vols passent souvent par Paris, Bruxelles, Lisbonne ou Casablanca : comparez la durée de l'escale."),
]

# ville, pays, [(quartier, pour qui)], conseil, aéroport (code)
HOTELS = [
    ("Dakar", "Sénégal", [("Plateau", "proche des administrations et du centre d'affaires"), ("Almadies et Ngor", "bord de mer, restaurants, plus calme"), ("Mermoz et Sacré-Cœur", "résidentiel, bon rapport qualité-prix")],
     "L'aéroport Blaise-Diagne est loin du centre (environ 45 km) : pour une arrivée tardive, une nuit près de l'aéroport ou à Saly peut être plus pratique.", "DSS"),
    ("Abidjan", "Côte d'Ivoire", [("Plateau", "quartier des affaires"), ("Cocody", "résidentiel, hôtels et restaurants"), ("Zone 4 (Marcory)", "vie nocturne, proche de l'aéroport")],
     "Marcory et la Zone 4 sont les plus proches de l'aéroport Félix-Houphouët-Boigny : pratique pour un court séjour.", "ABJ"),
    ("Bamako", "Mali", [("ACI 2000", "quartier moderne, hôtels d'affaires"), ("Hippodrome", "animé, restaurants"), ("Badalabougou", "rive droite, plus calme")],
     "Vérifiez les conseils aux voyageurs du ministère des Affaires étrangères avant de réserver, et privilégiez les annulations gratuites.", "BKO"),
    ("Casablanca", "Maroc", [("Centre-ville et Maârif", "commerces, transports, prix moyens"), ("Aïn Diab", "corniche et bord de mer"), ("Gauthier", "central et calme")],
     "Le train relie l'aéroport Mohammed-V au centre : inutile de payer un hôtel près de l'aéroport.", "CMN"),
    ("Marrakech", "Maroc", [("Médina", "riads traditionnels, au cœur de la ville"), ("Guéliz", "ville moderne, restaurants"), ("Hivernage", "hôtels avec piscine, plus chic")],
     "Les riads de la médina affichent souvent des prix plus bas sur réservation directe hors saison : comparez avec Booking.", "RAK"),
    ("Douala", "Cameroun", [("Bonanjo", "quartier administratif et des affaires"), ("Akwa", "commerçant et animé"), ("Bonapriso", "résidentiel, plus calme")],
     "Les embouteillages sont fréquents : choisissez votre hôtel près de vos rendez-vous plutôt que le moins cher.", "DLA"),
    ("Conakry", "Guinée", [("Kaloum", "centre administratif et des affaires"), ("Ratoma", "résidentiel, hôtels récents"), ("Kipé", "restaurants, plus calme")],
     "Kaloum est éloigné de l'aéroport et souvent embouteillé : vérifiez le temps de trajet avant de réserver.", "CKY"),
    ("Lomé", "Togo", [("Centre-ville", "marché, commerces"), ("Bè et bord de mer", "plages et maquis"), ("Quartier administratif", "calme, proche des institutions")],
     "Lomé est compacte : un hôtel en bord de mer reste proche de tout.", "LFW"),
    ("Cotonou", "Bénin", [("Haie Vive", "restaurants et vie nocturne"), ("Ganhi", "centre des affaires"), ("Fidjrossè", "bord de mer, plus détendu")],
     "Haie Vive est proche de l'aéroport : pratique pour une arrivée ou un départ de nuit.", "COO"),
    ("Kinshasa", "RD Congo", [("Gombe", "centre des affaires, hôtels internationaux"), ("Ngaliema", "résidentiel"), ("Limete", "commerçant")],
     "L'aéroport de N'djili est loin de la Gombe : prévoyez du temps de trajet, surtout en fin de journée.", "FIH"),
    ("Alger", "Algérie", [("Centre (Alger-Centre, Didouche)", "transports et commerces"), ("Hydra", "résidentiel et calme"), ("Bab Ezzouar", "proche de l'aéroport, hôtels d'affaires")],
     "Bab Ezzouar est pratique pour un court séjour ou une correspondance, à quelques minutes de l'aéroport.", "ALG"),
    ("Tunis", "Tunisie", [("Centre-ville", "médina et avenue Bourguiba"), ("Les Berges du Lac", "moderne, hôtels d'affaires"), ("La Marsa et Gammarth", "bord de mer")],
     "Hors été, les hôtels de bord de mer de Gammarth baissent beaucoup leurs prix.", "TUN"),
    ("Paris", "France", [("Gare du Nord et République", "bien reliés à Roissy (RER B)"), ("Bastille et Nation", "prix plus doux, bien desservis"), ("Porte de Versailles et Montparnasse", "pratique pour Orly")],
     "Pour un vol tôt le matin, un hôtel près de la ligne du RER B (Roissy) ou de l'Orlyval évite un taxi coûteux.", "CDG"),
    ("Dubaï", "Émirats arabes unis", [("Deira et Bur Dubaï", "les plus abordables, proches de l'aéroport et du métro"), ("Downtown", "Burj Khalifa et Dubai Mall"), ("Dubai Marina", "bord de mer, plus cher")],
     "Les prix chutent l'été (juin-août) mais il fait très chaud : idéal pour un séjour en hôtel avec piscine.", "DXB"),
    ("Istanbul", "Turquie", [("Sultanahmet", "monuments à pied"), ("Beyoğlu et Taksim", "animé, restaurants"), ("Kadıköy", "côté asiatique, plus local et abordable")],
     "Le nouvel aéroport d'Istanbul est loin du centre : comptez au moins une heure de trajet.", "IST"),
    ("Montréal", "Canada", [("Centre-ville", "proche de tout, métro"), ("Plateau-Mont-Royal", "quartier vivant, appartements"), ("Vieux-Montréal", "charme historique, plus cher")],
     "L'hiver (janvier-mars) est la saison la moins chère pour les hôtels, sauf pendant les festivals.", "YUL"),
]

def hotel_slug(h):
    return f"hotel-pas-cher-{slug(h[0])}"

def slug(t):
    t = t.lower().replace("'", "-")
    for a, b in (("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"), ("à", "a"), ("â", "a"), ("ï", "i"), ("î", "i"), ("ô", "o"), ("û", "u"), ("ü", "u"), ("ç", "c")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

def route_slug(r):
    return f"vol-{slug(r[2])}-{slug(r[3])}"

E = html.escape

# Script Travelpayouts (vérification du site et suivi des liens partenaires), inséré dans le <head> de chaque page
# Il reste bloqué (type="text/plain") tant que le visiteur n'a pas accepté les cookies : site/consent.js l'active.
TRAVELPAYOUTS = (ROOT / "scripts" / "travelpayouts-snippet.html").read_text(encoding="utf-8").strip()
TRAVELPAYOUTS = TRAVELPAYOUTS.replace("<script ", '<script type="text/plain" data-consent="marketing" ', 1)
TRAVELPAYOUTS += '\n<script src="/consent.js" defer></script>'

HEAD = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{tp}
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#18202c">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="manifest" href="/manifest.webmanifest">
<meta property="og:type" content="article">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Escale">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{domain}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@700&display=swap">
<link rel="stylesheet" href="/pages.css">
{ld}
</head>
<body>
<header class="board"><div class="wrap">
  <div class="page-top"><a class="brand" href="/"><span class="brand-mark">ESC</span><span class="brand-name">Escale</span></a>{switch}</div>
  {hero}
</div></header>
<main class="wrap">
{body}
</main>
<footer class="wrap">
  <nav class="foot-nav" aria-label="Pages du site"><a href="/">Comparer vols, hôtels et voitures</a><a href="/#guides">Guides des trajets</a><a href="/mentions-legales/">Mentions légales</a><a href="/confidentialite/">Confidentialité</a><a href="/contact/">Contact</a><a href="/bons-plans/">Bons plans</a><a href="#cookies" data-open-consent>Gérer les cookies</a></nav>
  <p>Escale ne vend pas de billets et ne fixe aucun prix. Les durées et informations sont indicatives : les programmes des compagnies changent, vérifiez toujours sur le site de réservation.</p>
</footer>
</body>
</html>
"""

def page(path, title, desc, hero, body, ld="", paths=None):
    url = f"{DOMAIN}/{path}/" if path else f"{DOMAIN}/"
    if paths:
        ld = build_i18n.alternates(paths, DOMAIN) + "\n" + ld
    switch = build_i18n.switcher(paths, "fr") if paths else ""
    out = HEAD.format(tp=TRAVELPAYOUTS, title=E(title), desc=E(desc), url=url, domain=DOMAIN, hero=hero, body=body, ld=ld, switch=switch)
    d = SITE / path
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(out, encoding="utf-8")
    return url

def route_page(r):
    fr, to, cf, ct, country, airport, dur, peak, note = r
    s = route_slug(r)
    title = f"Vol pas cher {cf} {ct} : comparer les prix"
    desc = (f"Trouvez un billet d'avion pas cher {cf} – {ct} ({fr} → {to}) : durée du vol, aéroport, meilleure période pour réserver "
            f"et comparaison des prix sur Google Flights, Skyscanner, Kayak et momondo.")
    app = "/?" + urllib.parse.urlencode({"type": "vols", "from": fr, "to": to})
    back = "/?" + urllib.parse.urlencode({"type": "vols", "from": to, "to": fr})
    hp = next((h for h in HOTELS if h[0] == ct), None)
    hotels = f"/{hotel_slug(hp)}/" if hp else "/?" + urllib.parse.urlencode({"type": "hotels", "dest": ct})
    cars = "/?" + urllib.parse.urlencode({"type": "voitures", "pick": to})
    gf = "https://www.google.com/travel/flights?" + urllib.parse.urlencode({"q": f"Flights from {fr} to {to}", "hl": "fr", "curr": "EUR"})
    sky = f"https://www.skyscanner.fr/transport/vols/{fr.lower()}/{to.lower()}/"
    dur_txt = f"environ {dur} en vol direct" if dur else "variable : la plupart des trajets ont au moins une escale"
    faq = [
        (f"Combien de temps dure un vol {cf} – {ct} ?", f"Comptez {dur_txt}. Avec une escale, le trajet total dure souvent plusieurs heures de plus selon la correspondance."),
        (f"Quand réserver un vol {cf} – {ct} pas cher ?", f"En général deux à trois mois avant le départ. Les prix montent fortement pendant {peak} : réservez plus tôt pour ces périodes."),
        (f"Quel aéroport à {ct} ?", f"Les vols arrivent à l'{airport[0].lower() + airport[1:]} (code {to})."),
        ("Les bagages sont-ils inclus ?", "Pas toujours. Les tarifs les plus bas n'incluent parfois qu'un petit sac. Vérifiez la franchise bagage en soute avant de payer, surtout si vous voyagez avec des valises."),
    ]
    ld = '<script type="application/ld+json">' + __import__("json").dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    }, ensure_ascii=False) + "</script>"
    hero = f"""<p class="eyebrow">{E(country)}</p>
  <h1>Vol pas cher {E(cf)} <span>→</span> {E(ct)}</h1>
  <p class="codes">{fr} → {to}</p>
  <p class="hero-price" id="hero-price" hidden></p>
  <div class="cta-row"><a class="btn" href="{E(app)}">Comparer les prix maintenant</a><a class="btn ghost" href="{E(back)}">Trajet retour {E(ct)} → {E(cf)}</a></div>"""
    facts = f"""<dl class="facts">
  <div><dt>Durée</dt><dd>{E(dur_txt[0].upper() + dur_txt[1:])}</dd></div>
  <div><dt>Arrivée</dt><dd>{E(airport)} ({to})</dd></div>
  <div><dt>Prix les plus hauts</dt><dd>{E(peak[0].upper() + peak[1:])}</dd></div>
</dl>"""
    body = f"""{facts}
<section id="route-prices" data-from="{fr}" data-to="{to}" hidden><h2>Prix repérés récemment</h2>
<p class="small">Prix aller-retour les plus bas trouvés ces derniers jours par des voyageurs, par mois de départ. Le tarif exact et disponible s'affiche sur les sites de réservation.</p>
<ul class="price-list"></ul></section>
<script src="/route-prices.js" defer></script>
{build_i18n.calendar_html("fr", fr, to)}
<section><h2>Notre conseil pour ce trajet</h2><p>{E(note)}</p></section>
<section><h2>Comment payer moins cher</h2>
<ol class="steps">
  <li><strong>Activez les dates flexibles.</strong> Décaler le départ d'un ou deux jours change souvent plus le prix que le choix du site.</li>
  <li><strong>Comparez au moins trois sites.</strong> Escale ouvre votre recherche déjà triée par prix sur Google Flights, Skyscanner, Kayak et momondo.</li>
  <li><strong>Vérifiez les bagages.</strong> Ajoutez le prix de la valise avant de comparer deux tarifs.</li>
  <li><strong>Créez une alerte prix</strong> sur Google Flights ou Kayak si vous partez dans plusieurs mois.</li>
</ol>
<p><a class="btn" href="{E(app)}">Lancer la recherche {E(cf)} → {E(ct)}</a></p>
</section>
<section><h2>Accès direct aux comparateurs</h2>
<ul class="links">
  <li><a href="{E(gf)}" target="_blank" rel="noopener noreferrer">Calendrier des prix sur Google Flights</a></li>
  <li><a href="{E(sky)}" target="_blank" rel="noopener noreferrer">Prix du mois sur Skyscanner</a></li>
  <li><a href="{E(hotels)}">Hôtels à {E(ct)}</a></li>
  <li><a href="{E(cars)}">Location de voiture à {E(ct)}</a></li>
</ul></section>
{build_i18n.extras_html(SITE, "fr", ct, build_i18n.city(ct, "en"), to)}
<section class="faq"><h2>Questions fréquentes</h2>
{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)}
</section>
<section><h2>Autres trajets</h2><ul class="route-links">{''.join(f'<li><a href="/{route_slug(o)}/">{E(o[2])} → {E(o[3])}</a></li>' for o in related(r))}</ul></section>"""
    paths = {"fr": s, **{l: build_i18n.route_path(r, l) for l in build_i18n.LANGS}}
    return page(s, title, desc, hero, body, ld, paths)

def related(r, n=9):
    """Trajets proches : même destination, même pays ou même ville de départ, puis le reste."""
    score = lambda o: (o[3] == r[3]) * 3 + (o[4] == r[4]) * 2 + (o[2] == r[2])
    others = [o for o in ROUTES if o is not r]
    return sorted(others, key=lambda o: -score(o))[:n]

def hotel_page(h):
    city, country, areas, tip, code = h
    s = hotel_slug(h)
    title = f"Hôtel pas cher à {city} : comparer les prix"
    desc = (f"Trouvez un hôtel pas cher à {city} ({country}) : quartiers où dormir, conseils pour payer moins cher et "
            f"comparaison des prix sur Booking, Google Hôtels, Kayak, Hotels.com, Agoda et Airbnb.")
    app = "/?" + urllib.parse.urlencode({"type": "hotels", "dest": city})
    booking = "https://www.booking.com/searchresults.fr.html?" + urllib.parse.urlencode({"ss": city, "order": "price"})
    google = "https://www.google.com/travel/search?" + urllib.parse.urlencode({"q": f"hôtels {city}", "hl": "fr", "curr": "EUR"})
    airbnb = f"https://www.airbnb.fr/s/{urllib.parse.quote(city)}/homes"
    flights = [r for r in ROUTES if r[3] == city]
    cars = "/?" + urllib.parse.urlencode({"type": "voitures", "pick": code})
    faq = [
        (f"Quel quartier choisir pour dormir à {city} ?", " ; ".join(f"{a} : {b}" for a, b in areas) + "."),
        (f"Comment trouver un hôtel pas cher à {city} ?", "Comparez plusieurs sites pour les mêmes dates, triez par prix, choisissez l'annulation gratuite et réservez tôt pour les périodes de fêtes. Regardez aussi les appartements, souvent avantageux à partir de 3 nuits."),
        ("Faut-il réserver avec annulation gratuite ?", "Oui, surtout si vos billets d'avion ne sont pas encore pris : vous pourrez rebasculer sur une meilleure offre si le prix baisse."),
    ]
    ld = '<script type="application/ld+json">' + __import__("json").dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]
    }, ensure_ascii=False) + "</script>"
    hero = f"""<p class="eyebrow">{E(country)}</p>
  <h1>Hôtel pas cher à <span>{E(city)}</span></h1>
  <p class="codes">{code} · {"hôtels, riads, appartements" if country == "Maroc" else "hôtels et appartements"}</p>
  <div class="cta-row"><a class="btn" href="{E(app)}">Comparer les prix des hôtels</a>{f'<a class="btn ghost" href="/{route_slug(flights[0])}/">Vols vers {E(city)}</a>' if flights else ''}</div>"""
    areas_html = "".join(f"<div><dt>{E(a)}</dt><dd>{E(b[0].upper() + b[1:])}</dd></div>" for a, b in areas)
    body = f"""<section><h2>Où dormir à {E(city)}</h2><dl class="facts">{areas_html}</dl></section>
<section><h2>Notre conseil</h2><p>{E(tip)}</p></section>
<section><h2>Comment payer moins cher</h2>
<ol class="steps">
  <li><strong>Comparez au moins trois sites.</strong> Le même hôtel n'a pas toujours le même prix sur Booking, Hotels.com ou Agoda.</li>
  <li><strong>Choisissez l'annulation gratuite.</strong> Vous pourrez réserver ailleurs si le prix baisse.</li>
  <li><strong>Regardez le prix total.</strong> Taxes de séjour, petit-déjeuner et frais de ménage changent le classement.</li>
  <li><strong>Pour 3 nuits ou plus, regardez les appartements</strong> : souvent moins chers pour une famille.</li>
</ol>
<p><a class="btn" href="{E(app)}">Lancer la recherche à {E(city)}</a></p>
</section>
<section><h2>Accès direct aux comparateurs</h2>
<ul class="links">
  <li><a href="{E(booking)}" target="_blank" rel="noopener noreferrer">Hôtels à {E(city)} sur Booking.com, du moins cher au plus cher</a></li>
  <li><a href="{E(google)}" target="_blank" rel="noopener noreferrer">Comparer les prix sur Google Hôtels</a></li>
  <li><a href="{E(airbnb)}" target="_blank" rel="noopener noreferrer">Appartements à {E(city)} sur Airbnb</a></li>
  <li><a href="{E(cars)}">Location de voiture à {E(city)}</a></li>
</ul></section>
{f'<section><h2>Vols vers {E(city)}</h2><ul class="route-links">' + "".join(f'<li><a href="/{route_slug(r)}/">{E(r[2])} → {E(r[3])}</a></li>' for r in flights) + '</ul></section>' if flights else ''}
{build_i18n.extras_html(SITE, "fr", city, build_i18n.city(city, "en"), code)}
<section class="faq"><h2>Questions fréquentes</h2>
{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)}
</section>
<section><h2>Autres villes</h2><ul class="route-links">{''.join(f'<li><a href="/{hotel_slug(o)}/">Hôtels à {E(o[0])}</a></li>' for o in HOTELS if o is not h)}</ul></section>"""
    paths = {"fr": s, **{l: build_i18n.hotel_path(h, l) for l in build_i18n.LANGS}}
    return page(s, title, desc, hero, body, ld, paths)

def legal_pages():
    urls = []
    hero = '<h1>Mentions légales</h1>'
    body = """<section><h2>Éditeur du site</h2>
<p>Le site Escale (escale-voyage.netlify.app) est édité à titre non professionnel.</p>
<p>Conformément à l'article 6, III-2 de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l'économie numérique, l'éditeur non professionnel peut ne tenir à la disposition du public que le nom et l'adresse de son hébergeur, après lui avoir communiqué ses éléments d'identification.</p>
<p>Contact : <a href="/contact/">formulaire de contact</a>.</p>
</section>
<section><h2>Hébergeur</h2>
<p>Netlify, Inc.<br>512 2nd Street, Suite 200<br>San Francisco, CA 94107, États-Unis<br>netlify.com</p>
</section>
<section><h2>Nature du service</h2>
<p>Escale est un outil de recherche gratuit. Il ne vend aucun billet, nuit d'hôtel ou location et ne fixe aucun prix. Chaque bouton « Voir les prix » ouvre une recherche sur un site tiers, qui est seul responsable de ses tarifs, de ses conditions et des réservations.</p>
<p>Certains liens peuvent être des liens partenaires : si vous réservez, Escale peut percevoir une commission, sans surcoût pour vous.</p>
</section>
<section><h2>Propriété intellectuelle</h2>
<p>Les textes et le design du site sont la propriété de l'éditeur. Les marques citées (Google Flights, Skyscanner, Kayak, momondo, Booking.com, Hotels.com, Agoda, Airbnb, Rentalcars, Discover Cars) appartiennent à leurs propriétaires respectifs et sont citées uniquement pour identifier les services comparés.</p>
</section>"""
    urls.append(page("mentions-legales", "Mentions légales | Escale", "Mentions légales du site Escale, comparateur de vols, hôtels et locations de voitures.", hero, body))
    hero = '<h1>Confidentialité</h1>'
    body = """<section><h2>En bref</h2>
<p>Escale ne demande aucun compte et ne collecte ni nom, ni e-mail, ni numéro de téléphone (sauf si vous nous écrivez via le formulaire de contact).</p>
</section>
<section><h2>Ce qui reste sur votre appareil</h2>
<p>Vos dernières recherches, le dernier onglet, la langue, la devise, votre aéroport de départ et votre choix concernant les cookies sont enregistrés dans le stockage local de votre navigateur, uniquement pour vous les reproposer. Ces données ne quittent pas votre appareil. Vous pouvez les effacer à tout moment en supprimant les données du site dans votre navigateur.</p>
</section>
<section><h2>Aéroport le plus proche</h2>
<p>Pour vous proposer l'aéroport de départ le plus proche et la bonne devise, notre hébergeur Netlify déduit votre ville et votre pays approximatifs de votre adresse IP au moment de la visite. Cette information sert uniquement à préremplir le formulaire : elle n'est ni enregistrée ni transmise à des tiers. Vous pouvez toujours changer l'aéroport et la devise.</p>
</section>
<section><h2>Prix indicatifs</h2>
<p>Pour afficher un prix indicatif, le site envoie le trajet et les dates recherchés (par exemple CDG → BKO en novembre) à notre serveur, qui interroge un fournisseur de données de prix. Aucune donnée personnelle n'est transmise.</p>
</section>
<section><h2>Liens partenaires (Travelpayouts)</h2>
<p>Avec votre accord seulement, le site charge un script de notre partenaire d'affiliation Travelpayouts. Il sert à attribuer à Escale les réservations faites après un clic sur un lien partenaire, et peut pour cela déposer des cookies ou utiliser des identifiants techniques sur votre navigateur. Travelpayouts applique sa propre politique de confidentialité, disponible sur travelpayouts.com.</p>
<p>Votre choix (accepter ou refuser) est demandé à votre première visite, gardé 6 mois dans votre navigateur, puis redemandé. Vous pouvez le changer à tout moment avec le lien <a href="#cookies" data-open-consent>Gérer les cookies</a>, aussi présent en bas de chaque page. Refuser ne change rien au fonctionnement des recherches.</p>
</section>
<section><h2>Hébergement</h2>
<p>Comme tout hébergeur, Netlify enregistre des journaux techniques (adresse IP, page demandée, date) nécessaires au fonctionnement et à la sécurité du site.</p>
</section>
<section><h2>Sites partenaires</h2>
<p>Quand vous cliquez sur « Voir les prix », vous quittez Escale. Le site ouvert (Google, Skyscanner, Booking, etc.) applique sa propre politique de confidentialité et ses propres cookies.</p>
</section>
<section><h2>Vos droits</h2>
<p>Conformément au RGPD, vous pouvez demander l'accès, la rectification ou l'effacement de données vous concernant. Escale ne détenant aucune donnée personnelle sur ses visiteurs, aucune information ne peut normalement vous être rattachée.</p>
</section>"""
    urls.append(page("confidentialite", "Confidentialité | Escale", "Politique de confidentialité du site Escale : aucun compte, aucun cookie de suivi.", hero, body))
    hero = '<h1>Contact</h1>'
    body = """<section><p>Une question, une erreur sur le site, une destination à ajouter ? Écrivez-nous. Pour une réservation, contactez directement le site où vous avez réservé : Escale ne gère aucune réservation.</p>
<form class="contact" name="contact" method="POST" action="/contact/merci/" data-netlify="true" netlify-honeypot="site-web">
  <input type="hidden" name="form-name" value="contact">
  <p class="hp"><label>Ne pas remplir : <input name="site-web"></label></p>
  <label for="c-nom">Votre nom</label><input id="c-nom" name="nom" autocomplete="name">
  <label for="c-mail">Votre e-mail</label><input id="c-mail" name="email" type="email" autocomplete="email" required>
  <label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required></textarea>
  <button class="btn" type="submit">Envoyer</button>
</form>
<p class="small">Votre e-mail sert uniquement à vous répondre.</p></section>"""
    urls.append(page("contact", "Contact | Escale", "Contacter l'équipe Escale : question, erreur, destination à ajouter.", hero, body))
    page("contact/merci", "Message envoyé | Escale", "Merci pour votre message.", "<h1>Message envoyé</h1>",
         '<section><p>Merci, votre message est bien arrivé. Nous vous répondrons par e-mail.</p><p><a class="btn" href="/">Retour à la recherche</a></p></section>')
    return urls

def main():
    urls = [f"{DOMAIN}/"]
    urls += [route_page(r) for r in ROUTES]
    urls += [hotel_page(h) for h in HOTELS]
    airports = {a[0]: a for a in __import__("json").loads((SITE / "data" / "airports.json").read_text(encoding="utf-8"))}
    ctx = dict(domain=DOMAIN, tp=TRAVELPAYOUTS, routes=ROUTES, hotels=HOTELS, route_slug=route_slug, hotel_slug=hotel_slug,
               airports=airports, related=related)
    i18n_urls, route_paths, hotel_paths = build_i18n.build(SITE, ctx)
    urls += i18n_urls + build_i18n.build_indexes(SITE, ctx, route_paths, hotel_paths) + build_i18n.build_deals(SITE, ctx)
    urls += legal_pages()

    # Liste des guides sur la page d'accueil
    idx = SITE / "index.html"
    s = idx.read_text(encoding="utf-8")
    s = s.replace(DEFAULT_DOMAIN, DOMAIN)
    def group(title, items):
        return f'<h3 class="sub-h">{title}</h3><ul class="route-links">' + "".join(items) + "</ul>"
    by_origin = {}
    for r in ROUTES:
        by_origin.setdefault(r[2], []).append(f'<li><a href="/{route_slug(r)}/">Vol {E(r[2])} → {E(r[3])}</a></li>')
    links = "".join(group(f"Vols au départ de {E(o)}", items) for o, items in by_origin.items())
    links += group("Hôtels pas chers", [f'<li><a href="/{hotel_slug(h)}/">Hôtel pas cher à {E(h[0])}</a></li>' for h in HOTELS])
    links += '<p class="lead guides-langs">Guides in English, en español, em português, بالعربية : ' + " · ".join(
        f'<a href="/{l}/" hreflang="{l}" lang="{l}">{build_i18n.NAMES[l]}</a>' for l in build_i18n.LANGS) + "</p>"
    s = re.sub(r"<!-- TRAVELPAYOUTS:START -->.*?<!-- TRAVELPAYOUTS:END -->",
               lambda m: "<!-- TRAVELPAYOUTS:START -->\n" + TRAVELPAYOUTS + "\n<!-- TRAVELPAYOUTS:END -->", s, flags=re.S)
    s = re.sub(r"<!-- ROUTES:START -->.*?<!-- ROUTES:END -->",
               lambda m: "<!-- ROUTES:START -->\n    " + links + "\n    <!-- ROUTES:END -->", s, flags=re.S)
    idx.write_text(s, encoding="utf-8")

    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    print(f"{len(urls)} pages dans le sitemap")

if __name__ == "__main__":
    main()
