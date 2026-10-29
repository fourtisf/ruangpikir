#!/usr/bin/env bash
# Suara EP08 dengan resep EP01 (suara acuan ALFA): voice Achird, model gemini-3.1-flash-tts-preview,
# instruksi gaya panjang EP01, semua kalimat dalam 1 request, dipotong di jeda terpanjang (vo_full.py).
# Selalu cek hasilnya dengan transkripsi: instruksi tidak boleh ikut terbaca.
set -e
cd "$(dirname "$0")"
python3 vo_full.py
python3 tighten.py 0.25     # jeda > 0,25 dtk di dalam kalimat dipendekkan (durasi video tetap <= 55 dtk)
