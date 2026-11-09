# EP 30 — Makin dewasa, kok makin jauh dari orang tua?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep30-jauh-dari-orang-tua.mp4` (±55 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/jauh-dari-orang-tua/`.
Format: **"fakta psikologi yang agak nyakitin" / 3 alasan** (permintaan ALFA: "dark psikologi, kenapa udah dewasa kita jadi jarang ke orang tua"). Pasangan EP29 (telepon orang tua).

## Riset
1. **Waktu terasa masih banyak** — Fredrickson, B. L., & Carstensen, L. L. (1990). Choosing social partners: How old age and anticipated endings make people more selective. *Psychology and Aging, 5*(3), 335–347. (Teori selektivitas sosioemosional, Laura Carstensen, Stanford.)
   - Saat masa depan terasa panjang, orang muda memilih teman bergaul relatif merata, termasuk yang baru (informasi, peluang). Orang tua lebih memilih orang yang bermakna secara emosional.
   - Saat anak muda diminta membayangkan **akan pindah jauh** (akhir yang terasa dekat), pilihan mereka **sama dengan orang tua**: orang yang paling bermakna secara emosional.
2. **Nasihat yang tidak diminta** — Birditt, K. S., Miller, L. M., Fingerman, K. L., & Lefkowitz, E. S. (2009). Tensions in the parent and adult child relationship: Links to solidarity and ambivalence. *Psychology and Aging, 24*(2), 287–295.
   - **474** orang tua dan anak dewasa (usia ≥ 22). Perbedaan sifat dan **nasihat yang tidak diminta** termasuk sumber tegang yang paling bikin masalah (kutipan Kira Birditt di rilis University of Michigan). Orang tua secara umum melaporkan tegang lebih kuat soal gaya hidup anak.
3. **Orang tua merasa lebih dekat daripada anaknya** — *intergenerational stake* (Bengtson & Kuypers, 1971); Giarrusso, R., Feng, D., & Bengtson, V. L. (2004). The intergenerational stake phenomenon over 20 years. *Annual Review of Gerontology and Geriatrics, 24*, 55–76 (data Longitudinal Study of Generations, 1971–1991).
   - Orang tua cenderung menilai hubungannya dengan anak lebih dekat/positif daripada penilaian si anak.
4. **Hitungan 140 hari** — hitungan sederhana, bukan riset: pulang 7 hari setahun × 20 tahun = 140 hari (< 5 bulan); 20 tahun = 1.040 minggu. Kotak emas di kalender video bergeser ±11 hari lebih awal tiap tahun seperti Lebaran.
- **Jujur soal batasnya:** riset dari Amerika Serikat. Ada peneliti yang menjelaskan selisih penilaian (alasan 3) dengan "bias positif" orang yang lebih tua, bukan hanya stake. Contoh "kapan nikah?", "kok gendutan?" adalah contoh sehari-hari, bukan kalimat dari riset. Batang di video ilustratif tanpa angka. Video tidak menyalahkan anak maupun orang tua dan tidak membahas hubungan yang berbahaya (kalau hubungan dengan orang tua menyakitkan, menjaga jarak bisa jadi pilihan yang sehat — ini bisa dibalas di komentar). Tidak ada data Francesca Gino.

## Judul di layar
```
Makin dewasa, kok [makin jauh dari orang tua?]
```

