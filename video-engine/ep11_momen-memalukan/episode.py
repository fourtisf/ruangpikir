#!/usr/bin/env python3
"""Ruang Pikir reel #11: 'Momen memalukan, kok keinget terus?' (McGaugh 2004; Berntsen, ingatan tak diundang;
Gilovich dkk. 2000; Leary dkk. 2007)
Gaya "kamar jam 2 pagi + arsip ingatan": kamar gelap dengan jendela bulan, orang berbaring yang matanya melotot lalu terpejam,
polaroid momen memalukan (wajah meringis) yang muncul di langit-langit, lemari arsip ingatan + stempel PENTING, siang sibuk vs
malam santai, sorot lampu, jaringan "semua orang pernah malu", tangan hangat yang melunakkan ingatan.
python3 episode.py preview t1 t2 ... | timeline out.json | video out.mp4"""
import sys, os, math, json, subprocess, random
import skia
import base as b
from base import (clamp, lerp, prog, eo, ei, eio, bo, bump, col, P, lg, rg, layer, font, XB, B, M, MONO, bl, tracked, parse,
                 pill, sparkle, person, ACC, ACC_L, ACC_XL, TXT, MUTED, CORAL, MINT, W, H, FPS)

VIOLET, YELLOW, INK, HL = '#B57BFF', '#FFD23F', '#0B0C1E', '#AEB6FF'

# adegan (waktu animasi, DUR 42); tag tidak ditampilkan
b.GROUPS = [(0.0, 4.8, 'A'), (4.8, 9.0, 'B'), (9.0, 15.31, 'C'), (15.31, 22.0, 'D'), (22.0, 26.2, 'E'),
            (26.2, 31.23, 'F'), (31.23, 36.6, 'G'), (36.6, 42.0, 'J')]
PHRASES = [(0.15, 'Kamu pasti masih ingat'), (1.11, 'momen paling [memalukanmu].'), (2.72, 'Otakmu memang [sengaja menyimpannya].'),
           (4.8, 'Apalagi pas [mau tidur],'), (6.31, 'tiba-tiba [muncul lagi],'), (7.52, 'bikin pengen [teriak ke bantal].'),
           (9.0, 'Tahun [2004],'), (10.1, '[James McGaugh] menjelaskan:'), (11.46, 'saat [emosi memuncak],'), (12.79, 'amigdala bikin ingatan [tersimpan lebih kuat].'),
           (15.31, 'Kenapa munculnya pas [mau tidur]?'), (17.01, 'Ingatan tak diundang paling sering datang'), (18.87, 'saat pikiran lagi [santai],'), (20.58, 'kata [Dorthe Berntsen].'),
           (22.0, 'Padahal orang lain jauh lebih jarang'), (23.9, '[memperhatikan kita] dari yang kita kira.'),
           (26.2, 'Jadi kalau [muncul lagi],'), (27.55, 'bilang ke diri sendiri:'), (28.63, '"semua orang [pernah malu],'), (29.79, 'dan itu [manusiawi]."'),
           (31.23, 'Riset [Mark Leary]:'), (32.43, '[baik ke diri sendiri] bikin kita menerima kesalahan,'), (35.05, 'tanpa [tenggelam dalam malu].'),
           (36.6, 'Follow [Ruang Pikir],'), (37.99, 'biar makin kenal [isi kepalamu].')]
b.CAPS = [(t, s, '') for t, s in PHRASES]          # dipakai base hanya untuk jadwal

