#!/usr/bin/env python3
"""Ruang Pikir reel #4: 'Pura-pura gapapa, kok capek?' (menahan emosi vs memaknai ulang, Gross & Levenson 1997; Gross 1998)
python3 episode.py preview t1 t2 ... | timeline out.json | video out.mp4"""
import sys, os, math, json, subprocess, random
import skia
import base as b
from base import (clamp, lerp, prog, eo, ei, eio, bo, bump, col, P, lg, rg, layer, font, XB, B, M, MONO, bl, tracked, parse,
                 pill, sparkle, person, watcher_eye, scribble, spotlight, ACC, ACC_L, ACC_XL, TXT, MUTED, CORAL, MINT, W, H, FPS)

VIOLET, YELLOW, INK = '#B57BFF', '#FFD23F', '#0B0C1E'

b.GROUPS = [(0.0, 6.22, 'PSIKOLOGI'), (6.22, 8.91, 'TERNYATA'), (8.91, 23.32, 'RISET · 1997'),
            (23.32, 32.85, 'RISET · 1998'), (32.85, 36.6, 'UNTUKMU'), (36.6, 42.0, 'RUANG PIKIR')]
b.CAPS = [(0.15, "Bilang \"aku gapapa\",", "padahal [nggak baik-baik aja]?"),
          (3.48, "Senyum di luar,", "di dalam [mau meledak]"),
          (6.22, "Nahan emosi bikin", "tubuh [makin tegang]"),
          (8.91, "Tahun 1997, psikolog", "[James Gross] & tim menguji"),
          (13.13, "Peserta nonton film sedih,", "separuh [menahan ekspresi]"),
          (16.91, "Wajahnya datar, tapi", "[sedihnya tetap ada]"),
          (20.31, "Jantung & pembuluh darah", "[kerja lebih keras]"),
          (23.32, "Cara yang lebih sehat:", "[memaknai ulang]"),
          (27.87, "Perasaan reda,", "tubuh [nggak ikut tegang]"),
          (32.85, "Nggak harus selalu kuat,", "[cerita] ke orang terpercaya"),
          (36.6, "Follow [Ruang Pikir]", "biar makin kenal isi kepalamu")]

def draw_title(cv, t):
    a = eo(prog(t, 0.1, 0.55))
    if a <= 0: return
    segs = parse("Pura-pura gapapa, [kok capek]?"); size = 62; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 482) + (1 - a) * 20
    layer(cv, a); xx = x
    for s, h in segs: cv.drawString(s, xx, y + 5, f, P(col('#000000', 0.5), blur=7)); xx += f.measureText(s)
    for s, h in segs: cv.drawString(s, x, y, f, P(col(ACC_L if h else TXT))); x += f.measureText(s)
    cv.restore()
b.draw_title = draw_title

# ------------------------------------------------------------ premium background: aurora + bokeh di atas latar standar
random.seed(11)
BOKEH = [(random.uniform(60, W - 60), random.uniform(560, 1180), random.uniform(10, 36), random.uniform(0.3, 1.0),
          random.uniform(0, 6.3), random.choice((ACC, ACC_L, VIOLET))) for _ in range(14)]
def draw_bg(cv, t):
    cv.drawImage(b.bg_img(), 0, 0)
    for cx, cy, r, c, sp, ph in ((300, 760, 560, '#5B4BD6', 0.23, 0.0), (800, 1020, 600, '#3346C9', 0.19, 2.1)):
        x = cx + 110 * math.sin(t * sp + ph); y = cy + 70 * math.cos(t * sp * 0.8 + ph)
        cv.drawCircle(x, y, r, P(shader=rg(x, y, r, [col(c, 0.15), col(c, 0)])))
    for x, y, r, dep, ph, c in BOKEH:
        yy = 560 + (y - 560 - t * 9 * dep) % 640
        a = (0.035 + 0.05 * (0.5 + 0.5 * math.sin(t * 0.9 + ph))) * min(1, (yy - 560) / 80, (1200 - yy) / 80)
        if a > 0: cv.drawCircle(x + 24 * math.sin(t * 0.35 + ph), yy, r, P(col(c, a), blur=r * 0.45))
b.draw_bg = draw_bg          # tanpa titik-titik debu (permintaan ALFA sejak EP03)
b.draw_progress = lambda cv, t: None   # tanpa garis progress; tag scene tetap tampil

# ilustrasi selalu memudar lembut sebelum zona caption (y 1200-1390) dan di bawah judul
_draw_groups = b.draw_groups
_MASK = skia.Paint(Shader=lg(0, 520, 0, 1200, [col('#000000', 0), col('#000000', 1), col('#000000', 1), col('#000000', 0)],
                              [0, 40 / 680, 655 / 680, 1]), BlendMode=skia.BlendMode.kDstIn)
def draw_groups(cv, t):
    n = cv.getSaveCount(); cv.saveLayer(None, None); _draw_groups(cv, t)
    if cv.getSaveCount() != n + 1: print(f'peringatan: save/restore tidak seimbang di t={t:.2f}', file=sys.stderr); cv.restoreToCount(n + 1)
    cv.drawRect(skia.Rect(0, 0, W, H), _MASK); cv.restore()
b.draw_groups = draw_groups

# ------------------------------------------------------------ helpers
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

def rich(cv, s, cx, cy, size, a=1.0, fg=TXT, hl_shader=True, f_n=B, f_h=XB):
    """teks satu baris rata tengah; bagian [..] diberi gradasi aksen"""
    segs = parse(s); fn, fh = font(f_n, size), font(f_h, size)
    ws = [(fh if h else fn).measureText(x) for x, h in segs]; x = cx - sum(ws) / 2; y = bl(fn, cy)
    for (txt, h), w in zip(segs, ws):
        if h: cv.drawString(txt, x, y, fh, P(shader=lg(0, cy - size * 0.6, 0, cy + size * 0.6, [col('#C9CEFF', a), col(ACC, a)])))
        else: cv.drawString(txt, x, y, fn, P(col(fg, a)))
        x += w
    return sum(ws)

