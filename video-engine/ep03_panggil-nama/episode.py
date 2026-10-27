#!/usr/bin/env python3
"""Ruang Pikir reel #3: 'Panggil namamu, kok jadi tenang?' (distanced self-talk, Kross dkk. 2014)
python3 episode.py preview t1 t2 ... | timeline out.json | video out.mp4"""
import sys, os, math, json, subprocess, random
import skia
import base as b
from base import (clamp, lerp, prog, eo, ei, eio, bo, bump, col, P, lg, rg, layer, font, XB, B, M, MONO, bl, tracked, parse,
                 pill, sparkle, person, watcher_eye, scribble, spotlight, ACC, ACC_L, ACC_XL, TXT, MUTED, CORAL, MINT, W, H, FPS)

VIOLET, YELLOW, INK = '#B57BFF', '#FFD23F', '#0B0C1E'
NAME = 'Dina'

b.GROUPS = [(0.0, 5.38, 'PSIKOLOGI'), (5.38, 8.82, 'COBA INI'), (8.82, 21.81, 'RISET · 2014'),
            (21.81, 33.08, 'ILUSTRASI'), (33.08, 36.64, 'KOMENTAR'), (36.64, 42.0, 'RUANG PIKIR')]
b.CAPS = [(0.15, "Mau presentasi, terus", "[deg-degan parah]?"),
          (2.62, "Coba semangati diri", "pakai [namamu sendiri]"),
          (5.38, "Bukan \"aku bisa\", tapi", "\"[Dina], kamu bisa\""),
          (8.82, "Tahun 2014, psikolog", "[Ethan Kross] mengujinya"),
          (11.98, "Peserta siapin", "[pidato dadakan]"),
          (17.39, "Yang pakai nama", "tampil [lebih baik]"),
          (21.81, "Namamu bikin kamu lihat", "diri sendiri [dari luar]"),
          (25.49, "Ini namanya", "[self-distancing]"),
          (29.17, "Cemas tetap ada, tapi", "kamu [pegang kendali]"),
          (33.08, "Tulis di komentar", "pakai [namamu sendiri]!"),
          (36.64, "Follow [Ruang Pikir]", "biar makin kenal isi kepalamu")]

def draw_title(cv, t):
    a = eo(prog(t, 0.1, 0.55))
    if a <= 0: return
    segs = parse("Panggil namamu, [kok jadi tenang]?"); size = 62; f = font(XB, size)
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

def name_badge(cv, x, y, s, a, rot=-6):
    """stiker 'HALO, NAMAKU' di dada"""
    if a <= 0 or s <= 0: return
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(s, s)
    r = skia.Rect(-70, -44, 70, 44)
    cv.drawRoundRect(r, 14, 14, P(col(ACC, 0.6 * a), blur=18))
    cv.drawRoundRect(r, 14, 14, P(col('#F4F3FA', a)))
    cv.save(); cv.clipRect(skia.Rect(-70, -44, 70, -14)); cv.drawRoundRect(r, 14, 14, P(shader=lg(0, -44, 0, -14, [col('#A3ADFF', a), col(ACC, a)]))); cv.restore()
    tracked(cv, 'HALO, NAMAKU', 0, -29, font(MONO, 13), P(col(INK, a)), 1.5)
    f = font(XB, 34); w = f.measureText(NAME.upper()); cv.drawString(NAME.upper(), -w / 2, bl(f, 13), f, P(col(INK, a)))
    cv.restore()

def mic(cv, x0, foot, mx, my, a=1.0):
    if a <= 0: return
    cv.drawOval(skia.Rect(x0 - 46, foot - 8, x0 + 46, foot + 8), P(col('#000000', 0.5 * a), blur=6))
    cv.drawLine(x0 - 34, foot, x0 + 34, foot, P(col('#3A3C4E', a), stroke=8))
    stem = skia.Path(); stem.moveTo(x0, foot); stem.lineTo(x0, my + 60); stem.quadTo(x0, my + 10, mx, my)
    cv.drawPath(stem, P(col('#40435A', a), stroke=7)); cv.drawPath(stem, P(col(ACC, 0.35 * a), stroke=2))
    cv.save(); cv.translate(mx, my); cv.rotate(-35)
    r = skia.Rect(-17, -30, 17, 26)
    cv.drawRoundRect(r, 17, 17, P(shader=lg(-17, 0, 17, 0, [col('#5A5D78', a), col('#2A2C3C', a)])))
    for k in range(5): cv.drawLine(-12, -20 + k * 7, 12, -20 + k * 7, P(col('#1A1B26', 0.8 * a), stroke=2))
    cv.drawRoundRect(r, 17, 17, P(col(ACC_L, 0.6 * a), stroke=2))
    cv.restore()

# ------------------------------------------------------------ 0: PSIKOLOGI (0 - 5.38)
BEATS = []; _tb, _iv = 0.35, 0.95
while _tb < 5.3: BEATS.append(round(_tb, 3)); _tb += _iv; _iv = max(0.5, _iv * 0.88)
def pulse(t):
    v = 0.0
    for bt in BEATS:
        for off, g in ((0, 1.0), (0.17, 0.65)):
            d = t - bt - off
            if 0 <= d < 0.6: v = max(v, g * math.exp(-d / 0.09))
    return v
def ecg(tau):
    v = 0.0
    for bt in BEATS:
        d = tau - bt
        if -0.12 < d < 0.4:
            v += 0.12 * math.exp(-((d + 0.07) / 0.025) ** 2) - 0.2 * math.exp(-(d / 0.009) ** 2) + 1.0 * math.exp(-((d - 0.016) / 0.011) ** 2)
            v += -0.32 * math.exp(-((d - 0.037) / 0.012) ** 2) + 0.22 * math.exp(-((d - 0.2) / 0.05) ** 2)
    return v