# ------------------------------------------------------------ chrome gaya sinematik
b.draw_tag = lambda cv, t: None
b.draw_progress = lambda cv, t: None
def draw_title(cv, t):
    a = eo(prog(t, 0.05, 0.35)) * (1 - eio(prog(t, 4.45, 4.85)))
    if a <= 0: return
    segs = parse("Momen memalukan, [kok keinget terus]?"); size = 60; f = font(XB, size)
    tot = sum(f.measureText(s) for s, _ in segs)
    if tot > 940: size *= 940 / tot; f = font(XB, size); tot = sum(f.measureText(s) for s, _ in segs)
    x = 540 - tot / 2; y = bl(f, 232) + (1 - eo(prog(t, 0.05, 0.35))) * 16 - 10 * eio(prog(t, 4.45, 4.85))
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
    # cahaya bulan dingin dari kanan atas (tanpa titik/bokeh)
    cv.drawCircle(900, 380, 900, P(shader=rg(900, 380, 900, [col('#AFC3FF', 0.07), col('#7F8CFF', 0.03), col('#7F8CFF', 0)], [0, 0.5, 1])))
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
# ------------------------------------------------------------ helper EP11: kamar jam 2 pagi + arsip ingatan (polaroid momen memalukan)
CRINGE = [('salah manggil guru "mama"', ('#FF9AC1', '#B57BFF')), ('dadah ke orang yang bukan dadah ke aku', ('#FFC56B', '#FF7F7F')),
          ('kepleset di depan gebetan', ('#7FB8FF', '#6A4BD6')), ('salah kirim chat ke grup keluarga', ('#5AD1E6', '#3F6BFF')),
          ('jawab "kamu juga" ke kasir', ('#9FE08A', '#3FB98A'))]
MOON = '#DDE6FF'

def cringe_face(cv, cx, cy, r, a=1.0, t=0.0):
    """wajah meringis malu: mata terpejam rapat, mulut gelombang, pipi merah"""
    if a <= 0: return
    sphere(cv, cx, cy, r, ('#FFE3C9', '#F2A97F', '#8A4A3A'), a, 0.4)
    ink = P(col('#3A1C20', 0.9 * a), stroke=max(3, r * 0.08))
    for s in (-1, 1):
        ex, ey = cx + s * r * 0.33, cy - r * 0.08
        e = skia.Path(); e.moveTo(ex - s * r * 0.15, ey - r * 0.07); e.lineTo(ex + s * r * 0.05, ey + r * 0.02); e.lineTo(ex - s * r * 0.15, ey + r * 0.11)
        cv.drawPath(e, ink)
        cv.drawOval(skia.Rect(ex - r * 0.17, ey + r * 0.2, ex + r * 0.17, ey + r * 0.34), P(col('#FF5A6A', 0.5 * a), blur=r * 0.05))
    m = skia.Path(); my = cy + r * 0.42
    for i in range(7):
        x = cx - r * 0.24 + i * r * 0.08; y = my + (r * 0.04 if i % 2 else -r * 0.04)
        (m.moveTo if i == 0 else m.lineTo)(x, y)
    cv.drawPath(m, ink)
    sw = skia.Path(); sx, sy = cx + r * 0.72, cy - r * 0.45
    sw.moveTo(sx, sy - r * 0.18); sw.quadTo(sx + r * 0.12, sy + r * 0.05, sx, sy + r * 0.1); sw.quadTo(sx - r * 0.12, sy + r * 0.05, sx, sy - r * 0.18)
    cv.drawPath(sw, P(col('#BFE6FF', 0.9 * a)))

def polaroid(cv, w, k, a, t, heat=1.0, soft=0.0):
    """polaroid momen memalukan (koordinat lokal, pusat 0,0): foto bergradasi + wajah meringis + keterangan tulisan tangan"""
    if a <= 0: return
    cap, (c1, c2) = CRINGE[k % len(CRINGE)]
    h = w * 1.22; r = skia.Rect(-w / 2, -h / 2, w / 2, h / 2)
    if heat > 0: cv.drawRect(r.makeOutset(10, 10), P(col('#FF4A5A', 0.55 * heat * a), blur=26))
    cv.drawRect(r.makeOffset(0, 16), P(col('#000000', 0.5 * a), blur=20))
    cv.drawRect(r, P(col(mixc('#F6F2EA', '#E6E4F2', soft), a)))
    im = skia.Rect(-w * 0.43, -h * 0.43, w * 0.43, h * 0.2)
    cv.drawRect(im, P(shader=lg(0, im.top(), 0, im.bottom(), [col(mixc(c1, '#8C93FF', soft * 0.6), a), col(mixc(c2, '#4A4FD0', soft * 0.6), a)])))
    cv.save(); cv.clipRect(im, skia.ClipOp.kIntersect, True)
    if soft < 0.5: cringe_face(cv, 0, im.centerY() + w * 0.04, w * 0.22, a * (1 - soft * 2) if soft > 0 else a, t)
    if soft > 0: mood_ball(cv, 0, im.centerY() + w * 0.04, w * 0.22, a * clamp(soft * 2 - 0.0), t, 'smile_closed', ('#E3FFF6', '#8C93FF', '#2A2470'))
    cv.restore()
    f = font(B, w * 0.075); words = cap.split(' '); lines, cur = [], ''
    for wd in words:
        if f.measureText((cur + ' ' + wd).strip()) > w * 0.84: lines.append(cur); cur = wd
        else: cur = (cur + ' ' + wd).strip()
    lines.append(cur)
    for li, ln in enumerate(lines[:2]):
        cv.drawString(ln, -f.measureText(ln) / 2, bl(f, h * 0.28 + li * w * 0.095), f, P(col('#2A2D55', a)))

