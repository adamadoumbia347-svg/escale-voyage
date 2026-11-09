"""Pages en nouchi (/nouchi/…) : les conseils clés d'Escale racontés comme on parle à Abidjan, pour la communauté ivoirienne.
Nouchi léger, lisible par tous, sans caricature. Chaque page renvoie vers la version française complète (qui reste la page de
référence : balise canonique vers elle-même ici, mais lien clair). Les textes sont à relire par Dobam ; une phrase « dis-nous si
une expression sonne faux » invite les lecteurs à corriger. Aucun chiffre : les prix se lisent sur les pages trajets."""
import html

import build_i18n as B

E = html.escape
INTRO = ("Ici on parle comme au pays. Même conseils que sur le reste d'Escale, mais dits à la manière d'Abidjan. "
         "Si une expression sonne faux, <a href=\"/contact/\">dis-le-nous</a> : on corrige.")

PAGES = [
    dict(slug="visa", titre="Faut-il un visa ? On dit quoi ?", ref="/visa/", ref_l="la page Visa (version complète)",
         lead="Avant de gbê ton billet, il faut savoir si on va te laisser passer là-bas. Tout dépend de ton passeport et du pays où tu vas.",
         sections=[
             ("C'est comment ?", ["Ton passeport ivoirien ne te donne pas les mêmes droits qu'un passeport français. Pour certains pays, tu passes sans rien ; pour d'autres, il faut demander le visa avant, et ça peut prendre des semaines.",
                                  "Sur Escale, tu choisis ton passeport et ta destination : la page te dit si c'est libre, visa à l'arrivée ou visa à demander avant. Et elle te donne le lien officiel, pas un lien de môgô qui veut ton djai."]),
             ("Les pièges", ["Attendre la dernière semaine pour demander le visa : là tu vas pleurer.", "Payer un « facilitateur » sur Facebook : souvent c'est du gbagba. Le vrai visa se demande sur le site officiel de l'ambassade ou du pays.", "Oublier que le passeport doit souvent être valable encore 6 mois après ton retour."]),
             ("Ce qu'il faut faire", ["Vérifie sur Escale, puis sur le site officiel.", "Demande le visa tôt, garde les reçus.", "Imprime tout : confirmation de vol, réservation d'hôtel, visa. À l'aéroport, le papier sauve."]),
         ]),
    dict(slug="bagages", titre="Les bagages : combien de kilos tu peux amener ?", ref="/guides/bagages-avion/", ref_l="le guide Bagages (version complète)",
         lead="Tu veux amener les cadeaux pour toute la famille. Normal. Mais faut pas que la valise te coûte plus cher que le billet.",
         sections=[
             ("Ça dépend du tarif", ["Le même vol existe en plusieurs tarifs. Le moins cher (« light », « basic ») : souvent pas de valise en soute, juste un petit sac. Le tarif normal : une valise, souvent 23 kg.", "Au-dessus de 23 kg tu paies le supplément ; au-dessus de 32 kg, la valise peut être refusée. Chaque compagnie a sa règle : c'est écrit dans ta réservation."]),
             ("Comment ne pas se faire gbê", ["Ajoute la valise au moment où tu réserves, pas au comptoir : au comptoir c'est le prix fort.", "Compare le prix total (billet + valises), pas le petit prix qui brille.", "Pèse ta valise la veille. Les 2 kg de trop, ça se paie cash à l'aéroport.", "Batterie externe et vapoteuse : en cabine, jamais en soute."]),
             ("Le bon réflexe", ["Prends une photo de ta valise et mets ton numéro dedans. Si elle se perd, tu déclares au comptoir de la compagnie avant de sortir de l'aéroport."]),
         ]),
    dict(slug="quand-reserver", titre="Quand acheter le billet pour payer moins ?", ref="/guides/quand-reserver/", ref_l="le guide Quand réserver (version complète)",
         lead="Il n'y a pas de jour magique. Mais il y a des habitudes qui font gagner du djai, surtout pour Noël et les fêtes.",
         sections=[
             ("Hors vacances", ["Deux à trois mois avant, c'est souvent bien. La dernière semaine, sur Paris – Abidjan, c'est rarement le moins cher."]),
             ("Noël, été, Tabaski, Aïd", ["Là il faut réserver quatre à six mois avant. En décembre, les prix peuvent doubler : celui qui attend, c'est lui qui pleure.", "La Tabaski et l'Aïd avancent d'à peu près 11 jours chaque année. Vérifie la date de ton année."]),
             ("Les petits réglages qui payent", ["Décale le départ de quelques jours : le milieu de semaine est souvent moins cher que le vendredi ou le dimanche.", "Compare les aéroports proches : Orly, Beauvais, Bruxelles, Lyon, Milan.", "Compare avec les bagages, sinon le calcul est faux.", "Si ton voyage est encore loin, mets une alerte prix et attends tranquille."]),
         ]),
    dict(slug="acheter-ou-attendre", titre="J'achète maintenant ou j'attends ?", ref="/acheter-ou-attendre/", ref_l="la page Acheter ou attendre (version complète)",
         lead="La question que tout le monde se pose devant le prix. Escale te donne une vraie réponse, trajet par trajet.",
         sections=[
             ("Comment ça marche", ["Chaque nuit, Escale relève le prix de 70 grands trajets Europe – Afrique. Sur la page du trajet, tu vois si le prix du jour est bas, moyen ou élevé par rapport à d'habitude, et notre conseil : c'est le moment, ou attends.", "Tu vois aussi la courbe des 30 derniers jours : si ça monte, tu sais ; si ça descend, tu sais aussi."]),
             ("Le matin, regarde « À saisir aujourd'hui »", ["C'est la liste des trajets qui sont nettement sous leur prix habituel ce jour-là. Quand ton trajet y est, c'est le moment de ne pas dormir."]),
             ("Mais attention", ["C'est un signal, pas une promesse. Le prix exact dépend de tes dates et se confirme sur le site de réservation."]),
         ]),
    dict(slug="billet-trop-cher", titre="Le billet est trop cher : on fait comment ?", ref="/billet-trop-cher/", ref_l="la page Billet trop cher (version complète)",
         lead="Tu as regardé le prix, ça t'a fait mal. Avant d'abandonner, essaie ça.",
         sections=[
             ("Cinq choses à essayer", ["Change de dates : ±3 jours, parfois ça change tout.", "Change d'aéroport : Bruxelles ou Lyon au lieu de Paris, Milan au lieu de Rome.", "Accepte une escale : Casablanca, Istanbul, Addis-Abeba sont souvent moins chers que le direct.", "Regarde le mois d'à côté : le calendrier des prix te montre le mois le moins cher.", "Mets une alerte prix et attends la baisse si tu peux."]),
             ("Ce qu'il ne faut pas faire", ["Acheter sur un site inconnu parce que c'est 50 € moins cher. Un billet pas cher qui n'existe pas, c'est le billet le plus cher du monde.", "Oublier les bagages dans le calcul."]),
         ]),
    dict(slug="payer-en-plusieurs-fois", titre="Payer le billet en plusieurs fois, c'est possible ?", ref="/payer-billet-avion-plusieurs-fois/", ref_l="la page Payer en plusieurs fois (version complète)",
         lead="Oui, chez certaines compagnies. Mais lis bien les conditions avant de signer.",
         sections=[
             ("Qui le propose", ["Plusieurs compagnies qui vont vers l'Afrique permettent de payer en 3 ou 4 fois, parfois en 10 fois, souvent avec un organisme de crédit. Parfois sans frais si tu réserves tôt, parfois avec des frais. La liste à jour est sur la page complète."]),
             ("Les conditions", ["En général : être résident en France, avoir une carte Visa ou Mastercard valable jusqu'à la dernière échéance.", "Le 6 ou 10 fois, c'est souvent un vrai crédit avec des intérêts. Regarde le coût total.", "Si tu annules, tu dois quand même payer les échéances si le billet n'est pas remboursable."]),
         ]),
    dict(slug="mobile-money", titre="Payer le billet avec Orange Money ou Wave ?", ref="/payer-billet-avion-mobile-money/", ref_l="la page Mobile money (version complète)",
         lead="Quand c'est la famille au pays qui paie, le mobile money peut servir. Voici comment ça se passe.",
         sections=[
             ("Comment ça marche", ["Certaines compagnies et agences acceptent Orange Money, Wave, MTN MoMo ou Moov Money au paiement, surtout si tu réserves depuis un pays d'Afrique. La page complète liste qui accepte quoi, avec les liens officiels."]),
             ("Les précautions", ["Paie seulement sur le site officiel de la compagnie ou d'une agence connue. Jamais un numéro envoyé en message privé.", "Garde la preuve de paiement et le numéro de réservation.", "Vérifie que le nom sur le billet est exactement celui du passeport."]),
         ]),
    dict(slug="rentrer-au-pays", titre="Rentrer au pays pour les fêtes sans se ruiner", ref="/diaspora/cote-d-ivoire/", ref_l="la page Rentrer en Côte d'Ivoire (version complète)",
         lead="Noël, Tabaski, l'indépendance, les vacances : tout le monde veut rentrer en même temps. Alors les prix montent. Voici le plan.",
         sections=[
             ("Le calendrier", ["Sur la page Côte d'Ivoire, tu as chaque période de l'année avec le prix repéré depuis Paris. Tu vois d'un coup d'œil quand c'est doux et quand c'est caillou."]),
             ("Le plan qui marche", ["Noël : réserve entre septembre et mi-octobre.", "Tabaski et Aïd : six à huit semaines avant, pas plus tard.", "Été : entre janvier et mars pour juillet-août.", "Et si vous partez à plusieurs depuis plusieurs villes, l'outil « Partir à plusieurs » te dit qui paie le moins."]),
             ("Partage dans le groupe", ["Chaque page a un bouton pour envoyer le calendrier dans le groupe WhatsApp de la famille. Comme ça tout le monde réserve au bon moment."]),
         ]),
]