EYES0 = [(935, 640, 22, .0), (150, 820, 26, .3), (945, 865, 26, .55), (130, 1035, 22, .15), (935, 1060, 22, .7), (290, 1130, 17, .4), (790, 1135, 17, .85)]
def g0(cv, t):
    a0 = eo(prog(t, 0.05, 0.5)); pu = pulse(t)
    spotlight(cv, 540, 1150, 215, a0, top=585)
    for i, (x, y, s, ph) in enumerate(EYES0):
        watcher_eye(cv, x, y, s, 540, 880, t, ph, eo(prog(t, 0.3 + i * 0.09, 0.7 + i * 0.09)))
    cv.drawLine(150, 1150, 930, 1150, P(shader=lg(150, 0, 930, 0, [col(ACC, 0), col(ACC, 0.45 * a0), col(ACC, 0)])))
    halo(cv, 540, 1150, 260, ACC, 0.5 * a0)
    # karakter gugup: gemetar, berkeringat, garis stres berdenyut mengikuti detak
    jit = 1.6 * math.sin(t * 47) * a0
    hx, hy, hr = person(cv, 540 + jit, 1150, 360, mood='worried', look=(0, 0.25), a=a0, sweat=(0.5 + 0.5 * math.sin(t * 3)) * prog(t, 0.6, 1.2), blink=blink_at(t, 0.2))
    for s in (-1, 1):
        for k in range(3):
            ang = math.radians((-50 + k * 22) if s > 0 else (230 - k * 22)); r0 = hr * (1.35 + 0.12 * pu); r1 = r0 + 18 + 10 * pu
            cv.drawLine(hx + math.cos(ang) * r0, hy + math.sin(ang) * r0, hx + math.cos(ang) * r1, hy + math.sin(ang) * r1, P(col(CORAL, (0.35 + 0.65 * pu) * a0), stroke=5))
    mic(cv, 420, 1150, 466, 932, a0)
    # jantung di dada
    cy_chest = 1150 - 216 * 0.55
    hs = 18 * (1 + 0.28 * pu)
    cv.drawPath(heart_path(510, cy_chest - 22, hs * 1.6), P(col(CORAL, 0.45 * pu * a0), blur=16))
    # widget detak jantung (kaca, kiri atas)
    wa = eo(prog(t, 0.35, 0.8))
    if wa > 0:
        r = skia.Rect(70, 588, 450, 700)
        cv.save(); cv.translate(0, (1 - wa) * 20); pth = glass(cv, r, 28, wa, glow=0.25 * pu, gc=CORAL, edge=CORAL)
        cv.drawPath(heart_path(124, 640, 21 * (1 + 0.25 * pu)), P(col(CORAL, 0.5 * wa), blur=10))
        cv.drawPath(heart_path(124, 640, 21 * (1 + 0.25 * pu)), P(shader=lg(0, 615, 0, 665, [col('#FF9A8A', wa), col(CORAL, wa)])))
        tracked(cv, 'DETAK', 124, 676, font(MONO, 13), P(col(CORAL, 0.8 * wa)), 2)
        span, x0, x1, by = 2.4, 172, 428, 652; ln = skia.Path()
        for k in range(301):
            u = k / 300; tau = t - span * (1 - u); y = by - 40 * ecg(tau)
            (ln.moveTo if k == 0 else ln.lineTo)(lerp(x0, x1, u), y)
        cv.save(); cv.clipRect(skia.Rect(x0, 596, x1 + 6, 696))
        cv.drawPath(ln, P(col(CORAL, 0.35 * wa), stroke=9, blur=6)); cv.drawPath(ln, P(shader=lg(x0, 0, x1, 0, [col(CORAL, 0), col(CORAL, wa), col('#FFC2B8', wa)], [0, 0.35, 1]), stroke=3.5))
        cv.drawCircle(x1, by - 40 * ecg(t), 6, P(col('#FFE1DB', wa))); cv.drawCircle(x1, by - 40 * ecg(t), 14, P(col(CORAL, 0.5 * wa), blur=8))
        cv.restore(); cv.restore()
    # 'semangati diri pakai namamu': stiker nama + pill
    bp_ = prog(t, 3.3, 3.75)
    if bp_ > 0:
        name_badge(cv, 548, cy_chest + 6, bo(bp_), clamp(bp_ * 3), rot=-6 + 4 * math.sin(t * 2.2) * 0.3)
        for k, (dx, dy, rr, ph) in enumerate(((-95, -40, 14, 0), (95, -55, 18, 1.3), (80, 50, 11, 2.2), (-85, 45, 10, 3.1))):
            sparkle(cv, 548 + dx, cy_chest + dy, rr * (0.6 + 0.4 * math.sin(t * 5 + ph)), bump(prog(t, 3.45 + k * 0.08, 4.6 + k * 0.08)))
    pa = prog(t, 4.3, 4.7)
    if pa > 0:
        pth = skia.Path(); pth.moveTo(712, 792); pth.cubicTo(700, 880, 660, 960, 624, 1000)
        m = skia.PathMeasure(pth, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(prog(t, 4.45, 4.9)), seg, True)
        cv.drawPath(seg, P(col(ACC_L, 0.9), stroke=4, effect=skia.DashPathEffect.Make([12, 10], -t * 40)))
        halo(cv, 780, 760, 170, ACC, pa)
        pill(cv, 'pakai namamu', 780, 760, pa, bgc=ACC, fg=INK, size=32)

