"""CAN 2027 (Coupe d'Afrique des nations, co-organisée par le Kenya, l'Ouganda et la Tanzanie) : page d'ensemble + une page par ville
hôte, en français (/can-2027/…) et en anglais (/en/afcon-2027/…). Prix aller-retour repérés depuis Paris, Bruxelles, Milan, Rome,
Londres (chargés par site/ete.js depuis /api/prix, comme les pages été), visa et santé avec liens officiels, conseils.
Dates et stades : la CAF n'a pas tout officialisé au moment de l'écriture ; la page le dit et renvoie vers cafonline.com."""
import html

import build_i18n as B

E = html.escape
DEP, RET = "2027-06", "2027-07"           # mois de recherche (la compétition est prévue à l'été 2027)
D1, D2 = "2027-06-18", "2027-07-20"       # dates proposées dans les liens « Voir les vols »
DEPARTS = [("CDG", "Paris", "Paris"), ("BRU", "Bruxelles", "Brussels"), ("MXP", "Milan", "Milan"), ("FCO", "Rome", "Rome"), ("LHR", "Londres", "London")]

VILLES = [
    dict(slug="nairobi", en="nairobi", ville="Nairobi", pays=("Kenya", "Kenya"), flag="🇰🇪", code="NBO",
         visa=("La plupart des voyageurs doivent obtenir une autorisation électronique (eTA) avant le départ, en ligne. Vérifiez votre cas sur le site officiel.",
               "Most visitors need an electronic travel authorisation (eTA) before departure, online. Check your case on the official site."),
         visa_url="https://www.etakenya.go.ke/",
         sante=("Certificat de vaccination contre la fièvre jaune demandé selon votre provenance et votre itinéraire ; traitement antipaludique conseillé selon les zones. Parlez-en à votre médecin.",
                "Yellow fever certificate requested depending on where you come from and your route; antimalarial treatment advised depending on the areas. Ask your doctor."),
         infos=("Capitale du Kenya, hub d'Afrique de l'Est : nombreux vols directs ou avec une escale depuis l'Europe (Paris, Londres, Amsterdam, via Addis-Abeba, Istanbul ou le Golfe). Juin-juillet correspond à la saison fraîche et sèche.",
                "Kenya's capital and East Africa's hub: many direct or one-stop flights from Europe (Paris, London, Amsterdam, via Addis Ababa, Istanbul or the Gulf). June–July is the cool, dry season.")),
    dict(slug="kampala", en="kampala", ville="Kampala", pays=("Ouganda", "Uganda"), flag="🇺🇬", code="EBB",
         visa=("Visa électronique à demander en ligne avant le départ pour la plupart des nationalités. Vérifiez votre cas sur le site officiel.",
               "Electronic visa to apply for online before departure for most nationalities. Check your case on the official site."),
         visa_url="https://visas.immigration.go.ug/",
         sante=("Le certificat de vaccination contre la fièvre jaune est en général exigé à l'arrivée en Ouganda ; traitement antipaludique conseillé. Parlez-en à votre médecin.",
                "A yellow fever vaccination certificate is generally required on arrival in Uganda; antimalarial treatment advised. Ask your doctor."),
         infos=("L'aéroport est à Entebbe (EBB), à environ 40 km de Kampala : prévoyez le trajet. Vols depuis l'Europe surtout avec une escale (Addis-Abeba, Nairobi, Istanbul, Golfe, Bruxelles en direct selon la saison).",
                "The airport is in Entebbe (EBB), about 40 km from Kampala: plan the transfer. Flights from Europe mostly with one stop (Addis Ababa, Nairobi, Istanbul, the Gulf; Brussels direct depending on the season).")),
    dict(slug="dar-es-salaam", en="dar-es-salaam", ville="Dar es Salaam", pays=("Tanzanie", "Tanzania"), flag="🇹🇿", code="DAR",
         visa=("Visa électronique à demander en ligne avant le départ pour la plupart des nationalités (le visa à l'arrivée existe pour certaines). Vérifiez votre cas sur le site officiel.",
               "Electronic visa to apply for online before departure for most nationalities (visa on arrival exists for some). Check your case on the official site."),
         visa_url="https://visa.immigration.go.tz/",
         sante=("Certificat de fièvre jaune demandé selon votre provenance ; traitement antipaludique conseillé. Parlez-en à votre médecin.",
                "Yellow fever certificate requested depending on where you come from; antimalarial treatment advised. Ask your doctor."),
         infos=("Plus grande ville de Tanzanie, sur l'océan Indien. Vols depuis l'Europe avec une escale le plus souvent (Addis-Abeba, Nairobi, Istanbul, Golfe) ; saison sèche en juin-juillet.",
                "Tanzania's largest city, on the Indian Ocean. Flights from Europe mostly with one stop (Addis Ababa, Nairobi, Istanbul, the Gulf); dry season in June–July.")),
    dict(slug="arusha", en="arusha", ville="Arusha", pays=("Tanzanie", "Tanzania"), flag="🇹🇿", code="JRO",
         visa=("Mêmes règles que pour Dar es Salaam : visa électronique en ligne pour la plupart des nationalités. Vérifiez votre cas sur le site officiel.",
               "Same rules as Dar es Salaam: electronic visa online for most nationalities. Check your case on the official site."),
         visa_url="https://visa.immigration.go.tz/",
         sante=("Certificat de fièvre jaune demandé selon votre provenance ; traitement antipaludique conseillé. Parlez-en à votre médecin.",
                "Yellow fever certificate requested depending on where you come from; antimalarial treatment advised. Ask your doctor."),
         infos=("L'aéroport du Kilimandjaro (JRO) dessert Arusha, porte des safaris du nord de la Tanzanie. Vols depuis l'Europe via Addis-Abeba, Nairobi, Amsterdam, Istanbul ou le Golfe selon la saison.",
                "Kilimanjaro airport (JRO) serves Arusha, the gateway to northern Tanzania's safaris. Flights from Europe via Addis Ababa, Nairobi, Amsterdam, Istanbul or the Gulf depending on the season.")),
]

