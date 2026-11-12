"""Pages pratiques ajoutées le 12 novembre 2026 (demande de Dobam) :
  /envoyer-argent-au-pays/      comment comparer les services de transfert (aucun tarif : ils changent chaque jour)
  /envoyer-colis-au-pays/       valises en plus, colis postal, fret aérien, groupage maritime
  /vol-plusieurs-etapes/        outil : un voyage en 2 à 4 étapes, une recherche par étape (site/etapes.js)
  /aller-a-l-aeroport/          comment rejoindre son aéroport de départ en Europe (+ une page par aéroport)
Règles : aucun prix, aucune durée précise, aucun horaire. Seulement les lignes et gares qui desservent l'aéroport et le lien
vers le site officiel, qui fait foi. Pas de lien d'affiliation sur les pages argent et colis. Relu en novembre 2026."""
import html

import build_i18n as B

E = html.escape
CHECKED = "novembre 2026"
# Adresses par langue (versions anglaise et italienne : scripts/diaspora_plus_i18n.py)
PATHS = {"argent": {"fr": "envoyer-argent-au-pays", "en": "en/send-money-home", "it": "it/inviare-soldi-a-casa"},
         "colis": {"fr": "envoyer-colis-au-pays", "en": "en/send-parcel-home", "it": "it/spedire-pacchi-a-casa"},
         "etapes": {"fr": "vol-plusieurs-etapes", "en": "en/multi-city-flights", "it": "it/viaggio-multi-tratta"},
         "hub": {"fr": "aller-a-l-aeroport", "en": "en/getting-to-the-airport", "it": "it/arrivare-in-aeroporto"}}
SLUG_EN = {"paris-cdg": "paris-cdg", "paris-orly": "paris-orly", "lyon": "lyon", "marseille": "marseille", "bruxelles": "brussels", "londres-heathrow": "london-heathrow", "milan-malpensa": "milan-malpensa",
           "rome-fiumicino": "rome-fiumicino", "geneve": "geneva", "madrid": "madrid", "barcelone": "barcelona", "francfort": "frankfurt", "lisbonne": "lisbon", "montreal": "montreal"}
SLUG_IT = {"paris-cdg": "parigi-cdg", "paris-orly": "parigi-orly", "lyon": "lione", "marseille": "marsiglia", "bruxelles": "bruxelles", "londres-heathrow": "londra-heathrow", "milan-malpensa": "milano-malpensa",
           "rome-fiumicino": "roma-fiumicino", "geneve": "ginevra", "madrid": "madrid", "barcelone": "barcellona", "francfort": "francoforte", "lisbonne": "lisbona", "montreal": "montreal"}
A_PATHS = lambda slug: {"fr": f"aller-aeroport-{slug}", "en": f"en/getting-to-{SLUG_EN[slug]}-airport", "it": f"it/arrivare-aeroporto-{SLUG_IT[slug]}"}
EXT = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
ul = lambda items: "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
faq_html = lambda faq: "".join(f"<details><summary>{E(q)}</summary><p>{E(r)}</p></details>" for q, r in faq)
PLUS = ('<section><h2>Pour aller plus loin</h2><ul>'
        '<li><a href="/envoyer-argent-au-pays/">Envoyer de l\'argent au pays : comment comparer</a></li>'
        '<li><a href="/envoyer-colis-au-pays/">Envoyer un colis ou des valises au pays</a></li>'
        '<li><a href="/vol-plusieurs-etapes/">Vol à plusieurs étapes</a></li>'
        '<li><a href="/aller-a-l-aeroport/">Rejoindre son aéroport de départ</a></li>'
        '<li><a href="/bagages-compagnies-afrique/">Bagages : la franchise de chaque compagnie</a></li>'
        '<li><a href="/guides/">Tous les guides</a></li></ul></section>')

# ---------------------------------------------------------------- argent
ARGENT_FAQ = [
    ("Quel est le service le moins cher pour envoyer de l'argent en Afrique ?",
     "Il n'y a pas de réponse fixe : cela dépend du pays, du montant, du mode de réception et du jour. Le bon réflexe est de comparer, pour le même montant envoyé, la somme que la personne recevra réellement. Les comparateurs publics cités sur cette page font ce calcul gratuitement."),
    ("Pourquoi regarder le taux de change et pas seulement les frais ?",
     "Parce qu'une partie du coût est souvent cachée dans le taux de change. Un service peut afficher « zéro frais » et appliquer un taux moins bon. Seul le montant reçu, dans la monnaie du pays, permet de comparer."),
    ("Mobile money, compte bancaire ou retrait en espèces ?",
     "Le mobile money (Orange Money, Wave, MTN MoMo…) est pratique quand le bénéficiaire n'a pas de compte bancaire et vit loin d'une agence. Le virement sur compte convient aux gros montants. Le retrait en espèces reste utile en dépannage, mais demande une pièce d'identité et un déplacement."),
    ("Comment éviter les arnaques ?",
     "N'envoyez de l'argent qu'à des personnes que vous connaissez. Méfiez-vous des urgences inventées, des gains promis et des demandes de garder le transfert secret. Passez toujours par le site ou l'application officielle du service, jamais par un lien reçu par message."),
]


