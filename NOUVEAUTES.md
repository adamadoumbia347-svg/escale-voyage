# Nouveautés automatiques (tous les 2 jours)

Une tâche planifiée de Claude ajoute une nouveauté au site tous les 2 jours, l'envoie sur `main`
(Cloudflare publie, IndexNow signale les pages) et la note ici. Ce journal évite de refaire deux fois la même chose.

## Règles
- Une seule nouveauté par passage, utile aux voyageurs et bonne pour Google, en 5 langues (fr, en, es, pt, ar).
- Tourner entre les types : **guide pratique** → **page hôtels d'une ville** → guide pratique… Chaque guide répond à UNE question précise que la diaspora tape vraiment, avec la question dans le titre (depuis le 13 novembre 2026 : les pages qui répondent à une question précise montent dans Google, les pages trajets génériques restent loin ; plus de nouveaux trajets génériques sauf demande de Dobam).
- Rien d'inventé : pas de prix, d'horaires ou de règles précises qu'on ne peut pas vérifier ; rester général et renvoyer aux sources officielles.
- Toujours lancer `python3 scripts/build_pages.py` (et `node scripts/make_og.js` si de nouveaux trajets) avant d'envoyer.

## Idées en réserve
- Guides : visa et passeport (généralités), voyager pendant le ramadan / la Tabaski,
  assurance voyage,
  droits en cas de retard (règlement européen 261/2004), envoyer des colis au pays.
- Trajets : nouvelles villes de départ (Toulouse vers l'Afrique de l'Ouest, Clermont-Ferrand, Amsterdam, Zurich… ; Milan est déjà couvert par les pages en italien) vers l'Afrique et le Maghreb.
- Hôtels : Niamey, Ouagadougou, Nouakchott.

## Journal
| Date | Nouveauté |
|---|---|
| 2026-10-15 | Mise en place de la tâche planifiée |
| 2026-10-15 | Guide « Check-list avant de partir » en 5 langues (`/guides/check-list-depart/`) — prochain : nouveaux trajets |
| 2026-10-17 | 14 trajets depuis Lille et Nantes (Alger, Oran, Casablanca, Marrakech, Oujda/Agadir, Tunis, Dakar) en 5 langues, avec images de partage — prochain : page hôtels |
| 2026-10-19 | Page « Hôtel pas cher à Accra » en 5 langues (`/hotel-pas-cher-accra/`) — prochain : guide pratique |
| 2026-10-21 | Guide « Argent en voyage : carte, change et Mobile Money » en 5 langues (`/guides/argent-en-voyage/`) — prochain : nouveaux trajets |
| 2026-10-23 | 14 trajets depuis Montpellier (Alger, Oran, Constantine, Casablanca, Marrakech, Fès, Tunis) et Strasbourg (Alger, Oran, Casablanca, Marrakech, Tunis, Istanbul, Dakar) en 5 langues, avec images de partage — prochain : page hôtels |
| 2026-10-25 | Page « Hôtel pas cher à Lagos » en 5 langues (`/hotel-pas-cher-lagos/`) — prochain : guide pratique |
| 2026-10-27 | Guide « Correspondances et longues escales » en 5 langues (`/guides/correspondances-escales/`) — prochain : nouveaux trajets |
| 2026-10-29 | 14 trajets depuis Rennes (Alger, Oran, Casablanca, Marrakech, Agadir, Tunis, Dakar) et Bâle-Mulhouse (Alger, Oran, Constantine, Casablanca, Marrakech, Tunis, Istanbul) en 5 langues, avec images de partage — prochain : page hôtels |
| 2026-10-31 | Page « Hôtel pas cher à Nairobi » en 5 langues (`/hotel-pas-cher-nairobi/`) — prochain : guide pratique |
| 2026-11-01 | Guide « Vol de nuit : bien dormir et arriver en forme » en 5 langues (`/guides/vol-de-nuit/`) — prochain : nouveaux trajets |
| 2026-11-03 | 14 trajets depuis Barcelone (Dakar, Casablanca, Marrakech, Tanger, Alger, Oran, Bamako) et Francfort (Addis-Abeba, Accra, Lagos, Casablanca, Tunis, Istanbul, Dakar) en 5 langues, avec images de partage — prochain : page hôtels |
| 2026-11-05 | Page « Hôtel pas cher à Addis-Abeba » en 5 langues (`/hotel-pas-cher-addis-abeba/`) — prochain : guide pratique |

