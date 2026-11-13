import skia, math, os
from logo import P, col, font, head_path
BLACK, CARD, WHITE, GREY, RULE = '#0B0B0C', '#151517', '#F3F1EC', '#8A8884', '#2A2A2D'
def open_head():
    p = skia.Path()
    p.moveTo(372, 905); p.cubicTo(372, 840, 330, 800, 300, 735); p.cubicTo(240, 600, 262, 420, 372, 330)
    p.cubicTo(470, 250, 640, 238, 742, 318); p.cubicTo(812, 372, 838, 452, 830, 530); p.cubicTo(828, 552, 832, 566, 842, 582)
    p.lineTo(888, 652); p.cubicTo(898, 668, 890, 680, 872, 684); p.lineTo(852, 688); p.cubicTo(860, 704, 858, 716, 846, 724)
    p.cubicTo(856, 736, 854, 752, 840, 760); p.cubicTo(846, 790, 834, 812, 800, 818); p.cubicTo(752, 826, 712, 826, 690, 846)
    p.cubicTo(672, 862, 668, 884, 670, 905)
    return p
def spiral(cx, cy, a, b, th_end, steps=400):
    p = skia.Path(); first = True
    for i in range(steps + 1):
        th = th_end * i / steps; r = a + b * th
        x, y = cx + r * math.cos(th), cy + r * math.sin(th)
        (p.moveTo if first else p.lineTo)(x, y); first = False
    return p, (cx + (a + b * th_end) * math.cos(th_end), cy + (a + b * th_end) * math.sin(th_end))
W = lambda a=1: col(WHITE, a)

def c_A(cv):  # garis tunggal
    cv.translate(-80, -60)
    cv.drawPath(open_head(), P(W(), stroke=16))
    sp, end = spiral(565, 505, 8, 18, 3 * math.pi)
    sp.cubicTo(end[0] - 4, end[1] - 70, end[0] - 90, end[1] - 40, 258, 470)
    cv.drawPath(sp, P(W(), stroke=16))
    cv.drawCircle(565, 505, 20, P(W()))

def c_B(cv):  # gelembung pikiran
    cv.translate(-150, -10)
    cv.drawPath(head_path(), P(W()))
    for (x, y, r) in ((880, 360, 24), (930, 270, 38), (960, 140, 60)): cv.drawCircle(x, y, r, P(W()))

def c_C(cv):  # lapisan pikiran
    cv.translate(-80, -60)
    hp = open_head()
    cv.drawPath(hp, P(W(), stroke=16))
    for k, a in ((0.78, 0.85), (0.58, 0.7), (0.38, 0.55)):
        m = skia.Matrix(); m.setScale(k, k, 560, 470); q = skia.Path(); head_path().transform(m, q)
        cv.drawPath(q, P(W(a), stroke=12))
    cv.drawCircle(568, 452, 22, P(W()))

def c_D(cv):  # jaringan pikiran
    cv.translate(-80, -60)
    cv.drawPath(open_head(), P(W(), stroke=16))
    N = [(400, 420), (470, 340), (575, 320), (680, 360), (740, 450), (640, 450), (520, 440), (430, 540), (560, 560), (680, 560), (610, 650), (470, 640)]
    for i, a in enumerate(N):
        for j, b in enumerate(N):
            if j > i and math.dist(a, b) < 175: cv.drawLine(*a, *b, P(W(0.55), stroke=6))
    for i, (x, y) in enumerate(N):
        if i == 5: cv.drawCircle(x, y, 44, P(W(0.18))); cv.drawCircle(x, y, 26, P(W()))
        else: cv.drawCircle(x, y, 13, P(W()))

def c_E(cv):  # pikiran terbuka
    cv.translate(-80, -10)
    hp = head_path()
    cut = skia.Path(); cut.moveTo(150, 520); cut.cubicTo(400, 430, 650, 420, 950, 455); cut.lineTo(950, 1000); cut.lineTo(150, 1000); cut.close()
    lower = skia.Op(hp, cut, skia.PathOp.kIntersect_PathOp); upper = skia.Op(hp, cut, skia.PathOp.kDifference_PathOp)
    cv.drawPath(lower, P(W()))
    cv.save(); cv.translate(-4, -18); cv.rotate(-21, 262, 500); cv.drawPath(upper, P(W())); cv.restore()
    for (x, y, r, a) in ((820, 330, 18, 1), (870, 250, 13, .85), (800, 205, 11, .7), (905, 160, 9, .55), (850, 100, 7, .45), (930, 60, 6, .35)):
        cv.drawCircle(x, y, r, P(W(a)))

def c_F(cv):  # spiral negatif
    cv.translate(-80, -60)
    cv.drawPath(head_path(), P(W()))
    sp, end = spiral(560, 500, 6, 17, 3 * math.pi)
    cv.drawPath(sp, P(col(BLACK), stroke=24)); cv.drawCircle(560, 500, 22, P(col(BLACK)))

CONCEPTS = [('A', 'Garis Tunggal', 'Satu garis membentuk kepala lalu berputar jadi pikiran', c_A),
            ('B', 'Gelembung Pikiran', 'Kepala solid, pikiran melayang naik', c_B),
            ('C', 'Lapisan Pikiran', 'Kepala berlapis, makin ke dalam makin dalam', c_C),
            ('D', 'Jaringan Pikiran', 'Pikiran sebagai titik-titik yang saling terhubung', c_D),
            ('E', 'Pikiran Terbuka', 'Kepala terbuka, isi pikiran keluar', c_E),
            ('F', 'Spiral Dalam', 'Kepala solid dengan pusaran pikiran di dalamnya', c_F)]

