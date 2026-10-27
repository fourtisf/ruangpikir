#!/usr/bin/env bash
# Suara EP03 (Achird, tanpa prefix gaya). Dipecah jadi beberapa request kecil supaya pemotongan per baris akurat.
# Kuota gratis ±3 request/menit, jadi ada jeda di antara request.
set -e
cd "$(dirname "$0")"
export GEMINI_TTS_MODEL=${GEMINI_TTS_MODEL:-gemini-3.8-flash-tts}
CHUNKS=${*:-"0,1 2 3,4 5,6 7,8 9,10"}
first=1
for c in $CHUNKS; do
  [ $first = 1 ] || sleep 22
  first=0
  python3 vo_rest.py "$c"
done