## 12-13 novembre 2026 : rubrique « Que visiter » et nouveau style
- `/visiter/` : 24 pays, 192 villes et lieux en photos (scripts/visiter.py, photos dans site/img/visiter, crédits dans site/data/visiter-photos.json).
- Style « serein » (bloc en fin de site/pages.css et dans site/index.html) : titres Fraunces, texte Nunito, animations ; couleurs d'Escale conservées.
- Accueil : le titre reste fixe, un ruban de pays défile dessous (site/motion.js, site/hero-anim.js et sa copie src/accueil-anim.ts).

## 13 novembre 2026 : « Que visiter » en trois langues, 8 pays d'Afrique de plus, 6 outils
- 32 pays, 253 lieux, en français (`/visiter/`), anglais (`/en/what-to-visit/`) et italien (`/it/cosa-visitare/`). Textes : scripts/visiter.py (fr),
  visiter_en.py, visiter_it.py ; pays ajoutés (Mali, Guinée, Bénin, Togo, Burkina Faso, RD Congo, Gabon, Nigeria) dans visiter_afrique.py, trois langues ensemble.
- Outils : jeu « Devine le pays » (visiter-jeu.js), carte postale à partager, carte du monde cliquable avec prix (visiter-carte.js),
  comparateur de deux pays (visiter-comparer.js), alerte prix depuis « Mes envies », budget du voyage (visiter.js).
- Prix : /api/ruban (src/api/ruban.ts), aller-retour le plus bas repéré depuis la ville du visiteur ; rien n'est affiché sans prix repéré.

## 13 novembre 2026 : lieux retirés de « Que visiter » (zones déconseillées)
- Règle (demande de Dobam) : un lieu situé dans une zone déconseillée par les conseils aux voyageurs de France Diplomatie n'est pas mis en avant.
- Pays retirés en entier : Mali, Burkina Faso, RD Congo. Lieux retirés : Rhumsiki, Waza, mont Cameroun, Limbé ; Yankari, Zuma Rock ; Pendjari, Tata Somba ;
  Koutammakou ; parc de Taï ; monts Nimba ; Lamu ; Tozeur (Chebika). Liste et raisons : `PAYS_RETIRES` et `RETIRES` dans scripts/visiter.py.
- Relevé fait à partir d'extraits des fiches officielles (site non joignable depuis la session) : à revérifier sur diplomatie.gouv.fr avant de remettre un lieu
  ou d'en ajouter dans ces pays. Restent 29 pays et 217 lieux ; un pays est publié à partir de 4 lieux.

## 13 novembre 2026 : rubans en bas de l'accueil, optimisation
- Accueil : en bas de page, section « Envie d'explorer ? » avec deux rubans défilants (nouveautés, pays). Traductions dans site/i18n.js (dernier bloc).
- Polices : Fraunces en une seule graisse (600) et taille optique fixe : 79 Ko de polices par page au lieu de 184 Ko. Anciennes polices supprimées
  (Bricolage, Plus Jakarta, Instrument, JetBrains). Si un titre doit changer de graisse, il faudra recharger une autre version de Fraunces.
- Script de langue écrit dans chaque page (scripts/build_pages.py, `_langue_inline`) : site/langue.js reste la source.
- « Que visiter » : les cartes annoncent 70 % de la largeur d'écran (version 640 px sur les téléphones courants) ; les photos d'ouverture ont une
  version 820 px (`<clé>-820.webp`, à créer pour tout nouveau pays : PIL, largeur 820, qualité 66).
- Animations décoratives (formes du haut de page, avion du logo) : quelques secondes puis repos.

## 13 novembre 2026 : copie de secours des relevés (alerte « erreur serveur 5xx » de Google)
- Le 12 novembre, la Search Console a signalé des « erreurs serveur (5xx) » sur des pages du sitemap. Cause : le 11 novembre, le quota
  gratuit de KV a été dépassé (100 000 lectures à 15 h 32 UTC, puis écritures et listes) ; jusqu'à minuit UTC, les pages écrites à partir
  des relevés (245 pages « bons plans » par ville et par mois, « à saisir » en français et en anglais) ont répondu 503.
