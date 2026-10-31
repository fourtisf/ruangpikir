#!/usr/bin/env python3
"""Ruang Pikir reel #15: 'Chat duluan, kok gengsi?' (menyapa teman lama; Liu, Rim, Min & Min 2022/2023, JPSP)
Format "trik psikologi praktis" seperti EP03/EP12-EP14: tokoh kapsul ragu chat duluan, ponsel kaca dengan layar chat (riwayat lama,
mengetik lalu menghapus, gelembung rahasia emas "1 chat ini"), dua jendela kota + pesan yang terbang, "yang dikira" vs "kenyataannya",
notifikasi kejutan + meter KAGET/SENANG, dinding kaca GENGSI yang retak dan pecah + stempel SALAH TEBAK, kolom komentar inisial.
python3 episode.py preview t1 t2 ... | timeline out.json | video out.mp4"""
import sys, os, math, json, subprocess, random
import skia
import base as b
from base import (clamp, lerp, prog, eo, ei, eio, bo, bump, col, P, lg, rg, layer, font, XB, B, M, MONO, bl, tracked, parse,
                 pill, sparkle, person, ACC, ACC_L, ACC_XL, TXT, MUTED, CORAL, MINT, W, H, FPS)

VIOLET, YELLOW, INK, HL = '#B57BFF', '#FFD23F', '#0B0C1E', '#AEB6FF'

# adegan (waktu animasi, DUR 42); tag tidak ditampilkan
b.GROUPS = [(0.0, 4.38, 'A'), (4.38, 8.9, 'B'), (8.9, 14.82, 'C'), (14.82, 19.73, 'D'), (19.73, 23.85, 'E'),
            (23.85, 27.85, 'F'), (27.85, 30.96, 'G'), (30.96, 36.6, 'H'), (36.6, 42.0, 'J')]
PHRASES = [(0.15, 'Tiba-tiba [keinget teman lama],'), (1.94, 'tapi [gengsi chat duluan]?'), (2.96, 'Kirim [satu chat ini].'),
           (4.38, 'Kita sering mikir:'), (5.44, 'nanti [ganggu],'), (6.43, 'nanti [dikira aneh],'), (7.53, 'udah [kelamaan] nggak ngobrol.'),
           (8.9, 'Tahun [2022],'), (10.38, 'psikolog [Peggy Liu] menguji ini'), (12.07, 'ke lebih dari [5.900 orang].'),
           (14.82, 'Peserta diminta [menyapa teman]'), (16.5, 'yang udah [lama nggak dikontak],'), (18.1, 'cukup lewat [pesan singkat].'),
           (19.73, 'Hasilnya?'), (20.8, 'Yang disapa ternyata [lebih senang]'), (22.25, 'dari yang [dikira pengirimnya].'),
           (23.85, 'Apalagi kalau chatnya [nggak disangka-sangka].'), (25.81, 'Makin [kaget],'), (26.8, 'makin [senang].'),
           (27.85, 'Jadi, rasa [takut ganggu] itu,'), (29.71, 'seringnya cuma [salah tebak].'),
           (30.96, 'Kirim aja:'), (31.77, '"hai, [tiba-tiba keinget kamu]."'), (33.27, 'Siapa yang [muncul di kepalamu]?'), (34.89, 'Tulis [inisialnya] di komentar!'),
           (36.6, 'Follow [Ruang Pikir],'), (37.9, 'biar makin kenal [isi kepalamu].')]
b.CAPS = [(t, s, '') for t, s in PHRASES]          # dipakai base hanya untuk jadwal

# ------------------------------------------------------------ chrome gaya sinematik
b.draw_tag = lambda cv, t: None
b.draw_progress = lambda cv, t: None
def draw_title(cv, t):
    a = eo(prog(t, 0.05, 0.35)) * (1 - eio(prog(t, 4.0, 4.38)))
    if a <= 0: return
    segs = parse("Chat duluan, [kok gengsi]?"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 232) + (1 - eo(prog(t, 0.05, 0.35))) * 16 - 10 * eio(prog(t, 4.0, 4.38))
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
    # pendar layar ponsel dari bawah (tanpa titik/bokeh)
    cv.drawCircle(560, 1000, 900, P(shader=rg(560, 1000, 900, [col('#7F8CFF', 0.07), col('#B57BFF', 0.03), col('#B57BFF', 0)], [0, 0.5, 1])))
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

def phone(cv, w, h, a, t, banner=0.0, btext='kamu kok gitu sih?', screen=1.0, btitle='Komentar baru'):
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
            by = lerp(-h * 0.62, -h * 0.06, bo(banner)); notif(cv, 0, by, w * 0.88, btext, sa * clamp(banner * 3), title=btitle)
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

GREY = ('#D5D7E8', '#6A6D85', '#24263A')

def mood_ball(cv, cx, cy, r, a, t, mood='sad', cols=None, label=None):
    sphere(cv, cx, cy, r, cols or GREY, a, 0.6)
    face(cv, cx, cy + r * 0.05, r, mood, a, t)
    if label: mono(cv, label, cx, cy + r + 46, 26, ACC_L, 0.9 * a, sp=3)

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

AV_COL = ['#FF8A7A', '#7FB8FF', '#B57BFF', '#FFC56B', '#3FD6A4', '#FF7FC8', '#8C93FF', '#5AD1E6']
# ------------------------------------------------------------ helper EP12: panggung sinematik + tokoh kapsul premium (gaya EP03 yang viral)
AV_COL = ['#FF8A7A', '#7FB8FF', '#B57BFF', '#FFC56B', '#3FD6A4', '#FF7FC8', '#8C93FF', '#5AD1E6']
GOLD = '#FFC56B'; HOTPINK = '#FF7FC8'

