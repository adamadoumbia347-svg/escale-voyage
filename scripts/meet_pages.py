"""Page « On se retrouve où ? » (fr, en, it, de) : deux personnes, deux villes de départ, la destination où les deux
allers-retours additionnés coûtent le moins cher. Aucun prix écrit dans la page : site/retrouver.js interroge
/api/explore (wide=1) pour chaque ville et croise les destinations."""
import html
import json

import build_i18n as B
from explore_pages import ORIGINS

E = html.escape
COL = {"fr": 1, "en": 2, "it": 2, "de": 2}
PATHS = {"fr": "on-se-retrouve-ou", "en": "en/meet-halfway", "it": "it/dove-ci-incontriamo", "de": "de/wo-treffen-wir-uns"}

T = {
    "fr": dict(
        title="On se retrouve où ? La destination la moins chère pour deux | Escale",
        desc="Vous êtes dans deux villes différentes ? Escale trouve la destination où vos deux billets aller-retour additionnés coûtent le moins cher. Prix réels.",
        h1="On se retrouve <span>où ?</span>",
        lead="Toi d'un côté, un proche de l'autre : choisissez vos deux villes et un mois. Escale additionne vos deux billets aller-retour et classe les destinations de la moins chère à la plus chère.",
        a="Moi, je pars de", b="L'autre part de", month="Mois", go="Trouver où se retrouver",
        load="On cherche les meilleurs points de rencontre…", none="Pas de destination commune trouvée ce mois-ci. Essayez un autre mois ou d'autres villes.",
        same="Choisissez deux villes différentes.", count="{n} destinations, la moins chère pour vous deux en premier",
        you="Moi", them="L'autre", total="à deux", together="{n} jours ensemble", adjust="dates à ajuster",
        visit="Ou l'un rend visite à l'autre", visit_ab="{a} → {b}", book="Voir les vols",
        tips_h="Bon à savoir",
        tips=["Chaque prix est l'aller-retour le moins cher trouvé pour chacun dans le mois : les dates ne sont pas forcément les mêmes. Le badge vert indique les jours où vous seriez sur place ensemble.",
              "Ouvrez les deux recherches et alignez vos dates : le prix change souvent de quelques euros selon le jour.",
              "Pensez aux visas : vérifiez que la destination est accessible avec vos deux passeports."],
        note="Prix aller-retour trouvés récemment par notre partenaire de recherche (Aviasales). Ils se confirment sur le site de réservation."),
    "en": dict(
        title="Meet halfway: the cheapest place for two to meet | Escale",
        desc="Living in two different cities? Escale finds the destination where your two round-trip tickets added together cost the least. Real prices.",
        h1="Where shall we <span>meet?</span>",
        lead="You on one side, a loved one on the other: pick your two cities and a month. Escale adds up both round-trip tickets and ranks destinations from cheapest to most expensive.",
        a="I'm leaving from", b="They're leaving from", month="Month", go="Find where to meet",
        load="Looking for the best meeting points…", none="No common destination found this month. Try another month or other cities.",
        same="Pick two different cities.", count="{n} destinations, cheapest for both of you first",
        you="Me", them="Them", total="for two", together="{n} days together", adjust="dates to adjust",
        visit="Or one visits the other", visit_ab="{a} → {b}", book="See flights",
        tips_h="Good to know",
        tips=["Each price is the cheapest round trip found for each person in the month, so the dates may differ. The green badge shows the days you would both be there.",
              "Open both searches and line up your dates: prices often change by a few euros from one day to the next.",
              "Check visas: make sure the destination is open to both your passports."],
        note="Round-trip prices recently found by our search partner (Aviasales). They are confirmed on the booking site."),
    "it": dict(
        title="Dove ci incontriamo? La meta più economica per due | Escale",
        desc="Vivete in due città diverse? Escale trova la meta dove i vostri due biglietti andata e ritorno sommati costano meno. Prezzi reali.",
        h1="Dove ci <span>incontriamo?</span>",
        lead="Tu da una parte, una persona cara dall'altra: scegliete le vostre due città e un mese. Escale somma i due biglietti andata e ritorno e ordina le mete dalla più economica.",
        a="Io parto da", b="L'altra persona parte da", month="Mese", go="Trova dove incontrarsi",
        load="Cerchiamo i migliori punti d'incontro…", none="Nessuna meta comune trovata questo mese. Prova un altro mese o altre città.",
        same="Scegli due città diverse.", count="{n} mete, dalla più economica per entrambi",
        you="Io", them="L'altra persona", total="in due", together="{n} giorni insieme", adjust="date da sistemare",
        visit="Oppure uno va a trovare l'altro", visit_ab="{a} → {b}", book="Vedi i voli",
        tips_h="Da sapere",
        tips=["Ogni prezzo è l'andata e ritorno più economico trovato per ciascuno nel mese: le date possono essere diverse. Il badge verde indica i giorni in cui sareste lì insieme.",
              "Apri le due ricerche e allinea le date: il prezzo cambia spesso di qualche euro da un giorno all'altro.",
              "Controlla i visti: verifica che la meta sia accessibile con entrambi i passaporti."],
        note="Prezzi andata e ritorno trovati di recente dal nostro partner di ricerca (Aviasales). Vengono confermati sul sito di prenotazione."),
    "de": dict(
        title="Wo treffen wir uns? Das günstigste Ziel für zwei | Escale",
        desc="Ihr wohnt in zwei verschiedenen Städten? Escale findet das Ziel, an dem eure beiden Hin- und Rückflüge zusammen am wenigsten kosten. Echte Preise.",
        h1="Wo treffen <span>wir uns?</span>",
        lead="Du auf der einen Seite, ein lieber Mensch auf der anderen: Wählt eure beiden Städte und einen Monat. Escale addiert beide Hin- und Rückflüge und sortiert die Ziele vom günstigsten an.",
        a="Ich fliege ab", b="Die andere Person fliegt ab", month="Monat", go="Treffpunkt finden",
        load="Die besten Treffpunkte werden gesucht…", none="Kein gemeinsames Ziel in diesem Monat gefunden. Versuche einen anderen Monat oder andere Städte.",
        same="Wähle zwei verschiedene Städte.", count="{n} Ziele, günstigstes für euch beide zuerst",
        you="Ich", them="Die andere Person", total="zu zweit", together="{n} Tage zusammen", adjust="Daten anpassen",
        visit="Oder einer besucht den anderen", visit_ab="{a} → {b}", book="Flüge ansehen",
        tips_h="Gut zu wissen",
        tips=["Jeder Preis ist der günstigste Hin- und Rückflug, der für jede Person im Monat gefunden wurde: Die Daten können abweichen. Das grüne Abzeichen zeigt die Tage, an denen ihr beide vor Ort wärt.",
              "Öffne beide Suchen und gleiche eure Daten ab: Der Preis ändert sich oft um ein paar Euro von Tag zu Tag.",
              "Denk an Visa: Prüfe, ob das Ziel mit beiden Reisepässen zugänglich ist."],
        note="Hin- und Rückflugpreise, kürzlich von unserem Suchpartner (Aviasales) gefunden. Sie werden auf der Buchungsseite bestätigt."),
}


