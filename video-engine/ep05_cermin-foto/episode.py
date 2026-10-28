#!/usr/bin/env python3
"""Ruang Pikir reel #5: 'Cakep di cermin, kok jelek di foto?' (efek paparan, Mita, Dermer & Knight 1977)
Gaya sinematik (seperti video acuan "Jam 2 pagi, kok overthinking?"): judul hanya di awal, tanpa tag, caption besar per frasa
tanpa kotak, ilustrasi besar-minimalis (bola 3D lembut, kartu kaca, kata besar, siluet garis), kamera bergerak halus.
python3 episode.py preview t1 t2 ... | timeline out.json | video out.mp4"""
import sys, os, math, json, subprocess, random
import skia
import base as b
from base import (clamp, lerp, prog, eo, ei, eio, bo, bump, col, P, lg, rg, layer, font, XB, B, M, MONO, bl, tracked, parse,
                 pill, sparkle, person, ACC, ACC_L, ACC_XL, TXT, MUTED, CORAL, MINT, W, H, FPS)

VIOLET, YELLOW, INK, HL = '#B57BFF', '#FFD23F', '#0B0C1E', '#AEB6FF'

# adegan (waktu animasi, DUR 42); tag tidak ditampilkan di gaya ini
b.GROUPS = [(0.0, 2.95, 'A'), (2.95, 5.75, 'B'), (5.75, 9.37, 'C'), (9.37, 13.43, 'D'), (13.43, 21.56, 'E'),
            (21.56, 25.24, 'F'), (25.24, 29.08, 'G'), (29.08, 32.59, 'H'), (32.59, 36.6, 'I'), (36.6, 42.0, 'J')]
# caption per frasa, disinkronkan ke jeda suara; [..] = kata kunci
PHRASES = [(0.15, 'Kamu [nggak jelek] di foto.'), (1.4, 'Kamu cuma [belum terbiasa].'),
           (2.95, 'Di [cermin] cakep,'), (3.8, 'tapi di [kamera belakang],'), (4.75, '[kok beda]?'),
           (5.75, 'Soalnya wajah kita [nggak simetris],'), (7.47, 'dan di cermin,'), (8.2, '[kiri jadi kanan].'),
           (9.37, 'Tahun [1977],'), (10.93, 'psikolog [Theodore Mita] mengujinya.'),
           (13.43, 'Peserta dikasih [dua foto] wajahnya:'), (15.1, 'versi [asli],'), (15.9, 'dan versi [cermin].'),
           (16.95, 'Hasilnya?'), (17.5, 'Mereka lebih suka [versi cermin].'), (19.05, 'Tapi teman-temannya'), (20.15, 'lebih suka [versi asli].'),
           (21.56, 'Ini [efek paparan]:'), (22.6, 'makin sering kita lihat sesuatu,'), (24.3, '[makin kita suka].'),
           (25.24, 'Kamu tiap hari lihat [versi cermin].'), (26.9, 'Temanmu tiap hari lihat [versi asli].'),
           (29.08, 'Jadi foto yang kamu [benci],'), (30.68, 'bisa jadi versi yang [orang lain suka].'),
           (32.59, 'Coba [balik fotomu] sekarang.'), (33.78, 'Mana yang lebih kamu suka?'), (35.15, 'Tulis di [komentar]!'),
           (36.6, 'Follow [Ruang Pikir],'), (37.75, 'biar makin kenal [isi kepalamu].')]
b.CAPS = [(t, s, '') for t, s in PHRASES]          # dipakai base hanya untuk jadwal

# ------------------------------------------------------------ chrome gaya sinematik
b.draw_tag = lambda cv, t: None
b.draw_progress = lambda cv, t: None
def draw_title(cv, t):
    a = eo(prog(t, 0.05, 0.35)) * (1 - eio(prog(t, 5.5, 6.0)))
    if a <= 0: return
    segs = parse("Cakep di cermin, [kok jelek di foto]?"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 232) + (1 - eo(prog(t, 0.05, 0.35))) * 16 - 10 * eio(prog(t, 5.5, 6.0))
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
        e = PHRASES[i + 1][0] - 0.2 if i + 1 < len(PHRASES) else 41.7
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


# ------------------------------------------------------------ helper EP05: potret asimetris, ponsel, cermin, foto polaroid
SKIN = ('#E4E6FF', '#A7AEF5', '#4E54B0')
def portrait(cv, cx, cy, s, a=1.0, mirror=False, mood='smile', t=0.0, glitch=0.0, ph=0.0, flipx=1.0):
    """potret bergaya (kotak lokal ±200 x ±260 pada s=1) yang sengaja tidak simetris: poni ke kanan, alis kanan lebih tinggi,
    tahi lalat di pipi kanan, anting di telinga kiri, senyum miring. mirror=True membalik kiri-kanan.
    flipx (−1..1) dipakai untuk animasi membalik (skala sumbu x)."""
    if a <= 0 or s <= 0: return
    cv.save(); cv.translate(cx, cy); cv.scale(s * flipx * (-1 if mirror else 1), s)
    if glitch > 0:
        for dx, c in ((-9, '#FF5A7A'), (9, '#5AC8FF')):
            cv.save(); cv.translate(dx * glitch, 0); layer(cv, 0.35 * glitch * a); _portrait_body(cv, 1.0, mood, t, ph, tint=c); cv.restore(); cv.restore()
    layer(cv, a); _portrait_body(cv, 1.0, mood, t, ph); cv.restore()
    cv.restore()

