#!/usr/bin/env python3
"""Ruang Pikir reel #20: 'Cerita duluan, kok jadi akrab?' (saling terbuka bergantian; Sprecher, Treger, Wondra, Hilaire & Wallpe 2013, JESP)
Format seri psikologi ngobrol (EP14/EP17/EP19): dua tokoh kapsul di kafe malam dengan kotak cerita emas bergembok; satu membuka kotaknya
("aku dulu takut gelap"), gembok yang lain ikut terbuka; "kamu duluan deh"/DIEM-DIEMAN, video call 12 menit, bola cerita GANTIAN vs
SATU ARAH, hati kaca SALING SUKA, tukar peran yang nggak bisa ngejar, "aku percaya sama kamu" -> MEMBALAS, "kalau kamu?".
python3 episode.py preview t1 t2 ... | timeline out.json | video out.mp4"""
import sys, os, math, json, subprocess, random
import skia
import base as b
from base import (clamp, lerp, prog, eo, ei, eio, bo, bump, col, P, lg, rg, layer, font, XB, B, M, MONO, bl, tracked, parse,
                 pill, sparkle, person, ACC, ACC_L, ACC_XL, TXT, MUTED, CORAL, MINT, W, H, FPS)

VIOLET, YELLOW, INK, HL = '#B57BFF', '#FFD23F', '#0B0C1E', '#AEB6FF'

# adegan (waktu animasi, DUR 42); tag tidak ditampilkan
b.GROUPS = [(0.0, 3.05, 'A'), (3.05, 7.27, 'B'), (7.27, 13.25, 'C'), (13.25, 18.55, 'D'), (18.55, 21.34, 'E'),
            (21.34, 25.15, 'F'), (25.15, 30.39, 'G'), (30.39, 36.6, 'H'), (36.6, 42.0, 'J')]
PHRASES = [(0.15, 'Mau dia [terbuka] sama kamu?'), (1.42, 'Coba ini: "[cerita duluan]."'),
           (3.05, 'Kita sering [nunggu] orang lain buka diri duluan.'), (5.33, 'Akhirnya, [dua-duanya diem].'),
           (7.27, 'Tahun [2013],'), (8.8, 'psikolog [Susan Sprecher]'), (9.91, 'meneliti dua [orang asing] yang ngobrol lewat [video call].'),
           (13.25, 'Ada yang ceritanya [gantian], bolak-balik.'), (15.67, 'Ada yang [satu cerita terus],'), (17.17, 'yang lain [cuma dengerin].'),
           (18.55, 'Hasilnya?'), (19.32, 'Yang [gantian cerita],'), (20.24, '[lebih saling suka].'),
           (21.34, 'Bahkan setelah [tukar peran],'), (23.01, 'yang satu arah tetap [nggak bisa ngejar].'),
           (25.15, 'Soalnya [cerita duluan] itu kayak bilang:'), (27.45, '"[aku percaya sama kamu]."'), (28.91, 'Dan orang cenderung [membalas].'),
           (30.39, 'Mulai dari [hal kecil],'), (31.68, 'terus [tanya balik].'), (32.68, 'Cerita apa yang pernah bikin kamu [langsung akrab]?'), (34.87, 'Tulis di [komentar]!'),
           (36.6, 'Follow [Ruang Pikir],'), (37.97, 'biar makin kenal [isi kepalamu].')]
b.CAPS = [(t, s, '') for t, s in PHRASES]          # dipakai base hanya untuk jadwal

# ------------------------------------------------------------ chrome gaya sinematik
b.draw_tag = lambda cv, t: None
b.draw_progress = lambda cv, t: None
def draw_title(cv, t):
    a = eo(prog(t, 0.05, 0.35)) * (1 - eio(prog(t, 2.7, 3.05)))
    if a <= 0: return
    segs = parse("Cerita duluan, [kok jadi akrab]?"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 232) + (1 - eo(prog(t, 0.05, 0.35))) * 16 - 10 * eio(prog(t, 2.7, 3.05))
    layer(cv, a); xx = x
    for s, h in segs: cv.drawString(s, xx, y + 5, f, P(col('#000000', 0.55), blur=8)); xx += f.measureText(s)
    for s, h in segs: cv.drawString(s, x, y, f, P(col(HL if h else TXT))); x += f.measureText(s)
    cv.restore()
b.draw_title = draw_title

def _tokens(text):
    """kata + flag 'ada spasi sebelumnya' (tanda baca setelah [..] menempel tanpa spasi)"""
    out, prev_space = [], False
    for seg, h in parse(text):
        for k, w in enumerate(seg.split(' ')):
            if w: out.append((w, h, k > 0 or prev_space))
        prev_space = seg.endswith(' ')
    return out
_LAYOUT = {}
def cap_layout(text, size=56, maxw=900):
    key = (text, size)
    if key not in _LAYOUT:
        f = font(XB, size); sp = f.measureText(' ')
        lines, cur, cw = [], [], 0
        for w, h, spc in _tokens(text):
            ww = f.measureText(w); gap = sp if (cur and spc) else 0
            if cur and spc and cw + gap + ww > maxw: lines.append((cur, cw)); cur, cw, gap = [], 0, 0
            cw += gap + ww; cur.append((w, h, ww, gap))
        if cur: lines.append((cur, cw))
        _LAYOUT[key] = lines
    return _LAYOUT[key]
def draw_captions(cv, t):
    size, lh = 56, 68; f = font(XB, size)
    for i, (s, txt) in enumerate(PHRASES):
        e = PHRASES[i + 1][0] - 0.2 if i + 1 < len(PHRASES) else b.DUR - 0.3
        if t < s or t > e + 0.17: continue
        aout = 1 - prog(t, e, e + 0.16)
        lines = cap_layout(txt, size)
        y0 = 1332 - (len(lines) - 1) * lh / 2; n = 0
        for li, (words, wtot) in enumerate(lines):
            x = 540 - wtot / 2; cy = y0 + li * lh
            for w, h, ww, gap in words:
                x += gap
                p_ = prog(t, s + n * 0.035, s + n * 0.035 + 0.22); n += 1
                a = eo(p_) * aout
                if a > 0:
                    y = bl(f, cy) + (1 - eo(p_)) * 14
                    cv.drawString(w, x, y + 4, f, P(col('#000000', 0.55 * a), blur=9))
                    if h: cv.drawString(w, x, y, f, P(col(HL, 0.45 * a), blur=10))
                    cv.drawString(w, x, y, f, P(col(HL if h else TXT, a)))
                x += ww
b.draw_captions = draw_captions

def draw_bg(cv, t):
    cv.drawImage(b.bg_img(), 0, 0)
    for cx, cy, r, c, sp, ph in ((360, 700, 640, '#4B46D6', 0.17, 0.0), (760, 980, 620, '#2F3FC0', 0.14, 2.1)):
        x = cx + 120 * math.sin(t * sp + ph); y = cy + 80 * math.cos(t * sp * 0.8 + ph)
        cv.drawCircle(x, y, r, P(shader=rg(x, y, r, [col(c, 0.17), col(c, 0)])))
    # pendar kafe hangat dari atas (tanpa titik/bokeh)
    cv.drawCircle(540, 260, 900, P(shader=rg(540, 260, 900, [col('#FFC98A', 0.06), col('#B57BFF', 0.03), col('#B57BFF', 0)], [0, 0.5, 1])))
b.draw_bg = draw_bg

# crossfade antar adegan + kamera bergerak halus; ilustrasi memudar sebelum zona caption
_MASK = skia.Paint(Shader=lg(0, 200, 0, 1245, [col('#000000', 0), col('#000000', 1), col('#000000', 1), col('#000000', 0)],
                              [0, 50 / 1045, 995 / 1045, 1]), BlendMode=skia.BlendMode.kDstIn)
FADE2 = 0.45
def draw_groups(cv, t):
    n0 = cv.getSaveCount(); cv.saveLayer(None, None)
    G = b.GROUPS
    for i, (s, e, _) in enumerate(G):
        fi = FADE2 if i > 0 else 0; fo = FADE2 if i < len(G) - 1 else 0
        if t < s or t > e + fo: continue
        ain = eo(prog(t, s, s + fi)) if fi else 1.0; aout = 1 - eio(prog(t, e, e + fo)) if fo else 1.0
        a = min(ain, aout); sc = (1.06 - 0.06 * ain if fi else 1.0) * (1 + 0.025 * eio(prog(t, s, e))) * (1 + 0.04 * eio(prog(t, e, e + fo)) if fo else 1)
        cv.save(); cv.translate(540, 760); cv.scale(sc, sc); cv.translate(-540, -760)
        if a < 1: layer(cv, a)
        b.DRAWERS[i](cv, t)
        if a < 1: cv.restore()
        cv.restore()
    if cv.getSaveCount() != n0 + 1: print(f'peringatan: save/restore tidak seimbang di t={t:.2f}', file=sys.stderr); cv.restoreToCount(n0 + 1)
    cv.drawRect(skia.Rect(0, 0, W, H), _MASK); cv.restore()
b.draw_groups = draw_groups

# ------------------------------------------------------------ helper umum
def glass(cv, r, rad=34, a=1.0, glow=0.0, gc=ACC, edge=ACC, fill=('#23253C', '#121320')):
    """kartu kaca: bayangan dalam, isi gradasi, kilau atas, tepi bergradasi"""
    if a <= 0: return None
    rr = skia.RRect.MakeRectXY(r, rad, rad); pth = skia.Path(); pth.addRRect(rr)
    cv.drawRRect(skia.RRect.MakeRectXY(r.makeOffset(0, 26), rad, rad), P(col('#000000', 0.55 * a), blur=30))
    if glow > 0: cv.drawRRect(rr, P(col(gc, 0.5 * clamp(glow) * a), stroke=12, blur=24))
    cv.drawRRect(rr, P(shader=lg(0, r.top(), 0, r.bottom(), [col(fill[0], 0.95 * a), col(fill[1], 0.95 * a)])))
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    hh = r.top() + r.height() * 0.42
    cv.drawRect(skia.Rect(r.left(), r.top(), r.right(), hh), P(shader=lg(0, r.top(), 0, hh, [col('#FFFFFF', 0.08 * a), col('#FFFFFF', 0)])))
    cv.drawCircle(r.left() + r.width() * 0.18, r.top(), r.width() * 0.55, P(shader=rg(r.left() + r.width() * 0.18, r.top(), r.width() * 0.55, [col(edge, 0.14 * a), col(edge, 0)])))
    cv.restore()
    cv.drawRRect(rr, P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col(ACC_XL, 0.7 * a), col(edge, 0.4 * a), col(edge, 0.12 * a)], [0, 0.45, 1]), stroke=2.5))
    return pth

def sheen(cv, pth, r, u, a=1.0):
    """pita cahaya diagonal yang lewat di atas kartu, u 0..1"""
    if not (0 < u < 1) or pth is None: return
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    x = lerp(r.left() - 260, r.right() + 260, eio(u))
    cv.drawRect(r, P(shader=lg(x - 150, r.top(), x + 150, r.bottom(), [col('#FFFFFF', 0), col('#FFFFFF', 0.2 * a), col('#FFFFFF', 0)])))
    cv.restore()

def rays(cv, cx, cy, r, a, t, n=14, c=ACC, spin=5):
    if a <= 0: return
    cv.save(); cv.translate(cx, cy); cv.rotate(t * spin)
    p = skia.Path()
    for k in range(n):
        ang = k * math.tau / n; w = math.tau / n * 0.22
        p.moveTo(0, 0); p.lineTo(math.cos(ang - w) * r, math.sin(ang - w) * r); p.lineTo(math.cos(ang + w) * r, math.sin(ang + w) * r); p.close()
    cv.drawPath(p, P(shader=rg(0, 0, r, [col(c, 0.3 * a), col(c, 0.1 * a), col(c, 0)], [0, 0.5, 1]), blur=8))
    cv.restore()

def halo(cv, x, y, r, c=ACC, a=1.0):
    if a > 0: cv.drawCircle(x, y, r, P(shader=rg(x, y, r, [col(c, 0.32 * a), col(c, 0)])))

def glow_text(cv, s, cx, cy, f, c=TXT, a=1.0, glow=0.0, gc=ACC, shader=None):
    w = f.measureText(s); y = bl(f, cy)
    if glow > 0: cv.drawString(s, cx - w / 2, y, f, P(col(gc, 0.6 * glow * a), blur=f.getSize() * 0.22))
    cv.drawString(s, cx - w / 2, y, f, P(col(c, a), shader=shader))
    return w

def chip(cv, text, x, y, a=1.0, size=26, fg=ACC_XL, bgc='#262842', f=B, edge=ACC):
    if a <= 0: return
    ff = font(f, size); w = ff.measureText(text); h = size * 1.7
    r = skia.Rect.MakeXYWH(x - w / 2 - 22, y - h / 2, w + 44, h)
    cv.drawRoundRect(r, h / 2, h / 2, P(col(bgc, a))); cv.drawRoundRect(r, h / 2, h / 2, P(col(edge, 0.45 * a), stroke=2))
    cv.drawString(text, x - w / 2, bl(ff, y), ff, P(col(fg, a)))

def check_mark(cv, cx, cy, r, p_, a=1.0, c=MINT):
    """lingkaran + centang yang tergambar"""
    if p_ <= 0 or a <= 0: return
    s = bo(prog(p_, 0, 0.4))
    cv.save(); cv.translate(cx, cy); cv.scale(s, s)
    cv.drawCircle(0, 0, r * 1.3, P(col(c, 0.35 * a), blur=r * 0.5)); cv.drawCircle(0, 0, r, P(shader=lg(0, -r, 0, r, [col('#7CF0C6', a), col(c, a)])))
    d = prog(p_, 0.3, 1.0)
    if d > 0:
        pth = skia.Path(); pth.moveTo(-r * 0.45, 0.02 * r); pth.lineTo(-r * 0.12, r * 0.33); pth.lineTo(r * 0.48, -r * 0.3)
        m = skia.PathMeasure(pth, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(d), seg, True)
        cv.drawPath(seg, P(col(INK, a), stroke=r * 0.2))
    cv.restore()

def heart_path(cx, cy, s):
    p = skia.Path(); p.moveTo(cx, cy + s * 0.9)
    p.cubicTo(cx - s * 1.35, cy + s * 0.05, cx - s * 0.95, cy - s * 1.05, cx, cy - s * 0.38)
    p.cubicTo(cx + s * 0.95, cy - s * 1.05, cx + s * 1.35, cy + s * 0.05, cx, cy + s * 0.9); p.close()
    return p

def blink_at(t, ph):
    c = (t * 0.45 + ph) % 1.0
    return 1.0 - abs((c - 0.975) / 0.025) if c > 0.95 else 0.0

def comet(cv, pth, u, c=ACC_XL, n=9, r=14):
    m = skia.PathMeasure(pth, False); L = m.getLength()
    for k in range(n):
        d = clamp(u - k * 0.03) * L; pos = m.getPosTan(d)
        if pos is None: continue
        (px, py) = (pos[0].x(), pos[0].y()) if hasattr(pos[0], 'x') else pos[0]
        cv.drawCircle(px, py, r * (1 - k / n) + 1, P(col(c, (1 - k / n) * 0.9), blur=2 + k))

def accel_phase(t, t0, f0, f1, dur):
    """fase detak yang makin cepat: frekuensi naik f0 -> f1 selama dur detik"""
    tau = max(0.0, t - t0)
    if tau <= dur: return f0 * tau + (f1 - f0) * tau * tau / (2 * dur)
    return f0 * dur + (f1 - f0) * dur / 2 + f1 * (tau - dur)

def beat_pulse(ph):
    fr = ph % 1.0
    return max(math.exp(-fr / 0.07), 0.6 * math.exp(-max(0, fr - 0.22) / 0.07) if fr > 0.22 else 0)

def beat_times(t0, t1, f0, f1, dur):
    out, k, t = [], 1, t0
    while t < t1:
        t += 0.002
        if accel_phase(t, t0, f0, f1, dur) >= k: out.append(round(t, 3)); k += 1
    return out

def icon(cv, kind, cx, cy, r, c, a=1.0, t=0.0):
    """ikon kecil digambar sebagai bentuk (font tidak punya glyph ikon)"""
    if a <= 0: return
    cv.drawCircle(cx, cy, r, P(col(c, 0.16 * a))); cv.drawCircle(cx, cy, r, P(col(c, 0.7 * a), stroke=2.5))
    s = r * 0.55; pc = P(col(c, a), stroke=max(2.5, r * 0.1))
    if kind == 'face':
        cv.drawCircle(cx - s * 0.4, cy - s * 0.2, s * 0.12, P(col(c, a))); cv.drawCircle(cx + s * 0.4, cy - s * 0.2, s * 0.12, P(col(c, a)))
        cv.drawLine(cx - s * 0.45, cy + s * 0.35, cx + s * 0.45, cy + s * 0.35, pc)
    elif kind == 'cloud':
        for (dx, dy, rr) in ((-0.35, 0.0, 0.38), (0.1, -0.2, 0.48), (0.45, 0.05, 0.34)): cv.drawCircle(cx + dx * s, cy + dy * s, rr * s, P(col(c, a)))
        for k in range(3): cv.drawLine(cx + (-0.4 + k * 0.4) * s, cy + 0.5 * s, cx + (-0.5 + k * 0.4) * s, cy + 0.85 * s, P(col(c, a), stroke=max(2, r * 0.07)))
    elif kind == 'heart':
        hp = heart_path(cx, cy + s * 0.05, s * 0.75 * (1 + 0.18 * beat_pulse(t * 2.2))); cv.drawPath(hp, P(col(c, a)))
    elif kind == 'lock':
        cv.drawRoundRect(skia.Rect(cx - s * 0.55, cy - s * 0.1, cx + s * 0.55, cy + s * 0.7), s * 0.15, s * 0.15, P(col(c, a)))
        sh = skia.Path(); sh.addArc(skia.Rect(cx - s * 0.35, cy - s * 0.75, cx + s * 0.35, cy + s * 0.05), 180, 180); cv.drawPath(sh, pc)
    elif kind == 'reframe':
        for k in (0, 1):
            arc = skia.Path(); arc.addArc(skia.Rect(cx - s * 0.7, cy - s * 0.7, cx + s * 0.7, cy + s * 0.7), 200 + k * 180 + t * 90, 120); cv.drawPath(arc, pc)

