"""Page « Surprends-moi » (fr, en, it, de) : tirage au sort d'une destination aller-retour sous le budget choisi,
dans les 3 prochains mois. Aucun prix écrit dans la page : site/surprise.js interroge /api/explore (wide=1)."""
import html
import json

import build_i18n as B
from explore_pages import ORIGINS

E = html.escape
COL = {"fr": 1, "en": 2, "it": 2, "de": 2}
PATHS = {"fr": "surprends-moi", "en": "en/surprise-me", "it": "it/sorprendimi", "de": "de/ueberrasch-mich"}
BUDGETS = (100, 200, 300, 500)

T = {
    "fr": dict(
        title="Surprends-moi : une destination au hasard dans ton budget | Escale",
        desc="Tu ne sais pas où partir ? Choisis ta ville et ton budget, Escale tire au sort une destination aller-retour pas chère pour les 3 prochains mois. Prix réels.",
        h1="Surprends-<span>moi</span> 🎲",
        lead="Tu ne sais pas où partir ? Choisis ta ville et ton budget : Escale tire au sort une destination où l'aller-retour rentre dans ton budget, dans les 3 prochains mois.",
        from_l="Départ de", budget="Budget aller-retour", any="Peu importe", go="🎲 Surprends-moi",
        load="Le tirage se prépare…", none="Aucune destination trouvée dans ce budget pour l'instant. Essaie un budget plus élevé ou une autre ville.",
        again="🎲 Encore !", book="Voir les vols", share="Partager sur WhatsApp", direct="direct", stop="avec escale",
        share_txt="Escale m'a tiré au sort {c} pour {p} aller-retour 😱",
        note="Prix aller-retour trouvés récemment par notre partenaire de recherche (Aviasales), pour les dates affichées. Ils se confirment sur le site de réservation."),
    "en": dict(
        title="Surprise me: a random destination within your budget | Escale",
        desc="Don't know where to go? Pick your city and budget and Escale draws a cheap round-trip destination for the next 3 months. Real prices.",
        h1="Surprise <span>me</span> 🎲",
        lead="Don't know where to go? Pick your city and budget: Escale draws a destination where the round trip fits your budget, over the next 3 months.",
        from_l="Leaving from", budget="Round-trip budget", any="Any", go="🎲 Surprise me",
        load="Getting the draw ready…", none="No destination found within this budget right now. Try a higher budget or another city.",
        again="🎲 Again!", book="See flights", share="Share on WhatsApp", direct="direct", stop="with a stop",
        share_txt="Escale picked {c} for me, {p} round trip 😱",
        note="Round-trip prices recently found by our search partner (Aviasales), for the dates shown. They are confirmed on the booking site."),
    "it": dict(
        title="Sorprendimi: una meta a caso nel tuo budget | Escale",
        desc="Non sai dove andare? Scegli la tua città e il budget, Escale estrae a sorte una meta andata e ritorno economica per i prossimi 3 mesi. Prezzi reali.",
        h1="Sorprendi<span>mi</span> 🎲",
        lead="Non sai dove andare? Scegli la tua città e il budget: Escale estrae una meta dove l'andata e ritorno rientra nel tuo budget, nei prossimi 3 mesi.",
        from_l="Partenza da", budget="Budget andata e ritorno", any="Qualsiasi", go="🎲 Sorprendimi",
        load="L'estrazione si prepara…", none="Nessuna meta trovata con questo budget per ora. Prova un budget più alto o un'altra città.",
        again="🎲 Ancora!", book="Vedi i voli", share="Condividi su WhatsApp", direct="diretto", stop="con scalo",
        share_txt="Escale mi ha estratto {c} a {p} andata e ritorno 😱",
        note="Prezzi andata e ritorno trovati di recente dal nostro partner di ricerca (Aviasales), per le date indicate. Vengono confermati sul sito di prenotazione."),
    "de": dict(
        title="Überrasch mich: ein zufälliges Ziel in deinem Budget | Escale",
        desc="Du weißt nicht, wohin? Wähle deine Stadt und dein Budget, Escale lost ein günstiges Ziel mit Hin- und Rückflug für die nächsten 3 Monate aus. Echte Preise.",
        h1="Überrasch <span>mich</span> 🎲",
        lead="Du weißt nicht, wohin? Wähle deine Stadt und dein Budget: Escale lost ein Ziel aus, dessen Hin- und Rückflug in dein Budget passt, in den nächsten 3 Monaten.",
        from_l="Abflug ab", budget="Budget hin und zurück", any="Egal", go="🎲 Überrasch mich",
        load="Die Auslosung wird vorbereitet…", none="Gerade kein Ziel in diesem Budget gefunden. Versuche ein höheres Budget oder eine andere Stadt.",
        again="🎲 Nochmal!", book="Flüge ansehen", share="Auf WhatsApp teilen", direct="direkt", stop="mit Umstieg",
        share_txt="Escale hat mir {c} ausgelost, {p} hin und zurück 😱",
        note="Hin- und Rückflugpreise, kürzlich von unserem Suchpartner (Aviasales) gefunden, für die angezeigten Daten. Sie werden auf der Buchungsseite bestätigt."),
}


def build(site, ctx):
    urls = []
    for lang, t in T.items():
        opts = "".join(f'<option value="{o[0]}">{E(o[COL[lang]])} ({o[0]})</option>' for o in ORIGINS)
        keys = ("load", "none", "again", "book", "share", "direct", "stop", "share_txt")
        tj = E(json.dumps({k: t[k] for k in keys}, ensure_ascii=False))
        chips = "".join(f'<button type="button" data-max="{m}" aria-pressed="{"true" if m == 200 else "false"}">≤ {m} €</button>' for m in BUDGETS)
        chips += f'<button type="button" data-max="0" aria-pressed="false">{E(t["any"])}</button>'
        body = (f'<div class="sp-box" id="sp-box" data-t="{tj}">'
                f'<div class="sp-controls"><label class="any-field"><span>{E(t["from_l"])}</span><select id="sp-from">{opts}</select></label>'
                f'<div class="any-field"><span id="sp-bl">{E(t["budget"])}</span><div class="chips" id="sp-budget" role="group" aria-labelledby="sp-bl">{chips}</div></div></div>'
                f'<button class="btn sp-go" id="sp-go" type="button">{E(t["go"])}</button>'
                '<div class="sp-stage" id="sp-stage" aria-live="polite"></div></div>'
                f'<p class="small">{E(t["note"])}</p>'
                '<script src="/surprise.js" defer></script>')
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, PATHS[lang], lang, t["title"], t["desc"], hero, body, "", PATHS, ctx))
    return urls
