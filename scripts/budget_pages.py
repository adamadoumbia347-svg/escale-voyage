"""Pages « Où partir avec 100 / 200 / 300 / 500 € ? » (fr, en, it, de).
Aucun prix écrit dans les pages : site/budget.js interroge /api/explore (les 3 prochains mois) depuis l'aéroport
du visiteur (site/fetes.js) et n'affiche que les allers-retours sous le budget de la page."""
import html
import json

import build_i18n as B

E = html.escape
BUDGETS = (100, 200, 300, 500)

PATH = {
    "fr": "ou-partir-avec-{n}-euros",
    "en": "en/where-to-go-for-{n}-euros",
    "it": "it/dove-andare-con-{n}-euro",
    "de": "de/wohin-reisen-mit-{n}-euro",
}

T = {
    "fr": dict(
        title="Où partir avec {n} € ? Vols aller-retour pas chers | Escale",
        desc="Où partir avec {n} € aller-retour depuis votre aéroport : les destinations sous {n} € des 3 prochains mois, avec de vrais prix mis à jour en continu.",
        h1="Où partir avec <span>{n} €</span> ?",
        lead="Toutes les destinations où l'aller-retour coûte {n} € ou moins depuis votre aéroport, pour les 3 prochains mois. Les prix sont réels et changent chaque jour.",
        from_l="Départ de", change="Changer d'aéroport", other="Autre budget",
        map="Voir sur la carte du monde →", loading="Recherche des destinations sous votre budget…",
        none="Aucun aller-retour sous {n} € trouvé pour l'instant depuis votre aéroport. Essayez un budget plus élevé ou un autre aéroport.",
        count="{c} destinations à {n} € ou moins", direct="direct", stop="avec escale",
        tips_h="Pour que {n} € suffisent",
        tips=["Ces prix sont des tarifs de base, souvent sans bagage en soute : voyager avec un bagage cabine évite les frais en plus.",
              "Les dates sont souples ? Ouvrez le calendrier des prix sur la page du trajet pour trouver le jour le moins cher.",
              "Pensez au trajet jusqu'à l'aéroport d'arrivée : certains aéroports bon marché sont loin du centre-ville.",
              "Les prix changent tous les jours : réservez dès qu'un prix vous plaît, ou créez une alerte prix."],
        note="Prix aller-retour trouvés récemment par notre partenaire de recherche (Aviasales), pour les dates affichées. Ils se confirment sur le site de réservation."),
    "en": dict(
        title="Where to go for €{n}? Cheap round-trip flights | Escale",
        desc="Where to go for €{n} round trip from your airport: every destination under €{n} for the next 3 months, with real prices updated continuously.",
        h1="Where to go <span>for €{n}</span>?",
        lead="Every destination where a round trip costs €{n} or less from your airport, over the next 3 months. Prices are real and change every day.",
        from_l="Leaving from", change="Change airport", other="Other budget",
        map="See it on the world map →", loading="Finding destinations within your budget…",
        none="No round trip under €{n} found from your airport right now. Try a higher budget or another airport.",
        count="{c} destinations for €{n} or less", direct="direct", stop="with a stop",
        tips_h="Making €{n} go further",
        tips=["These are base fares, often without checked luggage: travelling with a cabin bag avoids extra fees.",
              "Flexible dates? Open the price calendar on the route page to find the cheapest day.",
              "Think about getting into town: some low-cost airports are far from the city centre.",
              "Prices change every day: book as soon as a price suits you, or set a price alert."],
        note="Round-trip prices recently found by our search partner (Aviasales), for the dates shown. They are confirmed on the booking site."),
    "it": dict(
        title="Dove andare con {n} €? Voli andata e ritorno economici | Escale",
        desc="Dove andare con {n} € andata e ritorno dal tuo aeroporto: tutte le destinazioni sotto i {n} € dei prossimi 3 mesi, con prezzi reali aggiornati di continuo.",
        h1="Dove andare <span>con {n} €</span>?",
        lead="Tutte le destinazioni dove l'andata e ritorno costa {n} € o meno dal tuo aeroporto, nei prossimi 3 mesi. I prezzi sono reali e cambiano ogni giorno.",
        from_l="Partenza da", change="Cambia aeroporto", other="Altro budget",
        map="Vedi sulla mappa del mondo →", loading="Ricerca delle destinazioni nel tuo budget…",
        none="Nessun andata e ritorno sotto i {n} € dal tuo aeroporto per ora. Prova un budget più alto o un altro aeroporto.",
        count="{c} destinazioni a {n} € o meno", direct="diretto", stop="con scalo",
        tips_h="Per far bastare {n} €",
        tips=["Questi prezzi sono tariffe base, spesso senza bagaglio in stiva: viaggiare con il solo bagaglio a mano evita costi extra.",
              "Date flessibili? Apri il calendario prezzi nella pagina della tratta per trovare il giorno più economico.",
              "Pensa al tragitto verso il centro: alcuni aeroporti low cost sono lontani dalla città.",
              "I prezzi cambiano ogni giorno: prenota appena un prezzo ti piace, o crea un avviso prezzo."],
        note="Prezzi andata e ritorno trovati di recente dal nostro partner di ricerca (Aviasales), per le date indicate. Vengono confermati sul sito di prenotazione."),
    "de": dict(
        title="Wohin reisen mit {n} €? Günstige Hin- und Rückflüge | Escale",
        desc="Wohin mit {n} € hin und zurück ab deinem Flughafen: alle Ziele unter {n} € in den nächsten 3 Monaten, mit echten, laufend aktualisierten Preisen.",
        h1="Wohin reisen <span>mit {n} €</span>?",
        lead="Alle Ziele, bei denen Hin- und Rückflug ab deinem Flughafen {n} € oder weniger kosten, in den nächsten 3 Monaten. Die Preise sind echt und ändern sich täglich.",
        from_l="Abflug ab", change="Flughafen ändern", other="Anderes Budget",
        map="Auf der Weltkarte ansehen →", loading="Ziele in deinem Budget werden gesucht…",
        none="Gerade kein Hin- und Rückflug unter {n} € ab deinem Flughafen. Versuche ein höheres Budget oder einen anderen Flughafen.",
        count="{c} Ziele für {n} € oder weniger", direct="direkt", stop="mit Umstieg",
        tips_h="Damit {n} € reichen",
        tips=["Das sind Basistarife, oft ohne Aufgabegepäck: Mit Handgepäck vermeidest du Zusatzkosten.",
              "Flexible Daten? Öffne den Preiskalender auf der Streckenseite, um den günstigsten Tag zu finden.",
              "Denk an den Weg in die Stadt: Manche Billigflughäfen liegen weit vom Zentrum entfernt.",
              "Die Preise ändern sich täglich: Buche, sobald dir ein Preis gefällt, oder richte einen Preisalarm ein."],
        note="Hin- und Rückflugpreise, kürzlich von unserem Suchpartner (Aviasales) gefunden, für die angezeigten Daten. Sie werden auf der Buchungsseite bestätigt."),
}

