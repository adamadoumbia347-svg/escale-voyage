"""Pages ajoutées le 12 novembre 2026 (demande de Dobam), en français :
  /escale-longue/ + Casablanca, Istanbul, Lisbonne, Addis-Abeba : que faire pendant une longue correspondance
  /ponts-2027/                         jours fériés et ponts 2027 (France, Italie, Belgique), liens de recherche par dates (site/ponts.js)
  /voyager-parent-age-enfant-seul/     assistance en aéroport, enfant qui voyage seul, documents
  /deces-rapatriement/                 démarches en cas de décès loin du pays (ton sobre, aucun tarif)
  /compte-a-rebours/                   image « J-45 avant Abidjan » à partager (site/compte.js)
Règles : aucun prix, aucun horaire, aucune règle de visa ; les conditions des compagnies (hôtel offert, visite gratuite) sont données
« sous conditions » avec le lien officiel, vérifiées le 12 novembre 2026 sur les sites des compagnies. Les jours fériés sont calculés (Pâques 2027 = 28 mars)."""
import datetime
import html

import build_i18n as B

E = html.escape
CHECKED = "novembre 2026"
EXT = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
ul = lambda items: "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
faq_html = lambda faq: "".join(f"<details><summary>{E(q)}</summary><p>{E(r)}</p></details>" for q, r in faq)
LIENS = [("escale-longue", "Longue escale : que faire à Casablanca, Istanbul, Lisbonne, Addis-Abeba"), ("ponts-2027", "Ponts et jours fériés 2027 : partir en posant peu de congés"),
         ("voyager-parent-age-enfant-seul", "Faire voyager un parent âgé ou un enfant seul"), ("deces-rapatriement", "Décès loin du pays : démarches et rapatriement"),
         ("compte-a-rebours", "Compte à rebours avant le départ, à partager")]
PLUS = '<section><h2>Pour aller plus loin</h2><ul>' + "".join(f'<li><a href="/{p}/">{E(t)}</a></li>' for p, t in LIENS) + '<li><a href="/guides/">Tous les guides</a></li></ul></section>'

