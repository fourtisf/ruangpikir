import skia, math, os, random
from logo import P, col, font, head_path
from premium import open_head, spiral
BG0, BG1 = '#16161A', '#060607'
def lg(x0, y0, x1, y1, cs, pos=None): return skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], [col(c) if isinstance(c, str) else c for c in cs], pos)
def rg(x, y, r, cs, pos=None): return skia.GradientShader.MakeRadial(skia.Point(x, y), r, [col(c) if isinstance(c, str) else c for c in cs], pos)
HEAD_FILL = lambda: lg(300, 240, 840, 900, ['#34343B', '#1C1C21', '#121215'], [0, .55, 1])

def dark_head(cv, accent, glow=True, path=None):
    hp = path or head_path()
    if glow: cv.drawPath(hp, P(col(accent, 0.35), stroke=26, blur=22))
    cv.drawPath(hp, P(shader=HEAD_FILL()))
    cv.drawPath(hp, P(col(accent), stroke=9))
    return hp

# 1 ISI KEPALA: galaksi pikiran di dalam kepala (ungu)
def c1(cv):
    A = '#9A7BFF'; cv.translate(-80, -55); hp = dark_head(cv, A)
    cv.save(); cv.clipPath(hp, skia.ClipOp.kIntersect, True)
    cv.drawCircle(560, 480, 230, P(shader=rg(560, 480, 230, [col(A, 0.45), col(A, 0.0)])))
    random.seed(5)
    for k in range(260):
        arm = k % 3; t = random.uniform(0, 1)
        ang = t * 4.2 + arm * 2.094; r = 18 + t * 200
        x = 560 + math.cos(ang) * r * 1.1 + random.gauss(0, 10); y = 480 + math.sin(ang) * r * 0.8 + random.gauss(0, 10)
        cv.drawCircle(x, y, random.uniform(2.5, 7.5) * (1.2 - t * 0.6), P(col(random.choice(['#C9B8FF', A, '#E4DAFF', '#7F5CFF']), random.uniform(.55, 1))))
    cv.drawCircle(560, 480, 22, P(col('#E8E0FF'))); cv.drawCircle(560, 480, 46, P(col(A, 0.5), blur=16))
    cv.restore()

# 2 BAWAH SADAR: gunung es Freud berbentuk kepala (biru laut)
def c2(cv):
    A = '#3CC6D6'; cv.translate(-80, -40); hp = head_path(); wl = 440
    cv.drawPath(hp, P(col(A, 0.3), stroke=26, blur=24))
    above = skia.Path(); above.addRect(skia.Rect(0, 0, 1100, wl)); top = skia.Op(hp, above, skia.PathOp.kIntersect_PathOp); bot = skia.Op(hp, above, skia.PathOp.kDifference_PathOp)
    cv.drawPath(bot, P(shader=lg(0, wl, 0, 905, ['#1B6E86', '#0E3A4F', '#0A2433'])))
    cv.drawPath(top, P(shader=lg(0, 240, 0, wl, ['#BFF3F7', '#6FD9E4'])))
    cv.drawPath(hp, P(col(A), stroke=8))
    w = skia.Path(); w.moveTo(60, wl)
    for i in range(1, 25): x = 60 + i * 42; w.lineTo(x, wl + 7 * math.sin(i * 1.4))
    cv.drawPath(w, P(col('#8BE6EF'), stroke=7))
    cv.save(); cv.clipPath(bot, skia.ClipOp.kIntersect, True)
    for (x, y, r) in ((470, 600, 9), (610, 680, 6), (540, 760, 11), (680, 560, 5), (420, 720, 6)): cv.drawCircle(x, y, r, P(col('#8BE6EF', .55), stroke=3))
    cv.restore()

# 3 PSIKOFAKTA: simbol psikologi Ψ di dalam kepala (merah ruby)
def c3(cv):
    A = '#FF4D6A'; cv.translate(-80, -55); dark_head(cv, A)
    cx, top, bot = 560, 330, 690
    psi = skia.Path(); psi.moveTo(cx - 140, top + 10); psi.cubicTo(cx - 140, top + 190, cx - 90, top + 245, cx, top + 245)
    psi.cubicTo(cx + 90, top + 245, cx + 140, top + 190, cx + 140, top + 10)
    cv.drawPath(psi, P(col(A, .5), stroke=60, blur=18)); cv.drawPath(psi, P(col(A), stroke=46))
    cv.drawLine(cx, top - 30, cx, bot, P(col(A), stroke=46))
    cv.drawLine(cx - 70, bot, cx + 70, bot, P(col(A), stroke=34))