def chip(cv, text, x, y, a=1.0, size=26, fg=ACC_XL, bgc='#262842', f=B, edge=ACC):
    if a <= 0: return
    ff = font(f, size); w = ff.measureText(text); h = size * 1.7
    r = skia.Rect.MakeXYWH(x - w / 2 - 22, y - h / 2, w + 44, h)
    cv.drawRoundRect(r, h / 2, h / 2, P(col(bgc, a))); cv.drawRoundRect(r, h / 2, h / 2, P(col(edge, 0.45 * a), stroke=2))
    cv.drawString(text, x - w / 2, bl(ff, y), ff, P(col(fg, a)))

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

def x_mark(cv, cx, cy, r, p_, a=1.0):
    if p_ <= 0 or a <= 0: return
    s = bo(prog(p_, 0, 0.5)); cv.save(); cv.translate(cx, cy); cv.scale(s, s)
    cv.drawCircle(0, 0, r * 1.3, P(col(CORAL, 0.35 * a), blur=r * 0.5)); cv.drawCircle(0, 0, r, P(col(CORAL, a)))
    k = r * 0.36
    cv.drawLine(-k, -k, k, k, P(col('#2A0E12', a), stroke=r * 0.2)); cv.drawLine(-k, k, k, -k, P(col('#2A0E12', a), stroke=r * 0.2))
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

def ghost(cv, x, foot, h, a, t, look=(-1, 0)):
    """'diri dari luar': sosok kaca bercahaya"""
    bw, bh, hr = 0.42 * h, 0.6 * h, 0.17 * h
    fl = 7 * math.sin(t * 2.0); hx, hy = x, foot - bh - hr * 0.92 + fl
    if a <= 0: return hx, hy, hr
    cv.drawOval(skia.Rect(x - bw, foot - 14, x + bw, foot + 16), P(shader=rg(x, foot, bw, [col(ACC, 0.35 * a), col(ACC, 0)])))
    body = skia.RRect.MakeRectXY(skia.Rect(x - bw / 2, foot - bh + fl, x + bw / 2, foot - 8 + fl), bw * 0.45, bw * 0.45)
    for (draw, args) in ((cv.drawRRect, (body,)), (cv.drawCircle, (hx, hy, hr))):
        draw(*args, P(col(ACC, 0.4 * a), stroke=20, blur=22))
    cv.drawRRect(body, P(shader=lg(0, foot - bh, 0, foot, [col('#A7B0FF', 0.36 * a), col('#7F8CFF', 0.03 * a)])))
    cv.drawCircle(hx, hy, hr, P(shader=rg(hx - hr * 0.3, hy - hr * 0.4, hr * 1.7, [col('#D6DAFF', 0.55 * a), col('#7F8CFF', 0.14 * a)])))
    cv.drawRRect(body, P(shader=lg(0, foot - bh, 0, foot, [col(ACC_XL, 0.9 * a), col(ACC_L, 0.1 * a)]), stroke=3))
    cv.drawCircle(hx, hy, hr, P(col(ACC_XL, 0.95 * a), stroke=3))
    bk = blink_at(t, 0.4)
    for s in (-1, 1):
        ex = hx + s * hr * 0.36 + look[0] * hr * 0.12; eh = hr * 0.16 * (1 - 0.9 * bk)
        cv.drawOval(skia.Rect(ex - hr * 0.12, hy - hr * 0.05 - eh, ex + hr * 0.12, hy - hr * 0.05 + eh), P(col('#FFFFFF', a)))
    m = skia.Path(); my = hy + hr * 0.4; m.moveTo(hx - hr * 0.28, my - hr * 0.04); m.quadTo(hx, my + hr * 0.26, hx + hr * 0.28, my - hr * 0.04)
    cv.drawPath(m, P(col('#FFFFFF', a), stroke=max(2.5, hr * 0.07)))
    return hx, hy, hr

# ------------------------------------------------------------ helper EP04
def smile_mask(cv, hx, hy, hr, a=1.0, crack=0.0, dx=0.0, dy=0.0, rot=0.0, stick=True):
    """topeng senyum yang dipegang di depan wajah"""
    if a <= 0: return
    cv.save(); cv.translate(hx + dx, hy + dy); cv.rotate(rot); layer(cv, a)
    w, h = hr * 1.1, hr * 1.2
    if stick:
        cv.drawLine(w * 0.5, h * 0.75, w * 1.15, h * 2.7, P(col('#8C95E8'), stroke=hr * 0.11))
        cv.drawLine(w * 0.5, h * 0.75, w * 1.15, h * 2.7, P(col('#E3E6FF', 0.7), stroke=hr * 0.04))
    oval = skia.Rect(-w, -h, w, h); op = skia.Path(); op.addOval(oval)
    cv.drawOval(oval.makeOffset(0, hr * 0.14), P(col('#000000', 0.45), blur=hr * 0.25))
    cv.drawOval(oval, P(col(ACC, 0.55), blur=hr * 0.4))
    cv.drawOval(oval, P(shader=lg(0, -h, 0, h, [col('#FFFFFF'), col('#DDE0FF'), col('#A9B2FF')], [0, 0.55, 1])))
    cv.save(); cv.clipPath(op, skia.ClipOp.kIntersect, True)
    cv.drawOval(skia.Rect(-w * 0.85, -h * 1.1, w * 0.45, -h * 0.2), P(col('#FFFFFF', 0.6), blur=hr * 0.12))
    cv.restore()
    cv.drawOval(oval, P(col('#8C95E8'), stroke=max(2, hr * 0.045)))
    for s in (-1, 1):
        ex, ey = s * w * 0.38, -h * 0.12; e = skia.Path()
        e.moveTo(ex - hr * 0.17, ey + hr * 0.05); e.quadTo(ex, ey - hr * 0.17, ex + hr * 0.17, ey + hr * 0.05)
        cv.drawPath(e, P(col(INK), stroke=hr * 0.075))
        cv.drawOval(skia.Rect.MakeXYWH(ex - hr * 0.17, h * 0.12, hr * 0.34, hr * 0.15), P(col('#FF8FA8', 0.6), blur=hr * 0.05))
    m = skia.Path(); m.moveTo(-w * 0.46, h * 0.24); m.quadTo(0, h * 0.78, w * 0.46, h * 0.24); m.quadTo(0, h * 0.42, -w * 0.46, h * 0.24); m.close()
    cv.drawPath(m, P(col(INK)))
    if crack > 0:
        cp = skia.Path(); pts = [(w * 0.12, -h * 1.0), (-w * 0.04, -h * 0.62), (w * 0.18, -h * 0.4), (-w * 0.02, -h * 0.12), (w * 0.12, h * 0.1)]
        cp.moveTo(*pts[0])
        for q in pts[1:]: cp.lineTo(*q)
        mm = skia.PathMeasure(cp, False); seg = skia.Path(); mm.getSegment(0, mm.getLength() * eo(crack), seg, True)
        cv.save(); cv.clipPath(op, skia.ClipOp.kIntersect, True)
        cv.drawPath(seg, P(col(CORAL, 0.6), stroke=hr * 0.1, blur=hr * 0.05)); cv.drawPath(seg, P(col(INK), stroke=hr * 0.045))
        cv.restore()
    cv.restore(); cv.restore()