def _portrait_body(cv, a, mood, t, ph, tint=None):
    tc = (lambda c: tint) if tint else (lambda c: c)
    # bahu
    sh = skia.Path(); sh.moveTo(-205, 265); sh.cubicTo(-200, 175, -120, 150, -55, 140); sh.lineTo(55, 140); sh.cubicTo(120, 150, 200, 175, 205, 265); sh.close()
    cv.drawPath(sh, P(shader=lg(0, 140, 0, 265, [col(tc('#3A3E7A'), a), col(tc('#17183A'), a)])))
    cv.drawPath(sh, P(col(tc(ACC_L), 0.5 * a), stroke=3))
    cv.drawRect(skia.Rect(-38, 95, 38, 150), P(shader=lg(0, 95, 0, 150, [col(tc('#6E75D0'), a), col(tc('#4A4FA8'), a)])))
    # telinga + anting (hanya telinga kiri)
    for sx in (-1, 1):
        cv.drawOval(skia.Rect(sx * 138 - 22, -45, sx * 138 + 22, 25), P(shader=rg(sx * 138, -15, 40, [col(tc(SKIN[1]), a), col(tc(SKIN[2]), a)])))
    cv.drawCircle(-140, 38, 13, P(col(tc(YELLOW), 0.9 * a), stroke=4)); cv.drawCircle(-140, 52, 6, P(col(tc('#FFE58A'), a)))
    # kepala
    hr = skia.Rect(-138, -175, 138, 120); hp = skia.Path(); hp.addOval(hr)
    cv.drawOval(hr.makeOffset(0, 10), P(col('#000000', 0.35 * a), blur=18))
    cv.drawOval(hr, P(shader=rg(-45, -95, 290, [col(tc(SKIN[0]), a), col(tc(SKIN[1]), a), col(tc(SKIN[2]), a)], [0, 0.55, 1])))
    cv.save(); cv.clipPath(hp, skia.ClipOp.kIntersect, True)
    cv.drawOval(skia.Rect(40, -120, 190, 140), P(col(tc('#2A2E7A'), 0.28 * a), blur=30))
    cv.restore()
    cv.drawOval(hr, P(col(tc(ACC_XL), 0.55 * a), stroke=2.5))
    # pipi merona
    for sx in (-1, 1): cv.drawOval(skia.Rect(sx * 72 - 30, 22, sx * 72 + 30, 48), P(col(tc('#FF8FB0'), 0.35 * a), blur=10))
    # alis: kanan lebih tinggi
    for sx, yb, tilt in ((-1, -62, 4), (1, -76, -6)):
        br = skia.Path(); br.moveTo(sx * 30, yb + 6); br.quadTo(sx * 58, yb - 8 + tilt * 0.2, sx * 88, yb + tilt); cv.drawPath(br, P(col(tc('#1E1F48'), a), stroke=9))
    # mata (berkedip)
    bk = blink_at(t, ph)
    for sx in (-1, 1):
        ex, ey = sx * 58, -30; eh = 15 * (1 - 0.92 * bk)
        e = skia.Path(); e.moveTo(ex - 26, ey); e.quadTo(ex, ey - eh * 1.6, ex + 26, ey); e.quadTo(ex, ey + eh * 1.3, ex - 26, ey); e.close()
        cv.drawPath(e, P(col(tc('#F4F5FF'), a)))
        if bk < 0.6:
            cv.save(); cv.clipPath(e, skia.ClipOp.kIntersect, True)
            cv.drawCircle(ex + 2, ey, 12, P(shader=rg(ex + 2, ey, 12, [col(tc('#7F8CFF'), a), col(tc('#262A6E'), a)])))
            cv.drawCircle(ex + 2, ey, 5.5, P(col(INK, a))); cv.drawCircle(ex - 2, ey - 4, 3, P(col('#FFFFFF', a)))
            cv.restore()
        cv.drawPath(e, P(col(tc('#1E1F48'), 0.8 * a), stroke=2.5))
    # hidung
    n = skia.Path(); n.moveTo(4, -10); n.quadTo(12, 28, -6, 34); cv.drawPath(n, P(col(tc('#5A60B8'), 0.8 * a), stroke=4))
    # tahi lalat di pipi kanan
    cv.drawCircle(64, 50, 6, P(col(tc('#262A5E'), a)))
    # mulut: senyum miring (sudut kanan lebih tinggi)
    m = skia.Path()
    if mood == 'smile':
        m.moveTo(-46, 66); m.quadTo(-5, 104, 50, 58); m.quadTo(0, 84, -46, 66); m.close()
        cv.drawPath(m, P(col(tc('#2A1E4E'), a))); cv.drawPath(m, P(col(tc('#2A1E4E'), a), stroke=4))
    else:
        m.moveTo(-36, 76); m.quadTo(0, 80, 40, 70); cv.drawPath(m, P(col(tc('#2A1E4E'), a), stroke=6))
    # rambut: poni menyapu ke kanan (asimetris)
    hair = skia.Path(); hair.moveTo(-150, -10); hair.cubicTo(-175, -150, -95, -235, 5, -232); hair.cubicTo(110, -230, 175, -160, 150, -20)
    hair.cubicTo(140, -90, 120, -120, 95, -128); hair.cubicTo(60, -70, 0, -80, -40, -112); hair.cubicTo(-85, -95, -120, -80, -150, -10); hair.close()
    cv.drawPath(hair, P(shader=lg(0, -235, 0, -10, [col(tc('#2C2F6E'), a), col(tc('#121332'), a)])))
    hl = skia.Path(); hl.moveTo(-90, -190); hl.quadTo(-10, -225, 70, -195); cv.drawPath(hl, P(col(tc('#8C93FF'), 0.45 * a), stroke=8, blur=3))
    cv.drawPath(hair, P(col(tc(ACC_L), 0.45 * a), stroke=2.5))

