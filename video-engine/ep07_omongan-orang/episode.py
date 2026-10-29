#!/usr/bin/env python3
"""Ruang Pikir reel #7: 'Omongan orang, kok kepikiran terus?' (sociometer, Leary dkk. 1995; Savitsky, Epley & Gilovich 2001)
Gaya "dunia 3D + UI medsos": ponsel & kartu kaca miring dalam perspektif (plane_m/plane), komentar yang berputar
mengelilingi kepala (orbit), teks 3D (extrude), alat ukur fisik, alarm asap yang kelewat sensitif, kartu riset yang berputar.
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
b.GROUPS = [(0.0, 4.19, 'A'), (4.19, 8.11, 'B'), (8.11, 12.82, 'C'), (12.82, 16.13, 'D'), (16.13, 17.86, 'E1'), (17.86, 20.67, 'E2'),
            (20.67, 23.05, 'F'), (23.05, 26.12, 'G1'), (26.12, 30.18, 'G2'), (30.18, 32.67, 'H'), (32.67, 36.6, 'I'), (36.6, 42.0, 'J')]
PHRASES = [(0.15, 'Satu [komentar kecil]'), (1.05, 'bisa [kepikiran seharian].'), (2.62, 'Itu [bukan karena kamu lemah].'),
           (4.19, 'Di kepalamu ada [alat ukur]'), (5.51, 'yang terus [menilai]:'), (6.49, 'kamu [disukai],'), (7.27, 'atau [nggak].'),
           (8.11, 'Tahun [1995],'), (9.71, 'psikolog [Mark Leary] menyebutnya [sociometer].'),
           (12.82, '[Harga dirimu] naik turun,'), (14.27, 'ikut seberapa kamu [merasa diterima].'),
           (16.13, 'Dulu,'), (16.62, '[dikucilkan] itu [bahaya].'), (17.86, 'Jadi [ditolak sedikit],'), (18.96, 'otak bereaksi mirip [rasa sakit].'),
           (20.67, 'Masalahnya,'), (21.45, 'alat ukur ini [kelewat sensitif].'),
           (23.05, 'Tahun [2001],'), (24.32, '[Savitsky] dan timnya menemukan:'), (26.12, 'kalau kita [salah] di depan orang,'),
           (27.87, 'mereka nggak menilai [seburuk yang kita kira].'),
           (30.18, 'Kita yang terlalu fokus ke [kesalahan sendiri].'),
           (32.67, 'Jadi kalau [omongan orang] kepikiran lagi,'), (34.59, 'ingat: alat ukurmu [suka lebay].'),
           (36.6, 'Follow [Ruang Pikir],'), (37.94, 'biar makin kenal [isi kepalamu].')]
b.CAPS = [(t, s, '') for t, s in PHRASES]          # dipakai base hanya untuk jadwal

# ------------------------------------------------------------ chrome gaya sinematik
b.draw_tag = lambda cv, t: None
b.draw_progress = lambda cv, t: None
def draw_title(cv, t):
    a = eo(prog(t, 0.05, 0.35)) * (1 - eio(prog(t, 3.75, 4.15)))
    if a <= 0: return
    segs = parse("Omongan orang, [kok kepikiran terus]?"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 232) + (1 - eo(prog(t, 0.05, 0.35))) * 16 - 10 * eio(prog(t, 3.75, 4.15))
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

def research_card(cv, t, t0, year, names, journal, back=None, t_flip=None, y=700, t_out=None):
    """kartu riset kaca yang berputar masuk dalam 3D; bisa dibalik (t_flip) untuk menampilkan sisi belakang"""
    p = prog(t, t0, t0 + 0.7)
    if p <= 0: return
    ry = lerp(80, 0, bo(p)) + 5 * math.sin((t - t0) * 0.9); rx = 5 * math.sin((t - t0) * 0.7 + 0.5); z = lerp(600, 0, eo(p))
    if t_flip: ry += 180 * eio(prog(t, t_flip, t_flip + 0.6))
    if t_out: z += 900 * ei(prog(t, t_out, t_out + 0.5))
    w, h = 780, 540; a = clamp(p * 2.5)
    with plane(cv, 540, y, z, w, h, ry, rx) as ok:
        if not ok: return
        r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
        if facing(ry, rx) >= 0:
            pth = glass(cv, r, rad=34, a=a, glow=0.35)
            mono(cv, 'ARSIP RISET', r.left() + 54, r.top() + 60, 25, ACC_L, 0.85 * a, sp=4, align=0)
            mono(cv, 'JPSP', r.right() - 54, r.top() + 60, 25, MINT, 0.8 * a, sp=3, align=1)
            cv.drawLine(r.left() + 54, r.top() + 102, r.right() - 54, r.top() + 102, P(col(ACC_L, 0.25 * a), stroke=2))
            extrude(cv, year, 0, r.top() + 228, 170, a * eo(prog(t, t0 + 0.25, t0 + 0.6)), depth=14)
            na = eo(prog(t, t0 + 0.5, t0 + 0.9))
            f = font(XB, 44); ww = f.measureText(names); cv.drawString(names, -ww / 2, bl(f, r.top() + 385) + (1 - na) * 12, f, P(col(TXT, na * a)))
            f = font(M, 27); ww = f.measureText(journal); cv.drawString(journal, -ww / 2, bl(f, r.top() + 445), f, P(col(ACC_L, 0.85 * na * a)))
            sheen(cv, pth, r, prog(t, t0 + 0.6, t0 + 1.5), a)
        elif back:
            cv.scale(-1, 1); back(cv, r, a)

# ------------------------------------------------------------ A: HOOK — satu komentar, diputar ulang seharian (0 - 4.19)
HOOK_TXT = 'kamu kok gitu sih?'
def ph_banner(t): return prog(t, 0.02, 0.24)
def phone_m(t):
    sink = eio(prog(t, 0.55, 1.25)); vib = 8 * math.sin(t * 95) * (1 - prog(t, 0.05, 0.6))
    return (540 + vib, 760 + 160 * sink, 700 * sink, 420, 840, -18 + 5 * math.sin(t * 1.4), 10 + 25 * sink)
def spin_A(t):
    # sudut putaran: makin cepat 1.3 -> 2.62, berhenti mendadak di 2.62
    tt = min(t, 2.62) - 1.25
    return 0.0 if tt <= 0 else 1.2 * tt + 2.6 * tt * tt
def counter_A(t):
    tt = clamp((min(t, 2.62) - 1.3) / 1.32); return int(round(1 + 98 * tt ** 1.7))
def gA(cv, t):
    push = 1 + 0.05 * eio(prog(t, 0, 3.0)) + 1.6 * ei(prog(t, 3.55, 4.6))
    cv.save(); cv.translate(540, 790); cv.scale(push, push); cv.translate(-540, -790)
    pa = 1 - eio(prog(t, 0.95, 1.35))
    if pa > 0:
        m = phone_m(t)
        with plane(cv, *m) as ok:
            if ok: phone(cv, 420, 840, pa, t, ph_banner(t) if t < 0.55 else 0.0)
        vb = 1 - prog(t, 0.05, 0.6)
        if vb > 0:
            for sd in (-1, 1):
                for k in range(2):
                    u = ((t * 3.2 + k * 0.5) % 1.0); x = 540 + sd * (230 + 60 * u)
                    arc = skia.Path(); arc.addArc(skia.Rect(x - 40, 640, x + 40, 840), -40 if sd > 0 else 140, 80)
                    cv.drawPath(arc, P(col(ACC_L, 0.8 * vb * (1 - u)), stroke=4))
    # banner lepas dari ponsel, terbang ke depan kamera
    fp = prog(t, 0.55, 1.0); fo = 1 - eio(prog(t, 1.15, 1.45))
    if fp > 0 and fo > 0:
        x0, y0 = 540, 760 - 840 * 0.06; x1, y1 = 540, 520
        x = lerp(x0, x1, eio(fp)); y = lerp(y0, y1, eio(fp)) - 40 * bump(fp); sc = lerp(1.0, 1.5, eo(fp))
        cv.save(); cv.translate(x, y); cv.rotate(-6 * (1 - eo(fp))); cv.scale(sc, sc)
        notif(cv, 0, 0, 340, HOOK_TXT, fo, glow=0.6 * bump(fp)); cv.restore()
    # kepala + putaran komentar
    ha = eo(prog(t, 0.95, 1.4)); hy = 860 + 60 * (1 - ha)
    if ha > 0:
        drop = eio(prog(t, 2.7, 3.4)); spin = spin_A(t) + 0.4
        hot = 0.6 * clamp(prog(t, 1.6, 2.6)) * (1 - drop)
        def center():
            head_solid(cv, 540, hy, 0.68, ha, 1, ACC_L, 0.3 + 0.7 * hot, CORAL)
            ga = eo(prog(t, 2.8, 3.3))
            if ga > 0:
                halo(cv, 532, hy - 70, 230, ACC, ga)
                gauge(cv, 532, hy - 70, 88, 0.6 * math.sin(t * 6), ga, t, ga, label=None, read=None, ends=False)
                mono(cv, '?', 655, hy - 185, 70, HL, ga * (0.6 + 0.4 * math.sin(t * 7)), glow=0.8)
        born = lambda k: prog(t, 1.15 + k * 0.1, 1.4 + k * 0.1)
        orbit(cv, 540, hy - 40, 330, spin, 6, HOOK_TXT, ha, 25, center, born, drop, 0.42, hot)
        fz = prog(t, 2.62, 2.95)
        if 0 < fz < 1: cv.drawCircle(540, hy - 40, 200 + 380 * eo(fz), P(col('#FFFFFF', 0.55 * (1 - fz)), stroke=6, blur=4))
    cv.restore()
    ca = clamp(prog(t, 1.3, 1.5)) * (1 - eio(prog(t, 2.9, 3.2)))
    if ca > 0:
        n = counter_A(t); mono(cv, f'diputar ulang di kepala: {n}x', 540, 1150, 30, CORAL, ca, sp=1, glow=0.6)

# ------------------------------------------------------------ B: alat ukur di kepalamu (4.19 - 8.11)
def v_B(t):
    if t < 5.51: return 0.7 * math.sin((t - 4.19) * 7.0) * math.cos((t - 4.19) * 2.3)
    if t < 6.49: return lerp(0.7 * math.sin(1.32 * 7.0) * math.cos(1.32 * 2.3), 0.0, eio(prog(t, 5.51, 5.8))) + 0.5 * math.sin((t - 5.51) * 6.4) * prog(t, 5.6, 5.9)
    if t < 7.27: return lerp(0.5 * math.sin(0.98 * 6.4), 0.9, bo(prog(t, 6.49, 6.8)))
    return lerp(0.9, -0.92, bo(prog(t, 7.27, 7.55))) + 0.03 * math.sin(t * 40) * (1 - prog(t, 7.55, 8.2))
HEARTS = [(-0.9, 0.0), (-0.55, 0.15), (-0.2, 0.05), (0.15, 0.2), (0.5, 0.1), (0.85, 0.25)]
def gB(cv, t):
    p = prog(t, 4.19, 4.9); z = lerp(-700, 0, eo(p)); ry = lerp(-35, 10, eo(p)) + 5 * math.sin(t * 0.9); rx = 9 + 3 * math.sin(t * 0.6)
    sx = shake(t, 7.27, 12)
    al = bump(prog(t, 7.27, 8.3)); v = v_B(t)
    with plane(cv, 540 + sx, 690, z, 640, 640, ry, rx) as ok:
        if ok:
            gauge_phys(cv, 0, 0, 225, v, clamp(p * 3), t, eo(prog(t, 4.19, 4.8)), al)
            crack(cv, -150, 40, 150, prog(t, 7.3, 7.6), 1 - eio(prog(t, 8.0, 8.4)))
    hp_ = prog(t, 6.55, 7.3)
    if 0 < hp_ < 1:
        for k, (dx, ph) in enumerate(HEARTS):
            u = clamp(hp_ * 1.25 - ph)
            if 0 < u < 1: heart_shape(cv, 760 + dx * 120, 760 - 380 * eo(u), 26 + 10 * (k % 2), bump(u) * 1.2, MINT)
        rays(cv, 540, 690, 560, bump(hp_), t, n=16, c=MINT)
    fl = prog(t, 7.27, 7.7)
    if 0 < fl < 1: cv.drawRect(skia.Rect(0, 260, W, 1220), P(shader=rg(540, 690, 700, [col(CORAL, 0.35 * (1 - fl)), col(CORAL, 0)])))

# ------------------------------------------------------------ C: riset 1995 -> sociometer (8.11 - 12.82)
def back_socio(cv, r, a):
    glass(cv, r, rad=34, a=a, glow=0.5)
    mono(cv, 'NAMANYA', 0, r.top() + 70, 25, ACC_L, 0.8 * a, sp=6)
    extrude(cv, 'SOCIOMETER', 0, -10, 104, a, depth=10)
    f = font(XB, 104); wS = f.measureText('SOCIO'); wT = f.measureText('SOCIOMETER'); x0 = -wT / 2
    for x_a, x_b, lab, c in ((x0, x0 + wS, 'sosial', ACC_L), (x0 + wS, x0 + wT, 'alat ukur', MINT)):
        xm = (x_a + x_b) / 2; hw = (x_b - x_a) / 2 - 10; yy = 80
        p = skia.Path(); p.moveTo(xm - hw, yy - 12); p.lineTo(xm - hw, yy); p.lineTo(xm + hw, yy); p.lineTo(xm + hw, yy - 12)
        cv.drawPath(p, P(col(c, 0.9 * a), stroke=3)); mono(cv, lab, xm, yy + 46, 34, c, a, glow=0.5)
def gC(cv, t):
    research_card(cv, t, 8.11, '1995', 'Mark Leary dkk.', 'Journal of Personality and Social Psychology', back_socio, 11.3)

# ------------------------------------------------------------ D: harga diri naik turun, ikut seberapa diterima (12.82 - 16.13)
AV_COL = ['#FF8A7A', '#7FB8FF', '#B57BFF', '#FFC56B', '#3FD6A4', '#FF7FC8', '#8C93FF', '#5AD1E6']
def acc_D(k, t):
    on = eo(prog(t, 12.9 + k * 0.12, 13.15 + k * 0.12))
    off = {1: 14.35, 4: 14.55, 6: 14.75}.get(k)
    if off: on *= 1 - eio(prog(t, off, off + 0.3)) * (1 - (eio(prog(t, 15.35, 15.65)) if k == 4 else 0))
    return on
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
def tube(cv, cx, top, bot, w, lvl, a, t, c):
    if a <= 0: return
    rx, ry = w / 2, w * 0.16; body = skia.Rect(cx - rx, top, cx + rx, bot)
    cv.drawOval(skia.Rect(cx - rx * 1.6, bot - ry * 0.8, cx + rx * 1.6, bot + ry * 1.6), P(col('#000000', 0.5 * a), blur=20))
    shp = skia.Op(skia.Op(skia.Path.Rect(skia.Rect(cx - rx, top, cx + rx, bot)), skia.Path.Oval(skia.Rect(cx - rx, bot - ry, cx + rx, bot + ry)), skia.PathOp.kUnion_PathOp), skia.Path.Oval(skia.Rect(cx - rx, top - ry, cx + rx, top + ry)), skia.PathOp.kUnion_PathOp)
    cv.drawPath(shp, P(col('#15162A', 0.75 * a)))
    ly = lerp(bot, top + ry, lvl)
    liq = skia.Op(skia.Path.Rect(skia.Rect(cx - rx + 8, ly, cx + rx - 8, bot)), skia.Path.Oval(skia.Rect(cx - rx + 8, bot - ry + 6, cx + rx - 8, bot + ry - 6)), skia.PathOp.kUnion_PathOp)
    cv.drawPath(liq, P(col(c, 0.55 * a), blur=20))
    cv.drawPath(liq, P(shader=lg(0, ly, 0, bot, [col(mixc(c, '#FFFFFF', 0.3), a), col(c, a), col(mixc(c, '#000000', 0.3), a)], [0, 0.5, 1])))
    wv = 4 * math.sin(t * 5)
    cv.drawOval(skia.Rect(cx - rx + 8, ly - ry * 0.8 + wv * 0.3, cx + rx - 8, ly + ry * 0.8 - wv * 0.3), P(col(mixc(c, '#FFFFFF', 0.55), a)))
    cv.drawRect(skia.Rect(cx - rx * 0.62, top + 10, cx - rx * 0.38, bot - 10), P(shader=lg(0, top, 0, bot, [col('#FFFFFF', 0.28 * a), col('#FFFFFF', 0.06 * a)])))
    cv.drawPath(shp, P(col(ACC_XL, 0.45 * a), stroke=2.5))
    cv.drawOval(skia.Rect(cx - rx, top - ry, cx + rx, top + ry), P(col(ACC_XL, 0.6 * a), stroke=2.5))
    for k in range(1, 10):
        y = lerp(bot, top + ry, k / 10); cv.drawLine(cx + rx - 24, y, cx + rx - 8, y, P(col('#FFFFFF', 0.4 * a), stroke=2))
def gD(cv, t):
    a0 = eo(prog(t, 12.82, 13.2)); acc = [acc_D(k, t) for k in range(8)]
    lvl = 0.1 + 0.85 * sum(acc) / 8; c = vcol(lvl * 2 - 1); spin = 0.35 * (t - 12.82) - 0.4
    started = [prog(t, 12.9 + k * 0.12, 13.15 + k * 0.12) >= 1 for k in range(8)]
    items = sorted(range(8), key=lambda k: -ring_pos(k, 8, spin, 350, 0.28)[2]); drawn = False
    def center():
        tube(cv, 540, 470, 980, 150, lvl, a0, t, c)
        mono(cv, 'HARGA DIRI', 540, 405, 27, ACC_L, 0.9 * a0, sp=4)
        mono(cv, f'{int(round(lvl * 100))}%', 540, 1060, 50, c, a0, glow=0.6)
    for k in items:
        x, y, z = ring_pos(k, 8, spin, 350, 0.28)
        if z < 0 and not drawn: center(); drawn = True
        gone = (1 - acc[k]) if started[k] else 0.0
        out = 60 * gone; X, Y, s = P3(540 + x * (1 + out / 350), 720 + y, z + out)
        dep = clamp((350 - z) / 700)
        avatar(cv, X, Y, 54 * s, AV_COL[k], a0 * lerp(0.45, 1, dep) * (1 - 0.4 * gone), acc[k], gone)
    if not drawn: center()

# ------------------------------------------------------------ E1: dulu, dikucilkan itu bahaya (16.13 - 17.86)
def sitter(cv, x, y, s, a=1.0, rim=FIRE, side=1, cool=0.0):
    """siluet orang duduk memeluk lutut (padat); cahaya tepi di sisi yang menghadap api (side=1: api di kanan)"""
    if a <= 0: return
    p = skia.Path.Circle(x + side * s * 0.04, y - s * 0.86, s * 0.23)
    b_ = skia.Path(); b_.moveTo(x - s * 0.08, y - s * 0.66)
    b_.cubicTo(x - s * 0.34, y - s * 0.64, x - s * 0.4, y - s * 0.5, x - s * 0.38, y - s * 0.2)
    b_.lineTo(x - s * 0.36, y + s * 0.12); b_.cubicTo(x - s * 0.4, y + s * 0.3, x - s * 0.2, y + s * 0.36, x, y + s * 0.36)
    b_.lineTo(x + s * 0.5, y + s * 0.36); b_.cubicTo(x + s * 0.62, y + s * 0.36, x + s * 0.62, y + s * 0.1, x + s * 0.42, y - s * 0.05)
    b_.cubicTo(x + s * 0.38, y - s * 0.4, x + s * 0.3, y - s * 0.64, x + s * 0.08, y - s * 0.66); b_.close()
    if side < 0: m = skia.Matrix(); m.setScale(-1, 1, x, y); b_.transform(m)
    p = skia.Op(p, b_, skia.PathOp.kUnion_PathOp)
    cv.drawPath(p, P(shader=lg(x, y - s, x, y + s * 0.4, [col(mixc('#1C1622', '#151A38', cool), a), col('#060509', a)])))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True); rp = skia.Path(p); rp.offset(-side * s * 0.13, s * 0.02)
    cv.drawPath(rp, P(col(mixc(rim, ACC, cool), 0.8 * a), stroke=s * 0.12, blur=s * 0.06)); cv.restore()
GROUP_E = [0.3, 1.2, 2.4, 3.5, 4.6]          # sudut duduk di sekitar api; indeks 1 = "kamu"
def gE1(cv, t):
    a0 = eo(prog(t, 16.13, 16.5)); fx, fy = 540, 900
    cv.drawOval(skia.Rect(fx - 420, fy - 90, fx + 420, fy + 130), P(shader=rg(fx, fy + 20, 420, [col(FIRE, 0.28 * a0), col(FIRE, 0.08 * a0), col(FIRE, 0)], [0, 0.6, 1])))
    mono(cv, 'ZAMAN DULU', 540, 360, 28, AMBER, 0.85 * a0, sp=8)
    out = eio(prog(t, 16.65, 17.35)); ppl = []
    for k, ang in enumerate(GROUP_E):
        x = fx + 300 * math.sin(ang); y = fy - 40 + 95 * math.cos(ang)
        if k == 1: x, y = lerp(x, 925, out), lerp(y, 600, out)
        ppl.append((y, k, x))
    ppl.sort()
    def person(p_):
        y, k, x = p_; cool = out if k == 1 else 0.0
        sitter(cv, x, y, 135 * lerp(0.85, 1.05, clamp((y - 600) / 400)), a0, FIRE, 1 if x < fx else -1, cool)
    for p_ in ppl:
        if p_[0] <= fy - 20: person(p_)
    flame(cv, fx, fy, 64, t, a0)
    for p_ in ppl:
        if p_[0] > fy - 20: person(p_)
    if out > 0:
        yx, yy = next((x, y) for y, k, x in ppl if k == 1)
        cv.drawRect(skia.Rect(0, 260, W, 1220), P(shader=rg(fx, fy - 60, 900, [col('#000000', 0), col('#000000', 0.35 * out)], [0.45, 1])))
        cv.drawCircle(yx, yy - 40, 190, P(shader=rg(yx, yy - 40, 190, [col(CORAL, 0.18 * out), col(CORAL, 0)])))
        wa = prog(t, 17.25, 17.5)
        if wa > 0:
            cv.save(); cv.translate(yx, yy - 230); cv.scale(bo(wa), bo(wa)); warn_tri(cv, 0, 0, 44, a0 * (0.75 + 0.25 * math.sin(t * 20))); cv.restore()
            mono(cv, 'BAHAYA', yx - 20, yy + 90, 30, CORAL, a0 * clamp(wa * 2), sp=5, glow=0.6)

# ------------------------------------------------------------ E2: ditolak -> otak bereaksi mirip rasa sakit (17.86 - 20.67)
_BRAIN = None
def brain_paths():
    global _BRAIN
    if _BRAIN is None:
        lobes = [(-0.62, 0.05, 0.4), (-0.42, -0.3, 0.42), (-0.05, -0.45, 0.46), (0.36, -0.36, 0.44), (0.64, -0.02, 0.38),
                 (0.42, 0.22, 0.36), (0.0, 0.18, 0.44), (-0.38, 0.26, 0.36)]
        p = skia.Path()
        for x, y, r in lobes: p = skia.Op(p, skia.Path.Circle(x * 100, y * 100, r * 100), skia.PathOp.kUnion_PathOp)
        cb = skia.Path.Circle(48, 52, 22); st = skia.Path.RRect(skia.RRect.MakeRectXY(skia.Rect(8, 30, 30, 92), 11, 11))
        g = skia.Path()
        for k, (x, y, r) in enumerate(lobes):
            for fr, a0, sw in ((0.62, 200 + k * 47, 150), (0.32, 30 + k * 61, 170)):
                g.addArc(skia.Rect(x * 100 - r * 100 * fr, y * 100 - r * 100 * fr, x * 100 + r * 100 * fr, y * 100 + r * 100 * fr), a0 % 360, sw)
        g.moveTo(-70, -10); g.cubicTo(-20, -30, 20, 10, 75, -5)
        _BRAIN = (p, cb, st, g)
    return _BRAIN
def brain(cv, cx, cy, s, a=1.0, pain=0.0, t=0.0, label=None):
    if a <= 0: return
    p, cb, st, g = brain_paths()
    cv.save(); cv.translate(cx, cy); cv.scale(s, s)
    cv.drawPath(p, P(col(ACC, 0.45 * a), blur=18)); cv.drawPath(st, P(col('#2A2D55', a))); cv.drawPath(cb, P(col('#3A3E78', a)))
    cv.drawPath(p, P(shader=rg(-30, -60, 160, [col('#4E54B8', a), col('#252860', a), col('#14163A', a)], [0, 0.6, 1])))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawPath(g, P(col(ACC_XL, 0.28 * a), stroke=3))
    if pain > 0:
        pu = 0.75 + 0.25 * math.sin(t * 9)
        cv.drawCircle(0, -30, 70, P(shader=rg(0, -30, 70, [col('#FFD1C8', 0.95 * pain * pu * a), col(CORAL, 0.7 * pain * a), col(CORAL, 0)], [0, 0.35, 1])))
    cv.restore()
    cv.drawPath(p, P(col(ACC_XL, 0.6 * a), stroke=2.5))
    if pain > 0:
        for k in range(2):
            u = ((t - 17.0) * 0.9 + k / 2) % 1.0; cv.drawCircle(0, -30, 30 + 120 * u, P(col(CORAL, 0.5 * (1 - u) * pain * a), stroke=3))
    cv.restore()
    if label: mono(cv, label, cx, cy + 135 * s, 28, ACC_L, 0.9 * a, sp=3)
def gE2(cv, t):
    a0 = eo(prog(t, 17.86, 18.2)); sp = eio(prog(t, 18.9, 19.4))
    bx = lerp(540, 300, sp); bs = lerp(2.6, 1.55, sp)
    hit = prog(t, 18.25, 18.5)
    cv.save(); cv.translate(shake(t, 18.3, 10, 0.4), 0)
    brain(cv, bx, 720, bs, a0, clamp(hit * 2) * (0.6 + 0.4 * sp), t, 'DITOLAK' if sp > 0.5 else None)
    cv.restore()
    ca = prog(t, 17.9, 18.3); co = 1 - eio(prog(t, 18.45, 18.7))
    if ca > 0 and co > 0:
        comment(cv, 'kamu nggak diajak ya', lerp(1180, 720, eio(ca)), lerp(380, 450, eio(ca)), co, lerp(0.8, 1, eo(ca)), size=32, rot=-5, glow=0.4)
    if sp > 0:
        brain(cv, lerp(900, 780, sp), 720, 1.55, a0 * sp, sp, t, 'SAKIT FISIK')
        mono(cv, '≈', 540, 700, 80, HL, a0 * sp, glow=0.6)
        la = eo(prog(t, 19.4, 19.8))
        mono(cv, 'area otak yang sama ikut aktif', 540, 455, 30, CORAL, a0 * la, glow=0.5)
        mono(cv, 'Eisenberger dkk. (2003), Science', 540, 1020, 22, ACC_L, 0.75 * a0 * la)

# ------------------------------------------------------------ F: alat ukurnya kelewat sensitif = alarm asap (20.67 - 23.05)
def smoke_alarm(cv, cx, cy, s, on, t, a=1.0):
    if a <= 0: return
    cv.drawRect(skia.Rect(0, 255, W, cy - s * 0.28), P(shader=lg(0, 255, 0, cy - s * 0.28, [col('#0B0C16', 0), col('#1A1C30', 0.9 * a)])))
    cv.drawLine(0, cy - s * 0.28, W, cy - s * 0.28, P(col(ACC_L, 0.35 * a), stroke=2))
    if on > 0:
        fl = on * (0.5 + 0.5 * (1 if (t * 4) % 1 < 0.5 else 0))
        cv.drawRect(skia.Rect(0, 255, W, 1220), P(shader=rg(cx, cy, 900, [col(CORAL, 0.38 * fl), col(CORAL, 0.1 * fl), col(CORAL, 0)], [0, 0.4, 1])))
        cv.save(); cv.translate(cx, cy + s * 0.2); cv.rotate(t * 260)
        bm = skia.Path(); bm.moveTo(0, 0); bm.lineTo(900, -120); bm.lineTo(900, 120); bm.close()
        cv.drawPath(bm, P(shader=lg(0, 0, 900, 0, [col(CORAL, 0.25 * on), col(CORAL, 0)]))); cv.rotate(180); cv.drawPath(bm, P(shader=lg(0, 0, 900, 0, [col(CORAL, 0.25 * on), col(CORAL, 0)])))
        cv.restore()
        for sd in (-1, 1):
            for k in range(3):
                u = ((t * 1.6 + k / 3) % 1.0); rr = s * (1.2 + 1.3 * u)
                arc = skia.Path(); arc.addArc(skia.Rect(cx - rr, cy - rr * 0.7, cx + rr, cy + rr * 0.7), (-35 if sd > 0 else 145), 70)
                cv.drawPath(arc, P(col(CORAL, 0.8 * (1 - u) * on), stroke=5))
    rx_, ry_ = s, s * 0.36; th = s * 0.16
    cv.drawOval(skia.Rect(cx - rx_ * 1.05, cy - ry_ + th + 10, cx + rx_ * 1.05, cy + ry_ + th + 30), P(col('#000000', 0.5 * a), blur=24))
    side = skia.Path(); side.addRect(skia.Rect(cx - rx_, cy - th, cx + rx_, cy + th)); side.addOval(skia.Rect(cx - rx_, cy - ry_ + th, cx + rx_, cy + ry_ + th))
    cv.drawPath(side, P(shader=lg(cx - rx_, 0, cx + rx_, 0, [col('#8D90A8', a), col('#E8E9F4', a), col('#9A9DB4', a)], [0, 0.4, 1])))
    face = skia.Rect(cx - rx_, cy - ry_ - th, cx + rx_, cy + ry_ - th)
    cv.drawOval(face, P(shader=rg(cx - rx_ * 0.3, cy - th - ry_ * 0.4, rx_ * 1.3, [col('#FFFFFF', a), col('#D4D6E6', a), col('#A9ACC4', a)], [0, 0.6, 1])))
    for k in (0.78, 0.55):
        cv.drawOval(skia.Rect(cx - rx_ * k, cy - th - ry_ * k, cx + rx_ * k, cy - th + ry_ * k), P(col('#7E8199', 0.6 * a), stroke=2))
    for k in range(16):
        ang = k * math.tau / 16; x0, y0 = cx + math.cos(ang) * rx_ * 0.62, cy - th + math.sin(ang) * ry_ * 0.62
        x1, y1 = cx + math.cos(ang) * rx_ * 0.72, cy - th + math.sin(ang) * ry_ * 0.72
        cv.drawLine(x0, y0, x1, y1, P(col('#6A6D85', 0.8 * a), stroke=4))
    lx, ly = cx + rx_ * 0.32, cy - th + ry_ * 0.05; blink = on * (1 if (t * 4) % 1 < 0.5 else 0.25)
    lc = CORAL if on > 0 else MINT
    cv.drawCircle(lx, ly, 26, P(col(lc, (0.7 * blink if on > 0 else 0.4) * a), blur=16))
    cv.drawCircle(lx, ly, 9, P(col(mixc(lc, '#FFFFFF', 0.4), a)))
    mono(cv, 'SOCIOMETER', cx - rx_ * 0.1, cy - th - ry_ * 0.05, 22, '#4A4D66', a, sp=3)
def gF(cv, t):
    a0 = eo(prog(t, 20.67, 21.0)); on = clamp(prog(t, 21.5, 21.6))
    cv.save(); cv.translate(shake(t, 21.5, 9, 0.6) + (3 * math.sin(t * 70) * on), 0)
    smoke_alarm(cv, 540, 470, 170, on, t, a0)
    cv.restore()
    ca = eo(prog(t, 20.95, 21.25))
    if ca > 0:
        cv.save(); cv.translate(540, 1000); s = lerp(0.6, 1, bo(ca)); cv.scale(s, s)
        chip(cv, 'dibaca', -12, 0, ca * a0, size=26, fg=ACC_XL)
        f = font(B, 26); w = f.measureText('dibaca'); ck = P(col('#7FB8FF', ca * a0), stroke=3.5)
        for k in range(2):
            x = w / 2 - 2 + k * 12; cv.drawLine(x - 9, 2, x - 3, 8, ck); cv.drawLine(x - 3, 8, x + 8, -5, ck)
        cv.restore()
        for k in range(2):
            wp = skia.Path(); ph = t * 2.2 + k * 1.7; wp.moveTo(540 + k * 20 - 10, 960)
            for i in range(1, 7): wp.lineTo(540 + k * 20 - 10 + 12 * math.sin(ph + i * 0.9), 960 - i * 22)
            cv.drawPath(wp, P(col('#C9CBE0', 0.35 * ca * a0), stroke=4, blur=3))
        brackets(cv, skia.Rect(430, 955, 650, 1045), ca * a0 * (0.6 + 0.4 * on), ACC_L, 22, 2.5)
        mono(cv, 'pemicunya cuma ini', 540, 1100, 24, ACC_L, ca * a0 * eo(prog(t, 21.9, 22.2)), sp=2)
    if on > 0:
        for k, (x, y, rot, t0) in enumerate(((250, 720, -10, 21.55), (830, 700, 9, 21.75), (540, 820, -4, 22.0))):
            pa = prog(t, t0, t0 + 0.15)
            if pa > 0:
                cv.save(); cv.translate(x, y); cv.rotate(rot); s = lerp(1.6, 1, eo(pa)); cv.scale(s, s)
                extrude(cv, 'BIP!', 0, 0, 74, clamp(pa * 3) * a0, depth=8, front=('#FFFFFF', '#FFB3A6'), side='#5A1530', glow=CORAL); cv.restore()

# ------------------------------------------------------------ G1: riset 2001 (23.05 - 26.12)
def gG1(cv, t):
    research_card(cv, t, 23.05, '2001', 'Savitsky, Epley & Gilovich', 'Journal of Personality and Social Psychology')

# ------------------------------------------------------------ G2: salah di depan orang; mereka nggak menilai seburuk itu (26.12 - 30.18)
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
AUD = [(680, 1085, 'susah sih soalnya', 720), (840, 1110, 'biasa aja', 820), (985, 1080, 'wajar kok', 910)]
def gG2(cv, t):
    a0 = eo(prog(t, 26.12, 26.5)); px = 330
    cone = skia.Path(); cone.moveTo(px - 30, 255); cone.lineTo(px + 30, 255); cone.lineTo(px + 190, 1080); cone.lineTo(px - 190, 1080); cone.close()
    cv.drawPath(cone, P(shader=lg(0, 255, 0, 1080, [col('#DDE0FF', 0.22 * a0), col('#AEB6FF', 0.07 * a0)])))
    cv.drawOval(skia.Rect(px - 200, 1050, px + 200, 1110), P(col('#DDE0FF', 0.18 * a0), blur=10))
    stander(cv, px, 1080, 330, a0, '#DDE0FF')
    ta = 1 - eio(prog(t, 27.7, 28.0)); bad = eo(prog(t, 26.85, 27.05))
    if ta > 0:
        for k, ch in enumerate('HALSA'):
            tp = eo(prog(t, 26.15 + k * 0.06, 26.45 + k * 0.06))
            tile(cv, ch, 330 - 2 * 108 + k * 108 + shake(t, 26.9, 9, 0.4), 470 + (1 - tp) * 30, 92, a0 * tp * ta, bad)
        cross(cv, 330, 610, 44, a0 * ta, CORAL, 13, prog(t, 26.9, 27.2))
        mono(cv, 'GAGAL', 330, 690, 32, CORAL, a0 * ta * eo(prog(t, 27.05, 27.25)), sp=6, glow=0.6)
    for k, (x, y, txt, ty) in enumerate(AUD): bust(cv, x, y, 88, a0 * eo(prog(t, 26.2 + k * 0.08, 26.6 + k * 0.08)), '#AEB6FF')
    ya = prog(t, 27.87, 28.15)
    if ya > 0:
        shr = eio(prog(t, 29.2, 29.6)); sc = lerp(lerp(0.6, 1.0, bo(ya)), 0.62, shr)
        thought(cv, 'mereka pasti ilfeel banget', 400, 560, 36, a0 * clamp(ya * 2), CORAL, (350, 700), sc, ('#3A1C2A', '#1E0E18'), '#FFD9D2', shake(t, 27.95, 6, 0.6) + 2 * math.sin(t * 30) * (1 - shr))
        mono(cv, 'KITA KIRA', 400, 455, 24, CORAL, a0 * clamp(ya * 2) * (1 - shr), sp=4)
    for k, (x, y, txt, ty) in enumerate(AUD):
        pa = prog(t, 28.35 + k * 0.2, 28.65 + k * 0.2)
        if pa > 0: thought(cv, txt, min(x - 40, 920), ty - 30 * k, 26, a0 * clamp(pa * 2), MINT, (x, y - 110), lerp(0.6, 1, bo(pa)), ('#173A30', '#0D2019'), '#D8FFF0')
    ka = eo(prog(t, 28.5, 28.8))
    mono(cv, 'KENYATAAN', 850, 640, 24, MINT, a0 * ka, sp=4)

# ------------------------------------------------------------ H: kita yang terlalu fokus ke kesalahan sendiri (30.18 - 32.67)
def gH(cv, t):
    a0 = eo(prog(t, 30.18, 30.5)); r = skia.Rect(250, 540, 830, 820)
    glass(cv, r, rad=26, a=a0)
    for k, wl in enumerate((0.85, 0.7, 0.9, 0.55)):
        y = r.top() + 62 + k * 56; cv.drawRoundRect(skia.Rect(r.left() + 50, y - 9, r.left() + 50 + (r.width() - 100) * wl, y + 9), 9, 9, P(col(ACC_L, 0.22 * a0)))
    ex, ey = 640, r.top() + 118; cross(cv, ex, ey, 9, a0, CORAL, 4)
    lk = eio(prog(t, 30.4, 30.9))
    bx = skia.Rect(lerp(r.left() - 20, ex - 40, lk), lerp(r.top() - 20, ey - 40, lk), lerp(r.right() + 20, ex + 40, lk), lerp(r.bottom() + 20, ey + 40, lk))
    brackets(cv, bx, a0 * (1 - eio(prog(t, 31.0, 31.2))), CORAL if lk >= 1 else ACC_L, 30, 3)
    la = eo(prog(t, 30.95, 31.35))
    if la > 0:
        lr = max(1.0, 150 * (bo(la) if la < 1 else 1)); lx, ly = ex, ey + 60 * (1 - la); pth = skia.Path(); pth.addCircle(lx, ly, lr)
        cv.drawCircle(lx, ly, lr, P(col(CORAL, 0.4 * la), blur=30))
        cv.drawCircle(lx, ly, lr, P(shader=rg(lx, ly - lr * 0.3, lr * 1.3, [col('#2A1C2E', 0.96 * la), col('#140E1A', 0.96 * la)])))
        cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True); cross(cv, lx, ly, 70, la, CORAL, 20); cv.restore()
        cv.drawCircle(lx, ly, lr, P(shader=skia.GradientShader.MakeSweep(lx, ly, [col(c_, la) for c_ in ('#8A90B8', '#E6E8FF', '#3A3D55', '#A8AED6', '#8A90B8')], [0, 0.25, 0.5, 0.75, 1]), stroke=12))
        hx, hy = lx + lr * 0.74, ly + lr * 0.74
        cv.drawLine(hx, hy, hx + 100, hy + 100, P(col('#000000', 0.5 * la), stroke=30, blur=10)); cv.drawLine(hx, hy, hx + 100, hy + 100, P(shader=lg(hx, hy, hx + 100, hy + 100, [col('#6A6E8E', la), col('#1A1B2A', la)]), stroke=24))
        mono(cv, 'FOKUS: KESALAHAN SENDIRI', 540, 410, 28, CORAL, la, sp=2, glow=0.6)
    for k, (x, txt) in enumerate(((240, 'laper'), (540, 'tugas numpuk'), (840, 'chat doi'))):
        pa = eo(prog(t, 31.1 + k * 0.17, 31.45 + k * 0.17))
        if pa > 0:
            bust(cv, x, 1095, 62, pa, ACC_L); chip(cv, txt, x, 975 + (1 - pa) * 14, pa, size=24, fg=ACC_XL)

# ------------------------------------------------------------ I: omongan orang kepikiran lagi -> alat ukurmu suka lebay (32.67 - 36.6)
def knob(cv, cx, cy, r, val, a=1.0, label='SENSITIVITAS'):
    if a <= 0: return
    tk = skia.Path()
    for k in range(21):
        ang = math.radians(135 + k * 13.5); r0, r1 = r * 1.22, r * (1.42 if k % 5 == 0 else 1.34)
        tk.moveTo(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0); tk.lineTo(cx + math.cos(ang) * r1, cy + math.sin(ang) * r1)
    cv.drawPath(tk, P(col(ACC_L, 0.5 * a), stroke=3))
    arc = skia.Path(); arc.addArc(skia.Rect(cx - r * 1.28, cy - r * 1.28, cx + r * 1.28, cy + r * 1.28), 135, max(0.5, 270 * val))
    c = mixc(MINT, CORAL, val); cv.drawPath(arc, P(col(c, 0.5 * a), stroke=12, blur=8)); cv.drawPath(arc, P(col(c, a), stroke=5))
    cv.drawCircle(cx, cy + r * 0.15, r * 1.05, P(col('#000000', 0.55 * a), blur=r * 0.25))
    sw = skia.GradientShader.MakeSweep(cx, cy, [col(c_, a) for c_ in ('#9AA0C8', '#2A2C40', '#E8EAFF', '#3A3D55', '#9AA0C8')], [0, 0.25, 0.5, 0.75, 1])
    cv.drawCircle(cx, cy, r, P(shader=sw)); cv.drawCircle(cx, cy, r * 0.8, P(shader=rg(cx - r * 0.2, cy - r * 0.3, r, [col('#3C3F5C', a), col('#16172A', a)])))
    ang = math.radians(135 + 270 * val)
    cv.drawLine(cx + math.cos(ang) * r * 0.25, cy + math.sin(ang) * r * 0.25, cx + math.cos(ang) * r * 0.72, cy + math.sin(ang) * r * 0.72, P(col(c, a), stroke=7))
    mono(cv, label, cx - r * 1.75, cy, 22, ACC_L, 0.85 * a, sp=3, align=1)
    mono(cv, 'MIN', cx - r * 1.45, cy + r * 1.25, 18, MINT, 0.8 * a); mono(cv, 'MAKS', cx + r * 1.45, cy + r * 1.25, 18, CORAL, 0.8 * a)
def gI(cv, t):
    a0 = eo(prog(t, 32.67, 33.0)); calm = eio(prog(t, 34.75, 35.45)); hy = 800
    spin = 1.1 * (t - 32.67) + 0.9 * (t - 32.67) ** 2 * (1 - calm) if t < 34.75 else 1.1 * 2.08 + 0.9 * 2.08 ** 2 + 1.0 * (t - 34.75) - 0.6 * (t - 34.75) ** 2 * calm
    def center():
        hot = (1 - calm) * clamp(prog(t, 33.0, 33.6))
        head_solid(cv, 540, hy, 0.68, a0, 1, mixc(ACC_L, MINT, calm), 0.3 + 0.7 * hot, mixc(CORAL, MINT, calm))
        gv = lerp(-0.6 + 0.3 * math.sin(t * 13), 0.2 + 0.03 * math.sin(t * 2), calm)
        gauge(cv, 532, hy - 70, 88, gv, a0, t, 1.0, 0.8 * hot, label=None, read=None, ends=False)
    born = lambda k: prog(t, 32.75 + k * 0.12, 33.0 + k * 0.12) * (1 - calm)
    orbit(cv, 540, hy - 40, 330, spin, 6, HOOK_TXT, a0, 25, center, born, 0.0, 0.42, 0.6 * (1 - calm))
    ka = eo(prog(t, 34.45, 34.75))
    knob(cv, 600, 1105, 48, lerp(1.0, 0.2, eio(prog(t, 34.65, 35.4))), ka * a0)
    stamp(cv, 'LEBAY', 540, 700, 110, t, 35.85, CORAL, -9, a0)

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
    ev = [(0.02, 'ding'), (0.05, 'clunk'), (0.2, 'clunk'), (0.35, 'clunk'), (0.55, 'whoosh'), (1.0, 'pop'), (1.4, 'rise'),
          (2.62, 'chop'), (2.64, 'stamp'), (2.75, 'swish'), (2.85, 'shine'), (3.55, 'zoom'),
          (4.19, 'whoosh'), (4.45, 'clunk'), (5.51, 'tick'), (5.8, 'tick'), (6.1, 'tick'), (6.49, 'rise'), (6.6, 'ding'),
          (7.27, 'chop'), (7.3, 'crack'), (7.32, 'buzzer'),
          (8.11, 'whoosh'), (8.2, 'card'), (8.45, 'stamp'), (8.75, 'ding_soft'), (11.3, 'swish'), (11.65, 'chop'), (11.75, 'plip'), (11.95, 'plip'),
          (12.82, 'whoosh'), (13.95, 'ding_soft'), (14.35, 'zap2'), (14.55, 'zap2'), (14.75, 'zap2'), (15.35, 'plip'),
          (16.13, 'whoosh'), (16.2, 'fizz_soft'), (16.65, 'swish'), (17.25, 'beep'), (17.5, 'beep'),
          (17.86, 'whoosh'), (17.95, 'swish'), (18.3, 'crack'), (18.32, 'heart'), (18.9, 'whoosh'), (19.0, 'heart'), (19.4, 'ding_soft'), (19.6, 'heart'),
          (20.67, 'whoosh'), (20.95, 'pop'), (21.5, 'buzzer'), (21.55, 'beep'), (21.75, 'beep'), (22.0, 'beep'), (22.25, 'beep'), (22.5, 'beep'), (22.75, 'beep'),
          (23.05, 'whoosh'), (23.15, 'card'), (23.4, 'stamp'), (23.7, 'ding_soft'),
          (26.12, 'whoosh'), (26.9, 'buzzer'), (27.05, 'stamp'), (27.87, 'boing'), (28.35, 'pop'), (28.55, 'pop'), (28.75, 'pop'), (29.2, 'fizz_soft'),
          (30.18, 'whoosh'), (30.4, 'zoom'), (30.95, 'pop'), (31.1, 'plip'), (31.27, 'plip'), (31.44, 'plip'),
          (32.67, 'whoosh'), (33.0, 'rise'), (34.45, 'clock'), (34.7, 'swish'), (35.4, 'shine'), (35.85, 'chop'), (35.88, 'stamp'),
          (36.6, 'whoosh'), (36.75, 'boing'), (37.1, 'shine'), (37.35, 'pop')]
    for k in range(8): ev += [(1.15 + k * 0.08, 'plip'), (12.9 + k * 0.12, 'pop'), (32.75 + k * 0.1, 'plip')]
    for k in range(5): ev.append((26.15 + k * 0.06, 'plip'))
    tt, k = 1.4, 0
    while tt < 2.6: ev.append((round(tt, 3), 'tick')); tt += max(0.05, 0.2 - 0.03 * k); k += 1
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


