"""« Que visiter » : explorer le monde pays par pays (demande de Dobam, 12 novembre 2026).
  /visiter/            tous les pays, par région
  /visiter/<pays>/     un pays : ses villes et ses lieux à voir, chacun avec une vraie photo créditée
Photos : Wikimedia Commons, licences libres ; auteur et licence dans site/data/visiter-photos.json (repris sur /credits-photos/).
Règles : aucun prix, aucune règle de visa, de santé ou de sécurité ; uniquement des repères stables (lieu, ce qu'on y voit, classement UNESCO).
Un lieu sans photo n'est pas publié ; un pays avec moins de 5 lieux en photo n'est pas publié."""
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
    dict(cc="jp", slug="japon", nom="Japon", en="au Japon", de="du Japon", flag="🇯🇵", air="TYO", ville="Tokyo", region="Asie",
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
    dict(cc="us", slug="etats-unis", nom="États-Unis", en="aux États-Unis", de="des États-Unis", flag="🇺🇸", air="NYC", ville="New York", region="Amériques",
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
REGIONS = ["Afrique", "Europe", "Asie", "Amériques"]
HEART = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 21s-7.5-4.6-10-9.3C.4 8.300 2.300 4.500 6 4.500c2 0 3.400 1 4.300 2.300.300.500 1.100.500 1.400 0C12.600 5.500 14 4.500 16 4.500c3.700 0 5.600 3.800 4 7.200C19.500 16.400 12 21 12 21z"/></svg>'
ENVIES = ('<section id="vx-envies" class="vx-envies" hidden><h2>Mes envies <span data-envies-n></span></h2><p class="small">Les lieux que vous avez marqués d\'un cœur. Ils restent dans ce téléphone, sans compte.</p><ul></ul></section>')
PATH = lambda p: f"visiter/{p['slug']}"


def photos(site):
    f = site / "data" / "visiter-photos.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def img(ph, key, cls="", eager=False, sizes="(min-width:700px) 440px, 100vw"):
    m = ph[key]
    return (f'<img src="/img/visiter/{key}.webp" srcset="/img/visiter/{key}-640.webp 640w, /img/visiter/{key}.webp {m["w"]}w" sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" alt="{E(m["alt"])}"'
            + (' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"') + (f' class="{cls}"' if cls else "") + ">")


def cred(ph, key):
    m = ph[key]
    return f'<p class="vx-cred">Photo : <a href="{E(m["page"])}" target="_blank" rel="noopener">{E(m["author"])}</a>, {E(m["license"])}, Wikimedia Commons</p>'


def publies(site):
    ph = photos(site)
    out = []
    for p in PAYS:
        lieux = [l for l in p["lieux"] if l["key"] in ph]
        if len(lieux) >= 5:
            out.append(dict(p, lieux=lieux))
    return out, ph


def build(site, ctx):
    pays, ph = publies(site)
    if not pays:
        return []
    for p in pays:
        for l in p["lieux"]:
            ph[l["key"]]["alt"] = f"{l['nom']}, {p['nom']}"
    urls = []
    for i, p in enumerate(pays):
        L = p["lieux"]
        hero = (f'<div class="vx"><p class="eyebrow">Explorer le monde · {E(p["region"])}</p><h1>Que visiter {E(p["en"])} <span>{p["flag"]}</span></h1>'
                f'<p class="hero-lead">{E(p["accroche"])} {len(L)} villes et lieux à voir, en photos.</p></div>')
        chips = '<nav class="vx-chips" aria-label="Lieux">' + "".join(f'<a href="#{l["key"]}">{E(l["nom"])}</a>' for l in L) + "</nav>"
        top = (f'<figure class="vx-hero">{img(ph, L[0]["key"], eager=True, sizes="(min-width:860px) 828px, 100vw")}<figcaption><span class="vx-title">{E(p["nom"])}</span>'
               f'<span class="vx-sub">{len(L)} lieux à voir · {E(", ".join(l["nom"] for l in L[:4]))}…</span></figcaption></figure>')
        cards = "".join(f'<article class="vx-card" id="{l["key"]}"><div class="vx-ph"><span class="vx-kind">{E(l["kind"])}</span><span class="vx-n">{n}</span>{img(ph, l["key"])}<button type="button" class="vx-like" data-k="{l["key"]}" data-n="{E(l["nom"])}" data-p="{E(p["nom"])}" aria-pressed="false" aria-label="Ajouter {E(l["nom"])} à mes envies">{HEART}</button></div>'
                        f'<div class="vx-tx"><h2>{E(l["nom"])}</h2><p>{l["txt"]}</p>{cred(ph, l["key"])}</div></article>' for n, l in enumerate(L, 1))
        autres = [pays[(i + k) % len(pays)] for k in (1, 2, 3)]
        cta = (f'<section class="vx-cta" data-air="{p["air"]}" data-ville="{E(p["ville"])}"><h2>Envie de partir {E(p["en"])} ?</h2><p>Comparez les vols pour {E(p["ville"])} et choisissez vos dates.</p>'
               '<p class="vx-dep"><label>Je pars de <select aria-label="Ville de départ"><option value="">choisir une ville</option></select></label></p><p class="vx-prix" role="status"></p>'
               f'<a class="btn" href="/?type=vols&amp;to={p["air"]}">Voir les vols pour {E(p["ville"])}</a><a class="btn ghost" href="/partout/">Voir les prix partout dans le monde</a>'
               f'<button type="button" class="btn ghost" id="vx-share" data-t="Que visiter {E(p["en"])} : {len(L)} villes et lieux à voir, en photos">Partager cette page</button></section>')
        suite = ('<section><h2>Continuer le voyage</h2><div class="vx-hub">' + "".join(
            f'<a href="/{PATH(a)}/">{img(ph, a["lieux"][0]["key"], sizes="(min-width:700px) 270px, 50vw")}<span class="vx-hl"><h3>{E(a["nom"])} {a["flag"]}</h3><small>{len(a["lieux"])} lieux à voir</small></span></a>' for a in autres)
            + '</div><p><a href="/visiter/">Tous les pays à explorer</a></p></section>')
        note = ('<p class="small">Ces repères sont généraux et ne remplacent pas un guide. Avant de partir, vérifiez les conditions d\'entrée du pays avec '
                '<a href="/visa/">l\'outil visa</a> et auprès des autorités. Photos : Wikimedia Commons, licences libres, <a href="/credits-photos/">tous les crédits</a>.</p>')
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": f"Que visiter {p['en']}", "itemListElement": [
            {"@type": "ListItem", "position": n, "name": l["nom"], "url": f"{ctx['domain']}/{PATH(p)}/#{l['key']}"} for n, l in enumerate(L, 1)]}, ensure_ascii=False) + "</script>"
        body = top + cred(ph, L[0]["key"]) + chips + f'<div class="vx-list">{cards}</div>' + cta + ENVIES + suite + note + '<script src="/visiter.js" defer></script>'
        urls.append(B.write(site, PATH(p), "fr", f"Que visiter {p['en']} : {len(L)} villes et lieux à voir | Escale",
                            f"{p['nom']} en photos : {', '.join(l['nom'] for l in L[:6])}… Les villes et les lieux à voir, avec de vraies photos, et les vols pour {p['ville']}.",
                            hero, body, ld, {"fr": PATH(p)}, ctx, og=f"img/visiter/{L[0]['key']}.webp"))
    # --- sommaire
    hero = ('<div class="vx"><p class="eyebrow">Explorer le monde</p><h1>Que visiter, <span>pays par pays</span></h1>'
            f'<p class="hero-lead">Pas seulement les capitales : pour chaque pays, ses villes et ses lieux à voir, avec de vraies photos. {len(pays)} pays pour commencer, d\'autres arrivent.</p></div>')
    body = ('<p class="vx-search"><label for="vx-q">Chercher un pays ou un lieu</label><input id="vx-q" type="search" placeholder="Japon, Kyoto, plage, safari…" autocomplete="off"><span id="vx-q-msg" class="small" role="status"></span></p>' + ENVIES)
    for r in REGIONS:
        ps = [p for p in pays if p["region"] == r]
        if not ps:
            continue
        body += f'<h2 class="vx-reg">{E(r)}</h2><div class="vx-hub">' + "".join(
            f'<a href="/{PATH(p)}/" data-mots="{E(p["nom"] + " " + p["region"] + " " + " ".join(l["nom"] + " " + l["kind"] for l in p["lieux"]))}">{img(ph, p["lieux"][0]["key"], sizes="(min-width:700px) 270px, 50vw", eager=(r == REGIONS[0] and k < 2))}<span class="vx-hl"><h3>{E(p["nom"])} {p["flag"]}</h3>'
            f'<small>{E(", ".join(l["nom"] for l in p["lieux"][:3]))}…</small></span></a>' for k, p in enumerate(ps)) + "</div>"
    body += ('<section><h2>Et pour partir</h2><ul><li><a href="/partout/">Les prix des vols partout dans le monde</a></li><li><a href="/surprends-moi/">Surprends-moi : une destination au hasard selon votre budget</a></li>'
             '<li><a href="/quiz-destination/">Quiz : quelle destination est faite pour moi ?</a></li></ul></section>'
             '<p class="small">Photos : Wikimedia Commons, licences libres, <a href="/credits-photos/">tous les crédits</a>.</p><script src="/visiter.js" defer></script>')
    urls.append(B.write(site, "visiter", "fr", "Que visiter : le monde pays par pays, en photos | Escale",
                        "Explorez le monde pays par pays : les villes et les lieux à voir, avec de vraies photos. " + ", ".join(p["nom"] for p in pays[:8]) + "…",
                        hero, body, "", {"fr": "visiter"}, ctx))
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
    """Pays publiés, pour l'accueil et le pied de page."""
    pays, ph = publies(site)
    return [(PATH(p), p["nom"], p["flag"], p["lieux"][0]["key"], ph[p["lieux"][0]["key"]]) for p in pays]
