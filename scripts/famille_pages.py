"""Pages « Faire venir sa famille en France ou en Italie » (français) : une page par ville de départ + une page d'ensemble.

Elles visent les recherches « faire venir sa mère d'Abidjan », « billet Dakar Paris pour mes parents », « invitation visa famille »…
Chaque page : prix repérés des vols vers l'Europe (chargés par site/ete.js depuis /api/prix, qui cherche au mois),
démarches de visa pour la France et pour l'Italie, quand acheter le billet, liens officiels.
Démarches vérifiées en octobre 2026 (à revérifier chaque année) : visa Schengen de court séjour (90 jours sur 180),
frais de 90 € par adulte et 45 € de 6 à 12 ans (gratuit avant 6 ans), assurance médicale d'au moins 30 000 € (règlement CE 810/2009),
attestation d'accueil validée en mairie avec un timbre fiscal de 30 € (France), dichiarazione di ospitalità dans les 48 h (Italie, art. 7 D.Lgs. 286/1998).
"""
import datetime
import json

# code, ville, pays, slug
VILLES = [
    ("ABJ", "Abidjan", "Côte d'Ivoire", "abidjan"), ("DSS", "Dakar", "Sénégal", "dakar"), ("BKO", "Bamako", "Mali", "bamako"),
    ("CKY", "Conakry", "Guinée", "conakry"), ("DLA", "Douala", "Cameroun", "douala"), ("FIH", "Kinshasa", "RD Congo", "kinshasa"),
    ("ALG", "Alger", "Algérie", "alger"), ("CMN", "Casablanca", "Maroc", "casablanca"), ("TUN", "Tunis", "Tunisie", "tunis"),
]
ARRIVEES = [("CDG", "Paris"), ("LYS", "Lyon"), ("MRS", "Marseille"), ("BRU", "Bruxelles"), ("MXP", "Milan"), ("FCO", "Rome")]
SLUG = "faire-venir-sa-famille"
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def _mois(n):
    """Mois dans n mois à partir d'aujourd'hui : (« AAAA-MM », « mars 2027 »)."""
    d = datetime.date.today().replace(day=1)
    y, m = d.year + (d.month - 1 + n) // 12, (d.month - 1 + n) % 12 + 1
    return f"{y}-{m:02d}", f"{MOIS[m - 1]} {y}"


def de(v):
    """« de Dakar », « d'Abidjan »."""
    return ("d'" if v[0] in "AEIOUÉ" else "de ") + v


def path(slug):
    return f"{SLUG}-{slug}"


