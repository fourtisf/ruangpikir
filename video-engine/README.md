# Mesin video Ruang Pikir

Video dibuat 100% dengan kode: ilustrasi digambar dengan **skia-python**, suara dari **Gemini TTS** (voice `Achird`), musik + SFX disintesis dengan **numpy/scipy**, lalu digabung dengan **ffmpeg**. Tidak ada biaya per video selain kuota TTS.

Output: MP4 1080×1920, 30 fps, H.264 + AAC 192k, loudness −14 LUFS. Render 45–50 detik ±4–6 menit di 2 vCPU.

## Instalasi
```bash
pip install -r requirements.txt      # skia-python, numpy, scipy, requests, pillow
# + ffmpeg di PATH
export GEMINI_API_KEY=...            # hanya kalau mau generate suara baru
# atau simpan sekali di file .env di folder repo (salin dari .env.example; .env tidak ikut git),
# dibaca otomatis oleh gemini_tts.py: GEMINI_API_KEY=...  GEMINI_TTS_MODEL=gemini-3.8-flash-tts
# + skia butuh libEGL di Linux: apt install libegl1 libgl1
```

## Render ulang episode yang ada (tanpa API key)
```bash
./ep01_spotlight/build.sh            # -> ep01_spotlight/ruang-pikir-ep01.mp4
./ep02_stroop/build.sh               # -> ep02_stroop/ruang-pikir-ep02.mp4
./ep03_panggil-nama/build.sh         # -> ep03_panggil-nama/ruang-pikir-ep03.mp4
./ep04_pura-pura-gapapa/build.sh     # -> ep04_pura-pura-gapapa/ruang-pikir-ep04.mp4
```
Suara sudah tersimpan di `vo/`. Tambah `--voice` untuk membuat ulang suaranya.

## Struktur satu episode
| File | Fungsi |
|---|---|
| `vo.py` | Naskah: daftar `(anchor_detik, kalimat)`. Anchor = waktu animasi saat kalimat mulai |
| `vo/lines.json` | Hasil TTS: file wav per kalimat + durasinya |
| `rp.py` (EP01) / `base.py` (EP02+) | Mesin + komponen gambar + layout + time-warp + CLI |
| `stroop.py` (EP02) / `episode.py` (EP03+) | Episode: mengisi `GROUPS`, `CAPS`, judul, fungsi scene `g0..g5`, `build_sfx()` |
| `audio.py` | Musik lo-fi sintetis, kamus `SFX`, mixing + ducking musik di bawah suara |
| `gemini_tts.py` | Panggil Gemini TTS, simpan wav 44.1 kHz, mode `script` memotong per kalimat |
| `vo_rest.py`, `countdown.py`, `tighten_countdown.py` | Alat suara EP02 (lihat "Jebakan suara") |
| `voice.sh`, `vo_full.py` (EP03+) | Suara resep EP01: `gemini-3.1-flash-tts-preview` + instruksi gaya EP01, 1 request. EP04: dipotong dengan `split_lines` (jeda panjang + durasi sebanding panjang kalimat); `--split-only` memotong ulang `vo/full.wav` tanpa request baru |
| `tighten.py` (EP04) | Pendekkan jeda > 0,3 dtk di dalam kalimat (kecepatan bicara tetap) supaya durasi ≤ 55 dtk |
| `logo*.py`, `premium.py`, `v3.py` | Gambar logo kepala + pintu untuk outro (`logo_rp.c4`) |
| `fonts/` | Plus Jakarta Sans + JetBrains Mono (OFL) |

Pola untuk episode baru adalah pola **EP04** (salin `ep04_pura-pura-gapapa/`, tanpa `vo/` dan `preview/`): `base.py` dipakai sebagai library, `episode.py` menimpa `b.GROUPS`, `b.CAPS`, `b.draw_title`, `b.DRAWERS`, lalu punya `build_sfx()` dan CLI sendiri. EP03 juga menimpa `b.draw_bg` (aurora + bokeh) dan `b.draw_groups` (ilustrasi memudar lembut sebelum zona caption, plus peringatan kalau `save()`/`restore()` tidak seimbang).

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
| Tag (+ progress bar di EP01–02; sejak EP03 tanpa progress bar) | 404 | `GROUPS[i][2]`, contoh `RISET · 2000` |
| Judul | 482 | `draw_title`, format "X, [kok bisa]?" (bagian dalam `[...]` berwarna aksen) |
| Ilustrasi | 560 – 1200 | semua gambar scene |
| Caption baris 1 / 2 | 1252 / 1340 | `CAPS`, kata dalam `[...]` diberi highlight |
| Watermark | 1440 | "RUANG PIKIR" |
Bawah 1500 dibiarkan kosong (tertutup UI Instagram/TikTok).

**Gaya sinematik (EP04, gaya standar sekarang):** judul y 232 hanya di adegan pertama; tanpa tag & progress bar; ilustrasi y 260–1220 (memudar lembut di tepi); caption per frasa di tengah y 1332 (1–2 baris, 56 px, tanpa kotak); watermark 1440. Adegan didefinisikan di `b.GROUPS` (9 adegan pendek), caption di `PHRASES` [(waktu, teks)] yang disinkronkan ke jeda suara.

