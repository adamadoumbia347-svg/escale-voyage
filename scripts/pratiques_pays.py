"""Pages pratiques (fr, en) : eSIM par pays (Airalo), location de voiture par ville (EconomyBookings),
hôtels près de l'aéroport pour une arrivée de nuit (Stay22, transfert Kiwitaxi). Une page d'index par famille.
Conseils généraux et prudents (vérifiés en novembre 2026) : pas de prix ni de forfaits écrits, pas d'opérateurs nommés ;
chaque page renvoie vers les offres en direct des partenaires (liens Travelpayouts déjà utilisés sur le site).
"""
import html
import urllib.parse

import build_i18n as B

E = html.escape
AIRALO = "https://airalo.tpm.lv/FrG2grmd"
CAR = "https://economybookings.tpm.lv/XjcDFT4f"
TAXI = "https://kiwitaxi.tpm.lv/hWfXu1nw"

# ---------- eSIM ----------
PAYS = [("ci", "côte-d-ivoire", "ivory-coast", "Côte d'Ivoire", "Côte d'Ivoire", "en Côte d'Ivoire", "🇨🇮"), ("sn", "senegal", "senegal", "Sénégal", "Senegal", "au Sénégal", "🇸🇳"),
        ("cm", "cameroun", "cameroon", "Cameroun", "Cameroon", "au Cameroun", "🇨🇲"), ("ml", "mali", "mali", "Mali", "Mali", "au Mali", "🇲🇱"),
        ("bj", "benin", "benin", "Bénin", "Benin", "au Bénin", "🇧🇯"), ("tg", "togo", "togo", "Togo", "Togo", "au Togo", "🇹🇬"),
        ("bf", "burkina-faso", "burkina-faso", "Burkina Faso", "Burkina Faso", "au Burkina Faso", "🇧🇫"), ("gn", "guinee", "guinea", "Guinée", "Guinea", "en Guinée", "🇬🇳"),
        ("ga", "gabon", "gabon", "Gabon", "Gabon", "au Gabon", "🇬🇦"), ("cd", "rd-congo", "dr-congo", "RD Congo", "DR Congo", "en RD Congo", "🇨🇩"),
        ("ng", "nigeria", "nigeria", "Nigeria", "Nigeria", "au Nigeria", "🇳🇬"), ("gh", "ghana", "ghana", "Ghana", "Ghana", "au Ghana", "🇬🇭"),
        ("ma", "maroc", "morocco", "Maroc", "Morocco", "au Maroc", "🇲🇦"), ("dz", "algerie", "algeria", "Algérie", "Algeria", "en Algérie", "🇩🇿"),
        ("tn", "tunisie", "tunisia", "Tunisie", "Tunisia", "en Tunisie", "🇹🇳"), ("eg", "egypte", "egypt", "Égypte", "Egypt", "en Égypte", "🇪🇬"),
        ("ke", "kenya", "kenya", "Kenya", "Kenya", "au Kenya", "🇰🇪")]
PAYS = [(c, f.replace("côte-d-ivoire", "cote-d-ivoire"), e, nf, ne, a, fl) for c, f, e, nf, ne, a, fl in PAYS]