## Hook (detik 0–3)
- Suara: **"Makin dewasa, kok makin jauh dari orang tua? Ini tiga alasan psikologis yang agak nyakitin."**
- Visual sejak frame pertama: tokoh anak kecil di samping Ibu (hati melayang), label **UMUR 5 TAHUN** yang terus naik sampai **25 TAHUN** sementara tokohnya tumbuh dan **menjauh** dari rumah (garis putus-putus **MAKIN JAUH**), lalu 3 kartu **ALASAN 01–03** disensor + gembok, kartu 03 merah berdenyut **PALING NYAKITIN**.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 41.5)
```python
LINES = [
    (0.15, "Makin dewasa, kok makin jauh dari orang tua? Ini tiga alasan psikologis yang agak nyakitin."),
    (5.39, "Pertama: kita ngerasa waktunya masih banyak, jadi sibuk ngejar hal baru."),
    (8.78, "Tapi di riset Laura Karstensen, begitu anak muda bayangin bakal pindah jauh, mereka milih orang yang paling berarti."),
    (14.3, "Kedua: nasihat yang nggak diminta. Riset Kira Birdit nemuin, ini salah satu pemicu tegang yang paling bikin masalah."),
    (19.5, "Ketiga, yang paling nyakitin: orang tua ngerasa lebih dekat ke kamu, daripada kamu ke mereka."),
    (24.05, "Vern Bengtsen nemuin pola ini berulang, selama dua puluh tahun."),
    (27.23, "Kalau kamu cuma pulang seminggu setahun, dua puluh tahun ke depan cuma seratus empat puluh hari."),
    (31.21, "Jadi bukan karena nggak sayang. Mulai dari telepon sebentar, malam ini."),
    (34.56, "Kirim video ini ke teman yang lagi jauh dari rumah!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Karstensen / Birdit / Bengtsen" = ejaan fonetik untuk TTS (caption tetap Carstensen, Birditt, Bengtson).

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–5.4 | **Hook:** anak tumbuh 5 → 25 tahun sambil menjauh dari rumah Ibu (MAKIN JAUH) + 3 kartu ALASAN disensor, 03 merah PALING NYAKITIN. |
| 5.4–8.8 | Kartu ALASAN 01 dibuka "Waktu kerasa masih banyak", jam pasir "MASIH BANYAK...", rumah Ibu kecil di kejauhan, chip kerja / teman baru / nongkrong / pasangan. |
| 8.8–14.3 | Kartu riset 1990 Fredrickson & Carstensen (Stanford) → BAYANGIN "Bakal pindah jauh": rute pesawat dari rumah ke KOTA BARU → KENALAN BARU ✗ vs ORANG PALING BERARTI ✓ (Ibu + anak). |
| 14.3–19.5 | ALASAN 02 "Nasihat yang nggak diminta", kartu Birditt dkk. 2009 · 474 orang tua & anak dewasa, Ibu: "kapan nikah?", "kok gendutan?", "gajinya berapa?", "jangan begadang!", meter TEGANG memerah, stempel PEMICU TEGANG. |
| 19.5–24.1 | ALASAN 03 merah "Mereka ngerasa lebih dekat": batang MENURUT ORANG TUA (tinggi) vs MENURUT ANAK (lebih pendek) + SELISIH. |
| 24.1–27.2 | 20 TAHUN · INTERGENERATIONAL STAKE: pasangan batang 1971 / 1985 / 1991 (ilustrasi), Bengtson & Kuypers 1971 · Giarrusso dkk. 2004. |
| 27.2–31.2 | 1 KOTAK = 1 MINGGU: kalender 20 tahun × 52 minggu, satu kotak emas per tahun (Lebaran maju tiap tahun) → 20 TAHUN = 1.040 MINGGU, PULANG = 20 MINGGU → **140 HARI** · KURANG DARI 5 BULAN. |
| 31.2–34.6 | "BUKAN KARENA nggak sayang." + MULAI DARI TELEPON SEBENTAR: ponsel berdering → tersambung, Ibu senang, hati beterbangan. |
| 34.6–36.6 | Kartu "MALAM INI · Telepon sebentar, ya." + panel KIRIM KE (teman rantau, sahabat, kakak, adik) + TERKIRIM. |
| 36.6–41.5 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Makin dewasa, kok makin jauh dari orang tua?
```
Alternatif: `3 alasan kamu makin jauh dari orang tua (no. 3 nyakitin)` atau `Pulang seminggu setahun = 140 hari lagi`

