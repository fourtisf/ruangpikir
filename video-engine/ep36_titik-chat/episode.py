#!/usr/bin/env python3
"""Ruang Pikir reel #36: 'Bales pakai titik, kok dikira marah?' — titik di chat (Gunraj, Drumm-Hewitt, Dashow, Upadhyay & Klin 2016, Computers in Human Behavior;
Houghton, Upadhyay & Klin 2018) + lagu. Gaya premium (pelajaran EP35): studio sorot + lantai pantul, objek 3D besar di tengah, gerak fisik.
Hook: ponsel chat 3D, balasan "oke." -> titik jadi bola krom raksasa yang jatuh ke gelembung "oke" besar: retak + membeku, meter KESAN TULUS
turun, teman cemas "dia marah ya?", kartu TRIK 1 TANDA buram. Kartu riset 2016 + bola titik; 126 MAHASISWA (grid orang) -> dua ponsel 3D
balasan 1 kata (TANPA TITIK vs PAKAI TITIK); tabung kaca SEBERAPA TULUS (di chat titik lebih rendah, di kertas tulisan tangan sama);
ikon NADA SUARA & EKSPRESI MUKA dicoret -> tanda baca 3D mengorbit ponsel; bola titik jatuh jadi dinding es OBROLAN DITUTUP (kesannya ketus,
padahal "aku biasa aja kok"); kartu dibuka "Balas singkat? Hapus titiknya." + tombol hapus, bola titik pecah, gelembung jadi hangat.
python3 episode.py preview t1 t2 ... | timeline out.json | video out.mp4"""
import sys, os, math, json, subprocess, random
import skia
import base as b
from base import (clamp, lerp, prog, eo, ei, eio, bo, bump, col, P, lg, rg, layer, font, XB, B, M, MONO, bl, tracked, parse,
                 pill, sparkle, person, ACC, ACC_L, ACC_XL, TXT, MUTED, CORAL, MINT, W, H, FPS)

VIOLET, YELLOW, INK, HL = '#B57BFF', '#FFD23F', '#0B0C1E', '#AEB6FF'

# adegan (waktu animasi, DUR 42); tag tidak ditampilkan
b.GROUPS = [(0.0, 5.88, 'A'), (5.88, 9.4, 'B'), (9.4, 14.36, 'C'), (14.36, 20.28, 'D'), (20.28, 25.53, 'E'),
            (25.53, 30.53, 'F'), (30.53, 34.26, 'G'), (34.26, 36.6, 'H'), (36.6, 42.0, 'J')]
PHRASES = [(0.15, 'Kamu suka bales chat pakai [titik]?'), (2.07, '[Hati-hati].'), (2.58, 'Kata riset,'), (3.22, 'balasan kayak gitu bisa kedengeran [nggak tulus].'),
           (5.88, 'Tahun [2016],'), (6.99, 'peneliti [Celia Klin] dan timnya menguji ini.'),
           (9.4, '[126 mahasiswa]'), (10.93, 'membaca chat yang dibalas [satu kata].'), (12.51, 'Ada yang pakai [titik],'), (13.34, 'ada yang [nggak].'),
           (14.36, '[Hasilnya]?'), (15.19, 'Yang pakai titik dinilai [kurang tulus].'), (17.28, 'Anehnya,'), (18.08, 'kalau [ditulis tangan],'), (19.0, '[nggak ada bedanya].'),
           (20.28, 'Soalnya di [chat],'), (21.45, 'kita nggak bisa dengar [nada suara]'), (22.59, 'atau lihat [muka].'), (23.47, 'Jadi [tanda baca] yang ngegantiin.'),
           (25.53, 'Dan [titik] di balasan singkat'), (26.9, 'kerasa kayak [nutup obrolan].'), (28.2, 'Kesannya [ketus],'), (29.15, 'padahal kamu [nggak marah].'),
           (30.53, 'Jadi kalau balasnya cuma [satu kata],'), (32.26, 'coba [trik kecil] ini:'), (33.12, '[Hapus titiknya].'),
           (34.26, '[Kirim] video ini ke teman yang suka bales pakai [titik]!'),
           (36.6, 'Follow [Ruang Pikir],'), (37.36, 'biar makin kenal [isi kepalamu].')]
b.CAPS = [(t, s, '') for t, s in PHRASES]          # dipakai base hanya untuk jadwal

# ------------------------------------------------------------ chrome gaya sinematik
b.draw_tag = lambda cv, t: None
b.draw_progress = lambda cv, t: None
def draw_title(cv, t):
    a = eo(prog(t, 0.05, 0.35)) * (1 - eio(prog(t, 5.4, 5.88)))
    if a <= 0: return
    segs = parse("Bales pakai titik, kok [dikira marah?]"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 232) + (1 - eo(prog(t, 0.05, 0.35))) * 16 - 10 * eio(prog(t, 5.4, 5.88))
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
        e = PHRASES[i + 1][0] - 0.2 if i + 1 < len(PHRASES) else b.DUR - 0.3
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
    # pendar kafe hangat dari atas (tanpa titik/bokeh)
    cv.drawCircle(540, 260, 900, P(shader=rg(540, 260, 900, [col('#FFC98A', 0.06), col('#B57BFF', 0.03), col('#B57BFF', 0)], [0, 0.5, 1])))
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

def research_card(cv, t, t0, year, names, journal, back=None, t_flip=None, y=700, t_out=None, tag='JPSP'):
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
            mono(cv, tag, r.right() - 54, r.top() + 60, 25, MINT, 0.8 * a, sp=3, align=1)
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

# ------------------------------------------------------------ helper EP17: kartu pertanyaan 3D + lapisan diri
QTEXT = 'Kalau bisa makan malam bareng siapa aja di dunia, kamu pilih siapa?'
def wob(t): return 4 * math.sin(t * 1.5), 4 * math.sin(t * 1.1)
def wrap(text, f, maxw):
    lines, cur = [], ''
    for w in text.split(' '):
        nxt = (cur + ' ' + w).strip()
        if cur and f.measureText(nxt) > maxw: lines.append(cur); cur = w
        else: cur = nxt
    if cur: lines.append(cur)
    return lines

def q_card(cv, cx, cy, w, h, a, t, ry=0.0, rx=0.0, z=0.0, num='01', text=QTEXT, hl=0.0, glow=0.6, size=44, back_only=False):
    """kartu pertanyaan 3D: muka = pertanyaan (ry 0), belakang = '?' emas (ry 180)"""
    if a <= 0: return
    with plane(cv, cx, cy, z, w, h, ry, rx) as ok:
        if not ok: return
        r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2); rad = w * 0.07
        cv.drawRoundRect(r, rad, rad, P(col(GOLD, 0.5 * glow * a), blur=30))
        if facing(ry, rx) >= 0 and not back_only:
            cv.drawRoundRect(r, rad, rad, P(shader=lg(0, -h / 2, 0, h / 2, [col('#2A2440', a), col('#16142A', a)])))
            cv.drawRoundRect(r, rad, rad, P(col(GOLD, a), stroke=4)); cv.drawRoundRect(r.makeInset(14, 14), rad * 0.7, rad * 0.7, P(col(GOLD, 0.35 * a), stroke=1.5))
            mono(cv, f'PERTANYAAN {num} / 36', 0, -h / 2 + 52, max(16, w * 0.04), GOLD, a, sp=3)
            f = font(XB, size); lines = wrap(text, f, w * 0.8); lh = size * 1.22
            y0 = -(len(lines) - 1) * lh / 2 + h * 0.05
            for i, ln in enumerate(lines):
                last = i == len(lines) - 1
                c = mixc(TXT, GOLD, hl) if last or (i == len(lines) - 2 and 'kamu' in ln) else TXT
                cv.drawString(ln, -f.measureText(ln) / 2, bl(f, y0 + i * lh), f, P(col(c, a)))
        else:
            if facing(ry, rx) < 0: cv.scale(-1, 1)
            cv.drawRoundRect(r, rad, rad, P(shader=lg(-w / 2, -h / 2, w / 2, h / 2, [col('#FFD98A', a), col('#E09A3A', a), col('#B8741E', a)])))
            for k in range(6):
                cv.drawCircle(0, 0, w * (0.12 + 0.07 * k), P(col('#FFFFFF', 0.08 * a), stroke=2))
            f = font(XB, w * 0.5); s_ = '?'
            cv.drawString(s_, -f.measureText(s_) / 2, bl(f, 0) + 6, f, P(col('#6A4A10', 0.6 * a), blur=4))
            cv.drawString(s_, -f.measureText(s_) / 2, bl(f, 0), f, P(col('#FFF6E0', a)))
            cv.drawRoundRect(r, rad, rad, P(col('#FFFFFF', 0.5 * a), stroke=3))

def mini_card(cv, x, y, w, h, a, rot, num, c=('#3A3D66', '#22243A'), edge=ACC_L, nc=ACC_XL):
    if a <= 0: return
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    cv.drawRoundRect(r.makeOffset(3, 8), 10, 10, P(col('#000000', 0.45 * a), blur=8))
    cv.drawRoundRect(r, 10, 10, P(shader=lg(0, -h / 2, 0, h / 2, [col(c[0], a), col(c[1], a)])))
    cv.drawRoundRect(r, 10, 10, P(col(edge, 0.6 * a), stroke=2))
    mono(cv, num, 0, 0, w * 0.32, nc, a, sp=1)
    cv.restore()

def depth_col(u):
    """warna kartu dari ringan (biru) ke pribadi (emas/pink)"""
    return mixc(mixc('#7FB8FF', '#B57BFF', clamp(u * 2)), HOTPINK if u < 0.9 else GOLD, clamp(u * 2 - 1))

def shells(cv, x, cy, a, t, opened, c):
    """lapisan diri: 3 cangkang kaca di sekitar tokoh; opened 0..3 = berapa lapis yang sudah terbuka (memudar keluar)"""
    for k in range(3):
        rr = 210 - k * 45; o = clamp(opened - k)
        if o >= 1: continue
        sc = 1 + 0.35 * eo(o); aa = a * (1 - o)
        cv.drawOval(skia.Rect(x - rr * 0.75 * sc, cy - rr * sc, x + rr * 0.75 * sc, cy + rr * sc), P(col(ACC_L, 0.08 * aa)))
        cv.drawOval(skia.Rect(x - rr * 0.75 * sc, cy - rr * sc, x + rr * 0.75 * sc, cy + rr * sc), P(col(ACC_L, 0.45 * aa), stroke=2.5))
    warm = clamp(opened / 3)
    cv.drawCircle(x, cy - 20, 90, P(shader=rg(x, cy - 20, 160, [col(c, 0.45 * warm * a), col(c, 0)])))

KRIK = [('krik...', 170, 520, -8, -0.4), ('krik...', 900, 600, 7, 0.45), ('. . .', 540, 470, 0, 1.0)]

# ------------------------------------------------------------ helper EP19: hati kaca berisi cairan + bantuan kecil
def glass_heart(cv, cx, cy, s, v, a, t, label='SUKA', c=HOTPINK, glow=0.0):
    """hati kaca 3D berisi cairan yang bergelombang (v 0..1 = tinggi cairan)"""
    if a <= 0: return
    hp = heart_path(cx, cy, s)
    top, bot = cy - s * 0.85, cy + s * 0.9
    if glow > 0: cv.drawPath(hp, P(col(c, 0.55 * glow * a), blur=s * 0.45))
    cv.drawPath(hp, P(col('#1A1430', 0.55 * a)))
    cv.save(); cv.clipPath(hp, skia.ClipOp.kIntersect, True)
    lvl = lerp(bot, top, clamp(v))
    wv = skia.Path(); wv.moveTo(cx - s * 1.5, bot + 10)
    for i in range(41):
        x = cx - s * 1.5 + 3 * s * i / 40; wv.lineTo(x, lvl + s * 0.06 * math.sin(i * 0.5 + t * 4))
    wv.lineTo(cx + s * 1.5, bot + 10); wv.close()
    cv.drawPath(wv, P(shader=lg(0, lvl, 0, bot, [col(mixc(c, '#FFFFFF', 0.35), a), col(c, a), col(mixc(c, '#000000', 0.35), a)], [0, 0.4, 1])))
    for k in range(3):
        bu = (t * 0.5 + k * 0.33) % 1.0
        by = lerp(bot - s * 0.1, lvl, bu)
        if by > lvl + 4: cv.drawCircle(cx + (k - 1) * s * 0.3, by, s * 0.05, P(col('#FFFFFF', 0.45 * a * (1 - bu))))
    cv.drawOval(skia.Rect(cx - s * 0.75, cy - s * 0.7, cx - s * 0.25, cy - s * 0.25), P(col('#FFFFFF', 0.28 * a), blur=s * 0.06))
    cv.restore()
    cv.drawPath(hp, P(col('#FFFFFF', 0.6 * a), stroke=3))
    if label: mono(cv, f'{label} {int(round(v * 100))}%', cx, bot + 34, 22, mixc(c, '#FFFFFF', 0.3), a, sp=2)

def pen(cv, x, y, s, a, rot=-35, c=GOLD):
    """pulpen emas (ujung di x,y)"""
    if a <= 0: return
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    body = skia.Rect(-s * 0.09, -s * 1.0, s * 0.09, -s * 0.16)
    cv.drawRoundRect(body.makeOffset(4, 8), s * 0.09, s * 0.09, P(col('#000000', 0.4 * a), blur=8))
    cv.drawRoundRect(body, s * 0.09, s * 0.09, P(shader=lg(-s * 0.09, 0, s * 0.09, 0, [col(mixc(c, '#FFFFFF', 0.45), a), col(c, a), col(mixc(c, '#000000', 0.4), a)])))
    tip = skia.Path(); tip.moveTo(-s * 0.09, -s * 0.16); tip.lineTo(s * 0.09, -s * 0.16); tip.lineTo(0, 0); tip.close()
    cv.drawPath(tip, P(col('#E8E6F0', a))); cv.drawRect(skia.Rect(-s * 0.1, -s * 0.78, s * 0.1, -s * 0.7), P(col('#FFFFFF', 0.6 * a)))
    cv.restore()

def coin(cv, x, y, r, a, t=0.0, spin=0.0):
    """koin emas yang berputar (spin = fase)"""
    if a <= 0: return
    sx = max(0.15, abs(math.cos(spin)))
    cv.save(); cv.translate(x, y); cv.scale(sx, 1)
    cv.drawCircle(0, 4, r, P(col('#000000', 0.4 * a), blur=6))
    cv.drawCircle(0, 0, r, P(shader=rg(-r * 0.3, -r * 0.3, r * 1.6, [col('#FFF1B8', a), col(GOLD, a), col('#B8741E', a)])))
    cv.drawCircle(0, 0, r * 0.78, P(col('#FFF6D8', 0.7 * a), stroke=r * 0.08))
    f = font(XB, r * 1.0); s_ = '$'; cv.drawString(s_, -f.measureText(s_) / 2, bl(f, 0), f, P(col('#8A5A12', a)))
    cv.restore()

def clipboard(cv, x, y, s, a):
    if a <= 0: return
    r = skia.Rect(x - s * 0.38, y - s * 0.5, x + s * 0.38, y + s * 0.5)
    cv.drawRoundRect(r, s * 0.06, s * 0.06, P(col('#6A4A30', a)))
    cv.drawRect(r.makeInset(s * 0.06, s * 0.08), P(col('#F4F2FA', a)))
    for k in range(4): cv.drawLine(r.left() + s * 0.12, r.top() + s * (0.25 + 0.15 * k), r.right() - s * 0.12, r.top() + s * (0.25 + 0.15 * k), P(col('#9A9CB8', a), stroke=3))
    cv.drawRoundRect(skia.Rect(x - s * 0.14, r.top() - s * 0.05, x + s * 0.14, r.top() + s * 0.06), s * 0.03, s * 0.03, P(col('#C9CBE0', a)))

def favor_card(cv, text, x, y, a, ok=True, sc=1.0, strike=0.0):
    """kartu kaca bantuan kecil (✓) atau besar (✗)"""
    if a <= 0: return
    c = MINT if ok else CORAL
    f = font(B, 30); w = f.measureText(text) + 120; h = 74
    cv.save(); cv.translate(x, y); cv.scale(sc, sc)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    glass(cv, r, rad=h * 0.4, a=a, glow=0.35, gc=c)
    cv.drawString(text, -w / 2 + 34, bl(f, 0), f, P(col(TXT, a)))
    if ok: check_mark(cv, w / 2 - 44, 0, 20, 1.0, a, MINT)
    else: cross(cv, w / 2 - 44, 0, 18, a, CORAL, 6)
    if strike > 0: cv.drawLine(-w / 2 + 24, 0, -w / 2 + 24 + (w - 48) * eo(strike), 0, P(col(CORAL, a), stroke=5))
    cv.restore()

# ------------------------------------------------------------ helper EP20: kotak cerita emas + bola cerita yang bolak-balik
def orb(cv, x, y, r, a, c=GOLD):
    """bola cahaya cerita"""
    if a <= 0: return
    cv.drawCircle(x, y, r * 2.2, P(shader=rg(x, y, r * 2.2, [col(c, 0.45 * a), col(c, 0)])))
    cv.drawCircle(x, y, r, P(shader=rg(x - r * 0.3, y - r * 0.3, r * 1.4, [col('#FFFFFF', a), col(mixc(c, '#FFFFFF', 0.4), a), col(c, a)], [0, 0.4, 1])))

def padlock(cv, x, y, s, a, u=0.0, c=GOLD):
    """gembok: u 0 terkunci -> 1 terbuka (shackle naik & berputar)"""
    if a <= 0: return
    cv.save(); cv.translate(x, y)
    sh = skia.Path(); sh.addArc(skia.Rect(-s * 0.32, -s * 0.95, s * 0.32, -s * 0.25), 180, 180)
    sh.moveTo(-s * 0.32, -s * 0.6); sh.lineTo(-s * 0.32, -s * 0.15)
    sh.moveTo(s * 0.32, -s * 0.6); sh.lineTo(s * 0.32, -s * 0.15 - s * 0.25 * eo(u))
    cv.save(); cv.translate(-s * 0.32, -s * 0.15); cv.rotate(-35 * eo(u)); cv.translate(s * 0.32, s * 0.15 - s * 0.3 * eo(u))
    cv.drawPath(sh, P(col('#C9CBE0', a), stroke=s * 0.13)); cv.restore()
    body = skia.Rect(-s * 0.48, -s * 0.2, s * 0.48, s * 0.5)
    cv.drawRoundRect(body, s * 0.12, s * 0.12, P(shader=lg(0, -s * 0.2, 0, s * 0.5, [col(mixc(c, '#FFFFFF', 0.4), a), col(c, a), col(mixc(c, '#000000', 0.35), a)])))
    cv.drawCircle(0, s * 0.1, s * 0.08, P(col('#4A3410', a))); cv.drawRect(skia.Rect(-s * 0.03, s * 0.1, s * 0.03, s * 0.3), P(col('#4A3410', a)))
    cv.restore()

def story_box(cv, x, y, s, a, t, open_=0.0, lock=0.0, glow=0.0, c=GOLD, show_lock=True):
    """kotak cerita emas: tutup terbuka ke belakang (open_ 0..1) + pancaran cahaya dari dalam, gembok di depan"""
    if a <= 0: return
    w, h = s, s * 0.62; ly = y - h / 2; o = eo(open_)
    if o > 0:
        beam = skia.Path(); beam.moveTo(x - w * 0.42, ly); beam.lineTo(x + w * 0.42, ly); beam.lineTo(x + w * 1.0, ly - 360); beam.lineTo(x - w * 1.0, ly - 360); beam.close()
        cv.drawPath(beam, P(shader=lg(0, ly, 0, ly - 360, [col(mixc(c, '#FFFFFF', 0.5), 0.55 * a * o), col(c, 0.18 * a * o), col(c, 0)], [0, 0.5, 1])))
        rays(cv, x, ly, s * 1.2 * o, 0.45 * a * o, t, n=12, c=c, spin=5)
        bl_ = h * 0.62 * o
        back = skia.Rect(x - w / 2 + 4, ly - bl_, x + w / 2 - 4, ly)
        cv.drawRoundRect(back, 8, 8, P(shader=lg(0, back.top(), 0, back.bottom(), [col(mixc(c, '#000000', 0.15), a), col(mixc(c, '#000000', 0.55), a)])))
        cv.drawRoundRect(back, 8, 8, P(col('#FFF1D0', 0.5 * a), stroke=2))
    if glow > 0: cv.drawRoundRect(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 14, 14, P(col(c, 0.5 * glow * a), blur=24))
    r = skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    cv.drawRoundRect(r.makeOffset(4, 12), 12, 12, P(col('#000000', 0.45 * a), blur=12))
    cv.drawRoundRect(r, 12, 12, P(shader=lg(0, r.top(), 0, r.bottom(), [col(mixc(c, '#FFFFFF', 0.25), a), col(c, a), col(mixc(c, '#000000', 0.45), a)], [0, 0.4, 1])))
    for bx in (x - w * 0.3, x + w * 0.3): cv.drawRect(skia.Rect(bx - w * 0.04, r.top(), bx + w * 0.04, r.bottom()), P(col(mixc(c, '#000000', 0.35), 0.7 * a)))
    cv.drawRoundRect(r, 12, 12, P(col('#FFF1D0', 0.5 * a), stroke=2))
    if o > 0: cv.drawOval(skia.Rect(x - w * 0.42, ly - 8, x + w * 0.42, ly + 8), P(col('#FFF6D8', 0.9 * a * o), blur=6))
    if o < 1:
        lh = h * 0.42; la = a * (1 - o)
        lid = skia.Path(); lid.moveTo(x - w / 2 - 6, ly); lid.lineTo(x - w / 2 + 6, ly - lh); lid.lineTo(x + w / 2 - 6, ly - lh); lid.lineTo(x + w / 2 + 6, ly); lid.close()
        cv.save(); cv.translate(0, -40 * o)
        cv.drawPath(lid, P(shader=lg(0, ly - lh, 0, ly, [col(mixc(c, '#FFFFFF', 0.45), la), col(mixc(c, '#000000', 0.25), la)])))
        cv.drawPath(lid, P(col('#FFF1D0', 0.5 * la), stroke=2)); cv.restore()
    if show_lock and lock < 1: padlock(cv, x, y + h * 0.05, s * 0.28, a * (1 - prog(lock, 0.7, 1.0)), lock, '#E8E6F0')