# 4 RUANG PIKIR: pintu terbuka bercahaya di dalam kepala (biru keunguan)
def c4(cv):
    A = '#7F8CFF'; cv.translate(-80, -55); hp = dark_head(cv, A)
    dx0, dy0, dx1, dy1 = 480, 340, 640, 640
    cv.save(); cv.clipPath(hp, skia.ClipOp.kIntersect, True)
    beam = skia.Path(); beam.moveTo(dx0, dy1); beam.lineTo(dx1, dy1); beam.lineTo(dx1 + 200, 900); beam.lineTo(dx0 - 160, 900); beam.close()
    cv.drawPath(beam, P(shader=lg(0, dy1, 0, 880, [col('#AEB6FF', 0.55), col('#AEB6FF', 0.0)])))
    cv.restore()
    cv.drawRoundRect(skia.Rect(dx0, dy0, dx1, dy1), 80, 80, P(col('#C9CEFF', 0.5), blur=26))
    door = skia.RRect.MakeRectXY(skia.Rect(dx0, dy0, dx1, dy1), 80, 80)
    cv.drawRRect(door, P(shader=lg(0, dy0, 0, dy1, ['#E3E6FF', '#9AA5FF'])))
    leaf = skia.Path(); leaf.moveTo(dx0, dy0 + 70); leaf.cubicTo(dx0, dy0 + 20, dx0 + 20, dy0, dx0 + 60, dy0 + 8)
    leaf.lineTo(dx0 + 82, dy0 + 40); leaf.lineTo(dx0 + 82, dy1 + 30); leaf.lineTo(dx0, dy1); leaf.close()
    cv.drawPath(leaf, P(shader=lg(dx0, 0, dx0 + 82, 0, ['#2A2D52', '#3B3F78'])))
    cv.drawCircle(dx0 + 62, dy0 + 170, 9, P(col('#9AA5FF')))

# 5 OVERTHINK: pikiran kusut meledak dari kepala (merah koral)
def c5(cv):
    A = '#FF6B57'; cv.translate(-80, 10); dark_head(cv, A)
    pts = []
    for k in range(521):
        u = k / 520 * math.tau * 1.8
        x = 0.62 * math.sin(3.1 * u + 2) + 0.38 * math.sin(7.7 * u + 3.0); y = 0.62 * math.cos(2.3 * u + 1) + 0.38 * math.cos(6.1 * u + 2.0)
        pts.append((560 + x * 230, 250 + y * 150))
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    cv.drawPath(p, P(col(A, .45), stroke=22, blur=12)); cv.drawPath(p, P(col(A), stroke=9))

# 6 NALAR: jaringan pikiran (hijau zamrud)
def c6(cv):
    A = '#3FD6A4'; cv.translate(-80, -55); hp = dark_head(cv, A)
    N = [(400, 420), (470, 340), (575, 320), (680, 360), (740, 450), (640, 450), (520, 440), (430, 540), (560, 560), (680, 560), (610, 650), (470, 640)]
    for i, a in enumerate(N):
        for j, b in enumerate(N):
            if j > i and math.dist(a, b) < 175: cv.drawLine(*a, *b, P(col(A, 0.6), stroke=6))
    for i, (x, y) in enumerate(N):
        if i == 5: cv.drawCircle(x, y, 50, P(col(A, 0.35), blur=14)); cv.drawCircle(x, y, 26, P(col('#B6F5DE')))
        else: cv.drawCircle(x, y, 13, P(col(A)))

CONCEPTS = [('1', 'ISI KEPALA', '@isikepala', 'Galaksi pikiran di dalam kepala', c1, '#9A7BFF'),
            ('2', 'BAWAH SADAR', '@bawahsadar', 'Gunung es Freud: yang terlihat cuma sedikit', c2, '#3CC6D6'),
            ('3', 'PSIKOFAKTA', '@psikofakta', 'Simbol Psi, lambang resmi ilmu psikologi', c3, '#FF4D6A'),
            ('4', 'RUANG PIKIR', '@ruangpikir', 'Pintu ke ruang paling dalam di kepala', c4, '#7F8CFF'),
            ('5', 'OVERTHINK', '@overthink.id', 'Isi kepala yang nggak bisa diem', c5, '#FF6B57'),
            ('6', 'NALAR', '@nalar.id', 'Pikiran yang saling terhubung', c6, '#3FD6A4')]

