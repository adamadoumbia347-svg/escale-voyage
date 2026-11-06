"""Page « Payer son billet d'avion en plusieurs fois » (français).
Uniquement des conditions vérifiées sur les sites officiels des compagnies ou dans la presse spécialisée, avec la date de
vérification ; les montants et frais changent souvent, d'où les liens vers les pages officielles. À revérifier régulièrement."""
import html
import json

import build_i18n as B

E = html.escape
PATH = "payer-billet-avion-plusieurs-fois"
CHECKED = "novembre 2026"

# (compagnie, ce qui est proposé, conditions principales, lien officiel ou source)
OFFRES = [
    ("Corsair", "2, 3 ou 4 fois sans frais par carte ; ou 3, 4, 6 ou 10 fois avec Oney",
     "Sans frais : Carte Bleue, Visa, Mastercard ou American Express, tout doit être payé 7 jours avant le départ ; le 3 fois demande un départ à plus de 69 jours, le 4 fois à plus de 99 jours. "
     "Avec Oney : 3 fois (1,67 % de frais, 60 € au plus) ou 4 fois (2,50 %, 90 € au plus) dès 100 € ; 6 et 10 fois dès 500 €, sur certains tarifs seulement, avec un crédit qui peut coûter cher (taux de 20,90 % donné en exemple). Allers-retours, particuliers résidant en France.",
     "https://www.flycorsair.com/en/payment/can-i-pay-several-instalments"),
    ("Air Caraïbes", "3 ou 4 fois avec Oney, même à la dernière minute",
     "De 100 € à 8 000 € (4 000 € pour Cayenne), billets aller-retour, départ à plus d'un jour. Frais : 1,71 % en 3 fois (30 € au plus), 2,55 % en 4 fois (60 € au plus). Visa ou Mastercard (pas de Maestro, Electron, Nickel, American Express ni carte professionnelle). Particuliers résidant en France métropolitaine ou dans les DOM.",
     "https://www.aircaraibes.com/avant-voyage/moyens-paiement/paiement-plusieurs-fois"),
    ("Air France", "3 ou 4 fois avec Oney (avec frais) ; 3 fois sans frais avec la carte American Express Air France-KLM",
     "Oney : carte Visa ou Mastercard, sous réserve d'acceptation du dossier par Oney. Carte American Express Air France-KLM : paiement en 3 fois sans frais dès 50 €. Vérifiez les frais exacts au moment de payer.",
     "https://wwws.airfrance.fr/information/meilleures-offres/oney-paiement-echelonne"),
    ("Royal Air Maroc", "3 ou 4 fois avec Oney, depuis la France",
     "La compagnie indique que le paiement en 3 ou 4 fois Oney est disponible en France. Les moyens de paiement proposés changent selon le pays depuis lequel vous réservez.",
     "https://royalairmaroc.com/int-fr/moyens-paiement"),
    ("ASL Airlines France", "3, 4 ou 10 fois avec FLOA (notamment vers l'Algérie)",
     "Annoncé en mars 2026 : particuliers majeurs résidant en France, carte Visa ou Mastercard valable pendant toute la durée du paiement. Les frais sont détaillés dans les conditions FLOA sur le site de la compagnie.",
     "https://observalgerie.com/2026/03/13/voyage/asl-airlines-nouvelle-annonce-sur-le-paiement-des-billets/"),
]

FAQ = [
    ("Le paiement en plusieurs fois est-il gratuit ?",
     "Pas toujours. Certaines offres sont sans frais (par exemple chez Corsair, si vous réservez assez tôt), d'autres ajoutent des frais de 1,5 % à 3 % environ en 3 ou 4 fois, et le paiement en 6 ou 10 fois est souvent un vrai crédit, avec des intérêts. Regardez le coût total affiché avant de valider."),
    ("Faut-il une carte de crédit ?",
     "Il faut presque toujours une carte Visa ou Mastercard valable jusqu'à la dernière échéance. Les cartes à autorisation systématique (Maestro, Electron), certaines cartes de néobanques et les cartes professionnelles sont souvent refusées."),
    ("Je ne vis pas en France, est-ce possible ?",
     "La plupart des offres sont réservées aux personnes qui résident en France (parfois aussi dans les DOM). Depuis l'Afrique, regardez plutôt le paiement par mobile money proposé par certaines compagnies."),
    ("Quand faut-il réserver ?",
     "Les offres sans frais demandent souvent de réserver plusieurs semaines ou mois avant le départ, car tout doit être payé avant le vol. Pour les grandes périodes (Noël, été, fêtes), réserver tôt permet à la fois un meilleur prix et l'accès au paiement sans frais."),
    ("Que se passe-t-il si j'annule ?",
     "Les échéances restent liées au billet : si le billet n'est pas remboursable, vous devez quand même les payer. Lisez les conditions du tarif et du financement avant de réserver."),
]


