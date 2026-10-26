#!/usr/bin/env python3
"""Ruang Pikir reel #2: 'Tes otak 7 detik, berani?' (Stroop effect)
python3 stroop.py preview t1 t2 ... | timeline out.json | video out.mp4"""
import sys, os, math, json, subprocess, random
import skia
import base as b
from base import (clamp, lerp, prog, eo, ei, eio, bo, bump, col, P, lg, rg, layer, font, XB, B, M, MONO, bl, tracked, parse,
                 pill, sparkle, person, ACC, ACC_L, ACC_XL, TXT, MUTED, CORAL, MINT, W, H, FPS)

RED, BLUE, GREEN, YELLOW, PURPLE = '#FF5A5F', '#4D8DFF', '#3FD68B', '#FFD23F', '#B57BFF'
NAMES = {'MERAH': RED, 'BIRU': BLUE, 'HIJAU': GREEN, 'KUNING': YELLOW, 'UNGU': PURPLE}
GRID = [('MERAH', BLUE), ('BIRU', YELLOW), ('HIJAU', RED), ('KUNING', PURPLE), ('UNGU', GREEN), ('MERAH', GREEN),
        ('BIRU', RED), ('HIJAU', PURPLE), ('KUNING', BLUE), ('UNGU', YELLOW), ('MERAH', YELLOW), ('HIJAU', BLUE)]
T_TEST0, T_TEST1 = 6.5, 13.5
try:
    _on = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vo', 'countdown_onsets_scaled.json')))
    CD = [3.6 + 0.04 + o for o in _on]
except Exception:
    CD = [3.6, 4.15, 4.75, 5.35, 5.95]

b.GROUPS = [(0.0, 6.3, 'TES OTAK'), (6.3, 13.8, 'MULAI!'), (13.8, 20.5, 'RISET · 1935'),
            (20.5, 31.0, 'ILUSTRASI'), (31.0, 38.5, 'KOMENTAR'), (38.5, 42.0, 'RUANG PIKIR')]
b.CAPS = [(0.15, "Sebutin [warnanya],", "bukan tulisannya!"),
          (3.6, "Siap?", "3... 2... 1... [mulai!]"),
          (6.5, "Sebutin [warnanya]!", "jangan baca tulisannya"),
          (13.8, "Susah, kan?", "Otak kayak [nge-lag]"),
          (17.0, "Ini namanya", "[efek Stroop] (1935)"),
          (20.5, "Otakmu terlatih", "[membaca otomatis]"),
          (24.0, "Tulisan selalu", "[sampai duluan]"),
          (27.5, "Dua informasi", "[tabrakan], otak ngerem"),
          (31.0, "Makanya kamu", "[lebih lambat] & sering salah"),
          (34.5, "Berapa yang benar?", "Tulis di [komentar]!"),
          (38.5, "Follow [Ruang Pikir]", "buat tes otak berikutnya")]

def draw_title(cv, t):
    a = eo(prog(t, 0.1, 0.55))
    if a <= 0: return
    segs = parse("Tes otak 7 detik, [berani]?"); f = font(XB, 62)
    tot = sum(f.measureText(s) for s, _ in segs); x = 540 - tot / 2; y = bl(f, 482) + (1 - a) * 20
    layer(cv, a); xx = x
    for s, h in segs: cv.drawString(s, xx, y + 5, f, P(col('#000000', 0.5), blur=7)); xx += f.measureText(s)
    for s, h in segs: cv.drawString(s, x, y, f, P(col(ACC_L if h else TXT))); x += f.measureText(s)
    cv.restore()
b.draw_title = draw_title

# ------------------------------------------------------------ helpers
def neon_word(cv, word, c, cx, cy, size, a=1.0, sc=1.0):
    if a <= 0: return
    f = font(XB, size * sc); w = f.measureText(word); y = bl(f, cy)
    cv.drawString(word, cx - w / 2, y, f, P(col(c, 0.55 * a), blur=size * 0.18))
    cv.drawString(word, cx - w / 2, y, f, P(col(c, a)))

def card(cv, cx, cy, w, h, a=1.0, border=ACC):
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    cv.drawRoundRect(r.makeOffset(0, 18), 30, 30, P(col('#000000', 0.55 * a), blur=22))
    cv.drawRoundRect(r, 30, 30, P(shader=lg(0, r.top(), 0, r.bottom(), [col('#1C1D2B', a), col('#101018', a)])))
    cv.drawRoundRect(r, 30, 30, P(col(border, 0.55 * a), stroke=3))
    return r