def tile(fn, size):
    s = skia.Surface(size, size); cv = s.getCanvas()
    cv.drawRect(skia.Rect(0, 0, size, size), P(shader=rg(size * .5, size * .45, size * .75, [BG0, BG1])))
    k = size / 1000 * 0.8; cv.translate(size / 2 - 500 * k, size / 2 - 500 * k); cv.scale(k, k); fn(cv)
    return s.makeImageSnapshot()

def circ(img, size, bg):
    s = skia.Surface(size, size); cv = s.getCanvas(); cv.clear(col(bg))
    c = skia.Path(); c.addCircle(size / 2, size / 2, size / 2); cv.clipPath(c, skia.ClipOp.kIntersect, True)
    cv.drawImageRect(img, skia.Rect(0, 0, size, size), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)); return s.makeImageSnapshot()

if __name__ == '__main__':
    os.makedirs('out/v3', exist_ok=True)
    big = {}
    for n, name, handle, desc, fn, acc in CONCEPTS:
        im = tile(fn, 1080); big[n] = im
        im.save(f'out/v3/logo-{n}-{name.lower().replace(" ", "-")}.png', skia.kPNG)
    CW, CH, cols, rows = 600, 860, 3, 2
    SW, SH = 80 * 2 + CW * cols + 30 * (cols - 1), 250 + CH * rows + 30 + 70
    s = skia.Surface(SW, SH); cv = s.getCanvas(); cv.clear(col('#050506'))
    cv.drawString('Referensi logo + nama brand', 80, 125, font('PlusJakartaSans-ExtraBold.ttf', 64), P(col('#EDEBF2')))
    cv.drawString('Foto profil Instagram · background penuh · pilih nomor 1–6', 80, 180, font('PlusJakartaSans-Medium.ttf', 30), P(col('#8C8A94')))
    for i, (n, name, handle, desc, fn, acc) in enumerate(CONCEPTS):
        x0 = 80 + (i % cols) * (CW + 30); y0 = 240 + (i // cols) * (CH + 30)
        r = skia.Rect.MakeXYWH(x0, y0, CW, CH)
        cv.drawRoundRect(r, 30, 30, P(col('#111114'))); cv.drawRoundRect(r, 30, 30, P(col('#ffffff', 0.06), stroke=2))
        sq = big[n]
        cv.save(); cc = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 + 30, y0 + 30, 540, 540), 22, 22); cv.clipRRect(cc, skia.ClipOp.kIntersect, True)
        cv.drawImageRect(sq, skia.Rect.MakeXYWH(x0 + 30, y0 + 30, 540, 540), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)); cv.restore()
        fn_ = font('PlusJakartaSans-ExtraBold.ttf', 44); nm = name; sp = 6
        xx = x0 + 30
        for ch in nm: cv.drawString(ch, xx, y0 + 640, fn_, P(col('#EDEBF2'))); xx += fn_.measureText(ch) + sp
        cv.drawString(f'{n}', x0 + CW - 70, y0 + 640, font('PlusJakartaSans-ExtraBold.ttf', 44), P(col(acc)))
        cv.drawString(handle, x0 + 30, y0 + 686, font('PlusJakartaSans-SemiBold.ttf', 28), P(col(acc)))
        cv.drawString(desc, x0 + 30, y0 + 730, font('PlusJakartaSans-Medium.ttf', 24), P(col('#8C8A94')))
        cv.drawImage(circ(sq, 84, '#111114'), x0 + 30, y0 + 756)
        cv.drawImage(circ(sq, 48, '#111114'), x0 + 130, y0 + 774)
        cv.drawString('tampilan bulat IG', x0 + 196, y0 + 806, font('PlusJakartaSans-Medium.ttf', 20), P(col('#5E5C66')))
    s.makeImageSnapshot().save('out/v3/referensi-logo-nama.png', skia.kPNG)
    print('ok', SW, SH)
