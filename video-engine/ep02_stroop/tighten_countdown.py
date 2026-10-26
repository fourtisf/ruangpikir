"""Rapatkan jeda di suara hitung mundur (vo/l01.wav) supaya 'Siap? 3, 2, 1, mulai!' muat sebelum tes dimulai.
Menulis vo/countdown_onsets_scaled.json (waktu mulai tiap kata) yang dipakai stroop.py untuk menyinkronkan angka di layar."""
import json, numpy as np, scipy.io.wavfile as wf
sr, x = wf.read('vo/l01.wav'); x = x.astype(np.float32) / 32768
win = 441; e = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, mode='same')); loud = e > 0.02
segs = []; i = 0
while i < len(loud):
    if loud[i]:
        j = i
        while j < len(loud) and loud[j:j + 2646].any(): j += 1
        if (j - i) / sr > 0.15: segs.append((i / sr, j / sr))
        i = j
    else: i += 1
merged = []
for sg in segs:
    if merged and sg[0] - merged[-1][1] < 0.15: merged[-1] = (merged[-1][0], sg[1])
    else: merged.append(sg)
segs = merged
assert len(segs) == 5, f'butuh 5 kata (siap, tiga, dua, satu, mulai), dapat {len(segs)}: generate ulang countdown.py'
pad, gap = 0.04, 0.14
out = [np.zeros(int(0.05 * sr), np.float32)]; onsets = []
for k, (a, b) in enumerate(segs):
    if k > 0: out.append(np.zeros(int(gap * sr), np.float32))
    onsets.append(round(sum(len(o) for o in out) / sr + pad, 3))
    out.append(x[int(max(0, a - pad) * sr):int(min(len(x) / sr, b + (pad if k < 4 else 0.45)) * sr)])
y = np.concatenate(out)
wf.write('vo/l01.wav', sr, (np.clip(y, -1, 1) * 32767).astype(np.int16))
json.dump(onsets, open('vo/countdown_onsets_scaled.json', 'w'))
meta = json.load(open('vo/lines.json'))
for m in meta:
    if m['i'] == 1: m['dur'] = round(len(y) / sr, 3)
json.dump(meta, open('vo/lines.json', 'w'), indent=1)
print('onsets', onsets, 'durasi', round(len(y) / sr, 2))
