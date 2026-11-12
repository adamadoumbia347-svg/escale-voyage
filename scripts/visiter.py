"""« Que visiter » : explorer le monde pays par pays (demande de Dobam, 12 novembre 2026).
  /visiter/            tous les pays, par région
  /visiter/<pays>/     un pays : ses villes et ses lieux à voir, chacun avec une vraie photo créditée
Photos : Wikimedia Commons, licences libres ; auteur et licence dans site/data/visiter-photos.json (repris sur /credits-photos/).
Règles : aucun prix, aucune règle de visa, de santé ou de sécurité ; uniquement des repères stables (lieu, ce qu'on y voit, classement UNESCO).
Un lieu sans photo n'est pas publié ; un pays avec moins de 4 lieux en photo n'est pas publié.
Les lieux situés dans des zones déconseillées par les conseils aux voyageurs officiels ne sont pas publiés (voir RETIRES plus bas)."""
import html
import json

import build_i18n as B

E = html.escape
P = lambda cc, key, nom, kind, txt: dict(key=f"{cc}-{key}", nom=nom, kind=kind, txt=txt)

PAYS = [
    dict(cc="ci", slug="cote-d-ivoire", nom="Côte d'Ivoire", en="en Côte d'Ivoire", de="de la Côte d'Ivoire", flag="🇨🇮", air="ABJ", ville="Abidjan", region="Afrique",
         accroche="Une capitale économique au bord de la lagune, la plus grande basilique du monde, des villes coloniales classées et des plages bordées de cocotiers.",
         lieux=[P("ci", "abidjan", "Abidjan", "Ville", "La capitale économique s'étire autour de la lagune Ébrié. Le quartier du <strong>Plateau</strong> aligne ses tours au bord de l'eau, face à Cocody et Treichville."),
                P("ci", "stpaul", "Cathédrale Saint-Paul", "Monument", "Au Plateau, une cathédrale à l'architecture audacieuse, consacrée en <strong>1985</strong>, avec ses grands vitraux et sa vue sur la lagune."),
                P("ci", "basilique", "Yamoussoukro", "Capitale", "La capitale politique abrite la <strong>basilique Notre-Dame-de-la-Paix</strong>, consacrée en 1990 et souvent présentée comme la plus grande église du monde."),
                P("ci", "bassam", "Grand-Bassam", "Ville historique", "L'ancienne capitale coloniale, à l'est d'Abidjan : maisons anciennes, artisans et plage. Ici, l'ancien palais du gouverneur, devenu <strong>musée national du Costume</strong>. Sa ville historique est classée à l'<strong>UNESCO depuis 2012</strong>."),
                P("ci", "assinie", "Assinie", "Plage", "Une bande de sable entre l'océan et la lagune, à l'est du pays : cocotiers, pirogues et week-ends au bord de l'eau."),
                P("ci", "man", "Man", "Montagne", "À l'ouest, la « ville aux 18 montagnes » : cascades, forêt, ponts de lianes et la silhouette de la <strong>Dent de Man</strong>."),
                P("ci", "sanpedro", "San-Pédro", "Plage", "Un grand port du sud-ouest et, autour, de longues plages sauvages face à l'Atlantique."),
                P("ci", "sassandra", "Sassandra", "Plage", "Une petite ville de pêcheurs à l'embouchure du fleuve du même nom : cocotiers, pirogues et plages tranquilles."),
                P("ci", "tai", "Parc national de Taï", "Nature", "Dans le sud-ouest, l'une des dernières grandes forêts primaires d'Afrique de l'Ouest, refuge de chimpanzés. Classé à l'<strong>UNESCO depuis 1982</strong>."),
                P("ci", "korhogo", "Korhogo", "Culture", "La grande ville du nord, au cœur du pays sénoufo : tisserands, toiles peintes et sculpteurs.")]),
    dict(cc="sn", slug="senegal", nom="Sénégal", en="au Sénégal", de="du Sénégal", flag="🇸🇳", air="DSS", ville="Dakar", region="Afrique",
         accroche="Le pays de la Teranga : une capitale sur l'océan, des îles chargées d'histoire, un lac rose et des deltas où l'on circule en pirogue.",
         lieux=[P("sn", "dakar", "Dakar", "Capitale", "Posée sur une presqu'île, la capitale regarde l'Atlantique. Le <strong>monument de la Renaissance africaine</strong>, inauguré en 2010, domine la ville."),
                P("sn", "goree", "Île de Gorée", "Histoire", "À quelques minutes de bateau de Dakar, une île sans voitures aux maisons colorées, lieu de mémoire de la traite. Classée à l'<strong>UNESCO depuis 1978</strong>."),
                P("sn", "lacrose", "Lac Rose", "Nature", "Le lac Retba, au nord-est de Dakar, prend des teintes roses selon la saison et la lumière. On y récolte le sel à la main."),
                P("sn", "saintlouis", "Saint-Louis", "Ville historique", "L'ancienne capitale, sur une île du fleuve Sénégal, reliée par le <strong>pont Faidherbe</strong>. Classée à l'UNESCO depuis <strong>2000</strong>."),
                P("sn", "saloum", "Sine Saloum", "Nature", "Un delta de mangroves, d'îles et de bras de mer que l'on parcourt en pirogue. Classé à l'<strong>UNESCO depuis 2011</strong>."),
                P("sn", "casamance", "Cap Skirring", "Plage", "En Casamance, au sud du pays : de longues plages de sable clair bordées de palmiers."),
                P("sn", "touba", "Touba", "Spiritualité", "La ville sainte du mouridisme et sa <strong>Grande Mosquée</strong>, l'une des plus vastes d'Afrique de l'Ouest."),
                P("sn", "saly", "Saly", "Plage", "Sur la Petite Côte, au sud de Dakar : la station balnéaire la plus connue du pays.")]),
    dict(cc="ma", slug="maroc", nom="Maroc", en="au Maroc", de="du Maroc", flag="🇲🇦", air="RAK", ville="Marrakech", region="Afrique",
         accroche="Médinas, montagnes, dunes et océan : des villes impériales aux portes du désert.",
         lieux=[P("ma", "marrakech", "Marrakech", "Ville", "La place <strong>Jemaa el-Fna</strong> s'anime chaque soir : conteurs, musiciens, étals. La médina est classée à l'UNESCO depuis <strong>1985</strong>."),
                P("ma", "chefchaouen", "Chefchaouen", "Ville", "Dans le Rif, une petite ville aux ruelles peintes en <strong>bleu</strong>, du sol jusqu'aux portes."),
                P("ma", "fes", "Fès", "Ville impériale", "L'une des plus grandes médinas du monde, classée à l'UNESCO depuis <strong>1981</strong>, et ses tanneries à ciel ouvert."),
                P("ma", "casablanca", "Casablanca", "Ville", "La capitale économique et sa <strong>mosquée Hassan II</strong>, achevée en 1993 au bord de l'océan : son minaret mesure 210 m."),
                P("ma", "merzouga", "Merzouga", "Désert", "Aux portes du Sahara, les grandes dunes de l'<strong>erg Chebbi</strong> : lever de soleil sur le sable et nuits en bivouac."),
                P("ma", "essaouira", "Essaouira", "Océan", "Une ville fortifiée face à l'Atlantique, connue pour son port, ses remparts et son vent. Médina classée à l'UNESCO depuis <strong>2001</strong>."),
                P("ma", "aitbenhaddou", "Aït-Ben-Haddou", "Patrimoine", "Un village fortifié en terre, sur l'ancienne route des caravanes. Classé à l'<strong>UNESCO depuis 1987</strong>, il a servi de décor à de nombreux films."),
                P("ma", "rabat", "Rabat", "Capitale", "La capitale, au bord de l'océan : la <strong>tour Hassan</strong>, minaret inachevé du XII<sup>e</sup> siècle, et la kasbah des Oudayas.")]),
    dict(cc="ke", slug="kenya", nom="Kenya", en="au Kenya", de="du Kenya", flag="🇰🇪", air="NBO", ville="Nairobi", region="Afrique",
         accroche="Safaris, flamants roses, sommets enneigés et plages de l'océan Indien.",
         lieux=[P("ke", "mara", "Maasai Mara", "Safari", "La réserve la plus célèbre du pays, dans le sud-ouest : lions, guépards, éléphants et grands troupeaux de gnous."),
                P("ke", "amboseli", "Amboseli", "Safari", "Des troupeaux d'éléphants avec, en toile de fond, le <strong>Kilimandjaro</strong>, de l'autre côté de la frontière."),
                P("ke", "nairobi", "Nairobi", "Capitale", "Un <strong>parc national aux portes de la ville</strong> : on y voit des girafes devant les gratte-ciel."),
                P("ke", "nakuru", "Lac Nakuru", "Nature", "Un lac de la vallée du Rift connu pour ses flamants roses. Les lacs kényans du Rift sont classés à l'<strong>UNESCO depuis 2011</strong>."),
                P("ke", "mountkenya", "Mont Kenya", "Montagne", "<strong>5 199 m</strong> : le deuxième sommet d'Afrique, classé à l'UNESCO depuis <strong>1997</strong>."),
                P("ke", "lamu", "Lamu", "Ville historique", "Une vieille ville swahilie sur une île, aux ruelles étroites. Classée à l'<strong>UNESCO depuis 2001</strong>."),
                P("ke", "diani", "Diani Beach", "Plage", "Sable blanc et océan Indien, au sud de Mombasa."),
                P("ke", "mombasa", "Mombasa", "Ville", "Le grand port de la côte et son <strong>Fort Jésus</strong>, bâti par les Portugais à la fin du XVI<sup>e</sup> siècle, classé à l'UNESCO depuis 2011.")]),
    dict(cc="eg", slug="egypte", nom="Égypte", en="en Égypte", de="de l'Égypte", flag="🇪🇬", air="CAI", ville="Le Caire", region="Afrique",
         accroche="Les pyramides, les temples du Nil et la mer Rouge : plusieurs millénaires d'histoire le long d'un fleuve.",
         lieux=[P("eg", "gizeh", "Pyramides de Gizeh", "Antiquité", "Aux portes du Caire, les trois grandes pyramides. Celle de <strong>Khéops</strong> est la seule des Sept Merveilles du monde antique encore debout."),
                P("eg", "sphinx", "Le Sphinx", "Antiquité", "Un lion à tête humaine taillé dans la roche, au pied des pyramides."),
                P("eg", "caire", "Le Caire", "Capitale", "Une immense capitale au bord du Nil. Le <strong>Caire historique</strong> est classé à l'UNESCO depuis 1979."),
                P("eg", "louxor", "Louxor", "Antiquité", "L'ancienne Thèbes : le temple de <strong>Karnak</strong>, son allée de sphinx à tête de bélier et sa salle aux colonnes géantes, sur la rive est du Nil."),
                P("eg", "abousimbel", "Abou Simbel", "Antiquité", "Deux temples creusés dans la roche sous Ramsès II, <strong>déplacés dans les années 1960</strong> pour les sauver des eaux du lac Nasser."),
                P("eg", "assouan", "Assouan", "Nil", "La grande ville du sud, au bord du Nil, et le temple de <strong>Philae</strong>, posé sur une île."),
                P("eg", "alexandrie", "Alexandrie", "Ville", "La grande ville de la Méditerranée et la <strong>citadelle de Qaitbay</strong>, bâtie à l'emplacement de l'ancien phare."),
                P("eg", "merrouge", "Mer Rouge", "Plage", "Autour d'Hurghada : plages, eau claire et fonds marins réputés pour la plongée.")]),
    dict(cc="it", slug="italie", nom="Italie", en="en Italie", de="de l'Italie", flag="🇮🇹", air="FCO", ville="Rome", region="Europe",
         accroche="Ruines antiques, villes d'art, villages colorés au bord de la mer : chaque région a son décor.",
         lieux=[P("it", "rome", "Rome", "Capitale", "Le <strong>Colisée</strong>, achevé en l'an 80, pouvait accueillir des dizaines de milliers de spectateurs. Le centre historique est classé à l'UNESCO."),
                P("it", "venise", "Venise", "Ville", "Une ville bâtie sur l'eau : ici, pas de voitures, on circule à pied et en bateau. Classée à l'UNESCO depuis <strong>1987</strong>."),
                P("it", "florence", "Florence", "Ville d'art", "Le berceau de la Renaissance et la coupole de sa cathédrale, achevée au XV<sup>e</sup> siècle. Centre classé à l'UNESCO depuis <strong>1982</strong>."),
                P("it", "milan", "Milan", "Ville", "La capitale de la mode et son <strong>Duomo</strong>, une cathédrale gothique de marbre dont la construction a duré près de six siècles."),
                P("it", "cinqueterre", "Cinque Terre", "Bord de mer", "Cinq villages colorés accrochés à la falaise, en Ligurie. Classés à l'<strong>UNESCO depuis 1997</strong>."),
                P("it", "amalfi", "Côte amalfitaine", "Bord de mer", "Au sud de Naples, des villages en terrasses au-dessus de la mer, comme <strong>Positano</strong>. Classée à l'UNESCO depuis 1997."),
                P("it", "pise", "Pise", "Monument", "La <strong>tour penchée</strong>, clocher de la cathédrale, sur une place classée à l'UNESCO depuis 1987."),
                P("it", "pompei", "Pompéi", "Antiquité", "Une ville romaine ensevelie par l'éruption du Vésuve en <strong>79</strong>, et conservée sous la cendre.")]),
    dict(cc="nl", slug="pays-bas", nom="Pays-Bas", en="aux Pays-Bas", de="des Pays-Bas", flag="🇳🇱", air="AMS", ville="Amsterdam", region="Europe",
         accroche="Canaux, moulins, tulipes et vélos : la Hollande, et tout le reste du pays.",
         lieux=[P("nl", "canaux", "Amsterdam", "Capitale", "Des maisons étroites au bord de l'eau. Les canaux du XVII<sup>e</sup> siècle sont classés à l'<strong>UNESCO depuis 2010</strong>."),
                P("nl", "rijks", "Le Rijksmuseum", "Musée", "Le grand musée d'Amsterdam, où l'on voit <strong>La Ronde de nuit</strong> de Rembrandt."),
                P("nl", "kinderdijk", "Kinderdijk", "Patrimoine", "<strong>19 moulins à vent</strong> alignés le long de l'eau, classés à l'UNESCO depuis 1997."),
                P("nl", "tulipes", "Lisse", "Nature", "Au printemps, les champs de tulipes dessinent des bandes de couleurs à perte de vue."),
                P("nl", "keukenhof", "Keukenhof", "Jardin", "Un immense parc de fleurs, <strong>ouvert seulement au printemps</strong>."),
                P("nl", "giethoorn", "Giethoorn", "Village", "Des maisons au toit de chaume et des canaux : ici, on se déplace en barque."),
                P("nl", "rotterdam", "Rotterdam", "Ville", "Le grand port du pays, à l'architecture moderne : les <strong>maisons cubes</strong> jaunes sont penchées sur la pointe."),
                P("nl", "lahaye", "La Haye", "Ville", "Le siège du gouvernement : le <strong>Binnenhof</strong>, ensemble de bâtiments anciens au bord d'un étang.")]),
    dict(cc="jp", slug="japon", nom="Japon", en="au Japon", de="du Japon", flag="🇯🇵", air="NRT", ville="Tokyo", region="Asie",
         accroche="Néons et temples, cerfs en liberté et sanctuaires sur l'eau : de Tokyo à Hiroshima.",
         lieux=[P("jp", "shibuya", "Tokyo", "Capitale", "À <strong>Shibuya</strong>, le passage piéton le plus célèbre du monde : tout le monde traverse en même temps."),
                P("jp", "sensoji", "Asakusa", "Temple", "Le <strong>Sensō-ji</strong>, le plus ancien temple de Tokyo, et sa grande lanterne rouge."),
                P("jp", "fuji", "Mont Fuji", "Montagne", "<strong>3 776 m</strong>, le sommet du Japon, classé à l'UNESCO depuis <strong>2013</strong>. Ici vu depuis la pagode Chūreitō."),
                P("jp", "kyoto", "Kyoto", "Ville", "L'ancienne capitale impériale. Au sanctuaire <strong>Fushimi Inari</strong>, des milliers de portiques rouges forment un tunnel sur la colline."),
                P("jp", "kinkakuji", "Kinkaku-ji", "Temple", "À Kyoto, le <strong>Pavillon d'or</strong> : ses étages recouverts de feuilles d'or se reflètent dans l'étang."),
                P("jp", "osaka", "Osaka", "Ville", "La grande ville du Kansai, réputée pour sa cuisine de rue, et son <strong>château</strong> entouré de douves."),
                P("jp", "nara", "Nara", "Ville historique", "Des cerfs en liberté dans le parc, et le <strong>Tōdai-ji</strong>, qui abrite un Bouddha géant de bronze."),
                P("jp", "miyajima", "Miyajima", "Sanctuaire", "Près d'Hiroshima, le grand portique rouge du sanctuaire d'<strong>Itsukushima</strong> semble flotter à marée haute. Classé à l'UNESCO depuis 1996.")]),
    dict(cc="th", slug="thailande", nom="Thaïlande", en="en Thaïlande", de="de la Thaïlande", flag="🇹🇭", air="BKK", ville="Bangkok", region="Asie",
         accroche="Temples dorés, anciennes capitales en ruines et îles aux falaises de calcaire.",
         lieux=[P("th", "bangkok", "Bangkok", "Capitale", "Au bord du fleuve Chao Phraya, le <strong>Wat Arun</strong>, le temple de l'Aube, et sa tour couverte de porcelaine."),
                P("th", "palais", "Grand Palais", "Monument", "À Bangkok, l'ancien palais des rois, fondé en <strong>1782</strong>, et le temple du Bouddha d'émeraude."),
                P("th", "ayutthaya", "Ayutthaya", "Histoire", "L'ancienne capitale du royaume de Siam, au nord de Bangkok : des temples en ruines classés à l'<strong>UNESCO depuis 1991</strong>."),
                P("th", "chiangmai", "Chiang Mai", "Ville", "La grande ville du nord, entourée de montagnes. Le temple doré de <strong>Doi Suthep</strong> la domine."),
                P("th", "chiangrai", "Chiang Rai", "Temple", "Le <strong>Wat Rong Khun</strong>, ou temple blanc : une œuvre contemporaine entièrement blanche, ouverte en 1997."),
                P("th", "phuket", "Phuket", "Plage", "La plus grande île du pays, dans la mer d'Andaman : de longues plages de sable."),
                P("th", "phiphi", "Îles Phi Phi", "Îles", "Des falaises de calcaire qui plongent dans une eau turquoise, entre Phuket et Krabi."),
                P("th", "krabi", "Krabi", "Plage", "La plage de <strong>Railay</strong>, entourée de falaises : on y arrive en bateau.")]),
    dict(cc="id", slug="indonesie", nom="Indonésie", en="en Indonésie", de="de l'Indonésie", flag="🇮🇩", air="DPS", ville="Bali", region="Asie",
         accroche="Bali et ses temples, mais aussi les volcans de Java, Borobudur et les dragons de Komodo.",
         lieux=[P("id", "ulundanu", "Bali", "Île", "Le temple d'<strong>Ulun Danu Bratan</strong>, posé sur un lac de montagne. Il figure sur le billet de 50 000 roupies."),
                P("id", "tegallalang", "Ubud", "Nature", "Autour d'Ubud, les rizières en terrasses de Tegallalang. L'irrigation balinaise, le <strong>subak</strong>, est classée à l'UNESCO depuis 2012."),
                P("id", "tanahlot", "Tanah Lot", "Temple", "À Bali, un temple sur un rocher dans la mer, entouré par les vagues à marée haute."),
                P("id", "nusapenida", "Nusa Penida", "Île", "La plage de <strong>Kelingking</strong> et sa falaise, sur l'île en face de Bali."),
                P("id", "borobudur", "Borobudur", "Temple", "Sur l'île de Java, le plus grand temple bouddhiste du monde, bâti au IX<sup>e</sup> siècle. Classé à l'<strong>UNESCO depuis 1991</strong>."),
                P("id", "bromo", "Mont Bromo", "Volcan", "À l'est de Java, un volcan actif au milieu d'une mer de sable : on y monte pour le lever du soleil."),
                P("id", "komodo", "Komodo", "Nature", "Un parc national d'îles arides, refuge du <strong>dragon de Komodo</strong>, le plus grand lézard du monde. Classé à l'UNESCO depuis 1991. Ici, l'île de Padar."),
                P("id", "jakarta", "Jakarta", "Ville", "La plus grande ville du pays, sur l'île de Java, et son <strong>Monument national</strong> (Monas).")]),
    dict(cc="us", slug="etats-unis", nom="États-Unis", en="aux États-Unis", de="des États-Unis", flag="🇺🇸", air="JFK", ville="New York", region="Amériques",
         accroche="Gratte-ciel, canyons, plages et grands ponts : de New York à la Californie.",
         lieux=[P("us", "liberty", "New York", "Ville", "La <strong>statue de la Liberté</strong>, offerte par la France et inaugurée en 1886. Classée à l'UNESCO depuis 1984."),
                P("us", "times", "Times Square", "Quartier", "À New York, des panneaux lumineux sur tous les immeubles : il y fait jour même la nuit."),
                P("us", "brooklyn", "Brooklyn Bridge", "Monument", "Ouvert en <strong>1883</strong>. On le traverse à pied, face aux tours de Manhattan."),
                P("us", "grandcanyon", "Grand Canyon", "Nature", "En Arizona, une gorge creusée par le fleuve Colorado, profonde de plus de 1 500 m. Classé à l'<strong>UNESCO depuis 1979</strong>."),
                P("us", "sanfrancisco", "San Francisco", "Ville", "Le <strong>Golden Gate Bridge</strong>, pont suspendu rouge-orangé ouvert en 1937, à l'entrée de la baie."),
                P("us", "losangeles", "Los Angeles", "Ville", "La ville du cinéma et les lettres blanches de <strong>Hollywood</strong>, sur la colline."),
                P("us", "miami", "Miami", "Plage", "<strong>Miami Beach</strong> : la plage, les palmiers et les immeubles Art déco aux couleurs pastel."),
                P("us", "chicago", "Chicago", "Ville", "Au bord du lac Michigan, une ville de gratte-ciel réputée pour son architecture.")]),
    dict(cc="mx", slug="mexique", nom="Mexique", en="au Mexique", de="du Mexique", flag="🇲🇽", air="MEX", ville="Mexico", region="Amériques",
         accroche="Pyramides, mer turquoise, villes coloniales et cuisine de légende.",
         lieux=[P("mx", "chichen", "Chichén Itzá", "Antiquité", "La pyramide de Kukulcán, au cœur du Yucatán. Site maya classé à l'<strong>UNESCO depuis 1988</strong>."),
                P("mx", "teotihuacan", "Teotihuacán", "Antiquité", "La <strong>pyramide du Soleil</strong>, près de Mexico. Un site classé à l'UNESCO depuis 1987."),
                P("mx", "tulum", "Tulum", "Bord de mer", "Des ruines mayas posées sur la falaise, au-dessus d'une plage de la mer des Caraïbes."),
                P("mx", "mexico", "Mexico", "Capitale", "Le <strong>palais des Beaux-Arts</strong>, inauguré en 1934, au cœur d'une ville immense."),
                P("mx", "oaxaca", "Oaxaca", "Ville", "L'église Santo Domingo et un centre historique classé à l'<strong>UNESCO depuis 1987</strong>."),
                P("mx", "guanajuato", "Guanajuato", "Ville", "Une ville minière aux maisons de toutes les couleurs, accrochées aux collines. Classée à l'UNESCO depuis 1988."),
                P("mx", "cancun", "Cancún", "Plage", "Sur la mer des Caraïbes : une longue bande de sable blanc et une eau turquoise."),
                P("mx", "cenote", "Cenotes", "Nature", "Dans le Yucatán, des <strong>puits naturels d'eau douce</strong> creusés dans la roche, où l'on descend se baigner.")]),
]
PAYS += [
    dict(cc="cm", slug="cameroun", nom="Cameroun", en="au Cameroun", de="du Cameroun", flag="🇨🇲", air="DLA", ville="Douala", region="Afrique",
         accroche="Le grand port de Douala, la capitale sur ses collines, les plages de Kribi et le palais des sultans bamoun.",
         lieux=[P("cm", "douala", "Douala", "Ville", "La capitale économique et le grand port du pays, sur l'estuaire du Wouri. Ici le quartier Bali."),
                P("cm", "yaounde", "Yaoundé", "Capitale", "La capitale politique, bâtie sur des collines. Ici l'<strong>Immeuble Étoile</strong>, dans le quartier administratif."),
                P("cm", "kribi", "Kribi", "Plage", "La station balnéaire du sud : plages de sable et <strong>chutes de la Lobé</strong>, qui se jettent directement dans l'océan."),
                P("cm", "limbe", "Limbé", "Plage", "Au pied du mont Cameroun, des plages de sable noir volcanique."),
                P("cm", "montcameroun", "Mont Cameroun", "Volcan", "Un volcan actif de plus de <strong>4 000 m</strong>, le plus haut sommet d'Afrique de l'Ouest et centrale."),
                P("cm", "foumban", "Foumban", "Culture", "La capitale du royaume bamoun, dans l'Ouest : le <strong>palais des sultans</strong> et ses artisans."),
                P("cm", "rhumsiki", "Rhumsiki", "Paysage", "Dans l'Extrême-Nord, un village entouré de pics volcaniques, au cœur des monts Mandara."),
                P("cm", "waza", "Parc de Waza", "Safari", "Dans l'Extrême-Nord, une grande réserve de savane : éléphants, girafes, antilopes.")]),
    dict(cc="gh", slug="ghana", nom="Ghana", en="au Ghana", de="du Ghana", flag="🇬🇭", air="ACC", ville="Accra", region="Afrique",
         accroche="Une capitale tournée vers l'océan, des forts chargés d'histoire, une forêt que l'on traverse sur des ponts suspendus.",
         lieux=[P("gh", "accra", "Accra", "Capitale", "La <strong>place de l'Indépendance</strong> et son arche surmontée de l'étoile noire, symbole du pays indépendant depuis 1957."),
                P("gh", "nkrumah", "Mausolée Kwame Nkrumah", "Mémoire", "À Accra, le mémorial du premier président du Ghana, figure du panafricanisme."),
                P("gh", "capecoast", "Cape Coast", "Histoire", "Un fort de la côte, lieu de mémoire de la traite atlantique. Les forts et châteaux du Ghana sont classés à l'<strong>UNESCO depuis 1979</strong>."),
                P("gh", "elmina", "Elmina", "Histoire", "Le château d'Elmina, fondé par les Portugais en <strong>1482</strong> : l'un des plus anciens bâtiments européens au sud du Sahara."),
                P("gh", "kakum", "Parc de Kakum", "Nature", "Une forêt tropicale que l'on découvre d'en haut, sur une <strong>passerelle suspendue</strong> entre les arbres."),
                P("gh", "kumasi", "Kumasi", "Culture", "La capitale du royaume ashanti : le palais de Manhyia et l'un des plus grands marchés d'Afrique de l'Ouest."),
                P("gh", "mole", "Parc de Mole", "Safari", "Dans le nord, la plus grande réserve du pays, connue pour ses éléphants."),
                P("gh", "volta", "Chutes de Wli", "Nature", "Dans la région de la Volta, près de la frontière du Togo : les plus hautes chutes du pays.")]),
    dict(cc="tn", slug="tunisie", nom="Tunisie", en="en Tunisie", de="de la Tunisie", flag="🇹🇳", air="TUN", ville="Tunis", region="Afrique",
         accroche="Villages bleu et blanc, ruines antiques, médinas classées et l'île de Djerba.",
         lieux=[P("tn", "sidibou", "Sidi Bou Saïd", "Village", "Au-dessus de la mer, un village aux murs blancs et aux portes bleues, à quelques kilomètres de Tunis."),
                P("tn", "tunis", "Tunis", "Capitale", "La médina, ses souks et la mosquée Zitouna. Classée à l'<strong>UNESCO depuis 1979</strong>."),
                P("tn", "carthage", "Carthage", "Antiquité", "Les vestiges de la grande rivale de Rome, face à la mer : les thermes d'Antonin. Site classé à l'UNESCO depuis 1979."),
                P("tn", "eljem", "El Jem", "Antiquité", "Un amphithéâtre romain du III<sup>e</sup> siècle, parmi les plus grands du monde. Classé à l'<strong>UNESCO depuis 1979</strong>."),
                P("tn", "kairouan", "Kairouan", "Ville sainte", "Fondée au VII<sup>e</sup> siècle, la ville abrite l'une des plus anciennes grandes mosquées du Maghreb. Classée à l'UNESCO depuis 1988."),
                P("tn", "sousse", "Sousse", "Bord de mer", "Une médina fortifiée au bord de la Méditerranée, classée à l'UNESCO depuis 1988, avec son <strong>ribat</strong>, et de longues plages."),
                P("tn", "djerba", "Djerba", "Île", "Une île du sud : plages, palmiers et villages blancs. Ici <strong>Houmt Souk</strong>, sa ville principale. Classée à l'<strong>UNESCO depuis 2023</strong>."),
                P("tn", "tozeur", "Tozeur", "Désert", "Aux portes du Sahara, une immense palmeraie et, tout près, les oasis de montagne. Ici <strong>Chebika</strong>.")]),
    dict(cc="za", slug="afrique-du-sud", nom="Afrique du Sud", en="en Afrique du Sud", de="de l'Afrique du Sud", flag="🇿🇦", air="CPT", ville="Le Cap", region="Afrique",
         accroche="Une ville entre montagne et océan, des safaris, des manchots sur la plage et des canyons.",
         lieux=[P("za", "lecap", "Le Cap", "Ville", "La ville s'étend au pied de la <strong>montagne de la Table</strong>, un plateau de plus de 1 000 m que l'on rejoint en téléphérique."),
                P("za", "bokaap", "Bo-Kaap", "Quartier", "Au Cap, un quartier aux maisons peintes de couleurs vives, sur les pentes de Signal Hill."),
                P("za", "capbonne", "Cap de Bonne-Espérance", "Paysage", "Une côte rocheuse battue par les vagues et le vent, à la pointe de la péninsule du Cap."),
                P("za", "boulders", "Boulders Beach", "Nature", "Près du Cap, une plage où vit une colonie de <strong>manchots du Cap</strong>."),
                P("za", "kruger", "Parc Kruger", "Safari", "L'une des plus grandes réserves d'Afrique : lions, éléphants, rhinocéros, buffles et léopards."),
                P("za", "johannesburg", "Johannesburg", "Ville", "La plus grande ville du pays, née de la ruée vers l'or à la fin du XIX<sup>e</sup> siècle."),
                P("za", "drakensberg", "Drakensberg", "Montagne", "Une chaîne de montagnes et de falaises, classée à l'<strong>UNESCO depuis 2000</strong>."),
                P("za", "blyde", "Blyde River Canyon", "Paysage", "L'un des plus grands canyons du monde, couvert de végétation, et ses trois pitons arrondis.")]),
    dict(cc="tz", slug="tanzanie", nom="Tanzanie", en="en Tanzanie", de="de la Tanzanie", flag="🇹🇿", air="ZNZ", ville="Zanzibar", region="Afrique",
         accroche="Zanzibar et ses plages, le Serengeti, le cratère du Ngorongoro et le toit de l'Afrique.",
         lieux=[P("tz", "zanzibar", "Stone Town", "Ville historique", "La vieille ville de Zanzibar : ruelles, portes sculptées et maisons de pierre. Classée à l'<strong>UNESCO depuis 2000</strong>."),
                P("tz", "plage", "Plages de Zanzibar", "Plage", "Au nord de l'île, autour de Nungwi : sable blanc, eau turquoise et boutres traditionnels."),
                P("tz", "serengeti", "Serengeti", "Safari", "Une plaine immense où se déplacent chaque année des centaines de milliers de gnous. Classé à l'<strong>UNESCO depuis 1981</strong>."),
                P("tz", "ngorongoro", "Ngorongoro", "Safari", "Un cratère d'environ 20 km de large, où vit une faune très dense. Classé à l'UNESCO depuis 1979."),
                P("tz", "kilimandjaro", "Kilimandjaro", "Montagne", "<strong>5 895 m</strong> : le plus haut sommet d'Afrique. Parc classé à l'UNESCO depuis 1987. Vu ici depuis la plaine d'Amboseli, côté kényan."),
                P("tz", "manyara", "Tarangire", "Safari", "Un parc connu pour ses baobabs et ses grands troupeaux d'éléphants."),
                P("tz", "natron", "Ol Doinyo Lengaï", "Volcan", "Un volcan actif au sud du lac Natron, la « montagne de Dieu » des Maasaï."),
                P("tz", "dar", "Dar es Salaam", "Ville", "La plus grande ville du pays, sur l'océan Indien, d'où partent les bateaux pour Zanzibar.")]),
    dict(cc="fr", slug="france", nom="France", en="en France", de="de la France", flag="🇫🇷", air="CDG", ville="Paris", region="Europe",
         accroche="Paris, mais aussi une abbaye sur un rocher, la Côte d'Azur, le plus haut sommet des Alpes et de grandes villes du Sud.",
         lieux=[P("fr", "paris", "Paris", "Capitale", "La <strong>tour Eiffel</strong>, construite pour l'Exposition universelle de 1889. Les rives de la Seine sont classées à l'UNESCO depuis 1991."),
                P("fr", "versailles", "Versailles", "Château", "Le château de Louis XIV, sa galerie des Glaces et ses jardins. Classé à l'<strong>UNESCO depuis 1979</strong>."),
                P("fr", "montstmichel", "Mont-Saint-Michel", "Patrimoine", "Une abbaye sur un îlot rocheux, entourée par la mer à marée haute. Classé à l'<strong>UNESCO depuis 1979</strong>."),
                P("fr", "lyon", "Lyon", "Ville", "Entre Rhône et Saône, le Vieux-Lyon et la colline de Fourvière. Site historique classé à l'UNESCO depuis 1998."),
                P("fr", "marseille", "Marseille", "Ville", "Le <strong>Vieux-Port</strong>, vu ici depuis la basilique Notre-Dame-de-la-Garde, sur la colline."),
                P("fr", "nice", "Nice", "Bord de mer", "La <strong>promenade des Anglais</strong> le long de la baie des Anges. Classée à l'UNESCO depuis 2021."),
                P("fr", "bordeaux", "Bordeaux", "Ville", "La place de la Bourse et son miroir d'eau. Le port de la Lune est classé à l'UNESCO depuis 2007."),
                P("fr", "chamonix", "Chamonix", "Montagne", "Au pied du <strong>mont Blanc</strong>, le plus haut sommet des Alpes, à plus de 4 800 m. Ici le dôme du Goûter, sur la voie du sommet.")]),
    dict(cc="es", slug="espagne", nom="Espagne", en="en Espagne", de="de l'Espagne", flag="🇪🇸", air="BCN", ville="Barcelone", region="Europe",
         accroche="Gaudí à Barcelone, les palais d'Andalousie, des criques aux Baléares et des musées d'avant-garde.",
         lieux=[P("es", "barcelone", "Barcelone", "Ville", "La <strong>Sagrada Família</strong>, la basilique de Gaudí commencée en 1882. Ses œuvres sont classées à l'UNESCO."),
                P("es", "madrid", "Madrid", "Capitale", "La <strong>Plaza Mayor</strong>, grande place à arcades du XVII<sup>e</sup> siècle, au cœur de la capitale."),
                P("es", "seville", "Séville", "Ville", "La <strong>place d'Espagne</strong>, en demi-cercle, bâtie pour l'Exposition ibéro-américaine de 1929."),
                P("es", "grenade", "Grenade", "Patrimoine", "L'<strong>Alhambra</strong>, palais et forteresse des souverains nasrides, face à la Sierra Nevada. Classée à l'UNESCO depuis 1984."),
                P("es", "cordoue", "Cordoue", "Patrimoine", "La mosquée-cathédrale et sa forêt de colonnes et d'arcs rouges et blancs. Classée à l'<strong>UNESCO depuis 1984</strong>."),
                P("es", "valence", "Valence", "Ville", "La <strong>Cité des arts et des sciences</strong>, un ensemble futuriste de bâtiments blancs."),
                P("es", "majorque", "Majorque", "Île", "La plus grande île des Baléares : des criques d'eau claire entre les falaises."),
                P("es", "bilbao", "Bilbao", "Musée", "Le <strong>musée Guggenheim</strong>, ouvert en 1997 : un bâtiment aux formes courbes recouvert de titane.")]),
    dict(cc="pt", slug="portugal", nom="Portugal", en="au Portugal", de="du Portugal", flag="🇵🇹", air="LIS", ville="Lisbonne", region="Europe",
         accroche="Tramways jaunes, palais colorés, falaises dorées et vignobles en terrasses.",
         lieux=[P("pt", "lisbonne", "Lisbonne", "Capitale", "Des collines, des ruelles et le <strong>tramway 28</strong>, qui traverse les vieux quartiers."),
                P("pt", "belem", "Belém", "Monument", "À Lisbonne, la <strong>tour de Belém</strong>, bâtie au XVI<sup>e</sup> siècle au bord du Tage. Classée à l'UNESCO depuis 1983."),
                P("pt", "sintra", "Sintra", "Palais", "Le <strong>palais de Pena</strong>, aux couleurs vives, sur une colline boisée. Classé à l'UNESCO depuis 1995."),
                P("pt", "porto", "Porto", "Ville", "Le quartier de la Ribeira, au bord du Douro, et le pont Dom-Luís. Centre classé à l'<strong>UNESCO depuis 1996</strong>."),
                P("pt", "douro", "Vallée du Douro", "Paysage", "Des vignobles en terrasses le long du fleuve. Classée à l'UNESCO depuis 2001."),
                P("pt", "algarve", "Algarve", "Bord de mer", "Au sud, des falaises dorées, des arches et des grottes : ici la <strong>Ponta da Piedade</strong>, à Lagos."),
                P("pt", "obidos", "Óbidos", "Village", "Un village médiéval aux maisons blanches, entouré de remparts et dominé par son <strong>château</strong>."),
                P("pt", "madere", "Madère", "Île", "Une île de l'Atlantique, montagneuse et verte. Ici les hauteurs de <strong>Funchal</strong>, sa capitale.")]),
    dict(cc="gr", slug="grece", nom="Grèce", en="en Grèce", de="de la Grèce", flag="🇬🇷", air="ATH", ville="Athènes", region="Europe",
         accroche="Temples antiques, monastères perchés et îles blanches au-dessus de la mer.",
         lieux=[P("gr", "athenes", "Athènes", "Capitale", "L'<strong>Acropole</strong> et le Parthénon, du V<sup>e</sup> siècle avant notre ère. Classée à l'UNESCO depuis 1987."),
                P("gr", "santorin", "Santorin", "Île", "Des villages blancs aux coupoles bleues, accrochés au bord d'un ancien volcan. Ici <strong>Oia</strong>."),
                P("gr", "mykonos", "Mykonos", "Île", "Dans les Cyclades, une île connue pour ses <strong>moulins à vent</strong> et ses ruelles blanches."),
                P("gr", "meteores", "Météores", "Monastères", "Des monastères bâtis au sommet de pitons rocheux. Classés à l'<strong>UNESCO depuis 1988</strong>."),
                P("gr", "delphes", "Delphes", "Antiquité", "Le sanctuaire où l'on venait consulter l'oracle. Classé à l'UNESCO depuis 1987."),
                P("gr", "crete", "Crète", "Île", "La plus grande île grecque. Ici le lagon de <strong>Balos</strong>, au nord-ouest."),
                P("gr", "rhodes", "Rhodes", "Ville médiévale", "Une vieille ville fortifiée par les chevaliers de Saint-Jean. Classée à l'UNESCO depuis 1988."),
                P("gr", "zakynthos", "Zante", "Plage", "La plage du <strong>Navagio</strong>, au pied des falaises, que l'on voit d'en haut ou par la mer.")]),
    dict(cc="tr", slug="turquie", nom="Turquie", en="en Turquie", de="de la Turquie", flag="🇹🇷", air="IST", ville="Istanbul", region="Asie",
         accroche="Istanbul entre deux continents, les cheminées de fée de Cappadoce, des ruines antiques et la côte turquoise.",
         lieux=[P("tr", "istanbul", "Istanbul", "Ville", "<strong>Sainte-Sophie</strong>, bâtie au VI<sup>e</sup> siècle. Les quartiers historiques sont classés à l'UNESCO depuis 1985."),
                P("tr", "mosqueebleue", "Mosquée bleue", "Monument", "À Istanbul, la mosquée du sultan Ahmet, achevée au début du XVII<sup>e</sup> siècle, et ses <strong>six minarets</strong>."),
                P("tr", "bosphore", "Bosphore", "Paysage", "Le détroit qui sépare l'Europe de l'Asie, au cœur d'Istanbul. Ici la mosquée d'Ortaköy, au pied du pont."),
                P("tr", "cappadoce", "Cappadoce", "Paysage", "Des cheminées de fée et des villages creusés dans la roche, que l'on survole en <strong>montgolfière</strong>. Classée à l'UNESCO depuis 1985."),
                P("tr", "pamukkale", "Pamukkale", "Nature", "Le « château de coton » : des bassins blancs en terrasses, formés par des sources chaudes. Classé à l'<strong>UNESCO depuis 1988</strong>."),
                P("tr", "ephese", "Éphèse", "Antiquité", "Une grande cité antique et la façade de la <strong>bibliothèque de Celsus</strong>. Classée à l'UNESCO depuis 2015."),
                P("tr", "antalya", "Antalya", "Bord de mer", "Sur la Méditerranée, une vieille ville autour d'un petit port, au pied des montagnes."),
                P("tr", "bodrum", "Bodrum", "Bord de mer", "Sur la mer Égée, un port dominé par le <strong>château Saint-Pierre</strong>, bâti au XV<sup>e</sup> siècle.")]),
    dict(cc="ae", slug="emirats-arabes-unis", nom="Émirats arabes unis", en="aux Émirats arabes unis", de="des Émirats arabes unis", flag="🇦🇪", air="DXB", ville="Dubaï", region="Asie",
         accroche="Dubaï et ses tours, Abou Dabi et sa grande mosquée, et le désert à la sortie de la ville.",
         lieux=[P("ae", "dubai", "Dubaï", "Ville", "Le <strong>Burj Khalifa</strong>, 828 m, la plus haute tour du monde, inaugurée en 2010."),
                P("ae", "burjalarab", "Burj Al Arab", "Monument", "À Dubaï, un hôtel en forme de voile, bâti sur une île artificielle."),
                P("ae", "marina", "Dubai Marina", "Quartier", "Un quartier de gratte-ciel construit autour d'un canal artificiel."),
                P("ae", "palm", "Palm Jumeirah", "Île", "Une île artificielle en forme de palmier, visible depuis le ciel."),
                P("ae", "vieuxdubai", "Vieux Dubaï", "Histoire", "Le long de la crique, le quartier ancien d'Al Fahidi et les <strong>abras</strong>, les barques qui font la traversée."),
                P("ae", "desert", "Désert", "Nature", "À la sortie de la ville, des dunes de sable orangé à perte de vue."),
                P("ae", "abudhabi", "Abou Dabi", "Capitale", "La <strong>grande mosquée Cheikh Zayed</strong>, en marbre blanc, ouverte en 2007. Ici l'allée de palmiers qui y mène."),
                P("ae", "louvre", "Louvre Abou Dabi", "Musée", "Un musée ouvert en <strong>2017</strong> sous une immense coupole ajourée, au bord de l'eau.")]),
    dict(cc="br", slug="bresil", nom="Brésil", en="au Brésil", de="du Brésil", flag="🇧🇷", air="GIG", ville="Rio de Janeiro", region="Amériques",
         accroche="Rio et ses plages, les chutes d'Iguaçu, l'Amazonie et des dunes semées de lagons.",
         lieux=[P("br", "rio", "Rio de Janeiro", "Ville", "Le <strong>Christ rédempteur</strong>, inauguré en 1931 au sommet du Corcovado, les bras ouverts sur la baie."),
                P("br", "painsucre", "Pain de Sucre", "Paysage", "À Rio, un piton de granit à l'entrée de la baie, que l'on rejoint en téléphérique."),
                P("br", "copacabana", "Copacabana", "Plage", "À Rio, une plage de quatre kilomètres bordée par une promenade aux pavés noirs et blancs."),
                P("br", "iguacu", "Chutes d'Iguaçu", "Nature", "À la frontière de l'Argentine, des centaines de cascades au milieu de la forêt. Classées à l'<strong>UNESCO depuis 1986</strong>."),
                P("br", "salvador", "Salvador", "Ville historique", "Le <strong>Pelourinho</strong>, quartier aux maisons colorées de la première capitale du Brésil. Classé à l'UNESCO depuis 1985."),
                P("br", "amazonie", "Amazonie", "Nature", "Le plus grand fleuve du monde par son débit, et la forêt qui l'entoure. Ici la forêt près de Manaus, au bord du rio Negro."),
                P("br", "lencois", "Lençóis Maranhenses", "Paysage", "Des dunes blanches semées de lagons d'eau de pluie. Classé à l'<strong>UNESCO depuis 2024</strong>."),
                P("br", "saopaulo", "São Paulo", "Ville", "La plus grande ville du pays et d'Amérique du Sud. Ici le parc d'Ibirapuera et, derrière, les tours.")]),
]
import visiter_afrique as _AF  # noqa: E402
PAYS += _AF.PAYS
ORDRE = ["ci", "sn", "ml", "gn", "bf", "bj", "tg", "ng", "cm", "ga", "cd", "gh", "ma", "tn", "eg", "ke", "tz", "za", "fr", "it", "es", "pt", "gr", "nl", "tr", "ae", "jp", "th", "id", "us", "mx", "br"]
PAYS.sort(key=lambda p: ORDRE.index(p["cc"]))
REGIONS = ["Afrique", "Europe", "Asie", "Amériques"]

