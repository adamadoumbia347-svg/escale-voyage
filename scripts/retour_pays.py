"""Guide « Rentrer au pays pour de bon » (/retour-au-pays/) : les démarches quand on quitte la France (ou l'Europe) pour
s'installer en Afrique. Uniquement des points de repère généraux avec les liens vers les sites officiels ; aucun montant,
aucune règle fiscale chiffrée : chaque situation se vérifie à la source. Relu en novembre 2026."""
import html

import build_i18n as B

E = html.escape
PATH = "retour-au-pays"
CHECKED = "novembre 2026"

ETAPES = [
    ("6 à 12 mois avant : décider et chiffrer", [
        "Faites la liste de ce que vous emportez, de ce que vous vendez et de ce que vous laissez : c'est ce qui décide entre quelques valises, du fret aérien (rapide, cher au kilo) et un conteneur ou un groupage maritime (lent, bien moins cher au mètre cube).",
        "Demandez plusieurs devis de déménageurs internationaux et de transitaires, avec le détail porte à porte : enlèvement, douane au départ et à l'arrivée, livraison.",
        "Renseignez-vous sur les règles d'importation du pays d'arrivée (effets personnels, véhicule, électroménager) : certains pays exonèrent les affaires personnelles d'un résident qui revient, sous conditions et avec justificatifs.",
    ]),
    ("Papiers et administration", [
        "Passeport et pièces d'identité valides pour toute la famille, actes de naissance et de mariage (plusieurs copies), diplômes, relevés de carrière, certificats de travail.",
        "Déclarez votre changement d'adresse aux organismes français : impôts, caisse de retraite, sécurité sociale, CAF, banque, assurances. Le service en ligne <a href=\"https://www.service-public.fr/particuliers/vosdroits/F14128\" target=\"_blank\" rel=\"noopener\">Je déménage</a> de service-public.fr centralise plusieurs de ces démarches.",
        "Inscription au registre des Français établis hors de France auprès du consulat, si vous gardez la nationalité française : utile pour les papiers, les élections et les urgences (<a href=\"https://www.service-public.fr/particuliers/vosdroits/F33307\" target=\"_blank\" rel=\"noopener\">service-public.fr</a>).",
    ]),
    ("Impôts", [
        "L'année du départ, vous devez signaler votre nouvelle adresse à l'étranger et déposer une déclaration pour vos revenus français : le détail est sur la page <a href=\"https://www.impots.gouv.fr/particulier/je-pars-letranger\" target=\"_blank\" rel=\"noopener\">« Je pars à l'étranger »</a> d'impots.gouv.fr.",
        "Selon votre situation (biens en France, revenus de location, pension), vous pouvez rester imposable en France sur certains revenus. Un rendez-vous avec le service des impôts des particuliers non-résidents évite les mauvaises surprises.",
        "Vérifiez s'il existe une convention fiscale entre la France et votre pays d'arrivée : elle détermine où chaque revenu est imposé.",
    ]),
    ("Retraite et protection sociale", [
        "Une retraite française se verse à l'étranger : il faut fournir chaque année un certificat de vie. Les démarches sont expliquées sur <a href=\"https://www.lassuranceretraite.fr/portail-info/home/retraites/vivre-a-letranger.html\" target=\"_blank\" rel=\"noopener\">lassuranceretraite.fr</a>.",
        "La sécurité sociale française cesse en général de couvrir les soins reçus à l'étranger une fois que vous n'êtes plus résident : regardez la Caisse des Français de l'étranger (<a href=\"https://www.cfe.fr/\" target=\"_blank\" rel=\"noopener\">cfe.fr</a>) ou une assurance santé locale ou internationale.",
        "Si vous avez travaillé dans plusieurs pays, demandez un relevé de carrière avant de partir : il sera plus difficile à reconstituer de loin.",
    ]),
    ("Santé", [
        "Mettez à jour les vaccins de toute la famille. Le certificat de vaccination contre la fièvre jaune est exigé à l'entrée de nombreux pays d'Afrique subsaharienne : regardez les recommandations par pays de l'<a href=\"https://www.pasteur.fr/fr/centre-medical/preparer-son-voyage\" target=\"_blank\" rel=\"noopener\">Institut Pasteur</a>.",
        "Emportez vos dossiers médicaux, ordonnances et une provision de vos traitements habituels, avec les noms des molécules (les marques changent d'un pays à l'autre).",
        "Pour une installation durable, demandez à votre médecin un traitement préventif ou des conseils adaptés au paludisme selon la région.",
    ]),
    ("Le déménagement : valises, fret, conteneur", [
        "Bagages supplémentaires en avion : souvent la solution la plus simple pour 2 à 4 valises en plus. Achetez-les en ligne avant le départ, c'est moins cher qu'à l'aéroport. Les règles de chaque compagnie : <a href=\"/bagages-compagnies-afrique/\">bagages par compagnie</a>.",
        "Fret aérien : pour quelques cartons urgents (ordinateurs, documents, affaires des enfants), en quelques jours ; le prix se calcule au kilo ou au volume.",
        "Groupage maritime ou conteneur : pour le mobilier et l'électroménager, comptez plusieurs semaines de transport, plus le passage en douane. Faites un inventaire détaillé et photographié : il servira à la douane et à l'assurance.",
        "Véhicule : l'exportation depuis la France (certificat, douane) et l'importation dans le pays d'arrivée (taxes, âge maximal du véhicule, conformité) ont chacune leurs règles. Côté français, la douane explique la procédure sur <a href=\"https://www.douane.gouv.fr/\" target=\"_blank\" rel=\"noopener\">douane.gouv.fr</a>.",
    ]),
    ("Animaux de compagnie", [
        "Chien ou chat : puce électronique, vaccination antirabique à jour et certificat vétérinaire récent sont la base. Les compagnies acceptent les petits animaux en cabine et les plus gros en soute, sur réservation et avec une caisse aux normes ; certaines races ne voyagent pas.",
        "Chaque pays d'arrivée a ses propres conditions (quarantaine, permis d'importation) : renseignez-vous auprès de son ambassade et sur le <a href=\"https://agriculture.gouv.fr/voyager-avec-son-animal-de-compagnie\" target=\"_blank\" rel=\"noopener\">site du ministère de l'Agriculture</a>, plusieurs mois avant le départ.",
    ]),
    ("Argent et banque", [
        "Gardez un compte en Europe quelques mois après le départ : remboursements, dernières factures, retraite ou loyers se gèrent plus facilement. Prévenez votre banque de votre nouvelle résidence.",
        "Ouvrez un compte local dès l'arrivée et renseignez-vous sur les solutions de transfert (virement international, services de transfert, mobile money) et leurs frais.",
        "Pour le billet d'avion lui-même, les compagnies acceptent parfois le <a href=\"/payer-billet-avion-plusieurs-fois/\">paiement en plusieurs fois</a> ou le <a href=\"/payer-billet-avion-mobile-money/\">mobile money</a>.",
    ]),
    ("Enfants et scolarité", [
        "Demandez les certificats de scolarité et de radiation, les bulletins et, pour le lycée, les relevés de notes officiels. L'inscription dans un établissement du réseau AEFE (lycées français à l'étranger) se prépare des mois à l'avance : <a href=\"https://www.aefe.fr/\" target=\"_blank\" rel=\"noopener\">aefe.fr</a>.",
        "Pour les plus jeunes, un carnet de santé à jour et les vaccins exigés par les écoles locales.",
    ]),
]