# ------------------------------------------------------------ 1: COBA INI (5.38 - 8.82) — momen wow
CRACK = [(-14, -90), (10, -46), (-12, -14), (12, 18), (-8, 52), (6, 90)]
def g1(cv, t):
    happy = prog(t, 7.15, 7.35)
    ca = eo(prog(t, 5.45, 5.8))
    hx, hy, hr = person(cv, 205, 1165, 270, mood='happy' if happy > 0.5 else 'worried', look=(1, -0.4), a=ca,
                        sweat=(1 - happy) * (0.5 + 0.5 * math.sin(t * 3)), glow=1 + 1.5 * happy, blink=blink_at(t, 0.6))
    if happy > 0:
        halo(cv, hx, hy, 170, ACC, happy)
        for k in range(5):
            ang = k * math.tau / 5 + t * 0.8; rr = hr * 1.9
            sparkle(cv, hx + math.cos(ang) * rr, hy + math.sin(ang) * rr, 9 + 4 * math.sin(t * 6 + k), happy * 0.9)
    # gelembung 1: "Aku pasti bisa." -> retak, jatuh
    p1 = prog(t, 5.95, 6.35); crk = prog(t, 6.82, 7.02); fall = prog(t, 7.02, 7.6)
    if p1 > 0 and fall < 1:
        cx, cy, w, h = 630, 718, 470, 124
        pth, r = bubble_path(cx, cy, w, h, (hx + 46, hy - 70))
        tint = prog(t, 6.8, 6.95)
        def body(alpha):
            draw_bubble(cv, pth, r, alpha, fill=('#2A2C40', '#18192A') if tint < 0.5 else ('#3A2228', '#1E1418'), edge=MUTED if tint < 0.5 else CORAL)
            glow_text(cv, 'Aku pasti bisa.', cx, cy, font(B, 46), c=TXT if tint < 0.5 else '#FFB3A6', a=alpha)
        s = 0.6 + 0.4 * bo(p1)
        cv.save(); cv.translate(cx, cy); cv.scale(s, s); cv.translate(-cx, -cy)
        tracked(cv, 'PAKAI "AKU"', r.left() + 92, r.top() - 30, font(MONO, 19), P(col(MUTED if tint < 0.5 else CORAL, clamp(p1 * 2) * (1 - fall))), 3)
        if fall <= 0:
            body(clamp(p1 * 2))
            if crk > 0:
                cp = skia.Path(); cp.moveTo(cx + CRACK[0][0], cy + CRACK[0][1])
                for dx, dy in CRACK[1:]: cp.lineTo(cx + dx, cy + dy)
                m = skia.PathMeasure(cp, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(crk), seg, True)
                cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
                cv.drawPath(seg, P(col('#FFFFFF', 0.6), stroke=9, blur=5)); cv.drawPath(seg, P(col('#FFE6E1'), stroke=4))
                cv.restore()
        else:
            for side in (-1, 1):
                half = skia.Path(); half.moveTo(cx + side * 900, cy - 900)
                for dx, dy in [(-14, -900)] + CRACK + [(6, 900)]: half.lineTo(cx + dx, cy + dy)
                half.lineTo(cx + side * 900, cy + 900); half.close()
                cv.save(); cv.translate(side * 70 * eo(fall), 260 * ei(fall)); cv.rotate(side * 14 * fall)
                cv.clipPath(half, skia.ClipOp.kIntersect, True); body(1 - eio(fall)); cv.restore()
        cv.restore()
        x_mark(cv, r.right() - 10, r.top() + 8, 30, prog(t, 6.85, 7.25), 1 - prog(t, 7.1, 7.4))
    # gelembung 2: "Dina, kamu pasti bisa." -> membesar + glow + centang
    p2 = prog(t, 7.12, 7.6)
    if p2 > 0:
        cx, cy, w, h = 626, 948, 664, 150
        flash = bump(prog(t, 7.1, 7.55))
        halo(cv, cx, cy, 520, ACC, 0.55 * flash + 0.35 * p2)
        rays(cv, cx, cy, 470, eo(p2) * (0.8 + 0.2 * math.sin(t * 3)), t, n=16)
        s = 0.55 + 0.45 * bo(p2)
        cv.save(); cv.translate(cx, cy); cv.scale(s, s); cv.translate(-cx, -cy)
        pth, r = bubble_path(cx, cy, w, h, (hx + 50, hy - 6), rad=60)
        tracked(cv, 'PAKAI NAMA', r.left() + 88, r.top() - 32, font(MONO, 19), P(col(ACC_L, clamp(p2 * 2))), 3)
        draw_bubble(cv, pth, r, clamp(p2 * 2), glow=0.6 + 0.4 * flash + 0.15 * math.sin(t * 4), fill=('#3A3F78', '#1D1F3C'))
        sheen(cv, pth, r, prog(t, 7.4, 8.2))
        rich(cv, f'[{NAME},] kamu pasti bisa.', cx, cy, 52, a=clamp(p2 * 2), f_n=XB)
        cv.restore()
        check_mark(cv, cx + w / 2 - 12, cy - h / 2 - 2, 36, prog(t, 7.75, 8.25))
        for k, (dx, dy, rr) in enumerate(((-360, -40, 16), (310, 90, 22), (-250, 105, 13), (200, -120, 15), (40, 125, 11))):
            sparkle(cv, cx + dx, cy + dy, rr * (0.7 + 0.3 * math.sin(t * 5 + k)), bump(prog(t, 7.3 + k * 0.1, 8.7 + k * 0.05)))