def argent(site, ctx):
    hero = ('<p class="eyebrow">Guide · relu en ' + CHECKED + '</p><h1>Envoyer de l\'argent <span>au pays</span></h1>'
            '<p class="hero-lead">Wise, Remitly, WorldRemit, Sendwave, Taptap Send, Western Union, MoneyGram… Les tarifs changent chaque jour. Voici comment comparer en deux minutes et ne pas perdre d\'argent dans le taux de change.</p>')
    body = ('<section><h2>En bref</h2>' + ul([
        "Ne comparez pas les frais affichés : comparez <strong>le montant que la personne reçoit</strong> pour la même somme envoyée.",
        "Le coût se cache souvent dans le <strong>taux de change</strong>, même quand le service annonce « zéro frais ».",
        "Le mode de réception change le prix : <strong>mobile money</strong>, compte bancaire ou retrait en espèces.",
        "Utilisez un <strong>comparateur public et gratuit</strong> avant chaque envoi important.",
    ]) + '</section>'
        '<section><h2>La méthode en 4 étapes</h2><ol>'
        "<li>Décidez du montant à envoyer et de la façon dont la personne veut le recevoir (mobile money, compte, espèces).</li>"
        "<li>Ouvrez deux ou trois services et saisissez exactement le même montant et le même pays.</li>"
        "<li>Notez pour chacun le <strong>montant reçu dans la monnaie du pays</strong> et le délai annoncé.</li>"
        "<li>Choisissez celui qui donne le plus à l'arrivée dans un délai qui vous convient. Refaites la comparaison la fois suivante : le classement change.</li>"
        '</ol></section>'
        '<section><h2>Les comparateurs publics</h2><p>Ces sites comparent les services de transfert sans rien vendre :</p>' + ul([
            EXT("https://www.envoidargent.fr/", "envoidargent.fr") + " : comparateur soutenu par l'Agence française de développement, pour les envois depuis la France.",
            EXT("https://www.mandasoldiacasa.it/", "mandasoldiacasa.it") + " : comparateur italien des envois d'argent depuis l'Italie.",
            EXT("https://remittanceprices.worldbank.org/", "Remittance Prices Worldwide") + " : la base de la Banque mondiale, pays par pays (en anglais).",
        ]) + '</section>'
        '<section><h2>Les services les plus connus</h2><p>Liens vers les sites officiels, sans classement : Escale ne touche aucune commission sur ces services.</p>' + ul([
            EXT("https://wise.com/", "Wise") + " : virement vers un compte bancaire, et mobile money dans certains pays.",
            EXT("https://www.remitly.com/", "Remitly") + " : compte bancaire, mobile money ou retrait en espèces selon le pays.",
            EXT("https://www.worldremit.com/", "WorldRemit") + " : mobile money, compte bancaire, espèces, recharge téléphonique.",
            EXT("https://www.sendwave.com/", "Sendwave") + " : application mobile, surtout vers le mobile money.",
            EXT("https://www.taptapsend.com/", "Taptap Send") + " : application mobile, surtout vers le mobile money.",
            EXT("https://www.westernunion.com/", "Western Union") + " et " + EXT("https://www.moneygram.com/", "MoneyGram") + " : réseaux d'agences pour le retrait en espèces, et envoi en ligne.",
        ]) + '<p class="small">Tous les services ne desservent pas tous les pays ni tous les opérateurs de mobile money : vérifiez sur leur site avant de créer un compte.</p></section>'
        '<section><h2>Les pièges à éviter</h2>' + ul([
            "Envoyer en plusieurs petites fois : des frais fixes peuvent s'additionner. Regardez si un seul envoi revient moins cher.",
            "Payer par carte de crédit : certains services ou certaines banques ajoutent des frais. Le virement ou la carte de débit coûtent souvent moins.",
            "Se tromper d'un chiffre dans le numéro du bénéficiaire : un transfert vers le mauvais numéro est très difficile à récupérer. Relisez deux fois.",
            "Oublier les plafonds : chaque service limite les montants et peut demander une pièce d'identité ou un justificatif.",
        ]) + '</section>'
        '<section><h2>Et pour le billet d\'avion ?</h2><p>Un proche au pays peut parfois payer le billet lui-même : voyez <a href="/payer-billet-avion-mobile-money/">payer son billet avec Orange Money, Wave ou MTN MoMo</a> et <a href="/payer-billet-avion-plusieurs-fois/">payer en plusieurs fois</a>. Pour l\'argent sur place pendant le voyage : <a href="/guides/argent-en-voyage/">argent en voyage</a>.</p></section>'
        f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(ARGENT_FAQ)}</section>' + PLUS +
        '<p class="small">Escale ne vend pas de transfert d\'argent et n\'affiche aucun tarif ici, parce qu\'ils changent chaque jour. Les sites officiels font foi.</p>' + B.faq_ld(ARGENT_FAQ))
    return B.write(site, "envoyer-argent-au-pays", "fr", "Envoyer de l'argent au pays : comment comparer | Escale",
                   "Wise, Remitly, WorldRemit, Sendwave, Taptap Send, Western Union : la méthode pour comparer le montant vraiment reçu, les comparateurs publics gratuits et les pièges du taux de change.",
                   hero, body, "", PATHS["argent"], ctx)


