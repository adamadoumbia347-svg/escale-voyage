"""Outils (fr, en) : « As-tu payé ton billet trop cher ? » et « Le vrai budget du voyage en famille ».
Aucun prix écrit : les vrais prix viennent du calendrier des prix (/api/calendar) ; bagages, visa et assurance sont saisis
par le visiteur (seul raccourci : visa Schengen 90 € adulte / 45 € de 6 à 12 ans, vérifié en novembre 2026)."""
import html
import json

import build_i18n as B

E = html.escape
CURS = ["EUR", "USD", "GBP", "CAD", "CHF", "XOF", "XAF", "MAD"]

TC = {
    "fr": dict(path="billet-trop-cher", title="As-tu payé ton billet d'avion trop cher ? Le test gratuit | Escale",
               desc="Entre ton trajet, ta date et le prix payé : Escale compare avec les vrais prix trouvés pour le même jour et le même mois, et te dit si tu as payé trop cher.",
               h1="As-tu payé ton billet <span>trop cher ?</span>", lead="Entre ton trajet, ta date de départ et le prix payé. Escale compare avec les vrais prix trouvés le même jour et dans le même mois.",
               f=dict(fr="Départ", to="Arrivée", dep="Date de départ", paid="Prix payé (total)", cur="Monnaie", pax="Nombre de billets", go="Tester mon billet", ph="Ville ou aéroport"),
               t=dict(err="Choisis un départ et une arrivée dans la liste, une date et un prix.", loading="Comparaison avec les vrais prix…",
                      none="Pas assez de prix connus pour ce trajet ce mois-là. Essaie un aéroport proche.", v_good="🟢 Bien joué : tu as payé le bon prix !",
                      v_mid="🟡 Un peu cher", v_bad="🔴 Trop cher", more="Environ {x} de plus que le meilleur prix connu, par billet.", less="{x} de moins que le meilleur prix connu, par billet. Bravo !",
                      l_same="Meilleur prix trouvé pour un départ le {d} : {p}", l_best="Meilleur prix du mois (départ le {d}) : {p}", l_paid="Ton prix par billet : {p}",
                      share="Défie tes amis", share_bad="J'ai testé mon billet sur Escale : je l'ai payé {x} trop cher 😅 Et toi ?", share_good="J'ai testé mon billet sur Escale : j'ai payé le bon prix 😎 Et toi ?",
                      see="Voir le meilleur prix", note="Comparaison avec les prix aller-retour trouvés récemment par notre partenaire de recherche (Aviasales), convertis en euros au taux du jour. Les bagages et options ne sont pas comptés."),
               next_h="La prochaine fois", next=["Crée une alerte prix : tu seras prévenu quand le prix baisse.", "Regarde le meilleur mois pour partir et les dates ±3 jours."]),
    "en": dict(path="en/did-i-overpay", title="Did you pay too much for your flight? The free test | Escale",
               desc="Enter your route, date and the price you paid: Escale compares it with real prices found for the same day and the same month, and tells you if you overpaid.",
               h1="Did you pay <span>too much?</span>", lead="Enter your route, departure date and the price you paid. Escale compares it with real prices found on the same day and in the same month.",
               f=dict(fr="From", to="To", dep="Departure date", paid="Price paid (total)", cur="Currency", pax="Number of tickets", go="Test my ticket", ph="City or airport"),
               t=dict(err="Pick a departure and an arrival from the list, a date and a price.", loading="Comparing with real prices…",
                      none="Not enough known prices for this route that month. Try a nearby airport.", v_good="🟢 Well done: you paid the right price!",
                      v_mid="🟡 A bit expensive", v_bad="🔴 Too expensive", more="About {x} more than the best known price, per ticket.", less="{x} less than the best known price, per ticket. Well done!",
                      l_same="Best price found for a departure on {d}: {p}", l_best="Best price of the month (departure on {d}): {p}", l_paid="Your price per ticket: {p}",
                      share="Challenge your friends", share_bad="I tested my ticket on Escale: I paid {x} too much 😅 What about you?", share_good="I tested my ticket on Escale: I paid the right price 😎 What about you?",
                      see="See the best price", note="Compared with round-trip prices recently found by our search partner (Aviasales), converted to euros at today's rate. Baggage and extras are not included."),
               next_h="Next time", next=["Set a price alert: you'll be told when the price drops.", "Check the cheapest month to fly and ±3 day dates."]),
}

