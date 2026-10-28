#!/usr/bin/env python3
"""Ruang Pikir reel #6: 'Habis ngobrol, kok takut ilfeel?' (liking gap, Boothby, Cooney, Sandstrom & Clark 2018)
Gaya "garis neon + tipografi kinetik": ilustrasi garis tipis yang menggambar dirinya sendiri, kata raksasa yang menghantam layar.
Gaya sinematik (seperti video acuan "Jam 2 pagi, kok overthinking?"): judul hanya di awal, tanpa tag, caption besar per frasa
tanpa kotak, ilustrasi besar-minimalis (bola 3D lembut, kartu kaca, kata besar, siluet garis), kamera bergerak halus.
python3 episode.py preview t1 t2 ... | timeline out.json | video out.mp4"""
import sys, os, math, json, subprocess, random
import skia
import base as b
from base import (clamp, lerp, prog, eo, ei, eio, bo, bump, col, P, lg, rg, layer, font, XB, B, M, MONO, bl, tracked, parse,
                 pill, sparkle, person, ACC, ACC_L, ACC_XL, TXT, MUTED, CORAL, MINT, W, H, FPS)

VIOLET, YELLOW, INK, HL = '#B57BFF', '#FFD23F', '#0B0C1E', '#AEB6FF'

# adegan (waktu animasi, DUR 42); tag tidak ditampilkan
b.GROUPS = [(0.0, 2.62, 'A'), (2.62, 5.98, 'B'), (5.98, 9.55, 'C'), (9.55, 12.46, 'D'), (12.46, 16.31, 'E'),
            (16.31, 22.58, 'F'), (22.58, 27.91, 'G'), (27.91, 32.15, 'H'), (32.15, 36.6, 'I'), (36.6, 42.0, 'J')]
PHRASES = [(0.15, 'Dia [lebih suka kamu],'), (1.4, 'daripada yang [kamu kira].'),
           (2.62, 'Tapi habis ngobrol,'), (3.65, 'kita malah mikir:'), (4.38, '"dia [ilfeel] nggak, ya?"'),
           (5.98, 'Tahun [2018],'), (7.28, 'psikolog [Erica Boothby] menelitinya.'),
           (9.55, 'Dua [orang asing] dipasangkan,'), (10.98, 'lalu ngobrol [lima menit].'),
           (12.46, 'Setelahnya, mereka [menebak]:'), (13.95, 'seberapa suka [lawan bicaranya] sama mereka?'),
           (16.31, 'Hasilnya?'), (17.0, 'Kebanyakan menebak [terlalu rendah].'),
           (18.73, 'Lawan bicaranya'), (19.67, 'ternyata [lebih suka] mereka,'), (21.0, 'daripada yang mereka kira.'),
           (22.58, 'Ini namanya [liking gap]:'), (24.04, 'kita sibuk [menilai diri sendiri],'), (25.64, 'sampai nggak lihat [sinyal suka] dari dia.'),
           (27.91, 'Bahkan di antara [teman sekamar] baru,'), (29.57, 'salah tebak ini bertahan [berbulan-bulan].'),
           (32.15, 'Jadi, nggak usah [diputar ulang] di kepala.'), (34.2, 'Kamu [lebih disukai] dari yang kamu kira.'),
           (36.6, 'Follow [Ruang Pikir],'), (37.84, 'biar makin kenal [isi kepalamu].')]
b.CAPS = [(t, s, '') for t, s in PHRASES]          # dipakai base hanya untuk jadwal

# ------------------------------------------------------------ chrome gaya sinematik
b.draw_tag = lambda cv, t: None
b.draw_progress = lambda cv, t: None
def draw_title(cv, t):
    a = eo(prog(t, 0.05, 0.35)) * (1 - eio(prog(t, 5.5, 5.95)))
    if a <= 0: return
    segs = parse("Habis ngobrol, [kok takut ilfeel]?"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 232) + (1 - eo(prog(t, 0.05, 0.35))) * 16 - 10 * eio(prog(t, 5.5, 5.95))
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
    off = (t * 12) % 72
    gp = P(shader=lg(0, 260, 0, 1200, [col(ACC_L, 0), col(ACC_L, 0.05), col(ACC_L, 0.05), col(ACC_L, 0)], [0, 0.15, 0.85, 1]), stroke=1.2)
    for k in range(-1, 17): x = k * 72 + off * 0.5; cv.drawLine(x, 260, x, 1200, gp)
    for k in range(14): y = 260 + k * 72 + off; cv.drawLine(0, y, W, y, gp)
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