def phone(cv, cx, cy, w, h, a=1.0, content=None, ui='camera', t=0.0, flash=0.0):
    """ponsel kaca; content(cv) menggambar isi layar (sudah di-clip)"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); rad = w * 0.13
    cv.drawRoundRect(r.makeOffset(0, 26), rad, rad, P(col('#000000', 0.6 * a), blur=30))
    cv.drawRoundRect(r, rad, rad, P(col(ACC, 0.35 * a), stroke=14, blur=20))
    cv.drawRoundRect(r, rad, rad, P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col('#3A3E66', a), col('#14152A', a)])))
    sc = r.makeInset(w * 0.045, w * 0.045); srad = rad * 0.8
    sp = skia.Path(); sp.addRRect(skia.RRect.MakeRectXY(sc, srad, srad))
    cv.save(); cv.clipPath(sp, skia.ClipOp.kIntersect, True)
    cv.drawRect(sc, P(shader=rg(cx, cy - h * 0.1, h * 0.7, [col('#2A2F66', a), col('#0C0D1C', a)])))
    if content: content(cv)
    if ui == 'camera':
        for (x, y, dx, dy) in ((sc.left() + 30, sc.top() + 90, 1, 1), (sc.right() - 30, sc.top() + 90, -1, 1), (sc.left() + 30, sc.bottom() - 150, 1, -1), (sc.right() - 30, sc.bottom() - 150, -1, -1)):
            br = skia.Path(); br.moveTo(x, y + dy * 34); br.lineTo(x, y); br.lineTo(x + dx * 34, y); cv.drawPath(br, P(col('#FFFFFF', 0.75 * a), stroke=4))
        cv.drawCircle(cx, sc.bottom() - 70, 34, P(col('#FFFFFF', 0.9 * a), stroke=6)); cv.drawCircle(cx, sc.bottom() - 70, 25, P(col('#FFFFFF', 0.85 * a)))
    if flash > 0: cv.drawRect(sc, P(col('#FFFFFF', flash * a)))
    cv.drawRect(skia.Rect(sc.left(), sc.top(), sc.right(), sc.top() + sc.height() * 0.35), P(shader=lg(0, sc.top(), 0, sc.top() + sc.height() * 0.35, [col('#FFFFFF', 0.07 * a), col('#FFFFFF', 0)])))
    cv.restore()
    cv.drawRoundRect(skia.Rect(cx - w * 0.16, sc.top() + 14, cx + w * 0.16, sc.top() + 40), 13, 13, P(col('#05050A', a)))
    cv.drawRoundRect(r, rad, rad, P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col(ACC_XL, 0.8 * a), col(ACC, 0.3 * a), col(ACC, 0.1 * a)], [0, 0.5, 1]), stroke=3))

def mirror_frame(cv, cx, cy, w, h, a=1.0, content=None, t=0.0):
    """cermin oval berbingkai kaca dengan kilau"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); op = skia.Path(); op.addOval(r)
    cv.drawOval(r.makeOffset(0, 24), P(col('#000000', 0.55 * a), blur=28))
    cv.drawOval(r.makeOutset(16, 16), P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col('#C9CEFF', a), col('#5A60C8', a), col('#E3E6FF', a)], [0, 0.5, 1])))
    cv.drawOval(r.makeOutset(16, 16), P(col(ACC, 0.45 * a), stroke=10, blur=14))
    cv.save(); cv.clipPath(op, skia.ClipOp.kIntersect, True)
    cv.drawRect(r, P(shader=rg(cx, cy - h * 0.1, h * 0.8, [col('#3A4088', a), col('#14163A', a)])))
    if content: content(cv)
    u = (t * 0.35) % 1.0; x = lerp(r.left() - w * 0.6, r.right() + w * 0.6, u)
    cv.drawRect(r, P(shader=lg(x - 60, r.top(), x + 60, r.bottom(), [col('#FFFFFF', 0), col('#FFFFFF', 0.22 * a), col('#FFFFFF', 0)])))
    cv.drawOval(skia.Rect(r.left() + w * 0.1, r.top() + h * 0.06, r.left() + w * 0.45, r.top() + h * 0.3), P(col('#FFFFFF', 0.12 * a), blur=18))
    cv.restore()
    cv.drawOval(r, P(col('#FFFFFF', 0.5 * a), stroke=3))