## Komponen siap pakai
Di `base.py`: `person()` (karakter kapsul: mood neutral/worried/happy, sweat, phone, shirt), `spotlight()`, `watcher_eye()`, `scribble()` (pikiran kusut), `pill()`, `sparkle()`, `caption_line()`, `tracked()`, easing `eo/ei/eio/bo/bump`, `prog(t,a,b)`.
Di `stroop.py`: `neon_word()`, `card()`, `ring()`, `brain()`, `eye()`, `stamp()`, contoh grafik batang, gelembung komentar, outro logo.
Di `ep03_panggil-nama/episode.py` dan `ep04_pura-pura-gapapa/episode.py` (gaya premium): `glass()` (kartu kaca), `sheen()` (kilau lewat), `rays()` (sinar berputar), `halo()`, `bubble_path()`/`draw_bubble()` (gelembung bicara), `rich()` (teks dengan kata beraksen), `chip()`, `check_mark()`/`x_mark()` (centang/silang digambar), `ghost()` (sosok bercahaya), `name_badge()`, `mic()`, `stopwatch()`, widget detak jantung (`ecg()`), meter cemas, kemudi, daftar komentar + kolom ketik. EP04 v1 (arsip di riwayat git) menambah `smile_mask()` (topeng senyum + retak), `gauge()` (meter tekanan), `storm()` (badai di dada), detak makin cepat (`accel_phase`/`beat_times`, dipakai juga untuk SFX), `icon()` (wajah/awan/hati/gembok/putar), `tear()`, `meter_row()` (batang hasil dengan penanda pembanding), `flip_card()` (kartu pikiran dibalik). EP04 gaya sinematik: `sphere()` (bola 3D lembut + label), `floor()`/`sag_y()` (lantai yang melengkung karena beban), `face()` (wajah di bola), `pill_bar()` (batang perbandingan berlabel), `head_outline()` (siluet kepala+bahu dari logo), `eye()`, `thought_chip()` (pikiran + coret), `draw_captions()` per kata, `draw_groups()` dengan kamera halus.

Aturan gerak: elemen muncul dengan `bo()` (back-out pop) 0.3–0.5 dtk; antar scene crossfade 0.35 dtk + zoom 5%; tidak ada elemen penting yang muncul < 0.3 dtk sebelum dibacakan.

## SFX tersedia (`audio.SFX`)
whoosh, swish, zoom, plop, pop, tick, chop, crack, fizz, fizz_soft, rise, sting, blink, plip, zap, zap2, ding, ding_soft, card, boing, shine, clunk, heart, stamp, beep, go, buzzer, clock.

## Jebakan suara (penting)
- **Suara resmi = resep EP01** (dipilih ALFA, 27 Okt 2026, acuan video "Jam 2 pagi, kok overthinking?"): `gemini-3.1-flash-tts-preview` + `STYLE` EP01 + "Beri jeda sekitar satu detik di antara setiap baris.", semua kalimat 1 request, `split_by_pauses`. Ciri terukur: nada median ±185 Hz, ±16 karakter/detik, ekspresif. Diukur dengan MFCC, audio final EP03 berjarak 0,32 dari video acuan (EP01 0,29; EP02 0,51).
- EP02 memakai `gemini-3.8-flash-tts` (nada ±150 Hz, lebih kalem); suaranya terdengar seperti orang lain. Model ini sekarang **membacakan prefix gaya** (prefix EP02, versi Inggris, format "DIRECTOR'S NOTES / TRANSCRIPT" semuanya ikut terbaca, dicek 27 Okt 2026). Jangan dipakai lagi.
- `gemini-3.1-flash-tts-preview` dengan prefix pendek EP02 nadanya jadi terlalu tinggi (±216 Hz); pakai `STYLE` panjang EP01. `gemini-2.5-flash-preview-tts` memotong kalimat terakhir.
- Mempercepat/memperlambat suara (time-stretch) membuat suara terdengar seperti orang lain; jangan dipakai.
- Prompt gaya yang panjang kadang **ikut dibacakan** oleh model. Pakai prefix gaya pendek (mis. "Ucapkan dengan santai, ramah, dan antusias seperti kreator TikTok:") atau tanpa prefix, dan **cek durasi**: tolak hasil yang > 2× perkiraan (±14 karakter/detik).
- Kalimat dengan jeda internal (hitung mundur) jangan digabung dalam satu request: buat terpisah (`countdown.py`), lalu rapatkan jedanya (`tighten_countdown.py`).
- Banyak kalimat dalam satu request lalu dipotong (`vo_rest.py`) lebih hemat kuota dan suaranya lebih konsisten. Dengan instruksi "beri jeda sekitar satu detik" (resep EP01), jeda di dalam kalimat ("Hasilnya?", "Misalnya,") bisa sama panjang dengan jeda antarkalimat, jadi pakai `split_lines` EP04 dan tetap cek dengan transkripsi. Model kadang menambah "Hmm" di awal: cek transkripsi baris pertama dan buang kalau ada.
- Kuota gratis: ±3 request/menit per model + batas harian. Kena 429 → tunggu, atau ganti `GEMINI_TTS_MODEL`.

## QA sebelum diserahkan
1. `python3 episode.py preview t1 t2 ...` untuk ±12 titik waktu, lalu susun jadi contact sheet dan periksa.
2. Tidak ada tumpang tindih teks; ilustrasi tidak masuk zona caption.
3. Glyph khusus (★ ✓ Ψ) tidak tersedia di font. Gambar sebagai bentuk, jangan sebagai teks.
4. Setelah render: `ffmpeg -i final.mp4 -af ebur128 -f null -` → Integrated sekitar −14 LUFS.
5. Tonton bagian awal: hook harus terbaca dalam 2 detik pertama.