BF = {
    "fr": dict(path="budget-voyage-famille", title="Budget voyage en famille : le vrai prix tout compris, en euros et en FCFA | Escale",
               desc="Combien coûte vraiment le voyage en famille ? Billets réels pour chaque voyageur, bagages, visa et assurance : le total en euros et en francs CFA, à partager avec la famille.",
               h1="Le vrai budget du voyage <span>en famille</span>", lead="Billets au vrai prix pour chaque voyageur, plus les bagages, le visa et l'assurance : le total tout compris, en euros et en francs CFA.",
               f=dict(fr="Départ", to="Arrivée", month="Mois", ad="Adultes", ch="Enfants (2-11 ans)", bb="Bébés (moins de 2 ans)", bags="Valises en soute par personne",
                      bagp="Prix d'une valise en soute (aller-retour, €)", visa_a="Visa par adulte (€)", visa_c="Visa par enfant (€)", sch="Visa Schengen", ins="Assurance par personne (€)",
                      go="Calculer le budget", ph="Ville ou aéroport", opt="Facultatif : laissez 0 si rien à payer."),
               t=dict(err="Choisis un départ et une arrivée dans la liste.", loading="Calcul avec les vrais prix…", none="Pas assez de prix connus pour ce trajet ce mois-là. Essaie un autre mois ou un aéroport proche.",
                      r_tickets="Billets aller-retour ({n} × {p})", r_bags="Bagages en soute ({n} × {p})", r_visa="Visas", r_ins="Assurance ({n} personnes)", total="Total tout compris",
                      per="Soit environ {p} par personne.", dates="Prix du jour le moins cher du mois : départ le {d}, retour le {r}.",
                      baby="Bébé(s) : {n}. Le tarif bébé dépend de la compagnie (il n'est pas compté ici) : vérifiez-le au moment de réserver.",
                      child="Enfants comptés au prix adulte : les compagnies font parfois un peu moins cher.",
                      bag_hint="Prix des bagages non saisi : voyez <a href=\"/bagages-compagnies-afrique/\">les bagages de chaque compagnie</a>.",
                      see="Voir les vols à ces dates", share="Partager avec la famille",
                      wa="Budget voyage {a} → {b} pour {n} personnes : {t} tout compris ({c}). Calculé sur Escale :",
                      note="Billets : meilleur prix aller-retour du mois trouvé récemment par notre partenaire de recherche (Aviasales). Bagages, visa et assurance : montants saisis par vous.")),
    "en": dict(path="en/family-trip-budget", title="Family trip budget: the real all-in price, in euros and CFA francs | Escale",
               desc="How much does the family trip really cost? Real fares for each traveller, baggage, visa and insurance: the total in euros and CFA francs, to share with the family.",
               h1="The real cost of a <span>family trip</span>", lead="Real fares for each traveller, plus baggage, visa and insurance: the all-in total, in euros and CFA francs.",
               f=dict(fr="From", to="To", month="Month", ad="Adults", ch="Children (2-11)", bb="Infants (under 2)", bags="Checked bags per person",
                      bagp="Price of one checked bag (return, €)", visa_a="Visa per adult (€)", visa_c="Visa per child (€)", sch="Schengen visa", ins="Insurance per person (€)",
                      go="Calculate the budget", ph="City or airport", opt="Optional: leave 0 if nothing to pay."),
               t=dict(err="Pick a departure and an arrival from the list.", loading="Calculating with real prices…", none="Not enough known prices for this route that month. Try another month or a nearby airport.",
                      r_tickets="Round-trip tickets ({n} × {p})", r_bags="Checked bags ({n} × {p})", r_visa="Visas", r_ins="Insurance ({n} people)", total="All-in total",
                      per="About {p} per person.", dates="Price of the cheapest day of the month: out on {d}, back on {r}.",
                      baby="Infant(s): {n}. Infant fares depend on the airline (not counted here): check when booking.",
                      child="Children counted at the adult fare: airlines sometimes charge a little less.",
                      bag_hint="Baggage price not entered: see <a href=\"/bagages-compagnies-afrique/\">each airline's baggage rules</a>.",
                      see="See flights on these dates", share="Share with the family",
                      wa="Trip budget {a} → {b} for {n} people: {t} all-in ({c}). Calculated on Escale:",
                      note="Tickets: best round-trip price of the month recently found by our search partner (Aviasales). Baggage, visa and insurance: amounts entered by you.")),
}