# ---------------------------------------------------------------------------------------------------------------
# Langues : le français est écrit ci-dessus ; l'anglais et l'italien sont dans scripts/visiter_en.py et visiter_it.py
# (mêmes clés). Un pays sans traduction complète n'est pas publié dans cette langue.
# ---------------------------------------------------------------------------------------------------------------
LANGS = ["fr", "en", "it"]
BASE = {"fr": "visiter", "en": "en/what-to-visit", "it": "it/cosa-visitare"}
SUB = {"jeu": {"fr": "jeu", "en": "game", "it": "gioco"}, "comparer": {"fr": "comparer", "en": "compare", "it": "confronta"}}
TR = {}
for _l in ("en", "it"):
    try:
        TR[_l] = __import__("visiter_" + _l)
    except ImportError:
        pass
for _l, (_p, _x) in _AF.TR.items():  # pays ajoutés dans scripts/visiter_afrique.py : traductions fusionnées
    if _l in TR:
        TR[_l].PAYS.update(_p)
        TR[_l].LIEUX.update(_x)
_K = lambda en, it: {"en": en, "it": it}
KINDS = {"Antiquité": _K("Ancient site", "Antichità"), "Bord de mer": _K("Seaside", "Mare"), "Capitale": _K("Capital", "Capitale"), "Château": _K("Palace", "Reggia"),
         "Culture": _K("Culture", "Cultura"), "Désert": _K("Desert", "Deserto"), "Histoire": _K("History", "Storia"), "Jardin": _K("Garden", "Giardino"),
         "Monastères": _K("Monasteries", "Monasteri"), "Montagne": _K("Mountain", "Montagna"), "Monument": _K("Landmark", "Monumento"), "Musée": _K("Museum", "Museo"),
         "Mémoire": _K("Memorial", "Memoria"), "Nature": _K("Nature", "Natura"), "Nil": _K("Nile", "Nilo"), "Océan": _K("Ocean", "Oceano"), "Palais": _K("Palace", "Palazzo"),
         "Patrimoine": _K("Heritage", "Patrimonio"), "Paysage": _K("Scenery", "Paesaggio"), "Plage": _K("Beach", "Spiaggia"), "Quartier": _K("District", "Quartiere"),
         "Safari": _K("Safari", "Safari"), "Sanctuaire": _K("Shrine", "Santuario"), "Spiritualité": _K("Holy city", "Spiritualità"), "Temple": _K("Temple", "Tempio"),
         "Village": _K("Village", "Villaggio"), "Ville": _K("City", "Città"), "Ville d'art": _K("City of art", "Città d'arte"), "Ville historique": _K("Historic town", "Città storica"),
         "Ville impériale": _K("Imperial city", "Città imperiale"), "Ville médiévale": _K("Medieval town", "Città medievale"), "Ville sainte": _K("Holy city", "Città santa"),
         "Volcan": _K("Volcano", "Vulcano"), "Île": _K("Island", "Isola"), "Îles": _K("Islands", "Isole"), "Cascade": _K("Waterfall", "Cascata"), "Fleuve": _K("River", "Fiume"),
         "Forêt": _K("Forest", "Foresta"), "Lac": _K("Lake", "Lago")}
