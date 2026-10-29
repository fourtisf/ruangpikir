#!/usr/bin/env python3
"""Ruang Pikir reel #8: 'Deadline besok, kok masih nunda?' (menunda = memperbaiki mood sesaat; Sirois & Pychyl 2013,
Tice, Bratslavsky & Baumeister 2001, Wohl, Pychyl & Bennett 2010)
Gaya "meja belajar malam": objek 3D lembut (laptop, ponsel, stik game, balok es, balok TUGAS, tangga) dalam perspektif,
cahaya lampu meja hangat + pendar ungu malam, teks 3D yang pecah, makhluk asap "rasa nggak enak".
python3 episode.py preview t1 t2 ... | timeline out.json | video out.mp4"""
import sys, os, math, json, subprocess, random
import skia
import base as b
from base import (clamp, lerp, prog, eo, ei, eio, bo, bump, col, P, lg, rg, layer, font, XB, B, M, MONO, bl, tracked, parse,
                 pill, sparkle, person, ACC, ACC_L, ACC_XL, TXT, MUTED, CORAL, MINT, W, H, FPS)

VIOLET, YELLOW, INK, HL = '#B57BFF', '#FFD23F', '#0B0C1E', '#AEB6FF'

# adegan (waktu animasi, DUR 42); tag tidak ditampilkan
b.GROUPS = [(0.0, 4.22, 'A'), (4.22, 8.57, 'B'), (8.57, 13.44, 'C'), (13.44, 18.7, 'D'), (18.7, 22.66, 'E'),
            (22.66, 26.25, 'F'), (26.25, 32.53, 'G'), (32.53, 36.6, 'H'), (36.6, 42.0, 'J')]
PHRASES = [(0.15, 'Kamu [nunda kerjaan]'), (1.4, 'bukan karena [malas].'), (2.41, 'Kamu lagi [kabur] dari [rasa nggak enak].'),
           (4.22, 'Tugasnya bikin [bosan],'), (5.41, '[cemas], atau [bingung] mulai dari mana.'), (7.05, 'Jadi kamu [kabur ke HP].'),
           (8.57, 'Tahun [2013],'), (9.71, 'psikolog [Sirois & Pychyl] menyebutnya:'), (11.67, '[memperbaiki mood sesaat].'),
           (13.44, 'Tahun [2001],'), (14.86, 'peneliti bikin peserta [bad mood] sebelum latihan tes.'), (17.07, 'Mereka malah [sibuk main].'),
           (18.7, 'Tapi saat diyakinkan'), (20.11, '[mood-nya nggak bisa berubah],'), (21.06, 'mereka [berhenti menunda].'),
           (22.66, 'Yang dikejar cuma [lega sesaat].'), (24.24, 'Tugasnya [tetap ada],'), (25.25, 'dan [makin berat].'),
           (26.25, 'Tahun [2010],'), (27.47, 'riset [Michael Wohl]:'), (28.64, 'mahasiswa yang [memaafkan diri] setelah menunda,'),
           (30.86, '[lebih jarang menunda] lagi.'),
           (32.53, 'Jadi jangan [marahin diri].'), (34.01, '[Maafin] dulu,'), (34.75, 'lalu mulai dari [langkah paling kecil].'),
           (36.6, 'Follow [Ruang Pikir],'), (37.73, 'biar makin kenal [isi kepalamu].')]
b.CAPS = [(t, s, '') for t, s in PHRASES]          # dipakai base hanya untuk jadwal

# ------------------------------------------------------------ chrome gaya sinematik
b.draw_tag = lambda cv, t: None
b.draw_progress = lambda cv, t: None
def draw_title(cv, t):
    a = eo(prog(t, 0.05, 0.35)) * (1 - eio(prog(t, 3.85, 4.25)))
    if a <= 0: return
    segs = parse("Deadline besok, [kok masih nunda]?"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 232) + (1 - eo(prog(t, 0.05, 0.35))) * 16 - 10 * eio(prog(t, 3.85, 4.25))
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
    # cahaya lampu meja hangat dari kiri atas (tanpa titik/bokeh)
    lx = 120 + 30 * math.sin(t * 0.3)
    cv.drawCircle(lx, 300, 900, P(shader=rg(lx, 300, 900, [col('#FFC98A', 0.10), col('#FFC98A', 0.03), col('#FFC98A', 0)], [0, 0.5, 1])))
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
    w, h = 780, 540; a = clamp(p * 2.5) * ((1 - eio(prog(t, t_out, t_out + 0.4))) if t_out else 1.0)
    if a <= 0: return
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

