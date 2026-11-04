"""« Escale pour les agences » : page d'offre (fr, en) avec formulaire de demande (/api/form, form-name=agence)
et une page par agence partenaire validée (site/data/agences.json → /agence/<slug>/).

Le visiteur de la page d'une agence compare les vrais prix (moteur Escale, liens partenaires d'Escale) et peut, s'il préfère payer
en mobile money ou en agence, écrire à l'agence sur WhatsApp avec le trajet choisi. Escale ne touche jamais à l'argent.
La page d'exemple (« demo ») n'est pas référencée (noindex) et le dit clairement.
"""
import html
import json

import build_i18n as B

E = html.escape
J = lambda o: E(json.dumps(o, ensure_ascii=False))

OFFER = {
    "fr": dict(path="pour-les-agences", title="Escale pour les agences de voyage : votre page de comparaison gratuite | Escale",
               desc="Agence de voyage à Abidjan, Dakar, Douala ou ailleurs ? Recevez une page Escale à votre nom : vos clients comparent les vrais prix et vous contactent sur WhatsApp pour payer en mobile money. Gratuit.",
               h1="Escale pour <span>les agences</span>", lead="Une page à votre nom, gratuite : vos clients comparent les vrais prix des vols depuis votre ville, puis vous écrivent sur WhatsApp pour réserver et payer chez vous.",
               why_h="Ce que votre agence y gagne", why=["Une page professionnelle à partager à vos clients (WhatsApp, Facebook, carte de visite), sans site à créer.",
                   "Les vrais prix des compagnies et des agences en ligne, mis à jour en continu : vos clients vous font confiance.",
                   "Un bouton WhatsApp qui vous envoie directement le trajet et les dates choisis par le client.",
                   "Vos moyens de paiement mis en avant : Orange Money, Wave, MTN MoMo, Moov Money, espèces en agence…", "C'est gratuit, sans engagement."],
               how_h="Comment ça marche", how=["Vous remplissez le formulaire ci-dessous.", "Escale vous contacte pour vérifier vos informations et créer votre page.",
                   "Vous recevez votre lien (escale.live/agence/votre-nom) à partager à vos clients."],
               demo="Voir un exemple de page d'agence", form_h="Demander ma page", f=dict(agence="Nom de l'agence", ville="Ville", pays="Pays", aeroport="Aéroport principal (ex. ABJ, DSS, DLA)",
                   nom="Votre nom", whatsapp="WhatsApp de l'agence (avec l'indicatif, ex. +225…)", email="E-mail", site="Site ou page Facebook (facultatif)",
                   paiements="Moyens de paiement acceptés (ex. Orange Money, Wave, espèces)", message="Message (facultatif)",
                   consent="J'accepte qu'Escale me contacte au sujet de cette demande. Mes coordonnées ne sont utilisées que pour cela.", send="Envoyer ma demande"),
               note="Escale est un comparateur : les réservations faites en ligne depuis la page passent par les sites partenaires d'Escale. Les clients qui vous contactent sur WhatsApp réservent et paient directement chez vous.",
               thanks_t="Merci, demande reçue | Escale", thanks="Merci ! Votre demande a bien été reçue. Escale vous contacte rapidement pour créer votre page."),
    "en": dict(path="en/for-travel-agencies", title="Escale for travel agencies: your free comparison page | Escale",
               desc="Travel agency in Lagos, Accra, Abidjan or elsewhere? Get an Escale page in your name: clients compare real prices and contact you on WhatsApp to pay by mobile money. Free.",
               h1="Escale for <span>travel agencies</span>", lead="A free page in your name: your clients compare real flight prices from your city, then message you on WhatsApp to book and pay with you.",
               why_h="What your agency gets", why=["A professional page to share with your clients (WhatsApp, Facebook, business card), with no website to build.",
                   "Real airline and online agency prices, updated continuously: your clients trust you.", "A WhatsApp button that sends you the route and dates chosen by the client.",
                   "Your payment methods highlighted: mobile money, cash at the agency…", "It's free, with no commitment."],
               how_h="How it works", how=["Fill in the form below.", "Escale contacts you to check your details and create your page.", "You get your link (escale.live/agence/your-name) to share with your clients."],
               demo="See an example agency page", form_h="Request my page", f=dict(agence="Agency name", ville="City", pays="Country", aeroport="Main airport (e.g. LOS, ACC, ABJ)",
                   nom="Your name", whatsapp="Agency WhatsApp (with country code, e.g. +234…)", email="Email", site="Website or Facebook page (optional)",
                   paiements="Payment methods accepted (e.g. mobile money, cash)", message="Message (optional)",
                   consent="I agree that Escale may contact me about this request. My details are used only for this.", send="Send my request"),
               note="Escale is a comparison site: bookings made online from the page go through Escale's partner sites. Clients who contact you on WhatsApp book and pay directly with you.",
               thanks_t="Thank you, request received | Escale", thanks="Thank you! Your request has been received. Escale will contact you soon to create your page."),
}

