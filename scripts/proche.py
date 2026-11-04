"""Page « Fais venir un proche / Paye pour moi » (fr, en).

Le proche (au pays) choisit un vol réel et l'envoie sur WhatsApp à la personne qui paie ; celle-ci ouvre le lien,
voit le même vol et le prix actuel, puis réserve chez le partenaire (site/proche.js). Escale ne touche jamais à l'argent.
Check-list vérifiée en novembre 2026 (plusieurs sources concordantes ; liens vers les sites officiels) :
visa Schengen 90 € (adulte) / 45 € (6-12 ans) depuis juin 2024, assurance d'au moins 30 000 €,
France : attestation d'accueil en mairie (cerfa 10798, timbre fiscal 30 €), Italie : dichiarazione di ospitalità / invito,
Belgique : engagement de prise en charge (annexe 3bis) à la commune.
"""
import html
import json

import build_i18n as B

E = html.escape

FROM = [["ABJ", "Abidjan", "🇨🇮"], ["DSS", "Dakar", "🇸🇳"], ["DLA", "Douala", "🇨🇲"], ["BKO", "Bamako", "🇲🇱"], ["CKY", "Conakry", "🇬🇳"],
        ["OUA", "Ouagadougou", "🇧🇫"], ["LFW", "Lomé", "🇹🇬"], ["COO", "Cotonou", "🇧🇯"], ["FIH", "Kinshasa", "🇨🇩"], ["NSI", "Yaoundé", "🇨🇲"],
        ["LBV", "Libreville", "🇬🇦"], ["CMN", "Casablanca", "🇲🇦"], ["ALG", "Alger", "🇩🇿"], ["TUN", "Tunis", "🇹🇳"], ["LOS", "Lagos", "🇳🇬"], ["ACC", "Accra", "🇬🇭"]]
TO = {"fr": [["PAR", "Paris"], ["MIL", "Milan"], ["ROM", "Rome"], ["BRU", "Bruxelles"], ["LYS", "Lyon"], ["MRS", "Marseille"], ["TLS", "Toulouse"],
             ["GVA", "Genève"], ["LON", "Londres"], ["MAD", "Madrid"], ["BCN", "Barcelone"], ["FRA", "Francfort"], ["LIS", "Lisbonne"], ["BLQ", "Bologne"], ["TRN", "Turin"]],
      "en": [["PAR", "Paris"], ["MIL", "Milan"], ["ROM", "Rome"], ["BRU", "Brussels"], ["LYS", "Lyon"], ["MRS", "Marseille"], ["TLS", "Toulouse"],
             ["GVA", "Geneva"], ["LON", "London"], ["MAD", "Madrid"], ["BCN", "Barcelona"], ["FRA", "Frankfurt"], ["LIS", "Lisbon"], ["BLQ", "Bologna"], ["TRN", "Turin"]]}
FROM_EN = {"ALG": "Algiers"}