def ring(cv, cx, cy, r, frac, c, w=10, a=1.0):
    cv.drawCircle(cx, cy, r, P(col('#ffffff', 0.08 * a), stroke=w))
    p = skia.Path(); p.addArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), -90, 360 * frac); cv.drawPath(p, P(col(c, a), stroke=w))

def brain(cv, x, y, r, glow=0.0, hot=0.0, a=1.0):
    if a <= 0: return
    cv.save(); cv.translate(x, y)
    if glow > 0: cv.drawCircle(0, 0, r * 1.5, P(col(CORAL if hot > 0.5 else ACC, 0.35 * glow), blur=r * 0.4))
    blob = skia.Path()
    for (bx, by, br) in ((-0.55, -0.15, 0.62), (0.0, -0.35, 0.66), (0.55, -0.12, 0.62), (-0.35, 0.3, 0.55), (0.38, 0.3, 0.55)):
        blob.addCircle(bx * r, by * r, br * r)
    c1 = b.col('#C9CEFF', a) if hot < 0.5 else b.col('#FFB3A6', a)
    c2 = b.col('#7F8CFF', a) if hot < 0.5 else b.col('#FF5A5F', a)
    cv.drawPath(blob, P(shader=rg(-0.35 * r, -0.45 * r, 1.6 * r, [c1, c2, col('#2A2F66', a)], [0, 0.6, 1])))
    for pts in (((-0.9, -0.1), (-0.5, -0.35), (-0.2, 0.0)), ((-0.1, -0.7), (0.15, -0.35), (-0.05, 0.05)),
                ((0.3, -0.5), (0.65, -0.3), (0.85, 0.1)), ((-0.6, 0.45), (-0.25, 0.25), (0.05, 0.55)), ((0.2, 0.35), (0.5, 0.15), (0.75, 0.45))):
        p = skia.Path(); p.moveTo(pts[0][0] * r, pts[0][1] * r); p.quadTo(pts[1][0] * r, pts[1][1] * r, pts[2][0] * r, pts[2][1] * r)
        cv.drawPath(p, P(col('#1A1C3A', 0.55 * a), stroke=r * 0.06))
    cv.drawLine(0, -0.9 * r, 0, 0.75 * r, P(col('#1A1C3A', 0.4 * a), stroke=r * 0.05))
    cv.restore()

def eye(cv, x, y, s, a=1.0, look=(1, 0)):
    if a <= 0: return
    e = skia.Path(); e.moveTo(x - s, y); e.quadTo(x, y - s * 1.1, x + s, y); e.quadTo(x, y + s * 1.1, x - s, y); e.close()
    cv.drawPath(e, P(col(ACC, 0.4 * a), blur=14)); cv.drawPath(e, P(col('#D9DDFF', a)))
    cv.save(); cv.clipPath(e, skia.ClipOp.kIntersect, True)
    cv.drawCircle(x + look[0] * s * 0.25, y, s * 0.42, P(col(ACC, a))); cv.drawCircle(x + look[0] * s * 0.25, y, s * 0.2, P(col('#0B0C1E', a)))
    cv.drawCircle(x + look[0] * s * 0.25 - s * 0.12, y - s * 0.12, s * 0.07, P(col('#ffffff', a)))
    cv.restore()

def stamp(cv, text, cx, cy, p_, c=CORAL, rot=-12, size=54):
    if p_ <= 0: return
    cv.save(); cv.translate(cx, cy); cv.rotate(rot); s = 1.8 - 0.8 * eo(p_); cv.scale(s, s); layer(cv, clamp(p_ * 2))
    f = font(XB, size); w = f.measureText(text)
    r = skia.Rect(-w / 2 - 28, -size * 0.85, w / 2 + 28, size * 0.85)
    cv.drawRoundRect(r, 16, 16, P(col('#0B0B10', 0.8))); cv.drawRoundRect(r, 16, 16, P(col(c), stroke=6))
    cv.drawString(text, -w / 2, bl(f, 0), f, P(col(c))); cv.restore(); cv.restore()

