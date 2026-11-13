"""Pages hôtels ajoutées le 13 novembre 2026 : Yaoundé, Libreville, Kigali, Abuja, Brazzaville, Zanzibar.

Pourquoi ces villes : dans la Search Console (15 oct. – 10 nov. 2026), les pages hôtels de villes africaines peu concurrencées
(Bamako, Douala, Lomé) sortent déjà entre les positions 11 et 18 après quatre semaines. Même modèle ici.

Ce module complète les tables des autres fichiers (il ne fabrique aucune page lui-même) :
  - build_pages.HOTELS / HOTELS_FR (français), trajets_en.HOTELS (bloc détaillé en anglais) ;
  - translations.HOTEL_TIPS / AREAS / CITIES / COUNTRIES (anglais, espagnol, portugais, arabe) ;
  - routes_itde.HOTEL_TIPS / AREAS / COUNTRIES (italien, allemand) ;
  - build_i18n.PHOTO_VISITER (photo d'en-tête prise dans site/data/visiter-photos.json).
Contenu : repères généraux (quartiers, position de l'aéroport), sans prix ni règle de visa ou de santé.
"""
import translations as TR
import routes_itde as RX
import trajets_en as TEN

# (ville, pays, [(quartier, description)], conseil, code de l'aéroport)
HOTELS = [
    ("Yaoundé", "Cameroun", [("Centre-ville", "administrations, hôtels d'affaires"), ("Bastos", "résidentiel, ambassades et restaurants"), ("Mont Fébé", "sur les hauteurs, calme, vue sur la ville")],
     "L'aéroport de Yaoundé-Nsimalen est au sud de la ville, à l'écart du centre : prévoyez le trajet, surtout aux heures de pointe.", "NSI"),
    ("Libreville", "Gabon", [("Centre-ville", "bord de mer, administrations, hôtels d'affaires"), ("Quartier Louis", "restaurants et vie nocturne"), ("La Sablière", "résidentiel, proche de la plage et de l'aéroport")],
     "L'aéroport Léon-Mba est au nord de la ville, tout près du bord de mer : les trajets vers les hôtels sont courts.", "LBV"),
    ("Kigali", "Rwanda", [("Kiyovu", "centre-ville, quartier des affaires et hôtels"), ("Kimihurura et Kacyiru", "restaurants, ambassades, centre de conventions"), ("Remera", "animé, proche de l'aéroport et du stade")],
     "L'aéroport de Kigali est à une dizaine de kilomètres du centre : les trajets sont courts, quel que soit le quartier.", "KGL"),
    ("Abuja", "Nigeria", [("Wuse 2", "commerces, restaurants, hôtels de milieu de gamme"), ("Maitama et Asokoro", "résidentiel haut de gamme, ambassades"), ("Central Business District", "quartier des affaires, grands hôtels")],
     "L'aéroport Nnamdi-Azikiwe est loin du centre, à l'ouest de la ville : prévoyez le trajet et réservez un transfert pour une arrivée de nuit.", "ABV"),
    ("Brazzaville", "Congo", [("Centre-ville", "administrations, hôtels d'affaires"), ("Poto-Poto", "animé et populaire, marché"), ("Bacongo", "au bord du fleuve Congo, plus calme")],
     "L'aéroport Maya-Maya est dans la ville : le trajet vers le centre est court.", "BZV"),
    ("Zanzibar", "Tanzanie", [("Stone Town", "vieille ville classée à l'UNESCO, ruelles et marchés"), ("Nungwi et Kendwa", "plages du nord de l'île"), ("Paje et Jambiani", "côte est, lagon et kitesurf")],
     "L'aéroport est tout près de Stone Town ; les plages du nord et de l'est sont à une heure de route ou plus : prévoyez le transfert.", "ZNZ"),
]

# Photo d'en-tête : clé de site/data/visiter-photos.json (Zanzibar a déjà la sienne dans photos.json)
PHOTOS = {"NSI": "cm-yaounde", "LBV": "ga-libreville", "KGL": "rw-kigali", "ABV": "ng-abuja", "BZV": "cg-brazzaville"}