def call_frame(cv, cx, cy, w, h, a, c=ACC_L):
    """bingkai video call kaca"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    glass(cv, r, rad=24, a=0.8 * a, glow=0.15, gc=c, fill=('#1E1F3C', '#111226'))
    cv.drawCircle(r.left() + 22, r.top() + 22, 7, P(col(CORAL, a)))
    mono(cv, 'LIVE', r.left() + 36, r.top() + 22, 14, ACC_L, a, sp=2, align=0)

def race_bar(cv, x0, x1, y, v, a, c, label):
    if a <= 0: return
    mono(cv, label, x0, y - 30, 20, c, a, sp=2, align=0)
    cv.drawRoundRect(skia.Rect(x0, y - 14, x1, y + 14), 14, 14, P(col('#1A1B30', 0.95 * a)))
    xv = x0 + (x1 - x0) * clamp(v)
    if xv > x0 + 24:
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 10, xv - 4, y + 10), 10, 10, P(col(c, 0.5 * a), blur=10))
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 10, xv - 4, y + 10), 10, 10, P(shader=lg(x0, 0, x1, 0, [col(mixc(c, '#FFFFFF', 0.4), a), col(c, a)])))

def fly_orb(cv, t, t0, dur, x0, y0, x1, y1, a, c=GOLD, lift=160, r=16):
    u = prog(t, t0, t0 + dur)
    if not (0 < u < 1): return
    x = lerp(x0, x1, eio(u)); y = lerp(y0, y1, eio(u)) - lift * math.sin(u * math.pi)
    for k in range(5):
        uu = max(0.0, u - k * 0.04); xx = lerp(x0, x1, eio(uu)); yy = lerp(y0, y1, eio(uu)) - lift * math.sin(uu * math.pi)
        cv.drawCircle(xx, yy, r * (1 - k * 0.15), P(col(c, 0.25 * (1 - k / 5) * a), blur=6))
    orb(cv, x, y, r, a * bump(u) * 1.3 if u > 0.85 or u < 0.15 else a, c)

# ------------------------------------------------------------ helper EP21: alat ukur CANGGUNG + kolam dangkal -> lautan deep talk
SEA = '#2BB3C9'
DQ = 'Hal apa yang paling kamu syukuri?'
def sea_bg(cv, a, t, depth=1.0):
    """latar bawah laut: gradien biru-ungu dalam + sorot cahaya dari permukaan (tanpa titik/bokeh)"""
    if a <= 0: return
    top = mixc('#1E3A8A', '#141A4A', depth); bot = mixc('#0E1440', '#05061A', depth)
    cv.drawRect(skia.Rect(0, 0, W, 1250), P(shader=lg(0, 0, 0, 1250, [col(top, 0.85 * a), col(bot, 0.9 * a)])))
    for k in range(5):
        x = 140 + k * 210 + 40 * math.sin(t * 0.6 + k * 1.7); w0, w1 = 40 + 10 * k % 30, 160
        ray = skia.Path(); ray.moveTo(x - w0, 0); ray.lineTo(x + w0, 0); ray.lineTo(x + w1 + 90 * math.sin(t * 0.4 + k), 1250); ray.lineTo(x - w1 + 90 * math.sin(t * 0.4 + k), 1250); ray.close()
        cv.drawPath(ray, P(shader=lg(0, 0, 0, 1250, [col('#9FE8FF', (0.10 - 0.04 * depth) * a), col('#9FE8FF', 0)])))
    for k in range(3):
        y = 330 + k * 270 + 30 * math.sin(t * 0.5 + k)
        p = skia.Path(); p.moveTo(0, y)
        for i in range(1, 25): p.lineTo(i * 45, y + 14 * math.sin(i * 0.7 + t * 1.2 + k))
        cv.drawPath(p, P(col('#9FE8FF', 0.06 * a), stroke=3, blur=4))

def water_front(cv, ys, a, t, c=SEA):
    """air kolam di depan (permukaan bergelombang + kilau)"""
    if a <= 0: return
    p = skia.Path(); p.moveTo(0, ys)
    for i in range(1, 37): p.lineTo(i * 30, ys + 9 * math.sin(i * 0.55 + t * 2.2))
    p.lineTo(W, 1250); p.lineTo(0, 1250); p.close()
    cv.drawPath(p, P(shader=lg(0, ys, 0, 1250, [col(c, 0.55 * a), col('#123A5A', 0.75 * a)])))
    hl = skia.Path(); hl.moveTo(0, ys)
    for i in range(1, 37): hl.lineTo(i * 30, ys + 9 * math.sin(i * 0.55 + t * 2.2))
    cv.drawPath(hl, P(col('#CFF6FF', 0.7 * a), stroke=3)); cv.drawPath(hl, P(col('#9FE8FF', 0.4 * a), stroke=10, blur=8))

def depth_meter(cv, x, y0, y1, v, a, label='KEDALAMAN', unit_max=100):
    """meteran kedalaman vertikal dengan penanda"""
    if a <= 0: return
    cv.drawRoundRect(skia.Rect(x - 10, y0, x + 10, y1), 10, 10, P(col('#0E1430', 0.9 * a))); cv.drawRoundRect(skia.Rect(x - 10, y0, x + 10, y1), 10, 10, P(col(SEA, 0.5 * a), stroke=2))
    for k in range(6):
        yy = lerp(y0, y1, k / 5); cv.drawLine(x + 14, yy, x + 30, yy, P(col(ACC_L, 0.5 * a), stroke=2))
        mono(cv, f'{int(unit_max * k / 5)}m', x + 38, yy, 16, ACC_L, 0.6 * a, align=0)
    ym = lerp(y0, y1, clamp(v))
    cv.drawRoundRect(skia.Rect(x - 6, y0 + 4, x + 6, max(y0 + 8, ym)), 6, 6, P(shader=lg(0, y0, 0, y1, [col('#9FE8FF', a), col(GOLD, a)])))
    cv.drawCircle(x, ym, 16, P(col(GOLD, 0.6 * a), blur=10)); cv.drawCircle(x, ym, 12, P(col('#FFF1D0', a)))
    mono(cv, label, x, y0 - 30, 18, SEA, a, sp=3)

def deep_card(cv, cx, cy, w, h, a, t, text=DQ, size=40, glow=1.0, label='PERTANYAAN DALAM', rot=0.0):
    """kartu kaca emas pertanyaan dalam"""
    if a <= 0: return
    cv.save(); cv.translate(cx, cy); cv.rotate(rot)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    cv.drawRoundRect(r, 30, 30, P(col(GOLD, 0.5 * glow * a), blur=34))
    cv.drawRoundRect(r, 30, 30, P(shader=lg(0, -h / 2, 0, h / 2, [col('#2A2440', 0.95 * a), col('#16142A', 0.95 * a)])))
    cv.drawRoundRect(r, 30, 30, P(col(GOLD, a), stroke=4)); cv.drawRoundRect(r.makeInset(14, 14), 20, 20, P(col(GOLD, 0.35 * a), stroke=1.5))
    mono(cv, label, 0, -h / 2 + 46, 20, GOLD, a, sp=3)
    f = font(XB, size); lines = wrap(text, f, w * 0.82); lh = size * 1.22
    y0 = -(len(lines) - 1) * lh / 2 + h * 0.06
    for i, ln in enumerate(lines): cv.drawString(ln, -f.measureText(ln) / 2, bl(f, y0 + i * lh), f, P(col('#FFE9C0', a)))
    cv.restore()

def float_hero(cv, x, y, h, mood, a, t, rot=0.0, glow=0.0, gc=GOLD, ph=0.0):
    """tokoh kapsul yang melayang/berenang (badan dimiringkan, naik turun pelan)"""
    if a <= 0: return
    yy = y + 10 * math.sin(t * 1.6 + ph)
    cv.save(); cv.translate(x, yy); cv.rotate(rot + 4 * math.sin(t * 1.1 + ph)); cv.translate(-x, -yy)
    hero(cv, x, yy, h, mood, a, t, glow=glow, gc=gc, mouth_open=0.4)
    cv.restore()

def compare_bars(cv, cx, base, a, label, dikira, nyata, c_dk, c_ny, g):
    """dua batang: 'dikira' (bayangan putus-putus) vs 'kenyataan' (padat), tanpa angka"""
    if a <= 0: return
    mono(cv, label, cx, base - 330, 26, ACC_XL, a, sp=4, glow=0.3)
    for k, (v, c, lab) in enumerate(((dikira, c_dk, 'dikira'), (lerp(dikira, nyata, g), c_ny, 'kenyataan'))):
        x = cx - 70 + k * 140; hgt = 260 * v
        r = skia.Rect(x - 48, base - hgt, x + 48, base)
        if k == 0:
            cv.drawRoundRect(r, 14, 14, P(col(c, 0.18 * a))); cv.drawRoundRect(r, 14, 14, P(col(c, 0.7 * a), stroke=3))
        else:
            cv.drawRoundRect(r, 14, 14, P(col(c, 0.45 * a), blur=16))
            cv.drawRoundRect(r, 14, 14, P(shader=lg(0, r.top(), 0, r.bottom(), [col(mixc(c, '#FFFFFF', 0.35), a), col(mixc(c, '#000000', 0.25), a)])))
        mono(cv, lab, x, base + 30, 18, ACC_L, a, sp=1)

def choice_card(cv, cx, cy, w, h, a, t, title, deep=False, glow=0.0, tried=0.0):
    """kartu pilihan: kolam dangkal (gelombang tipis) vs laut dalam (gradien + sorot cahaya)"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    if glow > 0: cv.drawRoundRect(r, 28, 28, P(col(GOLD, 0.55 * glow * a), blur=30))
    cv.save(); pr = skia.Path(); pr.addRoundRect(r, 28, 28); cv.clipPath(pr, skia.ClipOp.kIntersect, True)
    if deep:
        cv.drawRect(r, P(shader=lg(0, r.top(), 0, r.bottom(), [col('#1E3A8A', a), col('#060820', a)])))
        for k in range(3):
            x = r.left() + w * (0.25 + 0.25 * k); ray = skia.Path(); ray.moveTo(x - 10, r.top()); ray.lineTo(x + 10, r.top()); ray.lineTo(x + 50, r.bottom()); ray.lineTo(x - 30, r.bottom()); ray.close()
            cv.drawPath(ray, P(col('#9FE8FF', 0.12 * a)))
        cv.drawCircle(cx, cy + h * 0.12, w * 0.16, P(shader=rg(cx, cy + h * 0.12, w * 0.3, [col(GOLD, 0.8 * a), col(GOLD, 0)])))
    else:
        cv.drawRect(r, P(shader=lg(0, r.top(), 0, r.bottom(), [col('#1A1C34', a), col('#14162A', a)])))
        ys = cy + h * 0.15
        for k in range(3):
            p = skia.Path(); p.moveTo(r.left(), ys + k * 18)
            for i in range(1, 21): p.lineTo(r.left() + i * w / 20, ys + k * 18 + 6 * math.sin(i * 0.9 + t * 2 + k))
            cv.drawPath(p, P(col(SEA, (0.6 - 0.15 * k) * a), stroke=3))
    cv.restore()
    cv.drawRoundRect(r, 28, 28, P(col(GOLD if deep else ACC_L, 0.8 * a), stroke=3))
    f = font(XB, 38); cv.drawString(title, cx - f.measureText(title) / 2, bl(f, r.top() + 60), f, P(col(TXT, a)))
    if tried > 0: check_mark(cv, r.right() - 40, r.top() + 40, 22, tried, a, MINT)

# ------------------------------------------------------------ helper EP22: toples pujian emas
def jar(cv, x, y, s, a, t, lid=0.0, shake=0.0, inner='bajumu bagus!', inner_a=1.0, glow=0.0):
    """toples kaca bertutup emas berisi gelembung pujian yang berpendar; lid 0 tertutup -> 1 terlempar"""
    if a <= 0: return
    x += shake * 6 * math.sin(t * 40)
    w, h = s, s * 1.15; r = skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    if glow > 0: cv.drawRoundRect(r, w * 0.22, w * 0.22, P(col(GOLD, 0.5 * glow * a), blur=30))
    cv.drawOval(skia.Rect(x - w * 0.55, r.bottom() - 10, x + w * 0.55, r.bottom() + 16), P(col('#000000', 0.5 * a), blur=10))
    cv.drawRoundRect(r, w * 0.22, w * 0.22, P(shader=lg(r.left(), 0, r.right(), 0, [col('#CFE3FF', 0.20 * a), col('#7F8CFF', 0.08 * a), col('#CFE3FF', 0.24 * a)])))
    if inner_a > 0:
        cv.save(); pr = skia.Path(); pr.addRoundRect(r.makeInset(10, 10), w * 0.18, w * 0.18); cv.clipPath(pr, skia.ClipOp.kIntersect, True)
        cv.drawCircle(x, y + h * 0.05, w * 0.5, P(shader=rg(x, y + h * 0.05, w * 0.6, [col(GOLD, 0.55 * a * inner_a), col(GOLD, 0)])))
        f = font(XB, w * 0.13); tw = f.measureText(inner)
        if tw > w * 0.66: f = font(XB, w * 0.13 * w * 0.66 / tw); tw = f.measureText(inner)
        bw = tw + w * 0.16; bh = w * 0.26
        br = skia.Rect(x - bw / 2, y - bh / 2 + 6 * math.sin(t * 3), x + bw / 2, y + bh / 2 + 6 * math.sin(t * 3))
        cv.drawRoundRect(br, bh * 0.45, bh * 0.45, P(col('#3A2A10', 0.95 * a * inner_a))); cv.drawRoundRect(br, bh * 0.45, bh * 0.45, P(col(GOLD, a * inner_a), stroke=3))
        cv.drawString(inner, x - tw / 2, bl(f, br.centerY()), f, P(col('#FFE3B0', a * inner_a)))
        cv.restore()
    cv.drawRoundRect(r, w * 0.22, w * 0.22, P(col('#E8F0FF', 0.6 * a), stroke=3))
    cv.drawLine(r.left() + w * 0.16, r.top() + h * 0.18, r.left() + w * 0.16, r.bottom() - h * 0.25, P(col('#FFFFFF', 0.45 * a), stroke=7, blur=3))
    lu = eo(lid); lx = x + 140 * lu; ly = r.top() - 14 - 260 * lu + 380 * lu * lu
    cv.save(); cv.translate(lx, ly); cv.rotate(220 * lu)
    lr = skia.Rect(-w * 0.42, -18, w * 0.42, 18)
    cv.drawRoundRect(lr, 10, 10, P(shader=lg(0, -18, 0, 18, [col('#FFE3A0', a * (1 - prog(lid, 0.8, 1.0))), col('#B8741E', a * (1 - prog(lid, 0.8, 1.0)))])))
    cv.restore()

def magnifier(cv, x, y, r, a, c=ACC_L):
    if a <= 0: return
    cv.drawCircle(x, y, r, P(col('#CFE3FF', 0.12 * a))); cv.drawCircle(x, y, r, P(col(c, a), stroke=r * 0.14))
    cv.drawLine(x + r * 0.72, y + r * 0.72, x + r * 1.5, y + r * 1.5, P(col(c, a), stroke=r * 0.22))
    cv.drawOval(skia.Rect(x - r * 0.6, y - r * 0.65, x - r * 0.1, y - r * 0.35), P(col('#FFFFFF', 0.35 * a), blur=4))

def praise_card(cv, text, x, y, a, sc=1.0, rot=0.0):
    """kartu kaca pujian sederhana dengan ikon hati"""
    if a <= 0: return
    f = font(B, 30); w = f.measureText(text) + 120; h = 74
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(sc, sc)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    glass(cv, r, rad=h * 0.4, a=a, glow=0.4, gc=GOLD)
    heart_shape(cv, -w / 2 + 40, 0, 15, a, HOTPINK)
    cv.drawString(text, -w / 2 + 70, bl(f, 0), f, P(col(TXT, a)))
    cv.restore()

# ------------------------------------------------------------ helper EP23: baterai sosial 3D
def bat_col(v):
    return mixc(CORAL, '#FFC56B', clamp(v / 0.35)) if v < 0.35 else mixc('#FFC56B', MINT, clamp((v - 0.35) / 0.3))

def battery3d(cv, cx, cy, w, v, a, t, charging=0.0, warn=0.0, label=True, glow=0.6):
    """baterai kaca 3D horizontal: isi berwarna (hijau->kuning->merah), segmen, persen, petir saat dicas"""
    if a <= 0: return
    h = w * 0.46; r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2 - w * 0.06, cy + h / 2); rad = h * 0.22
    c = bat_col(v)
    if warn > 0 and (t * 3) % 1 < 0.55: cv.drawRoundRect(r, rad, rad, P(col(CORAL, 0.7 * warn * a), blur=30))
    cv.drawRoundRect(r, rad, rad, P(col(c, 0.35 * glow * a), blur=26))
    cv.drawRoundRect(r.makeOffset(6, 16), rad, rad, P(col('#000000', 0.5 * a), blur=18))
    cv.drawRoundRect(r, rad, rad, P(shader=lg(0, r.top(), 0, r.bottom(), [col('#2E3150', 0.92 * a), col('#14162A', 0.95 * a)])))
    nub = skia.Rect(r.right(), cy - h * 0.2, r.right() + w * 0.06, cy + h * 0.2)
    cv.drawRoundRect(nub, 8, 8, P(shader=lg(0, nub.top(), 0, nub.bottom(), [col('#9A9CB8', a), col('#4A4D68', a)])))
    inner = r.makeInset(h * 0.1, h * 0.1); fw = inner.width() * clamp(v)
    if fw > 2:
        fr = skia.Rect(inner.left(), inner.top(), inner.left() + fw, inner.bottom())
        cv.drawRoundRect(fr, rad * 0.6, rad * 0.6, P(shader=lg(0, fr.top(), 0, fr.bottom(), [col(mixc(c, '#FFFFFF', 0.4), a), col(c, a), col(mixc(c, '#000000', 0.3), a)], [0, 0.45, 1])))
        cv.drawRoundRect(skia.Rect(fr.left() + 6, fr.top() + 5, fr.right() - 6, fr.top() + fr.height() * 0.3), 8, 8, P(col('#FFFFFF', 0.25 * a)))
    for k in range(1, 4):
        x = inner.left() + inner.width() * k / 4; cv.drawLine(x, inner.top() + 4, x, inner.bottom() - 4, P(col('#0B0C1E', 0.55 * a), stroke=5))
    cv.drawRoundRect(r, rad, rad, P(col('#FFFFFF', 0.35 * a), stroke=3))
    cv.drawLine(r.left() + rad, r.top() + 8, r.right() - rad, r.top() + 8, P(col('#FFFFFF', 0.3 * a), stroke=3, blur=2))
    if charging > 0:
        bt = skia.Path(); s = h * 0.42
        bt.moveTo(cx + s * 0.1, cy - s); bt.lineTo(cx - s * 0.45, cy + s * 0.12); bt.lineTo(cx - s * 0.02, cy + s * 0.12); bt.lineTo(cx - s * 0.15, cy + s); bt.lineTo(cx + s * 0.45, cy - s * 0.15); bt.lineTo(cx + s * 0.02, cy - s * 0.15); bt.close()
        cv.drawPath(bt, P(col('#FFF1D0', 0.6 * charging * a), blur=10)); cv.drawPath(bt, P(col('#FFFFFF', charging * a)))
    if label:
        f = font(XB, h * 0.42); s_ = f'{int(round(clamp(v) * 100))}%'
        cv.drawString(s_, cx - w * 0.03 - f.measureText(s_) / 2, bl(f, cy + h * 0.85), f, P(col(c, a)))

def fun_card(cv, kind, label, x, y, a, sc=1.0, t=0.0):
    """kartu kaca momen nongkrong: ketawa / ngobrol / foto"""
    if a <= 0: return
    cv.save(); cv.translate(x, y); cv.scale(sc, sc)
    r = skia.Rect(-120, -120, 120, 120); glass(cv, r, rad=34, a=a, glow=0.4, gc=GOLD)
    if kind == 'laugh':
        cv.drawCircle(0, -14, 54, P(col(GOLD, a)))
        m = skia.Path(); m.moveTo(-30, -6); m.quadTo(0, 40, 30, -6); m.close(); cv.drawPath(m, P(col('#4A2A10', a)))
        for s in (-1, 1):
            e = skia.Path(); e.moveTo(s * 22 - 12, -30); e.quadTo(s * 22, -42, s * 22 + 12, -30); cv.drawPath(e, P(col('#4A2A10', a), stroke=5))
    elif kind == 'chat':
        bp_, rr = bubble_path(-18, -30, 120, 64, (-50, 10)); draw_bubble(cv, bp_, rr, a, 0.4, ('#3A3D66', '#22243A'), ACC_L, ACC_L)
        bp_, rr = bubble_path(22, 22, 110, 58, (60, 60)); draw_bubble(cv, bp_, rr, a, 0.4, ('#3A2A10', '#1E1608'), GOLD, GOLD)
    else:
        cv.drawRoundRect(skia.Rect(-70, -50, 70, 40), 16, 16, P(col('#C9CBE0', a))); cv.drawRect(skia.Rect(-30, -66, 10, -50), P(col('#C9CBE0', a)))
        cv.drawCircle(0, -5, 32, P(col('#2A2C48', a))); cv.drawCircle(0, -5, 20, P(col('#7FB8FF', a)))
        fl = bump(((t * 1.3) % 1.0)); cv.drawCircle(52, -40, 14 + 30 * fl, P(col('#FFFFFF', 0.8 * fl * a), blur=8))
    f = font(XB, 30); cv.drawString(label, -f.measureText(label) / 2, bl(f, 90), f, P(col(TXT, a)))
    cv.restore()

def bed(cv, cx, y, w, a):
    if a <= 0: return
    cv.drawRoundRect(skia.Rect(cx - w / 2, y - 40, cx + w / 2, y + 40), 22, 22, P(shader=lg(0, y - 40, 0, y + 40, [col('#3A3D66', a), col('#1E1F3C', a)])))
    cv.drawRoundRect(skia.Rect(cx - w / 2 - 10, y - 140, cx - w / 2 + 30, y + 60), 14, 14, P(col('#2A2C48', a)))
    cv.drawRoundRect(skia.Rect(cx - w / 2 + 40, y - 80, cx - w / 2 + 170, y - 30), 24, 24, P(col('#E8E6F0', 0.9 * a)))
    cv.drawRoundRect(skia.Rect(cx - w / 2 + 120, y - 50, cx + w / 2 - 10, y + 10), 26, 26, P(shader=lg(0, y - 50, 0, y + 10, [col('#7F8CFF', 0.9 * a), col('#4A4FD0', 0.9 * a)])))

def big_clock(cv, cx, cy, r, a, t, ang_h, ang_m, glow=0.0):
    if a <= 0: return
    if glow > 0: cv.drawCircle(cx, cy, r * 1.2, P(col(GOLD, 0.4 * glow * a), blur=30))
    cv.drawCircle(cx, cy, r, P(shader=rg(cx - r * 0.3, cy - r * 0.3, r * 1.6, [col('#2E3150', 0.95 * a), col('#14162A', 0.95 * a)])))
    cv.drawCircle(cx, cy, r, P(col(ACC_L, 0.6 * a), stroke=4))
    for k in range(12):
        an = k * math.tau / 12; r0 = r * (0.8 if k % 3 else 0.72)
        cv.drawLine(cx + math.cos(an) * r0, cy + math.sin(an) * r0, cx + math.cos(an) * r * 0.9, cy + math.sin(an) * r * 0.9, P(col(ACC_L, 0.7 * a), stroke=4 if k % 3 else 7))
    for an, L, wd, c in ((ang_h, 0.5, 10, TXT), (ang_m, 0.75, 6, GOLD)):
        aa = math.radians(an - 90); cv.drawLine(cx, cy, cx + math.cos(aa) * r * L, cy + math.sin(aa) * r * L, P(col(c, a), stroke=wd))
    cv.drawCircle(cx, cy, 10, P(col(GOLD, a)))

FRIENDS_COL = ['#FF8A7A', '#7FB8FF', '#B57BFF', '#3FD6A4', '#FF7FC8', '#FFC56B', '#8C93FF', '#5AD1E6']


# ------------------------------------------------------------ helper EP24: hati kaca retak + kintsugi emas, keping unsur maaf, kartu kalimat rahasia
ICE = '#8FD3FF'
CRACK_MAIN = [(0, -0.38), (-0.10, -0.18), (0.08, 0.0), (-0.07, 0.2), (0.09, 0.42), (-0.04, 0.64), (0, 0.9)]
CRACK_BR = [[(-0.10, -0.18), (-0.36, -0.32), (-0.56, -0.26)], [(0.08, 0.0), (0.38, 0.06), (0.62, -0.06)],
            [(-0.07, 0.2), (-0.34, 0.3), (-0.52, 0.24)], [(0.09, 0.42), (0.3, 0.5)]]
def _poly(pts, cx, cy, s):
    p = skia.Path(); p.moveTo(cx + pts[0][0] * s, cy + pts[0][1] * s)
    for x, y in pts[1:]: p.lineTo(cx + x * s, cy + y * s)
    return p
def crack_lines(cx, cy, s):
    """retakan utama (zigzag atas -> ujung bawah) lalu cabang-cabangnya, sebagai kontur terpisah"""
    p = _poly(CRACK_MAIN, cx, cy, s)
    for br in CRACK_BR: p.addPath(_poly(br, cx, cy, s))
    return p
def _heart_body(cv, cx, cy, s, v, a, t, c):
    hp = heart_path(cx, cy, s); top, bot = cy - s * 0.85, cy + s * 0.9
    cv.drawPath(hp, P(col('#1A1430', 0.6 * a)))
    cv.save(); cv.clipPath(hp, skia.ClipOp.kIntersect, True)
    lvl = lerp(bot, top, clamp(v)); wv = skia.Path(); wv.moveTo(cx - s * 1.5, bot + 10)
    for i in range(41): wv.lineTo(cx - s * 1.5 + 3 * s * i / 40, lvl + s * 0.05 * math.sin(i * 0.5 + t * 3.5))
    wv.lineTo(cx + s * 1.5, bot + 10); wv.close()
    cv.drawPath(wv, P(shader=lg(0, lvl, 0, bot, [col(mixc(c, '#FFFFFF', 0.35), a), col(c, a), col(mixc(c, '#000000', 0.4), a)], [0, 0.4, 1])))
    cv.drawOval(skia.Rect(cx - s * 0.75, cy - s * 0.7, cx - s * 0.25, cy - s * 0.25), P(col('#FFFFFF', 0.3 * a), blur=s * 0.06))
    cv.drawRect(skia.Rect(cx - s * 1.4, cy - s, cx + s * 1.4, cy - s * 0.2), P(shader=lg(0, cy - s, 0, cy - s * 0.2, [col('#FFFFFF', 0.1 * a), col('#FFFFFF', 0)])))
    cv.restore()
    cv.drawPath(hp, P(col('#FFFFFF', 0.65 * a), stroke=3))

def crack_heart(cv, cx, cy, s, a, t, v=0.85, crack=0.0, split=0.0, gold=0.0, chill=0.0, glow=0.0, label=None):
    """hati kaca berisi cairan: bisa retak (crack 0..1), terbelah dua (split), membeku (chill) dan disambung emas ala kintsugi (gold 0..1)"""
    if a <= 0: return
    c = mixc(HOTPINK, ICE, clamp(chill)); gc = mixc(c, GOLD, clamp(gold))
    gl = glow + 0.9 * clamp(gold) ** 2
    if gl > 0: cv.drawPath(heart_path(cx, cy, s * 1.02), P(col(gc, 0.5 * clamp(gl) * a), blur=s * 0.5))
    pts = [(cx + x * s, cy + y * s) for x, y in CRACK_MAIN]
    sides = (-1, 1) if crack > 0 else (0,)
    for sd in sides:
        cv.save()
        if sd:
            half = skia.Path(); half.moveTo(*pts[0])
            for p_ in pts[1:]: half.lineTo(*p_)
            half.lineTo(cx + sd * 2 * s, cy + 1.2 * s); half.lineTo(cx + sd * 2 * s, cy - 1.4 * s); half.lineTo(pts[0][0], cy - 1.4 * s); half.close()
            cv.translate(sd * split * s * 0.22, split * s * 0.04)
            cv.translate(cx, cy + 0.9 * s); cv.rotate(sd * split * 9); cv.translate(-cx, -(cy + 0.9 * s))
            cv.clipPath(half, skia.ClipOp.kIntersect, True)
        _heart_body(cv, cx, cy, s, v, a, t, c)
        if sd:
            cl = partial(crack_lines(cx, cy, s), clamp(crack))
            cv.drawPath(cl, P(col(CORAL, 0.45 * a * (1 - clamp(gold))), stroke=7, blur=5))
            cv.drawPath(cl, P(col('#FFFFFF', 0.9 * a * (1 - 0.6 * clamp(gold))), stroke=2.4))
        cv.restore()
    if gold > 0 and crack > 0:
        gp = partial(crack_lines(cx, cy, s), clamp(gold))
        cv.drawPath(gp, P(col(GOLD, 0.8 * a), stroke=14, blur=10))
        cv.drawPath(gp, P(shader=lg(cx - s, 0, cx + s, 0, [col('#FFE9B0', a), col(GOLD, a), col('#E09A3A', a)]), stroke=6))
        cv.drawPath(gp, P(col('#FFFFFF', 0.7 * a), stroke=1.6))
    if label: mono(cv, label, cx, cy + s * 0.9 + 40, 22, mixc(gc, '#FFFFFF', 0.3), a, sp=2)

def frost(cv, a, t):
    """kristal es di sudut layar (garis bercabang, tanpa titik) + tint biru dingin"""
    if a <= 0: return
    cv.drawRect(skia.Rect(0, 0, W, H), P(col('#7FB8FF', 0.07 * a)))
    rnd = random.Random(7)
    for x0, y0, dx, dy in ((0, 250, 1, 1), (1080, 250, -1, 1), (0, 1180, 1, -1), (1080, 1180, -1, -1)):
        p = skia.Path()
        for k in range(5):
            ang = math.atan2(dy, dx) + rnd.uniform(-0.7, 0.7); L = rnd.uniform(120, 250) * eo(clamp(a))
            x1, y1 = x0 + math.cos(ang) * L, y0 + math.sin(ang) * L * 0.8
            p.moveTo(x0, y0); p.lineTo(x1, y1)
            for j in (0.35, 0.6, 0.8):
                bx, by = lerp(x0, x1, j), lerp(y0, y1, j); bl_ = L * 0.22 * (1 - j)
                for s_ in (-1, 1): p.moveTo(bx, by); p.lineTo(bx + math.cos(ang + s_ * 0.8) * bl_, by + math.sin(ang + s_ * 0.8) * bl_)
        cv.drawPath(p, P(col(ICE, 0.35 * a), stroke=5, blur=6)); cv.drawPath(p, P(col('#E8F6FF', 0.7 * a), stroke=1.8))

