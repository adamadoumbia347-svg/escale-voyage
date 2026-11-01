"""Outil « Visa selon mon passeport » (/visa/ en français, /en/visa/ en anglais).

Résumé PRUDENT pour un court séjour touristique, vérifié en novembre 2026. Les règles changent souvent et dépendent de la
situation de chacun : quand ce n'est pas clair et stable, le statut est « à vérifier ». Chaque résultat renvoie vers la
source officielle du pays de destination ou vers l'IATA Travel Centre (référence utilisée par les compagnies aériennes).
Statuts : 0 sans visa · 1 autorisation / visa électronique ou à l'arrivée · 2 visa à demander avant le départ · 9 à vérifier.
Pour mettre à jour : modifier RULES / EXCEPT ci-dessous et la date CHECKED.
"""
import html
import json

import build_i18n as B

E = html.escape
CHECKED = {"fr": "novembre 2026", "en": "November 2026"}

# Passeports : code -> (fr, en, drapeau)
PASS = {
    "CI": ("Côte d'Ivoire", "Côte d'Ivoire", "🇨🇮"), "SN": ("Sénégal", "Senegal", "🇸🇳"), "ML": ("Mali", "Mali", "🇲🇱"),
    "GN": ("Guinée", "Guinea", "🇬🇳"), "BF": ("Burkina Faso", "Burkina Faso", "🇧🇫"), "TG": ("Togo", "Togo", "🇹🇬"),
    "BJ": ("Bénin", "Benin", "🇧🇯"), "NE": ("Niger", "Niger", "🇳🇪"), "CM": ("Cameroun", "Cameroon", "🇨🇲"),
    "GA": ("Gabon", "Gabon", "🇬🇦"), "CG": ("Congo", "Republic of the Congo", "🇨🇬"), "CD": ("RD Congo", "DR Congo", "🇨🇩"),
    "NG": ("Nigeria", "Nigeria", "🇳🇬"), "GH": ("Ghana", "Ghana", "🇬🇭"), "MA": ("Maroc", "Morocco", "🇲🇦"),
    "DZ": ("Algérie", "Algeria", "🇩🇿"), "TN": ("Tunisie", "Tunisia", "🇹🇳"),
    "FR": ("France", "France", "🇫🇷"), "BE": ("Belgique", "Belgium", "🇧🇪"), "IT": ("Italie", "Italy", "🇮🇹"), "DE": ("Allemagne", "Germany", "🇩🇪"),
    "NL": ("Pays-Bas", "Netherlands", "🇳🇱"), "GB": ("Royaume-Uni", "United Kingdom", "🇬🇧"), "US": ("États-Unis", "United States", "🇺🇸"),
    "CA": ("Canada", "Canada", "🇨🇦"),
}
EU = ["FR", "BE", "IT", "DE", "NL"]
WEST = EU + ["GB", "US", "CA"]
ECOWAS = ["CI", "SN", "ML", "GN", "BF", "TG", "BJ", "NE", "NG", "GH"]  # libre circulation CEDEAO (Mali, Burkina, Niger : AES, accord maintenu)
CEMAC = ["CM", "GA", "CG"]
AFR = [p for p in PASS if p not in WEST]
IATA = "https://www.iatatravelcentre.com/"

# Destinations : code -> (fr, en, drapeau, lien officiel)
DEST = {
    "SCH": ("France et espace Schengen", "France and the Schengen area", "🇪🇺", "https://france-visas.gouv.fr/"),
    "GB": ("Royaume-Uni", "United Kingdom", "🇬🇧", "https://www.gov.uk/check-uk-visa"),
    "US": ("États-Unis", "United States", "🇺🇸", "https://travel.state.gov/content/travel/en/us-visas.html"),
    "CA": ("Canada", "Canada", "🇨🇦", "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html"),
    "AE": ("Émirats (Dubaï)", "UAE (Dubai)", "🇦🇪", "https://u.ae/en/information-and-services/visa-and-emirates-id"),
    "TR": ("Turquie", "Turkey", "🇹🇷", "https://www.evisa.gov.tr/"),
    "MA": ("Maroc", "Morocco", "🇲🇦", IATA), "TN": ("Tunisie", "Tunisia", "🇹🇳", IATA), "DZ": ("Algérie", "Algeria", "🇩🇿", IATA),
    "EG": ("Égypte", "Egypt", "🇪🇬", "https://visa2egypt.gov.eg/"),
    "SN": ("Sénégal", "Senegal", "🇸🇳", IATA), "CI": ("Côte d'Ivoire", "Côte d'Ivoire", "🇨🇮", "https://www.snedai.com/"),
    "ML": ("Mali", "Mali", "🇲🇱", IATA), "GN": ("Guinée", "Guinea", "🇬🇳", IATA), "BF": ("Burkina Faso", "Burkina Faso", "🇧🇫", IATA),
    "TG": ("Togo", "Togo", "🇹🇬", IATA), "BJ": ("Bénin", "Benin", "🇧🇯", IATA), "CM": ("Cameroun", "Cameroon", "🇨🇲", IATA),
    "GA": ("Gabon", "Gabon", "🇬🇦", IATA), "CD": ("RD Congo", "DR Congo", "🇨🇩", IATA), "NG": ("Nigeria", "Nigeria", "🇳🇬", IATA),
    "GH": ("Ghana", "Ghana", "🇬🇭", IATA), "KE": ("Kenya", "Kenya", "🇰🇪", "https://www.etakenya.go.ke/"), "ET": ("Éthiopie", "Ethiopia", "🇪🇹", IATA),
    "RW": ("Rwanda", "Rwanda", "🇷🇼", IATA), "ZA": ("Afrique du Sud", "South Africa", "🇿🇦", IATA),
}