def gauge(cv, cx, cy, r, v, a=1.0, t=0.0):
    """meter tekanan setengah lingkaran; v 0..1, bergetar di zona merah"""
    if a <= 0: return
    hot = prog(v, 0.78, 0.95)
    if hot > 0: cv.drawCircle(cx, cy - r * 0.3, r * 1.25, P(shader=rg(cx, cy - r * 0.3, r * 1.25, [col(CORAL, 0.35 * hot * a), col(CORAL, 0)])))
    tr = skia.Path(); tr.addArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), 180, 180)
    cv.drawPath(tr, P(col('#FFFFFF', 0.08 * a), stroke=r * 0.22))
    cv.drawPath(tr, P(shader=lg(cx - r, 0, cx + r, 0, [col(MINT, a), col(YELLOW, a), col(CORAL, a)]), stroke=r * 0.16))
    for k in range(11):
        ang = math.radians(180 + k * 18); r0, r1 = r * 0.74, r * (0.62 if k % 5 == 0 else 0.67)
        cv.drawLine(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0, cx + math.cos(ang) * r1, cy + math.sin(ang) * r1, P(col('#FFFFFF', 0.45 * a), stroke=max(2, r * 0.025)))
    vv = clamp(v + hot * 0.025 * math.sin(t * 70))
    ang = math.radians(180 + 180 * vv); L = r * 0.78
    cv.drawLine(cx, cy, cx + math.cos(ang) * L, cy + math.sin(ang) * L, P(col(CORAL, 0.5 * a), stroke=r * 0.11, blur=r * 0.06))
    cv.drawLine(cx, cy, cx + math.cos(ang) * L, cy + math.sin(ang) * L, P(col(TXT, a), stroke=r * 0.055))
    cv.drawCircle(cx, cy, r * 0.12, P(col(TXT, a))); cv.drawCircle(cx, cy, r * 0.055, P(col(CORAL, a)))

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

def storm(cv, cx, cy, r, a, t):
    """isi dada: badai emosi di balik senyum"""
    if a <= 0: return
    p = skia.Path(); p.addCircle(cx, cy, r)
    cv.drawCircle(cx, cy, r * 1.35, P(col(CORAL, 0.35 * a), blur=r * 0.4))
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawCircle(cx, cy, r, P(shader=rg(cx, cy, r, [col('#5A1F2A', a), col('#2A0E16', a)])))
    for k in range(3):
        cv.save(); cv.translate(cx, cy); cv.rotate(t * (120 + k * 60) * (1 if k % 2 else -1))
        arc = skia.Path(); rr = r * (0.35 + k * 0.2); arc.addArc(skia.Rect(-rr, -rr, rr, rr), k * 40, 200)
        cv.drawPath(arc, P(col('#FF9A8A', 0.55 * a), stroke=r * 0.07)); cv.restore()
    if int(t * 7) % 4 != 0:
        bolt = skia.Path(); bolt.moveTo(cx + r * 0.1, cy - r * 0.7); bolt.lineTo(cx - r * 0.2, cy + r * 0.05); bolt.lineTo(cx + r * 0.05, cy + r * 0.05)
        bolt.lineTo(cx - r * 0.15, cy + r * 0.75); bolt.lineTo(cx + r * 0.3, cy - r * 0.15); bolt.lineTo(cx + r * 0.02, cy - r * 0.15); bolt.close()
        cv.drawPath(bolt, P(col(YELLOW, 0.5 * a), blur=r * 0.12)); cv.drawPath(bolt, P(col('#FFE58A', a)))
    cv.restore()
    cv.drawCircle(cx, cy, r, P(shader=lg(cx - r, cy - r, cx + r, cy + r, [col('#FFC2B8', 0.9 * a), col(CORAL, 0.4 * a)]), stroke=3))

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

def meter_row(cv, y, kind, label, c, ghost_v, v, a, t):
    if a <= 0: return
    icon(cv, kind, 150, y, 32, c, a, t)
    cv.drawString(label, 205, bl(font(B, 27), y - 26), font(B, 27), P(col(TXT, a)))
    x0, x1, by = 205, 930, y + 16
    cv.drawRoundRect(skia.Rect(x0, by - 13, x1, by + 13), 13, 13, P(col('#FFFFFF', 0.07 * a)))
    if v > 0.01:
        r = skia.Rect(x0, by - 13, x0 + (x1 - x0) * v, by + 13)
        cv.drawRoundRect(r, 13, 13, P(col(c, 0.45 * a), blur=10))
        cv.drawRoundRect(r, 13, 13, P(shader=lg(x0, 0, r.right(), 0, [col(c, 0.55 * a), col(c, a)])))
    gx = x0 + (x1 - x0) * ghost_v
    cv.drawLine(gx, by - 24, gx, by + 24, P(col('#FFFFFF', 0.75 * a), stroke=3, effect=skia.DashPathEffect.Make([6, 5], 0)))