def polaroid(cv, cx, cy, w, h, a=1.0, rot=0.0, content=None, label='', lc=TXT, glow=0.0, gc=ACC):
    if a <= 0: return
    cv.save(); cv.translate(cx, cy); cv.rotate(rot)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    if glow > 0: cv.drawRoundRect(r, 22, 22, P(col(gc, 0.6 * glow * a), stroke=18, blur=26))
    cv.drawRoundRect(r.makeOffset(0, 22), 22, 22, P(col('#000000', 0.55 * a), blur=24))
    cv.drawRoundRect(r, 22, 22, P(shader=lg(0, -h / 2, 0, h / 2, [col('#F2F2FA', a), col('#C9CCE6', a)])))
    ph = skia.Rect(-w / 2 + 18, -h / 2 + 18, w / 2 - 18, h / 2 - 78); pp = skia.Path(); pp.addRoundRect(ph, 12, 12)
    cv.save(); cv.clipPath(pp, skia.ClipOp.kIntersect, True)
    cv.drawRect(ph, P(shader=rg(0, -h * 0.15, h * 0.7, [col('#3A4088', a), col('#14163A', a)])))
    if content: content(cv)
    cv.restore()
    f = font(XB, 34); tw = f.measureText(label); cv.drawString(label, -tw / 2, bl(f, h / 2 - 40), f, P(col(lc, a)))
    cv.restore()

def heart_fly(cv, x0, y0, x1, y1, u, a=1.0, s=22, c=CORAL):
    if u <= 0 or u >= 1 or a <= 0: return
    x = lerp(x0, x1, eio(u)); y = lerp(y0, y1, eio(u)) - math.sin(math.pi * u) * 120
    cv.drawPath(heart_path(x, y, s * 1.3), P(col(c, 0.45 * a), blur=10)); cv.drawPath(heart_path(x, y, s), P(col(c, a)))

def flip_state(t, flips, dur=0.16):
    """jumlah flip yang sudah lewat + skala x animasi (cos) di sekitar tiap flip"""
    n = sum(1 for f in flips if t >= f + dur / 2); fx = 1.0
    for f in flips:
        if f <= t < f + dur: fx = max(0.04, abs(math.cos(math.pi * (t - f) / dur)))
    return n, fx

def ui_editor(cv, cx, sc_bottom, t, tap=0.0, a=1.0):
    y = sc_bottom - 78
    cv.drawRoundRect(skia.Rect(cx - 150, y - 44, cx + 150, y + 44), 44, 44, P(col('#0C0D1C', 0.85 * a)))
    if tap > 0: cv.drawCircle(cx - 70, y, 30 + 50 * tap, P(col(ACC_L, 0.5 * (1 - tap) * a), stroke=4))
    cv.drawCircle(cx - 70, y, 30, P(shader=lg(0, y - 30, 0, y + 30, [col('#A9B2FF', a), col(ACC, a)])))
    for s in (-1, 1):
        ar = skia.Path(); ar.moveTo(cx - 70 - 14 * s, y - 8 * s); ar.lineTo(cx - 70 + 14 * s, y - 8 * s); ar.lineTo(cx - 70 + 6 * s, y - 15 * s)
        cv.drawPath(ar, P(col(INK, a), stroke=4))
    f = font(XB, 30); cv.drawString('Balik', cx - 25, bl(f, y), f, P(col(TXT, a)))

# ------------------------------------------------------------ A: HOOK — jepret, lalu wajah bolak-balik cermin <-> foto (0 - 2.95)
A_FLIPS = [0.45, 0.95, 1.3, 1.6, 1.86]
def gA(cv, t):
    a = eo(prog(t, 0.0, 0.18)); punch = 1 + 0.07 * (1 - eo(prog(t, 0.22, 0.6)))
    n, fx = flip_state(t, A_FLIPS); mir = n % 2 == 0
    last = max([f for f in A_FLIPS if f <= t], default=-9)
    gl = (0.9 * (1 - prog(t, last + 0.08, last + 0.45))) if not mir else 0.0
    cv.save(); cv.translate(540, 700); cv.scale(punch, punch); cv.translate(-540, -700)
    halo(cv, 540, 700, 480, ACC if mir else CORAL, 0.55 * a)
    flash = bump(prog(t, 0.2, 0.5))
    phone(cv, 540, 700, 400, 720, a, content=lambda c: portrait(c, 540, 690, 0.82, a, mirror=mir, mood='smile' if mir else 'flat', t=t, glitch=gl, flipx=fx),
          ui='camera', t=t, flash=0.9 * flash)
    cv.restore()
    lab, c = ('CERMIN', MINT) if mir else ('FOTO', CORAL)
    pop = bo(prog(t, max(last + 0.08, 0.05), max(last + 0.08, 0.05) + 0.2))
    cv.save(); cv.translate(540, 448); cv.scale(0.7 + 0.3 * pop, 0.7 + 0.3 * pop)
    chip(cv, lab, 0, 0, a, size=26, f=MONO, fg=c, edge=c, bgc='#15162A'); cv.restore()
    if flash > 0: cv.drawCircle(540, 700, 620, P(shader=rg(540, 700, 620, [col('#FFFFFF', 0.55 * flash), col('#FFFFFF', 0)])))

