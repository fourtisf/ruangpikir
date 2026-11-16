# EP 46 — Anak sulung, kok dicap galak?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep46-anak-sulung.mp4` (±54 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/anak-sulung/`.
Format: **fakta mengejutkan / mitos**, hasil riset topik netizen Indonesia: konten anak sulung/bungsu dan tagar #anakperempuanpertama yang ramai di TikTok. Ajakan komentar "kamu anak ke berapa?" + tag saudara.
Gaya: premium **"panggung tiga podium"**: studio sorot, podium kaca bernomor, label stereotip berayun di rantai, tabung kaca data.

## Riset
- **Sumber utama:** Rohrer, J. M., Egloff, B., & Schmukle, S. C. (2015). Examining the effects of birth order on personality. *PNAS.* https://doi.org/10.1073/pnas.1506451112
  - Data 3 panel nasional: Amerika Serikat (n = 5.240), Inggris (n = 4.489), Jerman (n = 10.457); total lebih dari 20.000 orang dewasa.
  - Membandingkan saudara dalam satu keluarga maupun antar keluarga.
  - **Tidak ada** efek urutan lahir pada ekstraversi (supel), stabilitas emosi (gampang cemas), keramahan, kehati-hatian (rajin), dan imajinasi.
  - Hanya ada penurunan kecil (±1/10 SD) pada "merasa pintar" (laporan diri) seiring urutan lahir, dan efek kecil pada kecerdasan.
- **Pendukung:** Damian, R. I., & Roberts, B. W. (2015). *Journal of Research in Personality*, 377.000 siswa SMA di AS.
  - Anak pertama sekitar **1 poin IQ** lebih tinggi; signifikan secara statistik, tapi nyaris tidak bermakna dalam kehidupan sehari-hari.
  - Perbedaan kepribadian setara korelasi **0,02** ("sangat kecil").
- **Jujur soal batasnya:**
  - Data dari negara Barat (AS, Inggris, Jerman), bukan Indonesia.
  - Ini rata-rata kelompok; pengalaman tiap keluarga bisa berbeda, misalnya anak sulung yang diberi tanggung jawab lebih (tidak diukur).
  - Riset lanjutan Rohrer dkk. (2017) tentang sifat yang lebih spesifik hasilnya campur.
- Tidak ada data Francesca Gino.

## Judul di layar
```
Anak sulung, kok [dicap galak?]
```