def flip_card(cv, cx, cy, w, h, p_, front, back, a=1.0):
    """kartu pikiran yang dibalik (sumbu vertikal); front/back = (teks, warna, fill)"""
    if a <= 0: return
    sx = abs(math.cos(math.pi * p_)); side = back if p_ >= 0.5 else front
    txt, c, fill = side
    cv.save(); cv.translate(cx, cy); cv.scale(max(sx, 0.02), 1); cv.translate(-cx, -cy)
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    pth = glass(cv, r, 36, a, glow=0.6, gc=c, edge=c, fill=fill)
    glow_text(cv, txt, cx, cy, font(XB, 50), TXT, a)
    cv.restore()
    return pth, r

# ------------------------------------------------------------ 0: PSIKOLOGI (0 - 6.22)
def g0(cv, t):
    a0 = eo(prog(t, 0.05, 0.5))
    spotlight(cv, 540, 1150, 215, a0 * 0.8, top=585)
    halo(cv, 540, 1150, 260, ACC, 0.45 * a0)
    inside = prog(t, 4.6, 5.0)
    shake = 2.5 * math.sin(t * 60) * prog(t, 5.3, 5.6) * (1 - prog(t, 6.0, 6.3))
    hx, hy, hr = person(cv, 540 + shake, 1150, 360, mood='worried', a=a0, glow=1 + 0.8 * inside, blink=blink_at(t, 0.2))
    chest = (540 + shake, 1150 - 216 * 0.52)
    # air mata dari balik topeng
    for k, t0 in enumerate((2.0, 2.55)):
        tp = prog(t, t0, t0 + 1.0)
        if 0 < tp < 1: tear(cv, hx - hr * (0.5 + 0.12 * k), hy + hr * 1.08 + tp * hr * 1.5, hr * 0.34, eo(prog(tp, 0, 0.15)) * (1 - prog(tp, 0.7, 1.0)) * a0)
    smile_mask(cv, hx, hy, hr, a0, crack=prog(t, 5.6, 5.85), dx=-hr * 0.08 + 0.3 * shake, rot=-3 + 2 * math.sin(t * 1.3))
    # "Aku gapapa kok."
    ba = prog(t, 0.85, 1.25) * (1 - prog(t, 4.3, 4.6))
    if ba > 0:
        cv.save(); cv.translate(790, 690); s = 0.7 + 0.3 * bo(ba); cv.scale(s, s); cv.translate(-790, -690)
        pth, r = bubble_path(790, 690, 380, 96, (hx + hr * 0.9, hy - hr * 0.7))
        draw_bubble(cv, pth, r, clamp(ba * 2), glow=0.35)
        glow_text(cv, 'Aku gapapa kok.', 790, 690, font(XB, 40), TXT, clamp(ba * 2))
        cv.restore()
    # di dalam: badai + meter tekanan
    if inside > 0:
        storm(cv, chest[0], chest[1], 64 * (0.6 + 0.4 * bo(inside)), inside * a0, t)
        ga = eo(prog(t, 4.75, 5.15))
        r = skia.Rect(70, 640, 400, 900)
        cv.save(); cv.translate(0, (1 - ga) * 30)
        glass(cv, r, 30, ga, glow=0.5 * prog(t, 5.4, 5.8), gc=CORAL, edge=CORAL)
        tracked(cv, 'TEKANAN', 235, 682, font(MONO, 20), P(col(CORAL, ga)), 4)
        gauge(cv, 235, 845, 118, lerp(0.12, 0.93, eio(prog(t, 4.9, 5.9))), ga, t)
        cv.restore()
        if ga > 0:
            ln = skia.Path(); ln.moveTo(400, 800); ln.cubicTo(450, 840, 450, 960, chest[0] - 64, chest[1])
            cv.drawPath(ln, P(col(CORAL, 0.7 * ga), stroke=3, effect=skia.DashPathEffect.Make([10, 8], -t * 40)))
        for k in range(4):
            sp = ((t * 0.9 + k * 0.25) % 1.0); sa = prog(t, 5.5, 5.8) * (1 - sp)
            if sa > 0: cv.drawCircle(235 + 30 * math.sin(k * 2.1 + t * 2), 700 - sp * 90, 10 + sp * 18, P(col('#FFC2B8', 0.35 * sa), blur=8))