# ---------- conseil de la ville : (anglais, espagnol, portugais, arabe) puis (italien, allemand)
TR.HOTEL_TIPS.update({
    "Yaoundé": ("Yaoundé-Nsimalen Airport is south of the city, away from the centre: allow time for the journey, especially at rush hour.",
                "El aeropuerto de Yaundé-Nsimalen está al sur de la ciudad, lejos del centro: cuenta con el trayecto, sobre todo en hora punta.",
                "O aeroporto de Yaoundé-Nsimalen fica a sul da cidade, afastado do centro: conte com o trajeto, sobretudo nas horas de ponta.",
                "مطار ياوندي-نسيمالين يقع جنوب المدينة بعيدًا عن المركز: احسب وقت الطريق، خصوصًا في ساعات الذروة."),
    "Libreville": ("Léon-Mba Airport is in the north of the city, right by the seafront: journeys to the hotels are short.",
                   "El aeropuerto Léon-Mba está al norte de la ciudad, junto al mar: los trayectos a los hoteles son cortos.",
                   "O aeroporto Léon-Mba fica a norte da cidade, junto ao mar: os trajetos até aos hotéis são curtos.",
                   "مطار ليون مبا يقع شمال المدينة بمحاذاة البحر: الطريق إلى الفنادق قصير."),
    "Kigali": ("Kigali airport is about ten kilometres from the centre: journeys are short whichever area you choose.",
               "El aeropuerto de Kigali está a unos diez kilómetros del centro: los trayectos son cortos sea cual sea el barrio.",
               "O aeroporto de Kigali fica a cerca de dez quilómetros do centro: os trajetos são curtos seja qual for o bairro.",
               "مطار كيغالي يبعد نحو عشرة كيلومترات عن المركز: التنقل قصير أيًّا كان الحي."),
    "Abuja": ("Nnamdi Azikiwe Airport is far from the centre, west of the city: allow time for the journey and book a transfer for a night arrival.",
              "El aeropuerto Nnamdi Azikiwe está lejos del centro, al oeste de la ciudad: cuenta con el trayecto y reserva un traslado si llegas de noche.",
              "O aeroporto Nnamdi Azikiwe fica longe do centro, a oeste da cidade: conte com o trajeto e reserve um transfer para uma chegada à noite.",
              "مطار نامدي أزيكيوي بعيد عن المركز، غرب المدينة: احسب وقت الطريق واحجز نقلًا مسبقًا إذا وصلت ليلًا."),
    "Brazzaville": ("Maya-Maya Airport is inside the city: the journey to the centre is short.",
                    "El aeropuerto Maya-Maya está dentro de la ciudad: el trayecto al centro es corto.",
                    "O aeroporto Maya-Maya fica dentro da cidade: o trajeto até ao centro é curto.",
                    "مطار مايا مايا يقع داخل المدينة: الطريق إلى المركز قصير."),
    "Zanzibar": ("The airport is right next to Stone Town; the beaches in the north and east are an hour's drive or more: plan your transfer.",
                 "El aeropuerto está junto a Stone Town; las playas del norte y del este quedan a una hora de carretera o más: prevé el traslado.",
                 "O aeroporto fica mesmo ao lado de Stone Town; as praias do norte e do leste ficam a uma hora de estrada ou mais: preveja o transfer.",
                 "المطار قريب جدًا من ستون تاون؛ أما شواطئ الشمال والشرق فتبعد ساعة بالسيارة أو أكثر: رتّب النقل مسبقًا."),
})
RX.HOTEL_TIPS.update({
    "Yaoundé": ("L'aeroporto di Yaoundé-Nsimalen è a sud della città, lontano dal centro: calcola il tragitto, soprattutto nelle ore di punta.",
                "Der Flughafen Yaoundé-Nsimalen liegt südlich der Stadt, abseits des Zentrums: Plane die Fahrt ein, besonders zu Stoßzeiten."),
    "Libreville": ("L'aeroporto Léon-Mba è a nord della città, vicino al lungomare: i tragitti verso gli hotel sono brevi.",
                   "Der Flughafen Léon-Mba liegt im Norden der Stadt direkt am Meer: Die Wege zu den Hotels sind kurz."),
    "Kigali": ("L'aeroporto di Kigali è a una decina di chilometri dal centro: i tragitti sono brevi qualunque sia il quartiere.",
               "Der Flughafen Kigali liegt rund zehn Kilometer vom Zentrum entfernt: Die Wege sind kurz, egal in welchem Viertel."),
    "Abuja": ("L'aeroporto Nnamdi Azikiwe è lontano dal centro, a ovest della città: calcola il tragitto e prenota un transfer per un arrivo notturno.",
              "Der Flughafen Nnamdi Azikiwe liegt weit vom Zentrum entfernt, westlich der Stadt: Plane die Fahrt ein und buche bei Ankunft in der Nacht einen Transfer."),
    "Brazzaville": ("L'aeroporto Maya-Maya è dentro la città: il tragitto verso il centro è breve.",
                    "Der Flughafen Maya-Maya liegt mitten in der Stadt: Der Weg ins Zentrum ist kurz."),
    "Zanzibar": ("L'aeroporto è accanto a Stone Town; le spiagge del nord e dell'est sono a un'ora di strada o più: organizza il transfer.",
                 "Der Flughafen liegt direkt bei Stone Town; die Strände im Norden und Osten sind eine Autostunde oder mehr entfernt: Plane den Transfer ein."),
})

