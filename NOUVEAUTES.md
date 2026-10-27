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
  assurance voyage, voyager enceinte, vol de nuit,
  droits en cas de retard (règlement européen 261/2004), envoyer des colis au pays.
- Trajets : nouvelles villes de départ (Rennes, Milan, Francfort, Bâle-Mulhouse, Barcelone…) vers l'Afrique et le Maghreb.
- Hôtels : Nairobi, Addis-Abeba, Libreville, Yaoundé, Niamey, Ouagadougou, Nouakchott.

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
