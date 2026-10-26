#!/usr/bin/env python3
"""Ruang Pikir reel: 'Ngerasa diliatin terus, kok bisa?' (spotlight effect)
python3 rp.py preview t1 t2 ...   (animation-time stills)
python3 rp.py timeline out.json
python3 rp.py video out.mp4
"""
import skia, math, random, json, sys, os, subprocess
import numpy as np

W, H, FPS, DUR = 1080, 1920, 30, 42.0
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, 'fonts')
ACC, ACC_L, ACC_XL = '#7F8CFF', '#AEB6FF', '#E3E6FF'
TXT, MUTED, CORAL, MINT = '#F0EFF6', '#8C8A94', '#FF6B57', '#3FD6A4'

# ------------------------------------------------------------ utils
def clamp(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def lerp(a, b, t): return a + (b - a) * t
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else (1.0 if t >= a else 0.0)
def eo(t): t = clamp(t); return 1 - (1 - t) ** 3
def ei(t): t = clamp(t); return t ** 3
def eio(t): t = clamp(t); return t * t * (3 - 2 * t)
def bo(t, s=1.70158): t = clamp(t) - 1; return t * t * ((s + 1) * t + s) + 1
def bump(t): t = clamp(t); return math.sin(math.pi * t)
def col(h, a=1.0):
    h = h.lstrip('#'); return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(clamp(a) * 255))
def P(c=None, stroke=0, blur=0, shader=None, effect=None):
    p = skia.Paint(AntiAlias=True)
    if c is not None: p.setColor(c)
    if shader is not None: p.setShader(shader)
    if stroke: p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke); p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if effect is not None: p.setPathEffect(effect)
    return p
def lg(x0, y0, x1, y1, cs, pos=None): return skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], cs, pos)
def rg(x, y, r, cs, pos=None): return skia.GradientShader.MakeRadial(skia.Point(x, y), r, cs, pos)
def layer(cv, a, rect=None): cv.saveLayerAlpha(rect, int(clamp(a) * 255))
_tf = {}
def font(name, size):
    if name not in _tf: _tf[name] = skia.Typeface.MakeFromFile(os.path.join(FD, name))
    f = skia.Font(_tf[name], size); f.setEdging(skia.Font.Edging.kAntiAlias); f.setSubpixel(True); return f
XB, B, M, MONO = 'PlusJakartaSans-ExtraBold.ttf', 'PlusJakartaSans-Bold.ttf', 'PlusJakartaSans-Medium.ttf', 'JetBrainsMono-ExtraBold.ttf'
def bl(f, cy): m = f.getMetrics(); return cy - (m.fAscent + m.fDescent) / 2
def tracked(cv, s, cx, cy, f, paint, sp):
    w = sum(f.measureText(c) + sp for c in s) - sp; x = cx - w / 2; b = bl(f, cy)
    for c in s: cv.drawString(c, x, b, f, paint); x += f.measureText(c) + sp
    return w
def parse(s):
    out, buf = [], ''
    for ch in s:
        if ch == '[':
            if buf: out.append((buf, False)); buf = ''
        elif ch == ']': out.append((buf, True)); buf = ''
        else: buf += ch
    if buf: out.append((buf, False))
    return out

# ------------------------------------------------------------ timeline
GROUPS = [(0.0, 7.0, 'PSIKOLOGI'), (7.0, 14.5, 'RISET · 2000'), (14.5, 22.5, 'RISET'),
          (22.5, 29.5, 'ILUSTRASI'), (29.5, 38.5, 'ILUSTRASI'), (38.5, 42.0, 'RUANG PIKIR')]
FADE = 0.35
CAPS = [(0.15, "Kamu ngerasa [semua orang]", "ngeliatin kamu?"),
        (3.0, "Salah ngomong dikit,", "langsung [kepikiran seharian]"),
        (7.0, "Tahun 2000, peneliti [Cornell]", "bikin eksperimen unik"),
        (10.5, "Mahasiswa pakai kaos", "yang [malu-maluin]"),
        (14.5, "Mereka yakin", "[setengah kelas] bakal sadar"),
        (18.0, "Kenyataannya? Cuma", "[1 dari 4] orang yang notice"),
        (22.5, "Ini namanya", "[spotlight effect]"),
        (25.5, "Di kepalamu, kamu", "[tokoh utama] yang disorot"),
        (29.5, "Padahal semua orang sibuk", "sama [sorotannya sendiri]"),
        (34.0, "Jadi santai aja.", "Nggak ada yang [seperhatian itu]"),
        (38.5, "Follow [Ruang Pikir]", "biar makin kenal isi kepalamu")]
def cap_windows():
    out = []
    for i, (s, a, b) in enumerate(CAPS):
        e = CAPS[i + 1][0] - 0.12 if i + 1 < len(CAPS) else DUR
        out.append((s, e, a, b))
    return out