# ---------------------------------------------------------------- escales longues
# slug, ville, code, compagnie, lien officiel du programme, ce que propose la compagnie, rejoindre la ville, sur place
HUBS = [
    ("casablanca", "Casablanca", "CMN", "Royal Air Maroc", "https://www.royalairmaroc.com/ma-fr/airport-transit",
     ["Pour une correspondance <strong>entre deux vols internationaux opérés par Royal Air Maroc</strong>, la compagnie prévoit selon la durée de l'escale un bon de repas, l'accès à un salon ou un hébergement.",
      "L'hébergement n'est <strong>pas garanti</strong> : il dépend de la durée de l'escale, du type de billet et des chambres disponibles. Demandez une confirmation écrite avant le départ, et renseignez-vous au comptoir de transit en arrivant.",
      "Sortir de l'aéroport suppose d'avoir le droit d'entrer au Maroc : vérifiez-le pour votre passeport avant de compter dessus."],
     ["Le <strong>train de l'ONCF</strong> part de la gare située sous le terminal vers Casa-Voyageurs et Casa-Port.", "Des <strong>taxis</strong> attendent devant le terminal : mettez-vous d'accord sur le prix avant de monter."],
     ["La <strong>mosquée Hassan II</strong>, au bord de l'océan, et la corniche d'Aïn Diab.", "Le quartier des <strong>Habous</strong> et le centre-ville Art déco, autour de la place Mohammed V."],
     "/arriver-aeroport-casablanca/"),
    ("istanbul", "Istanbul", "IST", "Turkish Airlines", "https://www.turkishairlines.com/fr-fr/flights/fly-different/touristanbul/",
     ["<strong>Touristanbul</strong> : une visite guidée gratuite de la ville pour les passagers en correspondance internationale de 6 à 24 heures, quand les deux vols sont opérés par Turkish Airlines sur la même réservation et que les horaires s'y prêtent.",
      "Un <strong>hébergement offert</strong> existe aussi pour les escales plus longues, sous conditions (durée, trajet, classe du billet). Les deux services ne se cumulent pas sur la même escale.",
      "Les conditions changent : lisez la page officielle avant de réserver, et vérifiez si votre passeport permet d'entrer en Turquie."],
     ["Le <strong>métro M11</strong> relie l'aéroport d'Istanbul à Gayrettepe, où l'on change pour le reste du réseau.", "Les <strong>bus Havaist</strong> desservent les grands quartiers (Taksim, Sultanahmet…)."],
     ["<strong>Sultanahmet</strong> : Sainte-Sophie, la Mosquée bleue et le palais de Topkapı sont à quelques minutes à pied les uns des autres.", "Le <strong>Grand Bazar</strong> et une traversée du Bosphore en bateau public."],
     ""),
    ("lisbonne", "Lisbonne", "LIS", "TAP Air Portugal", "https://www.flytap.com/fr-fr/stopover",
     ["Le programme <strong>Portugal Stopover</strong> permet d'ajouter un arrêt à Lisbonne ou à Porto, jusqu'à 10 jours, à l'aller ou au retour : on le choisit au moment de la réservation sur le site de TAP.",
      "Ce n'est pas un hôtel offert : l'hébergement reste à votre charge. L'intérêt est de visiter deux destinations avec un seul billet.",
      "Pour une simple correspondance de quelques heures, l'aéroport est proche du centre : une sortie est possible si votre passeport permet d'entrer dans l'espace Schengen."],
     ["Le <strong>métro, ligne rouge (Vermelha)</strong>, part de la station « Aeroporto » au terminal 1.", "Des <strong>bus</strong> de la ville et des taxis rejoignent le centre."],
     ["La <strong>Baixa</strong> et la place du Commerce, au bord du Tage.", "<strong>Belém</strong> : la tour, le monastère des Hiéronymites et les célèbres pastéis de nata."],
     "/aller-aeroport-lisbonne/"),
    ("addis-abeba", "Addis-Abeba", "ADD", "Ethiopian Airlines", "https://www.ethiopianairlines.com/RW/services/services-at-the-airport/addis-ababa-stopovers",
     ["Pour une correspondance de <strong>8 à 24 heures</strong> entre deux vols Ethiopian Airlines sur le même billet, la compagnie propose un hébergement de transit, sous conditions.",
      "Le bon se demande à l'enregistrement ou au comptoir de transit à l'arrivée. Vérifiez votre cas sur la page officielle ou auprès de la compagnie avant de partir : les conditions varient selon le billet.",
      "L'entrée en Éthiopie dépend de votre passeport : renseignez-vous avant de prévoir une sortie."],
     ["L'aéroport de Bole est <strong>tout proche du centre</strong> : la ville se rejoint en taxi.", "Les hôtels de transit ont en général leur <strong>navette</strong>."],
     ["Le <strong>Musée national d'Éthiopie</strong>, qui conserve le fossile de Lucy.", "Le quartier de <strong>Piazza</strong>, la cathédrale de la Sainte-Trinité et un café éthiopien préparé dans les règles."],
     ""),
]
H_PATH = lambda slug: f"escale-longue-{slug}"
H_FAQ = lambda v: [
    (f"Puis-je sortir de l'aéroport pendant mon escale à {v} ?", "Cela dépend de votre passeport, de la durée de l'escale et des règles d'entrée du pays. Vérifiez avant le départ avec l'outil visa d'Escale et sur les sites officiels, et gardez une marge large pour repasser les contrôles."),
    ("Dois-je récupérer mes bagages ?", "Avec un billet unique, les bagages en soute suivent en général jusqu'à la destination finale : faites-le confirmer à l'enregistrement. Avec deux billets séparés, vous devez les récupérer et les réenregistrer."),
    ("Combien de temps faut-il pour sortir et revenir ?", "Comptez le trajet aller et retour, les contrôles à la sortie puis à l'entrée, et l'heure limite d'embarquement. En dessous de six heures d'escale, il est souvent plus prudent de rester dans l'aéroport."),
    ("L'hôtel est-il vraiment offert par la compagnie ?", "Parfois, sous conditions : durée de l'escale, vols opérés par la même compagnie, type de billet, disponibilité. Ce n'est jamais automatique. Lisez la page officielle de la compagnie et demandez une confirmation avant de partir."),
]