def esim_body(lang, name, a_name):
    fr = lang == "fr"
    if fr:
        secs = [("eSIM ou carte SIM locale ?", [
            "<strong>L'eSIM</strong> s'achète en ligne avant de partir et s'installe en quelques minutes avec un QR code : internet fonctionne dès l'atterrissage, sans chercher de vendeur à l'aéroport. Tu gardes ta carte SIM habituelle pour les appels et les SMS.",
            "<strong>La carte SIM locale</strong> s'achète sur place (aéroport, boutiques d'opérateurs). Elle donne un numéro local, utile pour appeler sur place et pour le mobile money. Il faut en général présenter son passeport pour l'enregistrer.",
            "Beaucoup de voyageurs combinent les deux : l'eSIM pour arriver connecté, puis une SIM locale si le séjour est long."]),
            ("Avant d'acheter une eSIM", [
                "Vérifie que ton téléphone accepte l'eSIM (réglages → réseau mobile → « ajouter une eSIM ») et qu'il n'est pas bloqué par ton opérateur.",
                f"Vérifie que le pays est bien couvert et regarde la durée et le volume de données du forfait {a_name}.",
                "Installe l'eSIM avant le départ, avec une connexion Wi-Fi, et active-la seulement à l'arrivée.",
                "Pense à désactiver l'itinérance de ta carte SIM habituelle pour éviter des frais."]),
            ("Bon à savoir", [
                "WhatsApp, appels et messages passent par internet : une eSIM « données » suffit souvent pour rester en contact avec la famille.",
                "En dehors des grandes villes, la couverture peut être plus faible : télécharge les cartes hors ligne avant de partir."])]
        cta = f"Voir les eSIM pour {name}"
    else:
        secs = [("eSIM or local SIM card?", [
            "<strong>An eSIM</strong> is bought online before you go and installs in minutes with a QR code: internet works as soon as you land, with no need to find a seller at the airport. You keep your usual SIM for calls and texts.",
            "<strong>A local SIM card</strong> is bought there (airport, operator shops). It gives you a local number, useful for local calls and mobile money. You usually need your passport to register it.",
            "Many travellers combine both: an eSIM to arrive connected, then a local SIM for a long stay."]),
            ("Before buying an eSIM", [
                "Check your phone supports eSIM (settings → mobile network → 'add eSIM') and isn't locked to your carrier.",
                f"Check the country is covered and look at the plan's duration and data volume in {name}.",
                "Install the eSIM before leaving, on Wi-Fi, and only switch it on when you arrive.",
                "Turn off roaming on your usual SIM to avoid charges."]),
            ("Good to know", [
                "WhatsApp, calls and messages go over the internet: a data-only eSIM is often enough to stay in touch with family.",
                "Outside big cities coverage can be weaker: download offline maps before you go."])]
        cta = f"See eSIMs for {name}"
    body = "".join(f"<section><h2>{E(h)}</h2><ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul></section>" for h, items in secs)
    body += (f'<p><a class="btn" href="{AIRALO}" target="_blank" rel="sponsored noopener noreferrer">📱 {E(cta)} · Airalo ↗</a></p>'
             f'<p class="small">{"Lien partenaire : Escale peut toucher une commission, sans frais pour toi. Forfaits et prix à vérifier sur Airalo." if fr else "Partner link: Escale may earn a commission at no extra cost to you. Plans and prices to check on Airalo."}</p>')
    return body


# ---------- Location de voiture ----------
VILLES = [("abidjan", "abidjan", "Abidjan", "Abidjan", "à Abidjan", "ABJ"), ("dakar", "dakar", "Dakar", "Dakar", "à Dakar", "DSS"),
          ("casablanca", "casablanca", "Casablanca", "Casablanca", "à Casablanca", "CMN"), ("marrakech", "marrakech", "Marrakech", "Marrakech", "à Marrakech", "RAK"),
          ("agadir", "agadir", "Agadir", "Agadir", "à Agadir", "AGA"), ("tunis", "tunis", "Tunis", "Tunis", "à Tunis", "TUN"),
          ("djerba", "djerba", "Djerba", "Djerba", "à Djerba", "DJE"), ("alger", "algiers", "Alger", "Algiers", "à Alger", "ALG"),
          ("douala", "douala", "Douala", "Douala", "à Douala", "DLA"), ("accra", "accra", "Accra", "Accra", "à Accra", "ACC"),
          ("lome", "lome", "Lomé", "Lomé", "à Lomé", "LFW")]


