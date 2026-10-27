# Mesin video Ruang Pikir

Video dibuat 100% dengan kode: ilustrasi digambar dengan **skia-python**, suara dari **Gemini TTS** (voice `Achird`), musik + SFX disintesis dengan **numpy/scipy**, lalu digabung dengan **ffmpeg**. Tidak ada biaya per video selain kuota TTS.

Output: MP4 1080×1920, 30 fps, H.264 + AAC 192k, loudness −14 LUFS. Render 45–50 detik ±4–6 menit di 2 vCPU.

## Instalasi
```bash
pip install -r requirements.txt      # skia-python, numpy, scipy, requests, pillow
# + ffmpeg di PATH
export GEMINI_API_KEY=...            # hanya kalau mau generate suara baru
# atau simpan sekali di file pribadi (di luar repo), dibaca otomatis oleh gemini_tts.py:
#   ~/.config/ruangpikir/gemini.env  berisi  export GEMINI_API_KEY=...   (chmod 600)
# + skia butuh libEGL di Linux: apt install libegl1 libgl1
```

## Render ulang episode yang ada (tanpa API key)
```bash
./ep01_spotlight/build.sh            # -> ep01_spotlight/ruang-pikir-ep01.mp4
./ep02_stroop/build.sh               # -> ep02_stroop/ruang-pikir-ep02.mp4
```
Suara sudah tersimpan di `vo/`. Tambah `--voice` untuk membuat ulang suaranya.

## Struktur satu episode
| File | Fungsi |
|---|---|
| `vo.py` | Naskah: daftar `(anchor_detik, kalimat)`. Anchor = waktu animasi saat kalimat mulai |
| `vo/lines.json` | Hasil TTS: file wav per kalimat + durasinya |
| `rp.py` (EP01) / `base.py` (EP02+) | Mesin + komponen gambar + layout + time-warp + CLI |
| `stroop.py` (EP02) | Episode: mengisi `GROUPS`, `CAPS`, judul, fungsi scene `g0..g5`, `build_sfx()` |
| `audio.py` | Musik lo-fi sintetis, kamus `SFX`, mixing + ducking musik di bawah suara |
| `gemini_tts.py` | Panggil Gemini TTS, simpan wav 44.1 kHz, mode `script` memotong per kalimat |
| `vo_rest.py`, `countdown.py`, `tighten_countdown.py` | Alat suara EP02 (lihat "Jebakan suara") |
| `logo*.py`, `premium.py`, `v3.py` | Gambar logo kepala + pintu untuk outro (`logo_rp.c4`) |
| `fonts/` | Plus Jakarta Sans + JetBrains Mono (OFL) |

Pola untuk episode baru adalah pola **EP02**: `base.py` dipakai sebagai library, file episode menimpa `b.GROUPS`, `b.CAPS`, `b.draw_title`, `b.DRAWERS`, lalu punya `build_sfx()` dan CLI sendiri.

## Pipeline
```
vo.py ──TTS──> vo/lNN.wav + lines.json
           └─> episode.py timeline  (time-warp + jadwal SFX + posisi suara)
                 ├─> audio.py       (musik + SFX + suara, ducking)  -> audio.wav
                 └─> episode.py video (render frame skia -> ffmpeg)  -> raw.mp4
ffmpeg mux + loudnorm -14 LUFS -> final.mp4
```

**Time-warp:** animasi ditulis dalam "waktu animasi" (DUR = 42 dtk). Kalau sebuah kalimat lebih panjang dari jendelanya (anchor ke anchor berikutnya), jendela itu otomatis diperlambat supaya suara dan animasi tetap sinkron. Durasi akhir mengikuti panjang suara.

## Layout (wajib dipatuhi)
| Zona | y (px) | Isi |
|---|---|---|
| Tag + progress bar | 404 | `GROUPS[i][2]`, contoh `RISET · 2000` |
| Judul | 482 | `draw_title`, format "X, [kok bisa]?" (bagian dalam `[...]` berwarna aksen) |
| Ilustrasi | 560 – 1200 | semua gambar scene |
| Caption baris 1 / 2 | 1252 / 1340 | `CAPS`, kata dalam `[...]` diberi highlight |
| Watermark | 1440 | "RUANG PIKIR" |
Bawah 1500 dibiarkan kosong (tertutup UI Instagram/TikTok).

## Komponen siap pakai
Di `base.py`: `person()` (karakter kapsul: mood neutral/worried/happy, sweat, phone, shirt), `spotlight()`, `watcher_eye()`, `scribble()` (pikiran kusut), `pill()`, `sparkle()`, `caption_line()`, `tracked()`, easing `eo/ei/eio/bo/bump`, `prog(t,a,b)`.
Di `stroop.py`: `neon_word()`, `card()`, `ring()`, `brain()`, `eye()`, `stamp()`, contoh grafik batang, gelembung komentar, outro logo.

Aturan gerak: elemen muncul dengan `bo()` (back-out pop) 0.3–0.5 dtk; antar scene crossfade 0.35 dtk + zoom 5%; tidak ada elemen penting yang muncul < 0.3 dtk sebelum dibacakan.

## SFX tersedia (`audio.SFX`)
whoosh, swish, zoom, plop, pop, tick, chop, crack, fizz, fizz_soft, rise, sting, blink, plip, zap, zap2, ding, ding_soft, card, boing, shine, clunk, heart, stamp, beep, go, buzzer, clock.

## Jebakan suara (penting)
- **`gemini-3.8-flash-tts` membacakan prefix gaya, bahkan yang pendek** (dicek 27 Okt 2026 lewat transkripsi: "Ucapkan dengan santai…" ikut terbaca). Kirim kalimatnya saja tanpa prefix (`style=''`); hasilnya tetap santai. Cek dengan transkripsi (mis. `gemini-3.5-flash-lite`) sebelum render.
- Prompt gaya yang panjang kadang **ikut dibacakan** oleh model. Pakai prefix gaya pendek (mis. "Ucapkan dengan santai, ramah, dan antusias seperti kreator TikTok:") atau tanpa prefix, dan **cek durasi**: tolak hasil yang > 2× perkiraan (±14 karakter/detik).
- Kalimat dengan jeda internal (hitung mundur) jangan digabung dalam satu request: buat terpisah (`countdown.py`), lalu rapatkan jedanya (`tighten_countdown.py`).
- Banyak kalimat dalam satu request lalu dipotong (`vo_rest.py`) lebih hemat kuota dan suaranya lebih konsisten.
- Kuota gratis: ±3 request/menit per model + batas harian. Kena 429 → tunggu, atau ganti `GEMINI_TTS_MODEL`.

## QA sebelum diserahkan
1. `python3 episode.py preview t1 t2 ...` untuk ±12 titik waktu, lalu susun jadi contact sheet dan periksa.
2. Tidak ada tumpang tindih teks; ilustrasi tidak masuk zona caption.
3. Glyph khusus (★ ✓ Ψ) tidak tersedia di font. Gambar sebagai bentuk, jangan sebagai teks.
4. Setelah render: `ffmpeg -i final.mp4 -af ebur128 -f null -` → Integrated sekitar −14 LUFS.
5. Tonton bagian awal: hook harus terbaca dalam 2 detik pertama.
