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

# Phrases pour les départs de Belgique et de Suisse
SANS_VISA_UE = "Pas de visa pour les ressortissants de l'Union européenne et de la Suisse pour un séjour de moins de 90 jours ; passeport valide demandé."
BAG_MAGHREB = ("Les compagnies à bas prix font payer la valise en soute ; les compagnies nationales l'incluent souvent selon le tarif. "
               "En été, beaucoup de voyageurs partent chargés : comparez le prix total avec le nombre de valises dont vous avez besoin.")

TRAJETS.update({
    ("BRU", "FIH"): dict(
        natio="belge ou française",
        intro=("Bruxelles – Kinshasa est la ligne historique entre l'Europe et la RD Congo : la Belgique accueille une importante diaspora congolaise "
               "et Brussels Airlines dessert Kinshasa depuis des décennies. Depuis le nord de la France, un départ de Bruxelles est souvent "
               "une bonne alternative à Paris, même en ajoutant le train."),
        direct=("Brussels Airlines vole en direct en 8 h environ. Air Congo a ouvert une ligne Kinshasa – Bruxelles en 2026 : "
                "vérifiez ses jours de vol et ses conditions de bagages."),
        escales="Avec escale : Addis-Abeba (Ethiopian Airlines), Istanbul (Turkish Airlines), Casablanca (Royal Air Maroc) ou Paris (Air France).",
        saison=("La saison sèche, de juin à septembre, est la plus fraîche. Il pleut beaucoup d'octobre à mai. "
                "Les prix montent en juillet-août et pour les fêtes de fin d'année."),
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité belge ou française. " + FJ_OBLIG + " " + PALU,
        faq=[("Bruxelles ou Paris pour aller à Kinshasa ?", "Comparez les deux : Brussels Airlines (Bruxelles) et Air France (Paris) volent en direct. Le train entre Paris et Bruxelles prend environ 1 h 25."),
             ("Combien de temps dure le vol Bruxelles – Kinshasa ?", "Environ 8 heures sans escale.")],
    ),
    ("BRU", "DSS"): dict(
        natio="belge ou française",
        intro=("Bruxelles – Dakar sert la diaspora sénégalaise de Belgique et du nord de la France, ainsi que les touristes vers la Petite-Côte. "
               "Les vols arrivent à l'aéroport Blaise-Diagne (AIBD), à 45 minutes à 1 heure de Dakar."),
        direct=("Brussels Airlines assure l'essentiel des vols directs (environ 6 h). Air Sénégal a ouvert une ligne Dakar – Bruxelles fin 2025, "
                "avec quelques vols par semaine."),
        escales="Avec escale : Lisbonne (TAP), Casablanca (Royal Air Maroc), Madrid (Iberia) ou Paris (Air France).",
        saison=("La saison sèche, de novembre à juin, est la plus agréable. Juillet-août, les fêtes de fin d'année, la Tabaski et le Magal "
                "sont les périodes les plus chères."),
        bagages=BAG_AFRIQUE,
        formalites=SANS_VISA_UE + " " + FJ_RECO + " " + PALU,
        faq=[("Quelles compagnies volent en direct entre Bruxelles et Dakar ?", "Brussels Airlines, et Air Sénégal depuis fin 2025 avec quelques vols par semaine."),
             ("Faut-il un visa pour le Sénégal depuis la Belgique ?", "Pas pour les ressortissants de l'Union européenne pour moins de 90 jours. Les autres nationalités doivent vérifier les règles avant de partir.")],
    ),
    ("BRU", "ABJ"): dict(
        natio="belge ou française",
        intro=("Bruxelles – Abidjan est une alternative à Paris pour la diaspora ivoirienne de Belgique et du nord de la France. "
               "L'offre directe est plus limitée qu'au départ de Paris : comparez toujours les deux villes."),
        direct="Brussels Airlines assure quelques vols directs par semaine (7 h environ, certains vols faisant un arrêt en route).",
        escales="Avec escale : Paris (Air France, Air Côte d'Ivoire), Casablanca (Royal Air Maroc), Istanbul (Turkish Airlines) ou Addis-Abeba (Ethiopian Airlines).",
        saison=("Abidjan est chaude et humide toute l'année ; la grande saison des pluies dure de mai à juillet. "
                "Prix les plus hauts en juillet-août et pour les fêtes de fin d'année."),
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité belge ou française (demande en ligne). " + FJ_OBLIG + " " + PALU,
        faq=[("Le vol Bruxelles – Abidjan est-il direct ?", "Brussels Airlines propose quelques vols par semaine, parfois avec un arrêt en route. Sinon, passez par Paris, Casablanca ou Istanbul."),
             ("Vaut-il mieux partir de Paris pour Abidjan ?", "Paris a beaucoup plus de vols directs (Air France, Air Côte d'Ivoire, Corsair). Comparez en ajoutant le prix du train.")],
    ),
    ("BRU", "DLA"): dict(
        natio="belge ou française",
        intro=("Bruxelles – Douala est l'une des lignes phares de Brussels Airlines vers l'Afrique centrale, très utilisée par la diaspora camerounaise "
               "de Belgique, mais aussi depuis la France par ceux qui cherchent une alternative à Air France."),
        direct="Brussels Airlines dessert Douala quelques fois par semaine ; certains vols s'arrêtent à Yaoundé (ou inversement).",
        escales="Avec escale : Paris (Air France), Casablanca (Royal Air Maroc), Istanbul (Turkish Airlines) ou Addis-Abeba (Ethiopian Airlines).",
        saison="Décembre à février est la période la plus sèche. Il pleut beaucoup de juillet à septembre. Prix les plus hauts en juillet-août et pour les fêtes.",
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité belge ou française. " + FJ_OBLIG + " " + PALU,
        faq=[("Le vol Bruxelles – Douala fait-il un arrêt ?", "Certains vols de Brussels Airlines passent par Yaoundé. Regardez le détail du vol : la durée totale change."),
             ("Douala ou Yaoundé depuis Bruxelles ?", "Brussels Airlines dessert les deux villes. Choisissez selon votre destination finale, la route entre les deux prend plusieurs heures.")],
    ),
    ("MRS", "ALG"): dict(
        intro=("Marseille – Alger est l'une des lignes les plus chargées de Provence, portée par la diaspora algérienne du sud de la France. "
               "Le vol ne dure qu'environ 1 h 30 : c'est souvent la façon la plus rapide de rejoindre l'Algérie depuis le Sud."),
        direct="Air Algérie et des compagnies françaises (dont Transavia, selon les saisons) proposent des vols directs d'environ 1 h 30.",
        escales="Le direct est la norme. Si les prix sont trop hauts, comparez avec Oran, Constantine ou Béjaïa, ou un départ de Lyon ou Montpellier.",
        saison=("Juillet-août, le Ramadan, l'Aïd et les vacances scolaires concentrent les prix les plus élevés. "
                "Pour l'été, réservez dès le début de l'année : les vols se remplissent très vite."),
        bagages=BAG_MAGHREB,
        formalites="Un visa est exigé pour les voyageurs de nationalité française (demande auprès des consulats d'Algérie).",
        faq=[("Combien de temps dure le vol Marseille – Alger ?", "Environ 1 h 30 sans escale."),
             ("Quand réserver un Marseille – Alger pour l'été ?", "Dès janvier-février si possible : juillet-août est la période la plus demandée de l'année.")],
    ),
    ("MRS", "TUN"): dict(
        intro=("Marseille – Tunis est un vol court (environ 1 h 30) très utilisé par la diaspora tunisienne et les vacanciers du sud de la France."),
        direct="Tunisair, Transavia et Nouvelair proposent des vols directs, plus nombreux en été.",
        escales="Le direct est la norme. Pour la plage, comparez avec Djerba, Monastir ou Enfidha, souvent desservis depuis Marseille en été.",
        saison="Mai-juin et septembre-octobre sont idéaux. Juillet-août et l'Aïd sont les périodes les plus chères.",
        bagages=BAG_MAGHREB,
        formalites="Pas de visa pour les voyageurs de nationalité française pour un séjour de moins de 90 jours ; passeport valide demandé.",
        faq=[("Quelles compagnies relient Marseille à Tunis ?", "En général Tunisair, Transavia et Nouvelair, en vols directs d'environ 1 h 30."),
             ("Quand partir en Tunisie depuis Marseille ?", "En mai-juin ou en septembre-octobre : il fait beau et les prix sont plus doux qu'en été.")],
    ),
    ("MRS", "DSS"): dict(
        intro=("Marseille – Dakar évite de monter à Paris pour la diaspora sénégalaise du sud de la France. "
               "L'offre directe est limitée à quelques vols par semaine, avec des tarifs parfois très bas hors saison."),
        direct="Transavia assure quelques vols directs par semaine (environ 5 h), avec une offre qui varie selon les saisons.",
        escales="Avec escale : Paris (Air France), Casablanca (Royal Air Maroc), Lisbonne (TAP) ou Madrid (Iberia).",
        saison=("La saison sèche, de novembre à juin, est la plus agréable. Juillet-août, les fêtes et la Tabaski sont les périodes les plus chères."),
        bagages=("Transavia fait payer la valise en soute : ajoutez son prix pour comparer avec un vol via Paris ou Casablanca, "
                 "qui inclut souvent une ou deux valises."),
        formalites="Pas de visa pour les voyageurs de nationalité française pour moins de 90 jours. " + FJ_RECO + " " + PALU,
        faq=[("Y a-t-il des vols directs Marseille – Dakar ?", "Oui, Transavia propose quelques vols par semaine, plus ou moins nombreux selon la saison."),
             ("Low cost direct ou vol avec escale pour Dakar ?", "Avec beaucoup de bagages, un vol avec escale incluant les valises peut revenir moins cher. Comparez le prix total.")],
    ),
    ("LYS", "CMN"): dict(
        intro=("Lyon – Casablanca relie la deuxième agglomération française au cœur économique du Maroc, en un peu moins de 3 heures. "
               "Casablanca est aussi une escale pratique vers l'Afrique de l'Ouest avec Royal Air Maroc."),
        direct="Royal Air Maroc et des compagnies à bas prix proposent des vols directs d'environ 2 h 45.",
        escales="Le direct est la norme. Pour d'autres villes du Maroc (Marrakech, Agadir, Oujda, Fès), Lyon a aussi des vols directs.",
        saison="Climat doux toute l'année. Les prix flambent en juillet-août, pendant les vacances scolaires et autour de l'Aïd.",
        bagages=BAG_MAGHREB,
        formalites="Pas de visa pour les voyageurs de nationalité française pour un séjour de moins de 90 jours ; passeport valide demandé.",
        faq=[("Combien de temps dure un vol Lyon – Casablanca ?", "Environ 2 h 45 sans escale."),
             ("Peut-on aller en Afrique de l'Ouest via Casablanca depuis Lyon ?", "Oui : Royal Air Maroc relie Casablanca à de nombreuses capitales africaines, souvent à bon prix.")],
    ),
    ("LYS", "DSS"): dict(
        intro=("Lyon – Dakar permet à la diaspora sénégalaise de Rhône-Alpes de partir sans passer par Paris. "
               "L'offre directe reste limitée : surveillez les prix tôt pour les vacances."),
        direct="Transavia assure quelques vols directs par semaine (environ 5 h 15), selon les saisons.",
        escales="Avec escale : Paris (Air France), Casablanca (Royal Air Maroc), Lisbonne (TAP) ou Madrid (Iberia).",
        saison="La saison sèche, de novembre à juin, est la plus agréable. Juillet-août, les fêtes et la Tabaski sont les plus chers.",
        bagages="Transavia fait payer la valise en soute : ajoutez son prix avant de comparer avec un vol via Paris ou Casablanca.",
        formalites="Pas de visa pour les voyageurs de nationalité française pour moins de 90 jours. " + FJ_RECO + " " + PALU,
        faq=[("Y a-t-il des vols directs Lyon – Dakar ?", "Oui, Transavia propose quelques vols par semaine selon la saison."),
             ("Comment payer moins cher un Lyon – Dakar ?", "Comparez le direct avec un vol via Casablanca ou Paris, en comptant les valises, et activez les dates flexibles.")],
    ),
    ("LYS", "ALG"): dict(
        intro=("Lyon – Alger est très fréquentée par la diaspora algérienne de la région lyonnaise. Le vol dure environ 2 heures."),
        direct="Air Algérie et des compagnies françaises (dont Transavia, selon les saisons) proposent des vols directs.",
        escales="Le direct est la norme. Lyon dessert aussi Oran et Constantine : comparez selon votre destination finale.",
        saison="Juillet-août, le Ramadan, l'Aïd et les vacances scolaires sont les périodes les plus chères : réservez tôt pour l'été.",
        bagages=BAG_MAGHREB,
        formalites="Un visa est exigé pour les voyageurs de nationalité française (demande auprès des consulats d'Algérie).",
        faq=[("Combien de temps dure le vol Lyon – Alger ?", "Environ 2 heures sans escale."),
             ("Lyon dessert-elle d'autres villes d'Algérie ?", "Oui, notamment Oran et Constantine. Comparez selon la ville où vous allez.")],
    ),
    ("GVA", "DSS"): dict(
        natio="suisse ou française",
        intro=("Genève – Dakar concerne la diaspora sénégalaise de Suisse romande et de Haute-Savoie. "
               "Il n'y a pas toujours de vol direct : la comparaison des escales est essentielle."),
        direct="Les vols directs sont rares ou saisonniers sur cette ligne : vérifiez s'il en existe à vos dates.",
        escales=("La plupart des trajets passent par Paris (Air France), Lisbonne (TAP), Casablanca (Royal Air Maroc), Bruxelles (Brussels Airlines) "
                 "ou Madrid (Iberia). Pensez aussi à partir de Lyon, à 1 h 45 de route, qui a des vols directs."),
        saison="La saison sèche, de novembre à juin, est la plus agréable. Juillet-août, les fêtes et la Tabaski sont les plus chers.",
        bagages=BAG_AFRIQUE,
        formalites=SANS_VISA_UE + " " + FJ_RECO + " " + PALU,
        faq=[("Y a-t-il un vol direct Genève – Dakar ?", "Pas de façon régulière. Passez par Paris, Lisbonne, Casablanca ou Bruxelles, ou partez de Lyon."),
             ("Faut-il un visa pour le Sénégal depuis la Suisse ?", "Pas pour les ressortissants suisses et européens pour moins de 90 jours.")],
    ),
    ("GVA", "CMN"): dict(
        natio="suisse ou française",
        intro=("Genève – Casablanca relie la Suisse romande et le Genevois français au Maroc en un peu plus de 2 h 30."),
        direct="Royal Air Maroc et des compagnies à bas prix proposent des vols directs, plus nombreux en été.",
        escales="Le direct est la norme. Genève dessert aussi Marrakech et d'autres villes marocaines selon les saisons.",
        saison="Climat doux toute l'année. Prix les plus hauts en juillet-août, pendant les vacances scolaires et autour de l'Aïd.",
        bagages=BAG_MAGHREB,
        formalites=SANS_VISA_UE,
        faq=[("Combien de temps dure le vol Genève – Casablanca ?", "Environ 2 h 30 à 2 h 45 sans escale."),
             ("Faut-il un visa pour le Maroc depuis la Suisse ?", "Non pour les ressortissants suisses et européens pour un séjour de moins de 90 jours.")],
    ),
    ("CDG", "PTP"): dict(
        intro=("Paris – Pointe-à-Pitre relie la métropole à la Guadeloupe en 8 h 30 environ. L'aéroport Pôle Caraïbes est aux Abymes, "
               "tout près de Pointe-à-Pitre. Les vols partent surtout d'Orly."),
        direct="Air France, Air Caraïbes et Corsair proposent des vols directs, principalement depuis Orly.",
        escales="Le direct est la norme. Pensez à comparer avec Fort-de-France pour un voyage combiné entre les deux îles.",
        saison=("La saison sèche (le « carême »), de décembre à avril, est la plus agréable mais aussi la plus chère. "
                "De juin à novembre, c'est la saison des pluies et des cyclones. Les prix sont les plus hauts à Noël, en février et en juillet-août."),
        bagages="Les compagnies incluent souvent une valise en soute, mais certains tarifs économiques n'en ont pas : vérifiez avant de payer.",
        formalites="La Guadeloupe est un département français : la carte d'identité ou le passeport suffit pour les voyageurs français.",
        faq=[("Depuis quel aéroport partent les vols pour la Guadeloupe ?", "Surtout depuis Orly (Air France, Air Caraïbes, Corsair)."),
             ("Quand partir en Guadeloupe pas cher ?", "En mai-juin ou en septembre-octobre, hors vacances scolaires, en acceptant la saison des pluies.")],
    ),
    ("CDG", "FDF"): dict(
        intro=("Paris – Fort-de-France relie la métropole à la Martinique en 8 h 30 environ. L'aéroport Aimé-Césaire est au Lamentin, "
               "à une quinzaine de minutes de Fort-de-France."),
        direct="Air France, Air Caraïbes et Corsair proposent des vols directs, principalement depuis Orly.",
        escales="Le direct est la norme. Comparez avec Pointe-à-Pitre pour un voyage combiné Martinique-Guadeloupe.",
        saison=("Le carême, de décembre à avril, est la saison sèche et la plus demandée. Juin à novembre correspond à la saison des pluies et des cyclones. "
                "Les prix montent à Noël, au Carnaval (février-mars) et en juillet-août."),
        bagages="Les compagnies incluent souvent une valise en soute, mais certains tarifs économiques n'en ont pas : vérifiez avant de payer.",
        formalites="La Martinique est un département français : la carte d'identité ou le passeport suffit pour les voyageurs français.",
        faq=[("Combien de temps dure le vol Paris – Martinique ?", "Environ 8 h 30 à l'aller, un peu moins au retour."),
             ("Faut-il un passeport pour la Martinique ?", "Non pour les voyageurs français : la carte d'identité suffit.")],
    ),
    ("CDG", "ORN"): dict(
        intro=("Paris – Oran relie la capitale à la deuxième ville d'Algérie, porte d'entrée de l'Ouest algérien. "
               "L'aéroport Ahmed-Ben-Bella est à une dizaine de kilomètres du centre."),
        direct="Air Algérie et des compagnies françaises (dont Transavia) proposent des vols directs d'environ 2 h 15, depuis Orly et Roissy.",
        escales="Le direct est la norme. Comparez avec Alger ou Tlemcen selon votre destination finale.",
        saison="Juillet-août, le Ramadan, l'Aïd et les vacances scolaires concentrent les prix les plus élevés. Réservez tôt pour l'été.",
        bagages=BAG_MAGHREB,
        formalites="Un visa est exigé pour les voyageurs de nationalité française (demande auprès des consulats d'Algérie).",
        faq=[("Combien de temps dure le vol Paris – Oran ?", "Environ 2 h 15 sans escale."),
             ("Quelles compagnies desservent Oran depuis Paris ?", "En général Air Algérie et Transavia, avec d'autres compagnies selon la saison.")],
    ),
    ("CDG", "DJE"): dict(
        intro=("Paris – Djerba est une ligne à la fois touristique (plages, hôtels-clubs) et familiale pour la diaspora du sud tunisien. "
               "Le vol dure environ 2 h 45."),
        direct="Tunisair, Transavia, Nouvelair et d'autres compagnies proposent des vols directs, beaucoup plus nombreux en été.",
        escales="Le direct est la norme. En hiver, certains trajets passent par Tunis.",
        saison=("Djerba est agréable presque toute l'année ; la baignade est idéale de juin à octobre. "
                "Juillet-août et l'Aïd sont les périodes les plus chères."),
        bagages=BAG_MAGHREB,
        formalites="Pas de visa pour les voyageurs de nationalité française pour un séjour de moins de 90 jours ; passeport valide demandé.",
        faq=[("Quand partir à Djerba pas cher ?", "En mai, juin ou septembre-octobre : il fait beau et les prix sont plus doux qu'en juillet-août."),
             ("Combien de temps dure le vol Paris – Djerba ?", "Environ 2 h 45 sans escale.")],
    ),
    ("CDG", "BZV"): dict(
        intro=("Paris – Brazzaville relie la France à la capitale du Congo, face à Kinshasa de l'autre côté du fleuve. "
               "Les billets y sont parmi les plus chers d'Afrique centrale : la comparaison des escales est souvent payante."),
        direct="Air France relie Roissy à Brazzaville (environ 7 h à 8 h selon les vols).",
        escales=("Avec escale : Casablanca (Royal Air Maroc), Addis-Abeba (Ethiopian Airlines), Istanbul (Turkish Airlines) ou Lomé (ASKY). "
                 "Pointe-Noire, la capitale économique, a aussi ses propres vols."),
        saison="La saison sèche, de juin à septembre, est la plus fraîche. Il pleut beaucoup d'octobre à mai. Prix les plus hauts en juillet-août et pour les fêtes.",
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité française. " + FJ_OBLIG + " " + PALU,
        faq=[("Pourquoi les billets Paris – Brazzaville sont-ils chers ?", "La concurrence est faible sur le direct. Les vols via Casablanca, Addis-Abeba ou Istanbul sont parfois nettement moins chers."),
             ("Brazzaville ou Pointe-Noire ?", "Choisissez selon votre destination finale : les deux villes sont éloignées et ont chacune leurs vols.")],
    ),
    ("CDG", "NDJ"): dict(
        intro=("Paris – N'Djamena est utilisée par la diaspora tchadienne, les ONG et les voyageurs d'affaires. "
               "L'offre est limitée et les billets sont chers : réservez tôt et comparez les escales."),
        direct="Air France relie Roissy à N'Djamena, avec quelques vols par semaine.",
        escales="Avec escale : Addis-Abeba (Ethiopian Airlines), Istanbul (Turkish Airlines), Casablanca (Royal Air Maroc) ou Alger (Air Algérie).",
        saison=("De novembre à février, il fait plus frais et sec. Mars à juin est très chaud, et les pluies tombent de juillet à septembre."),
        bagages=BAG_AFRIQUE,
        formalites=("Un visa est exigé pour les voyageurs de nationalité française. " + FJ_RECO + " " + PALU +
                    " Consultez les conseils aux voyageurs de France Diplomatie : la situation sécuritaire évolue."),
        faq=[("Y a-t-il des vols directs Paris – N'Djamena ?", "Air France propose quelques vols par semaine. Sinon, passez par Addis-Abeba, Istanbul ou Casablanca."),
             ("Quand partir au Tchad ?", "De novembre à février, pendant la saison sèche et plus fraîche.")],
    ),
    ("CDG", "TNR"): dict(
        intro=("Paris – Antananarivo est un long-courrier de 10 h 45 environ vers la capitale de Madagascar, très utilisé par la diaspora malgache de France. "
               "L'aéroport d'Ivato est à une quinzaine de kilomètres du centre de « Tana »."),
        direct="Air France et Madagascar Airlines (ex-Air Madagascar) proposent des vols directs, depuis Roissy et parfois Orly.",
        escales=("Avec escale : La Réunion (Air Austral), Maurice (Air Mauritius), Addis-Abeba (Ethiopian Airlines), Nairobi (Kenya Airways) "
                 "ou Istanbul (Turkish Airlines). Un stop à La Réunion ou à Maurice permet de combiner deux séjours."),
        saison=("La saison sèche, d'avril à novembre, est la meilleure pour voyager. De janvier à mars, c'est la saison des pluies et des cyclones. "
                "Prix les plus hauts en juillet-août et pour les fêtes."),
        bagages="Les vols directs incluent souvent une ou deux valises selon le tarif. Sur les trajets avec escale, vérifiez la franchise de chaque compagnie.",
        formalites="Un visa est exigé pour les voyageurs de nationalité française (en ligne ou à l'arrivée, payant). " + PALU,
        faq=[("Combien de temps dure le vol Paris – Antananarivo ?", "Environ 10 h 45 sans escale."),
             ("Peut-on faire escale à La Réunion ou à Maurice ?", "Oui, avec Air Austral ou Air Mauritius : c'est parfois moins cher et permet de combiner deux destinations.")],
    ),
    ("CDG", "JED"): dict(
        intro=("Paris – Djeddah est la principale porte d'entrée pour la Omra, et pour le Hajj depuis la France. "
               "L'aéroport King Abdulaziz est à environ 1 h 15 de route de La Mecque, aussi reliée par le train à grande vitesse Haramain."),
        direct="Saudia assure des vols directs depuis Roissy (environ 5 h 45). Air France ne dessert pas Djeddah.",
        escales="Avec escale : Istanbul (Turkish Airlines), Le Caire (EgyptAir), Dubaï (Emirates), Doha (Qatar Airways) ou Abou Dabi (Etihad).",
        saison=("Les prix flambent pendant le Ramadan (surtout les dix derniers jours) et autour du Hajj. "
                "Pour une Omra moins chère, visez les mois hors Ramadan et hors vacances scolaires. L'été est extrêmement chaud."),
        bagages=("Saudia inclut en général des valises en soute. Au retour, l'eau de Zamzam est soumise à des règles particulières "
                 "(bidons de 5 litres, souvent hors franchise) : vérifiez auprès de la compagnie."),
        formalites=("Un visa est exigé : le visa touristique électronique permet la Omra hors saison du Hajj. "
                    "Le Hajj nécessite un visa spécifique, obtenu via une agence agréée. Le vaccin contre la méningite (ACYW) est exigé pour les pèlerins."),
        faq=[("Quel visa pour la Omra depuis la France ?", "Le visa touristique électronique saoudien permet d'effectuer la Omra hors période du Hajj. Vérifiez les conditions à jour avant de réserver."),
             ("Y a-t-il des vols directs Paris – Djeddah ?", "Oui, avec Saudia depuis Roissy, en 5 h 45 environ. Sinon, passez par Istanbul, Le Caire ou le Golfe.")],
    ),
})