def hero(cv, x, foot, h, mood='worried', a=1.0, t=0.0, sweat=0.0, glow=0.0, gc=ACC, tremble=0.0, mouth_open=0.0):
    """tokoh kapsul premium (siluet seperti EP03): badan kapsul mengilap + kepala bola dengan ekspresi"""
    if a <= 0: return
    x += tremble * 5 * math.sin(t * 58)
    bw, bh, hr = 0.42 * h, 0.6 * h, 0.17 * h
    hx, hy = x, foot - bh - hr * 0.92
    if a < 1: layer(cv, a)
    cv.drawOval(skia.Rect(x - bw * 0.85, foot - 12, x + bw * 0.85, foot + 14), P(col('#000000', 0.6), blur=10))
    body = skia.RRect.MakeRectXY(skia.Rect(x - bw / 2, foot - bh, x + bw / 2, foot), bw * 0.45, bw * 0.45)
    if glow > 0:
        cv.drawRRect(body, P(col(gc, 0.45 * glow), stroke=26, blur=22)); cv.drawCircle(hx, hy, hr * 1.2, P(col(gc, 0.4 * glow), blur=hr * 0.5))
    cv.drawRRect(body, P(shader=lg(x - bw / 2, foot - bh, x + bw / 2, foot, [col('#4A4E7A'), col('#22243A'), col('#14152A')], [0, 0.5, 1])))
    pb = skia.Path(); pb.addRRect(body); cv.save(); cv.clipPath(pb, skia.ClipOp.kIntersect, True)
    cv.drawOval(skia.Rect(x - bw * 0.42, foot - bh * 0.95, x - bw * 0.05, foot - bh * 0.45), P(col('#FFFFFF', 0.12), blur=8))
    rp = skia.Path(pb); rp.offset(-bw * 0.08, 0); cv.drawPath(rp, P(col(gc if glow > 0 else ACC_L, 0.5), stroke=bw * 0.08, blur=bw * 0.05))
    cv.restore()
    cv.drawRRect(body, P(col(ACC_L, 0.55), stroke=2.5))
    cv.drawCircle(hx, hy, hr, P(shader=rg(hx - hr * 0.35, hy - hr * 0.4, hr * 1.6, [col('#6A6E9E'), col('#33365A'), col('#1A1B30')], [0, 0.55, 1])))
    cv.drawOval(skia.Rect(hx - hr * 0.6, hy - hr * 0.85, hx - hr * 0.05, hy - hr * 0.45), P(col('#FFFFFF', 0.22), blur=hr * 0.1))
    cv.drawCircle(hx, hy, hr, P(col(ACC_L, 0.6), stroke=2.5))
    ink = P(col(ACC_XL), stroke=max(3, hr * 0.08))
    ey = hy - hr * 0.05
    for s in (-1, 1):
        ex = hx + s * hr * 0.36
        if mood == 'excited':
            e = skia.Path(); e.moveTo(ex - hr * 0.14, ey + hr * 0.04); e.quadTo(ex, ey - hr * 0.16, ex + hr * 0.14, ey + hr * 0.04); cv.drawPath(e, ink)
        elif mood == 'calm':
            e = skia.Path(); e.moveTo(ex - hr * 0.13, ey); e.quadTo(ex, ey + hr * 0.1, ex + hr * 0.13, ey); cv.drawPath(e, ink)
        else:
            bk = blink_at(t, 0.2 + s * 0.05); eh = hr * 0.17 * (1 - 0.9 * bk)
            cv.drawOval(skia.Rect(ex - hr * 0.13, ey - eh, ex + hr * 0.13, ey + eh), P(col(ACC_XL)))
            if mood == 'worried': cv.drawLine(ex - s * hr * 0.17, ey - hr * 0.36, ex + s * hr * 0.12, ey - hr * 0.27, ink)
    my = hy + hr * 0.42; m = skia.Path()
    if mood == 'excited':
        mo = hr * (0.16 + 0.14 * mouth_open)
        m.moveTo(hx - hr * 0.32, my - hr * 0.06); m.quadTo(hx, my + mo * 2.2, hx + hr * 0.32, my - hr * 0.06); m.close()
        cv.drawPath(m, P(col(ACC_XL))); cv.drawPath(m, ink)
        for s in (-1, 1): cv.drawOval(skia.Rect(hx + s * hr * 0.62 - hr * 0.14, my - hr * 0.22, hx + s * hr * 0.62 + hr * 0.14, my - hr * 0.08), P(col('#FF8FA8', 0.55), blur=3))
    elif mood in ('happy', 'calm'):
        m.moveTo(hx - hr * 0.26, my - hr * 0.04); m.quadTo(hx, my + hr * 0.2, hx + hr * 0.26, my - hr * 0.04); cv.drawPath(m, ink)
    elif mood == 'worried':
        m.moveTo(hx - hr * 0.24, my + hr * 0.04)
        for k in range(1, 7): m.lineTo(hx - hr * 0.24 + k * hr * 0.08, my + (hr * 0.05 if k % 2 else -hr * 0.03))
        cv.drawPath(m, ink)
    else:
        m.moveTo(hx - hr * 0.18, my); m.lineTo(hx + hr * 0.18, my); cv.drawPath(m, ink)
    if sweat > 0:
        for k, (dx, ph) in enumerate(((0.95, 0.0), (-1.0, 0.5))):
            u = ((t * 0.9 + ph) % 1.0) * sweat
            sx, sy = hx + dx * hr, hy - hr * 0.35 + u * hr * 0.6
            d = skia.Path(); d.moveTo(sx, sy - hr * 0.26); d.quadTo(sx + hr * 0.15, sy, sx, sy + hr * 0.1); d.quadTo(sx - hr * 0.15, sy, sx, sy - hr * 0.26); d.close()
            cv.drawPath(d, P(col('#8FD3FF', min(1, sweat * 1.5) * (1 - u * 0.5))))
    if a < 1: cv.restore()
    return hx, hy, hr

def stage(cv, a, t, warm=0.0, cx=540, floor_y=1080, cone_w=260):
    """panggung: tirai beludru, lantai mengilap, lampu sorot volumetrik (warm 0..1 jadi keemasan)"""
    if a <= 0: return
    for sd in (-1, 1):
        cur = skia.Path(); x0 = 0 if sd < 0 else W; x1 = 170 if sd < 0 else W - 170
        cur.moveTo(x0, 250); cur.lineTo(x1, 250)
        for i in range(9):
            y = 250 + i * 110; cur.quadTo(x1 + sd * -18 * math.sin(i * 1.3 + t * 0.6), y + 55, x1 + sd * (6 * math.sin(i * 1.7)), y + 110)
        cur.lineTo(x0, 1250); cur.close()
        cv.drawPath(cur, P(shader=lg(x0, 0, x1, 0, [col('#2A0F3A', a), col('#4A1E66', a), col('#2A0F3A', a)], [0, 0.6, 1])))
        for k in range(4):
            fx = x0 + (x1 - x0) * (0.2 + k * 0.22); cv.drawLine(fx, 250, fx + sd * 6, 1250, P(col('#000000', 0.25 * a), stroke=10, blur=6))
    fl = skia.Path(); fl.moveTo(0, floor_y - 40); fl.lineTo(W, floor_y - 40); fl.lineTo(W, 1250); fl.lineTo(0, 1250); fl.close()
    cv.drawPath(fl, P(shader=lg(0, floor_y - 40, 0, 1250, [col('#1E1A3A', a), col('#0B0A16', a)])))
    for k in range(7):
        y = floor_y - 40 + k * k * 6; cv.drawLine(0, y, W, y, P(col('#AEB6FF', 0.05 * a), stroke=1.5))
    lc = mixc('#DDE0FF', GOLD, warm)
    cone = skia.Path(); cone.moveTo(cx - 40, 250); cone.lineTo(cx + 40, 250); cone.lineTo(cx + cone_w, floor_y); cone.lineTo(cx - cone_w, floor_y); cone.close()
    cv.drawPath(cone, P(shader=lg(0, 250, 0, floor_y, [col(lc, (0.26 + 0.1 * warm) * a), col(lc, 0.07 * a)])))
    cv.drawOval(skia.Rect(cx - cone_w - 30, floor_y - 34, cx + cone_w + 30, floor_y + 34), P(shader=rg(cx, floor_y, cone_w + 30, [col(lc, 0.35 * a), col(lc, 0)])))

def ecg_path(x0, x1, y, amp, t, rate=1.6, phase=0.0):
    """garis detak jantung yang berjalan"""
    p = skia.Path(); n = 120
    for i in range(n + 1):
        u = i / n; x = lerp(x0, x1, u); ph = (u * 3 - t * rate + phase) % 1.0
        v = 0.0
        if 0.40 < ph < 0.44: v = -0.25
        elif 0.44 < ph < 0.48: v = 1.0
        elif 0.48 < ph < 0.53: v = -0.55
        elif 0.60 < ph < 0.72: v = 0.18 * math.sin((ph - 0.6) / 0.12 * math.pi)
        (p.moveTo if i == 0 else p.lineTo)(x, y - v * amp)
    return p

def heart_big(cv, cx, cy, s, a, t, rate=2.2, c=CORAL):
    if a <= 0: return
    pu = 1 + 0.12 * beat_pulse(t * rate)
    hp = heart_path(cx, cy, s * pu)
    cv.drawPath(hp, P(col(c, 0.55 * a), blur=s * 0.35))
    cv.drawPath(hp, P(shader=rg(cx - s * 0.3, cy - s * 0.4, s * 1.6, [col(mixc(c, '#FFFFFF', 0.45), a), col(c, a), col(mixc(c, '#000000', 0.45), a)], [0, 0.5, 1])))
    cv.drawOval(skia.Rect(cx - s * 0.75, cy - s * 0.65, cx - s * 0.25, cy - s * 0.3), P(col('#FFFFFF', 0.3 * a), blur=s * 0.08))

def say(cv, text, cx, cy, size, a, c, fill, fg, tail, sc=1.0, glow=0.6, strike=0.0):
    """gelembung ucapan kaca + coretan"""
    if a <= 0: return
    f = font(XB, size); w = f.measureText(text) + size * 1.6; h = size * 2.0
    cv.save(); cv.translate(cx, cy); cv.scale(sc, sc)
    pth, r = bubble_path(0, 0, w, h, ((tail[0] - cx) / sc, (tail[1] - cy) / sc), maxlen=size * 1.4)
    draw_bubble(cv, pth, r, a, glow, fill, c, c)
    cv.drawString(text, -f.measureText(text) / 2, bl(f, 0), f, P(col(fg, a)))
    if strike > 0:
        x0 = -w / 2 + 14; cv.drawLine(x0, 4, x0 + (w - 28) * eo(strike), -4, P(col(CORAL, 0.6 * a), stroke=18, blur=8)); cv.drawLine(x0, 4, x0 + (w - 28) * eo(strike), -4, P(col('#FFFFFF', a), stroke=7))
    cv.restore()