# ------------------------------------------------------------ 1: TERNYATA (6.22 - 8.91)
G1_F = (0.9, 2.6, 2.2)        # detak: 0.9 -> 2.6 per detik selama 2.2 dtk
def g1(cv, t):
    a = eo(prog(t, 6.25, 6.7))
    x, foot, h = 540, 1175, 540
    bw, bh, hr = 0.42 * h, 0.6 * h, 0.17 * h; hx, hy = x, foot - bh - hr * 0.92
    tens = eio(prog(t, 6.8, 8.3))
    ph = accel_phase(t, 6.3, *G1_F); pu = beat_pulse(ph)
    body = skia.RRect.MakeRectXY(skia.Rect(x - bw / 2, foot - bh, x + bw / 2, foot), bw * 0.45, bw * 0.45)
    halo(cv, x, foot - bh * 0.6, 420, CORAL, (0.3 + 0.5 * tens) * a)
    cv.drawRRect(body, P(col(ACC, 0.35 * a), stroke=18, blur=20)); cv.drawCircle(hx, hy, hr, P(col(ACC, 0.35 * a), stroke=18, blur=20))
    cv.drawRRect(body, P(shader=lg(0, foot - bh, 0, foot, [col('#2A2C4A', 0.85 * a), col('#14152A', 0.85 * a)])))
    cv.drawCircle(hx, hy, hr, P(shader=rg(hx - hr * 0.3, hy - hr * 0.4, hr * 1.7, [col('#3A3D60', a), col('#1A1B30', a)])))
    cv.drawRRect(body, P(col(ACC_L, 0.8 * a), stroke=3)); cv.drawCircle(hx, hy, hr, P(col(ACC_L, 0.8 * a), stroke=3))
    # pembuluh darah dari jantung
    hcx, hcy = x - bw * 0.1, foot - bh * 0.66
    ends = [(hx - hr * 0.2, hy + hr * 0.7), (hx + hr * 0.3, hy + hr * 0.8), (x - bw * 0.38, foot - bh * 0.3), (x + bw * 0.38, foot - bh * 0.35),
            (x - bw * 0.25, foot - 20), (x + bw * 0.22, foot - 20), (x + bw * 0.4, foot - bh * 0.72), (x - bw * 0.4, foot - bh * 0.8)]
    cv.save(); clipb = skia.Path(); clipb.addRRect(body); clipb.addCircle(hx, hy, hr); cv.clipPath(clipb, skia.ClipOp.kIntersect, True)
    for k, (ex, ey) in enumerate(ends):
        d = eo(prog(t, 6.8 + k * 0.08, 7.6 + k * 0.08))
        if d <= 0: continue
        pth = skia.Path(); pth.moveTo(hcx, hcy); pth.cubicTo(hcx + (ex - hcx) * 0.3 + (18 if k % 2 else -18), hcy + (ey - hcy) * 0.2, ex - (ex - hcx) * 0.2, ey - (ey - hcy) * 0.35, ex, ey)
        mm = skia.PathMeasure(pth, False); seg = skia.Path(); mm.getSegment(0, mm.getLength() * d, seg, True)
        cv.drawPath(seg, P(col(CORAL, (0.25 + 0.35 * pu) * a), stroke=14, blur=8)); cv.drawPath(seg, P(col('#FF9A8A', 0.9 * a), stroke=4))
        if d >= 1: comet(cv, pth, (ph * 0.9 + k * 0.13) % 1.0, c='#FFE1DB', n=6, r=7)
    cv.restore()
    hs = 46 * (1 + 0.22 * pu)
    cv.drawPath(heart_path(hcx, hcy, hs * 1.25), P(col(CORAL, (0.4 + 0.5 * pu) * a), blur=20))
    cv.drawPath(heart_path(hcx, hcy, hs), P(shader=lg(0, hcy - hs, 0, hcy + hs, [col('#FF9A8A', a), col(CORAL, a)])))
    for k in range(2):
        rp = ((ph + k * 0.5) % 1.0)
        cv.drawCircle(hcx, hcy, hs * (1.2 + rp * 2.2), P(col(CORAL, 0.5 * (1 - rp) * a * tens), stroke=3))
    smile_mask(cv, hx, hy, hr, a, crack=1.0, dx=-hr * 0.06, rot=-3, stick=False)
    pill(cv, 'makin tegang', 830, 760, prog(t, 7.95, 8.3), bgc=CORAL, fg='#2A0E12', size=32)

# ------------------------------------------------------------ 2: RISET · 1997 (8.91 - 23.32)
def research_card(cv, t):
    ent = prog(t, 8.95, 9.5); ext = prog(t, 12.85, 13.2)
    if ent <= 0 or ext >= 1: return
    a = clamp(ent * 2) * (1 - ext)
    cv.save(); cv.translate(540, 860); s = (0.86 + 0.14 * bo(ent)) * (1 - 0.35 * ei(ext)); cv.scale(s, s * (0.75 + 0.25 * eo(ent))); cv.translate(-540, -860 - 120 * ei(ext))
    rays(cv, 540, 860, 560, 0.5 * a, t, n=12, spin=3)
    pa = eo(prog(t, 9.1, 9.7)) * a
    if pa > 0:
        cv.save(); cv.translate(625, 770); cv.rotate(2 + 5 * pa)
        r = skia.Rect(-250, -190, 250, 190)
        cv.drawRoundRect(r.makeOffset(0, 16), 18, 18, P(col('#000000', 0.5 * pa), blur=20))
        cv.drawRoundRect(r, 18, 18, P(shader=lg(0, -190, 0, 190, [col('#2B2D46', pa), col('#1B1C2C', pa)]))); cv.drawRoundRect(r, 18, 18, P(col(ACC, 0.3 * pa), stroke=2))
        cv.drawString('Hiding feelings', -222, -136, font(B, 22), P(col(ACC_XL, 0.85 * pa)))
        cv.drawString('J. Abnormal Psychology', -222, -106, font(M, 18), P(col(MUTED, pa)))
        for k in range(6): cv.drawLine(-222, -66 + k * 26, 222 - (k % 3) * 60, -66 + k * 26, P(col('#FFFFFF', 0.07 * pa), stroke=7))
        cv.restore()
    r = skia.Rect(170, 690, 910, 1080)
    pth = glass(cv, r, 34, a, glow=0.35, fill=('#262842', '#131422'))
    sheen(cv, pth, r, prog(t, 9.55, 10.4))
    tracked(cv, 'PENELITI', 540, 736, font(MONO, 22), P(col(ACC_L, a)), 6)
    glow_text(cv, 'James Gross', 540, 792, font(XB, 66), TXT, a)
    glow_text(cv, '& Robert Levenson', 540, 846, font(B, 32), ACC_XL, a)
    glow_text(cv, '1997', 540, 950, font(XB, 128), a=a, glow=0.5, shader=lg(0, 895, 0, 1005, [col('#E3E6FF', a), col(ACC, a)]))
    chip(cv, '180 peserta', 540, 1035, eo(prog(t, 10.3, 10.6)) * a)
    cv.restore()
    st = prog(t, 11.85, 12.15)
    if st > 0 and ext < 1:
        layer(cv, 1 - ext); b_stamp(cv, 'MENAHAN EMOSI', 760, 1100, st); cv.restore()

def b_stamp(cv, text, cx, cy, p_, c=CORAL, rot=-10, size=34):
    if p_ <= 0: return
    cv.save(); cv.translate(cx, cy); cv.rotate(rot); s = 1.8 - 0.8 * eo(p_); cv.scale(s, s); layer(cv, clamp(p_ * 2))
    f = font(XB, size); w = f.measureText(text)
    r = skia.Rect(-w / 2 - 26, -size * 0.85, w / 2 + 26, size * 0.85)
    cv.drawRoundRect(r, 14, 14, P(col(c, 0.4), blur=14))
    cv.drawRoundRect(r, 14, 14, P(col('#0B0B10', 0.88))); cv.drawRoundRect(r, 14, 14, P(col(c), stroke=5))
    cv.drawString(text, -w / 2, bl(f, 0), f, P(col(c))); cv.restore(); cv.restore()

