# Escale : plan pour attirer plus de visiteurs

Ce qui est déjà fait dans le code, puis ce qu'il reste à faire, dans l'ordre où ça rapporte le plus.

## Déjà en place

| Amélioration | Pourquoi |
|---|---|
| Titre, description, mots-clés, `lang="fr"` | Google comprend de quoi parle le site |
| Données structurées `WebSite` et `FAQPage` | La FAQ peut apparaître directement dans les résultats Google |
| Image de partage (`og-image.png`) + balises Open Graph | Un bel aperçu quand le lien est partagé sur WhatsApp, Facebook, X |
| Liens de recherche partageables (`?type=vols&from=CDG&to=BKO…`) | Un visiteur envoie sa recherche à sa famille, qui arrive directement sur les résultats |
| Bouton « Partager sur WhatsApp » et « Copier le lien » | Le bouche-à-oreille est le premier canal pour la diaspora |
| Section « Destinations populaires » (Paris–Bamako, Dakar, Abidjan, Kinshasa…) | Contenu utile et mots-clés recherchés |
| FAQ de 6 questions | Répond aux vraies questions et nourrit le référencement |
| Appli installable (`manifest.webmanifest`, icônes) | « Ajouter à l'écran d'accueil » sur téléphone |
| `robots.txt` et `sitemap.xml` | À compléter avec le vrai domaine (voir étape 1) |
| Emplacements pour vos identifiants d'affiliation (`AFFILIATE` dans `index.html`) | Le site peut gagner de l'argent sans rien changer d'autre |

| 14 pages trajets (`/vol-paris-bamako/`, `/vol-paris-dakar/`…) avec FAQ structurée | Capter les recherches Google précises (« vol pas cher Paris Bamako ») |
| Pages Mentions légales, Confidentialité, Contact (formulaire enregistré sur Cloudflare) | Obligations légales et confiance des visiteurs |
| Fonction `/api/prix` (Travelpayouts) + encart « dès X € » | Affiche un prix réel dès que la clé est configurée |
| Projet Netlify `escale-voyage` créé, public, formulaires activés | Adresse : https://escale-voyage.netlify.app |
| Sitemap, robots.txt, liens canoniques sur cette adresse | Générés par `scripts/build_pages.py` |

## À faire

### 1. Site en ligne ✔
Publié sur https://escale-voyage.netlify.app (dépôt du dossier du projet sur Netlify).
Pour publier une mise à jour : redéposer le dossier du projet dans l'onglet Deploys, ou relier le dépôt GitHub
(Project configuration > Build & deploy > Link repository) pour des mises à jour automatiques.
Plus tard : un nom de domaine à vous (environ 10 €/an) ; changer alors `DOMAIN` dans `scripts/build_pages.py`
et l'adresse dans `site/index.html`.

### 2. Google ✔ (13 octobre 2026)
Site validé dans Google Search Console (fichier `site/google07cf151d39bf7608.html`, à ne pas supprimer) et sitemap envoyé.
À suivre chaque semaine dans Search Console : pages indexées, requêtes qui amènent des visiteurs.
Pour aller plus loin : ajouter des pages trajets (une par ligne recherchée) et des pages hôtels par ville,
puis les déclarer aussi dans Bing Webmaster Tools (import direct depuis Search Console).

