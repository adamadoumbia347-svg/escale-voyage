"""Pages thématiques pour les voyageurs qui partent d'Afrique (français et anglais) :
- Hajj et Omra : vols vers Djeddah et Médine ;
- Études : vols vers la France, le Canada, le Maroc, la Turquie, la Chine, le Royaume-Uni ;
- Commerce : vols vers Dubaï, Canton (Guangzhou) et Istanbul.

Chaque page liste les trajets avec le prix trouvé récemment (hub.js) et son équivalent en monnaie locale (fx.js),
puis des conseils prudents qui renvoient aux sources officielles (Hajj, visas, études). Vérifié : novembre 2026.
"""
import html

import build_i18n as B

E = html.escape

THEMES = {
    "hajj": dict(
        routes=[("DSS", "JED"), ("DSS", "MED"), ("BKO", "JED"), ("ABJ", "JED"), ("CKY", "JED"), ("NIM", "JED"), ("KAN", "JED"), ("LOS", "JED"),
                ("DLA", "JED"), ("CMN", "JED"), ("ALG", "JED"), ("TUN", "JED"), ("CDG", "JED"), ("CDG", "MED")],
        fr=dict(path="vols-hajj-omra", title="Hajj et Omra 2027 : billets d'avion pas chers depuis l'Afrique | Escale",
                desc="Vols vers Djeddah et Médine depuis Dakar, Bamako, Abidjan, Conakry, Niamey, Kano, Lagos, Casablanca et Alger : prix récents, dates 2027 et conseils pour le Hajj et l'Omra.",
                h1="Hajj et Omra 2027 : <span>les vols moins chers</span>",
                lead="Les prix des vols vers Djeddah et Médine depuis l'Afrique de l'Ouest, le Maghreb et Paris, avec l'essentiel à savoir avant de réserver.",
                table="Vols vers Djeddah et Médine", tips_h="À savoir avant de réserver",
                tips=["<strong>Dates 2027.</strong> Le Hajj devrait avoir lieu vers la mi-mai 2027 ; les dates exactes dépendent de l'observation de la lune. L'Omra se fait toute l'année, avec une forte demande pendant le Ramadan (vers février-mars 2027).",
                      "<strong>Hajj : le billet seul ne suffit pas.</strong> Le visa Hajj est délivré dans le cadre du quota de chaque pays, par les agences agréées ou l'organisme officiel du Hajj de votre pays. Adressez-vous à eux avant d'acheter un billet.",
                      "<strong>Omra : le visa dépend de votre nationalité.</strong> Vérifiez les conditions sur la plateforme officielle <a href=\"https://www.nusuk.sa/\" target=\"_blank\" rel=\"noopener\">Nusuk</a> ou auprès d'une agence agréée.",
                      "<strong>Santé.</strong> L'Arabie saoudite demande le vaccin contre la méningite (ACYW) pour le Hajj et l'Omra, et le certificat de fièvre jaune si vous venez d'un pays où elle est présente. Vérifiez les exigences à jour avant le départ.",
                      "<strong>Réservez tôt pour le Ramadan :</strong> les prix vers Djeddah montent fortement à l'approche des dix derniers jours. Comparez aussi l'arrivée à Médine.",
                      "<strong>Bagages et eau de Zamzam :</strong> les règles changent selon la compagnie ; demandez-les avant de payer."],
                faq=[("Quand a lieu le Hajj 2027 ?", "Vers la mi-mai 2027. Les dates exactes dépendent de l'observation de la lune et sont confirmées par les autorités saoudiennes."),
                     ("Puis-je acheter seulement un billet pour le Hajj ?", "Non. Le Hajj demande un visa spécifique, attribué dans le cadre du quota de chaque pays par les agences agréées ou l'organisme officiel du Hajj. Renseignez-vous auprès d'eux d'abord."),
                     ("Quel aéroport pour l'Omra : Djeddah ou Médine ?", "Djeddah est le plus desservi et souvent le moins cher ; Médine évite un long trajet si vous commencez par la visite de la Mosquée du Prophète. Comparez les deux.")]),
        en=dict(path="en/hajj-umrah-flights", title="Hajj and Umrah 2027: cheap flights from Africa | Escale",
                desc="Flights to Jeddah and Medina from Lagos, Kano, Dakar, Bamako, Abidjan, Conakry, Niamey, Casablanca and Algiers: recent prices, 2027 dates and tips for Hajj and Umrah.",
                h1="Hajj and Umrah 2027: <span>cheaper flights</span>",
                lead="Flight prices to Jeddah and Medina from West Africa, North Africa and Paris, with what you need to know before booking.",
                table="Flights to Jeddah and Medina", tips_h="Before you book",
                tips=["<strong>2027 dates.</strong> Hajj is expected around mid-May 2027; exact dates depend on the moon sighting. Umrah is possible all year, with high demand during Ramadan (around February–March 2027).",
                      "<strong>Hajj: a ticket alone is not enough.</strong> Hajj visas are issued under each country's quota, through approved agencies or your country's official Hajj body. Contact them before buying a ticket.",
                      "<strong>Umrah: the visa depends on your nationality.</strong> Check the conditions on the official <a href=\"https://www.nusuk.sa/\" target=\"_blank\" rel=\"noopener\">Nusuk</a> platform or with an approved agency.",
                      "<strong>Health.</strong> Saudi Arabia requires the meningitis (ACYW) vaccine for Hajj and Umrah, and a yellow fever certificate if you come from a country where it is present. Check the current requirements before you travel.",
                      "<strong>Book early for Ramadan:</strong> prices to Jeddah rise sharply ahead of the last ten nights. Compare arriving in Medina too.",
                      "<strong>Baggage and Zamzam water:</strong> rules vary by airline; ask before you pay."],
                faq=[("When is Hajj 2027?", "Around mid-May 2027. Exact dates depend on the moon sighting and are confirmed by the Saudi authorities."),
                     ("Can I just buy a ticket for Hajj?", "No. Hajj needs a specific visa, issued under each country's quota through approved agencies or the official Hajj body. Contact them first."),
                     ("Which airport for Umrah: Jeddah or Medina?", "Jeddah has the most flights and is often cheaper; Medina saves a long transfer if you start with the Prophet's Mosque. Compare both.")])),
    "etudes": dict(
        routes=[("ABJ", "CDG"), ("DSS", "CDG"), ("BKO", "CDG"), ("CKY", "CDG"), ("DLA", "CDG"), ("LFW", "CDG"), ("COO", "CDG"), ("OUA", "CDG"), ("NIM", "CDG"),
                ("FIH", "BRU"), ("ABJ", "YUL"), ("DSS", "YUL"), ("DLA", "YUL"), ("ABJ", "CMN"), ("DLA", "CMN"), ("FIH", "CMN"), ("NIM", "CMN"),
                ("ABJ", "IST"), ("NIM", "IST"), ("ABJ", "PEK"), ("LOS", "PEK"), ("LOS", "LHR"), ("ACC", "LHR"), ("ABV", "LHR")],
        fr=dict(path="etudiants-billet-avion", title="Étudiants : billet d'avion pas cher pour partir étudier | Escale",
                desc="Partir étudier en France, au Canada, au Maroc, en Turquie ou en Chine depuis Abidjan, Dakar, Bamako, Douala ou Kinshasa : prix des vols, bon moment pour réserver, bagages.",
                h1="Partir étudier : <span>le billet moins cher</span>",
                lead="Les prix des vols pour la rentrée depuis l'Afrique vers la France, la Belgique, le Canada, le Maroc, la Turquie, la Chine et le Royaume-Uni.",
                table="Vols pour aller étudier", tips_h="Nos conseils pour les étudiants",
                tips=["<strong>Réservez dès que le visa est en bonne voie :</strong> pour une rentrée en septembre, les prix montent fortement en juillet et août. Un billet modifiable coûte un peu plus mais protège si le visa tarde.",
                      "<strong>Aller simple ou aller-retour ?</strong> Pour une année d'études, comparez les deux : l'aller simple est parfois presque aussi cher qu'un aller-retour.",
                      "<strong>Bagages :</strong> c'est souvent le vrai coût. Comparez la franchise de chaque compagnie et demandez si une offre étudiante permet un bagage en plus.",
                      "<strong>Visa étudiant :</strong> pour la France, la procédure passe par <a href=\"https://www.campusfrance.org/\" target=\"_blank\" rel=\"noopener\">Campus France</a> ; pour le Canada, par le permis d'études sur <a href=\"https://www.canada.ca/fr/immigration-refugies-citoyennete/services/etudier-canada.html\" target=\"_blank\" rel=\"noopener\">canada.ca</a>. Pour les autres pays, voyez le consulat.",
                      "<strong>Arrivée :</strong> prévoyez le trajet de l'aéroport au logement (transfert réservé, carte eSIM pour avoir Internet dès l'atterrissage)."],
                faq=[("Quand réserver son billet pour la rentrée ?", "Dès que le visa est en bonne voie, idéalement avant juin pour une rentrée en septembre. Les prix montent en juillet et août."),
                     ("Vaut-il mieux un aller simple ?", "Pas toujours : comparez l'aller simple et l'aller-retour, l'écart est parfois faible. L'aller-retour peut aussi rassurer le consulat selon les pays."),
                     ("Comment emporter plus de bagages ?", "Comparez les franchises des compagnies, demandez les offres étudiantes et pensez à réserver le bagage en ligne avant le départ, moins cher qu'à l'aéroport.")]),
        en=dict(path="en/student-flights-from-africa", title="Student flights from Africa: cheap tickets to study abroad | Escale",
                desc="Going to study in the UK, France, Canada, Morocco, Turkey or China from Lagos, Accra, Abuja, Abidjan or Dakar: flight prices, when to book and baggage tips.",
                h1="Going abroad to study: <span>cheaper flights</span>",
                lead="Flight prices for the academic year from Africa to the UK, France, Belgium, Canada, Morocco, Turkey and China.",
                table="Flights to go and study", tips_h="Our tips for students",
                tips=["<strong>Book once your visa is on track:</strong> for a September start, prices rise sharply in July and August. A changeable ticket costs a bit more but protects you if the visa is delayed.",
                      "<strong>One way or return?</strong> For a year of study, compare both: a one-way ticket is sometimes almost as expensive as a return.",
                      "<strong>Baggage</strong> is often the real cost. Compare each airline's allowance and ask whether a student fare includes an extra bag.",
                      "<strong>Student visa:</strong> for the UK, see <a href=\"https://www.gov.uk/student-visa\" target=\"_blank\" rel=\"noopener\">gov.uk</a>; for Canada, the study permit on <a href=\"https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada.html\" target=\"_blank\" rel=\"noopener\">canada.ca</a>; for France, <a href=\"https://www.campusfrance.org/en\" target=\"_blank\" rel=\"noopener\">Campus France</a>.",
                      "<strong>Arrival:</strong> plan the trip from the airport to your accommodation (pre-booked transfer, eSIM to be online as soon as you land)."],
                faq=[("When should I book my flight for the new academic year?", "Once your visa is on track, ideally before June for a September start. Prices rise in July and August."),
                     ("Is a one-way ticket better?", "Not always: compare one way and return, the difference is sometimes small."),
                     ("How can I take more baggage?", "Compare airline allowances, ask about student fares and add bags online before departure, which is cheaper than at the airport.")])),
    "commerce": dict(
        routes=[("LOS", "DXB"), ("LOS", "CAN"), ("LOS", "IST"), ("ABV", "DXB"), ("KAN", "DXB"), ("KAN", "CAN"), ("ACC", "DXB"), ("ACC", "CAN"),
                ("FIH", "DXB"), ("FIH", "CAN"), ("DLA", "DXB"), ("DLA", "CAN"), ("ABJ", "DXB"), ("ABJ", "CAN"), ("DSS", "DXB"), ("BKO", "DXB"),
                ("CKY", "DXB"), ("ABJ", "IST"), ("DSS", "IST"), ("BKO", "IST")],
        fr=dict(path="vols-commerce-dubai-canton-istanbul", title="Vols pas chers vers Dubaï, Canton et Istanbul depuis l'Afrique | Escale",
                desc="Voyage d'affaires ou d'achats à Dubaï, Canton (Guangzhou) ou Istanbul depuis Lagos, Kinshasa, Douala, Abidjan, Dakar : prix récents, visas et conseils bagages.",
                h1="Commerce : <span>Dubaï, Canton, Istanbul</span>",
                lead="Les prix des vols vers les grandes places du commerce depuis l'Afrique de l'Ouest et centrale, et ce qu'il faut prévoir avant de partir.",
                table="Vols vers Dubaï, Canton et Istanbul", tips_h="Nos conseils pour les voyages d'affaires",
                tips=["<strong>Foire de Canton :</strong> elle a lieu deux fois par an, au printemps (avril-mai) et à l'automne (octobre-novembre). Les vols et hôtels montent à ces dates : réservez tôt.",
                      "<strong>Visas :</strong> la Chine et les Émirats demandent un visa à la plupart des passeports africains ; pour la Turquie, cela dépend du passeport. Vérifiez avec notre outil <a href=\"/visa/\">Visa selon mon passeport</a> puis sur le site officiel.",
                      "<strong>Excédent de bagages :</strong> il coûte cher à l'aéroport. Comparez les franchises, achetez les kilos en plus en ligne, ou envoyez la marchandise en fret.",
                      "<strong>Escales :</strong> Addis-Abeba, Dubaï, Doha et Istanbul relient l'Afrique à la Chine ; une escale plus longue peut faire baisser le prix."],
                faq=[("Quand a lieu la Foire de Canton ?", "Deux fois par an : au printemps (avril-mai) et à l'automne (octobre-novembre). Vérifiez les dates exactes sur le site officiel de la foire."),
                     ("Faut-il un visa pour Dubaï ?", "Pour la plupart des passeports africains, oui, avant le départ. Vérifiez avec l'outil Visa selon mon passeport et le site officiel des Émirats."),
                     ("Comment éviter de payer trop cher les bagages ?", "Achetez les kilos supplémentaires en ligne avant le départ, comparez les franchises des compagnies, ou envoyez les marchandises en fret.")]),
        en=dict(path="en/business-flights-dubai-guangzhou-istanbul", title="Cheap flights to Dubai, Guangzhou and Istanbul from Africa | Escale",
                desc="Business and shopping trips to Dubai, Guangzhou or Istanbul from Lagos, Kano, Abuja, Accra, Kinshasa and Douala: recent prices, visas and baggage tips.",
                h1="Business trips: <span>Dubai, Guangzhou, Istanbul</span>",
                lead="Flight prices to the big trading hubs from West and Central Africa, and what to plan before you go.",
                table="Flights to Dubai, Guangzhou and Istanbul", tips_h="Our tips for business trips",
                tips=["<strong>Canton Fair:</strong> it takes place twice a year, in spring (April–May) and autumn (October–November). Flights and hotels go up around those dates: book early.",
                      "<strong>Visas:</strong> China and the UAE require a visa for most African passports; for Turkey, it depends on your passport. Check with our <a href=\"/en/visa/\">visa by passport</a> tool, then on the official website.",
                      "<strong>Excess baggage</strong> is expensive at the airport. Compare allowances, buy extra kilos online, or ship goods by cargo.",
                      "<strong>Stopovers:</strong> Addis Ababa, Dubai, Doha and Istanbul connect Africa with China; a longer stop can lower the price."],
                faq=[("When is the Canton Fair?", "Twice a year: in spring (April–May) and autumn (October–November). Check the exact dates on the fair's official website."),
                     ("Do I need a visa for Dubai?", "For most African passports, yes, before departure. Check with the visa by passport tool and the official UAE website."),
                     ("How do I avoid paying too much for baggage?", "Buy extra kilos online before departure, compare airline allowances, or ship goods by cargo.")])),
}
LABEL = {"fr": dict(th=("Trajet", "Aller-retour dès", ""), see="Voir", from_="dès", others="Voir aussi", country="Vols au départ de votre pays"),
         "en": dict(th=("Route", "Round trip from", ""), see="See", from_="from", others="See also", country="Flights from your country")}