# ------------------------------------------------------------ scenes
def g0(cv, t):
    # example card (0.2 - 3.6)
    ca = eo(prog(t, 0.2, 0.6)) * (1 - eio(prog(t, 3.3, 3.7)))
    if ca > 0:
        cv.save(); cv.translate(540, 760); s = 0.85 + 0.15 * bo(prog(t, 0.2, 0.7)); cv.scale(s, s); cv.translate(-540, -760)
        card(cv, 540, 760, 640, 300, ca)
        tracked(cv, 'CONTOH', 540, 650, font(MONO, 22), P(col(ACC_L, ca)), 6)
        neon_word(cv, 'MERAH', BLUE, 540, 775, 150, ca)
        cv.restore()
        wa = prog(t, 1.1, 1.4) * ca
        if wa > 0:
            pill(cv, 'MERAH', 400, 1010, wa, bgc='#2A1B22', fg=RED, size=34)
            cv.drawLine(330, 1010, 470, 1010, P(col(CORAL, wa), stroke=5))
            tracked(cv, 'SALAH', 400, 1080, font(MONO, 20), P(col(CORAL, wa)), 4)
        ra = prog(t, 1.7, 2.0) * ca
        if ra > 0:
            pill(cv, 'BIRU', 680, 1010, ra, bgc=BLUE, fg='#06122B', size=34)
            tracked(cv, 'BENAR', 680, 1080, font(MONO, 20), P(col(MINT, ra)), 4)
    # countdown (3.6 - 6.0), synced to the voice: 3 at ~4.25, 2 at ~4.85, 1 at ~5.45
    for k, (n, t0) in enumerate((('3', CD[1]), ('2', CD[2]), ('1', CD[3]))):
        p_ = prog(t, t0, t0 + 0.6)
        if 0 < p_ < 1:
            a = 1 - ei(prog(p_, 0.65, 1.0)); sc = 0.6 + 0.5 * bo(prog(p_, 0, 0.35))
            ring(cv, 540, 820, 190, p_, ACC, w=12, a=a)
            cv.save(); cv.translate(540, 820); cv.scale(sc, sc)
            f = font(XB, 260); w = f.measureText(n)
            cv.drawString(n, -w / 2, bl(f, 0), f, P(col(ACC, 0.5 * a), blur=30)); cv.drawString(n, -w / 2, bl(f, 0), f, P(col(TXT, a)))
            cv.restore()
    gp = prog(t, CD[4], CD[4] + 0.45)
    if 0 < gp < 1: neon_word(cv, 'MULAI!', MINT, 540, 820, 170, 1 - ei(prog(gp, 0.5, 1.0)), sc=0.7 + 0.4 * bo(prog(gp, 0, 0.5)))
    if CD[0] <= t < CD[1]:
        a = eo(prog(t, CD[0], CD[0] + 0.3)); neon_word(cv, 'SIAP?', ACC_L, 540, 820, 140, a)

def grid_pos(i):
    c, r = i % 3, i // 3
    return 210 + c * 330, 640 + r * 135
def g1(cv, t):
    tt = t - 6.0
    for i, (w, c) in enumerate(GRID):
        x, y = grid_pos(i); pr_ = prog(t, T_TEST0 + i * 0.04, T_TEST0 + 0.3 + i * 0.04)
        if pr_ <= 0: continue
        p_ = bo(pr_)
        cur = int((t - T_TEST0) / ((T_TEST1 - T_TEST0) / 12))
        on = cur == i and t < T_TEST1
        done = cur > i or t >= T_TEST1
        if on:
            r = skia.Rect(x - 150, y - 52, x + 150, y + 52)
            cv.drawRoundRect(r, 26, 26, P(col(c, 0.14))); cv.drawRoundRect(r, 26, 26, P(col(c, 0.9), stroke=4))
        neon_word(cv, w, c, x, y, 62, a=(0.45 if done and not on else 1.0), sc=p_ * (1.12 if on else 1.0))
    if T_TEST0 <= t:
        rem = clamp(1 - (t - T_TEST0) / (T_TEST1 - T_TEST0))
        cx, cy = 540, 1150
        f = font(XB, 40); s = f'{math.ceil(rem * 7) if rem > 0 else 0}'
        bar = skia.Rect(240, cy - 10, 840, cy + 10)
        cv.drawRoundRect(bar, 10, 10, P(col('#ffffff', 0.1)))
        cv.drawRoundRect(skia.Rect(240, cy - 10, 240 + 600 * rem, cy + 10), 10, 10, P(col(CORAL if rem < 0.3 else ACC)))
        cv.drawString(s + ' dtk', 860, bl(f, cy), f, P(col(TXT)))
    stamp(cv, 'WAKTU HABIS!', 540, 830, prog(t, T_TEST1, T_TEST1 + 0.3))

