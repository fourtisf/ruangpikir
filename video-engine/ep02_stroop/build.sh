#!/usr/bin/env bash
# Render EP02. Pakai suara yang sudah ada di vo/. Tambah --voice untuk generate ulang suara (butuh GEMINI_API_KEY).
set -e
cd "$(dirname "$0")"
if [ "$1" = "--voice" ]; then
  export GEMINI_TTS_MODEL=${GEMINI_TTS_MODEL:-gemini-3.8-flash-tts}
  python3 countdown.py                       # baris hitung mundur dibuat terpisah (punya jeda internal)
  python3 vo_rest.py 0,2,3,4,5,6,7,8,9       # baris lain dalam 1 request, lalu dipotong otomatis
  python3 tighten_countdown.py               # rapatkan jeda + simpan waktu tiap kata untuk sinkron angka di layar
fi
python3 stroop.py timeline timeline.json
python3 audio.py timeline.json audio.wav
python3 stroop.py video raw.mp4
ffmpeg -y -loglevel error -i raw.mp4 -i audio.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:v libx264 -preset slow -crf 24 -tune animation -x264-params aq-mode=3 -pix_fmt yuv420p -profile:v high \
  -c:a aac -b:a 128k -ar 44100 -shortest -movflags +faststart ruang-pikir-ep02.mp4
rm -f raw.mp4 audio.wav timeline.json
echo "Selesai: ruang-pikir-ep02.mp4"
