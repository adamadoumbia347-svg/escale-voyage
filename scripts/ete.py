"""Pages « Vacances d'été 2027 au pays » (français) : une page par destination + une page d'ensemble.

Elles visent les recherches « vol Dakar été 2027 », « billet Paris Bamako juillet 2027 »… que les familles de la diaspora
font dès janvier. Chaque page : prix repérés par période (départ juin, juillet ou août) et par aéroport de départ
(chargés par site/ete.js depuis /api/prix, qui cherche au mois), climat de l'été, conseils propres à la destination,
alerte prix et services partenaires.
À mettre à jour chaque année : ANNEE, PERIODES, les dates citées dans les textes.
Repères vérifiés en octobre 2026 : vacances scolaires d'été 2027 du samedi 3 juillet au jeudi 2 septembre (zones A, B, C) ;
Grand Magal de Touba (18 safar 1449) estimé vers le 22-23 juillet 2027, selon l'observation de la lune.
"""
import json

ANNEE = 2027
SLUG = "vols-ete-2027"

# Périodes comparées : /api/prix cherche le prix le plus bas pour un mois de départ et un mois de retour
# (mois de départ, mois de retour, dates proposées par défaut pour la recherche, libellé, remarque)
PERIODES = [
    ("2027-06", "2027-07", "2027-06-26", "2027-07-24", "Départ en juin, retour en juillet", "Partir avant les vacances scolaires : souvent la période la moins chère."),
    ("2027-07", "2027-07", "2027-07-03", "2027-07-31", "Départ et retour en juillet", "Le plus demandé : départs dès le 3 juillet."),
    ("2027-07", "2027-08", "2027-07-10", "2027-08-07", "Départ en juillet, retour en août", "Le grand séjour de l'été."),
    ("2027-08", "2027-08", "2027-08-07", "2027-08-28", "Départ et retour en août", "Les prix baissent souvent après le 15 août."),
]
# Aéroports de départ comparés (départ en juillet, retour en août)
DEPARTS = [("CDG", "Paris"), ("LYS", "Lyon"), ("MRS", "Marseille"), ("BRU", "Bruxelles"), ("GVA", "Genève")]

ESCALES_OUEST = "Casablanca, Alger, Tunis, Istanbul ou Addis-Abeba"