T = {
    "fr": dict(base="can-2027", eyebrow="CAN 2027 · Kenya, Ouganda, Tanzanie", h1="Vols pour la <span>CAN 2027</span>", title="Vols pour la CAN 2027 (Kenya, Ouganda, Tanzanie) : prix et conseils | Escale",
               desc="Coupe d'Afrique des nations 2027 au Kenya, en Ouganda et en Tanzanie : les prix des vols repérés vers Nairobi, Kampala, Dar es Salaam et Arusha, le visa, la santé et quand réserver.",
               lead="La Coupe d'Afrique des nations 2027 se joue dans trois pays d'Afrique de l'Est. Voici les prix des vols repérés depuis l'Europe vers chaque ville hôte, ce qu'il faut pour entrer et quand réserver.",
               warn="Dates, stades et calendrier des matchs : la Confédération africaine de football publie les informations officielles sur cafonline.com. Cette page suit une compétition prévue à l'été 2027 ; les prix affichés portent sur juin-juillet 2027.",
               cities="Les villes hôtes", prices="Prix repérés pour juin-juillet 2027", th=("Trajet", "Prix repéré", ""), go="Voir les vols",
               note="Prix aller-retour le plus bas repéré récemment, par personne, pour le mois choisi (juin → juillet 2027). Les dates affichées sont celles du vol trouvé ; le tarif exact se confirme sur le site de réservation. S'il n'y a pas encore de prix, les compagnies n'ont pas encore ouvert ces dates : créez une alerte.",
               visa="Visa et entrée", sante="Santé", infos="Bon à savoir", official="Site officiel ↗", when="Quand réserver ?",
               when_txt=["Les compagnies ouvrent en général leurs réservations 10 à 11 mois à l'avance : les vols de juin-juillet 2027 arrivent progressivement.",
                         "Pour un grand événement, les prix montent dès que le calendrier des matchs est connu et que les supporters réservent. Les tarifs les plus bas se trouvent souvent 4 à 6 mois avant.",
                         "Comparez un arrivée dans une ville et un retour depuis une autre (Nairobi → Dar es Salaam par exemple) : les trois pays sont voisins et bien reliés.",
                         "Créez une alerte prix sur le trajet qui vous intéresse : vous serez prévenu dès qu'un tarif baisse."],
               multi="Plusieurs villes, un seul voyage", multi_txt="Nairobi, Kampala et Dar es Salaam sont reliées par des vols régionaux (Kenya Airways, Uganda Airlines, Air Tanzania, Precision Air…) et par la route. Comparez les vols intra-africains sur Escale avant de décider dans quelle ville atterrir.",
               h1_city="Vols pour <span>{v}</span> · CAN 2027", title_city="Vol pour {v} pendant la CAN 2027 : prix, visa, conseils | Escale",
               desc_city="Coupe d'Afrique des nations 2027 à {v} ({p}) : prix des vols repérés depuis Paris, Bruxelles, Milan, Rome et Londres, visa électronique, santé, et quand réserver.",
               lead_city="{v} accueille des matchs de la CAN 2027. Les prix des vols repérés depuis l'Europe pour juin-juillet 2027, et ce qu'il faut savoir avant de partir.",
               other="Les autres villes hôtes", back="Toute la CAN 2027", wa="Partager dans un groupe de supporters"),
    "en": dict(base="en/afcon-2027", eyebrow="AFCON 2027 · Kenya, Uganda, Tanzania", h1="Flights for <span>AFCON 2027</span>", title="Flights for AFCON 2027 (Kenya, Uganda, Tanzania): fares and tips | Escale",
               desc="Africa Cup of Nations 2027 in Kenya, Uganda and Tanzania: fares found to Nairobi, Kampala, Dar es Salaam and Arusha, visas, health and when to book.",
               lead="The 2027 Africa Cup of Nations is played in three East African countries. Here are the fares found from Europe to each host city, what you need to enter, and when to book.",
               warn="Dates, stadiums and match schedule: the Confederation of African Football publishes official information on cafonline.com. This page follows a tournament planned for summer 2027; fares shown are for June–July 2027.",
               cities="Host cities", prices="Fares found for June–July 2027", th=("Route", "Fare found", ""), go="See flights",
               note="Lowest round-trip fare found recently, per person, for the chosen month (June → July 2027). Dates shown are those of the flight found; the exact fare is confirmed on the booking site. If there is no fare yet, airlines have not opened these dates: set an alert.",
               visa="Visa and entry", sante="Health", infos="Good to know", official="Official site ↗", when="When to book?",
               when_txt=["Airlines usually open bookings 10 to 11 months ahead: June–July 2027 flights are appearing gradually.",
                         "For a major event, fares rise as soon as the match schedule is known and fans start booking. The lowest fares are often found 4 to 6 months ahead.",
                         "Compare arriving in one city and returning from another (Nairobi → Dar es Salaam for instance): the three countries are neighbours and well connected.",
                         "Set a price alert on the route you want: you will be told as soon as a fare drops."],
               multi="Several cities, one trip", multi_txt="Nairobi, Kampala and Dar es Salaam are linked by regional flights (Kenya Airways, Uganda Airlines, Air Tanzania, Precision Air…) and by road. Compare intra-African flights on Escale before choosing where to land.",
               h1_city="Flights to <span>{v}</span> · AFCON 2027", title_city="Flights to {v} for AFCON 2027: fares, visa, tips | Escale",
               desc_city="Africa Cup of Nations 2027 in {v} ({p}): fares found from Paris, Brussels, Milan, Rome and London, e-visa, health, and when to book.",
               lead_city="{v} hosts AFCON 2027 matches. Fares found from Europe for June–July 2027, and what to know before you go.",
               other="Other host cities", back="All of AFCON 2027", wa="Share with your supporters' group"),
}


