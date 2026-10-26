#!/usr/bin/env python3
"""Bangun bagian website yang berasal dari website/episodes.json.

Jalankan setiap kali menambah atau mengubah episode:
    python3 tools/build_site.py

Yang dihasilkan (semua di folder website/):
  index.html               kartu episode terbaru + JSON-LD (di antara penanda <!-- build:... -->)
  episode/<slug>/          halaman per episode: video, penjelasan, sumber riset
  episode/                 daftar semua episode
  404.html, sitemap.xml, robots.txt
  episodes/<slug>-card.jpg (4:5), -poster.jpg (9:16), -og.jpg (preview link 1200x630)
  og.png, apple-touch-icon.png
Gambar yang sudah ada tidak dibuat ulang; hapus filenya kalau mau dibuat ulang.
Header, footer, CSS, dan skrip bersama diambil dari index.html, jadi ubah di sana saja.
Butuh: Python 3, Pillow, ffmpeg/ffprobe.
"""
import html
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / 'website'
VIDEOS = ROOT / 'videos'
SITE = 'https://ruangpikir.id'
LATEST = 8                                   # jumlah episode di beranda
FONT_DIR = ROOT / 'video-engine' / 'ep02_stroop' / 'fonts'
SERIF = ROOT / 'tools' / 'fonts' / 'InstrumentSerif-Italic.ttf'

INK, TEXT, MUTED, VIOLET, VIOLET2 = (6, 6, 8), (240, 239, 246), (152, 150, 166), (127, 140, 255), (174, 182, 255)
esc = html.escape


def font(name, size):
    return ImageFont.truetype(str(SERIF if name == 'serif' else FONT_DIR / name), size)


# ---------------------------------------------------------------- potongan dari index.html
INDEX = (WEB / 'index.html').read_text()


def block(name, text=INDEX):
    m = re.search(rf'<!-- build:{name} -->\n?(.*?)\n?<!-- /build:{name} -->', text, re.S)
    if not m:
        raise SystemExit(f'Penanda build:{name} tidak ada di index.html')
    return m.group(1)


def for_subpage(fragment):
    """Link ke bagian beranda (#tes, #episode, ...) harus diawali '/' di halaman lain."""
    fragment = fragment.replace('href="#top"', 'href="/"')
    return re.sub(r'href="#([a-z])', r'href="/#\1', fragment)


STYLE = re.search(r'<style>.*?</style>', INDEX, re.S).group(0)
HEAD = block('head')
HEADER = for_subpage(block('header'))
FOOTER = for_subpage(block('footer'))
COMMON = re.search(r'<script id="common">.*?</script>', INDEX, re.S).group(0)
SOCIAL = {k: re.search(rf"{k}: '([^']*)'", COMMON).group(1) for k in ('instagram', 'tiktok')}
IG_SVG = re.search(r'<svg class="ig".*?</svg>', INDEX, re.S).group(0)
TT_SVG = re.search(r'<svg class="tt".*?</svg>', INDEX, re.S).group(0)