def pol3d(cv, x, y, z, w, k, a, t, ry=0.0, rx=0.0, rz=0.0, heat=1.0, soft=0.0):
    with plane(cv, x, y, z, w, w * 1.22, ry, rx, rz) as ok:
        if ok: polaroid(cv, w, k, a, t, heat, soft)

def bedroom(cv, a, t, eye=1.0, pillow=0.0, calm=0.0, blush=0.0):
    """kamar gelap: jendela + bulan, kasur samping, orang berbaring (mata terbuka/terpejam), bantal bisa menutup wajah"""
    if a <= 0: return
    wx, wy = 820, 470
    win = skia.Rect(wx - 130, wy - 150, wx + 130, wy + 150)
    cv.drawRect(win, P(shader=lg(0, win.top(), 0, win.bottom(), [col('#1E2A5A', 0.9 * a), col('#0E1430', 0.9 * a)])))
    cv.drawCircle(wx + 40, wy - 60, 46, P(col(MOON, 0.9 * a))); cv.drawCircle(wx + 62, wy - 74, 44, P(col('#1A2550', 0.95 * a)))
    halo(cv, wx + 30, wy - 60, 200, MOON, 0.35 * a)
    cv.drawRect(win, P(col('#8C93FF', 0.6 * a), stroke=6)); cv.drawLine(wx, win.top(), wx, win.bottom(), P(col('#8C93FF', 0.6 * a), stroke=4)); cv.drawLine(win.left(), wy, win.right(), wy, P(col('#8C93FF', 0.6 * a), stroke=4))
    beam = skia.Path(); beam.moveTo(win.left(), win.top()); beam.lineTo(win.right(), win.top()); beam.lineTo(560, 1200); beam.lineTo(120, 1200); beam.close()
    cv.drawPath(beam, P(shader=lg(0, win.top(), 0, 1200, [col(MOON, 0.08 * a), col(MOON, 0)])))
    by = 1000
    cv.drawRoundRect(skia.Rect(120, by - 40, 960, by + 90), 26, 26, P(col('#1A1C34', a)))
    cv.drawRoundRect(skia.Rect(120, by - 40, 960, by - 10), 14, 14, P(col('#2A2D55', a)))
    cv.drawRoundRect(skia.Rect(150, by - 120, 420, by - 30), 40, 40, P(shader=lg(0, by - 120, 0, by - 30, [col('#E6E8F6', 0.95 * a), col('#B9BCD6', 0.95 * a)])))
    hx, hy = 300, by - 120
    cv.drawCircle(hx, hy, 70, P(shader=rg(hx - 20, hy - 25, 100, [col('#5A5F9E', a), col('#2E3160', a)])))
    hair = skia.Path(); hair.addArc(skia.Rect(hx - 72, hy - 74, hx + 72, hy + 70), 160, 200); cv.drawPath(hair, P(col('#15162A', a), stroke=26))
    if eye > 0.1:
        bk = blink_at(t, 0.2) * 0.9
        eh = 9 * eye * (1 - bk)
        cv.drawOval(skia.Rect(hx + 14, hy - 4 - eh, hx + 40, hy - 4 + eh), P(col('#F0EFF6', a)))
        if eh > 3: cv.drawCircle(hx + 30, hy - 6, 5, P(col('#15162A', a)))
    else:
        cl = skia.Path(); cl.moveTo(hx + 12, hy - 4); cl.quadTo(hx + 27, hy + 6, hx + 42, hy - 4); cv.drawPath(cl, P(col('#C9CBE0', a), stroke=4))
    if blush > 0: cv.drawOval(skia.Rect(hx + 10, hy + 14, hx + 46, hy + 30), P(col('#FF5A6A', 0.6 * blush * a), blur=6))
    bl_ = skia.Path(); bl_.moveTo(330, by - 60)
    bl_.cubicTo(450, by - 140 - 10 * math.sin(t * 1.2), 620, by - 90, 760, by - 120); bl_.cubicTo(860, by - 140, 930, by - 80, 950, by - 20); bl_.lineTo(330, by - 20); bl_.close()
    cv.drawPath(bl_, P(shader=lg(0, by - 140, 0, by, [col(mixc('#4A4FD0', '#3A6A8A', calm), a), col(mixc('#262A6A', '#1E3A4A', calm), a)])))
    cv.drawPath(bl_, P(col('#AEB6FF', 0.3 * a), stroke=2))
    if pillow > 0:
        px = lerp(230, hx + 10, eio(pillow)); py = lerp(by - 75, hy - 5, eio(pillow)); rot = lerp(0, -25, eio(pillow))
        cv.save(); cv.translate(px, py); cv.rotate(rot + 4 * math.sin(t * 25) * pillow)
        cv.drawRoundRect(skia.Rect(-130, -50, 130, 50), 40, 40, P(col('#000000', 0.4 * a), blur=14))
        cv.drawRoundRect(skia.Rect(-130, -50, 130, 50), 40, 40, P(shader=lg(0, -50, 0, 50, [col('#F2F3FA', a), col('#C2C5DE', a)]))); cv.restore()