REG = {"Afrique": _K("Africa", "Africa"), "Europe": _K("Europe", "Europa"), "Asie": _K("Asia", "Asia"), "Amériques": _K("Americas", "Americhe")}

U = {
    "fr": dict(eyebrow="Explorer le monde", h1="Que visiter {en}", lead="{n} villes et lieux à voir, en photos.", sub="{n} lieux à voir", photo="Photo",
               title="Que visiter {en} : {n} villes et lieux à voir | Escale", desc="{nom} en photos : {lieux}… Les villes et les lieux à voir, avec de vraies photos, et les vols pour {ville}.",
               like="Ajouter {n} à mes envies", carte="Carte postale", cta="Envie de partir {en} ?", cta_p="Comparez les vols pour {ville} et choisissez vos dates.",
               dep="Je pars de", dep0="choisir une ville", vols="Voir les vols pour {ville}", partout="Voir les prix partout dans le monde", share="Partager cette page",
               share_t="Que visiter {en} : {n} villes et lieux à voir, en photos",
               budget="Calculer le budget du voyage", b_vol="Vol aller-retour, par personne (€)", b_pers="Voyageurs", b_nuits="Nuits sur place", b_log="Logement, par nuit (€)",
               b_jour="Dépenses sur place, par jour et par personne (€)", b_note="Le prix du vol est celui repéré récemment depuis votre ville ; le logement et les dépenses sont vos propres chiffres. Escale n'invente aucun prix.",
               envies="Mes envies", envies_p="Les lieux que vous avez marqués d'un cœur. Ils restent dans ce téléphone, sans compte.",
               suite="Continuer le voyage", n_lieux="{n} lieux à voir", tous="Tous les pays à explorer", jeu="🎯 Jeu : devine le pays", comparer="⚖️ Comparer deux pays",
               note="Ces repères sont généraux et ne remplacent pas un guide. Avant de partir, vérifiez les conditions d'entrée du pays avec <a href=\"/visa/\">l'outil visa</a> et lisez les "
                    "<a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/\" target=\"_blank\" rel=\"noopener\">conseils aux voyageurs</a> de votre ministère des Affaires étrangères. "
                    "Photos : Wikimedia Commons, licences libres, <a href=\"/credits-photos/\">tous les crédits</a>.",
               hub_h1="Que visiter, <span>pays par pays</span>", hub_lead="Pas seulement les capitales : pour chaque pays, ses villes et ses lieux à voir, avec de vraies photos. {n} pays, et d'autres arrivent.",
               hub_title="Que visiter : le monde pays par pays, en photos | Escale", hub_desc="Explorez le monde pays par pays : les villes et les lieux à voir, avec de vraies photos. {noms}…",
               q="Chercher un pays ou un lieu", q_ph="Japon, Kyoto, plage, safari…", map_h="Sur la carte", map_p="Touchez un point pour voir le pays et le prix du vol depuis votre ville.",
               zoom=["Monde", "Afrique", "Europe", "Asie", "Amériques"], partir="Et pour partir",
               l_partout=("/partout/", "Les prix des vols partout dans le monde"), l_surp=("/surprends-moi/", "Surprends-moi : une destination au hasard selon votre budget"),
               l_quiz=("/quiz-destination/", "Quiz : quelle destination est faite pour moi ?"), credits="Photos : Wikimedia Commons, licences libres, <a href=\"/credits-photos/\">tous les crédits</a>.",
               jeu_title="Jeu : devine le pays en photo | Escale", jeu_desc="Une vraie photo, quatre pays : saurez-vous reconnaître Zanzibar, Kyoto ou Grand-Bassam ? Dix photos, un score à partager.",
               jeu_h1="Devine <span>le pays</span>", jeu_lead="Une vraie photo, quatre réponses. Dix photos, un score à partager.", jeu_go="Jouer",
               cmp_title="Comparer deux pays : prix du vol et lieux à voir | Escale", cmp_desc="Sénégal ou Maroc ? Japon ou Thaïlande ? Comparez deux pays côte à côte : prix du vol depuis votre ville et lieux à voir.",
               cmp_h1="Comparer <span>deux pays</span>", cmp_lead="Choisissez deux pays : le prix du vol depuis votre ville et les lieux à voir, côte à côte.", cmp_a="Premier pays", cmp_b="Deuxième pays"),
    "en": dict(eyebrow="Explore the world", h1="What to visit {en}", lead="{n} cities and places to see, in photos.", sub="{n} places to see", photo="Photo",
               title="What to visit {en}: {n} cities and places to see | Escale", desc="{nom} in photos: {lieux}… The cities and places to see, with real photos, and flights to {ville}.",
               like="Add {n} to my wishlist", carte="Postcard", cta="Ready to go?", cta_p="Compare flights to {ville} and pick your dates.",
               dep="I'm leaving from", dep0="choose a city", vols="See flights to {ville}", partout="See prices everywhere in the world", share="Share this page",
               share_t="What to visit {en}: {n} cities and places to see, in photos",
               budget="Work out the trip budget", b_vol="Return flight, per person (€)", b_pers="Travellers", b_nuits="Nights there", b_log="Accommodation, per night (€)",
               b_jour="Spending there, per day and per person (€)", b_note="The flight price is the one spotted recently from your city; accommodation and spending are your own figures. Escale never makes up a price.",
               envies="My wishlist", envies_p="The places you marked with a heart. They stay on this phone, no account needed.",
               suite="Keep exploring", n_lieux="{n} places to see", tous="All countries to explore", jeu="🎯 Game: guess the country", comparer="⚖️ Compare two countries",
               note="These pointers are general and do not replace a guidebook. Before you travel, check the country's entry requirements with <a href=\"/en/visa/\">the visa tool</a> and read your government's "
                    "<a href=\"https://www.gov.uk/foreign-travel-advice\" target=\"_blank\" rel=\"noopener\">travel advice</a>. "
                    "Photos: Wikimedia Commons, free licences, <a href=\"/credits-photos/\">all credits</a>.",
               hub_h1="What to visit, <span>country by country</span>", hub_lead="Not just capitals: each country's cities and places to see, with real photos. {n} countries, and more to come.",
               hub_title="What to visit: the world country by country, in photos | Escale", hub_desc="Explore the world country by country: the cities and places to see, with real photos. {noms}…",
               q="Search for a country or a place", q_ph="Japan, Kyoto, beach, safari…", map_h="On the map", map_p="Tap a dot to see the country and the flight price from your city.",
               zoom=["World", "Africa", "Europe", "Asia", "Americas"], partir="And to get there",
               l_partout=("/en/anywhere/", "Flight prices everywhere in the world"), l_surp=("/en/surprise-me/", "Surprise me: a random destination within your budget"),
               l_quiz=("/en/destination-quiz/", "Quiz: which destination suits me?"), credits="Photos: Wikimedia Commons, free licences, <a href=\"/credits-photos/\">all credits</a>.",
               jeu_title="Game: guess the country from a photo | Escale", jeu_desc="One real photo, four countries: can you recognise Zanzibar, Kyoto or Grand-Bassam? Ten photos, a score to share.",
               jeu_h1="Guess <span>the country</span>", jeu_lead="One real photo, four answers. Ten photos, a score to share.", jeu_go="Play",
               cmp_title="Compare two countries: flight price and places to see | Escale", cmp_desc="Senegal or Morocco? Japan or Thailand? Compare two countries side by side: flight price from your city and places to see.",
               cmp_h1="Compare <span>two countries</span>", cmp_lead="Pick two countries: the flight price from your city and the places to see, side by side.", cmp_a="First country", cmp_b="Second country"),
    "it": dict(eyebrow="Esplora il mondo", h1="Cosa visitare {en}", lead="{n} città e luoghi da vedere, in foto.", sub="{n} luoghi da vedere", photo="Foto",
               title="Cosa visitare {en}: {n} città e luoghi da vedere | Escale", desc="{nom} in foto: {lieux}… Le città e i luoghi da vedere, con foto vere, e i voli per {ville}.",
               like="Aggiungi {n} ai miei desideri", carte="Cartolina", cta="Voglia di partire?", cta_p="Confronta i voli per {ville} e scegli le date.",
               dep="Parto da", dep0="scegli una città", vols="Vedi i voli per {ville}", partout="Vedi i prezzi in tutto il mondo", share="Condividi questa pagina",
               share_t="Cosa visitare {en}: {n} città e luoghi da vedere, in foto",
               budget="Calcola il budget del viaggio", b_vol="Volo andata e ritorno, a persona (€)", b_pers="Viaggiatori", b_nuits="Notti sul posto", b_log="Alloggio, a notte (€)",
               b_jour="Spese sul posto, al giorno e a persona (€)", b_note="Il prezzo del volo è quello rilevato di recente dalla tua città; alloggio e spese sono le tue cifre. Escale non inventa nessun prezzo.",
               envies="I miei desideri", envies_p="I luoghi che hai segnato con un cuore. Restano su questo telefono, senza account.",
               suite="Continua il viaggio", n_lieux="{n} luoghi da vedere", tous="Tutti i paesi da esplorare", jeu="🎯 Gioco: indovina il paese", comparer="⚖️ Confronta due paesi",
               note="Queste indicazioni sono generali e non sostituiscono una guida. Prima di partire, verifica le condizioni d'ingresso del paese e leggi le schede di "
                    "<a href=\"https://www.viaggiaresicuri.it/\" target=\"_blank\" rel=\"noopener\">Viaggiare Sicuri</a> del Ministero degli Affari Esteri. "
                    "Foto: Wikimedia Commons, licenze libere, <a href=\"/credits-photos/\">tutti i crediti</a>.",
               hub_h1="Cosa visitare, <span>paese per paese</span>", hub_lead="Non solo le capitali: per ogni paese, le città e i luoghi da vedere, con foto vere. {n} paesi, e altri in arrivo.",
               hub_title="Cosa visitare: il mondo paese per paese, in foto | Escale", hub_desc="Esplora il mondo paese per paese: le città e i luoghi da vedere, con foto vere. {noms}…",
               q="Cerca un paese o un luogo", q_ph="Giappone, Kyoto, spiaggia, safari…", map_h="Sulla mappa", map_p="Tocca un punto per vedere il paese e il prezzo del volo dalla tua città.",
               zoom=["Mondo", "Africa", "Europa", "Asia", "Americhe"], partir="E per partire",
               l_partout=("/en/anywhere/", "I prezzi dei voli in tutto il mondo (in inglese)"), l_surp=("/it/sorprendimi/", "Sorprendimi: una meta a caso secondo il tuo budget"),
               l_quiz=("/it/quiz-destinazione/", "Quiz: quale meta fa per me?"), credits="Foto: Wikimedia Commons, licenze libere, <a href=\"/credits-photos/\">tutti i crediti</a>.",
               jeu_title="Gioco: indovina il paese dalla foto | Escale", jeu_desc="Una foto vera, quattro paesi: sai riconoscere Zanzibar, Kyoto o Grand-Bassam? Dieci foto, un punteggio da condividere.",
               jeu_h1="Indovina <span>il paese</span>", jeu_lead="Una foto vera, quattro risposte. Dieci foto, un punteggio da condividere.", jeu_go="Gioca",
               cmp_title="Confronta due paesi: prezzo del volo e luoghi da vedere | Escale", cmp_desc="Senegal o Marocco? Giappone o Thailandia? Confronta due paesi fianco a fianco: prezzo del volo dalla tua città e luoghi da vedere.",
               cmp_h1="Confronta <span>due paesi</span>", cmp_lead="Scegli due paesi: il prezzo del volo dalla tua città e i luoghi da vedere, fianco a fianco.", cmp_a="Primo paese", cmp_b="Secondo paese"),
}
HEART = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 21s-7.5-4.6-10-9.3C.4 8.3 2.3 4.5 6 4.5c2 0 3.4 1 4.3 2.3.3.5 1.1.5 1.4 0C12.6 5.5 14 4.5 16 4.5c3.700 0 5.600 3.800 4 7.200C19.500 16.400 12 21 12 21z"/></svg>'
W_MAP, K_MAP, TOP_MAP, H_MAP = 2000, 2000 / 360, 84, 789  # même projection que site/partout.js (img/world.svg)