# ------------------------------------------------------------ 2: RISET · 2014 (8.82 - 21.81)
def research_card(cv, t):
    ent = prog(t, 8.95, 9.5); ext = prog(t, 11.75, 12.15)
    if ent <= 0 or ext >= 1: return
    a = clamp(ent * 2) * (1 - ext)
    cv.save(); cv.translate(540, 840); s = (0.86 + 0.14 * bo(ent)) * (1 - 0.35 * ei(ext)); cv.scale(s, s * (0.75 + 0.25 * eo(ent))); cv.translate(-540, -840 - 120 * ei(ext))
    rays(cv, 540, 840, 560, 0.5 * a, t, n=12, spin=3)
    # lembar jurnal di belakang
    pa = eo(prog(t, 9.1, 9.7)) * a
    if pa > 0:
        cv.save(); cv.translate(625, 760); cv.rotate(2 + 5 * pa)
        r = skia.Rect(-250, -190, 250, 190)
        cv.drawRoundRect(r.makeOffset(0, 16), 18, 18, P(col('#000000', 0.5 * pa), blur=20))
        cv.drawRoundRect(r, 18, 18, P(shader=lg(0, -190, 0, 190, [col('#2B2D46', pa), col('#1B1C2C', pa)]))); cv.drawRoundRect(r, 18, 18, P(col(ACC, 0.3 * pa), stroke=2))
        cv.drawString('Self-talk as a regulatory mechanism', -222, -136, font(B, 21), P(col(ACC_XL, 0.8 * pa)))
        cv.drawString('J. Personality & Social Psychology', -222, -106, font(M, 18), P(col(MUTED, pa)))
        for k in range(6): cv.drawLine(-222, -66 + k * 26, 222 - (k % 3) * 60, -66 + k * 26, P(col('#FFFFFF', 0.07 * pa), stroke=7))
        cv.restore()
    r = skia.Rect(190, 690, 890, 1070)
    pth = glass(cv, r, 34, a, glow=0.35, fill=('#262842', '#131422'))
    sheen(cv, pth, r, prog(t, 9.55, 10.4))
    tracked(cv, 'PENELITI', 540, 742, font(MONO, 22), P(col(ACC_L, a)), 6)
    glow_text(cv, 'Ethan Kross', 540, 808, font(XB, 74), TXT, a)
    glow_text(cv, '2014', 540, 925, font(XB, 140), a=a, glow=0.5, shader=lg(0, 865, 0, 985, [col('#E3E6FF', a), col(ACC, a)]))
    chip(cv, '7 studi', 430, 1018, eo(prog(t, 9.9, 10.2)) * a)
    chip(cv, '585 peserta', 640, 1018, eo(prog(t, 10.05, 10.35)) * a)
    cv.restore()
    st = prog(t, 10.9, 11.2)
    if st > 0 and ext < 1:
        layer(cv, 1 - ext); b_stamp(cv, 'SELF-TALK', 800, 1095, st); cv.restore()

def b_stamp(cv, text, cx, cy, p_, c=CORAL, rot=-12, size=38):
    if p_ <= 0: return
    cv.save(); cv.translate(cx, cy); cv.rotate(rot); s = 1.8 - 0.8 * eo(p_); cv.scale(s, s); layer(cv, clamp(p_ * 2))
    f = font(XB, size); w = f.measureText(text)
    r = skia.Rect(-w / 2 - 26, -size * 0.85, w / 2 + 26, size * 0.85)
    cv.drawRoundRect(r, 14, 14, P(col(c, 0.4), blur=14))
    cv.drawRoundRect(r, 14, 14, P(col('#0B0B10', 0.88))); cv.drawRoundRect(r, 14, 14, P(col(c), stroke=5))
    cv.drawString(text, -w / 2, bl(f, 0), f, P(col(c))); cv.restore(); cv.restore()

def stopwatch(cv, cx, cy, r, t, a, spin=1.0):
    if a <= 0: return
    cv.drawRoundRect(skia.Rect(cx - r * 0.16, cy - r * 1.28, cx + r * 0.16, cy - r * 1.08), r * 0.06, r * 0.06, P(col('#4A4D68', a)))
    cv.drawRoundRect(skia.Rect(cx - r * 0.3, cy - r * 1.4, cx + r * 0.3, cy - r * 1.25), r * 0.07, r * 0.07, P(col(ACC_L, a)))
    cv.drawCircle(cx, cy, r * 1.25, P(col(ACC, 0.25 * a), blur=r * 0.35))
    cv.drawCircle(cx, cy, r * 1.05, P(shader=rg(cx - r * 0.3, cy - r * 0.4, r * 1.6, [col('#2E3150', a), col('#14152A', a)])))
    cv.drawCircle(cx, cy, r * 1.05, P(shader=lg(cx - r, cy - r, cx + r, cy + r, [col(ACC_XL, 0.8 * a), col(ACC, 0.25 * a)]), stroke=max(2, r * 0.04)))
    for k in range(12):
        ang = k * math.tau / 12; r0 = r * (0.78 if k % 3 else 0.7)
        cv.drawLine(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0, cx + math.cos(ang) * r * 0.88, cy + math.sin(ang) * r * 0.88, P(col(ACC_XL, 0.6 * a), stroke=max(1.5, r * 0.035)))
    ang = -math.pi / 2 + spin * t * 4.2
    arc = skia.Path(); arc.addArc(skia.Rect(cx - r * 0.95, cy - r * 0.95, cx + r * 0.95, cy + r * 0.95), -90, math.degrees(ang + math.pi / 2) % 360)
    cv.drawPath(arc, P(col(CORAL, 0.85 * a), stroke=max(3, r * 0.08)))
    cv.drawLine(cx, cy, cx + math.cos(ang) * r * 0.7, cy + math.sin(ang) * r * 0.7, P(col(TXT, a), stroke=max(2.5, r * 0.06)))
    cv.drawCircle(cx, cy, r * 0.08, P(col(CORAL, a)))