# ------------------------------------------------------------ A: HOOK — "LEBIH SUKA" (0 - 2.62)
def gA(cv, t):
    a = eo(prog(t, 0.0, 0.15))
    d = two_heads(cv, t, 0.0, a, s=0.42, y=640)
    hp = prog(t, 0.35, 0.9)
    if hp > 0:
        hs = 46 * (1 + 0.08 * math.sin(t * 7)); hl = heart_line(540, 620, hs)
        neon(cv, hl, eo(hp), '#C7F7E4', 5, a, 1.2, MINT)
        if hp >= 1: cv.drawPath(hl, P(col(MINT, 0.25 * a)))
    slam(cv, 'LEBIH SUKA', 540, 930, 150, t, 0.45, '#FFFFFF', '#9FF2D0', MINT, shake=8)
    ka = eo(prog(t, 1.4, 1.75))
    if ka > 0:
        f = font(XB, 50); w = f.measureText('daripada yang kamu kira'); y = bl(f, 1060) + (1 - ka) * 16
        cv.drawString('daripada yang kamu kira', 540 - w / 2, y, f, P(col(ACC_XL, ka * a)))

# ------------------------------------------------------------ B: habis ngobrol, overthinking "ILFEEL?" (2.62 - 5.98)
def gB(cv, t):
    a = eo(prog(t, 2.65, 3.0))
    ph = head_line(470, 680, 0.62, 1)
    neon(cv, ph, eo(prog(t, 2.65, 3.25)), ACC_XL, 4.5, a)
    # gelembung obrolan tadi diputar ulang (mundur)
    for k in range(3):
        u = (t * 0.6 + k / 3) % 1.0; ba = prog(t, 2.9, 3.3) * a * bump(u)
        if ba <= 0: continue
        x = 900 - u * 80; y = 450 + k * 115
        bp = skia.Path(); bp.addRRect(skia.RRect.MakeRectXY(skia.Rect(x - 90, y - 34, x + 90, y + 34), 34, 34))
        neon(cv, bp, 1, HL, 3, ba, 0.6)
        for j in range(3): cv.drawLine(x - 50 + j * 30, y, x - 34 + j * 30, y, P(col(HL, ba), stroke=5))
    # pikiran berputar di kepala
    ra = eo(prog(t, 3.65, 4.0)) * a
    if ra > 0:
        sc = skia.Path(); cx, cy = 480, 600
        for i in range(181):
            u = i / 180 * math.tau * 2.2 + t * 2.4
            x = cx + (70 + 25 * math.sin(3 * u)) * math.cos(u) * 0.9; y = cy + (55 + 20 * math.cos(2 * u)) * math.sin(u)
            (sc.moveTo if i == 0 else sc.lineTo)(x, y)
        neon(cv, sc, eo(prog(t, 3.65, 4.3)), '#FFC9BF', 3.5, ra, 0.9, CORAL)
        loop_arrow(cv, 480, 600, 150, t, ra * 0.9, CORAL, spin=-160)
    slam(cv, 'ILFEEL?', 540, 1000, 170, t, 4.38, '#FFFFFF', '#FF9A8A', CORAL, shake=12)
    if t > 4.6 and int(t * 14) % 5 == 0:
        cv.save(); cv.translate(10, 0); layer(cv, 0.35)
        f = font(XB, 170); w = f.measureText('ILFEEL?'); cv.drawString('ILFEEL?', 540 - w / 2, bl(f, 1000), f, P(col('#5AC8FF')))
        cv.restore(); cv.restore()

# ------------------------------------------------------------ C: riset 2018 (5.98 - 9.55)
def gC(cv, t):
    a = eo(prog(t, 6.0, 6.35))
    pg = skia.Path(); pg.addRoundRect(skia.Rect(230, 400, 850, 1080), 34, 34)
    for k in range(6): pg.moveTo(300, 830 + k * 40); pg.lineTo(780 - (k % 3) * 70, 830 + k * 40)
    neon(cv, pg, eo(prog(t, 6.0, 6.9)), ACC_L, 3, a * 0.8, 0.6)
    tracked(cv, 'RISET', 540, 470, font(MONO, 26), P(col(HL, eo(prog(t, 6.2, 6.5)) * a)), 10)
    outline_text(cv, '2018', 540, 620, 200, eo(prog(t, 6.1, 7.0)), eo(prog(t, 6.9, 7.3)), a, ACC_XL, ACC,
                 shader=lg(0, 540, 0, 700, [col('#FFFFFF', a), col('#B9BFFF', a)]))
    na = eo(prog(t, 7.28, 7.65)) * a
    glow_text(cv, 'Boothby, Cooney, Sandstrom & Clark', 540, 760, font(XB, 34), TXT, na)
    glow_text(cv, 'Psychological Science', 540, 806, font(M, 26), MUTED, eo(prog(t, 7.45, 7.8)) * a)

