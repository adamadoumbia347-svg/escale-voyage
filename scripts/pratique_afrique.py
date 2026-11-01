"""Pages pratiques pour la diaspora et les voyageurs africains (français et anglais) :
- « Billet d'avion urgent » (décès, maladie, événement familial) ;
- « Bagages : les compagnies vers l'Afrique » (liens vers les pages officielles, sans chiffres qui changeraient) ;
- « Avis des voyageurs » : témoignages réels envoyés par formulaire (/api/form, « avis »), publiés seulement après relecture
  (liste validée : site/data/avis.json, à compléter à la main avec l'accord du propriétaire du site).
"""
import html
import json

import build_i18n as B

E = html.escape

URGENT = {
    "fr": dict(path="billet-avion-urgent", title="Billet d'avion urgent pour l'Afrique : décès, maladie, famille | Escale",
               desc="Partir vite au pays pour un décès, une maladie ou un événement familial : trouver un vol pour aujourd'hui ou demain, papiers à prévoir, rapatriement du corps.",
               h1="Partir en urgence <span>au pays</span>",
               lead="Un décès, un proche malade, un événement imprévu : les étapes pour trouver un vol rapidement, sans payer plus que nécessaire.",
               sections=[("Trouver un vol pour aujourd'hui ou demain", [
                   "Lancez la <a href=\"/recherche/\">recherche en direct</a> avec la date du jour ou du lendemain : elle compare des dizaines de compagnies et d'agences en même temps.",
                   "Élargissez : un autre aéroport de départ (Paris-Orly, Bruxelles, Lyon…) ou d'arrivée proche peut avoir une place libre ou un prix plus bas.",
                   "Un aller simple d'abord : le retour se réserve plus tard, quand vous connaissez la durée du séjour. Comparez quand même avec un aller-retour modifiable.",
                   "Appelez aussi directement les compagnies qui desservent votre ville : en cas de décès, certaines peuvent aider à trouver une place. Demandez-le, sans le tenir pour acquis."]),
                   ("Les papiers à vérifier avant de partir", [
                   "Passeport valide (souvent 6 mois après la date de retour) et, si vous n'avez pas la nationalité du pays, le visa ou l'e-visa : vérifiez avec l'outil <a href=\"/visa/\">Visa selon mon passeport</a>.",
                   "Titre de séjour en cours de validité pour revenir en Europe : s'il expire bientôt, renseignez-vous avant de partir.",
                   "Carnet de vaccination (fièvre jaune) pour une grande partie de l'Afrique de l'Ouest et centrale."]),
                   ("Rapatriement d'un défunt", [
                   "Le transport d'un corps passe par une entreprise de pompes funèbres spécialisée dans le rapatriement : elle s'occupe des soins, du cercueil adapté, des autorisations et du vol (en fret).",
                   "Le consulat du pays d'origine délivre en général l'autorisation nécessaire (laissez-passer mortuaire) : contactez-le dès le début.",
                   "Vérifiez si le défunt avait une assurance obsèques, une assurance rapatriement (carte bancaire, contrat d'assurance) ou une caisse de solidarité communautaire : elles prennent souvent en charge tout ou partie des frais."]),
                   ("Garder la tête froide sur les prix", [
                   "Les prix montent à la dernière minute : comparez au moins deux ou trois résultats avant de payer.",
                   "Méfiez-vous des intermédiaires qui demandent un paiement par transfert d'argent : réservez directement sur le site de la compagnie ou d'une agence connue."])],
               cta="Chercher un vol maintenant"),
    "en": dict(path="en/urgent-flight-to-africa", title="Urgent flight to Africa: bereavement, illness, family | Escale",
               desc="Need to travel home fast for a death, an illness or a family emergency? How to find a flight for today or tomorrow, documents to check and repatriation.",
               h1="Travelling home <span>urgently</span>",
               lead="A death, a sick relative, an emergency: the steps to find a flight quickly without paying more than you need to.",
               sections=[("Finding a flight for today or tomorrow", [
                   "Run the <a href=\"/recherche/\">live search</a> with today's or tomorrow's date: it compares dozens of airlines and agencies at once.",
                   "Widen the search: another departure airport (London Gatwick, Paris, Brussels…) or a nearby arrival airport may have seats or a lower price.",
                   "Book one way first: the return can be booked later, once you know how long you will stay. Still compare with a flexible return ticket.",
                   "Also call the airlines that fly to your city directly: in case of bereavement, some may help find a seat. Ask, without counting on it."]),
                   ("Documents to check before you go", [
                   "A valid passport (often 6 months beyond your return date) and, if you are not a citizen, the visa or e-visa: check with the <a href=\"/en/visa/\">visa by passport</a> tool.",
                   "A valid residence permit to come back: if it expires soon, check before you leave.",
                   "Vaccination card (yellow fever) for much of West and Central Africa."]),
                   ("Repatriating a loved one", [
                   "Transporting a body goes through a funeral director specialised in repatriation: they handle care, the right coffin, permits and the flight (as cargo).",
                   "The consulate of the home country usually issues the required authorisation: contact them from the start.",
                   "Check whether the deceased had funeral insurance, repatriation cover (bank card, insurance policy) or a community solidarity fund: they often cover all or part of the costs."]),
                   ("Keep a cool head on prices", [
                   "Prices rise at the last minute: compare at least two or three results before paying.",
                   "Beware of middlemen asking for payment by money transfer: book directly with the airline or a well-known agency."])],
               cta="Search a flight now"),
}