def escales(site, ctx):
    urls = []
    for slug, ville, code, cie, off, offre, aller, voir, lien in HUBS:
        faq = H_FAQ(ville)
        autres = "".join(f'<li><a href="/{H_PATH(x[0])}/">Longue escale à {E(x[1])} ({x[2]})</a></li>' for x in HUBS if x[0] != slug)
        hero = (f'<p class="eyebrow">Escale longue · relu en {CHECKED}</p><h1>Longue escale à <span>{E(ville)}</span></h1>'
                f'<p class="hero-lead">Six, dix ou vingt heures de correspondance à {E(ville)} ({code}) : rester dans l\'aéroport ou sortir, ce que propose {E(cie)}, comment rejoindre la ville et quoi voir en quelques heures.</p>')
        body = ('<section><h2>En bref</h2>' + ul([
            "Avant tout, vérifiez si votre <strong>passeport</strong> permet de sortir de l'aéroport : <a href=\"/visa/\">outil visa</a>.",
            "En dessous de <strong>six heures</strong> d'escale, rester dans l'aéroport est souvent le plus sûr.",
            f"{E(cie)} propose des <strong>services d'escale</strong>, sous conditions : lisez-les avant de réserver.",
            "Gardez une <strong>marge large</strong> pour revenir : contrôles, trajet, heure limite d'embarquement."]) + '</section>'
                f'<section><h2>Ce que propose {E(cie)}</h2>' + ul(offre) + f'<p>Conditions à jour : {EXT(off, "page officielle de " + E(cie))}.</p></section>'
                f'<section><h2>Rejoindre la ville</h2>' + ul(aller) + (f'<p>Plus de détails : <a href="{lien}">guide de l\'aéroport</a>.</p>' if lien else "") + '</section>'
                f'<section><h2>À voir en quelques heures</h2>' + ul(voir) + '</section>'
                '<section><h2>Si vous restez dans l\'aéroport</h2>' + ul([
                    "Repérez votre porte d'embarquement dès l'arrivée, puis éloignez-vous : les grands aéroports sont longs à traverser.",
                    "Gardez chargeur, médicaments et une tenue de rechange dans le bagage cabine.",
                    'Préparez vos informations de vol même sans connexion : <a href="/kit-voyage-hors-ligne/">kit voyage hors ligne</a>.']) + '</section>'
                f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(faq)}</section>'
                f'<section><h2>Autres escales</h2><ul class="links">{autres}<li><a href="/guides/correspondances-escales/">Vol direct ou avec escale : comment choisir</a></li></ul></section>' + PLUS +
                '<p class="small">Les services des compagnies et les règles d\'entrée changent : les sites officiels font foi. Escale n\'est liée à aucune de ces compagnies.</p>' + B.faq_ld(faq))
        urls.append(B.write(site, H_PATH(slug), "fr", f"Longue escale à {ville} : sortir, dormir, que voir | Escale",
                            f"Longue correspondance à {ville} ({code}) : peut-on sortir de l'aéroport, ce que propose {cie} pendant l'escale, comment rejoindre la ville et quoi voir en quelques heures.",
                            hero, body, "", {"fr": H_PATH(slug)}, ctx))
    faq = H_FAQ("l'étranger")[1:]
    liste = "".join(f'<li><a href="/{H_PATH(x[0])}/">{E(x[1])} ({x[2]}) · {E(x[3])}</a></li>' for x in HUBS)
    hero = ('<p class="eyebrow">Guides · relus en ' + CHECKED + '</p><h1>Longue escale : <span>en profiter au lieu de la subir</span></h1>'
            '<p class="hero-lead">Beaucoup de vols vers l\'Afrique passent par Casablanca, Istanbul, Lisbonne ou Addis-Abeba. Voici quoi faire de ces heures, ville par ville.</p>')
    body = (f'<section><h2>Choisissez votre escale</h2><ul class="links">{liste}</ul></section>'
            '<section><h2>Les trois questions à se poser</h2>' + ul([
                "<strong>Ai-je le droit de sortir ?</strong> Cela dépend de votre passeport : <a href=\"/visa/\">outil visa</a>.",
                "<strong>Ai-je un seul billet ?</strong> Avec un billet unique, la correspondance est protégée et les bagages suivent en général. Avec deux billets, non.",
                "<strong>Ai-je assez de temps ?</strong> En dessous de six heures, restez dans l'aéroport."]) + '</section>'
            '<section><h2>Faire d\'une escale un deuxième voyage</h2><p>Certaines compagnies permettent de rester un ou plusieurs jours dans leur ville de correspondance sans changer de billet. C\'est plus sûr que deux billets séparés. Pour un trajet en plusieurs villes, voyez aussi l\'outil <a href="/vol-plusieurs-etapes/">vol à plusieurs étapes</a>.</p></section>'
            f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(faq)}</section>' + PLUS + B.faq_ld(faq))
    urls.append(B.write(site, "escale-longue", "fr", "Longue escale : que faire à Casablanca, Istanbul, Lisbonne | Escale",
                        "Longue correspondance sur un vol vers l'Afrique : sortir ou rester, hôtel parfois offert par la compagnie, que voir à Casablanca, Istanbul, Lisbonne et Addis-Abeba.",
                        hero, body, "", {"fr": "escale-longue"}, ctx))
    return urls