# ------------------------------------------------------------ helper EP08: meja belajar malam (objek 3D lembut + lampu meja)
GREY = ('#D5D7E8', '#6A6D85', '#24263A')
LAMP = '#FFC98A'
def doc_screen(cv, r, a, t, typed=0.0, deadline=1.0, first=''):
    """layar dokumen kosong: judul file, kursor berkedip, chip deadline merah"""
    cv.drawRect(r, P(shader=lg(0, r.top(), 0, r.bottom(), [col('#1E2036', a), col('#121322', a)])))
    bar = skia.Rect(r.left(), r.top(), r.right(), r.top() + r.height() * 0.11)
    cv.drawRect(bar, P(col('#2A2D48', a)))
    f = font(B, r.height() * 0.05); cv.drawString('TUGAS_FINAL.docx', r.left() + r.width() * 0.05, bl(f, bar.centerY()), f, P(col(ACC_XL, 0.9 * a)))
    f2 = font(MONO, r.height() * 0.05); s_ = '23.47'; cv.drawString(s_, r.right() - r.width() * 0.05 - f2.measureText(s_), bl(f2, bar.centerY()), f2, P(col(MUTED, a)))
    pg = skia.Rect(r.left() + r.width() * 0.16, r.top() + r.height() * 0.17, r.right() - r.width() * 0.16, r.bottom() + 20)
    cv.drawRect(pg, P(col('#F1F0F7', 0.95 * a)))
    f3 = font(B, r.height() * 0.06); x = pg.left() + pg.width() * 0.09; y = pg.top() + pg.height() * 0.16
    sh = first[:int(len(first) * typed)]
    if sh: cv.drawString(sh, x, bl(f3, y), f3, P(col('#22243A', a)))
    if (t * 1.6) % 1 < 0.55: cx_ = x + f3.measureText(sh) + 3; cv.drawLine(cx_, y - r.height() * 0.035, cx_, y + r.height() * 0.035, P(col('#4A50D0', a), stroke=3))
    if deadline > 0:
        pu = 0.75 + 0.25 * math.sin(t * 7)
        f4 = font(XB, r.height() * 0.058); s_ = 'Deadline: besok 08.00'; w = f4.measureText(s_) + r.height() * 0.08
        cr = skia.Rect(r.centerX() - w / 2, pg.top() + pg.height() * 0.42, r.centerX() + w / 2, pg.top() + pg.height() * 0.42 + r.height() * 0.11)
        cv.drawRoundRect(cr, cr.height() / 2, cr.height() / 2, P(col(CORAL, 0.5 * deadline * a * pu), blur=12))
        cv.drawRoundRect(cr, cr.height() / 2, cr.height() / 2, P(col(CORAL, deadline * a)))
        cv.drawString(s_, cr.centerX() - f4.measureText(s_) / 2, bl(f4, cr.centerY()), f4, P(col('#FFFFFF', deadline * a)))

def laptop(cv, w, a, t, screen_fn=None, glow=1.0):
    """laptop (koordinat lokal): layar dari y=-h..0, alas trapesium di bawahnya"""
    if a <= 0: return
    h = w * 0.62
    cv.drawOval(skia.Rect(-w * 0.75, h * 0.08, w * 0.75, h * 0.34), P(col('#000000', 0.55 * a), blur=30))
    base = skia.Path(); base.moveTo(-w * 0.5, 0); base.lineTo(w * 0.5, 0); base.lineTo(w * 0.6, h * 0.16); base.lineTo(-w * 0.6, h * 0.16); base.close()
    cv.drawPath(base, P(shader=lg(0, 0, 0, h * 0.16, [col('#5C607E', a), col('#2A2C40', a)])))
    for k in range(3):
        y = h * (0.035 + k * 0.035); u = y / (h * 0.16); hw = lerp(w * 0.5, w * 0.6, u) * 0.82
        cv.drawLine(-hw, y, hw, y, P(col('#191A28', 0.8 * a), stroke=h * 0.018))
    cv.drawRoundRect(skia.Rect(-w * 0.12, h * 0.125, w * 0.12, h * 0.155), 4, 4, P(col('#3A3D55', a)))
    sr = skia.Rect(-w / 2, -h, w / 2, 0)
    if glow > 0: cv.drawRoundRect(sr, 22, 22, P(col('#8C93FF', 0.35 * glow * a), blur=50))
    cv.drawRoundRect(sr, 22, 22, P(shader=lg(sr.left(), sr.top(), sr.right(), sr.bottom(), [col('#4A4D68', a), col('#1A1B2A', a)])))
    inner = sr.makeInset(w * 0.025, w * 0.025)
    cv.save(); cv.clipRect(inner, skia.ClipOp.kIntersect, True)
    if screen_fn: screen_fn(cv, inner, a)
    cv.drawRect(inner, P(shader=lg(inner.left(), inner.top(), inner.right(), inner.bottom(), [col('#FFFFFF', 0.08 * a), col('#FFFFFF', 0), col('#FFFFFF', 0)], [0, 0.45, 1])))
    cv.restore()
    cv.drawRoundRect(sr, 22, 22, P(col('#FFFFFF', 0.25 * a), stroke=2.5))
    cv.drawLine(-w * 0.5, 0, w * 0.5, 0, P(col('#8A8EAE', a), stroke=4))

def blob(cv, cx, cy, r, t, a=1.0, look=(0.0, 0.0), angry=0.6):
    """'rasa nggak enak': makhluk asap gelap bermata"""
    if a <= 0 or r <= 2: return
    p = skia.Path(); N = 60
    for i in range(N + 1):
        ang = i / N * math.tau
        rr = r * (1 + 0.07 * math.sin(ang * 3 + t * 2.3) + 0.05 * math.sin(ang * 5 - t * 3.3) + (0.1 * math.sin(ang * 7 + t * 4) if math.sin(ang) > 0.3 else 0))
        x, y = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr * 0.95
        (p.moveTo if i == 0 else p.lineTo)(x, y)
    p.close()
    cv.drawPath(p, P(col('#7A3FD0', 0.45 * a), blur=r * 0.25))
    cv.drawPath(p, P(shader=rg(cx - r * 0.25, cy - r * 0.35, r * 1.4, [col('#4A2C78', a), col('#1E1233', a), col('#0C0716', a)], [0, 0.55, 1])))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True); rp = skia.Path(p); rp.offset(-r * 0.08, r * 0.08)
    cv.drawPath(rp, P(col(CORAL, 0.55 * a), stroke=r * 0.08, blur=r * 0.05)); cv.restore()
    for sd in (-1, 1):
        ex, ey = cx + sd * r * 0.32, cy - r * 0.12; bk = blink_at(t, 0.3 + sd * 0.01)
        eh = r * 0.17 * (1 - 0.9 * bk)
        cv.drawOval(skia.Rect(ex - r * 0.14, ey - eh, ex + r * 0.14, ey + eh), P(col('#FFF1EC', a)))
        if bk < 0.6: cv.drawCircle(ex + look[0] * r * 0.06, ey + look[1] * r * 0.05 + r * 0.02, r * 0.065, P(col('#140A20', a)))
        cv.drawLine(ex - sd * r * 0.17, ey - r * 0.25 - sd * 0 - angry * r * 0.06, ex + sd * r * 0.12, ey - r * 0.2 + angry * r * 0.03, P(col('#FFF1EC', 0.9 * a), stroke=r * 0.045))
    m = skia.Path(); m.moveTo(cx - r * 0.18, cy + r * 0.3); m.quadTo(cx, cy + r * 0.18, cx + r * 0.18, cy + r * 0.3)
    cv.drawPath(m, P(col('#FFF1EC', 0.9 * a), stroke=r * 0.045))