def tear(cv, x, y, s, a=1.0):
    if a <= 0: return
    d = skia.Path(); d.moveTo(x, y - s); d.quadTo(x + s * 0.6, y + s * 0.1, x, y + s * 0.45); d.quadTo(x - s * 0.6, y + s * 0.1, x, y - s); d.close()
    cv.drawPath(d, P(col('#8FD3FF', 0.5 * a), blur=s * 0.3)); cv.drawPath(d, P(col('#BFE6FF', a)))


def bubble_path(cx, cy, w, h, tip, rad=None, maxlen=95):
    rad = h / 2 if rad is None else rad
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(r, rad, rad))
    bx = clamp(tip[0] + (cx - tip[0]) * 0.35, r.left() + rad * 0.9, r.right() - rad * 0.9)
    by = r.bottom() - 6 if tip[1] > cy else r.top() + 6
    dx, dy = tip[0] - bx, tip[1] - by; L = math.hypot(dx, dy) or 1
    if L > maxlen: tip = (bx + dx / L * maxlen, by + dy / L * maxlen)
    tail = skia.Path(); tail.moveTo(bx - 26, by); tail.quadTo(bx - 4, by, tip[0], tip[1]); tail.quadTo(bx + 6, by, bx + 26, by); tail.close()
    return skia.Op(p, tail, skia.PathOp.kUnion_PathOp), r

def draw_bubble(cv, pth, r, a=1.0, glow=0.0, fill=('#2A2C48', '#171828'), edge=ACC, gc=ACC):
    if a <= 0: return
    sh = skia.Path(pth); sh.offset(0, 18); cv.drawPath(sh, P(col('#000000', 0.5 * a), blur=22))
    if glow > 0: cv.drawPath(pth, P(col(gc, 0.55 * glow * a), stroke=14, blur=26))
    cv.drawPath(pth, P(shader=lg(0, r.top(), 0, r.bottom(), [col(fill[0], 0.97 * a), col(fill[1], 0.97 * a)])))
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(r.left(), r.top(), r.right(), r.top() + r.height() * 0.5), P(shader=lg(0, r.top(), 0, r.top() + r.height() * 0.5, [col('#FFFFFF', 0.09 * a), col('#FFFFFF', 0)])))
    cv.restore()
    cv.drawPath(pth, P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col(ACC_XL, 0.75 * a), col(edge, 0.5 * a), col(edge, 0.2 * a)], [0, 0.5, 1]), stroke=2.5))

# ------------------------------------------------------------ helper gaya sinematik
BLUE = ('#8C93FF', '#4A4FD0', '#1E2170'); RED = ('#FFB3A6', '#E0506A', '#5A1530'); GRN = ('#C7F7E4', '#2FB98A', '#0E4A3A')
def mixc(c1, c2, u):
    u = clamp(u); a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b_ = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{int(round(lerp(x, y, u))):02X}' for x, y in zip(a, b_))
def tri(u_red=0.0, u_grn=0.0):
    return tuple(mixc(mixc(x, y, u_red), z, u_grn) for x, y, z in zip(BLUE, RED, GRN))

def sphere(cv, cx, cy, r, cols, a=1.0, glow=0.6, label=None, lsize=None, lc=TXT):
    """bola 3D lembut: gradasi radial, kilau atas, cahaya tepi bawah, pendar luar"""
    if a <= 0 or r <= 1: return
    top, mid, bot = cols
    cv.drawCircle(cx, cy, r * 1.5, P(shader=rg(cx, cy, r * 1.5, [col(mid, 0.4 * glow * a), col(mid, 0)])))
    cv.drawCircle(cx, cy, r, P(shader=rg(cx - r * 0.35, cy - r * 0.45, r * 1.75, [col(top, a), col(mid, a), col(bot, a)], [0, 0.48, 1])))
    p = skia.Path(); p.addCircle(cx, cy, r)
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawCircle(cx + r * 0.3, cy + r * 0.35, r * 1.02, P(col(top, 0.22 * a), stroke=r * 0.07, blur=r * 0.06))
    cv.drawOval(skia.Rect(cx - r * 0.58, cy - r * 0.82, cx + r * 0.02, cy - r * 0.4), P(col('#FFFFFF', 0.3 * a), blur=r * 0.12))
    cv.restore()
    cv.drawCircle(cx, cy, r, P(col('#FFFFFF', 0.16 * a), stroke=max(1.5, r * 0.012)))
    if label:
        f = font(B, lsize or r * 0.26); w = f.measureText(label)
        cv.drawString(label, cx - w / 2, bl(f, cy), f, P(col(lc, a)))

def floor(cv, x0, x1, y, a=1.0, sag=0.0):
    if a <= 0: return
    p = skia.Path(); p.moveTo(x0, y); p.quadTo((x0 + x1) / 2, y + sag * 2, x1, y)
    sh = lg(x0, 0, x1, 0, [col(ACC_L, 0), col(ACC_L, 0.8 * a), col(ACC_L, 0)])
    cv.drawPath(p, P(col(ACC, 0.35 * a), stroke=10, blur=8)); cv.drawPath(p, P(shader=sh, stroke=3))
def sag_y(x0, x1, y, sag, x):
    u = (x - x0) / (x1 - x0); return y + 2 * u * (1 - u) * sag * 2

def face(cv, cx, cy, r, mood, a=1.0, t=0.0, ph=0.0):
    """wajah di atas bola: 'sad' / 'flat' / 'happy' / 'smile_closed'"""
    if a <= 0: return
    ink = P(col(INK, 0.85 * a), stroke=max(2.5, r * 0.07)); bk = blink_at(t, ph)
    for s in (-1, 1):
        ex, ey = cx + s * r * 0.33, cy - r * 0.1
        if mood == 'smile_closed':
            e = skia.Path(); e.moveTo(ex - r * 0.15, ey + r * 0.04); e.quadTo(ex, ey - r * 0.14, ex + r * 0.15, ey + r * 0.04); cv.drawPath(e, ink)
        else:
            eh = r * 0.11 * (1 - 0.9 * bk); cv.drawOval(skia.Rect(ex - r * 0.08, ey - eh, ex + r * 0.08, ey + eh), P(col(INK, 0.85 * a)))
        if mood == 'sad': cv.drawLine(ex - s * r * 0.15, ey - r * 0.26, ex + s * r * 0.1, ey - r * 0.2, ink)
    m = skia.Path(); my = cy + r * 0.32
    if mood == 'sad': m.moveTo(cx - r * 0.22, my + r * 0.06); m.quadTo(cx, my - r * 0.12, cx + r * 0.22, my + r * 0.06)
    elif mood == 'flat': m.moveTo(cx - r * 0.2, my); m.lineTo(cx + r * 0.2, my)
    else: m.moveTo(cx - r * 0.25, my - r * 0.04); m.quadTo(cx, my + r * 0.2, cx + r * 0.25, my - r * 0.04)
    cv.drawPath(m, ink)

def pill_bar(cv, x0, x1, y, h, frac, label, c, a=1.0):
    if a <= 0: return
    r = skia.Rect(x0, y - h / 2, x1, y + h / 2)
    cv.drawRoundRect(r.makeOffset(0, 10), h / 2, h / 2, P(col('#000000', 0.45 * a), blur=14))
    cv.drawRoundRect(r, h / 2, h / 2, P(shader=lg(0, r.top(), 0, r.bottom(), [col('#15162A', 0.95 * a), col('#202240', 0.95 * a)])))
    cv.drawRoundRect(r, h / 2, h / 2, P(col('#FFFFFF', 0.08 * a), stroke=2))
    fw = max(h, (x1 - x0) * frac); fr = skia.Rect(x0 + 6, y - h / 2 + 6, x0 + fw - 6, y + h / 2 - 6)
    cv.drawRoundRect(fr, (h - 12) / 2, (h - 12) / 2, P(col(c, 0.45 * a), blur=14))
    cv.drawRoundRect(fr, (h - 12) / 2, (h - 12) / 2, P(shader=lg(fr.left(), 0, fr.right(), 0, [col(mixc(c, '#FFFFFF', 0.35), a), col(c, a)])))
    f = font(B, 30); cv.drawString(label, x0 + 30, bl(f, y), f, P(col(TXT if frac > 0.3 else ACC_XL, a)))

def head_outline(cv, cx, cy, s, a=1.0, fill=0.35):
    """siluet kepala + bahu dari logo (garis tipis bercahaya), kotak logo 1000 px"""
    if a <= 0: return
    hp = __import__('logo').head_path()
    sh = skia.Path(); sh.moveTo(372, 905); sh.cubicTo(330, 960, 210, 990, 140, 1090); sh.moveTo(670, 905); sh.cubicTo(720, 960, 850, 990, 930, 1090)
    cv.save(); cv.translate(cx - 569 * s, cy - 571 * s); cv.scale(s, s)
    cv.drawPath(hp, P(shader=rg(560, 560, 420, [col('#2A2F66', fill * a), col('#2A2F66', 0)])))
    for p in (hp, sh):
        cv.drawPath(p, P(col(ACC, 0.45 * a), stroke=12 / s, blur=10 / s)); cv.drawPath(p, P(col(ACC_XL, 0.95 * a), stroke=3 / s))
    cv.restore()

def eye(cv, cx, cy, s, a=1.0, t=0.0, look=(0.0, -0.4)):
    if a <= 0: return
    bk = blink_at(t, 0.15); hh = s * 0.55 * (1 - 0.92 * bk)
    e = skia.Path(); e.moveTo(cx - s, cy); e.quadTo(cx, cy - hh * 2, cx + s, cy); e.quadTo(cx, cy + hh * 2, cx - s, cy); e.close()
    cv.drawPath(e, P(col(ACC, 0.5 * a), blur=18)); cv.drawPath(e, P(shader=lg(0, cy - s, 0, cy + s, [col('#E9EBFF', a), col('#B9BFFF', a)])))
    if bk < 0.6:
        cv.save(); cv.clipPath(e, skia.ClipOp.kIntersect, True)
        ix, iy = cx + look[0] * s * 0.25, cy + look[1] * s * 0.3
        cv.drawCircle(ix, iy, s * 0.42, P(shader=rg(ix, iy, s * 0.42, [col(ACC_L, a), col('#3A3FBF', a)])))
        cv.drawCircle(ix, iy, s * 0.2, P(col(INK, a))); cv.drawCircle(ix - s * 0.12, iy - s * 0.12, s * 0.07, P(col('#FFFFFF', a)))
        cv.restore()
    cv.drawPath(e, P(col(ACC_XL, 0.8 * a), stroke=3))

def thought_chip(cv, text, cx, cy, a, c, fill, size=36, strike=0.0, sc=1.0):
    if a <= 0: return
    f = font(XB, size); w = f.measureText(text); h = size * 1.9
    cv.save(); cv.translate(cx, cy); cv.scale(sc, sc)
    r = skia.Rect(-w / 2 - 34, -h / 2, w / 2 + 34, h / 2)
    cv.drawRoundRect(r.makeOffset(0, 12), h / 2, h / 2, P(col('#000000', 0.5 * a), blur=16))
    cv.drawRoundRect(r, h / 2, h / 2, P(col(c, 0.4 * a), stroke=10, blur=14))
    cv.drawRoundRect(r, h / 2, h / 2, P(shader=lg(0, -h / 2, 0, h / 2, [col(fill[0], a), col(fill[1], a)])))
    cv.drawRoundRect(r, h / 2, h / 2, P(col(c, 0.8 * a), stroke=2.5))
    cv.drawString(text, -w / 2, bl(f, 0), f, P(col(TXT, a)))
    if strike > 0: cv.drawLine(-w / 2 - 10, 0, -w / 2 - 10 + (w + 20) * eo(strike), 0, P(col(CORAL, a), stroke=6))
    cv.restore()



# ------------------------------------------------------------ helper EP06: garis neon yang menggambar diri + tipografi kinetik
def partial(path, frac):
    """potongan awal path (semua kontur) sepanjang frac dari total panjangnya"""
    if frac >= 1: return path
    out = skia.Path()
    if frac <= 0: return out
    m = skia.PathMeasure(path, False); lens = []
    while True:
        lens.append(m.getLength())
        if not m.nextContour(): break
    target = sum(lens) * frac; acc = 0; m = skia.PathMeasure(path, False)
    for L in lens:
        if acc < target:
            seg = skia.Path(); m.getSegment(0, min(L, target - acc), seg, True); out.addPath(seg)   # getSegment menimpa dst, jadi pakai path sementara
        acc += L; m.nextContour()
    return out

def neon(cv, path, frac=1.0, c=ACC_XL, w=4, a=1.0, glow=1.0, gc=ACC):
    if a <= 0 or frac <= 0: return
    p = partial(path, frac)
    if glow > 0: cv.drawPath(p, P(col(gc, 0.45 * glow * a), stroke=w * 3.5, blur=w * 2.2))
    cv.drawPath(p, P(col(c, a), stroke=w))

_HEAD = None
def head_line(cx, cy, s, facing=1):
    """siluet kepala profil (dari logo) sebagai path; facing=1 menghadap kanan, -1 kiri"""
    global _HEAD
    if _HEAD is None: _HEAD = __import__('logo').head_path()
    m = skia.Matrix(); m.setTranslate(-569, -571); m.postScale(s * facing, s); m.postTranslate(cx, cy)
    p = skia.Path(_HEAD); p.transform(m); return p

def slam(cv, text, cx, cy, size, t, t0, c1=TXT, c2=HL, gc=ACC, t_out=None, shake=0.0, rings=True):
    """kata raksasa yang menghantam layar (skala 1.7 -> 1, cahaya, cincin benturan, goyang)"""
    p = prog(t, t0, t0 + 0.26)
    if p <= 0: return
    a = clamp(p * 3) * ((1 - eio(prog(t, t_out, t_out + 0.25))) if t_out else 1)
    if a <= 0: return
    if rings:
        for k in range(2):
            rp = prog(t, t0 + 0.22 + k * 0.1, t0 + 0.9 + k * 0.1)
            if 0 < rp < 1:
                rr = skia.Rect(cx - 260 - 260 * rp, cy - 70 - 120 * rp, cx + 260 + 260 * rp, cy + 70 + 120 * rp)
                cv.drawRoundRect(rr, 120, 120, P(col(gc, 0.6 * (1 - rp) * a), stroke=3))
    s = lerp(1.7, 1.0, eo(p)); sh = shake * math.sin(t * 63) * (1 - prog(t, t0 + 0.3, t0 + 0.9))
    cv.save(); cv.translate(cx + sh, cy); cv.scale(s, s)
    f = font(XB, size); w = f.measureText(text); y = bl(f, 0)
    cv.drawString(text, -w / 2, y + 8, f, P(col('#000000', 0.5 * a), blur=14))
    cv.drawString(text, -w / 2, y, f, P(col(gc, 0.6 * a), blur=size * 0.18))
    cv.drawString(text, -w / 2, y, f, P(shader=lg(0, -size * 0.5, 0, size * 0.5, [col(c1, a), col(c2, a)])))
    cv.restore()

def text_path(text, cx, cy, size):
    """path garis tepi huruf (dari glyph font), rata tengah di (cx, cy)"""
    f = font(XB, size); g = f.textToGlyphs(text); xs = f.getXPos(g); w = f.measureText(text); y = bl(f, cy)
    out = skia.Path()
    for gid, x in zip(g, xs):
        gp = f.getPath(gid)
        if gp is None: continue
        m = skia.Matrix(); m.setTranslate(cx - w / 2 + x, y); gp = skia.Path(gp); gp.transform(m); out.addPath(gp)
    return out

def outline_text(cv, text, cx, cy, size, frac, fill, a=1.0, c=ACC_XL, gc=ACC, shader=None):
    """teks yang tergambar sebagai garis neon (frac) lalu terisi (fill 0..1)"""
    if a <= 0: return
    pth = text_path(text, cx, cy, size)
    neon(cv, pth, frac, c, 3, a, 0.8, gc)
    if fill > 0: cv.drawPath(pth, P(col(c, fill * a), shader=shader))

def waves(cv, x0, x1, y, t, a=1.0, c=ACC_L, amp=26, k=3, speed=6):
    if a <= 0: return
    for j in range(k):
        p = skia.Path(); ph = t * speed + j * 1.1; A = amp * (1 - j * 0.28)
        for i in range(61):
            u = i / 60; x = lerp(x0, x1, u); env = math.sin(math.pi * u)
            yy = y + math.sin(u * 14 + ph) * A * env
            (p.moveTo if i == 0 else p.lineTo)(x, yy)
        cv.drawPath(p, P(col(c, (0.75 - j * 0.2) * a), stroke=3.5 - j))