# Lyon et Marseille : trajets qui ressortent déjà dans Google (Search Console, octobre 2026)
VIA_AFRIQUE = ("La plupart des trajets passent par Casablanca (Royal Air Maroc), Tunis (Tunisair), Alger (Air Algérie), "
               "Istanbul (Turkish Airlines) ou Paris (Air France). Comparez aussi avec un départ de Paris, qui a des vols directs.")
SANS_VISA_FR = "Pas de visa pour les voyageurs de nationalité française pour un séjour de moins de 90 jours ; passeport valide demandé."
VISA_DZ = "Un visa est exigé pour les voyageurs de nationalité française (demande auprès des consulats d'Algérie)."
SAISON_DZ = ("Juillet-août, le Ramadan, l'Aïd et les vacances scolaires concentrent les prix les plus élevés : pour l'été, réservez dès le début de l'année. "
             "Le printemps et l'automne sont les saisons les plus agréables et souvent les moins chères.")
SAISON_MA = "Climat doux une grande partie de l'année. Les prix montent en juillet-août, pendant les vacances scolaires et autour de l'Aïd."

TRAJETS.update({
    ("LYS", "TUN"): dict(
        intro="Lyon – Tunis est une ligne courte (environ 2 heures) très utilisée par la diaspora tunisienne de la région lyonnaise et par les vacanciers.",
        direct="Tunisair, Transavia et Nouvelair proposent des vols directs, plus nombreux en été.",
        escales="Le direct est la norme. Pour la plage, comparez avec Djerba et Monastir, aussi desservies depuis Lyon.",
        saison="Mai-juin et septembre-octobre sont idéaux : beau temps et prix plus doux. Juillet-août et l'Aïd sont les périodes les plus chères.",
        bagages=BAG_MAGHREB, formalites=SANS_VISA_FR,
        faq=[("Quelles compagnies volent entre Lyon et Tunis ?", "En général Tunisair, Transavia et Nouvelair, en vols directs d'environ 2 heures."),
             ("Quand partir à Tunis depuis Lyon pas cher ?", "Hors été et hors Aïd : mai-juin et septembre-octobre offrent souvent le meilleur rapport prix-météo.")],
    ),
    ("LYS", "DJE"): dict(
        intro="Lyon – Djerba relie la région lyonnaise à l'île tunisienne en 2 h 15 environ, pour les vacances comme pour les familles du sud tunisien.",
        direct="Tunisair, Transavia et Nouvelair proposent des vols directs, beaucoup plus nombreux en été.",
        escales="Le direct est la norme. En hiver, certains trajets passent par Tunis.",
        saison="La baignade est agréable de juin à octobre. Mai et septembre-octobre sont souvent moins chers que juillet-août.",
        bagages=BAG_MAGHREB, formalites=SANS_VISA_FR,
        faq=[("Combien de temps dure le vol Lyon – Djerba ?", "Environ 2 h 15 sans escale."),
             ("Y a-t-il des vols Lyon – Djerba toute l'année ?", "Les vols sont nombreux en été et plus rares en hiver : vérifiez vos dates, ou passez par Tunis.")],
    ),
    ("LYS", "AGA"): dict(
        intro="Lyon – Agadir est une ligne de soleil d'hiver et de vacances au bord de l'océan, à environ 3 h 15 de vol.",
        direct="Transavia et easyJet proposent quelques vols directs par semaine, selon les saisons.",
        escales="Hors des jours de vol direct, passez par Casablanca (Royal Air Maroc) ou par Marrakech, à environ 3 heures de route.",
        saison="Agadir est ensoleillée presque toute l'année : idéale pour fuir l'hiver. Les prix montent pendant les vacances scolaires, surtout à Noël et en février.",
        bagages=BAG_MAGHREB, formalites=SANS_VISA_FR,
        faq=[("Quelles compagnies volent en direct de Lyon à Agadir ?", "Transavia et easyJet, avec seulement quelques vols par semaine selon les saisons."),
             ("Agadir ou Marrakech depuis Lyon ?", "Marrakech a plus de vols directs depuis Lyon. Si les prix vers Agadir sont trop hauts, comparez avec Marrakech, à environ 3 heures de route.")],
    ),
    ("LYS", "RAK"): dict(
        intro="Lyon – Marrakech est l'une des lignes les plus fréquentées au départ de Lyon, pour un week-end comme pour des vacances.",
        direct="Transavia, easyJet, Royal Air Maroc et Volotea proposent des vols directs (environ 3 heures), avec des départs presque tous les jours.",
        escales="Le direct est la norme et souvent le moins cher.",
        saison="Le printemps et l'automne sont idéaux ; l'été est très chaud. Les prix montent pendant les vacances scolaires, surtout à la Toussaint, à Noël et à Pâques.",
        bagages=BAG_MAGHREB, formalites=SANS_VISA_FR,
        faq=[("Combien de compagnies volent entre Lyon et Marrakech ?", "En général quatre : Transavia, easyJet, Royal Air Maroc et Volotea. La concurrence fait souvent baisser les prix hors vacances."),
             ("Combien de temps dure un vol Lyon – Marrakech ?", "Environ 3 heures sans escale.")],
    ),
    ("LYS", "OUD"): dict(
        intro="Lyon – Oujda concerne surtout la diaspora de l'Oriental marocain. L'offre directe est très limitée et varie selon les saisons.",
        direct="Transavia a proposé des vols directs, parfois seulement quelques-uns par mois et pas toute l'année : vérifiez s'il en existe à vos dates.",
        escales="Sinon, passez par Casablanca (Royal Air Maroc), ou comparez avec Nador ou Fès, puis la route.",
        saison="L'été et les fêtes religieuses sont les périodes les plus demandées : réservez tôt, car les places directes sont rares.",
        bagages=BAG_MAGHREB, formalites=SANS_VISA_FR,
        faq=[("Y a-t-il des vols directs Lyon – Oujda ?", "Seulement par périodes, avec Transavia. Le reste de l'année, passez par Casablanca ou comparez avec Nador et Fès."),
             ("Quel aéroport près d'Oujda en plus ?", "Nador est à environ 2 heures de route et a souvent plus de vols depuis la France.")],
    ),
    ("LYS", "FEZ"): dict(
        intro="Lyon – Fès relie la région lyonnaise à la capitale spirituelle du Maroc. Les vols directs sont peu nombreux et saisonniers.",
        direct="Les vols directs sont rares ou saisonniers sur cette ligne : vérifiez s'il en existe à vos dates.",
        escales="Passez par Casablanca (Royal Air Maroc) ou comparez avec un vol direct vers Marrakech ou Casablanca, puis le train (le réseau ferré marocain relie bien ces villes).",
        saison="Le printemps et l'automne sont les plus agréables ; l'été est très chaud à Fès. " + SAISON_MA,
        bagages=BAG_MAGHREB, formalites=SANS_VISA_FR,
        faq=[("Comment aller de Lyon à Fès ?", "Avec un vol direct quand il y en a, sinon via Casablanca, ou un vol direct vers une autre ville marocaine puis le train."),
             ("Le train est-il pratique au Maroc ?", "Oui : Casablanca, Rabat, Fès et Marrakech sont reliées par des trains réguliers.")],
    ),
    ("LYS", "ORN"): dict(
        intro="Lyon – Oran relie la région lyonnaise à la deuxième ville d'Algérie, en 2 heures environ. La ligne est très chargée l'été.",
        direct="Transavia et Air Algérie proposent des vols directs, plus nombreux en été.",
        escales="Le direct est la norme. Comparez avec Alger, Tlemcen ou un départ de Marseille selon votre destination finale.",
        saison=SAISON_DZ, bagages=BAG_MAGHREB, formalites=VISA_DZ,
        faq=[("Quelles compagnies volent entre Lyon et Oran ?", "En général Transavia et Air Algérie, en vols directs d'environ 2 heures."),
             ("Quand réserver un Lyon – Oran pour l'été ?", "Dès janvier-février si possible : les vols de juillet-août se remplissent très vite.")],
    ),
    ("LYS", "CZL"): dict(
        intro="Lyon – Constantine relie la région lyonnaise à l'est algérien, en un peu plus de 2 heures.",
        direct="Transavia et Air Algérie proposent des vols directs, avec une offre qui varie selon les saisons.",
        escales="Si les prix sont trop hauts, comparez avec Alger ou Béjaïa, ou avec un départ de Marseille, très bien relié à Constantine.",
        saison=SAISON_DZ, bagages=BAG_MAGHREB, formalites=VISA_DZ,
        faq=[("Y a-t-il des vols directs Lyon – Constantine ?", "Oui, en général avec Transavia et Air Algérie, avec des fréquences qui varient selon les saisons."),
             ("Lyon ou Marseille pour Constantine ?", "Marseille a souvent plus de vols (Air Algérie, Volotea). Comparez les deux, en ajoutant le trajet jusqu'à l'aéroport.")],
    ),
    ("LYS", "IST"): dict(
        intro="Lyon – Istanbul est à la fois une destination de city-break et une escale très utilisée vers l'Afrique et l'Asie avec Turkish Airlines.",
        direct="Turkish Airlines et la compagnie à bas prix Pegasus proposent des vols directs, en 3 h 15 environ.",
        escales="Le direct est la norme. Vérifiez l'aéroport d'arrivée : IST côté européen, Sabiha-Gökçen (SAW) côté asiatique.",
        saison="Avril-juin et septembre-octobre sont idéaux. L'hiver est frais mais souvent bon marché.",
        bagages="Turkish Airlines inclut souvent une valise selon le tarif ; Pegasus la fait payer. Comparez le prix total.",
        formalites="Pas de visa pour les voyageurs de nationalité française pour un séjour touristique de moins de 90 jours.",
        faq=[("Quel aéroport à Istanbul depuis Lyon ?", "Turkish Airlines arrive en général à IST (côté européen), Pegasus à Sabiha-Gökçen (côté asiatique), plus loin du centre historique."),
             ("Istanbul est-elle une bonne escale vers l'Afrique depuis Lyon ?", "Oui : Turkish Airlines dessert de nombreuses villes africaines depuis Istanbul, souvent à bon prix.")],
    ),
    ("LYS", "DXB"): dict(
        intro="Lyon – Dubaï est desservie sans passer par Paris, ce qui en fait aussi une porte d'entrée vers l'Asie et l'océan Indien depuis la région lyonnaise.",
        direct="Emirates relie Lyon à Dubaï en vol direct (environ 6 h 30).",
        escales="Le direct est la norme. Un stop de quelques jours à Dubaï sur un billet vers l'Asie ne coûte parfois rien de plus.",
        saison="De novembre à mars, il fait chaud sans excès : c'est la haute saison. L'été est très chaud mais moins cher.",
        bagages="Emirates inclut généralement une valise en soute en classe économique, selon le tarif choisi.",
        formalites="Pas de visa préalable pour les voyageurs de nationalité française pour un séjour touristique court ; passeport valide au moins 6 mois.",
        faq=[("Y a-t-il un vol direct Lyon – Dubaï ?", "Oui, avec Emirates, en 6 h 30 environ."),
             ("Quand partir à Dubaï depuis Lyon ?", "De novembre à mars pour le climat ; fin octobre ou mars pour un bon compromis prix-météo.")],
    ),
    ("LYS", "ABJ"): dict(
        intro="Lyon – Abidjan concerne la diaspora ivoirienne de la région Rhône-Alpes. Il n'y a pas de vol direct : tout se joue sur le choix de l'escale.",
        direct="Pas de vol direct régulier entre Lyon et Abidjan.",
        escales=VIA_AFRIQUE,
        saison="Abidjan est chaude et humide toute l'année ; la grande saison des pluies dure de mai à juillet. Prix les plus hauts en juillet-août et pour les fêtes.",
        bagages=BAG_AFRIQUE + " Sur un trajet avec escale, vérifiez que la valise est enregistrée jusqu'à Abidjan.",
        formalites="Un visa est exigé pour les voyageurs de nationalité française (demande en ligne). " + FJ_OBLIG + " " + PALU,
        faq=[("Quelle escale choisir entre Lyon et Abidjan ?", "Casablanca, Tunis et Istanbul offrent souvent de bons prix ; Paris permet de prendre un vol direct pour la seconde partie."),
             ("Vaut-il mieux partir de Paris pour Abidjan ?", "Paris a des vols directs (Air France, Air Côte d'Ivoire, Corsair). Comparez en ajoutant le TGV Lyon–Paris.")],
    ),
    ("LYS", "BKO"): dict(
        intro="Lyon – Bamako concerne la diaspora malienne de la région lyonnaise. Il n'y a pas de vol direct et l'offre vers le Mali s'est réduite depuis 2023.",
        direct="Pas de vol direct entre Lyon et Bamako.",
        escales="Les trajets les plus courants passent par Casablanca (Royal Air Maroc), Alger (Air Algérie), Tunis (Tunisair) ou Istanbul (Turkish Airlines).",
        saison="La période la plus agréable va de novembre à février. Mars à mai est très chaud et la saison des pluies dure de juin à septembre.",
        bagages=BAG_AFRIQUE + " Vérifiez que la valise est enregistrée jusqu'à Bamako.",
        formalites=("Un visa est exigé pour les voyageurs de nationalité française. " + FJ_OBLIG + " " + PALU +
                    " Consultez les conseils aux voyageurs de France Diplomatie : la situation sécuritaire évolue."),
        faq=[("Quelle est la meilleure escale entre Lyon et Bamako ?", "Casablanca, Alger et Tunis offrent souvent les trajets les plus courts depuis Lyon. Comparez la durée totale."),
             ("Y a-t-il un vol direct Lyon – Bamako ?", "Non. Tous les trajets passent par une escale.")],
    ),
    ("MRS", "ORN"): dict(
        intro="Marseille – Oran est l'une des lignes les plus fréquentées entre la France et l'ouest algérien, en 1 h 30 environ.",
        direct="Air Algérie, Transavia et Volotea proposent des vols directs, avec plus de rotations en été.",
        escales="Le direct est la norme. Comparez avec Tlemcen ou Alger selon votre destination finale.",
        saison=SAISON_DZ, bagages=BAG_MAGHREB, formalites=VISA_DZ,
        faq=[("Quelles compagnies relient Marseille à Oran ?", "En général Air Algérie, Transavia et Volotea, en vols directs d'environ 1 h 30."),
             ("Combien de temps dure le vol Marseille – Oran ?", "Environ 1 h 30 sans escale.")],
    ),
    ("MRS", "CZL"): dict(
        intro="Marseille – Constantine relie Marseille à l'est algérien en 1 h 45 environ ; la ligne est très utilisée par la diaspora constantinoise.",
        direct="Air Algérie et Volotea proposent des vols directs ; Volotea a augmenté ses fréquences sur cette ligne en 2026.",
        escales="Le direct est la norme. Comparez avec Béjaïa ou Alger si les prix sont trop hauts.",
        saison=SAISON_DZ, bagages=BAG_MAGHREB, formalites=VISA_DZ,
        faq=[("Quelles compagnies volent entre Marseille et Constantine ?", "Air Algérie et Volotea, en vols directs."),
             ("Volotea inclut-elle les bagages ?", "Pas toujours : le tarif de base n'inclut souvent qu'un petit bagage. Ajoutez la valise avant de comparer avec Air Algérie.")],
    ),
    ("MRS", "CMN"): dict(
        intro="Marseille – Casablanca relie la Provence au cœur économique du Maroc en 2 h 30 environ ; Casablanca est aussi une escale pratique vers l'Afrique de l'Ouest.",
        direct="Royal Air Maroc assure des vols directs.",
        escales="Le direct est la norme. Pour Marrakech, Marseille a aussi plusieurs vols directs.",
        saison=SAISON_MA, bagages=BAG_MAGHREB, formalites=SANS_VISA_FR,
        faq=[("Quelle compagnie relie Marseille à Casablanca ?", "Royal Air Maroc, en vol direct d'environ 2 h 30."),
             ("Peut-on aller en Afrique de l'Ouest via Casablanca depuis Marseille ?", "Oui, Royal Air Maroc relie Casablanca à Dakar, Abidjan, Bamako et beaucoup d'autres villes africaines.")],
    ),
    ("MRS", "RAK"): dict(
        intro="Marseille – Marrakech est une ligne très demandée, en 2 h 45 environ, avec des départs presque tous les jours.",
        direct="Ryanair, Transavia et Royal Air Maroc proposent des vols directs.",
        escales="Le direct est la norme et souvent le moins cher.",
        saison="Le printemps et l'automne sont idéaux ; l'été est très chaud. Les prix montent pendant les vacances scolaires.",
        bagages="Ryanair et Transavia font payer la valise en soute (et parfois le bagage cabine) : comparez le prix total avec Royal Air Maroc.",
        formalites=SANS_VISA_FR,
        faq=[("Quelles compagnies volent entre Marseille et Marrakech ?", "En général Ryanair, Transavia et Royal Air Maroc, en vols directs."),
             ("Comment payer moins cher un Marseille – Marrakech ?", "Partez hors vacances scolaires, activez les dates flexibles et comparez le prix avec bagages.")],
    ),
    ("MRS", "DJE"): dict(
        intro="Marseille – Djerba est une ligne courte (moins de 2 heures) très utilisée l'été par les vacanciers et la diaspora du sud tunisien.",
        direct="Tunisair, Nouvelair et Transavia proposent des vols directs, surtout en été.",
        escales="Le direct est la norme en été ; en hiver, certains trajets passent par Tunis.",
        saison="La baignade est agréable de juin à octobre. Mai et septembre-octobre sont souvent moins chers que juillet-août.",
        bagages=BAG_MAGHREB, formalites=SANS_VISA_FR,
        faq=[("Combien de temps dure le vol Marseille – Djerba ?", "Un peu moins de 2 heures sans escale."),
             ("Quand partir à Djerba depuis Marseille pas cher ?", "En mai, juin ou septembre-octobre, hors vacances scolaires.")],
    ),
    ("MRS", "IST"): dict(
        intro="Marseille – Istanbul permet un city-break comme une escale vers l'Afrique, le Moyen-Orient et l'Asie avec Turkish Airlines.",
        direct="Turkish Airlines et Pegasus proposent des vols directs, en 3 heures environ.",
        escales="Le direct est la norme. Vérifiez l'aéroport d'arrivée : IST ou Sabiha-Gökçen (SAW).",
        saison="Avril-juin et septembre-octobre sont idéaux ; l'hiver est souvent bon marché.",
        bagages="Turkish Airlines inclut souvent une valise selon le tarif ; Pegasus la fait payer.",
        formalites="Pas de visa pour les voyageurs de nationalité française pour un séjour touristique de moins de 90 jours.",
        faq=[("Combien de temps dure le vol Marseille – Istanbul ?", "Environ 3 heures sans escale."),
             ("Quel aéroport choisir à Istanbul ?", "IST est plus pratique pour le centre historique ; Sabiha-Gökçen (SAW), côté asiatique, est plus éloigné.")],
    ),
    ("MRS", "BKO"): dict(
        intro="Marseille – Bamako concerne la diaspora malienne du sud de la France. Il n'y a pas de vol direct : la clé est de bien choisir l'escale.",
        direct="Pas de vol direct entre Marseille et Bamako.",
        escales="Les trajets les plus courants passent par Alger (Air Algérie), Casablanca (Royal Air Maroc), Tunis (Tunisair) ou Istanbul (Turkish Airlines). Depuis Marseille, ces escales sont proches.",
        saison="La période la plus agréable va de novembre à février. Mars à mai est très chaud et la saison des pluies dure de juin à septembre.",
        bagages=BAG_AFRIQUE + " Vérifiez que la valise est enregistrée jusqu'à Bamako.",
        formalites=("Un visa est exigé pour les voyageurs de nationalité française. " + FJ_OBLIG + " " + PALU +
                    " Consultez les conseils aux voyageurs de France Diplomatie : la situation sécuritaire évolue."),
        faq=[("Quelle escale entre Marseille et Bamako ?", "Alger, Casablanca et Tunis sont proches de Marseille et offrent souvent les trajets les plus courts."),
             ("Y a-t-il un vol direct Marseille – Bamako ?", "Non. Tous les trajets passent par une escale.")],
    ),
    ("MRS", "ABJ"): dict(
        intro="Marseille – Abidjan concerne la diaspora ivoirienne du sud de la France. Sans vol direct régulier, il faut comparer les escales.",
        direct="Pas de vol direct régulier entre Marseille et Abidjan : vérifiez s'il en existe à vos dates.",
        escales=VIA_AFRIQUE,
        saison="Abidjan est chaude et humide toute l'année ; la grande saison des pluies dure de mai à juillet. Prix les plus hauts en juillet-août et pour les fêtes.",
        bagages=BAG_AFRIQUE,
        formalites="Un visa est exigé pour les voyageurs de nationalité française (demande en ligne). " + FJ_OBLIG + " " + PALU,
        faq=[("Quelle escale entre Marseille et Abidjan ?", "Casablanca, Tunis et Istanbul sont souvent les moins chères ; Paris permet un vol direct pour la seconde partie."),
             ("Vaut-il mieux partir de Paris pour Abidjan ?", "Paris a des vols directs. Comparez le prix total, train ou vol Marseille–Paris compris.")],
    ),
})


def get(fr, to):
    return TRAJETS.get((fr, to))