def shatter_text(cv, text, cx, cy, size, t, t0, a=1.0, front=('#FFFFFF', '#FFB3A6'), side='#5A1530', glow=CORAL, n=7):
    """teks 3D yang pecah jadi kepingan miring dan berjatuhan setelah t0"""
    u = prog(t, t0, t0 + 0.9)
    if u <= 0: extrude(cv, text, cx, cy, size, a, depth=12, front=front, side=side, glow=glow); return
    if u >= 1: return
    f = font(XB, size); w = f.measureText(text); x0 = cx - w / 2 - 30; x1 = cx + w / 2 + 30; rnd = random.Random(5)
    cuts = [x0] + sorted(rnd.uniform(x0 + 40, x1 - 40) for _ in range(n - 1)) + [x1]
    for k in range(n):
        sk = rnd.uniform(-40, 40); poly = skia.Path()
        poly.moveTo(cuts[k] + sk, cy - size); poly.lineTo(cuts[k + 1] + sk, cy - size); poly.lineTo(cuts[k + 1] - sk, cy + size); poly.lineTo(cuts[k] - sk, cy + size); poly.close()
        vx = rnd.uniform(-160, 160); vy = rnd.uniform(-220, -60); rot = rnd.uniform(-60, 60)
        dx = vx * u; dy = vy * u + 900 * u * u; cxk = (cuts[k] + cuts[k + 1]) / 2
        cv.save(); cv.translate(cxk + dx, cy + dy); cv.rotate(rot * u); cv.translate(-cxk, -cy)
        cv.clipPath(poly, skia.ClipOp.kIntersect, True)
        extrude(cv, text, cx, cy, size, a * (1 - u), depth=12, front=front, side=side, glow=glow); cv.restore()

def feed_screen(cv, r, a, t, speed=600):
    """isi ponsel: feed yang di-scroll cepat"""
    cv.drawRect(r, P(col('#0E0F1C', a)))
    ch = r.width() * 1.05; off = (t * speed) % ch
    cols_ = [('#FF8A7A', '#B57BFF'), ('#5AD1E6', '#3F6BFF'), ('#FFC56B', '#FF7FC8'), ('#3FD6A4', '#7FB8FF')]
    for k in range(-1, 4):
        y = r.top() + k * ch - off + 20; c1, c2 = cols_[(k + int((t * speed) // ch)) % 4]
        cv.drawCircle(r.left() + 34, y + 22, 16, P(shader=lg(0, y, 0, y + 40, [col(c1, a), col(c2, a)])))
        cv.drawRoundRect(skia.Rect(r.left() + 60, y + 14, r.left() + 170, y + 28), 7, 7, P(col('#3A3D55', a)))
        im = skia.Rect(r.left() + 12, y + 50, r.right() - 12, y + 50 + ch * 0.62)
        cv.drawRoundRect(im, 14, 14, P(shader=lg(im.left(), im.top(), im.right(), im.bottom(), [col(c1, 0.85 * a), col(c2, 0.85 * a)])))
        heart_shape(cv, r.left() + 34, im.bottom() + 28, 12, a, '#FF7F9A')
        cv.drawRoundRect(skia.Rect(r.left() + 60, im.bottom() + 20, r.right() - 60, im.bottom() + 34), 7, 7, P(col('#2A2D48', a)))

def phone2(cv, w, h, a, t, screen_fn):
    """ponsel kaca dengan isi layar bebas (screen_fn(cv, rect, a))"""
    if a <= 0: return
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2); rad = w * 0.15
    cv.drawRRect(RR(r.makeOffset(0, 30), rad), P(col('#000000', 0.6 * a), blur=40))
    cv.drawRRect(RR(r, rad), P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col('#6A6E8E', a), col('#1A1B2A', a), col('#4A4D68', a), col('#15161F', a)], [0, 0.35, 0.7, 1])))
    sr = r.makeInset(w * 0.035, w * 0.035)
    cv.save(); cv.clipRRect(RR(sr, rad * 0.8), skia.ClipOp.kIntersect, True); screen_fn(cv, sr, a)
    cv.drawRect(sr, P(shader=lg(sr.left(), sr.top(), sr.right(), sr.bottom(), [col('#FFFFFF', 0.1 * a), col('#FFFFFF', 0), col('#FFFFFF', 0)], [0, 0.4, 1]))); cv.restore()
    cv.drawRoundRect(skia.Rect(-w * 0.13, -h / 2 + w * 0.07, w * 0.13, -h / 2 + w * 0.15), w * 0.04, w * 0.04, P(col('#000000', a)))
    cv.drawRRect(RR(r, rad), P(col('#FFFFFF', 0.28 * a), stroke=2.5))

def mood_ball(cv, cx, cy, r, a, t, mood='sad', cols=None, label=None):
    sphere(cv, cx, cy, r, cols or GREY, a, 0.6)
    face(cv, cx, cy + r * 0.05, r, mood, a, t)
    if label: mono(cv, label, cx, cy + r + 46, 26, ACC_L, 0.9 * a, sp=3)