- src/lot.ts : la copie groupée des relevés est aussi gardée 30 heures dans le cache de chaque centre de données (`__lot/v1/secours`).
  Si KV refuse les lectures, ces pages continuent d'afficher le relevé du matin au lieu de répondre 503. Sans copie (centre de données
  qui n'a pas vu les relevés depuis 30 heures), la réponse reste 503 avec « Retry-After ».
- Contrôle du 13 novembre : les 245 adresses de /barometre-prix/plan.xml et 11 autres pages écrites par le serveur répondent 200.

## 13 novembre 2026 : consommation Cloudflare mesurée, lectures KV des pages trajets supprimées
- Mesure sur 24 heures (journaux du Worker, API Cloudflare) : 22 900 appels du Worker (plafond gratuit : 100 000 par jour), dont 41 % de
  pages trajets et 35 % d'accueil avec une recherche préremplie (`/?type=vols&from=…`, presque uniquement des robots). Plus de la moitié
  des appels viennent de robots (Yandex 17 %, aperçus Meta, Bing, Semrush, Amazon, Exa, MJ12…). KV : 35 600 lectures (plafond 100 000),
  531 écritures (plafond 1 000), 25 listes.
- Diagnostic : une requête envoyée avec l'en-tête `X-Escale-Diag: 1` reçoit dans `X-Escale-KV` le détail des opérations KV qu'elle a
  coûtées (src/worker.ts). Sans cet en-tête, rien ne change.
- Pages trajets : la clé `paye:FROM-TO` n'est lue que si le trajet a une déclaration (inventaire gardé 10 minutes, src/api/paye.ts) ;
  le relevé « léger » lu dans KV est gardé 30 minutes dans le cache du centre de données (src/bonsplans.ts) ; les prix par mois ne sont
  plus revérifiés quand le relevé de la nuit les a déjà écrits (copie groupée). Une page d'un trajet suivi passe de 3 ou 4 lectures à 1,
  une page d'un trajet non suivi de 1 ou 2 lectures à 0.
- `/api/verdict` (« Acheter ou attendre ? ») : 1 lecture (copie groupée) au lieu de 90 à chaque calcul.
- À surveiller : les écritures (531 sur 1 000 par jour) : relevé de la nuit, une écriture par trajet suivi et par jour, compteur de clics.

## 13 novembre 2026 : trois chantiers tirés de la Search Console (4 semaines de données, 15 oct. – 10 nov.)
Données : 16 492 affichages, 97 clics ; les pages trajets font les deux tiers des affichages en position moyenne 45 ; la moitié des clics
arrivent sur l'accueil. Trois endroits où la demande existait et où la page y répondait mal :
- **Hôtels à Bamako, Douala, Lomé** (positions 11 à 18) : bloc détaillé pour Lomé en français (`HOTELS_FR`, scripts/build_pages.py) et en
  anglais (scripts/trajets_en.py), au niveau de Bamako et Douala ; vraie photo créditée en haut de toutes les pages hôtels
  (`hotel_photo`, scripts/build_i18n.py : photos.json, sinon une photo de « Que visiter » pour Douala et Lomé) ; liens croisés entre la
  page hôtels et le guide « arriver à l'aéroport » de la ville (français et anglais).
- **Italie → Maurice** (« voli per mauritius », position 23, page sans départ italien) : nouvelles pages `it/voli-milano-mauritius` et
  `it/voli-roma-mauritius` (scripts/italia.py), listées en tête de `it/voli-per-mauritius`. Durées estimées d'après la distance, comme
  les autres trajets italiens ; aucune information de visa ou de santé ajoutée.
- **« cheap flights » tapée en Tunisie et en Algérie** (1 041 affichages en position 7,5, aucun clic, sur les pages « vols pour Tunis /
  Alger ») : ces pages montrent maintenant, juste sous l'en-tête, les vols AU DÉPART de la ville avec leurs prix (scripts/hubs.py,
  `FROM_T`). Le bloc vaut pour toutes les villes qui ont une page « au départ de » (42 pages en français, anglais et arabe).
  « Vous partez de Alger » corrigé en « d'Alger ».
- À revoir dans trois ou quatre semaines avec un nouvel export : position des pages hôtels, clics sur « cheap flights », affichages de
  `it/voli-*-mauritius`.