# ------------------------------------------------------------ B: cermin cakep vs kamera belakang (2.95 - 5.75)
def gB(cv, t):
    ma = eo(prog(t, 3.0, 3.45)); pa = eo(prog(t, 3.8, 4.25))
    cv.save(); cv.translate(-(1 - ma) * 120, 0)
    if ma > 0:
        halo(cv, 300, 720, 330, MINT, 0.4 * ma)
        mirror_frame(cv, 300, 720, 330, 440, ma, content=lambda c: portrait(c, 300, 760, 0.74, ma, mirror=True, t=t, ph=0.2), t=t)
        for k, (dx, dy, r) in enumerate(((-170, -200, 16), (165, -150, 20), (-150, 170, 12), (175, 140, 14))):
            sparkle(cv, 300 + dx, 720 + dy, r * (0.7 + 0.3 * math.sin(t * 5 + k)), eo(prog(t, 3.3 + k * 0.08, 3.6 + k * 0.08)) * ma, c='#C7F7E4')
        check_mark(cv, 300 + 150, 720 - 225, 30, prog(t, 3.45, 3.9), ma)
        chip(cv, 'cermin', 300, 1010, ma, size=26, fg='#B9F5DF', bgc='#173A2E', edge=MINT)
    cv.restore()
    cv.save(); cv.translate((1 - pa) * 120, 0)
    if pa > 0:
        wob = 4 * math.sin(t * 14) * prog(t, 4.75, 5.0) * (1 - prog(t, 5.2, 5.5))
        phone(cv, 780 + wob, 720, 330, 590, pa, content=lambda c: portrait(c, 780 + wob, 700, 0.62, pa, mirror=False, mood='flat', t=t, glitch=0.35, ph=0.6), ui='camera', t=t)
        chip(cv, 'kamera belakang', 780, 1062, pa, size=26, fg='#FFC9BF', bgc='#3A2228', edge=CORAL)
        q = bo(prog(t, 4.75, 5.1))
        if q > 0:
            cv.save(); cv.translate(915, 455); cv.scale(q, q); cv.rotate(10 * math.sin(t * 3))
            glow_text(cv, '?', 0, 0, font(XB, 110), TXT, 1, glow=0.8, gc=CORAL, shader=lg(0, -55, 0, 55, [col('#FFFFFF'), col(CORAL)])); cv.restore()
    cv.restore()

# ------------------------------------------------------------ C: wajah nggak simetris, cermin membalik kiri-kanan (5.75 - 9.37)
MARKS = [(64, 50, 'tahi lalat'), (58, -82, 'alis'), (95, -150, 'poni'), (-140, 45, 'anting')]
def gC(cv, t):
    a = eo(prog(t, 5.8, 6.2)); s = 1.15; cx, cy = 540, 715
    fl = prog(t, 8.2, 8.75); fx = math.cos(math.pi * eio(fl))       # 1 -> -1 (membalik)
    halo(cv, cx, cy, 460, ACC, 0.5 * a)
    la = eo(prog(t, 5.95, 6.3)) * a
    if la > 0:
        cv.drawLine(cx, 380, cx, 380 + 700 * la, P(col(ACC_XL, 0.8 * la), stroke=3, effect=skia.DashPathEffect.Make([16, 12], -t * 40)))
    portrait(cv, cx, cy, s, a, mirror=False, t=t, ph=0.35, flipx=fx)
    for k, (mx, my, lab) in enumerate(MARKS):
        p_ = prog(t, 6.2 + k * 0.3, 6.5 + k * 0.3)
        if p_ <= 0: continue
        x, y = cx + mx * s * fx, cy + my * s
        cv.drawCircle(x, y, 26, P(col(CORAL, 0.5 * a), stroke=10, blur=8)); cv.drawCircle(x, y, 26 * (0.6 + 0.4 * bo(p_)), P(col('#FFC9BF', a), stroke=3.5))
        side = 1 if mx * fx > 0 else -1
        lx = min(max(x + side * 150, 140), 940)
        chip(cv, lab, lx, y - 36, eo(p_) * a * (1 - 0.6 * bump(fl)), size=24, fg='#FFC9BF', bgc='#3A2228', edge=CORAL)
    ar = eo(prog(t, 8.15, 8.5)) * a
    if ar > 0:
        for sgn in (-1, 1):
            p = skia.Path(); p.addArc(skia.Rect(cx - 330, cy - 330, cx + 330, cy + 330), (-60 if sgn > 0 else 120), 60 * ar)
            cv.drawPath(p, P(col(HL, 0.4 * ar), stroke=12, blur=8)); cv.drawPath(p, P(col(HL, ar), stroke=5))
        chip(cv, 'kiri  ⟷  kanan' if False else 'kiri jadi kanan', cx, 1075, ar, size=28, fg=ACC_XL)