# ---------------------------------------------------------------- ponts 2027
ANNEE = 2027
PAQUES = datetime.date(2027, 3, 28)
D = datetime.date
_p = lambda n: PAQUES + datetime.timedelta(days=n)
FERIES = {
    "France": {D(2027, 1, 1): "Jour de l'An", _p(1): "Lundi de Pâques", D(2027, 5, 1): "Fête du Travail", D(2027, 5, 8): "8 Mai", _p(39): "Ascension", _p(50): "Lundi de Pentecôte",
               D(2027, 7, 14): "Fête nationale", D(2027, 8, 15): "Assomption", D(2027, 11, 1): "Toussaint", D(2027, 11, 11): "Armistice", D(2027, 12, 25): "Noël"},
    "Italie": {D(2027, 1, 1): "Jour de l'An", D(2027, 1, 6): "Épiphanie", _p(1): "Lundi de Pâques", D(2027, 4, 25): "Fête de la Libération", D(2027, 5, 1): "Fête du Travail", D(2027, 6, 2): "Fête de la République",
               D(2027, 8, 15): "Ferragosto", D(2027, 10, 4): "Saint François d'Assise", D(2027, 11, 1): "Toussaint", D(2027, 12, 8): "Immaculée Conception", D(2027, 12, 25): "Noël", D(2027, 12, 26): "Saint-Étienne"},
    "Belgique": {D(2027, 1, 1): "Jour de l'An", _p(1): "Lundi de Pâques", D(2027, 5, 1): "Fête du Travail", _p(39): "Ascension", _p(50): "Lundi de Pentecôte", D(2027, 7, 21): "Fête nationale",
                 D(2027, 8, 15): "Assomption", D(2027, 11, 1): "Toussaint", D(2027, 11, 11): "Armistice", D(2027, 12, 25): "Noël"},
}
DRAPEAU = {"France": "🇫🇷", "Italie": "🇮🇹", "Belgique": "🇧🇪"}
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
fr = lambda d: f"{JOURS[d.weekday()]} {d.day}{'er' if d.day == 1 else ''} {MOIS[d.month - 1]}"
court = lambda d: f"{d.day}{'er' if d.day == 1 else ''} {MOIS[d.month - 1]}"


def fenetres(feries):
    """Fenêtres qui vont d'un samedi à un dimanche : 9 jours (4 jours posés ou moins) et 16 jours (8 jours posés ou moins),
    plus les week-ends de 3 ou 4 jours autour d'un jour férié. Renvoie (début, fin, jours de repos, jours à poser, fériés inclus)."""
    out = []
    sam = D(ANNEE, 1, 2)
    while sam.year == ANNEE:
        for n, maxi in ((9, 4), (16, 8)):
            jours = [sam + datetime.timedelta(days=i) for i in range(n)]
            if jours[-1].year != ANNEE: continue
            ouvr = [j for j in jours if j.weekday() < 5]
            fer = [j for j in ouvr if j in feries]
            poses = len(ouvr) - len(fer)
            if fer and poses <= maxi and (n == 9 or len(fer) >= 2): out.append((jours[0], jours[-1], n, poses, [feries[j] for j in fer]))
        sam += datetime.timedelta(days=7)
    courts = []
    for j, nom in sorted(feries.items()):
        w = j.weekday()
        if w == 0: courts.append((j - datetime.timedelta(days=2), j, 3, 0, [nom]))
        elif w == 4: courts.append((j, j + datetime.timedelta(days=2), 3, 0, [nom]))
        elif w == 1: courts.append((j - datetime.timedelta(days=3), j, 4, 1, [nom]))
        elif w == 3: courts.append((j, j + datetime.timedelta(days=3), 4, 1, [nom]))
    return courts, [x for x in out if x[2] == 9], [x for x in out if x[2] == 16]