AIRLINES = [  # nom, base, dessert surtout (fr, en), site officiel
    ("Air Côte d'Ivoire", "Abidjan", ("Afrique de l'Ouest et centrale, Paris", "West and Central Africa, Paris"), "https://www.aircotedivoire.com/"),
    ("ASKY Airlines", "Lomé", ("Afrique de l'Ouest et centrale", "West and Central Africa"), "https://www.flyasky.com/"),
    ("Air Sénégal", "Dakar", ("Afrique de l'Ouest, Europe", "West Africa, Europe"), "https://www.flyairsenegal.com/"),
    ("Air Peace", "Lagos", ("Nigeria, Afrique de l'Ouest, Londres", "Nigeria, West Africa, London"), "https://www.flyairpeace.com/"),
    ("RwandAir", "Kigali", ("Afrique de l'Est et centrale", "East and Central Africa"), "https://www.rwandair.com/"),
    ("Kenya Airways", "Nairobi", ("Afrique de l'Est et au-delà", "East Africa and beyond"), "https://www.kenya-airways.com/"),
    ("Ethiopian Airlines", "Addis-Abeba", ("Toute l'Afrique, Europe, Amériques, Asie", "All of Africa, Europe, the Americas, Asia"), "https://www.ethiopianairlines.com/"),
    ("Royal Air Maroc", "Casablanca", ("Maroc, Afrique de l'Ouest et centrale, Europe", "Morocco, West and Central Africa, Europe"), "https://www.royalairmaroc.com/"),
    ("Air Algérie", "Alger", ("Algérie, Europe, Afrique", "Algeria, Europe, Africa"), "https://www.airalgerie.dz/"),
    ("Tunisair", "Tunis", ("Tunisie, Europe, Afrique", "Tunisia, Europe, Africa"), "https://www.tunisair.com/"),
    ("EgyptAir", "Le Caire", ("Égypte, Afrique, Moyen-Orient", "Egypt, Africa, Middle East"), "https://www.egyptair.com/"),
    ("Air France", "Paris", ("Afrique de l'Ouest et centrale, Maghreb", "West and Central Africa, North Africa"), "https://www.airfrance.fr/"),
    ("Brussels Airlines", "Bruxelles", ("Afrique de l'Ouest, centrale et de l'Est", "West, Central and East Africa"), "https://www.brusselsairlines.com/"),
    ("Corsair", "Paris", ("Abidjan, Bamako, Cotonou, Douala, Antilles, Réunion", "Abidjan, Bamako, Cotonou, Douala, Caribbean, Réunion"), "https://www.flycorsair.com/"),
    ("Turkish Airlines", "Istanbul", ("Toute l'Afrique via Istanbul", "All of Africa via Istanbul"), "https://www.turkishairlines.com/"),
    ("Emirates", "Dubaï", ("Afrique via Dubaï", "Africa via Dubai"), "https://www.emirates.com/"),
    ("Qatar Airways", "Doha", ("Afrique via Doha", "Africa via Doha"), "https://www.qatarairways.com/"),
    ("TAP Air Portugal", "Lisbonne", ("Afrique lusophone et de l'Ouest", "Portuguese-speaking and West Africa"), "https://www.flytap.com/"),
    ("Iberia", "Madrid", ("Maroc, Sénégal, Afrique de l'Ouest", "Morocco, Senegal, West Africa"), "https://www.iberia.com/"),
    ("ITA Airways", "Rome", ("Afrique du Nord et de l'Ouest", "North and West Africa"), "https://www.ita-airways.com/"),
    ("Transavia", "Paris / Amsterdam", ("Maroc, Algérie, Tunisie, Sénégal", "Morocco, Algeria, Tunisia, Senegal"), "https://www.transavia.com/"),
]
BAG = {
    "fr": dict(path="bagages-compagnies-afrique", title="Bagages vers l'Afrique : la franchise de chaque compagnie | Escale",
               desc="Combien de kilos et de valises vers l'Afrique ? Air Côte d'Ivoire, ASKY, Air Sénégal, Royal Air Maroc, Ethiopian, Turkish, Air France… liens officiels et conseils.",
               h1="Bagages vers l'Afrique : <span>compagnie par compagnie</span>",
               lead="Combien de valises et de kilos pour votre voyage ? Voici où trouver la règle exacte de chaque compagnie, et comment ne pas payer trop cher.",
               why="Pourquoi pas de chiffres ici ? La franchise dépend du tarif choisi (Light, Standard, Flex…), de la classe et de la ligne, et les compagnies la changent souvent. Un chiffre faux peut vous coûter cher au comptoir : la règle qui compte est celle écrite dans votre réservation.",
               th=("Compagnie", "Basée à", "Dessert surtout", "Règles bagages"), go="Site officiel",
               tips_h="Nos conseils", tips=["Regardez la franchise <strong>avant</strong> de comparer deux billets : un billet moins cher sans valise peut finir plus cher.",
                    "La plupart des compagnies limitent un bagage en soute à 23 kg en classe économique ; au-delà, il y a un supplément, et un bagage trop lourd (souvent plus de 32 kg) peut être refusé.",
                    "Achetez le bagage supplémentaire en ligne, avant le jour du départ : c'est en général moins cher qu'à l'aéroport.",
                    "Pesez vos valises à la maison avec un pèse-bagage, et gardez quelques kilos de marge.",
                    "Calculez le vrai prix avec bagages grâce au <a href=\"/#calc\">calculateur du site</a> et au guide <a href=\"/guides/bagages-avion/\">Bagages : ne pas payer plus cher</a>."]),
    "en": dict(path="en/baggage-allowance-africa-airlines", title="Baggage to Africa: each airline's allowance | Escale",
               desc="How many bags and kilos to Africa? Ethiopian, Kenya Airways, RwandAir, ASKY, Royal Air Maroc, Turkish, Emirates, British routes… official links and tips.",
               h1="Baggage to Africa: <span>airline by airline</span>",
               lead="How many suitcases and kilos for your trip? Here is where to find each airline's exact rule, and how to avoid paying too much.",
               why="Why no figures here? The allowance depends on the fare (Light, Standard, Flex…), the cabin and the route, and airlines change it often. A wrong figure can cost you at the desk: the rule that counts is the one written in your booking.",
               th=("Airline", "Based in", "Mainly flies to", "Baggage rules"), go="Official website",
               tips_h="Our tips", tips=["Check the allowance <strong>before</strong> comparing two tickets: a cheaper fare without a suitcase can end up more expensive.",
                    "Most airlines limit a checked bag to 23 kg in economy; above that there is a fee, and a very heavy bag (often over 32 kg) can be refused.",
                    "Buy extra baggage online before the day of travel: it is usually cheaper than at the airport.",
                    "Weigh your bags at home with a luggage scale and keep a few kilos of margin.",
                    "Work out the real price with bags using the <a href=\"/?lang=en#calc\">site's calculator</a> and the guide <a href=\"/en/guides/\">on baggage</a>."]),
}