def loop_arrow(cv, cx, cy, r, t, a=1.0, c=CORAL, spin=220, sweep=300, w=6):
    if a <= 0: return
    cv.save(); cv.translate(cx, cy); cv.rotate(t * spin)
    p = skia.Path(); p.addArc(skia.Rect(-r, -r, r, r), 0, sweep)
    cv.drawPath(p, P(col(c, 0.45 * a), stroke=w * 3, blur=w)); cv.drawPath(p, P(col(c, a), stroke=w))
    ang = math.radians(sweep); ex, ey = r * math.cos(ang), r * math.sin(ang)
    hd = skia.Path(); hd.moveTo(ex + 18 * math.cos(ang - 1.2), ey + 18 * math.sin(ang - 1.2)); hd.lineTo(ex, ey); hd.lineTo(ex + 18 * math.cos(ang + 2.6), ey + 18 * math.sin(ang + 2.6))
    cv.drawPath(hd, P(col(c, a), stroke=w)); cv.restore()

def heart_line(cx, cy, s):
    p = skia.Path(); p.moveTo(cx, cy + s * 0.9)
    p.cubicTo(cx - s * 1.35, cy + s * 0.05, cx - s * 0.95, cy - s * 1.05, cx, cy - s * 0.38)
    p.cubicTo(cx + s * 0.95, cy - s * 1.05, cx + s * 1.35, cy + s * 0.05, cx, cy + s * 0.9)
    return p

def thought_bubble_line(cx, cy, w, h, tail):
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h / 2, h / 2))
    for k, (u, r) in enumerate(((0.35, 12), (0.7, 8))):
        x = lerp(cx - w * 0.15, tail[0], u); y = lerp(cy + h / 2, tail[1], u); p.addCircle(x, y, r)
    return p

def two_heads(cv, t, t0, a=1.0, s=0.4, y=700, xl=300, xr=780, cl=ACC_XL, cr=ACC_XL, slide=0.0):
    d = eo(prog(t, t0, t0 + 0.6))
    pl = head_line(xl - slide, y, s, 1); pr = head_line(xr + slide, y, s, -1)
    neon(cv, pl, d, cl, 4, a); neon(cv, pr, d, cr, 4, a)
    return d

# ------------------------------------------------------------ helper EP07: HUD / alat ukur
AMBER, FIRE = '#FFC56B', '#FF8A4C'
def vcol(v):
    """warna nilai: -1 nggak (coral) .. 0 ungu .. 1 suka (mint)"""
    return mixc(ACC, MINT, v) if v >= 0 else mixc(ACC, CORAL, -v)

def mono(cv, s, cx, cy, size, c=ACC_L, a=1.0, sp=0.0, align=0.5, glow=0.0):
    """teks mono gaya HUD; align 0 = kiri, 0.5 = tengah, 1 = kanan"""
    if a <= 0: return 0
    f = font(MONO, size); w = sum(f.measureText(ch) for ch in s) + sp * (len(s) - 1); x0 = cx - w * align; y = bl(f, cy)
    for pnt in ([P(col(c, 0.55 * glow * a), blur=size * 0.25)] if glow > 0 else []) + [P(col(c, a))]:
        if not sp: cv.drawString(s, x0, y, f, pnt); continue
        x = x0
        for ch in s: cv.drawString(ch, x, y, f, pnt); x += f.measureText(ch) + sp
    return w

def _sweep(a):
    st = [(0, 0.75), (30, 1.0), (150, -1.0), (210, -0.5), (270, 0.0), (330, 0.5), (360, 0.75)]
    return skia.GradientShader.MakeSweep(0, 0, [col(vcol(v), a) for _, v in st], [d / 360 for d, _ in st])

def gauge(cv, cx, cy, r, v, a=1.0, t=0.0, boot=1.0, alarm=0.0, label='SOCIOMETER', read='DITERIMA', ends=True, pct=None, pc=None):
    """alat ukur HUD: busur 240 derajat (kiri bawah NGGAK, kanan bawah SUKA), jarum di nilai v (-1..1)"""
    if a <= 0: return
    vc = mixc(vcol(clamp(v, -1, 1)), CORAL, alarm)
    halo(cv, cx, cy, r * 1.5, vc, 0.65 * a * boot)
    cv.save(); cv.translate(cx, cy)
    cv.save(); cv.rotate(t * 16); p = skia.Path()
    for k in range(6): p.addArc(skia.Rect(-r * 1.16, -r * 1.16, r * 1.16, r * 1.16), k * 60, 40 * boot)
    cv.drawPath(p, P(col(ACC_L, 0.4 * a), stroke=2)); cv.restore()
    cv.save(); cv.rotate(-t * 7); p = skia.Path()
    for k in range(36): p.addArc(skia.Rect(-r * 1.25, -r * 1.25, r * 1.25, r * 1.25), k * 10, 2.2 * boot)
    cv.drawPath(p, P(col(ACC_L, 0.22 * a), stroke=7)); cv.restore()
    cv.drawCircle(0, 0, r * 1.04, P(shader=rg(0, -r * 0.3, r * 1.3, [col('#20223A', 0.88 * a), col('#0C0D18', 0.88 * a)])))
    cv.drawCircle(0, 0, r * 1.04, P(col(ACC_L, 0.2 * a), stroke=2))
    arc = skia.Path(); arc.addArc(skia.Rect(-r * 0.92, -r * 0.92, r * 0.92, r * 0.92), 150, max(0.1, 240 * boot))
    cv.drawPath(arc, P(shader=_sweep(0.55 * a), stroke=r * 0.11, blur=r * 0.06))
    cv.drawPath(arc, P(shader=_sweep(a), stroke=r * 0.05))
    tk = skia.Path()
    for k in range(41):
        if k / 40 > boot: break
        ang = math.radians(150 + k * 6); r0 = r * (0.70 if k % 5 == 0 else 0.76); r1 = r * 0.82
        tk.moveTo(math.cos(ang) * r0, math.sin(ang) * r0); tk.lineTo(math.cos(ang) * r1, math.sin(ang) * r1)
    cv.drawPath(tk, P(shader=_sweep(a), stroke=max(2, r * 0.012)))
    if alarm > 0:
        fl = alarm * (0.55 + 0.45 * math.sin(t * 34))
        cv.drawCircle(0, 0, r * 1.04, P(col(CORAL, 0.85 * fl), stroke=5, blur=6))
        cv.drawPath(arc, P(col(CORAL, 0.45 * fl), stroke=r * 0.15, blur=r * 0.08))
    if label: mono(cv, label, 0, -r * 0.4, max(18, r * 0.075), ACC_L, 0.75 * a * boot, sp=r * 0.02)
    if ends:
        for s_, txt, c in ((-1, 'NGGAK', CORAL), (1, 'SUKA', MINT)):
            ang = math.radians(270 + s_ * 120)
            mono(cv, txt, math.cos(ang) * r * 0.86, math.sin(ang) * r * 0.86 + r * 0.2, max(18, r * 0.085), c, a * boot)
    th = math.radians(270 + clamp(v, -1.1, 1.1) * 120); ux, uy = math.cos(th), math.sin(th); px, py = -uy, ux
    L, wb, tl = r * 0.8, r * 0.045, r * 0.14
    nd = skia.Path(); nd.moveTo(ux * L, uy * L); nd.lineTo(px * wb - ux * tl, py * wb - uy * tl); nd.lineTo(-px * wb - ux * tl, -py * wb - uy * tl); nd.close()
    cv.drawPath(nd, P(col(vc, 0.75 * a * boot), blur=r * 0.05))
    cv.drawPath(nd, P(shader=lg(0, 0, ux * L, uy * L, [col('#FFFFFF', a * boot), col(mixc(vc, '#FFFFFF', 0.3), a * boot)])))
    cv.drawCircle(0, 0, r * 0.085, P(shader=rg(-r * 0.02, -r * 0.03, r * 0.1, [col('#3A3D66', a), col('#14152A', a)])))
    cv.drawCircle(0, 0, r * 0.085, P(col(vc, a), stroke=3))
    if read:
        mono(cv, read, 0, r * 0.36, max(18, r * 0.07), ACC_L, 0.7 * a * boot, sp=r * 0.012)
        val = pct if pct is not None else f'{int(round(50 + 50 * clamp(v, -1, 1)))}%'
        mono(cv, val, 0, r * 0.57, max(34, r * 0.19), pc or vc, a * boot, glow=0.6)
    cv.restore()

def brackets(cv, r, a=1.0, c=ACC_L, L=40, w=3, pad=0):
    """sudut bingkai HUD"""
    if a <= 0: return
    l, tp, rt, bt = r.left() - pad, r.top() - pad, r.right() + pad, r.bottom() + pad
    p = skia.Path()
    for x, y, dx, dy in ((l, tp, 1, 1), (rt, tp, -1, 1), (l, bt, 1, -1), (rt, bt, -1, -1)):
        p.moveTo(x + dx * L, y); p.lineTo(x, y); p.lineTo(x, y + dy * L)
    cv.drawPath(p, P(col(c, 0.4 * a), stroke=w * 3, blur=w * 2)); cv.drawPath(p, P(col(c, a), stroke=w))

def scanline(cv, x0, x1, y, a=1.0, c=ACC_L):
    if a <= 0: return
    cv.drawRect(skia.Rect(x0, y - 60, x1, y), P(shader=lg(0, y - 60, 0, y, [col(c, 0), col(c, 0.16 * a)])))
    sh = lg(x0, 0, x1, 0, [col(c, 0), col(c, a), col(c, 0)])
    cv.drawLine(x0, y, x1, y, P(col(c, 0.5 * a), stroke=8, blur=6)); cv.drawLine(x0, y, x1, y, P(shader=sh, stroke=2.5))

def warn_tri(cv, cx, cy, s, a=1.0, c=CORAL):
    if a <= 0: return
    p = skia.Path(); p.moveTo(cx, cy - s); p.lineTo(cx + s * 1.12, cy + s * 0.85); p.lineTo(cx - s * 1.12, cy + s * 0.85); p.close()
    cv.drawPath(p, P(col(c, 0.55 * a), stroke=s * 0.22, blur=s * 0.22)); cv.drawPath(p, P(col(c, 0.2 * a)))
    cv.drawPath(p, P(col(c, a), stroke=s * 0.11))
    glow_text(cv, '!', cx, cy + s * 0.2, font(XB, s * 1.05), c, a)

def comment(cv, text, cx, cy, a=1.0, sc=1.0, size=34, av=CORAL, rot=0.0, glow=0.0):
    """kartu komentar: avatar + nama (garis abu) + teks"""
    if a <= 0 or sc <= 0: return
    f = font(B, size); tw = f.measureText(text); h = size * 2.7; w = tw + size * 3.4
    cv.save(); cv.translate(cx, cy); cv.rotate(rot); cv.scale(sc, sc)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    glass(cv, r, rad=h * 0.3, a=a, glow=glow, gc=av)
    ax, ar = -w / 2 + size * 1.3, size * 0.66
    cv.drawCircle(ax, 0, ar, P(shader=lg(0, -ar, 0, ar, [col(mixc(av, '#FFFFFF', 0.35), a), col(av, a)])))
    cv.save(); pc = skia.Path(); pc.addCircle(ax, 0, ar); cv.clipPath(pc, skia.ClipOp.kIntersect, True)
    cv.drawCircle(ax, -ar * 0.2, ar * 0.32, P(col('#FFFFFF', 0.85 * a))); cv.drawOval(skia.Rect(ax - ar * 0.6, ar * 0.25, ax + ar * 0.6, ar * 1.3), P(col('#FFFFFF', 0.85 * a)))
    cv.restore()
    tx = -w / 2 + size * 2.35
    cv.drawRoundRect(skia.Rect(tx, -h * 0.29, tx + size * 2.4, -h * 0.29 + size * 0.3), 6, 6, P(col(MUTED, 0.7 * a)))
    cv.drawString(text, tx, bl(f, h * 0.12), f, P(col(TXT, a)))
    cv.restore()

def mini_person(cv, cx, cy, s, c=ACC_L, a=1.0, lit=1.0):
    """ikon orang (kepala + bahu) gaya HUD; lit 1 menyala, 0 redup"""
    if a <= 0: return
    p = skia.Path(); p.addCircle(cx, cy - s * 0.42, s * 0.3)
    bp = skia.Path(); bp.addArc(skia.Rect(cx - s * 0.62, cy - s * 0.02, cx + s * 0.62, cy + s * 1.2), 180, 180); bp.close(); p.addPath(bp)
    if lit > 0: cv.drawPath(p, P(col(c, 0.5 * lit * a), blur=s * 0.25))
    cv.drawPath(p, P(col(c, (0.1 + 0.3 * lit) * a)))
    cv.drawPath(p, P(col(c, (0.4 + 0.6 * lit) * a), stroke=3))

def cross(cv, cx, cy, s, a=1.0, c=CORAL, w=None, d=1.0):
    if a <= 0: return
    w = w or s * 0.25
    for k, (x0, y0, x1, y1) in enumerate(((-1, -1, 1, 1), (1, -1, -1, 1))):
        u = clamp(d * 2 - k)
        if u <= 0: continue
        ex, ey = lerp(x0, x1, eo(u)), lerp(y0, y1, eo(u))
        cv.drawLine(cx + x0 * s, cy + y0 * s, cx + ex * s, cy + ey * s, P(col(c, 0.5 * a), stroke=w * 2, blur=w))
        cv.drawLine(cx + x0 * s, cy + y0 * s, cx + ex * s, cy + ey * s, P(col(c, a), stroke=w))

def clock24(cv, cx, cy, r, hour, a=1.0, h0=8.0):
    """jam 24 jam: jejak waktu yang sudah lewat berwarna coral"""
    if a <= 0: return
    halo(cv, cx, cy, r * 1.4, ACC, 0.5 * a)
    cv.drawCircle(cx, cy, r, P(shader=rg(cx, cy - r * 0.3, r * 1.3, [col('#20223A', 0.88 * a), col('#0C0D18', 0.88 * a)])))
    cv.drawCircle(cx, cy, r, P(col(ACC_L, 0.35 * a), stroke=2.5))
    tk = skia.Path()
    for k in range(48):
        ang = math.radians(-90 + k * 7.5); r0 = r * (0.83 if k % 12 == 0 else 0.89 if k % 2 == 0 else 0.93)
        tk.moveTo(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0); tk.lineTo(cx + math.cos(ang) * r * 0.97, cy + math.sin(ang) * r * 0.97)
    cv.drawPath(tk, P(col(ACC_L, 0.6 * a), stroke=2.5))
    for hh in (0, 6, 12, 18):
        ang = math.radians(-90 + hh * 15); mono(cv, f'{hh:02d}', cx + math.cos(ang) * r * 0.68, cy + math.sin(ang) * r * 0.68, r * 0.1, ACC_L, 0.7 * a)
    sw = (hour - h0) * 15
    if sw > 0.5:
        tr = skia.Path(); tr.addArc(skia.Rect(cx - r * 0.97, cy - r * 0.97, cx + r * 0.97, cy + r * 0.97), -90 + h0 * 15, min(sw, 359.9))
        cv.drawPath(tr, P(col(CORAL, 0.4 * a), stroke=r * 0.12, blur=r * 0.05)); cv.drawPath(tr, P(col(CORAL, 0.85 * a), stroke=r * 0.035))
    ang = math.radians(-90 + hour * 15)
    cv.drawLine(cx, cy, cx + math.cos(ang) * r * 0.78, cy + math.sin(ang) * r * 0.78, P(col(ACC, 0.6 * a), stroke=14, blur=8))
    cv.drawLine(cx, cy, cx + math.cos(ang) * r * 0.78, cy + math.sin(ang) * r * 0.78, P(col(ACC_XL, a), stroke=6))
    cv.drawCircle(cx, cy, r * 0.06, P(col(ACC_XL, a)))
    hh = int(hour) % 24; mm = int((hour % 1) * 60)
    mono(cv, f'{hh:02d}.{mm:02d}', cx, cy - r * 0.3, r * 0.15, TXT, a, glow=0.4)

def flame(cv, cx, cy, s, t, a=1.0):
    if a <= 0: return
    halo(cv, cx, cy - s * 0.6, s * 6, FIRE, 0.8 * a)
    for dx in (-1, 1): cv.drawLine(cx - dx * s * 0.95, cy + s * 0.22, cx + dx * s * 0.95, cy - s * 0.04, P(col('#6B4636', a), stroke=s * 0.22))
    for k, (sc, c1, c2) in enumerate(((1.0, '#FF6B3D', '#FFB15C'), (0.66, '#FFB15C', '#FFE08A'), (0.36, '#FFF3C8', '#FFFFFF'))):
        fl = 1 + 0.1 * math.sin(t * 13 + k * 1.7) + 0.06 * math.sin(t * 23 + k)
        hg = s * 1.9 * sc * fl; w = s * 0.75 * sc; sw = s * 0.16 * math.sin(t * 8 + k * 0.9)
        p = skia.Path(); p.moveTo(cx + sw, cy - hg)
        p.cubicTo(cx + w * 1.25, cy - hg * 0.4, cx + w, cy + s * 0.05, cx, cy + s * 0.05)
        p.cubicTo(cx - w, cy + s * 0.05, cx - w * 1.25, cy - hg * 0.4, cx + sw, cy - hg); p.close()
        if k == 0: cv.drawPath(p, P(col(FIRE, 0.6 * a), blur=s * 0.35))
        cv.drawPath(p, P(shader=lg(0, cy - hg, 0, cy, [col(c2, a), col(c1, a)])))

