"""Outil « Partir à plusieurs » (/partir-a-plusieurs/ et /en/travel-together/) : une destination, des dates, et le prix repéré
depuis chaque grande ville de départ d'Europe (Paris, Bruxelles, Lyon, Marseille, Milan, Rome, Londres, Genève, Amsterdam),
avec le total pour le groupe. Les prix viennent de /api/prix dans le navigateur (site/plusieurs.js) : aucun chiffre écrit ici."""
import html
import json

import build_i18n as B

E = html.escape
ORIGINS = [("CDG", "Paris"), ("BRU", "Bruxelles"), ("LYS", "Lyon"), ("MRS", "Marseille"), ("MXP", "Milan"), ("FCO", "Rome"), ("LHR", "Londres"), ("GVA", "Genève"), ("AMS", "Amsterdam"), ("MAD", "Madrid")]
ORIGINS_EN = {"Bruxelles": "Brussels", "Londres": "London", "Genève": "Geneva", "Milan": "Milan"}
DEST = [("ABJ", "Abidjan"), ("DSS", "Dakar"), ("BKO", "Bamako"), ("CKY", "Conakry"), ("DLA", "Douala"), ("NSI", "Yaoundé"), ("FIH", "Kinshasa"), ("BZV", "Brazzaville"), ("LBV", "Libreville"),
        ("LFW", "Lomé"), ("COO", "Cotonou"), ("OUA", "Ouagadougou"), ("NIM", "Niamey"), ("NKC", "Nouakchott"), ("BJL", "Banjul"), ("ACC", "Accra"), ("LOS", "Lagos"), ("ABV", "Abuja"),
        ("CMN", "Casablanca"), ("RAK", "Marrakech"), ("ALG", "Alger"), ("ORN", "Oran"), ("TUN", "Tunis"), ("DJE", "Djerba"), ("CAI", "Le Caire"),
        ("ADD", "Addis-Abeba"), ("NBO", "Nairobi"), ("KGL", "Kigali"), ("DAR", "Dar es Salaam"), ("JNB", "Johannesburg"), ("TNR", "Antananarivo"), ("MRU", "Maurice"), ("RUN", "La Réunion"), ("PTP", "Pointe-à-Pitre"), ("FDF", "Fort-de-France")]
DEST_EN = {"Le Caire": "Cairo", "Addis-Abeba": "Addis Ababa", "Alger": "Algiers", "Maurice": "Mauritius", "La Réunion": "Réunion", "Marrakech": "Marrakesh"}