def photos(site):
    f = site / "data" / "visiter-photos.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def img(ph, key, alt, eager=False, sizes="(min-width:700px) 440px, 100vw"):
    m = ph[key]
    return (f'<img src="/img/visiter/{key}.webp" srcset="/img/visiter/{key}-640.webp 640w, /img/visiter/{key}.webp {m["w"]}w" sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" alt="{E(alt)}"'
            + (' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"') + ">")


def cred(ph, key, lang="fr"):
    m = ph[key]
    return f'<p class="vx-cred">{U[lang]["photo"]} : <a href="{E(m["page"])}" target="_blank" rel="noopener">{E(m["author"])}</a>, {E(m["license"])}, Wikimedia Commons</p>'


# ---------------------------------------------------------------------------------------------------------------
# Lieux et pays retirés (demande de Dobam, 13 novembre 2026) : on ne met pas en avant un lieu situé dans une zone que
# les « Conseils aux voyageurs » de France Diplomatie déconseillent formellement (rouge) ou déconseillent sauf raison
# impérative (orange). Relevé fait le 13 novembre 2026 à partir d'extraits des fiches officielles (le site lui-même
# n'était pas joignable) : à refaire sur diplomatie.gouv.fr avant de remettre un lieu. Les textes restent dans le code,
# les photos sont supprimées. Rien de tout cela n'est écrit sur le site : les pages renvoient aux conseils officiels.
# ---------------------------------------------------------------------------------------------------------------
PAYS_RETIRES = {
    "ml": "Mali : tout le territoire est formellement déconseillé",
    "bf": "Burkina Faso : tout déplacement est formellement déconseillé",
    "cd": "RD Congo : voyages touristiques déconseillés sur l'ensemble du territoire, est du pays formellement déconseillé",
}
RETIRES = {
    "cm-rhumsiki": "Extrême-Nord, formellement déconseillé (monts Mandara compris)", "cm-waza": "Extrême-Nord, formellement déconseillé",
    "cm-montcameroun": "la fiche déconseille de s'y rendre (troubles dans le Sud-Ouest)", "cm-limbe": "région du Sud-Ouest, par prudence (non confirmé pour la ville)",
    "ng-yankari": "nord-est du Nigeria, à éviter absolument", "ng-zuma": "État de Niger, sur l'axe Abuja-Kaduna déconseillé sauf raison impérative",
    "bj-pendjari": "parc de la Pendjari, formellement déconseillé", "bj-tata": "centre de l'Atacora (Natitingou, Boukoumbé), déconseillé sauf raison impérative",
    "tg-koutammakou": "frontière du Bénin, face à l'Atacora, par prudence (non confirmé pour la préfecture)",
    "ci-tai": "zone frontalière du Liberia (Taï), déconseillée sauf raison impérative",
    "gn-nimba": "zone frontalière de la Côte d'Ivoire, par prudence",
    "ke-lamu": "comté de Lamu, proche de la frontière somalienne, par prudence",
    "tn-tozeur": "la photo et le texte montrent Chebika, dans la bande frontalière avec l'Algérie",
}
MIN_LIEUX = 4