def cabinet(cv, cx, cy, s, a, t, open_=0.0, glow=0.0):
    """lemari arsip ingatan 3 laci; laci atas 'PENTING' bisa terbuka"""
    if a <= 0: return
    w, h = s, s * 1.3; r = skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    cv.drawRect(r.makeOffset(0, 24), P(col('#000000', 0.5 * a), blur=24))
    cv.drawRoundRect(r, 18, 18, P(shader=lg(r.left(), 0, r.right(), 0, [col('#3A3D66', a), col('#5A5F9E', a), col('#2E3160', a)])))
    for k, lab in enumerate(('PENTING', 'BIASA', 'LUPA')):
        dy = r.top() + h * (0.08 + k * 0.31); dh = h * 0.27
        off = (s * 0.32 * eo(open_)) if k == 0 else 0
        dr = skia.Rect(r.left() + w * 0.07, dy + off * 0.15, r.right() - w * 0.07, dy + dh + off * 0.15)
        if k == 0 and glow > 0: cv.drawRoundRect(dr, 12, 12, P(col('#FF4A5A', 0.6 * glow * a), stroke=16, blur=14))
        cv.drawRoundRect(dr, 12, 12, P(shader=lg(0, dr.top(), 0, dr.bottom(), [col(mixc('#6A6FB8', '#B84A5A', glow if k == 0 else 0), a), col(mixc('#3A3D66', '#5A1E2A', glow if k == 0 else 0), a)])))
        cv.drawRoundRect(dr, 12, 12, P(col('#FFFFFF', 0.25 * a), stroke=2))
        cv.drawRoundRect(skia.Rect(dr.centerX() - w * 0.12, dr.top() + dh * 0.6, dr.centerX() + w * 0.12, dr.top() + dh * 0.72), 6, 6, P(col('#C9CCE0', a)))
        lr = skia.Rect(dr.centerX() - w * 0.2, dr.top() + dh * 0.16, dr.centerX() + w * 0.2, dr.top() + dh * 0.46)
        cv.drawRect(lr, P(col('#F6F2EA', a))); f = font(MONO, dh * 0.2)
        cv.drawString(lab, lr.centerX() - f.measureText(lab) / 2, bl(f, lr.centerY()), f, P(col('#C2303A' if k == 0 else '#2A2D55', a)))

def chips_flow(cv, y, t, a, items, speed=260, gap=270, c=ACC_L):
    """rentetan pikiran sehari-hari yang mengalir (siang = sibuk)"""
    if a <= 0: return
    tot = gap * len(items)
    for k, txt in enumerate(items):
        x = (k * gap - t * speed) % tot - 120
        chip(cv, txt, x, y + (k % 2) * 70, a, size=28, fg=ACC_XL)