# ------------------------------------------------------------ D: dua orang asing, ngobrol 5 menit (9.55 - 12.46)
def gD(cv, t):
    a = eo(prog(t, 9.58, 9.9)); sl = (1 - eo(prog(t, 9.58, 10.2))) * 160
    two_heads(cv, t, 9.58, a, s=0.4, y=760, slide=sl)
    tags = eo(prog(t, 9.9, 10.25)) * a
    chip(cv, 'orang asing', 300, 530, tags, size=24, fg=ACC_XL); chip(cv, 'orang asing', 780, 530, tags, size=24, fg=ACC_XL)
    wa = eo(prog(t, 10.98, 11.3)) * a
    if wa > 0: waves(cv, 420, 660, 760, t, wa, HL, amp=34)
    ta = eo(prog(t, 10.98, 11.3)) * a
    if ta > 0:
        rr = skia.Path(); rr.addArc(skia.Rect(460, 330, 620, 490), -90, 360 * prog(t, 11.0, 12.4))
        cv.drawCircle(540, 410, 80, P(col('#FFFFFF', 0.1 * ta), stroke=6)); neon(cv, rr, 1, HL, 6, ta, 0.8)
        glow_text(cv, '5 menit', 540, 410, font(XB, 40), TXT, ta)

# ------------------------------------------------------------ E: menebak "seberapa suka?" (12.46 - 16.31)
def gE(cv, t):
    a = eo(prog(t, 12.5, 12.85))
    two_heads(cv, t, 12.5, a, s=0.4, y=820)
    for i, (cx, tail) in enumerate(((300, (330, 700)), (780, (750, 700)))):
        ba = eo(prog(t, 12.8 + i * 0.25, 13.2 + i * 0.25)) * a
        if ba <= 0: continue
        tb = thought_bubble_line(cx, 520, 360, 150, tail)
        neon(cv, tb, 1, ACC_L, 3, ba, 0.6)
        tracked(cv, 'DIA SUKA AKU?', cx, 478, font(MONO, 20), P(col(HL, ba)), 3)
        cv.drawLine(cx - 130, 548, cx + 130, 548, P(col('#FFFFFF', 0.2 * ba), stroke=6))
        v = 0.5 + 0.32 * math.sin(t * (3.1 + i) + i * 2) * (1 - 0.6 * prog(t, 15.4, 16.2))
        kx = cx - 130 + 260 * v
        cv.drawLine(cx - 130, 548, kx, 548, P(col(HL, ba), stroke=6))
        cv.drawCircle(kx, 548, 14, P(col(HL, 0.5 * ba), blur=8)); cv.drawCircle(kx, 548, 11, P(col('#FFFFFF', ba)))
    slam(cv, '?', 540, 1040, 160, t, 13.95, '#FFFFFF', HL, ACC, rings=False)

# ------------------------------------------------------------ F: hasil — tebakan vs kenyataan, celahnya (16.31 - 22.58)
def gF(cv, t):
    a = eo(prog(t, 16.35, 16.7)); base, top = 1110, 470
    ax = skia.Path(); ax.moveTo(200, 430); ax.lineTo(200, base); ax.lineTo(880, base)
    neon(cv, ax, eo(prog(t, 16.35, 16.9)), ACC_L, 3, a, 0.5)
    tg = eo(prog(t, 17.05, 17.9)) * 0.42; kn = eo(prog(t, 19.7, 20.7)) * 0.86
    for i, (x, v, lab, c, cc) in enumerate(((380, tg, 'TEBAKANMU', CORAL, '#FFC9BF'), (700, kn, 'KENYATAAN', MINT, '#C7F7E4'))):
        la = eo(prog(t, 16.9 + i * 0.2, 17.2 + i * 0.2)) * a
        tracked(cv, lab, x, 1150, font(MONO, 24), P(col(cc, la)), 4)
        if v <= 0.005: continue
        h = (base - top) * v; r = skia.Rect(x - 95, base - h, x + 95, base)
        bp = skia.Path(); bp.addRoundRect(r, 18, 18)
        cv.drawRoundRect(r, 18, 18, P(shader=lg(0, r.top(), 0, base, [col(c, 0.55 * a), col(c, 0.08 * a)])))
        neon(cv, bp, 1, cc, 4, a, 1.0, c)
    if tg > 0.4: glow_text(cv, 'terlalu rendah', 380, base - (base - top) * tg - 46, font(XB, 30), '#FFC9BF', eo(prog(t, 17.9, 18.2)) * a)
    ga = eo(prog(t, 21.0, 21.4)) * a
    if ga > 0:
        y1 = base - (base - top) * 0.42; y2 = base - (base - top) * 0.86
        br = skia.Path(); br.moveTo(520, y1); br.lineTo(540, y1); br.lineTo(540, y2); br.lineTo(520, y2)
        cv.drawLine(380 + 95, y1, 700 - 95, y1, P(col('#FFFFFF', 0.4 * ga), stroke=2, effect=skia.DashPathEffect.Make([10, 8], 0)))
        neon(cv, br, ga, '#FFFFFF', 4, a, 0.8, HL)
    slam(cv, 'GAP', 540, 380, 110, t, 21.0, '#FFFFFF', HL, ACC, shake=6)