def links(lang):
    """Liens vers les 3 pages, pour les autres pages (pays, accueil)."""
    return [(t[lang]["path"], re.sub(r"<[^>]+>", "", t[lang]["h1"])) for t in THEMES.values()]


import re  # noqa: E402


def build(site, ctx, route_paths):
    by_codes = {(r[0], r[1]): r for r in ctx["routes"]}
    urls = []
    for key, th in THEMES.items():
        paths = {"fr": th["fr"]["path"], "en": th["en"]["path"]}
        for lang in ("fr", "en"):
            t, L = th[lang], LABEL[lang]
            rows = ""
            for o, d in th["routes"]:
                r = by_codes.get((o, d))
                if not r or r not in route_paths:
                    continue
                a, b = (r[2], r[3]) if lang == "fr" else (B.city(r[2], "en"), B.city(r[3], "en"))
                href = f"/{route_paths[r][lang]}/"
                rows += (f'<tr><th scope="row"><a href="{href}"><bdi>{E(a)} → {E(b)}</bdi></a> <span class="hub-code" dir="ltr">{o}–{d}</span></th>'
                         f'<td class="hub-price" data-from="{o}" data-to="{d}" data-label="{E(L["from_"])}"></td><td><a class="price-go" href="{href}">{E(L["see"])}</a></td></tr>')
            others = [f'<a href="/{x[lang]["path"]}/">{E(re.sub(r"<[^>]+>", "", x[lang]["h1"]))}</a>' for k2, x in THEMES.items() if k2 != key]
            hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
            body = (f'<section class="hub"><h2>{E(t["table"])}</h2><table class="hub-table"><thead><tr><th scope="col">{E(L["th"][0])}</th><th scope="col">{E(L["th"][1])}</th><td></td></tr></thead>'
                    f'<tbody>{rows}</tbody></table></section><script src="/hub.js" defer></script><script src="/fx.js" defer></script>'
                    f'<section><h2>{E(t["tips_h"])}</h2><ul>' + "".join(f"<li>{x}</li>" for x in t["tips"]) + "</ul></section>"
                    f'<section class="faq"><h2>{"Questions fréquentes" if lang == "fr" else "Frequently asked questions"}</h2>' +
                    "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in t["faq"]) + "</section>"
                    f'<section><h2>{E(L["others"])}</h2><p class="pays-links">{" · ".join(others)}</p></section>')
            urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, B.faq_ld(t["faq"]), paths, ctx))
    return urls