# ---------------------------------------------------------------- colis
COLIS_FAQ = [
    ("Valise en plus ou colis : qu'est-ce qui revient le moins cher ?",
     "Pour une ou deux valises, le bagage supplémentaire acheté en ligne avant le départ est souvent le plus simple, puisque vous voyagez avec. Au-delà, ou si vous ne voyagez pas, demandez un devis de fret : le prix se calcule au kilo ou au volume et dépend du pays."),
    ("Combien de temps met un envoi par bateau ?",
     "Plusieurs semaines, auxquelles s'ajoute le passage en douane à l'arrivée. Le fret maritime convient aux affaires volumineuses et non urgentes. Demandez au transitaire un délai porte à porte, pas seulement la durée de la traversée."),
    ("Faut-il payer des droits de douane à l'arrivée ?",
     "Souvent oui : chaque pays a ses règles pour les marchandises neuves, l'électronique, les véhicules ou les quantités commerciales. Renseignez-vous auprès de la douane du pays d'arrivée ou du transitaire avant d'envoyer, pour ne pas découvrir les frais au retrait."),
    ("Puis-je confier un colis à un voyageur ?",
     "C'est une pratique courante, mais risquée des deux côtés : le voyageur est responsable de tout ce qu'il transporte devant la douane et la compagnie. Ne confiez et n'acceptez que des colis ouverts, dont le contenu est connu et autorisé."),
]


