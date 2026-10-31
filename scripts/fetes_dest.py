"""Pages « Vols pour la Tabaski 2027 » et « Vols pour l'Aïd el-Fitr 2027 » par destination (français).

Elles visent les recherches « billet Dakar Tabaski 2027 », « vol Alger Aïd 2027 »… Même principe que les pages été (ete.py) :
prix repérés par période et par aéroport de départ (chargés par site/ete.js depuis /api/prix, qui cherche au mois),
date estimée de la fête, quand partir et réserver, conseils propres à la destination, alerte prix.
À mettre à jour chaque année : FETES (dates, périodes) et les dates citées dans les textes.
Dates vérifiées en octobre 2026 (calendrier hégirien, à confirmer par l'observation de la lune) :
Aïd el-Fitr 1448 vers le mercredi 10 mars 2027 ; Aïd el-Adha (Tabaski) 1448 vers le dimanche 16 mai 2027 (16 ou 17 selon les pays).
"""
import json

ANNEE = 2027
DEPARTS = [("CDG", "Paris"), ("LYS", "Lyon"), ("MRS", "Marseille"), ("BRU", "Bruxelles"), ("GVA", "Genève")]

# code : (ville, pays, slug, conseil sur l'arrivée, valable toute l'année)
VILLES = {
    "DSS": ("Dakar", "Sénégal", "dakar", "L'aéroport Blaise-Diagne (AIBD) est à Diass, à environ 45 km du centre de Dakar : prévoyez le transfert, surtout pour une arrivée de nuit."),
    "BKO": ("Bamako", "Mali", "bamako", "La plupart des trajets vers Bamako passent par une escale (Casablanca, Alger, Tunis, Istanbul, Addis-Abeba…) : comparez le temps de correspondance autant que le prix. Consultez aussi la fiche Mali des « Conseils aux voyageurs » avant de réserver."),
    "CKY": ("Conakry", "Guinée", "conakry", "Comparez les vols directs et les vols avec escale (Casablanca, Dakar, Abidjan…) : avant une fête, l'écart de prix est souvent important. Le visa se demande en ligne avant le départ."),
    "ABJ": ("Abidjan", "Côte d'Ivoire", "abidjan", "L'aéroport Félix-Houphouët-Boigny est à Port-Bouët, au sud de la ville. Le visa pour la Côte d'Ivoire se demande en ligne (e-visa) avant le départ."),
    "OUA": ("Ouagadougou", "Burkina Faso", "ouagadougou", "Les vols vers Ouagadougou passent souvent par une escale (Abidjan, Casablanca, Alger, Istanbul…). Consultez la fiche Burkina Faso des « Conseils aux voyageurs » avant de réserver."),
    "NKC": ("Nouakchott", "Mauritanie", "nouakchott", "L'aéroport international Oumtounsy est au nord de Nouakchott. Comparez les vols avec escale à Casablanca, Alger, Tunis ou Dakar."),
    "ALG": ("Alger", "Algérie", "alger", "L'aéroport Houari-Boumediene est à l'est d'Alger. Comparez aussi Oran, Constantine ou Tlemcen si votre famille est loin de la capitale."),
    "ORN": ("Oran", "Algérie", "oran", "Comparez aussi les vols vers Tlemcen ou Alger si votre famille est entre les deux, et le bateau depuis Marseille si vous partez en voiture."),
    "CMN": ("Casablanca", "Maroc", "casablanca", "Comparez Casablanca avec Rabat, Tanger, Fès, Oujda ou Nador : selon votre famille, un autre aéroport peut être moins cher et plus proche."),
    "TUN": ("Tunis", "Tunisie", "tunis", "Comparez aussi Monastir, Enfidha et Djerba : selon votre famille, un autre aéroport peut être moins cher."),
}