def stamp(cv, text, cx, cy, size, t, t0, c=CORAL, rot=-9, a=1.0):
    """stempel yang dihantamkan (skala 1.8 -> 1, cincin benturan)"""
    p = prog(t, t0, t0 + 0.22)
    if p <= 0 or a <= 0: return
    a *= clamp(p * 3); s = lerp(1.8, 1.0, eo(p)); f = font(XB, size); w = f.measureText(text); h = size * 1.3
    rp = prog(t, t0 + 0.2, t0 + 0.8)
    if 0 < rp < 1:
        rr = skia.Rect(cx - w / 2 - 60 - 160 * rp, cy - h / 2 - 20 - 90 * rp, cx + w / 2 + 60 + 160 * rp, cy + h / 2 + 20 + 90 * rp)
        cv.drawRoundRect(rr, 40, 40, P(col(c, 0.6 * (1 - rp) * a), stroke=3))
    cv.save(); cv.translate(cx, cy); cv.rotate(rot); cv.scale(s, s)
    r = skia.Rect(-w / 2 - size * 0.35, -h / 2, w / 2 + size * 0.35, h / 2)
    cv.drawRoundRect(r, 20, 20, P(col(c, 0.5 * a), stroke=16, blur=18)); cv.drawRoundRect(r, 20, 20, P(col('#1C0F16', 0.82 * a)))
    cv.drawRoundRect(r, 20, 20, P(col(c, a), stroke=8)); cv.drawRoundRect(r.makeInset(14, 14), 10, 10, P(col(c, 0.7 * a), stroke=3))
    cv.drawString(text, -w / 2, bl(f, 0), f, P(col(c, 0.6 * a), blur=size * 0.12)); cv.drawString(text, -w / 2, bl(f, 0), f, P(col(mixc(c, '#FFFFFF', 0.25), a)))
    cv.restore()

def tile(cv, ch, cx, cy, s, a=1.0, bad=0.0):
    if a <= 0: return
    r = skia.Rect(cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2)
    glass(cv, r, rad=s * 0.2, a=a, glow=bad, gc=CORAL, edge=mixc(ACC, CORAL, bad))
    glow_text(cv, ch, cx, cy, font(XB, s * 0.55), mixc(TXT, CORAL, bad), a)

def file_card(cv, t, t0, year, names, journal, a=1.0, y0=420):
    """kartu arsip riset gaya HUD: tahun tergambar sebagai garis lalu terisi"""
    pa = eo(prog(t, t0, t0 + 0.45)); a *= pa
    if a <= 0: return
    dy = (1 - pa) * 40; r = skia.Rect(130, y0 + dy, 950, y0 + 520 + dy)
    pth = glass(cv, r, rad=30, a=a, glow=0.3)
    brackets(cv, r, a, ACC_L, 46, 3, pad=18)
    mono(cv, 'ARSIP RISET', r.left() + 56, r.top() + 64, 26, ACC_L, 0.85 * a, sp=4, align=0)
    mono(cv, 'TERVERIFIKASI', r.right() - 56, r.top() + 64, 22, MINT, 0.8 * a * eo(prog(t, t0 + 1.2, t0 + 1.5)), sp=2, align=1)
    cv.drawLine(r.left() + 56, r.top() + 108, r.right() - 56, r.top() + 108, P(col(ACC_L, 0.25 * a), stroke=2))
    outline_text(cv, year, 540, r.top() + 245, 190, eo(prog(t, t0 + 0.15, t0 + 1.0)), eo(prog(t, t0 + 0.8, t0 + 1.3)), a,
                 shader=lg(0, r.top() + 170, 0, r.top() + 320, [col('#FFFFFF', a), col(HL, a)]))
    na = eo(prog(t, t0 + 0.5, t0 + 0.9))
    if na > 0:
        f = font(XB, 46); w = f.measureText(names); cv.drawString(names, 540 - w / 2, bl(f, r.top() + 400) + (1 - na) * 12, f, P(col(TXT, na * a)))
        f = font(M, 29); w = f.measureText(journal); cv.drawString(journal, 540 - w / 2, bl(f, r.top() + 458), f, P(col(ACC_L, 0.85 * na * a)))
    sp = prog(t, t0 + 0.1, t0 + 1.1)
    if 0 < sp < 1:
        cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True); scanline(cv, r.left(), r.right(), lerp(r.top(), r.bottom() + 60, sp), a); cv.restore()
    sheen(cv, pth, r, prog(t, t0 + 1.3, t0 + 2.1), a)

def shake(t, t0, amp, dur=0.5):
    return amp * math.sin(t * 61) * (1 - prog(t, t0, t0 + dur)) if t >= t0 else 0.0

# ------------------------------------------------------------ helper EP07 v2: dunia 3D + UI medsos
F3 = 1500.0
def P3(sx, sy, z):
    """titik (sx, sy) di bidang layar z=0, didorong sejauh z -> posisi layar + skala (perspektif ke pusat 540, 760)"""
    s = F3 / max(60.0, F3 + z); return 540 + (sx - 540) * s, 760 + (sy - 760) * s, s

def plane_m(sx, sy, z, w, h, ry=0.0, rx=0.0, rz=0.0):
    """matrix yang memetakan kotak lokal (-w/2,-h/2)-(w/2,h/2) ke bidang 3D berpusat di (sx, sy, z), rotasi derajat"""
    cyy, syy = math.cos(math.radians(ry)), math.sin(math.radians(ry))
    cxx, sxx = math.cos(math.radians(rx)), math.sin(math.radians(rx))
    czz, szz = math.cos(math.radians(rz)), math.sin(math.radians(rz))
    src, dst = [], []
    for u, v in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        u2, v2 = u * czz - v * szz, u * szz + v * czz
        yy, zz = v2 * cxx, v2 * sxx
        xx, zz2 = u2 * cyy + zz * syy, -u2 * syy + zz * cyy
        if F3 + z + zz2 < 80: return None
        X, Y, _ = P3(sx + xx, sy + yy, z + zz2); src.append(skia.Point(u, v)); dst.append(skia.Point(X, Y))
    m = skia.Matrix()
    return m if m.setPolyToPoly(src, dst) else None

class plane:
    """with plane(cv, sx, sy, z, w, h, ry, rx) as ok: gambar di koordinat lokal (pusat 0,0)"""
    def __init__(self, cv, *a, **k): self.cv, self.m = cv, plane_m(*a, **k)
    def __enter__(self):
        if self.m is None: return False
        self.cv.save(); self.cv.concat(self.m); return True
    def __exit__(self, *e):
        if self.m is not None: self.cv.restore()
        return False

def facing(ry, rx=0.0): return math.cos(math.radians(ry)) * math.cos(math.radians(rx))

def RR(r, rad): return skia.RRect.MakeRectXY(r, rad, rad)

def extrude(cv, text, cx, cy, size, a=1.0, depth=12, front=('#FFFFFF', HL), side='#2E3270', glow=ACC, dx=0.5, dy=0.9):
    """teks 3D: lapisan samping bertumpuk + muka bergradasi + pendar"""
    if a <= 0: return 0
    f = font(XB, size); w = f.measureText(text); x = cx - w / 2; y = bl(f, cy); st = size / 120
    cv.drawString(text, x + dx * depth * st, y + (dy * depth + 14) * st, f, P(col('#000000', 0.55 * a), blur=size * 0.1))
    for k in range(depth, 0, -1):
        cv.drawString(text, x + dx * k * st, y + dy * k * st, f, P(col(mixc(side, '#05060F', 0.55 * k / depth), a)))
    cv.drawString(text, x, y, f, P(col(glow, 0.55 * a), blur=size * 0.14))
    cv.drawString(text, x, y, f, P(shader=lg(0, y - size * 0.75, 0, y + size * 0.05, [col(front[0], a), col(front[1], a)])))
    return w

def notif(cv, x, y, w, text, a=1.0, title='Komentar baru', glow=0.0):
    """banner notifikasi gaya ponsel (koordinat lokal, pusat x,y)"""
    if a <= 0: return
    h = w * 0.3; r = skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    glass(cv, r, rad=h * 0.28, a=a, glow=glow, gc=CORAL, fill=('#2B2D47', '#191A2C'))
    ic = h * 0.52; ix, iy = r.left() + h * 0.18, y - ic / 2
    icr = skia.Rect(ix, iy, ix + ic, iy + ic)
    cv.drawRoundRect(icr, ic * 0.26, ic * 0.26, P(shader=lg(ix, iy, ix + ic, iy + ic, [col('#FF8A7A', a), col('#B57BFF', a)])))
    bp, _ = bubble_path(ix + ic / 2, iy + ic * 0.46, ic * 0.56, ic * 0.4, (ix + ic * 0.32, iy + ic * 0.8), maxlen=ic * 0.2)
    cv.drawPath(bp, P(col('#FFFFFF', 0.95 * a)))
    tx = ix + ic + h * 0.16; f1 = font(B, h * 0.2); f2 = font(XB, h * 0.25); f3 = font(M, h * 0.17)
    cv.drawString(title, tx, bl(f1, y - h * 0.17), f1, P(col(ACC_L, 0.9 * a)))
    tw = f3.measureText('baru saja'); cv.drawString('baru saja', r.right() - h * 0.2 - tw, bl(f3, y - h * 0.17), f3, P(col(MUTED, a)))
    cv.drawString(text, tx, bl(f2, y + h * 0.16), f2, P(col(TXT, a)))

def phone(cv, w, h, a, t, banner=0.0, btext='kamu kok gitu sih?', screen=1.0):
    """ponsel kaca (koordinat lokal, pusat 0,0): bingkai logam, layar kunci, banner notifikasi turun (banner 0..1)"""
    if a <= 0: return
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2); rad = w * 0.15
    cv.drawRRect(RR(r.makeOffset(0, 34), rad), P(col('#000000', 0.6 * a), blur=44))
    cv.drawRRect(RR(r, rad), P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col('#6A6E8E', a), col('#1A1B2A', a), col('#4A4D68', a), col('#15161F', a)], [0, 0.35, 0.7, 1])))
    sr = r.makeInset(w * 0.035, w * 0.035); srad = rad * 0.8
    cv.drawRRect(RR(sr, srad), P(col('#04050A', a)))
    cv.save(); cv.clipRRect(RR(sr, srad), skia.ClipOp.kIntersect, True)
    if screen > 0:
        sa = a * screen
        cv.drawRect(sr, P(shader=lg(0, sr.top(), 0, sr.bottom(), [col('#2A2470', sa), col('#14123A', sa), col('#0A0A1A', sa)], [0, 0.5, 1])))
        cv.drawCircle(sr.left() + w * 0.2, sr.top() + h * 0.18, w * 0.75, P(shader=rg(sr.left() + w * 0.2, sr.top() + h * 0.18, w * 0.75, [col('#7F5CFF', 0.45 * sa), col('#7F5CFF', 0)])))
        cv.drawCircle(sr.right() - w * 0.1, sr.bottom() - h * 0.2, w * 0.8, P(shader=rg(sr.right() - w * 0.1, sr.bottom() - h * 0.2, w * 0.8, [col('#3F6BFF', 0.35 * sa), col('#3F6BFF', 0)])))
        f = font(M, w * 0.055); s_ = 'Selasa, 29 Oktober'; cv.drawString(s_, -f.measureText(s_) / 2, bl(f, -h * 0.33), f, P(col(ACC_XL, 0.85 * sa)))
        f = font(XB, w * 0.25); s_ = '23.47'; cv.drawString(s_, -f.measureText(s_) / 2, bl(f, -h * 0.24), f, P(col('#FFFFFF', 0.95 * sa)))
        if banner > 0:
            by = lerp(-h * 0.62, -h * 0.06, bo(banner)); notif(cv, 0, by, w * 0.88, btext, sa * clamp(banner * 3))
        cv.drawRect(sr, P(shader=lg(sr.left(), sr.top(), sr.right(), sr.bottom(), [col('#FFFFFF', 0.1 * a), col('#FFFFFF', 0), col('#FFFFFF', 0)], [0, 0.4, 1])))
    cv.restore()
    cv.drawRoundRect(skia.Rect(-w * 0.13, -h / 2 + w * 0.07, w * 0.13, -h / 2 + w * 0.15), w * 0.04, w * 0.04, P(col('#000000', a)))
    cv.drawRRect(RR(r, rad), P(col('#FFFFFF', 0.28 * a), stroke=2.5))

def head_solid(cv, cx, cy, s, a=1.0, face=1, rim=ACC_L, glow=0.0, gc=ACC):
    """kepala profil padat (dari logo) dengan cahaya tepi"""
    if a <= 0: return None
    hp = head_line(cx, cy, s, face)
    if glow > 0: cv.drawPath(hp, P(col(gc, 0.5 * glow * a), stroke=40 * s, blur=40 * s))
    sh = skia.Path(hp); sh.offset(0, 30 * s); cv.drawPath(sh, P(col('#000000', 0.55 * a), blur=36 * s))
    cv.drawPath(hp, P(shader=lg(cx + 260 * s * face, cy - 300 * s, cx - 260 * s * face, cy + 300 * s, [col('#2C3170', a), col('#121329', a), col('#090A14', a)], [0, 0.5, 1])))
    cv.save(); cv.clipPath(hp, skia.ClipOp.kIntersect, True)
    rp = skia.Path(hp); rp.offset(-16 * s * face, 16 * s); cv.drawPath(rp, P(col(rim, 0.75 * a), stroke=26 * s, blur=14 * s))
    cv.restore()
    cv.drawPath(hp, P(col(rim, 0.45 * a), stroke=2.5))
    return hp

def ring_pos(k, n, spin, R, tilt=0.3):
    ang = spin + k * math.tau / n
    return R * math.sin(ang), -R * tilt * math.cos(ang), R * math.cos(ang)

def orbit(cv, cx, cy, R, spin, n, text, a=1.0, size=24, center=None, born=None, drop=0.0, tilt=0.3, hot=0.0):
    """kartu komentar berputar mengelilingi pusat (perspektif, urut kedalaman); center() digambar di tengah antrian"""
    items = []
    for k in range(n):
        x, y, z = ring_pos(k, n, spin, R, tilt)
        b_ = 1.0 if born is None else born(k)
        if b_ <= 0: continue
        yy = y + drop * (380 + 90 * k) ** 1.0 * drop
        items.append((z, k, x, yy, b_))
    items.sort(key=lambda it: -it[0]); drawn = False
    for z, k, x, y, b_ in items:
        if z < 0 and not drawn and center: center(); drawn = True
        X, Y, s = P3(cx + x, cy + y, z)
        dep = clamp((R - z) / (2 * R)); af = a * b_ * lerp(0.3, 1.0, dep) * (1 - clamp(drop * 1.6))
        rot = (k % 3 - 1) * 4 + drop * (k % 2 * 2 - 1) * 40
        comment(cv, text, X, Y, af, s * lerp(0.6, 1.0, bo(b_)), size=size, rot=rot, glow=hot * dep)
    if center and not drawn: center()

def heart_shape(cv, cx, cy, s, a=1.0, c=MINT):
    if a <= 0: return
    hp = heart_path(cx, cy, s); cv.drawPath(hp, P(col(c, 0.5 * a), blur=s * 0.5)); cv.drawPath(hp, P(shader=lg(0, cy - s, 0, cy + s, [col(mixc(c, '#FFFFFF', 0.4), a), col(c, a)])))

def gauge_phys(cv, cx, cy, r, v, a=1.0, t=0.0, boot=1.0, alarm=0.0, **k):
    """alat ukur fisik premium: bingkai logam + kubah kaca di atas gauge()"""
    if a <= 0: return
    cv.drawCircle(cx, cy + r * 0.1, r * 1.22, P(col('#000000', 0.55 * a), blur=r * 0.18))
    sw = skia.GradientShader.MakeSweep(cx, cy, [col(c_, a) for c_ in ('#8A90B8', '#262838', '#E6E8FF', '#3A3D55', '#A8AED6', '#262838', '#8A90B8')], [0, 0.18, 0.32, 0.5, 0.68, 0.85, 1])
    cv.drawCircle(cx, cy, r * 1.17, P(shader=sw)); cv.drawCircle(cx, cy, r * 1.17, P(col('#FFFFFF', 0.35 * a), stroke=2))
    gauge(cv, cx, cy, r, v, a, t, boot, alarm, **k)
    gl = skia.Path(); gl.addArc(skia.Rect(cx - r * 0.98, cy - r * 0.98, cx + r * 0.98, cy + r * 0.98), 200, 70)
    cv.drawPath(gl, P(col('#FFFFFF', 0.22 * a), stroke=r * 0.06, blur=r * 0.02))
    cv.drawCircle(cx - r * 0.35, cy - r * 0.55, r * 0.5, P(shader=rg(cx - r * 0.35, cy - r * 0.55, r * 0.5, [col('#FFFFFF', 0.08 * a), col('#FFFFFF', 0)])))

