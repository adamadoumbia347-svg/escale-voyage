"""Calendrier des grands événements africains (/evenements/…) : pour chaque événement, la période, la ville, le prix aller-retour
repéré depuis Paris, Bruxelles, Milan, Rome et Londres pour le mois concerné (site/ete.js via /api/prix), et des repères pratiques.
Les dates précises changent chaque année (et certaines suivent la lune) : la page donne la période habituelle et renvoie vers
l'organisateur. Aucune date présentée comme certaine sans source officielle."""
import html
import urllib.parse

import build_i18n as B

E = html.escape
DEPARTS = [("CDG", "Paris"), ("BRU", "Bruxelles"), ("MXP", "Milan"), ("FCO", "Rome"), ("LHR", "Londres")]
# slug, nom, ville, pays, drapeau, aéroport, mois de recherche (dep, ret), dates proposées (d1, d2), période habituelle, description, conseils, site
EVTS = [
    dict(slug="fete-du-vodoun-ouidah", nom="Fête du Vodoun à Ouidah", ville="Ouidah (via Cotonou)", pays="Bénin", flag="🇧🇯", code="COO", dep="2027-01", ret="2027-01", d1="2027-01-07", d2="2027-01-14",
         periode="Chaque année le 10 janvier (jour férié au Bénin).",
         desc="Le 10 janvier, le Bénin célèbre les religions traditionnelles : cérémonies, danses masquées et processions sur la plage de Ouidah, à une heure de Cotonou. Une des fêtes les plus photographiées d'Afrique de l'Ouest.",
         conseils=["Réservez l'hébergement à Ouidah ou Cotonou dès novembre : la demande est forte autour du 10 janvier.", "Janvier est en pleine saison sèche : chaleur, harmattan possible.", "Arrivée à Cotonou (COO) ; Ouidah est à environ 40 km à l'ouest."],
         site="https://www.benin-tourisme.com/"),
    dict(slug="festival-sur-le-niger-segou", nom="Festival sur le Niger à Ségou", ville="Ségou (via Bamako)", pays="Mali", flag="🇲🇱", code="BKO", dep="2027-02", ret="2027-02", d1="2027-02-01", d2="2027-02-09",
         periode="Début février, chaque année (dates publiées par le festival).",
         desc="Musique, arts et culture au bord du fleuve Niger, à Ségou, à environ 240 km de Bamako. L'un des grands rendez-vous culturels du Sahel.",
         conseils=["Vérifiez les dates et l'édition de l'année sur le site du festival avant de réserver.", "Février est agréable : chaud le jour, frais la nuit.", "Arrivée à Bamako (BKO), puis route vers Ségou ; renseignez-vous sur les conditions de déplacement auprès des conseils aux voyageurs."],
         site="https://www.festivalsegou.org/"),
    dict(slug="fespaco-ouagadougou", nom="FESPACO à Ouagadougou", ville="Ouagadougou", pays="Burkina Faso", flag="🇧🇫", code="OUA", dep="2027-02", ret="2027-03", d1="2027-02-26", d2="2027-03-07",
         periode="Festival panafricain du cinéma, tous les deux ans (années impaires), fin février – début mars. Édition prévue en 2027 : dates à confirmer par le FESPACO.",
         desc="Le plus grand festival de cinéma d'Afrique réunit à Ouagadougou réalisateurs, acteurs et public de tout le continent pendant une semaine.",
         conseils=["Les hôtels de Ouagadougou se remplissent vite pendant le festival : réservez tôt.", "Consultez les conseils aux voyageurs de votre pays avant de partir.", "Vols depuis l'Europe surtout via Casablanca, Abidjan, Istanbul ou Addis-Abeba."],
         site="https://fespaco.org/"),
    dict(slug="femua-abidjan", nom="FEMUA à Abidjan", ville="Abidjan", pays="Côte d'Ivoire", flag="🇨🇮", code="ABJ", dep="2027-04", ret="2027-05", d1="2027-04-20", d2="2027-05-04",
         periode="Généralement entre avril et mai ; les dates exactes sont annoncées par le festival chaque année.",
         desc="Le Festival des musiques urbaines d'Anoumabo, à Abidjan, mêle grands concerts gratuits, actions sociales et ambiance de quartier. Un rendez-vous de la jeunesse ivoirienne et de la diaspora.",
         conseils=["Les dates bougent d'une année à l'autre : vérifiez avant d'acheter votre billet.", "Avril-mai : fin de la grande saison sèche, premières pluies possibles.", "Abidjan est très bien desservie depuis Paris, Bruxelles, Milan et Rome."],
         site="https://www.femua.com/"),
    dict(slug="gnaoua-essaouira", nom="Festival Gnaoua à Essaouira", ville="Essaouira (via Marrakech)", pays="Maroc", flag="🇲🇦", code="RAK", dep="2027-06", ret="2027-06", d1="2027-06-17", d2="2027-06-24",
         periode="En juin, chaque année (dates publiées par le festival).",
         desc="Musiques gnaoua et rencontres avec des artistes du monde entier, dans la ville fortifiée d'Essaouira, au bord de l'Atlantique.",
         conseils=["Essaouira est à environ 3 heures de route de Marrakech (RAK) ; des bus et navettes existent.", "Réservez l'hébergement à Essaouira dès que les dates sont connues.", "Juin est doux et venté à Essaouira, plus chaud à Marrakech."],
         site="https://www.festival-gnaoua.net/"),
    dict(slug="mawazine-rabat", nom="Mawazine à Rabat", ville="Rabat (via Casablanca)", pays="Maroc", flag="🇲🇦", code="CMN", dep="2027-06", ret="2027-06", d1="2027-06-18", d2="2027-06-27",
         periode="Fin juin en général ; dates annoncées par les organisateurs.",
         desc="L'un des plus grands festivals de musique du monde par la fréquentation : stars internationales et artistes marocains sur plusieurs scènes à Rabat.",
         conseils=["Rabat est à moins d'une heure de train de l'aéroport de Casablanca (CMN) ; Rabat-Salé (RBA) a aussi des vols depuis la France.", "Hôtels très demandés pendant le festival.", "Vérifiez la programmation et les dates sur le site officiel."],
         site="https://www.mawazine.ma/"),
    dict(slug="grand-magal-de-touba", nom="Grand Magal de Touba", ville="Touba (via Dakar)", pays="Sénégal", flag="🇸🇳", code="DSS", dep="2027-08", ret="2027-09", d1="2027-08-16", d2="2027-08-30",
         periode="Date religieuse (18 Safar du calendrier musulman) : elle avance d'environ 11 jours chaque année. Pour 2027, prévue vers la fin août ; à confirmer.",
         desc="Le plus grand pèlerinage du Sénégal rassemble des millions de fidèles mourides à Touba. Depuis la diaspora, c'est l'un des grands moments de retour au pays.",
         conseils=["La date exacte se confirme quelques semaines avant : surveillez les annonces officielles et réservez un billet modifiable si possible.", "Les vols vers Dakar sont très demandés la semaine du Magal : réservez plusieurs mois avant.", "Touba est à environ 190 km de Dakar ; la route est très chargée les jours du Magal."],
         site=""),
    dict(slug="carnaval-de-calabar", nom="Carnaval de Calabar", ville="Calabar (via Lagos)", pays="Nigeria", flag="🇳🇬", code="LOS", dep="2026-12", ret="2026-12", d1="2026-12-20", d2="2026-12-30",
         periode="Tout le mois de décembre, avec le grand défilé autour du 26-28 décembre.",
         desc="Surnommé « la plus grande fête de rue d'Afrique », le carnaval de Calabar réunit défilés costumés, musique et concerts pendant tout le mois de décembre.",
         conseils=["Décembre est la période la plus chère pour voler vers le Nigeria : réservez tôt.", "Calabar a un aéroport (CBQ) desservi depuis Lagos et Abuja ; comparez un vol international vers Lagos + un vol intérieur.", "Vérifiez les formalités de visa du Nigeria pour votre nationalité (visa à l'arrivée pour certains, e-visa pour d'autres)."],
         site="https://www.carnivalcalabar.com/"),
]