FETES = [
    dict(key="tabaski", slug="vols-tabaski-2027", nom="la Tabaski", court="Tabaski", parent="vols-tabaski",
         date="vers le dimanche 16 mai 2027",
         dates_txt="La Tabaski (Aïd el-Kébir, Aïd el-Adha) 2027 devrait tomber vers le dimanche 16 mai 2027, le 16 ou le 17 selon les pays. La date exacte est fixée par l'observation de la lune, quelques jours avant.",
         villes=["DSS", "BKO", "CKY", "ABJ", "OUA", "NKC"],
         periodes=[("2027-05", "2027-05", "2027-05-09", "2027-05-23", "Départ début mai, retour fin mai", "Arriver une semaine avant la fête : le plus demandé."),
                   ("2027-04", "2027-05", "2027-04-30", "2027-05-20", "Départ fin avril, retour après la fête", "Partir plus tôt coûte souvent moins cher."),
                   ("2027-05", "2027-06", "2027-05-12", "2027-06-02", "Départ mi-mai, retour en juin", "Rester après la fête : les retours de juin sont plus calmes.")],
         def_dep="2027-05-09", def_ret="2027-05-23", mois="2027-05",
         conseil_fete="Pour la Tabaski, les vols des cinq à sept jours qui précèdent la fête sont les plus demandés, et les retours du lendemain de la fête aussi.",
         reserver="Idéalement entre janvier et mars 2027 : les prix montent nettement dans les six dernières semaines avant la fête."),
    dict(key="aid", slug="vols-aid-el-fitr-2027", nom="l'Aïd el-Fitr", court="Aïd el-Fitr", parent="vols-ramadan-aid-el-fitr",
         date="vers le mercredi 10 mars 2027",
         dates_txt="Le Ramadan 2027 devrait commencer vers le lundi 8 février 2027, et l'Aïd el-Fitr tomber vers le mercredi 10 mars 2027. Les dates exactes sont fixées par l'observation de la lune.",
         villes=["ALG", "ORN", "CMN", "TUN", "DSS", "BKO"],
         periodes=[("2027-03", "2027-03", "2027-03-05", "2027-03-17", "Départ début mars, retour mi-mars", "Arriver quelques jours avant l'Aïd : le plus demandé."),
                   ("2027-02", "2027-03", "2027-02-20", "2027-03-13", "Ramadan au pays, retour après l'Aïd", "Passer la fin du Ramadan en famille."),
                   ("2027-03", "2027-04", "2027-03-08", "2027-04-03", "Départ en mars, retour en avril", "Rester après la fête, avec les vacances de printemps.")],
         def_dep="2027-03-05", def_ret="2027-03-17", mois="2027-03",
         conseil_fete="Pour l'Aïd el-Fitr, les vols des derniers jours du Ramadan et les retours du week-end qui suit la fête sont les plus chers.",
         reserver="Idéalement entre novembre 2026 et janvier 2027 : les prix montent dans le mois qui précède l'Aïd."),
]


def path(f, code):
    return f"{f['slug']}-{VILLES[code][2]}"


def links(key):
    """Liste des pages par destination d'une fête (pour la page d'ensemble de la fête, en français)."""
    f = next((x for x in FETES if x["key"] == key), None)
    if not f:
        return ""
    return ('<section><h2>Par destination</h2><ul class="route-links">'
            + "".join(f'<li><a href="/{path(f, c)}/">Vol pour {VILLES[c][0]} · {f["court"]} {ANNEE}</a></li>' for c in f["villes"]) + "</ul></section>")