def colis(site, ctx):
    hero = ('<p class="eyebrow">Guide · relu en ' + CHECKED + '</p><h1>Envoyer un colis <span>ou des valises au pays</span></h1>'
            '<p class="hero-lead">Bagage supplémentaire, colis postal, fret aérien, groupage maritime : quelle solution choisir selon le poids, l\'urgence et le budget, et les règles à connaître avant d\'envoyer.</p>')
    body = ('<section><h2>En bref</h2>' + ul([
        "<strong>Vous voyagez</strong> et il s'agit d'une ou deux valises : le bagage supplémentaire, acheté en ligne avant le départ.",
        "<strong>Petit colis urgent</strong> (papiers, médicaments autorisés, téléphone) : la poste ou un transporteur express.",
        "<strong>Quelques cartons</strong> : le fret aérien, au kilo, en quelques jours.",
        "<strong>Gros volume non urgent</strong> (meubles, électroménager, fûts) : le groupage maritime, en plusieurs semaines.",
    ]) + '</section>'
        '<section><h2>1. La valise en plus dans l\'avion</h2>' + ul([
            "Achetez le bagage supplémentaire <strong>en ligne avant le départ</strong> : c'est en général moins cher qu'au comptoir de l'aéroport.",
            "Comparez le billet <strong>avec bagages inclus</strong> plutôt que le billet seul : une compagnie plus chère peut revenir moins cher une fois les valises comptées.",
            "Pesez tout à la maison : le kilo en trop se paie cher à l'enregistrement.",
            'La franchise et les règles de chaque compagnie : <a href="/bagages-compagnies-afrique/">bagages par compagnie</a> et le guide <a href="/guides/bagages-avion/">ne pas payer plus cher</a>.',
        ]) + '</section>'
        '<section><h2>2. Le colis postal ou express</h2>' + ul([
            "Pour un petit colis, la poste de votre pays (" + EXT("https://www.laposte.fr/", "La Poste") + " en France, " + EXT("https://www.poste.it/", "Poste Italiane") + " en Italie, " + EXT("https://www.bpost.be/", "bpost") + " en Belgique) ou un transporteur express.",
            "Faites le devis en ligne avec le poids et les dimensions réels : le prix dépend aussi du volume.",
            "Remplissez la <strong>déclaration en douane</strong> avec soin (contenu, valeur) et gardez le numéro de suivi.",
            "Demandez si la livraison se fait à domicile ou au bureau de poste : dans beaucoup de villes, le destinataire doit aller retirer le colis.",
        ]) + '</section>'
        '<section><h2>3. Le fret aérien</h2>' + ul([
            "Des transitaires spécialisés par pays collectent les cartons en Europe et les remettent à l'arrivée, souvent à leur agence.",
            "Le prix se calcule <strong>au kilo ou au volume</strong> : demandez toujours un devis écrit, avec ce qui est inclus (emballage, douane, livraison).",
            "Vérifiez que le transitaire a une adresse, un numéro d'entreprise et un reçu avec le détail du colis.",
        ]) + '</section>'
        '<section><h2>4. Le groupage maritime</h2>' + ul([
            "Pour les fûts, les cartons en nombre, le mobilier et l'électroménager : vous payez une part d'un conteneur partagé.",
            "Comptez <strong>plusieurs semaines</strong>, plus le passage en douane à l'arrivée.",
            "Faites un <strong>inventaire détaillé et photographié</strong> : il sert à la douane et en cas de perte ou de casse.",
            'Pour un déménagement complet, voyez le guide <a href="/retour-au-pays/">rentrer au pays pour de bon</a>.',
        ]) + '</section>'
        '<section><h2>Ce qu\'on n\'envoie pas</h2>' + ul([
            "Les batteries au lithium seules, les aérosols, les produits inflammables et les parfums en quantité sont limités ou interdits en avion.",
            "L'argent liquide, les bijoux de valeur et les papiers d'identité originaux ne voyagent pas dans un colis ordinaire.",
            "Les médicaments, la nourriture, les plantes et les produits animaux ont des règles propres à chaque pays.",
            "La règle de la douane française pour les envois hors Union européenne : " + EXT("https://www.douane.gouv.fr/", "douane.gouv.fr") + ". Pour l'arrivée, c'est la douane du pays de destination qui décide.",
        ]) + '</section>'
        f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(COLIS_FAQ)}</section>' + PLUS +
        '<p class="small">Escale ne transporte pas de colis et n\'affiche aucun tarif ici : demandez toujours un devis écrit. Les règles de douane changent : les sites officiels font foi.</p>' + B.faq_ld(COLIS_FAQ))
    return B.write(site, "envoyer-colis-au-pays", "fr", "Envoyer un colis ou des valises au pays : que choisir | Escale",
                   "Bagage supplémentaire, colis postal, fret aérien ou groupage maritime vers l'Afrique : quelle solution selon le poids et l'urgence, la douane, ce qu'on n'envoie pas et les questions à poser au transitaire.",
                   hero, body, "", PATHS["colis"], ctx)


# ---------------------------------------------------------------- vol à plusieurs étapes
ETAPES_FAQ = [
    ("Pourquoi une recherche par étape ?",
     "Parce que les billets séparés sont souvent la façon la moins chère de visiter deux pays dans le même voyage, et que chaque étape se compare alors comme un aller simple. L'outil prépare ces recherches pour vous, avec les bonnes dates."),
    ("Quel est le risque des billets séparés ?",
     "Les vols ne sont pas liés entre eux. Si le premier a du retard et que vous manquez le suivant, la deuxième compagnie ne vous doit rien. Gardez une marge large entre deux étapes, idéalement une nuit, et récupérez vos bagages à chaque étape."),
    ("Faut-il un visa pour chaque pays ?",
     "Oui, chaque pays où vous entrez applique ses propres règles, même pour une étape courte. Vérifiez avant de réserver avec l'outil visa d'Escale et sur les sites officiels."),
    ("Et un billet unique avec une longue escale ?",
     "Certaines compagnies permettent de rester un ou plusieurs jours dans leur ville de correspondance sur un seul billet. C'est plus sûr que deux billets séparés. Regardez les offres de la compagnie qui relie vos deux villes."),
]