# ------------------------------------------------------------ A: HOOK — momen memalukan muncul di langit-langit kamar (0 - 4.8)
def gA(cv, t):
    sx = shake(t, 0.08, 12, 0.5)
    cv.save(); cv.translate(sx, 0)
    bedroom(cv, 1.0, t, eye=lerp(0.4, 1.4, eo(prog(t, 0.0, 0.2))), blush=eo(prog(t, 0.2, 0.6)))
    cv.restore()
    fl = prog(t, -0.05, 0.4)
    if 0 < fl < 1: cv.drawCircle(540, 600, 640, P(shader=rg(540, 600, 640, [col('#FF7F9A', 0.45 * (1 - fl)), col('#FF7F9A', 0)])))
    for k, (t0, x, y, rz, w) in enumerate(((-0.1, 470, 560, -6, 330), (1.1, 220, 470, 9, 230), (1.75, 760, 690, -10, 220), (2.72, 330, 760, 5, 210))):
        pa = prog(t, t0, t0 + 0.28)
        if pa <= 0: continue
        sc = lerp(1.5, 1.0, eo(pa)) if k == 0 else lerp(0.4, 1.0, bo(pa))
        pol3d(cv, x, y + 6 * math.sin(t * 1.3 + k), lerp(-300, 0, eo(pa)) if k == 0 else 0, w * sc, k, clamp(pa * 3), t, 6 * math.sin(t + k), 0, rz, 0.8)
    if prog(t, 2.72, 3.0) > 0:
        g = prog(t, 2.72, 3.2)
        mono(cv, 'DISIMPAN OTAK', 540, 300, 30, '#FF9AA6', eo(g) * (0.75 + 0.25 * math.sin(t * 8)), sp=5, glow=0.6)

# ------------------------------------------------------------ B: mau tidur, muncul lagi, teriak ke bantal (4.8 - 9.0)
def gB(cv, t):
    a0 = eo(prog(t, 4.8, 5.1)); pil = eio(prog(t, 7.52, 7.85))
    bedroom(cv, a0, t, eye=1.0, pillow=pil, blush=1.0)
    for k, (t0, x, y, rz) in enumerate(((5.0, 540, 560, -4), (6.31, 300, 480, 8), (6.6, 790, 520, -9))):
        pa = prog(t, t0, t0 + 0.3)
        if pa > 0: pol3d(cv, x, y + 5 * math.sin(t * 1.4 + k), 0, 230 * lerp(0.4, 1, bo(pa)), (k + 1) % 5, a0 * clamp(pa * 3), t, 5 * math.sin(t + k), 0, rz, 0.9)
    if pil > 0.5:
        u = prog(t, 7.75, 8.9)
        for k in range(3):
            v = clamp(u * 1.3 - k * 0.2)
            if 0 < v < 1:
                arc = skia.Path(); arc.addArc(skia.Rect(320 - 80 - 160 * v, 880 - 60 - 120 * v, 320 + 80 + 160 * v, 880 + 60 + 120 * v), 200, 140)
                cv.drawPath(arc, P(col('#FF9AA6', 0.7 * (1 - v) * a0), stroke=5))
        cv.save(); cv.translate(560, 790); cv.rotate(-8); s = lerp(1.6, 1, eo(prog(t, 7.8, 8.0)))
        cv.scale(s, s); extrude(cv, 'AAAAA!', 0, 0, 92, a0 * clamp(prog(t, 7.8, 7.95) * 3) * 0.85, depth=8, front=('#FFFFFF', '#FFB3C0'), side='#5A1530', glow=CORAL); cv.restore()
        mono(cv, '(teredam bantal)', 600, 880, 22, MUTED, a0 * eo(prog(t, 8.1, 8.4)))