### 3. Affiliation (en cours)
- ✔ Travelpayouts : script installé (chargé après accord via le bandeau cookies), identifiant 789659 ajouté aux liens Aviasales.
- À faire : liens partenaires Booking, Agoda, voitures (générés par l'outil de création de liens Travelpayouts ou les réseaux CJ / Agoda Partners),
  puis remplir l'objet `AFFILIATE` de `site/index.html`.

### 4. Prix réels ✔ (13 octobre 2026)
Clé `TRAVELPAYOUTS_TOKEN` ajoutée dans Netlify : l'encart « dès X € » s'affiche au-dessus des résultats de vols.
✔ Les prix (3 prochains mois) s'affichent aussi sur les 34 pages trajets, chargés à chaque visite via `site/route-prices.js`.

### 4 bis. Site international ✔ (13 octobre 2026)
3 214 aéroports dans 234 pays, interface FR/EN, 7 devises, aéroport de départ détecté, idées de voyage avec prix réels
(fonction `/api/explore`), panneau des départs animé.
✔ Pages trajets et hôtels traduites en anglais, espagnol, portugais et arabe (`/en/`, `/es/`, `/pt/`, `/ar/`), avec balises hreflang :
258 pages au total. Traductions dans `scripts/translations.py`, générateur `scripts/build_i18n.py`.
✔ Accueil (moteur de recherche) traduit en espagnol, portugais et arabe (`site/i18n.js`), arabe de droite à gauche.
Pistes suivantes : allemand, italien, chinois, turc (ajouter une colonne dans translations.py et une entrée dans UI).

### 4 ter. Nouveautés du 14 octobre 2026
- ✔ Page « Bons plans de la semaine » en 5 langues (`/bons-plans/`, `/en/deals/`…), fonction `/api/deals` mise en cache 6 h.
- ✔ Calendrier des prix sur les 170 pages trajets (fonction `/api/calendar`).
- ✔ Bloc « Avant de partir » : eSIM Airalo avec lien partenaire Travelpayouts (airalo.tpm.lv). Autres liens dans `site/data/partners.json`,
  à remplacer par vos liens partenaires Travelpayouts pour être rémunéré.
- ✔ GitHub relié à Netlify : chaque envoi sur `main` publie le site.

### 4 quater. Nouveautés du 14 octobre 2026 (suite)
- ✔ 139 nouveaux trajets (173 au total) depuis 13 villes de départ, en 5 langues.
- ✔ Image de partage par trajet (`site/og/`, `scripts/make_og.js`) ; sur WhatsApp/Facebook l'aperçu affiche « dès X € » (edge function `apercu-prix`).
- ✔ Guides pratiques (bagages, quand réserver, voyager avec des enfants) en 5 langues ; page À propos.
- ✔ Recherche « tout le mois », filtre budget sur les idées de voyage, calculateur du vrai prix (bagages et frais).
- ✔ Formulaire « bons plans » (e-mail / WhatsApp) : les inscrits sont dans Netlify > Forms > `bons-plans`.
- ✔ Alertes prix par e-mail (`/api/alert`, vérification quotidienne) : **s'affichent seulement quand** `RESEND_API_KEY` (ou `BREVO_API_KEY`) et `ALERT_FROM` sont définis dans Netlify.
- ✔ Statistiques sans cookie : tableau de bord `/stats/` (clé `STATS_KEY` dans les variables Netlify).
- ✔ Audit accessibilité (axe-core) : 0 erreur sur les pages principales, en clair et en sombre.

### 5. Réseaux sociaux et bouche-à-oreille
- Une **chaîne WhatsApp** « Bons plans billets Afrique » avec 2 ou 3 bons plans par semaine et le lien de recherche.
- Vidéos courtes TikTok et Instagram : « J'ai trouvé Paris–Dakar à X € : voici comment ».
- Groupes Facebook de la diaspora (Maliens, Sénégalais, Ivoiriens de France), en respectant leurs règles.

### 6. Faire revenir les visiteurs
- ✔ Alertes prix par e-mail (à activer avec une clé Resend ou Brevo).
- ✔ Inscription aux bons plans : envoyer chaque semaine un message aux inscrits.

### 7. Mesurer
- ✔ Statistiques sans cookie sur `/stats/` : pages vues, pages les plus vues, provenance, langues, clics par site partenaire.

### 8. Élargir le public
- Version anglaise, affichage en francs CFA (XOF) en plus des euros.
- Plus d'aéroports et de villes (actuellement environ 85).

### 9. Obligations légales (France)
- Page **mentions légales** (obligatoire) et **politique de confidentialité** ✔ (mise à jour : statistiques, bons plans, alertes prix).

## Sources
- [Travelpayouts : fonctionnement des programmes](https://support.travelpayouts.com/hc/en-us/articles/203955763)
- [PhocusWire : fermeture d'Amadeus Self-Service](https://www.phocuswire.com/amadeus-shut-down-self-service-apis-portal-developers)
- [Ignav : alternative après la fermeture d'Amadeus Self-Service](https://ignav.com/docs/amadeus-self-service-shutdown)

## Référencement Google (15 octobre 2026)
- ✔ Fil d'Ariane (BreadcrumbList) sur toutes les pages, nom du site (WebSite + Organization) sur l'accueil.
- ✔ Sitemap avec la vraie date de modification de chaque page (`scripts/lastmod.json`, mis à jour en lançant la génération en local).
- ✔ IndexNow : à chaque mise en ligne, `netlify/functions/deploy-succeeded.mts` envoie toutes les pages à Bing (et DuckDuckGo, Yahoo, Ecosia).
- À faire : nom de domaine à soi, Bing Webmaster Tools, liens depuis d'autres sites (associations, blogs, groupes de la diaspora), suivi mensuel dans Search Console.

## Déménagement sur Cloudflare (14 octobre 2026)
- Les crédits gratuits de Netlify (300 par mois, 15 par mise en ligne) étaient épuisés : le site passe sur Cloudflare Workers (gratuit).
- Nouvelle adresse : https://escale.live ; l'ancienne redirige (301) dès que Netlify accepte une nouvelle mise en ligne.
- Formulaires (contact, bons plans) lus sur `/admin/` ; statistiques dans Cloudflare Web Analytics.
- À faire : ajouter la nouvelle adresse dans Google Search Console (et Bing Webmaster Tools), renvoyer le sitemap,
  puis utiliser l'outil « Changement d'adresse » de Search Console une fois la redirection active.

## Nom de domaine escale.live (octobre 2026)
- Domaine acheté chez Squarespace, serveurs de noms confiés à Cloudflare, branché sur le Worker (escale.live et www.escale.live).
- Toutes les adresses officielles (canonical, sitemap, hreflang, images de partage) pointent vers https://escale.live.
- À faire : Search Console (propriété « Domaine » escale.live), renvoyer le sitemap, Bing Webmaster Tools.
