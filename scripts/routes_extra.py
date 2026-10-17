"""Lignes supplémentaires générées automatiquement (pages trajets dans les 5 langues).

Les durées sont ESTIMÉES d'après la distance entre les aéroports (préfixe « ~ ») : on ne prétend pas qu'un vol direct existe.
Saisons chères et conseils : génériques par grande région, traduits dans translations.py via les fonctions ci-dessous.
"""
import math

# Villes : code -> (nom français, pays en français, (en, es, pt, ar))
CITIES = {
    "TLS": ("Toulouse", "France", ("Toulouse", "Toulouse", "Toulouse", "تولوز")),
    "NCE": ("Nice", "France", ("Nice", "Niza", "Nice", "نيس")),
    "BOD": ("Bordeaux", "France", ("Bordeaux", "Burdeos", "Bordéus", "بوردو")),
    "LIL": ("Lille", "France", ("Lille", "Lille", "Lille", "ليل")),
    "NTE": ("Nantes", "France", ("Nantes", "Nantes", "Nantes", "نانت")),
    "LHR": ("Londres", "Royaume-Uni", ("London", "Londres", "Londres", "لندن")),
    "JFK": ("New York", "États-Unis", ("New York", "Nueva York", "Nova Iorque", "نيويورك")),
    "YUL": ("Montréal", "Canada", ("Montreal", "Montreal", "Montreal", "مونتريال")),
    "MAD": ("Madrid", "Espagne", ("Madrid", "Madrid", "Madrid", "مدريد")),
    "LIS": ("Lisbonne", "Portugal", ("Lisbon", "Lisboa", "Lisboa", "لشبونة")),
    "BZV": ("Brazzaville", "Congo", ("Brazzaville", "Brazzaville", "Brazzaville", "برازافيل")),
    "PNR": ("Pointe-Noire", "Congo", ("Pointe-Noire", "Pointe-Noire", "Pointe-Noire", "بوانت نوار")),
    "ACC": ("Accra", "Ghana", ("Accra", "Acra", "Acra", "أكرا")),
    "LOS": ("Lagos", "Nigeria", ("Lagos", "Lagos", "Lagos", "لاغوس")),
    "ABV": ("Abuja", "Nigeria", ("Abuja", "Abuya", "Abuja", "أبوجا")),
    "BJL": ("Banjul", "Gambie", ("Banjul", "Banjul", "Banjul", "بانجول")),
    "OXB": ("Bissau", "Guinée-Bissau", ("Bissau", "Bisáu", "Bissau", "بيساو")),
    "RAI": ("Praia", "Cap-Vert", ("Praia", "Praia", "Praia", "برايا")),
    "NDJ": ("N’Djamena", "Tchad", ("N'Djamena", "Yamena", "N'Djamena", "إنجامينا")),
    "ADD": ("Addis-Abeba", "Éthiopie", ("Addis Ababa", "Adís Abeba", "Adis Abeba", "أديس أبابا")),
    "NBO": ("Nairobi", "Kenya", ("Nairobi", "Nairobi", "Nairóbi", "نيروبي")),
    "JNB": ("Johannesburg", "Afrique du Sud", ("Johannesburg", "Johannesburgo", "Joanesburgo", "جوهانسبرغ")),
    "TNR": ("Antananarivo", "Madagascar", ("Antananarivo", "Antananarivo", "Antananarivo", "أنتاناناريفو")),
    "MRU": ("Maurice", "Maurice", ("Mauritius", "Mauricio", "Maurícia", "موريشيوس")),
    "LAD": ("Luanda", "Angola", ("Luanda", "Luanda", "Luanda", "لواندا")),
    "MPM": ("Maputo", "Mozambique", ("Maputo", "Maputo", "Maputo", "مابوتو")),
    "KGL": ("Kigali", "Rwanda", ("Kigali", "Kigali", "Kigali", "كيغالي")),
    "DAR": ("Dar es Salaam", "Tanzanie", ("Dar es Salaam", "Dar es-Salam", "Dar es Salaam", "دار السلام")),
    "CAI": ("Le Caire", "Égypte", ("Cairo", "El Cairo", "Cairo", "القاهرة")),
    "RBA": ("Rabat", "Maroc", ("Rabat", "Rabat", "Rabat", "الرباط")),
    "TNG": ("Tanger", "Maroc", ("Tangier", "Tánger", "Tânger", "طنجة")),
    "FEZ": ("Fès", "Maroc", ("Fez", "Fez", "Fez", "فاس")),
    "AGA": ("Agadir", "Maroc", ("Agadir", "Agadir", "Agadir", "أكادير")),
    "OUD": ("Oujda", "Maroc", ("Oujda", "Uchda", "Oujda", "وجدة")),
    "ORN": ("Oran", "Algérie", ("Oran", "Orán", "Orão", "وهران")),
    "CZL": ("Constantine", "Algérie", ("Constantine", "Constantina", "Constantina", "قسنطينة")),
    "DJE": ("Djerba", "Tunisie", ("Djerba", "Yerba", "Djerba", "جربة")),
    "MIR": ("Monastir", "Tunisie", ("Monastir", "Monastir", "Monastir", "المنستير")),
    "DOH": ("Doha", "Qatar", ("Doha", "Doha", "Doha", "الدوحة")),
    "MED": ("Médine", "Arabie saoudite", ("Medina", "Medina", "Medina", "المدينة المنورة")),
    "RUH": ("Riyad", "Arabie saoudite", ("Riyadh", "Riad", "Riade", "الرياض")),
    "BEY": ("Beyrouth", "Liban", ("Beirut", "Beirut", "Beirute", "بيروت")),
    "AMM": ("Amman", "Jordanie", ("Amman", "Amán", "Amã", "عمّان")),
    "FDF": ("Fort-de-France", "Martinique", ("Fort-de-France", "Fort-de-France", "Fort-de-France", "فور دو فرانس")),
    "CAY": ("Cayenne", "Guyane", ("Cayenne", "Cayena", "Caiena", "كايين")),
    "DZA": ("Mayotte", "Mayotte", ("Mayotte", "Mayotte", "Maiote", "مايوت")),
    "PAP": ("Port-au-Prince", "Haïti", ("Port-au-Prince", "Puerto Príncipe", "Porto Príncipe", "بور أو برنس")),
    "FIH": ("Kinshasa", "RD Congo", None), "DSS": ("Dakar", "Sénégal", None), "ABJ": ("Abidjan", "Côte d'Ivoire", None),
    "BKO": ("Bamako", "Mali", None), "CKY": ("Conakry", "Guinée", None), "DLA": ("Douala", "Cameroun", None),
    "NSI": ("Yaoundé", "Cameroun", None), "LFW": ("Lomé", "Togo", None), "COO": ("Cotonou", "Bénin", None),
    "OUA": ("Ouagadougou", "Burkina Faso", None), "NIM": ("Niamey", "Niger", None), "LBV": ("Libreville", "Gabon", None),
    "NKC": ("Nouakchott", "Mauritanie", None), "CMN": ("Casablanca", "Maroc", None), "RAK": ("Marrakech", "Maroc", None),
    "ALG": ("Alger", "Algérie", None), "TUN": ("Tunis", "Tunisie", None), "DXB": ("Dubaï", "Émirats arabes unis", None),
    "JED": ("Djeddah", "Arabie saoudite", None), "IST": ("Istanbul", "Turquie", None), "RUN": ("La Réunion", "La Réunion", None),
    "PTP": ("Pointe-à-Pitre", "Guadeloupe", None), "CDG": ("Paris", "France", None), "BRU": ("Bruxelles", "Belgique", None),
    "LYS": ("Lyon", "France", None), "MRS": ("Marseille", "France", None), "GVA": ("Genève", "Suisse", None),
}