def ponts(site, ctx):
    blocs = ""
    for pays, feries in FERIES.items():
        courts, neuf, seize = fenetres(feries)
        ligne = lambda x: (f'<tr><td><strong>{x[2]} jours</strong><br><span class="small">{E(" + ".join(x[4]))}</span></td><td>du {fr(x[0])}<br>au {fr(x[1])}</td>'
                           f'<td>{x[3] if x[3] else "aucun"}</td><td><a class="pt-go" data-dep="{x[0].isoformat()}" data-ret="{x[1].isoformat()}" href="/">Voir les vols</a></td></tr>')
        table = lambda rows: ('<div class="bt-wrap"><table class="bt-table pt-table"><thead><tr><th>Durée</th><th>Dates</th><th>Jours à poser</th><th></th></tr></thead><tbody>'
                              + "".join(ligne(x) for x in rows) + "</tbody></table></div>")
        liste = ", ".join(f"{E(n)} ({fr(d)})" for d, n in sorted(feries.items()))
        perdus = [f"{E(n)} ({fr(d)})" for d, n in sorted(feries.items()) if d.weekday() >= 5]
        blocs += (f'<section id="{pays.lower()}"><h2>{DRAPEAU[pays]} {pays} : ponts {ANNEE}</h2>'
                  f'<p class="small">Jours fériés {ANNEE} : {liste}.</p>'
                  + (f'<p class="small">Tombent un week-end en {ANNEE} : {", ".join(perdus)}.</p>' if perdus else "")
                  + (f'<h3>Une ou deux semaines au pays</h3>{table(neuf + seize)}' if neuf or seize else "")
                  + (f'<h3>Week-ends prolongés</h3>{table(courts)}' if courts else "") + '</section>')
    faq = [("Qu'est-ce qu'un pont ?", "C'est un jour de congé posé entre un jour férié et un week-end : avec un jour férié le jeudi, poser le vendredi donne quatre jours de repos d'affilée."),
           ("Les billets sont-ils plus chers pendant les ponts ?", "Souvent, parce que beaucoup de monde part aux mêmes dates. Décaler le départ d'un jour ou deux, ou partir en milieu de semaine, fait parfois baisser le prix : comparez plusieurs dates avant de poser vos congés."),
           ("Mon employeur doit-il m'accorder le pont ?", "Non : un pont se demande comme un congé ordinaire, sauf si votre entreprise ou votre convention le prévoit. En France, le lundi de Pentecôte peut être travaillé au titre de la journée de solidarité selon l'entreprise."),
           ("Ces dates valent-elles pour ma région ?", "Ce sont les jours fériés nationaux. Certaines régions ou villes ont un jour férié en plus (Alsace-Moselle en France, la fête du saint patron de la ville en Italie) : vérifiez votre calendrier local.")]
    hero = (f'<p class="eyebrow">Calendrier {ANNEE}</p><h1>Ponts {ANNEE} : <span>partir au pays en posant peu de congés</span></h1>'
            f'<p class="hero-lead">Les jours fériés {ANNEE} en France, en Italie et en Belgique, et les meilleures fenêtres pour partir 9 ou 16 jours. Choisissez votre trajet : chaque ligne ouvre la recherche aux bonnes dates.</p>')
    body = ('<section><h2>Votre trajet</h2><form id="pt-form" class="tool-form" novalidate><div class="tool-grid">'
            '<label><span>Départ</span><input id="pt-from" placeholder="Ville ou aéroport" autocomplete="off"></label>'
            '<label><span>Arrivée</span><input id="pt-to" placeholder="Ville ou aéroport" autocomplete="off"></label></div>'
            '<p id="pt-msg" class="small" role="status">Choisissez le départ et l\'arrivée dans la liste : les liens « Voir les vols » ouvriront la recherche aux dates de chaque pont.</p></form>'
            '<p><a href="#france">🇫🇷 France</a> · <a href="#italie">🇮🇹 Italie</a> · <a href="#belgique">🇧🇪 Belgique</a></p></section>'
            + blocs +
            '<section><h2>Bien utiliser ce calendrier</h2>' + ul([
                "Les fenêtres vont d'un samedi à un dimanche : adaptez d'un jour ou deux selon vos horaires, les prix changent beaucoup d'un jour à l'autre.",
                "Avant de poser vos congés, regardez le prix : <a href=\"/acheter-ou-attendre/\">acheter maintenant ou attendre ?</a>",
                'Mettez une alerte prix sur votre trajet pour être prévenu si le tarif baisse.',
                'Les fêtes au pays suivent un autre calendrier : <a href="/diaspora/">rentrer au pays pour les fêtes</a>.']) + '</section>'
            f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(faq)}</section>' + PLUS +
            f'<p class="small">Jours fériés nationaux {ANNEE}, calculés à partir du calendrier officiel de chaque pays (Pâques : {fr(PAQUES)} {ANNEE}). Vérifiez votre calendrier local et celui de votre entreprise.</p>'
            + B.faq_ld(faq) + '<script src="/ac-mini.js" defer></script><script src="/ponts.js" defer></script>')
    return [B.write(site, "ponts-2027", "fr", "Ponts 2027 : jours fériés en France, Italie, Belgique | Escale",
                    "Jours fériés et ponts 2027 en France, en Italie et en Belgique : les fenêtres pour partir 9 ou 16 jours au pays en posant peu de congés, avec la recherche de vols aux bonnes dates.",
                    hero, body, "", {"fr": "ponts-2027"}, ctx)]