# ------------------------------------------------------------ C: 2004, McGaugh: emosi memuncak -> amigdala bikin ingatan tersimpan kuat (9.0 - 15.31)
def gC(cv, t):
    research_card(cv, t, 9.0, '2004', 'James McGaugh', 'Annual Review of Neuroscience', None, None, 700, 11.25)
    a0 = eo(prog(t, 11.3, 11.7))
    if a0 <= 0: return
    cabinet(cv, 760, 760, 300, a0, t, prog(t, 13.5, 13.9) * (1 - prog(t, 14.5, 14.9)), eo(prog(t, 14.2, 14.6)))
    em = eo(prog(t, 11.46, 12.4))
    x0, y0 = 300, 640
    cv.drawCircle(x0, y0, 150 + 40 * em, P(shader=rg(x0, y0, 150 + 40 * em, [col('#FF4A5A', 0.55 * em * a0), col('#FF4A5A', 0)])))
    lv = skia.Rect(x0 - 26, y0 - 170, x0 + 26, y0 + 170)
    cv.drawRoundRect(lv, 26, 26, P(col('#1A1B30', 0.9 * a0))); cv.drawRoundRect(lv, 26, 26, P(col(ACC_XL, 0.4 * a0), stroke=2))
    fh = (lv.height() - 16) * (0.15 + 0.8 * em * (0.92 + 0.08 * math.sin(t * 9)))
    fr = skia.Rect(lv.left() + 8, lv.bottom() - 8 - fh, lv.right() - 8, lv.bottom() - 8)
    cv.drawRoundRect(fr, 18, 18, P(shader=lg(0, fr.top(), 0, fr.bottom(), [col('#FFB36B', a0), col('#FF4A5A', a0)])))
    mono(cv, 'EMOSI', x0, lv.top() - 32, 24, '#FF9AA6', a0, sp=3)
    mv = prog(t, 12.8, 13.6)
    px = lerp(x0 + 40, 760, eio(prog(t, 13.6, 14.3))); py = lerp(y0 + 230, 650, eio(prog(t, 13.6, 14.3))) - 60 * bump(prog(t, 13.6, 14.3))
    ps = lerp(1.0, 0.45, eio(prog(t, 13.6, 14.3)))
    if t < 14.35: pol3d(cv, px if t >= 13.6 else x0 + 140, py if t >= 13.6 else y0 + 260, 0, 200 * ps, 0, a0, t, 0, 0, -6, 0.9)
    stamp(cv, 'PENTING', x0 + 150, y0 + 250, 46, t, 12.85, CORAL, -12, a0 * (1 - eio(prog(t, 13.5, 13.7))))
    mono(cv, 'amigdala: "simpan kuat-kuat!"', 540, 1110, 26, '#FF9AA6', a0 * eo(prog(t, 12.9, 13.3)), sp=1, glow=0.5)

# ------------------------------------------------------------ D: munculnya pas mau tidur: pikiran santai (15.31 - 22.0)
DAY = ['kerjaan', 'chat grup', 'macet', 'makan apa', 'tugas', 'meeting', 'cucian']
def gD(cv, t):
    a0 = eo(prog(t, 15.31, 15.7)); night = eio(prog(t, 17.0, 17.6))
    cv.drawRect(skia.Rect(0, 150, W, 1220), P(shader=lg(0, 150, 0, 1220, [col('#FFC98A', 0), col('#FFC98A', 0.12 * (1 - night) * a0), col('#FFC98A', 0)], [0, 0.25, 1])))
    ic = 540
    if night < 1:
        cv.drawCircle(ic, 380, 54 * (1 - night), P(col('#FFD98A', a0 * (1 - night)))); halo(cv, ic, 380, 160, '#FFC98A', a0 * (1 - night))
    if night > 0:
        cv.drawCircle(ic, 380, 50 * night, P(col(MOON, a0 * night))); cv.drawCircle(ic + 22 * night, 366, 46 * night, P(col('#121A3A', a0 * night)))
    mono(cv, '14.00' if night < 0.5 else '23.47', 540, 470, 36, ACC_L, a0, sp=2)
    chips_flow(cv, 600, t, a0 * (1 - night), DAY)
    chips_flow(cv, 760, t * 1.2 + 3, a0 * (1 - night), DAY[::-1])
    cabinet(cv, 540, 980, 220, a0, t, eo(prog(t, 18.2, 18.6)), 0.7 * night)
    up = eo(prog(t, 18.5, 19.6))
    if up > 0:
        pol3d(cv, 540 + 30 * math.sin(t * 2), lerp(900, 640, up), 0, lerp(80, 240, up), 3, a0 * up, t, 6 * math.sin(t), 0, -5, 0.9)
        if night > 0.5: chip(cv, 'pikiran lagi santai', 270, 560, a0 * eo(prog(t, 19.0, 19.3)), size=26, fg=HL)
    if night < 0.5:
        dd = eo(prog(t, 15.5, 15.9))
        mono(cv, 'pikiran sibuk', 540, 530, 26, '#FFD98A', a0 * dd * (1 - night * 2), sp=3)
    ca = eo(prog(t, 20.58, 20.9))
    chip(cv, 'Dorthe Berntsen · ingatan tak diundang', 540, 1150, a0 * ca, size=24, fg=ACC_XL)

