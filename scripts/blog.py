"""Blog d'Escale (français) : articles de conseils qui renvoient vers les pages trajets et fêtes.

Chaque article : slug, title (balise <title>), h1, desc, date (publication), maj (dernière mise à jour), lead, blocs, liens.
Blocs : ("h2", texte) | ("p", html) | ("ul", [html, …]) | ("ol", [html, …]) | ("tip", html).
Le HTML des blocs est écrit à la main ici (liens internes) : il n'est pas échappé.
"""
import json

BLOG_DIR = "blog"
R = lambda slug, txt: f'<a href="/{slug}/">{txt}</a>'

ARTICLES = [
    dict(
        slug="tabaski-2027-quand-acheter-billet",
        title="Tabaski 2027 : quand acheter son billet d'avion pour rentrer au pays ?",
        h1="Tabaski 2027 : quand acheter son billet d'avion ?",
        desc="Tabaski 2027 prévue vers le 16-17 mai : quand réserver, quels jours partir et comment payer moins cher son vol vers Dakar, Bamako, Abidjan ou Conakry.",
        date="2026-10-25", maj="2026-10-25",
        lead="La Tabaski est, avec les vacances d'été et les fêtes de fin d'année, la période où les billets vers l'Afrique de l'Ouest sont les plus chers. Bonne nouvelle : en 2027, elle tombe sur un week-end prolongé en France. Voici comment s'organiser.",
        blocks=[
            ("h2", "Quelle est la date de la Tabaski 2027 ?"),
            ("p", "La Tabaski (Aïd el-Kébir) 2027 est prévue vers le <strong>dimanche 16 ou le lundi 17 mai 2027</strong>. La date exacte est fixée par les autorités religieuses de chaque pays après l'observation de la lune : elle peut différer d'un jour entre le Sénégal, le Mali ou la Côte d'Ivoire."),
            ("p", "En France, le lundi 17 mai 2027 est aussi le <strong>lundi de Pentecôte</strong>. Beaucoup de salariés auront donc un week-end de trois jours, ce qui va concentrer les départs sur les jours précédents."),
            ("h2", "Quand réserver ?"),
            ("p", "Pour une période aussi demandée, le bon moment est <strong>3 à 5 mois avant</strong>, soit entre décembre et février. Les places les moins chères partent en premier, et les prix montent fortement dans les six dernières semaines."),
            ("ul", ["<strong>Décembre - février</strong> : la meilleure fenêtre pour réserver.",
                    "<strong>Mars - avril</strong> : encore possible, mais comparez bien les escales.",
                    "<strong>Mai</strong> : il reste des places, souvent chères. Les vols avec escale et les aéroports alternatifs deviennent indispensables."]),
            ("h2", "Quels jours partir ?"),
            ("p", "Les vols des deux ou trois jours qui précèdent la fête sont les plus demandés. Si vous le pouvez, partez <strong>en milieu de semaine, 5 à 7 jours avant</strong>, et rentrez quelques jours après : l'écart de prix peut être important."),
            ("tip", "Prévoyez une marge d'un jour : si la fête est annoncée le dimanche plutôt que le lundi, vous ne voulez pas atterrir le soir même."),
            ("h2", "Comment payer moins cher"),
            ("ol", ["<strong>Activez les dates flexibles (±3 jours)</strong> dans la recherche : décaler le départ d'un ou deux jours change souvent plus le prix que le choix du site.",
                    "<strong>Comparez les escales</strong> : Casablanca, Istanbul, Tunis, Alger ou Addis-Abeba sont parfois bien moins chers que le direct.",
                    "<strong>Comparez les aéroports de départ</strong> : Bruxelles, Lyon ou Marseille ont parfois des prix plus bas que Paris.",
                    "<strong>Comptez les valises</strong> : on rentre souvent chargé de cadeaux. Un billet qui inclut deux valises peut revenir moins cher qu'un tarif de base + bagages.",
                    "<strong>Créez une alerte prix</strong> dès maintenant pour suivre l'évolution."]),
            ("h2", "Les prix pour la Tabaski"),
            ("p", "Notre page " + R("vols-tabaski", "Vols pour la Tabaski 2027") + " affiche les prix repérés récemment pour un départ le 12 mai et un retour le 24 mai, vers les grandes villes d'Afrique de l'Ouest."),
        ],
        links=[("vol-paris-dakar", "Vol Paris → Dakar"), ("vol-paris-bamako", "Vol Paris → Bamako"), ("vol-paris-abidjan", "Vol Paris → Abidjan"),
               ("vol-paris-conakry", "Vol Paris → Conakry"), ("vols-tabaski", "Prix pour la Tabaski 2027")],
    ),
    dict(
        slug="ramadan-aid-2027-billet-avion",
        title="Ramadan et Aïd el-Fitr 2027 : réserver son vol au bon moment",
        h1="Ramadan et Aïd el-Fitr 2027 : réserver son vol au bon moment",
        desc="Ramadan 2027 prévu vers le 8 février, Aïd el-Fitr vers le 9-10 mars : quand réserver son vol vers le Maghreb ou l'Afrique de l'Ouest, et les pièges des vacances d'hiver.",
        date="2026-10-25", maj="2026-10-25",
        lead="En 2027, le Ramadan commence pendant les vacances d'hiver françaises. Les vols vers le Maghreb et l'Afrique de l'Ouest vont être très demandés en février, puis à nouveau autour de l'Aïd. Voici le calendrier et nos conseils.",
        blocks=[
            ("h2", "Les dates prévues"),
            ("ul", ["<strong>Début du Ramadan 2027</strong> : vers le lundi 8 février 2027.",
                    "<strong>Aïd el-Fitr 2027</strong> : vers le mardi 9 ou le mercredi 10 mars 2027.",
                    "Ces dates sont des estimations : elles dépendent de l'observation de la lune et peuvent varier d'un jour selon les pays."]),
            ("h2", "Attention aux vacances d'hiver"),
            ("p", "Les vacances d'hiver 2027 s'étalent du 6 février au 8 mars selon les zones (zone C du 6 au 22 février, zone A du 13 février au 1er mars, zone B du 20 février au 8 mars). Le début du Ramadan tombe en plein dedans : les vols du samedi de départ de chaque zone seront parmi les plus chers de l'hiver, surtout vers le Maroc, l'Algérie et la Tunisie."),
            ("tip", "Si vous voulez passer le début du Ramadan en famille sans enfants scolarisés, partez un mardi ou un mercredi, hors des samedis de départ en vacances."),
            ("h2", "Pour l'Aïd : réservez 2 à 4 mois avant"),
            ("p", "Pour rentrer pour l'Aïd el-Fitr, la demande monte fortement dans les deux semaines qui précèdent la fête. Réservez <strong>dès novembre-décembre</strong> pour les meilleures places, et visez un départ quelques jours avant le 9 mars."),
            ("ul", ["Choisissez si possible un <strong>billet modifiable</strong> : la date de l'Aïd peut changer d'un jour.",
                    "Les <strong>vols de nuit et de milieu de semaine</strong> sont souvent les moins chers.",
                    "Vers l'Algérie, comparez Alger, Oran et Constantine, et plusieurs villes de départ (Paris, Lyon, Marseille).",
                    "Vers le Maroc, Casablanca, Marrakech, Tanger, Fès et Oujda ont chacune leurs vols : choisissez l'aéroport le plus proche de votre famille."]),
            ("h2", "Voir les prix"),
            ("p", "La page " + R("vols-ramadan-aid-el-fitr", "Vols pour le Ramadan et l'Aïd el-Fitr 2027") + " affiche les prix repérés pour un départ le 4 mars et un retour le 18 mars 2027. Pour février, consultez aussi " + R("vols-vacances-hiver", "les vols des vacances d'hiver") + "."),
        ],
        links=[("vol-paris-alger", "Vol Paris → Alger"), ("vol-paris-casablanca", "Vol Paris → Casablanca"), ("vol-paris-tunis", "Vol Paris → Tunis"),
               ("vol-paris-oran", "Vol Paris → Oran"), ("vol-paris-dakar", "Vol Paris → Dakar")],
    ),
    dict(
        slug="billet-noel-afrique-encore-temps",
        title="Billet d'avion pour Noël vers l'Afrique : est-il encore temps ?",
        h1="Billet pour Noël vers l'Afrique : est-il encore temps ?",
        desc="Vacances de Noël du 19 décembre au 4 janvier : comment trouver encore un vol abordable vers Dakar, Abidjan, Bamako ou Douala quand les prix montent.",
        date="2026-10-25", maj="2026-10-25",
        lead="Fin octobre, les vols de Noël vers l'Afrique ont déjà commencé à monter. Il reste pourtant des solutions pour ne pas payer le prix fort : voici celles qui marchent le mieux.",
        blocks=[
            ("h2", "Les dates à retenir"),
            ("p", "Les vacances de Noël 2026 vont du <strong>samedi 19 décembre 2026 au lundi 4 janvier 2027</strong>, pour les trois zones. Les vols du 18 au 20 décembre sont les premiers à se remplir, suivis des retours du 2 au 4 janvier."),
            ("h2", "1. Décalez vos dates"),
            ("p", "Partir le mardi 22 ou le mercredi 23 décembre plutôt que le samedi 19, ou rentrer le mardi 5 janvier plutôt que le dimanche 3, fait souvent gagner plusieurs dizaines d'euros par billet. Activez les <strong>dates flexibles ±3 jours</strong> pour voir les écarts d'un coup d'œil."),
            ("h2", "2. Acceptez une escale"),
            ("p", "En période de fêtes, le direct est souvent le plus cher. Les vols via <strong>Casablanca, Istanbul, Bruxelles, Lisbonne ou Addis-Abeba</strong> restent fréquemment plus abordables. Vérifiez la durée de correspondance (voir notre article " + R("blog/vol-avec-escale-bien-choisir-correspondance", "sur les escales") + ")."),
            ("h2", "3. Changez d'aéroport de départ"),
            ("p", "Depuis le nord de la France, un départ de Bruxelles peut revenir moins cher, même en ajoutant le train. Depuis le sud, regardez Lyon et Marseille. Notre article " + R("blog/quel-aeroport-depart-afrique", "Paris, Bruxelles, Lyon ou Genève ?") + " compare les options."),
            ("h2", "4. Regardez l'aéroport d'arrivée"),
            ("p", "Lomé et Cotonou sont à 2 h 30 de route l'une de l'autre ; Douala et Yaoundé ont chacune leurs vols. Un billet vers l'aéroport voisin peut être nettement moins cher."),
            ("h2", "5. Ne réservez pas sur un coup de stress"),
            ("ul", ["Comparez au moins trois sites : les écarts sont fréquents en haute saison.",
                    "Ajoutez le prix des valises avant de comparer : le billet le moins cher n'inclut parfois qu'un bagage cabine.",
                    "Méfiez-vous des billets séparés (deux réservations différentes) : en cas de retard, la correspondance n'est pas garantie."]),
            ("p", "Les prix repérés pour Noël sont sur la page " + R("vols-noel", "Billets d'avion pour Noël 2026") + "."),
        ],
        links=[("vols-noel", "Prix pour Noël 2026"), ("vol-paris-dakar", "Vol Paris → Dakar"), ("vol-paris-abidjan", "Vol Paris → Abidjan"),
               ("vol-paris-douala", "Vol Paris → Douala"), ("vol-bruxelles-kinshasa", "Vol Bruxelles → Kinshasa")],
    ),
    dict(
        slug="vol-avec-escale-bien-choisir-correspondance",
        title="Vol avec escale : 8 règles pour bien choisir sa correspondance",
        h1="Vol avec escale : 8 règles pour bien choisir sa correspondance",
        desc="Temps de correspondance, billet unique ou billets séparés, visa de transit, bagages : comment choisir un vol avec escale sans mauvaise surprise.",
        date="2026-10-25", maj="2026-10-25",
        lead="Une escale peut faire économiser beaucoup, surtout vers l'Afrique. Mais une correspondance mal choisie peut aussi coûter cher : nuit à l'aéroport, valise perdue, vol manqué. Voici les règles à vérifier avant de payer.",
        blocks=[
            ("h2", "1. Préférez un billet unique"),
            ("p", "Quand les deux vols sont sur <strong>la même réservation</strong>, la compagnie doit vous replacer sur le vol suivant si le premier est en retard. Avec deux billets séparés (achetés séparément ou combinés par un site), vous êtes seul responsable : si vous manquez le second vol, il est perdu."),
            ("h2", "2. Vérifiez la durée de correspondance"),
            ("p", "Moins d'une heure, c'est risqué ; plus de 8 heures, c'est épuisant. Entre <strong>1 h 30 et 4 heures</strong> est souvent un bon compromis, surtout dans les grands aéroports (Istanbul, Paris-Charles-de-Gaulle, Casablanca, Addis-Abeba)."),
            ("h2", "3. Regardez si la valise suit"),
            ("p", "Sur un billet unique, la valise est en général enregistrée jusqu'à la destination finale. Demandez-le au comptoir et vérifiez l'étiquette. Sur des billets séparés, il faut souvent la récupérer et la réenregistrer, ce qui demande plus de temps."),
            ("h2", "4. Attention aux changements d'aéroport"),
            ("p", "Certaines villes ont plusieurs aéroports : Paris (Roissy et Orly), Istanbul (IST et Sabiha-Gökçen), Londres, Milan… Une correspondance entre deux aéroports demande plusieurs heures et un transport. Vérifiez le code de l'aéroport sur chaque vol."),
            ("h2", "5. Vérifiez les règles de transit"),
            ("p", "Selon votre nationalité, un <strong>visa de transit</strong> peut être demandé, même sans sortir de l'aéroport. C'est le cas pour certaines nationalités dans l'espace Schengen, par exemple. Vérifiez auprès de la compagnie ou de l'ambassade du pays d'escale avant de réserver."),
            ("h2", "6. Comptez la durée totale, pas seulement le prix"),
            ("p", "Un vol à 40 € de moins mais avec 10 heures de trajet en plus, une nuit à l'aéroport et un repas à payer n'est pas toujours une affaire. Comparez prix et durée ensemble."),
            ("h2", "7. Méfiez-vous des escales de nuit"),
            ("p", "Les correspondances entre minuit et 6 h sont fréquentes vers l'Afrique. Certaines compagnies proposent un hôtel pour les longues escales : renseignez-vous. Sinon, prévoyez de quoi vous reposer."),
            ("h2", "8. Gardez l'essentiel en cabine"),
            ("p", "Médicaments, papiers, chargeur et une tenue de rechange : en cas de valise retardée, vous serez tranquille."),
            ("tip", "Les escales les plus utilisées vers l'Afrique de l'Ouest et centrale : Casablanca (Royal Air Maroc), Istanbul (Turkish Airlines), Bruxelles (Brussels Airlines), Addis-Abeba (Ethiopian Airlines), Lisbonne (TAP), Tunis (Tunisair) et Alger (Air Algérie)."),
        ],
        links=[("vol-paris-bamako", "Vol Paris → Bamako (presque toujours avec escale)"), ("vol-paris-ouagadougou", "Vol Paris → Ouagadougou"),
               ("vol-paris-istanbul", "Vol Paris → Istanbul"), ("vol-paris-casablanca", "Vol Paris → Casablanca")],
    ),
    dict(
        slug="partir-au-pays-beaucoup-de-valises",
        title="Partir au pays avec beaucoup de valises : comment payer moins cher",
        h1="Partir au pays avec beaucoup de valises sans exploser son budget",
        desc="Deux valises, des cadeaux, un carton : comment comparer les franchises bagages, éviter l'excédent et choisir le bon billet pour un voyage chargé vers l'Afrique.",
        date="2026-10-25", maj="2026-10-25",
        lead="Quand on rentre voir la famille, on part rarement léger. Sur ces voyages, le prix des bagages peut changer complètement le classement des billets. Voici comment ne pas se faire piéger.",
        blocks=[
            ("h2", "Comparez le prix total, valises comprises"),
            ("p", "Un billet à 365 € sans valise peut revenir plus cher qu'un billet à 420 € avec une valise incluse, une fois la valise et le siège ajoutés. Avant de choisir, notez pour chaque offre : le nombre de valises incluses, leur poids maximal et le prix d'une valise en plus. Le <a href=\"/#calculateur\">calculateur du vrai prix</a> d'Escale fait l'addition pour vous."),
            ("h2", "Les grandes compagnies sont souvent plus généreuses"),
            ("p", "Sur les lignes vers l'Afrique de l'Ouest et centrale, les grandes compagnies incluent souvent une valise de 23 kg, parfois deux selon le tarif. Les tarifs « light » et les compagnies à bas prix n'incluent souvent qu'un bagage cabine. Quand on part avec deux valises, la compagnie qui semblait chère devient souvent la moins chère."),
            ("h2", "Ajoutez les valises au moment de réserver"),
            ("p", "Une valise ajoutée pendant la réservation coûte en général moins cher qu'après, et beaucoup moins cher qu'au comptoir le jour du départ. Si vous hésitez, ajoutez-la tout de suite."),
            ("h2", "Évitez l'excédent de poids"),
            ("ul", ["Pesez vos valises la veille avec un pèse-bagage (quelques euros).",
                    "Répartissez le poids : deux valises de 23 kg passent, une de 30 kg non.",
                    "Gardez quelques kilos de marge pour le retour.",
                    "Les objets lourds et fragiles (électronique, documents) voyagent mieux en cabine, dans la limite autorisée."]),
            ("h2", "Et pour les très gros volumes ?"),
            ("p", "Pour un déménagement ou de nombreux cartons, l'envoi par fret ou par groupage maritime peut être bien moins cher que des valises en plus, à condition de s'y prendre plusieurs semaines à l'avance. Comparez les deux solutions."),
            ("tip", "Sur un trajet avec escale, vérifiez que la franchise bagages est la même sur les deux vols : elle peut changer d'une compagnie à l'autre."),
            ("p", "Pour aller plus loin : " + R("guides/bagages-avion", "notre guide des bagages en avion") + "."),
        ],
        links=[("guides/bagages-avion", "Guide : bagages en avion"), ("vol-paris-dakar", "Vol Paris → Dakar"), ("vol-paris-kinshasa", "Vol Paris → Kinshasa"),
               ("vol-marseille-dakar", "Vol Marseille → Dakar")],
    ),
    dict(
        slug="quel-aeroport-depart-afrique",
        title="Paris, Bruxelles, Lyon ou Genève : quel aéroport de départ pour l'Afrique ?",
        h1="Paris, Bruxelles, Lyon ou Genève : d'où partir pour l'Afrique ?",
        desc="Roissy, Orly, Bruxelles, Lyon, Marseille, Genève : comparer les aéroports de départ pour trouver un vol moins cher vers l'Afrique et le Maghreb.",
        date="2026-10-25", maj="2026-10-25",
        lead="On compare souvent les dates et les compagnies, mais rarement l'aéroport de départ. Pourtant, partir de Bruxelles plutôt que de Paris, ou de Lyon plutôt que de Genève, peut changer le prix du tout au tout.",
        blocks=[
            ("h2", "Paris : le plus de choix"),
            ("p", "Roissy-Charles-de-Gaulle concentre la plupart des vols directs vers l'Afrique (Air France, Air Sénégal, Air Côte d'Ivoire…). Orly accueille Corsair, Transavia et de nombreuses lignes vers le Maghreb et les Antilles. <strong>Cherchez toujours sur les deux aéroports</strong> : l'écart de prix est fréquent."),
            ("h2", "Bruxelles : l'alternative du Nord"),
            ("p", "Brussels Airlines dessert historiquement l'Afrique centrale et de l'Ouest : Kinshasa, Douala, Dakar, Abidjan, Lomé, Cotonou, Conakry… Depuis Lille ou Paris, le train jusqu'à Bruxelles prend environ 1 h 25 depuis Paris : comparez le prix total, train compris."),
            ("h2", "Lyon et Marseille : pour le Sud et le Maghreb"),
            ("p", "Lyon et Marseille ont de nombreux vols directs vers l'Algérie, la Tunisie et le Maroc, souvent à bon prix hors été. Vers Dakar, Transavia propose quelques vols directs selon les saisons. Pour les autres destinations africaines, il faudra une escale."),
            ("h2", "Genève : pratique pour la Haute-Savoie et l'Ain"),
            ("p", "Genève propose de nombreux vols vers le Maghreb et des correspondances vers l'Afrique, mais peu de vols directs vers l'Afrique subsaharienne. Comparez avec Lyon, à environ 1 h 45 de route."),
            ("h2", "Comment comparer efficacement"),
            ("ol", ["Faites la même recherche depuis deux ou trois aéroports.",
                    "Ajoutez le coût et la durée du trajet jusqu'à l'aéroport (train, parking, navette).",
                    "Vérifiez les bagages inclus : ils varient d'une compagnie à l'autre.",
                    "Pensez à l'aller et au retour séparément : partir de Bruxelles et rentrer à Paris est parfois possible."]),
            ("tip", "Sur Escale, la recherche part de l'aéroport le plus proche de vous, mais vous pouvez changer le départ en un clic pour comparer."),
        ],
        links=[("vol-bruxelles-kinshasa", "Vol Bruxelles → Kinshasa"), ("vol-bruxelles-dakar", "Vol Bruxelles → Dakar"), ("vol-lyon-alger", "Vol Lyon → Alger"),
               ("vol-marseille-alger", "Vol Marseille → Alger"), ("vol-geneve-casablanca", "Vol Genève → Casablanca")],
    ),
    dict(
        slug="choisir-compagnie-aerienne-afrique",
        title="Quelle compagnie aérienne choisir pour aller en Afrique ?",
        h1="Quelle compagnie aérienne choisir pour aller en Afrique ?",
        desc="Air France, Air Sénégal, Royal Air Maroc, Turkish Airlines, Brussels Airlines, Ethiopian… Les critères pour choisir sa compagnie vers l'Afrique, au-delà du prix.",
        date="2026-10-25", maj="2026-10-25",
        lead="Vers l'Afrique, le choix de la compagnie compte autant que le prix : direct ou escale, bagages inclus, horaires, programme de fidélité. Voici les critères qui font vraiment la différence.",
        blocks=[
            ("h2", "Direct ou escale ?"),
            ("p", "Les compagnies qui volent en direct depuis la France (Air France, Air Sénégal, Air Côte d'Ivoire, Corsair selon les lignes) font gagner du temps. Les compagnies qui passent par leur « hub » (Royal Air Maroc via Casablanca, Turkish Airlines via Istanbul, Brussels Airlines via Bruxelles, Ethiopian Airlines via Addis-Abeba) sont souvent moins chères et desservent plus de villes."),
            ("h2", "Les bagages inclus"),
            ("p", "C'est souvent le critère décisif pour un voyage en famille. Regardez le nombre de valises incluses dans le tarif choisi, et non dans le « meilleur » tarif de la compagnie. Lisez notre article " + R("blog/partir-au-pays-beaucoup-de-valises", "sur les voyages avec beaucoup de valises") + "."),
            ("h2", "Les alliances et les miles"),
            ("p", "Si vous voyagez souvent, regrouper vos vols dans une même alliance permet de cumuler des miles et des avantages :"),
            ("ul", ["<strong>SkyTeam</strong> : Air France, KLM, Kenya Airways…",
                    "<strong>Star Alliance</strong> : Brussels Airlines, Turkish Airlines, Ethiopian Airlines, TAP…",
                    "<strong>oneworld</strong> : Royal Air Maroc, Iberia, Qatar Airways…",
                    "Air Sénégal, Air Algérie, Tunisair ou ASKY ont leurs propres programmes ou partenariats."]),
            ("h2", "Horaires et correspondances"),
            ("p", "Beaucoup de vols vers l'Afrique arrivent tard le soir ou partent dans la nuit. Si vous êtes attendu à l'aéroport ou si vous avez une longue route ensuite, l'horaire d'arrivée peut valoir quelques euros de plus."),
            ("h2", "Flexibilité"),
            ("p", "Pour les fêtes religieuses dont la date peut changer d'un jour, ou pour un voyage familial, un billet modifiable évite de tout perdre. Comparez les conditions de modification avant de payer."),
            ("tip", "Escale ne vend pas de billets : nous comparons les offres des sites partenaires. Vérifiez toujours les conditions (bagages, modification) sur la page de réservation."),
        ],
        links=[("vol-paris-dakar", "Vol Paris → Dakar"), ("vol-paris-abidjan", "Vol Paris → Abidjan"), ("vol-paris-lome", "Vol Paris → Lomé"),
               ("vol-paris-libreville", "Vol Paris → Libreville")],
    ),
]