def g2(cv, t):
    tt = t - 13.8
    # glitchy brain lag
    ba = eo(prog(tt, 0.0, 0.4)) * (1 - eio(prog(tt, 3.0, 3.3)))
    if ba > 0:
        gl = 1 if (int(t * 12) % 5 == 0) else 0
        for dx, c in ((-8 * gl, '#FF5A5F'), (8 * gl, '#4D8DFF')):
            if gl: cv.save(); cv.translate(dx, 0); layer(cv, 0.35 * ba); brain(cv, 540, 820, 170, a=1); cv.restore(); cv.restore()
        brain(cv, 540, 820, 170, glow=0.6, a=ba)
        cv.save(); cv.translate(540, 820); cv.rotate(t * 260)
        arc = skia.Path(); arc.addArc(skia.Rect(-250, -250, 250, 250), 0, 80); cv.drawPath(arc, P(col(ACC_L, ba), stroke=10))
        cv.restore()
        cv.drawCircle(540, 820, 250, P(col('#ffffff', 0.07 * ba), stroke=10))
        pill(cv, 'LOADING...', 540, 1120, prog(tt, 0.5, 0.9) * ba, bgc='#262838', fg=ACC_XL, size=28, f=MONO)
    # research card
    cp = bo(prog(tt, 3.2, 3.7)); cpa = eo(prog(tt, 3.2, 3.5))
    if cpa > 0:
        cv.save(); cv.translate(540, 830); cv.rotate(-3 + 3 * cp); cv.scale(0.7 + 0.3 * cp, 0.7 + 0.3 * cp); layer(cv, cpa)
        r = skia.Rect(-330, -200, 330, 200)
        cv.drawRoundRect(r.makeOffset(0, 18), 26, 26, P(col('#000000', 0.55), blur=22))
        cv.drawRoundRect(skia.Rect(-330, -240, -120, -180), 18, 18, P(col('#2A2D52')))
        cv.drawRoundRect(r, 26, 26, P(shader=lg(0, -200, 0, 200, [col('#24263F'), col('#171828')]))); cv.drawRoundRect(r, 26, 26, P(col(ACC, 0.6), stroke=3))
        tracked(cv, 'PENELITI', 0, -140, font(MONO, 22), P(col(ACC_L)), 5)
        f1 = font(XB, 62); w = f1.measureText('J. Ridley Stroop'); cv.drawString('J. Ridley Stroop', -w / 2, bl(f1, -50), f1, P(col(TXT)))
        f2 = font(XB, 120); w = f2.measureText('1935'); cv.drawString('1935', -w / 2, bl(f2, 80), f2, P(shader=lg(0, 20, 0, 140, [col('#C4CAFF'), col(ACC)])))
        cv.restore(); cv.restore()
        st = prog(tt, 4.0, 4.3)
        if st > 0: stamp(cv, 'EFEK STROOP', 740, 960, st, size=34, rot=-14)

LANE_Y = (740, 960); EX, BX = 175, 885
def lane_path(i):
    y = LANE_Y[i]; p = skia.Path(); p.moveTo(EX + 70, 850); p.cubicTo(EX + 200, y, BX - 260, y, BX - 140, 850 + (y - 850) * 0.3); return p