def crack(cv, cx, cy, r, u, a=1.0, seed=3):
    """retakan kaca yang menjalar (u 0..1)"""
    if u <= 0 or a <= 0: return
    rnd = random.Random(seed); p = skia.Path()
    for k in range(7):
        ang = k * math.tau / 7 + rnd.uniform(-0.3, 0.3); x, y = cx, cy; p.moveTo(x, y); L = r * rnd.uniform(0.6, 1.0) * eo(u)
        for j in range(4):
            ang += rnd.uniform(-0.5, 0.5); x += math.cos(ang) * L / 4; y += math.sin(ang) * L / 4; p.lineTo(x, y)
    cv.drawPath(p, P(col(CORAL, 0.5 * a), stroke=6, blur=5)); cv.drawPath(p, P(col('#FFFFFF', 0.9 * a), stroke=2.2))

def research_card(cv, t, t0, year, names, journal, back=None, t_flip=None, y=700, t_out=None, tag='JPSP'):
    """kartu riset kaca yang berputar masuk dalam 3D; bisa dibalik (t_flip) untuk menampilkan sisi belakang"""
    p = prog(t, t0, t0 + 0.7)
    if p <= 0: return
    ry = lerp(80, 0, bo(p)) + 5 * math.sin((t - t0) * 0.9); rx = 5 * math.sin((t - t0) * 0.7 + 0.5); z = lerp(600, 0, eo(p))
    if t_flip: ry += 180 * eio(prog(t, t_flip, t_flip + 0.6))
    if t_out: z += 900 * ei(prog(t, t_out, t_out + 0.5))
    w, h = 780, 540; a = clamp(p * 2.5) * ((1 - eio(prog(t, t_out, t_out + 0.4))) if t_out else 1.0)
    if a <= 0: return
    with plane(cv, 540, y, z, w, h, ry, rx) as ok:
        if not ok: return
        r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
        if facing(ry, rx) >= 0:
            pth = glass(cv, r, rad=34, a=a, glow=0.35)
            mono(cv, 'ARSIP RISET', r.left() + 54, r.top() + 60, 25, ACC_L, 0.85 * a, sp=4, align=0)
            mono(cv, tag, r.right() - 54, r.top() + 60, 25, MINT, 0.8 * a, sp=3, align=1)
            cv.drawLine(r.left() + 54, r.top() + 102, r.right() - 54, r.top() + 102, P(col(ACC_L, 0.25 * a), stroke=2))
            extrude(cv, year, 0, r.top() + 228, 170, a * eo(prog(t, t0 + 0.25, t0 + 0.6)), depth=14)
            na = eo(prog(t, t0 + 0.5, t0 + 0.9))
            f = font(XB, 44); ww = f.measureText(names); cv.drawString(names, -ww / 2, bl(f, r.top() + 385) + (1 - na) * 12, f, P(col(TXT, na * a)))
            f = font(M, 27); ww = f.measureText(journal); cv.drawString(journal, -ww / 2, bl(f, r.top() + 445), f, P(col(ACC_L, 0.85 * na * a)))
            sheen(cv, pth, r, prog(t, t0 + 0.6, t0 + 1.5), a)
        elif back:
            cv.scale(-1, 1); back(cv, r, a)

def thought(cv, text, cx, cy, size, a=1.0, c=ACC, tail=None, sc=1.0, fill=('#2A2C48', '#171828'), fg=TXT, shake_=0.0):
    """gelembung pikiran kaca dengan ekor ke arah tail"""
    if a <= 0: return
    f = font(XB, size); w = f.measureText(text) + size * 1.8; h = size * 2.0
    cv.save(); cv.translate(cx + shake_, cy); cv.scale(sc, sc)
    tip = ((tail[0] - cx) / sc, (tail[1] - cy) / sc) if tail else (0, h)
    pth, r = bubble_path(0, 0, w, h, tip, maxlen=size * 1.6)
    draw_bubble(cv, pth, r, a, 0.6, fill, c, c)
    cv.drawString(text, -f.measureText(text) / 2, bl(f, 0), f, P(col(fg, a)))
    cv.restore()

def bust(cv, x, y, s, a=1.0, rim=ACC_L):
    """kepala + bahu (padat), dilihat dari belakang/samping"""
    if a <= 0: return
    p = skia.Path.Circle(x, y - s * 0.62, s * 0.3)
    b_ = skia.Path(); b_.moveTo(x - s * 0.75, y + s * 0.9); b_.cubicTo(x - s * 0.75, y - s * 0.05, x - s * 0.45, y - s * 0.28, x, y - s * 0.28)
    b_.cubicTo(x + s * 0.45, y - s * 0.28, x + s * 0.75, y - s * 0.05, x + s * 0.75, y + s * 0.9); b_.close()
    p = skia.Op(p, b_, skia.PathOp.kUnion_PathOp)
    cv.drawPath(p, P(shader=lg(x, y - s, x, y + s, [col('#20234F', a), col('#0A0B16', a)])))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True); rp = skia.Path(p); rp.offset(0, s * 0.07)
    cv.drawPath(rp, P(col(rim, 0.7 * a), stroke=s * 0.08, blur=s * 0.04)); cv.restore()

GREY = ('#D5D7E8', '#6A6D85', '#24263A')

def mood_ball(cv, cx, cy, r, a, t, mood='sad', cols=None, label=None):
    sphere(cv, cx, cy, r, cols or GREY, a, 0.6)
    face(cv, cx, cy + r * 0.05, r, mood, a, t)
    if label: mono(cv, label, cx, cy + r + 46, 26, ACC_L, 0.9 * a, sp=3)

def avatar(cv, x, y, r, c, a=1.0, ok=1.0, gone=0.0):
    if a <= 0: return
    cc = mixc(c, '#3A3B4A', gone)
    cv.drawCircle(x, y + r * 0.2, r * 1.05, P(col('#000000', 0.5 * a), blur=r * 0.3))
    cv.drawCircle(x, y, r, P(shader=lg(x, y - r, x, y + r, [col(mixc(cc, '#FFFFFF', 0.35), a), col(cc, a)])))
    pc = skia.Path(); pc.addCircle(x, y, r); cv.save(); cv.clipPath(pc, skia.ClipOp.kIntersect, True)
    cv.drawCircle(x, y - r * 0.18, r * 0.36, P(col('#FFFFFF', 0.9 * a))); cv.drawOval(skia.Rect(x - r * 0.68, y + r * 0.28, x + r * 0.68, y + r * 1.5), P(col('#FFFFFF', 0.9 * a)))
    cv.restore()
    rc = mixc(MINT, CORAL, gone) if (ok > 0.05 or gone > 0.05) else ACC_L
    cv.drawCircle(x, y, r * 1.12, P(col(rc, (0.25 + 0.75 * max(ok, gone)) * a), stroke=r * 0.1))
    if ok > 0.5: heart_shape(cv, x + r * 0.75, y - r * 0.75, r * 0.3, a * prog(ok, 0.5, 1.0), MINT)
    if gone > 0.1: cross(cv, x + r * 0.75, y - r * 0.75, r * 0.22, a * gone, CORAL, r * 0.09)

def stander(cv, x, foot, h, a=1.0, rim=ACC_L):
    """siluet orang berdiri (padat) dengan cahaya tepi dari atas"""
    if a <= 0: return
    p = skia.Path.Circle(x, foot - h * 0.9, h * 0.075)
    b_ = skia.Path(); b_.moveTo(x - h * 0.04, foot - h * 0.83)
    b_.cubicTo(x - h * 0.17, foot - h * 0.82, x - h * 0.19, foot - h * 0.76, x - h * 0.19, foot - h * 0.64)
    b_.lineTo(x - h * 0.17, foot - h * 0.4); b_.lineTo(x - h * 0.125, foot - h * 0.4); b_.lineTo(x - h * 0.105, foot)
    b_.lineTo(x - h * 0.02, foot); b_.lineTo(x, foot - h * 0.36); b_.lineTo(x + h * 0.02, foot); b_.lineTo(x + h * 0.105, foot)
    b_.lineTo(x + h * 0.125, foot - h * 0.4); b_.lineTo(x + h * 0.17, foot - h * 0.4); b_.lineTo(x + h * 0.19, foot - h * 0.64)
    b_.cubicTo(x + h * 0.19, foot - h * 0.76, x + h * 0.17, foot - h * 0.82, x + h * 0.04, foot - h * 0.83); b_.close()
    p = skia.Op(p, b_, skia.PathOp.kUnion_PathOp)
    cv.drawPath(p, P(shader=lg(x, foot - h, x, foot, [col('#262A5E', a), col('#0A0B16', a)])))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True); rp = skia.Path(p); rp.offset(0, h * 0.035)
    cv.drawPath(rp, P(col(rim, 0.85 * a), stroke=h * 0.035, blur=h * 0.018)); cv.restore()

AV_COL = ['#FF8A7A', '#7FB8FF', '#B57BFF', '#FFC56B', '#3FD6A4', '#FF7FC8', '#8C93FF', '#5AD1E6']
# ------------------------------------------------------------ helper EP12: panggung sinematik + tokoh kapsul premium (gaya EP03 yang viral)
AV_COL = ['#FF8A7A', '#7FB8FF', '#B57BFF', '#FFC56B', '#3FD6A4', '#FF7FC8', '#8C93FF', '#5AD1E6']
GOLD = '#FFC56B'; HOTPINK = '#FF7FC8'

def hero(cv, x, foot, h, mood='worried', a=1.0, t=0.0, sweat=0.0, glow=0.0, gc=ACC, tremble=0.0, mouth_open=0.0):
    """tokoh kapsul premium (siluet seperti EP03): badan kapsul mengilap + kepala bola dengan ekspresi"""
    if a <= 0: return
    x += tremble * 5 * math.sin(t * 58)
    bw, bh, hr = 0.42 * h, 0.6 * h, 0.17 * h
    hx, hy = x, foot - bh - hr * 0.92
    if a < 1: layer(cv, a)
    cv.drawOval(skia.Rect(x - bw * 0.85, foot - 12, x + bw * 0.85, foot + 14), P(col('#000000', 0.6), blur=10))
    body = skia.RRect.MakeRectXY(skia.Rect(x - bw / 2, foot - bh, x + bw / 2, foot), bw * 0.45, bw * 0.45)
    if glow > 0:
        cv.drawRRect(body, P(col(gc, 0.45 * glow), stroke=26, blur=22)); cv.drawCircle(hx, hy, hr * 1.2, P(col(gc, 0.4 * glow), blur=hr * 0.5))
    cv.drawRRect(body, P(shader=lg(x - bw / 2, foot - bh, x + bw / 2, foot, [col('#4A4E7A'), col('#22243A'), col('#14152A')], [0, 0.5, 1])))
    pb = skia.Path(); pb.addRRect(body); cv.save(); cv.clipPath(pb, skia.ClipOp.kIntersect, True)
    cv.drawOval(skia.Rect(x - bw * 0.42, foot - bh * 0.95, x - bw * 0.05, foot - bh * 0.45), P(col('#FFFFFF', 0.12), blur=8))
    rp = skia.Path(pb); rp.offset(-bw * 0.08, 0); cv.drawPath(rp, P(col(gc if glow > 0 else ACC_L, 0.5), stroke=bw * 0.08, blur=bw * 0.05))
    cv.restore()
    cv.drawRRect(body, P(col(ACC_L, 0.55), stroke=2.5))
    cv.drawCircle(hx, hy, hr, P(shader=rg(hx - hr * 0.35, hy - hr * 0.4, hr * 1.6, [col('#6A6E9E'), col('#33365A'), col('#1A1B30')], [0, 0.55, 1])))
    cv.drawOval(skia.Rect(hx - hr * 0.6, hy - hr * 0.85, hx - hr * 0.05, hy - hr * 0.45), P(col('#FFFFFF', 0.22), blur=hr * 0.1))
    cv.drawCircle(hx, hy, hr, P(col(ACC_L, 0.6), stroke=2.5))
    ink = P(col(ACC_XL), stroke=max(3, hr * 0.08))
    ey = hy - hr * 0.05
    for s in (-1, 1):
        ex = hx + s * hr * 0.36
        if mood == 'excited':
            e = skia.Path(); e.moveTo(ex - hr * 0.14, ey + hr * 0.04); e.quadTo(ex, ey - hr * 0.16, ex + hr * 0.14, ey + hr * 0.04); cv.drawPath(e, ink)
        elif mood == 'calm':
            e = skia.Path(); e.moveTo(ex - hr * 0.13, ey); e.quadTo(ex, ey + hr * 0.1, ex + hr * 0.13, ey); cv.drawPath(e, ink)
        else:
            bk = blink_at(t, 0.2 + s * 0.05); eh = hr * 0.17 * (1 - 0.9 * bk)
            cv.drawOval(skia.Rect(ex - hr * 0.13, ey - eh, ex + hr * 0.13, ey + eh), P(col(ACC_XL)))
            if mood == 'worried': cv.drawLine(ex - s * hr * 0.17, ey - hr * 0.36, ex + s * hr * 0.12, ey - hr * 0.27, ink)
    my = hy + hr * 0.42; m = skia.Path()
    if mood == 'excited':
        mo = hr * (0.16 + 0.14 * mouth_open)
        m.moveTo(hx - hr * 0.32, my - hr * 0.06); m.quadTo(hx, my + mo * 2.2, hx + hr * 0.32, my - hr * 0.06); m.close()
        cv.drawPath(m, P(col(ACC_XL))); cv.drawPath(m, ink)
        for s in (-1, 1): cv.drawOval(skia.Rect(hx + s * hr * 0.62 - hr * 0.14, my - hr * 0.22, hx + s * hr * 0.62 + hr * 0.14, my - hr * 0.08), P(col('#FF8FA8', 0.55), blur=3))
    elif mood in ('happy', 'calm'):
        m.moveTo(hx - hr * 0.26, my - hr * 0.04); m.quadTo(hx, my + hr * 0.2, hx + hr * 0.26, my - hr * 0.04); cv.drawPath(m, ink)
    elif mood == 'worried':
        m.moveTo(hx - hr * 0.24, my + hr * 0.04)
        for k in range(1, 7): m.lineTo(hx - hr * 0.24 + k * hr * 0.08, my + (hr * 0.05 if k % 2 else -hr * 0.03))
        cv.drawPath(m, ink)
    else:
        m.moveTo(hx - hr * 0.18, my); m.lineTo(hx + hr * 0.18, my); cv.drawPath(m, ink)
    if sweat > 0:
        for k, (dx, ph) in enumerate(((0.95, 0.0), (-1.0, 0.5))):
            u = ((t * 0.9 + ph) % 1.0) * sweat
            sx, sy = hx + dx * hr, hy - hr * 0.35 + u * hr * 0.6
            d = skia.Path(); d.moveTo(sx, sy - hr * 0.26); d.quadTo(sx + hr * 0.15, sy, sx, sy + hr * 0.1); d.quadTo(sx - hr * 0.15, sy, sx, sy - hr * 0.26); d.close()
            cv.drawPath(d, P(col('#8FD3FF', min(1, sweat * 1.5) * (1 - u * 0.5))))
    if a < 1: cv.restore()
    return hx, hy, hr

def stage(cv, a, t, warm=0.0, cx=540, floor_y=1080, cone_w=260):
    """panggung: tirai beludru, lantai mengilap, lampu sorot volumetrik (warm 0..1 jadi keemasan)"""
    if a <= 0: return
    for sd in (-1, 1):
        cur = skia.Path(); x0 = 0 if sd < 0 else W; x1 = 170 if sd < 0 else W - 170
        cur.moveTo(x0, 250); cur.lineTo(x1, 250)
        for i in range(9):
            y = 250 + i * 110; cur.quadTo(x1 + sd * -18 * math.sin(i * 1.3 + t * 0.6), y + 55, x1 + sd * (6 * math.sin(i * 1.7)), y + 110)
        cur.lineTo(x0, 1250); cur.close()
        cv.drawPath(cur, P(shader=lg(x0, 0, x1, 0, [col('#2A0F3A', a), col('#4A1E66', a), col('#2A0F3A', a)], [0, 0.6, 1])))
        for k in range(4):
            fx = x0 + (x1 - x0) * (0.2 + k * 0.22); cv.drawLine(fx, 250, fx + sd * 6, 1250, P(col('#000000', 0.25 * a), stroke=10, blur=6))
    fl = skia.Path(); fl.moveTo(0, floor_y - 40); fl.lineTo(W, floor_y - 40); fl.lineTo(W, 1250); fl.lineTo(0, 1250); fl.close()
    cv.drawPath(fl, P(shader=lg(0, floor_y - 40, 0, 1250, [col('#1E1A3A', a), col('#0B0A16', a)])))
    for k in range(7):
        y = floor_y - 40 + k * k * 6; cv.drawLine(0, y, W, y, P(col('#AEB6FF', 0.05 * a), stroke=1.5))
    lc = mixc('#DDE0FF', GOLD, warm)
    cone = skia.Path(); cone.moveTo(cx - 40, 250); cone.lineTo(cx + 40, 250); cone.lineTo(cx + cone_w, floor_y); cone.lineTo(cx - cone_w, floor_y); cone.close()
    cv.drawPath(cone, P(shader=lg(0, 250, 0, floor_y, [col(lc, (0.26 + 0.1 * warm) * a), col(lc, 0.07 * a)])))
    cv.drawOval(skia.Rect(cx - cone_w - 30, floor_y - 34, cx + cone_w + 30, floor_y + 34), P(shader=rg(cx, floor_y, cone_w + 30, [col(lc, 0.35 * a), col(lc, 0)])))