PANELS = ((70, 520, 295), (560, 1010, 785))
def g2(cv, t):
    research_card(cv, t)
    # pidato dadakan: stopwatch besar lalu mengecil jadi ikon di atas
    sa = eo(prog(t, 12.0, 12.4)) * (1 - eo(prog(t, 17.35, 17.7)))
    if sa > 0:
        m = eio(prog(t, 13.25, 13.75))
        cx, cy, r = 540, lerp(830, 628, m), lerp(150, 40, m)
        sc = 0.6 + 0.4 * bo(prog(t, 12.0, 12.45))
        cv.save(); cv.translate(cx, cy); cv.scale(sc, sc); cv.translate(-cx, -cy)
        stopwatch(cv, cx, cy, r, t, sa)
        cv.restore()
        pill(cv, 'PIDATO DADAKAN', 540, 1050, prog(t, 12.35, 12.75) * (1 - prog(t, 13.2, 13.45)), bgc=CORAL, fg='#2A0E12', size=32)
    # dua panel: pakai "aku" vs pakai nama
    pe = prog(t, 13.45, 13.95); px = prog(t, 21.45, 21.81)
    if pe <= 0 or px >= 1: return
    pa = eo(pe) * (1 - px)
    ph_b = prog(t, 17.45, 17.85)      # karakter -> grafik batang
    ph_c = prog(t, 19.55, 19.9)       # grafik -> kepikiran sesudahnya
    for i, (x0, x1, cx) in enumerate(PANELS):
        off = (1 - eo(pe)) * (-160 if i == 0 else 160)
        cv.save(); cv.translate(off, 0)
        right = i == 1
        glow = (0.35 + 0.25 * math.sin(t * 3)) * prog(t, 15.9, 16.3) if right else 0
        r = skia.Rect(x0, 690, x1, 1170)
        glass(cv, r, 32, pa, glow=glow, edge=ACC if right else CORAL, fill=('#24264A', '#121326') if right else ('#2A2130', '#141219'))
        tracked(cv, 'PAKAI NAMA' if right else 'PAKAI "AKU"', cx, 736, font(MONO, 21), P(col(ACC_L if right else '#FF9A8A', pa)), 4)
        # fase A: karakter + kalimat ke diri sendiri
        ca = pa * (1 - eio(ph_b)) + pa * eio(ph_c)
        if ca > 0:
            dy = 40 * eio(ph_b) * (1 - eio(ph_c))
            on = prog(t, 15.9, 16.3) if right else prog(t, 14.8, 15.2)
            calm = prog(t, 16.3, 16.6) if right else 0
            hx, hy, hr = person(cv, cx + (0 if right else 1.3 * math.sin(t * 45)), 1140 + dy, 250 if ph_c <= 0 else 200, mood=('happy' if calm > 0.5 else 'neutral') if right else 'worried',
                                a=ca, sweat=0 if right else (0.5 + 0.5 * math.sin(t * 3)), glow=1 + calm, blink=blink_at(t, 0.3 + i * 0.4))
            if ph_c <= 0:
                bpth, br = bubble_path(cx, 838, 380, 78, (cx - 20, hy - hr - 8))
                if on > 0:
                    cv.save(); cv.translate(cx, 838); s = 0.7 + 0.3 * bo(on); cv.scale(s, s); cv.translate(-cx, -838)
                    draw_bubble(cv, bpth, br, clamp(on * 2) * ca, glow=0.4 if right else 0, fill=('#34387A', '#1C1E3C') if right else ('#33232A', '#1A1317'), edge=ACC if right else CORAL)
                    if right: rich(cv, f'[{NAME},] kamu bisa.', cx, 838, 30, a=clamp(on * 2) * ca, f_n=XB)
                    else: glow_text(cv, 'Aku pasti bisa...', cx, 838, font(B, 30), '#FFC9BF', clamp(on * 2) * ca)
                    cv.restore()
                if not right and on > 0:
                    scribble(cv, hx + 92, hy - 40, 34, t, head=eo(prog(t, 15.0, 15.8)) * ca, width=4)
            else:
                # fase C: sesudah pidato
                if right:
                    check_mark(cv, cx, 872, 42, prog(t, 19.95, 20.5), ca)
                else:
                    la = eo(prog(t, 19.8, 20.2)) * ca
                    if la > 0:
                        cv.save(); cv.translate(cx, 872); cv.rotate(t * 260)
                        arc = skia.Path(); arc.addArc(skia.Rect(-48, -48, 48, 48), 20, 290)
                        cv.drawPath(arc, P(col(CORAL, 0.4 * la), stroke=16, blur=8)); cv.drawPath(arc, P(col(CORAL, la), stroke=8))
                        hd = skia.Path(); ex, ey = 48 * math.cos(math.radians(310)), 48 * math.sin(math.radians(310))
                        hd.moveTo(ex + 16, ey - 2); hd.lineTo(ex - 6, ey - 16); hd.lineTo(ex - 2, ey + 14); hd.close()
                        cv.drawPath(hd, P(col(CORAL, la)))
                        cv.restore()
                        for k in range(3):
                            cv.drawCircle(cx - 16 + k * 16, 872, 5 + 2 * bump(((t * 2.2) - k * 0.2) % 1), P(col('#FFC9BF', la)))
        # fase B: grafik batang "Penampilan" (tanpa angka)
        ba = pa * eio(ph_b) * (1 - eio(ph_c))
        if ba > 0:
            g = eo(prog(t, 17.7 + i * 0.35, 18.7 + i * 0.35)); hgt = (125 if not right else 250) * g
            bx0, bx1, by = cx - 72, cx + 72, 1130
            cv.drawRoundRect(skia.Rect(bx0, by - 270, bx1, by), 22, 22, P(col('#FFFFFF', 0.05 * ba)))
            if hgt > 4:
                rr = skia.Rect(bx0, by - hgt, bx1, by)
                if right: cv.drawRoundRect(rr, 22, 22, P(col(ACC, 0.55 * ba), blur=26))
                cv.drawRoundRect(rr, 22, 22, P(shader=lg(0, rr.top(), 0, by, [col('#C9CEFF' if right else '#7C7A8A', ba), col(ACC if right else '#3A3946', ba)])))
                cv.save(); cv.clipRect(skia.Rect(bx0, by - hgt, bx1, by - hgt + 10)); cv.drawRoundRect(rr, 22, 22, P(col('#FFFFFF', 0.25 * ba))); cv.restore()
            if right:
                pa_ = prog(t, 18.75, 19.1) * ba
                if pa_ > 0:
                    halo(cv, cx, by - hgt - 50, 150, ACC, pa_)
                    pill(cv, 'lebih baik', cx, by - hgt - 52, pa_, bgc=MINT, fg='#062A1D', size=30)
                    for k in range(3): sparkle(cv, cx + (-95, 100, 70)[k], by - hgt - (95, 30, 110)[k], 12 + 3 * math.sin(t * 6 + k), pa_)
        cv.restore()
    # label tengah atas berganti sesuai fase
    la_b = eio(ph_b) * (1 - eio(ph_c)) * pa; la_c = eio(ph_c) * pa
    if la_b > 0: chip(cv, 'PENAMPILAN', 540, 628, la_b, size=24, f=MONO, fg=ACC_XL)
    if la_c > 0:
        chip(cv, 'SESUDAH PIDATO', 540, 628, la_c, size=24, f=MONO, fg=ACC_XL)
        chip(cv, 'kepikiran terus', 295, 788, eo(prog(t, 20.1, 20.4)) * pa, size=26, fg='#FFC9BF', bgc='#3A2228', edge=CORAL)
        chip(cv, 'jarang kepikiran', 785, 788, eo(prog(t, 20.4, 20.7)) * pa, size=26, fg='#B9F5DF', bgc='#173A2E', edge=MINT)