def avatar(fn, size):
    s = skia.Surface(size, size); cv = s.getCanvas(); cv.clear(skia.ColorTRANSPARENT)
    clip = skia.Path(); clip.addCircle(size / 2, size / 2, size / 2)
    cv.save(); cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect(0, 0, size, size), P(shader=skia.GradientShader.MakeRadial(skia.Point(size * .5, size * .42), size * .75, [col('#1B1B1E'), col(BLACK)])))
    k = size / 1000 * 0.82; cv.translate(size / 2 - 500 * k, size / 2 - 500 * k); cv.scale(k, k); fn(cv)
    cv.restore(); return s.makeImageSnapshot()

def wordmark(cv, x, y, size, color=WHITE, sub=True):
    f = font('CormorantGaramond-SemiBold.ttf', size); tr = size * 0.2
    for ch in 'BENAK': cv.drawString(ch, x, y, f, P(col(color))); x0 = x; x += f.measureText(ch) + tr
    total = x - tr
    if sub:
        fs = font('PlusJakartaSans-Medium.ttf', size * 0.16); t = 'PSIKOLOGI SEHARI-HARI'; xx = x - (x - tr)  # placeholder
        sx = None
    return total

def lockup(fn, w=1500, h=480):
    s = skia.Surface(w, h); cv = s.getCanvas(); cv.clear(col(BLACK))
    cv.save(); cv.translate(30, 15); cv.scale(0.45, 0.45); fn(cv); cv.restore()
    x0 = 540; end = wordmark(cv, x0, 290, 220)
    fs = font('PlusJakartaSans-Medium.ttf', 34); t = 'PSIKOLOGI SEHARI-HARI'; sp = 11
    x = x0 + 6
    for ch in t: cv.drawString(ch, x, 370, fs, P(col(GREY))); x += fs.measureText(ch) + sp
    return s.makeImageSnapshot()

if __name__ == '__main__':
    os.makedirs('out/premium', exist_ok=True)
    for L, name, desc, fn in CONCEPTS:
        slug = name.lower().replace(' ', '-')
        avatar(fn, 1080).save(f'out/premium/benak-{L}-{slug}.png', skia.kPNG)
        lockup(fn).save(f'out/premium/benak-{L}-{slug}-logo.png', skia.kPNG)
    CW, CH, cols = 860, 520, 2; rows = 3
    SW, SH = 90 * 2 + CW * 2 + 40, 240 + rows * CH + (rows - 1) * 40 + 90
    s = skia.Surface(SW, SH); cv = s.getCanvas(); cv.clear(col('#070708'))
    cv.drawString('BENAK · Referensi logo premium', 90, 130, font('CormorantGaramond-SemiBold.ttf', 70), P(col(WHITE)))
    cv.drawString('Kepala + pikiran · hitam premium · pilih huruf A–F', 90, 186, font('PlusJakartaSans-Medium.ttf', 30), P(col(GREY)))
    for i, (L, name, desc, fn) in enumerate(CONCEPTS):
        x0 = 90 + (i % cols) * (CW + 40); y0 = 240 + (i // cols) * (CH + 40)
        r = skia.Rect.MakeXYWH(x0, y0, CW, CH)
        cv.drawRoundRect(r, 30, 30, P(col(CARD))); cv.drawRoundRect(r, 30, 30, P(col('#ffffff', 0.06), stroke=2))
        cv.drawImage(avatar(fn, 300), x0 + 40, y0 + 40)
        cv.drawCircle(x0 + 190, y0 + 190, 150, P(col('#ffffff', 0.08), stroke=2))
        cv.drawImage(avatar(fn, 72), x0 + 40, y0 + 390); cv.drawImage(avatar(fn, 44), x0 + 128, y0 + 404)
        cv.drawString('ukuran kecil', x0 + 190, y0 + 434, font('PlusJakartaSans-Medium.ttf', 20), P(col('#66645F')))
        lk = lockup(fn); cv.save(); cv.translate(x0 + 380, y0 + 60); cv.scale(0.3, 0.3); cv.drawImage(lk, 0, 0); cv.restore()
        cv.drawRoundRect(skia.Rect.MakeXYWH(x0 + 380, y0 + 60, 450, 144), 10, 10, P(col('#ffffff', 0.06), stroke=2))
        b = skia.Rect.MakeXYWH(x0 + 380, y0 + 262, 60, 60)
        cv.drawRoundRect(b, 30, 30, P(col(WHITE), stroke=2.5))
        fb = font('CormorantGaramond-SemiBold.ttf', 42); cv.drawString(L, b.centerX() - fb.measureText(L) / 2, b.centerY() + 14, fb, P(col(WHITE)))
        cv.drawString(name, x0 + 460, y0 + 303, font('PlusJakartaSans-Bold.ttf', 36), P(col(WHITE)))
        fd = font('PlusJakartaSans-Medium.ttf', 25); words = desc.split(); line = ''; yy = y0 + 372
        for wd in words:
            t = (line + ' ' + wd).strip()
            if fd.measureText(t) > CW - 420: cv.drawString(line, x0 + 380, yy, fd, P(col(GREY))); yy += 36; line = wd
            else: line = t
        cv.drawString(line, x0 + 380, yy, fd, P(col(GREY)))
    s.makeImageSnapshot().save('out/premium/benak-referensi-logo-premium.png', skia.kPNG)
    print('ok', SW, SH)