# ------------------------------------------------------------ D: riset 1977 (9.37 - 13.43)
def gD(cv, t):
    ent = prog(t, 9.42, 10.0); a = clamp(ent * 2)
    rays(cv, 540, 700, 620, 0.45 * a, t, n=12, spin=3)
    cv.save(); cv.translate(540, 700); s = 0.88 + 0.12 * bo(ent); cv.scale(s, s); cv.translate(-540, -700)
    r = skia.Rect(170, 410, 910, 990); pth = glass(cv, r, 46, a, glow=0.35, fill=('#24264A', '#111226'))
    sheen(cv, pth, r, prog(t, 10.0, 10.9))
    tracked(cv, 'RISET', 540, 490, font(MONO, 26), P(col(HL, a)), 10)
    glow_text(cv, '1977', 540, 640, font(XB, 210), a=a, glow=0.55, shader=lg(0, 560, 0, 720, [col('#FFFFFF', a), col('#B9BFFF', a)]))
    na = eo(prog(t, 10.93, 11.3)) * a
    glow_text(cv, 'Mita, Dermer & Knight', 540, 790, font(XB, 44), TXT, na)
    glow_text(cv, 'J. Personality & Social Psychology', 540, 842, font(M, 25), MUTED, eo(prog(t, 11.1, 11.5)) * a)
    chip(cv, 'foto asli vs foto cermin', 540, 920, eo(prog(t, 11.6, 11.95)) * a, size=26)
    cv.restore()

# ------------------------------------------------------------ E: dua foto + siapa suka yang mana (13.43 - 21.56)
FRIENDS = [(720, 1100, 44), (830, 1085, 48), (940, 1102, 42)]
def gE(cv, t):
    for i, (x, rot, lab, mir, t0, hl_t, c) in enumerate(((330, -4, 'ASLI', False, 13.5, 15.1, ACC_L), (750, 4, 'CERMIN', True, 13.8, 15.9, MINT))):
        p_ = prog(t, t0, t0 + 0.55)
        if p_ <= 0: continue
        y = 700 - (1 - bo(p_)) * 160
        hl = bump(prog(t, hl_t, hl_t + 0.8)) * 0.8
        win = eo(prog(t, 18.2, 18.6)) if mir else eo(prog(t, 20.9, 21.3))
        polaroid(cv, x, y, 360, 450, clamp(p_ * 2), rot=rot, label=lab, lc='#2A2E6E' if not win else ('#0E4A3A' if mir else '#3A2E9E'),
                 content=lambda cc, m=mir, xx=x: portrait(cc, 0, -40, 0.62, 1, mirror=m, t=t, ph=0.3 + 0.4 * m), glow=max(hl, win), gc=c)
        if win > 0:
            n_h = 1 if mir else 3
            for k in range(n_h):
                hx = x + 120 - k * 52; hy = y - 230 - (k % 2) * 10; hs = 24 * bo(prog(t, (18.2 if mir else 20.9) + k * 0.12, (18.5 if mir else 21.2) + k * 0.12))
                if hs > 0: cv.drawPath(heart_path(hx, hy, hs * 1.3), P(col(CORAL, 0.45), blur=10)); cv.drawPath(heart_path(hx, hy, hs), P(col(CORAL)))
    # kamu -> cermin
    ka = eo(prog(t, 17.0, 17.4))
    if ka > 0:
        sphere(cv, 250, 1095, 48, BLUE, ka, glow=0.5); face(cv, 250, 1095, 48, 'happy', ka, t, 0.2)
        chip(cv, 'kamu', 250, 1172, ka, size=22, fg=ACC_XL)
        heart_fly(cv, 250, 1040, 750, 560, prog(t, 17.5, 18.2), ka, s=26)
    # teman-teman -> asli
    for k, (fx, fy, fr) in enumerate(FRIENDS):
        fa = eo(prog(t, 19.05 + k * 0.12, 19.4 + k * 0.12))
        if fa <= 0: continue
        sphere(cv, fx, fy, fr, tri(0.0, 0.0) if k != 1 else (mixc(BLUE[0], VIOLET, 0.5), VIOLET, '#3A1E70'), fa, glow=0.4); face(cv, fx, fy, fr, 'happy', fa, t, 0.4 + k * 0.3)
        heart_fly(cv, fx, fy - 50, 330, 560, prog(t, 20.15 + k * 0.15, 20.85 + k * 0.15), fa, s=22)
    chip(cv, 'teman-temanmu', 830, 1172, eo(prog(t, 19.3, 19.6)), size=22, fg=ACC_XL)

