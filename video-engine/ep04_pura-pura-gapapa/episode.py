#!/usr/bin/env python3
"""Ruang Pikir reel #4: 'Pura-pura gapapa, kok capek?' (menahan emosi vs memaknai ulang, Gross & Levenson 1997; Gross 1998)
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
b.GROUPS = [(0.0, 6.22, 'A'), (6.22, 8.91, 'B'), (8.91, 13.13, 'C'), (13.13, 16.91, 'D'), (16.91, 23.32, 'E'),
            (23.32, 27.87, 'F'), (27.87, 32.85, 'G'), (32.85, 36.6, 'H'), (36.6, 42.0, 'I')]
# caption per frasa, disinkronkan ke jeda suara; [..] = kata kunci
PHRASES = [(0.15, 'Pernah bilang ["aku gapapa"],'), (1.86, 'padahal lagi [nggak baik-baik aja]?'),
           (3.48, '[Senyum] di luar,'), (4.6, 'tapi di dalam rasanya [mau meledak].'),
           (6.22, 'Ternyata,'), (6.78, 'nahan emosi bikin tubuhmu [makin tegang].'),
           (8.91, 'Tahun [1997],'), (10.3, '[James Gross] dan timnya mengujinya.'),
           (13.13, 'Peserta nonton [film sedih].'), (14.9, 'Separuhnya disuruh [menahan ekspresi].'),
           (16.91, 'Hasilnya?'), (17.45, 'Wajahnya memang [datar],'), (18.9, 'tapi rasa sedihnya [tetap ada].'),
           (20.31, 'Malah,'), (20.8, '[jantung] dan pembuluh darahnya'), (22.1, 'kerja [lebih keras].'),
           (23.32, 'Setahun kemudian,'), (24.2, 'Gross menemukan cara yang [lebih sehat]:'), (25.9, '[memaknai ulang] situasinya.'),
           (27.87, 'Misalnya,'), (28.3, '"dia bukan [benci] aku,'), (29.65, 'dia lagi [capek]."'),
           (30.6, 'Perasaannya [reda],'), (31.5, 'tubuh [nggak ikut tegang].'),
           (32.85, 'Kamu nggak harus [selalu kuat].'), (34.3, '[Cerita] ke orang yang kamu percaya, ya.'),
           (36.6, 'Follow [Ruang Pikir],'), (37.6, 'biar makin kenal [isi kepalamu].')]
b.CAPS = [(t, s, '') for t, s in PHRASES]          # dipakai base hanya untuk jadwal

# ------------------------------------------------------------ chrome gaya sinematik
b.draw_tag = lambda cv, t: None
b.draw_progress = lambda cv, t: None
def draw_title(cv, t):
    a = eo(prog(t, 0.1, 0.55)) * (1 - eio(prog(t, 5.85, 6.35)))
    if a <= 0: return
    segs = parse("Pura-pura gapapa, [kok capek]?"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 232) + (1 - eo(prog(t, 0.1, 0.55))) * 16 - 10 * eio(prog(t, 5.85, 6.35))
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
        e = PHRASES[i + 1][0] - 0.06 if i + 1 < len(PHRASES) else 41.7
        if t < s or t > e + 0.2: continue
        aout = 1 - prog(t, e, e + 0.18)
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

# ------------------------------------------------------------ A: "aku gapapa" di luar, emosi membesar di dalam (0 - 6.22)
def gA(cv, t):
    a0 = eo(prog(t, 0.1, 0.6))
    ca = eo(prog(t, 0.2, 0.7)); smile = eio(prog(t, 3.45, 3.85))
    cv.save(); cv.translate(0, (1 - ca) * 24)
    r = skia.Rect(200, 345, 880, 535); pth = glass(cv, r, 42, ca, glow=0.25 + 0.3 * smile)
    sheen(cv, pth, r, prog(t, 3.5, 4.3))
    typed = 'Aku gapapa kok.'; n = int(len(typed) * prog(t, 0.55, 1.55)); f = font(XB, 72)
    if smile < 1 and ca > 0:
        w = f.measureText(typed); x = 540 - w / 2; aa = ca * (1 - smile)
        cv.drawString(typed[:n], x, bl(f, 440), f, P(col(TXT, aa)))
        if (t * 2) % 1 < 0.6 and t < 3.4: cx_ = x + f.measureText(typed[:n]) + 6; cv.drawLine(cx_, 405, cx_, 477, P(col(HL, aa), stroke=4))
    if smile > 0:
        cv.save(); cv.translate(540, 442); s = bo(smile); cv.scale(s, s)
        ink = P(col(HL, ca), stroke=11)
        for sx in (-1, 1):
            e = skia.Path(); e.moveTo(sx * 92 - 34, -14); e.quadTo(sx * 92, -52, sx * 92 + 34, -14); cv.drawPath(e, ink)
        m = skia.Path(); m.moveTo(-120, 18); m.quadTo(0, 120, 120, 18); cv.drawPath(m, P(col(HL, 0.4 * ca), stroke=22, blur=10)); cv.drawPath(m, ink)
        cv.restore()
    chip(cv, 'di luar', 790, 345, eo(prog(t, 3.6, 3.95)) * ca, size=24, fg=ACC_XL)
    cv.restore()
    # bola "emosi" di lantai: membesar dan memerah, lalu hampir meledak
    fy, x0, x1 = 1030, 190, 890
    grow = 0.22 * eio(prog(t, 1.9, 2.8)) + 0.78 * eio(prog(t, 4.5, 5.45))
    rr = lerp(72, 212, grow); red = eio(prog(t, 1.9, 5.3)); sag = 6 + 42 * grow
    floor(cv, x0, x1, fy, a0, sag)
    shake = 5 * math.sin(t * 57) * prog(t, 5.45, 5.65)
    cx = 540 + shake; cy = sag_y(x0, x1, fy, sag, 540) - rr
    cv.drawOval(skia.Rect(cx - rr * 0.8, cy + rr - 12, cx + rr * 0.8, cy + rr + 16), P(col('#000000', 0.55 * a0), blur=12))
    boom = prog(t, 5.55, 5.95)
    if boom > 0: rays(cv, cx, cy, rr * 2.1, 0.9 * boom, t, n=16, c=CORAL, spin=8)
    pr = prog(t, 5.15, 5.45)
    if pr > 0:
        for k in range(3):
            rp = (t * 1.7 + k / 3) % 1.0
            cv.drawCircle(cx, cy, rr * (1.04 + 0.4 * rp), P(col(CORAL, 0.55 * (1 - rp) * pr * a0), stroke=4))
    sphere(cv, cx, cy, rr, tri(red), a0, glow=0.6 + 0.7 * red, label='emosi', lsize=max(26, rr * 0.22))
    ia = prog(t, 4.6, 5.2)
    if ia > 0:
        p = skia.Path(); p.addCircle(cx, cy, rr); cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
        for k in range(4):
            ang = t * (1.6 + k * 0.45) + k * 1.7
            px, py = cx + math.cos(ang) * rr * 0.45, cy + math.sin(ang * 1.3) * rr * 0.38
            cv.drawCircle(px, py, rr * 0.38, P(shader=rg(px, py, rr * 0.38, [col('#FFC2B8', 0.5 * ia), col('#FF6B57', 0)])))
        if boom > 0:
            for k in range(5):
                ang = k * 1.26 + 0.4; seg = skia.Path(); seg.moveTo(cx, cy)
                for j in range(1, 5):
                    rr_ = rr * j / 4 * eo(boom); jit = (12 if j % 2 else -12)
                    seg.lineTo(cx + math.cos(ang) * rr_ + math.sin(ang) * jit, cy + math.sin(ang) * rr_ - math.cos(ang) * jit)
                cv.drawPath(seg, P(col('#FFE1DB', 0.7 * a0), stroke=9, blur=6)); cv.drawPath(seg, P(col('#FFFFFF', a0), stroke=3))
        cv.restore()
        f2 = font(B, max(26, rr * 0.22)); w = f2.measureText('emosi'); cv.drawString('emosi', cx - w / 2, bl(f2, cy), f2, P(col(TXT, a0)))
    chip(cv, 'di dalam', min(cx + rr * 0.95, 900), cy - rr * 0.85, eo(prog(t, 4.7, 5.05)) * a0, size=24, fg='#FFC9BF', bgc='#3A2228', edge=CORAL)

# ------------------------------------------------------------ B: tubuh makin tegang (6.22 - 8.91)
GB_F = (0.9, 2.6, 2.2)
def gB(cv, t):
    a = eo(prog(t, 6.25, 6.75)); s = 0.72; cx, cy = 540, 690
    ph = accel_phase(t, 6.3, *GB_F); pu = beat_pulse(ph); tens = eio(prog(t, 6.8, 8.3))
    halo(cv, 500, 1000, 420, CORAL, (0.25 + 0.5 * tens) * a)
    head_outline(cv, cx, cy, s, a)
    X = lambda bx: cx - 569 * s + bx * s; Y = lambda by: cy - 571 * s + by * s
    hx, hy = X(505), Y(1005)
    vessels = [((505, 1005), (500, 930), (520, 860), (540, 760)), ((505, 1005), (430, 990), (330, 1010), (210, 1070)),
               ((505, 1005), (590, 990), (720, 1010), (860, 1070)), ((540, 760), (500, 650), (460, 560), (420, 470)),
               ((540, 760), (620, 690), (700, 620), (760, 520))]
    for k, pts in enumerate(vessels):
        d = eo(prog(t, 6.8 + k * 0.12, 7.6 + k * 0.12))
        if d <= 0: continue
        p = skia.Path(); p.moveTo(X(pts[0][0]), Y(pts[0][1])); p.cubicTo(X(pts[1][0]), Y(pts[1][1]), X(pts[2][0]), Y(pts[2][1]), X(pts[3][0]), Y(pts[3][1]))
        mm = skia.PathMeasure(p, False); seg = skia.Path(); mm.getSegment(0, mm.getLength() * d, seg, True)
        cv.drawPath(seg, P(col(CORAL, (0.25 + 0.4 * pu) * a), stroke=12, blur=8)); cv.drawPath(seg, P(col('#FF9A8A', 0.9 * a), stroke=3.5))
        if d >= 1: comet(cv, p, (ph * 0.8 + k * 0.17) % 1.0, c='#FFE1DB', n=6, r=7)
    for k in range(2):
        rp = (ph + k * 0.5) % 1.0
        cv.drawCircle(hx, hy, 40 * (1.2 + rp * 2.4), P(col(CORAL, 0.5 * (1 - rp) * a * tens), stroke=3))
    hs = 40 * (1 + 0.24 * pu)
    cv.drawPath(heart_path(hx, hy, hs * 1.3), P(col(CORAL, (0.4 + 0.5 * pu) * a), blur=20))
    cv.drawPath(heart_path(hx, hy, hs), P(shader=rg(hx - hs * 0.3, hy - hs * 0.4, hs * 1.8, [col('#FFC2B8', a), col(CORAL, a), col('#8A1F33', a)])))
    chip(cv, 'detak makin cepat', 790, 1110, eo(prog(t, 7.6, 7.95)) * a, size=24, fg='#FFC9BF', bgc='#3A2228', edge=CORAL)

# ------------------------------------------------------------ C: kartu riset 1997 (8.91 - 13.13)
def gC(cv, t):
    ent = prog(t, 8.95, 9.55); a = clamp(ent * 2)
    rays(cv, 540, 700, 620, 0.45 * a, t, n=12, spin=3)
    cv.save(); cv.translate(540, 700); s = 0.88 + 0.12 * bo(ent); cv.scale(s, s); cv.translate(-540, -700)
    r = skia.Rect(170, 410, 910, 990); pth = glass(cv, r, 46, a, glow=0.35, fill=('#24264A', '#111226'))
    sheen(cv, pth, r, prog(t, 9.6, 10.5))
    tracked(cv, 'RISET', 540, 490, font(MONO, 26), P(col(HL, a)), 10)
    glow_text(cv, '1997', 540, 640, font(XB, 210), a=a, glow=0.55, shader=lg(0, 560, 0, 720, [col('#FFFFFF', a), col('#B9BFFF', a)]))
    na = eo(prog(t, 10.3, 10.7)) * a
    glow_text(cv, 'James Gross & Robert Levenson', 540, 790, font(XB, 40), TXT, na)
    glow_text(cv, 'Journal of Abnormal Psychology', 540, 842, font(M, 25), MUTED, eo(prog(t, 10.5, 10.9)) * a)
    chip(cv, '180 peserta', 540, 920, eo(prog(t, 11.0, 11.35)) * a, size=26)
    cv.restore()

# ------------------------------------------------------------ D: tes film sedih (13.13 - 16.91)
def gD(cv, t):
    a = eo(prog(t, 13.15, 13.6))
    chip(cv, 'nonton film sedih', 540, 395, eo(prog(t, 13.3, 13.65)) * a, size=26)
    r = skia.Rect(310, 455, 770, 745)
    cv.save(); cv.translate(540, 600); s = 0.88 + 0.12 * bo(prog(t, 13.15, 13.7)); cv.scale(s, s); cv.translate(-540, -600)
    glass(cv, r, 36, a, glow=0.3)
    sc = skia.Rect(330, 475, 750, 725); cv.drawRoundRect(sc, 24, 24, P(shader=lg(0, 475, 0, 725, [col('#1C1F3A', a), col('#0E0F1E', a)])))
    cv.save(); cv.clipRect(sc)
    for k in range(16):
        rx = 350 + (k * 61) % 390; ry = 480 + ((t * 230 + k * 53) % 245)
        cv.drawLine(rx, ry, rx - 5, ry + 16, P(col('#8FA6FF', 0.35 * a), stroke=3))
    cv.restore()
    sphere(cv, 540, 600, 82, BLUE, a, glow=0.4); face(cv, 540, 600, 82, 'sad', a, t, 0.3)
    for k in range(2):
        tp = (t * 0.7 + k * 0.5) % 1.0; tear(cv, 540 - 82 * 0.33, 600 + 10 + tp * 70, 9, a * (1 - tp))
    cv.restore()
    split = eio(prog(t, 14.85, 15.35))
    if split < 1: eye(cv, 540, 930, 92 * (1 - 0.3 * split), a * (1 - split), t)
    if split > 0:
        for i, (x, mood, lab, c) in enumerate(((365, 'sad', 'nonton biasa', ACC_L), (715, 'flat', 'tahan ekspresi', CORAL))):
            pa = eo(prog(t, 14.95 + i * 0.2, 15.4 + i * 0.2)) * a
            if pa <= 0: continue
            yy = 930 + (1 - bo(prog(t, 14.95 + i * 0.2, 15.45 + i * 0.2))) * 40
            sphere(cv, x, yy, 86, BLUE, pa, glow=0.4); face(cv, x, yy, 86, mood, pa, t, 0.5 + i * 0.3)
            if i == 0:
                tp = (t * 0.8) % 1.0; tear(cv, x - 86 * 0.33, yy + 6 + tp * 60, 9, pa * (1 - tp))
            else:
                la = prog(t, 15.45, 15.8)
                if la > 0:
                    cv.save(); cv.translate(x + 74, yy + 52); cv.scale(bo(la), bo(la)); cv.drawCircle(0, 0, 34, P(col(CORAL, 0.4), blur=10)); icon(cv, 'lock', 0, 0, 28, CORAL, 1, t); cv.restore()
            chip(cv, lab, x, 1080, pa, size=24, fg=c, edge=c, f=B)

# ------------------------------------------------------------ E: hasil (16.91 - 23.32)
METRICS = [(17.45, 'face', 'Ekspresi wajah', 0.78, 0.22, 'datar', HL),
           (18.9, 'cloud', 'Rasa sedih', 0.66, 0.66, 'tetap ada', '#C9D4FF'),
           (20.8, 'heart', 'Kerja jantung', 0.46, 0.9, 'lebih keras', CORAL)]
def gE(cv, t):
    a = eo(prog(t, 16.95, 17.4))
    k = max([i for i, m in enumerate(METRICS) if t >= m[0]], default=-1)
    # judul metrik (berganti)
    for i, (t0, ic, lab, vb, vt, word, c) in enumerate(METRICS):
        ha = eo(prog(t, t0, t0 + 0.3)) * (1 - eo(prog(t, METRICS[i + 1][0] - 0.05, METRICS[i + 1][0] + 0.2)) if i + 1 < len(METRICS) else 1) * a
        if ha <= 0: continue
        f = font(XB, 44); w = f.measureText(lab); x = 540 - (w + 76) / 2
        icon(cv, ic, x + 26, 450, 28, c, ha, t); cv.drawString(lab, x + 76, bl(f, 450) + (1 - ha) * 10, f, P(col(TXT, ha)))
    # dua batang
    def val(j):
        if k < 0: return (0.0, 0.0)
        t0 = METRICS[k][0]; u = eio(prog(t, t0 + 0.1, t0 + 0.8))
        pb, pt_ = (METRICS[k - 1][3], METRICS[k - 1][4]) if k > 0 else (0.0, 0.0)
        return (lerp(pb, METRICS[k][3], u), lerp(pt_, METRICS[k][4], u))
    vb, vt = val(0); ct = METRICS[k][6] if k >= 0 else HL
    pill_bar(cv, 190, 890, 580, 80, vb, 'Nonton biasa', ACC_L, a)
    pill_bar(cv, 190, 890, 700, 80, vt, 'Tahan ekspresi', ct if k == 2 else '#8C93FF', eo(prog(t, 17.1, 17.5)) * a)
    # kata besar
    for i, (t0, ic, lab, vb_, vt_, word, c) in enumerate(METRICS):
        wa = bo(prog(t, t0 + 0.45, t0 + 0.85)); wo = (1 - eo(prog(t, METRICS[i + 1][0] - 0.05, METRICS[i + 1][0] + 0.2))) if i + 1 < len(METRICS) else 1
        if wa <= 0 or wo <= 0: continue
        cv.save(); cv.translate(540, 905); s = 0.6 + 0.4 * wa; cv.scale(s, s)
        glow_text(cv, word, 0, 0, font(XB, 118), TXT, clamp(wa) * wo * a, glow=0.7, gc=c, shader=lg(0, -60, 0, 60, [col('#FFFFFF', clamp(wa) * wo * a), col(c, clamp(wa) * wo * a)]))
        cv.restore()
        if i == 2:
            for j in range(3):
                rp = (t * 1.5 + j / 3) % 1.0
                cv.drawCircle(540, 905, 160 * (1 + rp), P(col(CORAL, 0.35 * (1 - rp) * wo * a * prog(t, 22.2, 22.5)), stroke=3))

# ------------------------------------------------------------ F: 1998, cara yang lebih sehat (23.32 - 27.87)
def gF(cv, t):
    a = eo(prog(t, 23.4, 23.85))
    cv.save(); cv.translate(0, (1 - a) * 24)
    r = skia.Rect(250, 350, 830, 520); pth = glass(cv, r, 34, a, glow=0.3); sheen(cv, pth, r, prog(t, 23.9, 24.6))
    tracked(cv, 'RISET 1998', 540, 392, font(MONO, 22), P(col(HL, a)), 6)
    glow_text(cv, 'James Gross', 540, 444, font(XB, 46), TXT, a)
    glow_text(cv, 'J. Personality & Social Psychology', 540, 492, font(M, 22), MUTED, a)
    cv.restore()
    fy, x0, x1 = 1020, 150, 930; hl = eio(prog(t, 25.9, 26.4)); sag = 18 + 20 * hl
    floor(cv, x0, x1, fy, a, sag)
    for i, (x, lab) in enumerate(((330, 'menahan'), (750, 'maknai ulang'))):
        p_ = prog(t, 24.25 + i * 0.3, 24.85 + i * 0.3)
        if p_ <= 0: continue
        rr = 128; lift = (30 * hl) if i == 1 else 0
        y = sag_y(x0, x1, fy, sag, x) - rr - (1 - bo(p_)) * 140 - lift
        cols = tri(1.0) if i == 0 else tri(0.0, hl)
        aa = clamp(p_ * 2) * a * ((1 - 0.45 * hl) if i == 0 else 1)
        if i == 1 and hl > 0: rays(cv, x, y, 330, 0.8 * hl * a, t, n=14, c=MINT)
        cv.drawOval(skia.Rect(x - rr * 0.8, y + rr + lift - 10, x + rr * 0.8, y + rr + lift + 14), P(col('#000000', 0.5 * aa), blur=12))
        sphere(cv, x, y, rr, cols, aa, glow=0.5 + 0.6 * (hl if i == 1 else 0), label=lab, lsize=30)
    if hl > 0: check_mark(cv, 750, 1020 - 128 * 2 - 30 - 46, 34, prog(t, 26.2, 26.7), a)

# ------------------------------------------------------------ G: memaknai ulang, emosi mengempis (27.87 - 32.85)
def gG(cv, t):
    a = eo(prog(t, 27.95, 28.35))
    cv.save(); cv.translate(0, (1 - a) * 24)
    r = skia.Rect(190, 345, 890, 505); glass(cv, r, 34, a, glow=0.2)
    cv.drawCircle(262, 425, 40, P(shader=lg(0, 385, 0, 465, [col('#7FD4FF', a), col(ACC, a)])))
    f = font(XB, 34); cv.drawString('R', 262 - f.measureText('R') / 2, bl(f, 425), f, P(col(INK, a)))
    cv.drawString('teman', 322, bl(font(B, 24), 392), font(B, 24), P(col(MUTED, a)))
    br = skia.Rect(322, 412, 450, 470); cv.drawRoundRect(br, 26, 26, P(col('#2A2C40', a))); cv.drawRoundRect(br, 26, 26, P(col(MUTED, 0.5 * a), stroke=2))
    cv.drawString('ok.', 352, bl(font(XB, 34), 441), font(XB, 34), P(col(TXT, a)))
    cv.drawString('dibaca', 470, bl(font(M, 22), 460), font(M, 22), P(col(MUTED, a)))
    cv.restore()
    p1 = prog(t, 28.35, 28.7); st = prog(t, 29.6, 29.85); out1 = prog(t, 29.85, 30.15)
    if p1 > 0 and out1 < 1:
        thought_chip(cv, 'dia benci aku...', 540, 610, clamp(p1 * 2) * (1 - out1) * a, CORAL, ('#3A2228', '#1E1418'), strike=st, sc=(0.7 + 0.3 * bo(p1)) * (1 - 0.2 * out1))
    p2 = prog(t, 29.75, 30.15)
    if p2 > 0:
        thought_chip(cv, 'dia lagi capek.', 540, 610, clamp(p2 * 2) * a, MINT, ('#173A2E', '#0F1F19'), sc=0.7 + 0.3 * bo(p2))
        check_mark(cv, 540 + 190, 610 - 52, 28, prog(t, 30.1, 30.6), a)
    fy, x0, x1 = 1070, 190, 890
    d = eio(prog(t, 30.6, 31.45)); rr = lerp(200, 92, d); sag = lerp(44, 8, d)
    floor(cv, x0, x1, fy, a, sag)
    cx = 540 + 3 * math.sin(t * 50) * (1 - d) * prog(t, 28.0, 28.4); cy = sag_y(x0, x1, fy, sag, 540) - rr
    cv.drawOval(skia.Rect(cx - rr * 0.8, cy + rr - 10, cx + rr * 0.8, cy + rr + 14), P(col('#000000', 0.5 * a), blur=12))
    sphere(cv, cx, cy, rr, tri(1 - d, d), a, glow=0.5 + 0.4 * (1 - d), label='emosi', lsize=max(26, rr * 0.22))
    ta = eo(prog(t, 31.5, 31.85)) * a
    if ta > 0:
        r2 = skia.Rect(650, 880, 900, 960); glass(cv, r2, 40, ta, glow=0.4, gc=MINT, edge=MINT)
        ln = skia.Path()
        for k in range(61):
            u = k / 60; xx = lerp(675, 790, u); ph = u * 1.6 + t * 0.9
            yy = 920 - 16 * math.exp(-(((ph % 1.0) - 0.5) / 0.06) ** 2); (ln.moveTo if k == 0 else ln.lineTo)(xx, yy)
        cv.drawPath(ln, P(col(MINT, ta), stroke=3))
        cv.drawString('tenang', 800, bl(font(B, 26), 920), font(B, 26), P(col(TXT, ta)))

# ------------------------------------------------------------ H: nggak harus selalu kuat (32.85 - 36.6)
def gH(cv, t):
    a = eo(prog(t, 32.9, 33.3)); warm = eo(prog(t, 34.3, 35.0))
    halo(cv, 540, 900, 440, '#FFB38A', 0.3 * warm); halo(cv, 540, 900, 380, ACC, 0.45 * a)
    happy = prog(t, 35.3, 35.5)
    hx, hy, hr = person(cv, 380, 1090, 320, mood='happy' if happy > 0.5 else 'neutral', look=(1, 0), a=a, glow=1 + warm, blink=blink_at(t, 0.5))
    fa = eo(prog(t, 34.25, 34.7))
    if fa > 0: person(cv, 700, 1090, 310, mood='happy', look=(-1, 0), a=fa, glow=1.4, blink=blink_at(t, 0.9))
    mv = eio(prog(t, 34.75, 35.4))
    sx, sy = lerp(470, 540, mv), lerp(900, 830, mv) + 6 * math.sin(t * 2.2)
    sphere(cv, sx, sy, lerp(58, 50, mv), tri(0.0, 1.0), a, glow=0.6 + 0.4 * warm, label='emosi', lsize=18)
    ba = prog(t, 34.55, 34.9)
    if ba > 0:
        cv.save(); cv.translate(500, 640); s = 0.7 + 0.3 * bo(ba); cv.scale(s, s); cv.translate(-500, -640)
        pth, r = bubble_path(500, 640, 230, 92, (hx + hr * 0.7, hy - hr * 1.0))
        draw_bubble(cv, pth, r, clamp(ba * 2), glow=0.4)
        for k in range(3): cv.drawCircle(460 + k * 40, 640, 11 + 4 * bump(((t * 2.4) - k * 0.2) % 1), P(col(ACC_XL, clamp(ba * 2))))
        cv.restore()
    hp_ = prog(t, 35.35, 36.4)
    if hp_ > 0:
        y2 = lerp(800, 690, eo(hp_)); hs = 26 * bo(prog(hp_, 0, 0.3))
        cv.drawPath(heart_path(540, y2, hs * 1.3), P(col(CORAL, 0.5 * (1 - prog(hp_, 0.7, 1))), blur=12))
        cv.drawPath(heart_path(540, y2, hs), P(col('#FF9A8A', 1 - prog(hp_, 0.75, 1))))

# ------------------------------------------------------------ I: outro (36.6 - 42)
def gI(cv, t):
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
    press = 1 - 0.08 * bump(prog(tt, 0.75, 1.0))
    ba = prog(tt, 0.3, 0.7)
    if ba > 0:
        cv.save(); cv.translate(540, 1100); cv.scale(press, press); cv.translate(-540, -1100)
        cv.drawRoundRect(skia.Rect(430, 1062, 650, 1138), 38, 38, P(col(ACC, 0.45 * clamp(ba * 1.5)), blur=18))
        pill(cv, 'Follow', 540, 1100, ba, bgc='#A9B2FF', fg=INK, size=42); cv.restore()

b.DRAWERS = [gA, gB, gC, gD, gE, gF, gG, gH, gI]

def build_sfx():
    ev = [(0.1, 'whoosh'), (1.9, 'rise'), (3.45, 'swish'), (3.6, 'pop'), (4.5, 'zoom'), (4.7, 'pop'), (5.15, 'fizz_soft'), (5.55, 'crack'), (5.6, 'zap2'),
          (6.22, 'whoosh'), (6.8, 'rise'), (7.6, 'pop'),
          (8.91, 'whoosh'), (8.95, 'card'), (9.6, 'swish'), (10.3, 'pop'), (11.0, 'pop'),
          (13.13, 'whoosh'), (13.3, 'blink'), (14.85, 'swish'), (14.95, 'plop'), (15.15, 'plop'), (15.45, 'clunk'),
          (16.91, 'whoosh'), (17.1, 'swish'), (17.55, 'zap2'), (17.9, 'pop'), (19.0, 'swish'), (19.35, 'pop'), (20.9, 'rise'), (21.25, 'pop'),
          (23.32, 'whoosh'), (23.4, 'card'), (24.25, 'plop'), (24.55, 'plop'), (25.9, 'shine'), (26.2, 'plip'),
          (27.87, 'whoosh'), (27.95, 'plip'), (28.35, 'pop'), (29.6, 'swish'), (29.75, 'ding'), (30.6, 'fizz_soft'), (31.5, 'ding_soft'),
          (32.85, 'whoosh'), (34.25, 'pop'), (34.55, 'plip'), (35.35, 'shine'),
          (36.6, 'whoosh'), (36.75, 'boing'), (37.1, 'shine'), (37.35, 'pop')]
    ev += [(0.55 + k * 0.07, 'tick') for k in range(15)]
    ev += [(bt, 'heart') for bt in beat_times(6.3, 8.85, *GB_F)][::2]
    ev += [(21.6 + k * 0.5, 'heart') for k in range(3)]
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