# ---------------------------------------------------------------- parent âgé, enfant seul
def accompagner(site, ctx):
    faq = [("L'assistance en aéroport est-elle payante ?", "Non : dans les aéroports de l'Union européenne, l'assistance aux personnes handicapées ou à mobilité réduite est gratuite. Elle couvre aussi une personne âgée qui marche difficilement. Elle se demande à la compagnie, de préférence à la réservation et au plus tard 48 heures avant le départ."),
           ("Faut-il un certificat médical pour demander l'assistance ?", "En règle générale, non : il suffit de décrire le besoin (ne peut pas marcher longtemps, ne monte pas les escaliers, se déplace en fauteuil). Un certificat peut être demandé dans des cas précis, par exemple pour voyager avec de l'oxygène : renseignez-vous auprès de la compagnie."),
           ("À partir de quel âge un enfant peut-il voyager seul ?", "Cela dépend de la compagnie : chacune fixe ses âges et propose, souvent contre un supplément, un service d'accompagnement pour les plus jeunes. Certaines compagnies à bas prix n'acceptent pas les enfants seuls. Vérifiez sur le site de la compagnie avant d'acheter le billet."),
           ("Quels papiers pour un enfant qui voyage sans ses parents ?", "Son propre passeport, le visa si le pays l'exige, et selon le pays de résidence une autorisation de sortie du territoire signée par un parent. Le pays d'arrivée peut demander d'autres documents : renseignez-vous auprès de son ambassade.")]
    hero = ('<p class="eyebrow">Guide · relu en ' + CHECKED + '</p><h1>Faire voyager <span>un parent âgé ou un enfant seul</span></h1>'
            '<p class="hero-lead">Maman vient pour la première fois en Europe, ou votre enfant rentre seul au pays pour les vacances : l\'assistance gratuite en aéroport, le service d\'accompagnement des enfants et les documents à préparer.</p>')
    body = ('<section><h2>En bref</h2>' + ul([
        "L'<strong>assistance en aéroport</strong> est gratuite dans l'Union européenne : demandez-la à la compagnie à la réservation, au plus tard 48 heures avant.",
        "Pour un <strong>enfant seul</strong>, chaque compagnie a ses règles et son service d'accompagnement : vérifiez avant d'acheter.",
        "Préférez un <strong>vol direct</strong>, ou une seule escale sur un billet unique.",
        "Préparez une <strong>pochette</strong> avec les papiers, les numéros à appeler et l'adresse d'arrivée."]) + '</section>'
            '<section><h2>Un parent âgé : l\'assistance gratuite</h2>' + ul([
                "L'assistance prend la personne en charge <strong>de l'entrée de l'aéroport jusqu'à son siège</strong>, puis à l'arrivée jusqu'à la sortie : enregistrement, contrôles, embarquement, bagages.",
                "Elle se demande <strong>à la compagnie</strong> (ou à l'agence), pas à l'aéroport : dès la réservation si possible, et au plus tard 48 heures avant le départ.",
                "Précisez le besoin : ne peut pas marcher longtemps, ne monte pas les escaliers, a besoin d'un fauteuil jusqu'à la porte ou jusqu'au siège.",
                "Le jour du départ, arrivez en avance et présentez-vous au point d'accueil de l'assistance ou au comptoir de la compagnie.",
                "Les droits des passagers à mobilité réduite : " + EXT("https://europa.eu/youreurope/citizens/travel/transport-disability/reduced-mobility/index_fr.htm", "Your Europe (Union européenne)") + " et " + EXT("https://www.ecologie.gouv.fr/politiques-publiques/aviation-droits-personnes-handicapees-personnes-mobilite-reduite", "ministère chargé des Transports (France)") + "."]) +
            '<p>Hors d\'Europe, l\'assistance existe aussi dans la plupart des grands aéroports, mais elle dépend de la compagnie : demandez-la pour <strong>tout le trajet</strong>, escale et arrivée comprises.</p></section>'
            '<section><h2>Un parent qui voyage pour la première fois</h2>' + ul([
                "Écrivez sur une feuille, en gros : le numéro de vol, la ville d'arrivée, votre nom, votre numéro et l'adresse où il va.",
                "Expliquez les étapes dans l'ordre : enregistrement, contrôle des bagages, contrôle des passeports, porte d'embarquement.",
                "Médicaments et ordonnance dans le bagage cabine, avec de quoi tenir une journée de plus.",
                'Envoyez-lui la carte du voyage, lisible sans connexion : <a href="/kit-voyage-hors-ligne/">kit voyage hors ligne</a>.',
                'Pour l\'invitation, l\'hébergement et le visa : <a href="/faire-venir-sa-famille/">faire venir sa famille</a>.']) + '</section>'
            '<section><h2>Un enfant qui voyage seul</h2>' + ul([
                "Les compagnies proposent un <strong>service d'accompagnement</strong> : un agent prend l'enfant en charge à l'enregistrement et le remet à l'adulte désigné à l'arrivée, sur présentation d'une pièce d'identité.",
                "L'âge minimum, l'âge jusqu'auquel le service est obligatoire et son prix <strong>changent d'une compagnie à l'autre</strong> ; il se réserve à l'avance, souvent par téléphone.",
                "Certaines compagnies n'acceptent pas d'enfant seul, ou pas sur les vols avec correspondance : vérifiez avant d'acheter.",
                "L'adulte qui accompagne l'enfant à l'aéroport reste sur place jusqu'au décollage ; celui qui l'attend à l'arrivée doit être celui dont le nom a été donné."]) + '</section>'
            '<section><h2>Les documents de l\'enfant</h2>' + ul([
                "Son <strong>propre passeport</strong>, valide assez longtemps après le retour, et le visa si le pays l'exige : <a href=\"/visa/\">outil visa</a>.",
                "<strong>Enfant qui vit en France</strong> et voyage sans l'un de ses parents : une autorisation de sortie du territoire signée par un parent, avec la copie de sa pièce d'identité (" + EXT("https://www.service-public.fr/particuliers/vosdroits/F1359", "service-public.fr") + ").",
                "<strong>Dans les autres pays</strong> (Italie, Belgique, Suisse…), les règles diffèrent : renseignez-vous auprès de la commune, de la police ou du consulat.",
                "Le pays d'arrivée peut exiger une autorisation parentale ou un acte de naissance : demandez à son ambassade.",
                'Le guide complet : <a href="/guides/voyager-avec-enfants/">voyager avec des enfants</a>.']) + '</section>'
            f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(faq)}</section>' + PLUS +
            '<p class="small">Ces repères sont généraux. Les règles des compagnies et des pays changent : leurs sites officiels font foi.</p>' + B.faq_ld(faq))
    return [B.write(site, "voyager-parent-age-enfant-seul", "fr", "Faire voyager un parent âgé ou un enfant seul en avion | Escale",
                    "Assistance gratuite en aéroport pour un parent âgé, service d'accompagnement d'un enfant qui voyage seul, autorisation de sortie du territoire : ce qu'il faut demander et quand.",
                    hero, body, "", {"fr": "voyager-parent-age-enfant-seul"}, ctx)]


