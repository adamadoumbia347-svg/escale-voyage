"""Pages « communauté » (/diaspora/cote-d-ivoire/, /diaspora/senegal/…) : pour chaque grande communauté africaine d'Europe,
le calendrier des moments où l'on rentre au pays (fêtes religieuses, Noël, fête nationale, vacances d'été) avec, pour chacun,
le prix aller-retour repéré depuis Paris (chargé par site/ete.js depuis /api/prix, comme les pages été), les trajets existants
depuis la France, la Belgique, l'Italie et Londres, et un bouton pour partager la page dans un groupe WhatsApp.
Les dates des fêtes musulmanes sont des dates prévues (observation de la lune) : la page le dit."""
import html
import urllib.parse

import build_i18n as B

E = html.escape
ANNEE = 2027
# Fêtes mobiles 2026-2027 (dates prévues : calendrier astronomique, à confirmer par l'observation de la lune)
NOEL = ("Noël et Nouvel An 2026", "2026-12", "2027-01", "2026-12-19", "2027-01-03", "Période la plus demandée de l'année : réservez dès septembre-octobre.")
RAMADAN = ("Ramadan et Aïd el-Fitr 2027", "2027-02", "2027-03", "2027-02-27", "2027-03-14", "Ramadan prévu du 8 février au 9 mars 2027 environ, Aïd el-Fitr vers le 9-10 mars (dates à confirmer).")
TABASKI = ("Tabaski (Aïd el-Kébir) 2027", "2027-05", "2027-06", "2027-05-20", "2027-06-05", "Tabaski prévue vers le 26-27 mai 2027 (date à confirmer selon la lune). Les prix montent 3 à 4 semaines avant.")
ETE = ("Vacances d'été 2027", "2027-07", "2027-08", "2027-07-10", "2027-08-14", "Juillet-août : le plus cher de l'année avec Noël ; réservez entre janvier et mars.")
PAQUES = ("Vacances de printemps 2027", "2027-04", "2027-04", "2027-04-10", "2027-04-25", "Pâques le 28 mars 2027 ; vacances scolaires françaises selon la zone, en avril.")