def publies(site):
    """Pays publiés en français : ceux qui ont au moins MIN_LIEUX lieux en photo (les lieux sans photo ou retirés ne comptent pas)."""
    ph = photos(site)
    out = []
    for p in PAYS:
        if p["cc"] in PAYS_RETIRES:
            continue
        lieux = [l for l in p["lieux"] if l["key"] in ph and l["key"] not in RETIRES]
        if len(lieux) >= MIN_LIEUX:
            out.append(dict(p, lieux=lieux))
    return out, ph


def loc(p, lang):
    """Un pays (déjà filtré par publies) dans une langue ; None si la traduction manque."""
    if lang == "fr":
        return dict(p, region_l=p["region"])
    t = TR.get(lang)
    if not t or p["cc"] not in t.PAYS or any(l["key"] not in t.LIEUX for l in p["lieux"]):
        return None
    d = t.PAYS[p["cc"]]
    return dict(p, slug=d["slug"], nom=d["nom"], en=d["en"], ville=d["ville"], accroche=d["accroche"], region_l=REG[p["region"]][lang],
                lieux=[dict(l, nom=t.LIEUX[l["key"]][0], txt=t.LIEUX[l["key"]][1], kind=KINDS[l["kind"]][lang]) for l in p["lieux"]])


def par_langue(site):
    """{langue: [pays localisés]} et les photos ; chaque pays garde le même ordre dans toutes les langues."""
    pays, ph = publies(site)
    out = {}
    for lang in LANGS:
        L = [x for x in (loc(p, lang) for p in pays) if x]
        if L:
            out[lang] = L
    return out, ph


