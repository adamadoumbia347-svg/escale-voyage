# Escale

Comparateur de voyages : vols les moins chers, hôtels et locations de voitures.

Site statique hébergé sur **Cloudflare Workers** (fichiers de `site/`), avec quelques fonctions serveur (`src/`).

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
- `src/worker.ts` : point d'entrée du Worker Cloudflare, qui aiguille vers :
  - `api/prix`, `api/explore`, `api/calendar`, `api/deals` : prix réels (secret `TRAVELPAYOUTS_TOKEN`) ;
  - `api/geo` : ville et pays approximatifs du visiteur (aéroport et devise par défaut) ;
  - `api/form` : formulaires contact et bons plans, lus sur `/admin/` (secret `ADMIN_KEY`) ;
  - `api/alert` + `api/cron` : alertes prix par e-mail (`RESEND_API_KEY` ou `BREVO_API_KEY`, `ALERT_FROM`, `CRON_KEY`) ;
  - `apercu-prix.ts` : prix dans l'aperçu des liens partagés (WhatsApp, Facebook…).
- `wrangler.jsonc` : configuration du Worker (dossier publié, stockage KV `escale`, adresses qui passent par le code).
- `site/_headers` : en-têtes HTTP (cache, pages privées).
- `.github/workflows/quotidien.yml` : vérification quotidienne des alertes, envoi des pages à IndexNow.
- `netlify.toml` : redirection de l'ancienne adresse escale-voyage.netlify.app vers la nouvelle.

## Générer les pages

```
python3 scripts/build_pages.py
python3 -m http.server -d site 8000
```

Toujours lancer la génération avant d'envoyer sur GitHub : Cloudflare publie le dossier `site/` tel quel.

## Mise en ligne sur Cloudflare (gratuit)

Le Worker `escale-voyage` est relié au dépôt GitHub : chaque envoi sur `main` le publie (`npx wrangler deploy`).

- Secrets (Workers & Pages > escale-voyage > Paramètres > Variables et secrets) : `TRAVELPAYOUTS_TOKEN`, `ADMIN_KEY`
  (et plus tard `RESEND_API_KEY`/`BREVO_API_KEY`, `ALERT_FROM`, `CRON_KEY`).
- Stockage : l'espace KV `escale` est relié par `wrangler.jsonc` (variable `ESCALE`).
- Test en local : `npx wrangler dev` (secrets de test dans un fichier `.dev.vars`, jamais envoyé sur GitHub).
- Adresse : `DEFAULT_DOMAIN` dans `scripts/build_pages.py`, `SITE_URL` du workflow et `netlify.toml` doivent
  correspondre à l'adresse publique du Worker (ou à votre nom de domaine).

## Nom de domaine

Cloudflare > Worker escale-voyage > Paramètres > **Domaines et itinéraires** > *Ajouter* > *Domaine personnalisé*. Puis changer `DEFAULT_DOMAIN` dans
`scripts/build_pages.py` et régénérer : adresses officielles, sitemap, hreflang et images de partage suivent.