# code, ville, nom anglais (liens partenaires), pays, climat, conseils propres à l'été, question/réponse
DEST = [
    dict(code="DSS", ville="Dakar", en="Dakar", pays="Sénégal", slug="dakar",
         climat=["L'été correspond au début de l'hivernage, la saison des pluies, qui dure de juillet à octobre. Les averses sont surtout fortes en août et en septembre, souvent sous forme d'orages courts.",
                 "Il fait chaud et humide : 27 à 31 °C en journée, et l'océan est chaud pour la baignade."],
         conseils=["Le Grand Magal de Touba devrait tomber vers le 22-23 juillet 2027 (date confirmée par les autorités religieuses) : les vols vers Dakar des jours précédents sont très demandés.",
                   "L'aéroport Blaise-Diagne (AIBD) est à Diass, à environ 45 km du centre de Dakar : prévoyez le transfert dans votre budget, surtout pour une arrivée de nuit.",
                   "Avec des valises de cadeaux, comparez les tarifs qui incluent deux bagages en soute : ils reviennent souvent moins cher qu'un tarif de base avec bagages en supplément."],
         faq=("Fait-il beau à Dakar en juillet et en août ?", "Il fait chaud (27 à 31 °C) et c'est le début de la saison des pluies : les averses, plutôt courtes, sont plus fréquentes en août et en septembre qu'en juillet.")),
    dict(code="BKO", ville="Bamako", en="Bamako", pays="Mali", slug="bamako",
         climat=["La saison des pluies va de juin à septembre, avec les plus fortes pluies en juillet et en août.",
                 "Les températures restent élevées (25 à 32 °C) mais plus supportables qu'en avril-mai, la période la plus chaude."],
         conseils=[f"La plupart des trajets vers Bamako passent par une escale ({ESCALES_OUEST}…) : comparez le temps de correspondance autant que le prix.",
                   "Avant de réserver, consultez la fiche Mali des « Conseils aux voyageurs » du ministère des Affaires étrangères, régulièrement mise à jour.",
                   "Pendant l'hivernage, certaines routes de l'intérieur deviennent difficiles : gardez de la marge si vous continuez votre voyage par la route."],
         faq=("Quand partir à Bamako l'été pour payer moins cher ?", "En général, les départs de fin juin (avant les vacances scolaires) et ceux de la deuxième quinzaine d'août sont moins chers que les départs du début de juillet.")),
    dict(code="ABJ", ville="Abidjan", en="Abidjan", pays="Côte d'Ivoire", slug="abidjan",
         climat=["La grande saison des pluies d'Abidjan culmine en juin et se termine en juillet. Août et septembre forment la « petite saison sèche » : moins de pluie et un ciel souvent gris.",
                 "C'est la période la plus fraîche de l'année : 24 à 28 °C."],
         conseils=["Août est souvent le meilleur moment de l'été pour Abidjan : moins de pluie, et la fête de l'Indépendance le 7 août.",
                   "L'aéroport Félix-Houphouët-Boigny est à Port-Bouët, au sud de la ville : selon l'heure d'arrivée, comptez de 30 minutes à plus d'une heure jusqu'au Plateau ou à Cocody.",
                   "Le visa pour la Côte d'Ivoire se demande en ligne avant le départ (e-visa), et la carte de vaccination contre la fièvre jaune est obligatoire."],
         faq=("Quel est le meilleur mois pour aller à Abidjan l'été ?", "Août : c'est le début de la petite saison sèche, avec moins de pluie qu'en juin et juillet et des températures douces (24 à 28 °C).")),
    dict(code="CKY", ville="Conakry", en="Conakry", pays="Guinée", slug="conakry",
         climat=["Conakry est l'une des capitales les plus pluvieuses d'Afrique : juillet et août sont les mois les plus arrosés, avec des pluies presque quotidiennes.",
                 "Il fait 24 à 28 °C, avec une humidité très forte."],
         conseils=["Les pluies de juillet-août ralentissent fortement la circulation : prévoyez large pour rejoindre l'aéroport de Gbessia au retour.",
                   f"Comparez les vols directs et les vols avec escale ({ESCALES_OUEST}, Dakar…) : l'écart de prix l'été est souvent important.",
                   "Le visa pour la Guinée se demande en ligne avant le départ, et la vaccination contre la fièvre jaune est obligatoire."],
         faq=("Pleut-il beaucoup à Conakry en été ?", "Oui : juillet et août sont les mois les plus pluvieux de l'année à Conakry, avec des pluies presque tous les jours.")),
    dict(code="DLA", ville="Douala", en="Douala", pays="Cameroun", slug="douala",
         climat=["Douala est très pluvieuse de juillet à septembre : c'est le cœur de la saison des pluies sur la côte camerounaise.",
                 "Il fait 24 à 28 °C, avec une forte humidité."],
         conseils=["Pour l'Ouest ou le Centre du Cameroun, comparez aussi les vols vers Yaoundé-Nsimalen : le prix peut être très différent.",
                   "Le visa pour le Cameroun se demande en ligne avant le départ, et la vaccination contre la fièvre jaune est obligatoire.",
                   "Les vols directs depuis Paris partent vite en juillet : réservez tôt ou comparez les escales (Bruxelles, Casablanca, Istanbul, Addis-Abeba…)."],
         faq=("Vaut-il mieux arriver à Douala ou à Yaoundé ?", "Cela dépend de votre destination finale. Comparez les deux : pour un même week-end de juillet, l'écart de prix entre Douala et Yaoundé peut dépasser le coût du trajet en car entre les deux villes.")),
    dict(code="NSI", ville="Yaoundé", en="Yaounde", pays="Cameroun", slug="yaounde",
         climat=["À 750 m d'altitude, Yaoundé est plus fraîche que Douala : 20 à 27 °C en été.",
                 "Juillet et août correspondent à la petite saison sèche : il pleut nettement moins qu'au printemps et à l'automne."],
         conseils=["L'aéroport de Nsimalen est à environ 25 km du centre : prévoyez le transfert, surtout pour une arrivée de nuit.",
                   "Comparez avec les vols vers Douala, souvent plus nombreux, puis le trajet par la route (environ 4 heures).",
                   "Le visa pour le Cameroun se demande en ligne avant le départ, et la vaccination contre la fièvre jaune est obligatoire."],
         faq=("Quel temps fait-il à Yaoundé en juillet ?", "Plutôt frais et sec pour la région : 20 à 27 °C, et beaucoup moins de pluie qu'en avril-mai ou en septembre-octobre.")),
    dict(code="FIH", ville="Kinshasa", en="Kinshasa", pays="RD Congo", slug="kinshasa",
         climat=["L'été est la saison sèche à Kinshasa (de juin à septembre) : pas de pluie, un ciel souvent voilé.",
                 "C'est aussi la période la plus fraîche : 21 à 29 °C, avec des soirées agréables."],
         conseils=["Juillet et août sont la meilleure période pour le climat, et donc la plus demandée : réservez tôt.",
                   "Le visa pour la RD Congo s'obtient avant le départ, et la vaccination contre la fièvre jaune est obligatoire.",
                   "Comparez les vols directs et les vols avec escale (Bruxelles, Addis-Abeba, Istanbul, Casablanca…)."],
         faq=("Juillet est-il un bon mois pour Kinshasa ?", "Oui pour le climat : c'est la saison sèche et la plus fraîche de l'année. C'est aussi une période très demandée, donc plus chère : réservez plusieurs mois à l'avance.")),
    dict(code="LFW", ville="Lomé", en="Lome", pays="Togo", slug="lome",
         climat=["Sur la côte du golfe de Guinée, la petite saison sèche va de mi-juillet à mi-septembre : août est souvent le mois le moins pluvieux de l'été.",
                 "Il fait 24 à 28 °C. La mer est agitée : la baignade est dangereuse sur une grande partie des plages, à cause de la barre et des courants."],
         conseils=["Lomé et Cotonou ne sont qu'à environ 150 km l'une de l'autre : comparez les vols vers les deux villes.",
                   "Le visa pour le Togo se demande en ligne avant le départ, et la vaccination contre la fièvre jaune est obligatoire.",
                   f"Comparez les escales ({ESCALES_OUEST}, Abidjan…) : elles sont souvent moins chères que le direct en juillet."],
         faq=("Lomé ou Cotonou : où arriver ?", "Les deux villes sont à environ 150 km l'une de l'autre. Comparez les deux : en été, un billet moins cher vers la ville voisine compense souvent le trajet par la route.")),
    dict(code="COO", ville="Cotonou", en="Cotonou", pays="Bénin", slug="cotonou",
         climat=["Comme à Lomé, la petite saison sèche dure de mi-juillet à mi-septembre : août est souvent le mois le plus sec de l'été.",
                 "Il fait 24 à 28 °C, et l'océan est agité : la baignade est déconseillée sur la plupart des plages."],
         conseils=["Le 1er août est la fête de l'Indépendance du Bénin : les vols de fin juillet sont plus demandés.",
                   "Le visa pour le Bénin se demande en ligne avant le départ (e-visa), et la vaccination contre la fièvre jaune est obligatoire.",
                   "Comparez aussi les vols vers Lomé, à environ 150 km par la route."],
         faq=("Quel est le mois le moins pluvieux à Cotonou en été ?", "Août, en général : c'est le cœur de la petite saison sèche, qui va de mi-juillet à mi-septembre.")),
    dict(code="OUA", ville="Ouagadougou", en="Ouagadougou", pays="Burkina Faso", slug="ouagadougou",
         climat=["La saison des pluies va de juin à septembre, avec un pic en août.",
                 "Les pluies font baisser la chaleur : 25 à 33 °C, contre plus de 40 °C en avril."],
         conseils=[f"Beaucoup de trajets passent par une escale ({ESCALES_OUEST}, Abidjan…) : comparez la durée totale du voyage.",
                   "Avant de réserver, consultez la fiche Burkina Faso des « Conseils aux voyageurs » du ministère des Affaires étrangères.",
                   "La vaccination contre la fièvre jaune est obligatoire : gardez votre carnet avec votre passeport."],
         faq=("Quand partir à Ouagadougou l'été ?", "Fin juin ou à partir de mi-août, si vous pouvez : les prix sont souvent plus bas qu'au début de juillet, et les pluies sont plus faibles en juin qu'en août.")),
    dict(code="NIM", ville="Niamey", en="Niamey", pays="Niger", slug="niamey",
         climat=["La saison des pluies va de juin à septembre, avec un pic en août ; les orages peuvent être violents.",
                 "Il fait très chaud : 27 à 35 °C."],
         conseils=[f"Les trajets vers Niamey passent en général par une escale ({ESCALES_OUEST}, Ouagadougou…) : comparez la durée totale autant que le prix.",
                   "Avant de réserver, consultez la fiche Niger des « Conseils aux voyageurs » du ministère des Affaires étrangères.",
                   "La vaccination contre la fièvre jaune est obligatoire."],
         faq=("Y a-t-il des vols directs Paris – Niamey ?", "Les trajets passent le plus souvent par une escale. Lancez la recherche pour voir les itinéraires proposés à vos dates et la durée totale de chaque vol.")),
    dict(code="NKC", ville="Nouakchott", en="Nouakchott", pays="Mauritanie", slug="nouakchott",
         climat=["Il pleut très peu à Nouakchott : quelques averses possibles en août et en septembre.",
                 "Il fait chaud (28 à 35 °C), mais l'air de l'océan rafraîchit la ville ; les vents de sable sont possibles."],
         conseils=["L'aéroport Oumtounsy est à environ 25 km au nord de la ville : prévoyez le transfert.",
                   "Comparez les vols avec escale à Casablanca, Alger, Tunis ou Dakar : ils sont souvent moins chers en été.",
                   "Vérifiez les conditions d'entrée (visa) sur la page trajet avant de réserver."],
         faq=("Fait-il trop chaud à Nouakchott en été ?", "Il fait chaud (28 à 35 °C), mais moins que dans l'intérieur du pays grâce à l'océan. La pluie est rare, avec quelques averses possibles en août-septembre.")),
    dict(code="ALG", ville="Alger", en="Algiers", pays="Algérie", slug="alger",
         climat=["L'été est chaud et sec sur la côte : 29 à 33 °C à Alger, beaucoup plus dans l'intérieur.",
                 "La mer est chaude et calme : c'est la grande saison des plages."],
         conseils=["Juillet et août sont la période la plus demandée de l'année vers l'Algérie : les prix montent vite à partir du printemps.",
                   "Le 5 juillet est la fête de l'Indépendance : les vols des jours précédents sont très demandés.",
                   "Le bateau depuis Marseille est une alternative si vous partez en voiture : comparez le prix total, avec le carburant et la cabine."],
         faq=("Quand réserver un vol pour Alger pour l'été ?", "Idéalement entre janvier et mars. Les prix de juillet-août vers l'Algérie montent fortement à partir du printemps, surtout pour les départs du début de juillet.")),
    dict(code="ORN", ville="Oran", en="Oran", pays="Algérie", slug="oran",
         climat=["L'été à Oran est chaud et sec : 28 à 32 °C, avec une brise de mer.",
                 "Pas de pluie de juin à août : c'est la grande saison des plages de l'Oranie."],
         conseils=["Comparez les départs de Paris, Lyon et Marseille : selon la ville, l'écart de prix pour juillet peut être important.",
                   "Le bateau depuis Marseille ou Alicante est une alternative si vous partez en voiture.",
                   "Comparez aussi les vols vers Tlemcen ou Alger si votre famille est entre les deux."],
         faq=("Quelle est la période la moins chère pour Oran l'été ?", "En général, les départs de fin juin et ceux de la deuxième quinzaine d'août. Les départs du début de juillet sont les plus chers.")),
    dict(code="CMN", ville="Casablanca", en="Casablanca", pays="Maroc", slug="casablanca",
         climat=["Grâce à l'océan, l'été est doux à Casablanca : 23 à 27 °C, avec parfois de la brume le matin.",
                 "Il ne pleut presque pas de juin à septembre."],
         conseils=["L'été, c'est l'opération Marhaba, l'accueil des Marocains résidant à l'étranger : les vols et les bateaux vers le Maroc sont très demandés de juillet à août.",
                   "Comparez Casablanca avec Rabat, Tanger, Fès, Oujda ou Nador : selon votre famille, un autre aéroport peut être moins cher et plus proche.",
                   "Les compagnies à bas prix desservent beaucoup de villes marocaines : vérifiez bien le prix avec les bagages."],
         faq=("Quel aéroport choisir pour le Maroc l'été ?", "Comparez plusieurs aéroports : Casablanca a le plus de vols, mais Rabat, Tanger, Fès, Oujda ou Nador sont parfois moins chers et plus proches de votre destination.")),
    dict(code="TUN", ville="Tunis", en="Tunis", pays="Tunisie", slug="tunis",
         climat=["L'été est chaud et sec : 30 à 33 °C à Tunis, et la mer est chaude.",
                 "Il ne pleut presque pas de juin à août."],
         conseils=["Comparez Tunis avec Monastir, Enfidha et Djerba : selon la région de votre famille, un autre aéroport peut être moins cher.",
                   "Le bateau depuis Marseille ou Gênes est une alternative si vous partez en voiture.",
                   "Juillet et août sont la haute saison : les tarifs avec bagages en soute partent en premier."],
         faq=("Vaut-il mieux arriver à Tunis ou à Monastir ?", "Comparez les deux, ainsi qu'Enfidha et Djerba : l'été, les prix varient beaucoup d'un aéroport à l'autre, et le plus proche de votre famille n'est pas toujours le plus cher.")),
]


