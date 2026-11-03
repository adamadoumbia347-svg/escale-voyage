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


# « Payer son billet avec le mobile money » (Orange Money, Wave, MTN MoMo, Moov Money). Faits vérifiés en novembre 2026 :
# carte Visa virtuelle Orange Money en Côte d'Ivoire (lancée le 12/12/2025, créée dans l'appli Max it ; annoncée aussi au Mali et au Sénégal),
# carte virtuelle Wave au Sénégal (janvier 2026), carte Mastercard virtuelle MTN MoMo en Ouganda (février 2025) et au Cameroun (décembre 2025),
# MoovMoney Card en Côte d'Ivoire. Rien n'est affirmé sur une compagnie précise : on renvoie à l'étape de paiement de chaque site.
MOMO = {
    "fr": dict(path="payer-billet-avion-mobile-money", title="Payer son billet d'avion avec Orange Money, Wave ou MTN MoMo | Escale",
               desc="Orange Money, Wave, MTN MoMo, Moov Money : 3 façons de payer un billet d’avion avec le mobile money, la carte virtuelle étape par étape et les pièges à éviter.",
               h1="Payer son billet avec le <span>mobile money</span>",
               lead="Pas de carte bancaire ? Avec Orange Money, Wave, MTN MoMo ou Moov Money, vous pouvez quand même réserver vos vols et vos hôtels en ligne. Voici comment, et ce qu'il faut vérifier.",
               cta="Comparer les vols", checked="Informations vérifiées en novembre 2026. Les offres changent : vérifiez toujours dans l'application de votre opérateur et à l'étape de paiement du site.",
               sections=[
                   ("1. La carte virtuelle de votre portefeuille mobile (la solution la plus simple)", [
                       "<strong>Le principe :</strong> votre opérateur crée une carte Visa ou Mastercard « virtuelle » (un numéro de carte dans l'application), rechargée depuis votre solde mobile money. Elle se paie comme une carte bancaire sur les sites des compagnies et des agences.",
                       "<strong>Orange Money :</strong> carte Visa virtuelle lancée en Côte d'Ivoire en décembre 2025, à créer dans l'application Max it, rechargeable depuis le solde Orange Money. Orange l'a aussi annoncée au Mali et au Sénégal.",
                       "<strong>Wave :</strong> carte virtuelle lancée au Sénégal en janvier 2026, directement dans l'application Wave.",
                       "<strong>MTN MoMo :</strong> carte Mastercard virtuelle « Virtual Card by MoMo » en Ouganda et au Cameroun, liée au portefeuille MoMo, sans compte bancaire.",
                       "<strong>Moov Money :</strong> la MoovMoney Card existe en Côte d'Ivoire pour les paiements.",
                       "<strong>Comment faire :</strong> 1) comparez les prix sur Escale ; 2) notez le prix total ; 3) créez la carte dans l'application de votre opérateur ; 4) rechargez-la du montant du billet (plus une petite marge pour les frais) ; 5) payez sur le site de réservation avec le numéro de la carte virtuelle."]),
                   ("2. Payer directement sur le site d'une compagnie africaine", [
                       "Plusieurs compagnies africaines proposent le mobile money à l'étape de paiement de leur site ou de leur application, en francs CFA ou en monnaie locale.",
                       "Le choix change selon le pays d'où vous payez : regardez les moyens de paiement proposés à la dernière étape, avant de valider.",
                       "Comparez d'abord sur Escale : le même vol est parfois moins cher chez une agence en ligne que sur le site de la compagnie."]),
                   ("3. Passer par une agence de voyage de votre ville", [
                       "Beaucoup d'agences acceptent Orange Money, Wave ou MTN MoMo. Elles peuvent ajouter des frais de service : demandez le prix total avant de payer.",
                       "Montrez-leur le prix trouvé sur Escale : c'est une bonne base pour négocier."]),
                   ("Les pièges à éviter", [
                       "<strong>Plafonds :</strong> les cartes virtuelles ont des limites de paiement (fixées par l'opérateur et la banque centrale). Vérifiez le plafond avant d'acheter plusieurs billets.",
                       "<strong>Frais de change :</strong> un prix affiché en euros ou en dollars est converti ; il peut y avoir des frais. Choisissez si possible un paiement en francs CFA ou dans votre monnaie.",
                       "<strong>Arnaques :</strong> ne payez jamais par transfert mobile money un « agent » trouvé sur WhatsApp ou Facebook qui promet un billet très bon marché. Payez uniquement sur le site officiel de la compagnie, d'une agence connue, ou dans une agence physique.",
                       "<strong>Nom du passager :</strong> il doit être exactement celui du passeport. Gardez le reçu et l'e-mail de confirmation avec le numéro de réservation."])]),
    "en": dict(path="en/pay-flight-mobile-money", title="Pay for a flight with Orange Money, Wave or MTN MoMo | Escale",
               desc="Orange Money, Wave, MTN MoMo, Moov Money: 3 ways to pay for a flight with mobile money, the virtual card step by step, and the traps to avoid.",
               h1="Paying for flights with <span>mobile money</span>",
               lead="No bank card? With Orange Money, Wave, MTN MoMo or Moov Money you can still book flights and hotels online. Here is how, and what to check.",
               cta="Compare flights", checked="Information checked in November 2026. Offers change: always check in your operator's app and at the payment step of the site.",
               sections=[
                   ("1. Your mobile wallet's virtual card (the easiest way)", [
                       "<strong>How it works:</strong> your operator creates a 'virtual' Visa or Mastercard (a card number in the app), topped up from your mobile money balance. You pay with it like a bank card on airline and agency websites.",
                       "<strong>Orange Money:</strong> virtual Visa card launched in Côte d'Ivoire in December 2025, created in the Max it app and topped up from your Orange Money balance. Orange also announced it in Mali and Senegal.",
                       "<strong>Wave:</strong> virtual card launched in Senegal in January 2026, right in the Wave app.",
                       "<strong>MTN MoMo:</strong> Mastercard 'Virtual Card by MoMo' in Uganda and Cameroon, linked to your MoMo wallet, no bank account needed.",
                       "<strong>Moov Money:</strong> the MoovMoney Card exists in Côte d'Ivoire for payments.",
                       "<strong>Step by step:</strong> 1) compare prices on Escale; 2) note the total price; 3) create the card in your operator's app; 4) top it up with the ticket amount (plus a small margin for fees); 5) pay on the booking site with the virtual card number."]),
                   ("2. Pay directly on an African airline's website", [
                       "Several African airlines offer mobile money at the payment step of their website or app, in CFA francs or local currency.",
                       "Options depend on the country you pay from: look at the payment methods offered at the last step, before confirming.",
                       "Compare on Escale first: the same flight is sometimes cheaper with an online agency than on the airline's site."]),
                   ("3. Use a travel agency in your city", [
                       "Many agencies accept Orange Money, Wave or MTN MoMo. They may add service fees: ask for the total price before paying.",
                       "Show them the price you found on Escale: it is a good basis to negotiate."]),
                   ("Traps to avoid", [
                       "<strong>Limits:</strong> virtual cards have payment limits (set by the operator and the central bank). Check the limit before buying several tickets.",
                       "<strong>Exchange fees:</strong> a price in euros or dollars is converted and fees may apply. If you can, pay in CFA francs or your own currency.",
                       "<strong>Scams:</strong> never send mobile money to an 'agent' found on WhatsApp or Facebook promising a very cheap ticket. Pay only on the airline's official site, a well-known agency, or in a physical agency.",
                       "<strong>Passenger name:</strong> it must match the passport exactly. Keep the receipt and the confirmation email with the booking reference."])]),
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
    p_mm = {l: MOMO[l]["path"] for l in MOMO}
    for lang, t in MOMO.items():
        q = "" if lang == "fr" else "?lang=en"
        body = "".join(f'<section><h2>{E(h)}</h2><ul>' + "".join(f"<li>{x}</li>" for x in items) + "</ul></section>" for h, items in t["sections"])
        body += f'<p class="small">{E(t["checked"])}</p><p><a class="btn" href="/{q}">{E(t["cta"])}</a></p>'
        hero = f'<h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": t["title"].split(" | ")[0],
                                                                   "description": t["desc"], "inLanguage": lang, "dateModified": "2026-11-03",
                                                                   "author": {"@type": "Organization", "name": "Escale"}}, ensure_ascii=False) + "</script>"
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, ld, p_mm, ctx))
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