COUNTRIES = {
    "Royaume-Uni": ("United Kingdom", "Reino Unido", "Reino Unido", "المملكة المتحدة"),
    "États-Unis": ("United States", "Estados Unidos", "Estados Unidos", "الولايات المتحدة"),
    "Espagne": ("Spain", "España", "Espanha", "إسبانيا"),
    "Portugal": ("Portugal", "Portugal", "Portugal", "البرتغال"),
    "Belgique": ("Belgium", "Bélgica", "Bélgica", "بلجيكا"),
    "Suisse": ("Switzerland", "Suiza", "Suíça", "سويسرا"),
    "Congo": ("Republic of the Congo", "República del Congo", "República do Congo", "جمهورية الكونغو"),
    "Ghana": ("Ghana", "Ghana", "Gana", "غانا"),
    "Nigeria": ("Nigeria", "Nigeria", "Nigéria", "نيجيريا"),
    "Gambie": ("Gambia", "Gambia", "Gâmbia", "غامبيا"),
    "Guinée-Bissau": ("Guinea-Bissau", "Guinea-Bisáu", "Guiné-Bissau", "غينيا بيساو"),
    "Cap-Vert": ("Cape Verde", "Cabo Verde", "Cabo Verde", "الرأس الأخضر"),
    "Tchad": ("Chad", "Chad", "Chade", "تشاد"),
    "Éthiopie": ("Ethiopia", "Etiopía", "Etiópia", "إثيوبيا"),
    "Kenya": ("Kenya", "Kenia", "Quénia", "كينيا"),
    "Afrique du Sud": ("South Africa", "Sudáfrica", "África do Sul", "جنوب أفريقيا"),
    "Madagascar": ("Madagascar", "Madagascar", "Madagáscar", "مدغشقر"),
    "Maurice": ("Mauritius", "Mauricio", "Maurícia", "موريشيوس"),
    "Angola": ("Angola", "Angola", "Angola", "أنغولا"),
    "Mozambique": ("Mozambique", "Mozambique", "Moçambique", "موزمبيق"),
    "Rwanda": ("Rwanda", "Ruanda", "Ruanda", "رواندا"),
    "Tanzanie": ("Tanzania", "Tanzania", "Tanzânia", "تنزانيا"),
    "Égypte": ("Egypt", "Egipto", "Egito", "مصر"),
    "Qatar": ("Qatar", "Catar", "Catar", "قطر"),
    "Liban": ("Lebanon", "Líbano", "Líbano", "لبنان"),
    "Jordanie": ("Jordan", "Jordania", "Jordânia", "الأردن"),
    "Martinique": ("Martinique", "Martinica", "Martinica", "مارتينيك"),
    "Guyane": ("French Guiana", "Guayana Francesa", "Guiana Francesa", "غويانا الفرنسية"),
    "Mayotte": ("Mayotte", "Mayotte", "Maiote", "مايوت"),
    "Haïti": ("Haiti", "Haití", "Haiti", "هايتي"),
}