## Hook (detik 0–3)
- Suara: **"Anak sulung pasti galak, bungsu pasti manja? Riset dua puluh ribu orang bilang: itu mitos."**
- Visual sejak frame pertama:
  - tiga podium kaca bernomor 1, 2, 3 naik dari lantai di bawah lampu sorot berwarna, lalu tokoh kapsul SULUNG, TENGAH, BUNGSU jatuh ke atasnya;
  - label kaca **GALAK**, **TERLUPAKAN**, **MANJA** berayun di rantai di atas kepala mereka;
  - chip RISET 20.000 ORANG, lalu label putus dan jatuh + stempel **MITOS**.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Anak sulung pasti galak, bungsu pasti manja? Riset dua puluh ribu orang bilang: itu mitos."),
    (5.64, "Tapi tahun dua ribu lima belas, Julia Rohrer dan timnya ngecek data lebih dari dua puluh ribu orang, di Amerika, Inggris, dan Jerman."),
    (12.74, "Hasilnya? Urutan lahir nggak ngaruh ke kepribadian. Nggak bikin kamu lebih supel, lebih rajin, lebih ramah, atau lebih gampang cemas."),
    (19.6, "Riset lain dengan tiga ratus tujuh puluh tujuh ribu siswa juga sama: bedanya hampir nol."),
    (24.16, "Satu-satunya beda: anak pertama unggul sekitar satu poin IQ. Itu pun nyaris nggak kerasa."),
    (29.27, "Jadi kalau kamu dicap galak atau manja, itu bukan karena nomor urut lahirmu."),
    (33.57, "Kamu anak ke berapa? Tulis di komentar, terus tag kakak atau adikmu!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
- Transkripsi persis dan instruksi gaya tidak ikut terbaca.
- Suara versi ini lebih lambat, jadi baris kedua ("Kita sering dengar: anak pertama tegas, anak tengah terlupakan, anak bungsu manja.") dihapus dari `vo/lines.json`, supaya video ≤ 55 dtk; isinya sudah tercakup di hook. Dipakai juga `tighten.py 0.17`.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–5.6 | **Hook:** podium 1/2/3 naik + lampu sorot, tokoh jatuh ke podium, label GALAK / TERLUPAKAN / MANJA berayun di rantai → RISET 20.000 ORANG → label putus & jatuh + stempel **MITOS**. |
| 5.6–12.7 | Kartu ARSIP RISET 2015 · Rohrer, Egloff & Schmukle · PNAS → **20.000+ ORANG**: tiga tabung kaca data terisi (AMERIKA 5.240, INGGRIS 4.489, JERMAN 10.457). |
| 12.7–19.6 | HASILNYA? → **NGGAK NGARUH** + tiga tokoh 1/2/3 → 4 panel kaca (SUPEL, RAJIN, RAMAH, GAMPANG CEMAS) masing-masing dengan 3 tabung sama tinggi + keterangan 1 SULUNG / 2 TENGAH / 3 BUNGSU → SAMA AJA. |
| 19.6–24.2 | DAMIAN & ROBERTS · 2015 + **377.000 SISWA** + grid ikon orang → **≈ 0** + sinar → BEDANYA HAMPIR NOL. |
| 24.2–29.3 | SATU-SATUNYA BEDA → **±1 POIN IQ**: dua tabung ANAK PERTAMA vs ADIKNYA yang hampir sama tinggi + kaca pembesar → NYARIS NGGAK KERASA. |
| 29.3–33.6 | Tokoh di podium lagi, label GALAK & MANJA muncul lalu putus, tokoh tersenyum & berpendar → **BUKAN KARENA URUTAN LAHIR**. |
| 33.6–36.6 | KAMU ANAK KE BERAPA?: tombol ANAK PERTAMA / TENGAH / BUNGSU / TUNGGAL menyala bergantian + kolom komentar mengetik "aku anak ke-" + TAG KAKAK ATAU ADIKMU. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Kamu anak ke berapa? Riset bilang ini mitos
```
Alternatif: `Anak sulung galak, bungsu manja? MITOS` · `Riset 20.000 orang soal anak sulung`

## Caption Instagram
```
Anak sulung pasti galak, bungsu pasti manja? Riset 20.000 orang bilang: itu MITOS 😳

Tahun 2015, Julia Rohrer dan timnya ngecek data lebih dari 20.000 orang di Amerika, Inggris, dan Jerman. Hasilnya? Urutan lahir nggak ngaruh ke kepribadian. Nggak bikin kamu lebih supel, lebih rajin, lebih ramah, atau lebih gampang cemas.

Riset lain dengan 377.000 siswa juga sama: bedanya hampir nol.

Satu-satunya beda: anak pertama unggul sekitar 1 poin IQ. Itu pun nyaris nggak kerasa 🤏

Jadi kalau kamu dicap galak atau manja, itu bukan karena nomor urut lahirmu 💛

💬 Kamu anak ke berapa? Tulis di komentar!
👯 Tag kakak atau adikmu
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Rohrer, Egloff & Schmukle (2015), PNAS; Damian & Roberts (2015), Journal of Research in Personality.

#psikologi #faktapsikologi #anaksulung #anakpertama #anakbungsu #ruangpikir
```

## Caption TikTok
```
Anak sulung galak, bungsu manja? Riset 20.000 orang: MITOS 😳

Urutan lahir nggak ngaruh ke kepribadian. Bedanya cuma ±1 poin IQ, nyaris nggak kerasa 🤏

Kamu anak ke berapa? 👇 Tag kakak/adikmu!

#psikologi #anaksulung #anakpertama #anakbungsu #anakperempuanpertama #ruangpikir
```

## Komentar pertama (pin)
```
Aku anak pertama dan selalu dicap galak 😭 padahal cuma disuruh jagain adik dari kecil. Kamu anak ke berapa? Sulung, tengah, bungsu, atau tunggal? 👇
```

## Story promosi
```
Anak sulung pasti galak, bungsu pasti manja? 🤨
Riset 20.000 orang bilang: itu mitos.
Tonton video barunya 👇
```
Stiker kuis: `Kamu anak ke berapa? Sulung / Tengah / Bungsu / Tunggal`

## Judul YouTube Shorts
```
Anak sulung galak, bungsu manja? Riset 20.000 orang bilang ini MITOS #shorts
```

## Waktu upload
Minggu malam 19.00–21.00 WIB, saat kumpul keluarga. Di jam pertama, balas komentar dengan "terus sifat itu menurutmu dari mana?" supaya diskusinya hidup.

## Produksi
- **Folder:** `video-engine/ep46_anak-sulung/` (dibangun dari EP45).
- **Render:**
  - Render ulang dengan `./build.sh`; suara sudah ada di `vo/` (8 baris di `lines.json`).
  - Buat ulang suara dengan `./build.sh --voice`, lalu cek durasi (target ≤ 55 dtk) dan ubah anchor di `vo/lines.json`.
  - `DUR` 42, jeda antarbaris 0,35 dtk, encode CRF 26.
- **Lagu orisinal:** `audio.py` di folder ini (variasi EP22: 104 BPM, `TR = 0`).
- **Versi tanpa musik:**
  1. `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`
  2. Mux ke video yang sudah ada (loudnorm I=-13.6 → ±−14 LUFS).
- **Helper baru:**
  - `podium()` — podium kaca 3D bernomor.
  - `hang_tag()` — label kaca berayun di rantai, ayunan teredam, bisa putus & jatuh.
  - `trait_cell()` — panel sifat + 3 tabung sama tinggi.
  - `sib_legend()`.
- **Dipakai juga:** `studio()`, `spot()`, `hero()`, `tube()` (EP36), `person_grid()` (EP41), `magnifier()`, `chain()`, `stamp()`, `sparks()`, `team_btn()` (EP45), `research_card()`, `extrude()`.
