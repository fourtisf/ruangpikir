# EP 04 — Pura-pura gapapa, kok capek?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep04-pura-pura-gapapa.mp4` (±54 detik, 1080×1920), halaman web `ruangpikir.id/episode/pura-pura-gapapa/`.
Seri: Kenapa Kamu Gitu? · Topik: menahan emosi (expressive suppression) vs memaknai ulang (reappraisal).

## Riset
- **Sumber utama:** Gross, J. J., & Levenson, R. W. (1997). Hiding feelings: The acute effects of inhibiting negative and positive emotion. *Journal of Abnormal Psychology, 106*(1), 95–103.
  - 180 peserta (perempuan) menonton film sedih, netral, dan lucu; separuh diminta menahan ekspresi.
  - Menahan ekspresi menurunkan ekspresi wajah, **tidak** menurunkan rasa sedih, dan **menaikkan aktivasi simpatis sistem jantung–pembuluh darah**.
- **Studi lanjutan:** Gross, J. J. (1998). Antecedent- and response-focused emotion regulation: Divergent consequences for experience, expression, and physiology. *Journal of Personality and Social Psychology, 74*(1), 224–237.
  - 120 peserta menonton film menjijikkan: memaknai ulang (reappraisal) vs menahan ekspresi vs menonton biasa.
  - Keduanya menurunkan ekspresi, tapi **memaknai ulang menurunkan rasa jijiknya**, sedangkan menahan ekspresi **menaikkan aktivasi simpatis**.
- **Jujur soal batasnya:** ini efek sesaat di laboratorium. "Capek" di judul adalah bahasa sehari-hari untuk "tubuh bekerja lebih keras", bukan klaim kelelahan klinis. Menahan ekspresi sesekali itu wajar; yang dibahas adalah kebiasaan memendam.

## Judul di layar
```
Pura-pura gapapa, [kok capek]?
```

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Pernah bilang \"aku gapapa\", padahal lagi nggak baik-baik aja?"),
    (3.48, "Senyum di luar, tapi di dalam rasanya mau meledak."),
    (6.22, "Ternyata, nahan emosi bikin tubuhmu makin tegang."),
    (8.91, "Tahun sembilan belas sembilan puluh tujuh, James Gross dan timnya mengujinya."),
    (13.13, "Peserta nonton film sedih. Separuhnya disuruh menahan ekspresi wajah."),
    (16.91, "Hasilnya? Wajahnya memang datar, tapi rasa sedihnya tetap ada."),
    (20.31, "Malah, jantung dan pembuluh darahnya kerja lebih keras."),
    (23.32, "Setahun kemudian, Gross menemukan cara yang lebih sehat: memaknai ulang situasinya."),
    (27.87, "Misalnya, \"dia bukan benci aku, dia lagi capek\". Perasaannya reda, tubuh nggak ikut tegang."),
    (32.85, "Kamu nggak harus selalu kuat. Cerita ke orang yang kamu percaya, ya."),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```

## Caption layar (b.CAPS)
```python
CAPS = [
    (0.15, "Bilang \"aku gapapa\",", "padahal [nggak baik-baik aja]?"),
    (3.48, "Senyum di luar,", "di dalam [mau meledak]"),
    (6.22, "Nahan emosi bikin", "tubuh [makin tegang]"),
    (8.91, "Tahun 1997, psikolog", "[James Gross] & tim menguji"),
    (13.13, "Peserta nonton film sedih,", "separuh [menahan ekspresi]"),
    (16.91, "Wajahnya datar, tapi", "[sedihnya tetap ada]"),
    (20.31, "Jantung & pembuluh darah", "[kerja lebih keras]"),
    (23.32, "Cara yang lebih sehat:", "[memaknai ulang]"),
    (27.87, "Perasaan reda,", "tubuh [nggak ikut tegang]"),
    (32.85, "Nggak harus selalu kuat,", "[cerita] ke orang terpercaya"),
    (36.6, "Follow [Ruang Pikir]", "biar makin kenal isi kepalamu"),
]
```

## Adegan (gaya sinematik, seperti video acuan "Jam 2 pagi")
Judul hanya di adegan pertama, tanpa tag, caption besar per frasa (`PHRASES` di `episode.py`).

| Waktu | Visual |
|---|---|
| 0–6.2 | Kartu kaca mengetik "Aku gapapa kok." lalu berubah jadi wajah senyum ("di luar"); bola "emosi" di lantai membesar, memerah, lantai melengkung, lalu retak bercahaya ("di dalam", *momen wow*). |
| 6.2–8.9 | Siluet kepala + bahu garis tipis, jantung berdetak makin cepat, pembuluh darah menyala. |
| 8.9–13.1 | Kartu besar RISET · 1997 · James Gross & Robert Levenson · 180 peserta. |
| 13.1–16.9 | Layar "film sedih" dengan wajah sedih, mata menonton, lalu dua wajah: nonton biasa (menangis) vs tahan ekspresi (datar + gembok). |
| 16.9–23.3 | Batang perbandingan Nonton biasa vs Tahan ekspresi untuk Ekspresi wajah → "datar", Rasa sedih → "tetap ada", Kerja jantung → "lebih keras" (tanpa angka). |
| 23.3–27.9 | Kartu RISET 1998 · James Gross; bola "menahan" (merah) vs "maknai ulang" yang menyala hijau + centang. |
| 27.9–32.9 | Chat "ok." → pikiran "dia benci aku..." dicoret → "dia lagi capek."; bola emosi mengempis dan jadi hijau, "tenang". |
| 32.9–36.6 | Teman datang, bola emosi kecil dibagi di tengah, gelembung "...", hati. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
"Aku gapapa" itu bikin capek
```