# ---------------------------------------------------------------- décès, rapatriement
def deuil(site, ctx):
    faq = [("Qui organise le rapatriement d'un corps ?", "Une entreprise de pompes funèbres habilitée, avec l'accord des autorités du pays du décès et du pays d'arrivée. Le consulat conseille la famille et délivre les autorisations qui dépendent de lui, mais il n'organise pas le transport et ne le paie pas."),
           ("Qui paie le rapatriement ?", "La famille, sauf si une assurance le prévoit : contrat d'assistance ou de rapatriement, assurance de carte bancaire, mutuelle, contrat obsèques, caisse d'une association. Rassemblez les contrats du défunt avant de signer un devis."),
           ("Combien de temps cela prend-il ?", "Cela dépend des pays et des démarches (acte de décès, autorisations, vols disponibles). Les pompes funèbres vous donneront un délai réaliste : demandez-le par écrit."),
           ("Peut-on obtenir un billet d'avion en urgence pour un deuil ?", "Il n'existe pas de tarif « deuil » généralisé. Comparez les vols au départ de plusieurs aéroports et à un ou deux jours près, et appelez la compagnie : certaines acceptent de modifier un billet déjà acheté sur présentation d'un justificatif.")]
    hero = ('<p class="eyebrow">Guide · relu en ' + CHECKED + '</p><h1>Décès loin du pays : <span>démarches et rapatriement</span></h1>'
            '<p class="hero-lead">Un proche est décédé en Europe ou au pays. Voici, dans l\'ordre, ce qu\'il y a à faire, qui appeler et ce qu\'il faut vérifier avant de payer.</p>')
    body = ('<section><h2>Les premières heures</h2>' + ul([
        "Faites <strong>constater le décès</strong> par un médecin ou par l'hôpital, qui remet un certificat de décès.",
        "Prévenez le <strong>consulat ou l'ambassade</strong> du pays dont le défunt avait la nationalité : il explique les démarches et les documents nécessaires.",
        "Cherchez les <strong>contrats du défunt</strong> : assurance rapatriement, carte bancaire, mutuelle, contrat obsèques, association ou tontine. Certains prennent en charge tout ou partie des frais.",
        "Ne signez aucun devis dans l'urgence : demandez-en <strong>au moins deux</strong>, par écrit."]) + '</section>'
            '<section><h2>Le rapatriement du corps</h2>' + ul([
                "Il est organisé par une <strong>entreprise de pompes funèbres habilitée</strong>, qui s'occupe du cercueil aux normes du transport aérien, des autorisations et de la réservation auprès de la compagnie.",
                "Il faut en général l'<strong>acte de décès</strong>, une autorisation des autorités locales et un document du consulat du pays d'arrivée : les pompes funèbres en donnent la liste exacte.",
                "Le consulat <strong>conseille et délivre les documents qui dépendent de lui</strong> ; le transport reste à la charge de la famille ou de l'assurance.",
                "Demandez un devis <strong>détaillé</strong> : soins, cercueil, démarches, fret aérien, transport jusqu'à la ville d'arrivée."]) + '</section>'
            '<section><h2>Où se renseigner</h2>' + ul([
                "<strong>Décès en France</strong> : les démarches sont détaillées sur " + EXT("https://www.service-public.fr/", "service-public.fr") + ", rubrique « Décès ».",
                "<strong>Français décédé à l'étranger</strong> : le " + EXT("https://www.diplomatie.gouv.fr/fr/services-aux-francais/", "ministère de l'Europe et des Affaires étrangères") + " et le consulat de France du pays concerné.",
                "<strong>Autres nationalités</strong> : le consulat ou l'ambassade du pays d'origine, dans le pays où le décès a eu lieu.",
                "<strong>En Italie</strong> : la commune (Comune) du lieu du décès et les pompes funèbres indiquent les autorisations nécessaires au transport."]) + '</section>'
            '<section><h2>Partir pour les obsèques</h2>' + ul([
                'Comparez tout de suite plusieurs aéroports de départ et plusieurs dates : <a href="/billet-avion-urgent/">partir en urgence au pays</a>.',
                "Vérifiez la <strong>validité du passeport</strong> et le visa éventuel avant d'acheter : <a href=\"/visa/\">outil visa</a>.",
                "Si vous avez déjà un billet pour une autre date, appelez la compagnie : un changement est parfois possible sur justificatif.",
                "En France, le Code du travail prévoit des <strong>jours de congé pour le décès d'un proche</strong> : parlez-en à votre employeur."]) + '</section>'
            '<section><h2>Se protéger des abus</h2>' + ul([
                "Ne payez pas un intermédiaire inconnu qui promet de « tout régler » : passez par une entreprise identifiable, avec une adresse et un devis.",
                "Ne versez pas d'argent sur un compte personnel ou par transfert à un inconnu.",
                'En cas de doute sur un billet proposé par un « agent » : <a href="/verifier-billet-avion/">vérifier un billet d\'avion</a>.']) + '</section>'
            f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(faq)}</section>' + PLUS +
            '<p class="small">Ces repères sont généraux et ne remplacent pas les indications du consulat et des pompes funèbres. Escale ne vend ni assurance ni service funéraire et n\'affiche aucun tarif ici.</p>' + B.faq_ld(faq))
    return [B.write(site, "deces-rapatriement", "fr", "Décès loin du pays : démarches et rapatriement du corps | Escale",
                    "Un proche est décédé en Europe ou au pays : les premières démarches, qui organise et qui paie le rapatriement, les assurances à vérifier, où se renseigner et comment partir en urgence.",
                    hero, body, "", {"fr": "deces-rapatriement"}, ctx)]