# ------------------------------------------------------------ E: orang lain jauh lebih jarang memperhatikan (22.0 - 26.2)
def gE(cv, t):
    a0 = eo(prog(t, 22.0, 22.4)); shrink = eio(prog(t, 23.9, 24.6))
    cone = skia.Path(); cone.moveTo(330, 255); cone.lineTo(390, 255); cone.lineTo(lerp(560, 470, shrink), 1060); cone.lineTo(lerp(160, 250, shrink), 1060); cone.close()
    cv.drawPath(cone, P(shader=lg(0, 255, 0, 1060, [col('#DDE0FF', 0.2 * a0), col('#AEB6FF', 0.06 * a0)])))
    stander(cv, 360, 1060, 300, a0, '#DDE0FF')
    pol3d(cv, 360, 560, 0, lerp(300, 120, shrink), 2, a0, t, 4 * math.sin(t), 0, -4, lerp(0.9, 0.2, shrink))
    mono(cv, 'YANG KAMU KIRA', 360, 330, 22, '#FF9AA6', a0 * (1 - shrink), sp=3)
    for k, (x, y, txt) in enumerate(((680, 1080, 'laper'), (820, 1110, 'deadline'), (960, 1075, 'drakor'))):
        pa = eo(prog(t, 22.2 + k * 0.1, 22.6 + k * 0.1)); bust(cv, x, y, 80, a0 * pa, '#AEB6FF')
        qa = eo(prog(t, 24.0 + k * 0.18, 24.35 + k * 0.18))
        if qa > 0: thought(cv, txt, min(x, 940), 820 + (k % 2) * 80, 26, a0 * qa, ACC_L, (x, y - 110), lerp(0.6, 1, bo(qa)))
    chip(cv, 'spotlight effect · Gilovich dkk. (2000)', 540, 1170, a0 * eo(prog(t, 24.6, 24.9)), size=22, fg=ACC_XL)

# ------------------------------------------------------------ F: semua orang pernah malu, itu manusiawi (26.2 - 31.23)
def gF(cv, t):
    a0 = eo(prog(t, 26.2, 26.6))
    pts = [(220, 520), (540, 470), (860, 520), (180, 790), (900, 790), (300, 1040), (540, 1080), (780, 1040)]
    con = eo(prog(t, 29.79, 30.4))
    for k, (x, y) in enumerate(pts):
        if con > 0:
            p_ = skia.Path(); p_.moveTo(540, 780); p_.lineTo(x, y); neon(cv, p_, con, MINT, 3, a0 * 0.7, 0.7, MINT)
    for k, (x, y) in enumerate(pts):
        pa = eo(prog(t, 27.6 + k * 0.08, 27.95 + k * 0.08))
        avatar(cv, x, y, 52, AV_COL[k], a0 * pa, con, 0.0)
        qa = eo(prog(t, 28.63 + k * 0.07, 28.95 + k * 0.07))
        if qa > 0: pol3d(cv, x + 62, y - 62, 0, 74 * lerp(0.5, 1, bo(qa)), k, a0 * qa, t, 0, 0, (k % 3 - 1) * 8, 0.5 * (1 - con))
    you = eo(prog(t, 26.3, 26.7))
    pp = prog(t, 26.35, 26.65); po = 1 - eio(prog(t, 27.4, 27.8))
    if pp > 0 and po > 0: pol3d(cv, 540, 560 - 40 * eo(pp), 0, 220 * lerp(0.4, 1, bo(pp)) * lerp(0.5, 1, po), 0, a0 * clamp(pp * 3) * po, t, 4 * math.sin(t), 0, -5, 0.9)
    mood_ball(cv, 540, 780, 78, a0 * you, t, 'smile_closed' if con > 0.5 else 'flat', GRN if con > 0.5 else GREY)
    mono(cv, 'kamu', 540, 885, 24, ACC_L, a0 * you, sp=3)
    if con > 0.5: mono(cv, 'SEMUA ORANG PERNAH MALU', 540, 330, 28, MINT, a0 * prog(con, 0.5, 1.0), sp=3, glow=0.6)

