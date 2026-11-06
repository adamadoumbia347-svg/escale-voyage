"""Informations propres à chaque pays ou ville pour les pages eSIM, location de voiture et hôtels d'aéroport (fr, en, it, de).

Seulement des faits stables et connus (principaux opérateurs mobiles, mobile money, distance approximative aéroport–centre) ;
formulés avec prudence (« environ », « principaux »). À relire une fois par an (les opérateurs changent parfois de nom).
"""
import html

E = html.escape

OPS = {"ci": ["Orange", "MTN", "Moov Africa"], "sn": ["Orange", "Free", "Expresso"], "cm": ["MTN", "Orange"], "ml": ["Orange", "Moov Africa Malitel"],
       "bj": ["MTN", "Moov Africa"], "bf": ["Orange", "Moov Africa", "Telecel"], "ga": ["Airtel", "Moov Africa"], "cd": ["Vodacom", "Orange", "Airtel", "Africell"],
       "ng": ["MTN", "Airtel", "Glo"], "gh": ["MTN", "Telecel", "AT"], "ma": ["Maroc Telecom", "Orange", "inwi"], "dz": ["Mobilis", "Djezzy", "Ooredoo"],
       "tn": ["Ooredoo", "Orange", "Tunisie Telecom"], "eg": ["Vodafone", "Orange", "e&", "WE"], "ke": ["Safaricom", "Airtel"]}
MONEY = {"ci": "Orange Money, Wave, MTN MoMo", "sn": "Wave, Orange Money", "cm": "MTN MoMo, Orange Money", "ml": "Orange Money", "bf": "Orange Money, Moov Money",
         "bj": "MTN MoMo, Moov Money", "gh": "MTN MoMo", "ke": "M-Pesa", "cd": "M-Pesa, Orange Money, Airtel Money", "ng": "OPay, MoniePoint"}
MONEY_OK = {k for k in MONEY if k != "ng"}  # au Nigeria, ce sont surtout des banques en ligne : phrase à part

# code aéroport -> (km environ jusqu'au centre, centre fr, centre en)
DIST = {"ABJ": (16, "du Plateau", "the Plateau"), "DSS": (45, "du centre de Dakar", "central Dakar"), "CMN": (30, "du centre de Casablanca", "central Casablanca"),
        "RAK": (6, "de la médina", "the medina"), "AGA": (25, "du centre d'Agadir", "central Agadir"), "TUN": (8, "du centre de Tunis", "central Tunis"),
        "DJE": (8, "de Houmt Souk", "Houmt Souk"), "ALG": (20, "du centre d'Alger", "central Algiers"), "DLA": (10, "du quartier d'Akwa", "the Akwa district"),
        "ACC": (10, "du centre d'Accra", "central Accra"), "LFW": (5, "du centre de Lomé", "central Lomé"), "BKO": (15, "du centre de Bamako", "central Bamako"),
        "CKY": (15, "de Kaloum, le centre de Conakry", "Kaloum, central Conakry"), "LOS": (20, "de Victoria Island", "Victoria Island"), "FIH": (25, "du centre de Kinshasa (Gombe)", "central Kinshasa (Gombe)")}
EXTRA = {"CMN": {"fr": "Un train relie l'aéroport au centre de Casablanca : pratique et souvent moins cher que le taxi.",
                 "en": "A train links the airport with central Casablanca: convenient and often cheaper than a taxi.",
                 "it": "Un treno collega l'aeroporto al centro di Casablanca: comodo e spesso più economico del taxi.",
                 "de": "Ein Zug verbindet den Flughafen mit dem Zentrum von Casablanca: praktisch und oft günstiger als ein Taxi."},
         "LOS": {"fr": "Selon la circulation, le trajet vers Victoria Island ou Lekki peut prendre une à deux heures : évitez les heures de pointe.",
                 "en": "Depending on traffic, the ride to Victoria Island or Lekki can take one to two hours: avoid rush hour.",
                 "it": "A seconda del traffico, il tragitto verso Victoria Island o Lekki può richiedere da una a due ore: evita le ore di punta.",
                 "de": "Je nach Verkehr kann die Fahrt nach Victoria Island oder Lekki ein bis zwei Stunden dauern: Meide die Stoßzeiten."},
         "DSS": {"fr": "L'aéroport Blaise-Diagne est à Diass : prévoyez environ une heure de route vers Dakar, et le transfert dans votre budget.",
                 "en": "Blaise Diagne airport is in Diass: allow about an hour by road to Dakar, and budget for the transfer.",
                 "it": "L'aeroporto Blaise Diagne si trova a Diass: calcola circa un'ora di strada fino a Dakar e il transfer nel budget.",
                 "de": "Der Flughafen Blaise Diagne liegt in Diass: Rechne mit etwa einer Stunde Fahrt nach Dakar und plane den Transfer ein."}}