# ------------------------------------------------------------ G: liking gap — sibuk menilai diri, sinyal suka terlewat (22.58 - 27.91)
SIGNALS = ['senyum', 'angguk', 'antusias']
def gG(cv, t):
    a = eo(prog(t, 22.62, 22.95))
    slam(cv, 'liking gap', 540, 395, 96, t, 22.62, '#FFFFFF', HL, ACC, rings=False)
    two_heads(cv, t, 22.7, a, s=0.38, y=800, xl=280, xr=800)
    sa = eo(prog(t, 24.04, 24.4)) * a
    if sa > 0:
        for k, (txt, dx, dy) in enumerate((('tadi garing?', -10, -150), ('salah ngomong?', 10, -40), ('aku aneh ya?', -5, 70))):
            p_ = prog(t, 24.1 + k * 0.3, 24.45 + k * 0.3)
            thought_chip(cv, txt, 270 + dx, 800 + dy, eo(p_) * a, CORAL, ('#3A2228', '#1E1418'), size=26, sc=0.7 + 0.3 * bo(p_))
        loop_arrow(cv, 270, 800, 205, t, 0.5 * sa, CORAL, spin=120, w=4)
    for k, txt in enumerate(SIGNALS):
        u = prog(t, 25.7 + k * 0.45, 27.0 + k * 0.45)
        if u <= 0 or u >= 1: continue
        x = lerp(700, 380, u); y = 640 + k * 150 + math.sin(u * 6) * 10; fa = (1 - prog(u, 0.6, 1.0)) * a
        cv.save(); cv.translate(x, y)
        ic = skia.Path()
        if k == 0: ic.moveTo(-22, -4); ic.quadTo(0, 20, 22, -4)
        elif k == 1: ic.moveTo(0, -20); ic.lineTo(0, 20); ic.moveTo(-14, 6); ic.lineTo(0, 20); ic.lineTo(14, 6)
        else: ic.addPath(heart_line(0, 0, 18))
        neon(cv, ic, 1, '#C7F7E4', 4, fa, 1.0, MINT); cv.restore()
        f = font(B, 24); w = f.measureText(txt); cv.drawString(txt, x - w / 2, bl(f, y + 42), f, P(col('#B9F5DF', fa)))
    ma = eo(prog(t, 26.2, 26.55)) * a
    if ma > 0: chip(cv, 'sinyal suka terlewat', 540, 1130, ma, size=26, fg='#B9F5DF', bgc='#173A2E', edge=MINT)