AG_T = {
    "fr": dict(err="Choisis le départ, l'arrivée et la date.", none="Bons plans en cours de chargement… Utilisez la recherche ci-dessus.", online="Réserver en ligne", agency="Réserver avec l'agence",
               wa_trip="Bonjour, je cherche un billet {a} → {b}, départ le {d}. Pouvez-vous m'aider ?", wa_deal="Bonjour, j'ai vu sur votre page Escale : {a} → {b}, départ le {d}, dès {p}. Pouvez-vous me le réserver ?"),
    "en": dict(err="Choose departure, arrival and date.", none="Loading deals… Use the search above.", online="Book online", agency="Book with the agency",
               wa_trip="Hello, I'm looking for a ticket {a} → {b}, leaving on {d}. Can you help me?", wa_deal="Hello, I saw on your Escale page: {a} → {b}, leaving on {d}, from {p}. Can you book it for me?"),
}


def agency_page(site, ctx, a):
    lang = a.get("langue", "fr") if a.get("langue") in ("fr", "en") else "fr"
    fr = lang == "fr"
    t = AG_T[lang]
    waurl = "https://wa.me/" + "".join(ch for ch in a.get("whatsapp", "") if ch.isdigit()) if a.get("whatsapp") else ""
    pay = "".join(f'<li>{E(p)}</li>' for p in a.get("paiements", []))
    demo = ('<p class="ag-demo">' + ("⚠️ Ceci est un exemple de page d'agence partenaire, pas une vraie agence." if fr else "⚠️ This is an example partner agency page, not a real agency.") +
            f' <a href="/{OFFER[lang]["path"]}/">{"Demander la page de votre agence" if fr else "Request your agency page"}</a></p>') if a.get("demo") else ""
    lab = (["Départ", "Arrivée", "Date de départ", "Date de retour", "Passagers", "Comparer les prix", "Envoyer ce trajet à l'agence", "Ville ou aéroport"] if fr else
           ["From", "To", "Departure date", "Return date", "Passengers", "Compare prices", "Send this route to the agency", "City or airport"])
    contact = ""
    if waurl:
        contact += f'<a class="btn wa-btn" href="{E(waurl)}" target="_blank" rel="noopener">💬 WhatsApp</a> '
    if a.get("email"):
        contact += f'<a class="btn ghost" href="mailto:{E(a["email"])}">✉️ {E(a["email"])}</a>'
    info = "".join(f"<p>{x}</p>" for x in [(("🕘 " + E(a["horaires"])) if a.get("horaires") else ""), (("📍 " + E(a["adresse"])) if a.get("adresse") else "")] if x)
    body = (demo +
            f'<div id="ag-app" data-a="{J({"aeroport": a["aeroport"], "whatsapp": a.get("whatsapp", "")})}" data-t="{J(t)}">'
            f'<form id="ag-form" class="tool-form" novalidate><div class="tool-grid"><label><span>{lab[0]}</span><input id="ag-from" placeholder="{lab[7]}"></label>'
            f'<label><span>{lab[1]}</span><input id="ag-to" placeholder="{lab[7]}"></label><label><span>{lab[2]}</span><input id="ag-dep" type="date"></label>'
            f'<label><span>{lab[3]}</span><input id="ag-ret" type="date"></label><label><span>{lab[4]}</span><input id="ag-pax" type="number" min="1" max="9" value="1"></label></div>'
            f'<div class="pr-btns"><button class="btn" type="submit">{lab[5]}</button>' + (f'<a class="btn wa-btn" id="ag-wa" href="{E(waurl)}">💬 {lab[6]}</a>' if waurl else "") +
            f'</div><p class="small" id="ag-msg" role="status"></p></form>'
            f'<section><h2>{("Bons plans du mois prochain depuis " if fr else "Next month deals from ") + E(a["ville"])}</h2><ul class="ag-deals" id="ag-deals"></ul></section></div>'
            f'<section class="ag-info"><h2>{"L’agence" if fr else "The agency"}</h2><p>{E(a.get("message", ""))}</p>' + info +
            (f'<h3>{"Paiements acceptés" if fr else "Payment methods"}</h3><ul class="ag-pay">{pay}</ul>' if pay else "") + f'<p class="pr-btns">{contact}</p></section>'
            f'<p class="small">{"Page proposée par Escale, comparateur de vols. Les prix sont ceux trouvés récemment par nos partenaires ; ils se confirment au moment de réserver. Escale ne touche jamais à l’argent." if fr else "Page provided by Escale, flight comparison site. Prices are those recently found by our partners; they are confirmed when booking. Escale never handles money."}</p>'
            '<script src="/ac-mini.js" defer></script><script src="/agence.js" defer></script>')
    hero = f'<p class="eyebrow">✈️ {"Agence partenaire Escale" if fr else "Escale partner agency"}</p><h1>{E(a["nom"])} <span>· {E(a["ville"])}</span></h1><p class="hero-lead">{E(("Vols pas chers depuis " if fr else "Cheap flights from ") + a["ville"] + (" : comparez, puis réservez en ligne ou avec l’agence." if fr else ": compare, then book online or with the agency."))}</p>'
    path = f'agence/{a["slug"]}'
    url = B.write(site, path, lang, f'{a["nom"]} ({a["ville"]}) : vols pas chers, réservation en mobile money | Escale' if fr else f'{a["nom"]} ({a["ville"]}): cheap flights | Escale',
                  (f"Comparez les prix des vols depuis {a['ville']} et réservez avec {a['nom']} : " + ", ".join(a.get("paiements", [])) + "." if fr else f"Compare flight prices from {a['ville']} and book with {a['nom']}."),
                  hero, body, "", {lang: path}, ctx)
    if a.get("demo"):  # page d'exemple : pas dans Google ni dans le sitemap
        p = site / path / "index.html"
        p.write_text(p.read_text(encoding="utf-8").replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1), encoding="utf-8")
        return None
    return url