FAQ = [
    ("Combien de temps avant le départ faut-il s'y prendre ?",
     "Six mois est un minimum confortable pour un déménagement familial avec conteneur ; trois mois pour un départ léger en valises. Les étapes les plus longues sont les devis et le transport maritime, les démarches consulaires et l'inscription des enfants à l'école."),
    ("Vaut-il mieux envoyer un conteneur ou racheter sur place ?",
     "Cela dépend de ce que vous possédez et des prix locaux. Beaucoup de familles envoient un groupage (quelques mètres cubes) pour les affaires auxquelles elles tiennent et rachètent l'encombrant sur place. Demandez des devis des deux côtés avant de décider."),
    ("Puis-je garder ma retraite française en vivant en Afrique ?",
     "Oui : une pension française se verse à l'étranger, en échange d'un certificat de vie à fournir chaque année. Les détails sont sur le site de l'Assurance retraite. La couverture santé, elle, ne suit pas automatiquement."),
    ("Dois-je encore payer des impôts en France ?",
     "Cela dépend de vos revenus de source française (location, pension, activité) et de la convention fiscale avec votre pays. La page « Je pars à l'étranger » d'impots.gouv.fr et le service des impôts des non-résidents sont les bons interlocuteurs."),
    ("Comment transporter beaucoup de bagages en avion sans payer une fortune ?",
     "Comparez le prix du billet avec bagages inclus plutôt que le billet seul, achetez les bagages supplémentaires en ligne, et pesez tout à la maison. Au-delà de 4 ou 5 valises, le fret aérien ou maritime revient souvent moins cher."),
]


def build(site, ctx):
    sections = "".join(f"<section><h2>{E(h)}</h2><ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul></section>" for h, items in ETAPES)
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(r)}</p></details>" for q, r in FAQ)
    hero = ('<p class="eyebrow">Guide · relu en ' + CHECKED + '</p><h1>Rentrer au pays <span>pour de bon</span></h1>'
            '<p class="hero-lead">Quitter la France ou l\'Europe pour s\'installer en Afrique : les démarches, le déménagement, les impôts, la retraite, la santé, les enfants, les animaux. Des repères clairs et les liens officiels, étape par étape.</p>')
    body = (f'<section><h2>En bref</h2><ul><li>Commencez par la <strong>liste des affaires</strong> : elle décide du mode de transport et du budget.</li>'
            '<li>Prévenez les <strong>organismes français</strong> (impôts, retraite, sécurité sociale, banque) avant de partir : tout est plus simple depuis la France.</li>'
            '<li><strong>Santé et papiers</strong> de toute la famille à jour, avec copies.</li>'
            '<li>Pour le vol, comparez <strong>billet + bagages</strong>, pas le billet seul : <a href="/">comparateur Escale</a>.</li></ul></section>'
            + sections +
            f'<section class="faq"><h2>Questions fréquentes</h2>{faq}</section>'
            '<section><h2>Pour aller plus loin</h2><ul><li><a href="/diaspora/">Rentrer au pays pour les fêtes : calendrier par communauté</a></li>'
            '<li><a href="/visa/">Visa selon votre passeport</a></li><li><a href="/bagages-compagnies-afrique/">Bagages : la franchise de chaque compagnie</a></li>'
            '<li><a href="/guides/">Tous les guides</a></li></ul></section>'
            '<p class="small">Ces repères sont généraux et ne remplacent pas un conseil adapté à votre situation (notaire, expert-comptable, consulat, déménageur). Les règles changent : les sites officiels font foi.</p>'
            + B.faq_ld(FAQ))
    return [B.write(site, PATH, "fr", "Rentrer au pays pour de bon : démarches, déménagement, impôts, retraite, santé | Escale",
                    "S'installer en Afrique après des années en Europe : les démarches à faire avant de partir, le déménagement (valises, fret, conteneur, véhicule), les impôts, la retraite, la santé, les enfants et les animaux, avec les liens officiels.",
                    hero, body, "", {"fr": PATH}, ctx)]