def car_body(lang, name):
    fr = lang == "fr"
    if fr:
        secs = [("Avant de réserver", [
            "<strong>Permis :</strong> le permis international est souvent demandé, en plus de ton permis national. Renseigne-toi auprès du loueur et de l'ambassade, et prends les deux.",
            "<strong>Âge et carte :</strong> la plupart des loueurs demandent un âge minimum et une carte bancaire au nom du conducteur pour la caution.",
            "<strong>Assurance et franchise :</strong> regarde le montant de la franchise (ce que tu paies en cas de dégât) et ce qui est couvert.",
            "<strong>Carburant :</strong> préfère la formule « plein / plein » : tu rends la voiture avec le réservoir plein, sans frais cachés."]),
            ("Sur place", [
                "On roule à droite. Prends des photos de la voiture (carrosserie, pneus, compteur) au départ et au retour.",
                "Garde sur toi le contrat de location, ton permis et ton passeport : les contrôles routiers sont fréquents.",
                "En ville, la circulation peut être très dense : prévois de la marge pour l'aéroport.",
                "Une <strong>voiture avec chauffeur</strong> est souvent une bonne alternative pour un premier séjour : demande au loueur."]),
            ("Aéroport ou centre-ville ?", [
                "Prendre la voiture à l'aéroport est plus pratique à l'arrivée, mais parfois un peu plus cher qu'en ville. Compare les deux dans les offres."])]
        cta = f"Voir les voitures {E('à ' + name)}"
    else:
        secs = [("Before you book", [
            "<strong>Licence:</strong> an international driving permit is often required, on top of your national licence. Check with the rental company and the embassy, and bring both.",
            "<strong>Age and card:</strong> most companies require a minimum age and a credit card in the driver's name for the deposit.",
            "<strong>Insurance and excess:</strong> check the excess amount (what you pay if there's damage) and what is covered.",
            "<strong>Fuel:</strong> choose 'full to full': you return the car with a full tank, with no hidden fees."]),
            ("On the spot", [
                "Driving is on the right. Take photos of the car (body, tyres, mileage) at pick-up and return.",
                "Keep the rental contract, your licence and passport with you: road checks are frequent.",
                "City traffic can be very heavy: allow extra time to get to the airport.",
                "A <strong>car with driver</strong> is often a good option for a first trip: ask the rental company."]),
            ("Airport or city centre?", [
                "Picking up at the airport is handier on arrival, but sometimes a bit dearer than in town. Compare both in the offers."])]
        cta = f"See cars in {E(name)}"
    body = "".join(f"<section><h2>{E(h)}</h2><ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul></section>" for h, items in secs)
    body += (f'<p><a class="btn" href="{CAR}" target="_blank" rel="sponsored noopener noreferrer">🚗 {cta} · EconomyBookings ↗</a></p>'
             f'<p class="small">{"Lien partenaire : Escale peut toucher une commission, sans frais pour toi. Conditions (permis, âge, caution) à vérifier chez le loueur." if fr else "Partner link: Escale may earn a commission at no extra cost to you. Conditions (licence, age, deposit) to check with the rental company."}</p>')
    return body


# ---------- Hôtels près de l'aéroport ----------
AEROS = [("abidjan", "abidjan", "Abidjan", "Abidjan", "ABJ"), ("accra", "accra", "Accra", "Accra", "ACC"), ("alger", "algiers", "Alger", "Algiers", "ALG"),
         ("bamako", "bamako", "Bamako", "Bamako", "BKO"), ("casablanca", "casablanca", "Casablanca", "Casablanca", "CMN"), ("conakry", "conakry", "Conakry", "Conakry", "CKY"),
         ("dakar", "dakar", "Dakar", "Dakar", "DSS"), ("douala", "douala", "Douala", "Douala", "DLA"), ("kinshasa", "kinshasa", "Kinshasa", "Kinshasa", "FIH"),
         ("lagos", "lagos", "Lagos", "Lagos", "LOS"), ("lome", "lome", "Lomé", "Lomé", "LFW"), ("tunis", "tunis", "Tunis", "Tunis", "TUN")]
AERO_NAME = {"ABJ": "Félix-Houphouët-Boigny International Airport", "ACC": "Kotoka International Airport", "ALG": "Houari Boumediene Airport", "BKO": "Modibo Keita International Airport",
             "CMN": "Mohammed V International Airport", "CKY": "Conakry International Airport", "DSS": "Blaise Diagne International Airport", "DLA": "Douala International Airport",
             "FIH": "Ndjili International Airport", "LOS": "Murtala Muhammed International Airport", "LFW": "Lomé–Tokoin International Airport", "TUN": "Tunis Carthage International Airport"}