def ecg_path(x0, x1, y, amp, t, rate=1.6, phase=0.0):
    """garis detak jantung yang berjalan"""
    p = skia.Path(); n = 120
    for i in range(n + 1):
        u = i / n; x = lerp(x0, x1, u); ph = (u * 3 - t * rate + phase) % 1.0
        v = 0.0
        if 0.40 < ph < 0.44: v = -0.25
        elif 0.44 < ph < 0.48: v = 1.0
        elif 0.48 < ph < 0.53: v = -0.55
        elif 0.60 < ph < 0.72: v = 0.18 * math.sin((ph - 0.6) / 0.12 * math.pi)
        (p.moveTo if i == 0 else p.lineTo)(x, y - v * amp)
    return p

def heart_big(cv, cx, cy, s, a, t, rate=2.2, c=CORAL):
    if a <= 0: return
    pu = 1 + 0.12 * beat_pulse(t * rate)
    hp = heart_path(cx, cy, s * pu)
    cv.drawPath(hp, P(col(c, 0.55 * a), blur=s * 0.35))
    cv.drawPath(hp, P(shader=rg(cx - s * 0.3, cy - s * 0.4, s * 1.6, [col(mixc(c, '#FFFFFF', 0.45), a), col(c, a), col(mixc(c, '#000000', 0.45), a)], [0, 0.5, 1])))
    cv.drawOval(skia.Rect(cx - s * 0.75, cy - s * 0.65, cx - s * 0.25, cy - s * 0.3), P(col('#FFFFFF', 0.3 * a), blur=s * 0.08))

def say(cv, text, cx, cy, size, a, c, fill, fg, tail, sc=1.0, glow=0.6, strike=0.0):
    """gelembung ucapan kaca + coretan"""
    if a <= 0: return
    f = font(XB, size); w = f.measureText(text) + size * 1.6; h = size * 2.0
    cv.save(); cv.translate(cx, cy); cv.scale(sc, sc)
    pth, r = bubble_path(0, 0, w, h, ((tail[0] - cx) / sc, (tail[1] - cy) / sc), maxlen=size * 1.4)
    draw_bubble(cv, pth, r, a, glow, fill, c, c)
    cv.drawString(text, -f.measureText(text) / 2, bl(f, 0), f, P(col(fg, a)))
    if strike > 0:
        x0 = -w / 2 + 14; cv.drawLine(x0, 4, x0 + (w - 28) * eo(strike), -4, P(col(CORAL, 0.6 * a), stroke=18, blur=8)); cv.drawLine(x0, 4, x0 + (w - 28) * eo(strike), -4, P(col('#FFFFFF', a), stroke=7))
    cv.restore()

def mic_stand(cv, x, foot, top, a, glow=0.0):
    if a <= 0: return
    cv.drawLine(x, foot, x, top + 40, P(col('#8A8EAE', a), stroke=7)); cv.drawOval(skia.Rect(x - 50, foot - 8, x + 50, foot + 8), P(col('#5A5E7A', a)))
    hd = skia.Rect(x - 20, top - 20, x + 20, top + 44)
    if glow > 0: cv.drawRoundRect(hd, 20, 20, P(col(GOLD, 0.6 * glow * a), blur=16))
    cv.drawRoundRect(hd, 20, 20, P(shader=lg(x - 20, 0, x + 20, 0, [col('#9AA0C8', a), col('#E8EAFF', a), col('#5A5E7A', a)])))
    for k in range(4): cv.drawLine(x - 16, top - 8 + k * 11, x + 16, top - 8 + k * 11, P(col('#3A3D55', 0.6 * a), stroke=2))

def note(cv, x, y, s, a, c=GOLD):
    if a <= 0: return
    cv.drawOval(skia.Rect(x - s * 0.45, y - s * 0.3, x + s * 0.45, y + s * 0.3), P(col(c, a)))
    cv.drawLine(x + s * 0.4, y, x + s * 0.4, y - s * 1.5, P(col(c, a), stroke=s * 0.16)); cv.drawLine(x + s * 0.4, y - s * 1.5, x + s * 0.95, y - s * 1.2, P(col(c, a), stroke=s * 0.16))

def eyes_ring(cv, t, a, love=0.0):
    """mata penonton yang mengawasi di kegelapan (khas EP01/EP03), bisa berubah jadi hati"""
    for k, (x, y, s, ph) in enumerate(((150, 520, 26, 0.0), (960, 640, 28, 0.3), (120, 820, 22, 0.55), (960, 800, 24, 0.15), (220, 1010, 20, 0.7), (860, 1030, 22, 0.4))):
        if love > 0.5: heart_shape(cv, x, y, s * 0.9 * (1 + 0.08 * math.sin(t * 5 + k)), a * prog(love, 0.5, 1.0), HOTPINK)
        elif love < 0.5: b.watcher_eye(cv, x, y, s, 540, 760, t, ph, a * (1 - love * 2))

def podium(cv, x, foot, w, a):
    if a <= 0: return
    p = skia.Path(); p.moveTo(x - w * 0.5, foot - w * 0.95); p.lineTo(x + w * 0.5, foot - w * 0.95); p.lineTo(x + w * 0.38, foot); p.lineTo(x - w * 0.38, foot); p.close()
    cv.drawPath(p, P(shader=lg(0, foot - w, 0, foot, [col('#5A5F9E', a), col('#22243A', a)]))); cv.drawPath(p, P(col(ACC_L, 0.5 * a), stroke=2.5))
    cv.drawRoundRect(skia.Rect(x - w * 0.6, foot - w * 1.02, x + w * 0.6, foot - w * 0.9), 8, 8, P(col('#7F84C8', a)))

# ------------------------------------------------------------ helper EP14: kafe malam + dua tokoh kapsul ngobrol, meter nyambung
GOLD = '#FFC56B'; HOTPINK = '#FF7FC8'; WARM = '#FFC98A'
def cafe_bg(cv, a, t):
    """latar kafe malam: lampu gantung hangat + jendela kota buram (tanpa titik/bokeh)"""
    if a <= 0: return
    for k, x in enumerate((300, 780)):
        cv.drawLine(x, 255, x, 330, P(col('#3A3D55', a), stroke=4))
        sh = skia.Path(); sh.moveTo(x - 60, 380); sh.lineTo(x - 24, 330); sh.lineTo(x + 24, 330); sh.lineTo(x + 60, 380); sh.close()
        cv.drawPath(sh, P(shader=lg(0, 330, 0, 380, [col('#5A4A3A', a), col('#2A221A', a)])))
        cv.drawOval(skia.Rect(x - 60, 372, x + 60, 388), P(col(WARM, 0.9 * a)))
        cone = skia.Path(); cone.moveTo(x - 58, 382); cone.lineTo(x + 58, 382); cone.lineTo(x + 260, 1000); cone.lineTo(x - 260, 1000); cone.close()
        cv.drawPath(cone, P(shader=lg(0, 382, 0, 1000, [col(WARM, 0.16 * a), col(WARM, 0)])))
    for k in range(6):
        x = 60 + k * 190; h = 120 + 60 * ((k * 37) % 5)
        cv.drawRect(skia.Rect(x, 1010 - h, x + 120, 1010), P(col('#1A1C34', 0.6 * a)))
        for j in range(3):
            cv.drawRect(skia.Rect(x + 20, 1010 - h + 20 + j * 34, x + 50, 1010 - h + 36 + j * 34), P(col(WARM, 0.18 * a)))

def table(cv, cx, y, w, a, t, cups=True, legs=True):
    if a <= 0: return
    cv.drawOval(skia.Rect(cx - w / 2, y - 26, cx + w / 2, y + 26), P(shader=lg(0, y - 26, 0, y + 26, [col('#7A5A40', a), col('#4A3424', a)])))
    if legs:
        cv.drawRect(skia.Rect(cx - 14, y + 10, cx + 14, y + 150), P(col('#2A221A', a)))
        cv.drawOval(skia.Rect(cx - 80, y + 140, cx + 80, y + 162), P(col('#2A221A', a)))
    if cups:
        for sd in (-1, 1):
            x = cx + sd * w * 0.25
            cv.drawRoundRect(skia.Rect(x - 26, y - 62, x + 26, y - 10), 10, 10, P(shader=lg(x - 26, 0, x + 26, 0, [col('#F2F0F8', a), col('#C9CBE0', a)])))
            hd = skia.Path(); hd.addArc(skia.Rect(x + 16, y - 52, x + 44, y - 24), -90, 180); cv.drawPath(hd, P(col('#C9CBE0', a), stroke=5))
            for k in range(2):
                u = ((t * 0.7 + k * 0.5 + sd * 0.25) % 1.0); sp = skia.Path(); sp.moveTo(x - 6 + k * 12, y - 66)
                for i in range(1, 5): sp.lineTo(x - 6 + k * 12 + 6 * math.sin(i + t * 3 + k), y - 66 - i * 14 * (0.5 + u))
                cv.drawPath(sp, P(col('#F0EFF6', 0.35 * (1 - u) * a), stroke=4, blur=3))

def conn_meter(cv, x0, x1, y, v, a, t, label='NYAMBUNG'):
    """meter keterhubungan antara dua orang (0..1) dengan hati di ujung"""
    if a <= 0: return
    cv.drawRoundRect(skia.Rect(x0, y - 13, x1, y + 13), 13, 13, P(col('#1A1B30', 0.9 * a))); cv.drawRoundRect(skia.Rect(x0, y - 13, x1, y + 13), 13, 13, P(col(ACC_XL, 0.35 * a), stroke=2))
    xv = x0 + (x1 - x0) * clamp(v)
    if xv > x0 + 20:
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 9, xv, y + 9), 9, 9, P(col(HOTPINK, 0.5 * a), blur=10))
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 9, xv, y + 9), 9, 9, P(shader=lg(x0, 0, x1, 0, [col('#8C93FF', a), col(HOTPINK, a)])))
    heart_shape(cv, xv, y, 18 * (1 + 0.15 * v * math.sin(t * 6)), a, HOTPINK)
    mono(cv, label, (x0 + x1) / 2, y - 36, 22, ACC_L, 0.85 * a, sp=4)

