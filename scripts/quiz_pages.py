"""Page « Quiz : quelle destination est faite pour toi ? » (fr, en, it, de).
5 questions ; site/quiz.js calcule un score par destination (étiquettes ci-dessous), puis cherche le vrai prix
aller-retour depuis l'aéroport du visiteur (/api/prix) et garde les 3 meilleures qui rentrent dans son budget."""
import html
import json

import build_i18n as B

E = html.escape
PATHS = {"fr": "quiz-destination", "en": "en/destination-quiz", "it": "it/quiz-destinazione", "de": "de/reiseziel-quiz"}

# Étiquettes : b plage, c ville, h culture et histoire, n nature ; distance depuis l'Europe : s court, m moyen, l long ;
# a ambiance animée / q plutôt calme ; f facile en famille
DEST = [
    ("BCN", "bch", "s", "a", ""), ("LIS", "chb", "s", "a", ""), ("RAK", "hc", "s", "a", ""), ("IST", "hc", "s", "a", ""),
    ("ATH", "hb", "s", "a", ""), ("FAO", "bn", "s", "q", "f"), ("NAP", "hc", "s", "a", ""), ("DBV", "hb", "s", "q", ""),
    ("PRG", "ch", "s", "a", ""), ("BUD", "ch", "s", "a", ""), ("MLA", "bh", "s", "q", "f"), ("AGA", "b", "s", "q", "f"),
    ("DJE", "b", "s", "q", "f"), ("FNC", "n", "s", "q", "f"), ("KEF", "n", "s", "q", ""), ("TFS", "bn", "m", "q", "f"),
    ("DSS", "bh", "m", "a", ""), ("DXB", "cb", "l", "a", "f"), ("ZNZ", "b", "l", "q", ""), ("NBO", "n", "l", "q", ""),
    ("CPT", "nbc", "l", "a", ""), ("BKK", "ch", "l", "a", ""), ("DPS", "bn", "l", "q", ""), ("JFK", "c", "l", "a", ""),
    ("MRU", "b", "l", "q", "f"),
]

# Questions : (texte, [(réponse, effet)]) ; effet = clé lue par quiz.js
Q = {
    "fr": [("Tu as envie de quoi ?", [("🏖️ Plage et soleil", "t:b"), ("🌆 Ville et sorties", "t:c"), ("🏛️ Culture et histoire", "t:h"), ("🌋 Nature et grands espaces", "t:n")]),
           ("Tu pars avec qui ?", [("🙋 Seul·e", "w:solo"), ("💑 En couple", "w:duo"), ("🎉 Entre amis", "w:amis"), ("👨‍👩‍👧 En famille", "w:fam")]),
           ("Combien de temps ?", [("⚡ Un week-end", "d:s"), ("📅 Une semaine", "d:m"), ("🌍 Deux semaines ou plus", "d:l")]),
           ("Ton budget pour le billet aller-retour ?", [("💸 Moins de 150 €", "p:150"), ("💶 Jusqu'à 400 €", "p:400"), ("💎 Peu importe", "p:0")]),
           ("Plutôt…", [("🔥 Ça bouge, je veux sortir", "v:a"), ("🌿 Calme, je veux souffler", "v:q")])],
    "en": [("What are you in the mood for?", [("🏖️ Beach and sun", "t:b"), ("🌆 City and nightlife", "t:c"), ("🏛️ Culture and history", "t:h"), ("🌋 Nature and wide open spaces", "t:n")]),
           ("Who's coming?", [("🙋 Just me", "w:solo"), ("💑 My partner", "w:duo"), ("🎉 Friends", "w:amis"), ("👨‍👩‍👧 Family", "w:fam")]),
           ("How long?", [("⚡ A weekend", "d:s"), ("📅 A week", "d:m"), ("🌍 Two weeks or more", "d:l")]),
           ("Your budget for the round-trip ticket?", [("💸 Under €150", "p:150"), ("💶 Up to €400", "p:400"), ("💎 Doesn't matter", "p:0")]),
           ("You'd rather…", [("🔥 Lively, I want to go out", "v:a"), ("🌿 Quiet, I want to unwind", "v:q")])],
    "it": [("Di cosa hai voglia?", [("🏖️ Mare e sole", "t:b"), ("🌆 Città e locali", "t:c"), ("🏛️ Cultura e storia", "t:h"), ("🌋 Natura e grandi spazi", "t:n")]),
           ("Con chi parti?", [("🙋 Da solo/a", "w:solo"), ("💑 In coppia", "w:duo"), ("🎉 Con gli amici", "w:amis"), ("👨‍👩‍👧 In famiglia", "w:fam")]),
           ("Per quanto tempo?", [("⚡ Un weekend", "d:s"), ("📅 Una settimana", "d:m"), ("🌍 Due settimane o più", "d:l")]),
           ("Il tuo budget per il biglietto andata e ritorno?", [("💸 Meno di 150 €", "p:150"), ("💶 Fino a 400 €", "p:400"), ("💎 Non importa", "p:0")]),
           ("Preferisci…", [("🔥 Movimento, voglio uscire", "v:a"), ("🌿 Calma, voglio rilassarmi", "v:q")])],
    "de": [("Worauf hast du Lust?", [("🏖️ Strand und Sonne", "t:b"), ("🌆 Stadt und Ausgehen", "t:c"), ("🏛️ Kultur und Geschichte", "t:h"), ("🌋 Natur und Weite", "t:n")]),
           ("Mit wem reist du?", [("🙋 Allein", "w:solo"), ("💑 Zu zweit", "w:duo"), ("🎉 Mit Freunden", "w:amis"), ("👨‍👩‍👧 Mit der Familie", "w:fam")]),
           ("Wie lange?", [("⚡ Ein Wochenende", "d:s"), ("📅 Eine Woche", "d:m"), ("🌍 Zwei Wochen oder mehr", "d:l")]),
           ("Dein Budget für das Hin- und Rückflugticket?", [("💸 Unter 150 €", "p:150"), ("💶 Bis 400 €", "p:400"), ("💎 Egal", "p:0")]),
           ("Lieber…", [("🔥 Was los, ich will ausgehen", "v:a"), ("🌿 Ruhig, ich will abschalten", "v:q")])],
}