def lane_pt(i, u):
    y = LANE_Y[i]; p0, p1, p2, p3 = (EX + 70, 850), (EX + 200, y), (BX - 260, y), (BX - 140, 850 + (y - 850) * 0.3)
    q = lambda a, b_, c, d: (1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * b_ + 3 * (1 - u) * u * u * c + u ** 3 * d
    return q(p0[0], p1[0], p2[0], p3[0]), q(p0[1], p1[1], p2[1], p3[1])
def g3(cv, t):
    tt = t - 20.5
    a0 = eo(prog(tt, 0.0, 0.5))
    hot = prog(tt, 7.0, 7.2)
    shake = 10 * math.sin(t * 80) * (1 - prog(tt, 7.0, 7.8)) if tt > 7.0 else 0
    eye(cv, EX, 850, 70, a0)
    neon_word(cv, 'MERAH', BLUE, EX + 10, 990, 40, a0)
    for i, (lab, c) in enumerate((('JALUR BACA', ACC_L), ('JALUR WARNA', BLUE))):
        d = eo(prog(tt, 0.3 + i * 0.3, 1.3 + i * 0.3))
        if d <= 0: continue
        pth = lane_path(i)
        meas = skia.PathMeasure(pth, False); L = meas.getLength(); seg = skia.Path(); meas.getSegment(0, L * d, seg, True)
        cv.drawPath(seg, P(col(c, 0.25), stroke=26, blur=6)); cv.drawPath(seg, P(col(c, 0.8), stroke=6, effect=skia.DashPathEffect.Make([18, 12], -t * 60)))
        x, y = lane_pt(i, 0.5)
        pill(cv, lab, x, y + (-52 if i == 0 else 52), prog(tt, 1.0 + i * 0.3, 1.4 + i * 0.3), bgc='#20223A', fg=c, size=24, f=MONO)
    cv.save(); cv.translate(shake, 0)
    brain(cv, BX, 850, 120, glow=0.5 + 0.5 * hot, hot=hot, a=a0)
    cv.restore()
    # race (24.0 -> arrivals)
    if tt >= 3.5:
        u1 = eio(prog(tt, 3.5, 4.7)); u2 = eio(prog(tt, 3.6, 6.6))
        for i, (u, c, lbl) in enumerate(((u1, ACC_XL, 'TULISAN'), (u2, BLUE, 'WARNA'))):
            if u >= 1 and tt > (4.7 if i == 0 else 6.6) + 0.3: continue
            x, y = lane_pt(i, u)
            for k in range(7):
                xx, yy = lane_pt(i, max(0, u - k * 0.025)); cv.drawCircle(xx, yy, 16 - k * 1.8, P(col(c, 1 - k * 0.13), blur=1 + k))
        for i, (ta, n) in enumerate(((4.7, '1'), (6.6, '2'))):
            p_ = bo(prog(tt, ta, ta + 0.3))
            if p_ > 0:
                cv.save(); cv.translate(BX + (-70 if i == 0 else 70), 850 - 150); cv.scale(p_, p_)
                cv.drawCircle(0, 0, 34, P(col(MINT if i == 0 else BLUE))); f = font(XB, 40); w = f.measureText(n)
                cv.drawString(n, -w / 2, bl(f, 0), f, P(col('#06122B'))); cv.restore()
    # collision + brake
    if tt >= 7.0:
        f_ = 1 - prog(tt, 7.0, 7.4)
        for k in range(10):
            ang = k * math.tau / 10; r0, r1 = 150 + 60 * (1 - f_), 190 + 90 * (1 - f_)
            cv.drawLine(BX + math.cos(ang) * r0, 850 + math.sin(ang) * r0, BX + math.cos(ang) * r1, 850 + math.sin(ang) * r1, P(col(CORAL, f_), stroke=6))
        stamp(cv, 'TABRAKAN!', 540, 640, prog(tt, 7.0, 7.3), size=44, rot=-6)
        pill(cv, 'OTAK NGEREM', BX - 120, 1080, prog(tt, 7.8, 8.2), bgc=CORAL, fg='#2A0E12', size=28)

def g4(cv, t):
    tt = t - 31.0
    ba = eo(prog(tt, 0.1, 0.5)) * (1 - eio(prog(tt, 3.2, 3.5)))
    if ba > 0:
        layer(cv, ba)
        tracked(cv, 'WAKTU REAKSI', 540, 640, font(MONO, 24), P(col(ACC_L)), 6)
        rows = ((('BIRU', BLUE), 'Warna cocok', 0.42, MINT, 0.4), (('BIRU', RED), 'Warna beda', 0.86, CORAL, 0.9))
        for i, ((w, c), lab, frac, bc, t0) in enumerate(rows):
            y = 790 + i * 210
            neon_word(cv, w, c, 220, y, 64)
            cv.drawString(lab, 140, y + 70, font(B, 28), P(col(MUTED)))
            g = eo(prog(tt, t0, t0 + 1.3))
            cv.drawRoundRect(skia.Rect(380, y - 26, 380 + 560, y + 26), 26, 26, P(col('#ffffff', 0.08)))
            cv.drawRoundRect(skia.Rect(380, y - 26, 380 + 560 * frac * g, y + 26), 26, 26, P(shader=lg(380, 0, 940, 0, [col(bc, 0.6), col(bc)])))
        pill(cv, 'lebih lambat', 760, 1110, prog(tt, 2.3, 2.7), bgc=CORAL, fg='#2A0E12', size=28)
        cv.restore()
    # comment bubbles (34.5 -> )
    if tt >= 3.4:
        ic = bo(prog(tt, 3.4, 3.9))
        cv.save(); cv.translate(540, 840); cv.scale(ic, ic)
        bub = skia.Path(); bub.addRRect(skia.RRect.MakeRectXY(skia.Rect(-120, -95, 120, 75), 60, 60))
        tail = skia.Path(); tail.moveTo(-60, 60); tail.lineTo(-90, 130); tail.lineTo(10, 70); tail.close()
        bub = skia.Op(bub, tail, skia.PathOp.kUnion_PathOp)
        cv.drawPath(bub, P(col(ACC, 0.45), blur=20)); cv.drawPath(bub, P(shader=lg(0, -95, 0, 130, [col('#A9B2FF'), col(ACC)])))
        for k in (-1, 0, 1): cv.drawCircle(k * 55, -10, 16, P(col('#0B0C1E')))
        cv.restore()
        for k, (txt, x, y, c) in enumerate((('10/12', 230, 640, MINT), ('7/12', 850, 690, ACC_L), ('12/12?!', 230, 1040, YELLOW),
                                            ('salah di HIJAU', 820, 1010, CORAL), ('4/12 wkwk', 560, 600, ACC_XL))):
            p_ = prog(tt, 3.9 + k * 0.35, 4.25 + k * 0.35)
            if p_ > 0:
                yy = y - 6 * math.sin(t * 2 + k)
                pill(cv, txt, x, yy, p_, bgc='#1E2033', fg=c, size=36, f=XB)

def g5(cv, t):
    tt = t - 38.5
    p_ = bo(prog(tt, 0.0, 0.6))
    cv.save(); cv.translate(540, 760); cv.scale(p_, p_); cv.translate(-540, -760)
    cv.drawCircle(540, 760, 280, P(col(ACC, 0.18), blur=60))
    cv.save(); cv.translate(540 - 260, 760 - 260); cv.scale(0.52, 0.52); __import__('logo_rp').c4(cv); cv.restore()
    cv.restore()
    a = eo(prog(tt, 0.4, 0.9)); layer(cv, a)
    tracked(cv, 'RUANG PIKIR', 540, 1050, font(XB, 58), P(col(TXT)), 10)
    pill(cv, 'Main tesnya di ruangpikir.id', 540, 1140, prog(tt, 0.9, 1.3), bgc='#20223A', fg=ACC_XL, size=32, f=B)
    cv.restore()

b.DRAWERS = [g0, g1, g2, g3, g4, g5]

def build_sfx():
    ev = [(0.1, 'whoosh'), (0.25, 'card'), (1.1, 'buzzer'), (1.7, 'ding_soft'), (3.6, 'whoosh'),
          (CD[1], 'beep'), (CD[2], 'beep'), (CD[3], 'beep'), (CD[4], 'go'), (T_TEST1, 'buzzer'), (T_TEST1 + 0.05, 'stamp'),
          (13.8, 'whoosh'), (13.9, 'fizz_soft'), (17.0, 'card'), (17.8, 'stamp'), (20.5, 'whoosh'), (20.9, 'rise'),
          (24.0, 'zap'), (24.1, 'swish'), (25.2, 'ding_soft'), (27.1, 'ding_soft'), (27.5, 'crack'), (27.55, 'stamp'), (28.3, 'pop'),
          (31.0, 'whoosh'), (31.4, 'rise'), (31.9, 'rise'), (33.3, 'pop'), (34.4, 'boing'), (38.5, 'whoosh'), (38.6, 'boing'), (39.4, 'pop')]
    step = (T_TEST1 - T_TEST0) / 12
    ev += [(T_TEST0 + i * step, 'clock') for i in range(12)]
    ev += [(34.9 + k * 0.35, 'pop') for k in range(5)]
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