def night_body(site, lang, name, code, guide):
    fr = lang == "fr"
    addr = AERO_NAME[code] + ", " + name
    extra = ""
    if code == "DSS":
        extra = ("<li>L'aéroport Blaise-Diagne est loin du centre de Dakar (environ une heure de route selon la circulation) : dormir près de l'aéroport évite la route en pleine nuit.</li>" if fr else
                 "<li>Blaise Diagne Airport is far from central Dakar (about an hour's drive depending on traffic): sleeping near the airport avoids the road in the middle of the night.</li>")
    tips = (["Réserve ton transfert ou ton taxi <strong>avant</strong> de partir, ou fais-toi attendre par quelqu'un de confiance.", "Évite les « taxis » qui t'abordent dans le hall : utilise les taxis officiels ou ton transfert réservé.",
             "Garde un peu d'argent liquide local et ton téléphone chargé (une eSIM aide à être connecté dès l'arrivée).", "Envoie à un proche l'adresse de ton hôtel et ton heure d'arrivée."] if fr else
            ["Book your transfer or taxi <strong>before</strong> you go, or have someone you trust meet you.", "Avoid 'taxis' that approach you in the arrivals hall: use official taxis or your booked transfer.",
             "Keep some local cash and a charged phone (an eSIM helps you be online on arrival).", "Send a relative your hotel address and arrival time."])
    body = (f'<section><h2>{"Arriver de nuit : les bons réflexes" if fr else "Arriving at night: good habits"}</h2><ul>' + extra + "".join(f"<li>{x}</li>" for x in tips) + "</ul></section>"
            + B.hotel_map(lang, name + (" (aéroport)" if fr else " (airport)"), addr) +
            f'<p class="pr-btns"><a class="btn" href="{E(B.stay22(addr, "hotel-aeroport-" + lang))}" target="_blank" rel="sponsored noopener noreferrer">🛏️ {"Voir les hôtels près de l’aéroport" if fr else "See hotels near the airport"} ↗</a>'
            f'<a class="btn ghost" href="{TAXI}" target="_blank" rel="sponsored noopener noreferrer">🚕 {"Réserver un transfert" if fr else "Book a transfer"} · Kiwitaxi ↗</a></p>'
            f'<p><a href="/{guide}/">🛬 {"Guide complet : arriver à l’aéroport de " if fr else "Full guide: arriving at "}{E(name)}{"" if fr else " airport"} →</a></p>'
            f'<p class="small">{"Liens partenaires : Escale peut toucher une commission, sans frais pour toi." if fr else "Partner links: Escale may earn a commission at no extra cost to you."}</p>')
    return body


FAM = {
    "esim": dict(fr=dict(base="esim", ttl="eSIM pour l'Afrique : internet dès l'arrivée, pays par pays | Escale", h1="Une eSIM pour <span>l'Afrique</span>",
                         lead="Internet dès l'atterrissage, sans chercher de vendeur à l'aéroport : choisis ton pays.", desc="eSIM ou carte SIM locale ? Les conseils pour être connecté dès l'arrivée en Côte d'Ivoire, au Sénégal, au Cameroun, au Maroc et dans 13 autres pays."),
                 en=dict(base="en/esim", ttl="eSIM for Africa: internet on arrival, country by country | Escale", h1="An eSIM <span>for Africa</span>",
                         lead="Internet as soon as you land, with no seller to find at the airport: pick your country.", desc="eSIM or local SIM? Tips to be online on arrival in Nigeria, Ghana, Kenya, Côte d'Ivoire, Senegal, Morocco and more.")),
    "car": dict(fr=dict(base="location-voiture", ttl="Location de voiture en Afrique : Abidjan, Dakar, Casablanca, Marrakech… | Escale", h1="Louer une voiture <span>au pays</span>",
                        lead="Permis, assurance, carburant, aéroport ou centre-ville : les conseils et les offres, ville par ville.", desc="Louer une voiture à Abidjan, Dakar, Casablanca, Marrakech, Tunis, Alger, Douala, Accra ou Lomé : permis, franchise, carburant et offres en direct."),
                en=dict(base="en/car-rental", ttl="Car rental in Africa: Abidjan, Dakar, Casablanca, Accra… | Escale", h1="Rent a car <span>back home</span>",
                        lead="Licence, insurance, fuel, airport or city: tips and live offers, city by city.", desc="Rent a car in Accra, Lagos, Abidjan, Dakar, Casablanca, Marrakech or Tunis: licence, excess, fuel and live offers.")),
    "night": dict(fr=dict(base="hotel-aeroport", ttl="Arrivée de nuit : hôtels près de l'aéroport en Afrique | Escale", h1="Arrivée de nuit : <span>dormir près de l'aéroport</span>",
                          lead="Beaucoup de vols arrivent tard. Les hôtels proches de l'aéroport et les bons réflexes, aéroport par aéroport.", desc="Vol qui arrive de nuit à Abidjan, Dakar, Lagos, Douala, Kinshasa ? Les hôtels près de l'aéroport, le transfert à réserver et les bons réflexes."),
                  en=dict(base="en/airport-hotels", ttl="Arriving at night: hotels near African airports | Escale", h1="Arriving at night: <span>sleep near the airport</span>",
                          lead="Many flights land late. Hotels close to the airport and good habits, airport by airport.", desc="Landing at night in Lagos, Accra, Abidjan, Dakar, Douala? Hotels near the airport, the transfer to book and good habits.")),
}