# ------------------------------------------------------------ G: Leary: baik ke diri sendiri -> terima kesalahan tanpa tenggelam dalam malu (31.23 - 36.6)
def gG(cv, t):
    a0 = eo(prog(t, 31.23, 31.6)); soft = eio(prog(t, 33.0, 34.4)); sleep = eio(prog(t, 35.05, 35.8))
    bedroom(cv, a0, t, eye=1.0 - sleep * 1.2, calm=soft, blush=1 - soft)
    pol3d(cv, 540, 560, 0, 260, 0, a0, t, 5 * math.sin(t), 0, -4 + 4 * soft, 0.9 * (1 - soft), soft)
    hp = prog(t, 32.43, 33.2)
    if hp > 0:
        hx = lerp(920, 690, eio(hp)); hy = lerp(380, 470, eio(hp)) + 8 * math.sin(t * 3)
        halo(cv, 560, 560, 320, '#FFC98A', 0.55 * a0 * soft)
        for k in range(2):
            u = ((t - 32.9) * 0.8 + k / 2) % 1.0
            if t > 33.0: cv.drawCircle(560, 560, 150 + 220 * u, P(col('#FFC98A', 0.45 * (1 - u) * a0 * soft), stroke=4))
        heart_shape(cv, hx, hy, 44 * (1 + 0.1 * math.sin(t * 6)), a0 * clamp(hp * 3), '#FFC98A')
    chip(cv, 'Mark Leary dkk. (2007) · self-compassion', 540, 330, a0 * eo(prog(t, 31.5, 31.9)), size=24, fg=ACC_XL)
    if sleep > 0:
        for k in range(3):
            u = ((t * 0.6 + k / 3) % 1.0)
            mono(cv, 'z', 380 + k * 40 + 30 * u, 820 - 140 * u, 30 + 14 * k, ACC_L, a0 * sleep * (1 - u))

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

b.DRAWERS = [gA, gB, gC, gD, gE, gF, gG, gJ]

def build_sfx():
    ev = [(0.03, 'chop'), (0.05, 'stamp'), (0.08, 'crack'), (0.1, 'fizz_soft'), (1.1, 'pop'), (1.75, 'pop'), (2.72, 'pop'), (2.8, 'ding_soft'),
          (4.8, 'whoosh'), (5.0, 'pop'), (6.31, 'pop'), (6.6, 'pop'), (7.52, 'swish'), (7.8, 'boing'), (7.82, 'buzzer'),
          (9.0, 'whoosh'), (9.1, 'card'), (9.4, 'stamp'), (9.7, 'ding_soft'), (11.25, 'whoosh'), (11.46, 'rise'), (12.85, 'chop'), (12.88, 'stamp'),
          (13.6, 'swish'), (14.3, 'clunk'), (14.45, 'clunk'),
          (15.31, 'whoosh'), (15.5, 'tick'), (15.8, 'tick'), (16.1, 'tick'), (16.4, 'tick'), (17.0, 'zoom'), (17.4, 'shine'), (18.2, 'clunk'), (18.5, 'rise'), (19.6, 'ding_soft'),
          (22.0, 'whoosh'), (22.2, 'pop'), (22.3, 'pop'), (22.4, 'pop'), (23.9, 'fizz_soft'), (24.0, 'plip'), (24.18, 'plip'), (24.36, 'plip'),
          (26.2, 'whoosh'), (26.3, 'pop'), (27.6, 'plip'), (27.84, 'plip'), (28.08, 'plip'), (28.63, 'pop'), (29.79, 'shine'), (30.0, 'ding'),
          (31.23, 'whoosh'), (31.5, 'card'), (32.43, 'swish'), (33.0, 'shine'), (34.4, 'ding_soft'), (35.05, 'fizz_soft'),
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