# ------------------------------------------------------------ background + chrome
random.seed(3)
DUST = [(random.uniform(0, W), random.uniform(0, H), random.uniform(1, 2.6), random.uniform(6, 20), random.uniform(0, 6.3)) for _ in range(60)]
_bg = None
def bg_img():
    global _bg
    if _bg is None:
        s = skia.Surface(W, H); c = s.getCanvas()
        c.drawRect(skia.Rect(0, 0, W, H), P(shader=lg(0, 0, 0, H, [col('#08080B'), col('#111118'), col('#07070A')], [0, .5, 1])))
        c.drawRect(skia.Rect(0, 0, W, H), P(shader=rg(540, 860, 760, [col('#2A2F66', 0.42), col('#2A2F66', 0.0)])))
        c.drawRect(skia.Rect(0, 0, W, H), P(shader=rg(540, 900, 1300, [col('#000000', 0), col('#000000', 0), col('#000000', 0.6)], [0, .55, 1])))
        _bg = s.makeImageSnapshot()
    return _bg
def draw_bg(cv, t):
    cv.drawImage(bg_img(), 0, 0)
    for x, y, r, sp, ph in DUST:
        cv.drawCircle(x, (y - t * sp) % H, r, P(col(ACC_L, 0.08 + 0.14 * (0.5 + 0.5 * math.sin(t * 1.3 + ph)))))

def gi_at(t):
    for i, g in enumerate(GROUPS):
        if g[0] <= t < g[1]: return i
    return len(GROUPS) - 1
def draw_progress(cv, t):
    n, x0, x1, gap, y = len(GROUPS), 64, 1016, 12, 404
    sw = (x1 - x0 - gap * (n - 1)) / n; a = eo(prog(t, 0.05, 0.45))
    for i, g in enumerate(GROUPS):
        xa = x0 + i * (sw + gap)
        cv.drawLine(xa, y, xa + sw, y, P(col('#ffffff', 0.13 * a), stroke=6))
        f = prog(t, g[0], g[1])
        if f > 0: cv.drawLine(xa, y, xa + sw * f, y, P(col(ACC, a), stroke=6))
def draw_tag(cv, t):
    gi = gi_at(t); tag = GROUPS[gi][2]
    pop = bo(prog(t, GROUPS[gi][0], GROUPS[gi][0] + 0.35)) if gi > 0 else bo(prog(t, 0.1, 0.5))
    if pop <= 0: return
    f = font(MONO, 19); sp = 2.2; w = sum(f.measureText(c) + sp for c in tag) - sp
    cv.save(); cv.translate(540, 404); cv.scale(pop, pop); cv.translate(-540, -404)
    r = skia.Rect.MakeXYWH(540 - w / 2 - 18, 385, w + 36, 38)
    cv.drawRoundRect(r, 19, 19, P(col('#08080B'), stroke=14)); cv.drawRoundRect(r, 19, 19, P(shader=lg(0, 385, 0, 423, [col('#A3ADFF'), col(ACC)])))
    tracked(cv, tag, 540, 404, f, P(col('#0B0C1E')), sp)
    cv.restore()
def draw_title(cv, t):
    a = eo(prog(t, 0.1, 0.55))
    if a <= 0: return
    segs = parse("Ngerasa diliatin terus, [kok bisa]?"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 482) + (1 - a) * 20
    layer(cv, a)
    xx = x
    for s, h in segs: cv.drawString(s, xx, y + 5, f, P(col('#000000', 0.5), blur=7)); xx += f.measureText(s)
    for s, h in segs: cv.drawString(s, x, y, f, P(col(ACC_L if h else TXT))); x += f.measureText(s)
    cv.restore()
def caption_line(cv, s, cx, cy, size=44):
    segs = parse(s); fN, fH = font(B, size), font(XB, size); PH = 14
    ws = [(fH.measureText(x) + 2 * PH) if h else fN.measureText(x) for x, h in segs]
    tot = sum(ws); padX, h = 26, size * 1.72; x = cx - tot / 2
    r = skia.Rect.MakeXYWH(x - padX, cy - h / 2, tot + 2 * padX, h)
    cv.drawRoundRect(r.makeOffset(0, 10), 24, 24, P(col('#000000', 0.5), blur=14))
    cv.drawRoundRect(r, 24, 24, P(shader=lg(0, r.top(), 0, r.bottom(), [col('#1C1D2B', 0.95), col('#0E0E15', 0.95)])))
    cv.drawRoundRect(r, 24, 24, P(col(ACC, 0.35), stroke=2))
    b = bl(fN, cy)
    for (txt, hl), w in zip(segs, ws):
        if hl:
            rr = skia.Rect.MakeXYWH(x, cy - h * 0.37, w, h * 0.74)
            cv.drawRoundRect(rr, 12, 12, P(shader=lg(0, rr.top(), 0, rr.bottom(), [col('#A9B2FF'), col('#7F8CFF')])))
            cv.drawString(txt, x + PH, b, fH, P(col('#0B0C1E')))
        else: cv.drawString(txt, x, b, fN, P(col(TXT)))
        x += w