def build(page, E, alert_btn, route_exists, wa_btn):
    urls = []
    (m2, l2), (m3, l3), (m4, l4) = _mois(2), _mois(3), _mois(4)
    thead = '<thead><tr><th scope="col">{}</th><th scope="col">Prix repéré</th><th scope="col"><span class="sr-only">Voir</span></th></tr></thead>'
    for code, v, pays, slug in VILLES:
        rows = "".join(
            f'<tr data-from="{code}" data-to="{a}" data-dep="{m2}" data-ret="{m3}"><th scope="row">{E(v)} → {E(c)}</th>'
            f'<td class="fp" aria-live="polite">Recherche…</td>'
            f'<td><a class="price-go" href="/?type=vols&amp;from={code}&amp;to={a}&amp;dep={m2}-10&amp;ret={m3}-05">Voir les vols</a></td></tr>'
            for a, c in ARRIVEES)
        per = "".join(
            f'<tr data-from="{code}" data-to="CDG" data-dep="{d}" data-ret="{r}"><th scope="row">{E(lab)}</th>'
            f'<td class="fp" aria-live="polite">Recherche…</td>'
            f'<td><a class="price-go" href="/?type=vols&amp;from={code}&amp;to=CDG&amp;dep={d}-10&amp;ret={r}-05">Voir les vols</a></td></tr>'
            for d, r, lab in [(m2, m3, f"Arrivée en {l2}, retour en {l3}"), (m3, m4, f"Arrivée en {l3}, retour en {l4}")])
        hero = (f'<p class="eyebrow">Faire venir sa famille · {E(pays)}</p>'
                f'<h1>Faire venir sa famille {E(de(v))} en France ou en Italie</h1>'
                f'<p class="hero-lead">Le prix des billets {E(v)} → Europe repérés en ce moment, les démarches de visa (attestation d\'accueil, invitation, assurance) et le bon moment pour acheter le billet.</p>'
                f'<p class="hero-price" id="hero-price" hidden></p>'
                f'<div class="cta-row"><a class="btn" href="/?type=vols&amp;from={code}&amp;to=CDG&amp;dep={m2}-10&amp;ret={m3}-05">Comparer les vols {E(v)} → Paris</a></div>')
        body = (f'<section><h2>Combien coûte le billet ?</h2>'
                f'<table class="fete-table ete-table">{thead.format(f"Trajet (arrivée en {l2}, retour en {l3})")}<tbody>{rows}</tbody></table>'
                f'<table class="fete-table ete-table">{thead.format(f"{v} → Paris, selon la période")}<tbody>{per}</tbody></table>'
                '<p class="small">Prix aller-retour le plus bas repéré récemment, par personne, au départ d\'Afrique. Le tarif exact se confirme sur le site de réservation. '
                'Vous pouvez payer le billet depuis l\'Europe : la recherche fonctionne quel que soit le pays où vous êtes.</p></section>'
                '<section><h2>Les démarches pour venir en France</h2><ul>'
                '<li><strong>Visa de court séjour (Schengen)</strong> : il permet de rester jusqu\'à 90 jours. La demande se fait en ligne sur le site officiel France-Visas, puis au centre de dépôt des demandes du pays. Frais : 90 € par adulte, 45 € de 6 à 12 ans, gratuit avant 6 ans, plus les frais de service du centre.</li>'
                '<li><strong>Attestation d\'accueil</strong> : si votre parent loge chez vous, vous la demandez à la mairie de votre domicile, avec un timbre fiscal de 30 €. Vous l\'envoyez ensuite à votre parent pour sa demande de visa.</li>'
                '<li><strong>Assurance voyage</strong> obligatoire : au moins 30 000 € de frais médicaux et le rapatriement, pour toute la durée du séjour.</li>'
                '<li><strong>Justificatifs</strong> demandés en général : passeport valide, ressources, réservation de vol, et parfois une lettre expliquant le séjour.</li></ul></section>'
                '<section><h2>Les démarches pour venir en Italie</h2><ul>'
                '<li><strong>Visa de court séjour (Schengen)</strong>, demandé auprès du consulat d\'Italie ou du centre de visa du pays, avec les mêmes frais.</li>'
                '<li><strong>Lettre d\'invitation</strong> (« lettera d\'invito ») et justificatif de logement, avec la copie de votre titre de séjour.</li>'
                '<li><strong>À l\'arrivée</strong> : la personne qui héberge fait la « dichiarazione di ospitalità » au commissariat ou à la mairie dans les 48 heures.</li>'
                '<li>Assurance voyage d\'au moins 30 000 €, comme pour la France.</li></ul></section>'
                '<section><h2>Quand acheter le billet ?</h2><ul>'
                '<li>La demande de visa peut être déposée jusqu\'à 6 mois avant le voyage, et au plus tard environ 15 jours avant : déposez-la tôt.</li>'
                '<li>Pour le dossier, une <strong>réservation de vol</strong> suffit souvent. Si vous achetez le billet avant d\'avoir le visa, choisissez un tarif modifiable ou remboursable.</li>'
                '<li>Activez les dates flexibles (±3 jours) dans la recherche : décaler l\'arrivée de quelques jours change souvent beaucoup le prix.</li></ul></section>'
                f'<section id="price-alert" class="price-alert" data-from="{code}" data-to="CDG" hidden></section>'
                '<section><h2>Liens officiels</h2><ul>'
                '<li><a href="https://france-visas.gouv.fr/" target="_blank" rel="noopener">France-Visas</a> : demande de visa pour la France</li>'
                '<li><a href="https://www.service-public.fr/particuliers/vosdroits/F2191" target="_blank" rel="noopener">Service-public.fr</a> : l\'attestation d\'accueil</li>'
                '<li><a href="https://vistoperitalia.esteri.it/" target="_blank" rel="noopener">Il visto per l\'Italia</a> : visa pour l\'Italie</li></ul>'
                '<p class="small">Les règles et les montants changent : vérifiez toujours sur ces sites officiels avant de déposer un dossier. Escale ne délivre ni visa ni assurance.</p></section>'
                f'<section><h2>Les bons plans chaque semaine</h2><p>Les prix les plus bas entre l\'Europe et l\'Afrique, chaque semaine sur WhatsApp, gratuitement.</p>{wa_btn("fr")}</section>'
                '<section class="faq"><h2>Questions fréquentes</h2>'
                f'<details><summary>Combien coûte un billet {E(v)} – Paris ?</summary><p>Les prix repérés en ce moment sont dans le tableau en haut de cette page. Ils changent chaque jour : comparez plusieurs dates et créez une alerte prix si le voyage est dans plusieurs mois.</p></details>'
                '<details><summary>Faut-il acheter le billet avant d\'avoir le visa ?</summary><p>Ce n\'est pas obligatoire : une réservation suffit souvent pour le dossier. Si vous achetez avant, choisissez un tarif modifiable ou remboursable.</p></details>'
                '<details><summary>Combien coûte l\'attestation d\'accueil ?</summary><p>Un timbre fiscal de 30 €, payé par la personne qui accueille, à la demande en mairie.</p></details></section>'
                + '<section><h2>Pages utiles</h2><ul class="route-links">'
                + (f'<li><a href="/vol-paris-{slug}/">Vol Paris → {E(v)} : calendrier des prix</a></li>' if route_exists(f"vol-paris-{slug}") else "")
                + f'<li><a href="/{SLUG}/">Faire venir sa famille : toutes les villes</a></li></ul></section>'
                + '<section><h2>Depuis une autre ville</h2><ul class="links">'
                + "".join(f'<li><a href="/{path(s)}/">Faire venir sa famille {E(de(o))}</a></li>' for c, o, p, s in VILLES if c != code) + "</ul></section>"
                + '<script src="/ete.js" defer></script><script src="/alerts.js" defer></script>')
        faq = [(f"Combien coûte un billet {v} – Paris ?", "Les prix repérés en ce moment sont dans le tableau en haut de la page. Ils changent chaque jour : comparez plusieurs dates et créez une alerte prix."),
               ("Faut-il acheter le billet avant d'avoir le visa ?", "Ce n'est pas obligatoire : une réservation suffit souvent pour le dossier. Si vous achetez avant, choisissez un tarif modifiable ou remboursable."),
               ("Combien coûte l'attestation d'accueil ?", "Un timbre fiscal de 30 €, payé par la personne qui accueille, à la demande en mairie.")]
        ld = ('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False) + "</script>")
        urls.append(page(path(slug), f"Faire venir sa famille {de(v)} en France ou en Italie : billet et visa | Escale",
                         f"Faire venir ses parents {de(v)} : prix des billets {v} → Paris, Lyon, Bruxelles, Milan, Rome, visa, attestation d'accueil et assurance.",
                         hero, body, ld))
    items = "".join(f'<li><a href="/{path(s)}/"><strong>{E(v)}</strong></a> · <span class="small">{E(p)}</span></li>' for c, v, p, s in VILLES)
    hero = ('<p class="eyebrow">Faire venir sa famille</p><h1>Faire venir ses parents en France ou en Italie</h1>'
            '<p class="hero-lead">Pour chaque ville : le prix des billets vers l\'Europe repéré en ce moment, les démarches de visa et le bon moment pour acheter.</p>')
    body = (f'<section><h2>D\'où vient votre famille ?</h2><ul class="route-links">{items}</ul></section>'
            '<section><h2>L\'essentiel</h2><ul><li>Un visa de court séjour (Schengen) est nécessaire, pour 90 jours au plus.</li>'
            '<li>France : attestation d\'accueil en mairie (timbre fiscal de 30 €). Italie : lettre d\'invitation, puis déclaration d\'hospitalité dans les 48 heures après l\'arrivée.</li>'
            '<li>Assurance voyage d\'au moins 30 000 € obligatoire.</li>'
            '<li>Achetez un tarif modifiable si vous prenez le billet avant d\'avoir le visa.</li></ul></section>')
    urls.append(page(SLUG, "Faire venir sa famille en France ou en Italie : billets et visa | Escale",
                     "Faire venir ses parents d'Abidjan, Dakar, Bamako, Conakry, Douala, Kinshasa, Alger, Casablanca ou Tunis : prix des billets et démarches de visa.",
                     hero, body))
    return urls