# Grande région par pays -> saison chère (clé existante de translations.PEAKS) et conseil générique
REGION = {}
for c in ["Sénégal", "Mali", "Guinée", "Niger", "Mauritanie", "Gambie", "Tchad"]:
    REGION[c] = "ouest_tabaski"
for c in ["Côte d'Ivoire", "Burkina Faso", "Togo", "Bénin", "Cameroun", "Gabon", "Congo", "RD Congo", "Ghana", "Nigeria",
          "Guinée-Bissau", "Cap-Vert"]:
    REGION[c] = "ouest"
for c in ["Éthiopie", "Kenya", "Afrique du Sud", "Madagascar", "Maurice", "Angola", "Mozambique", "Rwanda", "Tanzanie"]:
    REGION[c] = "est"
for c in ["Maroc", "Algérie", "Tunisie", "Égypte"]:
    REGION[c] = "maghreb"
for c in ["Qatar", "Liban", "Jordanie", "Turquie"]:
    REGION[c] = "moyen_orient"
REGION["Émirats arabes unis"] = "emirats"
REGION["Arabie saoudite"] = "saoudite"
for c in ["Guadeloupe", "Martinique", "Guyane", "Haïti"]:
    REGION[c] = "antilles"
for c in ["La Réunion", "Mayotte"]:
    REGION[c] = "ocean_indien"