def controller(cv, cx, cy, s, a=1.0, on=1.0, t=0.0):
    """stik game (padat, tombol menyala saat dimainkan)"""
    if a <= 0: return
    body = skia.Op(skia.Path.RRect(skia.RRect.MakeRectXY(skia.Rect(cx - s, cy - s * 0.42, cx + s, cy + s * 0.3), s * 0.35, s * 0.35)),
                   skia.Op(skia.Path.Circle(cx - s * 0.68, cy + s * 0.28, s * 0.36), skia.Path.Circle(cx + s * 0.68, cy + s * 0.28, s * 0.36), skia.PathOp.kUnion_PathOp), skia.PathOp.kUnion_PathOp)
    if on > 0: cv.drawPath(body, P(col('#B57BFF', 0.55 * on * a), stroke=24, blur=24))
    sh = skia.Path(body); sh.offset(0, s * 0.18); cv.drawPath(sh, P(col('#000000', 0.5 * a), blur=s * 0.2))
    cv.drawPath(body, P(shader=lg(cx, cy - s * 0.5, cx, cy + s * 0.6, [col(mixc('#3A3D66', '#2A2C3A', 1 - on), a), col('#12131F', a)])))
    cv.drawPath(body, P(col('#FFFFFF', 0.25 * a), stroke=2.5))
    dx, dy, u = cx - s * 0.55, cy - s * 0.05, s * 0.09
    cv.drawRoundRect(skia.Rect(dx - u * 2.6, dy - u * 0.85, dx + u * 2.6, dy + u * 0.85), 4, 4, P(col('#8C93FF', (0.4 + 0.6 * on) * a)))
    cv.drawRoundRect(skia.Rect(dx - u * 0.85, dy - u * 2.6, dx + u * 0.85, dy + u * 2.6), 4, 4, P(col('#8C93FF', (0.4 + 0.6 * on) * a)))
    for k, (bx, by, c) in enumerate(((0.55, -0.22, MINT), (0.75, -0.05, CORAL), (0.55, 0.12, '#7FB8FF'), (0.35, -0.05, AMBER))):
        pu = on * (0.5 + 0.5 * math.sin(t * 9 + k * 1.7))
        x, y = cx + s * bx, cy + s * by
        if pu > 0: cv.drawCircle(x, y, s * 0.12, P(col(c, 0.6 * pu * a), blur=s * 0.08))
        cv.drawCircle(x, y, s * 0.075, P(col(mixc('#4A4D66', c, 0.3 + 0.7 * on), a)))

def test_sheet(cv, cx, cy, w, a=1.0, done=0.0, dim=0.0):
    """lembar latihan tes; done 0..1 = jumlah soal yang dicentang"""
    if a <= 0: return
    h = w * 1.25; r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    cv.drawRoundRect(r.makeOffset(0, 18), 18, 18, P(col('#000000', 0.5 * a), blur=22))
    cv.drawRoundRect(r, 18, 18, P(col(mixc('#F1F0F7', '#7A7C90', dim), a)))
    f = font(XB, w * 0.085); cv.drawString('LATIHAN TES', r.left() + w * 0.1, bl(f, r.top() + h * 0.1), f, P(col('#2A2D55', a)))
    f2 = font(MONO, w * 0.07)
    for k, q in enumerate(('12 × 7 = ...', '45 : 9 = ...', '3² + 4 = ...', '18 − 11 = ...')):
        y = r.top() + h * (0.27 + k * 0.17); cv.drawString(q, r.left() + w * 0.1, bl(f2, y), f2, P(col('#3A3D55', a)))
        cv.drawLine(r.left() + w * 0.1, y + h * 0.06, r.right() - w * 0.1, y + h * 0.06, P(col('#C9CADB', a), stroke=2))
        if done * 4 > k: check_mark(cv, r.right() - w * 0.14, y, w * 0.06, clamp(done * 4 - k), a)

def ice(cv, cx, cy, s, u, a=1.0, t=0.0):
    """balok es transparan yang membeku dari bawah ke atas (u 0..1), proyeksi isometrik"""
    if u <= 0 or a <= 0: return
    top = [(cx, cy - s * 1.05), (cx + s * 0.95, cy - s * 0.55), (cx, cy - s * 0.05), (cx - s * 0.95, cy - s * 0.55)]
    left = [(cx - s * 0.95, cy - s * 0.55), (cx, cy - s * 0.05), (cx, cy + s * 1.1), (cx - s * 0.95, cy + s * 0.6)]
    right = [(cx, cy - s * 0.05), (cx + s * 0.95, cy - s * 0.55), (cx + s * 0.95, cy + s * 0.6), (cx, cy + s * 1.1)]
    def poly(pts):
        p = skia.Path(); p.moveTo(*pts[0])
        for q in pts[1:]: p.lineTo(*q)
        p.close(); return p
    cv.save(); yc = lerp(cy + s * 1.15, cy - s * 1.1, eio(u)); cv.clipRect(skia.Rect(cx - s * 1.2, yc, cx + s * 1.2, cy + s * 1.2), skia.ClipOp.kIntersect, True)
    for pts, c1, c2, al in ((left, '#BFE6FF', '#5AA8E6', 0.32), (right, '#DDF2FF', '#7FC0F0', 0.26), (top, '#FFFFFF', '#CDEBFF', 0.38)):
        pp = poly(pts); cv.drawPath(pp, P(shader=lg(pts[0][0], pts[0][1], pts[2][0], pts[2][1], [col(c1, al * a), col(c2, al * a)])))
        cv.drawPath(pp, P(col('#EAF7FF', 0.75 * a), stroke=2.5))
    rnd = random.Random(2); cr = skia.Path()
    for k in range(6):
        x = cx + rnd.uniform(-0.8, 0.8) * s; y = cy + rnd.uniform(-0.3, 0.9) * s; cr.moveTo(x, y)
        for j in range(3): x += rnd.uniform(-0.18, 0.18) * s; y += rnd.uniform(-0.18, 0.18) * s; cr.lineTo(x, y)
    cv.drawPath(cr, P(col('#FFFFFF', 0.45 * a), stroke=2))
    hl = skia.Path(); hl.moveTo(cx - s * 0.8, cy - s * 0.4); hl.lineTo(cx - s * 0.62, cy - s * 0.3); hl.lineTo(cx - s * 0.62, cy + s * 0.45); hl.lineTo(cx - s * 0.8, cy + s * 0.35); hl.close()
    cv.drawPath(hl, P(col('#FFFFFF', 0.22 * a)))
    cv.restore()
    if 0 < u < 1: cv.drawLine(cx - s * 0.95, yc, cx + s * 0.95, yc, P(col('#EAF7FF', 0.9 * a), stroke=3, blur=2))