def mic_stand(cv, x, foot, top, a, glow=0.0):
    if a <= 0: return
    cv.drawLine(x, foot, x, top + 40, P(col('#8A8EAE', a), stroke=7)); cv.drawOval(skia.Rect(x - 50, foot - 8, x + 50, foot + 8), P(col('#5A5E7A', a)))
    hd = skia.Rect(x - 20, top - 20, x + 20, top + 44)
    if glow > 0: cv.drawRoundRect(hd, 20, 20, P(col(GOLD, 0.6 * glow * a), blur=16))
    cv.drawRoundRect(hd, 20, 20, P(shader=lg(x - 20, 0, x + 20, 0, [col('#9AA0C8', a), col('#E8EAFF', a), col('#5A5E7A', a)])))
    for k in range(4): cv.drawLine(x - 16, top - 8 + k * 11, x + 16, top - 8 + k * 11, P(col('#3A3D55', 0.6 * a), stroke=2))

def note(cv, x, y, s, a, c=GOLD):
    if a <= 0: return
    cv.drawOval(skia.Rect(x - s * 0.45, y - s * 0.3, x + s * 0.45, y + s * 0.3), P(col(c, a)))
    cv.drawLine(x + s * 0.4, y, x + s * 0.4, y - s * 1.5, P(col(c, a), stroke=s * 0.16)); cv.drawLine(x + s * 0.4, y - s * 1.5, x + s * 0.95, y - s * 1.2, P(col(c, a), stroke=s * 0.16))

def eyes_ring(cv, t, a, love=0.0):
    """mata penonton yang mengawasi di kegelapan (khas EP01/EP03), bisa berubah jadi hati"""
    for k, (x, y, s, ph) in enumerate(((150, 520, 26, 0.0), (960, 640, 28, 0.3), (120, 820, 22, 0.55), (960, 800, 24, 0.15), (220, 1010, 20, 0.7), (860, 1030, 22, 0.4))):
        if love > 0.5: heart_shape(cv, x, y, s * 0.9 * (1 + 0.08 * math.sin(t * 5 + k)), a * prog(love, 0.5, 1.0), HOTPINK)
        elif love < 0.5: b.watcher_eye(cv, x, y, s, 540, 760, t, ph, a * (1 - love * 2))

def podium(cv, x, foot, w, a):
    if a <= 0: return
    p = skia.Path(); p.moveTo(x - w * 0.5, foot - w * 0.95); p.lineTo(x + w * 0.5, foot - w * 0.95); p.lineTo(x + w * 0.38, foot); p.lineTo(x - w * 0.38, foot); p.close()
    cv.drawPath(p, P(shader=lg(0, foot - w, 0, foot, [col('#5A5F9E', a), col('#22243A', a)]))); cv.drawPath(p, P(col(ACC_L, 0.5 * a), stroke=2.5))
    cv.drawRoundRect(skia.Rect(x - w * 0.6, foot - w * 1.02, x + w * 0.6, foot - w * 0.9), 8, 8, P(col('#7F84C8', a)))

# ------------------------------------------------------------ helper EP14: kafe malam + dua tokoh kapsul ngobrol, meter nyambung
GOLD = '#FFC56B'; HOTPINK = '#FF7FC8'; WARM = '#FFC98A'
def cafe_bg(cv, a, t):
    """latar kafe malam: lampu gantung hangat + jendela kota buram (tanpa titik/bokeh)"""
    if a <= 0: return
    for k, x in enumerate((300, 780)):
        cv.drawLine(x, 255, x, 330, P(col('#3A3D55', a), stroke=4))
        sh = skia.Path(); sh.moveTo(x - 60, 380); sh.lineTo(x - 24, 330); sh.lineTo(x + 24, 330); sh.lineTo(x + 60, 380); sh.close()
        cv.drawPath(sh, P(shader=lg(0, 330, 0, 380, [col('#5A4A3A', a), col('#2A221A', a)])))
        cv.drawOval(skia.Rect(x - 60, 372, x + 60, 388), P(col(WARM, 0.9 * a)))
        cone = skia.Path(); cone.moveTo(x - 58, 382); cone.lineTo(x + 58, 382); cone.lineTo(x + 260, 1000); cone.lineTo(x - 260, 1000); cone.close()
        cv.drawPath(cone, P(shader=lg(0, 382, 0, 1000, [col(WARM, 0.16 * a), col(WARM, 0)])))
    for k in range(6):
        x = 60 + k * 190; h = 120 + 60 * ((k * 37) % 5)
        cv.drawRect(skia.Rect(x, 1010 - h, x + 120, 1010), P(col('#1A1C34', 0.6 * a)))
        for j in range(3):
            cv.drawRect(skia.Rect(x + 20, 1010 - h + 20 + j * 34, x + 50, 1010 - h + 36 + j * 34), P(col(WARM, 0.18 * a)))

def table(cv, cx, y, w, a, t, cups=True, legs=True):
    if a <= 0: return
    cv.drawOval(skia.Rect(cx - w / 2, y - 26, cx + w / 2, y + 26), P(shader=lg(0, y - 26, 0, y + 26, [col('#7A5A40', a), col('#4A3424', a)])))
    if legs:
        cv.drawRect(skia.Rect(cx - 14, y + 10, cx + 14, y + 150), P(col('#2A221A', a)))
        cv.drawOval(skia.Rect(cx - 80, y + 140, cx + 80, y + 162), P(col('#2A221A', a)))
    if cups:
        for sd in (-1, 1):
            x = cx + sd * w * 0.25
            cv.drawRoundRect(skia.Rect(x - 26, y - 62, x + 26, y - 10), 10, 10, P(shader=lg(x - 26, 0, x + 26, 0, [col('#F2F0F8', a), col('#C9CBE0', a)])))
            hd = skia.Path(); hd.addArc(skia.Rect(x + 16, y - 52, x + 44, y - 24), -90, 180); cv.drawPath(hd, P(col('#C9CBE0', a), stroke=5))
            for k in range(2):
                u = ((t * 0.7 + k * 0.5 + sd * 0.25) % 1.0); sp = skia.Path(); sp.moveTo(x - 6 + k * 12, y - 66)
                for i in range(1, 5): sp.lineTo(x - 6 + k * 12 + 6 * math.sin(i + t * 3 + k), y - 66 - i * 14 * (0.5 + u))
                cv.drawPath(sp, P(col('#F0EFF6', 0.35 * (1 - u) * a), stroke=4, blur=3))

def conn_meter(cv, x0, x1, y, v, a, t, label='NYAMBUNG'):
    """meter keterhubungan antara dua orang (0..1) dengan hati di ujung"""
    if a <= 0: return
    cv.drawRoundRect(skia.Rect(x0, y - 13, x1, y + 13), 13, 13, P(col('#1A1B30', 0.9 * a))); cv.drawRoundRect(skia.Rect(x0, y - 13, x1, y + 13), 13, 13, P(col(ACC_XL, 0.35 * a), stroke=2))
    xv = x0 + (x1 - x0) * clamp(v)
    if xv > x0 + 20:
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 9, xv, y + 9), 9, 9, P(col(HOTPINK, 0.5 * a), blur=10))
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 9, xv, y + 9), 9, 9, P(shader=lg(x0, 0, x1, 0, [col('#8C93FF', a), col(HOTPINK, a)])))
    heart_shape(cv, xv, y, 18 * (1 + 0.15 * v * math.sin(t * 6)), a, HOTPINK)
    mono(cv, label, (x0 + x1) / 2, y - 36, 22, ACC_L, 0.85 * a, sp=4)