def build(page, E, extras_html, alert_btn, route_exists, hub_exists, wa_btn):
    """Écrit les pages (une par fête et par destination, plus une page d'ensemble par fête). Renvoie les URL pour le sitemap."""
    urls = []
    thead = '<thead><tr><th scope="col">{}</th><th scope="col">Prix repéré</th><th scope="col"><span class="sr-only">Voir</span></th></tr></thead>'
    for f in FETES:
        for code in f["villes"]:
            v, pays, slug, arrivee = VILLES[code]
            rows = "".join(
                f'<tr data-from="CDG" data-to="{code}" data-dep="{dep}" data-ret="{ret}"><th scope="row">{E(lab)}<span class="small ete-note">{E(note)}</span></th>'
                f'<td class="fp" aria-live="polite">Recherche…</td>'
                f'<td><a class="price-go" href="/?type=vols&amp;from=CDG&amp;to={code}&amp;dep={d1}&amp;ret={d2}">Voir les vols</a></td></tr>'
                for dep, ret, d1, d2, lab, note in f["periodes"])
            orig = "".join(
                f'<tr data-from="{o}" data-to="{code}" data-dep="{f["mois"]}" data-ret="{f["mois"]}"><th scope="row">{E(c)} → {E(v)}</th>'
                f'<td class="fp" aria-live="polite">Recherche…</td>'
                f'<td><a class="price-go" href="/?type=vols&amp;from={o}&amp;to={code}&amp;dep={f["def_dep"]}&amp;ret={f["def_ret"]}">Voir les vols</a></td></tr>'
                for o, c in DEPARTS)
            route = f"vol-paris-{slug}"
            hero = (f'<p class="eyebrow">{E(f["court"])} {ANNEE} · {E(pays)}</p>'
                    f'<h1>Vol pour {E(v)} pour {E(f["nom"])} {ANNEE}</h1>'
                    f'<p class="hero-lead">{E(f["court"])} {ANNEE} {E(f["date"])} : les prix repérés pour rentrer à {E(v)}, le meilleur moment pour partir et pour réserver.</p>'
                    f'<p class="hero-price" id="hero-price" hidden></p>'
                    f'<div class="cta-row"><a class="btn" href="/?type=vols&amp;from=CDG&amp;to={code}&amp;dep={f["def_dep"]}&amp;ret={f["def_ret"]}">Comparer les vols pour {E(f["nom"])}</a>{alert_btn("fr")}</div>')
            body = (f'<section><h2>Quand tombe {E(f["nom"])} {ANNEE} ?</h2><p>{E(f["dates_txt"])}</p></section>'
                    f'<section><h2>Quand partir ?</h2>'
                    f'<table class="fete-table ete-table">{thead.format("Période (depuis Paris)")}<tbody>{rows}</tbody></table>'
                    f'<p class="small">Prix aller-retour le plus bas repéré récemment pour chaque période, par personne. Les dates indiquées sont celles du vol trouvé ; le tarif exact se confirme sur le site de réservation. '
                    f'S\'il n\'y a pas encore de prix, c\'est que peu de voyageurs ont déjà cherché ces dates : créez une alerte pour être prévenu.</p></section>'
                    f'<section><h2>Depuis quel aéroport partir ?</h2>'
                    f'<table class="fete-table ete-table">{thead.format("Trajet (départ et retour pendant le mois de la fête)")}<tbody>{orig}</tbody></table></section>'
                    f'<section id="price-alert" class="price-alert" data-from="CDG" data-to="{code}" hidden></section>'
                    f'<section><h2>À savoir pour {E(f["nom"])} {ANNEE}</h2><ul><li>{E(f["conseil_fete"])}</li><li>{E(arrivee)}</li>'
                    '<li>Avec des valises de cadeaux, comparez les tarifs qui incluent deux bagages en soute : ils reviennent souvent moins cher qu\'un tarif de base avec bagages en supplément.</li></ul></section>'
                    f'<section><h2>Quand réserver ?</h2><p>{E(f["reserver"])} Activez l\'option « dates flexibles (±3 jours) » dans la recherche : décaler le départ de quelques jours change souvent beaucoup le prix.</p></section>'
                    f'<section><h2>Les bons plans chaque semaine</h2><p>Les prix les plus bas vers {E(v)} et l\'Afrique, chaque semaine sur WhatsApp, gratuitement.</p>{wa_btn("fr")}</section>'
                    f'<section class="faq"><h2>Questions fréquentes</h2>'
                    f'<details><summary>Quelle est la date de {E(f["nom"])} {ANNEE} ?</summary><p>{E(f["dates_txt"])}</p></details>'
                    f'<details><summary>Quand acheter un billet pour {E(v)} pour {E(f["nom"])} {ANNEE} ?</summary><p>{E(f["reserver"])}</p></details></section>'
                    + extras_html("fr", v, v, code)
                    + '<section><h2>Pages utiles</h2><ul class="route-links">'
                    + (f'<li><a href="/{route}/">Vol Paris → {E(v)} toute l\'année : calendrier des prix, visa, bagages</a></li>' if route_exists(route) else "")
                    + (f'<li><a href="/vols-pour-{slug}/">Tous les vols pour {E(v)}</a></li>' if hub_exists(f"vols-pour-{slug}") else "")
                    + f'<li><a href="/{f["parent"]}/">{E(f["court"])} {ANNEE} : les prix pour toutes les destinations</a></li>'
                    + f'<li><a href="/{f["slug"]}/">{E(f["court"])} {ANNEE} : toutes nos pages par destination</a></li></ul></section>'
                    + f'<section><h2>Autres destinations pour {E(f["nom"])}</h2><ul class="links">'
                    + "".join(f'<li><a href="/{path(f, o)}/">Vol pour {E(VILLES[o][0])} · {E(f["court"])} {ANNEE}</a></li>' for o in f["villes"] if o != code) + "</ul></section>"
                    + '<script src="/ete.js" defer></script><script src="/alerts.js" defer></script>')
            faq = [(f"Quelle est la date de {f['nom']} {ANNEE} ?", f["dates_txt"]), (f"Quand acheter un billet pour {v} pour {f['nom']} {ANNEE} ?", f["reserver"])]
            ld = ('<script type="application/ld+json">' + json.dumps({
                "@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False) + "</script>")
            urls.append(page(path(f, code), f"Vol {v} {f['court']} {ANNEE} : prix et dates | Escale",
                             f"Billet d'avion pour {v} pour {f['nom']} {ANNEE} ({f['date']}) : prix repérés depuis Paris, Lyon, Marseille, Bruxelles, Genève et quand réserver.",
                             hero, body, ld))
        items = "".join(f'<li><a href="/{path(f, c)}/"><strong>{E(VILLES[c][0])}</strong></a> · <span class="small">{E(VILLES[c][1])}</span></li>' for c in f["villes"])
        hero = (f'<p class="eyebrow">{E(f["court"])} {ANNEE}</p><h1>Rentrer au pays pour {E(f["nom"])} {ANNEE}</h1>'
                f'<p class="hero-lead">{E(f["court"])} {ANNEE} {E(f["date"])}. Pour chaque destination : les prix repérés, le meilleur moment pour partir et pour réserver.</p>')
        body = (f'<section><h2>Choisissez votre destination</h2><ul class="route-links">{items}</ul></section>'
                f'<section><h2>Les dates à retenir</h2><p>{E(f["dates_txt"])}</p><p>{E(f["conseil_fete"])} {E(f["reserver"])}</p></section>'
                f'<section><p><a class="btn" href="/{f["parent"]}/">Voir les prix de {E(f["nom"])} par trajet</a></p></section>')
        urls.append(page(f["slug"], f"{f['court']} {ANNEE} au pays : prix des vols par destination | Escale",
                         f"Vols pour {f['nom']} {ANNEE} ({f['date']}) vers " + ", ".join(VILLES[c][0] for c in f["villes"]) + " : prix repérés et quand réserver.",
                         hero, body))
    return urls
