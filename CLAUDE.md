# Ruang Pikir — instruksi untuk Claude Code

Ruang Pikir adalah brand konten **psikologi sehari-hari** (Reels/TikTok/Shorts 9:16, 40–55 detik) dengan website **ruangpikir.id** dan Instagram/TikTok **@ruangpikir2026**. Pemilik: ALFA. Paket ini berisi semua yang dibutuhkan untuk (1) deploy website dan (2) membuat episode video baru dengan gaya yang sama.

## Isi paket

| Folder | Isi |
|---|---|
| `website/` | Situs statis: `index.html` (CSS/JS inline), `episodes.json` (data episode), halaman `episode/`, gambar `episodes/`, `DEPLOY.md` |
| `tools/` | `build_site.py`: membangun kartu & halaman episode, sitemap, gambar preview dari `episodes.json` |
| `deploy/` | Skrip VPS: `setup-vps.sh`, `deploy.sh` (`ruangpikir-deploy`), `nginx-site.conf`, statistik |
| `brand/` | Logo (foto profil 1080, horizontal, SVG) + `BRAND.md` (warna, font, nada bicara, aturan) |
| `content/` | Profil IG, TikTok & X (nama, bio), naskah + caption EP01–EP10, bank ide konten |
| `videos/` | Hasil render EP01–EP10 (MP4 1080×1920, ±2,5–5,5 MB) |
| `video-engine/` | Mesin animasi Python (skia) + suara Gemini TTS + audio/SFX + mux ffmpeg. Lihat `video-engine/README.md` |

## Tugas 1 — Deploy website ke ruangpikir.id

Ikuti `website/DEPLOY.md`. Ringkas:
- Website statis (tanpa server aplikasi/database). Header, footer, CSS, dan skrip bersama ada di `index.html`; halaman lain dibangun dari situ oleh `python3 tools/build_site.py` (butuh Pillow + ffmpeg). Setelah mengubah header/footer/CSS di `index.html`, jalankan build lagi supaya halaman episode ikut berubah.
- **Episode baru di website:** taruh MP4 di `videos/`, tambah entri di `website/episodes.json` (no, slug, judul, topik, tanggal, file video, `poster_time`, ringkasan, isi, sumber), jalankan `python3 tools/build_site.py`, commit, lalu `ruangpikir-deploy` di VPS.
- Hero 3D: skrip `<script type="module">` di akhir `index.html` (three.js 0.170.0 dari jsdelivr): kepala logo, pintu, sinar, chip pikiran (`THOUGHTS`), dan kamera masuk pintu saat scroll. Tanpa WebGL2/CDN gagal/reduced-motion: logo SVG atau gambar diam. Cek tampilannya dengan screenshot Playwright di beberapa ukuran layar sebelum push.
- Statistik pengunjung di `https://ruangpikir.id/statistik/` (GoAccess, tanpa cookie). Kejadian dikirim lewat `track('nama')` di skrip `common`.
- Domain `ruangpikir.id` terdaftar di **Hostinger**; DNS A record `@` → VPS Hostinger (Ubuntu 24.04), CNAME `www` → apex.
- Di VPS: repo di-clone ke `/var/www/ruangpikir`, nginx melayani `website/`. Pasang/ulang: `bash deploy/setup-vps.sh` (lihat "Opsi C" di `website/DEPLOY.md`). Update: `ruangpikir-deploy` di VPS (rollback: `ruangpikir-deploy <commit>`), atau `ssh root@31.97.111.49 ruangpikir-deploy` dari komputer.
- Setelah live, cek: HTTPS aktif, `https://ruangpikir.id` dan `https://www.ruangpikir.id` sama-sama jalan, game tes otak bisa dimainkan di HP.
- Link sosial media diatur di objek `SOCIAL` di bagian bawah `index.html` (Instagram & TikTok sudah `@ruangpikir2026`; YouTube kosong = tombol disembunyikan).

## Tugas 2 — Membuat episode video baru

