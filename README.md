# Escale

Comparateur de voyages : vols les moins chers, hôtels et locations de voitures.

Site statique hébergé sur **Cloudflare Pages**, avec quelques fonctions serveur (`functions/`).

- **Vols** : liste de vols avec prix réels repérés (Travelpayouts / Aviasales), bande de dates ±3 jours,
  tri moins cher / plus rapide / meilleur, filtre vols directs ; comparaison sur Skyscanner, Kayak, momondo, Aviasales.
- **Hôtels** : Booking.com, Google Hôtels, Kayak, Hotels.com, Agoda, Airbnb.
- **Voitures** : Kayak, momondo, recherche Google, Rentalcars et Discover Cars.

Les prix réels s'affichent sur les sites partenaires, où se fait la réservation.

Aussi : liens de recherche partageables (WhatsApp), destinations populaires, FAQ, référencement
(données structurées, Open Graph, sitemap), appli installable, emplacements pour l'affiliation.

Pour faire grandir le site : voir [CROISSANCE.md](CROISSANCE.md).

## Structure

- `site/` : le site publié (pages générées comprises, déjà construites dans le dépôt).
- `scripts/build_pages.py` : génère les pages trajets, hôtels, guides, pages légales et le sitemap
  (+ `build_i18n.py`, `translations.py`, `routes_extra.py`, `guides.py`, `about.py`).
- `site/app.js` + `site/i18n.js` : le moteur de l'accueil (5 langues, devises, recherche, résultats).
- `functions/` : fonctions Cloudflare Pages
  - `api/prix`, `api/explore`, `api/calendar`, `api/deals` : prix réels (variable `TRAVELPAYOUTS_TOKEN`) ;
  - `api/geo` : ville et pays approximatifs du visiteur (aéroport et devise par défaut) ;
  - `api/form` : formulaires contact et bons plans, lus sur `/admin/` (variable `ADMIN_KEY`) ;
  - `api/alert` + `api/cron` : alertes prix par e-mail (`RESEND_API_KEY` ou `BREVO_API_KEY`, `ALERT_FROM`, `CRON_KEY`) ;
  - `_middleware.ts` : prix dans l'aperçu des liens partagés (WhatsApp, Facebook…).
- `site/_headers`, `site/_routes.json` : en-têtes HTTP et chemins qui passent par les fonctions.
- `.github/workflows/quotidien.yml` : vérification quotidienne des alertes, envoi des pages à IndexNow.
- `netlify.toml` : redirection de l'ancienne adresse escale-voyage.netlify.app vers la nouvelle.

## Générer les pages

```
python3 scripts/build_pages.py
python3 -m http.server -d site 8000
```

Toujours lancer la génération avant d'envoyer sur GitHub : Cloudflare publie le dossier `site/` tel quel.

## Mise en ligne sur Cloudflare Pages (gratuit)

1. Cloudflare > **Workers & Pages** > **Create** > **Pages** > **Connect to Git** > dépôt `escale-voyage`.
2. Nom du projet : `escale-voyage`. Branche : `main`. Framework : *None*. **Build command : vide**.
   **Build output directory : `site`**. Valider : chaque envoi sur `main` publie le site.
3. **Settings > Variables and Secrets** (type *Secret*) : `TRAVELPAYOUTS_TOKEN`, `ADMIN_KEY`
   (et plus tard `RESEND_API_KEY`/`BREVO_API_KEY`, `ALERT_FROM`, `CRON_KEY`). Puis redéployer.
4. **Storage & Databases > KV** > *Create* un espace nommé `escale` ; puis dans le projet
   **Settings > Bindings > Add > KV namespace** : nom de variable **`ESCALE`**, espace `escale`. Redéployer.
5. **Metrics > Web Analytics** : activer (statistiques de visites sans cookie).
6. Si le nom `escale-voyage.pages.dev` n'est pas disponible : changer `DEFAULT_DOMAIN` dans
   `scripts/build_pages.py`, l'adresse dans `netlify.toml` et `SITE_URL` du workflow, puis régénérer.

## Nom de domaine

Cloudflare > projet > **Custom domains** > *Set up a domain*. Puis changer `DEFAULT_DOMAIN` dans
`scripts/build_pages.py` et régénérer : adresses officielles, sitemap, hreflang et images de partage suivent.
