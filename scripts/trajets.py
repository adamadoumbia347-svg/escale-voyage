"""Contenu propre à chaque grand trajet (pages françaises) : compagnies, escales, saison, bagages, formalités, FAQ.

Les informations sur les compagnies et les formalités changent : ce texte reste prudent (« en général », « à vérifier »)
et renvoie vers France Diplomatie. Mettre à jour la date VERIFIE après chaque relecture.
"""

VERIFIE = "octobre 2026"
DIPLO = "https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/"

# Phrases communes
FJ_OBLIG = "Le certificat de vaccination contre la fièvre jaune est exigé à l'arrivée : gardez le carnet international avec votre passeport."
FJ_RECO = "La vaccination contre la fièvre jaune est recommandée ; elle peut être demandée selon votre itinéraire (escale dans un pays à risque)."
PALU = "Un traitement préventif contre le paludisme est conseillé : parlez-en à votre médecin avant le départ."
BAG_AFRIQUE = ("Sur les lignes vers l'Afrique de l'Ouest et centrale, les grandes compagnies incluent souvent une valise en soute, "
               "parfois deux selon le tarif. Les tarifs les plus bas et certains vols avec escale n'incluent qu'un bagage cabine : "
               "vérifiez le nombre de valises et leur poids (souvent 23 kg) avant de comparer.")