def chat_panel(cv, cx, cy, w, h, msgs, a, t, t0, step=0.32, qc=GOLD):
    """panel obrolan kaca: msgs = [(sisi 'L'/'R', teks, pertanyaan?)], muncul bertahap"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); glass(cv, r, rad=30, a=a, glow=0.2)
    f = font(B, 24); y = r.top() + 50
    for k, (side, txt, q) in enumerate(msgs):
        pa = prog(t, t0 + k * step, t0 + k * step + 0.2)
        if pa <= 0: break
        tw = f.measureText(txt) + 40; bh = 50
        x = r.left() + 24 if side == 'L' else r.right() - 24 - tw
        br = skia.Rect(x, y - bh / 2, x + tw, y + bh / 2)
        c = qc if q else ('#3A3D66' if side == 'L' else '#2A2C48')
        cv.drawRoundRect(br, 22, 22, P(col(c, (0.95 if not q else 0.9) * a * clamp(pa * 2))))
        if q: cv.drawRoundRect(br, 22, 22, P(col(qc, 0.5 * a * pa), stroke=8, blur=8))
        cv.drawString(txt, br.left() + 20, bl(f, y), f, P(col(INK if q else TXT, a * clamp(pa * 2))))
        y += bh + 14

def ear(cv, cx, cy, s, a, c=MINT):
    if a <= 0: return
    p = skia.Path(); p.moveTo(cx - s * 0.2, cy + s * 0.9)
    p.cubicTo(cx - s * 0.9, cy + s * 0.6, cx - s * 0.9, cy - s * 0.9, cx, cy - s * 0.9)
    p.cubicTo(cx + s * 0.8, cy - s * 0.9, cx + s * 0.9, cy - s * 0.1, cx + s * 0.4, cy + s * 0.3)
    p.cubicTo(cx + s * 0.1, cy + s * 0.55, cx + s * 0.2, cy + s * 0.9, cx - s * 0.2, cy + s * 0.9)
    cv.drawPath(p, P(col(c, 0.45 * a), blur=s * 0.25)); cv.drawPath(p, P(shader=lg(cx, cy - s, cx, cy + s, [col(mixc(c, '#FFFFFF', 0.4), a), col(c, a)])))
    inner = skia.Path(); inner.moveTo(cx - s * 0.25, cy + s * 0.2); inner.cubicTo(cx - s * 0.5, cy - s * 0.4, cx + s * 0.4, cy - s * 0.6, cx + s * 0.25, cy - s * 0.05)
    cv.drawPath(inner, P(col('#0D2019', 0.6 * a), stroke=s * 0.1))
    for k in range(3):
        arc = skia.Path(); rr = s * (1.2 + 0.35 * k); arc.addArc(skia.Rect(cx - rr - s * 0.3, cy - rr, cx + rr - s * 0.3, cy + rr), 150, 60)
        cv.drawPath(arc, P(col(c, (0.6 - 0.15 * k) * a), stroke=4))

def two_chat(cv, t, a, lx=300, rx=780, foot=1000, h=330, lmood='neutral', rmood='happy', lglow=0.0, rglow=0.0, lc=GOLD, rc=HOTPINK, ltrem=0.0):
    hero(cv, lx, foot, h, lmood, a, t, glow=lglow, gc=lc, tremble=ltrem, mouth_open=0.4)
    hero(cv, rx, foot, h, rmood, a, t, glow=rglow, gc=rc, mouth_open=0.4 + 0.4 * math.sin(t * 5))

# ------------------------------------------------------------ helper EP17: kartu pertanyaan 3D + lapisan diri
QTEXT = 'Kalau bisa makan malam bareng siapa aja di dunia, kamu pilih siapa?'
def wob(t): return 4 * math.sin(t * 1.5), 4 * math.sin(t * 1.1)
def wrap(text, f, maxw):
    lines, cur = [], ''
    for w in text.split(' '):
        nxt = (cur + ' ' + w).strip()
        if cur and f.measureText(nxt) > maxw: lines.append(cur); cur = w
        else: cur = nxt
    if cur: lines.append(cur)
    return lines

def q_card(cv, cx, cy, w, h, a, t, ry=0.0, rx=0.0, z=0.0, num='01', text=QTEXT, hl=0.0, glow=0.6, size=44, back_only=False):
    """kartu pertanyaan 3D: muka = pertanyaan (ry 0), belakang = '?' emas (ry 180)"""
    if a <= 0: return
    with plane(cv, cx, cy, z, w, h, ry, rx) as ok:
        if not ok: return
        r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2); rad = w * 0.07
        cv.drawRoundRect(r, rad, rad, P(col(GOLD, 0.5 * glow * a), blur=30))
        if facing(ry, rx) >= 0 and not back_only:
            cv.drawRoundRect(r, rad, rad, P(shader=lg(0, -h / 2, 0, h / 2, [col('#2A2440', a), col('#16142A', a)])))
            cv.drawRoundRect(r, rad, rad, P(col(GOLD, a), stroke=4)); cv.drawRoundRect(r.makeInset(14, 14), rad * 0.7, rad * 0.7, P(col(GOLD, 0.35 * a), stroke=1.5))
            mono(cv, f'PERTANYAAN {num} / 36', 0, -h / 2 + 52, max(16, w * 0.04), GOLD, a, sp=3)
            f = font(XB, size); lines = wrap(text, f, w * 0.8); lh = size * 1.22
            y0 = -(len(lines) - 1) * lh / 2 + h * 0.05
            for i, ln in enumerate(lines):
                last = i == len(lines) - 1
                c = mixc(TXT, GOLD, hl) if last or (i == len(lines) - 2 and 'kamu' in ln) else TXT
                cv.drawString(ln, -f.measureText(ln) / 2, bl(f, y0 + i * lh), f, P(col(c, a)))
        else:
            if facing(ry, rx) < 0: cv.scale(-1, 1)
            cv.drawRoundRect(r, rad, rad, P(shader=lg(-w / 2, -h / 2, w / 2, h / 2, [col('#FFD98A', a), col('#E09A3A', a), col('#B8741E', a)])))
            for k in range(6):
                cv.drawCircle(0, 0, w * (0.12 + 0.07 * k), P(col('#FFFFFF', 0.08 * a), stroke=2))
            f = font(XB, w * 0.5); s_ = '?'
            cv.drawString(s_, -f.measureText(s_) / 2, bl(f, 0) + 6, f, P(col('#6A4A10', 0.6 * a), blur=4))
            cv.drawString(s_, -f.measureText(s_) / 2, bl(f, 0), f, P(col('#FFF6E0', a)))
            cv.drawRoundRect(r, rad, rad, P(col('#FFFFFF', 0.5 * a), stroke=3))

def mini_card(cv, x, y, w, h, a, rot, num, c=('#3A3D66', '#22243A'), edge=ACC_L, nc=ACC_XL):
    if a <= 0: return
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    cv.drawRoundRect(r.makeOffset(3, 8), 10, 10, P(col('#000000', 0.45 * a), blur=8))
    cv.drawRoundRect(r, 10, 10, P(shader=lg(0, -h / 2, 0, h / 2, [col(c[0], a), col(c[1], a)])))
    cv.drawRoundRect(r, 10, 10, P(col(edge, 0.6 * a), stroke=2))
    mono(cv, num, 0, 0, w * 0.32, nc, a, sp=1)
    cv.restore()

def depth_col(u):
    """warna kartu dari ringan (biru) ke pribadi (emas/pink)"""
    return mixc(mixc('#7FB8FF', '#B57BFF', clamp(u * 2)), HOTPINK if u < 0.9 else GOLD, clamp(u * 2 - 1))

def shells(cv, x, cy, a, t, opened, c):
    """lapisan diri: 3 cangkang kaca di sekitar tokoh; opened 0..3 = berapa lapis yang sudah terbuka (memudar keluar)"""
    for k in range(3):
        rr = 210 - k * 45; o = clamp(opened - k)
        if o >= 1: continue
        sc = 1 + 0.35 * eo(o); aa = a * (1 - o)
        cv.drawOval(skia.Rect(x - rr * 0.75 * sc, cy - rr * sc, x + rr * 0.75 * sc, cy + rr * sc), P(col(ACC_L, 0.08 * aa)))
        cv.drawOval(skia.Rect(x - rr * 0.75 * sc, cy - rr * sc, x + rr * 0.75 * sc, cy + rr * sc), P(col(ACC_L, 0.45 * aa), stroke=2.5))
    warm = clamp(opened / 3)
    cv.drawCircle(x, cy - 20, 90, P(shader=rg(x, cy - 20, 160, [col(c, 0.45 * warm * a), col(c, 0)])))

KRIK = [('krik...', 170, 520, -8, -0.4), ('krik...', 900, 600, 7, 0.45), ('. . .', 540, 470, 0, 1.0)]

# ------------------------------------------------------------ helper EP19: hati kaca berisi cairan + bantuan kecil
def glass_heart(cv, cx, cy, s, v, a, t, label='SUKA', c=HOTPINK, glow=0.0):
    """hati kaca 3D berisi cairan yang bergelombang (v 0..1 = tinggi cairan)"""
    if a <= 0: return
    hp = heart_path(cx, cy, s)
    top, bot = cy - s * 0.85, cy + s * 0.9
    if glow > 0: cv.drawPath(hp, P(col(c, 0.55 * glow * a), blur=s * 0.45))
    cv.drawPath(hp, P(col('#1A1430', 0.55 * a)))
    cv.save(); cv.clipPath(hp, skia.ClipOp.kIntersect, True)
    lvl = lerp(bot, top, clamp(v))
    wv = skia.Path(); wv.moveTo(cx - s * 1.5, bot + 10)
    for i in range(41):
        x = cx - s * 1.5 + 3 * s * i / 40; wv.lineTo(x, lvl + s * 0.06 * math.sin(i * 0.5 + t * 4))
    wv.lineTo(cx + s * 1.5, bot + 10); wv.close()
    cv.drawPath(wv, P(shader=lg(0, lvl, 0, bot, [col(mixc(c, '#FFFFFF', 0.35), a), col(c, a), col(mixc(c, '#000000', 0.35), a)], [0, 0.4, 1])))
    for k in range(3):
        bu = (t * 0.5 + k * 0.33) % 1.0
        by = lerp(bot - s * 0.1, lvl, bu)
        if by > lvl + 4: cv.drawCircle(cx + (k - 1) * s * 0.3, by, s * 0.05, P(col('#FFFFFF', 0.45 * a * (1 - bu))))
    cv.drawOval(skia.Rect(cx - s * 0.75, cy - s * 0.7, cx - s * 0.25, cy - s * 0.25), P(col('#FFFFFF', 0.28 * a), blur=s * 0.06))
    cv.restore()
    cv.drawPath(hp, P(col('#FFFFFF', 0.6 * a), stroke=3))
    if label: mono(cv, f'{label} {int(round(v * 100))}%', cx, bot + 34, 22, mixc(c, '#FFFFFF', 0.3), a, sp=2)

def pen(cv, x, y, s, a, rot=-35, c=GOLD):
    """pulpen emas (ujung di x,y)"""
    if a <= 0: return
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    body = skia.Rect(-s * 0.09, -s * 1.0, s * 0.09, -s * 0.16)
    cv.drawRoundRect(body.makeOffset(4, 8), s * 0.09, s * 0.09, P(col('#000000', 0.4 * a), blur=8))
    cv.drawRoundRect(body, s * 0.09, s * 0.09, P(shader=lg(-s * 0.09, 0, s * 0.09, 0, [col(mixc(c, '#FFFFFF', 0.45), a), col(c, a), col(mixc(c, '#000000', 0.4), a)])))
    tip = skia.Path(); tip.moveTo(-s * 0.09, -s * 0.16); tip.lineTo(s * 0.09, -s * 0.16); tip.lineTo(0, 0); tip.close()
    cv.drawPath(tip, P(col('#E8E6F0', a))); cv.drawRect(skia.Rect(-s * 0.1, -s * 0.78, s * 0.1, -s * 0.7), P(col('#FFFFFF', 0.6 * a)))
    cv.restore()

def coin(cv, x, y, r, a, t=0.0, spin=0.0):
    """koin emas yang berputar (spin = fase)"""
    if a <= 0: return
    sx = max(0.15, abs(math.cos(spin)))
    cv.save(); cv.translate(x, y); cv.scale(sx, 1)
    cv.drawCircle(0, 4, r, P(col('#000000', 0.4 * a), blur=6))
    cv.drawCircle(0, 0, r, P(shader=rg(-r * 0.3, -r * 0.3, r * 1.6, [col('#FFF1B8', a), col(GOLD, a), col('#B8741E', a)])))
    cv.drawCircle(0, 0, r * 0.78, P(col('#FFF6D8', 0.7 * a), stroke=r * 0.08))
    f = font(XB, r * 1.0); s_ = '$'; cv.drawString(s_, -f.measureText(s_) / 2, bl(f, 0), f, P(col('#8A5A12', a)))
    cv.restore()

def clipboard(cv, x, y, s, a):
    if a <= 0: return
    r = skia.Rect(x - s * 0.38, y - s * 0.5, x + s * 0.38, y + s * 0.5)
    cv.drawRoundRect(r, s * 0.06, s * 0.06, P(col('#6A4A30', a)))
    cv.drawRect(r.makeInset(s * 0.06, s * 0.08), P(col('#F4F2FA', a)))
    for k in range(4): cv.drawLine(r.left() + s * 0.12, r.top() + s * (0.25 + 0.15 * k), r.right() - s * 0.12, r.top() + s * (0.25 + 0.15 * k), P(col('#9A9CB8', a), stroke=3))
    cv.drawRoundRect(skia.Rect(x - s * 0.14, r.top() - s * 0.05, x + s * 0.14, r.top() + s * 0.06), s * 0.03, s * 0.03, P(col('#C9CBE0', a)))

def favor_card(cv, text, x, y, a, ok=True, sc=1.0, strike=0.0):
    """kartu kaca bantuan kecil (✓) atau besar (✗)"""
    if a <= 0: return
    c = MINT if ok else CORAL
    f = font(B, 30); w = f.measureText(text) + 120; h = 74
    cv.save(); cv.translate(x, y); cv.scale(sc, sc)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    glass(cv, r, rad=h * 0.4, a=a, glow=0.35, gc=c)
    cv.drawString(text, -w / 2 + 34, bl(f, 0), f, P(col(TXT, a)))
    if ok: check_mark(cv, w / 2 - 44, 0, 20, 1.0, a, MINT)
    else: cross(cv, w / 2 - 44, 0, 18, a, CORAL, 6)
    if strike > 0: cv.drawLine(-w / 2 + 24, 0, -w / 2 + 24 + (w - 48) * eo(strike), 0, P(col(CORAL, a), stroke=5))
    cv.restore()

# ------------------------------------------------------------ helper EP20: kotak cerita emas + bola cerita yang bolak-balik
def orb(cv, x, y, r, a, c=GOLD):
    """bola cahaya cerita"""
    if a <= 0: return
    cv.drawCircle(x, y, r * 2.2, P(shader=rg(x, y, r * 2.2, [col(c, 0.45 * a), col(c, 0)])))
    cv.drawCircle(x, y, r, P(shader=rg(x - r * 0.3, y - r * 0.3, r * 1.4, [col('#FFFFFF', a), col(mixc(c, '#FFFFFF', 0.4), a), col(c, a)], [0, 0.4, 1])))

def padlock(cv, x, y, s, a, u=0.0, c=GOLD):
    """gembok: u 0 terkunci -> 1 terbuka (shackle naik & berputar)"""
    if a <= 0: return
    cv.save(); cv.translate(x, y)
    sh = skia.Path(); sh.addArc(skia.Rect(-s * 0.32, -s * 0.95, s * 0.32, -s * 0.25), 180, 180)
    sh.moveTo(-s * 0.32, -s * 0.6); sh.lineTo(-s * 0.32, -s * 0.15)
    sh.moveTo(s * 0.32, -s * 0.6); sh.lineTo(s * 0.32, -s * 0.15 - s * 0.25 * eo(u))
    cv.save(); cv.translate(-s * 0.32, -s * 0.15); cv.rotate(-35 * eo(u)); cv.translate(s * 0.32, s * 0.15 - s * 0.3 * eo(u))
    cv.drawPath(sh, P(col('#C9CBE0', a), stroke=s * 0.13)); cv.restore()
    body = skia.Rect(-s * 0.48, -s * 0.2, s * 0.48, s * 0.5)
    cv.drawRoundRect(body, s * 0.12, s * 0.12, P(shader=lg(0, -s * 0.2, 0, s * 0.5, [col(mixc(c, '#FFFFFF', 0.4), a), col(c, a), col(mixc(c, '#000000', 0.35), a)])))
    cv.drawCircle(0, s * 0.1, s * 0.08, P(col('#4A3410', a))); cv.drawRect(skia.Rect(-s * 0.03, s * 0.1, s * 0.03, s * 0.3), P(col('#4A3410', a)))
    cv.restore()

def story_box(cv, x, y, s, a, t, open_=0.0, lock=0.0, glow=0.0, c=GOLD, show_lock=True):
    """kotak cerita emas: tutup terbuka ke belakang (open_ 0..1) + pancaran cahaya dari dalam, gembok di depan"""
    if a <= 0: return
    w, h = s, s * 0.62; ly = y - h / 2; o = eo(open_)
    if o > 0:
        beam = skia.Path(); beam.moveTo(x - w * 0.42, ly); beam.lineTo(x + w * 0.42, ly); beam.lineTo(x + w * 1.0, ly - 360); beam.lineTo(x - w * 1.0, ly - 360); beam.close()
        cv.drawPath(beam, P(shader=lg(0, ly, 0, ly - 360, [col(mixc(c, '#FFFFFF', 0.5), 0.55 * a * o), col(c, 0.18 * a * o), col(c, 0)], [0, 0.5, 1])))
        rays(cv, x, ly, s * 1.2 * o, 0.45 * a * o, t, n=12, c=c, spin=5)
        bl_ = h * 0.62 * o
        back = skia.Rect(x - w / 2 + 4, ly - bl_, x + w / 2 - 4, ly)
        cv.drawRoundRect(back, 8, 8, P(shader=lg(0, back.top(), 0, back.bottom(), [col(mixc(c, '#000000', 0.15), a), col(mixc(c, '#000000', 0.55), a)])))
        cv.drawRoundRect(back, 8, 8, P(col('#FFF1D0', 0.5 * a), stroke=2))
    if glow > 0: cv.drawRoundRect(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 14, 14, P(col(c, 0.5 * glow * a), blur=24))
    r = skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    cv.drawRoundRect(r.makeOffset(4, 12), 12, 12, P(col('#000000', 0.45 * a), blur=12))
    cv.drawRoundRect(r, 12, 12, P(shader=lg(0, r.top(), 0, r.bottom(), [col(mixc(c, '#FFFFFF', 0.25), a), col(c, a), col(mixc(c, '#000000', 0.45), a)], [0, 0.4, 1])))
    for bx in (x - w * 0.3, x + w * 0.3): cv.drawRect(skia.Rect(bx - w * 0.04, r.top(), bx + w * 0.04, r.bottom()), P(col(mixc(c, '#000000', 0.35), 0.7 * a)))
    cv.drawRoundRect(r, 12, 12, P(col('#FFF1D0', 0.5 * a), stroke=2))
    if o > 0: cv.drawOval(skia.Rect(x - w * 0.42, ly - 8, x + w * 0.42, ly + 8), P(col('#FFF6D8', 0.9 * a * o), blur=6))
    if o < 1:
        lh = h * 0.42; la = a * (1 - o)
        lid = skia.Path(); lid.moveTo(x - w / 2 - 6, ly); lid.lineTo(x - w / 2 + 6, ly - lh); lid.lineTo(x + w / 2 - 6, ly - lh); lid.lineTo(x + w / 2 + 6, ly); lid.close()
        cv.save(); cv.translate(0, -40 * o)
        cv.drawPath(lid, P(shader=lg(0, ly - lh, 0, ly, [col(mixc(c, '#FFFFFF', 0.45), la), col(mixc(c, '#000000', 0.25), la)])))
        cv.drawPath(lid, P(col('#FFF1D0', 0.5 * la), stroke=2)); cv.restore()
    if show_lock and lock < 1: padlock(cv, x, y + h * 0.05, s * 0.28, a * (1 - prog(lock, 0.7, 1.0)), lock, '#E8E6F0')

def call_frame(cv, cx, cy, w, h, a, c=ACC_L):
    """bingkai video call kaca"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    glass(cv, r, rad=24, a=0.8 * a, glow=0.15, gc=c, fill=('#1E1F3C', '#111226'))
    cv.drawCircle(r.left() + 22, r.top() + 22, 7, P(col(CORAL, a)))
    mono(cv, 'LIVE', r.left() + 36, r.top() + 22, 14, ACC_L, a, sp=2, align=0)

def race_bar(cv, x0, x1, y, v, a, c, label):
    if a <= 0: return
    mono(cv, label, x0, y - 30, 20, c, a, sp=2, align=0)
    cv.drawRoundRect(skia.Rect(x0, y - 14, x1, y + 14), 14, 14, P(col('#1A1B30', 0.95 * a)))
    xv = x0 + (x1 - x0) * clamp(v)
    if xv > x0 + 24:
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 10, xv - 4, y + 10), 10, 10, P(col(c, 0.5 * a), blur=10))
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 10, xv - 4, y + 10), 10, 10, P(shader=lg(x0, 0, x1, 0, [col(mixc(c, '#FFFFFF', 0.4), a), col(c, a)])))

def fly_orb(cv, t, t0, dur, x0, y0, x1, y1, a, c=GOLD, lift=160, r=16):
    u = prog(t, t0, t0 + dur)
    if not (0 < u < 1): return
    x = lerp(x0, x1, eio(u)); y = lerp(y0, y1, eio(u)) - lift * math.sin(u * math.pi)
    for k in range(5):
        uu = max(0.0, u - k * 0.04); xx = lerp(x0, x1, eio(uu)); yy = lerp(y0, y1, eio(uu)) - lift * math.sin(uu * math.pi)
        cv.drawCircle(xx, yy, r * (1 - k * 0.15), P(col(c, 0.25 * (1 - k / 5) * a), blur=6))
    orb(cv, x, y, r, a * bump(u) * 1.3 if u > 0.85 or u < 0.15 else a, c)

# ------------------------------------------------------------ A: HOOK — mau dia terbuka? coba ini: cerita duluan (0 - 3.05)
def gA(cv, t):
    zin = eo(prog(t, 0.0, 0.6)); push = lerp(1.1, 1.0, zin)
    cv.save(); cv.translate(540, 900); cv.scale(push, push); cv.translate(-540, -900)
    cafe_bg(cv, 1.0, t)
    lo = prog(t, 2.05, 2.5); ru = prog(t, 2.6, 2.9); ro = prog(t, 2.8, 3.05)
    two_chat(cv, t, 1.0, lmood='excited' if lo > 0.3 else 'worried', rmood='happy' if ru > 0.5 else 'neutral', lglow=0.6 * lo, rglow=0.6 * ro, lc=GOLD, rc=HOTPINK, ltrem=0.0 if lo > 0 else 0.3)
    table(cv, 540, 1010, 460, 1.0, t, cups=False)
    story_box(cv, 425, 950, 160, 1.0, t, open_=lo, lock=prog(t, 1.6, 2.05), glow=0.6 * prog(t, 1.42, 1.8))
    story_box(cv, 655, 950, 160, 1.0, t, open_=ro * 0.8, lock=ru, glow=0.6 * ru, c='#FF9AD0')
    cv.restore()
    for txt, x, y, rot, t0 in (('. . .', 300, 560, -4, -0.3), ('. . .', 780, 600, 4, 0.3)):
        q = prog(t, t0, t0 + 0.25)
        if q > 0:
            cv.save(); cv.translate(x, y + 5 * math.sin(t * 3 + x)); cv.rotate(rot)
            chip(cv, txt, 0, 0, clamp(q * 3) * (1 - eio(prog(t, 1.8, 2.05))), size=30, fg=MUTED, bgc='#1C1D30', edge='#4A4D68'); cv.restore()
    if lo > 0:
        u = eo(lo); orb(cv, 425, lerp(880, 620, u), 28, clamp(lo * 3))
        cv.save(); cv.translate(330, 520); sc = lerp(0.6, 1, bo(lo)); cv.scale(sc, sc)
        say(cv, 'aku dulu takut gelap', 0, 0, 32, clamp(lo * 3), GOLD, ('#3A2A10', '#1E1608'), '#FFE3B0', (40, 110), 1.0, 0.9); cv.restore()
    v = 0.12 + 0.02 * math.sin(t * 3) + 0.6 * eo(prog(t, 2.5, 3.05))
    conn_meter(cv, 240, 840, 1150, v, eo(prog(t, -0.2, 0.2)), t, label='SALING SUKA')