def path(d):
    return f"{SLUG}-{d['slug']}"


def build(page, E, extras_html, alert_btn, domain, route_exists, hub_exists, wa_btn):
    """Écrit les pages été (une par destination + la page d'ensemble). Renvoie les URL pour le sitemap."""
    urls = []
    for d in DEST:
        v, code = d["ville"], d["code"]
        route = f"vol-paris-{d['slug']}"
        rows = "".join(
            f'<tr data-from="CDG" data-to="{code}" data-dep="{dep}" data-ret="{ret}"><th scope="row">{E(lab)}<span class="small ete-note">{E(note)}</span></th>'
            f'<td class="fp" aria-live="polite">Recherche…</td>'
            f'<td><a class="price-go" href="/?type=vols&amp;from=CDG&amp;to={code}&amp;dep={d1}&amp;ret={d2}">Voir les vols</a></td></tr>'
            for dep, ret, d1, d2, lab, note in PERIODES)
        orig = "".join(
            f'<tr data-from="{o}" data-to="{code}" data-dep="2027-07" data-ret="2027-08"><th scope="row">{E(c)} → {E(v)}</th>'
            f'<td class="fp" aria-live="polite">Recherche…</td>'
            f'<td><a class="price-go" href="/?type=vols&amp;from={o}&amp;to={code}&amp;dep=2027-07-10&amp;ret=2027-08-07">Voir les vols</a></td></tr>'
            for o, c in DEPARTS)
        thead = '<thead><tr><th scope="col">{}</th><th scope="col">Prix repéré</th><th scope="col"><span class="sr-only">Voir</span></th></tr></thead>'
        hero = (f'<p class="eyebrow">Vacances d\'été {ANNEE} · {E(d["pays"])}</p>'
                f'<h1>Vol pour {E(v)} cet été {ANNEE}</h1>'
                f'<p class="hero-lead">Les prix repérés pour juillet et août {ANNEE} vers {E(v)}, le meilleur moment pour partir et réserver, et ce qu\'il faut savoir sur l\'été là-bas.</p>'
                f'<p class="hero-price" id="hero-price" hidden></p>'
                f'<div class="cta-row"><a class="btn" href="/?type=vols&amp;from=CDG&amp;to={code}&amp;dep=2027-07-03&amp;ret=2027-07-31">Comparer les vols de l\'été</a>{alert_btn("fr")}</div>')
        body = (f'<section><h2>Quand partir cet été ?</h2>'
                f'<table class="fete-table ete-table">{thead.format("Période (depuis Paris)")}<tbody>{rows}</tbody></table>'
                f'<p class="small">Prix aller-retour le plus bas repéré récemment pour chaque période, par personne. Les dates indiquées sont celles du vol trouvé ; le tarif exact se confirme sur le site de réservation. '
                f'S\'il n\'y a pas encore de prix, c\'est que peu de voyageurs ont déjà cherché ces dates : créez une alerte pour être prévenu.</p></section>'
                f'<section><h2>Depuis quel aéroport partir ?</h2>'
                f'<table class="fete-table ete-table">{thead.format("Trajet (départ en juillet, retour en août)")}<tbody>{orig}</tbody></table></section>'
                f'<section id="price-alert" class="price-alert" data-from="CDG" data-to="{code}" hidden></section>'
                + f'<section><h2>Les bons plans chaque semaine</h2><p>Les prix les plus bas vers {E(v)} et l\'Afrique, chaque semaine sur WhatsApp, gratuitement.</p>{wa_btn("fr")}</section>'
                f'<section><h2>Le temps à {E(v)} en juillet et en août</h2>' + "".join(f"<p>{E(x)}</p>" for x in d["climat"]) + "</section>"
                f'<section><h2>À savoir pour l\'été {ANNEE}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in d["conseils"]) + "</ul></section>"
                '<section><h2>Quand réserver ?</h2><ul>'
                '<li><strong>Entre janvier et mars</strong> : la meilleure période pour réserver un vol de juillet ou d\'août vers l\'Afrique et le Maghreb.</li>'
                '<li><strong>À partir d\'avril</strong> : les prix de l\'été montent, surtout pour les départs du premier week-end des vacances (3 juillet).</li>'
                '<li><strong>Dates flexibles</strong> : activez l\'option ±3 jours dans la recherche, décaler le départ de quelques jours change souvent beaucoup le prix.</li></ul></section>'
                f'<section class="faq"><h2>Questions fréquentes</h2><details><summary>{E(d["faq"][0])}</summary><p>{E(d["faq"][1])}</p></details>'
                f'<details><summary>Quand acheter un billet pour {E(v)} pour l\'été {ANNEE} ?</summary><p>Idéalement entre janvier et mars {ANNEE}. Les places les moins chères de juillet et d\'août partent en premier, et les prix montent nettement à partir du printemps.</p></details></section>'
                + extras_html("fr", v, d["en"], code)
                + '<section><h2>Pages utiles</h2><ul class="route-links">'
                + (f'<li><a href="/{route}/">Vol Paris → {E(v)} toute l\'année : calendrier des prix, visa, bagages</a></li>' if route_exists(route) else "")
                + (f'<li><a href="/vols-pour-{d["slug"]}/">Tous les vols pour {E(v)}</a></li>' if hub_exists(f"vols-pour-{d['slug']}") else "")
                + '<li><a href="/vols-vacances-ete/">Vols pour les vacances d\'été : toutes les destinations</a></li>'
                + f'<li><a href="/{SLUG}/">L\'été {ANNEE} : toutes nos pages par destination</a></li></ul></section>'
                + '<section><h2>Autres destinations cet été</h2><ul class="links">'
                + "".join(f'<li><a href="/{path(o)}/">Vol pour {E(o["ville"])} été {ANNEE}</a></li>' for o in DEST if o is not d) + "</ul></section>"
                + '<script src="/ete.js" defer></script><script src="/alerts.js" defer></script>')
        faq = [d["faq"], (f"Quand acheter un billet pour {v} pour l'été {ANNEE} ?", f"Idéalement entre janvier et mars {ANNEE}. Les places les moins chères de juillet et d'août partent en premier, et les prix montent nettement à partir du printemps.")]
        ld = ('<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False) + "</script>")
        urls.append(page(path(d), f"Vol pour {v} été {ANNEE} : prix juillet-août | Escale",
                         f"Billet d'avion pour {v} cet été {ANNEE} : prix repérés pour juillet et août depuis Paris, Lyon, Marseille, Bruxelles, Genève, climat et quand réserver.",
                         hero, body, ld))
    items = "".join(f'<li><a href="/{path(d)}/"><strong>{E(d["ville"])}</strong></a> · <span class="small">{E(d["pays"])}</span></li>' for d in DEST)
    hero = (f'<p class="eyebrow">Vacances d\'été {ANNEE}</p><h1>Rentrer au pays cet été {ANNEE}</h1>'
            f'<p class="hero-lead">Pour chaque destination : les prix repérés pour juillet et août, le meilleur moment pour partir, le temps qu\'il fera et nos conseils pour payer moins cher.</p>')
    body = (f'<section><h2>Choisissez votre destination</h2><ul class="route-links">{items}</ul></section>'
            '<section><h2>Les dates à retenir</h2><ul>'
            f'<li>Vacances scolaires d\'été {ANNEE} : du samedi 3 juillet au jeudi 2 septembre (zones A, B et C).</li>'
            '<li>Les départs du premier week-end (2 au 4 juillet) et les retours de fin août sont les plus chers.</li>'
            '<li>Réservez de préférence entre janvier et mars : les prix de l\'été montent ensuite.</li></ul></section>'
            '<section><p><a class="btn" href="/vols-vacances-ete/">Voir les prix de l\'été par trajet</a></p></section>')
    urls.append(page(SLUG, f"Vacances d'été {ANNEE} au pays : prix des vols par destination | Escale",
                     f"Vols pour l'été {ANNEE} vers Dakar, Bamako, Abidjan, Conakry, Douala, Kinshasa, Alger, Casablanca, Tunis… : prix de juillet-août et quand réserver.",
                     hero, body))
    return urls