def thermo(cv, x, y, h, v, a, t):
    """termometer kaca SUASANA: v 1 hangat (oranye) -> 0 dingin (biru es)"""
    if a <= 0: return
    w = 34; top, bot = y - h / 2, y + h / 2; c = mixc(ICE, '#FF9A5A', clamp(v))
    halo(cv, x, bot + 20, 120, c, 0.6 * a)
    cv.drawRoundRect(skia.Rect(x - w / 2, top, x + w / 2, bot), w / 2, w / 2, P(col('#1A1B30', 0.92 * a)))
    cv.drawCircle(x, bot + 20, 36, P(col('#1A1B30', 0.92 * a)))
    lv = lerp(bot, top + 14, clamp(v))
    cv.drawRoundRect(skia.Rect(x - 9, lv, x + 9, bot + 12), 9, 9, P(col(c, a)))
    cv.drawCircle(x, bot + 20, 25, P(col(c, a))); cv.drawCircle(x, bot + 20, 40, P(col(c, 0.35 * a), blur=16))
    for k in range(5): yy = lerp(bot - 10, top + 20, k / 4); cv.drawLine(x + w / 2 + 6, yy, x + w / 2 + 22, yy, P(col(ACC_L, 0.5 * a), stroke=2))
    cv.drawRoundRect(skia.Rect(x - w / 2, top, x + w / 2, bot), w / 2, w / 2, P(col('#FFFFFF', 0.5 * a), stroke=2.5))
    cv.drawCircle(x, bot + 20, 36, P(col('#FFFFFF', 0.5 * a), stroke=2.5))
    cv.drawLine(x - 7, top + 18, x - 7, bot - 6, P(col('#FFFFFF', 0.25 * a), stroke=3))

def piece_path(w, h):
    """keping puzzle: kartu membulat + tonjolan di kanan + lekukan di kiri (pas saling mengunci)"""
    r = h * 0.17; x0, x1 = -w / 2, w / 2
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, -h / 2, x1, h / 2), 20, 20))
    k = skia.Path(); k.addCircle(x1 + r * 0.6, 0, r); p = skia.Op(p, k, skia.PathOp.kUnion_PathOp)
    n = skia.Path(); n.addCircle(x0 + r * 0.6, 0, r); p = skia.Op(p, n, skia.PathOp.kDifference_PathOp)
    return p
_PP = {}
def piece(cv, cx, cy, w, h, title, quote, a, c=ACC_L, glow=0.0, rot=0.0, sc=1.0, badge=None, depth=10):
    """keping puzzle kaca 3D berisi satu unsur permintaan maaf (judul + contoh kalimat)"""
    if a <= 0 or sc <= 0: return
    key = (round(w), round(h))
    if key not in _PP: _PP[key] = piece_path(w, h)
    pth = _PP[key]
    cv.save(); cv.translate(cx, cy); cv.rotate(rot); cv.scale(sc, sc)
    sh = skia.Path(pth); sh.offset(0, 24); cv.drawPath(sh, P(col('#000000', 0.5 * a), blur=22))
    if glow > 0: cv.drawPath(pth, P(col(c, 0.6 * clamp(glow) * a), stroke=16, blur=22))
    for k in range(depth, 0, -2):
        q = skia.Path(pth); q.offset(k * 0.35, k * 0.9); cv.drawPath(q, P(col(mixc(c, '#06070F', 0.55 + 0.3 * k / depth), a)))
    cv.drawPath(pth, P(shader=lg(0, -h / 2, 0, h / 2, [col(mixc(c, '#23253C', 0.66), a), col(mixc(c, '#101120', 0.86), a)])))
    cv.save(); cv.clipPath(pth, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(-w / 2, -h / 2, w / 2, -h * 0.05), P(shader=lg(0, -h / 2, 0, -h * 0.05, [col('#FFFFFF', 0.13 * a), col('#FFFFFF', 0)])))
    cv.restore()
    cv.drawPath(pth, P(col(c, 0.9 * a), stroke=2.5))
    ts = h * 0.25; f = font(XB, ts); tw = f.measureText(title)
    if tw > w - 76: ts *= (w - 76) / tw; f = font(XB, ts); tw = f.measureText(title)
    ty = -h * 0.13 if quote else 0
    cv.drawString(title, -tw / 2, bl(f, ty), f, P(col(mixc(c, '#FFFFFF', 0.45), a)))
    if quote:
        f2 = font(M, h * 0.19); q_ = f'“{quote}”'; qw = f2.measureText(q_)
        cv.drawString(q_, -qw / 2, bl(f2, h * 0.21), f2, P(col(TXT, 0.8 * a)))
    if badge:
        bx, by = -w / 2 + 8, -h / 2 + 6
        cv.drawCircle(bx, by, 32, P(col(c, 0.6 * a), blur=12))
        cv.drawCircle(bx, by, 29, P(shader=lg(0, by - 29, 0, by + 29, [col(mixc(c, '#FFFFFF', 0.45), a), col(c, a)])))
        fb = font(XB, 27); bw_ = fb.measureText(badge); cv.drawString(badge, bx - bw_ / 2, bl(fb, by), fb, P(col(INK, a)))
    cv.restore()

def secret_card(cv, cx, cy, w, h, num, text, a, t, reveal=0.0, glow=0.0, size=58):
    """kartu kaca emas 'KALIMAT n': teks disensor buram + gembok, lalu terbuka (reveal 0..1)"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    pth = glass(cv, r, rad=30, a=a, glow=0.4 + glow, gc=GOLD, edge=GOLD, fill=('#302A3A', '#16141F'))
    cv.drawRoundRect(r, 30, 30, P(col(GOLD, 0.85 * a), stroke=2.5))
    mono(cv, f'KALIMAT {num}', r.left() + 34, r.top() + 34, 20, GOLD, 0.9 * a, sp=3, align=0)
    f = font(XB, size); tw = f.measureText(text)
    if tw > w - 90: size *= (w - 90) / tw; f = font(XB, size); tw = f.measureText(text)
    ty = bl(f, cy + h * 0.1); rv = clamp(reveal)
    if rv < 1: cv.drawString(text, cx - tw / 2, ty, f, P(col('#FFE3B0', 0.7 * a * (1 - rv)), blur=size * 0.32 * (1 - rv) + 3))
    if rv > 0:
        cv.drawString(text, cx - tw / 2, ty, f, P(col(GOLD, 0.55 * a * rv), blur=size * 0.2))
        cv.drawString(text, cx - tw / 2, ty, f, P(shader=lg(0, ty - size * 0.8, 0, ty, [col('#FFFFFF', a * rv), col('#FFE3B0', a * rv)])))
    la = a * (1 - eio(prog(rv, 0.5, 1.0)))
    if la > 0: padlock(cv, r.right() - 48, r.top() + 50, 34, la, u=prog(rv, 0.0, 0.5))
    if 0 < rv < 1: sheen(cv, pth, r, rv, a)

def plane_icon(cv, x, y, s, a, rot=-20):
    """pesawat kertas (tombol kirim)"""
    if a <= 0: return
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    p = skia.Path(); p.moveTo(-s, -s * 0.1); p.lineTo(s, -s * 0.6); p.lineTo(-s * 0.15, s * 0.55); p.lineTo(-s * 0.35, s * 0.08); p.close()
    cv.drawPath(p, P(col(GOLD, 0.55 * a), blur=s * 0.35))
    cv.drawPath(p, P(shader=lg(0, -s, 0, s, [col('#FFFFFF', a), col('#FFE3B0', a)])))
    f_ = skia.Path(); f_.moveTo(-s * 0.35, s * 0.08); f_.lineTo(s, -s * 0.6); cv.drawPath(f_, P(col('#B8873A', a), stroke=2.5))
    cv.restore()

PIECES = [('MENYESAL', 'aku nyesel', ACC_L), ('PENJELASAN', 'tadi aku kira...', ACC_L), ('AKUI SALAH', 'itu salahku', GOLD),
          ('JANJI BERUBAH', 'nggak bakal ngulang', ACC_L), ('TAWARKAN PERBAIKAN', 'aku perbaiki, ya', MINT), ('MINTA DIMAAFKAN', 'maafin aku ya', CORAL)]
L_X, R_X, FOOT, HH = 250, 830, 1090, 320
GOLD_FILL = ('#3A3020', '#1E1A14')

def right_hero(cv, t, a, mood, tilt, glow=0.0, gc=HOTPINK, x=R_X, foot=FOOT, h=HH):
    cv.save(); cv.translate(x, foot); cv.rotate(tilt); cv.translate(-x, -foot)
    hero(cv, x, foot, h, mood, a, t, glow=glow, gc=gc); cv.restore()


# ------------------------------------------------------------ helper EP25: tim kerja kelompok, diagram lingkaran 3D yang meluap, kartu tugas, grup chat
BLUE_C = '#7FB8FF'
TEAM = [(170, GOLD, 'Aku'), (390, HOTPINK, 'Rina'), (690, MINT, 'Dimas'), (910, BLUE_C, 'Sari')]
CLAIMS = [0.5, 0.5, 0.35, 0.3]          # total 165%

def pie3d(cv, cx, cy, r, slices, a, t, tilt=0.42, depth=36, gap=34, alarm=0.0, labels=True, lsize=None):
    """diagram lingkaran 3D (elips + sisi tebal). slices: [(frac, warna)]; total boleh > 1: kelebihannya menjadi
    lapisan kedua yang melayang di atas dan berpendar merah (klaim > 100%)"""
    if a <= 0: return
    ry = r * tilt; segs = {}; acc = 0.0; best = {}
    for idx, (fr, c) in enumerate(slices):
        s0, s1 = acc, acc + max(0.0, fr); acc = s1; u = s0
        while u < s1 - 1e-6:
            L = int(math.floor(u + 1e-9)); e = min(s1, L + 1)
            segs.setdefault(L, []).append((u - L, e - L, c, idx, fr))
            if e - u > best.get(idx, (0, None))[0]: best[idx] = (e - u, L)
            u = e
    ls = lsize or max(16, r * 0.17)
    for L in sorted(segs):
        yy = cy - L * (depth + gap); ox = 7 * alarm * math.sin(t * 43) if L > 0 else 0.0; x0 = cx + ox
        if L == 0: cv.drawOval(skia.Rect(cx - r * 1.08, yy - ry + depth * 0.6, cx + r * 1.08, yy + ry * 1.25 + depth), P(col('#000000', 0.55 * a), blur=22))
        else:
            cv.drawOval(skia.Rect(x0 - r * 1.15, yy - ry * 1.2, x0 + r * 1.15, yy + ry * 1.2 + depth), P(col(CORAL, (0.3 + 0.35 * alarm) * a), blur=34))
        for u0, u1, c, idx, fr in segs[L]:                                     # sisi depan
            th0, th1 = -math.pi / 2 + math.tau * u0, -math.pi / 2 + math.tau * u1
            s0_, s1_ = max(th0, 0.0), min(th1, math.pi)
            if s1_ > s0_:
                n = max(2, int((s1_ - s0_) / 0.07)); pts = [(x0 + r * math.cos(s0_ + (s1_ - s0_) * k / n), yy + ry * math.sin(s0_ + (s1_ - s0_) * k / n)) for k in range(n + 1)]
                p = skia.Path(); p.moveTo(*pts[0])
                for q in pts[1:]: p.lineTo(*q)
                for q in reversed(pts): p.lineTo(q[0], q[1] + depth)
                p.close()
                cv.drawPath(p, P(shader=lg(0, yy, 0, yy + ry + depth, [col(mixc(c, '#000000', 0.3), a), col(mixc(c, '#000000', 0.62), a)])))
        for u0, u1, c, idx, fr in segs[L]:                                     # permukaan atas
            th0, th1 = -math.pi / 2 + math.tau * u0, -math.pi / 2 + math.tau * u1
            n = max(2, int((th1 - th0) / 0.05)); p = skia.Path(); p.moveTo(x0, yy)
            for k in range(n + 1): th = th0 + (th1 - th0) * k / n; p.lineTo(x0 + r * math.cos(th), yy + ry * math.sin(th))
            p.close()
            cv.drawPath(p, P(shader=lg(x0 - r, yy - ry, x0 + r, yy + ry, [col(mixc(c, '#FFFFFF', 0.38), a), col(c, a), col(mixc(c, '#000000', 0.18), a)], [0, 0.55, 1])))
            cv.drawPath(p, P(col('#FFFFFF', 0.4 * a), stroke=2))
            if labels and best.get(idx, (0, -1))[1] == L and (u1 - u0) >= 0.07:
                mid = (th0 + th1) / 2; f = font(XB, ls); s = f'{int(round(fr * 100))}%'; w = f.measureText(s)
                lx, ly = x0 + r * 0.6 * math.cos(mid), yy + ry * 0.6 * math.sin(mid)
                cv.drawString(s, lx - w / 2, bl(f, ly) + 2, f, P(col('#000000', 0.4 * a), blur=4)); cv.drawString(s, lx - w / 2, bl(f, ly), f, P(col(INK, 0.9 * a)))
        cv.drawOval(skia.Rect(x0 - r * 0.62, yy - ry * 0.85, x0 - r * 0.05, yy - ry * 0.35), P(col('#FFFFFF', 0.16 * a), blur=r * 0.05))
        cv.drawOval(skia.Rect(x0 - r, yy - ry, x0 + r, yy + ry), P(col('#FFFFFF', 0.28 * a), stroke=2))
        if L > 0: cv.drawOval(skia.Rect(x0 - r - 6, yy - ry - 6, x0 + r + 6, yy + ry + 6), P(col(CORAL, (0.4 + 0.5 * alarm) * a), stroke=4, blur=3))

def laptop(cv, cx, y, w, a, t, glow=0.6, text='TUGAS KELOMPOK'):
    """laptop terbuka di meja: layar bercahaya (menghadap penonton) + alas keyboard"""
    if a <= 0: return
    h = w * 0.62; scr = skia.Rect(cx - w / 2, y - h, cx + w / 2, y - 10)
    halo(cv, cx, y - h / 2, w * 0.95, ACC, 0.55 * glow * a)
    cv.drawRoundRect(scr.makeOutset(9, 9), 16, 16, P(col('#2A2C44', a)))
    cv.drawRoundRect(scr, 9, 9, P(shader=lg(0, scr.top(), 0, scr.bottom(), [col('#3E44A0', a), col('#1A1C44', a)])))
    f = font(XB, w * 0.075); tw = f.measureText(text); cv.drawString(text, cx - tw / 2, bl(f, scr.top() + h * 0.22), f, P(col(ACC_XL, 0.9 * a)))
    for k in range(3):
        cv.drawRoundRect(skia.Rect(scr.left() + 20, scr.top() + h * 0.4 + k * h * 0.15, scr.left() + 20 + (w - 40) * (0.85 - 0.22 * k), scr.top() + h * 0.4 + k * h * 0.15 + h * 0.07), 5, 5, P(col(ACC_L, 0.45 * a)))
    base = skia.Path(); base.moveTo(cx - w / 2 - 24, y - 8); base.lineTo(cx + w / 2 + 24, y - 8); base.lineTo(cx + w / 2 + 50, y + 18); base.lineTo(cx - w / 2 - 50, y + 18); base.close()
    cv.drawPath(base, P(shader=lg(0, y - 8, 0, y + 18, [col('#A0A5C8', a), col('#4A4E6A', a)])))

def team(cv, t, a, moods=None, sweat=0.0, glows=None, foot=1060, h=270, laptop_on=True, tremble=0.0):
    """empat tokoh kapsul di balik meja panjang + laptop di tengah"""
    if a <= 0: return
    for k, (x, c, nm) in enumerate(TEAM):
        hero(cv, x, foot, h, (moods[k] if moods else 'neutral'), a, t, sweat=sweat, glow=(glows[k] if glows else 0.35), gc=c, tremble=tremble)
    cv.drawOval(skia.Rect(20, foot - 34, 1060, foot + 40), P(col('#000000', 0.5 * a), blur=18))
    cv.drawOval(skia.Rect(30, foot - 30, 1050, foot + 30), P(shader=lg(0, foot - 30, 0, foot + 30, [col('#7A5A40', a), col('#3E2C1E', a)])))
    cv.drawOval(skia.Rect(30, foot - 30, 1050, foot + 30), P(col('#FFC98A', 0.25 * a), stroke=2))
    if laptop_on: laptop(cv, 540, foot - 4, 190, a, t)

def task_card(cv, text, x, y, a, lit=1.0, c=GOLD, w=340, h=84):
    """kartu tugas kaca: terang (kerjaanku, dicentang) atau gelap & buram (kerjaan orang lain, '?')"""
    if a <= 0: return
    r = skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2); cc = mixc('#4A4D66', c, lit)
    glass(cv, r, rad=22, a=a * (0.5 + 0.5 * lit), glow=0.7 * lit, gc=c, edge=cc)
    cv.drawRoundRect(r, 22, 22, P(col(cc, (0.3 + 0.6 * lit) * a), stroke=2))
    f = font(XB, 29); tx = r.left() + 74
    if lit < 1: cv.drawString(text, tx, bl(f, y), f, P(col(MUTED, 0.65 * a * (1 - lit)), blur=10 * (1 - lit) + 2))
    if lit > 0: cv.drawString(text, tx, bl(f, y), f, P(col(TXT, a * lit)))
    if lit > 0.5: check_mark(cv, r.left() + 40, y, 19, prog(lit, 0.5, 1.0), a, c)
    else:
        cv.drawCircle(r.left() + 40, y, 19, P(col(MUTED, 0.5 * a), stroke=2.5))
        fq = font(XB, 24); cv.drawString('?', r.left() + 40 - fq.measureText('?') / 2, bl(fq, y), fq, P(col(MUTED, 0.7 * a)))

def counter(cv, v, cx, cy, size, a, t, warn=0.0, ok=0.0, suffix='%'):
    """angka persen 3D besar: putih -> merah (warn, bergetar) / mint (ok)"""
    if a <= 0: return
    front = ('#FFFFFF', HL)
    if warn > 0: front = (mixc('#FFFFFF', '#FFD0C8', warn), mixc(HL, CORAL, warn))
    if ok > 0: front = (mixc(front[0], '#FFFFFF', ok), mixc(front[1], MINT, ok))
    side = mixc(mixc('#2E3270', '#5A1530', warn), '#0E4A3A', ok); gl = mixc(mixc(ACC, CORAL, warn), MINT, ok)
    sx = 6 * warn * math.sin(t * 47) * (1 - ok)
    extrude(cv, f'{int(round(v))}{suffix}', cx + sx, cy, size, a, depth=12, front=front, side=side, glow=gl)

def bar_pct(cv, x0, y, pct, a, c, label, icons, t, unit=500, endtxt=None):
    """batang persen klaim: bagian > 100% berpendar merah; ikon orang sebanyak anggota"""
    if a <= 0: return
    mono(cv, label, x0, y - 74, 22, ACC_L, a, sp=3, align=0)
    for k in range(icons): mini_person(cv, x0 + 250 + k * 44, y - 80, 15, TEAM[k % 4][1], a)
    full = x0 + unit * 1.0; xe = x0 + unit * pct
    cv.drawRoundRect(skia.Rect(x0, y - 22, x0 + unit * 1.5, y + 22), 22, 22, P(col('#1A1B30', 0.95 * a)))
    if xe > x0 + 30:
        cv.drawRoundRect(skia.Rect(x0 + 4, y - 18, min(xe, full) - 4, y + 18), 18, 18, P(shader=lg(x0, 0, full, 0, [col(mixc(c, '#FFFFFF', 0.35), a), col(c, a)])))
    if xe > full:
        cv.drawRoundRect(skia.Rect(full - 14, y - 18, xe - 4, y + 18), 18, 18, P(col(CORAL, 0.6 * a), blur=12))
        cv.drawRoundRect(skia.Rect(full - 14, y - 18, xe - 4, y + 18), 18, 18, P(shader=lg(full, 0, xe, 0, [col('#FF9A8A', a), col(CORAL, a)])))
    if endtxt: mono(cv, endtxt, xe + 18, y, 28, CORAL if xe > full + 30 else TXT, a, sp=1, align=0, glow=0.3)

GROUP_MSGS = [('wkwk ini kita banget', HOTPINK, 'Rina', 34.15), ('oke aku list kerjaan masing2 ya', MINT, 'Dimas', 34.55), ('jangan2 aku yg suka ngilang', BLUE_C, 'Sari', 34.95)]
def group_phone(cv, t, a):
    """ponsel grup chat KELOMPOK 3: video terkirim + balasan anggota"""
    if a <= 0: return
    r = skia.Rect(290, 300, 790, 1160)
    pth = glass(cv, r, rad=58, a=a, glow=0.5, fill=('#1C1E33', '#0E0F1C'))
    cv.drawRoundRect(r, 58, 58, P(col(ACC_L, 0.5 * a), stroke=3))
    cv.drawRoundRect(skia.Rect(480, 318, 600, 336), 9, 9, P(col('#05060C', a)))
    cv.drawLine(r.left() + 24, 450, r.right() - 24, 450, P(col(ACC_L, 0.2 * a), stroke=2))
    for k, (x, c, nm) in enumerate(TEAM): avatar(cv, r.left() + 64 + k * 26, 400, 22, c, a, ok=0.0)
    f = font(XB, 30); cv.drawString('KELOMPOK 3', r.left() + 190, bl(f, 388), f, P(col(TXT, a)))
    f2 = font(M, 22); cv.drawString('4 anggota · online', r.left() + 190, bl(f2, 420), f2, P(col(MUTED, a)))
    va = eo(prog(t, 33.75, 34.05))
    if va > 0:                                                                  # video yang dikirim (kanan)
        vr = skia.Rect(430, 480 + 20 * (1 - va), 760, 690 + 20 * (1 - va))
        cv.drawRoundRect(vr, 22, 22, P(shader=lg(0, vr.top(), 0, vr.bottom(), [col('#3A3F8A', va * a), col('#16183A', va * a)])))
        cv.drawRoundRect(vr, 22, 22, P(col(ACC_L, 0.5 * va * a), stroke=2))
        pie3d(cv, vr.left() + 82, vr.top() + 92, 48, [(fr, TEAM[k][1]) for k, fr in enumerate(CLAIMS)], va * a, t, depth=12, gap=12, labels=False)
        cv.drawCircle(vr.right() - 70, vr.top() + 80, 34, P(col('#FFFFFF', 0.9 * va * a)))
        tri_ = skia.Path(); cx_, cy_ = vr.right() - 66, vr.top() + 80; tri_.moveTo(cx_ - 10, cy_ - 16); tri_.lineTo(cx_ + 16, cy_); tri_.lineTo(cx_ - 10, cy_ + 16); tri_.close()
        cv.drawPath(tri_, P(col(INK, va * a)))
        f3 = font(B, 21)
        for i, ln in enumerate(('Kerja kelompok, kok aku', 'paling capek? · Ruang Pikir')):
            cv.drawString(ln, vr.left() + 20, bl(f3, vr.top() + 168 + i * 26), f3, P(col(TXT, 0.9 * va * a)))
    y = 760
    for txt, c, nm, t0 in GROUP_MSGS:                                          # balasan (kiri)
        q = prog(t, t0, t0 + 0.28)
        if q <= 0: y += 120; continue
        aa = a * clamp(q * 3); s_ = lerp(0.7, 1, bo(q)); fm = font(B, 24); lines = wrap(txt, fm, 290)
        bh = 28 + 30 * len(lines) + 26; br = skia.Rect(372, y - 20, 372 + 40 + max(fm.measureText(l) for l in lines), y - 20 + bh)
        cv.save(); cv.translate(br.left(), y); cv.scale(s_, s_); cv.translate(-br.left(), -y)
        avatar(cv, 336, y + 6, 20, c, aa, ok=0.0)
        cv.drawRoundRect(br, 20, 20, P(col('#262842', 0.95 * aa))); cv.drawRoundRect(br, 20, 20, P(col(c, 0.45 * aa), stroke=2))
        fn = font(XB, 18); cv.drawString(nm, br.left() + 20, bl(fn, y + 2), fn, P(col(c, aa)))
        for i, ln in enumerate(lines): cv.drawString(ln, br.left() + 20, bl(fm, y + 34 + i * 30), fm, P(col(TXT, aa)))
        cv.restore(); y += bh + 22
    sheen(cv, pth, r, prog(t, 33.6, 34.4), a)


# ------------------------------------------------------------ helper EP26: ikon layanan, mahkota, panel kelompok, lampu sorot
def svc_icon(cv, kind, x, y, a, t):
    """ikon layanan yang mengecewakan: pesanan telat / paket telat / antre lama"""
    if kind == 'food':
        cv.drawOval(skia.Rect(x - 62, y - 10, x + 62, y + 30), P(col('#E8E6F2', a))); cv.drawOval(skia.Rect(x - 40, y - 2, x + 40, y + 22), P(col('#C9CBE0', a)))
        cv.drawCircle(x + 40, y - 40, 26, P(col(GOLD, a))); cv.drawCircle(x + 40, y - 40, 26, P(col('#4A2A10', a), stroke=3))
        cv.drawLine(x + 40, y - 40, x + 40, y - 56, P(col('#4A2A10', a), stroke=4)); cv.drawLine(x + 40, y - 40, x + 40 + 12 * math.cos(t * 4), y - 40 + 12 * math.sin(t * 4), P(col('#4A2A10', a), stroke=4))
    elif kind == 'box':
        top = skia.Path(); top.moveTo(x, y - 60); top.lineTo(x + 52, y - 34); top.lineTo(x, y - 8); top.lineTo(x - 52, y - 34); top.close()
        cv.drawPath(top, P(col('#E2B874', a)))
        l = skia.Path(); l.moveTo(x - 52, y - 34); l.lineTo(x, y - 8); l.lineTo(x, y + 42); l.lineTo(x - 52, y + 16); l.close(); cv.drawPath(l, P(col('#C99A55', a)))
        r = skia.Path(); r.moveTo(x, y - 8); r.lineTo(x + 52, y - 34); r.lineTo(x + 52, y + 16); r.lineTo(x, y + 42); r.close(); cv.drawPath(r, P(col('#A87A3E', a)))
        cv.drawLine(x - 26, y - 47, x + 26, y - 21, P(col('#FFF3D6', 0.8 * a), stroke=6))
    else:
        for k in range(3): mini_person(cv, x - 56 + k * 52, y + 10, 22, ACC_L if k else GOLD, a)
        cv.drawLine(x - 80, y + 40, x + 80, y + 40, P(col(ACC_L, 0.4 * a), stroke=3))

def crown(cv, x, y, s, a, c=GOLD):
    if a <= 0: return
    p = skia.Path(); p.moveTo(x - s, y + s * 0.5); p.lineTo(x - s, y - s * 0.3); p.lineTo(x - s * 0.5, y + s * 0.1); p.lineTo(x, y - s * 0.6)
    p.lineTo(x + s * 0.5, y + s * 0.1); p.lineTo(x + s, y - s * 0.3); p.lineTo(x + s, y + s * 0.5); p.close()
    cv.drawPath(p, P(col(c, 0.5 * a), blur=s * 0.3)); cv.drawPath(p, P(shader=lg(0, y - s * 0.6, 0, y + s * 0.5, [col('#FFE9B0', a), col(c, a)])))
    cv.drawPath(p, P(col('#6A4A10', a), stroke=2.5))

def spot(cv, x, a, c=WARM, top=230, foot=1110, w=210):
    if a <= 0: return
    cone = skia.Path(); cone.moveTo(x - 42, top); cone.lineTo(x + 42, top); cone.lineTo(x + w, foot); cone.lineTo(x - w, foot); cone.close()
    cv.drawPath(cone, P(shader=lg(0, top, 0, foot, [col(c, 0.26 * a), col(c, 0.05 * a)])))
    cv.drawOval(skia.Rect(x - 46, top - 14, x + 46, top + 14), P(col(c, 0.9 * a)))
    cv.drawOval(skia.Rect(x - w, foot - 26, x + w, foot + 26), P(col(c, 0.16 * a), blur=10))

def group_panel(cv, x, title, text, c, a, t, happy=0.0, fill=('#2A2C48', '#171828'), fg=TXT):
    """panel kaca kelompok eksperimen: staf + kalimatnya + pelanggan"""
    if a <= 0: return
    r = skia.Rect(x - 222, 320, x + 222, 1090)
    glass(cv, r, rad=34, a=a, glow=0.35 if c == GOLD else 0.15, gc=c, edge=c)
    mono(cv, title, x, r.top() + 46, 22, c, a, sp=4)
    svc_icon(cv, 'food', x - 20, 700, a, t)
    mono(cv, 'NUNGGU LAMA', x, 770, 18, ACC_L, 0.8 * a, sp=3)
    hero(cv, x - 95, 1040, 230, 'worried' if c != GOLD else 'calm', a, t, glow=0.3, gc=c)
    hero(cv, x + 100, 1040, 210, 'happy' if happy > 0.5 else 'neutral', a, t, glow=0.6 * happy, gc=GOLD)
    say(cv, text, x, 520, 30, a, c, fill, fg, (x - 95, 800), glow=0.5 if c == GOLD else 0.2)


# ------------------------------------------------------------ helper EP27: monitor detak jantung kaca, lembar soal stres
def monitor(cv, cx, cy, w, h, a, t, rate=1.4, c=MINT, label='DETAK JANTUNG', alarm=0.0, arrow=0, amp=None):
    """monitor kaca dengan garis detak jantung berjalan; rate = kecepatan detak, arrow +1 naik / -1 turun"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    glass(cv, r, rad=26, a=a, glow=0.3 + 0.6 * alarm, gc=c, edge=c)
    for k in range(1, 6): x = r.left() + k * w / 6; cv.drawLine(x, r.top() + 56, x, r.bottom() - 16, P(col(ACC_L, 0.08 * a), stroke=1))
    for k in range(1, 4): y = r.top() + 56 + k * (h - 72) / 4; cv.drawLine(r.left() + 16, y, r.right() - 16, y, P(col(ACC_L, 0.08 * a), stroke=1))
    mono(cv, label, r.left() + 28, r.top() + 32, 18, c, a, sp=3, align=0)
    heart_big(cv, r.right() - 38, r.top() + 32, 15, a, t, rate=rate, c=c)
    cv.save(); cv.clipRect(r.makeInset(10, 10))
    p = ecg_path(r.left() + 16, r.right() - 16, cy + 20, amp or h * 0.28, t, rate)
    cv.drawPath(p, P(col(c, 0.55 * a), stroke=9, blur=6)); cv.drawPath(p, P(col(mixc(c, '#FFFFFF', 0.35), a), stroke=3.5))
    cv.restore()
    if alarm > 0: cv.drawRoundRect(r, 26, 26, P(col(c, 0.6 * alarm * a * (0.6 + 0.4 * math.sin(t * 10))), stroke=4))
    if arrow:
        ax, ay = r.right() - 44, r.bottom() - 46; d = -arrow
        tri_ = skia.Path(); tri_.moveTo(ax - 18, ay - d * 10); tri_.lineTo(ax, ay + d * 14); tri_.lineTo(ax + 18, ay - d * 10); tri_.close()
        cv.drawPath(tri_, P(col(c, a)))