for c in ["France", "Belgique", "Suisse", "Royaume-Uni", "Espagne", "Portugal", "Canada", "États-Unis"]:
    REGION[c] = "nord"

PEAK = {
    "ouest_tabaski": "juillet-août, les fêtes de fin d'année et la Tabaski",
    "ouest": "juillet-août et les fêtes de fin d'année",
    "est": "juillet-août et décembre-janvier",
    "maghreb": "juillet-août, l'Aïd et les vacances scolaires",
    "moyen_orient": "juillet-août et l'Aïd",
    "emirats": "de novembre à mars, quand il fait moins chaud",
    "saoudite": "le Ramadan, le Hajj et les vacances scolaires",
    "antilles": "juillet-août, Noël et le carnaval",
    "ocean_indien": "juillet-août et décembre-janvier",
    "nord": "juillet-août et les fêtes de fin d'année",
}

# Conseils génériques par région : (fr, en, es, pt, ar)
NOTE = {
    "afrique": (
        "Comparez les vols directs et avec escale : sur cette ligne, une escale bien placée fait souvent baisser le prix. Vérifiez aussi la franchise bagage, souvent décisive pour les voyages en famille.",
        "Compare direct flights and flights with a stop: on this route, a well-placed connection often lowers the price. Also check the baggage allowance, often decisive for family trips.",
        "Compara vuelos directos y con escala: en esta ruta, una buena escala suele bajar el precio. Revisa también el equipaje permitido, a menudo decisivo en viajes en familia.",
        "Compare voos diretos e com escala: nesta rota, uma boa escala costuma baixar o preço. Verifique também a franquia de bagagem, muitas vezes decisiva em viagens em família.",
        "قارن بين الرحلات المباشرة والرحلات مع توقف: على هذا الخط، التوقف المناسب يخفض السعر غالبًا. تحقّق أيضًا من وزن الأمتعة المسموح، فهو حاسم غالبًا في السفر العائلي."),
    "maghreb": (
        "Les prix grimpent vite en été et pendant l'Aïd : réservez tôt et comparez les aéroports proches, souvent desservis par des compagnies low-cost.",
        "Prices climb fast in summer and around Eid: book early and compare nearby airports, often served by low-cost airlines.",
        "Los precios suben rápido en verano y durante el Eid: reserva pronto y compara aeropuertos cercanos, a menudo con aerolíneas de bajo coste.",
        "Os preços sobem depressa no verão e durante o Eid: reserve cedo e compare aeroportos próximos, muitas vezes servidos por companhias low-cost.",
        "ترتفع الأسعار بسرعة في الصيف وخلال العيد: احجز مبكرًا وقارن المطارات القريبة، التي تخدمها غالبًا شركات منخفضة التكلفة."),
    "moyen_orient": (
        "Comparez les compagnies du Golfe et les vols avec escale : les écarts de prix selon le jour de départ sont fréquents.",
        "Compare Gulf airlines and flights with a stop: price gaps depending on the departure day are common.",
        "Compara las aerolíneas del Golfo y los vuelos con escala: las diferencias de precio según el día de salida son frecuentes.",
        "Compare as companhias do Golfo e os voos com escala: as diferenças de preço conforme o dia de partida são frequentes.",
        "قارن بين شركات الخليج والرحلات مع توقف: فروق الأسعار حسب يوم المغادرة شائعة."),
    "outremer": (
        "Comparez les dates à quelques jours près et les aéroports de départ : les écarts sont importants pendant les vacances scolaires.",
        "Compare dates a few days apart and departure airports: gaps are large during school holidays.",
        "Compara fechas con unos días de diferencia y los aeropuertos de salida: las diferencias son grandes en vacaciones escolares.",
        "Compare datas com alguns dias de diferença e os aeroportos de partida: as diferenças são grandes nas férias escolares.",
        "قارن التواريخ بفارق أيام قليلة ومطارات المغادرة: الفروق كبيرة خلال العطل المدرسية."),
}
NOTE_OF_REGION = {"ouest_tabaski": "afrique", "ouest": "afrique", "est": "afrique", "maghreb": "maghreb", "moyen_orient": "moyen_orient",
                  "emirats": "moyen_orient", "saoudite": "moyen_orient", "antilles": "outremer", "ocean_indien": "outremer", "nord": "afrique"}

