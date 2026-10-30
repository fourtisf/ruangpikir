#!/usr/bin/env bash
# Render EP11 (CRF 26: animasi padat, SSIM ±0,996). Pakai suara yang sudah ada di vo/. Tambah --voice untuk generate ulang suara (butuh GEMINI_API_KEY di .env).
set -e
cd "$(dirname "$0")"
[ "$1" = "--voice" ] && ./voice.sh       # suara baru (resep EP01, lihat vo_full.py)
python3 episode.py timeline timeline.json
python3 audio.py timeline.json audio.wav
python3 episode.py video raw.mp4
ffmpeg -y -loglevel error -i raw.mp4 -i audio.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:v libx264 -preset slow -crf 26 -tune animation -x264-params aq-mode=3 -pix_fmt yuv420p -profile:v high \
  -c:a aac -b:a 128k -ar 44100 -shortest -movflags +faststart ruang-pikir-ep11.mp4
rm -f raw.mp4 audio.wav timeline.json
echo "Selesai: ruang-pikir-ep11.mp4"