def build(site, ctx):
    urls, items = [], []
    thead = '<thead><tr><th scope="col">Trajet</th><th scope="col">Prix repéré</th><th scope="col"><span class="sr-only">Voir</span></th></tr></thead>'
    for ev in EVTS:
        path = f'evenements/{ev["slug"]}'
        url = f"{ctx['domain']}/{path}/"
        rows = "".join(
            f'<tr data-from="{o}" data-to="{ev["code"]}" data-dep="{ev["dep"]}" data-ret="{ev["ret"]}"><th scope="row">{E(c)} → {E(ev["ville"].split(" (")[0])}</th>'
            f'<td class="fp" aria-live="polite">…</td><td><a class="price-go" href="/?type=vols&amp;from={o}&amp;to={ev["code"]}&amp;dep={ev["d1"]}&amp;ret={ev["d2"]}">Voir les vols</a></td></tr>'
            for o, c in DEPARTS)
        wa = "https://wa.me/?text=" + urllib.parse.quote(f"{ev['nom']} : les prix des vols et les infos pratiques → {url}")
        hero = (f'<p class="eyebrow">{ev["flag"]} {E(ev["pays"])} · événement</p><h1>{E(ev["nom"])} <span>: y aller</span></h1>'
                f'<p class="hero-lead">{E(ev["desc"])}</p><p class="hero-price" id="hero-price" hidden></p>'
                f'<div class="cta-row"><a class="btn" href="/?type=vols&amp;from=CDG&amp;to={ev["code"]}&amp;dep={ev["d1"]}&amp;ret={ev["d2"]}">Comparer les vols</a>'
                f'<a class="btn ghost" href="{E(wa)}" target="_blank" rel="noopener">📲 Partager</a></div>')
        body = (f'<section><h2>Quand ?</h2><p>{E(ev["periode"])}' + (f' <a href="{E(ev["site"])}" target="_blank" rel="noopener nofollow">Site de l\'événement ↗</a>' if ev["site"] else "") + '</p></section>'
                f'<section><h2>Prix des vols repérés pour la période</h2><table class="fete-table ete-table" data-hero="CDG">{thead}<tbody>{rows}</tbody></table>'
                '<p class="small">Prix aller-retour le plus bas repéré récemment, par personne, pour le mois de l\'événement. Les dates affichées sont celles du vol trouvé ; le tarif exact se confirme sur le site de réservation. S\'il n\'y a pas encore de prix, créez une alerte.</p></section>'
                f'<section id="price-alert" class="price-alert" data-from="CDG" data-to="{ev["code"]}" hidden></section>'
                '<section><h2>Conseils</h2><ul>' + "".join(f"<li>{E(c)}</li>" for c in ev["conseils"]) + "</ul></section>"
                '<section><h2>Les autres événements</h2><ul class="route-links">' + "".join(f'<li><a href="/evenements/{o["slug"]}/">{o["flag"]} {E(o["nom"])}</a></li>' for o in EVTS if o is not ev) + '<li><a href="/evenements/">Tout le calendrier</a></li></ul></section>'
                + B.wa_btn("fr") + '<script src="/ete.js" defer></script><script src="/alerts.js" defer></script>')
        title = f"{ev['nom']} : vols, dates et conseils | Escale"
        desc = f"{ev['nom']} ({ev['pays']}) : la période, les prix des vols repérés depuis Paris, Bruxelles, Milan, Rome et Londres, et les conseils pratiques pour y aller."
        urls.append(B.write(site, path, "fr", title, desc, hero, body, "", {"fr": path}, ctx))
        items.append(f'<li><a href="/evenements/{ev["slug"]}/"><strong>{ev["flag"]} {E(ev["nom"])}</strong><br><span class="small">{E(ev["periode"].split(".")[0])}.</span></a></li>')
    hero = ('<p class="eyebrow">Afrique · culture et fêtes</p><h1>Les grands événements <span>africains</span></h1>'
            '<p class="hero-lead">Festivals, carnavals, pèlerinages et fêtes populaires : la période de chacun, et les prix des vols repérés pour y aller depuis l\'Europe.</p>')
    body = (f'<section><ul class="pf-list">{"".join(items)}</ul></section>'
            '<section><h2>Et aussi</h2><ul><li><a href="/can-2027/">🏆 Vols pour la CAN 2027</a> (Kenya, Ouganda, Tanzanie)</li><li><a href="/diaspora/">🎉 Rentrer au pays pour les fêtes : Noël, Tabaski, Aïd, par communauté</a></li><li><a href="/vols-hajj-omra/">🕋 Hajj et Omra</a></li></ul></section>'
            '<p class="small">Les dates changent chaque année et certaines suivent le calendrier lunaire : vérifiez toujours auprès de l\'organisateur avant de réserver.</p>' + B.wa_btn("fr"))
    urls.append(B.write(site, "evenements", "fr", "Les grands événements africains : dates et prix des vols | Escale",
                        "FEMUA, FESPACO, Festival sur le Niger, Gnaoua, Mawazine, Grand Magal de Touba, Fête du Vodoun, Carnaval de Calabar : la période de chaque événement et les prix des vols repérés pour y aller.",
                        hero, body, "", {"fr": "evenements"}, ctx))
    return urls