def build(site, ctx):
    urls = []
    tp = {l: TC[l]["path"] for l in TC}
    for lang, t in TC.items():
        f = t["f"]
        opts = "".join(f"<option{' selected' if c == 'EUR' else ''}>{c}</option>" for c in CURS)
        body = (f'<form id="tc-form" class="tool-form" novalidate data-t="{E(json.dumps(t["t"], ensure_ascii=False))}"><div class="tool-grid">'
                f'<label><span>{E(f["fr"])}</span><input id="tc-from" placeholder="{E(f["ph"])}" required></label>'
                f'<label><span>{E(f["to"])}</span><input id="tc-to" placeholder="{E(f["ph"])}" required></label>'
                f'<label><span>{E(f["dep"])}</span><input id="tc-dep" type="date" required></label>'
                f'<label><span>{E(f["pax"])}</span><input id="tc-pax" type="number" min="1" max="9" value="1" inputmode="numeric"></label>'
                f'<label><span>{E(f["paid"])}</span><input id="tc-paid" type="number" min="1" inputmode="decimal" required></label>'
                f'<label><span>{E(f["cur"])}</span><select id="tc-cur">{opts}</select></label></div>'
                f'<button class="btn" type="submit">{E(f["go"])}</button></form><div id="tc-out" aria-live="polite"></div>'
                f'<section id="price-alert" class="price-alert" data-from="PAR" data-to="DSS" hidden></section>'
                f'<section><h2>{E(t["next_h"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["next"]) + "</ul></section>"
                '<script src="/fetes.js" defer></script><script src="/ac-mini.js" defer></script><script src="/trop-cher.js" defer></script><script src="/alerts.js" defer></script>')
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, "", tp, ctx))
    bp = {l: BF[l]["path"] for l in BF}
    for lang, t in BF.items():
        f = t["f"]
        n = lambda i, lab, v="0", mx="9": f'<label><span>{E(lab)}</span><input id="{i}" type="number" min="0" max="{mx}" value="{v}" inputmode="numeric"></label>'
        body = (f'<form id="bf-form" class="tool-form" novalidate data-t="{E(json.dumps(t["t"], ensure_ascii=False))}"><div class="tool-grid">'
                f'<label><span>{E(f["fr"])}</span><input id="bf-from" placeholder="{E(f["ph"])}" required></label>'
                f'<label><span>{E(f["to"])}</span><input id="bf-to" placeholder="{E(f["ph"])}" required></label>'
                f'<label><span>{E(f["month"])}</span><select id="bf-month"></select></label>'
                + n("bf-ad", f["ad"], "2") + n("bf-ch", f["ch"], "2") + n("bf-bb", f["bb"]) + n("bf-bags", f["bags"], "1", "4") + n("bf-bagp", f["bagp"], "0", "999") +
                f'</div><p class="small">{E(f["opt"])}</p><div class="tool-grid">' + n("bf-visa-a", f["visa_a"], "0", "999") + n("bf-visa-c", f["visa_c"], "0", "999") + n("bf-ins", f["ins"], "0", "999") +
                f'<p class="bf-sch-wrap"><button type="button" class="btn ghost" id="bf-sch">🇪🇺 {E(f["sch"])} : 90 € / 45 €</button></p></div>'
                f'<button class="btn" type="submit">{E(f["go"])}</button></form><div id="bf-out" aria-live="polite"></div>'
                '<script src="/fetes.js" defer></script><script src="/ac-mini.js" defer></script><script src="/budget-famille.js" defer></script>')
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, "", bp, ctx))
    return urls