def build(site, ctx):
    urls = []
    paths = {l: OFFER[l]["path"] for l in OFFER}
    data = json.loads((site / "data" / "agences.json").read_text(encoding="utf-8"))
    demo = next((a for a in data["agences"] if a.get("demo")), None)
    for lang, t in OFFER.items():
        f = t["f"]
        inp = lambda k, req=False, ty="text": f'<label><span>{E(f[k])}</span><input name="{k}" type="{ty}"{" required" if req else ""} maxlength="200"></label>'
        form = (f'<form class="nl tool-form" name="agence" method="POST" action="/api/form"><input type="hidden" name="form-name" value="agence"><input type="hidden" name="langue" value="{lang}">'
                f'<p class="hp" hidden><label>Ne pas remplir <input name="site-web" tabindex="-1" autocomplete="off"></label></p><div class="tool-grid">'
                + inp("agence", True) + inp("ville", True) + inp("pays", True) + inp("aeroport") + inp("nom") + inp("whatsapp", ty="tel") + inp("email", ty="email") + inp("site") + inp("paiements") +
                f'</div><label class="tool-grid-full"><span>{E(f["message"])}</span><textarea name="message" rows="3" maxlength="1000"></textarea></label>'
                f'<label class="consent"><input type="checkbox" name="consent" value="oui" required> {E(f["consent"])}</label><button class="btn" type="submit">{E(f["send"])}</button></form>')
        body = (f'<section><h2>{E(t["why_h"])}</h2><ul>' + "".join(f"<li>{E(x)}</li>" for x in t["why"]) + "</ul></section>"
                f'<section><h2>{E(t["how_h"])}</h2><ol>' + "".join(f"<li>{E(x)}</li>" for x in t["how"]) + "</ol>"
                + (f'<p><a class="btn ghost" href="/agence/{demo["slug"]}/">👀 {E(t["demo"])}</a></p>' if demo else "") + "</section>"
                f'<section><h2>{E(t["form_h"])}</h2>{form}<p class="small">{E(t["note"])}</p></section>')
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, "", paths, ctx))
    t = OFFER["fr"]
    B.write(site, "pour-les-agences/merci", "fr", t["thanks_t"], t["thanks"], f'<h1>Merci <span>!</span></h1><p class="hero-lead">{E(t["thanks"])} {E(OFFER["en"]["thanks"])}</p>',
            '<p><a class="btn" href="/">Escale</a></p>', "", {"fr": "pour-les-agences/merci"}, ctx)
    for a in data["agences"]:
        u = agency_page(site, ctx, a)
        if u:
            urls.append(u)
    return urls