AVIS = {
    "fr": dict(path="avis-voyageurs", title="Avis des voyageurs : leurs vols vers l'Afrique | Escale",
               desc="Témoignages de voyageurs de la diaspora : trajet, prix payé, compagnie et conseils. Racontez aussi votre voyage pour aider les autres.",
               h1="Avis des <span>voyageurs</span>", lead="De vrais voyages racontés par la diaspora : le trajet, le prix payé, la compagnie et le conseil qu'ils donneraient. Chaque avis est relu avant publication.",
               list_h="Leurs voyages", empty="Pas encore d'avis publié : soyez le premier à raconter votre voyage !",
               form_h="Racontez votre voyage", f=dict(prenom="Prénom", ville="Votre ville", trajet="Trajet (ex. Paris → Abidjan)", compagnie="Compagnie", prix="Prix payé aller-retour (€)", mois="Mois du voyage",
                   note="Note de votre voyage", texte="Votre conseil ou votre expérience", email="E-mail (jamais publié, seulement si nous avons une question)",
                   consent="J'accepte que mon prénom, ma ville et mon témoignage soient publiés sur Escale après relecture. Mon e-mail n'est jamais publié.", send="Envoyer mon avis"),
               note="Escale publie les avis tels quels après relecture (sans les modifier, sauf fautes de frappe), sans contrepartie. Les avis ne sont ni achetés ni rédigés par Escale."),
    "en": dict(path="en/traveller-reviews", title="Traveller reviews: their flights to Africa | Escale",
               desc="Reviews from diaspora travellers: route, price paid, airline and tips. Share your trip too, to help others.",
               h1="Traveller <span>reviews</span>", lead="Real trips shared by the diaspora: the route, the price paid, the airline and the tip they would give. Each review is read before publication.",
               list_h="Their trips", empty="No reviews published yet: be the first to share your trip!",
               form_h="Share your trip", f=dict(prenom="First name", ville="Your city", trajet="Route (e.g. London → Lagos)", compagnie="Airline", prix="Round-trip price paid (€ or your currency)", mois="Month of travel",
                   note="Rating", texte="Your tip or experience", email="Email (never published, only if we have a question)",
                   consent="I agree that my first name, city and review are published on Escale after reading. My email is never published.", send="Send my review"),
               note="Escale publishes reviews as written after reading (no edits except typos), with nothing in return. Reviews are never bought or written by Escale."),
}