# ------------------------------------------------------------ F: efek paparan (21.56 - 25.24)
def gF(cv, t):
    a = eo(prog(t, 21.6, 22.0))
    cv.save(); cv.translate(540, 420); s = 0.7 + 0.3 * bo(prog(t, 21.6, 22.1)); cv.scale(s, s)
    glow_text(cv, 'efek paparan', 0, 0, font(XB, 92), TXT, a, glow=0.7, shader=lg(0, -46, 0, 46, [col('#FFFFFF', a), col(HL, a)]))
    cv.restore()
    for k in range(12):
        col_, row = k % 4, k // 4; x, y = 270 + col_ * 180, 600 + row * 150
        p_ = prog(t, 22.6 + k * 0.11, 22.9 + k * 0.11)
        if p_ <= 0: continue
        sc = bo(p_); cv.save(); cv.translate(x, y); cv.scale(sc, sc)
        cv.drawRoundRect(skia.Rect(-72, -66, 72, 66), 18, 18, P(col('#1C1E3A', 0.9 * a))); cv.drawRoundRect(skia.Rect(-72, -66, 72, 66), 18, 18, P(col(ACC, 0.5 * a), stroke=2))
        cv.save(); cv.clipRect(skia.Rect(-72, -66, 72, 66)); portrait(cv, 0, 6, 0.26, a, mirror=True, t=t + k * 0.37, ph=k * 0.13); cv.restore()
        cv.restore()
    hp = prog(t, 24.3, 24.8)
    if hp > 0:
        rays(cv, 540, 1075, 300, 0.7 * eo(hp) * a, t, n=14, c=CORAL)
        hs = 70 * bo(hp) * (1 + 0.06 * math.sin(t * 8))
        cv.drawPath(heart_path(540, 1075, hs * 1.35), P(col(CORAL, 0.5 * a), blur=24))
        cv.drawPath(heart_path(540, 1075, hs), P(shader=rg(520, 1050, hs * 1.6, [col('#FFC2B8', a), col(CORAL, a), col('#8A1F33', a)])))

# ------------------------------------------------------------ G: kamu lihat versi cermin, temanmu lihat versi asli (25.24 - 29.08)
def gG(cv, t):
    for i, (x0, x1, cx, lab, sub, t0, c) in enumerate(((80, 520, 300, 'KAMU', 'tiap hari: versi cermin', 25.3, MINT), (560, 1000, 780, 'TEMANMU', 'tiap hari: versi asli', 26.9, ACC_L))):
        pa = eo(prog(t, t0, t0 + 0.45))
        if pa <= 0: continue
        cv.save(); cv.translate(0, (1 - pa) * 50)
        r = skia.Rect(x0, 420, x1, 1095); glass(cv, r, 36, pa, glow=0.3 * pa, gc=c, edge=c)
        tracked(cv, lab, cx, 470, font(MONO, 24), P(col(c, pa)), 6)
        if i == 0:
            mirror_frame(cv, cx, 730, 260, 350, pa, content=lambda cc: portrait(cc, cx, 760, 0.58, pa, mirror=True, t=t, ph=0.2), t=t)
        else:
            polaroid(cv, cx, 720, 270, 340, pa, rot=3, content=lambda cc: portrait(cc, 0, -30, 0.46, 1, mirror=False, t=t, ph=0.5), label='ASLI', lc='#2A2E6E')
            sphere(cv, cx + 125, 900, 42, BLUE, pa, glow=0.4); face(cv, cx + 125, 900, 42, 'happy', pa, t, 0.7)
        chip(cv, sub, cx, 1035, pa, size=23, fg=ACC_XL if i else '#B9F5DF', bgc='#262842' if i else '#173A2E', edge=c)
        cv.restore()

# ------------------------------------------------------------ H: foto yang kamu benci, disukai orang lain (29.08 - 32.59)
def gH(cv, t):
    a = eo(prog(t, 29.15, 29.6)); love = eo(prog(t, 30.7, 31.2))
    halo(cv, 540, 700, 420, CORAL if love < 0.5 else MINT, 0.45 * a)
    polaroid(cv, 540, 700, 420, 520, a, rot=-2, content=lambda cc: portrait(cc, 0, -45, 0.72, 1, mirror=False, t=t, ph=0.4), label='foto kamu', lc='#2A2E6E', glow=0.7 * love, gc=MINT)
    ca = eo(prog(t, 29.5, 29.85)) * (1 - love)
    if ca > 0:
        chip(cv, 'yang kamu benci', 540, 395, ca, size=28, fg='#FFC9BF', bgc='#3A2228', edge=CORAL)
    for k in range(8):
        u = prog(t, 30.7 + k * 0.12, 31.9 + k * 0.12)
        if 0 < u < 1:
            x = 540 + (k - 3.5) * 95 + 25 * math.sin(t * 3 + k); y = lerp(1060, 520, eio(u)); hs = 20 + 6 * (k % 3)
            cv.drawPath(heart_path(x, y, hs * 1.3), P(col(CORAL, 0.4 * (1 - u)), blur=10)); cv.drawPath(heart_path(x, y, hs), P(col('#FF9A8A', 1 - prog(u, 0.7, 1))))
    for k, (txt, x, y) in enumerate((('cakep kok!', 225, 520), ('natural banget', 860, 640), ('suka yang ini', 230, 900))):
        thought_chip(cv, txt, x, y, eo(prog(t, 30.85 + k * 0.3, 31.2 + k * 0.3)), MINT, ('#173A2E', '#0F1F19'), size=28, sc=0.7 + 0.3 * bo(prog(t, 30.85 + k * 0.3, 31.25 + k * 0.3)))

