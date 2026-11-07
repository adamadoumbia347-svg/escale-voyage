#!/bin/bash
# À lancer une seule fois sur le Chromebook (Linux) : installe ffmpeg, les polices emoji et Chromium pour fabriquer les vidéos.
set -e
sudo apt-get update -qq
sudo apt-get install -y -qq ffmpeg fonts-noto-color-emoji fonts-noto-core >/dev/null
mkdir -p "$HOME/outils-video" && cd "$HOME/outils-video"
[ -f package.json ] || npm init -y >/dev/null
npm i playwright >/dev/null
npx playwright install --with-deps chromium
echo "C'est prêt : pour faire les vidéos, lancez  bash ~/escale-voyage/video/videos.sh"