def block3d(cv, cx, cy, s, a=1.0, label='TUGAS', heat=0.0):
    """balok padat isometrik berlabel (makin gelap/merah saat heat naik)"""
    if a <= 0: return
    def poly(pts):
        p = skia.Path(); p.moveTo(*pts[0])
        for q in pts[1:]: p.lineTo(*q)
        p.close(); return p
    top = poly([(cx, cy - s), (cx + s * 0.95, cy - s * 0.5), (cx, cy), (cx - s * 0.95, cy - s * 0.5)])
    left = poly([(cx - s * 0.95, cy - s * 0.5), (cx, cy), (cx, cy + s * 1.05), (cx - s * 0.95, cy + s * 0.55)])
    right = poly([(cx, cy), (cx + s * 0.95, cy - s * 0.5), (cx + s * 0.95, cy + s * 0.55), (cx, cy + s * 1.05)])
    cv.drawOval(skia.Rect(cx - s * 1.2, cy + s * 0.6, cx + s * 1.2, cy + s * 1.35), P(col('#000000', 0.55 * a), blur=s * 0.2))
    base = mixc('#5A5F9E', '#8A2E3E', heat)
    cv.drawPath(left, P(col(mixc(base, '#0A0B14', 0.45), a))); cv.drawPath(right, P(col(mixc(base, '#0A0B14', 0.25), a))); cv.drawPath(top, P(col(mixc(base, '#FFFFFF', 0.15), a)))
    for p_ in (left, right, top): cv.drawPath(p_, P(col('#FFFFFF', 0.18 * a), stroke=2))
    f = font(XB, s * 0.22); w = f.measureText(label)
    cv.save(); m = skia.Matrix(); m.setAll(1, 0, cx, -0.526, 1, cy + s * 0.525, 0, 0, 1); cv.concat(m)
    cv.drawString(label, s * 0.475 - w / 2, bl(f, 0), f, P(col('#FFFFFF', 0.85 * a))); cv.restore()

def stairs(cv, cx, by, n, sw, sh, a=1.0, lit=0.0, labels=(), t=0.0):
    """tangga isometrik; anak tangga ke-0 menyala (lit) dengan label"""
    if a <= 0: return
    for k in range(n - 1, -1, -1):
        x = cx - (n - 1) * sw * 0.5 + k * sw; y = by - k * sh
        on = lit if k == 0 else 0.0
        top = skia.Path(); top.moveTo(x - sw * 0.5, y); top.lineTo(x + sw * 0.5, y); top.lineTo(x + sw * 0.5 + sw * 0.28, y - sw * 0.2); top.lineTo(x - sw * 0.5 + sw * 0.28, y - sw * 0.2); top.close()
        front = skia.Path(); front.addRect(skia.Rect(x - sw * 0.5, y, x + sw * 0.5, by + sh * 0.6))
        side = skia.Path(); side.moveTo(x + sw * 0.5, y); side.lineTo(x + sw * 0.78, y - sw * 0.2); side.lineTo(x + sw * 0.78, by + sh * 0.6 - sw * 0.2); side.lineTo(x + sw * 0.5, by + sh * 0.6); side.close()
        bc = mixc('#2E3160', MINT, on * 0.85)
        if on > 0: cv.drawPath(top, P(col(MINT, 0.6 * on * a), blur=22))
        cv.drawPath(front, P(col(mixc(bc, '#0A0B14', 0.4), a))); cv.drawPath(side, P(col(mixc(bc, '#0A0B14', 0.6), a))); cv.drawPath(top, P(col(mixc(bc, '#FFFFFF', 0.2), a)))
        cv.drawPath(top, P(col('#FFFFFF', 0.3 * a), stroke=2))
        if k < len(labels):
            mono(cv, labels[k], x + sw * 0.14, y - sw * 0.2 - 105, 24, MINT if k == 0 else ACC_L, a * (1.0 if k == 0 else 0.6), sp=1)