# ---------------------------------------------------------------- compte à rebours
def compte(site, ctx):
    faq = [("Où va l'image ?", "Nulle part : elle est fabriquée dans votre téléphone. Vous la téléchargez ou vous la partagez vous-même, sur votre statut WhatsApp par exemple."),
           ("D'où vient le prix affiché ?", "C'est l'aller-retour le plus bas repéré récemment pour le mois de votre départ, si vous indiquez votre ville de départ. Sans ville de départ, ou sans prix connu, l'image n'affiche aucun prix.")]
    hero = ('<p class="eyebrow">Outil gratuit</p><h1>Compte à rebours <span>avant le départ</span></h1>'
            '<p class="hero-lead">« J-45 avant Abidjan » : créez votre image en dix secondes et partagez-la sur votre statut WhatsApp.</p>')
    body = ('<section><h2>Votre voyage</h2><form id="cr-form" class="tool-form" novalidate><div class="tool-grid">'
            '<label><span>Destination</span><input id="cr-to" placeholder="Ville ou aéroport" autocomplete="off"></label>'
            '<label><span>Date du départ</span><input id="cr-date" type="date"></label>'
            '<label><span>Ville de départ (facultatif)</span><input id="cr-from" placeholder="Pour afficher le prix du moment" autocomplete="off"></label></div>'
            '<p><button type="submit" class="btn">Créer mon image</button></p><p id="cr-msg" class="small" role="status"></p></form>'
            '<div id="cr-out" hidden><canvas id="cr-canvas" width="1080" height="1920" style="width:min(100%,320px);height:auto;border-radius:18px;box-shadow:0 20px 50px -20px rgba(0,0,0,.5)"></canvas>'
            '<p class="cr-btns" style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px"><button type="button" class="btn" id="cr-share">Partager</button><a class="btn ghost" id="cr-dl" download="escale-compte-a-rebours.jpg">Télécharger l\'image</a>'
            '<a class="btn ghost" id="cr-wa" target="_blank" rel="noopener">Envoyer sur WhatsApp</a></p></div></section>'
            '<section><h2>Et en attendant le départ</h2><ul><li><a href="/controle-avant-vol/">Contrôle avant le vol : passeport, visa, documents</a></li>'
            '<li><a href="/guides/check-list-depart/">Check-list du départ</a></li><li><a href="/ponts-2027/">Ponts 2027 : partir en posant peu de congés</a></li></ul></section>'
            f'<section class="faq"><h2>Questions fréquentes</h2>{faq_html(faq)}</section>' + PLUS + B.faq_ld(faq) +
            '<script src="/ac-mini.js" defer></script><script src="/compte.js" defer></script>')
    return [B.write(site, "compte-a-rebours", "fr", "Compte à rebours avant le départ : image à partager | Escale",
                    "Créez une image « J-45 avant Abidjan » pour votre statut WhatsApp : destination, date du départ, et le prix du moment si vous le souhaitez. Gratuit, rien n'est envoyé.",
                    hero, body, "", {"fr": "compte-a-rebours"}, ctx)]


def build(site, ctx):
    return escales(site, ctx) + ponts(site, ctx) + accompagner(site, ctx) + deuil(site, ctx) + compte(site, ctx)