def build(site, ctx):
    urls = []
    for lang, t in T.items():
        opts = "".join(f'<option value="{o[0]}">{E(o[COL[lang]])} ({o[0]})</option>' for o in ORIGINS)
        keys = ("load", "none", "same", "count", "you", "them", "total", "together", "adjust", "visit", "visit_ab", "book")
        tj = E(json.dumps({k: t[k] for k in keys}, ensure_ascii=False))
        body = (f'<form class="mt-form" id="mt-form" data-t="{tj}" novalidate>'
                f'<label class="any-field"><span>{E(t["a"])}</span><select id="mt-a">{opts}</select></label>'
                f'<label class="any-field"><span>{E(t["b"])}</span><select id="mt-b">{opts}</select></label>'
                f'<div class="any-field"><span id="mt-ml">{E(t["month"])}</span><div class="chips" id="mt-months" role="group" aria-labelledby="mt-ml"></div></div>'
                f'<button class="btn" type="submit">{E(t["go"])}</button></form>'
                '<p class="small mt-status" id="mt-status" role="status"></p>'
                '<div class="mt-visit" id="mt-visit" hidden></div>'
                '<ul class="mt-list" id="mt-list"></ul>'
                f'<section><h2>{E(t["tips_h"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["tips"]) +
                f'</ul><p class="small">{E(t["note"])}</p></section>'
                '<script src="/retrouver.js" defer></script>')
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, PATHS[lang], lang, t["title"], t["desc"], hero, body, "", PATHS, ctx))
    return urls