def draw_captions(cv, t):
    for (s, e, l1, l2) in cap_windows():
        if t < s or t > e + 0.25: continue
        ao = 1 - prog(t, e, e + 0.22)
        for i, line in enumerate((l1, l2)):
            d = i * 0.12; p_ = prog(t, s + d, s + d + 0.38)
            if p_ <= 0: continue
            sc = 0.82 + 0.18 * bo(p_); aa = min(clamp((t - s - d) / 0.16), ao)
            cy = (1252, 1340)[i] + (1 - eo(p_)) * 18
            cv.save(); cv.translate(540, cy); cv.scale(sc, sc); cv.translate(-540, -cy)
            layer(cv, aa, skia.Rect(0, cy - 100, W, cy + 100)); caption_line(cv, line, 540, cy); cv.restore(); cv.restore()
def draw_watermark(cv, t):
    tracked(cv, 'RUANG PIKIR', 540, 1440, font(MONO, 20), P(col(ACC_L, 0.3 * eo(prog(t, .5, 1.2)))), 6)

# ------------------------------------------------------------ props
def spotlight(cv, sx, floor_y, rw, a=1.0, top=560, warm=False, flick=1.0):
    if a <= 0: return
    a *= flick
    c0 = '#DDE1FF' if not warm else '#FFE2C2'
    cone = skia.Path(); cone.moveTo(sx - 34, top); cone.lineTo(sx + 34, top); cone.lineTo(sx + rw, floor_y); cone.lineTo(sx - rw, floor_y); cone.close()
    cv.drawPath(cone, P(shader=lg(0, top, 0, floor_y, [col(c0, 0.34 * a), col(c0, 0.07 * a)]), blur=10))
    cv.drawOval(skia.Rect(sx - rw * 1.15, floor_y - rw * 0.2, sx + rw * 1.15, floor_y + rw * 0.2), P(shader=rg(sx, floor_y, rw * 1.15, [col(c0, 0.45 * a), col(c0, 0.0)])))
    cv.drawRoundRect(skia.Rect(sx - 46, top - 30, sx + 46, top + 6), 10, 10, P(col('#2B2C38', a)))
    cv.drawRoundRect(skia.Rect(sx - 38, top - 4, sx + 38, top + 8), 6, 6, P(col(c0, 0.9 * a)))

