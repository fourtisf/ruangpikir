# EP 16 — Mau ujian, kok blank?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep16-takut-blank.mp4` (±55 detik, 1080×1920), halaman web `ruangpikir.id/episode/takut-blank/`.
Seri: Trik Psikologi (format seperti EP03, EP12–EP15) · Topik: menulis kekhawatiran 10 menit sebelum ujian (expressive writing).

## Riset
- **Sumber utama:** Ramirez, G., & Beilock, S. L. (2011). Writing about testing worries boosts exam performance in the classroom. *Science, 331*(6014), 211–213. (University of Chicago)
  - Eksperimen lab dengan mahasiswa: tes matematika dengan tekanan tinggi. Yang hanya duduk diam sebelum tes nilainya turun ("choking"); yang menulis kekhawatirannya tentang tes selama ±10 menit justru tampil lebih baik. Eksperimen kedua: menulis tentang hal lain (bukan kekhawatiran) tidak membantu.
  - Studi kelas: siswa kelas 9 high school di AS (tahun pertama SMA di sana) menjelang ujian akhir biologi. Manfaat menulis kekhawatiran paling terasa pada siswa yang mudah cemas menghadapi ujian.
  - Penjelasan peneliti: kekhawatiran memakan memori kerja; menuliskannya mengurangi beban itu.
- **Jujur soal batasnya:** besar efek berbeda-beda di tiap liputan media, jadi video memakai "anjlok" vs "naik" tanpa angka. Siswa yang tidak mudah cemas tidak banyak terbantu. Bukan pengganti bantuan untuk kecemasan berat; halaman web menyarankan bercerita ke konselor/psikolog.

## Judul di layar
```
Mau ujian, [kok blank]?
```

## Hook (detik 0–3)
- Suara: **"Besok ujian, tapi takut blank? Sepuluh menit sebelum mulai, tulis ini."** Situasi yang dialami hampir semua pelajar/mahasiswa + open loop "tulis ini" (baru dijawab di detik ±33: "tulis semua takutmu").
- Visual sejak frame pertama: ruang ujian malam, tokoh kapsul gemetar di balik meja, jam dinding berdetak cepat; balok-balok kekhawatiran 3D ("nanti salah", "nilai jelek", "kata ortu?", "waktu habis!", "lupa rumus", "malu") berjatuhan ke panel kaca **MEMORI KERJA** sampai **98% PENUH!**; di kata "blank" lembar soal glitch merah lalu kosong "..."; chip "10 menit"; di "tulis ini" kertas emas misterius **"? ? ?"** + pulpen emas melayang dengan sinar.

## Gaya visual
"Ruang ujian malam + panel memori kerja": panel kaca dengan slot + balok kekhawatiran 3D mengilap, bar persen hijau→merah + PENUH!, lembar soal (glitch/blank, jawaban tinta biru), kertas bergaris yang ditulisi, pulpen emas, meja kayu, jam dinding, timer 10:00, batang nilai + panah ANJLOK/NAIK, kartu UJIAN BIOLOGI dengan DNA, balok yang terbang dari kepala ke kertas sampai **KEPALA LEGA** dan balok "rumus" akhirnya muat. Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 41.2)
```python
LINES = [
    (0.15, "Besok ujian, tapi takut blank? Sepuluh menit sebelum mulai, tulis ini."),
    (3.69, "Soalnya pas cemas, pikiran kayak nanti salah, nanti nilainya jelek, ikut makan tempat di memori kerja otakmu."),
    (9.2, "Tahun dua ribu sebelas, psikolog Gerardo Ramirez dan Sian Bailok menguji ini."),
    (13.09, "Sebelum ujian yang menegangkan, sebagian mahasiswa cuma duduk diam, sebagian lagi menulis semua kekhawatirannya selama sepuluh menit."),
    (19.82, "Hasilnya? Yang cuma diam, nilainya anjlok. Yang menulis, nilainya justru naik."),
    (23.76, "Di ujian biologi anak SMA, efeknya paling terasa buat yang gampang cemas."),
    (27.45, "Soalnya kekhawatiran yang udah pindah ke kertas, nggak lagi menuh-menuhin kepala."),
    (31.54, "Jadi sebelum ujian, tulis semua takutmu sepuluh menit. Kamu ujian apa minggu ini? Tulis di komentar!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Sian Bailok" = ejaan fonetik Sian Beilock untuk TTS (caption tetap "Sian Beilock").

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–3.7 | **Hook:** ruang ujian, balok kekhawatiran memenuhi MEMORI KERJA 98% PENUH!, lembar soal glitch → kosong, chip "10 menit", kertas emas "? ? ?" + pulpen. |
| 3.7–9.2 | SAAT CEMAS: panel memori besar, enam balok jatuh satu per satu sampai penuh; balok "rumus" (hijau) memantul — "nggak muat!". |
| 9.2–13.1 | Kartu ARSIP RISET 2011 · Ramirez & Beilock · Science; chip University of Chicago. |
| 13.1–19.8 | DUDUK DIAM (tokoh cemas, lembar soal) vs MENULIS (tokoh tenang menulis "takut salah / takut lupa / takut gagal"); timer 10:00 berjalan. |
| 19.8–23.8 | Batang nilai: duduk diam ANJLOK (panah merah turun), menulis NAIK (panah emas naik + kilau). |
| 23.8–27.5 | Kartu UJIAN BIOLOGI · siswa SMA; "santai" efek kecil vs "gampang cemas" efek besar + "paling terasa". |
| 27.5–31.5 | Balok kekhawatiran terbang dari panel ke kertas, memori turun ke ±24%, KEPALA LEGA, balok "rumus" akhirnya muat ✓. |
| 31.5–36.6 | Tokoh tersenyum mengerjakan soal (jawaban tinta biru), teks 3D "TULIS TAKUTMU" + "10 MENIT SEBELUM UJIAN", komentar "UAS kalkulus", "ujian SIM wkwk", "sidang skripsi", "UTBK!". |
| 36.6–41.2 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Takut blank pas ujian? Lakukan ini
```
Alternatif: `10 menit sebelum ujian, tulis ini` atau `Biar nggak blank pas ujian`