# code, nom, forme « en / au », drapeau, aéroports [(code, ville)], fêtes nationales [(libellé, date ISO)], périodes spécifiques, pays « lire aussi »
PAYS = [
    dict(slug="cote-d-ivoire", nom="Côte d'Ivoire", au="en Côte d'Ivoire", flag="🇨🇮", code="ci", aeroports=[("ABJ", "Abidjan")],
         nat=[("Fête de l'Indépendance", "2027-08-07")], fetes=[NOEL, RAMADAN, PAQUES, TABASKI, ETE], ville="Abidjan",
         intro="Abidjan est l'un des trajets les plus demandés depuis Paris, Bruxelles et l'Italie. Les retours au pays se concentrent sur Noël, la Tabaski et l'été."),
    dict(slug="senegal", nom="Sénégal", au="au Sénégal", flag="🇸🇳", code="sn", aeroports=[("DSS", "Dakar")],
         nat=[("Fête de l'Indépendance", "2027-04-04")], fetes=[NOEL, RAMADAN, TABASKI, ETE], ville="Dakar",
         intro="Dakar est desservi en direct depuis Paris, Bruxelles, Milan, Rome et Londres. La Tabaski et le Grand Magal de Touba (date lunaire) sont des périodes de forte demande."),
    dict(slug="mali", nom="Mali", au="au Mali", flag="🇲🇱", code="ml", aeroports=[("BKO", "Bamako")],
         nat=[("Fête de l'Indépendance", "2027-09-22")], fetes=[NOEL, RAMADAN, TABASKI, ETE], ville="Bamako",
         intro="Les vols directs Paris – Bamako sont rares selon les périodes : la plupart des trajets passent par Casablanca, Alger, Tunis ou Istanbul. Comparez la durée totale, pas seulement le prix."),
    dict(slug="guinee", nom="Guinée", au="en Guinée", flag="🇬🇳", code="gn", aeroports=[("CKY", "Conakry")],
         nat=[("Fête de l'Indépendance", "2027-10-02")], fetes=[NOEL, RAMADAN, TABASKI, ETE], ville="Conakry",
         intro="Conakry se rejoint depuis Paris et Bruxelles en direct ou via Casablanca, Dakar et Abidjan. Les prix montent fort avant la Tabaski et l'été."),
    dict(slug="cameroun", nom="Cameroun", au="au Cameroun", flag="🇨🇲", code="cm", aeroports=[("DLA", "Douala"), ("NSI", "Yaoundé")],
         nat=[("Fête nationale", "2027-05-20")], fetes=[NOEL, PAQUES, ETE], ville="Douala",
         intro="Douala et Yaoundé sont desservis depuis Paris et Bruxelles, en direct ou via Istanbul, Addis-Abeba et Casablanca. Décembre et l'été sont les périodes les plus chères."),
    dict(slug="rd-congo", nom="RD Congo", au="en RD Congo", flag="🇨🇩", code="cd", aeroports=[("FIH", "Kinshasa")],
         nat=[("Fête de l'Indépendance", "2027-06-30")], fetes=[NOEL, PAQUES, ETE], ville="Kinshasa",
         intro="Kinshasa se rejoint surtout depuis Bruxelles et Paris, en direct ou via Addis-Abeba, Istanbul et Casablanca. Noël et l'été concentrent la demande."),
    dict(slug="maroc", nom="Maroc", au="au Maroc", flag="🇲🇦", code="ma", aeroports=[("CMN", "Casablanca"), ("RAK", "Marrakech")],
         nat=[("Fête du Trône", "2027-07-30"), ("Fête de l'Indépendance", "2027-11-18")], fetes=[NOEL, RAMADAN, PAQUES, TABASKI, ETE], ville="Casablanca",
         intro="Le Maroc est l'une des destinations les mieux desservies d'Europe, avec des compagnies à bas prix depuis presque toutes les villes. Les prix montent autour de l'Aïd, en juillet-août et pendant les vacances scolaires."),
    dict(slug="algerie", nom="Algérie", au="en Algérie", flag="🇩🇿", code="dz", aeroports=[("ALG", "Alger"), ("ORN", "Oran")],
         nat=[("Fête de l'Indépendance", "2027-07-05"), ("Fête de la Révolution", "2027-11-01")], fetes=[NOEL, RAMADAN, PAQUES, TABASKI, ETE], ville="Alger",
         intro="Alger, Oran, Constantine et les autres villes sont desservies depuis Paris, Lyon, Marseille, Lille et Toulouse. L'été et l'Aïd sont très chers : pour juillet-août, réservez dès le début de l'année."),
    dict(slug="tunisie", nom="Tunisie", au="en Tunisie", flag="🇹🇳", code="tn", aeroports=[("TUN", "Tunis"), ("DJE", "Djerba")],
         nat=[("Fête de l'Indépendance", "2027-03-20")], fetes=[NOEL, RAMADAN, PAQUES, TABASKI, ETE], ville="Tunis",
         intro="Tunis et Djerba sont desservis depuis Paris, Marseille, Lyon, Milan et Rome, souvent à bas prix hors saison. Juillet-août et l'Aïd sont les périodes les plus chères."),
    dict(slug="togo", nom="Togo", au="au Togo", flag="🇹🇬", code="tg", aeroports=[("LFW", "Lomé")],
         nat=[("Fête de l'Indépendance", "2027-04-27")], fetes=[NOEL, RAMADAN, TABASKI, ETE], ville="Lomé",
         intro="Lomé est le hub d'ASKY : on y arrive depuis Paris et Bruxelles, en direct ou via Casablanca, Addis-Abeba et Istanbul."),
    dict(slug="benin", nom="Bénin", au="au Bénin", flag="🇧🇯", code="bj", aeroports=[("COO", "Cotonou")],
         nat=[("Fête de l'Indépendance", "2027-08-01")], fetes=[NOEL, RAMADAN, TABASKI, ETE], ville="Cotonou",
         intro="Cotonou se rejoint depuis Paris en direct ou via Casablanca, Istanbul et Addis-Abeba. Le 10 janvier (fête du Vodoun) et Noël sont des périodes de retours."),
    dict(slug="burkina-faso", nom="Burkina Faso", au="au Burkina Faso", flag="🇧🇫", code="bf", aeroports=[("OUA", "Ouagadougou")],
         nat=[("Fête de l'Indépendance", "2027-12-11")], fetes=[NOEL, RAMADAN, TABASKI, ETE], ville="Ouagadougou",
         intro="Ouagadougou se rejoint depuis Paris et Bruxelles, surtout via Casablanca, Istanbul, Addis-Abeba ou Abidjan."),
]
DEPARTS = [("CDG", "Paris"), ("BRU", "Bruxelles"), ("LYS", "Lyon"), ("MRS", "Marseille"), ("MXP", "Milan"), ("FCO", "Rome"), ("LHR", "Londres")]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def fr_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MOIS[int(m) - 1]} {y}"