def person(cv, x, foot, h, mood='neutral', look=(0, 0), shirt='plain', a=1.0, sweat=0.0, phone=0.0, glow=1.0, blink=0.0):
    bw, bh, hr = 0.42 * h, 0.6 * h, 0.17 * h
    hx, hy = x, foot - bh - hr * 0.92
    if a <= 0: return hx, hy, hr
    if a < 1: layer(cv, a)
    cv.drawOval(skia.Rect(x - bw * 0.75, foot - 10, x + bw * 0.75, foot + 12), P(col('#000000', 0.55), blur=8))
    body = skia.RRect.MakeRectXY(skia.Rect(x - bw / 2, foot - bh, x + bw / 2, foot), bw * 0.45, bw * 0.45)
    if glow > 0: cv.drawRRect(body, P(col(ACC, 0.25 * glow), stroke=12, blur=10))
    cv.drawRRect(body, P(shader=lg(0, foot - bh, 0, foot, [col('#30323F'), col('#191A22')])))
    cv.drawRRect(body, P(col(ACC, 0.8), stroke=3))
    if shirt == 'cringe':
        cx, cy, r = x, foot - bh * 0.55, bw * 0.3
        cv.drawCircle(cx, cy, r, P(col(CORAL, 0.18))); cv.drawCircle(cx, cy, r, P(col(CORAL), stroke=4))
        for s in (-1, 1): cv.drawLine(cx + s * r * 0.45, cy - r * 0.35, cx + s * r * 0.2, cy - r * 0.2, P(col(CORAL), stroke=4))
        m = skia.Path(); m.moveTo(cx - r * 0.55, cy + r * 0.1); m.quadTo(cx, cy + r * 0.85, cx + r * 0.55, cy + r * 0.1); m.close()
        cv.drawPath(m, P(col(CORAL)))
        cv.drawLine(cx - r * 0.35, cy + r * 0.25, cx + r * 0.35, cy + r * 0.25, P(col('#1A1B22'), stroke=2.5))
    if phone > 0:
        pr = skia.Rect.MakeXYWH(x - bw * 0.2, foot - bh * 0.78, bw * 0.4, bw * 0.55)
        cv.drawRoundRect(pr, 6, 6, P(col('#0E0F16'))); cv.drawRoundRect(pr.makeInset(3, 3), 4, 4, P(col(ACC_L, 0.85 * phone)))
        cv.drawCircle(hx, hy + hr * 0.4, hr * 1.1, P(col(ACC_L, 0.18 * phone), blur=14))
    if glow > 0: cv.drawCircle(hx, hy, hr, P(col(ACC, 0.25 * glow), stroke=12, blur=10))
    cv.drawCircle(hx, hy, hr, P(shader=rg(hx - hr * 0.3, hy - hr * 0.4, hr * 1.5, [col('#4A4D63'), col('#262735')])))
    cv.drawCircle(hx, hy, hr, P(col(ACC, 0.85), stroke=3))
    lx, ly = look
    ey = hy - hr * 0.05
    for s in (-1, 1):
        ex = hx + s * hr * 0.36 + lx * hr * 0.12
        eh = hr * 0.17 * (1 - blink * 0.9)
        cv.drawOval(skia.Rect(ex - hr * 0.13, ey - eh + ly * hr * 0.1, ex + hr * 0.13, ey + eh + ly * hr * 0.1), P(col(ACC_XL)))
        if mood == 'worried':
            cv.drawLine(ex - s * hr * 0.16, ey - hr * 0.34, ex + s * hr * 0.12, ey - hr * 0.26, P(col(ACC_XL), stroke=max(2, hr * 0.06)))
    my = hy + hr * 0.42
    m = skia.Path()
    if mood == 'happy':
        m.moveTo(hx - hr * 0.3, my - hr * 0.05); m.quadTo(hx, my + hr * 0.28, hx + hr * 0.3, my - hr * 0.05)
        for s in (-1, 1): cv.drawOval(skia.Rect.MakeXYWH(hx + s * hr * 0.6 - hr * 0.13, my - hr * 0.2, hr * 0.26, hr * 0.13), P(col('#FF8FA8', 0.5), blur=3))
    elif mood == 'worried':
        m.moveTo(hx - hr * 0.24, my + hr * 0.04)
        for k in range(1, 7): m.lineTo(hx - hr * 0.24 + k * hr * 0.08, my + (hr * 0.05 if k % 2 else -hr * 0.03))
    else:
        m.moveTo(hx - hr * 0.18, my); m.lineTo(hx + hr * 0.18, my)
    cv.drawPath(m, P(col(ACC_XL), stroke=max(2.5, hr * 0.07)))
    if sweat > 0:
        sx, sy = hx + hr * 0.95, hy - hr * 0.35 + sweat * hr * 0.3
        d = skia.Path(); d.moveTo(sx, sy - hr * 0.28); d.quadTo(sx + hr * 0.16, sy, sx, sy + hr * 0.1); d.quadTo(sx - hr * 0.16, sy, sx, sy - hr * 0.28); d.close()
        cv.drawPath(d, P(col('#8FD3FF', min(1, sweat * 2))))
    if a < 1: cv.restore()
    return hx, hy, hr

def watcher_eye(cv, x, y, s, tx, ty, t, ph, a):
    if a <= 0: return
    bl_ = 1.0
    cyc = (t * 0.55 + ph) % 1.0
    if cyc > 0.93: bl_ = abs((cyc - 0.965) / 0.035)
    for side in (-1, 1):
        ex = x + side * s * 1.25
        e = skia.Path(); h = s * 0.55 * bl_
        e.moveTo(ex - s, y); e.quadTo(ex, y - h * 2, ex + s, y); e.quadTo(ex, y + h * 2, ex - s, y); e.close()
        cv.drawPath(e, P(col(ACC_L, 0.45 * a), blur=10))
        cv.drawPath(e, P(col('#D9DDFF', a)))
        dx, dy = tx - ex, ty - y; L = math.hypot(dx, dy) or 1
        if bl_ > 0.3:
            cv.save(); cv.clipPath(e, skia.ClipOp.kIntersect, True)
            cv.drawCircle(ex + dx / L * s * 0.35, y + dy / L * s * 0.2, s * 0.42, P(col('#0B0C1E', a)))
            cv.restore()

def scribble(cv, cx, cy, r, t, head=1.0, color=CORAL, width=6):
    N = int(360 * head)
    if N < 3: return
    p = skia.Path()
    for k in range(N + 1):
        u = k / 360 * math.tau * 1.6 + 0.3
        x = 0.62 * math.sin(3.1 * u + 2) + 0.38 * math.sin(7.7 * u + 3.0); y = 0.62 * math.cos(2.3 * u + 1) + 0.38 * math.cos(6.1 * u + 2.0)
        x += 0.03 * math.sin(t * 3 + k * 0.05)
        (p.moveTo if k == 0 else p.lineTo)(cx + x * r, cy + y * r * 0.62)
    cv.drawPath(p, P(col(color, 0.4), stroke=width * 3, blur=8)); cv.drawPath(p, P(col(color), stroke=width))