def build(site, ctx):
    urls = []
    items = {"esim": [], "car": [], "night": []}
    for c, sf, se, nf, ne, a_fr, fl in PAYS:
        paths = {"fr": f"esim/{sf}", "en": f"en/esim/{se}"}
        for lang in ("fr", "en"):
            fr = lang == "fr"
            name = nf if fr else ne
            title = (f"eSIM {name} : internet dès l'arrivée, eSIM ou SIM locale ? | Escale" if fr else f"eSIM for {name}: internet on arrival, eSIM or local SIM? | Escale")
            desc = (f"Être connecté dès l'atterrissage {a_fr} : eSIM ou carte SIM locale, téléphone compatible, installation et conseils." if fr else f"Be online as soon as you land in {name}: eSIM or local SIM, compatible phone, setup and tips.")
            hero = f'<p class="eyebrow">{fl} {"eSIM" }</p><h1>{"Internet dès l’arrivée " + E(a_fr) if fr else "Internet on arrival in " + E(name)}</h1><p class="hero-lead">{E(desc)}</p>'
            urls.append(B.write(site, paths[lang], lang, title, desc, hero, esim_body(lang, name, a_fr if fr else name), "", paths, ctx))
            items["esim"].append((lang, paths[lang], f"{fl} {name}"))
    for sf, se, nf, ne, a_fr, code in VILLES:
        paths = {"fr": f"location-voiture/{sf}", "en": f"en/car-rental/{se}"}
        for lang in ("fr", "en"):
            fr = lang == "fr"
            name = nf if fr else ne
            title = (f"Location de voiture {a_fr} : permis, assurance, conseils et offres | Escale" if fr else f"Car rental in {name}: licence, insurance, tips and offers | Escale")
            desc = (f"Louer une voiture {a_fr} : permis international, franchise, carburant, aéroport ou centre-ville, et les offres en direct." if fr else f"Renting a car in {name}: international permit, excess, fuel, airport or city centre, and live offers.")
            hero = f'<p class="eyebrow">🚗 {"Location de voiture" if fr else "Car rental"}</p><h1>{("Louer une voiture <span>" + E(a_fr) + "</span>") if fr else ("Rent a car <span>in " + E(name) + "</span>")}</h1><p class="hero-lead">{E(desc)}</p>'
            urls.append(B.write(site, paths[lang], lang, title, desc, hero, car_body(lang, name), "", paths, ctx))
            items["car"].append((lang, paths[lang], name))
    for sf, se, nf, ne, code in AEROS:
        paths = {"fr": f"hotel-aeroport/{sf}", "en": f"en/airport-hotels/{se}"}
        for lang in ("fr", "en"):
            fr = lang == "fr"
            name = nf if fr else ne
            guide = f"arriver-aeroport-{sf}" if fr else f"en/arriving-at-{se}-airport"
            title = (f"Hôtel près de l'aéroport de {name} : arriver de nuit sereinement | Escale" if fr else f"Hotel near {name} airport: arriving at night with peace of mind | Escale")
            desc = (f"Vol qui arrive de nuit à {name} ? Les hôtels proches de l'aéroport, le transfert à réserver et les bons réflexes pour arriver sereinement." if fr else f"Landing at night in {name}? Hotels close to the airport, the transfer to book and good habits to arrive with peace of mind.")
            hero = f'<p class="eyebrow">🌙 {"Arrivée de nuit" if fr else "Night arrival"}</p><h1>{("Dormir près de l’aéroport <span>de " + E(name) + "</span>") if fr else ("Sleep near <span>" + E(name) + " airport</span>")}</h1><p class="hero-lead">{E(desc)}</p>'
            urls.append(B.write(site, paths[lang], lang, title, desc, hero, night_body(site, lang, name, code, guide), "", paths, ctx))
            items["night"].append((lang, paths[lang], name))
    for fam, conf in FAM.items():
        paths = {l: conf[l]["base"] for l in ("fr", "en")}
        for lang in ("fr", "en"):
            c = conf[lang]
            links = "".join(f'<li><a class="tool-chip" href="/{p}/">{E(n)}</a></li>' for l, p, n in items[fam] if l == lang)
            hero = f'<h1>{c["h1"]}</h1><p class="hero-lead">{E(c["lead"])}</p>'
            urls.append(B.write(site, c["base"], lang, c["ttl"], c["desc"], hero, f'<ul class="pv-other">{links}</ul>', "", paths, ctx))
    return urls