# ---------- descriptions des quartiers : français -> (en, es, pt, ar) et (it, de)
_AREAS = {
    "administrations, hôtels d'affaires": (("government offices, business hotels", "administración, hoteles de negocios", "administração, hotéis de negócios", "إدارات وفنادق أعمال"),
                                           ("uffici pubblici, hotel d'affari", "Behörden, Businesshotels")),
    "bord de mer, administrations, hôtels d'affaires": (("seafront, government offices, business hotels", "frente al mar, administración, hoteles de negocios", "à beira-mar, administração, hotéis de negócios", "على البحر، إدارات وفنادق أعمال"),
                                                        ("lungomare, uffici pubblici, hotel d'affari", "am Meer, Behörden, Businesshotels")),
    "résidentiel, ambassades et restaurants": (("residential, embassies and restaurants", "residencial, embajadas y restaurantes", "residencial, embaixadas e restaurantes", "سكني، سفارات ومطاعم"),
                                               ("residenziale, ambasciate e ristoranti", "Wohnviertel, Botschaften und Restaurants")),
    "sur les hauteurs, calme, vue sur la ville": (("on the hills, quiet, views over the city", "en las alturas, tranquilo, vistas a la ciudad", "nas colinas, calmo, vista sobre a cidade", "على المرتفعات، هادئ، إطلالة على المدينة"),
                                                  ("in collina, tranquillo, vista sulla città", "auf den Hügeln, ruhig, Blick über die Stadt")),
    "restaurants et vie nocturne": (("restaurants and nightlife", "restaurantes y vida nocturna", "restaurantes e vida noturna", "مطاعم وحياة ليلية"),
                                    ("ristoranti e vita notturna", "Restaurants und Nachtleben")),
    "résidentiel, proche de la plage et de l'aéroport": (("residential, close to the beach and the airport", "residencial, cerca de la playa y del aeropuerto", "residencial, perto da praia e do aeroporto", "سكني، قريب من الشاطئ والمطار"),
                                                         ("residenziale, vicino alla spiaggia e all'aeroporto", "Wohnviertel, nah an Strand und Flughafen")),
    "centre-ville, quartier des affaires et hôtels": (("city centre, business district and hotels", "centro, barrio de negocios y hoteles", "centro, bairro de negócios e hotéis", "وسط المدينة، حي الأعمال والفنادق"),
                                                      ("centro città, quartiere degli affari e hotel", "Stadtzentrum, Geschäftsviertel und Hotels")),
    "restaurants, ambassades, centre de conventions": (("restaurants, embassies, convention centre", "restaurantes, embajadas, centro de convenciones", "restaurantes, embaixadas, centro de convenções", "مطاعم، سفارات، مركز المؤتمرات"),
                                                       ("ristoranti, ambasciate, centro congressi", "Restaurants, Botschaften, Kongresszentrum")),
    "animé, proche de l'aéroport et du stade": (("lively, close to the airport and the stadium", "animado, cerca del aeropuerto y del estadio", "animado, perto do aeroporto e do estádio", "حيوي، قريب من المطار والملعب"),
                                                ("vivace, vicino all'aeroporto e allo stadio", "lebhaft, nah an Flughafen und Stadion")),
    "commerces, restaurants, hôtels de milieu de gamme": (("shops, restaurants, mid-range hotels", "comercios, restaurantes, hoteles de gama media", "comércio, restaurantes, hotéis de gama média", "متاجر، مطاعم، فنادق متوسطة"),
                                                          ("negozi, ristoranti, hotel di fascia media", "Geschäfte, Restaurants, Mittelklassehotels")),
    "résidentiel haut de gamme, ambassades": (("upscale residential, embassies", "residencial de alto nivel, embajadas", "residencial de alto padrão, embaixadas", "سكني راقٍ، سفارات"),
                                              ("residenziale di alto livello, ambasciate", "gehobenes Wohnviertel, Botschaften")),
    "quartier des affaires, grands hôtels": (("business district, large hotels", "barrio de negocios, grandes hoteles", "bairro de negócios, grandes hotéis", "حي الأعمال، فنادق كبرى"),
                                             ("quartiere degli affari, grandi hotel", "Geschäftsviertel, große Hotels")),
    "animé et populaire, marché": (("lively and popular, market", "animado y popular, mercado", "animado e popular, mercado", "حيوي وشعبي، سوق"),
                                   ("vivace e popolare, mercato", "lebhaft und volkstümlich, Markt")),
    "au bord du fleuve Congo, plus calme": (("by the Congo River, quieter", "a orillas del río Congo, más tranquilo", "à beira do rio Congo, mais calmo", "على ضفة نهر الكونغو، أهدأ"),
                                            ("sul fiume Congo, più tranquillo", "am Kongo, ruhiger")),
    "vieille ville classée à l'UNESCO, ruelles et marchés": (("UNESCO-listed old town, alleys and markets", "casco antiguo declarado por la UNESCO, callejuelas y mercados", "cidade velha classificada pela UNESCO, ruelas e mercados", "المدينة القديمة المدرجة في اليونسكو، أزقة وأسواق"),
                                                             ("città vecchia patrimonio UNESCO, vicoli e mercati", "UNESCO-Altstadt, Gassen und Märkte")),
    "plages du nord de l'île": (("beaches in the north of the island", "playas del norte de la isla", "praias do norte da ilha", "شواطئ شمال الجزيرة"),
                                ("spiagge del nord dell'isola", "Strände im Norden der Insel")),
    "côte est, lagon et kitesurf": (("east coast, lagoon and kitesurfing", "costa este, laguna y kitesurf", "costa leste, lagoa e kitesurf", "الساحل الشرقي، بحيرة شاطئية ورياضة الكايت سيرف"),
                                    ("costa orientale, laguna e kitesurf", "Ostküste, Lagune und Kitesurfen")),
}
for _fr, (_a, _b) in _AREAS.items():
    TR.AREAS.setdefault(_fr, _a)
    RX.AREAS.setdefault(_fr, _b)