## Caption Instagram
```
"Aku gapapa kok." Padahal di dalam lagi nggak baik-baik aja? 🙂

Tahun 1997, psikolog James Gross dan Robert Levenson meminta 180 peserta menonton film sedih. Separuhnya disuruh menahan ekspresi wajah.

Hasilnya: wajah mereka memang datar, tapi rasa sedihnya tetap ada. Malah, jantung dan pembuluh darahnya bekerja lebih keras.

Setahun kemudian, Gross menemukan cara yang lebih sehat: memaknai ulang situasinya. Misalnya, chat cuma dibalas "ok." → "dia mungkin lagi capek", bukan langsung "dia benci aku". Perasaannya reda, tubuh nggak ikut tegang.

Kamu nggak harus selalu kuat. Cerita ke orang yang kamu percaya, atau ke psikolog kalau rasanya berat terus 🤍

📩 Kirim ke teman yang paling sering bilang "aku gapapa".
💬 Kalimat "gapapa" versi kamu apa? Tulis di komentar 😅
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Gross & Levenson (1997), Journal of Abnormal Psychology; Gross (1998), Journal of Personality and Social Psychology.

#psikologi #faktapsikologi #kesehatanmental #emosi #selfcare #ruangpikir
```

## Caption TikTok
```
"Aku gapapa kok", padahal nggak? 🙂

Riset Gross & Levenson (1997): menahan ekspresi bikin wajah datar, tapi rasa sedihnya tetap ada dan tubuh malah lebih tegang. Cara yang lebih sehat: memaknai ulang situasinya (Gross, 1998).

Kirim ke teman yang paling sering bilang "gapapa" 🤍

#psikologi #kesehatanmental #emosi #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Contoh memaknai ulang: chat dibalas "ok." → bukan "dia marah sama aku", tapi "mungkin dia lagi sibuk atau capek". Kamu punya contoh lain? 👇
```

## Story promosi
```
Sering bilang "aku gapapa"? 🙂
Ternyata nahan emosi bikin tubuh makin tegang.
Tonton video barunya 👇
```

## Produksi
Folder `video-engine/ep04_pura-pura-gapapa/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice`. Suara resep EP01 (`vo_full.py`), dipotong per kalimat dengan `split_lines` (memperhitungkan panjang kalimat), lalu `tighten.py 0.30` memendekkan jeda > 0,3 dtk di dalam kalimat supaya durasi ≤ 55 dtk. Di take ini model menambahkan "Hmm" di awal baris pertama; bagian itu (0,8 dtk pertama `l00.wav`) dibuang manual.