Baca `video-engine/README.md` lalu pakai template prompt di `video-engine/PROMPT_VIDEO_BARU.md` (episode terbaru sebagai contoh gaya premium: `video-engine/ep10_sebut-perasaan/`, format 30 detik). Prinsip yang tidak boleh dilanggar:
- **Gaya visual (sejak EP04: gaya sinematik, seperti video acuan ALFA "Jam 2 pagi, kok overthinking?")**: background hitam-ungu malam dengan pendar biru-ungu, aksen `#7F8CFF`/`#AEB6FF`, judul "X, kok Y?" di atas **hanya di adegan pertama**, tanpa tag, caption besar per frasa (56 px, putih, kata kunci ungu muda, tanpa kotak, muncul per kata, sinkron ke jeda suara), ilustrasi besar-minimalis (bola 3D lembut, kartu kaca, kata/angka besar, siluet garis tipis), satu ide visual per adegan, crossfade + kamera bergerak halus, watermark "RUANG PIKIR", outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. **Tanpa garis progress bar dan tanpa titik-titik debu/bokeh** (permintaan ALFA). Contoh: `video-engine/ep04_pura-pura-gapapa/episode.py` dan `video-engine/ep05_cermin-foto/episode.py`. Variasi gaya per episode boleh asal aturan dasar ini tetap: EP06 memakai "garis neon + tipografi kinetik" (`video-engine/ep06_liking-gap/episode.py`), EP07 memakai "dunia 3D + UI medsos" (`video-engine/ep07_omongan-orang/episode.py`: ponsel/kartu miring dalam perspektif, komentar berputar mengelilingi kepala, teks 3D), EP08 memakai "meja belajar malam" (`video-engine/ep08_nunda-kerjaan/episode.py`: laptop/ponsel/balok es 3D, lampu meja hangat, kata "MALAS" yang pecah), EP09 memakai "di balik postingan" (`video-engine/ep09_kok-minder/episode.py`: kartu medsos 3D yang dibalik, grid profil + glitch, gunung es), EP10 memakai "energi emosi" (`video-engine/ep10_sebut-perasaan/episode.py`: bola magma yang meledak lalu mendingin, latar ikut memerah, pemindai MRI). **Format 30 detik** (EP10): 5 kalimat ±330 karakter, `DUR` di `base.py` folder itu diturunkan (outro + 5.4) dan anchor dirapatkan ke durasi suara. Hook yang terbukti: kalimat yang relatable + janji jawaban ("Satu komentar kecil bisa kepikiran seharian. Itu bukan karena kamu lemah.") dengan visual UI yang langsung dikenali (notifikasi ponsel) di frame pertama. **Hook wajib di 0–3 detik**: kalimat pertama berupa klaim mengejutkan, visual bergerak sejak frame pertama (mis. jepretan + kilat, transformasi cepat).
- **Suara**: Gemini TTS, voice `Achird`, **resep EP01** (suara yang dipilih ALFA, acuannya video "Jam 2 pagi, kok overthinking?"): model `gemini-3.1-flash-tts-preview` + instruksi gaya panjang EP01, semua kalimat dalam 1 request, dipotong di jeda terpanjang. Lihat `video-engine/ep04_pura-pura-gapapa/vo_full.py` (+ `tighten.py` untuk memendekkan jeda panjang kalau durasi > 55 dtk). Jangan pakai resep EP02 (`gemini-3.8-flash-tts`): suaranya beda dan model itu ikut membacakan instruksi gaya. Selalu cek transkripsi (instruksi tidak boleh terbaca) dan durasi tiap baris.
- **Isi**: satu pertanyaan per video, berbasis riset nyata (sebut peneliti + tahun), bukan diagnosis, tidak melabeli orang nyata dengan gangguan mental, tidak membahas cara menyakiti diri.
- **QA wajib** sebelum menyerahkan: render contact sheet ±12 frame, pastikan tidak ada teks bertabrakan (zona caption y 1200–1390 harus bersih dari ilustrasi), loudness akhir sekitar −14 LUFS.

## Rahasia / API key

- **Jangan** menulis API key ke file di dalam repo atau commit (repo ini publik). Gunakan environment variable `GEMINI_API_KEY`:
  - di cloud Claude Code: pengaturan environment (Network secrets / environment variable `GEMINI_API_KEY`);
  - di VPS/laptop/sesi ini: file `.env` di folder repo (salin dari `.env.example`, chmod 600). `.env` diabaikan git, tetap ada saat `ruangpikir-deploy`, dan dibaca otomatis oleh `gemini_tts.py` (juga `GEMINI_TTS_MODEL`).
- `gemini-3.8-flash-tts` ikut membacakan prefix gaya: kirim kalimat tanpa prefix dan cek hasil suara dengan transkripsi.
- Kuota gratis Gemini TTS terbatas (±3 request/menit per model dan ada batas harian). Kalau kena 429, tunggu atau ganti model TTS (`GEMINI_TTS_MODEL`, misalnya `gemini-3.8-flash-tts` atau `gemini-2.5-flash-preview-tts`).