# ---------- noms de pays quand ils manquaient (les noms de villes viennent déjà de routes_extra et de villes)
for _k, _v in {"Rwanda": ("Rwanda", "Ruanda", "Ruanda", "رواندا"), "Nigeria": ("Nigeria", "Nigeria", "Nigéria", "نيجيريا"),
               "Congo": ("Congo", "Congo", "Congo", "الكونغو"), "Tanzanie": ("Tanzania", "Tanzania", "Tanzânia", "تنزانيا")}.items():
    TR.COUNTRIES.setdefault(_k, _v)
for _k, _v in {"Rwanda": ("Ruanda", "Ruanda"), "Nigeria": ("Nigeria", "Nigeria"), "Congo": ("Congo", "Kongo"), "Tanzanie": ("Tanzania", "Tansania")}.items():
    RX.COUNTRIES.setdefault(_k, _v)

# ---------- bloc détaillé en français (« Séjourner à … : ce qu'il faut savoir »)
_LIBRE = ("Faut-il préférer un appartement ?", "Pour un séjour d'une semaine ou plus, un appartement meublé avec cuisine revient souvent moins cher par nuit qu'un hôtel, surtout en famille.")
FR = {
    "Yaoundé": dict(
        intro="Yaoundé est la capitale du Cameroun, bâtie sur des collines. Les hôtels d'affaires sont dans le centre-ville ; Bastos, plus résidentiel, réunit ambassades et restaurants. L'aéroport de Nsimalen est au sud de la ville, à l'écart du centre.",
        tips=["La circulation est dense aux heures de pointe : choisissez un hôtel proche de vos rendez-vous.",
              "Pour une arrivée de nuit, réservez à l'avance le transfert depuis l'aéroport.",
              "Si votre famille est plus proche de Douala, comparez aussi les vols vers Douala (DLA)."],
        faq=[("Où loger à Yaoundé ?", "Dans le centre-ville pour les administrations et les hôtels d'affaires ; à Bastos pour un quartier résidentiel avec restaurants ; vers le mont Fébé pour le calme."),
             ("L'aéroport est-il loin de Yaoundé ?", "L'aéroport de Yaoundé-Nsimalen est au sud de la ville, à l'écart du centre : prévoyez le trajet, surtout aux heures de pointe."), _LIBRE],
        more=[]),
    "Libreville": dict(
        intro="Libreville s'étire le long de l'océan. Les hôtels d'affaires sont en centre-ville, sur le bord de mer ; le quartier Louis est connu pour ses restaurants et ses sorties ; La Sablière, au nord, est résidentielle et proche de l'aéroport.",
        tips=["L'aéroport Léon-Mba est dans la ville, au nord : les trajets vers les hôtels sont courts.",
              "Les hôtels du bord de mer sont pratiques pour un court séjour d'affaires.",
              "Comparez les prix avec annulation gratuite : vous pourrez changer si le tarif baisse."],
        faq=[("Où loger à Libreville ?", "En centre-ville, sur le bord de mer, pour les affaires ; au quartier Louis pour les restaurants ; à La Sablière pour un quartier résidentiel proche de la plage et de l'aéroport."),
             ("L'aéroport est-il loin du centre de Libreville ?", "Non : l'aéroport Léon-Mba est au nord de la ville, tout près du bord de mer."), _LIBRE],
        more=[]),
    "Kigali": dict(
        intro="Kigali est une ville de collines, compacte. On loge dans le centre (Kiyovu) pour les affaires, à Kimihurura ou Kacyiru pour les restaurants et les ambassades, ou à Remera, près de l'aéroport. L'aéroport est à une dizaine de kilomètres du centre.",
        tips=["La ville est vallonnée : regardez la carte avant de choisir un hôtel si vous comptez marcher.",
              "Les trajets sont courts d'un quartier à l'autre : inutile de payer plus cher pour être au centre.",
              "Pour une arrivée de nuit, demandez à l'hôtel d'organiser le transfert."],
        faq=[("Où loger à Kigali ?", "À Kiyovu, dans le centre, pour les affaires ; à Kimihurura et Kacyiru pour les restaurants et les ambassades ; à Remera pour être près de l'aéroport."),
             ("À quelle distance est l'aéroport de Kigali ?", "À une dizaine de kilomètres du centre : le trajet est court."), _LIBRE],
        more=[]),
    "Abuja": dict(
        intro="Abuja est la capitale du Nigeria, une ville récente et étendue. Wuse 2 réunit commerces, restaurants et hôtels de milieu de gamme ; Maitama et Asokoro sont résidentiels ; les grands hôtels sont dans le quartier des affaires. L'aéroport est loin du centre, à l'ouest de la ville.",
        tips=["Réservez le transfert depuis l'aéroport à l'avance, surtout pour une arrivée de nuit : le trajet est long.",
              "La ville est étendue : choisissez un hôtel proche de vos rendez-vous.",
              "Comparez aussi les vols vers Lagos (LOS) : l'offre est plus large, puis un vol intérieur relie les deux villes."],
        faq=[("Où loger à Abuja ?", "À Wuse 2 pour les commerces et les restaurants ; à Maitama ou Asokoro pour un quartier résidentiel ; dans le Central Business District pour les grands hôtels d'affaires."),
             ("L'aéroport est-il loin d'Abuja ?", "Oui : l'aéroport Nnamdi-Azikiwe est à l'ouest de la ville, loin du centre. Prévoyez le trajet et un transfert réservé à l'avance."), _LIBRE],
        more=[]),
    "Brazzaville": dict(
        intro="Brazzaville est au bord du fleuve Congo, en face de Kinshasa. Les hôtels d'affaires sont dans le centre-ville ; Poto-Poto est le quartier animé et populaire ; Bacongo, près du fleuve, est plus calme. L'aéroport Maya-Maya est dans la ville.",
        tips=["L'aéroport est tout proche du centre : un hôtel central convient même pour une arrivée tardive.",
              "Pour une arrivée de nuit, demandez à l'hôtel d'organiser le transfert.",
              "Comparez les prix avec annulation gratuite : vous pourrez changer si le tarif baisse."],
        faq=[("Où loger à Brazzaville ?", "Dans le centre-ville pour les affaires ; à Poto-Poto pour un quartier animé ; à Bacongo, près du fleuve, pour plus de calme."),
             ("L'aéroport est-il loin du centre de Brazzaville ?", "Non : l'aéroport Maya-Maya est dans la ville, le trajet vers le centre est court."), _LIBRE],
        more=[]),
    "Zanzibar": dict(
        intro="À Zanzibar, on choisit entre la vieille ville et les plages. Stone Town, classée à l'UNESCO, se visite à pied ; Nungwi et Kendwa sont les plages du nord ; Paje et Jambiani, sur la côte est, attirent les amateurs de lagon et de kitesurf. L'aéroport est tout près de Stone Town.",
        tips=["Les plages du nord et de l'est sont à une heure de route ou plus de l'aéroport : réservez le transfert avec l'hôtel.",
              "Beaucoup de voyageurs passent une ou deux nuits à Stone Town, puis le reste du séjour sur une plage.",
              "Sur la côte est, la mer se retire loin à marée basse : regardez les horaires des marées si vous voulez nager."],
        faq=[("Où loger à Zanzibar ?", "À Stone Town pour la vieille ville ; à Nungwi ou Kendwa pour les plages du nord ; à Paje ou Jambiani pour la côte est, son lagon et le kitesurf."),
             ("L'aéroport est-il loin des plages de Zanzibar ?", "L'aéroport est tout près de Stone Town, mais les plages du nord et de l'est sont à une heure de route ou plus."), _LIBRE],
        more=[]),
}