def chat_panel(cv, cx, cy, w, h, msgs, a, t, t0, step=0.32, qc=GOLD):
    """panel obrolan kaca: msgs = [(sisi 'L'/'R', teks, pertanyaan?)], muncul bertahap"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); glass(cv, r, rad=30, a=a, glow=0.2)
    f = font(B, 24); y = r.top() + 50
    for k, (side, txt, q) in enumerate(msgs):
        pa = prog(t, t0 + k * step, t0 + k * step + 0.2)
        if pa <= 0: break
        tw = f.measureText(txt) + 40; bh = 50
        x = r.left() + 24 if side == 'L' else r.right() - 24 - tw
        br = skia.Rect(x, y - bh / 2, x + tw, y + bh / 2)
        c = qc if q else ('#3A3D66' if side == 'L' else '#2A2C48')
        cv.drawRoundRect(br, 22, 22, P(col(c, (0.95 if not q else 0.9) * a * clamp(pa * 2))))
        if q: cv.drawRoundRect(br, 22, 22, P(col(qc, 0.5 * a * pa), stroke=8, blur=8))
        cv.drawString(txt, br.left() + 20, bl(f, y), f, P(col(INK if q else TXT, a * clamp(pa * 2))))
        y += bh + 14

def ear(cv, cx, cy, s, a, c=MINT):
    if a <= 0: return
    p = skia.Path(); p.moveTo(cx - s * 0.2, cy + s * 0.9)
    p.cubicTo(cx - s * 0.9, cy + s * 0.6, cx - s * 0.9, cy - s * 0.9, cx, cy - s * 0.9)
    p.cubicTo(cx + s * 0.8, cy - s * 0.9, cx + s * 0.9, cy - s * 0.1, cx + s * 0.4, cy + s * 0.3)
    p.cubicTo(cx + s * 0.1, cy + s * 0.55, cx + s * 0.2, cy + s * 0.9, cx - s * 0.2, cy + s * 0.9)
    cv.drawPath(p, P(col(c, 0.45 * a), blur=s * 0.25)); cv.drawPath(p, P(shader=lg(cx, cy - s, cx, cy + s, [col(mixc(c, '#FFFFFF', 0.4), a), col(c, a)])))
    inner = skia.Path(); inner.moveTo(cx - s * 0.25, cy + s * 0.2); inner.cubicTo(cx - s * 0.5, cy - s * 0.4, cx + s * 0.4, cy - s * 0.6, cx + s * 0.25, cy - s * 0.05)
    cv.drawPath(inner, P(col('#0D2019', 0.6 * a), stroke=s * 0.1))
    for k in range(3):
        arc = skia.Path(); rr = s * (1.2 + 0.35 * k); arc.addArc(skia.Rect(cx - rr - s * 0.3, cy - rr, cx + rr - s * 0.3, cy + rr), 150, 60)
        cv.drawPath(arc, P(col(c, (0.6 - 0.15 * k) * a), stroke=4))

def two_chat(cv, t, a, lx=300, rx=780, foot=1000, h=330, lmood='neutral', rmood='happy', lglow=0.0, rglow=0.0, lc=GOLD, rc=HOTPINK, ltrem=0.0):
    hero(cv, lx, foot, h, lmood, a, t, glow=lglow, gc=lc, tremble=ltrem, mouth_open=0.4)
    hero(cv, rx, foot, h, rmood, a, t, glow=rglow, gc=rc, mouth_open=0.4 + 0.4 * math.sin(t * 5))

# ------------------------------------------------------------ helper EP15: ponsel chat + dua tokoh kapsul berjauhan
CHATB = '#5B5FE0'
def typed_at(t, seq):
    """isi kolom ketik: seq = [(t0, teks, lama ketik, tahan, lama hapus atau None)]"""
    s = ''
    for t0, txt, dt, hold, dd in seq:
        if t < t0: break
        s = txt[:int(round(len(txt) * prog(t, t0, t0 + dt)))]
        if dd is not None and t > t0 + dt + hold:
            s = txt[:int(round(len(txt) * (1 - prog(t, t0 + dt + hold, t0 + dt + hold + dd))))]
    return s

def ticks(cv, x, y, s, a, c='#7FE0FF'):
    if a <= 0: return
    for k in range(2):
        p = skia.Path(); x0 = x + k * s * 0.45
        p.moveTo(x0, y); p.lineTo(x0 + s * 0.3, y + s * 0.3); p.lineTo(x0 + s * 0.85, y - s * 0.35)
        cv.drawPath(p, P(col(c, a), stroke=s * 0.16))

def msg_bubble(cv, x, y, text, size, a, side='R', fill=CHATB, fg='#FFFFFF', glow=0.0, gc=None, tick=0.0):
    """gelembung chat: x = tepi kanan ('R') / kiri ('L'), y = tengah"""
    if a <= 0: return None
    f = font(B, size); tw = f.measureText(text); pw, ph = size * 0.75, size * 0.6
    w = tw + 2 * pw + (size * 1.25 if tick > 0 else 0); h = size + 2 * ph
    r = skia.Rect(x - w, y - h / 2, x, y + h / 2) if side == 'R' else skia.Rect(x, y - h / 2, x + w, y + h / 2)
    if glow > 0: cv.drawRoundRect(r, h * 0.42, h * 0.42, P(col(gc or fill, 0.6 * glow * a), blur=20))
    cv.drawRoundRect(r, h * 0.42, h * 0.42, P(shader=lg(0, r.top(), 0, r.bottom(), [col(mixc(fill, '#FFFFFF', 0.12), a), col(fill, a)])))
    cv.drawString(text, r.left() + pw, bl(f, y), f, P(col(fg, a)))
    if tick > 0: ticks(cv, r.right() - pw - size * 0.9, y + size * 0.08, size * 0.6, a * tick)
    return r

def chat_phone(cv, cx, cy, w, h, a, t, typed='', hist=(), name='Dimas', status='terakhir chat 3 tahun lalu', caret=True,
               mystery=0.0, sent=None, sent_u=0.0, tick=0.0, reply=None, reply_u=0.0, send_glow=0.0, dim=0.0, gap=None):
    """ponsel kaca dengan layar chat (pusat cx,cy): riwayat lama yang redup, kolom ketik + kursor, tombol kirim,
    gelembung rahasia emas (mystery), pesan terkirim yang naik (sent_u) + centang biru, balasan yang muncul (reply_u)"""
    if a <= 0: return
    cv.save(); cv.translate(cx, cy)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2); rad = w * 0.14
    cv.drawRRect(RR(r.makeOffset(0, 36), rad), P(col('#000000', 0.6 * a), blur=46))
    cv.drawRRect(RR(r, rad), P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col('#6A6E8E', a), col('#1A1B2A', a), col('#4A4D68', a), col('#15161F', a)], [0, 0.35, 0.7, 1])))
    sr = r.makeInset(w * 0.035, w * 0.035); srad = rad * 0.8
    cv.drawRRect(RR(sr, srad), P(col('#04050A', a)))
    cv.save(); cv.clipRRect(RR(sr, srad), skia.ClipOp.kIntersect, True)
    cv.drawRect(sr, P(shader=lg(0, sr.top(), 0, sr.bottom(), [col('#1C1A48', a), col('#100F2A', a), col('#0A0A18', a)], [0, 0.5, 1])))
    cv.drawCircle(sr.right() - w * 0.1, sr.bottom() - h * 0.25, w * 0.8, P(shader=rg(sr.right() - w * 0.1, sr.bottom() - h * 0.25, w * 0.8, [col('#3F4BFF', 0.22 * a), col('#3F4BFF', 0)])))
    # header
    hh = h * 0.115; hy = sr.top() + w * 0.07 + hh / 2
    cv.drawRect(skia.Rect(sr.left(), sr.top(), sr.right(), hy + hh / 2), P(col('#1E1F3C', 0.95 * a)))
    cv.drawLine(sr.left(), hy + hh / 2, sr.right(), hy + hh / 2, P(col(ACC_L, 0.15 * a), stroke=2))
    av = hh * 0.34; ax = sr.left() + w * 0.13
    f = font(XB, w * 0.06); cv.drawString('<', sr.left() + w * 0.03, bl(f, hy), f, P(col(ACC_L, a)))
    cv.drawCircle(ax, hy, av, P(shader=lg(0, hy - av, 0, hy + av, [col('#FFC56B', a), col('#FF8A7A', a)])))
    fa = font(XB, av * 1.0); cv.drawString(name[0], ax - fa.measureText(name[0]) / 2, bl(fa, hy), fa, P(col(INK, a)))
    f1 = font(XB, w * 0.07); f2 = font(M, w * 0.042)
    cv.drawString(name, ax + av * 1.5, bl(f1, hy - hh * 0.14), f1, P(col(TXT, a)))
    cv.drawString(status, ax + av * 1.5, bl(f2, hy + hh * 0.22), f2, P(col(MUTED, a)))
    # riwayat lama
    y = hy + hh / 2 + h * 0.06; fs = w * 0.055
    if hist:
        f3 = font(B, w * 0.038); ds = '12 MAR 2023'; dw = f3.measureText(ds) + 30
        cv.drawRoundRect(skia.Rect(-dw / 2, y - 18, dw / 2, y + 18), 18, 18, P(col('#2A2C48', 0.9 * a)))
        cv.drawString(ds, -dw / 2 + 15, bl(f3, y), f3, P(col(MUTED, a))); y += h * 0.075
        for side, txt in hist:
            msg_bubble(cv, sr.right() - w * 0.05 if side == 'R' else sr.left() + w * 0.05, y, txt, fs, 0.55 * a, side, CHATB if side == 'R' else '#34365A')
            y += fs * 2.5
    y_hist = y
    # kolom ketik
    iy = sr.bottom() - h * 0.07; ih = h * 0.07; ir = skia.Rect(sr.left() + w * 0.04, iy - ih / 2, sr.right() - w * 0.2, iy + ih / 2)
    cv.drawRoundRect(ir, ih / 2, ih / 2, P(col('#24264A', a))); cv.drawRoundRect(ir, ih / 2, ih / 2, P(col(ACC_L, 0.25 * a), stroke=2))
    fi = font(B, w * 0.055)
    if typed:
        tw = fi.measureText(typed); tx = min(ir.left() + ih * 0.45, ir.right() - ih * 0.45 - tw)
        cv.save(); cv.clipRect(ir.makeInset(ih * 0.3, 0)); cv.drawString(typed, tx, bl(fi, iy), fi, P(col(TXT, a))); cv.restore()
        cx_ = tx + tw + 4
    else:
        cv.drawString('Ketik pesan', ir.left() + ih * 0.45, bl(fi, iy), fi, P(col(MUTED, 0.6 * a))); cx_ = ir.left() + ih * 0.45 - 4
    if caret and (t * 2.2) % 1.0 < 0.55: cv.drawLine(cx_, iy - ih * 0.28, cx_, iy + ih * 0.28, P(col(ACC_XL, a), stroke=3))
    bx = sr.right() - w * 0.11; br_ = ih * 0.55
    if send_glow > 0:
        cv.drawCircle(bx, iy, br_ * (1.3 + 0.5 * send_glow), P(col(GOLD, 0.5 * send_glow * a), blur=14))
    cv.drawCircle(bx, iy, br_, P(shader=lg(0, iy - br_, 0, iy + br_, [col(mixc(ACC, '#FFFFFF', 0.3) if send_glow <= 0 else GOLD, a), col(ACC if send_glow <= 0 else '#E09A3A', a)])))
    ar = skia.Path(); ar.moveTo(bx - br_ * 0.42, iy - br_ * 0.38); ar.lineTo(bx + br_ * 0.48, iy); ar.lineTo(bx - br_ * 0.42, iy + br_ * 0.38); ar.lineTo(bx - br_ * 0.22, iy); ar.close()
    cv.drawPath(ar, P(col('#FFFFFF', a)))
    slot = iy - ih - h * 0.12
    if gap and hist:
        gy = (y_hist + slot) / 2 - h * 0.04; fg_ = font(XB, w * 0.04); gw = fg_.measureText(gap) + 44
        cv.drawLine(sr.left() + w * 0.06, gy, -gw / 2 - 10, gy, P(col(CORAL, 0.35 * a), stroke=2)); cv.drawLine(gw / 2 + 10, gy, sr.right() - w * 0.06, gy, P(col(CORAL, 0.35 * a), stroke=2))
        cv.drawRoundRect(skia.Rect(-gw / 2, gy - 22, gw / 2, gy + 22), 22, 22, P(col('#2A1420', 0.95 * a))); cv.drawRoundRect(skia.Rect(-gw / 2, gy - 22, gw / 2, gy + 22), 22, 22, P(col(CORAL, 0.6 * a), stroke=2))
        cv.drawString(gap, -gw / 2 + 22, bl(fg_, gy), fg_, P(col('#FFD9D2', a)))
    if mystery > 0:
        my = slot + 10 * math.sin(t * 3); sc = lerp(0.6, 1.0, bo(clamp(mystery * 1.4)))
        cv.save(); cv.translate(sr.right() - w * 0.05, my); cv.scale(sc, sc)
        rr = msg_bubble(cv, 0, 0, '                ', fs * 1.5, a * clamp(mystery * 2), 'R', '#5A4012', '#FFC56B', glow=1.2, gc=GOLD)
        if rr:
            f4 = font(XB, fs * 1.6); s4 = '? ? ?'; cv.drawString(s4, rr.centerX() - f4.measureText(s4) / 2, bl(f4, 0), f4, P(col('#FFE3B0', a * clamp(mystery * 2))))
        cv.restore()
    if sent and sent_u > 0:
        y0 = lerp(iy, slot - fs * 2.2, eo(sent_u)); sc = lerp(0.85, 1.0, eo(sent_u))
        cv.save(); cv.translate(sr.right() - w * 0.05, y0); cv.scale(sc, sc)
        msg_bubble(cv, 0, 0, sent, fs * 0.92, a * clamp(sent_u * 3), 'R', CHATB, glow=0.6 * (1 - sent_u) + 0.3, gc=ACC, tick=max(0.4, tick))
        cv.restore()
    if reply and reply_u > 0:
        ry_ = slot + fs * 0.4; sc = lerp(0.5, 1.0, bo(reply_u))
        cv.save(); cv.translate(sr.left() + w * 0.05, ry_); cv.scale(sc, sc)
        msg_bubble(cv, 0, 0, reply, fs * 1.15, a * clamp(reply_u * 3), 'L', '#3A2A66', glow=0.9, gc=HOTPINK)
        cv.restore()
    if dim > 0: cv.drawRect(sr, P(col('#05050C', 0.55 * dim * a)))
    cv.drawRect(sr, P(shader=lg(sr.left(), sr.top(), sr.right(), sr.bottom(), [col('#FFFFFF', 0.08 * a), col('#FFFFFF', 0), col('#FFFFFF', 0)], [0, 0.4, 1])))
    cv.restore()
    cv.drawRoundRect(skia.Rect(-w * 0.12, -h / 2 + w * 0.06, w * 0.12, -h / 2 + w * 0.13), w * 0.035, w * 0.035, P(col('#000000', a)))
    cv.drawRRect(RR(r, rad), P(col('#FFFFFF', 0.28 * a), stroke=2.5))
    cv.restore()

def window(cv, r, a, t, label, c=ACC_L, warm=0.0):
    """jendela kaca kecil berisi 'dunia' seseorang: langit malam + siluet kota"""
    if a <= 0: return
    glass(cv, r, rad=34, a=a, glow=0.25, gc=c)
    cv.save(); pr = skia.Path(); pr.addRRect(RR(r.makeInset(8, 8), 28)); cv.clipPath(pr, skia.ClipOp.kIntersect, True)
    cv.drawRect(r, P(shader=lg(0, r.top(), 0, r.bottom(), [col(mixc('#1A1850', '#3A2A20', warm), 0.9 * a), col('#0A0A1A', 0.9 * a)])))
    cv.drawCircle(r.right() - 70, r.top() + 70, 26, P(col('#E8E6FF', 0.85 * a))); cv.drawCircle(r.right() - 70, r.top() + 70, 60, P(col('#AEB6FF', 0.25 * a), blur=20))
    for k in range(6):
        x = r.left() + k * (r.width() / 5.5); hh = 70 + 50 * ((k * 53 + int(r.left())) % 4)
        cv.drawRect(skia.Rect(x, r.bottom() - hh, x + r.width() / 7, r.bottom()), P(col('#1E2040', 0.95 * a)))
        cv.drawRect(skia.Rect(x + 12, r.bottom() - hh + 18, x + 26, r.bottom() - hh + 30), P(col(WARM, 0.3 * a)))
    cv.restore()
    mono(cv, label, r.centerX(), r.top() - 30, 24, c, a, sp=4, glow=0.4)

def meter(cv, x0, x1, y, v, a, label, c):
    if a <= 0: return
    mono(cv, label, x0, y - 34, 22, c, 0.9 * a, sp=3, align=0)
    cv.drawRoundRect(skia.Rect(x0, y - 14, x1, y + 14), 14, 14, P(col('#1A1B30', 0.95 * a))); cv.drawRoundRect(skia.Rect(x0, y - 14, x1, y + 14), 14, 14, P(col(c, 0.35 * a), stroke=2))
    xv = x0 + (x1 - x0) * clamp(v)
    if xv > x0 + 24:
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 10, xv - 4, y + 10), 10, 10, P(col(c, 0.5 * a), blur=12))
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 10, xv - 4, y + 10), 10, 10, P(shader=lg(x0, 0, x1, 0, [col(mixc(c, '#FFFFFF', 0.4), a), col(c, a)])))

def burst(cv, cx, cy, s, a, t, c=GOLD, txt='!'):
    """seruan kaget: tanda seru tebal + garis-garis kejut"""
    if a <= 0: return
    for k in range(10):
        ang = k * math.tau / 10 + 0.2; r0, r1 = s * 0.75, s * (1.05 + 0.12 * math.sin(t * 12 + k))
        cv.drawLine(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0, cx + math.cos(ang) * r1, cy + math.sin(ang) * r1, P(col(c, 0.85 * a), stroke=s * 0.07))
    f = font(XB, s * 1.1); w = f.measureText(txt)
    cv.drawString(txt, cx - w / 2, bl(f, cy), f, P(col(c, 0.6 * a), blur=s * 0.12)); cv.drawString(txt, cx - w / 2, bl(f, cy), f, P(col('#FFF1D6', a)))

SHARDS = None
def glass_wall(cv, r, a, t, crack_u=0.0, shatter=0.0, label='GENGSI'):
    """dinding kaca vertikal berlabel; retak (crack_u) lalu pecah berhamburan (shatter 0..1)"""
    global SHARDS
    if a <= 0: return
    if shatter <= 0:
        cv.drawRoundRect(r, 26, 26, P(col('#9FB0FF', 0.35 * a), blur=24))
        cv.drawRoundRect(r, 26, 26, P(shader=lg(r.left(), 0, r.right(), 0, [col('#B9C2FF', 0.28 * a), col('#6A74D8', 0.16 * a), col('#B9C2FF', 0.3 * a)])))
        cv.drawRoundRect(r, 26, 26, P(col('#DDE2FF', 0.75 * a), stroke=3))
        cv.drawLine(r.left() + 26, r.top() + 40, r.left() + 26, r.bottom() - 120, P(col('#FFFFFF', 0.35 * a), stroke=6, blur=3))
        f = font(XB, 44)
        for k, ch in enumerate(label):
            cv.drawString(ch, r.centerX() - f.measureText(ch) / 2, bl(f, r.top() + 110 + k * 66), f, P(col('#FFFFFF', 0.92 * a)))
        crack(cv, r.centerX() + 6, r.centerY() + 40, r.width() * 1.3, crack_u, a, seed=5)
        return
    if SHARDS is None:
        rnd = random.Random(11); SHARDS = []
        for k in range(26):
            x = rnd.uniform(r.left(), r.right()); y = rnd.uniform(r.top(), r.bottom()); s = rnd.uniform(18, 46)
            SHARDS.append((x, y, s, rnd.uniform(-1, 1), rnd.uniform(-1.4, 0.2), rnd.uniform(-300, 300), rnd.random() * math.tau))
    u = eo(shatter)
    for x, y, s, vx, vy, spin, ph in SHARDS:
        px = x + vx * 520 * u; py = y + vy * 380 * u + 700 * u * u; aa = a * (1 - shatter)
        if aa <= 0: continue
        cv.save(); cv.translate(px, py); cv.rotate(spin * u + ph * 20)
        p = skia.Path(); p.moveTo(0, -s); p.lineTo(s * 0.8, s * 0.6); p.lineTo(-s * 0.7, s * 0.5); p.close()
        cv.drawPath(p, P(col('#B9C2FF', 0.35 * aa))); cv.drawPath(p, P(col('#FFFFFF', 0.8 * aa), stroke=2))
        cv.restore()

# ------------------------------------------------------------ A: HOOK — keinget teman lama, gengsi chat duluan; "kirim satu chat ini" (0 - 4.38)
HIST = [('L', 'wkwk iya, kabar-kabarin ya'), ('R', 'siap! kapan-kapan main')]
TYPE_A = [(-0.7, 'hai, apa kabar?', 0.8, 0.25, 0.4), (0.95, 'eh, masih inget aku?', 0.75, 0.2, 0.4), (2.4, 'hmm...', 0.3, 0.1, 0.15)]
def gA(cv, t):
    zin = eo(prog(t, 0.0, 0.6)); push = lerp(1.1, 1.0, zin) * (1 + 0.04 * eo(prog(t, 2.96, 3.6)))
    cv.save(); cv.translate(540, 760); cv.scale(push, push); cv.translate(-540, -760)
    mys = prog(t, 2.96, 3.3)
    if mys > 0:
        halo(cv, 660, 700, 520, GOLD, 0.55 * mys); rays(cv, 660, 700, 560, 0.45 * mys, t, n=16, c=GOLD, spin=6)
    worried = t < 2.96
    hero(cv, 205, 1130, 360, 'worried' if worried else 'excited', 1.0, t, sweat=1.0 if worried else 0.0, tremble=0.5 if worried else 0.0,
         glow=0.7 * mys, gc=GOLD, mouth_open=0.3)
    tilt = 4 * math.sin(t * 1.3) - 3
    cv.save(); cv.translate(665, 735); cv.rotate(tilt); cv.translate(-665, -735)
    chat_phone(cv, 665, 735, 450, 880, 1.0, t, typed_at(t, TYPE_A), HIST, mystery=mys, send_glow=mys, gap='3 TAHUN KEMUDIAN')
    cv.restore()
    cv.restore()
    ga = prog(t, 1.94, 2.2)
    if ga > 0:
        cv.save(); cv.translate(215, 560); cv.rotate(-6); sc = lerp(1.6, 1, eo(ga)); cv.scale(sc, sc)
        chip(cv, 'gengsi...', 0, 0, clamp(ga * 3) * (1 - eio(prog(t, 2.85, 3.1))), size=30, fg='#FFD9D2', bgc='#2A1420', edge=CORAL); cv.restore()
    ka = prog(t, 2.96, 3.25)
    if ka > 0:
        cv.save(); cv.translate(215, 560); cv.rotate(-5); sc = lerp(1.7, 1, eo(ka)) * (1 + 0.03 * math.sin(t * 7)); cv.scale(sc, sc)
        chip(cv, '1 chat ini', 0, 0, clamp(ka * 3), size=32, fg=INK, bgc=GOLD, edge=GOLD); cv.restore()
        rp = prog(t, 3.0, 3.7)
        if 0 < rp < 1: cv.drawCircle(665, 735, 300 + 260 * rp, P(col(GOLD, 0.55 * (1 - rp)), stroke=4))

# ------------------------------------------------------------ B: nanti ganggu, nanti dikira aneh, udah kelamaan (4.38 - 8.9)
WORRY = [('nanti ganggu', 250, 470, -7, 5.44), ('nanti dikira aneh', 820, 540, 6, 6.43), ('udah kelamaan', 260, 680, 5, 7.53), ('dia masih inget aku?', 810, 760, -5, 8.0)]
def gB(cv, t):
    a0 = eo(prog(t, 4.38, 4.75))
    hero(cv, 540, 1090, 400, 'worried', a0, t, sweat=1.0, tremble=0.4)
    pa = eo(prog(t, 4.4, 4.9))
    cv.save(); cv.translate(640, 960); cv.rotate(-14 + 3 * math.sin(t * 1.5))
    chat_phone(cv, 0, 0, 150, 290, a0 * pa, t, typed_at(t, [(4.6, 'hai...', 0.5, 0.6, 0.3), (6.6, 'hai', 0.3, 0.5, 0.2)]), (), name='Dimas', status='3 tahun lalu')
    cv.restore()
    for txt, x, y, rot, t0 in WORRY:
        q = prog(t, t0, t0 + 0.25)
        if q > 0:
            cv.save(); cv.translate(x, y + 6 * math.sin(t * 2 + x)); cv.rotate(rot); sc = lerp(1.4, 1, eo(q)); cv.scale(sc, sc)
            chip(cv, txt, 0, 0, a0 * clamp(q * 3), size=29, fg='#FFD9D2', bgc='#2A1420', edge=CORAL); cv.restore()
    ra = eo(prog(t, 5.44, 5.8))
    if ra > 0:
        for k in range(3):
            u = ((t * 0.9 + k / 3) % 1.0); rr = 120 + 160 * u
            cv.drawCircle(540, 760, rr, P(col(CORAL, 0.3 * (1 - u) * ra * a0), stroke=3))
    mono(cv, 'YANG KITA PIKIRIN', 540, 350, 26, CORAL, a0 * eo(prog(t, 4.5, 4.9)), sp=4, glow=0.4)

# ------------------------------------------------------------ C: riset 2022, Peggy Liu, 5.900+ orang (8.9 - 14.82)
def gC(cv, t):
    research_card(cv, t, 8.9, '2022', 'Liu, Rim, Min & Min', 'Journal of Personality and Social Psychology', None, None, 640)
    ca = eo(prog(t, 12.07, 12.4))
    if ca > 0:
        v = int(5900 * eo(prog(t, 12.07, 13.2))); s_ = f'{v:,}'.replace(',', '.') + ('+' if v >= 5900 else '')
        extrude(cv, s_, 540, 1010, 96, ca, depth=10, front=('#FFFFFF', '#C9F3E2'), side='#1E5A48', glow=MINT)
        mono(cv, 'orang ikut diuji', 540, 1100, 26, ACC_L, ca, sp=2)
        for k in range(6):
            x = 540 + (1 if k % 2 else -1) * (250 + 64 * (k // 2)); pa_ = prog(t, 12.1 + k * 0.08, 12.35 + k * 0.08)
            if pa_ > 0: avatar(cv, x, 1000, 24, AV_COL[k % 8], ca * pa_ * 0.7)

# ------------------------------------------------------------ D: menyapa teman yang lama nggak dikontak, lewat pesan singkat (14.82 - 19.73)
def gD(cv, t):
    a0 = eo(prog(t, 14.82, 15.2))
    L = skia.Rect(70, 330, 500, 760); R = skia.Rect(580, 620, 1010, 1060)
    la = eo(prog(t, 14.85, 15.3)); ra = eo(prog(t, 15.05, 15.5))
    window(cv, L, a0 * la, t, 'KAMU'); window(cv, R, a0 * ra, t, 'TEMAN LAMA', HOTPINK, warm=0.4)
    hero(cv, 285, 740, 250, 'neutral', a0 * la, t, mouth_open=0.2)
    got = prog(t, 18.95, 19.2)
    hero(cv, 795, 1040, 250, 'happy' if got > 0.5 else 'neutral', a0 * ra, t, glow=0.6 * got, gc=HOTPINK)
    p_ = skia.Path(); p_.moveTo(400, 560); p_.cubicTo(560, 470, 700, 560, 770, 760)
    neon(cv, p_, eo(prog(t, 15.6, 16.4)) * (1 - eio(prog(t, 19.0, 19.4))), ACC_L, 3, a0 * 0.6, 0.5, ACC)
    ga = eo(prog(t, 16.5, 16.9))
    if ga > 0:
        cv.save(); cv.translate(285, 830); cv.rotate(-3); chip(cv, 'terakhir ngobrol: 3 tahun lalu', 0, 0, a0 * ga, size=24, fg='#D5D7E8', bgc='#22243A', edge=MUTED); cv.restore()
    fl = prog(t, 18.1, 18.95)
    m = skia.PathMeasure(p_, False)
    if 0 < fl < 1:
        comet(cv, p_, eo(fl), GOLD, 10, 12)
        pos = m.getPosTan(m.getLength() * eo(fl)); pt = pos[0]; px, py = (pt.x(), pt.y()) if hasattr(pt, 'x') else pt
        cv.save(); cv.translate(px, py); cv.rotate(-8 + 16 * fl); msg_bubble(cv, 110, 0, 'hai, apa kabar?', 30, a0 * clamp(fl * 6), 'R', CHATB, glow=0.8, gc=GOLD); cv.restore()
    if got > 0:
        notif(cv, 795, 700, 360, 'hai, apa kabar?', a0 * clamp(got * 3) * (1 - eio(prog(t, 19.5, 19.73))), title='Pesan baru', glow=0.6)
        rp = prog(t, 18.95, 19.6)
        if 0 < rp < 1: cv.drawCircle(795, 700, 110 + 180 * rp, P(col(GOLD, 0.6 * (1 - rp)), stroke=4))

# ------------------------------------------------------------ E: yang disapa lebih senang dari yang dikira pengirim (19.73 - 23.85)
def gE(cv, t):
    a0 = eo(prog(t, 19.73, 20.1))
    hap = prog(t, 20.8, 21.1)
    hero(cv, 250, 1080, 300, 'neutral', a0, t, mouth_open=0.2)
    hero(cv, 770, 1080, 390, 'excited' if hap > 0.3 else 'neutral', a0, t, glow=0.9 * hap, gc=HOTPINK, mouth_open=0.6 + 0.3 * math.sin(t * 6))
    if hap > 0:
        cv.save(); cv.translate(735, 540); cv.rotate(3); sc = lerp(1.6, 1, eo(hap)) * (1 + 0.03 * math.sin(t * 7)); cv.scale(sc, sc)
        say(cv, 'EH! apa kabar?! kangen!', 0, 0, 36, a0 * clamp(hap * 3), GOLD, ('#3A2A10', '#1E1608'), '#FFE3B0', (40, 120), 1.0, 1.0); cv.restore()
        mono(cv, 'KENYATAANNYA', 735, 430, 24, GOLD, a0 * clamp(hap * 3), sp=4, glow=0.5)
        for k in range(5):
            u = clamp(prog(t, 20.9, 23.8) * 1.3 - k * 0.15)
            if 0 < u < 1: heart_shape(cv, (640, 680, 860, 900, 940)[k], 900 - 190 * eo(u), 16 + 6 * (k % 2), bump(u) * a0, HOTPINK)
    da = prog(t, 22.25, 22.5)
    if da > 0:
        say(cv, 'oh... hai.', 250, 640, 32, a0 * clamp(da * 3), ACC_L, ('#22243A', '#15162A'), MUTED, (250, 760), lerp(0.6, 1, bo(da)), 0.2)
        mono(cv, 'YANG DIKIRA', 250, 545, 22, '#7FB8FF', a0 * clamp(da * 3), sp=4)

# ------------------------------------------------------------ F: makin nggak disangka, makin kaget, makin senang (23.85 - 27.85)
def gF(cv, t):
    a0 = eo(prog(t, 23.85, 24.2))
    ban = prog(t, 24.3, 24.9); kag = prog(t, 25.81, 26.05)
    hero(cv, 300, 960, 360, 'excited' if kag > 0.2 else 'neutral', a0, t, glow=0.8 * kag, gc=GOLD, mouth_open=1.0 * kag)
    burst(cv, 300, 470, 90, a0 * clamp(kag * 3) * (1 + 0 * t), t)
    cv.save(); cv.translate(770, 600); cv.rotate(6 - 2 * math.sin(t * 1.4))
    phone(cv, 330, 660, a0, t, banner=ban, btext='hai! apa kabar?', btitle='Dimas')
    cv.restore()
    if 0 < ban < 1:
        rp = prog(t, 24.5, 25.2)
        if 0 < rp < 1: cv.drawCircle(770, 560, 150 + 220 * rp, P(col(GOLD, 0.5 * (1 - rp)), stroke=4))
    ma = eo(prog(t, 24.0, 24.4))
    meter(cv, 180, 900, 1050, 0.15 + 0.8 * eo(prog(t, 25.81, 26.6)), a0 * ma, 'KAGET', GOLD)
    meter(cv, 180, 900, 1140, 0.25 + 0.72 * eo(prog(t, 26.8, 27.5)), a0 * ma, 'SENANG', HOTPINK)
    if prog(t, 26.8, 27.0) > 0: heart_shape(cv, 180 + 720 * (0.25 + 0.72 * eo(prog(t, 26.8, 27.5))), 1140, 20 * (1 + 0.15 * math.sin(t * 6)), a0, HOTPINK)

# ------------------------------------------------------------ G: takut ganggu = salah tebak; dinding gengsi pecah (27.85 - 30.96)
def gG(cv, t):
    a0 = eo(prog(t, 27.85, 28.2))
    sh = prog(t, 29.71, 30.5); free = sh > 0
    hero(cv, 240, 1080, 320, 'excited' if free else 'worried', a0, t, sweat=0.0 if free else 0.6, glow=0.6 * eo(sh), gc=GOLD, mouth_open=0.4)
    hero(cv, 840, 1080, 320, 'happy' if free else 'neutral', a0, t, glow=0.6 * eo(sh), gc=HOTPINK)
    glass_wall(cv, skia.Rect(470, 380, 610, 1080), a0, t, crack_u=prog(t, 28.6, 29.6), shatter=sh, label='GENGSI')
    ta = eo(prog(t, 28.0, 28.4)) * (1 - eio(prog(t, 29.6, 29.8)))
    if ta > 0:
        cv.save(); cv.translate(540, 330); chip(cv, 'takut ganggu', 0, 0, a0 * ta, size=30, fg='#FFD9D2', bgc='#2A1420', edge=CORAL); cv.restore()
    stamp(cv, 'SALAH TEBAK', 540, 560, 64, t, 29.75, c=GOLD, rot=-7, a=a0)
    if free:
        p_ = skia.Path(); p_.moveTo(330, 760); p_.cubicTo(450, 680, 630, 680, 750, 760)
        neon(cv, p_, eo(prog(t, 30.0, 30.6)), HOTPINK, 5, a0, 1.0, HOTPINK)
        for k in range(4):
            u = clamp(prog(t, 30.1, 30.96) * 1.3 - k * 0.15)
            if 0 < u < 1: heart_shape(cv, 470 + k * 45, 740 - 160 * eo(u), 15, bump(u) * a0, HOTPINK)

# ------------------------------------------------------------ H: kirim aja "hai, tiba-tiba keinget kamu"; tulis inisial di komentar (30.96 - 36.6)
CMTS = [('inisial R', 250, 420, 34.89), ('D, udah 3 tahun', 840, 500, 35.12), ('A. aku chat sekarang!', 300, 640, 35.35), ('kamu tau siapa', 820, 770, 35.58)]
def gH(cv, t):
    a0 = eo(prog(t, 30.96, 31.3))
    snd = prog(t, 32.85, 33.15); rep = prog(t, 33.45, 33.75)
    hero(cv, 140, 1130, 290, 'excited', a0, t, glow=0.6, gc=GOLD, mouth_open=0.4)
    hero(cv, 945, 1130, 290, 'excited' if rep > 0.3 else 'neutral', a0, t, glow=0.8 * rep, gc=HOTPINK, mouth_open=0.6 * rep)
    pa = eo(prog(t, 30.96, 31.4))
    cv.save(); cv.translate(540, 730); cv.scale(lerp(0.9, 1, pa), lerp(0.9, 1, pa)); cv.rotate(-2 + 2 * math.sin(t * 1.1))
    typed = typed_at(t, [(31.77, 'hai, tiba-tiba keinget kamu', 0.95, 9.0, None)]) if snd <= 0 else ''
    chat_phone(cv, 0, 0, 470, 860, a0 * pa, t, typed, HIST, status='terakhir chat 3 tahun lalu' if rep <= 0 else 'online',
               sent='hai, tiba-tiba keinget kamu' if snd > 0 else None, sent_u=snd, tick=prog(t, 33.15, 33.3),
               reply='EH!! kangen bgt!' if rep > 0 else None, reply_u=rep, send_glow=0.8 * prog(t, 32.7, 32.85) * (1 - prog(t, 33.0, 33.3)),
               dim=0.5 * eo(prog(t, 34.8, 35.2)))
    cv.restore()
    if rep > 0:
        for k in range(5):
            u = clamp(prog(t, 33.5, 35.0) * 1.3 - k * 0.15)
            if 0 < u < 1: heart_shape(cv, 900 + (k - 2) * 40, 860 - 200 * eo(u), 15 + 5 * (k % 2), bump(u) * a0, HOTPINK)
    for k, (txt, x, y, t0) in enumerate(CMTS):
        q = prog(t, t0, t0 + 0.3)
        if q > 0: comment(cv, txt, x, y, a0 * clamp(q * 2), lerp(0.7, 1, bo(q)), size=27, av=AV_COL[k], rot=(-4 if x < 540 else 4))

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
    ev = [(0.0, 'whoosh'), (0.05, 'pop'), (0.07, 'tick'), (0.95, 'tick'), (1.06, 'tick'), (1.17, 'tick'), (1.28, 'tick'), (1.39, 'tick'), (1.5, 'tick'), (1.61, 'tick'), (1.94, 'pop'), (2.4, 'tick'), (2.51, 'tick'), (2.62, 'tick'), (2.96, 'chop'), (2.98, 'ding'), (3.0, 'rise'), (3.1, 'shine'), (4.38, 'whoosh'), (5.44, 'pop'), (5.6, 'fizz_soft'), (6.43, 'pop'), (7.53, 'pop'), (8.0, 'pop'), (8.9, 'whoosh'), (8.96, 'card'), (9.26, 'stamp'), (9.54, 'ding_soft'), (12.07, 'rise'), (13.2, 'ding'), (14.82, 'whoosh'), (15.6, 'swish'), (16.5, 'pop'), (18.1, 'zoom'), (18.95, 'ding'), (19.0, 'plip'), (19.73, 'whoosh'), (20.8, 'chop'), (20.85, 'ding'), (21.0, 'heart'), (22.25, 'plop'), (23.85, 'whoosh'), (24.3, 'plip'), (24.35, 'ding_soft'), (25.81, 'chop'), (25.84, 'shine'), (26.8, 'heart'), (26.85, 'rise'), (27.85, 'whoosh'), (28.0, 'pop'), (28.6, 'crack'), (29.2, 'crack'), (29.71, 'crack'), (29.75, 'stamp'), (30.0, 'shine'), (30.1, 'heart'), (30.96, 'whoosh'), (31.77, 'tick'), (31.86, 'tick'), (31.95, 'tick'), (32.04, 'tick'), (32.13, 'tick'), (32.22, 'tick'), (32.31, 'tick'), (32.4, 'tick'), (32.49, 'tick'), (32.58, 'tick'), (32.67, 'tick'), (32.85, 'swish'), (32.9, 'plip'), (33.2, 'tick'), (33.45, 'ding'), (33.5, 'heart'), (34.89, 'pop'), (35.12, 'pop'), (35.35, 'pop'), (35.58, 'pop'), (36.6, 'whoosh'), (36.75, 'boing'), (37.1, 'shine'), (37.35, 'pop')]
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