T = {
    "fr": dict(h_sim="Opérateurs et cartes SIM sur place", ops="Les principaux opérateurs mobiles {a} sont {o}. Leurs cartes SIM se vendent dans leurs boutiques et souvent à l'aéroport ; il faut en général présenter son passeport pour l'enregistrer.",
               money="Pour payer et envoyer de l'argent au quotidien, le mobile money est très utilisé : {m}.", ng="Au quotidien, on paie beaucoup par virement et par carte via les banques en ligne : gardez une carte bancaire qui fonctionne à l'étranger.",
               h_go="De l'aéroport au centre", dist="L'aéroport est à environ {k} km {c} : comptez en général 20 à 60 minutes selon la circulation.", et=" et "),
    "en": dict(h_sim="Local operators and SIM cards", ops="The main mobile operators in {a} are {o}. Their SIM cards are sold in their shops and often at the airport; you usually need your passport to register one.",
               money="Mobile money is widely used for everyday payments and transfers: {m}.", ng="Day to day, people pay a lot by bank transfer and card through online banks: bring a bank card that works abroad.",
               h_go="From the airport to the city", dist="The airport is about {k} km from {c}: allow 20 to 60 minutes depending on traffic.", et=" and "),
    "it": dict(h_sim="Operatori e SIM sul posto", ops="I principali operatori mobili {a} sono {o}. Le loro SIM si vendono nei negozi e spesso in aeroporto; di solito serve il passaporto per registrarla.",
               money="Per pagare e inviare denaro ogni giorno si usa molto il mobile money: {m}.", ng="Nella vita di tutti i giorni si paga molto con bonifico e carta tramite banche online: porta una carta che funzioni all'estero.",
               h_go="Dall'aeroporto al centro", dist="L'aeroporto si trova a circa {k} km dal centro: calcola in genere da 20 a 60 minuti a seconda del traffico.", et=" e "),
    "de": dict(h_sim="Mobilfunkanbieter und SIM-Karten vor Ort", ops="Die wichtigsten Mobilfunkanbieter {a} sind {o}. Ihre SIM-Karten gibt es in den Shops und oft am Flughafen; zur Registrierung brauchst du meist deinen Reisepass.",
               money="Für tägliche Zahlungen und Überweisungen ist Mobile Money weit verbreitet: {m}.", ng="Im Alltag zahlt man viel per Überweisung und Karte über Online-Banken: Nimm eine Bankkarte mit, die im Ausland funktioniert.",
               h_go="Vom Flughafen ins Zentrum", dist="Der Flughafen liegt etwa {k} km vom Zentrum entfernt: Rechne je nach Verkehr mit 20 bis 60 Minuten.", et=" und "),
}


def _join(xs, lang):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + T[lang]["et"] + xs[-1]


def esim(country, lang, a):
    """Bloc « opérateurs » d'une page eSIM ; a = « en Côte d'Ivoire », « Nigeria », « in Costa d'Avorio »…"""
    t, ops = T[lang], OPS.get(country)
    if not ops:
        return ""
    if lang == "en":
        a = a
    elif lang == "de":
        a = a if a.startswith("in ") else "in " + a
    p = [t["ops"].format(a=a, o=_join(ops, lang))]
    if country in MONEY_OK:
        p.append(t["money"].format(m=MONEY[country]))
    elif country == "ng":
        p.append(t["ng"])
    return f'<section><h2>{E(t["h_sim"])}</h2>' + "".join(f"<p>{E(x)}</p>" for x in p) + "</section>"


def transfer(code, lang):
    """Bloc « de l'aéroport au centre » d'une page location de voiture ou hôtel d'aéroport."""
    d = DIST.get(code)
    if not d:
        return ""
    t = T[lang]
    c = d[1] if lang == "fr" else d[2]
    txt = t["dist"].format(k=d[0], c=c)
    if code in ("LOS", "DSS"):  # durée donnée plus bas, plus précise
        txt = txt.split(":")[0].rstrip() + "."
    extra = EXTRA.get(code, {}).get(lang, "")
    return f'<section><h2>{E(t["h_go"])}</h2><p>{E(txt)}</p>' + (f"<p>{E(extra)}</p>" if extra else "") + "</section>"
