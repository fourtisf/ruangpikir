#!/usr/bin/env bash
# Suara EP03: voice Achird, model gemini-3.8-flash-tts (sama dengan EP02).
# Model ini sekarang ikut membacakan prefix gaya EP02 ("Ucapkan dengan santai..."), jadi dikirim TANPA prefix,
# 2 kalimat per request supaya pemotongan per baris akurat, lalu slow_voice.py memperlambat temponya
# (tanpa mengubah nada) supaya mendekati EP02. Selalu cek hasilnya dengan transkripsi.
# Kuota gratis ±3 request/menit, jadi ada jeda di antara request.
set -e
cd "$(dirname "$0")"
export GEMINI_TTS_MODEL=${GEMINI_TTS_MODEL:-gemini-3.8-flash-tts}
export VO_STYLE=${VO_STYLE-}
CHUNKS=${*:-"0,1 2 3,4 5,6 7,8 9,10"}
first=1
for c in $CHUNKS; do
  [ $first = 1 ] || sleep 22
  first=0
  python3 vo_rest.py "$c"
done
python3 slow_voice.py 0.85