T = {
    "fr": dict(title="Quiz : quelle destination est faite pour toi ? | Escale",
               desc="5 questions pour trouver ta destination idéale, avec le vrai prix du billet aller-retour depuis ton aéroport. Gratuit, sans inscription.",
               h1="Quelle destination <span>est faite pour toi ?</span>",
               lead="5 questions, 30 secondes : Escale te propose 3 destinations qui te ressemblent, avec le vrai prix de l'aller-retour depuis ton aéroport.",
               start="C'est parti →", step="Question {i} sur {n}", back="← Retour", load="On calcule tes destinations…",
               res_h="Tes 3 destinations", from_l="Prix aller-retour depuis", none_price="prix à vérifier", over="au-dessus de ton budget",
               book="Voir les vols", again="Refaire le quiz", share="Partager sur WhatsApp",
               share_txt="Le quiz Escale dit que je suis fait·e pour {c} ! Et toi ?",
               tags={"b": "🏖️ Plage", "c": "🌆 Ville", "h": "🏛️ Culture", "n": "🌋 Nature", "s": "✈️ Proche de l'Europe", "m": "✈️ Moyen-courrier", "l": "✈️ Long-courrier", "f": "👨‍👩‍👧 En famille"},
               note="Les prix sont les allers-retours les moins chers trouvés récemment par notre partenaire de recherche (Aviasales) pour le mois prochain. Ils se confirment sur le site de réservation."),
    "en": dict(title="Quiz: which destination is right for you? | Escale",
               desc="5 questions to find your ideal destination, with the real round-trip price from your airport. Free, no sign-up.",
               h1="Which destination <span>is right for you?</span>",
               lead="5 questions, 30 seconds: Escale suggests 3 destinations that suit you, with the real round-trip price from your airport.",
               start="Let's go →", step="Question {i} of {n}", back="← Back", load="Working out your destinations…",
               res_h="Your 3 destinations", from_l="Round-trip price from", none_price="price to check", over="above your budget",
               book="See flights", again="Take the quiz again", share="Share on WhatsApp",
               share_txt="The Escale quiz says {c} is my place! What about you?",
               tags={"b": "🏖️ Beach", "c": "🌆 City", "h": "🏛️ Culture", "n": "🌋 Nature", "s": "✈️ Close to Europe", "m": "✈️ Medium-haul", "l": "✈️ Long-haul", "f": "👨‍👩‍👧 Family-friendly"},
               note="Prices are the cheapest round trips recently found by our search partner (Aviasales) for next month. They are confirmed on the booking site."),
    "it": dict(title="Quiz: quale meta fa per te? | Escale",
               desc="5 domande per trovare la tua meta ideale, con il prezzo reale del biglietto andata e ritorno dal tuo aeroporto. Gratis, senza registrazione.",
               h1="Quale meta <span>fa per te?</span>",
               lead="5 domande, 30 secondi: Escale ti propone 3 mete che ti somigliano, con il prezzo reale dell'andata e ritorno dal tuo aeroporto.",
               start="Iniziamo →", step="Domanda {i} di {n}", back="← Indietro", load="Calcoliamo le tue mete…",
               res_h="Le tue 3 mete", from_l="Prezzo andata e ritorno da", none_price="prezzo da verificare", over="sopra il tuo budget",
               book="Vedi i voli", again="Rifai il quiz", share="Condividi su WhatsApp",
               share_txt="Il quiz di Escale dice che {c} fa per me! E tu?",
               tags={"b": "🏖️ Mare", "c": "🌆 Città", "h": "🏛️ Cultura", "n": "🌋 Natura", "s": "✈️ Vicino all'Europa", "m": "✈️ Medio raggio", "l": "✈️ Lungo raggio", "f": "👨‍👩‍👧 In famiglia"},
               note="I prezzi sono le andate e ritorno più economiche trovate di recente dal nostro partner di ricerca (Aviasales) per il mese prossimo. Vengono confermati sul sito di prenotazione."),
    "de": dict(title="Quiz: Welches Reiseziel passt zu dir? | Escale",
               desc="5 Fragen zu deinem idealen Reiseziel, mit dem echten Preis für Hin- und Rückflug ab deinem Flughafen. Kostenlos, ohne Anmeldung.",
               h1="Welches Reiseziel <span>passt zu dir?</span>",
               lead="5 Fragen, 30 Sekunden: Escale schlägt dir 3 passende Ziele vor, mit dem echten Preis für Hin- und Rückflug ab deinem Flughafen.",
               start="Los geht's →", step="Frage {i} von {n}", back="← Zurück", load="Deine Reiseziele werden berechnet…",
               res_h="Deine 3 Reiseziele", from_l="Preis hin und zurück ab", none_price="Preis prüfen", over="über deinem Budget",
               book="Flüge ansehen", again="Quiz wiederholen", share="Auf WhatsApp teilen",
               share_txt="Laut Escale-Quiz passt {c} zu mir! Und zu dir?",
               tags={"b": "🏖️ Strand", "c": "🌆 Stadt", "h": "🏛️ Kultur", "n": "🌋 Natur", "s": "✈️ Nah an Europa", "m": "✈️ Mittelstrecke", "l": "✈️ Langstrecke", "f": "👨‍👩‍👧 Familienfreundlich"},
               note="Die Preise sind die günstigsten Hin- und Rückflüge, die unser Suchpartner (Aviasales) kürzlich für den nächsten Monat gefunden hat. Sie werden auf der Buchungsseite bestätigt."),
}


def build(site, ctx):
    urls = []
    for lang, t in T.items():
        keys = ("step", "back", "load", "res_h", "from_l", "none_price", "over", "book", "again", "share", "share_txt", "tags")
        cfg = {"t": {k: t[k] for k in keys}, "q": Q[lang], "d": DEST}
        body = (f'<div class="qz" id="qz" data-cfg="{E(json.dumps(cfg, ensure_ascii=False))}">'
                f'<button class="btn qz-start" id="qz-start" type="button">{E(t["start"])}</button></div>'
                f'<p class="small">{E(t["note"])}</p>'
                '<script src="/fetes.js" defer></script><script src="/quiz.js" defer></script>')
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, PATHS[lang], lang, t["title"], t["desc"], hero, body, "", PATHS, ctx))
    return urls
