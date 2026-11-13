# Nouveautés automatiques (tous les 2 jours)

Une tâche planifiée de Claude ajoute une nouveauté au site tous les 2 jours, l'envoie sur `main`
(Cloudflare publie, IndexNow signale les pages) et la note ici. Ce journal évite de refaire deux fois la même chose.

## Règles
- Une seule nouveauté par passage, utile aux voyageurs et bonne pour Google, en 5 langues (fr, en, es, pt, ar).
- Tourner entre les types, dans cet ordre : **guide pratique** → **nouveaux trajets** → **page hôtels d'une ville** → guide pratique…
- Rien d'inventé : pas de prix, d'horaires ou de règles précises qu'on ne peut pas vérifier ; rester général et renvoyer aux sources officielles.
- Toujours lancer `python3 scripts/build_pages.py` (et `node scripts/make_og.js` si de nouveaux trajets) avant d'envoyer.

## Idées en réserve
- Guides : visa et passeport (généralités), voyager pendant le ramadan / la Tabaski,
  assurance voyage, voyager enceinte,
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