def _row(code, lab, note, dep, ret, d1, d2):
    return (f'<tr data-from="CDG" data-to="{code}" data-dep="{dep}" data-ret="{ret}"><th scope="row">{E(lab)}<span class="small ete-note">{E(note)}</span></th>'
            f'<td class="fp" aria-live="polite">Recherche…</td>'
            f'<td><a class="price-go" href="/?type=vols&amp;from=CDG&amp;to={code}&amp;dep={d1}&amp;ret={d2}">Voir les vols</a></td></tr>')


def build(site, ctx, exists):
    urls = []
    thead = '<thead><tr><th scope="col">{}</th><th scope="col">Prix repéré</th><th scope="col"><span class="sr-only">Voir</span></th></tr></thead>'
    index_items = []
    for p in PAYS:
        code = p["aeroports"][0][0]
        path = f"diaspora/{p['slug']}"
        url = f"{ctx['domain']}/{path}/"
        # Périodes : fêtes mobiles + fêtes nationales (séjour autour de la date)
        rows = [_row(code, lab, note, dep, ret, d1, d2) for lab, dep, ret, d1, d2, note in p["fetes"]]
        for lab, iso in p["nat"]:
            ym = iso[:7]
            rows.append(_row(code, f"{lab} ({fr_date(iso)})", "Séjour d'une à deux semaines autour de la fête.", ym, ym, iso, iso))
        # Trajets existants vers chaque aéroport
        links = []
        for ac, ville in p["aeroports"]:
            for oc, oville in DEPARTS:
                slug_o = B.slugify(oville)
                for cand in (f"vol-{slug_o}-{B.slugify(ville)}", f"it/voli-{ {'Milan': 'milano', 'Rome': 'roma'}.get(oville, slug_o)}-{B.slugify(ville)}", f"en/flights-{ {'Londres': 'london'}.get(oville, slug_o)}-{B.slugify(ville)}"):
                    if exists(cand):
                        links.append(f'<li><a href="/{cand}/">{E(oville)} → {E(ville)}</a></li>')
                        break
            if exists(f"vols-pour-{B.slugify(ville)}"):
                links.append(f'<li><a href="/vols-pour-{B.slugify(ville)}/">Tous les vols pour {E(ville)}</a></li>')
        wa = "https://wa.me/?text=" + urllib.parse.quote(f"Calendrier des retours {p['au']} ({ANNEE}) avec les prix des billets : {url}")
        hero = (f'<p class="eyebrow">{p["flag"]} Communauté {E(p["nom"].replace("RD Congo", "congolaise"))}</p>'
                f'<h1>Rentrer {E(p["au"])} <span>en {ANNEE}</span></h1>'
                f'<p class="hero-lead">Noël, Ramadan, Tabaski, fête nationale, vacances d\'été : le calendrier des retours au pays, avec le prix aller-retour repéré depuis Paris pour chaque période, et les trajets existants depuis l\'Europe.</p>'
                f'<p class="hero-price" id="hero-price" hidden></p>'
                f'<div class="cta-row"><a class="btn" href="/?type=vols&amp;from=CDG&amp;to={code}">Comparer les vols</a>'
                f'<a class="btn ghost" href="{E(wa)}" target="_blank" rel="noopener">📲 Partager dans un groupe WhatsApp</a></div>')
        body = (f'<section><p>{E(p["intro"])}</p></section>'
                f'<section><h2>Les prix selon la période</h2><table class="fete-table ete-table" data-hero="CDG">{thead.format("Période (depuis Paris)")}<tbody>{"".join(rows)}</tbody></table>'
                '<p class="small">Prix aller-retour le plus bas repéré récemment pour chaque période, par personne, au départ de Paris. Les dates affichées sont celles du vol trouvé ; le tarif exact se confirme sur le site de réservation. '
                'Les dates des fêtes musulmanes sont prévisionnelles (observation de la lune). S\'il n\'y a pas encore de prix, peu de voyageurs ont cherché ces dates : créez une alerte.</p></section>'
                f'<section id="price-alert" class="price-alert" data-from="CDG" data-to="{code}" hidden></section>'
                + (f'<section><h2>Les trajets depuis l\'Europe</h2><ul class="route-links">{"".join(links)}</ul></section>' if links else "")
                + '<section><h2>Quand réserver pour payer moins cher ?</h2><ul>'
                '<li><strong>Noël</strong> : réservez entre septembre et mi-octobre ; en décembre, les prix doublent souvent.</li>'
                '<li><strong>Tabaski et Aïd el-Fitr</strong> : 6 à 8 semaines avant, les prix sont encore raisonnables ; les deux dernières semaines sont les plus chères.</li>'
                '<li><strong>Été</strong> : entre janvier et mars pour juillet-août. Décaler le départ d\'une semaine après la sortie des classes fait souvent une grosse différence.</li>'
                '<li><strong>Dates souples</strong> : activez ±3 jours dans la recherche, et comparez aussi un départ depuis une autre ville (Bruxelles, Lyon, Milan).</li>'
                f'<li>Pour savoir si le prix du moment est bon, regardez le verdict et le conseil sur la page du trajet, et le <a href="/barometre-prix/a-saisir/">tableau des trajets à saisir aujourd\'hui</a>.</li></ul></section>'
                f'<section><h2>Les bons plans chaque semaine</h2><p>Les prix les plus bas vers {E(p["ville"])} et l\'Afrique, deux fois par semaine sur WhatsApp, gratuitement.</p>{B.wa_btn("fr")}</section>'
                f'<section><h2>Pour aller plus loin</h2><ul><li><a href="/{p["code"]}/">Escale {E(p["nom"])} : les vols au départ {E(p["au"].replace("en ", "de ").replace("au ", "du "))}</a></li>'
                '<li><a href="/faire-venir-sa-famille/">Faire venir un proche en Europe</a></li><li><a href="/visa/">Faut-il un visa ? (selon votre passeport)</a></li>'
                '<li><a href="/bagages-compagnies-afrique/">Bagages : la franchise de chaque compagnie</a></li><li><a href="/payer-billet-avion-plusieurs-fois/">Payer son billet en plusieurs fois</a></li></ul></section>'
                '<script src="/ete.js" defer></script><script src="/alerts.js" defer></script>')
        title = f"Rentrer {p['au']} en {ANNEE} : les dates et les prix des vols | Escale"
        desc = f"Calendrier des retours {p['au']} en {ANNEE} : Noël, Ramadan, Tabaski, fête nationale, vacances. Pour chaque période, le prix aller-retour repéré depuis Paris et les trajets depuis la France, la Belgique, l'Italie et Londres."
        urls.append(B.write(site, path, "fr", title, desc, hero, body, "", {"fr": path}, ctx))
        index_items.append(f'<li><a href="/{path}/">{p["flag"]} {E(p["nom"])}</a></li>')
    # Page d'index
    hero = ('<p class="eyebrow">Diaspora africaine en Europe</p><h1>Rentrer au pays <span>pour les fêtes</span></h1>'
            f'<p class="hero-lead">Pour chaque communauté, le calendrier {ANNEE} des retours au pays (Noël, Ramadan, Tabaski, fête nationale, été) avec les prix des billets repérés et les trajets existants depuis l\'Europe.</p>')
    body = (f'<section><h2>Choisissez votre pays</h2><ul class="route-links">{"".join(index_items)}</ul></section>'
            '<section><h2>Les dates clés de 2027</h2><ul>'
            '<li><strong>Ramadan</strong> : du 8 février au 9 mars 2027 environ ; <strong>Aïd el-Fitr</strong> vers le 9-10 mars (dates prévues, à confirmer).</li>'
            '<li><strong>Pâques</strong> : dimanche 28 mars 2027.</li>'
            '<li><strong>Tabaski (Aïd el-Kébir)</strong> : vers le 26-27 mai 2027 (date prévue, à confirmer).</li>'
            '<li><strong>Vacances d\'été</strong> en France : début juillet à fin août ; les dates exactes par zone sont sur <a href="https://www.education.gouv.fr/calendrier-scolaire" target="_blank" rel="noopener">education.gouv.fr</a>.</li>'
            '<li><strong>Noël 2027</strong> : les prix de décembre se réservent dès septembre.</li></ul></section>'
            f'<section><h2>Les bons plans chaque semaine</h2>{B.wa_btn("fr")}</section>')
    urls.append(B.write(site, "diaspora", "fr", f"Rentrer au pays en {ANNEE} : dates et prix des vols par pays | Escale",
                        f"Côte d'Ivoire, Sénégal, Mali, Cameroun, Maroc, Algérie… Pour chaque communauté, les dates des retours au pays en {ANNEE} et le prix des billets repéré pour chaque période.",
                        hero, body, "", {"fr": "diaspora"}, ctx))
    return urls