def pill(cv, text, x, y, a, bgc=ACC, fg='#0B0C1E', size=28, f=XB):
    if a <= 0: return
    ff = font(f, size); w = ff.measureText(text); h = size * 1.6
    cv.save(); cv.translate(x, y); s = 0.7 + 0.3 * bo(a); cv.scale(s, s); layer(cv, clamp(a * 1.5))
    r = skia.Rect.MakeXYWH(-w / 2 - 20, -h / 2, w + 40, h)
    cv.drawRoundRect(r.makeOffset(0, 6), h / 2, h / 2, P(col('#000000', 0.45), blur=8)); cv.drawRoundRect(r, h / 2, h / 2, P(col(bgc)))
    cv.drawString(text, -w / 2, bl(ff, 0), ff, P(col(fg))); cv.restore(); cv.restore()

def sparkle(cv, x, y, r, a, c=ACC_L):
    if a <= 0 or r <= 0: return
    p = skia.Path(); p.moveTo(x, y - r); p.quadTo(x + r * .16, y - r * .16, x + r, y); p.quadTo(x + r * .16, y + r * .16, x, y + r)
    p.quadTo(x - r * .16, y + r * .16, x - r, y); p.quadTo(x - r * .16, y - r * .16, x, y - r); p.close()
    cv.drawPath(p, P(col(c, .5 * a), blur=r * .3)); cv.drawPath(p, P(col(c, a)))

# ------------------------------------------------------------ scenes
EYES = [(170, 700, 26, .0), (900, 660, 30, .3), (130, 930, 22, .55), (950, 900, 26, .15), (260, 1080, 20, .7), (830, 1100, 22, .4),
        (330, 620, 18, .85), (760, 600, 18, .6)]
def g0(cv, t):
    on = prog(t, 0.25, 0.32); flick = 1.0
    if 0.25 < t < 0.7: flick = 0.55 + 0.45 * (1 if int(t * 40) % 3 else 0.3)
    spotlight(cv, 540, 1150, 190, a=on, flick=flick)
    worried = t >= 3.0
    sw = prog(t, 3.2, 4.0) if worried else 0
    look = (math.sin(t * 2.2) * 0.8, 0) if not worried else (math.sin(t * 6) * 0.9, 0.2)
    bob = 4 * math.sin(t * 2.4)
    hx, hy, hr = person(cv, 540, 1150 + bob * 0, 400, mood='worried' if worried else 'neutral', look=look, a=eo(prog(t, 0.3, 0.6)), sweat=sw)
    if worried:
        k = 1 + 0.035 * bump(((t - 3.0) % 1.0) / 0.25) if (t - 3.0) % 1.0 < 0.25 else 1
        scribble(cv, hx, hy - hr * 2.0, 120, t, head=eo(prog(t, 3.3, 5.0)), width=6)
    for i, (x, y, s, ph) in enumerate(EYES):
        a = eo(prog(t, 0.6 + i * 0.18, 0.9 + i * 0.18))
        near = 1 + 0.15 * eio(prog(t, 3.0, 6.5))
        ex = lerp(540, x, 1 / near + (1 - 1 / near) * 0.6); ey = lerp(900, y, 1 / near + (1 - 1 / near) * 0.6)
        watcher_eye(cv, ex, ey, s * near, hx, hy, t, ph, a)