PAIRS = {
    "CDG": "BZV ACC LOS BJL OXB RAI NDJ PNR ADD NBO JNB TNR MRU LAD MPM KGL DAR CAI RBA TNG FEZ AGA OUD ORN CZL DJE MIR DOH MED RUH BEY AMM FDF CAY DZA PAP",
    "BRU": "CMN RAK TNG ALG TUN KGL LFW COO CKY BKO OUA ACC LBV NSI DXB IST",
    "LYS": "ALG TUN ORN CZL RAK AGA OUD FEZ ABJ BKO DJE IST DXB",
    "MRS": "ORN CZL CMN RAK ABJ BKO DJE MIR IST",
    "GVA": "ALG TUN RAK ABJ IST DXB",
    "TLS": "ALG ORN CMN RAK TUN",
    "NCE": "ALG TUN CMN DSS",
    "BOD": "ALG CMN RAK DSS",
    "LIL": "ALG ORN CMN RAK OUD TUN DSS",
    "NTE": "ALG ORN CMN RAK AGA TUN DSS",
    "LHR": "LOS ACC ABV NBO JNB ADD CAI DXB CMN RAK ALG DSS ABJ FIH",
    "JFK": "DSS ACC LOS ADD CMN ABJ CAI PAP",
    "YUL": "DSS ABJ CMN ALG TUN PAP DLA CKY",
    "MAD": "DSS CMN RAK TNG ALG ABJ BKO LOS",
    "LIS": "LAD MPM RAI OXB DSS CMN ABJ ACC",
}


def _duration(a, b):
    """Durée de vol estimée sans escale : distance / 800 km/h + 30 min, arrondie au quart d'heure."""
    r = math.pi / 180
    h = math.sin((b[5] - a[5]) * r / 2) ** 2 + math.cos(a[5] * r) * math.cos(b[5] * r) * math.sin((b[6] - a[6]) * r / 2) ** 2
    km = 12742 * math.asin(math.sqrt(h))
    minutes = round((km / 800 + 0.5) * 60 / 15) * 15
    hh, mm = divmod(minutes, 60)
    return (f"~{hh} h {mm:02d}" if mm else f"~{hh} h"), int(round(km, -1))


def extend(routes, translations, airports):
    """Ajoute les nouvelles lignes à ROUTES et complète les traductions. Ignore les paires de villes déjà présentes."""
    TR = translations
    for code, (fr, country, tr) in CITIES.items():
        if tr and fr not in TR.CITIES:
            TR.CITIES[fr] = tr
    for k, v in COUNTRIES.items():
        TR.COUNTRIES.setdefault(k, v)
    existing = {(r[2], r[3]) for r in routes}
    distances = {}
    added = []
    for orig, dests in PAIRS.items():
        for dest in dests.split():
            o, d = CITIES[orig], CITIES[dest]
            if (o[0], d[0]) in existing or orig == dest or orig not in airports or dest not in airports:
                continue
            region = REGION.get(d[1], "afrique")
            dur, km = _duration(airports[orig], airports[dest])
            note = NOTE[NOTE_OF_REGION.get(region, "afrique")]
            route = (orig, dest, o[0], d[0], d[1], airports[dest][2], dur, PEAK[region], note[0])
            TR.NOTES[f"{orig}-{dest}"] = note[1:]
            distances[(orig, dest)] = km
            existing.add((o[0], d[0]))
            added.append(route)
    routes.extend(added)
    return added, distances