# ---------- bloc détaillé en anglais (« Staying in … : what to know »)
_FREE = ("Is an apartment a better choice?", "For a stay of a week or more, a furnished apartment with a kitchen often costs less per night than a hotel, especially for a family.")
EN = {
    "Yaoundé": dict(
        intro="Yaoundé is the capital of Cameroon, built on hills. Business hotels are in the city centre; Bastos is more residential, with embassies and restaurants. Nsimalen Airport is south of the city, away from the centre.",
        tips=["Traffic is heavy at rush hour: choose a hotel close to your meetings.",
              "For a night arrival, book your airport transfer in advance.",
              "If your family lives closer to Douala, compare flights to Douala (DLA) too."],
        faq=[("Where to stay in Yaoundé?", "The city centre for government offices and business hotels; Bastos for a residential area with restaurants; around Mont Fébé for a quiet stay."),
             ("Is the airport far from Yaoundé?", "Yaoundé-Nsimalen Airport is south of the city, away from the centre: allow time for the journey, especially at rush hour."), _FREE]),
    "Libreville": dict(
        intro="Libreville stretches along the ocean. Business hotels are in the city centre, on the seafront; the Louis district is known for restaurants and nightlife; La Sablière, to the north, is residential and close to the airport.",
        tips=["Léon-Mba Airport is in the north of the city: journeys to the hotels are short.",
              "Seafront hotels are practical for a short business stay.",
              "Compare prices with free cancellation: you can rebook if the rate drops."],
        faq=[("Where to stay in Libreville?", "The city centre and seafront for business; the Louis district for restaurants; La Sablière for a residential area close to the beach and the airport."),
             ("Is the airport far from the centre of Libreville?", "No: Léon-Mba Airport is in the north of the city, right by the seafront."), _FREE]),
    "Kigali": dict(
        intro="Kigali is a compact city of hills. Visitors stay in the centre (Kiyovu) for business, in Kimihurura or Kacyiru for restaurants and embassies, or in Remera near the airport. The airport is about ten kilometres from the centre.",
        tips=["The city is hilly: check the map before choosing a hotel if you plan to walk.",
              "Journeys between districts are short: there is no need to pay more to be central.",
              "For a night arrival, ask your hotel to arrange the transfer."],
        faq=[("Where to stay in Kigali?", "Kiyovu, in the centre, for business; Kimihurura and Kacyiru for restaurants and embassies; Remera to be close to the airport."),
             ("How far is Kigali airport from the city?", "About ten kilometres from the centre: the journey is short."), _FREE]),
    "Abuja": dict(
        intro="Abuja is Nigeria's capital, a recent and spread-out city. Wuse 2 has shops, restaurants and mid-range hotels; Maitama and Asokoro are residential; the large hotels are in the business district. The airport is far from the centre, west of the city.",
        tips=["Book your airport transfer in advance, especially for a night arrival: the journey is long.",
              "The city is spread out: choose a hotel close to your meetings.",
              "Compare flights to Lagos (LOS) too: there are more of them, and a domestic flight links the two cities."],
        faq=[("Where to stay in Abuja?", "Wuse 2 for shops and restaurants; Maitama or Asokoro for a residential area; the Central Business District for the large business hotels."),
             ("Is the airport far from Abuja?", "Yes: Nnamdi Azikiwe Airport is west of the city, far from the centre. Allow time for the journey and book a transfer in advance."), _FREE]),
    "Brazzaville": dict(
        intro="Brazzaville lies on the Congo River, facing Kinshasa. Business hotels are in the city centre; Poto-Poto is the lively, popular district; Bacongo, near the river, is quieter. Maya-Maya Airport is inside the city.",
        tips=["The airport is very close to the centre: a central hotel works well even for a late arrival.",
              "For a night arrival, ask your hotel to arrange the transfer.",
              "Compare prices with free cancellation: you can rebook if the rate drops."],
        faq=[("Where to stay in Brazzaville?", "The city centre for business; Poto-Poto for a lively area; Bacongo, near the river, for a quieter stay."),
             ("Is the airport far from the centre of Brazzaville?", "No: Maya-Maya Airport is inside the city, and the journey to the centre is short."), _FREE]),
    "Zanzibar": dict(
        intro="In Zanzibar you choose between the old town and the beaches. UNESCO-listed Stone Town is explored on foot; Nungwi and Kendwa are the northern beaches; Paje and Jambiani, on the east coast, attract lagoon lovers and kitesurfers. The airport is right next to Stone Town.",
        tips=["The northern and eastern beaches are an hour's drive or more from the airport: book the transfer with your hotel.",
              "Many travellers spend a night or two in Stone Town, then the rest of the stay on a beach.",
              "On the east coast the sea goes out a long way at low tide: check the tide times if you want to swim."],
        faq=[("Where to stay in Zanzibar?", "Stone Town for the old town; Nungwi or Kendwa for the northern beaches; Paje or Jambiani for the east coast, its lagoon and kitesurfing."),
             ("Is the airport far from the beaches in Zanzibar?", "The airport is right next to Stone Town, but the northern and eastern beaches are an hour's drive or more away."), _FREE]),
}
TEN.HOTELS.update(EN)