def etapes(site, ctx):
    hero = ('<p class="eyebrow">Outil gratuit</p><h1>Vol à <span>plusieurs étapes</span></h1>'
            '<p class="hero-lead">Milan → Abidjan → Dakar → Milan ? Saisissez vos étapes : Escale prépare une recherche par étape, avec le prix le plus bas repéré ce mois-là quand il est connu.</p>')
    row = lambda i: (f'<div class="et-row" data-i="{i}"><div class="tool-grid"><label><span>Étape {i} : départ</span><input class="et-from" placeholder="Ville ou aéroport" autocomplete="off"></label>'
                     '<label><span>Arrivée</span><input class="et-to" placeholder="Ville ou aéroport" autocomplete="off"></label>'
                     '<label><span>Date</span><input class="et-date" type="date"></label></div></div>')
    body = ('<section><h2>Vos étapes</h2><form id="et-form" class="tool-form" novalidate>' + row(1) + row(2) +
            '<div id="et-more"></div><p class="et-actions"><button type="button" class="btn ghost" id="et-add">+ Ajouter une étape</button> '
            '<label class="et-pax"><span>Voyageurs</span> <select id="et-pax"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option></select></label></p>'
            '<p><button type="submit" class="btn">Préparer mes recherches</button></p><p id="et-msg" class="small" role="status"></p></form>'
            '<div id="et-out" aria-live="polite"></div></section>'
            '<section><h2>Comment ça marche</h2>' + ul([
                "Chaque étape est un <strong>aller simple</strong> : vous comparez et réservez les billets un par un.",
                "L'arrivée d'une étape devient le départ de la suivante, pour gagner du temps.",
                "Le prix affiché est le plus bas <strong>repéré récemment pour ce mois</strong>, par personne : il se confirme en ouvrant la recherche.",
            ]) + '</section>'
            '<section><h2>À savoir avant de réserver</h2>' + ul([
                "<strong>Billets séparés = correspondance non protégée.</strong> Si un vol a du retard, le suivant n'attend pas et n'est pas remboursé. Gardez une marge large, idéalement une nuit.",
                "Vous devez <strong>récupérer et réenregistrer vos bagages</strong> à chaque étape.",
                'Chaque pays a ses règles d\'entrée : vérifiez avec l\'<a href="/visa/">outil visa</a>.',
                'Comparez toujours avec un aller-retour simple : il est parfois moins cher de faire deux allers-retours depuis la même ville. <a href="/">Comparer un aller-retour</a>.',
            ]) + '</section>'
            f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(ETAPES_FAQ)}</section>' + PLUS + B.faq_ld(ETAPES_FAQ) +
            '<script src="/ac-mini.js" defer></script><script src="/etapes.js" defer></script>')
    return B.write(site, "vol-plusieurs-etapes", "fr", "Vol à plusieurs étapes : préparer un voyage multi-villes | Escale",
                   "Outil gratuit pour un voyage en 2 à 4 étapes (par exemple Milan, Abidjan, Dakar, Milan) : une recherche par étape, le prix le plus bas repéré ce mois-là et les précautions des billets séparés.",
                   hero, body, "", PATHS["etapes"], ctx)