# La carte n'existe qu'en fr/en/es/pt/ar : l'italien et l'allemand vont vers la version anglaise
PARTOUT = {"fr": "/partout/", "en": "/en/anywhere/", "it": "/en/anywhere/", "de": "/en/anywhere/"}


def path(lang, n):
    return PATH[lang].format(n=n)


def build(site, ctx):
    urls = []
    for n in BUDGETS:
        paths = {l: path(l, n) for l in PATH}
        for lang, t in T.items():
            f = lambda s: s.format(n=n)  # noqa: E731
            q = "" if lang == "fr" else f"?lang={lang}"
            tj = E(json.dumps({"loading": f(t["loading"]), "none": f(t["none"]), "count": t["count"].replace("{n}", str(n)),
                               "direct": t["direct"], "stop": t["stop"]}, ensure_ascii=False))
            chips = "".join(
                f'<a href="/{path(lang, m)}/" aria-current="{"page" if m == n else "false"}">≤ {m} €</a>' for m in BUDGETS)
            sep = "&" if "?" in PARTOUT[lang] else "?"
            body = (f'<div class="we-head"><p>{E(t["from_l"])} <strong class="we-from">…</strong> · <a href="/{q}">{E(t["change"])}</a></p>'
                    f'<nav class="bu-chips" aria-label="{E(t["other"])}">{chips}</nav></div>'
                    f'<p class="small bu-count" id="bu-count" role="status"></p>'
                    f'<ul class="we-grid" id="bu-list" data-max="{n}" data-t="{tj}"></ul>'
                    f'<p><a class="see-all" href="{PARTOUT[lang]}{sep}max={n}">{E(t["map"])}</a></p>'
                    f'<section><h2>{E(f(t["tips_h"]))}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["tips"]) +
                    f'</ul><p class="small">{E(t["note"])}</p></section>'
                    '<script src="/fetes.js" defer></script><script src="/budget.js" defer></script>')
            hero = f'<h1>{f(t["h1"])}</h1><p class="hero-lead">{E(f(t["lead"]))}</p>'
            urls.append(B.write(site, path(lang, n), lang, f(t["title"]), f(t["desc"]), hero, body, "", paths, ctx))
    return urls
