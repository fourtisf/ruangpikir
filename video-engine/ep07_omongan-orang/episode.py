#!/usr/bin/env python3
"""Ruang Pikir reel #7: 'Omongan orang, kok kepikiran terus?' (sociometer, Leary dkk. 1995; Savitsky, Epley & Gilovich 2001)
Gaya "HUD / alat ukur": dasbor instrumen futuristik (alat ukur jarum "sociometer", jam 24 jam, kartu arsip, slider sensitivitas),
teks mono, sudut bingkai HUD, sapuan radar samar di latar.
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
b.GROUPS = [(0.0, 4.43, 'A'), (4.43, 7.3, 'B'), (7.3, 11.9, 'C'), (11.9, 15.15, 'D'), (15.15, 17.31, 'E1'), (17.31, 20.24, 'E2'),
            (20.24, 22.95, 'F'), (22.95, 25.98, 'G1'), (25.98, 29.94, 'G2'), (29.94, 32.38, 'H'), (32.38, 36.6, 'I'), (36.6, 42.0, 'J')]
PHRASES = [(0.15, 'Di kepalamu ada [alat ukur]'), (1.62, 'yang terus [menilai]:'), (2.73, 'orang lain [suka kamu],'), (3.7, 'atau [nggak].'),
           (4.43, 'Makanya satu [komentar kecil],'), (5.75, 'bisa [kepikiran seharian].'),
           (7.3, 'Tahun [1995],'), (9.03, 'psikolog [Mark Leary]'), (10.53, 'menyebutnya [sociometer].'),
           (11.9, '[Harga dirimu] naik turun,'), (13.31, 'ikut seberapa kamu [merasa diterima].'),
           (15.15, 'Dulu,'), (15.91, '[dikucilkan] kelompok itu [bahaya].'), (17.31, 'Makanya [ditolak sedikit],'), (18.61, 'otak bereaksi mirip [rasa sakit].'),
           (20.24, 'Masalahnya,'), (21.28, 'alat ukur ini sering [kelewat sensitif].'),
           (22.95, 'Tahun [2001],'), (24.47, '[Savitsky] dan timnya menemukan:'), (25.98, 'kalau kita [salah] di depan orang,'),
           (27.77, 'mereka nggak menilai [seburuk yang kita kira].'),
           (29.94, 'Kita yang terlalu fokus ke [kesalahan sendiri].'),
           (32.38, 'Jadi kalau [omongan orang] kepikiran lagi,'), (34.48, 'ingat: alat ukurmu memang [suka lebay].'),
           (36.6, 'Follow [Ruang Pikir],'), (38.0, 'biar makin kenal [isi kepalamu].')]
b.CAPS = [(t, s, '') for t, s in PHRASES]          # dipakai base hanya untuk jadwal

# ------------------------------------------------------------ chrome gaya sinematik
b.draw_tag = lambda cv, t: None
b.draw_progress = lambda cv, t: None
def draw_title(cv, t):
    a = eo(prog(t, 0.05, 0.35)) * (1 - eio(prog(t, 6.55, 7.0)))
    if a <= 0: return
    segs = parse("Omongan orang, [kok kepikiran terus]?"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 232) + (1 - eo(prog(t, 0.05, 0.35))) * 16 - 10 * eio(prog(t, 6.55, 7.0))
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
    # cincin HUD samar + sapuan radar pelan (tanpa titik/bokeh)
    for rr in (330, 480, 630): cv.drawCircle(540, 760, rr, P(col(ACC_L, 0.045), stroke=1.2))
    cv.save(); cv.translate(540, 760); cv.rotate(t * 24)
    wedge = skia.Path(); wedge.moveTo(0, 0); wedge.arcTo(skia.Rect(-700, -700, 700, 700), -40, 40, False); wedge.close()
    cv.drawPath(wedge, P(shader=skia.GradientShader.MakeSweep(0, 0, [col(ACC, 0), col(ACC, 0), col(ACC, 0.035)], [0, 320 / 360, 1])))
    cv.restore()
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

# ------------------------------------------------------------ A: HOOK — alat ukur di kepala (0 - 4.43)
def v_hook(t):
    wild = 0.8 * math.sin(t * 9.5) * math.cos(t * 3.1) + 0.18 * math.sin(t * 27)
    weigh = 0.45 * math.sin((t - 1.62) * 5.5)
    if t < 2.73: return lerp(wild, weigh, eio(prog(t, 1.45, 1.85)))
    if t < 3.7: return lerp(0.45 * math.sin(1.11 * 5.5), 0.86, bo(prog(t, 2.73, 3.05)))
    return lerp(0.86, -0.88, bo(prog(t, 3.7, 3.98))) + 0.03 * math.sin(t * 40) * (1 - prog(t, 3.98, 4.6))

def gA(cv, t):
    gx, gy = 540, 650
    z = 1 + 0.42 * eio(prog(t, 1.3, 2.2)); sx = shake(t, 3.7, 12)
    cv.save(); cv.translate(gx + sx, gy); cv.scale(z, z); cv.translate(-gx, -gy)
    ha = 1 - eio(prog(t, 1.5, 2.1))
    if ha > 0:
        head = head_line(530, 735, 1.12)
        cv.drawPath(head, P(shader=rg(540, 640, 420, [col('#2A2F66', 0.35 * ha), col('#2A2F66', 0)])))
        neon(cv, head, eo(prog(t, -0.2, 0.45)), ACC_XL, 4, ha)
    gauge(cv, gx, gy, 185, v_hook(t), 1.0, t, eo(prog(t, -0.25, 0.5)), bump(prog(t, 3.7, 4.5)))
    cv.restore()
    sa = prog(t, 2.73, 3.3)
    if 0 < sa < 1: rays(cv, gx, gy, 520, bump(sa), t, n=16, c=MINT)
    sp = prog(t, 0.0, 0.7)
    if 0 < sp < 1: scanline(cv, 110, 970, lerp(290, 1190, eio(sp)), 1 - 0.5 * sp)
    for tx, ty, txt, c, t0 in ((815, 360, '+1 suka', MINT, 0.2), (250, 430, 'dilihat', ACC_L, 0.5), (850, 980, 'komentar baru', CORAL, 0.8)):
        pa = prog(t, t0, t0 + 0.3); out = 1 - eio(prog(t, 1.3, 1.6))
        if pa > 0 and out > 0:
            s = lerp(0.6, 1.0, bo(pa)); cv.save(); cv.translate(tx, ty); cv.scale(s, s)
            chip(cv, txt, 0, 0, clamp(pa * 2) * out, size=28, fg=c, edge=c); cv.restore()

# ------------------------------------------------------------ B: satu komentar kecil, kepikiran seharian (4.43 - 7.3)
ECHO = [(10.2, 200, 690), (14.6, 880, 740), (19.1, 200, 1000), (23.8, 880, 1050)]
def gB(cv, t):
    hour = 8 + 24 * eio(prog(t, 5.75, 7.6))
    ka = eo(prog(t, 5.55, 6.0))
    clock24(cv, 540, 880, 215 * lerp(0.85, 1, ka), hour, ka)
    for h, x, y in ECHO:
        ea = eo(prog(hour, h, h + 1.2))
        if ea > 0:
            mono(cv, f'{int(h) % 24:02d}.{int((h % 1) * 60):02d}', x, y - 50, 20, CORAL, 0.8 * ea)
            comment(cv, 'kamu kok gitu sih?', x, y, 0.75 * ea, lerp(0.7, 1.0, bo(ea)), size=21)
    ma = eo(prog(t, 4.45, 4.8)) * (1 - eio(prog(t, 5.35, 5.7)))
    if ma > 0:
        mv = lerp(0.55, -0.78, bo(prog(t, 4.62, 4.95))) + (0.04 * math.sin(t * 30) if t > 4.62 else 0)
        gauge(cv, 540, 905, 150, mv, ma, t, ma, 0.8 * clamp(prog(t, 4.7, 4.8)), label=None)
    rp = prog(t, 4.6, 5.4)
    if 0 < rp < 1:
        for k in range(2):
            u = clamp(rp * 1.3 - k * 0.3)
            if 0 < u < 1: cv.drawRoundRect(skia.Rect(540 - 330 - 140 * u, 560 - 70 - 80 * u, 540 + 330 + 140 * u, 560 + 70 + 80 * u), 80, 80, P(col(CORAL, 0.6 * (1 - u)), stroke=3))
    ca = prog(t, 4.43, 4.85); my = lerp(560, 470, eio(prog(t, 5.5, 6.0))); ms = lerp(1.0, 0.86, eio(prog(t, 5.5, 6.0)))
    pulse = max([bump(prog(hour, h, h + 1.2)) for h, _, _ in ECHO] + [0])
    comment(cv, 'kamu kok gitu sih?', 540 + shake(t, 4.62, 8, 0.4), my, clamp(ca * 2), lerp(0.6, 1.0, bo(ca)) * ms, size=40, glow=0.3 + 0.7 * pulse)
    mono(cv, 'KOMENTAR KECIL', 540, my - 92 * ms, 22, ACC_L, 0.7 * eo(prog(t, 4.8, 5.1)) * (1 - eio(prog(t, 5.5, 5.8))), sp=4)

# ------------------------------------------------------------ C: riset 1995, sociometer (7.3 - 11.9)
def gC(cv, t):
    ca = 1 - eio(prog(t, 10.25, 10.6))
    if ca > 0:
        cv.save(); s = lerp(1, 0.85, eio(prog(t, 10.25, 10.6))); cv.translate(540, 680); cv.scale(s, s); cv.translate(-540, -680)
        file_card(cv, t, 7.3, '1995', 'Mark Leary dkk.', 'Journal of Personality and Social Psychology', ca); cv.restore()
    if t >= 10.5:
        ga = eo(prog(t, 10.5, 10.9))
        gauge(cv, 540, 470, 120, 0.5 * math.sin((t - 10.5) * 2.4), ga, t, eo(prog(t, 10.5, 11.0)), label=None, read=None, ends=False)
        slam(cv, 'SOCIOMETER', 540, 790, 118, t, 10.53, '#FFFFFF', HL, ACC, shake=6)
        f = font(XB, 118); wS = f.measureText('SOCIO'); wT = f.measureText('SOCIOMETER'); x0 = 540 - wT / 2
        for k, (x_a, x_b, lab, c, t0) in enumerate(((x0, x0 + wS, 'sosial', ACC_L, 11.0), (x0 + wS, x0 + wT, 'alat ukur', MINT, 11.25))):
            u = eo(prog(t, t0, t0 + 0.35))
            if u > 0:
                y = 880; xm = (x_a + x_b) / 2; hw = (x_b - x_a) / 2 - 10
                p = skia.Path(); p.moveTo(xm - hw * u, y - 12); p.lineTo(xm - hw * u, y); p.lineTo(xm + hw * u, y); p.lineTo(xm + hw * u, y - 12)
                cv.drawPath(p, P(col(c, 0.9 * u), stroke=3))
                mono(cv, lab, xm, y + 44, 34, c, u, glow=0.5)

# ------------------------------------------------------------ D: harga diri ikut seberapa diterima (11.9 - 15.15)
PEOPLE = [(235, 520), (205, 780), (235, 1040), (845, 520), (875, 780), (845, 1040)]
def accept(k, t):
    on = eo(prog(t, 12.0 + k * 0.17, 12.3 + k * 0.17))
    if k == 1: on *= 1 - eio(prog(t, 13.4, 13.75))
    if k == 4: on *= 1 - eio(prog(t, 13.6, 13.95)) * (1 - eio(prog(t, 14.4, 14.75)))
    if k == 2: on *= 1 - eio(prog(t, 13.8, 14.15))
    return on
def gD(cv, t):
    a0 = eo(prog(t, 11.9, 12.3)); acc = [accept(k, t) for k in range(6)]
    lvl = 0.12 + 0.8 * sum(acc) / 6
    r = skia.Rect(490, 470, 590, 1010)
    for k, (x, y) in enumerate(PEOPLE):
        u = acc[k]; gone = (1 - u) * (1 if eo(prog(t, 12.0 + k * 0.17, 12.3 + k * 0.17)) >= 1 else 0)
        dx = (-1 if x < 540 else 1) * 40 * gone; c = mixc(MINT, CORAL, gone) if gone else mixc(ACC_L, MINT, u)
        ty = lerp(r.bottom(), r.top(), lvl); xx = r.left() if x < 540 else r.right()
        lp_ = skia.Path(); lp_.moveTo(x + dx + (45 if x < 540 else -45), y); lp_.cubicTo((x + xx) / 2, y, (x + xx) / 2, ty, xx, ty)
        cv.drawPath(lp_, P(col(c, (0.15 + 0.55 * u) * a0), stroke=2.5 if u > 0.5 else 1.5))
        mini_person(cv, x + dx, y, 70, c, a0 * (1 - 0.45 * gone), u)
        if u > 0.6: check_mark(cv, x + dx + 42, y - 52, 14, prog(u, 0.6, 1.0), a0)
        if gone > 0.1: cross(cv, x + dx + 42, y - 52, 12, a0 * gone, CORAL, 5)
    glass(cv, r, rad=50, a=a0)
    fh = (r.height() - 20) * lvl; fr = skia.Rect(r.left() + 10, r.bottom() - 10 - fh, r.right() - 10, r.bottom() - 10)
    fc = vcol(lvl * 2 - 1)
    cv.drawRoundRect(fr, 40, 40, P(col(fc, 0.55 * a0), blur=18))
    cv.drawRoundRect(fr, 40, 40, P(shader=lg(0, fr.top(), 0, fr.bottom(), [col(mixc(fc, '#FFFFFF', 0.4), a0), col(fc, a0)])))
    for k in range(1, 10):
        y = lerp(r.bottom(), r.top(), k / 10); cv.drawLine(r.right() - 26, y, r.right() - 10, y, P(col('#FFFFFF', 0.35 * a0), stroke=2))
    mono(cv, 'HARGA DIRI', 540, 420, 26, ACC_L, 0.85 * a0, sp=4)
    mono(cv, f'{int(round(lvl * 100))}%', 540, 1075, 46, fc, a0, glow=0.6)

# ------------------------------------------------------------ E1: dulu, dikucilkan kelompok itu bahaya (15.15 - 17.31)
GROUP = [(330, 900), (420, 790), (660, 790), (750, 900)]
def gE1(cv, t):
    a0 = eo(prog(t, 15.15, 15.5))
    mono(cv, 'ZAMAN DULU', 540, 360, 28, AMBER, 0.85 * a0, sp=8)
    flame(cv, 540, 930, 62, t, a0)
    for x, y in GROUP: mini_person(cv, x, y, 82, AMBER, a0, 0.6)
    u = eio(prog(t, 15.9, 16.6))
    yx, yy = lerp(540, 885, u), lerp(1040, 600, u); dark = u
    if dark > 0: cv.drawCircle(yx, yy, 200, P(shader=rg(yx, yy, 200, [col(CORAL, 0.16 * dark), col(CORAL, 0)])))
    mini_person(cv, yx, yy, 82, mixc(AMBER, CORAL, dark), a0 * (1 - 0.35 * dark), 0.6 * (1 - dark) + 0.3 * dark)
    ra = eo(prog(t, 16.0, 16.4))
    if ra > 0:
        p = skia.Path(); p.addOval(skia.Rect(225, 690, 855, 1050))
        cv.drawPath(partial(p, ra), P(col(AMBER, 0.5 * a0), stroke=2.5))
        mono(cv, 'KELOMPOK', 540, 1085, 22, AMBER, 0.75 * ra * a0, sp=4)
    wa = prog(t, 16.65, 16.95)
    if wa > 0:
        s = bo(wa); fl = 0.75 + 0.25 * math.sin(t * 20)
        cv.save(); cv.translate(yx, yy - 150); cv.scale(s, s); warn_tri(cv, 0, 0, 44, a0 * fl); cv.restore()
        mono(cv, 'BAHAYA', yx, yy + 120, 30, CORAL, a0 * clamp(wa * 2), sp=5, glow=0.6)

# ------------------------------------------------------------ E2: ditolak sedikit -> otak bereaksi mirip rasa sakit (17.31 - 20.24)
def gE2(cv, t):
    a0 = eo(prog(t, 17.31, 17.7)); hx, hy, hs = 540, 790, 0.86
    head = head_line(hx, hy, hs)
    cv.save(); cv.translate(shake(t, 17.75, 10, 0.45), 0)
    cv.drawPath(head, P(shader=rg(540, 700, 380, [col('#2A2F66', 0.35 * a0), col('#2A2F66', 0)])))
    neon(cv, head, eo(prog(t, 17.31, 17.8)), ACC_XL, 4, a0)
    sx, sy = 520, 690; pa = prog(t, 17.8, 18.3)
    if pa > 0:
        pu = 0.75 + 0.25 * math.sin(t * 9)
        cv.drawCircle(sx, sy, 150, P(shader=rg(sx, sy, 150, [col(CORAL, 0.75 * eo(pa) * pu), col(CORAL, 0.25 * eo(pa)), col(CORAL, 0)], [0, 0.4, 1])))
        cv.drawCircle(sx, sy, 34, P(col('#FFD1C8', 0.9 * eo(pa))))
        for k in range(3):
            u = ((t - 17.8) * 0.9 + k / 3) % 1.0
            cv.drawCircle(sx, sy, 40 + 230 * u, P(col(CORAL, 0.55 * (1 - u) * eo(pa)), stroke=3))
    cv.restore()
    ca = prog(t, 17.31, 17.75); co = 1 - eio(prog(t, 18.3, 18.6))
    if ca > 0 and co > 0:
        cx_ = lerp(1150, 650, eio(ca)); comment(cv, 'kamu nggak usah ikut ya', cx_, 470, co, lerp(0.8, 1.0, eo(ca)) * lerp(1, 0.9, 1 - co), size=32, av=CORAL, glow=0.3)
    la = eo(prog(t, 18.6, 19.0))
    if la > 0:
        cv.drawLine(sx, sy - 40, sx, 520 - 10 + 30 * (1 - la), P(col(CORAL, 0.7 * la), stroke=2.5))
        mono(cv, 'SINYAL MIRIP RASA SAKIT', 540, 470, 32, CORAL, la, sp=2, glow=0.6)
        mono(cv, 'Eisenberger dkk. (2003), Science', 540, 412, 21, ACC_L, 0.7 * la)

# ------------------------------------------------------------ F: alat ukurnya kelewat sensitif (20.24 - 22.95)
def v_sens(t):
    if t < 20.75: return 0.35 + 0.04 * math.sin(t * 5)
    return lerp(0.35, -1.0, bo(prog(t, 20.75, 21.05))) + 0.05 * math.sin(t * 38)
def slider(cv, y, val, a=1.0, t=0.0, maxflash=0.0):
    if a <= 0: return
    x0, x1 = 400, 930
    mono(cv, 'SENSITIVITAS', 150, y, 26, ACC_L, 0.85 * a, sp=2, align=0)
    cv.drawRoundRect(skia.Rect(x0, y - 9, x1, y + 9), 9, 9, P(col('#1A1B30', 0.95 * a))); cv.drawRoundRect(skia.Rect(x0, y - 9, x1, y + 9), 9, 9, P(col(ACC_L, 0.25 * a), stroke=2))
    xk = lerp(x0, x1, val); c = vcol(1 - 2 * val) if val > 0.5 else ACC
    cv.drawRoundRect(skia.Rect(x0, y - 9, xk, y + 9), 9, 9, P(shader=lg(x0, 0, x1, 0, [col(ACC, a), col(CORAL, a)])))
    cv.drawCircle(xk, y, 26, P(col(c, 0.6 * a), blur=14)); cv.drawCircle(xk, y, 22, P(col('#FFFFFF', a))); cv.drawCircle(xk, y, 22, P(col(c, a), stroke=4))
    if maxflash > 0: mono(cv, 'MAKS', x1, y - 52, 30, CORAL, maxflash * (0.7 + 0.3 * math.sin(t * 24)), sp=3, align=1, glow=0.8)
def gF(cv, t):
    a0 = eo(prog(t, 20.24, 20.6)); al = clamp(prog(t, 20.85, 21.0)) * (0.6 + 0.4 * eio(prog(t, 21.3, 22.4)))
    cv.save(); cv.translate(shake(t, 20.8, 12), 0)
    gauge(cv, 540, 690, 230, v_sens(t), a0, t, eo(prog(t, 20.24, 20.7)), al)
    cv.restore()
    ca = prog(t, 20.45, 20.75)
    if ca > 0:
        s = lerp(0.6, 1, bo(ca)); cv.save(); cv.translate(540, 335); cv.scale(s, s)
        chip(cv, 'cuma dibaca', -20, 0, clamp(ca * 2) * a0, size=30, fg=ACC_XL)
        f = font(B, 30); w = f.measureText('cuma dibaca'); ck = P(col('#7FB8FF', clamp(ca * 2) * a0), stroke=4)
        for k in range(2):
            x = w / 2 + 2 + k * 14; cv.drawLine(x - 10, 2, x - 3, 9, ck); cv.drawLine(x - 3, 9, x + 9, -6, ck)
        cv.restore()
    wa = prog(t, 20.9, 21.15)
    if wa > 0:
        cv.save(); cv.translate(858, 440); cv.scale(bo(wa), bo(wa)); warn_tri(cv, 0, 0, 34, a0 * (0.7 + 0.3 * math.sin(t * 20))); cv.restore()
    sa = eo(prog(t, 21.2, 21.5))
    slider(cv, 1085, lerp(0.5, 1.0, eio(prog(t, 21.4, 22.2))), sa * a0, t, eo(prog(t, 22.3, 22.5)))

# ------------------------------------------------------------ G1: riset 2001 (22.95 - 25.98)
def gG1(cv, t):
    file_card(cv, t, 22.95, '2001', 'Savitsky, Epley & Gilovich', 'Journal of Personality and Social Psychology')

# ------------------------------------------------------------ G2: salah di depan orang; mereka nggak menilai seburuk itu (25.98 - 29.94)
def gG2(cv, t):
    sa = eo(prog(t, 25.98, 26.35)) * (1 - eio(prog(t, 27.55, 27.9)))
    if sa > 0:
        bad = eo(prog(t, 26.75, 26.95))
        for k, ch in enumerate('HALSA'):
            tp = eo(prog(t, 26.0 + k * 0.06, 26.3 + k * 0.06))
            tile(cv, ch, 300 + k * 120 + shake(t, 26.8, 9, 0.4), 520 + (1 - tp) * 30, 100, sa * tp, bad)
        cross(cv, 540, 700, 50, sa, CORAL, 14, prog(t, 26.8, 27.15))
        mono(cv, 'GAGAL', 540, 790, 34, CORAL, sa * eo(prog(t, 27.0, 27.2)), sp=6, glow=0.6)
        neon(cv, head_line(250, 1010, 0.3, 1), eo(prog(t, 26.0, 26.5)), ACC_XL, 3, sa, 0.7)
        for k, x in enumerate((640, 790, 940)):
            neon(cv, head_line(x, 1010 - (k % 2) * 20, 0.26, -1), eo(prog(t, 26.1 + k * 0.08, 26.6 + k * 0.08)), ACC_L, 3, sa * 0.85, 0.6)
        mono(cv, 'PENONTON', 790, 1130, 22, ACC_L, 0.7 * sa, sp=4)
    ga = eo(prog(t, 27.6, 28.0))
    if ga > 0:
        vl = lerp(0.0, -0.88, bo(prog(t, 27.8, 28.3))); vr = lerp(0.0, -0.12, eo(prog(t, 28.1, 28.6))) + 0.03 * math.sin(t * 4)
        gauge(cv, 290, 720, 165, vl, ga, t, eo(prog(t, 27.6, 28.0)), 0.6 * prog(t, 28.3, 28.5), label='KITA KIRA', read='PENILAIAN', pct='PARAH', pc=CORAL)
        gauge(cv, 790, 720, 165, vr, ga, t, eo(prog(t, 27.75, 28.15)), label='KENYATAAN', read='PENILAIAN', pct='BIASA', pc=ACC_XL)
        mono(cv, 'vs', 540, 720, 40, ACC_L, ga * 0.8)

# ------------------------------------------------------------ H: kita yang terlalu fokus ke kesalahan sendiri (29.94 - 32.38)
def gH(cv, t):
    a0 = eo(prog(t, 29.94, 30.3)); r = skia.Rect(250, 560, 830, 840)
    glass(cv, r, rad=26, a=a0)
    for k, wl in enumerate((0.85, 0.7, 0.9, 0.55)):
        y = r.top() + 62 + k * 56; cv.drawRoundRect(skia.Rect(r.left() + 50, y - 9, r.left() + 50 + (r.width() - 100) * wl, y + 9), 9, 9, P(col(ACC_L, 0.22 * a0)))
    ex, ey = 640, r.top() + 118; cross(cv, ex, ey, 9, a0, CORAL, 4)
    lk = eio(prog(t, 30.2, 30.8))
    bx = skia.Rect(lerp(r.left() - 20, ex - 40, lk), lerp(r.top() - 20, ey - 40, lk), lerp(r.right() + 20, ex + 40, lk), lerp(r.bottom() + 20, ey + 40, lk))
    brackets(cv, bx, a0 * (1 - eio(prog(t, 30.9, 31.1))), CORAL if lk >= 1 else ACC_L, 30, 3)
    la = eo(prog(t, 30.85, 31.25))
    if la > 0:
        lx, ly, lr = ex, ey + 60 * (1 - la), 150 * bo(la) if la < 1 else 150
        lr = max(1, lr); pth = skia.Path(); pth.addCircle(lx, ly, lr)
        cv.drawCircle(lx, ly, lr, P(col(CORAL, 0.4 * la), blur=30))
        cv.drawCircle(lx, ly, lr, P(shader=rg(lx, ly - lr * 0.3, lr * 1.3, [col('#2A1C2E', 0.96 * la), col('#140E1A', 0.96 * la)])))
        cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True); cross(cv, lx, ly, 70, la, CORAL, 20); cv.restore()
        cv.drawCircle(lx, ly, lr, P(col(ACC_XL, 0.9 * la), stroke=5))
        hx, hy = lx + lr * 0.72, ly + lr * 0.72; cv.drawLine(hx, hy, hx + 90, hy + 90, P(col(ACC_XL, 0.9 * la), stroke=18))
        mono(cv, 'FOKUS: KESALAHAN', 540, 400, 30, CORAL, la, sp=3, glow=0.6)
        mono(cv, 'x10', lx - lr - 20, ly - lr + 10, 26, ACC_L, 0.8 * la, align=1)
    for k, (x, txt) in enumerate(((240, 'laper'), (540, 'tugas numpuk'), (840, 'chat doi'))):
        pa = eo(prog(t, 31.0 + k * 0.17, 31.35 + k * 0.17))
        if pa > 0:
            neon(cv, head_line(x, 1085, 0.2, 1 if k != 2 else -1), pa, ACC_L, 3, 0.85 * pa, 0.6)
            chip(cv, txt, x, 975 + (1 - pa) * 14, pa, size=24, fg=ACC_XL)

# ------------------------------------------------------------ I: omongan orang kepikiran lagi -> alat ukurmu suka lebay (32.38 - 36.6)
COMS = [('kok gitu sih?', 250, 380, -6, 32.5), ('hmm.', 860, 470, 5, 32.85), ('kamu beda ya', 220, 1000, 4, 33.2), ('serius?', 870, 960, -5, 33.55)]
def v_calm(t):
    hits = sum(0.5 * bump(prog(t, t0 + 0.1, t0 + 0.45)) for _, _, _, _, t0 in COMS)
    v = lerp(-0.2, -0.75, eio(prog(t, 32.5, 33.8))) - hits * 0.4 + 0.06 * math.sin(t * 31) * (1 - prog(t, 34.6, 35.0))
    return lerp(v, 0.15 + 0.03 * math.sin(t * 2.5), eio(prog(t, 34.6, 35.4)))
def gI(cv, t):
    a0 = eo(prog(t, 32.38, 32.75)); calm = eio(prog(t, 34.6, 35.4))
    al = clamp(prog(t, 32.6, 32.8)) * (1 - calm)
    gauge(cv, 540, 690, 225, v_calm(t), a0, t, eo(prog(t, 32.38, 32.8)), al * 0.8)
    for txt, x, y, rot, t0 in COMS:
        pa = prog(t, t0, t0 + 0.3); out = 1 - eio(prog(t, 34.55, 35.0))
        if pa > 0 and out > 0:
            sx_ = lerp(x + (-200 if x < 540 else 200), x, eo(pa))
            comment(cv, txt, sx_, y, clamp(pa * 2) * out * a0, lerp(0.7, 1, bo(pa)) * lerp(0.8, 1, out), size=28, rot=rot)
    sa = eo(prog(t, 34.4, 34.7))
    slider(cv, 1085, lerp(1.0, 0.4, eio(prog(t, 34.6, 35.3))), sa * a0, t)
    stamp(cv, 'LEBAY', 540, 600, 104, t, 35.55, CORAL, -9, a0)


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

b.DRAWERS = [gA, gB, gC, gD, gE1, gE2, gF, gG1, gG2, gH, gI, gJ]

def build_sfx():
    ev = [(0.02, 'whoosh'), (0.05, 'zap'), (0.2, 'pop'), (0.5, 'plip'), (0.8, 'pop'), (1.3, 'zoom'), (1.62, 'tick'), (2.0, 'tick'), (2.4, 'tick'),
          (2.73, 'rise'), (3.0, 'ding_soft'), (3.7, 'chop'), (3.72, 'buzzer'),
          (4.43, 'whoosh'), (4.6, 'plop'), (4.62, 'crack'), (5.6, 'swish'), (5.8, 'clock'), (6.1, 'pop'), (6.45, 'pop'), (6.8, 'pop'), (7.15, 'pop'),
          (7.3, 'whoosh'), (7.35, 'card'), (7.5, 'zap2'), (8.5, 'ding_soft'), (10.53, 'chop'), (10.56, 'stamp'), (11.0, 'plip'), (11.25, 'plip'),
          (11.9, 'whoosh'), (12.0, 'pop'), (12.17, 'pop'), (12.34, 'pop'), (12.51, 'pop'), (12.68, 'pop'), (12.85, 'ding_soft'),
          (13.4, 'zap2'), (13.6, 'zap2'), (13.8, 'zap2'), (14.4, 'plip'),
          (15.15, 'whoosh'), (15.2, 'fizz_soft'), (15.9, 'swish'), (16.65, 'beep'), (16.95, 'beep'),
          (17.31, 'whoosh'), (17.45, 'swish'), (17.75, 'crack'), (17.8, 'heart'), (18.3, 'heart'), (18.8, 'heart'), (18.6, 'ding_soft'),
          (20.24, 'whoosh'), (20.45, 'pop'), (20.8, 'chop'), (20.85, 'buzzer'), (21.4, 'rise'), (22.3, 'beep'),
          (22.95, 'whoosh'), (23.0, 'card'), (23.1, 'zap2'), (24.2, 'ding_soft'),
          (25.98, 'whoosh'), (26.0, 'plip'), (26.12, 'plip'), (26.24, 'plip'), (26.8, 'buzzer'), (27.0, 'stamp'),
          (27.6, 'whoosh'), (28.0, 'boing'), (28.4, 'ding_soft'),
          (29.94, 'whoosh'), (30.2, 'zoom'), (30.8, 'tick'), (30.9, 'pop'), (31.0, 'plip'), (31.17, 'plip'), (31.34, 'plip'),
          (32.38, 'whoosh'), (32.5, 'plop'), (32.85, 'plop'), (33.2, 'plop'), (33.55, 'plop'), (32.7, 'buzzer'),
          (34.6, 'swish'), (35.0, 'shine'), (35.55, 'chop'), (35.58, 'stamp'),
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