| 2026-11-13 | À la demande de Dobam (« Fais tout », lot 1) : pages hôtels de Yaoundé, Libreville, Kigali, Abuja, Brazzaville et Zanzibar en 7 langues (`scripts/hotels_plus.py`, photos Wikimedia de Kigali et Brazzaville) ; pages « Meilleur mois pour partir » de Bamako, Conakry, Cotonou, Lomé, Douala, Kinshasa et Ouagadougou en 4 langues (renvoi aux conseils aux voyageurs pour le Mali, le Burkina Faso et la RD Congo) ; Tabaski 2027 : Banjul, Lomé, Cotonou et Douala ajoutées, et calendrier des prix jour par jour (avril à juin 2027, `data-months` dans `site/route-calendar.js`) |
| 2026-11-13 | « Fais tout », lot 2 : outil « Match des aéroports » (`/match-des-aeroports/`, `site/match.js`, prix lus dans `/api/verdict`, 16 destinations avec au moins deux villes de départ) et page « Les 4 astuces » pour les visiteurs venus des vidéos (`/astuces-billets-afrique/`), toutes deux dans le ruban « Nouveautés » de l'accueil (`scripts/malin.py`) |
| 2026-11-13 | « Fais tout », lot 3 (technique) : compteur de clics en une seule écriture KV par clic (la page d'origine est rangée sous `@/chemin` dans `clics:`, lecteurs `admin.ts` et `digest.ts` adaptés, anciens jours `pages:` toujours lus) ; boutons sur fond turquoise foncé `--teal-fond` (#0b8577, contraste 4,5 avec le blanc) en mode clair ; `rel="nofollow"` sur les liens de recherche préremplie (`/?type=`) |
| 2026-11-13 | Optimisation (demande de Dobam) : contrôle des 5 616 pages (aucun titre ou description manquant ou en double, aucun lien cassé, une seule balise h1 partout) ; polices du haut de page préchargées sur les accueils seulement (mesure avec et sans : ailleurs, cela retardait le premier texte de 0,15 s) (`FONT_PRELOAD` dans `scripts/build_pages.py`) ; historique des pages trajets gardé 30 minutes dans le cache du centre de données (`readHistoryCached`, une lecture KV de moins par page vue). Photos déjà compressées au mieux : rien à gagner |
| 2026-11-13 | Accueil : photo d'en-tête retirée à la demande de Dobam (bloc `hero-bg` de `site/index.html` et chargement de photo d'`accueil.js`) ; le titre et le moteur de recherche s'affichent sur le fond clair d'origine |
| 2026-11-13 | Accueil : les prix « dès … » des pastilles de pays qui défilent sont retirés à la demande de Dobam (`site/ruban.js`) ; chaque pastille montre le pays et mène à sa page. L'appel à `/api/ruban` n'est plus fait par l'accueil |
| 2026-11-13 | Pages « Que visiter » d'un pays : le visiteur écrit lui-même sa ville ou son aéroport de départ (champ avec suggestions parmi 3 200 aéroports, `site/ac-mini.js` chargé au premier toucher), à la place de la liste fermée de 17 villes ; son choix reste dans son appareil (`escale.aeroport`). Demande de Dobam |
| 2026-11-13 | « Que visiter » : champ libre « ville ou aéroport » aussi sur la page « Comparer deux pays » et dans le formulaire d'alerte prix des envies (aide partagée `VX.champDepart` dans `site/visiter.js`) ; correction d'une perte de saisie quand les suggestions se chargeaient pendant la frappe |
| 2026-11-13 | « Que visiter » (sommaire) : champ libre « Je pars de : ville ou aéroport » au-dessus de la carte du monde ; les prix de la carte ne sont plus déduits du pays du visiteur, ils apparaissent quand il a écrit son départ (`site/visiter-carte.js`) |
| 2026-11-13 | Match des aéroports : champ libre « Je pars de : ville ou aéroport » ; le départ du visiteur entre dans le classement (« Votre départ ») avec le prix le plus bas des six prochains mois lu dans `/api/calendar` (6 appels, gardés 3 h), ou un message s'il n'y a pas de prix repéré ; pastille de destination choisie lisible en mode sombre |
| 2026-11-13 | Recherche en direct (`/recherche/`) : le moteur Travelpayouts est demandé tout en haut de la page (`modulepreload`) et lancé dans la page même (contenu de `site/wl.js`), au lieu d'attendre la feuille de style et les scripts différés : demandé environ 0,8 s plus tôt sur réseau mobile lent. La durée de la « Recherche de fournisseurs » elle-même dépend de Travelpayouts |
| 2026-11-13 | Accueil : recherche « en plein écran » à la demande de Dobam (`site/recherche-plein.js`) : sur téléphone, toucher Départ ou Arrivée ouvre un écran entier où les villes sortent avec leurs aéroports dessous ; toucher une date ouvre un calendrier de 12 mois avec le prix aller-retour le plus bas repéré sous chaque jour (`/api/calendar`, un appel par mois affiché), les moins chers en vert. Les champs du formulaire restent la référence ; sans ce script, rien ne change |
| 2026-11-13 | Indice des prix : série quotidienne téléchargeable en données libres (`/indice-prix/donnees.csv`, `/en/price-index/data.csv`, CC BY 4.0) : médianes par jour et par périmètre (ensemble, région d'arrivée, zone de départ), calculées par Escale, sans prix de trajet ni de vendeur ; lien sous l'indice et `distribution` dans les données structurées. Sert de base au dépôt sur les plateformes de données ouvertes |
| 2026-11-13 | Message WhatsApp : liens cliquables (adresses complètes en https://, et adresse courte `/v/LYS-ALG` qui redirige vers la recherche préremplie, `src/worker.ts`), à la demande de Dobam : WhatsApp ne rendait cliquable ni « escale.live/… » sans https, ni la fin d'une adresse coupée après « ? » |
| 2026-11-13 | Message WhatsApp, suite : l'e-mail du lundi et du jeudi a un bouton vert qui ouvre `/outils/whatsapp/?auto=1` (message préparé tout de suite, gros bouton « Copier le message » et lien vers la chaîne) ; la page outil écrit elle aussi des liens complets et courts (`https://escale.live/v/LYS-ALG`). Dobam n'arrivait pas à coller le message depuis l'e-mail |
| 2026-11-13 | Reprise de la tâche « nouveauté tous les 2 jours » (arrêtée le 7 novembre, accès GitHub coupé) : guide « Prendre l'avion enceinte : jusqu'à quand peut-on voyager ? » en 5 langues (`/guides/avion-enceinte/`) — prochain : page hôtels |
| 2026-11-13 | Outil « Partage des frais du voyage » en 5 langues (`/partage-frais-voyage/`, `en/split-trip-costs`, `es/dividir-gastos-viaje`, `pt/dividir-despesas-viagem`, `ar/split-trip-costs` ; `scripts/partage_frais.py`, `site/frais.js`) : voyageurs, dépenses, qui doit combien à qui avec le moins de virements possible, résumé WhatsApp. Tout est calculé et gardé dans le navigateur ; le lien de partage contient le compte (après le #). Textes es, pt et ar à faire relire |
| 2026-11-14 | Photos sur toutes les destinations (demande de Dobam) : une vraie photo créditée de la ville d'arrivée sous le titre des pages trajets (toutes langues), « vols pour… », fêtes et guides d'aéroport, en plus des pages hôtels (`dest_photo_data` dans `scripts/build_i18n.py`, passe finale de `scripts/build_pages.py`, chargement différé) ; 48 nouvelles photos de villes Wikimedia Commons (clés `v-<code>` de `site/data/visiter-photos.json`, créditées sur `/credits-photos/`) ; les autres réutilisent les photos déjà présentes. Mali, Burkina Faso et RD Congo : photo de ville neutre sur les pages de vols, toujours rien dans « Que visiter » |
| 2026-11-14 | Netlify : `ignore = "exit 0"` dans `netlify.toml`, pour que l'ancien site Netlify (qui ne sert plus qu'à rediriger vers escale.live) ne soit plus refabriqué à chaque envoi sur GitHub. Ces publications inutiles ont épuisé le quota gratuit du mois en une journée le 12 novembre (19 envois ce jour-là) |
| 2026-11-14 | Accueil : les « trajets populaires » quittent le dessous du moteur de recherche et défilent en ruban sous le titre, au-dessus des pays (demande de Dobam). Étiquette + trajets écrits deux fois pour une boucle continue ; remplis pour la ville de départ du visiteur par `site/app.js` (`heroPopular`) et, pour les pays suivis, par `src/accueil.ts` |
| 2026-11-14 | Accueil : les pastilles des deux rubans du haut (trajets populaires, pays) montrent qu'elles se touchent : bord turquoise, petite flèche ronde à droite, léger enfoncement au toucher (CSS seul, `site/index.html`). Demande de Dobam |
