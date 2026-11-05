"""Pages « voyage » : week-ends pas chers, premier voyage à…, meilleur mois pour partir à… (fr, en).
Aucun prix écrit dans les pages : tout vient en direct des API Escale (/api/weekends, /api/calendar),
depuis l'aéroport du visiteur (site/fetes.js : aéroport choisi sur Escale, sinon le plus proche, sinon Paris)."""
import html
import json

import build_i18n as B

E = html.escape

WE = {
    "fr": dict(path="week-end-pas-cher", title="Week-end pas cher : vols aller-retour à moins de 100 € | Escale",
               desc="Les week-ends aller-retour à moins de 100 € depuis votre aéroport, vendredi ou samedi → dimanche ou lundi, pour les 8 prochaines semaines. Prix réels, mis à jour en continu.",
               h1="Week-end <span>à moins de 100 €</span>", lead="Départ vendredi ou samedi, retour dimanche ou lundi : les destinations les moins chères des 8 prochains week-ends, depuis votre aéroport.",
               from_l="Départ de", budget="Budget aller-retour", loading="Recherche des meilleurs week-ends…",
               none="Aucun week-end trouvé sous ce budget pour l'instant depuis votre aéroport. Essayez un budget plus élevé ou un autre aéroport sur l'accueil.",
               direct="direct", stop="avec escale", change="Changer d'aéroport",
               tips_h="Pour payer encore moins", tips=["Partir le samedi et rentrer le lundi est souvent moins cher que vendredi → dimanche.",
                   "Ces prix sont des tarifs de base, souvent sans bagage en soute : un bagage cabine suffit pour un week-end.",
                   "Les prix changent tous les jours : réservez dès qu'un prix vous plaît, ou créez une alerte prix sur la page du trajet."],
               note="Prix aller-retour trouvés récemment par notre partenaire de recherche (Aviasales), pour les dates affichées. Ils se confirment sur le site de réservation."),
    "en": dict(path="en/cheap-weekends", title="Cheap weekend breaks: round-trip flights under €100 | Escale",
               desc="Round-trip weekend flights under €100 from your airport, Friday or Saturday → Sunday or Monday, for the next 8 weeks. Real prices, updated continuously.",
               h1="Weekend breaks <span>under €100</span>", lead="Leave Friday or Saturday, back Sunday or Monday: the cheapest destinations for the next 8 weekends, from your airport.",
               from_l="Leaving from", budget="Round-trip budget", loading="Finding the best weekends…",
               none="No weekend found under this budget from your airport right now. Try a higher budget or another airport on the home page.",
               direct="direct", stop="with a stop", change="Change airport",
               tips_h="To pay even less", tips=["Leaving Saturday and coming back Monday is often cheaper than Friday → Sunday.",
                   "These are base fares, often without checked luggage: a cabin bag is enough for a weekend.",
                   "Prices change every day: book as soon as a price suits you, or set a price alert on the route page."],
               note="Round-trip prices recently found by our search partner (Aviasales), for the dates shown. They are confirmed on the booking site."),
}


def build_weekends(site, ctx):
    paths = {l: WE[l]["path"] for l in WE}
    urls = []
    for lang, t in WE.items():
        q = "" if lang == "fr" else "?lang=en"
        tj = E(json.dumps({"loading": t["loading"], "none": t["none"], "direct": t["direct"], "stop": t["stop"]}, ensure_ascii=False))
        body = (f'<div class="we-head"><p>{E(t["from_l"])} <strong class="we-from">…</strong> · <a href="/{q}">{E(t["change"])}</a></p>'
                f'<div class="we-budget" role="group" aria-label="{E(t["budget"])}">'
                + "".join(f'<button type="button" data-max="{m}" aria-pressed="{"true" if m == 100 else "false"}">≤ {m} €</button>' for m in (50, 100, 150)) +
                f'</div></div><ul class="we-grid" id="we-list" data-max="100" data-t="{tj}"></ul>'
                f'<section><h2>{E(t["tips_h"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["tips"]) + f'</ul><p class="small">{E(t["note"])}</p></section>'
                '<script src="/fetes.js" defer></script><script src="/weekends.js" defer></script>')
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, "", paths, ctx))
    return urls


def build(site, ctx):
    import premier_voyage
    import meilleur_mois
    import proche
    import outils
    import protection
    import pratiques_pays
    return build_weekends(site, ctx) + premier_voyage.build(site, ctx) + meilleur_mois.build(site, ctx) + proche.build(site, ctx) + outils.build(site, ctx) + protection.build(site, ctx) + pratiques_pays.build(site, ctx)  # agences.build(site, ctx) : à réactiver plus tard (« Escale pour les agences »)