# ------------------------------------------------------------ H: teman sekamar, berbulan-bulan (27.91 - 32.15)
def gH(cv, t):
    a = eo(prog(t, 27.95, 28.3))
    chip(cv, 'teman sekamar baru', 540, 400, eo(prog(t, 28.0, 28.35)) * a, size=28, fg=ACC_XL)
    x0, x1, y0, y1 = 170, 910, 1060, 520
    ax = skia.Path(); ax.moveTo(x0, y1 - 20); ax.lineTo(x0, y0); ax.lineTo(x1, y0)
    neon(cv, ax, eo(prog(t, 28.0, 28.5)), ACC_L, 3, a, 0.5)
    d = eio(prog(t, 28.6, 31.6))
    def series(fn):
        p = skia.Path()
        for i in range(81):
            u = i / 80; (p.moveTo if i == 0 else p.lineTo)(lerp(x0, x1, u), lerp(y0, y1, fn(u)))
        return p
    real = series(lambda u: 0.72 + 0.06 * math.sin(u * 5)); guess = series(lambda u: 0.32 + 0.3 * u ** 3 + 0.04 * math.sin(u * 7))
    fill = skia.Path(); fill.addPath(partial(real, d))
    neon(cv, real, d, '#C7F7E4', 4.5, a, 1.0, MINT); neon(cv, guess, d, '#FFC9BF', 4.5, a, 1.0, CORAL)
    for txt, y, c in (('kenyataan', 0.72, '#C7F7E4'), ('tebakan', 0.34, '#FFC9BF')):
        f = font(B, 26); cv.drawString(txt, x0 + 20, bl(f, lerp(y0, y1, y) - 34), f, P(col(c, eo(prog(t, 28.7, 29.0)) * a)))
    ma = eo(prog(t, 29.6, 30.0)) * a
    for k, lab in enumerate(('bulan 1', 'bulan 3', 'bulan 6', 'bulan 8')):
        x = lerp(x0, x1, (k + 0.5) / 4); f = font(M, 22); w = f.measureText(lab)
        cv.drawString(lab, x - w / 2, bl(f, y0 + 34), f, P(col(MUTED, ma)))

# ------------------------------------------------------------ I: jangan diputar ulang; kamu lebih disukai (32.15 - 36.6)
def gI(cv, t):
    a = eo(prog(t, 32.2, 32.55))
    ra = a * (1 - eo(prog(t, 34.0, 34.3)))
    if ra > 0:
        loop_arrow(cv, 540, 640, 150, t, ra, ACC_L, spin=90, w=8)
        tri_ = skia.Path(); tri_.moveTo(515, 600); tri_.lineTo(575, 640); tri_.lineTo(515, 680); tri_.close()
        cv.drawPath(tri_, P(col(ACC_XL, ra)))
        x_ = eo(prog(t, 32.9, 33.4))
        if x_ > 0:
            cv.drawLine(400, 500, 400 + 280 * x_, 500 + 280 * x_, P(col(CORAL, 0.5 * ra), stroke=22, blur=10))
            cv.drawLine(400, 500, 400 + 280 * x_, 500 + 280 * x_, P(col(CORAL, ra), stroke=10))
    hp = prog(t, 34.2, 34.9)
    if hp > 0:
        hs = 120 * (1 + 0.04 * math.sin(t * 6)); hl = heart_line(540, 660, hs)
        rays(cv, 540, 660, 360, 0.6 * eo(hp) * a, t, n=16, c=MINT)
        neon(cv, hl, eo(hp), '#C7F7E4', 6, a, 1.2, MINT)
        if hp >= 1: cv.drawPath(hl, P(col(MINT, 0.18 * a)))
    slam(cv, 'lebih disukai', 540, 990, 104, t, 34.25, '#FFFFFF', '#9FF2D0', MINT, shake=4)

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
    ev = [(0.02, 'whoosh'), (0.35, 'rise'), (0.45, 'chop'), (0.5, 'stamp'), (1.4, 'pop'),
          (2.62, 'whoosh'), (2.9, 'swish'), (3.65, 'fizz_soft'), (4.38, 'chop'), (4.42, 'zap2'),
          (5.98, 'whoosh'), (6.1, 'swish'), (6.9, 'ding_soft'), (7.28, 'pop'),
          (9.55, 'whoosh'), (9.6, 'swish'), (9.9, 'pop'), (10.98, 'plip'),
          (12.46, 'whoosh'), (12.8, 'pop'), (13.05, 'pop'), (13.95, 'boing'),
          (16.31, 'whoosh'), (17.05, 'rise'), (17.9, 'pop'), (19.7, 'rise'), (20.6, 'ding'), (21.0, 'chop'), (21.05, 'stamp'),
          (22.58, 'whoosh'), (22.62, 'chop'), (24.1, 'pop'), (24.4, 'pop'), (24.7, 'pop'), (25.7, 'swish'), (26.15, 'swish'), (26.6, 'swish'),
          (27.91, 'whoosh'), (28.0, 'pop'), (28.6, 'rise'),
          (32.15, 'whoosh'), (32.9, 'swish'), (33.0, 'crack'), (34.2, 'shine'), (34.25, 'chop'),
          (36.6, 'whoosh'), (36.75, 'boing'), (37.1, 'shine'), (37.35, 'pop')]
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