PATH = lambda p, lang="fr": f"{BASE[lang]}/{p['slug']}"


def _coord(site):
    return {a[0]: (a[5], a[6]) for a in json.loads((site / "data" / "airports.json").read_text(encoding="utf-8"))}


def build(site, ctx):
    PL, ph = par_langue(site)
    if "fr" not in PL:
        return []
    coord = _coord(site)
    urls = []
    # chemins de chaque pays dans chaque langue (pour les liens entre langues)
    chem = {}
    for lang, L in PL.items():
        for p in L:
            chem.setdefault(p["cc"], {})[lang] = PATH(p, lang)
    hubs = {lang: BASE[lang] for lang in PL}
    subs = {k: {lang: f"{BASE[lang]}/{v[lang]}" for lang in PL} for k, v in SUB.items()}
    for lang, pays in PL.items():
        u = U[lang]
        A = lambda cle: "/" + subs[cle][lang] + "/"
        # --- données pour les outils (jeu, comparateur, carte, envies) : un petit fichier par langue
        data = {"base": "/" + BASE[lang] + "/", "pays": [
            {"cc": p["cc"], "slug": p["slug"], "nom": p["nom"], "flag": p["flag"], "ville": p["ville"], "air": p["air"], "region": p["region_l"],
             "lat": coord.get(p["air"], (0, 0))[0], "lon": coord.get(p["air"], (0, 0))[1],
             "lieux": [{"k": l["key"], "n": l["nom"], "a": ph[l["key"]]["author"], "l": ph[l["key"]]["license"]} for l in p["lieux"]]} for p in pays]}
        (site / "data" / f"visiter-{lang}.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        attrs = f'data-vx-base="/{BASE[lang]}/" data-vx-data="/data/visiter-{lang}.json"'
        envies = (f'<section id="vx-envies" class="vx-envies" hidden><h2>{u["envies"]} <span data-envies-n></span></h2><p class="small">{u["envies_p"]}</p><ul></ul>'
                  '<div id="vx-alertes"></div></section>')
        for i, p in enumerate(pays):
            L = p["lieux"]
            n = len(L)
            hero = (f'<div class="vx" {attrs}><p class="eyebrow">{u["eyebrow"]} · {E(p["region_l"])}</p><h1>{E(u["h1"].format(en=p["en"]))} <span>{p["flag"]}</span></h1>'
                    f'<p class="hero-lead">{E(p["accroche"])} {u["lead"].format(n=n)}</p></div>')
            chips = '<nav class="vx-chips" aria-label="' + u["sub"].format(n=n) + '">' + "".join(f'<a href="#{l["key"]}">{E(l["nom"])}</a>' for l in L) + "</nav>"
            top = (f'<figure class="vx-hero">{img(ph, L[0]["key"], L[0]["nom"] + ", " + p["nom"], eager=True, sizes="(min-width:860px) 828px, 100vw")}<figcaption><span class="vx-title">{E(p["nom"])}</span>'
                   f'<span class="vx-sub">{u["sub"].format(n=n)} · {E(", ".join(l["nom"] for l in L[:4]))}…</span></figcaption></figure>')
            cards = "".join(
                f'<article class="vx-card" id="{l["key"]}"><div class="vx-ph"><span class="vx-kind">{E(l["kind"])}</span><span class="vx-n">{k}</span>{img(ph, l["key"], l["nom"] + ", " + p["nom"])}'
                f'<button type="button" class="vx-like" data-k="{l["key"]}" data-n="{E(l["nom"])}" data-p="{E(p["nom"])}" data-cc="{p["cc"]}" aria-pressed="false" aria-label="{E(u["like"].format(n=l["nom"]))}">{HEART}</button></div>'
                f'<div class="vx-tx"><h2>{E(l["nom"])}</h2><p>{l["txt"]}</p>{cred(ph, l["key"], lang)}'
                f'<p class="vx-acts"><button type="button" class="vx-pc" data-k="{l["key"]}" data-n="{E(l["nom"])}" data-p="{E(p["nom"])}" data-f="{p["flag"]}" data-a="{E(ph[l["key"]]["author"])}" data-l="{E(ph[l["key"]]["license"])}">🖼 {u["carte"]}</button></p>'
                f'</div></article>' for k, l in enumerate(L, 1))
            autres = [pays[(i + k) % len(pays)] for k in (1, 2, 3)]
            cta = (f'<section class="vx-cta" data-air="{p["air"]}" data-ville="{E(p["ville"])}" data-cc="{p["cc"]}"><h2>{E(u["cta"].format(en=p["en"]))}</h2><p>{E(u["cta_p"].format(ville=p["ville"]))}</p>'
                   f'<p class="vx-dep"><label>{u["dep"]} <select aria-label="{u["dep"]}"><option value="">{u["dep0"]}</option></select></label></p><p class="vx-prix" role="status"></p>'
                   f'<a class="btn" href="/?type=vols&amp;to={p["air"]}{"" if lang == "fr" else "&amp;lang=" + lang}">{E(u["vols"].format(ville=p["ville"]))}</a>'
                   f'<a class="btn ghost" href="{u["l_partout"][0]}">{u["partout"]}</a>'
                   f'<button type="button" class="btn ghost" id="vx-share" data-t="{E(u["share_t"].format(en=p["en"], n=n))}">{u["share"]}</button>'
                   f'<details class="vx-budget"><summary>{u["budget"]}</summary><div class="vx-bgrid">'
                   f'<label><span>{u["b_vol"]}</span><input type="number" id="vb-vol" min="0" step="1" inputmode="numeric"></label>'
                   f'<label><span>{u["b_pers"]}</span><input type="number" id="vb-pers" min="1" max="12" step="1" value="2" inputmode="numeric"></label>'
                   f'<label><span>{u["b_nuits"]}</span><input type="number" id="vb-nuits" min="0" max="90" step="1" value="7" inputmode="numeric"></label>'
                   f'<label><span>{u["b_log"]}</span><input type="number" id="vb-log" min="0" step="1" inputmode="numeric"></label>'
                   f'<label><span>{u["b_jour"]}</span><input type="number" id="vb-jour" min="0" step="1" inputmode="numeric"></label></div>'
                   f'<p class="vx-btot" id="vb-tot" role="status"></p><p class="vx-bnote">{u["b_note"]}</p></details></section>')
            suite = (f'<section><h2>{u["suite"]}</h2><div class="vx-hub">' + "".join(
                f'<a href="/{PATH(a, lang)}/">{img(ph, a["lieux"][0]["key"], a["nom"], sizes="(min-width:700px) 270px, 50vw")}<span class="vx-hl"><h3>{E(a["nom"])} {a["flag"]}</h3><small>{u["n_lieux"].format(n=len(a["lieux"]))}</small></span></a>' for a in autres)
                + f'</div><p class="vx-more"><a href="/{BASE[lang]}/">{u["tous"]}</a> · <a href="{A("jeu")}">{u["jeu"]}</a> · <a href="{A("comparer")}?a={p["cc"]}">{u["comparer"]}</a></p></section>')
            ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": u["h1"].format(en=p["en"]), "itemListElement": [
                {"@type": "ListItem", "position": k, "name": l["nom"], "url": f"{ctx['domain']}/{PATH(p, lang)}/#{l['key']}"} for k, l in enumerate(L, 1)]}, ensure_ascii=False) + "</script>"
            body = (top + cred(ph, L[0]["key"], lang) + chips + f'<div class="vx-list">{cards}</div>' + cta + envies + suite + f'<p class="small">{u["note"]}</p>'
                    + '<script src="/visiter.js" defer></script>')
            urls.append(B.write(site, PATH(p, lang), lang, u["title"].format(en=p["en"], n=n),
                                u["desc"].format(nom=p["nom"], lieux=", ".join(l["nom"] for l in L[:6]), ville=p["ville"]),
                                hero, body, ld, chem[p["cc"]], ctx, og=f"img/visiter/{L[0]['key']}.webp"))
        # --- sommaire : recherche, envies, carte, pays par région
        hero = f'<div class="vx" {attrs}><p class="eyebrow">{u["eyebrow"]}</p><h1>{u["hub_h1"]}</h1><p class="hero-lead">{u["hub_lead"].format(n=len(pays))}</p></div>'
        pins = "".join(
            f'<a class="vx-pin" href="/{PATH(p, lang)}/" data-cc="{p["cc"]}" style="left:{(coord[p["air"]][1] + 180) * K_MAP / W_MAP * 100:.2f}%;top:{(TOP_MAP - coord[p["air"]][0]) * K_MAP / H_MAP * 100:.2f}%" '
            f'aria-label="{E(p["nom"])}"><i>{p["flag"]}</i></a>' for p in pays if p["air"] in coord)
        zooms = "".join(f'<button type="button" data-z="{k}"{" aria-pressed=true" if k == 1 else ""}>{z}</button>' for k, z in enumerate(u["zoom"]))
        body = (f'<p class="vx-search"><label for="vx-q">{u["q"]}</label><input id="vx-q" type="search" placeholder="{u["q_ph"]}" autocomplete="off"><span id="vx-q-msg" class="small" role="status"></span></p>'
                f'<p class="vx-tools"><a class="btn ghost" href="{A("jeu")}">{u["jeu"]}</a><a class="btn ghost" href="{A("comparer")}">{u["comparer"]}</a></p>' + envies
                + f'<section class="vx-mapbox"><h2>{u["map_h"]}</h2><p class="small">{u["map_p"]}</p><div class="vx-zoom" role="group">{zooms}</div>'
                  f'<div class="vx-map" id="vx-map"><div class="vx-map-in"><img src="/img/world.svg" alt="" width="2000" height="789" loading="lazy" decoding="async">{pins}</div></div>'
                  f'<div id="vx-map-card" class="vx-map-card" role="status"></div></section>')
        for r in REGIONS:
            ps = [p for p in pays if p["region"] == r]
            if not ps:
                continue
            body += f'<h2 class="vx-reg">{E(ps[0]["region_l"])}</h2><div class="vx-hub">' + "".join(
                f'<a href="/{PATH(p, lang)}/" data-mots="{E(p["nom"] + " " + p["region_l"] + " " + " ".join(l["nom"] + " " + l["kind"] for l in p["lieux"]))}">'
                f'{img(ph, p["lieux"][0]["key"], p["nom"], sizes="(min-width:700px) 270px, 50vw")}<span class="vx-hl"><h3>{E(p["nom"])} {p["flag"]}</h3>'
                f'<small>{E(", ".join(l["nom"] for l in p["lieux"][:3]))}…</small></span></a>' for p in ps) + "</div>"
        body += (f'<section><h2>{u["partir"]}</h2><ul>' + "".join(f'<li><a href="{h}">{E(t)}</a></li>' for h, t in (u["l_partout"], u["l_surp"], u["l_quiz"])) + '</ul></section>'
                 f'<p class="small">{u["credits"]}</p><script src="/visiter.js" defer></script><script src="/visiter-carte.js" defer></script>')
        urls.append(B.write(site, BASE[lang], lang, u["hub_title"], u["hub_desc"].format(noms=", ".join(p["nom"] for p in pays[:8])), hero, body, "", hubs, ctx))
        # --- jeu « devine le pays »
        hero = f'<div class="vx" {attrs}><p class="eyebrow">{u["eyebrow"]}</p><h1>{u["jeu_h1"]}</h1><p class="hero-lead">{u["jeu_lead"]}</p></div>'
        body = (f'<div id="vx-jeu" class="vx-jeu"><p><button type="button" class="btn" id="vj-go">{u["jeu_go"]}</button></p></div>'
                f'<p class="vx-more"><a href="/{BASE[lang]}/">{u["tous"]}</a> · <a href="{A("comparer")}">{u["comparer"]}</a></p><p class="small">{u["credits"]}</p>'
                '<script src="/visiter-jeu.js" defer></script>')
        urls.append(B.write(site, subs["jeu"][lang], lang, u["jeu_title"], u["jeu_desc"], hero, body, "", subs["jeu"], ctx))
        # --- comparateur de deux pays
        hero = f'<div class="vx" {attrs}><p class="eyebrow">{u["eyebrow"]}</p><h1>{u["cmp_h1"]}</h1><p class="hero-lead">{u["cmp_lead"]}</p></div>'
        opts = "".join(f'<option value="{p["cc"]}">{p["flag"]} {E(p["nom"])}</option>' for p in pays)
        body = (f'<div class="vx-cmp-form"><label><span>{u["cmp_a"]}</span><select id="vc-a">{opts}</select></label><label><span>{u["cmp_b"]}</span><select id="vc-b">{opts}</select></label>'
                f'<label><span>{u["dep"]}</span><select id="vc-from"><option value="">{u["dep0"]}</option></select></label></div><div id="vx-cmp" class="vx-cmp" role="status"></div>'
                f'<p class="vx-more"><a href="/{BASE[lang]}/">{u["tous"]}</a> · <a href="{A("jeu")}">{u["jeu"]}</a></p><p class="small">{u["credits"]}</p>'
                '<script src="/visiter.js" defer></script><script src="/visiter-comparer.js" defer></script>')
        urls.append(B.write(site, subs["comparer"][lang], lang, u["cmp_title"], u["cmp_desc"], hero, body, "", subs["comparer"], ctx))
    return urls