def _blocks(blocks):
    out = []
    for kind, val in blocks:
        if kind == "h2":
            out.append(f"<h2>{val}</h2>")
        elif kind == "p":
            out.append(f"<p>{val}</p>")
        elif kind in ("ul", "ol"):
            out.append(f'<{kind} class="{"steps" if kind == "ol" else "plain"}">' + "".join(f"<li>{x}</li>" for x in val) + f"</{kind}>")
        elif kind == "tip":
            out.append(f'<p class="tip"><strong>Astuce :</strong> {val}</p>')
    return "\n".join(out)


def _date_fr(d):
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    y, m, j = d.split("-")
    return f"{int(j)} {mois[int(m) - 1]} {y}"


def build(page, E, domain, extras=""):
    """Écrit le blog (index + articles) avec la fonction page() de build_pages. Renvoie les URL pour le sitemap."""
    urls = []
    for a in ARTICLES:
        path = f"{BLOG_DIR}/{a['slug']}"
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "BlogPosting", "headline": a["h1"], "description": a["desc"],
            "datePublished": a["date"], "dateModified": a["maj"], "inLanguage": "fr",
            "mainEntityOfPage": f"{domain}/{path}/", "image": f"{domain}/og-image.png",
            "author": {"@type": "Organization", "name": "Escale", "url": f"{domain}/"},
            "publisher": {"@type": "Organization", "name": "Escale", "logo": {"@type": "ImageObject", "url": f"{domain}/icon-512.png"}},
        }, ensure_ascii=False) + "</script>"
        hero = (f'<p class="eyebrow"><a href="/{BLOG_DIR}/">Blog</a></p><h1>{E(a["h1"])}</h1>'
                f'<p class="lead">{E(a["lead"])}</p><p class="small">Publié le {_date_fr(a["date"])}'
                + (f" · mis à jour le {_date_fr(a['maj'])}" if a["maj"] != a["date"] else "") + "</p>")
        others = [o for o in ARTICLES if o is not a][:3]
        body = (f'<article class="post">{_blocks(a["blocks"])}</article>'
                '<section><p><a class="btn" href="/?type=vols">Comparer les prix des vols</a></p></section>'
                + extras +
                '<section><h2>Pages utiles</h2><ul class="route-links">'
                + "".join(f'<li><a href="/{s}/">{E(t)}</a></li>' for s, t in a["links"]) + "</ul></section>"
                '<section><h2>À lire aussi</h2><ul class="links">'
                + "".join(f'<li><a href="/{BLOG_DIR}/{o["slug"]}/">{E(o["h1"])}</a></li>' for o in others) + "</ul></section>")
        urls.append(page(path, a["title"], a["desc"], hero, body, ld))
    items = "".join(
        f'<li><a href="/{BLOG_DIR}/{a["slug"]}/"><strong>{E(a["h1"])}</strong></a><br><span class="small">{E(a["desc"])}</span></li>'
        for a in sorted(ARTICLES, key=lambda x: x["date"], reverse=True))
    hero = '<h1>Le blog d\'Escale</h1><p class="lead">Conseils pour payer moins cher son billet d\'avion : fêtes, escales, bagages, aéroports et compagnies.</p>'
    urls.append(page(BLOG_DIR, "Blog voyage : conseils pour payer moins cher son billet | Escale",
                     "Les conseils d'Escale pour payer moins cher son billet d'avion vers l'Afrique, le Maghreb et ailleurs : fêtes, escales, bagages, aéroports.",
                     hero, f'<section><ul class="links blog-list">{items}</ul></section>'))
    return urls