def worksheet(cv, cx, cy, w, h, a, t, t0):
    """lembar soal hitungan yang bikin stres + timer melingkar"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    glass(cv, r, rad=28, a=a, glow=0.3, gc=CORAL, edge=ACC_L)
    mono(cv, 'SOAL HITUNGAN', r.left() + 36, r.top() + 38, 20, ACC_L, a, sp=3, align=0)
    f = font(XB, 40)
    for k, s in enumerate(('17 × 24 = ?', '386 − 79 = ?', '58 × 13 = ?')):
        q = prog(t, t0 + 0.15 * k, t0 + 0.15 * k + 0.25)
        if q > 0: cv.drawString(s, r.left() + 40, bl(f, r.top() + 104 + k * 62), f, P(col(TXT, a * clamp(q * 3))))
    tx, ty, tr = r.right() - 92, r.top() + 150, 56; u = prog(t, t0, t0 + 3.5)
    cv.drawCircle(tx, ty, tr, P(col('#1A1B30', 0.9 * a))); arc = skia.Path(); arc.addArc(skia.Rect(tx - tr, ty - tr, tx + tr, ty + tr), -90, 360 * (1 - u))
    cv.drawPath(arc, P(col(mixc(MINT, CORAL, u), a), stroke=10))
    sec = max(0, int(round(10 * (1 - u)))); fs = font(XB, 36); s = f'{sec}'; cv.drawString(s, tx - fs.measureText(s) / 2, bl(fs, ty), fs, P(col(TXT, a)))


# ------------------------------------------------------------ helper EP28: jempol, panel pertanyaan, kartu ide, garis waktu
def thumb(cv, x, y, s, a, c=GOLD):
    """ikon jempol (👍) sederhana"""
    if a <= 0: return
    cv.drawRoundRect(skia.Rect(x - s * 0.55, y - s * 0.1, x + s * 0.35, y + s * 0.75), s * 0.18, s * 0.18, P(col(c, a)))
    p = skia.Path(); p.moveTo(x - s * 0.15, y - s * 0.05); p.lineTo(x - s * 0.05, y - s * 0.75); p.quadTo(x + s * 0.2, y - s * 0.85, x + s * 0.2, y - s * 0.5); p.lineTo(x + s * 0.12, y - s * 0.05); p.close()
    cv.drawPath(p, P(col(c, a)))
    cv.drawRoundRect(skia.Rect(x - s * 0.85, y - s * 0.05, x - s * 0.6, y + s * 0.75), s * 0.08, s * 0.08, P(col(mixc(c, '#000000', 0.3), a)))
    for k in range(3): cv.drawLine(x - s * 0.5, y + s * (0.15 + 0.2 * k), x + s * 0.3, y + s * (0.15 + 0.2 * k), P(col(mixc(c, '#000000', 0.25), 0.6 * a), stroke=2))

def idea_card(cv, text, x, y, a, sc=1.0, rot=0.0, c=GOLD):
    """kartu ide konkret (masukan yang bisa langsung dipakai)"""
    if a <= 0: return
    f = font(B, 26); w = f.measureText(text) + 96; h = 64
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(sc, sc)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    glass(cv, r, rad=20, a=a, glow=0.5, gc=c, edge=c)
    cv.drawRoundRect(r, 20, 20, P(col(c, 0.7 * a), stroke=2))
    cv.drawCircle(r.left() + 34, 0, 14, P(col(c, a)))
    fb = font(XB, 18); cv.drawString('✓', r.left() + 34 - fb.measureText('✓') / 2, bl(fb, 0), fb, P(col(INK, a)))
    cv.drawString(text, r.left() + 62, bl(f, 0), f, P(col(TXT, a)))
    cv.restore()

def ask_panel(cv, x, title, q, c, a, t, answers, t_ans, fill=('#2A2C48', '#171828'), fg=TXT):
    """panel kelompok: pertanyaan + jawaban yang muncul"""
    if a <= 0: return
    r = skia.Rect(x - 222, 320, x + 222, 1090)
    glass(cv, r, rad=34, a=a, glow=0.35 if c == GOLD else 0.15, gc=c, edge=c)
    mono(cv, title, x, r.top() + 46, 22, c, a, sp=4)
    say(cv, q, x, 450, 32, a, c, fill, fg, (x - 90, 560), glow=0.5 if c == GOLD else 0.2)
    laptop(cv, x, 700, 200, a, t, glow=0.5, text='SLIDE')
    for k, (txt, cc) in enumerate(answers):
        q_ = prog(t, t_ans + 0.2 * k, t_ans + 0.2 * k + 0.3)
        if q_ > 0:
            f = font(B, 24); w = f.measureText(txt) + 40; y = 800 + k * 62
            rr = skia.Rect(x - w / 2, y - 24, x + w / 2, y + 24)
            cv.drawRoundRect(rr, 24, 24, P(col('#262842', 0.95 * a * clamp(q_ * 3)))); cv.drawRoundRect(rr, 24, 24, P(col(cc, 0.5 * a * clamp(q_ * 3)), stroke=2))
            cv.drawString(txt, x - w / 2 + 20, bl(f, y), f, P(col(TXT, a * clamp(q_ * 3))))

# ------------------------------------------------------------ helper EP29: ponsel chat Ibu + layar memanggil, tokoh ibu berkerudung, rumah malam, ikon telepon/email
ROSE = '#FF9EC4'; GREEN = '#3FD67A'
def ibu(cv, x, foot, h, mood='calm', a=1.0, t=0.0, glow=0.0, gc=ROSE):
    """tokoh kapsul ibu: hero + kerudung lembut yang membingkai wajah"""
    if a <= 0: return
    hx, hy, hr = hero(cv, x, foot, h, mood, a, t, glow=glow, gc=gc)
    outer = skia.Path(); outer.addCircle(hx, hy - hr * 0.04, hr * 1.2)
    dr = skia.Path(); dr.moveTo(hx - hr * 1.17, hy + hr * 0.1)
    dr.cubicTo(hx - hr * 1.3, hy + hr * 0.9, hx - hr * 1.55, hy + hr * 1.4, hx - hr * 1.42, hy + hr * 1.75)
    dr.quadTo(hx, hy + hr * 2.05, hx + hr * 1.42, hy + hr * 1.75)
    dr.cubicTo(hx + hr * 1.55, hy + hr * 1.4, hx + hr * 1.3, hy + hr * 0.9, hx + hr * 1.17, hy + hr * 0.1); dr.close()
    shape = skia.Op(outer, dr, skia.PathOp.kUnion_PathOp)
    fo = skia.Path(); fo.addOval(skia.Rect(hx - hr * 0.84, hy - hr * 0.82, hx + hr * 0.84, hy + hr * 0.88))
    shape = skia.Op(shape, fo, skia.PathOp.kDifference_PathOp)
    if shape is None: return hx, hy, hr
    if glow > 0: cv.drawPath(shape, P(col(gc, 0.35 * glow * a), blur=hr * 0.35))
    cv.drawPath(shape, P(shader=lg(0, hy - hr * 1.25, 0, hy + hr * 2.0, [col('#E9A6C8', a), col('#B5679A', a), col('#6E3766', a)], [0, 0.45, 1])))
    cv.save(); cv.clipPath(shape, skia.ClipOp.kIntersect, True)
    cv.drawOval(skia.Rect(hx - hr * 1.1, hy - hr * 1.25, hx - hr * 0.2, hy - hr * 0.6), P(col('#FFFFFF', 0.22 * a), blur=hr * 0.15))
    cv.drawOval(fo.getBounds(), P(col('#2A1030', 0.6 * a), stroke=hr * 0.12, blur=hr * 0.08))
    cv.restore()
    cv.drawPath(shape, P(col(ROSE, 0.55 * a), stroke=2.5))
    return hx, hy, hr

def handset(cv, x, y, s, a, c='#FFFFFF', rot=-25):
    """ikon gagang telepon"""
    if a <= 0: return
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    p = skia.Path(); p.addArc(skia.Rect(-s * 0.6, -s * 0.5, s * 0.6, s * 0.9), 200, 140)
    cv.drawPath(p, P(col(c, a), stroke=s * 0.2))
    for sx in (-1, 1):
        cv.drawRoundRect(skia.Rect(sx * s * 0.56 - s * 0.17, -s * 0.12, sx * s * 0.56 + s * 0.17, s * 0.26), s * 0.08, s * 0.08, P(col(c, a)))
    cv.restore()

def envelope_icon(cv, x, y, s, a, c=ACC_L):
    if a <= 0: return
    r = skia.Rect(x - s * 0.7, y - s * 0.45, x + s * 0.7, y + s * 0.45)
    cv.drawRoundRect(r, s * 0.1, s * 0.1, P(col(c, 0.2 * a)))
    cv.drawRoundRect(r, s * 0.1, s * 0.1, P(col(c, a), stroke=s * 0.08))
    p = skia.Path(); p.moveTo(r.left() + s * 0.08, r.top() + s * 0.1); p.lineTo(x, y + s * 0.1); p.lineTo(r.right() - s * 0.08, r.top() + s * 0.1)
    cv.drawPath(p, P(col(c, a), stroke=s * 0.08))

def stopwatch(cv, x, y, r, a, run=0.0, c=ACC_L):
    if a <= 0: return
    cv.drawRoundRect(skia.Rect(x - r * 0.18, y - r * 1.38, x + r * 0.18, y - r * 1.06), r * 0.06, r * 0.06, P(col(c, a)))
    cv.drawCircle(x, y, r, P(col('#1A1B30', 0.95 * a))); cv.drawCircle(x, y, r, P(col(c, a), stroke=r * 0.13))
    ang = math.radians(-90 + 360 * run)
    cv.drawLine(x, y, x + math.cos(ang) * r * 0.66, y + math.sin(ang) * r * 0.66, P(col(c, a), stroke=r * 0.12))
    cv.drawCircle(x, y, r * 0.1, P(col(c, a)))

def moon(cv, x, y, r, a):
    if a <= 0: return
    halo(cv, x, y, r * 3.2, '#FFE9B8', 0.3 * a)
    p1 = skia.Path(); p1.addCircle(x, y, r); p2 = skia.Path(); p2.addCircle(x + r * 0.48, y - r * 0.25, r * 0.88)
    cr = skia.Op(p1, p2, skia.PathOp.kDifference_PathOp)
    if cr is None: return
    cv.drawPath(cr, P(col('#FFE9B8', 0.5 * a), blur=r * 0.3))
    cv.drawPath(cr, P(shader=lg(x - r, y - r, x + r, y + r, [col('#FFF6DA', a), col('#FFD98A', a)])))

def house(cv, cx, base, w, a, t, lit=1.0):
    """rumah orang tua di malam hari: dinding, atap, dua jendela menyala hangat, pintu"""
    if a <= 0: return
    wh = w * 0.42; wt = base - wh
    halo(cv, cx, base - wh * 0.5, w * 0.85, WARM, 0.22 * lit * a)
    roof = skia.Path(); roof.moveTo(cx - w * 0.52, wt + 6); roof.lineTo(cx, wt - w * 0.3); roof.lineTo(cx + w * 0.52, wt + 6); roof.close()
    cv.drawPath(roof, P(col('#000000', 0.5 * a), blur=18))
    wall = skia.Rect(cx - w * 0.41, wt, cx + w * 0.41, base)
    cv.drawRect(wall, P(shader=lg(0, wt, 0, base, [col('#33355A', a), col('#1B1C32', a)])))
    cv.drawRect(wall, P(col(ACC_L, 0.35 * a), stroke=2.5))
    cv.drawPath(roof, P(shader=lg(0, wt - w * 0.3, 0, wt, [col('#4A3A5E', a), col('#251C34', a)])))
    cv.drawPath(roof, P(col(ACC_L, 0.4 * a), stroke=2.5))
    for sx in (-1, 1):
        r = skia.Rect(cx + sx * w * 0.24 - w * 0.085, wt + wh * 0.2, cx + sx * w * 0.24 + w * 0.085, wt + wh * 0.2 + w * 0.15)
        cv.drawRect(r, P(col(WARM, 0.6 * lit * a), blur=22))
        cv.drawRect(r, P(shader=lg(0, r.top(), 0, r.bottom(), [col('#FFE3B0', (0.25 + 0.75 * lit) * a), col('#FFB86B', (0.2 + 0.7 * lit) * a)])))
        cv.drawLine(r.centerX(), r.top(), r.centerX(), r.bottom(), P(col('#3A2A20', a), stroke=4))
        cv.drawLine(r.left(), r.centerY(), r.right(), r.centerY(), P(col('#3A2A20', a), stroke=4))
        cv.drawRect(r, P(col('#3A2A20', a), stroke=5))
    d = skia.Rect(cx - w * 0.07, base - wh * 0.56, cx + w * 0.07, base)
    cv.drawRect(d, P(shader=lg(0, d.top(), 0, d.bottom(), [col('#4A3424', a), col('#2A1C14', a)])))
    cv.drawCircle(d.right() - w * 0.022, d.centerY(), w * 0.008, P(col(GOLD, a)))

def mini_phone(cv, x, y, s, a, t, ring=0.0, call=0.0, rot=0.0):
    """ponsel kecil di tangan tokoh; ring = bergetar + gelombang dering, call = layar hijau tersambung"""
    if a <= 0: return
    if ring > 0:
        for k in range(2):
            u = (t * 1.6 + k * 0.5) % 1.0
            cv.drawCircle(x, y, s * (0.6 + 0.7 * u), P(col(GREEN, 0.5 * (1 - u) * ring * a), stroke=3))
    cv.save(); cv.translate(x + ring * 3 * math.sin(t * 60), y); cv.rotate(rot + ring * 5 * math.sin(t * 47))
    w, h = s * 0.58, s; r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    cv.drawRoundRect(r.makeOffset(0, 8), w * 0.2, w * 0.2, P(col('#000000', 0.5 * a), blur=10))
    cv.drawRoundRect(r, w * 0.2, w * 0.2, P(shader=lg(-w / 2, -h / 2, w / 2, h / 2, [col('#6A6E8E', a), col('#1A1B2A', a), col('#4A4D68', a)])))
    sr = r.makeInset(w * 0.08, w * 0.08)
    cv.drawRoundRect(sr, w * 0.13, w * 0.13, P(shader=lg(0, sr.top(), 0, sr.bottom(), [col(mixc('#2A2870', '#35B870', call), a), col(mixc('#121236', '#145A36', call), a)])))
    if call > 0.05 or ring > 0.05: handset(cv, 0, 0, w * 0.42, a * max(call, ring), '#FFFFFF')
    cv.restore()

def msg(cv, edge, y, text, size, a, side, fill, strike=0.0, fg=TXT):
    """gelembung chat (side 'L' rata kiri dari edge, 'R' rata kanan)"""
    if a <= 0: return
    f = font(B, size); w = f.measureText(text) + size * 1.3; h = size * 1.9
    x0 = edge if side == 'L' else edge - w
    r = skia.Rect(x0, y - h / 2, x0 + w, y + h / 2)
    cv.drawRoundRect(r, h * 0.42, h * 0.42, P(col(fill, a)))
    cv.drawString(text, x0 + size * 0.65, bl(f, y), f, P(col(fg, a)))
    if strike > 0:
        cv.drawLine(x0 + 8, y + 3, x0 + 8 + (w - 16) * eo(strike), y - 3, P(col(CORAL, 0.6 * a), stroke=14, blur=6))
        cv.drawLine(x0 + 8, y + 3, x0 + 8 + (w - 16) * eo(strike), y - 3, P(col('#FFFFFF', a), stroke=5))

def chat_phone2(cv, cx, cy, w, h, a, t, msgs, call=0.0, ring=0.0, glow=0.0):
    """ponsel kaca: chat dengan Ibu (msgs: (side, text, t0, t_strike)); call 0..1 berganti ke layar 'Memanggil Ibu...'"""
    if a <= 0: return
    cv.save(); cv.translate(cx, cy)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2); rad = w * 0.13
    if glow > 0: cv.drawRRect(RR(r, rad), P(col(mixc(ACC, GREEN, call), 0.55 * glow * a), stroke=18, blur=34))
    cv.drawRRect(RR(r.makeOffset(0, 36), rad), P(col('#000000', 0.6 * a), blur=46))
    cv.drawRRect(RR(r, rad), P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col('#6A6E8E', a), col('#1A1B2A', a), col('#4A4D68', a), col('#15161F', a)], [0, 0.35, 0.7, 1])))
    sr = r.makeInset(w * 0.035, w * 0.035); srad = rad * 0.8
    cv.drawRRect(RR(sr, srad), P(col('#04050A', a)))
    cv.save(); cv.clipRRect(RR(sr, srad), skia.ClipOp.kIntersect, True)
    cv.drawRect(sr, P(shader=lg(0, sr.top(), 0, sr.bottom(), [col('#1C1A48', a), col('#100F2A', a), col('#0A0A18', a)], [0, 0.5, 1])))
    ca = a * (1 - eio(clamp(call)))
    if ca > 0:
        hh = h * 0.11; hy = sr.top() + w * 0.08 + hh / 2
        cv.drawRect(skia.Rect(sr.left(), sr.top(), sr.right(), hy + hh / 2), P(col('#1E1F3C', 0.95 * ca)))
        cv.drawLine(sr.left(), hy + hh / 2, sr.right(), hy + hh / 2, P(col(ACC_L, 0.15 * ca), stroke=2))
        av = hh * 0.36; ax = sr.left() + w * 0.12
        cv.drawCircle(ax, hy, av, P(shader=lg(0, hy - av, 0, hy + av, [col('#FFC2DC', ca), col('#E07AAA', ca)])))
        fa = font(XB, av); cv.drawString('I', ax - fa.measureText('I') / 2, bl(fa, hy), fa, P(col(INK, ca)))
        f1 = font(XB, w * 0.07); f2 = font(M, w * 0.042)
        cv.drawString('Ibu', ax + av * 1.5, bl(f1, hy - hh * 0.15), f1, P(col(TXT, ca)))
        cv.drawString('online', ax + av * 1.5, bl(f2, hy + hh * 0.22), f2, P(col(MINT, ca)))
        handset(cv, sr.right() - w * 0.1, hy, w * 0.07, ca * (0.6 + 0.4 * glow), GREEN if glow > 0 else ACC_L)
        y = hy + hh / 2 + h * 0.09; fs = w * 0.078
        for side, txt, t0, ts in msgs:
            q = prog(t, t0, t0 + 0.25)
            if q > 0:
                yy = y + (1 - eo(q)) * 18
                msg(cv, sr.left() + w * 0.05 if side == 'L' else sr.right() - w * 0.05, yy, txt, fs, ca * clamp(q * 3), side,
                    '#34365A' if side == 'L' else '#4B53D6', strike=prog(t, ts, ts + 0.3) if ts else 0.0)
            y += fs * 2.3
        dq = prog(t, 2.95, 3.15)
        if dq > 0:
            f3 = font(M, w * 0.036); s3 = 'Dibaca 21.04'; cv.drawString(s3, sr.right() - w * 0.05 - f3.measureText(s3), bl(f3, y - fs * 0.9), f3, P(col(MUTED, ca * dq)))
        iy = sr.bottom() - h * 0.07; ih = h * 0.065; ir = skia.Rect(sr.left() + w * 0.05, iy - ih / 2, sr.right() - w * 0.05, iy + ih / 2)
        cv.drawRoundRect(ir, ih / 2, ih / 2, P(col('#24264A', ca))); cv.drawRoundRect(ir, ih / 2, ih / 2, P(col(ACC_L, 0.25 * ca), stroke=2))
        fi = font(M, w * 0.045); cv.drawString('Ketik pesan', ir.left() + ih * 0.5, bl(fi, iy), fi, P(col(MUTED, 0.7 * ca)))
    if call > 0:
        k = eio(clamp(call)); A = a * k; ay = sr.top() + h * 0.3; ar = w * 0.17
        for j in range(3):
            u = (t * 0.9 + j / 3) % 1.0
            cv.drawCircle(0, ay, ar * (1 + 0.9 * u), P(col(GREEN, 0.45 * (1 - u) * A * ring), stroke=3))
        cv.drawCircle(0, ay, ar, P(shader=lg(0, ay - ar, 0, ay + ar, [col('#FFC2DC', A), col('#E07AAA', A)])))
        fa = font(XB, ar * 0.9); cv.drawString('I', -fa.measureText('I') / 2, bl(fa, ay), fa, P(col(INK, A)))
        f1 = font(XB, w * 0.1); f2 = font(M, w * 0.05)
        cv.drawString('Ibu', -f1.measureText('Ibu') / 2, bl(f1, ay + ar * 1.6), f1, P(col(TXT, A)))
        st = 'Memanggil' + '.' * (1 + int(t * 3) % 3)
        cv.drawString(st, -f2.measureText('Memanggil...') / 2, bl(f2, ay + ar * 2.3), f2, P(col(MUTED, A)))
        by = sr.bottom() - h * 0.12; br = w * 0.1
        cv.drawCircle(0, by, br * (1 + 0.08 * math.sin(t * 8)), P(col(GREEN, 0.5 * A), blur=14))
        cv.drawCircle(0, by, br, P(col(GREEN, A)))
        handset(cv, 0, by, br * 0.8, A, '#FFFFFF')
    cv.restore()
    cv.drawRoundRect(skia.Rect(-w * 0.12, sr.top() + w * 0.025, w * 0.12, sr.top() + w * 0.06), 8, 8, P(col('#000000', a)))
    cv.restore()

def secret_card2(cv, cx, cy, w, h, label, lines, a, t, reveal=0.0, glow=0.0, size=54):
    """kartu kaca emas dua baris: teks disensor buram + gembok, lalu terbuka (reveal 0..1)"""
    if a <= 0: return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    pth = glass(cv, r, rad=30, a=a, glow=0.4 + glow, gc=GOLD, edge=GOLD, fill=('#302A3A', '#16141F'))
    cv.drawRoundRect(r, 30, 30, P(col(GOLD, 0.85 * a), stroke=2.5))
    mono(cv, label, r.left() + 34, r.top() + 34, 20, GOLD, 0.9 * a, sp=3, align=0)
    f = font(XB, size); mw = max(f.measureText(s) for s in lines)
    if mw > w - 90: size *= (w - 90) / mw; f = font(XB, size)
    lh = size * 1.2; y0 = cy + h * 0.1 - (len(lines) - 1) * lh / 2; rv = clamp(reveal)
    for i, s in enumerate(lines):
        tw = f.measureText(s); ty = bl(f, y0 + i * lh)
        if rv < 1: cv.drawString(s, cx - tw / 2, ty, f, P(col('#FFE3B0', 0.7 * a * (1 - rv)), blur=size * 0.32 * (1 - rv) + 3))
        if rv > 0:
            cv.drawString(s, cx - tw / 2, ty, f, P(col(GOLD, 0.55 * a * rv), blur=size * 0.2))
            cv.drawString(s, cx - tw / 2, ty, f, P(shader=lg(0, ty - size * 0.8, 0, ty, [col('#FFFFFF', a * rv), col('#FFE3B0', a * rv)])))
    la = a * (1 - eio(prog(rv, 0.5, 1.0)))
    if la > 0: padlock(cv, r.right() - 48, r.top() + 50, 34, la, u=prog(rv, 0.0, 0.5))
    if 0 < rv < 1: sheen(cv, pth, r, rv, a)

def ghost_bar(cv, x0, x1, y, v, a, c):
    """batang bayangan putus-putus (yang 'dikira')"""
    if a <= 0 or v <= 0.02: return
    xv = x0 + (x1 - x0) * clamp(v)
    cv.drawRoundRect(skia.Rect(x0 + 4, y - 12, xv - 4, y + 12), 12, 12, P(col(c, 0.12 * a)))
    cv.drawRoundRect(skia.Rect(x0 + 4, y - 12, xv - 4, y + 12), 12, 12, P(col(c, 0.75 * a), stroke=2.5, effect=skia.DashPathEffect.Make([12, 9], 0)))

LINE1 = ['Nggak ada apa-apa,', 'cuma kangen denger suara Ibu.']
CHAT = [('L', 'Nak, udah makan?', 0.2, None), ('L', 'Kapan pulang?', 0.65, None), ('R', 'iya', 2.17, 3.05), ('R', 'udah', 2.75, 3.15)]

# ------------------------------------------------------------ helper EP31: suara Ibu vs suara baru — busur suara, kenop radio, headphone, MRI, pusat rasa senang
BLUE = '#7FB8FF'
ORB_ROSE = ('#FFE6F1', ROSE, '#8A3A66'); ORB_BLUE = ('#E6F2FF', BLUE, '#2A4A8A'); ORB_DIM = ('#5A5C7A', '#33354F', '#1A1B2A')
def mix3(c1, c2, u): return tuple(mixc(x, y, clamp(u)) for x, y in zip(c1, c2))

def voice_arcs(cv, x, y, dirx, a, t, c=ROSE, n=3, r0=26, step=30, spd=1.3, w=5):
    """busur suara yang mengalir dari mulut ke arah dirx (+1 kanan, -1 kiri)"""
    if a <= 0: return
    for k in range(n):
        u = ((t * spd) + k / n) % 1.0; r = r0 + step * n * u
        p = skia.Path(); p.addArc(skia.Rect(x - r, y - r, x + r, y + r), -40 if dirx > 0 else 140, 80)
        cv.drawPath(p, P(col(c, 0.85 * a * (1 - u)), stroke=w))

def joy_orb(cv, x, y, r, a, t, cols, lit=1.0, label=None):
    """bola 'pusat rasa senang' yang menyala (lit 0..1) dengan sinar"""
    if a <= 0: return
    if lit > 0.05:
        rays(cv, x, y, r * 3.2, 0.7 * lit * a, t, n=12, c=cols[1], spin=12)
        halo(cv, x, y, r * 2.6, cols[1], 0.8 * lit * a)
    sphere(cv, x, y, r * (1 + 0.06 * lit * math.sin(t * 6)), mix3(ORB_DIM, cols, lit), a, glow=0.3 + 0.7 * lit)
    if label: mono(cv, label, x, y + r + 28, 16, mixc(MUTED, cols[1], lit), a, sp=2)

def dial(cv, cx, cy, r, v, a, t, static=0.0):
    """kenop radio kaca: v 0 = SUARA IBU (kiri, merah muda), 1 = SUARA BARU (kanan, biru)"""
    if a <= 0: return
    rr = skia.Rect(cx - r * 1.55, cy - r * 1.05, cx + r * 1.55, cy + r * 0.62)
    glass(cv, rr, rad=30, a=a, glow=0.3, gc=mixc(ROSE, BLUE, v), edge=mixc(ROSE, BLUE, v))
    sc = skia.Path(); sc.addArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), 200, 140)
    cv.drawPath(sc, P(shader=lg(cx - r, 0, cx + r, 0, [col(ROSE, 0.9 * a), col('#B57BFF', 0.7 * a), col(BLUE, 0.9 * a)]), stroke=10))
    for k in range(15):
        ang = math.radians(200 + k * 10); r1 = r * (0.8 if k % 7 == 0 else 0.86)
        cv.drawLine(cx + math.cos(ang) * r1, cy + math.sin(ang) * r1, cx + math.cos(ang) * r * 0.93, cy + math.sin(ang) * r * 0.93, P(col(ACC_XL, 0.5 * a), stroke=2.5))
    jit = static * 6 * math.sin(t * 70)
    ang = math.radians(lerp(205, 335, clamp(v)) + jit); nc = mixc(ROSE, BLUE, v)
    cv.drawLine(cx, cy, cx + math.cos(ang) * r * 0.9, cy + math.sin(ang) * r * 0.9, P(col(nc, 0.6 * a), stroke=12, blur=8))
    cv.drawLine(cx, cy, cx + math.cos(ang) * r * 0.9, cy + math.sin(ang) * r * 0.9, P(col('#FFFFFF', a), stroke=5))
    cv.drawCircle(cx, cy, r * 0.16, P(shader=rg(cx - 6, cy - 6, r * 0.2, [col('#8A8EAE', a), col('#2A2C48', a)])))
    mono(cv, 'SUARA IBU', cx - r * 0.95, cy + r * 0.32, 18, ROSE, a * (1 - 0.5 * v), sp=2)
    mono(cv, 'SUARA BARU', cx + r * 0.95, cy + r * 0.32, 18, BLUE, a * (0.5 + 0.5 * v), sp=2)

def headphones(cv, hx, hy, hr, a, c=BLUE, glow=0.0):
    if a <= 0: return
    band = skia.Path(); band.addArc(skia.Rect(hx - hr * 1.2, hy - hr * 1.32, hx + hr * 1.2, hy + hr * 1.08), 180, 180)
    cv.drawPath(band, P(col('#1E2036', a), stroke=hr * 0.18)); cv.drawPath(band, P(col(c, 0.75 * a), stroke=hr * 0.05))
    for s in (-1, 1):
        r = skia.Rect(hx + s * hr * 1.12 - hr * 0.2, hy - hr * 0.3, hx + s * hr * 1.12 + hr * 0.2, hy + hr * 0.36)
        if glow > 0: cv.drawRoundRect(r, hr * 0.16, hr * 0.16, P(col(c, 0.6 * glow * a), blur=hr * 0.3))
        cv.drawRoundRect(r, hr * 0.16, hr * 0.16, P(shader=lg(0, r.top(), 0, r.bottom(), [col('#4A4E7A', a), col('#191A2C', a)])))
        cv.drawRoundRect(r, hr * 0.16, hr * 0.16, P(col(c, 0.8 * a), stroke=2.5))

def mri(cv, cx, cy, R, a, t):
    """pemindai fMRI: cincin kaca besar, kepala profil di dalam, garis pindai bergerak"""
    if a <= 0: return
    cv.drawCircle(cx, cy + 30, R * 1.02, P(col('#000000', 0.55 * a), blur=40))
    cv.drawCircle(cx, cy, R * 0.81, P(col(ACC, 0.35 * a), stroke=R * 0.38, blur=30))
    cv.drawCircle(cx, cy, R * 0.81, P(shader=rg(cx - R * 0.4, cy - R * 0.5, R * 1.6, [col('#5A5E8E', a), col('#272944', a), col('#121322', a)], [0, 0.5, 1]), stroke=R * 0.38))
    cv.drawCircle(cx, cy, R * 0.62, P(col('#05060E', 0.92 * a)))
    cv.drawCircle(cx, cy, R * 0.62, P(col(ACC_L, 0.6 * a), stroke=3)); cv.drawCircle(cx, cy, R, P(col(ACC_L, 0.35 * a), stroke=2.5))
    cl = skia.Path(); cl.addCircle(cx, cy, R * 0.6); cv.save(); cv.clipPath(cl, skia.ClipOp.kIntersect, True)
    head_solid(cv, cx + 10, cy + 20, R * 0.0016, a, face=1, rim=ACC_L)
    sy = cy + math.sin(t * 2.2) * R * 0.5
    cv.drawRect(skia.Rect(cx - R, sy - 3, cx + R, sy + 3), P(col(MINT, 0.9 * a)))
    cv.drawRect(skia.Rect(cx - R, sy - 40, cx + R, sy), P(shader=lg(0, sy - 40, 0, sy, [col(MINT, 0), col(MINT, 0.25 * a)])))
    cv.restore()
    for k in range(6):
        ang = math.radians(k * 60 + t * 20); x = cx + math.cos(ang) * R * 0.81; y = cy + math.sin(ang) * R * 0.81
        cv.drawCircle(x, y, 6, P(col(MINT, 0.8 * a)))

def city(cv, x0, x1, base, a, t):
    """kota malam di luar rumah: gedung dengan jendela menyala"""
    if a <= 0: return
    rnd = random.Random(7); x = x0
    while x < x1:
        w = rnd.randint(70, 110); h = rnd.randint(160, 330)
        r = skia.Rect(x, base - h, x + w - 10, base)
        cv.drawRect(r, P(shader=lg(0, r.top(), 0, base, [col('#2A2D55', a), col('#15162A', a)])))
        cv.drawRect(r, P(col(BLUE, 0.3 * a), stroke=2))
        for j in range(int(h // 42)):
            for i in range(int((w - 30) // 26)):
                if rnd.random() < 0.55:
                    c = BLUE if rnd.random() < 0.5 else WARM
                    cv.drawRect(skia.Rect(x + 12 + i * 26, base - h + 18 + j * 42, x + 26 + i * 26, base - h + 34 + j * 42), P(col(c, (0.35 + 0.25 * math.sin(t * 2 + i + j)) * a)))
        x += w

def vbar(cv, x, base, hgt, a, c, label, sub=None):
    """batang vertikal kedekatan (tanpa angka)"""
    if a <= 0: return
    r = skia.Rect(x - 70, base - hgt, x + 70, base)
    if hgt > 4:
        cv.drawRoundRect(r, 22, 22, P(col(c, 0.45 * a), blur=18))
        cv.drawRoundRect(r, 22, 22, P(shader=lg(0, r.top(), 0, r.bottom(), [col(mixc(c, '#FFFFFF', 0.35), a), col(mixc(c, '#000000', 0.25), a)])))
        hp = skia.Path(); hp.addRRect(RR(r, 22)); cv.save(); cv.clipPath(hp, skia.ClipOp.kIntersect, True)
        cv.drawRect(skia.Rect(r.left(), r.top(), r.left() + 40, r.bottom()), P(col('#FFFFFF', 0.12 * a))); cv.restore()
    mono(cv, label, x, base + 34, 19, c, a, sp=2)
    if sub: mono(cv, sub, x, base + 62, 16, MUTED, a, sp=2)

def share_card_text(cv, s, r, a, maxsize=62):
    f = font(XB, maxsize); w = f.measureText(s); size = maxsize
    if w > r.width() - 108: size = maxsize * (r.width() - 108) / w; f = font(XB, size)
    y = bl(f, r.top() + 122); x = r.left() + 54
    cv.drawString(s, x, y, f, P(col(GOLD, 0.45 * a), blur=10)); cv.drawString(s, x, y, f, P(shader=lg(0, y - 50, 0, y, [col('#FFFFFF', a), col('#FFE3B0', a)])))

PENELITI = ['Otakmu lagi', 'latihan mandiri.']

# ------------------------------------------------------------ helper EP32: ponsel IG mantan, foto mantan, otak ketagihan, hati patah, kartu cara
ORB_RED = ('#FFE0DA', CORAL, '#7A1E2A')
TRIK = ['Ingat kebiasaan dia', 'yang nyebelin.']

def broken_heart(cv, cx, cy, s, a, split=0.0, c=CORAL):
    """hati yang retak dan terbelah (split 0..1)"""
    if a <= 0: return
    hp = heart_path(cx, cy, s)
    crack = skia.Path(); crack.moveTo(cx, cy - s * 0.55)
    for k, (dx, dy) in enumerate(((-0.12, -0.25), (0.1, 0.0), (-0.1, 0.3), (0.06, 0.6), (0.0, 0.95))): crack.lineTo(cx + dx * s, cy + dy * s)
    for side in (-1, 1):
        cv.save(); cv.translate(cx + side * s * 0.18 * split, cy + s * 0.08 * split); cv.rotate(side * 8 * split); cv.translate(-cx, -cy)
        half = skia.Path(); r = skia.Rect(cx - s * 2, cy - s * 2, cx, cy + s * 2) if side < 0 else skia.Rect(cx, cy - s * 2, cx + s * 2, cy + s * 2)
        cv.save(); cv.clipRect(r)
        cv.drawPath(hp, P(col(c, 0.5 * a), blur=s * 0.4)); cv.drawPath(hp, P(shader=lg(0, cy - s, 0, cy + s, [col(mixc(c, '#FFFFFF', 0.4), a), col(c, a)])))
        cv.restore(); cv.restore()
    if split < 0.95: cv.drawPath(crack, P(col('#1A0A10', a * (1 - split)), stroke=max(2, s * 0.08)))

def ex_avatar(cv, x, y, r, a, ring=True):
    """avatar 'dia' dengan cincin story bergradasi"""
    if a <= 0: return
    if ring: cv.drawCircle(x, y, r * 1.18, P(shader=lg(x - r, y - r, x + r, y + r, [col('#FFC56B', a), col(HOTPINK, a), col('#B57BFF', a)]), stroke=r * 0.12))
    avatar(cv, x, y, r, '#FF8A9A', a, ok=0.0)

def ig_phone(cv, cx, cy, w, h, a, t, scroll=0.0, xmark=0.0, glow=0.0):
    """ponsel kaca berisi profil medsos 'dia' + grid foto yang digulir; xmark = silang merah STOP"""
    if a <= 0: return
    cv.save(); cv.translate(cx, cy)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2); rad = w * 0.13
    if glow > 0: cv.drawRRect(RR(r, rad), P(col(CORAL, 0.5 * glow * a), stroke=16, blur=32))
    cv.drawRRect(RR(r.makeOffset(0, 36), rad), P(col('#000000', 0.6 * a), blur=46))
    cv.drawRRect(RR(r, rad), P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col('#6A6E8E', a), col('#1A1B2A', a), col('#4A4D68', a), col('#15161F', a)], [0, 0.35, 0.7, 1])))
    sr = r.makeInset(w * 0.035, w * 0.035); srad = rad * 0.8
    cv.drawRRect(RR(sr, srad), P(col('#04050A', a)))
    cv.save(); cv.clipRRect(RR(sr, srad), skia.ClipOp.kIntersect, True)
    cv.drawRect(sr, P(shader=lg(0, sr.top(), 0, sr.bottom(), [col('#1C1A48', a), col('#100F2A', a)])))
    top = sr.top() + w * 0.1
    f1 = font(XB, w * 0.065); cv.drawString('<', sr.left() + w * 0.05, bl(f1, top), f1, P(col(ACC_L, a)))
    cv.drawString('dia', -f1.measureText('dia') / 2, bl(f1, top), f1, P(col(TXT, a)))
    ay = top + w * 0.2; ex_avatar(cv, sr.left() + w * 0.2, ay, w * 0.1, a)
    fs = font(XB, w * 0.05); fm = font(M, w * 0.032)
    for k, (n, lab) in enumerate((('128', 'post'), ('2.041', 'pengikut'), ('530', 'mengikuti'))):
        x = sr.left() + w * (0.45 + k * 0.17)
        cv.drawString(n, x - fs.measureText(n) / 2, bl(fs, ay - w * 0.02), fs, P(col(TXT, a)))
        cv.drawString(lab, x - fm.measureText(lab) / 2, bl(fm, ay + w * 0.05), fm, P(col(MUTED, a)))
    gy0 = ay + w * 0.2; cs = (sr.width() - 8) / 3
    cv.save(); cv.clipRect(skia.Rect(sr.left(), gy0, sr.right(), sr.bottom()))
    off = (scroll * cs) % (cs + 4)
    rnd = random.Random(3)
    tones = [('#FF9A8A', '#6A3A8A'), ('#FFC56B', '#B5476A'), ('#7FB8FF', '#3A3A8A'), ('#3FD6A4', '#2A4A6A'), ('#FF7FC8', '#4A2A6A')]
    for row in range(-1, 8):
        for c_ in range(3):
            idx = (row + int(scroll)) * 3 + c_
            t0, t1 = tones[(idx * 7 + 3) % len(tones)]
            x = sr.left() + c_ * (cs + 4); y = gy0 + row * (cs + 4) - off
            tr = skia.Rect(x, y, x + cs, y + cs)
            cv.drawRect(tr, P(shader=lg(x, y, x + cs, y + cs, [col(t0, 0.85 * a), col(t1, 0.85 * a)])))
            kind = (idx * 5 + 1) % 3
            if kind == 0: heart_shape(cv, x + cs / 2, y + cs / 2, cs * 0.16, 0.8 * a, '#FFFFFF')
            elif kind == 1:
                cv.drawCircle(x + cs * 0.38, y + cs * 0.45, cs * 0.12, P(col('#FFFFFF', 0.75 * a))); cv.drawCircle(x + cs * 0.62, y + cs * 0.45, cs * 0.12, P(col('#FFFFFF', 0.75 * a)))
                cv.drawRoundRect(skia.Rect(x + cs * 0.24, y + cs * 0.6, x + cs * 0.76, y + cs * 0.85), cs * 0.1, cs * 0.1, P(col('#FFFFFF', 0.6 * a)))
            else:
                cv.drawCircle(x + cs * 0.7, y + cs * 0.3, cs * 0.1, P(col('#FFF3C0', 0.85 * a)))
                mp = skia.Path(); mp.moveTo(x, y + cs); mp.lineTo(x + cs * 0.35, y + cs * 0.5); mp.lineTo(x + cs * 0.6, y + cs * 0.75); mp.lineTo(x + cs * 0.8, y + cs * 0.55); mp.lineTo(x + cs, y + cs); mp.close()
                cv.drawPath(mp, P(col('#FFFFFF', 0.45 * a)))
    cv.restore(); cv.restore()
    cv.drawRoundRect(skia.Rect(-w * 0.12, sr.top() + w * 0.025, w * 0.12, sr.top() + w * 0.06), 8, 8, P(col('#000000', a)))
    if xmark > 0:
        cv.drawRRect(RR(sr, srad), P(col('#3A0A14', 0.55 * xmark * a)))
        cross(cv, 0, 0, w * 0.28 * lerp(1.4, 1, eo(xmark)), a * xmark, CORAL, w * 0.07)
        stamp(cv, 'STOP', 0, h * 0.28, w * 0.13, t, t - 1.0 if xmark >= 1 else t - 0.22 * xmark, c=CORAL, rot=-10, a=a * xmark)
    cv.restore()

def ex_photo(cv, x, y, w, a, rot=-6, t=0.0, glow=0.0):
    """foto polaroid 'dia' (siluet + hati)"""
    if a <= 0: return
    h = w * 1.18
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    if glow > 0: cv.drawRect(r, P(col(CORAL, 0.6 * glow * a), blur=30))
    cv.drawRect(r.makeOffset(0, 18), P(col('#000000', 0.5 * a), blur=22))
    cv.drawRect(r, P(col('#F4F1EA', a)))
    pr = skia.Rect(-w / 2 + w * 0.07, -h / 2 + w * 0.07, w / 2 - w * 0.07, -h / 2 + w * 0.93)
    cv.drawRect(pr, P(shader=lg(0, pr.top(), 0, pr.bottom(), [col('#FF9A8A', a), col('#6A3A8A', a)])))
    cv.save(); cv.clipRect(pr)
    cv.drawCircle(0, pr.top() + pr.height() * 0.42, pr.width() * 0.17, P(col('#2A1A3A', 0.9 * a)))
    cv.drawOval(skia.Rect(-pr.width() * 0.34, pr.top() + pr.height() * 0.66, pr.width() * 0.34, pr.bottom() + pr.height() * 0.3), P(col('#2A1A3A', 0.9 * a)))
    cv.restore()
    f = font(XB, w * 0.11); s = 'dia'; cv.drawString(s, -f.measureText(s) / 2, bl(f, pr.bottom() + (h / 2 - pr.bottom()) * 0.5 + h * 0.01), f, P(col('#3A3550', a)))
    heart_shape(cv, pr.right() - w * 0.1, pr.top() + w * 0.1, w * 0.07, a, HOTPINK)
    cv.restore()

def way_card(cv, cx, cy, w, h, num, text, a, t, good=False, bad=0.0, locked=False, reveal=0.0):
    """kartu cara: 01/02 biasa (bisa dicoret 'cinta nggak turun'), 03 terkunci lalu dibuka"""
    if a <= 0: return
    if locked:
        secret_card2(cv, cx, cy, w, h, f'CARA {num}', [text], a, t, reveal=reveal, glow=0.5 + 0.5 * reveal, size=40); return
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    glass(cv, r, rad=24, a=a * (1 - 0.35 * bad), glow=0.15)
    mono(cv, f'CARA {num}', r.left() + 28, r.top() + 30, 17, ACC_L, a, sp=3, align=0)
    f = font(XB, 38); cv.drawString(text, r.left() + 28, bl(f, cy + 16), f, P(col(TXT, a * (1 - 0.4 * bad))))
    if bad > 0:
        chip(cv, 'CINTA NGGAK TURUN', r.right() - 150, cy + 4, a * bad, size=18, fg='#FFFFFF', bgc=CORAL, edge=CORAL)

# ------------------------------------------------------------ helper EP13: kamar malam + tokoh kapsul di kasur, domba, jam, alarm otak
NIGHT = '#DDE6FF'; GOLD = '#FFC56B'
def sleeper(cv, cx, cy, s, a=1.0, t=0.0, eye=1.0, mood='worried', blanket=('#4A4FD0', '#262A6A'), headphones=0.0, glow=0.0, gc=ACC):
    """tokoh kapsul berbaring di kasur (kepala di kiri): eye 1 = melotot, 0 = terpejam"""
    if a <= 0: return
    if a < 1: layer(cv, a)
    bw = s * 2.4
    cv.drawOval(skia.Rect(cx - bw * 0.62, cy + s * 0.42, cx + bw * 0.62, cy + s * 0.7), P(col('#000000', 0.55), blur=16))
    cv.drawRoundRect(skia.Rect(cx - bw * 0.55, cy + s * 0.05, cx + bw * 0.55, cy + s * 0.5), 24, 24, P(col('#1A1C34')))
    cv.drawRoundRect(skia.Rect(cx - bw * 0.55, cy + s * 0.05, cx + bw * 0.55, cy + s * 0.18), 14, 14, P(col('#2E3160')))
    cv.drawRoundRect(skia.Rect(cx - bw * 0.62, cy - s * 0.6, cx - bw * 0.54, cy + s * 0.55), 14, 14, P(shader=lg(0, cy - s * 0.6, 0, cy + s * 0.55, [col('#5A5F9E'), col('#2E3160')])))
    cv.drawRoundRect(skia.Rect(cx - bw * 0.52, cy - s * 0.32, cx - bw * 0.2, cy + s * 0.08), 34, 34, P(shader=lg(0, cy - s * 0.32, 0, cy + s * 0.08, [col('#E6E8F6', 0.95), col('#B9BCD6', 0.95)])))
    hx, hy, hr = cx - bw * 0.36, cy - s * 0.3, s * 0.3
    if glow > 0: cv.drawCircle(hx, hy, hr * 1.4, P(col(gc, 0.5 * glow), blur=hr * 0.5))
    cv.drawCircle(hx, hy, hr, P(shader=rg(hx - hr * 0.35, hy - hr * 0.4, hr * 1.6, [col('#6A6E9E'), col('#33365A'), col('#1A1B30')], [0, 0.55, 1])))
    cv.drawOval(skia.Rect(hx - hr * 0.6, hy - hr * 0.85, hx - hr * 0.05, hy - hr * 0.45), P(col('#FFFFFF', 0.22), blur=hr * 0.1))
    cv.drawCircle(hx, hy, hr, P(col(ACC_L, 0.6), stroke=2.5))
    ink = P(col(ACC_XL), stroke=max(3, hr * 0.08))
    for sd in (-1, 1):
        ex, ey = hx + sd * hr * 0.36, hy - hr * 0.02
        if eye > 0.12:
            eh = hr * 0.19 * clamp(eye, 0, 1.4)
            cv.drawOval(skia.Rect(ex - hr * 0.14, ey - eh, ex + hr * 0.14, ey + eh), P(col('#F0EFF6')))
            cv.drawCircle(ex + hr * 0.02 * math.sin(t * 2), ey, hr * 0.07 * min(1.0, eye + 0.3), P(col('#15162A')))
            if eye < 0.9:
                lid = skia.Rect(ex - hr * 0.16, ey - hr * 0.24, ex + hr * 0.16, ey - eh + hr * 0.02)
                cv.drawRect(lid, P(col('#3A3D66')))
            if mood == 'worried': cv.drawLine(ex - sd * hr * 0.16, ey - hr * 0.34, ex + sd * hr * 0.1, ey - hr * 0.27, ink)
        else:
            cl = skia.Path(); cl.moveTo(ex - hr * 0.13, ey); cl.quadTo(ex, ey + hr * 0.1, ex + hr * 0.13, ey); cv.drawPath(cl, ink)
    my = hy + hr * 0.42; m = skia.Path()
    if mood == 'worried':
        m.moveTo(hx - hr * 0.2, my + hr * 0.03)
        for k in range(1, 6): m.lineTo(hx - hr * 0.2 + k * hr * 0.08, my + (hr * 0.04 if k % 2 else -hr * 0.03))
    elif mood == 'calm': m.moveTo(hx - hr * 0.2, my - hr * 0.02); m.quadTo(hx, my + hr * 0.14, hx + hr * 0.2, my - hr * 0.02)
    else: m.moveTo(hx - hr * 0.14, my); m.lineTo(hx + hr * 0.14, my)
    cv.drawPath(m, ink)
    if headphones > 0:
        hp = skia.Path(); hp.addArc(skia.Rect(hx - hr * 1.15, hy - hr * 1.2, hx + hr * 1.15, hy + hr * 0.9), 200, 140)
        cv.drawPath(hp, P(col('#2A2C40', headphones), stroke=hr * 0.18)); cv.drawPath(hp, P(col(CORAL, 0.8 * headphones), stroke=hr * 0.06))
        for sd in (-1, 1): cv.drawRoundRect(skia.Rect(hx + sd * hr * 1.0 - hr * 0.2, hy - hr * 0.35, hx + sd * hr * 1.0 + hr * 0.2, hy + hr * 0.25), 12, 12, P(col(CORAL, headphones)))
    bl_ = skia.Path(); x0 = cx - bw * 0.22
    bl_.moveTo(x0, cy + s * 0.08); bl_.cubicTo(x0 + bw * 0.1, cy - s * 0.42 - 8 * math.sin(t * 1.1), x0 + bw * 0.35, cy - s * 0.25, x0 + bw * 0.5, cy - s * 0.3)
    bl_.cubicTo(x0 + bw * 0.62, cy - s * 0.34, x0 + bw * 0.74, cy - s * 0.15, x0 + bw * 0.76, cy + s * 0.12); bl_.close()
    cv.drawPath(bl_, P(shader=lg(0, cy - s * 0.4, 0, cy + s * 0.15, [col(blanket[0]), col(blanket[1])])))
    cv.drawPath(bl_, P(col('#AEB6FF', 0.3), stroke=2))
    if a < 1: cv.restore()
    return hx, hy, hr

def sheep(cv, x, y, s, a=1.0, t=0.0, asleep=False):
    """domba lucu: badan bulu (awan), kepala gelap, kaki"""
    if a <= 0: return
    for sd in (-1, 1):
        for k in (0, 1):
            lx = x + sd * s * (0.25 + 0.2 * k); cv.drawLine(lx, y + s * 0.2, lx + (0 if asleep else s * 0.06 * math.sin(t * 12 + k)), y + s * 0.62, P(col('#2A2C40', a), stroke=s * 0.1))
    body = skia.Path()
    for dx, dy, r in ((-0.35, 0.0, 0.32), (0.0, -0.12, 0.36), (0.35, 0.0, 0.32), (-0.15, 0.15, 0.3), (0.2, 0.15, 0.3)):
        body = skia.Op(body, skia.Path.Circle(x + dx * s, y + dy * s, r * s), skia.PathOp.kUnion_PathOp)
    cv.drawPath(body, P(col('#000000', 0.3 * a), blur=s * 0.12))
    cv.drawPath(body, P(shader=rg(x - s * 0.2, y - s * 0.3, s * 0.9, [col('#FFFFFF', a), col('#DCDFF2', a), col('#A9ADCB', a)], [0, 0.6, 1])))
    hx, hy = x + s * 0.55, y - s * 0.12
    cv.drawOval(skia.Rect(hx - s * 0.2, hy - s * 0.15, hx + s * 0.2, hy + s * 0.17), P(col('#2E3048', a)))
    cv.drawOval(skia.Rect(hx - s * 0.32, hy - s * 0.13, hx - s * 0.12, hy - s * 0.02), P(col('#2E3048', a)))
    if asleep:
        cl = skia.Path(); cl.moveTo(hx - s * 0.02, hy - s * 0.02); cl.quadTo(hx + s * 0.06, hy + s * 0.04, hx + s * 0.13, hy - s * 0.02); cv.drawPath(cl, P(col('#F0EFF6', a), stroke=max(2, s * 0.04)))
    else:
        cv.drawCircle(hx + s * 0.07, hy - s * 0.03, s * 0.045, P(col('#F0EFF6', a)))

def fence(cv, x, y, w, a=1.0):
    if a <= 0: return
    pc = P(col('#8A6A50', a), stroke=10)
    for k in range(3): xx = x - w / 2 + k * w / 2; cv.drawLine(xx, y - 70, xx, y + 30, pc)
    cv.drawLine(x - w / 2 - 10, y - 45, x + w / 2 + 10, y - 45, pc); cv.drawLine(x - w / 2 - 10, y - 5, x + w / 2 + 10, y - 5, pc)

def dclock(cv, cx, cy, txt, a=1.0, c=CORAL, size=72, blink_colon=True, t=0.0):
    """jam digital kaca bercahaya"""
    if a <= 0: return
    f = font(MONO, size); w = f.measureText(txt) + size * 0.9; h = size * 1.5
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    glass(cv, r, rad=24, a=a, glow=0.4, gc=c, fill=('#1A1024', '#0E0A14'))
    shown = txt if (not blink_colon or (t * 2) % 1 < 0.6) else txt.replace(':', ' ').replace('.', ' ')
    tw = f.measureText(txt)
    cv.drawString(shown, cx - tw / 2, bl(f, cy), f, P(col(c, 0.6 * a), blur=size * 0.18)); cv.drawString(shown, cx - tw / 2, bl(f, cy), f, P(col(mixc(c, '#FFFFFF', 0.35), a)))

def siren(cv, cx, cy, s, a, t, on=1.0):
    """lampu alarm merah berputar"""
    if a <= 0: return
    if on > 0:
        cv.save(); cv.translate(cx, cy); cv.rotate(t * 300)
        bm = skia.Path(); bm.moveTo(0, 0); bm.lineTo(700, -110); bm.lineTo(700, 110); bm.close()
        for k in range(2): cv.drawPath(bm, P(shader=lg(0, 0, 700, 0, [col(CORAL, 0.28 * on * a), col(CORAL, 0)]))); cv.rotate(180)
        cv.restore()
        cv.drawCircle(cx, cy, s * 2.2, P(shader=rg(cx, cy, s * 2.2, [col(CORAL, 0.5 * on * a), col(CORAL, 0)])))
    dome = skia.Path(); dome.addArc(skia.Rect(cx - s, cy - s, cx + s, cy + s), 180, 180); dome.close()
    cv.drawPath(dome, P(shader=rg(cx - s * 0.3, cy - s * 0.5, s * 1.4, [col('#FFB3A6', a), col(CORAL, a), col('#7A1020', a)], [0, 0.5, 1])))
    cv.drawRoundRect(skia.Rect(cx - s * 1.2, cy, cx + s * 1.2, cy + s * 0.35), 8, 8, P(col('#3A3D55', a)))

def eye_icon(cv, cx, cy, s, a=1.0, open_=1.0, c=GOLD):
    if a <= 0: return
    hh = s * 0.55 * open_
    e = skia.Path(); e.moveTo(cx - s, cy); e.quadTo(cx, cy - hh * 2, cx + s, cy); e.quadTo(cx, cy + hh * 2, cx - s, cy); e.close()
    cv.drawPath(e, P(col(c, 0.45 * a), blur=s * 0.25)); cv.drawPath(e, P(col('#FFF6E3', a)))
    if open_ > 0.2:
        cv.save(); cv.clipPath(e, skia.ClipOp.kIntersect, True)
        cv.drawCircle(cx, cy, s * 0.42, P(shader=rg(cx, cy, s * 0.42, [col(c, a), col('#8A5A10', a)]))); cv.drawCircle(cx, cy, s * 0.18, P(col('#15162A', a)))
        cv.drawCircle(cx - s * 0.12, cy - s * 0.12, s * 0.07, P(col('#FFFFFF', a))); cv.restore()
    cv.drawPath(e, P(col(c, a), stroke=s * 0.07))

def cloud_bubble(cv, cx, cy, w, h, a, tail):
    """gelembung pikiran berbentuk awan (ekor segitiga, tanpa lingkaran kecil)"""
    if a <= 0: return None
    p = skia.Path()
    for dx, dy, r in ((-0.32, 0.05, 0.36), (0.0, -0.15, 0.42), (0.32, 0.02, 0.36), (-0.12, 0.2, 0.33), (0.18, 0.2, 0.33)):
        p = skia.Op(p, skia.Path.Oval(skia.Rect(cx + dx * w - r * w, cy + dy * h - r * h * 1.1, cx + dx * w + r * w, cy + dy * h + r * h * 1.1)), skia.PathOp.kUnion_PathOp)
    tl = skia.Path(); tl.moveTo(cx - w * 0.08, cy + h * 0.3); tl.lineTo(tail[0], tail[1]); tl.lineTo(cx + w * 0.06, cy + h * 0.32); tl.close()
    p = skia.Op(p, tl, skia.PathOp.kUnion_PathOp)
    sh = skia.Path(p); sh.offset(0, 16); cv.drawPath(sh, P(col('#000000', 0.5 * a), blur=20))
    cv.drawPath(p, P(shader=lg(0, cy - h * 0.6, 0, cy + h * 0.6, [col('#2A2C48', 0.96 * a), col('#171828', 0.96 * a)])))
    cv.drawPath(p, P(col(ACC_L, 0.7 * a), stroke=2.5))
    return p

def night_room(cv, a, t, moon=1.0):
    if a <= 0: return
    wx, wy = 860, 430
    win = skia.Rect(wx - 120, wy - 130, wx + 120, wy + 130)
    cv.drawRect(win, P(shader=lg(0, win.top(), 0, win.bottom(), [col('#1E2A5A', 0.9 * a), col('#0E1430', 0.9 * a)])))
    cv.drawCircle(wx + 30, wy - 45, 42, P(col(NIGHT, 0.9 * a * moon))); cv.drawCircle(wx + 50, wy - 58, 40, P(col('#1A2550', 0.95 * a)))
    halo(cv, wx + 20, wy - 45, 190, NIGHT, 0.3 * a * moon)
    cv.drawRect(win, P(col('#8C93FF', 0.6 * a), stroke=6)); cv.drawLine(wx, win.top(), wx, win.bottom(), P(col('#8C93FF', 0.6 * a), stroke=4)); cv.drawLine(win.left(), wy, win.right(), wy, P(col('#8C93FF', 0.6 * a), stroke=4))


# ------------------------------------------------------------ helper EP33: kertas daftar, Zzz, kabel lab tidur, tugas yang berputar di kepala
TRIK = ['Tulis daftar tugas', 'buat besok.']
TASKS = [('tugas MTK', GOLD), ('presentasi', HOTPINK), ('bayar kos', '#7FB8FF'), ('deadline!', CORAL), ('chat dosen', MINT)]

def paper(cv, cx, cy, w, h, a, title, items, t, kind='todo', blur=0.0, rot=0.0, hl=None, glow=0.0, done=0.0):
    """kertas catatan: title + item (kind 'done' = centang hijau, 'todo' = kotak kosong); blur > 0 = disensor"""
    if a <= 0: return
    cv.save(); cv.translate(cx, cy); cv.rotate(rot)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    if glow > 0: cv.drawRoundRect(r, 16, 16, P(col(GOLD, 0.6 * glow * a), blur=30))
    cv.drawRoundRect(r.makeOffset(0, 18), 16, 16, P(col('#000000', 0.5 * a), blur=22))
    cv.drawRoundRect(r, 16, 16, P(shader=lg(0, r.top(), 0, r.bottom(), [col('#FBF8F0', a), col('#E9E3D4', a)])))
    for k in range(1, 9):
        y = r.top() + 70 + k * (h - 90) / 9
        cv.drawLine(r.left() + 24, y, r.right() - 24, y, P(col('#B9C4E0', 0.5 * a), stroke=1.5))
    cv.drawLine(r.left() + 58, r.top() + 10, r.left() + 58, r.bottom() - 10, P(col('#F0A0A0', 0.6 * a), stroke=2))
    ft = font(XB, w * 0.075); cv.drawString(title, r.left() + 72, bl(ft, r.top() + 46), ft, P(col('#2A2550', a)))
    fi = font(B, w * 0.062); bp = P(col('#3A3560', a), blur=blur * 9) if blur > 0 else P(col('#3A3560', a))
    for k, txt in enumerate(items):
        y = r.top() + 108 + k * w * 0.13
        bx = r.left() + 72
        if kind == 'done':
            cv.drawCircle(bx + 12, y, 12, P(col(MINT, a))); fb = font(XB, 15); cv.drawString('✓', bx + 12 - fb.measureText('✓') / 2, bl(fb, y), fb, P(col('#FFFFFF', a)))
        else:
            cv.drawRoundRect(skia.Rect(bx, y - 12, bx + 24, y + 12), 5, 5, P(col('#3A3560', 0.8 * a), stroke=2.5))
            if done > k + 0.5: cv.drawLine(bx + 4, y, bx + 20, y, P(col(MINT, a), stroke=3))
        if hl is not None and hl[k] > 0:
            tw = fi.measureText(txt)
            cv.drawRoundRect(skia.Rect(bx + 34, y - 18, bx + 44 + tw, y + 18), 8, 8, P(col(GOLD, 0.35 * hl[k] * a)))
        cv.drawString(txt, bx + 38, bl(fi, y), fi, bp)
    cv.restore()

def zzz(cv, x, y, a, t, n=3, c=NIGHT, rise=150):
    if a <= 0: return
    for k in range(n):
        u = (t * 0.5 + k / n) % 1.0
        f = font(XB, 30 + 22 * u); s = 'z'
        cv.drawString(s, x + 40 * u + 10 * math.sin(t * 2 + k), y - rise * u, f, P(col(c, a * bump(u) * 1.2)))

def swirl_tasks(cv, cx, cy, rx, ry, t, a, speed=1.0, n=5, size=24):
    """chip tugas yang berputar mengelilingi titik (pikiran yang mengulang)"""
    if a <= 0: return
    for k in range(n):
        ang = t * speed + k * math.tau / n
        x = cx + math.cos(ang) * rx; y = cy + math.sin(ang) * ry
        txt, c = TASKS[k % len(TASKS)]
        chip(cv, txt, x, y, a * (0.65 + 0.35 * (math.sin(ang) + 1) / 2), size=size, fg=INK, bgc=c, edge=c)

# ------------------------------------------------------------ helper EP34: paru-paru kaca, grafik pola napas, lingkaran panduan napas
NAPAS = ['Tarik 2x,', 'buang panjang.']
def lungs(cv, cx, cy, s, fill, a, t, c=MINT, glow=0.0):
    """paru-paru kaca yang terisi (fill 0..1) + trakea"""
    if a <= 0: return
    s = s * (1 + 0.07 * clamp(fill))
    lobes = []
    for sd in (-1, 1):
        p = skia.Path(); p.moveTo(cx + sd * s * 0.12, cy - s * 0.5)
        p.cubicTo(cx + sd * s * 0.95, cy - s * 0.85, cx + sd * s * 1.1, cy + s * 0.55, cx + sd * s * 0.62, cy + s * 0.88)
        p.cubicTo(cx + sd * s * 0.4, cy + s * 1.0, cx + sd * s * 0.12, cy + s * 0.8, cx + sd * s * 0.12, cy + s * 0.45); p.close()
        lobes.append(p)
    if glow > 0:
        for p in lobes: cv.drawPath(p, P(col(c, 0.5 * glow * a), blur=s * 0.25))
    tr = skia.Path(); tr.moveTo(cx, cy - s * 1.15); tr.lineTo(cx, cy - s * 0.45)
    tr.moveTo(cx, cy - s * 0.5); tr.quadTo(cx - s * 0.1, cy - s * 0.3, cx - s * 0.35, cy - s * 0.15)
    tr.moveTo(cx, cy - s * 0.5); tr.quadTo(cx + s * 0.1, cy - s * 0.3, cx + s * 0.35, cy - s * 0.15)
    cv.drawPath(tr, P(col('#AEB6FF', 0.75 * a), stroke=s * 0.07))
    lvl = lerp(cy + s * 0.95, cy - s * 0.7, clamp(fill))
    for p in lobes:
        cv.drawPath(p, P(shader=lg(0, cy - s, 0, cy + s, [col('#2A2C48', 0.85 * a), col('#14152A', 0.85 * a)])))
        cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
        cv.drawRect(skia.Rect(cx - s * 1.3, lvl, cx + s * 1.3, cy + s * 1.1), P(shader=lg(0, lvl, 0, cy + s, [col(mixc(c, '#FFFFFF', 0.4), 0.95 * a), col(c, 0.85 * a)])))
        wp = skia.Path(); wp.moveTo(cx - s * 1.3, lvl)
        for i in range(25): x = cx - s * 1.3 + i * s * 0.11; wp.lineTo(x, lvl + 5 * math.sin(x * 0.05 + t * 4))
        cv.drawPath(wp, P(col('#FFFFFF', 0.5 * a), stroke=3))
        cv.drawOval(skia.Rect(cx - s * 0.9, cy - s * 0.7, cx - s * 0.3, cy - s * 0.1), P(col('#FFFFFF', 0.12 * a), blur=s * 0.1))
        cv.restore()
        cv.drawPath(p, P(col(c, 0.8 * a), stroke=3))

def breath_pattern(u):
    """pola cyclic sighing ternormalisasi: tarik (0-.22) -> tarik lagi (.3-.42) -> buang panjang (.48-1)"""
    if u < 0.22: return 0.7 * eo(u / 0.22)
    if u < 0.3: return 0.7
    if u < 0.42: return 0.7 + 0.3 * eo((u - 0.3) / 0.12)
    if u < 0.48: return 1.0
    return 1.0 - ei((u - 0.48) / 0.52) * 0.98 if u < 1 else 0.02

def breath_graph(cv, x0, x1, y, h, prog_u, a, c=MINT):
    if a <= 0: return
    cv.drawLine(x0, y, x1, y, P(col(ACC_L, 0.3 * a), stroke=2))
    p = skia.Path(); n = 80
    for i in range(n + 1):
        u = i / n
        if u > prog_u: break
        x = lerp(x0, x1, u); yy = y - h * breath_pattern(u)
        (p.moveTo if i == 0 else p.lineTo)(x, yy)
    cv.drawPath(p, P(col(c, 0.5 * a), stroke=10, blur=8)); cv.drawPath(p, P(col(mixc(c, '#FFFFFF', 0.4), a), stroke=4))
    for u, lab in ((0.11, 'TARIK'), (0.36, 'TARIK LAGI'), (0.74, 'BUANG PANJAAANG')):
        if prog_u > u - 0.05: mono(cv, lab, lerp(x0, x1, u), y + 30, 17, c, a * clamp((prog_u - u + 0.05) * 6), sp=2)

def breath_circle(cv, cx, cy, r0, v, a, t, c=MINT, label=None):
    """lingkaran panduan napas yang membesar/mengecil (v 0..1)"""
    if a <= 0: return
    r = r0 * (0.55 + 0.45 * clamp(v))
    halo(cv, cx, cy, r * 1.9, c, 0.6 * a)
    cv.drawCircle(cx, cy, r, P(shader=rg(cx - r * 0.3, cy - r * 0.35, r * 1.5, [col(mixc(c, '#FFFFFF', 0.5), 0.9 * a), col(c, 0.75 * a), col(mixc(c, '#000000', 0.4), 0.7 * a)], [0, 0.5, 1])))
    cv.drawCircle(cx, cy, r0, P(col(c, 0.4 * a), stroke=3, effect=skia.DashPathEffect.Make([10, 10], -t * 20)))
    if label:
        f = font(XB, 44); w = f.measureText(label); cv.drawString(label, cx - w / 2, bl(f, cy), f, P(col(INK, a)))

# ------------------------------------------------------------ helper EP35: DM dengan "dia" (mengetik... lalu hilang), hati tergantung tali, kartu profil, hati kondisi
TANYA = ['Aku suka dia,', 'atau cuma penasaran?']
BOYS = [('#7FB8FF', 'Raka'), ('#3FD6A4', 'Dimas'), ('#FFC56B', 'Bima'), ('#B57BFF', 'Arya')]

def dm_phone(cv, cx, cy, w, h, a, t, msgs, typing=0.0, status='online', glow=0.0):
    """ponsel kaca DM dengan 'dia': msgs (side, text, t0); typing 0..1 = gelembung 'mengetik...'"""
    if a <= 0: return
    cv.save(); cv.translate(cx, cy)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2); rad = w * 0.13
    if glow > 0: cv.drawRRect(RR(r, rad), P(col(ROSE, 0.5 * glow * a), stroke=16, blur=30))
    cv.drawRRect(RR(r.makeOffset(0, 36), rad), P(col('#000000', 0.6 * a), blur=46))
    cv.drawRRect(RR(r, rad), P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col('#6A6E8E', a), col('#1A1B2A', a), col('#4A4D68', a), col('#15161F', a)], [0, 0.35, 0.7, 1])))
    sr = r.makeInset(w * 0.035, w * 0.035); srad = rad * 0.8
    cv.drawRRect(RR(sr, srad), P(col('#04050A', a)))
    cv.save(); cv.clipRRect(RR(sr, srad), skia.ClipOp.kIntersect, True)
    cv.drawRect(sr, P(shader=lg(0, sr.top(), 0, sr.bottom(), [col('#1C1A48', a), col('#100F2A', a)])))
    hh = h * 0.11; hy = sr.top() + w * 0.08 + hh / 2
    cv.drawRect(skia.Rect(sr.left(), sr.top(), sr.right(), hy + hh / 2), P(col('#1E1F3C', 0.95 * a)))
    av = hh * 0.36; ax = sr.left() + w * 0.12
    cv.drawCircle(ax, hy, av, P(shader=lg(0, hy - av, 0, hy + av, [col('#9AC8FF', a), col('#4A6ACA', a)])))
    fa = font(XB, av); cv.drawString('D', ax - fa.measureText('D') / 2, bl(fa, hy), fa, P(col(INK, a)))
    f1 = font(XB, w * 0.07); f2 = font(M, w * 0.042)
    cv.drawString('dia', ax + av * 1.5, bl(f1, hy - hh * 0.15), f1, P(col(TXT, a)))
    cv.drawString(status, ax + av * 1.5, bl(f2, hy + hh * 0.22), f2, P(col(MINT if status == 'online' else MUTED, a)))
    y = hy + hh / 2 + h * 0.09; fs = w * 0.07
    for side, txt, t0 in msgs:
        q = prog(t, t0, t0 + 0.25)
        if q > 0:
            msg(cv, sr.left() + w * 0.05 if side == 'L' else sr.right() - w * 0.05, y + (1 - eo(q)) * 18, txt, fs, a * clamp(q * 3), side, '#34365A' if side == 'L' else '#4B53D6')
        y += fs * 2.3
    if typing > 0:
        tw = w * 0.3; tr = skia.Rect(sr.left() + w * 0.05, y - fs * 0.95, sr.left() + w * 0.05 + tw, y + fs * 0.95)
        cv.drawRoundRect(tr, fs, fs, P(col('#34365A', a * typing)))
        for k in range(3):
            bb = 0.5 + 0.5 * math.sin(t * 9 - k * 0.8)
            cv.drawCircle(tr.left() + tw * (0.28 + 0.22 * k), y - 6 * bb, fs * 0.16, P(col(ACC_XL, a * typing * (0.5 + 0.5 * bb))))
        fm = font(M, w * 0.04); cv.drawString('mengetik...', tr.right() + 12, bl(fm, y), fm, P(col(MUTED, a * typing)))
    cv.restore()
    cv.drawRoundRect(skia.Rect(-w * 0.12, sr.top() + w * 0.025, w * 0.12, sr.top() + w * 0.06), 8, 8, P(col('#000000', a)))
    cv.restore()

def hanging_heart(cv, x, top, length, s, a, t, swing=1.0, c=ROSE, q=0.0):
    """hati yang tergantung di tali dan berayun; q > 0 = tanda tanya di hati"""
    if a <= 0: return
    ang = math.radians(16 * swing * math.sin(t * 2.4))
    hx = x + math.sin(ang) * length; hy = top + math.cos(ang) * length
    cv.drawLine(x, top, hx, hy - s * 0.7, P(col('#C9CCE8', 0.8 * a), stroke=3))
    cv.drawCircle(x, top, 8, P(col('#8A8EAE', a)))
    cv.save(); cv.translate(hx, hy); cv.rotate(math.degrees(ang) * 0.6); cv.translate(-hx, -hy)
    heart_shape(cv, hx, hy, s, a, c)
    if q > 0:
        f = font(XB, s * 0.9); cv.drawString('?', hx - f.measureText('?') / 2, bl(f, hy - s * 0.05), f, P(col('#FFFFFF', a * q)))
    cv.restore()
    return hx, hy

def profile_card(cv, x, y, w, h, a, c, name, t, seen=0.0):
    if a <= 0: return
    r = skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    glass(cv, r, rad=24, a=a, glow=0.15, gc=c, edge=c)
    avatar(cv, r.left() + h * 0.42, y - h * 0.05, h * 0.26, c, a, ok=0.0)
    f = font(XB, h * 0.17); cv.drawString(name, r.left() + h * 0.85, bl(f, y - h * 0.16), f, P(col(TXT, a)))
    for k in range(2): cv.drawRoundRect(skia.Rect(r.left() + h * 0.85, y + h * (0.02 + 0.16 * k), r.right() - 24 - k * 40, y + h * (0.1 + 0.16 * k)), 6, 6, P(col(ACC_L, 0.35 * a)))
    if seen > 0: eye_icon(cv, r.right() - 34, r.top() + 30, 20, a * seen, 1.0, GOLD)

def cond_card(cv, x, y, w, h, a, t, title, kind, c, glow=0.0):
    """kartu kondisi: 'suka' (3 hati penuh), 'biasa' (1 hati), 'ragu' (hati ? berkedip)"""
    if a <= 0: return
    r = skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    glass(cv, r, rad=28, a=a, glow=0.2 + glow, gc=c, edge=c)
    mono(cv, '"DIA ITU..."', x, r.top() + 34, 16, MUTED, a, sp=2)
    if kind == 'suka':
        for k in range(3): heart_shape(cv, x - 70 + k * 70, y - 20, 28, a, c)
    elif kind == 'biasa':
        heart_shape(cv, x, y - 20, 30, a * 0.8, c)
        for k in (-1, 1): heart_shape(cv, x + k * 70, y - 20, 28, a * 0.18, ACC_L)
    else:
        fl = 0.5 + 0.5 * math.sin(t * 7)
        heart_shape(cv, x, y - 20, 44, a * (0.5 + 0.5 * fl), c)
        f = font(XB, 44); cv.drawString('?', x - f.measureText('?') / 2, bl(f, y - 22), f, P(col('#FFFFFF', a)))
    f = font(XB, 34 if len(title) < 11 else 30); tw = f.measureText(title)
    cv.drawString(title, x - tw / 2, bl(f, r.bottom() - 56), f, P(col(c, a)))

# ------------------------------------------------------------ helper EP35 v2 (premium): studio sorot + lantai pantul, bandul hati kaca, ponsel 3D, carousel profil, orbit pikiran
def studio(cv, a, t, c=ROSE, x=540, cone=260):
    """latar studio malam: lampu sorot volumetrik dari atas + lantai mengilap yang memantulkan cahaya"""
    if a <= 0: return
    cone_p = skia.Path(); cone_p.moveTo(x - 50, 250); cone_p.lineTo(x + 50, 250); cone_p.lineTo(x + cone * 1.8, 1130); cone_p.lineTo(x - cone * 1.8, 1130); cone_p.close()
    cv.drawPath(cone_p, P(shader=lg(0, 250, 0, 1130, [col('#FFFFFF', 0.10 * a), col(c, 0.07 * a), col(c, 0)])))
    cv.drawRect(skia.Rect(0, 1060, 1080, 1200), P(shader=lg(0, 1060, 0, 1200, [col('#1A1530', 0), col('#1A1530', 0.85 * a), col('#0A0A14', 0)])))
    cv.drawOval(skia.Rect(x - 420, 1085, x + 420, 1165), P(shader=rg(x, 1125, 420, [col(c, 0.22 * a), col(c, 0)])))
    cv.drawLine(60, 1090, 1020, 1090, P(shader=lg(60, 0, 1020, 0, [col(ACC_L, 0), col(ACC_L, 0.25 * a), col(ACC_L, 0)]), stroke=2))

def chain(cv, x0, y0, x1, y1, a, c='#C9CCE8'):
    """rantai logam berkilau dari (x0,y0) ke (x1,y1)"""
    L = math.hypot(x1 - x0, y1 - y0); n = max(2, int(L / 22))
    for i in range(n):
        u = (i + 0.5) / n; x = lerp(x0, x1, u); y = lerp(y0, y1, u)
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        cv.save(); cv.translate(x, y); cv.rotate(ang)
        r = skia.Rect(-12, -5, 12, 5) if i % 2 == 0 else skia.Rect(-10, -2.5, 10, 2.5)
        cv.drawRoundRect(r, 5, 5, P(col(c, 0.85 * a), stroke=3))
        cv.restore()

def pend_heart(cv, x, top, L, s, v, a, t, swing=1.0, c=ROSE, q=0.0, glow=0.0, phase=0.0, label=None, shadow=True, slosh=0.0):
    """bandul hati kaca berisi cairan: tergantung rantai dari (x, top), berayun (swing), cairan v; q = tanda tanya di dalam"""
    if a <= 0 or L <= 1: return x, top
    ang = math.radians(17 * swing * math.sin(t * 2.3 + phase))
    hx = x + math.sin(ang) * L; hy = top + math.cos(ang) * L
    if shadow:
        sw = s * 1.6 * (1 - 0.15 * abs(math.sin(ang)))
        cv.drawOval(skia.Rect(hx - sw, 1100, hx + sw, 1130), P(col('#000000', 0.45 * a), blur=14))
        cv.drawOval(skia.Rect(hx - sw * 0.8, 1105, hx + sw * 0.8, 1125), P(col(c, 0.18 * a * (0.5 + glow)), blur=18))
    cv.drawCircle(x, top, 12, P(shader=rg(x - 4, top - 4, 14, [col('#E6E8F6', a), col('#6A6E8E', a)])))
    chain(cv, x, top, hx, hy - s * 0.8, a)
    cv.save(); cv.translate(hx, hy); cv.rotate(-math.degrees(ang) * 0.8); cv.translate(-hx, -hy)
    vv = clamp(v + slosh * 0.12 * math.sin(t * 7 + phase))
    glass_heart(cv, hx, hy, s, vv, a, t, label=None, c=c, glow=glow)
    if q > 0:
        f = font(XB, s * 0.95); w = f.measureText('?')
        cv.drawString('?', hx - w / 2, bl(f, hy - s * 0.05), f, P(col('#FFFFFF', 0.5 * a * q), blur=8))
        cv.drawString('?', hx - w / 2, bl(f, hy - s * 0.05), f, P(col('#FFFFFF', a * q)))
    cv.restore()
    if label: mono(cv, label, hx, hy + s * 1.25, 20, mixc(c, '#FFFFFF', 0.25), a, sp=3)
    return hx, hy

def phone3d(cv, cx, cy, w, h, a, t, ry=-16, rx=8, z=0, **kw):
    """ponsel DM melayang dalam perspektif 3D + pendar neon di belakang"""
    if a <= 0: return
    halo(cv, cx, cy, w * 1.1, ROSE, 0.45 * a)
    with plane(cv, cx, cy, z, w, h, ry, rx) as ok:
        if ok: dm_phone(cv, 0, 0, w, h, a, t, **kw)

def carousel(cv, cx, cy, R, spin, a, t, seen=0.0):
    """4 kartu profil berputar dalam carousel 3D (urut kedalaman)"""
    items = []
    for k, (c, nm) in enumerate(BOYS):
        ang = spin + k * math.tau / 4
        x = R * math.sin(ang); z = R * (1 - math.cos(ang)) * 0.9
        items.append((z, k, x, ang, c, nm))
    items.sort(key=lambda it: -it[0])
    for z, k, x, ang, c, nm in items:
        dep = clamp(1 - z / (1.8 * R))
        with plane(cv, cx + x, cy, z, 450, 270, math.degrees(math.sin(ang)) * 0.6, -6) as ok:
            if ok:
                if True:
                    profile_card(cv, 0, 0, 450, 270, a * lerp(0.35, 1.0, dep), c, nm, t, seen=seen)
                else:
                    r = skia.Rect(-225, -135, 225, 135); glass(cv, r, rad=24, a=a * 0.5, glow=0.1)

def thought_ring(cv, cx, cy, R, spin, a, texts, tilt=0.32, size=24, center=None):
    """kartu pikiran mengorbit dalam 3D (perspektif + urut kedalaman); center() digambar di tengah antrian"""
    items = []
    for k, (txt, c) in enumerate(texts):
        x, y, z = ring_pos(k, len(texts), spin, R, tilt); items.append((z, k, x, y, txt, c))
    items.sort(key=lambda it: -it[0]); drawn = False
    for z, k, x, y, txt, c in items:
        if z < 0 and not drawn and center: center(); drawn = True
        X, Y, s = P3(cx + x, cy + y, z)
        dep = clamp((R - z) / (2 * R))
        comment(cv, txt, X, Y, a * lerp(0.35, 1.0, dep), s * 0.85, size=size, av=c, rot=(k % 3 - 1) * 4, glow=0.5 * dep)
    if center and not drawn: center()

# ------------------------------------------------------------ helper EP36 (premium): bola titik krom 3D, gelembung chat besar yang membeku, tabung kaca, kertas tulisan tangan, orbit tanda baca, dinding es, tombol hapus
TRIK = ['Balas singkat?', 'Hapus titiknya.']
FRIEND = '#7FB8FF'

def chrome_dot(cv, x, y, r, a=1.0, t=0.0, cold=0.0, glow=0.0, gc=CORAL):
    """'titik' sebagai bola krom hitam 3D: gradasi radial, pantulan horizon, cahaya tepi, kilau; cold = lapisan es"""
    if a <= 0 or r <= 1: return
    if glow > 0: cv.drawCircle(x, y, r * 2.0, P(shader=rg(x, y, r * 2.0, [col(gc, 0.5 * glow * a), col(gc, 0)])))
    cv.drawCircle(x, y, r, P(shader=rg(x - r * 0.35, y - r * 0.42, r * 1.65,
                                         [col(mixc('#6A6E98', '#CFEFFF', cold * 0.7), a), col(mixc('#1A1B30', '#20405E', cold), a), col('#04050B', a)], [0, 0.55, 1])))
    p = skia.Path(); p.addCircle(x, y, r)
    cv.save(); cv.clipPath(p, skia.ClipOp.kIntersect, True)
    cv.drawOval(skia.Rect(x - r * 1.0, y + r * 0.02, x + r * 1.0, y + r * 0.34), P(col(mixc(ACC_L, ICE, cold), 0.2 * a), blur=r * 0.08))
    cv.drawCircle(x + r * 0.28, y + r * 0.34, r * 1.02, P(col(mixc(ACC, ICE, cold), 0.55 * a), stroke=r * 0.13, blur=r * 0.1))
    cv.drawOval(skia.Rect(x - r * 0.64, y - r * 0.78, x - r * 0.06, y - r * 0.4), P(col('#FFFFFF', 0.5 * a), blur=r * 0.08))
    cv.drawOval(skia.Rect(x - r * 0.5, y - r * 0.66, x - r * 0.28, y - r * 0.5), P(col('#FFFFFF', 0.9 * a), blur=r * 0.03))
    if cold > 0.05:
        rnd = random.Random(3); pp = skia.Path()
        for k in range(6):
            ang = rnd.uniform(0, math.tau); L = r * rnd.uniform(0.5, 1.0) * clamp(cold * 1.4)
            pp.moveTo(x + math.cos(ang) * r * 0.15, y + math.sin(ang) * r * 0.15); pp.lineTo(x + math.cos(ang) * L, y + math.sin(ang) * L)
        cv.drawPath(pp, P(col('#E8F6FF', 0.6 * a * cold), stroke=max(1.2, r * 0.03)))
    cv.restore()
    cv.drawCircle(x, y, r, P(col('#FFFFFF', 0.2 * a), stroke=max(1.5, r * 0.02)))

def sparks(cv, x, y, r, u, a, c=GOLD, n=12):
    """ledakan garis cahaya (bukan titik)"""
    if a <= 0 or not (0 < u < 1): return
    for k in range(n):
        ang = k * math.tau / n + 0.3
        r0 = r * (0.3 + 0.9 * eo(u)); r1 = r0 + r * 0.45 * (1 - u)
        cv.drawLine(x + math.cos(ang) * r0, y + math.sin(ang) * r0, x + math.cos(ang) * r1, y + math.sin(ang) * r1, P(col(c, a * (1 - u)), stroke=5))

def ice_layer(cv, rct, rad, x0, y0, u, a, seed=5):
    """lapisan es di dalam bentuk (clip oleh pemanggil): tint biru + kristal bercabang dari (x0, y0)"""
    if a <= 0 or u <= 0: return
    cv.drawRoundRect(rct, rad, rad, P(col('#BFE6FF', 0.28 * u * a)))
    rnd = random.Random(seed); pth = skia.Path()
    for k in range(9):
        ang = rnd.uniform(0, math.tau); L = rnd.uniform(0.5, 1.0) * max(rct.width(), rct.height()) * 0.75 * eo(clamp(u))
        x1, y1 = x0 + math.cos(ang) * L, y0 + math.sin(ang) * L
        pth.moveTo(x0, y0); pth.lineTo(x1, y1)
        for j in (0.3, 0.55, 0.8):
            bx, by = lerp(x0, x1, j), lerp(y0, y1, j); bl_ = L * 0.2 * (1 - j)
            for s_ in (-1, 1): pth.moveTo(bx, by); pth.lineTo(bx + math.cos(ang + s_ * 0.8) * bl_, by + math.sin(ang + s_ * 0.8) * bl_)
    cv.drawPath(pth, P(col(ICE, 0.45 * a * u), stroke=6, blur=6)); cv.drawPath(pth, P(col('#F2FAFF', 0.85 * a * u), stroke=2))

def big_bubble(cv, cx, cy, word, size, a, t, dot=1.0, frost_=0.0, crack=0.0, warm=0.0, drop=0.0, cursor=0.0, burst=0.0, side='R', hl=0.0):
    """gelembung chat besar 'oke' + titik bola krom di ujungnya; frost_ membeku, crack retak, warm hangat (pendar mint)"""
    if a <= 0: return cx, cy
    f = font(XB, size); tw = f.measureText(word); dr = size * 0.4; gap = size * 0.08
    padx = size * 0.55; h = size * 1.6; w = tw + padx * 2 + (gap + dr * 2) * clamp(dot)
    r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); rad = h * 0.42
    if warm > 0: cv.drawRoundRect(r, rad, rad, P(col(MINT, 0.55 * warm * a), stroke=22, blur=30))
    cv.drawRoundRect(r.makeOffset(0, 26), rad, rad, P(col('#000000', 0.55 * a), blur=34))
    tail = skia.Path()
    if side == 'R': tail.moveTo(r.right() - rad * 0.9, r.bottom() - 6); tail.quadTo(r.right() + 4, r.bottom() + 4, r.right() + size * 0.22, r.bottom() + size * 0.18); tail.quadTo(r.right() - rad * 0.2, r.bottom() - rad * 0.2, r.right() - rad * 0.5, r.bottom() - rad * 0.6)
    else: tail.moveTo(r.left() + rad * 0.9, r.bottom() - 6); tail.quadTo(r.left() - 4, r.bottom() + 4, r.left() - size * 0.22, r.bottom() + size * 0.18); tail.quadTo(r.left() + rad * 0.2, r.bottom() - rad * 0.2, r.left() + rad * 0.5, r.bottom() - rad * 0.6)
    tail.close()
    c1, c2 = mixc('#6A72FF', '#9ED9FF', frost_ * 0.55), mixc('#3A3FB8', '#3A6A9A', frost_ * 0.6)
    if warm > 0: c1, c2 = mixc(c1, '#5FE0B8', warm * 0.45), mixc(c2, '#2A8A70', warm * 0.45)
    sh = lg(0, r.top(), 0, r.bottom(), [col(c1, a), col(c2, a)])
    cv.drawPath(tail, P(shader=sh)); cv.drawRoundRect(r, rad, rad, P(shader=sh))
    bp = skia.Path(); bp.addRoundRect(r, rad, rad)
    x0 = r.left() + padx; by = bl(f, cy); dx = x0 + tw + gap + dr; dy = by - dr * 0.8
    cv.save(); cv.clipPath(bp, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(r.left(), r.top(), r.right(), r.top() + h * 0.45), P(shader=lg(0, r.top(), 0, r.top() + h * 0.45, [col('#FFFFFF', 0.22 * a), col('#FFFFFF', 0)])))
    ice_layer(cv, r, rad, dx, dy, frost_, a)
    cv.restore()
    cv.drawRoundRect(r, rad, rad, P(col('#FFFFFF', 0.35 * a), stroke=2.5))
    cv.drawString(word, x0, by + 4, f, P(col('#000000', 0.25 * a), blur=6))
    cv.drawString(word, x0, by, f, P(col('#FFFFFF', a)))
    if crack > 0:
        rnd = random.Random(11); cp = skia.Path()
        for k in range(7):
            ang = -2.6 + k * 0.75 + rnd.uniform(-0.2, 0.2); L = h * rnd.uniform(0.35, 0.7) * eo(clamp(crack))
            px, py = dx, dy
            cp.moveTo(px, py)
            for j in range(3):
                ang += rnd.uniform(-0.4, 0.4); px += math.cos(ang) * L / 3; py += math.sin(ang) * L / 3; cp.lineTo(px, py)
        cv.save(); cv.clipPath(bp, skia.ClipOp.kIntersect, True)
        cv.drawPath(cp, P(col('#0A0B1A', 0.6 * a), stroke=5)); cv.drawPath(cp, P(col('#FFFFFF', 0.75 * a), stroke=1.6)); cv.restore()
    if dot > 0:
        cv.drawOval(skia.Rect(dx - dr, by - dr * 0.25, dx + dr, by + dr * 0.25), P(col('#000000', 0.45 * a * dot * (1 - clamp(drop / 200))), blur=8))
        chrome_dot(cv, dx, dy - drop, dr * dot, a, t, cold=frost_, glow=hl, gc=CORAL)
    sparks(cv, dx, dy, dr * 3, burst, a, GOLD)
    if cursor > 0 and (t * 2) % 1 < 0.6:
        cx_ = (x0 + tw + size * 0.06) if dot <= 0 else (dx + dr + size * 0.06)
        cv.drawRoundRect(skia.Rect(cx_, cy - size * 0.42, cx_ + 5, cy + size * 0.42), 2, 2, P(col('#FFFFFF', 0.9 * a * cursor)))
    return dx, dy

def chat_phone3(cv, w, h, a, t, msgs, name='Nadia', initial='N', avc=FRIEND, hl=0.0, cold=0.0):
    """ponsel kaca (koordinat lokal, pusat 0,0) dengan chat; msgs (side, text, t0); hl = titik di balasan menyala koral"""
    if a <= 0: return
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2); rad = w * 0.13
    cv.drawRRect(RR(r.makeOffset(0, 36), rad), P(col('#000000', 0.6 * a), blur=46))
    cv.drawRRect(RR(r, rad), P(shader=lg(r.left(), r.top(), r.right(), r.bottom(), [col('#6A6E8E', a), col('#1A1B2A', a), col('#4A4D68', a), col('#15161F', a)], [0, 0.35, 0.7, 1])))
    sr = r.makeInset(w * 0.035, w * 0.035); srad = rad * 0.8
    cv.drawRRect(RR(sr, srad), P(col('#04050A', a)))
    cv.save(); cv.clipRRect(RR(sr, srad), skia.ClipOp.kIntersect, True)
    cv.drawRect(sr, P(shader=lg(0, sr.top(), 0, sr.bottom(), [col(mixc('#1C1A48', '#16304A', cold), a), col(mixc('#100F2A', '#0C1C2E', cold), a)])))
    hh = h * 0.11; hy = sr.top() + w * 0.08 + hh / 2
    cv.drawRect(skia.Rect(sr.left(), sr.top(), sr.right(), hy + hh / 2), P(col('#1E1F3C', 0.95 * a)))
    av = hh * 0.36; ax = sr.left() + w * 0.12
    cv.drawCircle(ax, hy, av, P(shader=lg(0, hy - av, 0, hy + av, [col(mixc(avc, '#FFFFFF', 0.3), a), col(mixc(avc, '#000000', 0.3), a)])))
    fa = font(XB, av); cv.drawString(initial, ax - fa.measureText(initial) / 2, bl(fa, hy), fa, P(col(INK, a)))
    f1 = font(XB, w * 0.07); f2 = font(M, w * 0.042)
    cv.drawString(name, ax + av * 1.5, bl(f1, hy - hh * 0.15), f1, P(col(TXT, a)))
    cv.drawString('online', ax + av * 1.5, bl(f2, hy + hh * 0.22), f2, P(col(MINT, a)))
    y = hy + hh / 2 + h * 0.09; fs = w * 0.06
    for side, txt, t0 in msgs:
        q = prog(t, t0, t0 + 0.25)
        if q > 0:
            edge = sr.left() + w * 0.05 if side == 'L' else sr.right() - w * 0.05
            msg(cv, edge, y + (1 - eo(q)) * 18, txt, fs, a * clamp(q * 3), side, '#34365A' if side == 'L' else '#4B53D6')
            if side == 'R' and txt.endswith('.') and hl > 0:
                fb = font(B, fs); ww = fb.measureText(txt) + fs * 1.3
                px = edge - ww + fs * 0.65 + fb.measureText(txt[:-1]) + fb.measureText('.') / 2
                cv.drawCircle(px, y + fs * 0.25, fs * 0.42, P(col(CORAL, 0.7 * hl * a), blur=fs * 0.3))
                cv.drawCircle(px, y + fs * 0.25, fs * 0.13 * (1 + 0.4 * hl), P(col(CORAL, hl * a)))
        y += fs * 2.3
    cv.restore()
    cv.drawRoundRect(skia.Rect(-w * 0.12, sr.top() + w * 0.025, w * 0.12, sr.top() + w * 0.06), 8, 8, P(col('#000000', a)))
    cv.drawRRect(RR(r, rad), P(col('#FFFFFF', 0.25 * a), stroke=2.5))

def cphone3d(cv, cx, cy, w, h, a, t, ry=-14, rx=6, z=0, glowc=ACC, **kw):
    if a <= 0: return
    halo(cv, cx, cy, w * 1.1, glowc, 0.4 * a)
    with plane(cv, cx, cy, z, w, h, ry, rx) as ok:
        if ok: chat_phone3(cv, w, h, a, t, **kw)

def tube(cv, x, top, bot, w, v, a, t, c, glow=0.0):
    """tabung kaca 3D berisi cairan bergelombang (v 0..1)"""
    if a <= 0: return
    ew, eh = w / 2, w * 0.17
    if glow > 0: cv.drawRoundRect(skia.Rect(x - ew, top, x + ew, bot), ew, ew, P(col(c, 0.5 * glow * a), stroke=20, blur=26))
    cv.drawOval(skia.Rect(x - ew * 1.5, bot - 6, x + ew * 1.5, bot + 30), P(col('#000000', 0.5 * a), blur=14))
    cv.drawRect(skia.Rect(x - ew, top, x + ew, bot), P(col('#151628', 0.6 * a)))
    lvl = lerp(bot, top + eh, clamp(v))
    if v > 0.01:
        sh = lg(x - ew, 0, x + ew, 0, [col(mixc(c, '#000000', 0.45), a), col(mixc(c, '#FFFFFF', 0.25), a), col(c, a), col(mixc(c, '#000000', 0.5), a)], [0, 0.35, 0.6, 1])
        cv.drawRect(skia.Rect(x - ew, lvl, x + ew, bot), P(shader=sh))
        cv.drawOval(skia.Rect(x - ew, bot - eh, x + ew, bot + eh), P(shader=sh))
        wy = 3 * math.sin(t * 3 + x)
        cv.drawOval(skia.Rect(x - ew, lvl - eh + wy, x + ew, lvl + eh + wy), P(col(mixc(c, '#FFFFFF', 0.35), a)))
        cv.drawOval(skia.Rect(x - ew, lvl - eh + wy, x + ew, lvl + eh + wy), P(col('#FFFFFF', 0.5 * a), stroke=2))
    cv.drawRect(skia.Rect(x - ew * 0.62, top + eh, x - ew * 0.42, bot - eh), P(col('#FFFFFF', 0.22 * a), blur=4))
    cv.drawRect(skia.Rect(x + ew * 0.5, top + eh, x + ew * 0.58, bot - eh), P(col('#FFFFFF', 0.12 * a), blur=3))
    cv.drawLine(x - ew, top, x - ew, bot, P(col('#FFFFFF', 0.35 * a), stroke=2.5)); cv.drawLine(x + ew, top, x + ew, bot, P(col('#FFFFFF', 0.35 * a), stroke=2.5))
    cv.drawOval(skia.Rect(x - ew, top - eh, x + ew, top + eh), P(col('#FFFFFF', 0.45 * a), stroke=2.5))
    p = skia.Path(); p.addArc(skia.Rect(x - ew, bot - eh, x + ew, bot + eh), 0, 180)
    cv.drawPath(p, P(col('#FFFFFF', 0.35 * a), stroke=2.5))

def paper_scrap(cv, cx, cy, w, h, text, a, rot=-4.0, ink='#2A3A9A'):
    """sobekan kertas dengan tulisan tangan (miring)"""
    if a <= 0: return
    cv.save(); cv.translate(cx, cy); cv.rotate(rot)
    r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    cv.drawRect(r.makeOffset(6, 14), P(col('#000000', 0.45 * a), blur=14))
    cv.drawRect(r, P(shader=lg(0, -h / 2, 0, h / 2, [col('#FFF8E6', a), col('#EFE4C8', a)])))
    for k in range(1, 3): cv.drawLine(-w / 2 + 10, -h / 2 + k * h / 3, w / 2 - 10, -h / 2 + k * h / 3, P(col('#9AB0E0', 0.45 * a), stroke=1.5))
    f = font(M, h * 0.5); tw = f.measureText(text)
    cv.save(); cv.skew(-0.22, 0); cv.drawString(text, -tw / 2 + h * 0.08, bl(f, 0), f, P(col(ink, a))); cv.restore()
    cv.restore()

def cue_icon(cv, x, y, r, kind, a, t, off=0.0):
    """ikon isyarat tatap muka: 'voice' (gelombang nada suara) atau 'face' (ekspresi muka), dicoret saat off"""
    if a <= 0: return
    glass(cv, skia.Rect(x - r, y - r, x + r, y + r), rad=r, a=a, glow=0.35 * (1 - off), gc=ACC)
    ia = a * (1 - 0.65 * off)
    if kind == 'voice':
        for k in range(7):
            hh = r * (0.18 + 0.42 * abs(math.sin(t * 5 + k * 0.9))) * (1 - 0.6 * off)
            xx = x - r * 0.48 + k * r * 0.16
            cv.drawRoundRect(skia.Rect(xx - 5, y - hh, xx + 5, y + hh), 5, 5, P(col(ACC_XL, ia)))
    else:
        cv.drawCircle(x, y, r * 0.56, P(col(GOLD, 0.25 * ia)))
        cv.drawCircle(x, y, r * 0.56, P(col(GOLD, ia), stroke=4))
        br = 3 * math.sin(t * 4)
        for s_ in (-1, 1):
            cv.drawLine(x + s_ * r * 0.28 - 10, y - r * 0.22 + br, x + s_ * r * 0.28 + 10, y - r * 0.26 + br, P(col(GOLD, ia), stroke=4))
            cv.drawCircle(x + s_ * r * 0.2, y - r * 0.08, r * 0.06, P(col(GOLD, ia)))
        sm = skia.Path(); sm.addArc(skia.Rect(x - r * 0.26, y - r * 0.1, x + r * 0.26, y + r * 0.3), 20, 140)
        cv.drawPath(sm, P(col(GOLD, ia), stroke=4))
    if off > 0: cross(cv, x, y, r * 0.62, a, CORAL, d=off)

GLYPHS = [('.', CORAL), ('!', GOLD), ('?', ACC_XL), ('?!', MINT), (',', ROSE), ('!!', HOTPINK)]
def glyph_ring(cv, cx, cy, R, spin, a, t, tilt=0.3, center=None, size=120):
    """tanda baca 3D (titik = bola krom) mengorbit dalam perspektif, urut kedalaman"""
    items = []
    for k, (g, c) in enumerate(GLYPHS):
        x, y, z = ring_pos(k, len(GLYPHS), spin, R, tilt); items.append((z, k, x, y, g, c))
    items.sort(key=lambda it: -it[0]); drawn = False
    for z, k, x, y, g, c in items:
        if z < 0 and not drawn and center: center(); drawn = True
        X, Y, s = P3(cx + x, cy + y, z); dep = clamp((R - z) / (2 * R)); aa = a * lerp(0.35, 1.0, dep)
        if g == '.': chrome_dot(cv, X, Y, size * 0.26 * s, aa, t, glow=0.5 * dep, gc=c)
        else: extrude(cv, g, X, Y, size * s, aa, depth=10, front=('#FFFFFF', c), side=mixc(c, '#000000', 0.6), glow=c)
    if center and not drawn: center()

def ice_wall(cv, x, top, bot, u, a, t):
    """dinding es vertikal yang tumbuh dari tengah (u 0..1)"""
    if a <= 0 or u <= 0: return
    mid = (top + bot) / 2; y0 = lerp(mid, top, eo(u)); y1 = lerp(mid, bot, eo(u)); hw = 26
    r = skia.Rect(x - hw, y0, x + hw, y1)
    cv.drawRoundRect(r, 14, 14, P(col(ICE, 0.35 * a), blur=26))
    cv.drawRoundRect(r, 14, 14, P(shader=lg(x - hw, 0, x + hw, 0, [col('#CFEFFF', 0.25 * a), col('#8FD3FF', 0.45 * a), col('#CFEFFF', 0.2 * a)])))
    rnd = random.Random(21); pth = skia.Path()
    for k in range(10):
        yy = lerp(y0, y1, (k + 0.5) / 10); s_ = 1 if k % 2 else -1; L = rnd.uniform(40, 90) * eo(u)
        pth.moveTo(x, yy); pth.lineTo(x + s_ * L, yy - L * 0.5); pth.moveTo(x + s_ * L * 0.5, yy - L * 0.25); pth.lineTo(x + s_ * L * 0.7, yy + L * 0.05)
    cv.drawPath(pth, P(col('#F2FAFF', 0.7 * a), stroke=2.2))
    cv.drawRoundRect(r, 14, 14, P(col('#FFFFFF', 0.6 * a), stroke=2))

def key_back(cv, x, y, s, a, press=0.0, glow=0.0):
    """tombol hapus (backspace) kaca 3D"""
    if a <= 0: return
    d = 12 * (1 - press)
    r = skia.Rect(x - s, y - s * 0.7, x + s, y + s * 0.7)
    if glow > 0: cv.drawRoundRect(r, 20, 20, P(col(GOLD, 0.6 * glow * a), stroke=18, blur=24))
    cv.drawRoundRect(r.makeOffset(0, 14), 20, 20, P(col('#0A0B16', a)))
    rr = r.makeOffset(0, 14 - d)
    cv.drawRoundRect(rr, 20, 20, P(shader=lg(0, rr.top(), 0, rr.bottom(), [col('#4A4E7A', a), col('#24263E', a)])))
    cv.drawRoundRect(rr, 20, 20, P(col('#FFFFFF', 0.35 * a), stroke=2))
    cx, cy = rr.centerX(), rr.centerY(); k = s * 0.42
    pth = skia.Path(); pth.moveTo(cx - k * 1.25, cy); pth.lineTo(cx - k * 0.55, cy - k * 0.7); pth.lineTo(cx + k * 1.1, cy - k * 0.7)
    pth.lineTo(cx + k * 1.1, cy + k * 0.7); pth.lineTo(cx - k * 0.55, cy + k * 0.7); pth.close()
    cv.drawPath(pth, P(col(GOLD, a), stroke=4))
    for s_ in (-1, 1): cv.drawLine(cx + k * 0.05, cy - k * 0.32 * s_, cx + k * 0.65, cy + k * 0.32 * s_, P(col(GOLD, a), stroke=4))

def h_meter(cv, x0, x1, y, v, a, t, label, c):
    """meter kaca horizontal bercahaya dengan label di atas"""
    if a <= 0: return
    r = skia.Rect(x0, y - 22, x1, y + 22)
    glass(cv, r, rad=22, a=a, glow=0.2, gc=c, edge=c)
    xv = lerp(x0 + 8, x1 - 8, clamp(v))
    if v > 0.01:
        fr = skia.Rect(x0 + 8, y - 14, xv, y + 14)
        cv.drawRoundRect(fr, 14, 14, P(col(c, 0.6 * a), blur=10))
        cv.drawRoundRect(fr, 14, 14, P(shader=lg(x0, 0, x1, 0, [col(mixc(c, '#FFFFFF', 0.25), a), col(c, a)])))
    mono(cv, label, x0 + 4, y - 50, 20, mixc(c, '#FFFFFF', 0.3), a, sp=3, align=0)
    f = font(XB, 30); s_ = f'{int(round(v * 100))}%'; cv.drawString(s_, x1 - f.measureText(s_), bl(f, y - 52), f, P(col(TXT, a)))

# ------------------------------------------------------------ A: HOOK — kamu suka bales chat pakai titik? hati-hati, bisa kedengeran nggak tulus (0 - 5.88)
CHAT_A = [('L', 'besok jadi nongkrong?', 0.15), ('L', 'aku udah booking!', 0.45), ('R', 'oke.', 1.0)]
def gA(cv, t):
    zin = eo(prog(t, 0.0, 0.6)); push = lerp(1.08, 1.0, zin)
    cv.save(); cv.translate(540, 760); cv.scale(push, push); cv.translate(-540, -760)
    studio(cv, 1.0, t, ACC, x=560, cone=220)
    cv.restore()
    mv = eio(prog(t, 1.3, 2.0)); out = eio(prog(t, 4.85, 5.2))
    px = lerp(540, 250, mv); pw = lerp(380, 250, mv); py = lerp(680, 600, mv)
    cphone3d(cv, px, py + 8 * math.sin(t * 1.6), pw, pw * 1.75, 1.0 - 0.35 * mv - 0.5 * out, t, ry=lerp(-10, -26, mv) + 3 * math.sin(t * 0.9), rx=6,
             z=lerp(0, 80, mv), msgs=CHAT_A, hl=0.6 + 0.4 * math.sin(t * 6) if t > 1.15 else 0.0, cold=eo(prog(t, 2.1, 3.0)))
    ba = eo(prog(t, 1.35, 1.75)) * (1 - out)
    if ba > 0:
        fr = eo(prog(t, 2.12, 3.1)); hit = prog(t, 2.07, 2.15)
        drop = 0.0 if t >= 2.07 else lerp(150, 0, eio(prog(t, 1.75, 2.07))) if t > 1.75 else 150
        sy = shake(t, 2.07, 9, 0.5)
        sc = lerp(0.4, 1.0, bo(prog(t, 1.35, 1.75)))
        cv.save(); cv.translate(660, 520 + sy); cv.scale(sc, sc); cv.rotate(-3 + 2 * math.sin(t * 0.8)); cv.translate(-660, -520)
        big_bubble(cv, 660, 520, 'oke', 132, ba, t, dot=eo(prog(t, 1.55, 1.8)), frost_=fr, crack=prog(t, 2.07, 2.4), drop=drop, hl=0.4 * (1 - fr))
        cv.restore()
        if 0 < hit < 1 or 2.07 <= t < 2.5:
            u = prog(t, 2.07, 2.5); cv.drawCircle(780, 540, 60 + 160 * u, P(col(ICE, 0.5 * (1 - u) * ba), stroke=5))
        ma = eo(prog(t, 3.0, 3.3)) * (1 - out)
        if ma > 0:
            v = lerp(0.92, 0.28, eio(prog(t, 3.3, 4.2)))
            h_meter(cv, 450, 920, 790, v, ma, t, 'KESAN TULUS', mixc(MINT, CORAL, prog(t, 3.3, 4.0)))
        ta = eo(prog(t, 3.9, 4.15)) * (1 - out)
        if ta > 0: thought(cv, 'dia marah ya?', 560, 960, 30, ta, FRIEND, (770, 960), sc=lerp(0.6, 1, bo(prog(t, 3.9, 4.15))), fg='#FFFFFF')
        hero(cv, 840, 1110, 250, 'worried', ba * eo(prog(t, 2.3, 2.7)), t, sweat=0.6 if t > 3.9 else 0.0, glow=0.3, gc=FRIEND)
    c2 = prog(t, 4.88, 5.25)
    if c2 > 0:
        with plane(cv, 540, 640, lerp(500, 0, eo(c2)), 860, 220, lerp(30, 0, eo(c2)), 6) as ok:
            if ok: secret_card2(cv, 0, 0, 860, 220, 'TRIK 1 TANDA', TRIK, clamp(c2 * 3), t, reveal=0.0, glow=0.7, size=58)

# ------------------------------------------------------------ B: 2016, Celia Klin dan timnya (5.88 - 9.4)
def gB(cv, t):
    studio(cv, eo(prog(t, 5.88, 6.2)), t, ACC)
    research_card(cv, t, 5.92, '2016', 'Gunraj dkk. & Celia Klin', 'Binghamton Univ. · Computers in Human Behavior', None, None, 560, t_out=9.25, tag='CHB')
    da = eo(prog(t, 7.0, 7.4)) * (1 - eo(prog(t, 9.2, 9.45)))
    if da > 0:
        y = 1000 + 10 * math.sin(t * 1.8)
        chrome_dot(cv, 540, y - 20, 66, da, t, glow=0.5, gc=CORAL)
        mono(cv, 'SATU TANDA KECIL', 540, y + 76, 20, ACC_L, da, sp=4)

# ------------------------------------------------------------ C: 126 mahasiswa membaca chat yang dibalas satu kata, pakai titik vs nggak (9.4 - 14.36)
WORDS = ['oke', 'iya', 'sip', 'boleh', 'oke']
def gC(cv, t):
    a0 = eo(prog(t, 9.4, 9.7)); g_out = eo(prog(t, 10.75, 11.15))
    studio(cv, a0, t, ACC)
    ga = a0 * (1 - g_out)
    if ga > 0:
        extrude(cv, '126 MAHASISWA', 540, 420, 84 * lerp(1.2, 1, eo(prog(t, 9.4, 9.7))), ga, depth=12, front=('#FFFFFF', HL), side='#2E3270', glow=ACC)
        for k in range(126):
            u = prog(t, 9.42 + k * 0.005, 9.7 + k * 0.005)
            if u <= 0: continue
            x = 150 + (k % 14) * 60; y = 560 + (k // 14) * 62
            mini_person(cv, x, y, 34 * lerp(0.5, 1, bo(u)), ACC_L if k % 9 else FRIEND, ga * clamp(u * 3), lit=0.5 + 0.5 * math.sin(t * 2 + k * 0.4) ** 2)
    pa = eo(prog(t, 10.95, 11.4))
    if pa > 0:
        mono(cv, 'DIBALAS 1 KATA', 540, 330, 22, ACC_XL, pa, sp=4)
        wi = min(len(WORDS) - 1, max(0, int((t - 11.2) / 0.32))) if t > 11.2 else 0
        word = WORDS[wi] if t < 12.5 else 'oke'
        right_dot = t >= 12.51
        for k, (x, ry, lab, c, t0) in enumerate(((300, 14, 'TANPA TITIK', MINT, 13.34), (780, -14, 'PAKAI TITIK', CORAL, 12.51))):
            msgs = [('L', 'mau ikut nonton?', 11.0), ('R', word + ('.' if (k == 1 and right_dot) else ''), 11.2)]
            on = eo(prog(t, t0, t0 + 0.3))
            cphone3d(cv, x, 720 + 8 * math.sin(t * 1.4 + k), 300, 525, pa, t, ry=ry + 3 * math.sin(t * 0.8 + k), rx=5, z=lerp(200, 0, pa), glowc=c if on > 0 else ACC,
                     msgs=msgs, name='Raka' if k == 0 else 'Sasa', initial='R' if k == 0 else 'S', avc=FRIEND if k == 0 else GOLD, hl=on if k == 1 else 0.0)
            dd = eo(prog(t, 12.51, 12.8)) if k == 1 else 0.0
            cv.save(); cv.translate(x + 30, 800); cv.rotate(-3 if k == 0 else 3); cv.translate(-(x + 30), -800)
            big_bubble(cv, x + 30, 800 + 6 * math.sin(t * 2 + k), word, 78, pa * eo(prog(t, 11.2, 11.5)), t, dot=dd, hl=0.5 * dd, warm=0.4 * on if k == 0 else 0.0)
            cv.restore()
            if on > 0:
                chip(cv, lab, x, 420, pa * on, size=24, fg=INK, bgc=c, edge=c)
                if k == 1:
                    u = prog(t, 12.51, 13.0)
                    if 0 < u < 1: cv.drawCircle(880, 790, 40 + 140 * u, P(col(CORAL, 0.6 * (1 - u)), stroke=4))

# ------------------------------------------------------------ D: hasilnya? pakai titik = kurang tulus; ditulis tangan = nggak ada bedanya (14.36 - 20.28)
def gD(cv, t):
    a0 = eo(prog(t, 14.36, 14.65))
    studio(cv, a0, t, ACC)
    ha = eo(prog(t, 14.4, 14.7)) * (1 - eo(prog(t, 15.0, 15.3)))
    if ha > 0:
        cv.save(); cv.translate(540, 640); s_ = lerp(1.3, 1.0, eo(prog(t, 14.4, 14.7))); cv.scale(s_, s_)
        extrude(cv, 'HASILNYA?', 0, 0, 110, ha, depth=14); cv.restore()
    ta = eo(prog(t, 15.0, 15.35))
    if ta <= 0: return
    mono(cv, 'SEBERAPA TULUS?', 540, 330, 22, ACC_XL, ta, sp=4)
    sl = eio(prog(t, 17.28, 17.9))
    gx = lerp(540, 320, sl); gs = lerp(1.0, 0.78, sl); gap = 280 * gs
    top, bot = lerp(500, 540, sl), 980
    fill = eo(prog(t, 15.2, 16.0))
    for k, (dx, word, c, v) in enumerate(((-0.5, 'oke', MINT, 0.8), (0.5, 'oke', CORAL, 0.56))):
        x = gx + dx * gap
        tube(cv, x, top, bot, 150 * gs, v * fill, ta, t, c, glow=0.3 if k == 1 and t > 15.9 else 0.0)
        big_bubble(cv, x, top - 70, word, 52 * gs, ta, t, dot=1.0 if k == 1 else 0.0, hl=0.3 if k == 1 else 0.0)
    if sl > 0: mono(cv, 'DI CHAT', gx, 392, 22, ACC_L, ta * sl, sp=4)
    ka = eo(prog(t, 15.9, 16.2)) * (1 - sl)
    if ka > 0: chip(cv, 'KURANG TULUS', gx + 0.5 * gap, 1040, ta * ka, size=24, fg=INK, bgc=CORAL, edge=CORAL)
    pa = eo(prog(t, 18.0, 18.4))
    if pa > 0:
        rx_ = 790; pg = 0.78 * 280; pf = eo(prog(t, 18.4, 19.1))
        mono(cv, 'DI KERTAS', rx_, 392, 22, ACC_L, pa, sp=4)
        for k, (dx, word) in enumerate(((-0.5, 'oke'), (0.5, 'oke.'))):
            x = rx_ + dx * pg
            tube(cv, x, 540, 980, 150 * 0.78, 0.68 * pf, pa, t, GOLD)
            paper_scrap(cv, x, 480, 150, 70, word, pa, rot=-5 + 8 * k)
        ea = eo(prog(t, 19.0, 19.3))
        if ea > 0:
            chip(cv, 'NGGAK ADA BEDANYA', rx_, 1050, ea, size=24, fg=INK, bgc=MINT, edge=MINT)

# ------------------------------------------------------------ E: di chat nggak ada nada suara & muka, tanda baca yang ngegantiin (20.28 - 25.53)
CHAT_E = [('L', 'nanti kabarin ya', 20.45), ('R', 'oke', 20.75)]
def gE(cv, t):
    a0 = eo(prog(t, 20.28, 20.6))
    studio(cv, a0, t, ACC)
    ra = eo(prog(t, 23.47, 23.9)); ia = a0 * (1 - eo(prog(t, 23.35, 23.75)))
    spin = (t - 23.47) * 0.9
    def ph():
        cphone3d(cv, 540, 700 + 8 * math.sin(t * 1.3), 320, 560, a0, t, ry=-8 + 6 * math.sin(t * 0.7), rx=5, msgs=CHAT_E, name='Dimas', initial='D', avc=MINT)
    if ra > 0: glyph_ring(cv, 540, 700, lerp(150, 360, eo(ra)), spin, a0 * ra, t, tilt=0.32, center=ph, size=150)
    else: ph()
    if ia > 0:
        for k, (x, kind, lab, t0, t_off) in enumerate(((210, 'voice', 'NADA SUARA', 20.5, 22.1), (870, 'face', 'EKSPRESI MUKA', 20.65, 22.95))):
            q = prog(t, t0, t0 + 0.35)
            if q <= 0: continue
            off = eo(prog(t, t_off, t_off + 0.35))
            cv.save(); cv.translate(x, 500); s_ = lerp(0.6, 1, bo(q)); cv.scale(s_, s_); cv.translate(-x, -500)
            cue_icon(cv, x, 500, 92, kind, ia * clamp(q * 3), t, off=off)
            cv.restore()
            mono(cv, lab, x, 630, 19, CORAL if off > 0.5 else ACC_L, ia * clamp(q * 3), sp=3)
    if ra > 0: mono(cv, 'TANDA BACA = NADA', 540, 1075, 22, GOLD, a0 * eo(prog(t, 23.9, 24.2)), sp=5)

# ------------------------------------------------------------ F: titik di balasan singkat = nutup obrolan, kesannya ketus, padahal nggak marah (25.53 - 30.53)
FLOW = ['haha iya bener', 'terus terus?', 'seru banget tau!']
def gF(cv, t):
    a0 = eo(prog(t, 25.53, 25.85))
    studio(cv, a0, t, ICE)
    cold = eo(prog(t, 28.2, 28.9))
    if cold > 0:
        cv.drawRect(skia.Rect(540, 0, 1080, H), P(shader=lg(540, 0, 1080, 0, [col('#7FB8FF', 0), col('#7FB8FF', 0.1 * cold * a0)])))
    calm = eo(prog(t, 29.15, 29.5))
    hero(cv, 200, 1110, 270, 'calm' if calm > 0.5 else 'neutral', a0, t, glow=0.25 + 0.35 * calm, gc=MINT if calm > 0.5 else ACC)
    hero(cv, 880, 1110, 270, 'worried' if cold > 0.4 else 'happy', a0, t, sweat=0.5 * cold, glow=0.3, gc=FRIEND, tremble=0.2 * cold)
    fa = a0 * (1 - eo(prog(t, 27.4, 28.0)))
    for k, txt in enumerate(FLOW):
        q = prog(t, 25.6 + k * 0.25, 25.85 + k * 0.25)
        if q > 0: msg(cv, 1010, 470 + k * 78 + (1 - eo(q)) * 16, txt, 34, fa * clamp(q * 3), 'R', '#34365A' if k % 2 else '#3A4A8A')
    fly = prog(t, 26.35, 26.9)
    ba = eo(prog(t, 26.0, 26.3))
    dxy = (300, 560)
    if ba > 0:
        cv.save(); cv.translate(300, 560); cv.rotate(-3); cv.translate(-300, -560)
        dxy = big_bubble(cv, 300, 560, 'oke', 84, a0 * ba, t, dot=1.0 if fly <= 0 else 0.0, hl=0.5, frost_=0.5 * cold)
        cv.restore()
    wall = prog(t, 26.9, 27.6)
    ice_wall(cv, 540, 400, 1090, wall, a0, t)
    if fly > 0:
        u = eio(fly); x = lerp(dxy[0], 540, u); y = lerp(dxy[1], 720, u) - 280 * math.sin(math.pi * u); rr = lerp(84 * 0.4, 96, u)
        if t > 26.9: x, y, rr = 540, 720 - 12 * bump(prog(t, 26.9, 27.2)) + shake(t, 26.9, 8, 0.4), 96
        cv.drawOval(skia.Rect(x - rr * 1.1, 1095, x + rr * 1.1, 1125), P(col('#000000', 0.5 * a0 * u), blur=16))
        chrome_dot(cv, x, y, rr, a0, t, cold=eo(prog(t, 27.0, 27.8)), glow=0.4, gc=ICE)
        if 26.9 <= t < 27.5:
            uu = prog(t, 26.9, 27.5); cv.drawCircle(540, 720, 100 + 260 * uu, P(col(ICE, 0.55 * (1 - uu) * a0), stroke=6))
    oa = eo(prog(t, 27.0, 27.3))
    if oa > 0: extrude(cv, 'OBROLAN DITUTUP', 540, 340, 58, a0 * oa, depth=8, front=('#FFFFFF', '#CFEFFF'), side='#1E3A5A', glow=ICE)
    ka = eo(prog(t, 28.2, 28.5))
    if ka > 0:
        thought(cv, 'dia marah ya?', 820, 680, 30, a0 * ka, FRIEND, (870, 860), sc=lerp(0.6, 1, bo(ka)), fg='#FFFFFF')
        chip(cv, 'KESANNYA KETUS', 820, 540, a0 * ka, size=22, fg=INK, bgc=CORAL, edge=CORAL)
    if calm > 0:
        thought(cv, 'aku biasa aja kok', 285, 735, 28, a0 * calm, MINT, (210, 860), sc=lerp(0.6, 1, bo(calm)), fg='#FFFFFF')

# ------------------------------------------------------------ G: balas satu kata? coba trik kecil: hapus titiknya (30.53 - 34.26)
def gG(cv, t):
    a0 = eo(prog(t, 30.53, 30.85)); rv = eio(prog(t, 33.12, 33.6))
    studio(cv, a0, t, GOLD)
    if rv > 0:
        rays(cv, 540, 420, 560, 0.6 * rv * a0, t, n=18, c=GOLD, spin=6)
        halo(cv, 540, 420, 460, GOLD, 0.5 * rv * a0)
    with plane(cv, 540, 420, 0, 900, 230, 4 * math.sin(t * 0.8), 4) as ok:
        if ok:
            s_ = 1 + 0.05 * bump(prog(t, 33.5, 33.9)); cv.scale(s_, s_)
            secret_card2(cv, 0, 0, 900, 230, 'TRIK 1 TANDA', TRIK, a0, t, reveal=rv, glow=0.5 + 0.5 * rv, size=62)
    press = bump(prog(t, 33.3, 33.55)); gone = eo(prog(t, 33.35, 33.6)); warm = eo(prog(t, 33.5, 34.0))
    ba = eo(prog(t, 30.7, 31.1))
    if ba > 0:
        cv.save(); cv.translate(470, 790); cv.rotate(-2 + 1.5 * math.sin(t * 0.8)); cv.translate(-470, -790)
        big_bubble(cv, 470, 790, 'oke', 124, a0 * ba, t, dot=1 - gone, frost_=0.65 * (1 - warm), warm=warm, burst=prog(t, 33.38, 33.9),
                   cursor=1.0 if t > 32.3 else 0.0, hl=0.5 * (1 - gone) if t > 31.2 else 0.0)
        cv.restore()
    ka = eo(prog(t, 32.26, 32.6))
    if ka > 0: key_back(cv, 830, 780, 70, a0 * ka, press=press, glow=0.6 * bump(prog(t, 33.2, 33.8)) + 0.3)
    ha = eo(prog(t, 33.6, 34.0))
    hero(cv, 860, 1110, 210, 'happy' if ha > 0.5 else 'worried', a0 * eo(prog(t, 30.8, 31.2)), t, glow=0.3 + 0.3 * ha, gc=MINT if ha > 0.5 else FRIEND)
    if ha > 0:
        mono(cv, 'JADI KERASA HANGAT', 470, 950, 20, MINT, a0 * ha, sp=4)

# ------------------------------------------------------------ H: kirim ke teman yang suka bales pakai titik (34.26 - 36.6)
SHARE = [('bestie', '#FF7FC8'), ('teman kerja', '#7FB8FF'), ('teman kelas', '#FFC56B'), ('pacar', '#3FD6A4')]
PICK = 0
def gH(cv, t):
    a0 = eo(prog(t, 34.26, 34.52))
    halo(cv, 540, 600, 460, ACC, 0.35 * a0)
    r = skia.Rect(130, 290, 950, 530)
    pth = glass(cv, r, rad=34, a=a0, glow=0.7, gc=GOLD, edge=GOLD, fill=('#302A3A', '#16141F'))
    cv.drawRoundRect(r, 34, 34, P(col(GOLD, 0.85 * a0), stroke=2.5))
    mono(cv, 'SIMPAN TRIK INI', r.left() + 40, r.top() + 40, 21, GOLD, 0.9 * a0, sp=4, align=0)
    f = font(XB, 56)
    for k, s2 in enumerate(TRIK):
        y = bl(f, r.top() + 112 + k * 70); x = r.left() + 54
        cv.drawString(s2, x, y, f, P(col(GOLD, 0.45 * a0), blur=10)); cv.drawString(s2, x, y, f, P(shader=lg(0, y - 46, 0, y, [col('#FFFFFF', a0), col('#FFE3B0', a0)])))
    chrome_dot(cv, 860, 380, 34, a0 * (1 - eo(prog(t, 34.6, 34.9))), t, glow=0.4)
    sparks(cv, 860, 380, 70, prog(t, 34.6, 35.1), a0, GOLD)
    sheen(cv, pth, r, prog(t, 34.34, 35.14), a0)
    sa = eo(prog(t, 34.44, 34.69))
    if sa > 0:
        cy = 720; sr = skia.Rect(130, cy - 110, 950, cy + 110)
        glass(cv, sr, rad=30, a=sa * a0, glow=0.3)
        mono(cv, 'KIRIM KE', sr.left() + 40, sr.top() + 36, 21, ACC_L, sa * a0, sp=4, align=0)
        sent = eo(prog(t, 35.29, 35.54))
        for k, (nm, c) in enumerate(SHARE):
            x = 240 + k * 200; q = prog(t, 34.49 + 0.07 * k, 34.79 + 0.07 * k)
            if q <= 0: continue
            aa = sa * a0 * clamp(q * 3); s_ = lerp(0.6, 1, bo(q))
            cv.save(); cv.translate(x, cy + 6); cv.scale(s_, s_); cv.translate(-x, -(cy + 6))
            avatar(cv, x, cy + 6, 42, c, aa, ok=sent if k == PICK else 0.0)
            f2 = font(B, 22); w2 = f2.measureText(nm); cv.drawString(nm, x - w2 / 2, bl(f2, cy + 78), f2, P(col(TXT if k == PICK else MUTED, aa)))
            cv.restore()
        fp = prog(t, 34.69, 35.29)
        if 0 < fp < 1:
            tx = 240 + PICK * 200; x = lerp(700, tx, eio(fp)); y = lerp(530, cy - 10, eio(fp)) - 40 * math.sin(math.pi * fp)
            plane_icon(cv, x, y, 34 * (1 - 0.3 * fp), a0, rot=lerp(-30, 20, fp))
        if sent > 0:
            rp = prog(t, 35.29, 35.84)
            if 0 < rp < 1: cv.drawCircle(240 + PICK * 200, cy + 6, 50 + 80 * rp, P(col(MINT, 0.6 * (1 - rp) * a0), stroke=4))
            chip(cv, 'TERKIRIM', 760, sr.top() + 36, sent * a0, size=22, fg=INK, bgc=MINT, edge=MINT)
    hero(cv, 290, 1110, 250, 'happy', a0, t, glow=0.5, gc=MINT); hero(cv, 790, 1110, 250, 'excited', a0, t, glow=0.5, gc=GOLD)


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
    ev = [(0.0, 'whoosh'), (0.15, 'plip'), (0.45, 'plip'), (1.0, 'pop'), (1.2, 'tick'), (1.35, 'zoom'), (2.07, 'clunk'), (2.1, 'crack'), (2.3, 'fizz_soft'), (3.3, 'tick'), (3.6, 'tick'), (3.9, 'pop'), (4.88, 'card'), (4.95, 'shine'),
          (5.88, 'whoosh'), (5.94, 'card'), (6.24, 'stamp'), (6.52, 'ding_soft'), (7.0, 'pop'),
          (9.4, 'whoosh'), (9.5, 'rise'), (10.95, 'swish'), (11.2, 'tick'), (11.52, 'tick'), (11.84, 'tick'), (12.16, 'tick'), (12.51, 'pop'), (12.55, 'ding_soft'), (13.34, 'pop'),
          (14.36, 'whoosh'), (14.4, 'chop'), (15.2, 'rise'), (15.9, 'sting'), (17.28, 'swish'), (18.0, 'card'), (18.4, 'rise'), (19.0, 'ding'),
          (20.28, 'whoosh'), (20.5, 'pop'), (20.65, 'pop'), (22.1, 'chop'), (22.95, 'chop'), (23.47, 'zoom'), (23.6, 'shine'),
          (25.53, 'whoosh'), (25.7, 'plip'), (26.02, 'plip'), (26.34, 'plip'), (26.9, 'clunk'), (26.95, 'crack'), (27.05, 'fizz'), (28.2, 'sting'), (28.3, 'pop'), (29.15, 'pop'), (29.2, 'ding_soft'),
          (30.53, 'whoosh'), (30.7, 'pop'), (32.26, 'pop'), (33.12, 'clunk'), (33.2, 'shine'), (33.3, 'tick'), (33.38, 'pop'), (33.5, 'fizz_soft'), (33.75, 'ding'),
          (34.26, 'whoosh'), (34.44, 'swish'), (34.6, 'pop'), (34.69, 'zoom'), (35.29, 'ding'), (35.34, 'pop'),
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