def film_test(cv, t):
    ent = prog(t, 13.15, 13.6); ext = prog(t, 16.85, 17.15)
    if ent <= 0 or ext >= 1: return
    a = eo(ent) * (1 - eio(ext))
    layer(cv, a)
    # layar film sedih
    r = skia.Rect(250, 600, 830, 880)
    cv.save(); cv.translate(540, 740); s = 0.85 + 0.15 * bo(ent); cv.scale(s, s); cv.translate(-540, -740)
    glass(cv, r, 28, 1, glow=0.3)
    sc = skia.Rect(272, 622, 808, 858)
    cv.drawRoundRect(sc, 18, 18, P(shader=lg(0, sc.top(), 0, sc.bottom(), [col('#1C1F3A'), col('#0E0F1E')])))
    cv.save(); cv.clipRect(sc)
    for k in range(18):
        rx = 300 + (k * 53) % 500; ry = 640 + ((t * 260 + k * 47) % 230)
        cv.drawLine(rx, ry, rx - 6, ry + 18, P(col('#8FA6FF', 0.45), stroke=3))
    cv.restore()
    for (dx, dy, rr) in ((-60, 0, 46), (0, -26, 60), (62, 4, 44)): cv.drawCircle(540 + dx, 720 + dy, rr, P(col('#5B6290')))
    tracked(cv, 'FILM SEDIH', 335, 834, font(MONO, 18), P(col(ACC_L)), 3)
    cv.drawRoundRect(skia.Rect(470, 829, 790, 837), 4, 4, P(col('#FFFFFF', 0.12)))
    cv.drawRoundRect(skia.Rect(470, 829, 470 + 320 * prog(t, 13.3, 16.8), 837), 4, 4, P(col(ACC_L)))
    cv.restore()
    # dua penonton
    for i, (x, lab, c) in enumerate(((340, 'NONTON BIASA', ACC_L), (740, 'TAHAN EKSPRESI', CORAL))):
        pa = eo(prog(t, 13.9 + i * 0.25, 14.3 + i * 0.25))
        if pa <= 0: continue
        hx, hy, hr = person(cv, x, 1175, 230, mood='worried' if i == 0 else 'neutral', look=(0, -0.5), a=pa, blink=blink_at(t, 0.3 + i * 0.4))
        if i == 0:
            for k in range(2):
                tp = ((t * 0.8 + k * 0.5) % 1.0); tear(cv, hx - hr * 0.36, hy + hr * 0.1 + tp * hr * 1.2, hr * 0.13, pa * (1 - tp))
        else:
            la = prog(t, 14.95, 15.3)
            if la > 0:
                cv.save(); cv.translate(hx + hr * 1.15, hy + hr * 0.35); cv.scale(bo(la), bo(la))
                cv.drawCircle(0, 0, 30, P(col(CORAL, 0.4), blur=10)); icon(cv, 'lock', 0, 0, 26, CORAL, 1, t); cv.restore()
        chip(cv, lab, x, 918, pa * clamp(prog(t, 14.4 + i * 0.5, 14.7 + i * 0.5) * 2), size=21, f=MONO, fg=c, edge=c)
    cv.restore()

def results(cv, t):
    ent = prog(t, 16.95, 17.4)
    if ent <= 0: return
    a = eo(ent)
    r = skia.Rect(80, 615, 1000, 1150)
    cv.save(); cv.translate(0, (1 - a) * 40)
    glass(cv, r, 34, a, glow=0.25)
    tracked(cv, 'YANG MENAHAN EKSPRESI', 330, 662, font(MONO, 20), P(col(CORAL, a)), 3)
    cv.drawLine(760, 662, 790, 662, P(col('#FFFFFF', 0.75 * a), stroke=3, effect=skia.DashPathEffect.Make([6, 5], 0)))
    cv.drawString('nonton biasa', 800, bl(font(B, 21), 662), font(B, 21), P(col(MUTED, a)))
    cv.drawLine(110, 692, 970, 692, P(col('#FFFFFF', 0.06 * a), stroke=2))
    # 1. ekspresi wajah: turun
    r1 = eo(prog(t, 17.2, 17.6)) * a; v1 = lerp(0.8, 0.18, eio(prog(t, 17.5, 18.5)))
    meter_row(cv, 775, 'face', 'Ekspresi wajah', ACC_L, 0.8, v1 * eo(prog(t, 17.2, 17.5)) if t < 17.5 else v1, r1, t)
    chip(cv, 'datar', 860, 742, eo(prog(t, 18.4, 18.7)) * a, size=22, fg=ACC_XL)
    # 2. rasa sedih: tetap
    r2 = eo(prog(t, 18.55, 18.9)) * a; v2 = 0.7 * eo(prog(t, 18.6, 19.3))
    meter_row(cv, 915, 'cloud', 'Rasa sedih', '#8FA6FF', 0.7, v2, r2, t)
    chip(cv, 'tetap ada', 845, 882, eo(prog(t, 19.25, 19.55)) * a, size=22, fg='#C9D4FF')
    # 3. jantung & pembuluh darah: naik
    r3 = eo(prog(t, 20.35, 20.7)) * a; v3 = lerp(0.0, 0.5, eo(prog(t, 20.4, 20.9))) + 0.38 * eio(prog(t, 20.9, 22.0))
    meter_row(cv, 1055, 'heart', 'Jantung & pembuluh darah', CORAL, 0.5, v3, r3, t)
    chip(cv, 'lebih keras', 830, 1022, eo(prog(t, 21.9, 22.2)) * a, size=22, fg='#FFC9BF', bgc='#3A2228', edge=CORAL)
    cv.restore()

def g2(cv, t):
    research_card(cv, t); film_test(cv, t); results(cv, t)