def rules():
    R = {}
    def put(dest, passports, st):
        for p in passports:
            R[f"{p}-{dest}"] = st
    # Europe, Amérique du Nord, Golfe
    put("SCH", AFR, 2); put("SCH", WEST, 0)
    put("GB", AFR, 2); put("GB", EU + ["US", "CA"], 1); put("GB", ["GB"], 0)
    put("US", AFR, 2); put("US", EU + ["GB"], 1); put("US", ["US", "CA"], 0)
    put("CA", AFR, 2); put("CA", ["MA"], 9); put("CA", EU + ["GB"], 1); put("CA", ["US", "CA"], 0)
    put("AE", AFR, 2); put("AE", WEST, 0)
    put("TR", AFR, 9); put("TR", ["MA", "TN"], 0); put("TR", EU + ["GB"], 0); put("TR", ["US", "CA"], 9)
    # Maghreb et Égypte
    put("MA", AFR, 9); put("MA", WEST + ["TN", "DZ", "SN", "CI", "ML", "GN", "NE", "CG", "GA", "MA"], 0)
    put("TN", AFR, 9); put("TN", WEST + ["MA", "DZ", "SN", "CI", "ML", "TN"], 0)
    put("DZ", AFR, 9); put("DZ", WEST, 2); put("DZ", ["MA"], 2); put("DZ", ["TN", "DZ"], 0)
    put("EG", AFR, 9); put("EG", WEST, 1)
    # Afrique de l'Ouest (CEDEAO) et centrale (CEMAC)
    west = {"SN": 0, "CI": 1, "ML": 2, "GN": 1, "BF": 2, "TG": 1, "BJ": 1, "NG": 2, "GH": 2}
    for d, w in west.items():
        put(d, AFR, 9); put(d, ECOWAS, 0); put(d, WEST, w)
    put("SN", ["MA"], 0); put("CI", ["MA"], 0); put("ML", ["MA"], 0)
    for d, w in {"CM": 2, "GA": 1, "CD": 2}.items():
        put(d, AFR, 9); put(d, WEST, w)
    put("CM", CEMAC, 0); put("GA", CEMAC, 0); put("CD", ["CD"], 0)
    # Afrique de l'Est et du Sud
    put("KE", AFR, 9); put("KE", WEST, 1)
    put("ET", AFR, 9); put("ET", WEST, 1)
    put("RW", AFR, 0); put("RW", WEST, 1)
    put("ZA", AFR, 9); put("ZA", ["NG", "CM", "CD"], 2); put("ZA", WEST, 0)
    # Son propre pays : pas de visa
    for p in PASS:
        if p in DEST:
            R[f"{p}-{p}"] = 0
    return R


NOTES = {
    "fr": {"SCH-W": "Pour les voyageurs exemptés de visa, l'autorisation en ligne ETIAS est prévue pour l'espace Schengen : vérifiez si elle est déjà en vigueur.",
           "GB-1": "Autorisation électronique ETA à demander en ligne avant le départ.",
           "US-1": "Autorisation électronique ESTA à demander en ligne avant le départ.",
           "CA-1": "Autorisation électronique eTA à demander en ligne avant le départ.",
           "CA-MA": "Visa en général ; une eTA est possible sous conditions (visa canadien récent ou visa américain valide).",
           "ECOWAS": "Libre circulation CEDEAO : carte d'identité ou passeport valide, sans visa pour un court séjour.",
           "CEMAC": "Libre circulation CEMAC : sans visa pour un court séjour."},
    "en": {"SCH-W": "For visa-exempt travellers, the ETIAS online authorisation is planned for the Schengen area: check whether it is already in force.",
           "GB-1": "Electronic Travel Authorisation (ETA) to apply for online before you travel.",
           "US-1": "ESTA electronic authorisation to apply for online before you travel.",
           "CA-1": "eTA electronic authorisation to apply for online before you travel.",
           "CA-MA": "Usually a visa; an eTA may be possible under conditions (recent Canadian visa or valid US visa).",
           "ECOWAS": "ECOWAS free movement: valid ID card or passport, no visa for a short stay.",
           "CEMAC": "CEMAC free movement: no visa for a short stay."},
}