def build(site, ctx):
    rows = "".join(
        f'<li><h3>{E(c)}</h3><p><strong>{E(w)}</strong></p><p>{E(d)}</p><p><a href="{E(u)}" target="_blank" rel="noopener nofollow">{"Voir l'article ↗" if "observalgerie" in u else "Voir les conditions officielles ↗"}</a></p></li>'
        for c, w, d, u in OFFRES)
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(r)}</p></details>" for q, r in FAQ)
    ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]}, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    body = (
        '<section><h2>En bref</h2><ul>'
        '<li>Plusieurs compagnies permettent de payer un billet en <strong>3 ou 4 fois</strong>, parfois en 10 fois, souvent via un organisme de crédit (Oney, FLOA).</li>'
        '<li><strong>Sans frais</strong> seulement dans certains cas : réservation tôt, carte particulière ou promotion. Sinon, comptez quelques pourcents de frais en 3 ou 4 fois.</li>'
        '<li>Les offres sont en général réservées aux <strong>particuliers résidant en France</strong>, avec une carte Visa ou Mastercard.</li>'
        '<li>L\'option apparaît au moment de payer, sur le site de la compagnie : comparez d\'abord les prix sur Escale, puis vérifiez sur le site de la compagnie si elle propose le paiement en plusieurs fois.</li></ul></section>'
        f'<section><h2>Les compagnies qui le proposent</h2><p class="small">Conditions vérifiées en {CHECKED} sur les pages officielles ou dans la presse spécialisée. Elles changent souvent : la page officielle fait foi.</p>'
        f'<ul class="pf-list">{rows}</ul></section>'
        '<section><h2>Comment faire, étape par étape</h2><ol>'
        '<li>Trouvez le vol le moins cher pour vos dates avec la <a href="/recherche/">recherche en direct</a> ou le <a href="/calendrier-prix-diaspora/">calendrier des prix</a>.</li>'
        '<li>Si la compagnie la moins chère fait partie de la liste, réservez directement sur son site : l\'option « paiement en plusieurs fois » s\'affiche à l\'étape du paiement.</li>'
        '<li>Comparez le <strong>coût total</strong> (billet + frais du paiement fractionné) avec un vol un peu plus cher payable en une fois, ou sans frais.</li>'
        '<li>Vérifiez que votre carte sera encore valable à la dernière échéance et qu\'il y aura assez d\'argent sur le compte à chaque prélèvement.</li></ol></section>'
        '<section><h2>Les autres solutions</h2><ul>'
        '<li><a href="/payer-billet-avion-mobile-money/">Payer avec Orange Money, Wave ou MTN MoMo</a> : pratique quand un proche en Afrique paie le billet.</li>'
        '<li><a href="/acheter-ou-attendre/">Acheter maintenant ou attendre ?</a> : savoir si le prix risque de monter avant de vous engager.</li>'
        '<li><a href="/billet-trop-cher/">Billet trop cher ?</a> : les astuces pour faire baisser le prix (autre aéroport, autres dates, escale).</li></ul></section>'
        f'<section class="faq"><h2>Questions fréquentes</h2>{faq}</section>'
        '<p class="small">Escale n\'est pas un organisme de crédit et ne vend pas de billets. Un crédit vous engage et doit être remboursé : vérifiez vos capacités de remboursement avant de vous engager.</p>'
        + ld)
    hero = ('<h1>Payer son billet d\'avion <span>en plusieurs fois</span></h1>'
            '<p class="hero-lead">Quelles compagnies acceptent le paiement en 3, 4 ou 10 fois, à quelles conditions et avec quels frais : le point, avec les liens vers les pages officielles.</p>')
    return [B.write(site, PATH, "fr", "Payer son billet d'avion en plusieurs fois (3x, 4x, 10x) : les compagnies | Escale",
                    "Corsair, Air Caraïbes, Air France, Royal Air Maroc, ASL Airlines : qui propose le paiement du billet d'avion en 3, 4 ou 10 fois, avec ou sans frais, et à quelles conditions.",
                    hero, body, "", {"fr": PATH}, ctx)]
