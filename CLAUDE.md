# Ruang Pikir — instruksi untuk Claude Code

Ruang Pikir adalah brand konten **psikologi sehari-hari** (Reels/TikTok/Shorts 9:16, 40–55 detik) dengan website **ruangpikir.id** dan Instagram/TikTok **@ruangpikir2026**. Pemilik: ALFA. Paket ini berisi semua yang dibutuhkan untuk (1) deploy website dan (2) membuat episode video baru dengan gaya yang sama.

## Isi paket

| Folder | Isi |
|---|---|
| `website/` | Situs statis: `index.html` (CSS/JS inline), `episodes.json` (data episode), halaman `episode/`, gambar `episodes/`, `DEPLOY.md` |
| `tools/` | `build_site.py`: membangun kartu & halaman episode, sitemap, gambar preview dari `episodes.json` |
| `deploy/` | Skrip VPS: `setup-vps.sh`, `deploy.sh` (`ruangpikir-deploy`), `nginx-site.conf`, statistik |
| `brand/` | Logo (foto profil 1080, horizontal, SVG) + `BRAND.md` (warna, font, nada bicara, aturan) |
| `content/` | Profil IG, TikTok & X (nama, bio), naskah + caption EP01–EP03, bank ide konten |
| `videos/` | Hasil render EP01–EP03 (MP4 1080×1920) |
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

Baca `video-engine/README.md` lalu pakai template prompt di `video-engine/PROMPT_VIDEO_BARU.md` (episode terbaru sebagai contoh gaya premium: `video-engine/ep03_panggil-nama/`). Prinsip yang tidak boleh dilanggar:
- **Gaya visual tetap**: background hitam-ungu malam, aksen biru-ungu `#7F8CFF`, tag mono di atas judul, progress bar per bagian, judul "X, kok Y?" di atas, caption 2 baris dengan kata kunci di-highlight, watermark "RUANG PIKIR", outro logo + ruangpikir.id.
- **Suara**: Gemini TTS, voice `Achird`. Jangan pakai prompt gaya yang panjang (model kadang ikut membacakan instruksinya). Selalu cek durasi tiap baris.
- **Isi**: satu pertanyaan per video, berbasis riset nyata (sebut peneliti + tahun), bukan diagnosis, tidak melabeli orang nyata dengan gangguan mental, tidak membahas cara menyakiti diri.
- **QA wajib** sebelum menyerahkan: render contact sheet ±12 frame, pastikan tidak ada teks bertabrakan (zona caption y 1200–1390 harus bersih dari ilustrasi), loudness akhir sekitar −14 LUFS.

## Rahasia / API key

- **Jangan** menulis API key ke file di dalam repo atau commit (repo ini publik). Gunakan environment variable `GEMINI_API_KEY`:
  - di cloud Claude Code: pengaturan environment (Network secrets / environment variable `GEMINI_API_KEY`);
  - di VPS/laptop/sesi ini: file `.env` di folder repo (salin dari `.env.example`, chmod 600). `.env` diabaikan git, tetap ada saat `ruangpikir-deploy`, dan dibaca otomatis oleh `gemini_tts.py` (juga `GEMINI_TTS_MODEL`).
- `gemini-3.8-flash-tts` ikut membacakan prefix gaya: kirim kalimat tanpa prefix dan cek hasil suara dengan transkripsi.
- Kuota gratis Gemini TTS terbatas (±3 request/menit per model dan ada batas harian). Kalau kena 429, tunggu atau ganti model TTS (`GEMINI_TTS_MODEL`, misalnya `gemini-3.8-flash-tts` atau `gemini-2.5-flash-preview-tts`).