def g1(cv, t):
    tt = t - 7.0
    # case file card
    cp = bo(prog(tt, 0.2, 0.7)); ca = 1 - eio(prog(tt, 3.2, 3.6))
    if cp > 0 and ca > 0:
        cv.save(); cv.translate(540, 830); cv.rotate(-3 + 3 * cp); cv.scale(0.7 + 0.3 * cp, 0.7 + 0.3 * cp); layer(cv, ca)
        r = skia.Rect(-330, -200, 330, 200)
        cv.drawRoundRect(r.makeOffset(0, 18), 26, 26, P(col('#000000', 0.55), blur=22))
        tab = skia.Rect(-330, -240, -120, -180); cv.drawRoundRect(tab, 18, 18, P(col('#2A2D52')))
        cv.drawRoundRect(r, 26, 26, P(shader=lg(0, -200, 0, 200, [col('#24263F'), col('#171828')])))
        cv.drawRoundRect(r, 26, 26, P(col(ACC, 0.6), stroke=3))
        tracked(cv, 'EKSPERIMEN', 0, -140, font(MONO, 22), P(col(ACC_L)), 5)
        f1 = font(XB, 64); w = f1.measureText('Cornell University'); cv.drawString('Cornell University', -w / 2, bl(f1, -50), f1, P(col(TXT)))
        f2 = font(XB, 120); w = f2.measureText('2000'); cv.drawString('2000', -w / 2, bl(f2, 80), f2, P(shader=lg(0, 20, 0, 140, [col('#C4CAFF'), col(ACC)])))
        st = prog(tt, 0.9, 1.25)
        if st > 0:
            cv.save(); cv.translate(210, 120); cv.rotate(-14); s = 1.6 - 0.6 * eo(st); cv.scale(s, s); layer(cv, st)
            cv.drawRoundRect(skia.Rect(-110, -34, 110, 34), 10, 10, P(col(CORAL), stroke=5))
            tracked(cv, 'SPOTLIGHT', 0, 0, font(MONO, 24), P(col(CORAL)), 3)
            cv.restore(); cv.restore()
        cv.restore(); cv.restore()
    # classroom scene from 10.5
    if tt >= 3.35:
        a = eo(prog(tt, 3.35, 3.8))
        # audience row (backs of heads)
        layer(cv, a)
        walk = eo(prog(tt, 3.5, 5.2)); px = lerp(140, 540, walk); hop = abs(math.sin(tt * 9)) * 10 * (1 - walk)
        spotlight(cv, 540, 1060, 170, a=0.55 * a)
        hx, hy, hr = person(cv, px, 1060 - hop, 340, mood='worried' if tt > 5.0 else 'neutral', shirt='cringe', look=(0.0, 0.4), sweat=prog(tt, 5.6, 6.4))
        zoom = bo(prog(tt, 5.7, 6.2)) * (1 - prog(tt, 7.2, 7.5))
        if zoom > 0:
            cv.save(); cv.translate(830, 760); cv.scale(zoom, zoom)
            cv.drawCircle(0, 0, 120, P(col('#000000', .5), blur=16)); cv.drawCircle(0, 0, 112, P(col('#20212C'))); cv.drawCircle(0, 0, 112, P(col(CORAL), stroke=5))
            r = 66
            cv.drawCircle(0, 0, r, P(col(CORAL), stroke=6))
            for s in (-1, 1): cv.drawLine(s * r * .45, -r * .35, s * r * .2, -r * .2, P(col(CORAL), stroke=6))
            m = skia.Path(); m.moveTo(-r * .55, r * .1); m.quadTo(0, r * .85, r * .55, r * .1); m.close(); cv.drawPath(m, P(col(CORAL)))
            cv.restore()
            cv.drawLine(hx + 40, 1060 - 340 * 0.35, 830 - 90, 760 + 60, P(col(CORAL, 0.6 * zoom), stroke=3, effect=skia.DashPathEffect.Make([10, 8], 0)))
        for i in range(5):
            bx = 150 + i * 195; by = 1165
            cv.drawCircle(bx, by - 60, 46, P(shader=rg(bx - 10, by - 80, 70, [col('#2C2E3D'), col('#15161E')])))
            cv.drawRoundRect(skia.Rect(bx - 70, by - 22, bx + 70, by + 60), 40, 40, P(col('#14151C')))
            cv.drawCircle(bx, by - 60, 46, P(col(ACC, 0.35), stroke=2))
        cv.restore()

def g2(cv, t):
    tt = t - 14.5
    base, x1, x2, maxh, bw = 1100, 330, 750, 440, 200
    a0 = eo(prog(tt, 0.1, 0.5))
    layer(cv, a0)
    cv.drawLine(150, base, 930, base, P(col('#ffffff', 0.18), stroke=3))
    def bar(x, frac, label, num, c1, c2, a):
        h = maxh * frac
        r = skia.Rect(x - bw / 2, base - h, x + bw / 2, base)
        if h > 1:
            cv.drawRoundRect(r, 22, 22, P(col(c2, 0.35), blur=18)); cv.drawRoundRect(r, 22, 22, P(shader=lg(0, base - h, 0, base, [col(c1), col(c2)])))
        tracked(cv, label, x, base + 44, font(MONO, 22), P(col(MUTED)), 3)
        if a > 0:
            f = font(XB, 76); s = num; w = f.measureText(s)
            cv.drawString(s, x - w / 2, base - h - 34, f, P(col(TXT, a)))
    g = eo(prog(tt, 0.5, 2.0)); bar(x1, 0.5 * g, 'TEBAKAN', f'{int(round(50 * g))}%', '#C4CAFF', ACC, a=min(1, g * 3))
    r_ = eo(prog(tt, 3.6, 4.8)); bar(x2, 0.25 * r_, 'KENYATAAN', f'{int(round(25 * r_))}%', '#FFB09F', CORAL, a=min(1, r_ * 3))
    # 1 dari 4 icons
    for i in range(4):
        p_ = bo(prog(tt, 5.0 + i * 0.2, 5.35 + i * 0.2))
        if p_ <= 0: continue
        cx = 360 + i * 120; cy = 690
        cv.save(); cv.translate(cx, cy); cv.scale(p_, p_)
        lit = i == 0 and tt > 5.9
        c = CORAL if lit else '#3A3C4C'
        cv.drawCircle(0, -36, 26, P(col(c))); cv.drawRoundRect(skia.Rect(-34, -4, 34, 64), 26, 26, P(col(c)))
        if lit:
            cv.drawCircle(0, 10, 70, P(col(CORAL, 0.25), blur=20))
            for k in range(8):
                ang = k * math.pi / 4; rr = 70 + 14 * bump(prog(tt, 5.9, 6.6))
                cv.drawLine(math.cos(ang) * 58, 14 + math.sin(ang) * 58, math.cos(ang) * rr, 14 + math.sin(ang) * rr, P(col(CORAL, bump(prog(tt, 5.9, 6.8))), stroke=4))
        cv.restore()
    pill(cv, '1 dari 4 orang', 540, 600, prog(tt, 6.0, 6.4), bgc=CORAL, fg='#2A0E12', size=30)
    cv.restore()