# ---------------------------------------------------------------- rejoindre l'aéroport de départ
# slug, nom complet, ville, code, site officiel, [transports], remarque
AERO = [
    ("paris-cdg", "Paris-Charles de Gaulle", "Paris", "CDG", "https://www.parisaeroport.fr/", [
        "<strong>RER B</strong> depuis Gare du Nord, Châtelet-Les Halles, Saint-Michel ou Denfert-Rochereau. Deux gares : « Aéroport Charles de Gaulle 1 » pour les terminaux 1 et 3, « Aéroport Charles de Gaulle 2 TGV » pour le terminal 2.",
        "<strong>Roissybus</strong> depuis le quartier de l'Opéra.",
        "<strong>TGV</strong> : la gare du terminal 2 reçoit des trains directs de nombreuses villes de France et de Bruxelles, sans passer par Paris.",
        "<strong>CDGVAL</strong> : la navette automatique gratuite relie les terminaux, les gares et les parkings.",
    ], "Vérifiez votre terminal sur le billet : l'aéroport est très étendu et le terminal 2 compte plusieurs halls."),
    ("paris-orly", "Paris-Orly", "Paris", "ORY", "https://www.parisaeroport.fr/", [
        "<strong>Métro ligne 14</strong> jusqu'à la station « Aéroport d'Orly », depuis Châtelet, Gare de Lyon ou Saint-Lazare.",
        "<strong>Tramway T7</strong> depuis Villejuif-Louis Aragon (métro ligne 7).",
        "<strong>Orlyval</strong> depuis la gare d'Antony (RER B).",
    ], "Orly compte quatre secteurs (Orly 1, 2, 3 et 4) reliés à pied : regardez le vôtre sur le billet."),
    ("lyon", "Lyon-Saint-Exupéry", "Lyon", "LYS", "https://www.lyonaeroports.com/", [
        "<strong>Rhônexpress</strong> : le tramway express depuis la gare de Lyon Part-Dieu.",
        "<strong>TGV</strong> : la gare Lyon-Saint-Exupéry TGV est à côté des terminaux.",
        "Des <strong>cars</strong> relient l'aéroport à plusieurs villes de la région (Grenoble, Chambéry, Annecy…).",
    ], ""),
    ("marseille", "Marseille-Provence", "Marseille", "MRS", "https://www.marseille-airport.com/", [
        "<strong>Navette en car</strong> depuis la gare Marseille Saint-Charles.",
        "<strong>Train</strong> jusqu'à la gare « Vitrolles Aéroport Marseille Provence », puis navette en bus jusqu'aux terminaux.",
        "Des cars relient aussi l'aéroport à Aix-en-Provence.",
    ], "L'aéroport a deux terminaux, dont un pour les compagnies à bas prix : vérifiez le vôtre."),
    ("bruxelles", "Bruxelles-Zaventem", "Bruxelles", "BRU", "https://www.brusselsairport.be/", [
        "<strong>Train</strong> : la gare « Brussels Airport-Zaventem » est sous le terminal. Trains directs depuis Bruxelles-Midi, Bruxelles-Central et Bruxelles-Nord, et depuis plusieurs villes belges (Anvers, Gand, Louvain, Liège…).",
        "<strong>Bus</strong> depuis Bruxelles et les communes voisines, au niveau 0 du terminal.",
    ], "Ne confondez pas avec Bruxelles-Sud Charleroi (CRL), un autre aéroport à environ une heure de route de Bruxelles."),
    ("londres-heathrow", "Londres-Heathrow", "Londres", "LHR", "https://www.heathrow.com/", [
        "<strong>Elizabeth line</strong> depuis le centre de Londres (Paddington, Bond Street, Liverpool Street…).",
        "<strong>Métro Piccadilly line</strong> : le moins cher, plus lent.",
        "<strong>Heathrow Express</strong> : train sans arrêt depuis la gare de Paddington.",
        "<strong>Cars</strong> depuis de nombreuses villes du Royaume-Uni jusqu'à la gare routière centrale.",
    ], "Heathrow a quatre terminaux en service (2, 3, 4 et 5), avec des gares différentes : vérifiez le vôtre avant de monter dans le train."),
    ("milan-malpensa", "Milan-Malpensa", "Milan", "MXP", "https://www.milanomalpensa-airport.com/", [
        "<strong>Malpensa Express</strong> : train depuis Milano Centrale, Milano Porta Garibaldi et Milano Cadorna, jusqu'aux terminaux 1 et 2.",
        "<strong>Cars</strong> depuis la gare Milano Centrale, et depuis d'autres villes du nord de l'Italie.",
    ], "Milan a trois aéroports : Malpensa (MXP), Linate (LIN) et Bergame-Orio al Serio (BGY). Vérifiez le code sur votre billet."),
    ("rome-fiumicino", "Rome-Fiumicino", "Rome", "FCO", "https://www.adr.it/", [
        "<strong>Leonardo Express</strong> : train sans arrêt depuis la gare Roma Termini.",
        "<strong>Train régional FL1</strong> depuis Roma Tiburtina, Roma Ostiense et Roma Trastevere (il ne passe pas par Termini).",
        "<strong>Cars</strong> depuis Termini et d'autres points de la ville.",
    ], "Ne confondez pas avec Rome-Ciampino (CIA), l'autre aéroport de Rome."),
    ("geneve", "Genève", "Genève", "GVA", "https://www.gva.ch/", [
        "<strong>Train</strong> : la gare « Genève-Aéroport » est reliée au terminal. Tous les trains depuis Genève-Cornavin y vont en quelques minutes, et des trains directs arrivent de Lausanne, Berne ou Zurich.",
        "<strong>Bus</strong> des transports publics genevois depuis le centre-ville.",
    ], "L'aéroport a aussi un secteur français, accessible depuis la France sans passer la douane suisse."),
    ("madrid", "Madrid-Barajas", "Madrid", "MAD", "https://www.aena.es/", [
        "<strong>Métro ligne 8</strong> depuis Nuevos Ministerios : une station pour les terminaux 1-2-3, une autre pour le terminal 4.",
        "<strong>Train de banlieue (Cercanías)</strong> lignes C1 et C10 jusqu'au terminal 4, depuis Atocha et Chamartín.",
        "<strong>Bus Exprés Aeropuerto</strong> depuis Atocha et Cibeles, jour et nuit.",
    ], "Le terminal 4 est éloigné des trois autres : une navette gratuite les relie, comptez du temps."),
    ("barcelone", "Barcelone-El Prat", "Barcelone", "BCN", "https://www.aena.es/", [
        "<strong>Aerobús</strong> depuis la Plaça de Catalunya, vers le terminal 1 ou le terminal 2.",
        "<strong>Métro ligne L9 Sud</strong> jusqu'aux deux terminaux.",
        "<strong>Train R2 Nord</strong> depuis Barcelona Sants et Passeig de Gràcia jusqu'au terminal 2.",
    ], "Les deux terminaux sont éloignés l'un de l'autre : une navette gratuite les relie."),
    ("francfort", "Francfort", "Francfort", "FRA", "https://www.frankfurt-airport.com/", [
        "<strong>S-Bahn S8 et S9</strong> depuis la gare centrale (Hauptbahnhof) jusqu'à la gare régionale de l'aéroport, au terminal 1.",
        "<strong>Trains longue distance (ICE)</strong> : la gare « Frankfurt Flughafen Fernbahnhof » reçoit des trains directs de nombreuses villes d'Allemagne.",
    ], "Ne confondez pas avec Francfort-Hahn (HHN), un aéroport très éloigné de la ville."),
    ("lisbonne", "Lisbonne", "Lisbonne", "LIS", "https://www.ana.pt/", [
        "<strong>Métro ligne rouge (Vermelha)</strong> jusqu'à la station « Aeroporto », au terminal 1.",
        "<strong>Bus</strong> de la ville depuis le centre.",
    ], "Le terminal 2, utilisé par des compagnies à bas prix pour les départs, se rejoint par une navette gratuite depuis le terminal 1."),
    ("montreal", "Montréal-Trudeau", "Montréal", "YUL", "https://www.admtl.com/", [
        "<strong>Bus 747</strong> de la STM depuis le centre-ville (station Berri-UQAM, avec un arrêt à Lionel-Groulx), jour et nuit.",
        "<strong>Taxi</strong> à tarif fixe entre l'aéroport et le centre-ville.",
    ], ""),
]
A_PATH = lambda slug: f"aller-aeroport-{slug}"
A_FAQ = lambda a: [
    (f"Combien de temps avant le vol faut-il arriver à {a[1]} ?",
     "Pour un vol long-courrier vers l'Afrique, les compagnies recommandent souvent d'arriver environ trois heures avant le départ. L'heure limite d'enregistrement de votre compagnie est indiquée sur le billet : c'est elle qui compte."),
    ("Train ou voiture ?",
     "Le train ou le métro évitent les bouchons et le prix du parking pour un séjour long. La voiture reste pratique en famille avec beaucoup de valises ou pour un vol très tôt : dans ce cas, réservez le parking officiel en ligne à l'avance."),
    ("Où trouver les horaires et les tarifs ?",
     "Sur le site officiel de l'aéroport et sur celui du transporteur. Escale n'affiche ni horaires ni tarifs, parce qu'ils changent : vérifiez la veille du départ, surtout en cas de grève ou de travaux."),
]