# ------------------------------------------------------------ 3: ILUSTRASI (21.81 - 33.08)
CX, GX, FOOT = 330, 790, 1150
def g3(cv, t):
    out = prog(t, 29.15, 29.55)
    if out < 1:
        oa = 1 - eio(out)
        z_ = eio(prog(t, 21.9, 23.4)); z = lerp(2.3, 1.0, z_)
        fx, fy = lerp(CX, 540, z_), lerp(905, 870, z_)
        cv.save(); cv.translate(540, 870); cv.scale(z, z); cv.translate(-fx, -fy); layer(cv, oa)
        # bingkai pandangan dari luar
        fa = eo(prog(t, 23.15, 23.55)) * (1 - eo(prog(t, 25.5, 25.9)))
        happy = prog(t, 26.55, 26.75)
        halo(cv, CX, 930, 230, ACC, 0.4 + 0.6 * happy)
        hx, hy, hr = person(cv, CX, FOOT, 330, mood='happy' if happy > 0.5 else 'neutral', look=(1 if t > 23.6 else 0, 0), a=1.0,
                            glow=1 + 1.4 * happy, blink=blink_at(t, 0.15))
        if happy > 0:
            for k in range(6):
                ang = k * math.tau / 6 + t * 0.9; rr = hr * (1.8 + 0.4 * eo(happy))
                sparkle(cv, hx + math.cos(ang) * rr, hy + math.sin(ang) * rr, 10 + 4 * math.sin(t * 5 + k), bump(prog(t, 26.6, 28.6)) * 0.9 + 0.1 * happy)
        if fa > 0:
            r = skia.Rect(160, 705, 500, 1180); L = 46
            for (x, y, dx, dy) in ((r.left(), r.top(), 1, 1), (r.right(), r.top(), -1, 1), (r.left(), r.bottom(), 1, -1), (r.right(), r.bottom(), -1, -1)):
                pth = skia.Path(); pth.moveTo(x, y + dy * L); pth.lineTo(x, y); pth.lineTo(x + dx * L, y)
                cv.drawPath(pth, P(col(ACC_L, 0.4 * fa), stroke=12, blur=6)); cv.drawPath(pth, P(col(ACC_XL, fa), stroke=5))
            cv.drawCircle(r.left() + 34, r.top() + 34, 8, P(col(CORAL, fa * (0.5 + 0.5 * math.sin(t * 6)))))
        # diri dari luar (ghost)
        ga = eo(prog(t, 23.6, 24.3))
        if ga > 0:
            rays(cv, GX, 860, 330, 0.55 * ga, t, n=12, spin=-4)
            gx_, gy_, gr = ghost(cv, GX, FOOT, 380, ga, t, look=(-1, 0))
            la = prog(t, 24.0, 24.5) * (1 - prog(t, 25.6, 25.9))
            if la > 0:
                sl = skia.Path(); sl.moveTo(gx_ - gr * 1.05, gy_ - gr * 0.05); sl.lineTo(505, 905)
                m = skia.PathMeasure(sl, False); seg = skia.Path(); m.getSegment(0, m.getLength() * eo(la), seg, True)
                cv.drawPath(seg, P(col(ACC_L, 0.85 * la), stroke=4, effect=skia.DashPathEffect.Make([14, 12], -t * 50)))
            # 'kayak nyemangatin teman': gelembung + energi ke karakter
            sb = prog(t, 25.6, 26.0) * (1 - eio(prog(t, 27.45, 27.75)))
            if sb > 0:
                cv.save(); cv.translate(GX - 20, 690); s = 0.65 + 0.35 * bo(sb); cv.scale(s, s); cv.translate(-(GX - 20), -690)
                bpth, br = bubble_path(GX - 20, 690, 400, 92, (gx_ - 10, gy_ - gr - 8))
                draw_bubble(cv, bpth, br, clamp(sb * 2), glow=0.5, fill=('#3A3F78', '#1D1F3C'))
                rich(cv, f'[{NAME},] kamu bisa!', GX - 20, 690, 36, a=clamp(sb * 2), f_n=XB)
                cv.restore()
            cu = prog(t, 25.95, 26.6)
            if 0 < cu < 1:
                arc = skia.Path(); arc.moveTo(gx_ - gr * 1.2, gy_ + 10); arc.quadTo(560, 720, hx + hr * 1.2, hy - 6)
                cv.drawPath(arc, P(col(ACC, 0.25 * bump(cu)), stroke=10, blur=8))
                comet(cv, arc, eio(cu))
            # self-distancing: penggaris jarak di lantai
            dr = prog(t, 27.7, 28.2)
            if dr > 0:
                y = 1170; x0, x1 = 410, 705; e_ = eo(dr); mx = (x0 + x1) / 2
                cv.drawLine(mx - (mx - x0) * e_, y, mx + (x1 - mx) * e_, y, P(col(ACC_L, 0.4), stroke=10, blur=6))
                cv.drawLine(mx - (mx - x0) * e_, y, mx + (x1 - mx) * e_, y, P(col(ACC_XL), stroke=4))
                for xx in (mx - (mx - x0) * e_, mx + (x1 - mx) * e_): cv.drawLine(xx, y - 16, xx, y + 16, P(col(ACC_XL), stroke=4))
        cv.restore(); cv.restore()
        sp = prog(t, 27.75, 28.15)
        if sp > 0:
            halo(cv, 540, 625, 300, ACC, sp * oa)
            rays(cv, 540, 625, 300, 0.6 * sp * oa, t, n=14)
            pill(cv, 'self-distancing', 540, 625, sp * oa, bgc=ACC, fg=INK, size=40)
    # cemas tetap ada, tapi lebih pegang kendali
    ce = prog(t, 29.3, 29.8)
    if ce <= 0: return
    ca = eo(ce)
    calm = eio(prog(t, 31.3, 32.2))
    for i, (x0, x1, cx, lab, c) in enumerate(((80, 520, 300, 'CEMAS', CORAL), (560, 1000, 780, 'KENDALI', MINT))):
        dy = (1 - eo(prog(t, 29.3 + i * 0.15, 29.8 + i * 0.15))) * 60
        a = clamp(prog(t, 29.3 + i * 0.15, 29.6 + i * 0.15) * 2)
        cv.save(); cv.translate(0, dy)
        r = skia.Rect(x0, 640, x1, 1120)
        glass(cv, r, 34, a, glow=(0.5 * calm if i == 1 else 0.15), gc=c, edge=c)
        tracked(cv, lab, cx, 694, font(MONO, 24), P(col(c, a)), 6)
        if i == 0:
            gy, gr = 940, 150
            track = skia.Path(); track.addArc(skia.Rect(cx - gr, gy - gr, cx + gr, gy + gr), 180, 180)
            cv.drawPath(track, P(col('#FFFFFF', 0.08 * a), stroke=30))
            cv.drawPath(track, P(shader=lg(cx - gr, 0, cx + gr, 0, [col(MINT, a), col(YELLOW, a), col(CORAL, a)]), stroke=22))
            for k in range(11):
                ang = math.radians(180 + k * 18); r0, r1 = gr - 34, gr - (46 if k % 5 == 0 else 40)
                cv.drawLine(cx + math.cos(ang) * r0, gy + math.sin(ang) * r0, cx + math.cos(ang) * r1, gy + math.sin(ang) * r1, P(col('#FFFFFF', 0.4 * a), stroke=3))
            amp = lerp(1.0, 0.3, calm)
            v = lerp(0.7, 0.6, calm) + amp * (0.07 * math.sin(t * 8.3) + 0.04 * math.sin(t * 13.7 + 1))
            v = lerp(0.08, v, eo(prog(t, 29.5, 30.3)))
            ang = math.radians(180 + 180 * v); L = gr - 30
            cv.drawLine(cx, gy, cx + math.cos(ang) * L, gy + math.sin(ang) * L, P(col(CORAL, 0.5 * a), stroke=14, blur=8))
            cv.drawLine(cx, gy, cx + math.cos(ang) * L, gy + math.sin(ang) * L, P(col(TXT, a), stroke=7))
            cv.drawCircle(cx, gy, 18, P(col(TXT, a))); cv.drawCircle(cx, gy, 8, P(col(CORAL, a)))
            chip(cv, 'tetap ada', cx, 1040, eo(prog(t, 30.1, 30.45)) * a, size=28, fg='#FFC9BF', bgc='#3A2228', edge=CORAL)
        else:
            wy, wr = 900, 112
            fill_ = eo(prog(t, 31.3, 32.4))
            ring = skia.Path(); ring.addArc(skia.Rect(cx - wr - 32, wy - wr - 32, cx + wr + 32, wy + wr + 32), -90, 360 * 0.82 * fill_)
            cv.drawCircle(cx, wy, wr + 32, P(col('#FFFFFF', 0.07 * a), stroke=10))
            if fill_ > 0: cv.drawPath(ring, P(col(MINT, 0.5 * a), stroke=18, blur=10)); cv.drawPath(ring, P(col(MINT, a), stroke=10))
            halo(cv, cx, wy, 210, MINT, 0.5 * calm * a)
            cv.save(); cv.translate(cx, wy); cv.rotate(14 * math.sin(t * 1.7) * (1 - 0.5 * calm))
            wc = MINT if calm > 0.3 else ACC_L
            cv.drawCircle(0, 0, wr, P(col(wc, 0.35 * a), stroke=30, blur=10))
            cv.drawCircle(0, 0, wr, P(shader=lg(0, -wr, 0, wr, [col('#E3FFF4' if calm > 0.3 else ACC_XL, a), col(wc, a)]), stroke=22))
            for ang in (180, 0, 90):
                ra = math.radians(ang); cv.drawLine(math.cos(ra) * 30, math.sin(ra) * 30, math.cos(ra) * (wr - 8), math.sin(ra) * (wr - 8), P(col(wc, a), stroke=18))
            cv.drawCircle(0, 0, 34, P(shader=rg(-8, -10, 50, [col('#3C3F5C', a), col('#1B1C2C', a)]))); cv.drawCircle(0, 0, 34, P(col(wc, a), stroke=4))
            cv.restore()
            chip(cv, 'lebih terkendali', cx, 1060, eo(prog(t, 31.9, 32.25)) * a, size=28, fg='#B9F5DF', bgc='#173A2E', edge=MINT)
        cv.restore()

