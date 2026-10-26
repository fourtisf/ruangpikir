import os, sys, json, time, numpy as np
import scipy.io.wavfile as wf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gemini_tts as g
from vo import LINES, OUT
IDX = [int(v) for v in sys.argv[1].split(',')]
rest = [LINES[k] for k in IDX]
text = '\n\n'.join(t for _, t in rest)
style = 'Ucapkan dengan santai, ramah, dan antusias seperti kreator TikTok. Beri jeda satu detik di antara setiap paragraf:'
x = None
for attempt in range(5):
    try:
        x = g.tts(text, 'Achird', style=style); break
    except SystemExit as e:
        print('retry', str(e)[:200], flush=True); time.sleep(30 + 20 * attempt)
if x is None: sys.exit('failed')
g.save(os.path.join(OUT, 'chunk_' + '_'.join(map(str, IDX)) + '.wav'), x)
if len(IDX) == 1: gaps_only = True
sr = 44100; win = 441
e = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, mode='same')); quiet = e < 0.012
gaps = []; i = 0
while i < len(quiet):
    if quiet[i]:
        j = i
        while j < len(quiet) and quiet[j]: j += 1
        if i > 0 and j < len(quiet) and (j - i) > 0.15 * sr: gaps.append(((i + j) // 2, j - i))
        i = j
    else: i += 1
chars = np.array([len(t) for _, t in rest], float); cum = np.cumsum(chars)[:-1] / chars.sum()
total = len(x); cuts = []; last = 0
for c in cum:
    target = c * total
    cands = [g_ for g_ in gaps if g_[0] > last + 0.5 * sr] or gaps
    best = min(cands, key=lambda g_: abs(g_[0] - target) / sr - 0.6 * min(g_[1] / sr, 1.0))
    cuts.append(best[0]); last = best[0]
bounds = [0] + cuts + [total]
meta = json.load(open(os.path.join(OUT, 'lines.json'))) if os.path.exists(os.path.join(OUT, 'lines.json')) else []
meta = [m for m in meta if m['i'] not in IDX]
for n, (a, b) in enumerate(zip(bounds[:-1], bounds[1:])):
    seg = x[a:b]; idx = np.where(np.abs(seg) > 0.01)[0]
    if len(idx): seg = seg[max(0, idx[0] - 441): idx[-1] + 3500]
    k = IDX[n]; p = os.path.join(OUT, f'l{k:02d}.wav'); g.save(p, seg)
    meta.append({'i': k, 'anchor': LINES[k][0], 'text': LINES[k][1], 'file': p, 'dur': round(len(seg) / 44100, 3)})
    print(f'{k:2d} {len(seg)/44100:5.2f}s (exp {len(LINES[k][1])/14:4.2f}) {LINES[k][1]}', flush=True)
meta.sort(key=lambda m: m['i'])
json.dump(meta, open(os.path.join(OUT, 'lines.json'), 'w'), indent=1)
print('total', round(total / sr, 2))
