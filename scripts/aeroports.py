"""Guides « Arriver à l'aéroport de … » (français et anglais) pour les grandes villes d'Afrique et du Maghreb.

Informations générales et prudentes, vérifiées en novembre 2026 : moyens de transport vers la ville, cartes SIM, argent,
pièges courants. Pas de prix de taxi chiffrés (ils changent vite) : on conseille de convenir du prix avant de monter.
Les services (applis de VTC, navettes, opérateurs) évoluent : chaque page invite à vérifier sur place.
"""
import html

import build_i18n as B

E = html.escape
TRANSFER = "https://kiwitaxi.tpm.lv/hWfXu1nw"
ESIM = "https://airalo.tpm.lv/FrG2grmd"
CHECKED = {"fr": "novembre 2026", "en": "November 2026"}

# code : (ville fr, ville en, slug fr, slug en, pays fr, pays en, aéroport, {fr: [...], en: [...]} conseils, monnaie fr, monnaie en, opérateurs)
A = {
    "ABJ": ("Abidjan", "Abidjan", "abidjan", "abidjan", "Côte d'Ivoire", "Côte d'Ivoire", "Aéroport Félix-Houphouët-Boigny", "Félix Houphouët-Boigny Airport",
            {"fr": ["L'aéroport est à Port-Bouët, au sud de la ville : comptez de 20 minutes à plus d'une heure pour le Plateau, Cocody ou Yopougon selon les bouchons (évitez si possible 7 h – 9 h et 17 h – 20 h).",
                    "Taxis : prenez un taxi à la station officielle de l'aéroport et convenez du prix avant de partir. Des applications de VTC (comme Yango ou Heetch) fonctionnent aussi à Abidjan.",
                    "Un proche vient vous chercher ? Donnez-lui votre numéro de vol pour suivre l'heure d'arrivée réelle."],
             "en": ["The airport is in Port-Bouët, south of the city: allow 20 minutes to over an hour to the Plateau, Cocody or Yopougon depending on traffic (avoid 7–9 am and 5–8 pm if you can).",
                    "Taxis: take one from the official airport rank and agree the price before you leave. Ride-hailing apps (such as Yango or Heetch) also work in Abidjan.",
                    "Someone picking you up? Give them your flight number so they can follow the real arrival time."]},
            "franc CFA (XOF)", "CFA franc (XOF)", "Orange, MTN, Moov Africa"),
    "DSS": ("Dakar", "Dakar", "dakar", "dakar", "Sénégal", "Senegal", "Aéroport international Blaise-Diagne (AIBD)", "Blaise Diagne International Airport (AIBD)",
            {"fr": ["L'aéroport Blaise-Diagne est à Diass, à environ 45 km de Dakar : comptez 45 minutes à 1 h 30 selon l'heure et le quartier.",
                    "Pour rejoindre la ville : taxi de l'aéroport (prix à convenir avant de monter), bus express vers Dakar, ou transfert réservé à l'avance, pratique pour une arrivée de nuit. Vérifiez sur place si le train (TER) dessert déjà l'aéroport.",
                    "Les péages de l'autoroute sont en général à la charge du passager : demandez si le prix annoncé les inclut."],
             "en": ["Blaise Diagne Airport is in Diass, about 45 km from Dakar: allow 45 minutes to 1 h 30 depending on the time and neighbourhood.",
                    "To reach the city: airport taxi (agree the price before you get in), express bus to Dakar, or a transfer booked in advance, handy for night arrivals. Check locally whether the TER train already serves the airport.",
                    "Motorway tolls are usually paid by the passenger: ask whether the quoted price includes them."]},
            "franc CFA (XOF)", "CFA franc (XOF)", "Orange, Yas (ex-Free), Expresso"),
    "LOS": ("Lagos", "Lagos", "lagos", "lagos", "Nigeria", "Nigeria", "Aéroport international Murtala-Muhammed", "Murtala Muhammed International Airport",
            {"fr": ["L'aéroport est à Ikeja : comptez de 1 h à plus de 2 h pour Victoria Island ou Lekki aux heures de pointe.",
                    "Les applications Uber et Bolt fonctionnent à Lagos ; sinon, prenez un taxi agréé de l'aéroport. Ne suivez pas les personnes qui proposent un taxi dans le hall.",
                    "Changez seulement un petit montant à l'aéroport ; préférez les distributeurs ou les bureaux de change agréés en ville."],
             "en": ["The airport is in Ikeja: allow 1 to over 2 hours to Victoria Island or Lekki at rush hour.",
                    "Uber and Bolt work in Lagos; otherwise, use an approved airport taxi. Do not follow people offering rides inside the terminal.",
                    "Only change a small amount at the airport; use ATMs or licensed exchange offices in town."]},
            "naira (NGN)", "naira (NGN)", "MTN, Airtel, Glo"),
    "ACC": ("Accra", "Accra", "accra", "accra", "Ghana", "Ghana", "Aéroport international de Kotoka", "Kotoka International Airport",
            {"fr": ["L'aéroport est à une dizaine de kilomètres du centre : 20 à 45 minutes selon la circulation.",
                    "Uber et Bolt fonctionnent à Accra ; les taxis de l'aéroport sont aussi disponibles (prix à convenir avant).",
                    "Pour une carte SIM, prévoyez votre passeport : l'enregistrement est obligatoire."],
             "en": ["The airport is about 10 km from the centre: 20 to 45 minutes depending on traffic.",
                    "Uber and Bolt work in Accra; airport taxis are also available (agree the price first).",
                    "For a SIM card, bring your passport: registration is compulsory."]},
            "cedi (GHS)", "cedi (GHS)", "MTN, Telecel, AT"),
    "DLA": ("Douala", "Douala", "douala", "douala", "Cameroun", "Cameroon", "Aéroport international de Douala", "Douala International Airport",
            {"fr": ["L'aéroport est proche de la ville : 20 à 45 minutes pour Akwa ou Bonanjo selon la circulation.",
                    "Prenez un taxi à la sortie de l'aéroport en convenant du prix avant, ou faites-vous attendre par un proche ou un transfert réservé.",
                    "Gardez vos bagages près de vous dans le hall d'arrivée, très fréquenté."],
             "en": ["The airport is close to town: 20 to 45 minutes to Akwa or Bonanjo depending on traffic.",
                    "Take a taxi outside the airport and agree the price first, or have a relative or a pre-booked transfer meet you.",
                    "Keep your bags close in the busy arrivals hall."]},
            "franc CFA (XAF)", "CFA franc (XAF)", "MTN, Orange"),
    "CMN": ("Casablanca", "Casablanca", "casablanca", "casablanca", "Maroc", "Morocco", "Aéroport Mohammed-V", "Mohammed V Airport",
            {"fr": ["L'aéroport est à environ 30 km du centre. Un train relie l'aéroport aux gares de Casablanca : pratique et sans bouchons.",
                    "Les grands taxis blancs attendent à la sortie : mettez-vous d'accord sur le prix avant de partir.",
                    "Le dirham ne s'exporte pas : retirez ou changez sur place, et gardez vos reçus de change."],
             "en": ["The airport is about 30 km from the centre. A train links the airport with Casablanca's stations: easy and traffic-free.",
                    "White 'grand taxis' wait outside: agree the price before you leave.",
                    "The dirham cannot be taken out of the country: withdraw or change money there and keep your exchange receipts."]},
            "dirham (MAD)", "dirham (MAD)", "Maroc Telecom, Orange, inwi"),
    "FIH": ("Kinshasa", "Kinshasa", "kinshasa", "kinshasa", "RD Congo", "DR Congo", "Aéroport international de N'djili", "N'djili International Airport",
            {"fr": ["L'aéroport de N'djili est à environ 25 km de la Gombe : le trajet peut prendre plus d'une heure, surtout en fin de journée.",
                    "Faites-vous attendre par un proche, votre hôtel ou un transfert réservé à l'avance : c'est le plus simple et le plus sûr.",
                    "Le dollar américain est très utilisé à côté du franc congolais : prévoyez des petites coupures en bon état."],
             "en": ["N'djili Airport is about 25 km from Gombe: the drive can take over an hour, especially in the late afternoon.",
                    "Have a relative, your hotel or a pre-booked transfer meet you: it is the easiest and safest option.",
                    "US dollars are widely used alongside the Congolese franc: bring small notes in good condition."]},
            "franc congolais (CDF) et dollar", "Congolese franc (CDF) and US dollar", "Vodacom, Orange, Airtel, Africell"),
    "BKO": ("Bamako", "Bamako", "bamako", "bamako", "Mali", "Mali", "Aéroport international Modibo-Keïta", "Modibo Keïta International Airport",
            {"fr": ["L'aéroport est à une quinzaine de kilomètres au sud du centre : 30 à 45 minutes selon la circulation.",
                    "Prenez un taxi en convenant du prix avant, ou faites-vous attendre, surtout pour une arrivée de nuit.",
                    "Lisez les conseils aux voyageurs de votre pays avant le départ : la situation varie selon les régions."],
             "en": ["The airport is about 15 km south of the centre: 30 to 45 minutes depending on traffic.",
                    "Take a taxi after agreeing the price, or have someone meet you, especially at night.",
                    "Read your government's travel advice before you go: the situation varies by region."]},
            "franc CFA (XOF)", "CFA franc (XOF)", "Orange, Moov Africa"),
    "CKY": ("Conakry", "Conakry", "conakry", "conakry", "Guinée", "Guinea", "Aéroport international de Conakry-Gbessia", "Conakry Gbessia International Airport",
            {"fr": ["L'aéroport est dans la ville : comptez de 20 minutes à plus d'une heure pour Kaloum selon les bouchons.",
                    "Faites-vous attendre ou prenez un taxi en convenant du prix avant de monter.",
                    "Le franc guinéen se change surtout sur place ; prévoyez aussi quelques euros ou dollars en espèces."],
             "en": ["The airport is inside the city: allow 20 minutes to over an hour to Kaloum depending on traffic.",
                    "Have someone meet you or take a taxi after agreeing the price.",
                    "Guinean francs are mostly exchanged locally; bring some euros or dollars in cash too."]},
            "franc guinéen (GNF)", "Guinean franc (GNF)", "Orange, MTN"),
    "ALG": ("Alger", "Algiers", "alger", "algiers", "Algérie", "Algeria", "Aéroport Houari-Boumediene", "Houari Boumediene Airport",
            {"fr": ["L'aéroport est à environ 20 km à l'est du centre. Un train relie l'aéroport au centre d'Alger.",
                    "Les taxis attendent à la sortie : convenez du prix avant de partir.",
                    "Changez de l'argent uniquement dans les bureaux et banques agréés, et gardez vos reçus."],
             "en": ["The airport is about 20 km east of the centre. A train links the airport with central Algiers.",
                    "Taxis wait outside: agree the price before leaving.",
                    "Only change money at licensed offices and banks, and keep your receipts."]},
            "dinar algérien (DZD)", "Algerian dinar (DZD)", "Mobilis, Djezzy, Ooredoo"),
    "TUN": ("Tunis", "Tunis", "tunis", "tunis", "Tunisie", "Tunisia", "Aéroport de Tunis-Carthage", "Tunis-Carthage Airport",
            {"fr": ["L'aéroport est à environ 8 km du centre : 15 à 30 minutes en taxi.",
                    "Les taxis jaunes ont un compteur : demandez qu'il soit allumé. Des applications de VTC fonctionnent aussi à Tunis.",
                    "Le dinar ne s'exporte pas : changez seulement ce dont vous avez besoin et gardez vos reçus."],
             "en": ["The airport is about 8 km from the centre: 15 to 30 minutes by taxi.",
                    "Yellow taxis have meters: ask for it to be switched on. Ride-hailing apps also work in Tunis.",
                    "The dinar cannot be taken out of the country: change only what you need and keep your receipts."]},
            "dinar tunisien (TND)", "Tunisian dinar (TND)", "Ooredoo, Orange, Tunisie Telecom"),
    "LFW": ("Lomé", "Lomé", "lome", "lome", "Togo", "Togo", "Aéroport international Gnassingbé-Eyadéma", "Gnassingbé Eyadéma International Airport",
            {"fr": ["L'aéroport est tout proche du centre : 15 à 30 minutes.",
                    "Taxis et motos-taxis (zémidjans) sont partout ; avec des bagages, préférez un taxi et convenez du prix avant.",
                    "Des applications de VTC fonctionnent à Lomé : pratiques pour connaître le prix à l'avance."],
             "en": ["The airport is very close to the centre: 15 to 30 minutes.",
                    "Taxis and motorbike taxis (zémidjans) are everywhere; with luggage, take a taxi and agree the price first.",
                    "Ride-hailing apps work in Lomé: handy to know the price in advance."]},
            "franc CFA (XOF)", "CFA franc (XOF)", "Moov Africa, Togocom"),
}
T = {
    "fr": dict(path="arriver-aeroport-{s}", title="Arriver à l'aéroport {dc} : taxi, SIM, argent | Escale",
               desc="Arrivée à l'aéroport {dc} ({code}) : rejoindre la ville, taxi ou VTC, carte SIM, argent et pièges à éviter. Conseils pratiques vérifiés en {m}.",
               h1="Arriver à l'aéroport <span>{dc}</span>", lead="{ap} ({code}) : comment rejoindre la ville, avoir Internet et de l'argent dès l'arrivée, et les pièges à éviter.",
               city_h="Rejoindre la ville", sim_h="Téléphone et Internet", sim="Opérateurs : {ops}. Pour une carte SIM, prévoyez votre passeport (enregistrement obligatoire). Pour avoir Internet dès l'atterrissage, sans chercher de boutique, une eSIM s'installe avant le départ.",
               money_h="Argent", money="Monnaie : {cur}. Retirez au distributeur de l'aéroport ou en ville plutôt que de changer de grosses sommes à l'arrivée ; gardez de petites coupures pour le taxi.",
               traps_h="Pièges à éviter", traps=["Les personnes qui proposent de porter vos bagages ou un taxi dans le hall : refusez poliment et allez à la station officielle.", "Monter dans un taxi sans avoir convenu du prix.", "Sortir de grosses sommes en public : préparez l'argent du taxi avant de sortir."],
               book_h="À réserver avant de partir", transfer="Transfert aéroport réservé à l'avance (prix fixe) · Kiwitaxi", esim="Carte eSIM pour avoir Internet à l'arrivée · Airalo",
               flights="Vols pour {c} au meilleur prix", others="Autres guides d'arrivée", warn="Conseils généraux vérifiés en {m} : les services changent, vérifiez sur place."),
    "en": dict(path="en/arriving-at-{s}-airport", title="Arriving at {c} airport: taxi, SIM, money | Escale",
               desc="Arriving at {c} airport ({code}): getting into town, taxi or ride-hailing, SIM card, money and scams to avoid. Practical tips checked in {m}.",
               h1="Arriving at <span>{c} airport</span>", lead="{ap} ({code}): how to get into town, get online and get cash on arrival, and what to avoid.",
               city_h="Getting into town", sim_h="Phone and internet", sim="Operators: {ops}. For a SIM card, bring your passport (registration is compulsory). To be online as soon as you land without looking for a shop, an eSIM can be installed before you leave.",
               money_h="Money", money="Currency: {cur}. Withdraw at the airport ATM or in town rather than changing large sums on arrival; keep small notes for the taxi.",
               traps_h="Scams to avoid", traps=["People offering to carry your bags or find you a taxi inside the terminal: politely decline and go to the official rank.", "Getting into a taxi without agreeing the price.", "Taking out large sums in public: prepare your taxi money before you walk out."],
               book_h="Book before you go", transfer="Airport transfer booked in advance (fixed price) · Kiwitaxi", esim="eSIM to be online on arrival · Airalo",
               flights="Cheap flights to {c}", others="Other arrival guides", warn="General tips checked in {m}: services change, check locally."),
}