# ------------------------------------------------------------ 3: RISET · 1998 (23.32 - 32.85)
def g3(cv, t):
    # studi lanjutan: menahan vs memaknai ulang
    ca = eo(prog(t, 23.4, 23.85)) * (1 - eio(prog(t, 27.55, 27.9)))
    if ca > 0:
        cv.save(); cv.translate(0, (1 - eo(prog(t, 23.4, 23.85))) * 30); layer(cv, ca)
        r = skia.Rect(240, 610, 840, 760)
        pth = glass(cv, r, 30, 1, glow=0.3)
        sheen(cv, pth, r, prog(t, 23.9, 24.6))
        tracked(cv, 'STUDI LANJUTAN', 540, 645, font(MONO, 20), P(col(ACC_L)), 4)
        glow_text(cv, 'James Gross · 1998', 540, 700, font(XB, 50), TXT)
        hl = prog(t, 25.9, 26.3)
        for i, (x, kind, lab, c) in enumerate(((300, 'lock', 'Menahan', CORAL), (780, 'reframe', 'Memaknai ulang', MINT))):
            pa = eo(prog(t, 24.25 + i * 0.3, 24.65 + i * 0.3))
            if pa <= 0: continue
            on = hl if i == 1 else 0; dim = 1 - 0.55 * hl if i == 0 else 1
            rr = skia.Rect(x - 215, 815, x + 215, 1095)
            if on > 0: rays(cv, x, 955, 330, 0.7 * on, t, n=14, c=MINT)
            cv.save(); cv.translate(x, 955); s = (0.85 + 0.15 * bo(pa)) * (1 + 0.06 * on); cv.scale(s, s); cv.translate(-x, -955)
            glass(cv, rr, 32, pa * dim, glow=0.8 * on, gc=c, edge=c)
            icon(cv, kind, x, 915, 48, c, pa * dim, t)
            glow_text(cv, lab, x, 1012, font(XB, 38), TXT, pa * dim)
            cv.restore()
        if hl > 0: check_mark(cv, 975, 830, 30, prog(t, 26.2, 26.7))
        cv.restore(); cv.restore()
    # contoh: pesan cuek -> "dia benci aku" -> dibalik -> "dia lagi capek"
    ma = eo(prog(t, 27.95, 28.3))
    if ma <= 0: return
    cv.save(); cv.translate(0, (1 - ma) * 30); layer(cv, ma)
    cv.drawCircle(175, 660, 34, P(shader=lg(0, 626, 0, 694, [col('#7FD4FF'), col(ACC)])))
    f = font(XB, 30); cv.drawString('R', 175 - f.measureText('R') / 2, bl(f, 660), f, P(col(INK)))
    cv.drawString('teman', 228, bl(font(B, 21), 632), font(B, 21), P(col(MUTED)))
    br = skia.Rect(228, 646, 340, 700); cv.drawRoundRect(br, 22, 22, P(col('#2A2C40'))); cv.drawRoundRect(br, 22, 22, P(col(MUTED, 0.5), stroke=2))
    cv.drawString('ok.', 254, bl(font(B, 30), 673), font(B, 30), P(col(TXT)))
    cv.drawString('dibaca 22.14', 360, bl(font(M, 20), 690), font(M, 20), P(col(MUTED)))
    cv.restore(); cv.restore()
    fp = eio(prog(t, 29.7, 30.25)); fa = eo(prog(t, 28.35, 28.75))
    if fa > 0:
        cv.save(); cv.translate(540, 845); s = 0.7 + 0.3 * bo(fa); cv.scale(s, s); cv.translate(-540, -845)
        res = flip_card(cv, 540, 845, 720, 160, fp, ('Dia benci aku...', CORAL, ('#3A2228', '#1E1418')), ('Dia lagi capek.', MINT, ('#173A2E', '#0F1F19')), clamp(fa * 2))
        cv.restore()
        if fp >= 1: check_mark(cv, 880, 772, 32, prog(t, 30.3, 30.8))
        if fp < 0.5: tracked(cv, 'PIKIRANMU', 540, 742, font(MONO, 19), P(col(MUTED, fa)), 4)
    # efeknya: perasaan reda, tubuh tetap tenang
    for i, (x, kind, lab) in enumerate(((310, 'cloud', 'PERASAAN'), (770, 'heart', 'TUBUH'))):
        pa = eo(prog(t, 30.55 + i * 0.6, 30.9 + i * 0.6))
        if pa <= 0: continue
        r = skia.Rect(x - 215, 975, x + 215, 1135)
        glass(cv, r, 28, pa, glow=0.4 * pa, gc=MINT, edge=MINT)
        icon(cv, kind, x - 140, 1055, 34, MINT, pa, t * 0.6)
        tracked(cv, lab, x + 35, 1018, font(MONO, 19), P(col(MINT, pa)), 3)
        if i == 0:
            v = lerp(0.85, 0.3, eio(prog(t, 30.7, 31.5)))
            bx0, bx1 = x - 85, x + 175
            cv.drawRoundRect(skia.Rect(bx0, 1058, bx1, 1080), 11, 11, P(col('#FFFFFF', 0.08 * pa)))
            cc = CORAL if v > 0.6 else MINT
            cv.drawRoundRect(skia.Rect(bx0, 1058, bx0 + (bx1 - bx0) * v, 1080), 11, 11, P(col(cc, pa)))
            cv.drawString('reda', x + 10, bl(font(B, 24), 1108), font(B, 24), P(col(TXT, pa * prog(t, 31.3, 31.6))))
        else:
            ln = skia.Path()
            for k in range(81):
                u = k / 80; xx = lerp(x - 85, x + 175, u); ph = u * 2.2 + t * 0.9
                yy = 1070 - 22 * math.exp(-(((ph % 1.0) - 0.5) / 0.05) ** 2)
                (ln.moveTo if k == 0 else ln.lineTo)(xx, yy)
            cv.drawPath(ln, P(col(MINT, 0.4 * pa), stroke=8, blur=5)); cv.drawPath(ln, P(col(MINT, pa), stroke=3))
            cv.drawString('tetap tenang', x - 20, bl(font(B, 24), 1110), font(B, 24), P(col(TXT, pa)))