def build(site, ctx):
    urls, items = [], []
    for p in PAGES:
        path = f'nouchi/{p["slug"]}'
        body = (f'<section><p class="small">{INTRO}</p></section>'
                + "".join(f"<section><h2>{E(h)}</h2>" + "".join(f"<p>{E(x)}</p>" for x in ps) + "</section>" for h, ps in p["sections"])
                + f'<section><h2>Pour aller plus loin</h2><p>Tout le détail, les chiffres du jour et les liens officiels : <a href="{p["ref"]}">{E(p["ref_l"])}</a>.</p>'
                '<ul class="route-links">' + "".join(f'<li><a href="/nouchi/{o["slug"]}/">{E(o["titre"])}</a></li>' for o in PAGES if o is not p) + '</ul></section>'
                + B.wa_btn("fr"))
        hero = f'<p class="eyebrow">🇨🇮 Escale en nouchi</p><h1>{E(p["titre"])}</h1><p class="hero-lead">{E(p["lead"])}</p>'
        urls.append(B.write(site, path, "fr", f'{p["titre"]} · Escale en nouchi', p["lead"], hero, body, "", {"fr": path}, ctx))
        items.append(f'<li><a href="/nouchi/{p["slug"]}/"><strong>{E(p["titre"])}</strong><br><span class="small">{E(p["lead"])}</span></a></li>')
    hero = ('<p class="eyebrow">🇨🇮 Pour la communauté ivoirienne</p><h1>Escale <span>en nouchi</span></h1>'
            '<p class="hero-lead">Les conseils d\'Escale pour voyager moins cher, racontés comme on parle à Abidjan. Mêmes infos, même sérieux, juste la manière de dire.</p>')
    body = (f'<section><p class="small">{INTRO}</p></section><section><ul class="pf-list">{"".join(items)}</ul></section>'
            '<section><h2>Pourquoi cette rubrique ?</h2><p>Parce qu\'un conseil qu\'on comprend tout de suite, on l\'applique. Et parce qu\'Escale a été créé par un Ivoirien de la diaspora, pour la diaspora. Les pages en français restent les pages de référence, avec les chiffres du jour et les liens officiels.</p></section>'
            + B.wa_btn("fr"))
    urls.append(B.write(site, "nouchi", "fr", "Escale en nouchi : les conseils voyage racontés comme à Abidjan | Escale",
                        "Visa, bagages, quand réserver, acheter ou attendre, billet trop cher, payer en plusieurs fois, mobile money, rentrer au pays : les conseils d'Escale en nouchi, pour la communauté ivoirienne.",
                        hero, body, "", {"fr": "nouchi"}, ctx))
    return urls