## Caption Instagram
```
Besok ujian, tapi takut blank? 😵‍💫 Sepuluh menit sebelum mulai, coba ini.

Pas cemas, pikiran kayak "nanti salah", "nanti nilainya jelek", ikut makan tempat di memori kerja otak. Padahal ruang itu yang kita pakai buat ngingat rumus dan mikir.

Tahun 2011, psikolog Gerardo Ramirez dan Sian Beilock (University of Chicago) menguji trik sederhana. Sebelum ujian yang menegangkan, sebagian mahasiswa cuma duduk diam, sebagian lagi menulis semua kekhawatirannya selama 10 menit.

Hasilnya? Yang cuma diam, nilainya anjlok. Yang menulis, nilainya justru naik ✍️ Di ujian biologi anak SMA, efeknya paling terasa buat yang gampang cemas.

Jadi sebelum ujian: ambil kertas, tulis semua takutmu 10 menit. Biar kekhawatirannya pindah ke kertas, bukan menuh-menuhin kepala 🤍

📌 Simpan buat dipakai sebelum ujian.
💬 Kamu ujian apa minggu ini? Tulis di komentar 👇
📩 Kirim ke teman yang besok ujian.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Ramirez & Beilock (2011), Science.

#psikologi #faktapsikologi #ujian #mahasiswa #tipsbelajar #ruangpikir
```

## Caption TikTok
```
Takut blank pas ujian? Tulis semua kekhawatiranmu 10 menit sebelum mulai ✍️

Riset Ramirez & Beilock (2011, Science): yang cuma diam sebelum ujian nilainya anjlok, yang menulis kekhawatirannya justru naik. Paling terasa buat yang gampang cemas.

Kamu ujian apa minggu ini? 👇

#psikologi #ujian #tipsbelajar #mahasiswa #ruangpikir
```

## Komentar pertama (pin)
```
Coba sebelum ujian berikutnya: 10 menit, tulis semua yang kamu takutin (nggak usah rapi, nggak usah dibaca orang). Abis ujian balik ke sini, ceritain hasilnya 👇
```

## Story promosi
```
Besok ujian? 😵‍💫
Takut blank? Lakukan ini 10 menit sebelum mulai.
Tonton video barunya 👇
```

## Judul YouTube Shorts
```
Takut blank pas ujian? Coba trik 10 menit ini (riset psikologi) #shorts
```

## Produksi
Folder `video-engine/ep16_takut-blank/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01; jeda dipendekkan dengan `tighten.py 0.18`, dan `DUR` di `base.py` folder ini 41.2 supaya video ≤ 55 dtk). Encode CRF 26. Helper baru: `mem_panel()` (panel kaca memori kerja: slot, balok jatuh/keluar, bar persen, PENUH!), `block3d()` (balok kekhawatiran 3D), `exam_paper()` (`blank` glitch, `ans` jawaban), `note_paper()` (tulisan bertahap, `mystery`), `pen()`, `desk()`, `wall_clock()`, `big_arrow()`, `score_col()`, `dna()`, `research_card(tag=...)`; plus helper EP12–EP15 (`hero()`, `meter()`, `chip()`, `comment()`, `extrude()`).