# ------------------------------------------------------------ A: HOOK — "MALAS" dipecah, ternyata kabur dari rasa nggak enak (0 - 4.22)
def gA(cv, t):
    push = 1 + 0.08 * eio(prog(t, 0, 4.4))
    cv.save(); cv.translate(540, 760); cv.scale(push, push); cv.translate(-540, -760)
    sx = shake(t, 0.08, 14, 0.5)
    ry = -16 + 6 * eio(prog(t, 0, 4)); rx = 8
    with plane(cv, 540 + sx, 880, 0, 700, 560, ry, rx) as ok:
        if ok: laptop(cv, 660, 1.0, t, lambda c, r, a: doc_screen(c, r, a, t), glow=0.8)
    ba = eo(prog(t, 2.41, 2.95))
    if ba > 0:
        blob(cv, 540 + 30 * math.sin(t * 1.3), lerp(820, 520, ba), 150 * lerp(0.4, 1.0, bo(ba)), t, ba, (0.6, 0.0))
        chip(cv, 'rasa nggak enak', 250, 400, ba * eo(prog(t, 2.8, 3.1)), size=28, fg='#FFB3A6', edge=CORAL)
    pa = eo(prog(t, 2.9, 3.4))
    if pa > 0:
        with plane(cv, lerp(1250, 885, pa), 930, 0, 190, 380, -24, 8) as ok:
            if ok: phone2(cv, 190, 380, pa, t, lambda c, r, a: feed_screen(c, r, a, t, 300))
        ar = skia.Path(); ar.moveTo(640, 760); ar.quadTo(780, 640, 840, 760)
        neon(cv, ar, eo(prog(t, 3.2, 3.6)), AMBER, 5, pa, 0.8, AMBER)
        if prog(t, 3.2, 3.6) >= 1:
            hd = skia.Path(); hd.moveTo(818, 742); hd.lineTo(842, 764); hd.lineTo(848, 732); cv.drawPath(hd, P(col(AMBER, pa), stroke=5))
        chip(cv, 'kabur', 745, 690, pa * eo(prog(t, 3.3, 3.6)), size=28, fg=AMBER, edge=AMBER)
    cv.restore()
    sc = lerp(1.7, 1.0, eo(prog(t, -0.06, 0.2))); cv.save(); cv.translate(540, 600); cv.scale(sc, sc); cv.translate(-540, -600)
    shatter_text(cv, 'MALAS', 540, 600 + sx * 0.3, 200, t, 1.42, clamp(prog(t, -0.06, 0.15) * 2.5)); cv.restore()
    st = prog(t, 1.3, 1.5)
    if 0 < st and t < 1.62:
        cv.drawLine(250, 640, lerp(250, 830, eo(st)), 560, P(col(CORAL, 0.6), stroke=34, blur=12)); cv.drawLine(250, 640, lerp(250, 830, eo(st)), 560, P(col('#FFFFFF', 0.95), stroke=14))
    sl = prog(t, 0.04, 0.3)
    if 0 < sl < 1:
        for k in range(2):
            rp = clamp(sl * 1.2 - k * 0.2)
            if 0 < rp < 1: cv.drawRoundRect(skia.Rect(540 - 330 - 200 * rp, 600 - 90 - 120 * rp, 540 + 330 + 200 * rp, 600 + 90 + 120 * rp), 100, 100, P(col(CORAL, 0.6 * (1 - rp)), stroke=4))

# ------------------------------------------------------------ B: bosan, cemas, bingung -> kabur ke HP (4.22 - 8.57)
FEEL = [('bosan', GREY, 'flat', 4.4), ('cemas', RED, 'sad', 5.45), ('bingung', BLUE, 'flat', 6.0)]
def gB(cv, t):
    lo = eo(prog(t, 4.22, 4.6)) * (1 - eio(prog(t, 7.0, 7.5)))
    if lo > 0:
        with plane(cv, 540, 1080, 120, 640, 520, -10 + 4 * math.sin(t * 0.7), 10) as ok:
            if ok: laptop(cv, 600, lo, t, lambda c, r, a: doc_screen(c, r, a, t), glow=0.5)
    for k, (lab, cols, mood, t0) in enumerate(FEEL):
        pa = prog(t, t0, t0 + 0.45); out = 1 - eio(prog(t, 7.0, 7.4))
        if pa > 0 and out > 0:
            x = (270, 540, 810)[k]; y = lerp(920, 520 + (k % 2) * 40, eo(pa)) + 10 * math.sin(t * 2 + k)
            r = 95 * lerp(0.5, 1, bo(pa))
            mood_ball(cv, x, y, r, clamp(pa * 2) * out, t, mood, cols, lab)
            if lab == 'bingung': mono(cv, '?', x + r * 0.85, y - r * 0.9, 56, HL, clamp(pa * 2) * out, glow=0.7)
            if lab == 'cemas': tear(cv, x + r * 0.62, y - r * 0.35, r * 0.16, clamp(pa * 2) * out)
            if lab == 'bosan': mono(cv, 'z', x + r * 0.8, y - r * 0.8 - 12 * math.sin(t * 2), 40, ACC_L, clamp(pa * 2) * out * 0.8)
    pa = eo(prog(t, 7.0, 7.45))
    if pa > 0:
        z = lerp(500, 0, pa); ry = lerp(30, -8, pa) + 4 * math.sin(t)
        with plane(cv, 540, 740, z, 380, 760, ry, 6) as ok:
            if ok: phone2(cv, 380, 760, pa, t, lambda c, r, a: feed_screen(c, r, a, t, 900))
        mins = int(lerp(5, 140, eio(prog(t, 7.4, 8.8))))
        lab = f'{mins} menit' if mins < 60 else f'{mins // 60} jam {mins % 60:02d} menit'
        mono(cv, 'scroll: ' + lab, 540, 1165, 30, AMBER, pa, sp=1, glow=0.6)

# ------------------------------------------------------------ C: riset 2013 -> memperbaiki mood sesaat (8.57 - 13.44)
def back_mood(cv, r, a):
    glass(cv, r, rad=34, a=a, glow=0.5)
    mono(cv, 'NAMANYA', 0, r.top() + 70, 25, ACC_L, 0.8 * a, sp=6)
    extrude(cv, 'MOOD REPAIR', 0, -20, 96, a, depth=10, front=('#FFFFFF', '#C7F7E4'), side='#14524A', glow=MINT)
    mono(cv, 'memperbaiki mood sesaat', 0, 90, 34, MINT, a, glow=0.5)
def gC(cv, t):
    research_card(cv, t, 8.57, '2013', 'Sirois & Pychyl', 'Social and Personality Psychology Compass', back_mood, 11.5)

