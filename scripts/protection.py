"""Outils « protéger le voyageur » (fr, en) : anti-arnaque, indemnisation des retards, contrôle avant le vol,
destinations sans visa, calendrier des prix de la diaspora, acheter ou attendre, dossier de visa, kit hors ligne.

Faits vérifiés en novembre 2026 (sources officielles ou concordantes) :
- règlement (CE) 261/2004 : 250 € jusqu'à 1 500 km, 400 € intra-UE au-delà ou 1 500-3 500 km, 600 € au-delà ; retard d'au moins
  3 h à l'arrivée, annulation prévenue moins de 14 jours avant, refus d'embarquement ; vols au départ de l'UE (toute compagnie) ou
  vers l'UE avec une compagnie européenne ; réforme adoptée en juillet 2026 mais pas encore applicable (vers 2027). UK261 : 220/350/520 £ ;
- code des visas Schengen : dépôt au plus tôt 6 mois et au plus tard 15 jours avant, passeport délivré il y a moins de 10 ans,
  valable 3 mois après le départ de l'espace Schengen, 2 pages vierges, assurance 30 000 €, 90 € / 45 € ;
- fêtes : Ramadan vers le 8/2/2027, Aïd el-Fitr vers le 9-10/3/2027, Tabaski vers le 16-17/5/2027 (estimations, voir fetes.py).
Aucun prix écrit : tout vient des API Escale, depuis l'aéroport du visiteur.
"""
import html
import json

import build_i18n as B
import visa as V

E = html.escape
J = lambda o: E(json.dumps(o, ensure_ascii=False))
CURS = ["EUR", "USD", "GBP", "CAD", "CHF", "XOF", "XAF", "NGN", "GHS", "MAD"]
SCRIPTS = lambda *n: "".join(f'<script src="/{x}.js" defer></script>' for x in n)


def _tx(text, i):
    """Traduit un morceau de HTML anglais en italien (i=0) ou allemand (i=1) avec protection_itde.TR."""
    import re
    import protection_itde as PX
    TRX = PX.TR
    def one(s):
        v = TRX.get(s)
        return v[i] if v else None
    # 1. blocs avec balises (<li>, <p>… contenant <strong> ou <a>)
    for k, v in TRX.items():
        if k.startswith("HTML:"):
            src, dst = k[5:], v[i][5:]
            esc_src = re.sub(r"(^|>)([^<]+)", lambda m: m.group(1) + E(m.group(2)), src)
            for cand in (src, esc_src):
                text = text.replace(">" + cand + "<", ">" + dst + "<")
    # 2. nœuds de texte
    def node(m):
        raw = html.unescape(m.group(2))
        t = one(raw)
        return m.group(0) if t is None else ">" + m.group(1) + E(t, quote=False) + m.group(3) + "<"
    text = re.sub(r">(\s*)([^<>]*?[A-Za-z][^<>]*?)(\s*)<", node, text)
    # 3. attributs simples
    def attr(m):
        t = one(html.unescape(m.group(2)))
        return m.group(0) if t is None else f'{m.group(1)}="{E(t)}"'
    text = re.sub(r'\b(placeholder|title|aria-label|alt|data-for|data-name)="([^"]*)"', attr, text)
    # 4. attributs JSON (textes de l'outil, listes de documents, fêtes, pays)
    def walk(o, depth_row=False):
        if isinstance(o, str):
            t = one(o)
            return o if t is None else t
        if isinstance(o, list):
            return [walk(x) for x in o]
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        return o
    def jattr(m):
        try:
            o = json.loads(html.unescape(m.group(2)))
        except ValueError:
            return m.group(0)
        if m.group(1) == "data-d":
            for g in ("p", "d"):
                for row in o.get(g, {}).values():
                    t = one(row[1])
                    if t:
                        row[1] = t
        else:
            o = walk(o)
        return f'{m.group(1)}="{J(o)}"'
    text = re.sub(r'\b(data-t|data-l|data-e|data-d|data-c)="([^"]*)"', jattr, text)
    return text


def write(site, ctx, pages):
    import protection_itde as PX
    urls = []
    paths = {l: pages[l]["path"] for l in pages}
    itp = PX.PATHS[pages["en"]["path"]]
    paths.update(it=itp[0], de=itp[1])
    for lang, t in pages.items():
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, t["body"], "", paths, ctx))
    en = pages["en"]
    for i, lang in enumerate(("it", "de")):
        one = lambda s: (PX.TR.get(s) or (s,) * 2)[i]
        hero = _tx(f'<h1>{en["h1"]}</h1><p class="hero-lead">{E(en["lead"])}</p>', i)
        urls.append(B.write(site, paths[lang], lang, one(en["title"]), one(en["desc"]), hero, _tx(en["body"], i), "", paths, ctx))
    return urls


