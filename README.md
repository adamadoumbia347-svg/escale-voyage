# Escale

Comparateur de voyages : vols les moins chers, hôtels et locations de voitures.

Une seule page (`index.html`, sans dépendance ni serveur). Vous remplissez un formulaire et Escale
prépare la recherche, déjà triée par prix, sur les grands comparateurs :

- **Vols** : Google Flights, Skyscanner, Kayak, momondo (dates flexibles ±3 jours, vols directs,
  classe, enfants, destination « partout »), plus une grille jour par jour.
- **Hôtels** : Booking.com, Google Hôtels, Kayak, Hotels.com, Agoda, Airbnb.
- **Voitures** : Kayak, momondo, recherche Google, Rentalcars et Discover Cars.

Les prix réels s'affichent sur les sites partenaires, où se fait la réservation.

Aussi : liens de recherche partageables (WhatsApp), destinations populaires, FAQ, référencement
(données structurées, Open Graph, sitemap), appli installable, emplacements pour l'affiliation.

Pour faire grandir le site : voir [CROISSANCE.md](CROISSANCE.md).

## Structure

- `site/` : le site publié (page d'accueil, pages générées, icônes).
- `scripts/build_pages.py` : génère les pages trajets, légales, contact et le sitemap. Lancé automatiquement par Netlify.
- `scripts/build_i18n.py` + `scripts/translations.py` : versions anglaise, espagnole, portugaise et arabe des pages trajets et hôtels.
- `site/app.js` : le moteur de l'accueil (recherche mondiale, 5 langues, devises, idées de voyage, animations).
- `site/i18n.js` : traductions espagnol, portugais et arabe de l'accueil (clé = texte anglais).
- `site/data/airports.json` : 3 214 aéroports avec vols réguliers dans 234 pays (OurAirports, domaine public),
  régénéré par `scripts/build_airports.py`.
- `netlify/functions/prix.mts` : prix indicatifs d'un trajet (variable `TRAVELPAYOUTS_TOKEN`).
- `netlify/functions/explore.mts` : destinations les moins chères depuis un aéroport.
- `netlify/functions/geo.mts` : ville et pays approximatifs du visiteur (aéroport et devise par défaut).
- `netlify/functions/calendar.mts`, `deals.mts` : calendrier des prix et bons plans de la semaine.
- `netlify/functions/alert.mts` + `alerts-check.mts` (tous les jours à 6 h UTC) : alertes prix par e-mail.
  Variables : `RESEND_API_KEY` ou `BREVO_API_KEY`, et `ALERT_FROM` (ex. `Escale <alertes@votre-domaine.com>`).
- `netlify/functions/hit.mts`, `stats.mts`, `stats-rollup.mts` : statistiques anonymes sans cookie, lues sur `/stats/` avec `STATS_KEY`.
- `netlify/edge-functions/apercu-prix.ts` : ajoute le prix dans l'aperçu des liens partagés (robots des réseaux sociaux uniquement).
- `scripts/routes_extra.py`, `scripts/guides.py`, `scripts/about.py` : trajets supplémentaires, guides pratiques, page À propos.
- `scripts/make_og.js` : régénère les images de partage `site/og/` (Playwright) après ajout de trajets.
- `netlify.toml` : configuration Netlify.

## Lancer

```
python3 scripts/build_pages.py
python3 -m http.server -d site 8000
```

En ligne : https://escale-voyage.netlify.app (projet Netlify `escale-voyage`).

## Déploiement automatique depuis GitHub

1. Netlify > projet `escale-voyage` > **Project configuration** > **Build & deploy** > **Continuous deployment** > **Link repository**.
2. Choisir **GitHub**, autoriser l'application Netlify sur le dépôt `escale-voyage`, puis sélectionner ce dépôt.
3. **Branch to deploy** : `main` (déjà fait : chaque envoi sur `main` publie le site).
   Les champs « Build command » et « Publish directory » sont lus dans `netlify.toml` : laisser vides.
4. Valider. Chaque `git push` sur cette branche régénère les pages (`scripts/build_pages.py`) et publie le site.

## Nom de domaine

Acheter le nom, l'ajouter dans Netlify (Domain management > Add a domain) et le définir comme domaine principal.
Au déploiement suivant, `scripts/build_pages.py` lit la variable `URL` fournie par Netlify : adresses officielles,
sitemap, hreflang et image de partage passent automatiquement sur le nouveau nom. Aucune modification de code.