# ------------------------------------------------------------ B: kita sering nunggu orang lain buka diri duluan, akhirnya diem (3.05 - 7.27)
def gB(cv, t):
    a0 = eo(prog(t, 3.05, 3.4))
    cafe_bg(cv, a0 * 0.6, t)
    two_chat(cv, t, a0, lmood='worried', rmood='worried', ltrem=0.2)
    table(cv, 540, 1010, 460, a0, t, cups=False)
    sh = 3 * math.sin(t * 30) * prog(t, 4.0, 4.3)
    story_box(cv, 425 + sh, 950, 160, a0, t); story_box(cv, 655 - sh, 950, 160, a0, t, c='#FF9AD0')
    for txt, x, y, rot, t0 in (('kamu duluan deh', 290, 520, -5, 3.6), ('kamu aja duluan', 790, 560, 5, 4.2)):
        q = prog(t, t0, t0 + 0.25)
        if q > 0:
            cv.save(); cv.translate(x, y); cv.rotate(rot); sc = lerp(1.4, 1, eo(q)); cv.scale(sc, sc)
            chip(cv, txt, 0, 0, a0 * clamp(q * 3), size=28, fg='#FFD9D2', bgc='#2A1420', edge=CORAL); cv.restore()
    da = prog(t, 5.33, 5.6)
    if da > 0:
        cv.save(); cv.translate(540, 380); sc = lerp(1.6, 1, eo(da)); cv.scale(sc, sc)
        extrude(cv, 'DIEM-DIEMAN', 0, 0, 80, a0 * clamp(da * 3), depth=10, front=('#FFFFFF', '#C9CBE0'), side='#2E3270'); cv.restore()
        for k, (x, y) in enumerate(((300, 630), (780, 650))): chip(cv, 'krik...', x, y, a0 * prog(t, 5.6 + 0.3 * k, 5.9 + 0.3 * k), size=26, fg=MUTED, bgc='#1C1D30', edge='#4A4D68')
    conn_meter(cv, 240, 840, 1150, 0.12 - 0.06 * prog(t, 5.33, 6.2), a0, t, label='SALING SUKA')

# ------------------------------------------------------------ C: 2013, Susan Sprecher: dua orang asing ngobrol lewat video call (7.27 - 13.25)
def gC(cv, t):
    research_card(cv, t, 7.3, '2013', 'Sprecher dkk.', 'Journal of Experimental Social Psychology', None, None, 600, tag='JESP')
    va = eo(prog(t, 9.91, 10.4))
    if va > 0:
        for k, x in enumerate((370, 710)):
            pa = eo(prog(t, 9.95 + k * 0.15, 10.35 + k * 0.15))
            call_frame(cv, x, 1040, 250, 170, va * pa, GOLD if k == 0 else HOTPINK)
            hero(cv, x, 1110, 120, 'neutral', va * pa, t)
        mono(cv, 'VIDEO CALL · 12 MENIT', 540, 930, 22, ACC_L, va, sp=3)

# ------------------------------------------------------------ D: gantian bolak-balik vs satu arah (13.25 - 18.55)
def gD(cv, t):
    a0 = eo(prog(t, 13.25, 13.6))
    rows = ((620, 'GANTIAN', GOLD, True, 13.4), (960, 'SATU ARAH', '#7FB8FF', False, 15.67))
    for y, lab, c, recip, t1 in rows:
        pa = eo(prog(t, 13.3, 13.7)) if recip else max(0.45 * eo(prog(t, 13.4, 13.8)), eo(prog(t, 15.5, 15.9)))
        mono(cv, lab, 120, y - 150, 26, c, a0 * pa, sp=4, align=0, glow=0.4)
        for k, x in enumerate((330, 750)):
            call_frame(cv, x, y, 260, 230, a0 * pa, c)
            listening = (not recip) and k == 1
            hero(cv, x, y + 105, 170, 'neutral' if listening else 'happy', a0 * pa, t, mouth_open=0.4)
        if recip:
            for j in range(6):
                t0 = 13.6 + j * 0.75; lr = j % 2 == 0
                fly_orb(cv, t, t0, 0.65, 380 if lr else 700, y - 30, 700 if lr else 380, y - 30, a0 * pa, GOLD if lr else '#FF9AD0', lift=110, r=20)
        else:
            for j in range(4):
                t0 = 15.8 + j * 0.6
                fly_orb(cv, t, t0, 0.55, 380, y - 30, 700, y - 30, a0 * pa, '#7FB8FF', lift=70, r=16)
            la = prog(t, 17.17, 17.5)
            if la > 0: chip(cv, 'cuma dengerin...', 750, y - 160, a0 * la, size=24, fg=MUTED, bgc='#1C1D30', edge='#4A4D68')

# ------------------------------------------------------------ E: yang gantian cerita lebih saling suka (18.55 - 21.34)
def gE(cv, t):
    a0 = eo(prog(t, 18.55, 18.9)); g = eo(prog(t, 20.24, 20.9))
    for k, (x, lab, val, c) in enumerate(((300, 'SATU ARAH', 0.4, '#7FB8FF'), (780, 'GANTIAN', 0.88, GOLD))):
        pa = eo(prog(t, 18.6 + k * 0.15, 19.0 + k * 0.15)); hi = eo(prog(t, 19.32, 19.7)) if k else 0.0
        mono(cv, lab, x, 380, 28, c, a0 * pa, sp=4, glow=0.3 + 0.4 * hi)
        glass_heart(cv, x, 580, 100, 0.15 + (val - 0.15) * g, a0 * pa, t, label='SALING SUKA', c=HOTPINK if k else '#7FB8FF', glow=0.8 * g * k)
        for s in (-1, 1): hero(cv, x + s * 80, 1080, 210, 'happy' if (k and g > 0.4) else 'neutral', a0 * pa, t, glow=0.5 * k * g, gc=GOLD)

# ------------------------------------------------------------ F: setelah tukar peran, yang satu arah tetap nggak bisa ngejar (21.34 - 25.15)
def gF(cv, t):
    a0 = eo(prog(t, 21.34, 21.7))
    sw = eo(prog(t, 21.6, 22.6))
    for s, c in ((-1, '#7FB8FF'), (1, '#7FB8FF')):
        x = 540 + s * lerp(200, -200, sw) * 1.0
        hero(cv, x, 860, 230, 'neutral', a0, t)
    loop_arrow(cv, 540, 700, 170, t, a0 * prog(t, 21.5, 21.8), '#7FB8FF', spin=200, sweep=300, w=6)
    ta = eo(prog(t, 21.6, 22.0))
    if ta > 0: chip(cv, 'TUKAR PERAN', 540, 420, a0 * ta, size=32, fg=INK, bgc='#7FB8FF', edge='#7FB8FF')
    ga = eo(prog(t, 22.4, 22.8)); g2 = eo(prog(t, 23.01, 24.2))
    race_bar(cv, 160, 920, 960, 0.88 * ga, a0 * ga, GOLD, 'GANTIAN')
    race_bar(cv, 160, 920, 1050, (0.25 + 0.33 * g2) * ga, a0 * ga, '#7FB8FF', 'SATU ARAH (setelah tukar peran)')
    if g2 > 0.6:
        x = 160 + 760 * 0.88
        cv.drawLine(x, 920, x, 1075, P(col(GOLD, 0.7 * a0), stroke=3))
        chip(cv, 'nggak bisa ngejar', 600, 1125, a0 * prog(g2, 0.6, 1.0), size=24, fg='#FFD9D2', bgc='#2A1420', edge=CORAL)

# ------------------------------------------------------------ G: cerita duluan = "aku percaya sama kamu"; orang cenderung membalas (25.15 - 30.39)
def gG(cv, t):
    a0 = eo(prog(t, 25.15, 25.5))
    cafe_bg(cv, a0 * 0.6, t)
    lo = prog(t, 25.4, 26.0); tr = prog(t, 27.45, 27.75); ru = prog(t, 28.91, 29.2); ro = prog(t, 29.1, 29.6)
    two_chat(cv, t, a0, lmood='happy', rmood='excited' if ru > 0.4 else 'neutral', lglow=0.5 * lo, rglow=0.7 * ru, rc=HOTPINK)
    table(cv, 540, 1010, 460, a0, t, cups=False)
    story_box(cv, 425, 950, 160, a0, t, open_=lo, lock=lo, glow=0.5 * lo)
    story_box(cv, 655, 950, 160, a0, t, open_=ro, lock=ru, glow=0.6 * ru, c='#FF9AD0')
    fly_orb(cv, t, 26.2, 1.0, 425, 860, 655, 860, a0, GOLD, lift=260, r=24)
    fly_orb(cv, t, 29.5, 0.8, 655, 860, 425, 860, a0, '#FF9AD0', lift=260, r=24)
    if tr > 0:
        cv.save(); cv.translate(320, 520); sc = lerp(1.6, 1, eo(tr)); cv.scale(sc, sc)
        say(cv, 'aku percaya sama kamu', 0, 0, 32, a0 * clamp(tr * 3), GOLD, ('#3A2A10', '#1E1608'), '#FFE3B0', (40, 110), 1.0, 0.9); cv.restore()
    if ru > 0:
        cv.save(); cv.translate(800, 420); sc = lerp(1.5, 1, eo(ru)); cv.scale(sc, sc)
        chip(cv, 'MEMBALAS', 0, 0, a0 * clamp(ru * 3), size=32, fg=INK, bgc=HOTPINK, edge=HOTPINK); cv.restore()
    conn_meter(cv, 240, 840, 1150, 0.2 + 0.3 * eo(tr) + 0.45 * eo(ru), a0, t, label='SALING SUKA')

# ------------------------------------------------------------ H: mulai dari hal kecil, tanya balik; cerita apa yang bikin akrab? (30.39 - 36.6)
CMTS = [('cerita takut kucing', 250, 420, 33.0), ('pernah salah naik bus', 830, 500, 33.25), ('aib masa kecil wkwk', 260, 580, 33.5), ('cerita soal keluarga', 820, 645, 33.75)]
def gH(cv, t):
    a0 = eo(prog(t, 30.39, 30.7))
    cafe_bg(cv, a0 * 0.7, t)
    two_chat(cv, t, a0, lmood='excited', rmood='excited', lglow=0.6, rglow=0.6)
    table(cv, 540, 1010, 460, a0, t, cups=False)
    story_box(cv, 425, 950, 160, a0, t, open_=1.0, lock=1.0, glow=0.5); story_box(cv, 655, 950, 160, a0, t, open_=1.0, lock=1.0, glow=0.5, c='#FF9AD0')
    ka = prog(t, 30.45, 30.75); fade = 1 - eio(prog(t, 32.7, 33.0))
    if ka > 0:
        cv.save(); cv.translate(540, 360); sc = lerp(1.5, 1, eo(ka)); cv.scale(sc, sc)
        extrude(cv, 'MULAI DARI HAL KECIL', 0, 0, 62, a0 * clamp(ka * 3) * fade, depth=9); cv.restore()
        q = prog(t, 30.8, 31.1)
        if q > 0: say(cv, 'aku dulu takut gelap', 330, 520, 30, a0 * clamp(q * 3) * fade, GOLD, ('#3A2A10', '#1E1608'), '#FFE3B0', (330, 640), lerp(0.6, 1, bo(q)), 0.8)
        q = prog(t, 31.68, 31.95)
        if q > 0: say(cv, 'kalau kamu?', 760, 600, 34, a0 * clamp(q * 3) * fade, HOTPINK, ('#3A1030', '#1E0818'), '#FFD9F0', (780, 700), lerp(0.6, 1, bo(q)), 0.9)
    for k, (txt, x, y, t0) in enumerate(CMTS):
        q = prog(t, t0, t0 + 0.3)
        if q > 0: comment(cv, txt, x, y, a0 * clamp(q * 2), lerp(0.7, 1, bo(q)), size=27, av=AV_COL[k], rot=(-4 if x < 540 else 4))
    conn_meter(cv, 240, 840, 1150, 0.92, a0, t, label='SALING SUKA')

# ------------------------------------------------------------ J: outro (36.6 - 42)
def gJ(cv, t):
    tt = t - 36.6; p_ = bo(prog(tt, 0.0, 0.6)); a = eo(prog(tt, 0.0, 0.4))
    halo(cv, 540, 640, 440, ACC, 0.8 * a); rays(cv, 540, 640, 500, 0.6 * a, t, n=18, spin=4)
    cv.save(); cv.translate(540, 640); cv.scale(p_, p_); cv.translate(-540, -640)
    cv.drawCircle(540, 640, 250, P(col(ACC, 0.2), blur=60))
    cv.save(); cv.translate(540 - 240, 640 - 240); cv.scale(0.48, 0.48); __import__('logo_rp').c4(cv); cv.restore()
    cv.restore()
    ta = eo(prog(tt, 0.4, 0.9))
    if ta > 0:
        layer(cv, ta); tracked(cv, 'RUANG PIKIR', 540, 960, font(XB, 60), P(col(TXT)), 10)
        f = font(B, 30); w = f.measureText('ruangpikir.id'); cv.drawString('ruangpikir.id', 540 - w / 2, bl(f, 1018), f, P(col(MUTED))); cv.restore()
    press = 1 - 0.08 * bump(prog(tt, 0.75, 1.0)); ba = prog(tt, 0.3, 0.7)
    if ba > 0:
        cv.save(); cv.translate(540, 1100); cv.scale(press, press); cv.translate(-540, -1100)
        cv.drawRoundRect(skia.Rect(430, 1062, 650, 1138), 38, 38, P(col(ACC, 0.45 * clamp(ba * 1.5)), blur=18))
        pill(cv, 'Follow', 540, 1100, ba, bgc='#A9B2FF', fg=INK, size=42); cv.restore()

b.DRAWERS = [gA, gB, gC, gD, gE, gF, gG, gH, gJ]

def build_sfx():
    ev = [(0.0, 'whoosh'), (0.02, 'plip'), (0.05, 'pop'), (0.32, 'plip'), (1.42, 'ding_soft'), (1.6, 'clunk'), (2.05, 'chop'), (2.08, 'shine'), (2.15, 'rise'), (2.6, 'clunk'), (2.8, 'shine'), (2.9, 'heart'), (3.05, 'whoosh'), (3.6, 'pop'), (4.0, 'clunk'), (4.2, 'pop'), (5.33, 'chop'), (5.36, 'stamp'), (5.6, 'plip'), (5.9, 'plip'), (7.27, 'whoosh'), (7.33, 'card'), (7.63, 'stamp'), (7.91, 'ding_soft'), (9.95, 'pop'), (10.1, 'pop'), (13.25, 'whoosh'), (13.6, 'swish'), (14.35, 'swish'), (15.1, 'swish'), (15.5, 'pop'), (15.8, 'swish'), (15.85, 'swish'), (16.4, 'swish'), (16.6, 'swish'), (17.0, 'swish'), (17.17, 'plip'), (17.35, 'swish'), (17.6, 'swish'), (18.55, 'whoosh'), (19.32, 'pop'), (20.24, 'rise'), (20.6, 'heart'), (21.34, 'whoosh'), (21.6, 'swish'), (22.4, 'rise'), (23.01, 'pop'), (24.0, 'buzzer'), (25.15, 'whoosh'), (25.4, 'clunk'), (25.6, 'shine'), (26.2, 'swish'), (27.45, 'ding'), (28.91, 'clunk'), (29.0, 'chop'), (29.15, 'shine'), (29.5, 'swish'), (29.9, 'heart'), (30.39, 'whoosh'), (30.45, 'stamp'), (30.8, 'pop'), (31.68, 'ding_soft'), (33.0, 'pop'), (33.25, 'pop'), (33.5, 'pop'), (33.75, 'pop'), (36.6, 'whoosh'), (36.75, 'boing'), (37.1, 'shine'), (37.35, 'pop')]
    return sorted(ev)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'preview':
        os.makedirs('preview', exist_ok=True); s = skia.Surface(W, H); cv = s.getCanvas()
        for ts in sys.argv[2:]:
            t = float(ts); cv.clear(skia.ColorBLACK); b.draw_frame(cv, t); s.makeImageSnapshot().save(f'preview/t{t:05.2f}.png', skia.kPNG)
    elif mode == 'timeline':
        WA, WO, LINES = b.build_warp(); b.WA, b.WO, b.VO_LINES = WA, WO, LINES; b.OUT_DUR = float(WO[-1])
        tl = {'out_dur': b.OUT_DUR, 'sfx': [(round(b.out_t(t), 4), k) for t, k in build_sfx()],
              'voice': [(round(b.out_t(l['anchor']) + 0.04, 4), l['file']) for l in LINES]}
        json.dump(tl, open(sys.argv[2], 'w'), indent=1); print('out_dur', b.OUT_DUR)
    elif mode == 'video':
        WA, WO, LINES = b.build_warp(); b.WA, b.WO, b.VO_LINES = WA, WO, LINES; b.OUT_DUR = float(WO[-1])
        n = int(round(b.OUT_DUR * FPS)); s = skia.Surface(W, H); cv = s.getCanvas()
        pr = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', sys.argv[2]], stdin=subprocess.PIPE)
        for fi in range(n):
            cv.clear(skia.ColorBLACK); b.draw_frame(cv, b.anim_t(fi / FPS)); pr.stdin.write(s.makeImageSnapshot().tobytes())
            if fi % 200 == 0: print('frame', fi, '/', n, flush=True)
        pr.stdin.close(); pr.wait()