def ul(items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def cur_opts():
    return "".join(f"<option{' selected' if c == 'EUR' else ''}>{c}</option>" for c in CURS)


def months_opts(lang):
    import datetime as dt
    d = dt.date.today().replace(day=1)
    out = []
    for i in range(12):
        y, m = d.year + (d.month - 1 + i) // 12, (d.month - 1 + i) % 12 + 1
        out.append(f'<option value="{y}-{m:02d}"{" selected" if i == 1 else ""}>{m:02d}/{y}</option>')
    return "".join(out)


# ---------- 1. Anti-arnaque ----------
def p_arnaque():
    P = {}
    for lang in ("fr", "en"):
        fr = lang == "fr"
        t = dict(err="Choisis un départ et une arrivée dans la liste, un mois et un prix." if fr else "Pick a departure and an arrival from the list, a month and a price.",
                 loading="Comparaison avec les vrais prix…" if fr else "Comparing with real prices…",
                 none="Pas assez de prix connus pour ce trajet ce mois-là : sois encore plus prudent." if fr else "Not enough known prices for this route that month: be extra careful.",
                 v_bad="🔴 Prix anormalement bas : risque d'arnaque" if fr else "🔴 Abnormally low price: scam risk",
                 v_mid="🟡 Très bon prix : vérifie bien le vendeur" if fr else "🟡 Very good price: check the seller carefully",
                 v_good="🟢 Prix cohérent avec le marché" if fr else "🟢 Price in line with the market",
                 l_offer="Prix proposé : {p}" if fr else "Price offered: {p}", l_min="Prix le plus bas trouvé ce mois-ci par les comparateurs : {p}" if fr else "Lowest price found this month by comparison sites: {p}",
                 t_bad="Un billet bien moins cher que tous les prix du marché est presque toujours une arnaque. Ne paie rien avant d'avoir vérifié la réservation sur le site de la compagnie." if fr else "A ticket far cheaper than every market price is almost always a scam. Don't pay anything before checking the booking on the airline's website.",
                 t_mid="Le prix est possible mais très bas : vérifie la réservation sur le site de la compagnie avant de payer, et ne paie jamais par simple transfert." if fr else "The price is possible but very low: check the booking on the airline's site before paying, and never pay by plain transfer.",
                 t_good="Le prix est normal. Vérifie quand même la réservation et le vendeur avant de payer." if fr else "The price is normal. Still check the booking and the seller before paying.",
                 note="Comparaison avec les prix aller-retour trouvés récemment (Aviasales), convertis en euros au taux du jour." if fr else "Compared with round-trip prices recently found (Aviasales), converted to euros at today's rate.")
        flags = (["On te demande de payer par transfert d'argent, mobile money ou crypto à une personne, pas à une agence ou une compagnie.", "Le « vendeur » n'existe que sur WhatsApp, Facebook, TikTok ou Telegram, sans adresse ni site.",
                  "Le prix est beaucoup plus bas que partout ailleurs, ou c'est une « promo » réservée à toi, à payer tout de suite.", "On t'envoie une simple capture d'écran au lieu d'un billet électronique avec un code de réservation.",
                  "Le lien de paiement ne mène pas au vrai site de la compagnie (adresse bizarre, fautes)."] if fr else
                 ["You're asked to pay by money transfer, mobile money or crypto to a person, not to an agency or airline.", "The 'seller' only exists on WhatsApp, Facebook, TikTok or Telegram, with no address or website.",
                  "The price is far lower than anywhere else, or it's a 'special offer' just for you, to pay right now.", "You get a screenshot instead of an e-ticket with a booking reference.",
                  "The payment link doesn't go to the real airline website (odd address, typos)."])
        verify = (["Demande le <strong>code de réservation</strong> (6 lettres et chiffres) et le <strong>numéro de billet</strong> (13 chiffres, les 3 premiers sont le code de la compagnie).",
                   "Va <strong>toi-même</strong> sur le site officiel de la compagnie (pas par le lien reçu), rubrique « Gérer ma réservation », avec le code et ton nom.",
                   "Si la réservation n'apparaît pas, ou si le nom ou les dates ne correspondent pas : ne paie pas.", "Paie de préférence par carte, sur un site connu : en cas de fraude, ta banque peut parfois contester le paiement."] if fr else
                  ["Ask for the <strong>booking reference</strong> (6 letters and numbers) and the <strong>ticket number</strong> (13 digits, the first 3 are the airline code).",
                   "Go <strong>yourself</strong> to the airline's official website (not via the link you received), under 'Manage my booking', with the reference and your name.",
                   "If the booking doesn't show up, or the name or dates don't match: don't pay.", "Pay by card on a well-known site if possible: in case of fraud, your bank can sometimes dispute the payment."])
        report = (["France : <a href=\"https://www.cybermalveillance.gouv.fr/\" target=\"_blank\" rel=\"noopener\">cybermalveillance.gouv.fr</a>", "Nigeria : <a href=\"https://www.efcc.gov.ng/\" target=\"_blank\" rel=\"noopener\">EFCC</a>",
                   "Ailleurs : la police et la plateforme où l'annonce a été publiée (signaler le compte)."] if fr else
                  ["France: <a href=\"https://www.cybermalveillance.gouv.fr/\" target=\"_blank\" rel=\"noopener\">cybermalveillance.gouv.fr</a>", "Nigeria: <a href=\"https://www.efcc.gov.ng/\" target=\"_blank\" rel=\"noopener\">EFCC</a>",
                   "Elsewhere: the police and the platform where the offer was posted (report the account)."])
        lab = (["Départ", "Arrivée", "Mois du voyage", "Prix proposé (aller-retour)", "Monnaie", "Vérifier ce prix", "Ville ou aéroport"] if fr else
               ["From", "To", "Travel month", "Price offered (round trip)", "Currency", "Check this price", "City or airport"])
        body = (f'<form id="ar-form" class="tool-form" novalidate data-t="{J(t)}"><div class="tool-grid">'
                f'<label><span>{lab[0]}</span><input id="ar-from" placeholder="{lab[6]}"></label><label><span>{lab[1]}</span><input id="ar-to" placeholder="{lab[6]}"></label>'
                f'<label><span>{lab[2]}</span><select id="ar-month">{months_opts(lang)}</select></label><label><span>{lab[3]}</span><input id="ar-price" type="number" min="1" inputmode="decimal"></label>'
                f'<label><span>{lab[4]}</span><select id="ar-cur">{cur_opts()}</select></label></div><button class="btn" type="submit">{lab[5]}</button></form><div id="ar-out" aria-live="polite"></div>'
                f'<section><h2>{"Les signes d’une arnaque" if fr else "Signs of a scam"}</h2>{ul([E(x) for x in flags])}</section>'
                f'<section><h2>{"Vérifier un billet avant de payer" if fr else "Check a ticket before paying"}</h2><ol>' + "".join(f"<li>{x}</li>" for x in verify) + "</ol></section>"
                f'<section><h2>{"Signaler une arnaque" if fr else "Report a scam"}</h2>{ul(report)}</section>' + SCRIPTS("fetes", "ac-mini", "arnaque"))
        P[lang] = dict(path="verifier-billet-avion" if fr else "en/check-flight-ticket-scam",
                       title="Billet d'avion : arnaque ou vrai prix ? Vérifie avant de payer | Escale" if fr else "Flight ticket: scam or real price? Check before you pay | Escale",
                       desc="Un agent sur WhatsApp te propose un billet pas cher ? Compare son prix avec les vrais prix du marché, repère les signes d'arnaque et vérifie la réservation avant de payer." if fr else "An agent on WhatsApp offers you a cheap ticket? Compare it with real market prices, spot the scam signs and check the booking before you pay.",
                       h1="Ce billet est-il <span>vrai ?</span>" if fr else "Is this ticket <span>real?</span>",
                       lead="Avant de payer un billet proposé par un agent ou sur les réseaux sociaux : compare son prix avec les vrais prix et vérifie la réservation." if fr else "Before paying for a ticket offered by an agent or on social media: compare its price with real prices and check the booking.", body=body)
    return P


# ---------- 2. Indemnisation des retards ----------
CLAIM = "https://compensair.tpm.lv/9rTXzlp7"


def p_retard():
    P = {}
    for lang in ("fr", "en"):
        fr = lang == "fr"
        t = dict(err="Choisis un départ et une arrivée dans la liste." if fr else "Pick a departure and an arrival from the list.",
                 no_event="Pas d'indemnisation pour un retard de moins de 3 heures à l'arrivée (mais la compagnie doit te prendre en charge : repas, hôtel si besoin)." if fr else "No compensation for an arrival delay under 3 hours (but the airline must look after you: meals, hotel if needed).",
                 no_rule="Ce vol n'est pas couvert par les règles européennes ou britanniques." if fr else "This flight isn't covered by EU or UK rules.",
                 no_rule_txt="Les règles européennes couvrent les vols au départ de l'Union européenne (toute compagnie) et les vols vers l'UE avec une compagnie européenne. Le pays de départ peut avoir ses propres règles : renseigne-toi auprès de la compagnie." if fr else "EU rules cover flights departing the European Union (any airline) and flights to the EU on a European airline. The departure country may have its own rules: ask the airline.",
                 yes="La compagnie te doit peut-être jusqu'à {x} par passager" if fr else "The airline may owe you up to {x} per passenger",
                 maybe="Possible : jusqu'à {x} par passager si la compagnie est européenne" if fr else "Possible: up to {x} per passenger if the airline is European",
                 l_km="Distance du vol : {k} km" if fr else "Flight distance: {k} km",
                 l_eu="Règle européenne (règlement 261/2004)" if fr else "EU rule (Regulation 261/2004)", l_uk="Règle britannique (UK261)" if fr else "UK rule (UK261)",
                 except_="", claim="Réclamer avec Compensair" if fr else "Claim with Compensair",
                 free="Tu peux aussi réclamer gratuitement toi-même avec le formulaire de la compagnie. Un service de réclamation garde une commission si tu gagnes, mais s'occupe de tout. Escale peut toucher une commission via ce lien." if fr else "You can also claim yourself for free with the airline's form. A claims service keeps a commission if you win, but handles everything. Escale may earn a commission through this link.")
        t["except"] = ("Pas d'indemnisation si la compagnie prouve des « circonstances extraordinaires » (météo dangereuse, grève du contrôle aérien, problème de sécurité…). Le montant peut être réduit de moitié si on t'a proposé un autre vol arrivé peu après. Gardé tes cartes d'embarquement et preuves." if fr else
                       "No compensation if the airline proves 'extraordinary circumstances' (dangerous weather, air traffic control strike, security issue…). The amount can be halved if you were rerouted and arrived shortly after. Keep your boarding passes and proof.").replace("Gardé", "Garde")
        del t["except_"]
        lab = (["Départ", "Arrivée", "Compagnie", "Que s'est-il passé ?", "Calculer", "Ville ou aéroport"] if fr else ["From", "To", "Airline", "What happened?", "Calculate", "City or airport"])
        car = ([("eu", "Compagnie européenne (Air France, Brussels Airlines, ITA, TAP…)"), ("uk", "Compagnie britannique (British Airways…)"), ("other", "Autre compagnie (Royal Air Maroc, Turkish, Ethiopian…)"), ("unknown", "Je ne sais pas")] if fr else
               [("eu", "European airline (Air France, Brussels Airlines, ITA, TAP…)"), ("uk", "British airline (British Airways…)"), ("other", "Other airline (Royal Air Maroc, Turkish, Ethiopian…)"), ("unknown", "I don't know")])
        what = ([("delay3", "Arrivé avec 3 heures de retard ou plus"), ("delay", "Arrivé avec moins de 3 heures de retard"), ("cancel", "Vol annulé, prévenu moins de 14 jours avant"), ("denied", "Refusé à l'embarquement (surbooking)")] if fr else
                [("delay3", "Arrived 3 hours late or more"), ("delay", "Arrived less than 3 hours late"), ("cancel", "Flight cancelled, told less than 14 days before"), ("denied", "Denied boarding (overbooking)")])
        sel = lambda i, o: f'<select id="{i}">' + "".join(f'<option value="{v}">{E(n)}</option>' for v, n in o) + "</select>"
        rights = (["Retard de 2 heures ou plus : la compagnie doit fournir repas et rafraîchissements, et un hôtel si tu dois attendre le lendemain.", "Annulation : tu as droit au remboursement du billet ou à un autre vol, en plus de l'indemnisation éventuelle.",
                   "Le délai pour réclamer dépend du pays (souvent plusieurs années) : ne tarde pas.", "Une réforme européenne a été adoptée en 2026 mais ne s'applique pas encore : les règles ci-dessus restent en vigueur."] if fr else
                  ["Delay of 2 hours or more: the airline must provide meals and refreshments, and a hotel if you have to wait until the next day.", "Cancellation: you're entitled to a refund or another flight, on top of any compensation.",
                   "The time limit to claim depends on the country (often several years): don't wait.", "An EU reform was adopted in 2026 but doesn't apply yet: the rules above remain in force."])
        off = ('<p><a href="https://europa.eu/youreurope/citizens/travel/passenger-rights/air/index_' + ("fr" if fr else "en") + '.htm" target="_blank" rel="noopener">' + ("Vos droits de passager aérien (Union européenne)" if fr else "Your air passenger rights (European Union)") +
               '</a> · <a href="https://www.caa.co.uk/passengers/resolving-travel-problems/delays-and-cancellations/" target="_blank" rel="noopener">UK Civil Aviation Authority</a></p>')
        body = (f'<form id="rt-form" class="tool-form" novalidate data-claim="{CLAIM}" data-t="{J(t)}"><div class="tool-grid">'
                f'<label><span>{lab[0]}</span><input id="rt-from" placeholder="{lab[5]}"></label><label><span>{lab[1]}</span><input id="rt-to" placeholder="{lab[5]}"></label>'
                f'<label><span>{lab[2]}</span>{sel("rt-carrier", car)}</label><label><span>{lab[3]}</span>{sel("rt-what", what)}</label></div>'
                f'<button class="btn" type="submit">{lab[4]}</button></form><div id="rt-out" aria-live="polite"></div>'
                f'<section><h2>{"Tes autres droits" if fr else "Your other rights"}</h2>{ul([E(x) for x in rights])}{off}</section>' + SCRIPTS("ac-mini", "retard"))
        P[lang] = dict(path="indemnisation-retard-vol" if fr else "en/flight-delay-compensation",
                       title="Vol retardé ou annulé : jusqu'à 600 € d'indemnisation, calcule ton montant | Escale" if fr else "Flight delayed or cancelled: up to €600 compensation, check your amount | Escale",
                       desc="Retard de plus de 3 heures, annulation ou refus d'embarquement ? Calcule en 30 secondes l'indemnisation prévue par le règlement européen (250, 400 ou 600 €) et réclame-la." if fr else "Delay over 3 hours, cancellation or denied boarding? Check in 30 seconds the compensation under EU rules (€250, €400 or €600) and claim it.",
                       h1="Vol retardé : <span>combien on te doit ?</span>" if fr else "Delayed flight: <span>how much are you owed?</span>",
                       lead="Retard de 3 heures ou plus à l'arrivée, vol annulé ou refus d'embarquement : la compagnie te doit peut-être 250, 400 ou 600 €. Calcule ton montant." if fr else "Arrived 3 hours late or more, flight cancelled or denied boarding: the airline may owe you €250, €400 or €600. Check your amount.", body=body)
    return P


# ---------- 3. Contrôle avant le vol ----------
def p_controle():
    P = {}
    dests = list(V.DEST.items())
    for lang in ("fr", "en"):
        fr = lang == "fr"
        col = 0 if fr else 1
        t = dict(err="Indique au moins la date de départ et la date d'expiration du passeport." if fr else "Enter at least the departure date and the passport expiry date.",
                 name_ok="Le nom sur le billet est exactement celui du passeport." if fr else "The name on the ticket exactly matches the passport.",
                 name_bad="Le nom ne correspond pas : contacte la compagnie ou l'agence MAINTENANT pour le corriger (sinon tu peux être refusé à l'embarquement)." if fr else "The name doesn't match: contact the airline or agency NOW to correct it (otherwise you may be denied boarding).",
                 name_warn="Vérifie que le nom et le prénom du billet sont écrits exactement comme sur le passeport (nom de jeune fille, deuxième prénom…)." if fr else "Check that the surname and first name on the ticket are exactly as on the passport (maiden name, middle name…).",
                 r_sch="espace Schengen : valable au moins 3 mois après le retour" if fr else "Schengen area: valid at least 3 months after you leave",
                 r_whole="valable pendant tout le séjour" if fr else "valid for the whole stay",
                 r_six="beaucoup de pays exigent 6 mois de validité après l'arrivée" if fr else "many countries require 6 months' validity after arrival",
                 exp_ok="Passeport valable jusqu'au {d} : OK ({r})." if fr else "Passport valid until {d}: OK ({r}).",
                 exp_bad="Passeport valable jusqu'au {d} : il faudrait au moins jusqu'au {n} ({r}). Renouvelle-le avant de partir." if fr else "Passport valid until {d}: it should be valid at least until {n} ({r}). Renew it before you travel.",
                 iss_ok="Passeport délivré il y a moins de 10 ans : OK." if fr else "Passport issued less than 10 years ago: OK.",
                 iss_bad="Passeport délivré il y a plus de 10 ans : refusé pour l'espace Schengen." if fr else "Passport issued more than 10 years ago: refused for the Schengen area.",
                 pages_ok="Au moins 2 pages vierges : OK." if fr else "At least 2 blank pages: OK.",
                 pages_warn="Une seule page vierge : certains pays ou visas en demandent 2." if fr else "Only one blank page: some countries or visas require 2.",
                 pages_bad="Aucune page vierge : impossible d'apposer un visa ou des tampons. Renouvelle le passeport." if fr else "No blank page: no room for a visa or stamps. Renew the passport.",
                 v_good="🟢 Tout est en ordre" if fr else "🟢 All good", v_mid="🟡 À vérifier avant de partir" if fr else "🟡 Check before you go", v_bad="🔴 Problème à régler avant le vol" if fr else "🔴 Problem to fix before the flight",
                 visa="Faut-il un visa ?" if fr else "Do I need a visa?",
                 note="Règles générales vérifiées en novembre 2026 : chaque pays peut avoir des exigences en plus. Vérifie toujours sur le site officiel du pays ou auprès de la compagnie." if fr else "General rules checked in November 2026: each country may have extra requirements. Always check the country's official website or with the airline.")
        lab = (["Pays de destination", "Ton passeport", "Date de départ", "Date de retour", "Expiration du passeport", "Date de délivrance (facultatif)", "Pages vierges", "Le nom sur le billet est-il exactement celui du passeport ?", "Vérifier"] if fr else
               ["Destination country", "Your passport", "Departure date", "Return date", "Passport expiry", "Issue date (optional)", "Blank pages", "Is the name on the ticket exactly as on the passport?", "Check"])
        dopt = "".join(f'<option value="{k}">{v[2]} {E(v[col])}</option>' for k, v in dests)
        popt = "".join(f'<option value="{k}">{v[2]} {E(v[col])}</option>' for k, v in V.PASS.items())
        nopt = "".join(f'<option value="{v}">{n}</option>' for v, n in ([("yes", "Oui"), ("unsure", "Je ne suis pas sûr"), ("no", "Non")] if fr else [("yes", "Yes"), ("unsure", "Not sure"), ("no", "No")]))
        body = (f'<form id="cv-form" class="tool-form" novalidate data-t="{J(t)}"><div class="tool-grid">'
                f'<label><span>{lab[0]}</span><select id="cv-dest">{dopt}</select></label><label><span>{lab[1]}</span><select id="cv-pass">{popt}</select></label>'
                f'<label><span>{lab[2]}</span><input id="cv-dep" type="date"></label><label><span>{lab[3]}</span><input id="cv-ret" type="date"></label>'
                f'<label><span>{lab[4]}</span><input id="cv-exp" type="date"></label><label><span>{lab[5]}</span><input id="cv-iss" type="date"></label>'
                f'<label><span>{lab[6]}</span><input id="cv-pages" type="number" min="0" max="40" value="2" inputmode="numeric"></label>'
                f'<label><span>{lab[7]}</span><select id="cv-name">{nopt}</select></label></div><button class="btn" type="submit">{lab[8]}</button></form><div id="cv-out" aria-live="polite"></div>'
                + SCRIPTS("controle"))
        P[lang] = dict(path="controle-avant-vol" if fr else "en/pre-flight-check",
                       title="Contrôle avant le vol : nom, passeport, visa, évite le refus d'embarquement | Escale" if fr else "Pre-flight check: name, passport, visa, avoid being denied boarding | Escale",
                       desc="En 1 minute, vérifie que le nom du billet correspond au passeport, que le passeport est assez valable pour ta destination et s'il te faut un visa. Évite d'être refusé à l'embarquement." if fr else "In 1 minute, check the ticket name matches your passport, your passport is valid long enough for your destination and whether you need a visa. Avoid being denied boarding.",
                       h1="Contrôle <span>avant le vol</span>" if fr else "Pre-flight <span>check</span>",
                       lead="Les deux causes les plus fréquentes de refus à l'embarquement : un nom qui ne correspond pas au passeport, et un passeport pas assez valable. Vérifie en 1 minute." if fr else "The two most common reasons for being denied boarding: a name that doesn't match the passport, and a passport not valid long enough. Check in 1 minute.", body=body)
    return P


# ---------- 4. Sans visa ----------
AIR = {"SCH": "PAR", "GB": "LON", "US": "NYC", "CA": "YMQ", "AE": "DXB", "TR": "IST", "MA": "CMN", "TN": "TUN", "DZ": "ALG", "EG": "CAI", "SN": "DSS", "CI": "ABJ", "ML": "BKO",
       "GN": "CKY", "BF": "OUA", "TG": "LFW", "BJ": "COO", "CM": "DLA", "GA": "LBV", "CD": "FIH", "NG": "LOS", "GH": "ACC", "KE": "NBO", "ET": "ADD", "RW": "KGL", "ZA": "JNB"}


def p_sansvisa():
    P = {}
    R = V.rules()
    data = {"p": {k: [v[0], v[1], v[2]] for k, v in V.PASS.items()}, "d": {k: [v[0], v[1], v[2], AIR[k]] for k, v in V.DEST.items()}, "r": R}
    for lang in ("fr", "en"):
        fr = lang == "fr"
        col = 0 if fr else 1
        t = dict(none="Aucune destination de la liste sans visa pour ce passeport : utilise l'outil visa pour les autres pays." if fr else "No destination on the list without a visa for this passport: use the visa tool for other countries.",
                 s0="Sans visa" if fr else "No visa", s1="Visa électronique ou à l'arrivée" if fr else "e-Visa or visa on arrival",
                 flights="Voir les vols" if fr else "See flights", details="Détails" if fr else "Details", **{"from": "dès" if fr else "from"})
        popt = "".join(f'<option value="{k}">{v[2]} {E(v[col])}</option>' for k, v in V.PASS.items())
        body = (f'<div id="sv-app" data-d="{J(data)}" data-t="{J(t)}"><label class="sv-pick"><span>{"Mon passeport" if fr else "My passport"}</span><select id="sv-pass">{popt}</select></label>'
                f'<p class="small">{"Prix aller-retour du mois prochain depuis" if fr else "Next month round-trip prices from"} <strong class="sv-from">Paris</strong>.</p>'
                f'<ul class="sv-grid" id="sv-grid"></ul></div>'
                f'<p class="small">{"Règles résumées pour un court séjour touristique, vérifiées en " + V.CHECKED[lang] + " : elles changent souvent. Vérifiez toujours sur le site officiel du pays avant de réserver. Les destinations « à vérifier » ne sont pas affichées." if fr else "Rules summarised for a short tourist stay, checked in " + V.CHECKED[lang] + ": they change often. Always check the country official website before booking. Destinations marked “to check” are not shown."}</p>'
                + SCRIPTS("fetes", "sansvisa"))
        P[lang] = dict(path="sans-visa" if fr else "en/visa-free",
                       title="Où partir sans visa avec mon passeport ? Destinations et prix des vols | Escale" if fr else "Where can I go without a visa on my passport? Destinations and flight prices | Escale",
                       desc="Passeport ivoirien, sénégalais, camerounais, nigérian, marocain… : les destinations sans visa ou avec visa à l'arrivée, avec le prix des vols depuis chez toi." if fr else "Ivorian, Senegalese, Cameroonian, Nigerian, Moroccan passport…: visa-free or visa-on-arrival destinations, with flight prices from your city.",
                       h1="Où partir <span>sans visa ?</span>" if fr else "Where to go <span>visa-free?</span>",
                       lead="Choisis ton passeport : Escale affiche les destinations sans visa ou avec visa électronique, avec le prix des vols depuis ton aéroport." if fr else "Pick your passport: Escale shows destinations with no visa or an e-visa, with flight prices from your airport.", body=body)
    return P


# ---------- 5. Calendrier des prix de la diaspora ----------
CTRY = {"CI": ("Côte d'Ivoire", "Côte d'Ivoire", "ABJ"), "SN": ("Sénégal", "Senegal", "DSS"), "CM": ("Cameroun", "Cameroon", "DLA"), "ML": ("Mali", "Mali", "BKO"),
        "BJ": ("Bénin", "Benin", "COO"), "TG": ("Togo", "Togo", "LFW"), "BF": ("Burkina Faso", "Burkina Faso", "OUA"), "GN": ("Guinée", "Guinea", "CKY"), "GA": ("Gabon", "Gabon", "LBV"),
        "CD": ("RD Congo", "DR Congo", "FIH"), "NE": ("Niger", "Niger", "NIM"), "NG": ("Nigeria", "Nigeria", "LOS"), "GH": ("Ghana", "Ghana", "ACC"), "MA": ("Maroc", "Morocco", "CMN"),
        "DZ": ("Algérie", "Algeria", "ALG"), "TN": ("Tunisie", "Tunisia", "TUN")}
MUSL = ["SN", "ML", "GN", "NE", "BF", "MA", "DZ", "TN", "CI", "NG", "CM", "TG", "BJ", "GH"]
NATIONAL = {"CI": ("08", "7 août", "7 Aug"), "SN": ("04", "4 avril", "4 Apr"), "CM": ("05", "20 mai", "20 May"), "ML": ("09", "22 sept.", "22 Sep"), "BJ": ("08", "1er août", "1 Aug"),
            "TG": ("04", "27 avril", "27 Apr"), "BF": ("12", "11 déc.", "11 Dec"), "GN": ("10", "2 oct.", "2 Oct"), "GA": ("08", "17 août", "17 Aug"), "CD": ("06", "30 juin", "30 Jun"),
            "NE": ("08", "3 août", "3 Aug"), "NG": ("10", "1er oct.", "1 Oct"), "GH": ("03", "6 mars", "6 Mar"), "MA": ("07", "fête du Trône, 30 juil.", "Throne Day, 30 Jul"),
            "DZ": ("07", "5 juil.", "5 Jul"), "TN": ("03", "20 mars", "20 Mar")}


def p_calendrier():
    P = {}
    for lang in ("fr", "en"):
        fr = lang == "fr"
        ev = [dict(m=["12", "01"], c=["*"], n="🎄 Noël" if fr else "🎄 Christmas"), dict(m=["07", "08"], c=["*"], n="☀️ Vacances d'été" if fr else "☀️ Summer holidays"),
              dict(m=["03"], c=MUSL, n="🌙 Aïd el-Fitr (≈ 9-10 mars 2027)" if fr else "🌙 Eid al-Fitr (≈ 9-10 Mar 2027)"), dict(m=["05"], c=MUSL, n="🐑 Tabaski (≈ 16-17 mai 2027)" if fr else "🐑 Tabaski (≈ 16-17 May 2027)")]
        for cc, (m, dfr, den) in NATIONAL.items():
            ev.append(dict(m=[m], c=[cc], n=("🇨🇮🇸🇳"[0:0]) + ("Fête nationale (" + dfr + ")" if fr else "National day (" + den + ")")))
        c = {k: [v[0] if fr else v[1], v[2]] for k, v in CTRY.items()}
        t = dict(loading="Lecture du calendrier des prix…" if fr else "Reading the price calendar…", none="Pas encore assez de prix pour ce trajet depuis ton aéroport." if fr else "Not enough prices yet for this route from your airport.",
                 best="Le mois le moins cher : {m}, dès {p} aller-retour." if fr else "Cheapest month: {m}, from {p} round trip.",
                 peaks="Mois les plus chers (pics de prix) : {m}. Pour ces périodes, réserve le plus tôt possible et crée une alerte prix." if fr else "Most expensive months (price peaks): {m}. For these periods, book as early as you can and set a price alert.",
                 flat="Pas de gros pic de prix repéré sur les 12 prochains mois." if fr else "No big price peak spotted over the next 12 months.")
        opt = "".join(f'<option value="{k}">{E(v[0])}</option>' for k, v in c.items())
        body = (f'<div id="cal-app" data-c="{J(c)}" data-e="{J(ev)}" data-t="{J(t)}"><label class="sv-pick"><span>{"Rentrer en" if fr else "Going home to"}</span><select id="cal-c">{opt}</select></label>'
                f'<p class="small">{"Prix aller-retour le plus bas de chaque mois vers la capitale, depuis" if fr else "Lowest round-trip price each month to the main city, from"} <strong class="cal-from">Paris</strong>. '
                f'{"En orange : les pics de prix. En jaune : le mois le moins cher." if fr else "Orange: price peaks. Yellow: cheapest month."}</p>'
                f'<div id="cal-chart" class="mm-chart"></div><div id="cal-tip" class="mm-summary" aria-live="polite"></div></div>'
                f'<p class="small">{"Dates des fêtes religieuses : estimations selon l’observation de la lune. Prix trouvés récemment (Aviasales), ils changent chaque jour." if fr else "Religious holiday dates are estimates based on the moon sighting. Prices recently found (Aviasales), they change every day."}</p>'
                + SCRIPTS("fetes", "calendrier"))
        P[lang] = dict(path="calendrier-prix-diaspora" if fr else "en/diaspora-price-calendar",
                       title="Calendrier des prix pour rentrer au pays : Noël, Tabaski, été, fête nationale | Escale" if fr else "Price calendar to fly home: Christmas, Tabaski, summer, national day | Escale",
                       desc="Côte d'Ivoire, Sénégal, Cameroun, Mali, Maroc… : le prix des billets mois par mois depuis chez toi, les pics de Noël, Tabaski, Aïd et des vacances, et le meilleur moment pour réserver." if fr else "Côte d'Ivoire, Senegal, Cameroon, Nigeria, Ghana…: ticket prices month by month from your city, the Christmas, Tabaski, Eid and holiday peaks, and the best time to book.",
                       h1="Le calendrier des prix <span>pour rentrer au pays</span>" if fr else "The price calendar <span>to fly home</span>",
                       lead="Les prix montent toujours aux mêmes périodes. Vois mois par mois le prix réel depuis ton aéroport, et les fêtes qui font grimper les billets." if fr else "Prices always rise at the same times. See the real price month by month from your airport, and the holidays that push fares up.", body=body)
    return P


# ---------- 6. Acheter ou attendre ----------
def p_attendre():
    P = {}
    for lang in ("fr", "en"):
        fr = lang == "fr"
        t = dict(low="🟢 Bon prix : achète" if fr else "🟢 Good price: buy", mid="🟡 Prix normal" if fr else "🟡 Typical price", high="🔴 Cher : attends si tu peux" if fr else "🔴 Expensive: wait if you can",
                 na="⏳ Pas encore assez de données" if fr else "⏳ Not enough data yet",
                 lowTxt="{x} % de moins que d'habitude (médiane {avg} sur {n} jours relevés)." if fr else "{x}% below usual (median {avg} over {n} days tracked).",
                 midTxt="Proche du prix habituel (médiane {avg} sur {n} jours relevés)." if fr else "Close to the usual price (median {avg} over {n} days tracked).",
                 highTxt="{x} % de plus que d'habitude (médiane {avg}) : crée une alerte prix et attends une baisse." if fr else "{x}% above usual (median {avg}): set a price alert and wait for a drop.",
                 naTxt="Le verdict apparaît après 7 jours de relevés." if fr else "The verdict appears after 7 days of tracking.",
                 none="Données en cours de collecte : reviens dans quelques jours." if fr else "Data being collected: come back in a few days.", **{"from": "dès" if fr else "from"})
        body = (f'<label class="sv-pick"><span>{"Chercher un trajet" if fr else "Search a route"}</span><input id="aa-filter" type="search" placeholder="{"Dakar, Abidjan, Lagos…" if fr else "Lagos, Accra, Dakar…"}"></label>'
                f'<ul class="aa-list" id="aa-list" data-t="{J(t)}"></ul>'
                f'<section><h2>{"Comment ça marche" if fr else "How it works"}</h2>{ul([E(x) for x in (["Escale relève chaque jour le prix aller-retour le plus bas des 6 prochains mois sur ces trajets.", "Le prix du jour est comparé à la médiane des 60 derniers jours : 8 % de moins ou plus donne le verdict.", "Ce n’est pas une prédiction : un prix peut encore baisser ou monter. Pour ne rien rater, crée une alerte prix sur la page du trajet."] if fr else ["Escale records every day the lowest round-trip price over the next 6 months on these routes.", "Today’s price is compared with the median of the last 60 days: 8% lower or higher gives the verdict.", "This is not a forecast: a price can still drop or rise. To miss nothing, set a price alert on the route page."])])}</section>'
                + SCRIPTS("attendre"))
        P[lang] = dict(path="acheter-ou-attendre" if fr else "en/buy-or-wait",
                       title="Billet d'avion : acheter maintenant ou attendre ? Le verdict trajet par trajet | Escale" if fr else "Flight ticket: buy now or wait? The verdict route by route | Escale",
                       desc="Paris → Dakar, Abidjan, Douala, Casablanca, Londres → Lagos… : le prix d'aujourd'hui comparé aux 60 derniers jours. Bon prix, prix normal ou trop cher ?" if fr else "London → Lagos, Accra, Paris → Dakar, Abidjan…: today's price compared with the last 60 days. Good price, typical or too expensive?",
                       h1="Acheter maintenant <span>ou attendre ?</span>" if fr else "Buy now <span>or wait?</span>",
                       lead="Pour les grands trajets de la diaspora, le prix d'aujourd'hui comparé aux 60 derniers jours : bon prix, normal ou trop cher." if fr else "For the main diaspora routes, today's price compared with the last 60 days: good, typical or too expensive.", body=body)
    return P


# ---------- 7. Dossier de visa ----------
def p_dossier():
    P = {}
    for lang in ("fr", "en"):
        fr = lang == "fr"
        L = {"SCH": dict(off="France-Visas (et site du consulat du pays visité)" if fr else "France-Visas (and the consulate of the country you visit)", url="https://france-visas.gouv.fr/",
                         when="Dépôt possible au plus tôt 6 mois avant le départ et au plus tard 15 jours avant. Décision en général sous 15 jours, parfois plus." if fr else "Apply at the earliest 6 months before departure and at the latest 15 days before. Decision usually within 15 days, sometimes longer.",
                         items=[("Formulaire de demande rempli et signé" if fr else "Completed and signed application form", "En ligne sur France-Visas pour la France" if fr else "Online on France-Visas for France"),
                                ("Photo d'identité récente aux normes" if fr else "Recent passport photo meeting the standards", ""),
                                ("Passeport délivré il y a moins de 10 ans" if fr else "Passport issued less than 10 years ago", "Valable au moins 3 mois après le retour, avec au moins 2 pages vierges" if fr else "Valid at least 3 months after return, with at least 2 blank pages"),
                                ("Assurance voyage d'au moins 30 000 €" if fr else "Travel insurance of at least €30,000", "Frais médicaux, hospitalisation et rapatriement, pour tout le séjour" if fr else "Medical costs, hospital and repatriation, for the whole stay"),
                                ("Justificatif d'hébergement" if fr else "Proof of accommodation", "Réservation d'hôtel, attestation d'accueil (France), dichiarazione di ospitalità (Italie)…" if fr else "Hotel booking, 'attestation d'accueil' (France), 'dichiarazione di ospitalità' (Italy)…"),
                                ("Justificatifs de ressources" if fr else "Proof of funds", "Relevés bancaires récents, bulletins de salaire, ou prise en charge par l'hôte" if fr else "Recent bank statements, payslips, or sponsorship by your host"),
                                ("Réservation de vol aller-retour" if fr else "Round-trip flight reservation", "Billet modifiable ou remboursable : ne paie pas un billet non remboursable avant d'avoir le visa" if fr else "Changeable or refundable fare: don't pay a non-refundable ticket before you get the visa"),
                                ("Preuves de ta situation et de ton retour" if fr else "Proof of your situation and return", "Attestation de travail et de congé, inscription scolaire, titre de propriété, famille…" if fr else "Employment and leave letter, school enrolment, property deed, family…"),
                                ("Frais de visa : 90 € (adulte), 45 € (6-12 ans)" if fr else "Visa fee: €90 (adult), €45 (ages 6-12)", "Plus les frais du centre de visa. Non remboursés en cas de refus" if fr else "Plus the visa centre fee. Not refunded if refused")]),
             "GB": dict(off="GOV.UK : Standard Visitor visa", url="https://www.gov.uk/standard-visitor", when="Délais actuels et pièces exactes : voir GOV.UK." if fr else "Current processing times and exact documents: see GOV.UK.",
                        items=[("Demande en ligne sur GOV.UK" if fr else "Online application on GOV.UK", ""), ("Passeport valable pendant tout le séjour" if fr else "Passport valid for the whole stay", ""),
                               ("Justificatifs de ressources" if fr else "Proof of funds", ""), ("Justificatifs du but du voyage et de ta situation" if fr else "Proof of the purpose of your trip and your situation", ""),
                               ("Lettre d'invitation si tu loges chez quelqu'un" if fr else "Invitation letter if you stay with someone", ""), ("Rendez-vous biométrique au centre de visa" if fr else "Biometrics appointment at the visa centre", "")]),
             "US": dict(off="travel.state.gov : visa visiteur" if fr else "travel.state.gov: visitor visa", url="https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html", when="Délais de rendez-vous : voir le site de l'ambassade des États-Unis." if fr else "Appointment wait times: see the US embassy website.",
                        items=[("Formulaire DS-160 en ligne" if fr else "Online DS-160 form", ""), ("Paiement des frais de visa" if fr else "Visa fee payment", ""), ("Rendez-vous et entretien au consulat" if fr else "Consulate appointment and interview", ""),
                               ("Passeport valable" if fr else "Valid passport", ""), ("Photo aux normes" if fr else "Photo meeting the standards", ""), ("Preuves de tes liens avec ton pays" if fr else "Proof of your ties to your home country", "Travail, famille, biens" if fr else "Work, family, property")]),
             "CA": dict(off="Canada.ca : visiter le Canada" if fr else "Canada.ca: visit Canada", url="https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html", when="Délais actuels : voir le site d'IRCC." if fr else "Current processing times: see the IRCC website.",
                        items=[("Demande en ligne (IRCC)" if fr else "Online application (IRCC)", ""), ("Passeport valable" if fr else "Valid passport", ""), ("Justificatifs financiers" if fr else "Proof of funds", ""),
                               ("Lettre d'invitation si tu es reçu" if fr else "Invitation letter if you are hosted", ""), ("Données biométriques" if fr else "Biometrics", ""), ("Preuves de ta situation et de ton retour" if fr else "Proof of your situation and return", "")])}
        L = {k: dict(v, items=[list(x) for x in v["items"]]) for k, v in L.items()}
        letter = ("Je soussigné(e) {host}, demeurant {addr}, {status}, déclare inviter {guest}, né(e) le {birth}, titulaire du passeport n° {passport}, mon/ma {rel}, "
                  "à séjourner à mon domicile du {start} au {end}. Je m'engage à l'héberger pendant toute la durée de son séjour.\n\nFait à {city}, le {date}.\n\nSignature :"
                  if fr else
                  "I, the undersigned {host}, residing at {addr}, {status}, hereby invite {guest}, born on {birth}, holder of passport no. {passport}, my {rel}, "
                  "to stay at my home from {start} to {end}. I undertake to accommodate them for the whole duration of their stay.\n\nDone in {city}, on {date}.\n\nSignature:")
        t = dict(prog="{d} / {n} pièces prêtes" if fr else "{d} / {n} documents ready", letter=letter, copied="Copié ✓" if fr else "Copied ✓")
        mist = (["Des dates ou des montants qui ne correspondent pas entre les documents (billet, hébergement, congé…).", "Des ressources insuffisantes ou des relevés bancaires avec un gros dépôt juste avant la demande.",
                 "Un dossier déposé trop tard : prévois au moins 1 à 2 mois avant le départ.", "Un billet non remboursable acheté avant le visa : en cas de refus, tu perds aussi le billet.",
                 "Des documents traduits ou copiés de mauvaise qualité : fournis des copies lisibles et, si demandé, des traductions."] if fr else
                ["Dates or amounts that don't match between documents (ticket, accommodation, leave…).", "Insufficient funds, or bank statements with a large deposit just before applying.",
                 "Applying too late: plan at least 1 to 2 months before departure.", "A non-refundable ticket bought before the visa: if refused, you lose the ticket too.",
                 "Poor quality copies or translations: provide readable copies and, if asked, translations."])
        dsel = "".join(f'<option value="{k}">{n}</option>' for k, n in [("SCH", "🇪🇺 Espace Schengen (France, Italie, Belgique…)" if fr else "🇪🇺 Schengen area (France, Italy, Belgium…)"), ("GB", "🇬🇧 Royaume-Uni" if fr else "🇬🇧 United Kingdom"), ("US", "🇺🇸 États-Unis" if fr else "🇺🇸 United States"), ("CA", "🇨🇦 Canada")])
        lf = ([("host", "Ton nom complet"), ("addr", "Ton adresse"), ("status", "Ta situation (ex. : titulaire d'un titre de séjour, de nationalité française…)"), ("guest", "Nom complet de l'invité"),
               ("birth", "Sa date de naissance"), ("passport", "Son numéro de passeport"), ("rel", "Lien de parenté (mère, frère, ami…)"), ("start", "Arrivée le"), ("end", "Départ le"), ("city", "Ville"), ("date", "Date du jour")] if fr else
              [("host", "Your full name"), ("addr", "Your address"), ("status", "Your status (e.g. resident permit holder, British citizen…)"), ("guest", "Guest's full name"),
               ("birth", "Their date of birth"), ("passport", "Their passport number"), ("rel", "Relationship (mother, brother, friend…)"), ("start", "Arriving on"), ("end", "Leaving on"), ("city", "City"), ("date", "Today's date")])
        body = (f'<div id="dv-app" data-t="{J(t)}" data-l="{J(L)}"><label class="sv-pick"><span>{"Visa pour" if fr else "Visa for"}</span><select id="dv-dest">{dsel}</select></label>'
                f'<p class="dv-bar" id="dv-bar"></p><ul class="dv-list" id="dv-list"></ul><p class="small" id="dv-when"></p><p class="small">{"Liste officielle et à jour :" if fr else "Official, up-to-date list:"} <span id="dv-off"></span></p></div>'
                f'<section><h2>{"Les erreurs qui font refuser un visa" if fr else "Mistakes that get visas refused"}</h2>{ul([E(x) for x in mist])}</section>'
                f'<section><h2>{"Modèle de lettre d’invitation" if fr else "Invitation letter template"}</h2><p class="small">{"Un modèle simple à adapter. En France, il ne remplace pas l’attestation d’accueil officielle délivrée par la mairie." if fr else "A simple template to adapt. In France it does not replace the official 'attestation d’accueil' from the town hall."}</p>'
                f'<form id="dv-letter" class="tool-form"><div class="tool-grid">' + "".join(f'<label><span>{E(n)}</span><input name="{k}"></label>' for k, n in lf) +
                f'</div><button class="btn" type="submit">{"Créer la lettre" if fr else "Create the letter"}</button></form>'
                f'<div id="dv-letter-out" hidden><textarea rows="10" class="dv-ta" aria-label="Lettre"></textarea><button type="button" class="btn ghost" id="dv-copy">{"Copier" if fr else "Copy"}</button></div></section>'
                + SCRIPTS("dossier"))
        P[lang] = dict(path="dossier-visa" if fr else "en/visa-application-checklist",
                       title="Dossier de visa : la check-list pour éviter le refus (Schengen, Royaume-Uni, USA, Canada) | Escale" if fr else "Visa application checklist: avoid refusal (Schengen, UK, USA, Canada) | Escale",
                       desc="Les pièces à fournir pour un visa Schengen, Royaume-Uni, États-Unis ou Canada, les erreurs qui font refuser un dossier et un modèle de lettre d'invitation." if fr else "Documents needed for a Schengen, UK, US or Canada visa, the mistakes that get applications refused, and an invitation letter template.",
                       h1="Mon dossier <span>de visa</span>" if fr else "My visa <span>application</span>",
                       lead="Près d'un dossier sur deux est refusé pour plusieurs pays africains, et les frais ne sont pas remboursés. Coche chaque pièce et évite les erreurs." if fr else "Nearly one in two applications is refused for several African countries, and fees aren't refunded. Tick off each document and avoid the mistakes.", body=body)
    return P


# ---------- 9. Kit voyage hors ligne ----------
GUIDES = ["abidjan", "accra", "alger", "bamako", "casablanca", "conakry", "dakar", "douala", "kinshasa", "lagos", "lome", "tunis"]
GUIDES_EN = {"alger": "algiers"}


def p_kit():
    P = {}
    for lang in ("fr", "en"):
        fr = lang == "fr"
        t = dict(flight="Vol" if fr else "Flight", code="réservation" if fr else "booking", when="Dates" if fr else "Dates", addr="Adresse sur place" if fr else "Address there", contact="Contact sur place" if fr else "Contact there",
                 emerg="En cas d'urgence" if fr else "Emergency", notes="Notes", card="Mon voyage" if fr else "My trip",
                 saved="Enregistré dans ce navigateur." if fr else "Saved in this browser.", saved_off="Enregistré : cette page et le guide s'ouvrent maintenant sans internet ✓" if fr else "Saved: this page and the guide now open without internet ✓",
                 confirm="Effacer toutes les infos du voyage ?" if fr else "Delete all trip details?")
        gopt = '<option value="">—</option>' + "".join(f'<option value="/{("arriver-aeroport-" + g) if fr else ("en/arriving-at-" + GUIDES_EN.get(g, g) + "-airport")}/">{g.capitalize() if fr else GUIDES_EN.get(g, g).capitalize()}</option>' for g in GUIDES)
        f = ([("dest", "Destination", "input"), ("guide", "Guide « Arriver à l'aéroport »", "guide"), ("flight", "Numéro de vol", "input"), ("code", "Code de réservation", "input"), ("dates", "Dates (aller / retour)", "input"),
              ("addr", "Adresse où tu dors", "text"), ("contact", "Personne à contacter sur place (nom, téléphone)", "text"), ("emerg", "Contact d'urgence (famille, ambassade…)", "text"), ("notes", "Notes (visa, bagages, rendez-vous…)", "text")] if fr else
             [("dest", "Destination", "input"), ("guide", "'Arriving at the airport' guide", "guide"), ("flight", "Flight number", "input"), ("code", "Booking reference", "input"), ("dates", "Dates (out / back)", "input"),
              ("addr", "Address where you stay", "text"), ("contact", "Contact person there (name, phone)", "text"), ("emerg", "Emergency contact (family, embassy…)", "text"), ("notes", "Notes (visa, baggage, appointments…)", "text")])
        fld = lambda k, n, ty: f'<label><span>{E(n)}</span>' + (f'<select name="{k}">{gopt}</select>' if ty == "guide" else f'<textarea name="{k}" rows="2"></textarea>' if ty == "text" else f'<input name="{k}">') + "</label>"
        chk = (["Passeport (et une photo de la page d'identité sur le téléphone)", "Visa ou autorisation électronique, si besoin", "Billet électronique et code de réservation", "Assurance voyage (numéro de contrat et téléphone)", "Adresse du logement et contact sur place", "Un peu d'argent liquide pour l'arrivée", "Chargeur et adaptateur de prise"] if fr else
               ["Passport (and a photo of the ID page on your phone)", "Visa or electronic authorisation, if needed", "E-ticket and booking reference", "Travel insurance (policy number and phone)", "Accommodation address and contact there", "Some cash for arrival", "Charger and plug adapter"])
        body = (f'<div id="kit-card" class="kit-card" hidden></div>'
                f'<form id="kit-form" class="tool-form" data-t="{J(t)}"><div class="tool-grid">' + "".join(fld(*x) for x in f) +
                f'</div><button class="btn" type="submit">{"💾 Enregistrer pour l’utiliser sans internet" if fr else "💾 Save to use without internet"}</button> <button type="button" class="btn ghost" id="kit-clear">{"Effacer" if fr else "Delete"}</button>'
                f'<p class="small" id="kit-msg" role="status"></p></form>'
                f'<p class="small">{"Tes infos restent uniquement dans ce navigateur, sur ton téléphone : rien n’est envoyé à Escale." if fr else "Your details stay only in this browser, on your phone: nothing is sent to Escale."}</p>'
                f'<section><h2>{"À avoir sur soi" if fr else "Keep with you"}</h2>{ul([E(x) for x in chk])}</section>' + SCRIPTS("kit"))
        P[lang] = dict(path="kit-voyage-hors-ligne" if fr else "en/offline-travel-kit",
                       title="Kit voyage hors ligne : tes infos de vol et d'arrivée, même sans internet | Escale" if fr else "Offline travel kit: your flight and arrival details, even without internet | Escale",
                       desc="Vol, code de réservation, adresse, contacts et guide de l'aéroport d'arrivée : enregistre tout sur ton téléphone et consulte-le sans réseau à l'arrivée." if fr else "Flight, booking reference, address, contacts and arrival airport guide: save everything on your phone and read it with no signal on arrival.",
                       h1="Mon kit voyage <span>hors ligne</span>" if fr else "My offline <span>travel kit</span>",
                       lead="À l'arrivée, on n'a souvent ni réseau ni données. Enregistre ici ton vol, ton adresse et tes contacts : la page s'ouvre ensuite sans internet." if fr else "On arrival you often have no signal or data. Save your flight, address and contacts here: the page then opens without internet.", body=body)
    return P


def build(site, ctx):
    urls = []
    for f in (p_arnaque, p_retard, p_controle, p_sansvisa, p_calendrier, p_attendre, p_dossier, p_kit):
        urls += write(site, ctx, f())
    return urls