# ------------------------------------------------------------ 4: KOMENTAR (33.08 - 36.64)
COMMENTS = [('dina.ayu', 'D', '#FF8FA8', '[Dina,] kamu udah latihan. Siap!'),
            ('rakaa_', 'R', '#7FD4FF', '[Raka,] tarik napas dulu ya.'),
            ('sasa.id', 'S', '#FFD23F', '[Sasa,] pelan-pelan, kamu hebat.')]
def g4(cv, t):
    sa = eo(prog(t, 33.15, 33.55))
    if sa <= 0: return
    cv.save(); cv.translate(0, (1 - sa) * 80)
    r = skia.Rect(80, 600, 1000, 1172)
    glass(cv, r, 40, sa, glow=0.2, fill=('#1F2136', '#111220'))
    cv.drawRoundRect(skia.Rect(500, 618, 580, 626), 4, 4, P(col('#FFFFFF', 0.25 * sa)))
    tracked(cv, 'KOMENTAR', 200, 666, font(MONO, 20), P(col(ACC_L, sa)), 4)
    cv.drawString('baru', 880, bl(font(B, 22), 666), font(B, 22), P(col(MUTED, sa)))
    cv.drawLine(120, 700, 960, 700, P(col('#FFFFFF', 0.07 * sa), stroke=2))
    for k, (user, ini, c, text) in enumerate(COMMENTS):
        p_ = prog(t, 33.4 + k * 0.45, 33.85 + k * 0.45)
        if p_ <= 0: continue
        a = clamp(p_ * 2) * sa; y = 790 + k * 118 + (1 - eo(p_)) * 40
        cv.save(); layer(cv, a)
        cv.drawCircle(165, y, 34, P(shader=lg(0, y - 34, 0, y + 34, [col(c), col(ACC)])))
        f = font(XB, 30); w = f.measureText(ini); cv.drawString(ini, 165 - w / 2, bl(f, y), f, P(col(INK)))
        cv.drawString(user, 225, bl(font(B, 21), y - 22), font(B, 21), P(col(MUTED)))
        segs = parse(text); fx = 225
        for s, h in segs:
            ff = font(XB if h else B, 30); cv.drawString(s, fx, bl(ff, y + 16), ff, P(col(ACC_L if h else TXT))); fx += ff.measureText(s)
        lk = prog(t, 34.6 + k * 0.3, 34.9 + k * 0.3)
        hp = heart_path(925, y, 15 * (1 + 0.35 * bump(lk)))
        if lk > 0: cv.drawPath(hp, P(col(CORAL, 0.5 * lk), blur=10)); cv.drawPath(hp, P(col(CORAL, lk)))
        cv.drawPath(hp, P(col(CORAL if lk > 0 else MUTED), stroke=3))
        cv.restore(); cv.restore()
    # kolom tulis komentar: mengetik kalimat semangat
    ia = eo(prog(t, 34.6, 34.95)) * sa
    if ia > 0:
        ir = skia.Rect(120, 1080, 960, 1146)
        cv.drawRoundRect(ir, 33, 33, P(col('#0C0D16', 0.9 * ia))); cv.drawRoundRect(ir, 33, 33, P(col(ACC, (0.5 + 0.3 * math.sin(t * 4)) * ia), stroke=2.5))
        typed = 'Namamu, kamu pasti bisa!'; n = int(len(typed) * prog(t, 35.0, 36.2))
        f = font(B, 28); tx = 160
        if n == 0: cv.drawString('Tulis pakai namamu...', tx, bl(f, 1113), f, P(col(MUTED, ia)))
        else: cv.drawString(typed[:n], tx, bl(f, 1113), f, P(col(TXT, ia)))
        if (t * 2) % 1 < 0.6: cx_ = tx + f.measureText(typed[:n]) + 4; cv.drawLine(cx_, 1094, cx_, 1132, P(col(ACC_L, ia), stroke=3))
        cv.drawCircle(915, 1113, 24, P(shader=lg(0, 1089, 0, 1137, [col('#A9B2FF', ia), col(ACC, ia)])))
        arw = skia.Path(); arw.moveTo(905, 1101); arw.lineTo(929, 1113); arw.lineTo(905, 1125); arw.lineTo(910, 1113); arw.close()
        cv.drawPath(arw, P(col(INK, ia)))
    cv.restore()