# ------------------------------------------------------------ I: coba balik fotomu (32.59 - 36.6)
I_FLIPS = [33.0, 33.95, 34.55]
def gI(cv, t):
    a = eo(prog(t, 32.65, 33.0))
    n, fx = flip_state(t, I_FLIPS, 0.3); mir = n % 2 == 1
    tap = max(prog(t, f - 0.12, f + 0.25) for f in I_FLIPS)
    halo(cv, 540, 700, 460, MINT if mir else ACC, 0.5 * a)
    cm = eo(prog(t, 35.1, 35.4))
    def content(cc):
        portrait(cc, 540, 650, 0.8, a, mirror=mir, t=t, ph=0.3, flipx=fx)
        if cm < 1: ui_editor(cc, 540, 1040, t, tap if tap < 1 else 0, a * (1 - cm))
        if cm > 0:
            y = 962 + (1 - cm) * 40; r = skia.Rect(370, y - 38, 710, y + 38)
            cc.drawRoundRect(r, 38, 38, P(col('#0C0D16', 0.95 * cm))); cc.drawRoundRect(r, 38, 38, P(col(ACC, 0.7 * cm), stroke=2.5))
            typed = 'aku pilih versi asli!'; nch = int(len(typed) * prog(t, 35.35, 36.2)); f = font(B, 25)
            cc.drawString(typed[:nch] if nch else 'Tulis komentar...', 395, bl(f, y), f, P(col(TXT if nch else MUTED, cm)))
            if (t * 2) % 1 < 0.6 and nch: x_ = 395 + f.measureText(typed[:nch]) + 3; cc.drawLine(x_, y - 16, x_, y + 16, P(col(HL, cm), stroke=3))
    phone(cv, 540, 700, 400, 720, a, content=content, ui=None, t=t)
    for k, (x, lab, c) in enumerate(((330, 'versi cermin', MINT), (750, 'versi asli', ACC_L))):
        p_ = prog(t, 33.8 + k * 0.2, 34.15 + k * 0.2)
        if p_ > 0:
            cv.save(); cv.translate(x, 1125); s_ = 0.7 + 0.3 * bo(p_); cv.scale(s_, s_)
            chip(cv, lab, 0, 0, eo(p_) * a, size=28, fg=c, edge=c, bgc='#15162A'); cv.restore()
    va = eo(prog(t, 34.0, 34.35)) * a
    if va > 0: glow_text(cv, 'vs', 540, 1125, font(XB, 34), MUTED, va)

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

b.DRAWERS = [gA, gB, gC, gD, gE, gF, gG, gH, gI, gJ]

def build_sfx():
    ev = [(0.03, 'whoosh'), (0.22, 'chop'), (0.24, 'blink'),
          (2.95, 'whoosh'), (3.05, 'card'), (3.4, 'shine'), (3.8, 'swish'), (4.75, 'boing'),
          (5.75, 'whoosh'), (5.95, 'swish'), (6.2, 'pop'), (6.5, 'pop'), (6.8, 'pop'), (7.1, 'pop'), (8.2, 'zoom'), (8.75, 'ding_soft'),
          (9.37, 'whoosh'), (9.45, 'card'), (10.0, 'swish'), (10.93, 'pop'), (11.6, 'pop'),
          (13.43, 'whoosh'), (13.5, 'card'), (13.8, 'card'), (15.1, 'pop'), (15.9, 'pop'), (17.0, 'plop'), (17.5, 'plip'), (18.2, 'ding'),
          (19.05, 'plop'), (19.17, 'plop'), (19.29, 'plop'), (20.15, 'plip'), (20.3, 'plip'), (20.45, 'plip'), (20.9, 'ding'),
          (21.56, 'whoosh'), (21.6, 'shine'), (24.3, 'rise'), (24.45, 'ding'),
          (25.24, 'whoosh'), (25.3, 'card'), (26.9, 'card'),
          (29.08, 'whoosh'), (29.15, 'card'), (29.5, 'clunk'), (30.7, 'shine'), (30.85, 'pop'), (31.15, 'pop'), (31.45, 'pop'),
          (32.59, 'whoosh'), (33.8, 'pop'), (34.0, 'pop'), (35.15, 'plip'),
          (36.6, 'whoosh'), (36.75, 'boing'), (37.1, 'shine'), (37.35, 'pop')]
    ev += [(f, 'swish') for f in A_FLIPS] + [(f - 0.1, 'tick') for f in I_FLIPS] + [(f, 'swish') for f in I_FLIPS]
    ev += [(22.6 + k * 0.11, 'tick') for k in range(12)]
    ev += [(35.3 + k * 0.045, 'tick') for k in range(0, 20, 2)]
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
