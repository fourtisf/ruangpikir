#!/usr/bin/env python3
"""Suara EP03 dengan resep EP01 (suara acuan ALFA): voice Achird, model gemini-3.1-flash-tts-preview,
instruksi gaya panjang EP01, semua kalimat dalam 1 request, lalu dipotong di jeda terpanjang.
python3 vo_full.py   ->  vo/full.wav, vo/lNN.wav, vo/lines.json"""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('GEMINI_TTS_MODEL', 'gemini-3.1-flash-tts-preview')
import gemini_tts as g
g.MODEL = os.environ['GEMINI_TTS_MODEL']
from vo import LINES, OUT, HERE
STYLE = ("Bacakan dalam bahasa Indonesia gaul yang santai, ramah, hangat dan ekspresif, seperti kreator konten TikTok "
         "yang lagi cerita fakta seru ke temannya. Senyum saat bicara, intonasi naik di pertanyaan, antusias di bagian kejutan. "
         "Tempo agak cepat dan energik, jangan lambat. Di kalimat pertama terdengar penasaran, di bagian angka riset terdengar kaget, di bagian akhir hangat menenangkan.")
text = '\n\n'.join(t for _, t in LINES)
x = None
for attempt in range(5):
    try:
        x = g.tts(text + '\n', 'Achird', STYLE + ' Beri jeda sekitar satu detik di antara setiap baris.'); break
    except SystemExit as e:
        print('ulang:', str(e)[:200], flush=True); time.sleep(30 + 20 * attempt)
if x is None: sys.exit('gagal membuat suara')
g.save(os.path.join(OUT, 'full.wav'), x)
segs = g.split_by_pauses(x, len(LINES))
meta = []
for i, ((anchor, t), s) in enumerate(zip(LINES, segs)):
    s = s.copy(); fi, fo = min(220, len(s) // 4), min(1300, len(s) // 4)   # fade 5 ms / 30 ms: tanpa bunyi klik
    s[:fi] *= np.linspace(0, 1, fi); s[len(s) - fo:] *= np.linspace(1, 0, fo)
    p = os.path.join(OUT, f'l{i:02d}.wav'); g.save(p, s)
    meta.append({'i': i, 'anchor': anchor, 'text': t, 'file': os.path.relpath(p, HERE), 'dur': round(len(s) / 44100, 3)})
    print(f'{i:2d} {len(s) / 44100:5.2f}s ({len(t) / max(len(s) / 44100, 0.01):4.1f} kar/dtk) {t}')
json.dump(meta, open(os.path.join(OUT, 'lines.json'), 'w'), indent=1)
print('total', round(len(x) / 44100, 2), 's, model', g.MODEL)
