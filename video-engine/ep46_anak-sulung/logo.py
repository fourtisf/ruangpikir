import skia, math, os, sys
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
def col(h, a=1.0):
    h = h.lstrip('#'); return skia.Color(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), int(a*255))
PLUM, PLUM2, LILAC, LILAC2, CORAL, INK = '#170F33', '#2B1D5E', '#B9A4FF', '#8F74F0', '#FF8C69', '#F5F0FF'
def P(c=None, stroke=0, shader=None, blur=0):
    p = skia.Paint(AntiAlias=True)
    if c is not None: p.setColor(c)
    if shader: p.setShader(shader)
    if stroke: p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke); p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p

def head_path():
    """profile facing right, in a 1000x1000 box"""
    p = skia.Path()
    p.moveTo(372, 905)
    p.cubicTo(372, 840, 330, 800, 300, 735)
    p.cubicTo(240, 600, 262, 420, 372, 330)
    p.cubicTo(470, 250, 640, 238, 742, 318)
    p.cubicTo(812, 372, 838, 452, 830, 530)
    p.cubicTo(828, 552, 832, 566, 842, 582)
    p.lineTo(888, 652)
    p.cubicTo(898, 668, 890, 680, 872, 684)
    p.lineTo(852, 688)
    p.cubicTo(860, 704, 858, 716, 846, 724)
    p.cubicTo(856, 736, 854, 752, 840, 760)
    p.cubicTo(846, 790, 834, 812, 800, 818)
    p.cubicTo(752, 826, 712, 826, 690, 846)
    p.cubicTo(672, 862, 668, 884, 670, 905)
    p.close()
    return p

def thought_path():
    """tangled loops on the left that straighten into a line ending at a point (kusut -> paham)"""
    p = skia.Path()
    p.moveTo(372, 560)
    p.cubicTo(352, 470, 452, 420, 492, 480)
    p.cubicTo(530, 538, 430, 600, 412, 520)
    p.cubicTo(396, 446, 520, 392, 566, 460)
    p.cubicTo(606, 520, 520, 566, 512, 502)
    p.cubicTo(504, 446, 560, 404, 640, 398)
    return p
DOT = (640, 398)

def draw_icon(cv, x, y, s, bg=None, head=LILAC, line=PLUM, dot=CORAL):
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    hp = head_path()
    if head == 'grad':
        cv.drawPath(hp, P(shader=skia.GradientShader.MakeLinear([skia.Point(300,250), skia.Point(820,900)], [col('#CDBDFF'), col(LILAC), col(LILAC2)], [0, 0.5, 1])))
    else:
        cv.drawPath(hp, P(col(head)))
    m = skia.Matrix(); m.setScale(1.2, 1.2, 548, 500); m.postTranslate(-6, 22)
    tp = skia.Path(); thought_path().transform(m, tp)
    cv.drawPath(tp, P(col(line), stroke=38))
    d = m.mapXY(*DOT)
    cv.drawCircle(d.x(), d.y(), 46, P(col(dot)))
    cv.restore()

def font(name, size):
    f = skia.Font(skia.Typeface.MakeFromFile(os.path.join(FD, name)), size); f.setEdging(skia.Font.Edging.kAntiAlias); f.setSubpixel(True); return f

def wordmark(cv, x, baseline, size, color=INK, track=-0.035):
    f = font('PlusJakartaSans-ExtraBold.ttf', size)
    for ch in 'benak':
        cv.drawString(ch, x, baseline, f, P(col(color))); x += f.measureText(ch) + track * size
    return x

def avatar(path, size=1080):
    s = skia.Surface(size, size); cv = s.getCanvas()
    cv.drawRect(skia.Rect(0, 0, size, size), P(shader=skia.GradientShader.MakeRadial(skia.Point(size*0.45, size*0.4), size*0.8, [col('#2E2066'), col(PLUM)])))
    k = size / 1000
    sc = 1.04 * k
    draw_icon(cv, size*0.5 - 580*sc, size*0.5 - 560*sc, sc, head='grad')
    s.makeImageSnapshot().save(path, skia.kPNG)

def horizontal(path, w=2000, h=700, bg=PLUM):
    s = skia.Surface(w, h); cv = s.getCanvas()
    cv.drawRect(skia.Rect(0, 0, w, h), P(col(bg)))
    draw_icon(cv, 60, 30, 0.62, head='grad')
    wordmark(cv, 640, 470, 330)
    s.makeImageSnapshot().save(path, skia.kPNG)

def svg_logo(path, w=2000, h=700):
    st = skia.FILEWStream(path)
    cv = skia.SVGCanvas.Make(skia.Rect(0, 0, w, h), st, skia.SVGCanvas.kConvertTextToPaths_Flag)
    draw_icon(cv, 60, 30, 0.62, head=LILAC)
    wordmark(cv, 640, 470, 330)
    del cv; st.flush(); del st

def svg_icon(path):
    st = skia.FILEWStream(path)
    cv = skia.SVGCanvas.Make(skia.Rect(0, 0, 1000, 1000), st, 0)
    draw_icon(cv, -70, -60, 1.0, head=LILAC)
    del cv; st.flush(); del st

if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    avatar('out/benak-avatar.png')
    horizontal('out/benak-logo.png')
    svg_logo('out/benak-logo.svg'); svg_icon('out/benak-icon.svg')
    print('ok')