T = {
    "fr": dict(path="faire-venir-un-proche", title="Faire venir un proche en Europe : choisir son billet et le faire payer en 1 clic | Escale",
               desc="Votre mère, votre père ou un frère vient vous voir ? Il choisit le vol le moins cher depuis Abidjan, Dakar, Douala… et vous l'envoie sur WhatsApp : vous payez en un clic. Visa, attestation d'accueil, assurance : la check-list.",
               h1="Fais venir <span>un proche</span>", lead="Ton proche choisit le vol le moins cher depuis chez lui et te l'envoie sur WhatsApp. Tu ouvres le lien et tu paies en un clic. Plus de captures d'écran, plus de billet payé trop cher.",
               how=["Ton proche (ou toi) choisit la ville de départ, la ville d'arrivée et le mois.", "Escale affiche les 3 vols aller-retour les moins chers, avec les vrais prix.",
                    "Il appuie sur « Envoyer pour paiement » : un message WhatsApp part avec le lien du vol.", "Tu ouvres le lien : même vol, mêmes dates, prix mis à jour. Tu réserves et tu paies chez le partenaire."],
               how_h="Comment ça marche", t=dict(q_from="D'où part ton proche ?", q_to="Où arrive-t-il ?", q_month="Quel mois ?", loading="Recherche des vols les moins chers…",
                   none="Pas encore de prix trouvé pour ce trajet ce mois-ci. Essaie un autre mois ou une autre ville d'arrivée.",
                   best_h="Les 3 vols les moins chers : {a} → {b}", cheapest="Le moins cher", rt="aller-retour", direct="direct", stop1="1 escale", stops="{n} escales",
                   send="Envoyer pour paiement", self="Réserver moi-même", note="Prix aller-retour trouvés récemment, pour ces dates précises. Ils se confirment sur le site de réservation.",
                   wa="Bonjour ! J'ai choisi ce billet sur Escale : {a} → {b}, aller le {d}, retour le {r}, vu à {p}. Tu peux le réserver et le payer ici : {u}",
                   pay_eyebrow="Ton proche a choisi ce vol", seen="Prix vu par ton proche : {p}", checking="Vérification du prix actuel…", now="Prix actuel : {p}",
                   now_none="Prix actuel indisponible pour l'instant : il s'affichera sur le site de réservation.", book="Réserver et payer ce vol",
                   book_note="Tu réserves sur le site de la compagnie ou de l'agence, au nom du passager (exactement comme sur son passeport). Escale ne touche jamais à l'argent."),
               chk_h="Check-list pour faire venir un proche", chk=[
                   ("🛂", "Le visa", "La plupart des passeports africains ont besoin d'un visa Schengen pour la France, l'Italie ou la Belgique : 90 € pour un adulte, 45 € de 6 à 12 ans, plus les frais du centre de visa. Vérifiez pour son passeport avec <a href=\"/visa/\">l'outil visa d'Escale</a>."),
                   ("🏠", "L'hébergement chez vous", "France : attestation d'accueil à demander à votre mairie (formulaire cerfa n°10798, timbre fiscal de 30 €). Italie : « dichiarazione di ospitalità » ou lettre d'invitation, selon le modèle du consulat. Belgique : engagement de prise en charge (annexe 3bis) à la commune."),
                   ("🛡️", "L'assurance", "Une assurance voyage couvrant au moins 30 000 € de frais médicaux et le rapatriement est exigée pour le visa."),
                   ("🎫", "Le billet", "Réservez au nom exact du passeport. Pour le visa, un aller-retour est demandé : gardez la confirmation pour le dossier."),
                   ("🧳", "Les bagages", "La franchise change selon la compagnie : voir <a href=\"/bagages-compagnies-afrique/\">les bagages de chaque compagnie</a>.")],
               off_h="Sites officiels", off=[("France-Visas (visas pour la France)", "https://france-visas.gouv.fr/"), ("Attestation d'accueil (Service-Public.fr)", "https://www.service-public.fr/particuliers/vosdroits/F2191"),
                   ("Visti per l'Italia (ministère italien des Affaires étrangères)", "https://vistoperitalia.esteri.it/"), ("Office des étrangers (Belgique)", "https://dofi.ibz.be/")],
               checked="Informations vérifiées en novembre 2026 : les règles et les montants changent. Vérifiez toujours auprès du consulat et de votre mairie ou commune."),
    "en": dict(path="en/bring-family", title="Bring a relative to Europe: they pick the flight, you pay in 1 click | Escale",
               desc="Your mother, father or brother is coming to visit? They pick the cheapest flight from Abidjan, Dakar, Lagos… and send it to you on WhatsApp: you pay in one click. Visa, invitation, insurance: the checklist.",
               h1="Bring <span>a relative</span>", lead="Your relative picks the cheapest flight from home and sends it to you on WhatsApp. You open the link and pay in one click. No more screenshots, no more overpriced tickets.",
               how=["Your relative (or you) picks the departure city, arrival city and month.", "Escale shows the 3 cheapest round trips, with real prices.",
                    "They tap 'Send for payment': a WhatsApp message goes out with the flight link.", "You open the link: same flight, same dates, updated price. You book and pay on the partner's site."],
               how_h="How it works", t=dict(q_from="Where is your relative flying from?", q_to="Where are they flying to?", q_month="Which month?", loading="Finding the cheapest flights…",
                   none="No price found yet for this route this month. Try another month or another arrival city.",
                   best_h="The 3 cheapest flights: {a} → {b}", cheapest="Cheapest", rt="round trip", direct="direct", stop1="1 stop", stops="{n} stops",
                   send="Send for payment", self="Book it myself", note="Round-trip prices recently found, for these exact dates. They are confirmed on the booking site.",
                   wa="Hi! I picked this ticket on Escale: {a} → {b}, out on {d}, back on {r}, seen at {p}. You can book and pay for it here: {u}",
                   pay_eyebrow="Your relative picked this flight", seen="Price seen by your relative: {p}", checking="Checking the current price…", now="Current price: {p}",
                   now_none="Current price not available right now: it will show on the booking site.", book="Book and pay for this flight",
                   book_note="You book on the airline's or agency's site, in the passenger's name (exactly as on their passport). Escale never handles any money."),
               chk_h="Checklist to bring a relative", chk=[
                   ("🛂", "Visa", "Most African passports need a Schengen visa for France, Italy or Belgium: €90 for an adult, €45 for ages 6 to 12, plus visa centre fees. Check for their passport with <a href=\"/en/visa/\">Escale's visa tool</a>."),
                   ("🏠", "Staying with you", "France: 'attestation d'accueil' from your town hall (cerfa form 10798, €30 tax stamp). Italy: 'dichiarazione di ospitalità' or invitation letter, using the consulate's template. Belgium: sponsorship form (annex 3bis) at your commune."),
                   ("🛡️", "Insurance", "Travel insurance covering at least €30,000 of medical costs and repatriation is required for the visa."),
                   ("🎫", "Ticket", "Book in the exact passport name. A round trip is expected for the visa: keep the confirmation for the file."),
                   ("🧳", "Baggage", "Allowances vary by airline: see <a href=\"/bagages-compagnies-afrique/\">each airline's baggage rules</a>.")],
               off_h="Official websites", off=[("France-Visas (visas for France)", "https://france-visas.gouv.fr/"), ("Attestation d'accueil (Service-Public.fr, in French)", "https://www.service-public.fr/particuliers/vosdroits/F2191"),
                   ("Visas for Italy (Italian Foreign Ministry)", "https://vistoperitalia.esteri.it/"), ("Immigration Office (Belgium)", "https://dofi.ibz.be/")],
               checked="Information checked in November 2026: rules and fees change. Always check with the consulate and your town hall or commune."),
}


