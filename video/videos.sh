#!/bin/bash
# Fabrique les vidéos TikTok sur le Chromebook, sans GitHub : français, italien et anglais, avec les prix du jour.
# Résultat : « Fichiers Linux › videos-escale » (une vidéo .mp4 et sa légende .txt par langue).
# Pour forcer un format : FORMAT=pays-quiz bash ~/escale-voyage/video/videos.sh
cd "$(dirname "$0")/.." || exit 1
export NODE_PATH="$HOME/outils-video/node_modules" NO_SEND=1
DEST="$HOME/videos-escale"; mkdir -p "$DEST"
for L in fr it en; do
  echo "— Vidéo $L…"
  if LANG_VIDEO=$L node video/make.js; then cp video/out/*.mp4 video/out/*.txt "$DEST"/; else echo "Vidéo $L non faite"; fi
done
echo "Terminé : vos vidéos sont dans Fichiers Linux › videos-escale"