def aeroports(site, ctx):
    urls = []
    for a in AERO:
        slug, nom, ville, code, off, lignes, note = a
        autres = "".join(f'<li><a href="/{A_PATH(x[0])}/">{E(x[1])} ({x[3]})</a></li>' for x in AERO if x[0] != slug)
        faq = A_FAQ(a)
        hero = (f'<p class="eyebrow">Aéroport de départ · relu en {CHECKED}</p><h1>Aller à l\'aéroport <span>{E(nom)} ({code})</span></h1>'
                f'<p class="hero-lead">Train, métro, bus, voiture : comment rejoindre {E(nom)} avant votre vol, et ce qu\'il faut vérifier la veille.</p>')
        body = ('<section><h2>En transports en commun</h2>' + ul(lignes) + (f"<p>{note}</p>" if note else "") +
                f'<p>Horaires, tarifs et travaux : {EXT(off, "site officiel de l’aéroport")}.</p></section>'
                '<section><h2>En voiture</h2>' + ul([
                    "Les <strong>parkings officiels</strong> se réservent en ligne sur le site de l'aéroport : c'est en général moins cher qu'en arrivant sans réservation.",
                    "Pour déposer quelqu'un, suivez les panneaux « dépose-minute » : l'arrêt y est limité à quelques minutes.",
                    "Prévoyez une marge pour les bouchons aux heures de pointe et pour la navette entre le parking et le terminal.",
                ]) + '</section>'
                '<section><h2>La veille du départ</h2>' + ul([
                    "Vérifiez le <strong>terminal</strong> et l'heure limite d'enregistrement sur votre billet.",
                    "Regardez s'il y a une grève ou des travaux sur votre ligne, et prévoyez un plan B.",
                    "Pesez vos valises : <a href=\"/bagages-compagnies-afrique/\">franchise de chaque compagnie</a>.",
                    'Passez en revue le <a href="/controle-avant-vol/">contrôle avant le vol</a> : passeport, visa, documents.',
                ]) + '</section>'
                f'<section><h2>Comparer les vols au départ de {E(ville)}</h2><p><a class="btn" href="/?type=vols&amp;from={code}">Voir les vols depuis {E(ville)}</a></p></section>'
                f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(faq)}</section>'
                f'<section><h2>Autres aéroports de départ</h2><ul class="links">{autres}</ul></section>' + PLUS +
                '<p class="small">Ces repères sont généraux. Les lignes, les arrêts et les terminaux peuvent changer : le site officiel de l\'aéroport fait foi.</p>' + B.faq_ld(faq))
        urls.append(B.write(site, A_PATH(slug), "fr", f"Aller à l'aéroport {nom} ({code}) : train, métro, bus | Escale",
                            f"Comment rejoindre l'aéroport {nom} ({code}) avant un vol : les trains, métros et bus qui le desservent, le parking, quoi vérifier la veille, avec le lien vers le site officiel.",
                            hero, body, "", A_PATHS(slug), ctx))
    liste = "".join(f'<li><a href="/{A_PATH(a[0])}/">{E(a[1])} ({a[3]})</a></li>' for a in AERO)
    faq = A_FAQ(("", "l'aéroport"))
    hero = ('<p class="eyebrow">Guides · relus en ' + CHECKED + '</p><h1>Rejoindre son <span>aéroport de départ</span></h1>'
            '<p class="hero-lead">Train, métro, bus ou voiture : comment aller à l\'aéroport avant un vol vers l\'Afrique, depuis les grandes villes d\'Europe et Montréal.</p>')
    body = (f'<section><h2>Choisissez votre aéroport</h2><ul class="links">{liste}</ul></section>'
            '<section><h2>Les bons réflexes</h2>' + ul([
                "Vérifiez le <strong>code de l'aéroport</strong> sur le billet : plusieurs villes en ont deux ou trois (Paris, Milan, Rome, Londres, Bruxelles).",
                "Pour un vol long-courrier, les compagnies recommandent souvent d'arriver environ <strong>trois heures avant</strong> : l'heure limite d'enregistrement est sur le billet.",
                "Regardez la veille s'il y a une grève ou des travaux sur votre ligne.",
                'À l\'arrivée en Afrique : <a href="/arriver-aeroport-abidjan/">Abidjan</a>, <a href="/arriver-aeroport-dakar/">Dakar</a>, <a href="/arriver-aeroport-bamako/">Bamako</a>, <a href="/arriver-aeroport-casablanca/">Casablanca</a> et les autres villes dans les <a href="/guides/">guides</a>.',
            ]) + '</section>'
            f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(faq)}</section>' + PLUS + B.faq_ld(faq))
    urls.append(B.write(site, "aller-a-l-aeroport", "fr", "Rejoindre son aéroport de départ : train, métro, bus | Escale",
                        "Comment aller à l'aéroport avant un vol : Paris CDG et Orly, Lyon, Marseille, Bruxelles, Londres Heathrow, Milan Malpensa, Rome Fiumicino, Genève, Madrid, Barcelone, Francfort, Lisbonne, Montréal.",
                        hero, body, "", PATHS["hub"], ctx))
    return urls


def build(site, ctx):
    return [argent(site, ctx), colis(site, ctx), etapes(site, ctx)] + aeroports(site, ctx)


LIENS = [("envoyer-argent-au-pays", "Envoyer de l'argent au pays : comment comparer"), ("envoyer-colis-au-pays", "Envoyer un colis ou des valises au pays"),
         ("vol-plusieurs-etapes", "Vol à plusieurs étapes"), ("aller-a-l-aeroport", "Rejoindre son aéroport de départ")]