def build(site, ctx):
    urls = []
    p_urg = {l: URGENT[l]["path"] for l in URGENT}
    for lang, t in URGENT.items():
        q = "" if lang == "fr" else "?lang=en"
        body = "".join(f'<section><h2>{E(h)}</h2><ul>' + "".join(f"<li>{x}</li>" for x in items) + "</ul></section>" for h, items in t["sections"])
        body += f'<p><a class="btn" href="/recherche/">{E(t["cta"])}</a> <a class="btn ghost" href="/{q}">Escale</a></p>'
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, "", p_urg, ctx))
    p_bag = {l: BAG[l]["path"] for l in BAG}
    for lang, t in BAG.items():
        col = 0 if lang == "fr" else 1
        rows = "".join(f'<tr><th scope="row">{E(n)}</th><td>{E(base)}</td><td>{E(serv[col])}</td><td><a class="price-go" href="{u}" target="_blank" rel="noopener">{E(t["go"])} ↗</a></td></tr>' for n, base, serv, u in AIRLINES)
        body = (f'<p class="small">ℹ️ {E(t["why"])}</p><div class="bt-wrap"><table class="hub-table"><thead><tr>' + "".join(f'<th scope="col">{E(x)}</th>' for x in t["th"]) +
                f'</tr></thead><tbody>{rows}</tbody></table></div><section><h2>{E(t["tips_h"])}</h2><ul>' + "".join(f"<li>{x}</li>" for x in t["tips"]) + "</ul></section>")
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, "", p_bag, ctx))
    # Avis : liste validée (site/data/avis.json) + formulaire
    try:
        avis = json.loads((site / "data" / "avis.json").read_text(encoding="utf-8"))
    except Exception:
        avis = []
    p_avis = {l: AVIS[l]["path"] for l in AVIS}
    for lang, t in AVIS.items():
        f = t["f"]
        items = "".join(
            f'<li class="avis"><p class="avis-head"><strong>{E(a.get("prenom", ""))}</strong>, {E(a.get("ville", ""))} · {E(a.get("trajet", ""))}'
            + (f' · {E(a["compagnie"])}' if a.get("compagnie") else "") + (f' · {E(a["prix"])}' if a.get("prix") else "") + (f' · {E(a["mois"])}' if a.get("mois") else "")
            + (f' · {"★" * int(a["note"])}' if str(a.get("note", "")).isdigit() else "") + f'</p><p>{E(a.get("texte", ""))}</p></li>' for a in avis)
        lst = f'<ul class="avis-list">{items}</ul>' if avis else f'<p>{E(t["empty"])}</p>'
        stars = "".join(f'<option value="{n}">{"★" * n}</option>' for n in (5, 4, 3, 2, 1))
        form = (f'<form class="nl avis-form" name="avis" method="POST" action="/api/form"><input type="hidden" name="form-name" value="avis"><input type="hidden" name="langue" value="{lang}">'
                f'<p class="hp" hidden><label>Ne pas remplir <input name="site-web" tabindex="-1" autocomplete="off"></label></p>'
                f'<div class="avis-grid"><label><span>{E(f["prenom"])}</span><input name="prenom" required maxlength="40" autocomplete="given-name"></label>'
                f'<label><span>{E(f["ville"])}</span><input name="ville" required maxlength="60"></label>'
                f'<label><span>{E(f["trajet"])}</span><input name="trajet" required maxlength="80"></label>'
                f'<label><span>{E(f["compagnie"])}</span><input name="compagnie" maxlength="60"></label>'
                f'<label><span>{E(f["prix"])}</span><input name="prix" maxlength="30" inputmode="numeric"></label>'
                f'<label><span>{E(f["mois"])}</span><input name="mois" maxlength="30"></label>'
                f'<label><span>{E(f["note"])}</span><select name="note">{stars}</select></label></div>'
                f'<label><span>{E(f["texte"])}</span><textarea name="texte" required maxlength="1200" rows="5"></textarea></label>'
                f'<label><span>{E(f["email"])}</span><input type="email" name="email" maxlength="120" autocomplete="email"></label>'
                f'<label class="consent"><input type="checkbox" name="consent" value="oui" required> {E(f["consent"])}</label>'
                f'<button class="btn" type="submit">{E(f["send"])}</button></form>')
        body = (f'<section><h2>{E(t["list_h"])}</h2>{lst}</section><section><h2>{E(t["form_h"])}</h2>{form}<p class="small">{E(t["note"])}</p></section>')
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, "", p_avis, ctx))
    # Page de remerciement (non référencée : pas dans le sitemap)
    B.write(site, "avis-voyageurs/merci", "fr", "Merci pour votre avis | Escale", "Merci pour votre avis.",
            "<h1>Merci <span>pour votre avis</span></h1><p class=\"hero-lead\">Il sera relu puis publié sur Escale. Thank you: your review will be read and then published.</p>",
            '<p><a class="btn" href="/avis-voyageurs/">Retour aux avis</a> <a class="btn ghost" href="/">Escale</a></p>', "", {"fr": "avis-voyageurs/merci"}, ctx)
    return urls