def g3(cv, t):
    tt = t - 22.5
    on = prog(tt, 0.05, 0.15); flick = 0.6 + 0.4 * (1 if int(t * 40) % 3 else .3) if tt < 0.4 else 1.0
    spotlight(cv, 540, 1150, 240, a=on * 1.1, flick=flick, top=600)
    # big title
    p_ = eo(prog(tt, 0.25, 0.9)) * (1 - eio(prog(tt, 2.7, 3.05)))
    if p_ > 0:
        layer(cv, p_)
        f = font(XB, 92); sp = 10
        cv.save(); cv.translate(0, (1 - p_) * 30)
        tracked(cv, 'SPOTLIGHT', 540, 680, f, P(col(ACC, 0.55), blur=16), sp)
        tracked(cv, 'SPOTLIGHT', 540, 680, f, P(shader=lg(0, 640, 0, 720, [col('#EEF0FF'), col(ACC_L)])), sp)
        tracked(cv, 'EFFECT', 540, 780, font(XB, 64), P(col(ACC_L)), 18)
        cv.restore(); cv.restore()
    hx, hy, hr = person(cv, 540, 1150, 330, mood='neutral' if tt < 3.0 else 'happy', look=(0, -0.3), glow=1.4)
    star = bo(prog(tt, 3.0, 3.5))
    if star > 0:
        pill(cv, 'TOKOH UTAMA', 540, hy - hr - 70, star, bgc=ACC, size=30)
        for k, (sx, sy, ph) in enumerate(((330, 940, 0), (760, 900, 1.2), (300, 1080, 2.1), (790, 1060, 3.3))):
            tw = 0.5 + 0.5 * math.sin(t * 4 + ph); sparkle(cv, sx, sy, 14 + 8 * tw, star * (0.4 + 0.6 * tw))

CROWD = [(170, 1080, 250, 0.0), (360, 1130, 270, 0.3), (720, 1130, 270, 0.6), (910, 1080, 250, 0.9)]
def g4(cv, t):
    tt = t - 29.5
    relax = eio(prog(tt, 4.5, 5.6))
    for i, (x, foot, h, d) in enumerate(CROWD):
        a = eo(prog(tt, 0.2 + d * 0.5, 0.6 + d * 0.5))
        spotlight(cv, x, foot, 100, a=a * (0.9 - 0.4 * relax), top=620)
        person(cv, x, foot, h, mood='neutral', look=(0, 0.6), phone=1.0, a=a, glow=0.6)
        if a > 0.5 and relax < 0.5:
            pill(cv, ['kerjaanku', 'chat dia', 'jerawatku', 'besok ujian'][i], x, foot - h - 30, (a - 0.5) * 2 * (1 - relax * 2), bgc='#262838', fg=ACC_XL, size=22, f=B)
    sp = 1 - 0.5 * relax
    spotlight(cv, 540, 1180, 150, a=sp, top=620)
    hx, hy, hr = person(cv, 540, 1180, 330, mood='happy' if relax > 0.3 else 'worried', look=(0, 0), glow=1.0, sweat=0 if relax > 0.1 else 0.6)
    if relax > 0:
        for k in range(6):
            ang = k * math.pi / 3 + t * 0.6; rr = 150 + 10 * math.sin(t * 3 + k)
            sparkle(cv, hx + math.cos(ang) * rr, hy + math.sin(ang) * rr * 0.6, 12, relax * (0.5 + 0.5 * math.sin(t * 5 + k)), c=MINT)
        pill(cv, 'santai aja', 540, hy - hr - 70, prog(tt, 5.0, 5.5), bgc=MINT, fg='#062018', size=30)

def door_head(cv, x, y, s, t):
    """Ruang Pikir logo (head with glowing door), drawn in 1000-box at (x,y) top-left scaled s"""
    from_logo = __import__('logo_rp')
    cv.save(); cv.translate(x, y); cv.scale(s, s); from_logo.c4(cv); cv.restore()

def g5(cv, t):
    tt = t - 38.5
    p_ = bo(prog(tt, 0.0, 0.6))
    cv.save(); cv.translate(540, 780); cv.scale(p_, p_); cv.translate(-540, -780)
    cv.drawCircle(540, 780, 300, P(col(ACC, 0.18), blur=60))
    door_head(cv, 540 - 280, 780 - 280, 0.56, t)
    cv.restore()
    a = eo(prog(tt, 0.4, 0.9))
    layer(cv, a)
    tracked(cv, 'RUANG PIKIR', 540, 1085, font(XB, 58), P(col(TXT)), 10)
    tracked(cv, 'ruangpikir.id', 540, 1140, font(B, 30), P(col(ACC_L)), 1)
    cv.restore()

