#!/usr/bin/env python3
"""Perlambat suara tanpa mengubah nada, supaya temponya mendekati EP02 (±12 karakter/detik).
gemini-3.8-flash-tts membacakan prefix gaya, jadi suara dibuat tanpa prefix (lebih cepat, ±15 kar/dtk) lalu diperlambat di sini.
python3 slow_voice.py [tempo]   (default 0.85)  ->  vo/lNN_s.wav + lines.json menunjuk ke file itu"""
import json, os, subprocess, sys
import numpy as np
import scipy.io.wavfile as wf
HERE = os.path.dirname(os.path.abspath(__file__)); VO = os.path.join(HERE, 'vo')
TEMPO = float(sys.argv[1]) if len(sys.argv) > 1 else 0.85
filters = subprocess.run(['ffmpeg', '-hide_banner', '-filters'], capture_output=True, text=True).stdout
af = f'rubberband=tempo={TEMPO}:pitchq=quality' if ' rubberband ' in filters else f'atempo={TEMPO}'
meta = json.load(open(os.path.join(VO, 'lines.json')))
for m in meta:
    src, dst = os.path.join(VO, f"l{m['i']:02d}.wav"), os.path.join(VO, f"l{m['i']:02d}_s.wav")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', af, '-ar', '44100', '-ac', '1', dst], check=True)
    sr, x = wf.read(dst); x = x.astype(np.float32) / 32768
    idx = np.where(np.abs(x) > 0.01)[0]
    x = x[max(0, idx[0] - 441): idx[-1] + 3500].copy()
    fi, fo = min(220, len(x) // 4), min(1300, len(x) // 4)
    x[:fi] *= np.linspace(0, 1, fi); x[len(x) - fo:] *= np.linspace(1, 0, fo)
    wf.write(dst, sr, (np.clip(x, -1, 1) * 32767).astype(np.int16))
    m['file'] = os.path.relpath(dst, HERE); m['dur'] = round(len(x) / sr, 3)
    print(f"{m['i']:2d} {m['dur']:5.2f}s  {len(m['text']) / m['dur']:4.1f} kar/dtk  {m['text']}")
json.dump(meta, open(os.path.join(VO, 'lines.json'), 'w'), indent=1)
print('filter:', af)