T = {
    "fr": dict(path="partir-a-plusieurs", title="Partir à plusieurs : quelle ville de départ coûte le moins ? | Escale",
               desc="Vous êtes plusieurs, dans plusieurs villes d'Europe, et vous voulez vous retrouver au pays ? Comparez d'un coup le prix du vol depuis Paris, Bruxelles, Lyon, Milan, Rome, Londres… pour les mêmes dates.",
               eyebrow="Outil gratuit", h1="Partir à plusieurs : <span>qui paie le moins ?</span>",
               lead="Une destination, des dates, et le prix aller-retour repéré depuis chaque grande ville de départ, classé du moins cher au plus cher, avec le total pour le groupe.",
               dest="Destination", dep="Départ", ret="Retour (vide = aller simple)", n="Nombre de voyageurs", go="Comparer les villes de départ",
               how_h="À quoi ça sert", how=["Une famille dispersée entre Paris, Bruxelles et Milan qui se retrouve à Abidjan pour les fêtes : chacun voit d'un coup d'œil ce que coûte son billet, et qui a intérêt à partir d'une autre ville.",
                    "Un groupe d'amis qui hésite entre partir de Marseille ou de Paris : l'écart peut dépasser 150 € par personne sur certaines dates.",
                    "Une personne qui rejoint ses proches : si le vol depuis sa ville est beaucoup plus cher, un train ou un bus vers un autre aéroport peut valoir le coup."],
               tips_h="Trois conseils", tips=["Comparez le <strong>coût total</strong> : billet + trajet jusqu'à l'aéroport + nuit d'hôtel éventuelle. Un vol moins cher à 400 km ne l'est pas toujours.",
                    "Pour un groupe, réservez tôt : les prix affichés sont souvent ceux des dernières places à ce tarif, et le prix monte dès que quelques sièges partent.",
                    "Si vous voyagez avec des enfants, regardez la franchise bagages de la compagnie avant de choisir : <a href=\"/bagages-compagnies-afrique/\">bagages par compagnie</a>."],
               note="Prix aller-retour le plus bas repéré récemment par des voyageurs sur Aviasales (via Travelpayouts), par personne, pour le mois des dates choisies. Le tarif exact dépend des dates et se confirme sur le site de réservation.",
               alt_h="Voir aussi", alt=[("/barometre-prix/a-saisir/", "Les trajets à saisir aujourd'hui"), ("/diaspora/", "Rentrer au pays pour les fêtes : calendrier par communauté"), ("/calendrier-prix-diaspora/", "Le calendrier des prix par mois")]),
    "en": dict(path="en/travel-together", title="Travelling together: which departure city is cheapest? | Escale",
               desc="Several of you, in several European cities, meeting back home? Compare at a glance the fare from Paris, Brussels, Lyon, Milan, Rome, London… for the same dates.",
               eyebrow="Free tool", h1="Travelling together: <span>who pays the least?</span>",
               lead="One destination, your dates, and the round-trip fare found from each major departure city, cheapest first, with the total for the group.",
               dest="Destination", dep="Departure", ret="Return (empty = one way)", n="Number of travellers", go="Compare departure cities",
               how_h="What it is for", how=["A family spread between Paris, Brussels and Milan meeting in Abidjan for the holidays: everyone sees at a glance what their ticket costs, and who should fly from another city.",
                    "Friends hesitating between Marseille and Paris: the gap can exceed €150 per person on some dates.",
                    "Someone joining relatives: if the flight from their city is much dearer, a train or bus to another airport can be worth it."],
               tips_h="Three tips", tips=["Compare the <strong>total cost</strong>: ticket + trip to the airport + a possible hotel night. A cheaper flight 400 km away is not always cheaper.",
                    "For a group, book early: the fares shown are often the last seats at that price, and it rises as soon as a few seats go.",
                    "Travelling with children? Check the airline's baggage allowance first: <a href=\"/en/baggage-allowance-africa-airlines/\">baggage by airline</a>."],
               note="Lowest round-trip fare found recently by travellers on Aviasales (via Travelpayouts), per person, for the month of the chosen dates. The exact fare depends on dates and is confirmed on the booking site.",
               alt_h="See also", alt=[("/en/price-index/deals-today/", "Routes worth booking today"), ("/en/price-index/", "The Escale Price Index"), ("/en/guides/", "Travel guides")]),
}


def build(site, ctx):
    urls, paths = [], {l: T[l]["path"] for l in T}
    for lang, t in T.items():
        origins = [(c, ORIGINS_EN.get(v, v) if lang == "en" else v) for c, v in ORIGINS]
        opts = "".join(f'<option value="{c}">{E(DEST_EN.get(v, v) if lang == "en" else v)} ({c})</option>' for c, v in sorted(DEST, key=lambda x: (DEST_EN.get(x[1], x[1]) if lang == "en" else x[1])))
        hero = (f'<p class="eyebrow">{E(t["eyebrow"])}</p><h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>')
        form = (f'<form id="pl-form" class="pl-form" data-origins=\'{json.dumps(origins, ensure_ascii=False)}\'>'
                f'<label>{E(t["dest"])}<select name="to" required><option value="">—</option>{opts}</select></label>'
                f'<label>{E(t["dep"])}<input type="date" name="dep" required></label>'
                f'<label>{E(t["ret"])}<input type="date" name="ret"></label>'
                f'<label>{E(t["n"])}<input type="number" name="n" min="1" max="9" value="2" inputmode="numeric"></label>'
                f'<button type="submit" class="btn">{E(t["go"])}</button></form>'
                f'<div id="pl-out" hidden></div><p class="small">{E(t["note"])}</p>')
        style = ('<style>.pl-form{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));align-items:end;margin:8px 0 14px}.pl-form label{display:grid;gap:4px;font-size:.9rem;color:var(--muted)}'
                 '.pl-form input,.pl-form select{font:inherit;padding:10px 12px;border:1px solid var(--line);border-radius:12px;background:var(--surface,#fff);color:inherit;min-width:0}.pl-form .btn{grid-column:1/-1;justify-self:start}#pl-out{margin-top:8px}</style>')
        body = (style + f'<section>{form}</section>'
                f'<section><h2>{E(t["how_h"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["how"]) + "</ul></section>"
                f'<section><h2>{E(t["tips_h"])}</h2><ul>' + "".join(f"<li>{x}</li>" for x in t["tips"]) + "</ul></section>"
                f'<section><h2>{E(t["alt_h"])}</h2><ul>' + "".join(f'<li><a href="{h}">{E(l)}</a></li>' for h, l in t["alt"]) + "</ul></section>"
                + B.wa_btn(lang) + '<script src="/plusieurs.js" defer></script>')
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, "", paths, ctx))
    return urls