# ------------------------------------------------------------ 4: UNTUKMU (32.85 - 36.6)
def g4(cv, t):
    a = eo(prog(t, 32.9, 33.3))
    warm = eo(prog(t, 34.3, 35.0))
    halo(cv, 560, 960, 420, '#FFB38A', 0.35 * warm)
    halo(cv, 560, 960, 380, ACC, 0.5 * a)
    lower = eio(prog(t, 33.2, 34.0))
    calm = prog(t, 34.0, 34.3); happy = prog(t, 35.4, 35.6)
    hx, hy, hr = person(cv, 420, 1150, 330, mood='happy' if happy > 0.5 else ('neutral' if calm > 0.5 else 'worried'), look=(1, 0), a=a,
                        glow=1 + warm, blink=blink_at(t, 0.5))
    smile_mask(cv, hx, hy, hr, a * (1 - prog(t, 33.7, 34.1)), crack=1.0, dx=hr * 0.6 * lower, dy=hr * 2.3 * lower, rot=-3 + 35 * lower)
    fa = eo(prog(t, 34.25, 34.7))
    if fa > 0:
        fx, fy, fr = person(cv, 760, 1150, 320, mood='happy', look=(-1, 0), a=fa, glow=1.6, blink=blink_at(t, 0.9))
        ba = prog(t, 34.6, 34.95)
        if ba > 0:
            cv.save(); cv.translate(590, 735); s = 0.7 + 0.3 * bo(ba); cv.scale(s, s); cv.translate(-590, -735)
            pth, r = bubble_path(590, 735, 230, 92, (hx + hr * 0.8, hy - hr * 0.9))
            draw_bubble(cv, pth, r, clamp(ba * 2), glow=0.4)
            for k in range(3): cv.drawCircle(550 + k * 40, 735, 11 + 4 * bump(((t * 2.4) - k * 0.2) % 1), P(col(ACC_XL, clamp(ba * 2))))
            cv.restore()
        hp_ = prog(t, 35.35, 36.4)
        if hp_ > 0:
            hy2 = lerp(960, 820, eo(hp_)); hs = 26 * bo(prog(hp_, 0, 0.3))
            cv.drawPath(heart_path(590, hy2, hs * 1.3), P(col(CORAL, 0.5 * (1 - prog(hp_, 0.7, 1))), blur=12))
            cv.drawPath(heart_path(590, hy2, hs), P(col('#FF9A8A', 1 - prog(hp_, 0.75, 1))))

# ------------------------------------------------------------ 5: RUANG PIKIR (36.6 - 42)
def g5(cv, t):
    tt = t - 36.6
    p_ = bo(prog(tt, 0.0, 0.6)); a = eo(prog(tt, 0.0, 0.4))
    halo(cv, 540, 765, 460, ACC, 0.8 * a)
    rays(cv, 540, 765, 520, 0.7 * a, t, n=18, spin=4)
    cv.save(); cv.translate(540, 765); cv.rotate(t * 30)
    orbit = skia.Path(); orbit.addArc(skia.Rect(-270, -270, 270, 270), 0, 300)
    cv.drawPath(orbit, P(shader=lg(-270, 0, 270, 0, [col(ACC_L, 0), col(ACC_L, 0.6 * a)]), stroke=3))
    cv.drawCircle(270, 0, 8, P(col(ACC_XL, a))); cv.drawCircle(270, 0, 18, P(col(ACC, 0.6 * a), blur=8))
    cv.restore()
    cv.save(); cv.translate(540, 765); cv.scale(p_, p_); cv.translate(-540, -765)
    cv.drawCircle(540, 765, 280, P(col(ACC, 0.2), blur=60))
    cv.save(); cv.translate(540 - 260, 765 - 260); cv.scale(0.52, 0.52); __import__('logo_rp').c4(cv); cv.restore()
    cv.restore()
    ta = eo(prog(tt, 0.4, 0.9)); layer(cv, ta)
    tracked(cv, 'RUANG PIKIR', 540, 1062, font(XB, 58), P(col(TXT)), 10)
    cv.restore()
    pill(cv, 'ruangpikir.id', 540, 1135, prog(tt, 0.9, 1.3), bgc=ACC, fg=INK, size=30)

b.DRAWERS = [g0, g1, g2, g3, g4, g5]

def build_sfx():
    ev = [(0.1, 'whoosh'), (0.85, 'pop'), (2.0, 'plip'), (2.55, 'plip'), (4.6, 'swish'), (4.7, 'fizz_soft'), (4.85, 'card'), (4.95, 'rise'),
          (5.6, 'crack'), (5.65, 'zap2'),
          (6.22, 'whoosh'), (6.8, 'rise'), (7.95, 'pop'),
          (8.91, 'whoosh'), (8.95, 'card'), (9.55, 'swish'), (10.3, 'pop'), (11.85, 'stamp'),
          (12.85, 'whoosh'), (13.3, 'blink'), (13.9, 'plop'), (14.15, 'plop'), (14.95, 'clunk'),
          (16.95, 'whoosh'), (17.5, 'zap2'), (18.4, 'pop'), (18.6, 'swish'), (19.25, 'pop'), (20.4, 'rise'), (21.9, 'pop'),
          (23.32, 'whoosh'), (23.4, 'card'), (23.9, 'swish'), (24.25, 'pop'), (24.55, 'pop'), (25.9, 'shine'), (26.2, 'plip'),
          (27.6, 'whoosh'), (27.95, 'plip'), (28.35, 'card'), (29.7, 'swish'), (30.25, 'ding'), (30.55, 'pop'), (31.15, 'pop'), (31.4, 'ding_soft'),
          (32.85, 'whoosh'), (33.2, 'swish'), (34.25, 'pop'), (34.6, 'plip'), (35.35, 'shine'),
          (36.6, 'whoosh'), (36.75, 'boing'), (37.1, 'shine'), (37.6, 'pop')]
    ev += [(bt, 'heart') for bt in beat_times(6.3, 8.85, *G1_F)][::2]
    ev += [(21.0 + k * 0.55, 'heart') for k in range(4)]
    for (s, a_, b_) in b.CAPS: ev.append((s, 'tick'))
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