def credits(site):
    pays, ph = publies(site)
    if not pays:
        return ""
    rows = "".join(f'<li><strong>{E(l["nom"])} ({E(p["nom"])})</strong> : <a href="{E(ph[l["key"]]["page"])}" rel="noopener">{E(ph[l["key"]]["file"].replace("File:", ""))}</a>, {E(ph[l["key"]]["author"])}, '
                   + (f'<a href="{E(ph[l["key"]]["license_url"])}" rel="noopener license">{E(ph[l["key"]]["license"])}</a>' if ph[l["key"]].get("license_url") else E(ph[l["key"]]["license"]))
                   + " (recadrée et redimensionnée)</li>" for p in pays for l in p["lieux"])
    return f'<section><h2>Photos de la rubrique « Que visiter »</h2><ul class="links">{rows}</ul></section>'


def liens(site):
    """Pays publiés, pour l'accueil : chemins et noms dans chaque langue, drapeau, ville, première photo."""
    PL, ph = par_langue(site)
    out = []
    for i, p in enumerate(PL.get("fr", [])):
        autres = {lang: next((x for x in L if x["cc"] == p["cc"]), None) for lang, L in PL.items()}
        out.append(dict(cc=p["cc"], flag=p["flag"], key=p["lieux"][0]["key"], m=ph[p["lieux"][0]["key"]],
                        href={lang: "/" + PATH(x, lang) + "/" for lang, x in autres.items() if x},
                        nom={lang: x["nom"] for lang, x in autres.items() if x}, ville={lang: x["ville"] for lang, x in autres.items() if x}))
    return out