# ------------------------------------------------------------ D: riset 2001 — dibuat bad mood, malah sibuk main (13.44 - 18.7)
def lab_scene(cv, t, a0, freeze=0.0, stop=0.0, done=0.0):
    mood_ball(cv, 540, 560, 120, a0, t, 'sad', tuple(mixc(c, g, 0.3) for c, g in zip(BLUE, GREY)), 'BAD MOOD')
    ice(cv, 540, 560, 175, freeze, a0, t)
    test_sheet(cv, 300, 930, 270, a0 * eo(prog(t, 14.9, 15.3)), done, dim=0.35 * (1 - stop))
    on = (1 - stop) * clamp(prog(t, 17.0, 17.3))
    ca = a0 * eo(prog(t, 15.1, 15.5))
    controller(cv, 790, 920, 160, ca, on, t)
    if stop > 0: cross(cv, 790, 920, 60, ca * stop, CORAL, 14, stop)
    return on
def gD(cv, t):
    a0 = eo(prog(t, 13.44, 13.8))
    cv.drawCircle(540, 560, 240, P(shader=rg(540, 560, 240, [col('#3F6BFF', 0.18 * a0), col('#3F6BFF', 0)])))
    for k in range(5):
        x = 470 + k * 35; ph = ((t * 1.4 + k * 0.37) % 1.0)
        cv.drawLine(x, 400 + ph * 60, x - 6, 420 + ph * 60, P(col('#8FB8FF', 0.55 * (1 - ph) * a0 * prog(t, 14.86, 15.2)), stroke=3))
    on = lab_scene(cv, t, a0)
    if on > 0:
        ar = skia.Path(); ar.moveTo(600, 700); ar.quadTo(720, 760, 760, 820)
        neon(cv, ar, eo(prog(t, 17.1, 17.4)), '#B57BFF', 5, a0, 0.8, '#B57BFF')
        mins = int(lerp(1, 14, eio(prog(t, 17.2, 18.6))))
        mono(cv, f'main: {mins} menit', 790, 1095, 28, '#C9A8FF', on, sp=1, glow=0.6)
        mono(cv, 'latihan: 0 menit', 300, 1145, 24, MUTED, on * 0.9, sp=1)
    mono(cv, 'EKSPERIMEN 2001', 540, 365, 26, ACC_L, 0.85 * a0, sp=5)

# ------------------------------------------------------------ E: mood dibekukan -> berhenti menunda (18.7 - 22.66)
def gE(cv, t):
    a0 = eo(prog(t, 18.7, 19.0)); fz = prog(t, 19.0, 20.1); stop = eo(prog(t, 21.06, 21.4)); done = prog(t, 21.3, 22.4)
    lab_scene(cv, t, a0, fz, stop, done)
    la = eo(prog(t, 20.1, 20.4))
    mono(cv, 'MOOD DIBEKUKAN', 540, 300, 32, '#BFE6FF', a0 * la, sp=4, glow=0.7)
    mono(cv, '"mood-nya nggak bisa diubah"', 540, 345, 22, ACC_L, 0.8 * a0 * la)
    if fz > 0 and fz < 1:
        for k in range(8):
            ang = k * math.tau / 8 + t; rr = 220 - 60 * fz
            cv.drawLine(540 + math.cos(ang) * rr, 560 + math.sin(ang) * rr, 540 + math.cos(ang) * (rr - 30), 560 + math.sin(ang) * (rr - 30), P(col('#DDF2FF', 0.7 * (1 - fz) * a0), stroke=3))
    if stop > 0:
        mono(cv, 'latihan dikerjakan', 300, 1145, 26, MINT, a0 * stop, sp=1, glow=0.6)

# ------------------------------------------------------------ F: lega sesaat, tugas makin berat (22.66 - 26.25)
def gF(cv, t):
    a0 = eo(prog(t, 22.66, 23.0))
    lv = 0.08 + 0.82 * bump(prog(t, 23.0, 24.3)) ** 0.6
    x0, top, bot = 230, 520, 1000; r = skia.Rect(x0 - 48, top, x0 + 48, bot)
    cv.drawRoundRect(r, 48, 48, P(col('#15162A', 0.85 * a0))); cv.drawRoundRect(r, 48, 48, P(col(ACC_XL, 0.4 * a0), stroke=2.5))
    fr = skia.Rect(x0 - 38, lerp(bot - 10, top + 10, lv), x0 + 38, bot - 10)
    if fr.height() > 10:
        cv.drawRoundRect(fr, 38, 38, P(col(MINT, 0.5 * a0), blur=18)); cv.drawRoundRect(fr, 38, 38, P(shader=lg(0, fr.top(), 0, fr.bottom(), [col('#C7F7E4', a0), col(MINT, a0)])))
    mono(cv, 'LEGA', x0, top - 45, 26, MINT, a0, sp=4)
    mono(cv, 'sesaat', x0, bot + 45, 24, ACC_L, 0.8 * a0 * eo(prog(t, 23.6, 24.0)))
    ga = eo(prog(t, 24.24, 24.6)); grow = eio(prog(t, 25.25, 26.2))
    if ga > 0:
        s = lerp(120, 205, grow) * lerp(0.6, 1, bo(ga)); by = 900
        sag = 26 * grow
        fl = skia.Path(); fl.moveTo(380, by + 30); fl.quadTo(650, by + 30 + sag * 2, 1000, by + 30)
        cv.drawPath(fl, P(col(ACC, 0.35 * a0), stroke=10, blur=8)); cv.drawPath(fl, P(col(ACC_L, 0.8 * a0), stroke=3))
        block3d(cv, 650, by + 30 + sag - s * 1.05, s, ga * a0, 'TUGAS', grow)
        if grow > 0.3: crack(cv, 650, by + 40 + sag, 90, prog(grow, 0.3, 1.0), a0, seed=7)
        mono(cv, 'deadline makin dekat', 650, 420, 26, CORAL, a0 * eo(prog(t, 25.3, 25.6)), sp=2, glow=0.5)