TRAJETS = {
    ("CDG", "DSS"): dict(
        intro=("Paris – Dakar est l'une des lignes les plus fréquentées entre la France et l'Afrique de l'Ouest : familles de la diaspora, "
               "étudiants, voyageurs d'affaires et touristes vers la Petite-Côte ou la Casamance. Les vols arrivent à l'aéroport "
               "Blaise-Diagne (AIBD), à Diass, à environ 45 minutes à 1 heure de Dakar selon la circulation : prévoyez le trajet "
               "en taxi, en navette ou en train express régional (TER) jusqu'en ville."),
        direct="Air France (depuis Roissy) et Air Sénégal assurent des vols directs d'environ 5 h 30, avec plusieurs départs par semaine.",
        escales=("Avec escale, les options les plus courantes passent par Casablanca (Royal Air Maroc), Lisbonne (TAP), Madrid (Iberia), "
                 "Bruxelles (Brussels Airlines) ou Istanbul (Turkish Airlines). Ces vols coûtent parfois nettement moins cher que le direct "
                 "en haute saison, au prix de quelques heures de plus."),
        saison=("La saison sèche, de novembre à juin, est la plus agréable pour un séjour. Juillet-août correspond à l'hivernage (chaleur humide, "
                "pluies) mais aussi aux vacances de la diaspora : c'est la période la plus chère, avec les fêtes de fin d'année, la Tabaski "
                "et le Magal de Touba. Pour ces dates, réservez 3 à 4 mois à l'avance."),
        bagages=BAG_AFRIQUE,
        formalites=("Les voyageurs de nationalité française n'ont pas besoin de visa pour un séjour de moins de 90 jours ; un passeport valide "
                    "est demandé. " + FJ_RECO + " " + PALU),
        faq=[("Faut-il un visa pour aller à Dakar ?", "Pas pour les voyageurs français pour un séjour de moins de 90 jours. Les règles varient selon la nationalité : vérifiez sur France Diplomatie avant de partir."),
             ("Comment aller de l'aéroport AIBD au centre de Dakar ?", "En taxi, en navette ou en TER depuis Diamniadio. Comptez de 45 minutes à plus d'une heure selon la circulation.")],
    ),
    ("CDG", "BKO"): dict(
        intro=("Paris – Bamako relie la France à l'une des plus grandes diasporas d'Afrique de l'Ouest. Depuis 2023, l'offre de vols directs "
               "est très réduite : la plupart des voyageurs passent par une escale. Le bon réflexe est de comparer la durée totale "
               "et le temps de correspondance, pas seulement le prix."),
        direct=("Air France ne dessert plus Bamako depuis août 2023. Corsair a proposé des vols directs depuis Orly (environ 6 h), "
                "avec des interruptions : vérifiez s'ils sont programmés à vos dates."),
        escales=("Les trajets avec une escale sont la norme : Casablanca (Royal Air Maroc), Alger (Air Algérie), Tunis (Tunisair), "
                 "Istanbul (Turkish Airlines), Addis-Abeba (Ethiopian Airlines), Dakar (Air Sénégal) ou Abidjan (Air Côte d'Ivoire). "
                 "Les escales en Afrique du Nord sont souvent les plus courtes."),
        saison=("La période la plus agréable va de novembre à février, quand il fait plus frais et sec. Mars à mai est très chaud (souvent plus de 40 °C) "
                "et la saison des pluies s'étend de juin à septembre. Les prix les plus hauts tombent en juillet-août, pour les fêtes de fin "
                "d'année et autour de la Tabaski."),
        bagages=BAG_AFRIQUE + " Sur un trajet avec escale, vérifiez que la valise est enregistrée jusqu'à Bamako.",
        formalites=("Un visa est exigé pour les voyageurs de nationalité française. " + FJ_OBLIG + " " + PALU +
                    " Consultez les conseils aux voyageurs de France Diplomatie : la situation sécuritaire évolue."),
        faq=[("Y a-t-il des vols directs Paris – Bamako ?", "Plus d'Air France depuis 2023. Corsair a proposé des vols directs depuis Orly avec des interruptions : la plupart des trajets passent par une escale (Casablanca, Alger, Tunis, Istanbul, Addis-Abeba)."),
             ("Quelle escale choisir pour aller à Bamako ?", "Casablanca, Alger et Tunis offrent souvent les trajets les plus courts. Comparez la durée totale et assurez-vous que la valise est enregistrée jusqu'à Bamako.")],
    ),
    ("CDG", "ABJ"): dict(
        intro=("Paris – Abidjan est une ligne très concurrentielle : la capitale économique ivoirienne est un grand centre d'affaires et une "
               "destination majeure de la diaspora. Les vols arrivent à l'aéroport Félix-Houphouët-Boigny, à Port-Bouët, à une vingtaine "
               "de minutes du Plateau hors heures de pointe."),
        direct=("Plusieurs compagnies volent en direct, en 6 h 30 environ : Air France depuis Roissy, Air Côte d'Ivoire et Corsair depuis Orly. "
                "Air France et Air Côte d'Ivoire partagent leurs vols depuis fin octobre 2026."),
        escales=("Avec escale, on trouve Casablanca (Royal Air Maroc), Bruxelles (Brussels Airlines), Tunis (Tunisair), Istanbul (Turkish Airlines) "
                 "ou Addis-Abeba (Ethiopian Airlines). La concurrence sur le direct rend ces options moins souvent intéressantes qu'ailleurs."),
        saison=("Abidjan est chaude et humide toute l'année. La grande saison des pluies dure de mai à juillet ; de décembre à février, il pleut peu. "
                "Les prix montent en juillet-août et pour les fêtes de fin d'année, et baissent souvent en mai-juin et en septembre-octobre."),
        bagages=BAG_AFRIQUE,
        formalites=("Un visa est exigé pour les voyageurs de nationalité française (demande en ligne avant le départ). " + FJ_OBLIG + " " + PALU),
        faq=[("Quelles compagnies volent en direct Paris – Abidjan ?", "En général Air France depuis Roissy, Air Côte d'Ivoire et Corsair depuis Orly. Comparez les deux aéroports parisiens."),
             ("Faut-il un visa pour la Côte d'Ivoire ?", "Oui pour les voyageurs français : la demande se fait en ligne avant le départ. Le certificat de vaccination contre la fièvre jaune est aussi demandé.")],
    ),
    ("CDG", "CKY"): dict(
        intro=("Paris – Conakry est surtout empruntée par la diaspora guinéenne et les voyageurs d'affaires (mines, ONG). "
               "L'offre directe est limitée à quelques vols par semaine : en haute saison, les places partent vite."),
        direct="Air France assure quelques vols directs par semaine depuis Roissy, en 6 h environ.",
        escales=("Les vols avec escale passent par Casablanca (Royal Air Maroc), Dakar (Air Sénégal), Bruxelles (Brussels Airlines), "
                 "Istanbul (Turkish Airlines), Tunis (Tunisair) ou Abidjan (Air Côte d'Ivoire). Ils sont parfois nettement moins chers que le direct."),
        saison=("Conakry est l'une des capitales les plus pluvieuses d'Afrique : de juin à septembre, les pluies sont très fortes. "
                "La saison sèche, de novembre à avril, est la plus confortable. Les prix sont les plus hauts en juillet-août et pour les fêtes."),
        bagages=BAG_AFRIQUE,
        formalites=("Un visa est exigé pour les voyageurs de nationalité française (demande en ligne possible). " + FJ_RECO + " " + PALU),
        faq=[("Combien de vols directs par semaine entre Paris et Conakry ?", "Seulement quelques-uns, opérés par Air France. En haute saison, réservez tôt ou comparez avec les vols via Casablanca, Dakar ou Bruxelles."),
             ("Quelle est la meilleure période pour aller à Conakry ?", "La saison sèche, de novembre à avril. De juin à septembre, les pluies sont très abondantes.")],
    ),
    ("CDG", "DLA"): dict(
        intro=("Douala est la capitale économique du Cameroun et son principal port : la ligne Paris – Douala sert autant la diaspora que les affaires. "
               "Si votre destination finale est Yaoundé ou le centre du pays, comparez aussi avec un vol vers Yaoundé-Nsimalen (NSI)."),
        direct="Air France propose des vols directs depuis Roissy, en 6 h 30 à 7 h 30 environ selon les rotations.",
        escales=("Brussels Airlines dessert Douala via Bruxelles, souvent à bon prix. On trouve aussi Royal Air Maroc via Casablanca, "
                 "Turkish Airlines via Istanbul et Ethiopian Airlines via Addis-Abeba."),
        saison=("Douala est très humide et il y pleut une grande partie de l'année, surtout de juillet à septembre. "
                "Décembre à février est la période la plus sèche. Les prix montent en juillet-août et pour les fêtes de fin d'année."),
        bagages=BAG_AFRIQUE,
        formalites=("Un visa est exigé pour les voyageurs de nationalité française (demande en ligne possible). "
                    + FJ_OBLIG + " " + PALU),
        faq=[("Vaut-il mieux atterrir à Douala ou à Yaoundé ?", "Cela dépend de votre destination finale : la route entre les deux villes prend plusieurs heures. Comparez les deux aéroports, les prix varient beaucoup."),
             ("Brussels Airlines est-elle intéressante pour Douala ?", "Souvent : le passage par Bruxelles est fréquent sur cette ligne, et l'écart de prix avec le direct peut être important.")],
    ),
    ("CDG", "NSI"): dict(
        intro=("Yaoundé, la capitale politique du Cameroun, est desservie par l'aéroport de Nsimalen, à une trentaine de kilomètres du centre. "
               "Certains vols font un arrêt à Douala : regardez bien s'il s'agit d'un vol direct ou d'un vol avec arrêt."),
        direct="Air France relie Roissy à Yaoundé, avec selon les jours des vols sans escale (6 h 30 environ) ou des vols qui s'arrêtent à Douala.",
        escales="Avec escale : Bruxelles (Brussels Airlines), Istanbul (Turkish Airlines), Casablanca (Royal Air Maroc) ou Addis-Abeba (Ethiopian Airlines).",
        saison=("Yaoundé a un climat plus doux que Douala grâce à l'altitude. Les deux saisons sèches (décembre à février, puis juillet-août) "
                "sont les plus agréables. Juillet-août et les fêtes concentrent aussi les prix les plus élevés."),
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité française. " + FJ_OBLIG + " " + PALU,
        faq=[("Le vol Paris – Yaoundé est-il direct ?", "Pas toujours : selon les jours, Air France vole sans escale ou fait un arrêt à Douala. Vérifiez le détail du vol avant de réserver."),
             ("À quelle distance de Yaoundé est l'aéroport de Nsimalen ?", "Environ 30 km au sud du centre-ville, soit 30 à 45 minutes en voiture hors embouteillages.")],
    ),
    ("CDG", "LFW"): dict(
        intro=("Lomé, capitale du Togo, est aussi le siège de la compagnie ASKY, très présente en Afrique de l'Ouest. "
               "La ville est à environ 2 h 30 de route de Cotonou et à 3 h d'Accra : comparer ces trois aéroports peut faire économiser."),
        direct="Air France assure des vols directs depuis Roissy, à raison de quelques vols par semaine (6 h environ).",
        escales=("Avec escale : Casablanca (Royal Air Maroc), Bruxelles (Brussels Airlines), Addis-Abeba (Ethiopian Airlines, partenaire d'ASKY) "
                 "ou Istanbul (Turkish Airlines). ASKY permet ensuite de rejoindre de nombreuses villes de la région depuis Lomé."),
        saison=("La saison sèche, de novembre à mars, est la plus agréable (avec l'harmattan, vent sec, de décembre à février). "
                "Les pluies tombent surtout d'avril à juillet, puis en septembre-octobre. Prix les plus hauts en juillet-août et pour les fêtes."),
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité française (demande en ligne possible). " + FJ_OBLIG + " " + PALU,
        faq=[("Faut-il comparer Lomé avec Cotonou ou Accra ?", "Oui : les trois villes sont proches par la route et les prix des billets varient beaucoup d'un aéroport à l'autre."),
             ("Quelle compagnie relie Paris à Lomé sans escale ?", "Air France, avec quelques vols par semaine. ASKY prépare des vols long-courriers, mais vérifiez qu'ils sont programmés.")],
    ),
    ("CDG", "COO"): dict(
        intro=("Cotonou, capitale économique du Bénin, est reliée à Paris par des vols directs et par de nombreuses correspondances. "
               "Lomé n'est qu'à 2 h 30 de route : un billet vers l'un ou l'autre aéroport peut être beaucoup moins cher selon les dates."),
        direct="Air France propose des vols directs depuis Roissy, en 6 h environ.",
        escales=("Avec escale : Casablanca (Royal Air Maroc), Bruxelles (Brussels Airlines), Lomé (ASKY), Istanbul (Turkish Airlines) "
                 "ou Addis-Abeba (Ethiopian Airlines)."),
        saison=("Comme à Lomé, la saison sèche de novembre à mars est la plus agréable. Les pluies tombent d'avril à juillet et en septembre-octobre. "
                "La fête du Vodoun, le 10 janvier, attire de nombreux visiteurs à Ouidah : réservez tôt pour cette période."),
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité française (e-visa à demander en ligne). " + FJ_OBLIG + " " + PALU,
        faq=[("Faut-il un visa pour le Bénin ?", "Oui pour les voyageurs français : l'e-visa se demande en ligne avant le départ. Le carnet de vaccination contre la fièvre jaune est demandé."),
             ("Quand partir à Cotonou ?", "De novembre à mars, pendant la saison sèche. Évitez si possible avril-juillet, la saison des grandes pluies.")],
    ),
    ("CDG", "OUA"): dict(
        intro=("Paris – Ouagadougou est surtout utilisée par la diaspora burkinabè. Depuis 2023, l'offre directe depuis la France a fortement "
               "diminué : les trajets avec une escale en Afrique du Nord ou de l'Ouest sont devenus la règle."),
        direct="Air France a suspendu ses vols vers Ouagadougou en août 2023. Vérifiez s'ils ont repris à vos dates avant de compter sur un direct.",
        escales=("Les escales les plus courantes : Abidjan (Air Côte d'Ivoire), Casablanca (Royal Air Maroc), Alger (Air Algérie), Tunis (Tunisair), "
                 "Istanbul (Turkish Airlines), Bruxelles (Brussels Airlines) ou Addis-Abeba (Ethiopian Airlines)."),
        saison=("De novembre à février, il fait plus frais et sec. Mars à mai est très chaud, et la saison des pluies dure de juin à septembre. "
                "Le FESPACO (festival du cinéma, années impaires, fin février) et le SIAO font monter les prix à leurs dates."),
        bagages=BAG_AFRIQUE + " Avec une escale, vérifiez que la valise est enregistrée jusqu'à Ouagadougou.",
        formalites=("Un visa est exigé pour les voyageurs de nationalité française. " + FJ_OBLIG + " " + PALU +
                    " Consultez les conseils aux voyageurs de France Diplomatie : la situation sécuritaire évolue."),
        faq=[("Y a-t-il des vols directs Paris – Ouagadougou ?", "Air France a suspendu ses vols en 2023. Aujourd'hui, la plupart des trajets passent par Abidjan, Casablanca, Alger, Tunis ou Istanbul."),
             ("Quelle escale est la plus rapide pour Ouagadougou ?", "Souvent Abidjan, Casablanca ou Alger. Comparez la durée totale du voyage, qui varie de quelques heures selon la correspondance.")],
    ),
    ("CDG", "FIH"): dict(
        intro=("Paris – Kinshasa relie la France à la plus grande ville francophone du monde. L'aéroport de N'djili est à environ 25 km du centre "
               "(Gombe) : selon la circulation, le trajet peut prendre plus d'une heure."),
        direct=("Air France est la seule compagnie à assurer des vols réguliers sans escale entre Paris et Kinshasa (8 h environ). "
                "Air Congo a annoncé une ligne vers Paris : vérifiez si elle est ouverte à vos dates."),
        escales=("Bruxelles est l'escale historique (Brussels Airlines, Air Congo) : depuis Paris, un départ de Bruxelles en train peut revenir moins cher. "
                 "On trouve aussi Addis-Abeba (Ethiopian Airlines), Istanbul (Turkish Airlines) et Casablanca (Royal Air Maroc)."),
        saison=("La saison sèche, de juin à septembre, est la plus fraîche et la plus agréable. Il pleut beaucoup d'octobre à mai. "
                "Juillet-août et les fêtes de fin d'année sont les périodes les plus chères."),
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité française. " + FJ_OBLIG + " " + PALU,
        faq=[("Paris – Kinshasa : direct ou via Bruxelles ?", "Air France vole sans escale depuis Roissy. Via Bruxelles, le trajet est plus long mais souvent moins cher : comparez en ajoutant le train Paris–Bruxelles."),
             ("Combien de temps dure le vol Paris – Kinshasa ?", "Environ 8 heures sans escale. Avec une correspondance, comptez de 11 à plus de 15 heures selon l'escale.")],
    ),
    ("CDG", "LBV"): dict(
        intro=("Libreville, capitale du Gabon, est une destination d'affaires (pétrole, bois) et de diaspora. "
               "Les billets y sont parmi les plus chers d'Afrique centrale : comparer les dates et les escales fait vraiment la différence."),
        direct="Air France relie Roissy à Libreville sans escale, en 7 h 30 à 8 h environ.",
        escales="Avec escale : Casablanca (Royal Air Maroc), Addis-Abeba (Ethiopian Airlines), Istanbul (Turkish Airlines) ou Lomé (ASKY).",
        saison=("La grande saison sèche, de juin à août, est la plus agréable et la meilleure pour observer baleines et tortues sur la côte. "
                "Il pleut beaucoup d'octobre à mai. Prix les plus hauts en juillet-août et pour les fêtes."),
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité française (e-visa en ligne). " + FJ_OBLIG + " " + PALU,
        faq=[("Pourquoi les billets Paris – Libreville sont-ils chers ?", "La concurrence est faible sur le direct. Les vols avec escale à Casablanca, Addis-Abeba ou Istanbul sont parfois moins chers."),
             ("Quelle est la meilleure saison pour le Gabon ?", "La saison sèche, de juin à août : moins de pluie et des températures plus douces.")],
    ),
    ("CDG", "NKC"): dict(
        intro=("Paris – Nouakchott est une ligne peu desservie, utilisée surtout par la diaspora mauritanienne et les voyageurs d'affaires. "
               "Le nouvel aéroport Oumtounsy est à environ 25 km au nord de la ville."),
        direct="Air France assure quelques vols directs par semaine depuis Roissy (environ 4 h 30 à 5 h).",
        escales="Avec escale : Casablanca (Royal Air Maroc), Tunis (Tunisair) ou Istanbul (Turkish Airlines).",
        saison=("De novembre à mars, les températures sont agréables. De mai à septembre, il fait très chaud, avec des vents de sable. "
                "Les prix montent en été et autour des fêtes religieuses."),
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité française (e-visa ou visa à l'arrivée selon les cas). " + FJ_RECO,
        faq=[("Combien de vols directs entre Paris et Nouakchott ?", "Seulement quelques-uns par semaine, opérés par Air France. Sinon, passez par Casablanca, Tunis ou Istanbul."),
             ("Quand partir en Mauritanie ?", "De novembre à mars, quand la chaleur est supportable.")],
    ),
    ("ORY", "CMN"): dict(
        intro=("Casablanca est la porte d'entrée économique du Maroc et le hub de Royal Air Maroc vers toute l'Afrique. "
               "L'aéroport Mohammed-V est à environ 30 km du centre, relié par train (environ 40 minutes) et par taxi."),
        direct=("La ligne est très fréquentée : Royal Air Maroc, Air France et des compagnies à bas prix (dont Transavia) proposent des vols directs "
                "d'environ 3 h depuis Orly et Roissy."),
        escales="Inutile de faire une escale sur ce trajet. En revanche, Casablanca est souvent l'escale la moins chère vers l'Afrique de l'Ouest.",
        saison=("Climat doux toute l'année. Les prix flambent en juillet-août, pendant les vacances scolaires et autour de l'Aïd. "
                "Hors de ces périodes, les vols à bas prix rendent la ligne très abordable."),
        bagages=("Sur les compagnies à bas prix, le tarif de base n'inclut souvent qu'un petit sac : la valise en soute est payante. "
                 "Royal Air Maroc et Air France incluent souvent une valise selon le tarif. Ajoutez toujours le prix des bagages avant de comparer."),
        formalites=("Pas de visa pour les voyageurs de nationalité française pour un séjour de moins de 90 jours ; passeport valide demandé."),
        faq=[("Low cost ou Royal Air Maroc pour Casablanca ?", "Avec un seul bagage cabine, le low cost est souvent moins cher. Avec des valises, comparez le prix total : Royal Air Maroc peut revenir moins cher."),
             ("Comment aller de l'aéroport Mohammed-V à Casablanca ?", "En train (environ 40 minutes jusqu'au centre) ou en taxi.")],
    ),
    ("CDG", "RAK"): dict(
        intro=("Marrakech est l'une des destinations les plus populaires au départ de Paris, pour un week-end comme pour des vacances. "
               "L'aéroport Marrakech-Ménara est à une quinzaine de minutes de la médina."),
        direct=("Royal Air Maroc, Transavia, easyJet et d'autres compagnies volent en direct en 3 h 30 environ, depuis Orly, Roissy et Beauvais."),
        escales="Le direct est la norme et souvent le moins cher. Une escale n'a d'intérêt que pour combiner avec une autre ville du Maroc.",
        saison=("Le printemps (mars-mai) et l'automne (octobre-novembre) sont idéaux. L'été est très chaud (souvent plus de 40 °C). "
                "Les prix montent pendant les vacances scolaires françaises, surtout à la Toussaint, à Noël et à Pâques."),
        bagages=("Les compagnies à bas prix font payer la valise en soute, et parfois le bagage cabine : comparez le prix final. "
                 "Beauvais est moins bien desservi en transports : ajoutez le coût de la navette."),
        formalites="Pas de visa pour les voyageurs de nationalité française pour un séjour de moins de 90 jours ; passeport valide demandé.",
        faq=[("Quand partir à Marrakech pas cher ?", "Hors vacances scolaires : fin janvier, mars, mai-juin et novembre sont souvent les mois les plus abordables."),
             ("Orly, Roissy ou Beauvais pour Marrakech ?", "Les trois sont desservis. Beauvais est souvent moins cher, mais ajoutez le prix et le temps de la navette depuis Paris.")],
    ),
    ("CDG", "ALG"): dict(
        intro=("Paris – Alger est une ligne très chargée, surtout l'été et pendant les fêtes religieuses. "
               "L'aéroport Houari-Boumédiène est à une vingtaine de kilomètres du centre d'Alger."),
        direct=("Air Algérie, Air France et Transavia proposent des vols directs d'environ 2 h 15, depuis Roissy et Orly. "
                "D'autres villes françaises (Lyon, Marseille, Bordeaux…) sont aussi reliées à Alger."),
        escales="Le direct est la norme. Si les prix sont trop hauts, comparez avec un départ d'une autre ville française ou vers Oran ou Constantine.",
        saison=("Le printemps et l'automne sont les plus agréables. Juillet-août, le Ramadan, l'Aïd et les vacances scolaires concentrent les prix les plus élevés : "
                "pour l'été, réservez dès le début de l'année."),
        bagages=("Air Algérie inclut en général une ou deux valises selon le tarif. Transavia fait payer la valise : comparez le prix total. "
                 "En été, les excédents de bagages sont fréquents, vérifiez le poids autorisé."),
        formalites="Un visa est exigé pour les voyageurs de nationalité française (demande auprès des consulats d'Algérie).",
        faq=[("Quand réserver un Paris – Alger pour l'été ?", "Le plus tôt possible, idéalement dès janvier-février : les vols de juillet-août se remplissent très vite."),
             ("Quelles compagnies volent entre Paris et Alger ?", "En général Air Algérie, Air France et Transavia, en vols directs d'environ 2 h 15.")],
    ),
    ("CDG", "TUN"): dict(
        intro=("Paris – Tunis sert à la fois la diaspora tunisienne et les vacanciers. L'aéroport de Tunis-Carthage est tout proche du centre "
               "(environ 15 minutes) et de la banlieue nord (La Marsa, Sidi Bou Saïd)."),
        direct="Tunisair, Transavia, Air France et Nouvelair proposent des vols directs d'environ 2 h 15 depuis Orly et Roissy.",
        escales="Le direct est la norme. Pour la plage, comparez avec Djerba (DJE), Monastir (MIR) ou Enfidha (NBE), souvent moins chers en été.",
        saison=("Mai-juin et septembre-octobre sont idéaux : chaud sans excès. Juillet-août et l'Aïd sont les périodes les plus chères."),
        bagages="Transavia fait payer la valise en soute ; Tunisair et Air France l'incluent souvent selon le tarif. Comparez le prix total.",
        formalites="Pas de visa pour les voyageurs de nationalité française pour un séjour de moins de 90 jours ; passeport valide demandé.",
        faq=[("Tunis ou Djerba pour des vacances en Tunisie ?", "Pour la plage, Djerba ou Monastir sont souvent plus pratiques et parfois moins chers en été. Tunis convient pour la ville, Carthage et Sidi Bou Saïd."),
             ("Combien de temps dure le vol Paris – Tunis ?", "Environ 2 h 15 en vol direct.")],
    ),
    ("CDG", "YUL"): dict(
        intro=("Paris – Montréal est l'une des lignes transatlantiques les plus fréquentées : étudiants, expatriés, familles et touristes. "
               "L'aéroport Montréal-Trudeau est à une vingtaine de kilomètres du centre, relié par bus express (ligne 747)."),
        direct="Air Canada, Air France, Air Transat et Corsair proposent des vols directs d'environ 7 h 30 à l'aller (le retour est plus court).",
        escales="Le direct est très concurrentiel. Une escale (Reykjavik, Londres, New York) n'a d'intérêt que pour un prix très bas.",
        saison=("L'été (juin-août) est la saison des festivals mais aussi la plus chère. L'automne (septembre-octobre) offre les couleurs des érables "
                "et des prix plus doux. L'hiver est très froid, de décembre à mars, mais les billets sont souvent les moins chers en janvier-février."),
        bagages=("Sur l'Atlantique, les tarifs de base n'incluent souvent qu'un bagage cabine : la valise en soute est payante. "
                 "Comparez le prix avec bagage, surtout pour un départ d'études ou d'installation."),
        formalites=("Une autorisation de voyage électronique (AVE) est obligatoire pour les voyageurs de nationalité française arrivant par avion : "
                    "demandez-la uniquement sur le site officiel du gouvernement du Canada, quelques jours avant le départ."),
        faq=[("Faut-il un visa pour Montréal ?", "Pas de visa pour un séjour touristique, mais l'AVE (autorisation de voyage électronique) est obligatoire. Demandez-la sur le site officiel du Canada."),
             ("Quel est le mois le moins cher pour Paris – Montréal ?", "Souvent janvier-février et novembre, hors fêtes. L'été et Noël sont les périodes les plus chères.")],
    ),
    ("CDG", "DXB"): dict(
        intro=("Dubaï attire autant pour un séjour (soleil d'hiver, shopping) que comme escale vers l'Asie, l'océan Indien et l'Afrique de l'Est. "
               "L'aéroport international de Dubaï est relié au centre par métro."),
        direct="Emirates et Air France volent en direct depuis Roissy, en 6 h 30 à 7 h environ.",
        escales="Le direct est la norme. À l'inverse, Dubaï est une escale pratique : un arrêt de quelques jours ne coûte parfois rien de plus.",
        saison=("De novembre à mars, il fait chaud sans excès : c'est la haute saison, avec des prix plus élevés pendant les vacances scolaires. "
                "De juin à septembre, la chaleur est extrême mais les hôtels et les billets sont moins chers."),
        bagages="Emirates et Air France incluent généralement une valise en soute en classe économique, selon le tarif choisi.",
        formalites="Pas de visa préalable pour les voyageurs de nationalité française pour un séjour touristique court ; passeport valide au moins 6 mois.",
        faq=[("Quand partir à Dubaï pas cher ?", "En été (juin-septembre) les prix baissent, mais la chaleur est extrême. Le meilleur compromis : fin octobre-novembre ou mars, hors vacances."),
             ("Peut-on faire escale plusieurs jours à Dubaï ?", "Oui, de nombreux billets vers l'Asie ou l'océan Indien permettent un stop à Dubaï, parfois sans supplément.")],
    ),
    ("CDG", "IST"): dict(
        intro=("Istanbul est à la fois une destination de city-break et le hub de Turkish Airlines, l'une des escales les plus utilisées vers l'Afrique "
               "et l'Asie. Attention : la ville a deux aéroports, Istanbul (IST) côté européen et Sabiha-Gökçen (SAW) côté asiatique."),
        direct="Turkish Airlines, Air France et la compagnie à bas prix Pegasus volent en direct, en 3 h 15 environ.",
        escales="Le direct est la norme. Vérifiez l'aéroport d'arrivée : SAW est plus loin du centre historique.",
        saison=("Avril-juin et septembre-octobre sont idéaux. L'été est chaud et plus cher ; l'hiver est frais mais les billets sont souvent bon marché."),
        bagages="Turkish Airlines inclut souvent une valise selon le tarif ; les compagnies à bas prix la font payer. Comparez le prix total.",
        formalites="Pas de visa pour les voyageurs de nationalité française pour un séjour touristique de moins de 90 jours.",
        faq=[("Quel aéroport choisir à Istanbul ?", "IST (côté européen) est plus pratique pour le centre historique. SAW (côté asiatique) accueille surtout les compagnies à bas prix et est plus éloigné."),
             ("Istanbul est-elle une bonne escale vers l'Afrique ?", "Oui : Turkish Airlines dessert de nombreuses villes africaines depuis Istanbul, souvent à bon prix.")],
    ),
    ("CDG", "RUN"): dict(
        intro=("Paris – La Réunion est un long-courrier de 11 h environ vers l'aéroport Roland-Garros, à Saint-Denis. "
               "Les familles et les vacances scolaires font varier les prix très fortement selon les dates."),
        direct="Air France, Air Austral, Corsair et French bee proposent des vols directs, depuis Roissy ou Orly selon la compagnie.",
        escales="Le direct est la norme. Certains combinent avec une escale à Maurice ou Dubaï pour un prix plus bas ou un séjour combiné.",
        saison=("La saison sèche, de mai à novembre, est la plus agréable pour la randonnée. De janvier à mars, c'est la saison chaude et des cyclones. "
                "Les prix sont les plus hauts pendant les vacances scolaires, surtout en juillet-août et à Noël."),
        bagages="Les compagnies incluent souvent une valise en soute, mais certains tarifs économiques n'en ont pas : vérifiez avant de payer.",
        formalites="La Réunion est un département français : la carte d'identité ou le passeport suffit pour les voyageurs français.",
        faq=[("Quand partir à La Réunion pas cher ?", "Hors vacances scolaires : mai-juin et septembre-octobre offrent souvent le meilleur rapport prix-météo."),
             ("Faut-il un passeport pour La Réunion ?", "Non pour les voyageurs français : la carte d'identité suffit, c'est un département français.")],
    ),
}


def get(fr, to):
    return TRAJETS.get((fr, to))