T = {
    "fr": dict(path="visa", title="Visa selon mon passeport : faut-il un visa ? | Escale",
               desc="Faut-il un visa pour la France, Dubaï, le Canada, le Maroc ou le Sénégal ? Choisissez votre passeport : réponse par destination et lien officiel.",
               h1="Faut-il un visa <span>avec mon passeport ?</span>",
               lead="Choisissez votre passeport et votre destination : vous voyez s'il faut un visa pour un court séjour touristique, et où le demander.",
               p="Mon passeport", d="Ma destination", all="Toutes les destinations pour ce passeport", official="Vérifier sur le site officiel",
               st={0: "Sans visa", 1: "Visa ou autorisation en ligne", 2: "Visa avant le départ", 9: "À vérifier"},
               sl={0: "Pas de visa pour un court séjour touristique.", 1: "Autorisation ou visa électronique à demander en ligne avant le départ (ou visa à l'arrivée selon le pays).",
                   2: "Visa à demander à l'ambassade ou en ligne avant le départ : prévoyez plusieurs semaines.", 9: "Les règles varient selon votre situation ou ont changé récemment : vérifiez avant de réserver."},
               warn="Résumé indicatif pour un court séjour touristique, vérifié en {c}. Les règles changent et dépendent de votre situation (motif du voyage, durée, titre de séjour…) : vérifiez toujours sur le site officiel ou l'IATA Travel Centre avant de réserver. Pensez aussi au passeport valable 6 mois et au carnet de vaccination (fièvre jaune).",
               cta="Comparer les vols", faq=[("Le résultat vaut-il pour un titre de séjour ?", "Non. Un titre de séjour ou un visa d'un autre pays peut changer les règles (par exemple un titre de séjour européen pour certains pays). Vérifiez sur le site officiel."),
                                              ("D'où viennent ces informations ?", "D'un résumé fait par Escale à partir des règles publiques, vérifié en {c}. Escale ne délivre pas de visa : seule la source officielle fait foi.")]),
    "en": dict(path="en/visa", title="Visa by passport: do I need a visa? | Escale",
               desc="Do you need a visa for the UK, Schengen, Dubai, Canada, Morocco or Ghana? Pick your passport: answer by destination with the official link.",
               h1="Do I need a visa <span>with my passport?</span>",
               lead="Pick your passport and your destination: see whether you need a visa for a short tourist stay, and where to apply.",
               p="My passport", d="My destination", all="All destinations for this passport", official="Check on the official website",
               st={0: "No visa", 1: "Online visa or authorisation", 2: "Visa before departure", 9: "Check"},
               sl={0: "No visa for a short tourist stay.", 1: "Electronic authorisation or e-visa to apply for online before you travel (or visa on arrival, depending on the country).",
                   2: "Visa to apply for at the embassy or online before departure: allow several weeks.", 9: "Rules depend on your situation or changed recently: check before you book."},
               warn="A guide for short tourist stays, checked in {c}. Rules change and depend on your situation (purpose, length of stay, residence permit…): always check the official website or the IATA Travel Centre before booking. Remember a passport valid for 6 months and your vaccination card (yellow fever).",
               cta="Compare flights", faq=[("Does the result apply if I hold a residence permit?", "No. A residence permit or a visa from another country can change the rules. Check the official website."),
                                         ("Where does this information come from?", "From a summary made by Escale from public rules, checked in {c}. Escale does not issue visas: only the official source is authoritative.")]),
}


def build(site, ctx):
    R = rules()
    urls = []
    paths = {"fr": T["fr"]["path"], "en": T["en"]["path"]}
    for lang, t in T.items():
        col = 0 if lang == "fr" else 1
        data = {"p": {k: [v[col], v[2]] for k, v in PASS.items()}, "d": {k: [v[col], v[2], v[3]] for k, v in DEST.items()}, "r": R,
                "st": t["st"], "sl": t["sl"], "n": NOTES[lang], "eu": EU, "west": WEST, "ecowas": ECOWAS, "cemac": CEMAC,
                "official": t["official"], "cta": t["cta"], "lang": lang}
        popt = "".join(f'<option value="{k}">{v[2]} {E(v[col])}</option>' for k, v in sorted(PASS.items(), key=lambda kv: kv[1][col]))
        dopt = "".join(f'<option value="{k}">{v[2]} {E(v[col])}</option>' for k, v in DEST.items())
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        body = (f'<section class="visa-tool"><div class="visa-form"><label><span>{E(t["p"])}</span><select id="visa-p">{popt}</select></label>'
                f'<label><span>{E(t["d"])}</span><select id="visa-d">{dopt}</select></label></div>'
                f'<div id="visa-res" class="visa-res" aria-live="polite"></div>'
                f'<h2>{E(t["all"])}</h2><ul id="visa-all" class="visa-all"></ul>'
                f'<p class="small visa-warn">⚠️ {E(t["warn"].format(c=CHECKED[lang]))}</p></section>'
                f'<script type="application/json" id="visa-data">{json.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script>'
                f'<script src="/visa.js" defer></script>'
                f'<section class="faq"><h2>{"Questions fréquentes" if lang == "fr" else "Frequently asked questions"}</h2>' +
                "".join(f"<details><summary>{E(q)}</summary><p>{E(a.format(c=CHECKED[lang]))}</p></details>" for q, a in t["faq"]) + "</section>")
        faq = [(q, a.format(c=CHECKED[lang])) for q, a in t["faq"]]
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, B.faq_ld(faq), paths, ctx))
    return urls