def build(site, ctx):
    paths = {l: T[l]["path"] for l in T}
    urls = []
    for lang, t in T.items():
        frm = [[c, FROM_EN.get(c, n) if lang == "en" else n, f] for c, n, f in FROM]
        q = "" if lang == "fr" else "?lang=en"
        how = "".join(f"<li>{E(x)}</li>" for x in t["how"])
        chk = "".join(f'<li class="pv-item"><span class="pv-ic" aria-hidden="true">{ic}</span><div><h3>{E(h)}</h3><p>{d}</p></div></li>' for ic, h, d in t["chk"])
        body = (f'<section class="pr-choose-only"><h2>{E(t["how_h"])}</h2><ol class="pr-how">{how}</ol></section>'
                f'<div id="pr-app" class="pr-app" data-t="{E(json.dumps(t["t"], ensure_ascii=False))}" data-from="{E(json.dumps(frm, ensure_ascii=False))}" data-to="{E(json.dumps(TO[lang], ensure_ascii=False))}">'
                f'<noscript><p><a class="btn" href="/{q}">Escale</a></p></noscript></div>'
                f'<section id="price-alert" class="price-alert" data-from="ABJ" data-to="PAR" hidden></section>'
                f'<section><h2>{E(t["chk_h"])}</h2><ol class="pv-list pr-chk">{chk}</ol></section>'
                f'<section><h2>{E(t["off_h"])}</h2><ul>' + "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(n)}</a></li>' for n, u in t["off"]) +
                f'</ul><p class="small">{E(t["checked"])}</p></section>'
                '<script src="/fetes.js" defer></script><script src="/proche.js" defer></script><script src="/alerts.js" defer></script>')
        hero = f'<p class="eyebrow">💝 Escale</p><h1>{t["h1"]}</h1><p class="hero-lead">{E(t["lead"])}</p>'
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "WebApplication", "name": t["title"].split(" | ")[0],
                                                                   "description": t["desc"], "inLanguage": lang, "applicationCategory": "TravelApplication", "operatingSystem": "Web",
                                                                   "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}, ensure_ascii=False) + "</script>"
        urls.append(B.write(site, t["path"], lang, t["title"], t["desc"], hero, body, ld, paths, ctx))
    return urls