def de(c):
    return ("d'" if c[:1] in "AEIOUÉ" else "de ") + c


def path(code, lang):
    a = A[code]
    return T[lang]["path"].format(s=a[2] if lang == "fr" else a[3])


def build(site, ctx, hubs_paths=None):
    urls = []
    for code, a in A.items():
        paths = {l: path(code, l) for l in ("fr", "en")}
        for lang in ("fr", "en"):
            t = T[lang]
            c, ap, cur = (a[0], a[6], a[9]) if lang == "fr" else (a[1], a[7], a[10])
            hub = (hubs_paths or {}).get(a[0], {}).get(lang)
            fl = f'/{hub}/' if hub else (f"/?type=vols&to={code}" + ("" if lang == "fr" else "&lang=en"))
            others = " · ".join(f'<a href="/{path(k, lang)}/">{E(v[0] if lang == "fr" else v[1])}</a>' for k, v in A.items() if k != code)
            hero = f'<p class="eyebrow">{E(a[4] if lang == "fr" else a[5])}</p><h1>{t["h1"].format(c=E(c), dc=E(de(c)))}</h1><p class="hero-lead">{E(t["lead"].format(ap=ap, code=code))}</p>'
            body = (f'<section><h2>{E(t["city_h"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in a[8][lang]) + "</ul></section>"
                    f'<section><h2>{E(t["sim_h"])}</h2><p>{E(t["sim"].format(ops=a[11]))}</p></section>'
                    f'<section><h2>{E(t["money_h"])}</h2><p>{E(t["money"].format(cur=cur))}</p></section>'
                    f'<section><h2>{E(t["traps_h"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["traps"]) + "</ul></section>"
                    f'<section><h2>{E(t["book_h"])}</h2><ul class="links"><li><a href="{TRANSFER}" target="_blank" rel="sponsored noopener">{E(t["transfer"])}</a></li>'
                    f'<li><a href="{ESIM}" target="_blank" rel="sponsored noopener">{E(t["esim"])}</a></li><li><a href="{E(fl)}">{E(t["flights"].format(c=c))}</a></li></ul></section>'
                    f'<p class="small">⚠️ {E(t["warn"].format(m=CHECKED[lang]))}</p>'
                    f'<section><h2>{E(t["others"])}</h2><p class="pays-links">{others}</p></section>')
            urls.append(B.write(site, paths[lang], lang, t["title"].format(c=c, dc=de(c)), t["desc"].format(c=c, dc=de(c), code=code, m=CHECKED[lang]), hero, body, "", paths, ctx))
    return urls
