import sys, json, time, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '.')
import gemini_tts as g
ok = False
for k in range(6):
    try:
        x = g.tts('Siap? Tiga... dua... satu... mulai!', 'Achird', style='')
    except SystemExit as e:
        print('429, wait', flush=True); time.sleep(62); continue
    idx = np.where(np.abs(x) > 0.01)[0]; x = x[max(0, idx[0] - 441): idx[-1] + 3500]
    d = len(x) / 44100
    win = 441; e = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, mode='same')); loud = e > 0.02
    segs = []; i = 0
    while i < len(loud):
        if loud[i]:
            j = i
            while j < len(loud) and loud[j:j + 2646].any(): j += 1
            if (j - i) / 44100 > 0.15: segs.append((round(i / 44100, 2), round(j / 44100, 2)))
            i = j
        else: i += 1
    merged = []
    for sg in segs:
        if merged and sg[0] - merged[-1][1] < 0.15: merged[-1] = (merged[-1][0], sg[1])
        else: merged.append(sg)
    segs = merged
    print('dur', round(d, 2), segs, flush=True)
    if 2.8 < d < 5.6 and len(segs) == 5:
        g.save('vo/l01.wav', x); json.dump([s[0] for s in segs], open('vo/countdown_onsets.json', 'w')); print('saved', flush=True); ok = True; break
    time.sleep(21)
if ok:
    meta = json.load(open('vo/lines.json'))
    for m in meta:
        if m['i'] == 1: m['dur'] = round(len(wf.read('vo/l01.wav')[1]) / 44100, 3)
    json.dump(meta, open('vo/lines.json', 'w'), indent=1); print([(m['i'], m['dur']) for m in meta])
