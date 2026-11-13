"""Deux pages pour les visiteurs venus des vidéos (13 novembre 2026), en français :
  - /match-des-aeroports/ : pour une destination, le classement des villes de départ suivies, du moins cher au plus cher ;
  - /astuces-billets-afrique/ : les quatre gestes montrés dans les vidéos, avec le lien vers l'outil du site pour chacun.
Aucun prix n'est écrit dans les pages : site/match.js lit les relevés du jour (/api/verdict).
"""
import html
import json

E = html.escape


def _faq_ld(faq):
    return ('<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False) + "</script>")


def _faq(faq):
    return ('<section class="faq"><h2>Questions fréquentes</h2>'
            + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq) + "</section>")


def build(page, wa_btn):
    urls = []
    # ---------- Match des aéroports
    faq = [("D'où viennent ces prix ?", "Escale relève chaque jour, pour chaque trajet suivi, le prix aller-retour le plus bas des six prochains mois. La date du relevé est affichée sous le classement. Le tarif exact se confirme sur le site de réservation."),
           ("Pourquoi partir d'une autre ville peut coûter moins cher ?", "Chaque aéroport a ses compagnies, ses vols directs et sa concurrence. Sur un même jour, l'écart entre deux villes de départ peut dépasser le prix du train ou du car pour y aller."),
           ("Faut-il compter le trajet jusqu'à l'aéroport ?", "Oui : ajoutez le train, le car ou l'essence, et parfois une nuit d'hôtel. Le match est gagné seulement si l'écart reste intéressant après ces frais."),
           ("Ma ville de départ n'est pas dans la liste ?", "Le classement ne montre que les trajets suivis chaque jour. Pour n'importe quelle autre ville, lancez une recherche : l'option « aéroports proches » compare aussi les aéroports voisins.")]
    hero = ('<p class="eyebrow">Outil gratuit · prix relevés chaque jour</p><h1>Le match <span>des aéroports</span></h1>'
            '<p class="hero-lead">Choisissez votre destination : Escale classe les villes de départ, de la moins chère à la plus chère, avec les vrais prix relevés aujourd\'hui.</p>')
    body = ('<section><h2 id="mt-h">Où allez-vous ?</h2><div class="chips mt-dest" id="mt-dest" role="group" aria-labelledby="mt-h"></div>'
            '<div id="mt-box" class="mt-box" aria-live="polite"><p class="pr-wait">Chargement des prix…</p></div>'
            '<p class="small" id="mt-note" hidden>Prix aller-retour le plus bas des six prochains mois, par personne, relevé le <span id="mt-date"></span>. '
            'Le tarif exact se confirme sur le site de réservation. N\'oubliez pas le coût du trajet jusqu\'à l\'aéroport.</p>'
            '<p class="cta-row"><button type="button" class="btn ghost" id="mt-share" hidden>Partager ce match</button></p></section>'
            '<section><h2>Comment lire le classement</h2><ul>'
            '<li>Le <strong>vainqueur</strong> est la ville de départ avec le prix relevé le plus bas pour cette destination.</li>'
            '<li>La barre montre l\'écart avec le vainqueur : plus elle est longue, plus le billet est cher.</li>'
            '<li>Touchez une ligne pour voir les vols de ce trajet, avec le calendrier des prix jour par jour.</li></ul></section>'
            '<section><h2>Aller plus loin</h2><ul class="route-links">'
            '<li><a href="/astuces-billets-afrique/">Les 4 astuces pour payer son billet moins cher</a></li>'
            '<li><a href="/acheter-ou-attendre/">Acheter maintenant ou attendre ? Le verdict trajet par trajet</a></li>'
            '<li><a href="/bons-plans/">Les bons plans du jour</a></li></ul></section>'
            + _faq(faq) + '<script src="/match.js" defer></script>')
    urls.append(page("match-des-aeroports", "Match des aéroports : de quelle ville partir pour payer moins cher ? | Escale",
                     "Dakar, Abidjan, Casablanca, Alger, Tunis, Lagos… : le classement des villes de départ (Paris, Bruxelles, Milan, Rome, Genève, Londres…) avec les prix relevés aujourd'hui.",
                     hero, body, _faq_ld(faq)))

    # ---------- Les 4 astuces
    tips = [("1", "Regardez le calendrier des prix", "Sur un même trajet, le prix change d'un jour à l'autre. Le calendrier colore chaque jour de départ, du moins cher au plus cher : décaler de deux ou trois jours suffit souvent.",
             "/calendrier-prix-diaspora/", "Ouvrir le calendrier des prix"),
            ("2", "Comparez les villes de départ", "Paris, Bruxelles, Milan, Genève, Lyon… Selon la destination, une autre ville de départ peut coûter bien moins cher, même en comptant le train pour y aller.",
             "/match-des-aeroports/", "Lancer le match des aéroports"),
            ("3", "Suivez les bons plans du jour", "Chaque jour, Escale repère les trajets dont le prix a nettement baissé par rapport aux relevés précédents.",
             "/bons-plans/", "Voir les bons plans du jour"),
            ("4", "Créez une alerte prix", "Pas le moment d'acheter ? Sur la page de votre trajet, indiquez votre budget : Escale vous envoie un e-mail quand un aller-retour passe en dessous. C'est gratuit.",
             "/acheter-ou-attendre/", "Choisir mon trajet et créer une alerte")]
    faq2 = [("Quel est le meilleur moment pour acheter un billet pour l'Afrique ?", "Pour l'été, Noël et les grandes fêtes, trois à quatre mois avant : les prix montent nettement dans les dernières semaines. Hors de ces périodes, comparez les dates avec le calendrier des prix."),
            ("Les prix affichés sur Escale sont-ils réels ?", "Oui : ce sont des prix relevés auprès des sites de réservation, avec leur date. Rien n'est inventé. Le tarif exact se confirme au moment de réserver, sur le site du vendeur."),
            ("Escale vend-il les billets ?", "Non. Escale compare les prix et vous envoie vers le site de réservation, où vous payez. La comparaison est gratuite.")]
    hero = ('<p class="eyebrow">Vu dans nos vidéos</p><h1>Payer son billet pour l\'Afrique moins cher <span>en 4 astuces</span></h1>'
            '<p class="hero-lead">Les quatre gestes qui font vraiment baisser le prix d\'un billet, et l\'outil gratuit pour chacun.</p>'
            '<div class="cta-row"><a class="btn" href="/?type=vols">Comparer les vols maintenant</a></div>')
    body = ('<section><ol class="as-list">'
            + "".join(f'<li class="as-item"><span class="as-n" aria-hidden="true">{n}</span><div><h2>{E(h)}</h2><p>{E(p)}</p><p><a class="price-go" href="{u}">{E(l)}</a></p></div></li>' for n, h, p, u, l in tips)
            + '</ol></section>'
            '<section><h2>Et aussi</h2><ul>'
            '<li>Avec des valises de cadeaux, comparez les tarifs qui incluent deux bagages en soute : ils reviennent souvent moins cher qu\'un tarif de base avec bagages en supplément.</li>'
            '<li>Regardez la durée de l\'escale autant que le prix : un billet un peu plus cher avec une correspondance courte vaut parfois mieux.</li>'
            '<li>Pour les fêtes, réservez tôt et préférez un billet modifiable si vos dates ne sont pas sûres.</li></ul></section>'
            '<section><h2>Les bons plans chaque semaine</h2><p>Les prix les plus bas vers l\'Afrique, chaque semaine sur WhatsApp, gratuitement.</p>' + wa_btn("fr") + '</section>'
            '<section><h2>Pages utiles</h2><ul class="route-links">'
            '<li><a href="/meilleur-mois-pour-partir/">Meilleur mois pour partir, ville par ville</a></li>'
            '<li><a href="/vols-noel-2026/">Noël 2026 : les prix par destination</a></li>'
            '<li><a href="/vols-tabaski-2027/">Tabaski 2027 : les prix par destination</a></li></ul></section>'
            + _faq(faq2))
    urls.append(page("astuces-billets-afrique", "Billet d'avion pour l'Afrique moins cher : les 4 astuces | Escale",
                     "Calendrier des prix, villes de départ, bons plans du jour, alerte prix : les quatre gestes pour payer moins cher son billet vers l'Afrique, avec les outils gratuits d'Escale.",
                     hero, body, _faq_ld(faq2)))
    return urls