## Caption Instagram
```
Makin dewasa, kok makin jauh dari orang tua? 🥲 Ini 3 alasan psikologis yang agak nyakitin.

1️⃣ Kita ngerasa waktunya masih banyak, jadi sibuk ngejar hal baru: kerja, teman, pasangan. Tapi di riset Laura Carstensen (1990), begitu anak muda bayangin bakal pindah jauh, mereka langsung milih orang yang paling berarti.

2️⃣ Nasihat yang nggak diminta 😅 "Kapan nikah?", "kok gendutan?". Riset Kira Birditt dkk. (2009) ke 474 orang tua & anak dewasa: ini salah satu pemicu tegang yang paling bikin masalah.

3️⃣ Yang paling nyakitin: orang tua ngerasa lebih dekat ke kamu, daripada kamu ke mereka. Vern Bengtson nemuin pola ini berulang selama 20 tahun.

Kalau kamu cuma pulang seminggu setahun, 20 tahun ke depan cuma 140 hari ⏳

Jadi bukan karena kamu nggak sayang. Mulai dari telepon sebentar, malam ini 📞🤍

📩 Kirim ke teman yang lagi jauh dari rumah
💬 Kamu paling relate alasan nomor berapa? 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Fredrickson & Carstensen (1990), Psychology and Aging; Birditt dkk. (2009), Psychology and Aging; Giarrusso, Feng & Bengtson (2004).

#psikologi #faktapsikologi #orangtua #anakrantau #keluarga #ruangpikir
```

## Caption TikTok
```
Makin dewasa, kok makin jauh dari orang tua? 🥲 3 alasan psikologisnya (no. 3 paling nyakitin)

Pulang seminggu setahun, 20 tahun ke depan cuma 140 hari ⏳ Telepon sebentar malam ini ya 🤍

Kirim ke teman yang lagi jauh dari rumah 📩

#psikologi #faktapsikologi #orangtua #anakrantau #ruangpikir
```

## Komentar pertama (pin)
```
Yang paling bikin aku diem: pulang seminggu setahun, 20 tahun lagi cuma 140 hari 🥲 Kamu paling relate alasan nomor berapa? 1, 2, atau 3? 👇
```
Kalau ada yang menulis hubungannya dengan orang tua menyakitkan: balas dengan hangat, misalnya *"Valid banget. Video ini buat hubungan yang aman. Kalau hubungannya menyakitkan, menjaga jarak juga bentuk menjaga diri 🤍"*.

## Story promosi
```
Makin dewasa, kok makin jauh dari orang tua? 🥲
3 alasan psikologisnya, dan nomor 3 agak nyakitin.
Tonton video barunya 👇
```
Stiker kuis: `Pulang seminggu setahun, 20 tahun ke depan jadi berapa hari? 52 / 140 / 365` (jawaban: 140)

## Judul YouTube Shorts
```
Makin dewasa kok makin jauh dari orang tua? 3 alasan psikologis #shorts
```

## Waktu upload
Malam 19.00–21.00 WIB, Jumat–Minggu (jam anak rantau santai dan sering kepikiran rumah). Upload EP29 (telepon orang tua) 1–2 hari setelahnya sebagai lanjutan: "kemarin alasannya, sekarang caranya".

## Produksi
Folder `video-engine/ep30_jauh-dari-ortu/` (dibangun dari EP29): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` lalu `python3 tighten.py 0.15` (resep EP01; suara mentah ±63 dtk). Supaya video ≤ 55 dtk, `base.py` folder ini memakai `DUR` 41.5 dan jeda antarbaris 0.26 dtk. Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 86 BPM, `TR = -3`, lebih sendu). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper baru: `reason_card()`, `reason_head()`, `grow_kid()`, `hourglass()`, `tension_bar()`, `vbar()`; plus dari EP29 `ibu()`, `house()`, `moon()`, `mini_phone()`, dan `research_card()`, `say()`, `stamp()`, `extrude()`, `check_mark()`, `cross()`, `avatar()`, `plane_icon()`, `waves()`.
