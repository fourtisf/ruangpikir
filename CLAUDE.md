# Ruang Pikir — instruksi untuk Claude Code

Ruang Pikir adalah brand konten **psikologi sehari-hari** (Reels/TikTok/Shorts 9:16, 40–55 detik) dengan website **ruangpikir.id** dan Instagram **@ruangpikir2026**. Pemilik: ALFA. Paket ini berisi semua yang dibutuhkan untuk (1) deploy website dan (2) membuat episode video baru dengan gaya yang sama.

## Isi paket

| Folder | Isi |
|---|---|
| `website/` | `index.html` satu file (semua CSS/JS/gambar sudah inline), `logo.svg`, `DEPLOY.md` |
| `brand/` | Logo (foto profil 1080, horizontal, SVG) + `BRAND.md` (warna, font, nada bicara, aturan) |
| `content/` | Profil IG (nama, bio), caption EP01 & EP02, bank ide konten |
| `videos/` | Hasil render EP01 & EP02 (MP4 1080×1920) |
| `video-engine/` | Mesin animasi Python (skia) + suara Gemini TTS + audio/SFX + mux ffmpeg. Lihat `video-engine/README.md` |

## Tugas 1 — Deploy website ke ruangpikir.id

Ikuti `website/DEPLOY.md`. Ringkas:
- Website hanya satu file statis `website/index.html`. Tidak butuh build, server, atau database.
- Domain `ruangpikir.id` terdaftar di **Hostinger**; DNS A record `@` → VPS Hostinger (Ubuntu 24.04), CNAME `www` → apex.
- Di VPS: repo di-clone ke `/var/www/ruangpikir`, nginx melayani `website/`. Pasang/ulang: `bash deploy/setup-vps.sh` (lihat "Opsi C" di `website/DEPLOY.md`). Update: `git -C /var/www/ruangpikir pull`.
- Setelah live, cek: HTTPS aktif, `https://ruangpikir.id` dan `https://www.ruangpikir.id` sama-sama jalan, game tes otak bisa dimainkan di HP.
- Link sosial media diatur di objek `SOCIAL` di bagian bawah `index.html` (Instagram sudah `@ruangpikir2026`; TikTok/YouTube kosong = tombol disembunyikan).

## Tugas 2 — Membuat episode video baru

Baca `video-engine/README.md` lalu pakai template prompt di `video-engine/PROMPT_VIDEO_BARU.md`. Prinsip yang tidak boleh dilanggar:
- **Gaya visual tetap**: background hitam-ungu malam, aksen biru-ungu `#7F8CFF`, tag mono di atas judul, progress bar per bagian, judul "X, kok Y?" di atas, caption 2 baris dengan kata kunci di-highlight, watermark "RUANG PIKIR", outro logo + ruangpikir.id.
- **Suara**: Gemini TTS, voice `Achird`. Jangan pakai prompt gaya yang panjang (model kadang ikut membacakan instruksinya). Selalu cek durasi tiap baris.
- **Isi**: satu pertanyaan per video, berbasis riset nyata (sebut peneliti + tahun), bukan diagnosis, tidak melabeli orang nyata dengan gangguan mental, tidak membahas cara menyakiti diri.
- **QA wajib** sebelum menyerahkan: render contact sheet ±12 frame, pastikan tidak ada teks bertabrakan (zona caption y 1200–1390 harus bersih dari ilustrasi), loudness akhir sekitar −14 LUFS.

## Rahasia / API key

- **Jangan** menulis API key ke file atau commit. Gunakan environment variable: `export GEMINI_API_KEY=...`
- Kuota gratis Gemini TTS terbatas (±3 request/menit per model dan ada batas harian). Kalau kena 429, tunggu atau ganti model TTS (`GEMINI_TTS_MODEL`, misalnya `gemini-3.8-flash-tts` atau `gemini-2.5-flash-preview-tts`).
