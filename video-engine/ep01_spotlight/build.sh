#!/usr/bin/env bash
# Render EP01. Pakai suara yang sudah ada di vo/. Tambah --voice untuk generate ulang suara (butuh GEMINI_API_KEY).
set -e
cd "$(dirname "$0")"
if [ "$1" = "--voice" ]; then python3 gemini_tts.py script Achird; fi
python3 rp.py timeline timeline.json
python3 audio.py timeline.json audio.wav
python3 rp.py video raw.mp4
ffmpeg -y -loglevel error -i raw.mp4 -i audio.wav -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart ruang-pikir-ep01.mp4
rm -f raw.mp4 audio.wav timeline.json
echo "Selesai: ruang-pikir-ep01.mp4"