DRAWERS = [g0, g1, g2, g3, g4, g5]
def draw_groups(cv, t):
    for i, (s, e, tag) in enumerate(GROUPS):
        fi = FADE if i > 0 else 0; fo = FADE if i < len(GROUPS) - 1 else 0
        if t < s or t > e + fo: continue
        ain = eo(prog(t, s, s + fi)) if fi else 1.0; aout = 1 - eio(prog(t, e, e + fo)) if fo else 1.0
        a = min(ain, aout); sc = (1.05 - 0.05 * ain) if fi else 1.0; sc *= 1 + 0.02 * prog(t, s, e)
        cv.save(); cv.translate(540, 880); cv.scale(sc, sc); cv.translate(-540, -880)
        if a < 1: layer(cv, a)
        DRAWERS[i](cv, t)
        if a < 1: cv.restore()
        cv.restore()

def draw_frame(cv, t):
    draw_bg(cv, t); draw_groups(cv, t); draw_watermark(cv, t); draw_progress(cv, t); draw_tag(cv, t); draw_title(cv, t); draw_captions(cv, t)
    fe = prog(t, DUR - 0.35, DUR)
    if fe > 0: cv.drawRect(skia.Rect(0, 0, W, H), P(col('#000000', fe)))

def build_sfx():
    ev = [(0.1, 'whoosh'), (0.25, 'clunk'), (3.0, 'heart'), (3.55, 'heart'), (3.3, 'fizz_soft'), (7.0, 'whoosh'), (7.2, 'card'), (7.9, 'stamp'),
          (10.35, 'whoosh'), (12.2, 'pop'), (13.0, 'boing'), (14.5, 'whoosh'), (15.0, 'rise'), (16.5, 'ding_soft'), (18.1, 'rise'), (19.3, 'zap2'),
          (19.5, 'pop'), (19.7, 'pop'), (19.9, 'pop'), (20.1, 'pop'), (20.4, 'ding'), (22.5, 'whoosh'), (22.55, 'clunk'), (22.8, 'shine'),
          (25.5, 'ding_soft'), (29.5, 'whoosh'), (29.7, 'clunk'), (29.85, 'clunk'), (30.0, 'clunk'), (30.15, 'clunk'), (34.0, 'shine'),
          (38.5, 'whoosh'), (38.6, 'boing'), (39.0, 'ding_soft')]
    for i in range(8): ev.append((0.6 + i * 0.18, 'blink'))
    for (s, a, b) in CAPS: ev.append((s, 'tick'))
    return sorted(ev)

# ------------------------------------------------------------ warp to voice
VO_META = os.path.join(HERE, 'vo', 'lines.json')
def build_warp():
    A, O = [0.0], [0.0]
    lines = json.load(open(VO_META)) if os.path.exists(VO_META) else []
    anchors = [l['anchor'] for l in lines]
    for k, l in enumerate(lines):
        if l['anchor'] > A[-1]: O.append(O[-1] + (l['anchor'] - A[-1])); A.append(l['anchor'])
        nxt = anchors[k + 1] if k + 1 < len(anchors) else DUR
        need = l['dur'] + (0.9 if k + 1 == len(lines) else 0.35)
        O.append(O[-1] + max(nxt - l['anchor'], need)); A.append(nxt)
    if A[-1] < DUR: O.append(O[-1] + DUR - A[-1]); A.append(DUR)
    return np.array(A), np.array(O), lines
WA, WO, VO_LINES = build_warp(); OUT_DUR = float(WO[-1])
def anim_t(T): return float(np.interp(T, WO, WA))
def out_t(t): return float(np.interp(t, WA, WO))

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'preview':
        os.makedirs(os.path.join(HERE, 'preview'), exist_ok=True); s = skia.Surface(W, H); cv = s.getCanvas()
        for ts in sys.argv[2:]:
            t = float(ts); cv.clear(skia.ColorBLACK); draw_frame(cv, t); s.makeImageSnapshot().save(os.path.join(HERE, 'preview', f't{t:05.2f}.png'), skia.kPNG)
    elif mode == 'timeline':
        tl = {'out_dur': OUT_DUR, 'sfx': [(round(out_t(t), 4), k) for t, k in build_sfx()],
              'voice': [(round(out_t(l['anchor']) + 0.04, 4), l['file']) for l in VO_LINES]}
        json.dump(tl, open(sys.argv[2], 'w'), indent=1); print('out_dur', OUT_DUR)
    elif mode == 'video':
        n = int(round(OUT_DUR * FPS)); s = skia.Surface(W, H); cv = s.getCanvas()
        pr = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', sys.argv[2]], stdin=subprocess.PIPE)
        for fi in range(n):
            cv.clear(skia.ColorBLACK); draw_frame(cv, anim_t(fi / FPS)); pr.stdin.write(s.makeImageSnapshot().tobytes())
            if fi % 200 == 0: print('frame', fi, '/', n, flush=True)
        pr.stdin.close(); pr.wait()