# ------------------------------------------------------------ 5: RUANG PIKIR (36.64 - 42)
def g5(cv, t):
    tt = t - 36.64
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
    ev = [(0.1, 'whoosh'), (0.4, 'fizz_soft'), (3.3, 'card'), (3.45, 'shine'), (4.3, 'pop'),
          (5.38, 'whoosh'), (5.95, 'pop'), (6.82, 'crack'), (6.88, 'zap2'), (7.12, 'rise'), (7.15, 'ding'), (7.35, 'shine'), (7.8, 'plip'),
          (8.82, 'whoosh'), (8.95, 'card'), (9.55, 'swish'), (9.9, 'pop'), (10.05, 'pop'), (10.9, 'stamp'),
          (11.75, 'whoosh'), (12.35, 'pop'), (13.45, 'swish'), (13.6, 'swish'), (14.8, 'plop'), (15.0, 'fizz_soft'), (15.9, 'pop'), (16.3, 'ding_soft'),
          (17.45, 'whoosh'), (17.7, 'rise'), (18.75, 'ding'), (19.55, 'whoosh'), (19.8, 'zap2'), (19.95, 'plip'), (20.1, 'pop'), (20.4, 'pop'),
          (21.81, 'zoom'), (23.15, 'blink'), (23.6, 'shine'), (24.0, 'swish'), (25.6, 'pop'), (25.95, 'zap'), (26.55, 'ding'),
          (27.75, 'shine'), (27.8, 'pop'), (29.15, 'whoosh'), (29.4, 'card'), (30.1, 'pop'), (31.3, 'rise'), (32.3, 'ding'), (31.9, 'pop'),
          (33.08, 'whoosh'), (33.4, 'plop'), (33.85, 'plop'), (34.3, 'plop'), (34.6, 'pop'), (34.9, 'pop'), (35.2, 'pop'),
          (36.64, 'whoosh'), (36.75, 'boing'), (37.1, 'shine'), (37.6, 'pop')]
    ev += [(bt, 'heart') for bt in BEATS]
    ev += [(12.1 + k * 0.28, 'clock') for k in range(5)]
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