# ---------------------------------------------------------------- gambar
def gradient_bg(w, h):
    im = Image.new('RGB', (w, h), INK)
    top, bot = (18, 20, 43), INK
    px = im.load()
    for y in range(h):
        t = y / (h - 1)
        c = tuple(round(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return im


def add_glow(im, cx, cy, r, alpha=110):
    glow = Image.new('L', im.size, 0)
    ImageDraw.Draw(glow).ellipse((cx - r, cy - r, cx + r, cy + r), fill=alpha)
    glow = glow.filter(ImageFilter.GaussianBlur(r * .45))
    im.paste(Image.new('RGB', im.size, (96, 108, 255)), (0, 0), glow)


def tracked(draw, xy, text, fnt, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing


def wrap(draw, text, fnt, max_w):
    lines, line = [], ''
    for w in text.split():
        t = f'{line} {w}'.strip()
        if draw.textlength(t, font=fnt) > max_w and line:
            lines.append(line)
            line = w
        else:
            line = t
    return lines + [line] if line else lines


def avatar(size):
    """Foto profil dipotong bulat dengan cincin ungu, seperti di Instagram."""
    ring = 10
    logo = Image.open(ROOT / 'brand' / 'ruangpikir-foto-profil.png').convert('RGB').resize((size - 2 * ring,) * 2, Image.LANCZOS)
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    grad = Image.linear_gradient('L').resize((size, size)).rotate(45)
    ring_img = Image.composite(Image.new('RGB', (size, size), (227, 230, 255)), Image.new('RGB', (size, size), (75, 85, 200)), grad)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    out.paste(ring_img, (0, 0), mask)
    inner = Image.new('L', logo.size, 0)
    ImageDraw.Draw(inner).ellipse((0, 0, logo.width - 1, logo.height - 1), fill=255)
    out.paste(logo, (ring, ring), inner)
    return out


def rounded(im, r):
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def make_home_og(path):
    W, H = 1200, 630
    im = gradient_bg(W, H)
    add_glow(im, 930, 300, 260)
    d = ImageDraw.Draw(im)
    tracked(d, (80, 96), 'PSIKOLOGI SEHARI-HARI · 60 DETIK', font('JetBrainsMono-ExtraBold.ttf', 22), VIOLET2, 4)
    d.text((76, 150), 'Ruang untuk', font=font('PlusJakartaSans-ExtraBold.ttf', 78), fill=TEXT)
    d.text((76, 238), 'memahami', font=font('PlusJakartaSans-ExtraBold.ttf', 78), fill=TEXT)
    d.text((80, 322), 'isi kepalamu.', font=font('serif', 96), fill=VIOLET2)
    d.text((80, 462), 'Psikologi sehari-hari, dijelaskan pakai riset.', font=font('PlusJakartaSans-Medium.ttf', 28), fill=MUTED)
    d.text((80, 530), 'ruangpikir.id  ·  @ruangpikir2026', font=font('PlusJakartaSans-Bold.ttf', 26), fill=TEXT)
    av = avatar(330)
    im.paste(av, (W - 330 - 100, 150), av)
    im.save(path, optimize=True)


def make_episode_og(ep, card_img, path):
    W, H = 1200, 630
    im = gradient_bg(W, H)
    add_glow(im, 960, 320, 240)
    d = ImageDraw.Draw(im)
    tracked(d, (80, 84), f'EP {ep["no"]:02d} · {ep["topic"].upper()}', font('JetBrainsMono-ExtraBold.ttf', 22), VIOLET2, 4)
    tf = font('PlusJakartaSans-ExtraBold.ttf', 64)
    y = 136
    for line in wrap(d, ep['title'], tf, 620)[:3]:
        d.text((76, y), line, font=tf, fill=TEXT)
        y += 78
    sf = font('PlusJakartaSans-Medium.ttf', 27)
    y += 18
    for line in wrap(d, ep['summary'], sf, 600)[:3]:
        d.text((80, y), line, font=sf, fill=MUTED)
        y += 40
    d.text((80, 540), 'ruangpikir.id  ·  @ruangpikir2026', font=font('PlusJakartaSans-Bold.ttf', 26), fill=TEXT)
    thumb = rounded(card_img.resize((368, 460), Image.LANCZOS), 28)
    im.paste(thumb, (W - 368 - 90, 85), thumb)
    im.convert('RGB').save(path, quality=86, optimize=True)


def video_frame(video, t):
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'f.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(video), '-frames:v', '1', str(out)], check=True)
        return Image.open(out).convert('RGB')


def duration(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(video)],
                       check=True, capture_output=True, text=True)
    return round(float(r.stdout))


def episode_images(ep):
    out = WEB / 'episodes'
    out.mkdir(exist_ok=True)
    card, poster, og = (out / f'{ep["slug"]}-{k}' for k in ('card.jpg', 'poster.jpg', 'og.jpg'))
    if not (card.exists() and poster.exists() and og.exists()):
        frame = video_frame(VIDEOS / ep['video'], ep.get('poster_time', 3))         # 1080x1920
        frame.resize((720, 1280), Image.LANCZOS).save(poster, quality=82, optimize=True)
        crop = frame.crop((0, 300, 1080, 1650))                                     # 4:5, area judul s/d caption
        crop.resize((640, 800), Image.LANCZOS).save(card, quality=82, optimize=True)
        make_episode_og(ep, crop, og)
        print('  gambar dibuat:', card.name, poster.name, og.name)


# ---------------------------------------------------------------- HTML
def jsonld(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>'


ORG = {'@type': 'Organization', 'name': 'Ruang Pikir', 'url': SITE + '/', 'logo': SITE + '/apple-touch-icon.png',
       'sameAs': [u for u in SOCIAL.values() if u]}


def mmss(sec):
    return f'{sec // 60}:{sec % 60:02d}'


def card(ep, player):
    url = f'/episode/{ep["slug"]}/'
    data = (f' data-video="/videos/{esc(ep["video"])}" data-poster="/episodes/{ep["slug"]}-poster.jpg"'
            f' data-title="{esc(ep["title"])}" data-slug="{ep["slug"]}"') if player else ''
    return f'''<article class="ep{' tilt' if player else ''}">
  <a class="ep-poster" href="{url}"{data} aria-label="Putar video: {esc(ep["title"])}">
    <img src="/episodes/{ep["slug"]}-card.jpg" alt="Cuplikan video: {esc(ep["title"])}" width="640" height="800" loading="lazy">
    <span class="play" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4.5v15l13-7.5z"/></svg></span>
    <span class="dur">{mmss(ep["duration"])}</span>
  </a>
  <div class="meta">
    <span class="eyebrow">EP {ep["no"]:02d} · {esc(ep["topic"])}</span>
    <h3><a href="{url}">{esc(ep["title"])}</a></h3>
    <p>{esc(ep["summary"])}</p>
    <a class="go" href="{url}">Penjelasan &amp; sumber →</a>
  </div>
</article>'''


def cards(eps, player=False):
    return '<div class="eps">\n' + '\n'.join(card(e, player) for e in eps) + '\n</div>'


def page(path, title, desc, body, og_image, og_type='website', ld=None, script='', noindex=False):
    url = SITE + path
    return f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{url}">'}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Ruang Pikir">
<meta property="og:locale" content="id_ID">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{HEAD}
{jsonld(ld) if ld else ''}
{STYLE}
</head>
<body>

{HEADER}

<main id="top">
{body}
</main>

{FOOTER}

{COMMON}
{script}
</body>
</html>
'''


def follow_buttons():
    return (f'<a class="btn btn-ghost js-ig" href="{SOCIAL["instagram"]}" target="_blank" rel="noopener">{IG_SVG}Instagram</a>'
            f'<a class="btn btn-ghost js-tt" href="{SOCIAL["tiktok"]}" target="_blank" rel="noopener">{TT_SVG}TikTok</a>')


def episode_page(ep, eps):
    others = [e for e in eps if e['slug'] != ep['slug']][:4]
    paras = '\n      '.join(f'<p>{esc(t)}</p>' for t in ep['body'])
    test_btn = '<a class="btn btn-primary" href="/#tes">Coba tes otaknya</a>' if ep.get('try_test') else ''
    more = f'''
<section class="section" style="background:var(--night)">
  <div class="wrap">
    <div class="sec-row">
      <div class="sec-head"><div class="eyebrow">Episode lain</div><h2 class="h2">Tonton juga</h2></div>
      <a class="btn btn-ghost" href="/episode/">Semua episode</a>
    </div>
    {cards(others)}
  </div>
</section>''' if others else ''
    body = f'''<article class="ep-page">
  <div class="wrap ep-grid">
    <div class="ep-video">
      <video controls playsinline preload="metadata" poster="/episodes/{ep["slug"]}-poster.jpg" src="/videos/{esc(ep["video"])}"></video>
    </div>
    <div class="ep-body">
      <a class="back" href="/episode/">← Semua episode</a>
      <div class="eyebrow">EP {ep["no"]:02d} · {esc(ep["topic"])}</div>
      <h1>{esc(ep["title"])}</h1>
      <p class="lead">{esc(ep["summary"])}</p>
      {paras}
      <div class="ep-source"><b>SUMBER</b>{esc(ep["source"])}</div>
      <div class="row">{test_btn}{follow_buttons()}</div>
    </div>
  </div>
</article>{more}'''
    ld = {'@context': 'https://schema.org', '@type': 'VideoObject', 'name': ep['title'], 'description': ep['summary'],
          'thumbnailUrl': [f'{SITE}/episodes/{ep["slug"]}-poster.jpg', f'{SITE}/episodes/{ep["slug"]}-card.jpg'],
          'uploadDate': ep['date'], 'duration': f'PT{ep["duration"]}S', 'contentUrl': f'{SITE}/videos/{ep["video"]}',
          'inLanguage': 'id', 'publisher': ORG}
    script = f'<script>document.querySelector(\'.ep-video video\').addEventListener(\'play\', () => track(\'putar-{ep["slug"]}\'), {{ once: true }});</script>'
    return page(f'/episode/{ep["slug"]}/', f'{ep["title"]} · Ruang Pikir', f'{ep["summary"]} Penjelasan singkat berbasis riset dan sumbernya.',
                body, f'/episodes/{ep["slug"]}-og.jpg', 'video.other', ld, script)


def list_page(eps):
    body = f'''<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Semua episode</div>
      <h1 class="h2">Satu pertanyaan, <em class="serif">satu video.</em></h1>
      <p>Psikologi sehari-hari dalam ±60 detik, lengkap dengan penjelasan dan sumber risetnya.</p>
    </div>
    {cards(eps)}
  </div>
</section>'''
    return page('/episode/', 'Semua episode · Ruang Pikir', 'Daftar semua video Ruang Pikir: psikologi sehari-hari dalam 60 detik, berbasis riset.',
                body, '/og.png')


def not_found_page():
    body = '''<section class="section">
  <div class="wrap notfound">
    <div class="eyebrow">404</div>
    <h1 class="h2">Halaman ini <em class="serif">nggak ketemu.</em></h1>
    <p style="color:var(--muted)">Mungkin linknya salah ketik, atau halamannya sudah pindah.</p>
    <div class="row" style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center">
      <a class="btn btn-primary" href="/">Ke beranda</a><a class="btn btn-ghost" href="/episode/">Lihat episode</a>
    </div>
  </div>
</section>'''
    return page('/404.html', 'Halaman tidak ditemukan · Ruang Pikir', 'Halaman yang kamu cari tidak ada.', body, '/og.png', noindex=True)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text() != text:
        path.write_text(text)
        print('  ditulis:', path.relative_to(ROOT))


def main():
    eps = json.loads((WEB / 'episodes.json').read_text())
    eps.sort(key=lambda e: e['no'], reverse=True)
    for ep in eps:
        if not (VIDEOS / ep['video']).exists():
            raise SystemExit(f'Video tidak ada: videos/{ep["video"]}')
        ep['duration'] = duration(VIDEOS / ep['video'])
        episode_images(ep)

    if not (WEB / 'og.png').exists():
        make_home_og(WEB / 'og.png')
        print('  gambar dibuat: og.png')
    if not (WEB / 'apple-touch-icon.png').exists():
        Image.open(ROOT / 'brand' / 'ruangpikir-foto-profil.png').convert('RGB').resize((180, 180), Image.LANCZOS).save(WEB / 'apple-touch-icon.png', optimize=True)
        print('  gambar dibuat: apple-touch-icon.png')
    if not (WEB / 'videos').exists():
        os.symlink('../videos', WEB / 'videos')            # nginx melayani folder video lewat symlink ini

    # beranda: kartu episode terbaru + JSON-LD
    index = INDEX
    index = re.sub(r'(<!-- build:episodes -->).*?(<!-- /build:episodes -->)',
                   lambda m: m.group(1) + '\n' + cards(eps[:LATEST], player=True) + '\n' + m.group(2), index, flags=re.S)
    site_ld = {'@context': 'https://schema.org', '@graph': [
        {**ORG, '@id': SITE + '/#org'},
        {'@type': 'WebSite', 'name': 'Ruang Pikir', 'url': SITE + '/', 'inLanguage': 'id', 'publisher': {'@id': SITE + '/#org'}}]}
    index = re.sub(r'(<!-- build:jsonld -->).*?(<!-- /build:jsonld -->)',
                   lambda m: m.group(1) + jsonld(site_ld) + m.group(2), index, flags=re.S)
    write(WEB / 'index.html', index)

    for ep in eps:
        write(WEB / 'episode' / ep['slug'] / 'index.html', episode_page(ep, eps))
    write(WEB / 'episode' / 'index.html', list_page(eps))
    write(WEB / '404.html', not_found_page())

    latest = max(e['date'] for e in eps)
    urls = [('/', latest), ('/episode/', latest)] + [(f'/episode/{e["slug"]}/', e['date']) for e in eps]
    write(WEB / 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod></url>\n' for u, d in urls) + '</urlset>\n')
    write(WEB / 'robots.txt', f'User-agent: *\nDisallow: /statistik/\nDisallow: /e/\n\nSitemap: {SITE}/sitemap.xml\n')
    print(f'Selesai: {len(eps)} episode.')


if __name__ == '__main__':
    main()