def _rows(code, lang):
    k = 2 if lang == "en" else 1
    return "".join(
        f'<tr data-from="{o}" data-to="{code}" data-dep="{DEP}" data-ret="{RET}"><th scope="row">{E(DEPARTS[i][k])} → {{v}}</th>'
        f'<td class="fp" aria-live="polite">…</td><td><a class="price-go" href="/?type=vols&amp;from={o}&amp;to={code}&amp;dep={D1}&amp;ret={D2}{"&amp;lang=en" if lang == "en" else ""}">{{go}}</a></td></tr>'
        for i, (o, _, _) in enumerate(DEPARTS))


def build(site, ctx):
    urls = []
    for lang, t in T.items():
        li = 1 if lang == "en" else 0
        thead = f'<thead><tr><th scope="col">{E(t["th"][0])}</th><th scope="col">{E(t["th"][1])}</th><th scope="col"><span class="sr-only">{E(t["go"])}</span></th></tr></thead>'
        # pages ville
        for v in VILLES:
            path = f'{t["base"]}/{v["slug"]}'
            paths = {"fr": f'can-2027/{v["slug"]}', "en": f'en/afcon-2027/{v["en"]}'}
            rows = _rows(v["code"], lang).replace("{v}", E(v["ville"])).replace("{go}", E(t["go"]))
            others = "".join(f'<li><a href="/{t["base"]}/{o["slug"]}/">{o["flag"]} {E(o["ville"])}</a></li>' for o in VILLES if o is not v)
            hero = (f'<p class="eyebrow">{v["flag"]} {E(t["eyebrow"])}</p><h1>{t["h1_city"].format(v=E(v["ville"]))}</h1>'
                    f'<p class="hero-lead">{E(t["lead_city"].format(v=v["ville"]))}</p><p class="hero-price" id="hero-price" hidden></p>'
                    f'<div class="cta-row"><a class="btn" href="/?type=vols&amp;from=CDG&amp;to={v["code"]}&amp;dep={D1}&amp;ret={D2}{"&amp;lang=en" if lang == "en" else ""}">{E(t["go"])}</a>{B.alert_btn(lang)}</div>')
            body = (f'<section><p class="small">{E(t["warn"])}</p></section>'
                    f'<section><h2>{E(t["prices"])}</h2><table class="fete-table ete-table" data-hero="CDG">{thead}<tbody>{rows}</tbody></table><p class="small">{E(t["note"])}</p></section>'
                    f'<section id="price-alert" class="price-alert" data-from="CDG" data-to="{v["code"]}" hidden></section>'
                    f'<section><h2>{E(t["visa"])}</h2><p>{E(v["visa"][li])} <a href="{E(v["visa_url"])}" target="_blank" rel="noopener nofollow">{E(t["official"])}</a></p></section>'
                    f'<section><h2>{E(t["sante"])}</h2><p>{E(v["sante"][li])}</p></section>'
                    f'<section><h2>{E(t["infos"])}</h2><p>{E(v["infos"][li])}</p></section>'
                    f'<section><h2>{E(t["when"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["when_txt"]) + "</ul></section>"
                    f'<section><h2>{E(t["other"])}</h2><ul class="route-links">{others}<li><a href="/{t["base"]}/">{E(t["back"])}</a></li></ul></section>'
                    + B.wa_btn(lang) + '<script src="/ete.js" defer></script><script src="/alerts.js" defer></script>')
            urls.append(B.write(site, path, lang, t["title_city"].format(v=v["ville"]), t["desc_city"].format(v=v["ville"], p=v["pays"][li]), hero, body, "", paths, ctx))
        # page d'ensemble
        cards = "".join(f'<li><a href="/{t["base"]}/{v["slug"]}/"><strong>{v["flag"]} {E(v["ville"])}</strong> · {E(v["pays"][li])} · {v["code"]}</a></li>' for v in VILLES)
        rows_all = "".join(_rows(v["code"], lang).replace("{v}", E(v["ville"])).replace("{go}", E(t["go"])) for v in VILLES[:3])
        hero = f'<p class="eyebrow">🏆 {E(t["eyebrow"])}</p><h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        body = (f'<section><p class="small">{E(t["warn"])}</p></section>'
                f'<section><h2>{E(t["cities"])}</h2><ul class="route-links can-cities">{cards}</ul></section>'
                f'<section><h2>{E(t["prices"])}</h2><table class="fete-table ete-table" data-hero="CDG">{thead}<tbody>{rows_all}</tbody></table><p class="small">{E(t["note"])}</p></section>'
                f'<section><h2>{E(t["when"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["when_txt"]) + "</ul></section>"
                f'<section><h2>{E(t["multi"])}</h2><p>{E(t["multi_txt"])}</p></section>'
                + B.wa_btn(lang) + '<script src="/ete.js" defer></script>')
        urls.append(B.write(site, t["base"], lang, t["title"], t["desc"], hero, body, "", {"fr": "can-2027", "en": "en/afcon-2027"}, ctx))
    return urls