# ------------------------------------------------------------ G: riset 2010 — yang memaafkan diri lebih jarang menunda (26.25 - 32.53)
def gG(cv, t):
    research_card(cv, t, 26.25, '2010', 'Michael Wohl dkk.', 'Personality and Individual Differences', None, None, 700, 28.35)
    a0 = eo(prog(t, 28.5, 28.9))
    if a0 <= 0: return
    for k, (x, txt, c, fill, fg, lab) in enumerate(((290, 'dasar pemalas!', CORAL, ('#3A1C2A', '#1E0E18'), '#FFD9D2', 'MARAHIN DIRI'),
                                                  (790, 'nggak apa-apa', MINT, ('#173A30', '#0D2019'), '#D8FFF0', 'MAAFIN DIRI'))):
        pa = eo(prog(t, 28.6 + k * 0.35, 29.0 + k * 0.35))
        bust(cv, x, 700, 110, a0 * pa, c)
        thought(cv, txt, x, 470, 32, a0 * pa, c, (x, 560), lerp(0.6, 1, bo(pa)), fill, fg)
        mono(cv, lab, x, 860, 24, c, a0 * pa, sp=3)
    ba = eo(prog(t, 30.86, 31.3))
    if ba > 0:
        mono(cv, 'NUNDA DI UJIAN BERIKUTNYA', 540, 935, 22, ACC_L, 0.85 * a0 * ba, sp=2)
        for k, (x, frac, c) in enumerate(((290, 0.85, CORAL), (790, 0.32, MINT))):
            w = 380 * frac * eo(prog(t, 31.0 + k * 0.15, 31.6 + k * 0.15))
            pill_bar(cv, x - 190, x - 190 + max(56, w), 1010, 56, 1.0, '', c, a0 * ba)
        mono(cv, 'lebih jarang', 790, 1080, 26, MINT, a0 * eo(prog(t, 31.5, 31.8)), glow=0.5)

# ------------------------------------------------------------ H: jangan marahin diri; maafin, mulai dari langkah terkecil (32.53 - 36.6)
def gH(cv, t):
    a0 = eo(prog(t, 32.53, 32.9))
    ca = prog(t, 32.6, 32.95)
    shatter_text(cv, 'DASAR MALAS!', 540, 520, 96, t, 33.55, a0 * clamp(ca * 3), ('#FFFFFF', '#FFB3A6'), '#5A1530', CORAL)
    if 33.3 < t < 33.7:
        u = prog(t, 33.3, 33.5); cv.drawLine(160, 560, lerp(160, 920, eo(u)), 480, P(col(CORAL, 0.6 * a0), stroke=26, blur=10)); cv.drawLine(160, 560, lerp(160, 920, eo(u)), 480, P(col('#FFFFFF', 0.95 * a0), stroke=10))
    ma = prog(t, 34.01, 34.35)
    if ma > 0:
        thought(cv, 'nggak apa-apa, maafin dulu', 540, 470, 34, a0 * clamp(ma * 2), MINT, (540, 600), lerp(0.6, 1, bo(ma)), ('#173A30', '#0D2019'), '#D8FFF0')
        heart_shape(cv, 540, 640, 34 * bo(prog(t, 34.2, 34.5)) * (1 + 0.08 * math.sin(t * 6)), a0, MINT)
    sa = eo(prog(t, 34.75, 35.1))
    if sa > 0:
        lit = eo(prog(t, 35.4, 35.8))
        stairs(cv, 560, 1070, 4, 175, 80, a0 * sa, lit, ('buka file', 'tulis 1 kalimat', '10 menit', 'selesai'), t)
        hop = prog(t, 35.4, 35.9); x0 = 560 - 1.5 * 175
        bx = lerp(x0 - 200, x0 + 20, eio(hop)); byy = 1000 - 90 * bump(hop)
        mood_ball(cv, bx, byy, 34, a0 * sa, t, 'happy' if hop >= 1 else 'flat', GRN if hop >= 1 else GREY)

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
    ev = [(0.0, 'chop'), (0.03, 'stamp'), (0.2, 'clock'), (1.3, 'swish'), (1.42, 'crack'), (1.45, 'chop'),
          (2.41, 'fizz_soft'), (2.5, 'rise'), (2.9, 'whoosh'), (3.2, 'swish'), (3.6, 'plip'),
          (4.22, 'whoosh'), (4.4, 'pop'), (5.45, 'pop'), (6.0, 'pop'), (7.0, 'whoosh'), (7.1, 'zoom'), (7.5, 'tick'), (7.8, 'tick'), (8.1, 'tick'), (8.4, 'tick'),
          (8.57, 'whoosh'), (8.65, 'card'), (8.95, 'stamp'), (9.2, 'ding_soft'), (11.5, 'swish'), (11.85, 'chop'), (12.0, 'shine'),
          (13.44, 'whoosh'), (13.6, 'fizz_soft'), (14.9, 'card'), (15.1, 'pop'), (17.0, 'zap'), (17.2, 'boing'),
          (18.7, 'whoosh'), (19.0, 'fizz'), (20.1, 'crack'), (20.15, 'ding_soft'), (21.06, 'chop'), (21.35, 'ding'), (21.6, 'plip'), (21.9, 'plip'), (22.2, 'plip'),
          (22.66, 'whoosh'), (23.0, 'rise'), (23.7, 'sting'), (24.24, 'clunk'), (25.25, 'clunk'), (25.6, 'crack'), (25.9, 'clunk'),
          (26.25, 'whoosh'), (26.35, 'card'), (26.65, 'stamp'), (26.9, 'ding_soft'), (28.35, 'whoosh'), (28.6, 'pop'), (28.95, 'pop'),
          (30.86, 'rise'), (31.3, 'ding'),
          (32.53, 'whoosh'), (32.62, 'chop'), (33.3, 'swish'), (33.55, 'crack'), (34.01, 'shine'), (34.2, 'pop'), (34.75, 'whoosh'), (35.4, 'boing'), (35.85, 'ding'),
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



