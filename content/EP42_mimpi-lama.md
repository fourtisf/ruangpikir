# EP 42 — Mimpi lama, kok belum dikejar?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep42-mimpi-lama.mp4` (±54 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/mimpi-lama/`.
Format: **seri 36 pertanyaan** (lanjutan EP39 yang viral, EP40, EP41): satu pertanyaan + plot twist riset + jawab di komentar. Gaya **"lab hologram"**.

## Riset
- **Pertanyaan:** Aron, A., Melinat, E., Aron, E. N., Vallone, R. D., & Bator, R. J. (1997). *PSPB, 23*(4), 363–377.
  - Pertanyaan nomor 14: *"Is there something that you've dreamed of doing for a long time? Why haven't you done it?"*
- **Plot twist:** Davidai, S., & Gilovich, T. (2018). The ideal road not taken: The self-discrepancies involved in people's most enduring regrets. *Emotion, 18*(3), 439–452. https://doi.org/10.1037/emo0000326 (Cornell University.)
  - 6 studi, ratusan peserta.
  - Dua jenis penyesalan:
    - **diri impian** (*ideal self*: tujuan, cita-cita, orang yang ingin kita jadi);
    - **diri yang seharusnya** (*ought self*: kewajiban, tanggung jawab).
  - Penyesalan soal diri impian jauh lebih sering: **72% vs 28%**. Saat diminta mendaftar semua penyesalan, selisihnya mengecil: 57% vs 43%.
  - Penjelasan: penyesalan soal kewajiban terasa lebih mendesak, jadi orang lebih cepat bertindak untuk membereskannya. Penyesalan soal mimpi lebih sering didiamkan, sehingga bertahan lebih lama.
- **Jujur soal batasnya:**
  - Data berasal dari laporan diri (orang mengingat penyesalannya sendiri), bukan pengamatan perilaku.
  - Kalimat "kewajiban yang gagal biasanya cepat kita beresin" adalah ringkasan dari temuan bahwa orang lebih banyak mengambil langkah untuk mengatasi penyesalan jenis ini.
  - Contoh alasan ("nanti aja", "belum waktunya", "takut gagal") ilustratif, bukan data riset.
- **Ilustratif:** siluet diri impian, kerumunan hologram, timbangan, kapsul mimpi. Tidak ada data Francesca Gino.

## Judul di layar
```
Mimpi lama, kok [belum dikejar?]
```

## Hook (detik 0–3)
- Suara: **"Penyesalan yang paling lama nempel, ternyata bukan soal kesalahan."**
- Visual sejak frame pertama (versi 2 "studio jam pasir"):
  - **jam pasir kaca raksasa** jatuh sambil terbalik di bawah lampu sorot studio, lalu mendarat dengan kilatan garis cahaya;
  - di tabung atas melayang **bintang mimpi** emas, pasir emas mulai mengalir;
  - teks 3D **PENYESALAN PALING LAMA**, lalu tag kaca **BUKAN SOAL KESALAHAN** berayun di rantai dan dicoret.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Penyesalan yang paling lama nempel, ternyata bukan soal kesalahan."),
    (3.74, "Coba jawab ini: ada mimpi yang udah lama pengen kamu lakuin? Kenapa belum?"),
    (7.27, "Ini pertanyaan nomor empat belas, dari tiga puluh enam pertanyaan psikolog Arthur Aron."),
    (11.19, "Mungkin jawabanmu: nanti aja, belum waktunya, atau takut gagal."),
    (15.35, "Tapi tahun dua ribu delapan belas, Thomas Gilovich dan timnya nanya ratusan orang soal penyesalan mereka."),
    (20.23, "Hasilnya? Tujuh puluh dua persen penyesalan itu soal diri impian yang nggak dikejar. Soal kewajiban yang gagal, cuma dua puluh delapan persen."),
    (26.79, "Soalnya kewajiban yang gagal biasanya cepat kita beresin. Tapi mimpi? Sering cuma kita tunda."),
    (31.52, "Kamu sendiri, mimpi apa yang belum kamu kejar? Tulis di komentar, terus kirim ke temanmu yang lagi nunda mimpinya!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
- Transkripsi persis dan instruksi gaya tidak ikut terbaca.
- `tighten.py 0.17` dan jeda antarbaris 0,30 dtk (`base.py`) dipakai supaya video ≤ 55 dtk.

## Adegan (versi 2 "studio jam pasir")
ALFA minta "visual berbeda yang lebih premium", jadi versi 1 (lab hologram: diri impian di jembatan cahaya, kapsul mimpi, timbangan hologram) diganti. Isinya:
- studio malam dengan lampu sorot dan lantai mengilap yang memantulkan objek;
- satu objek utama: **jam pasir kaca raksasa** berisi pasir emas dan bintang mimpi;
- banyak gerak fisik (jatuh, berayun, dibalik, menumpuk).

| Waktu animasi | Visual |
|---|---|
| 0–7.3 | **Hook + pertanyaan:** jam pasir jatuh, terbalik, lalu mendarat + PENYESALAN PALING LAMA + tag BUKAN SOAL ~~KESALAHAN~~ berayun di rantai → kamera mendekat, MIMPI LAMA, catatan kuning NANTI ditempel di kaca, pasir terkuras, kaca makin buram, tahun 2019 → 2026 → **KENAPA BELUM?** |
| 7.3–11.2 | 36 PERTANYAAN: cincin 36 kartu mini berputar 3D, kartu emas **14** maju ke depan lalu dibalik ("Ada mimpi yang udah lama pengen kamu lakuin? Kenapa belum?") + PSIKOLOG ARTHUR ARON · 1997. |
| 11.2–15.4 | JAWABANMU? → tiga balok kaca 3D jatuh dan menumpuk di depan jam pasir: NANTI AJA, BELUM WAKTUNYA, TAKUT GAGAL. Jam pasir bergetar, bintang meredup → **TEMBOK ALASAN**. |
| 15.4–20.2 | Kartu ARSIP RISET 2018 · Davidai & Gilovich · Cornell University · Emotion → **RATUSAN ORANG** + terowongan kartu kaca berisi contoh penyesalan yang melayang mendekati kamera (ilustratif) + APA PENYESALAN TERBESARMU? |
| 20.2–26.8 | HASILNYA? → diagram lingkaran 3D: irisan emas tumbuh jadi **72%** (DIRI IMPIAN), lalu irisan biru **28%** (KEWAJIBAN). |
| 26.8–31.5 | KENAPA? → kartu KEWAJIBAN retak, lalu disapu cahaya dan dicentang (CEPAT DIBERESIN), bergeser ke kiri → jam pasir kecil ditempeli 4 catatan NANTI, pasir terkuras, tahun 2026 → 2031 (DITUNDA TERUS). |
| 31.5–36.6 | MIMPIMU APA?: jam pasir dibalik, bintang mimpi lepas dan naik ke cahaya (sinar) → kolom komentar mengetik "mimpiku " + KIRIM KE TEMANMU. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Ada mimpi yang udah lama pengen kamu lakuin? Kenapa belum?
```
Alternatif: `Penyesalan paling lama bukan soal kesalahan` · `72% penyesalan orang soal ini`

## Caption Instagram
```
Penyesalan yang paling lama nempel, ternyata bukan soal kesalahan 👇

Coba jawab ini: "Ada mimpi yang udah lama pengen kamu lakuin? Kenapa belum?" ✨

Ini pertanyaan nomor 14 dari 36 pertanyaan psikolog Arthur Aron.

Mungkin jawabanmu: nanti aja, belum waktunya, atau takut gagal 😅

Tapi tahun 2018, Thomas Gilovich dan timnya nanya ratusan orang soal penyesalan mereka. Hasilnya? 72% penyesalan itu soal diri impian yang nggak dikejar. Soal kewajiban yang gagal, cuma 28% 😳

Soalnya kewajiban yang gagal biasanya cepat kita beresin. Tapi mimpi? Sering cuma kita tunda.

💬 Kamu sendiri, mimpi apa yang belum kamu kejar? Tulis di komentar!
📩 Kirim ke temanmu yang lagi nunda mimpinya
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Aron dkk. (1997), PSPB; Davidai & Gilovich (2018), Emotion.

#psikologi #faktapsikologi #pertanyaan #mimpi #penyesalan #ruangpikir
```

## Caption TikTok
```
Penyesalan paling lama ternyata bukan soal kesalahan 😶

Riset 2018: 72% penyesalan orang soal diri impian yang nggak dikejar. Soal kewajiban yang gagal cuma 28%.

Mimpi apa yang belum kamu kejar? Tulis di komentar 👇

#psikologi #mimpi #penyesalan #pertanyaan #ruangpikir
```

## Komentar pertama (pin)
```
Aku: pengen belajar gambar dari dulu, tapi selalu "nanti aja" 🥲 Kamu? Tulis mimpimu + alasan kenapa belum. Siapa tahu komentar ini jadi langkah pertamamu 👇
```

## Story promosi
```
Ada mimpi yang udah lama pengen kamu lakuin? Kenapa belum? ✨
Riset: 72% penyesalan orang soal mimpi yang nggak dikejar.
Tonton video barunya 👇
```
Stiker kotak pertanyaan: `Mimpi apa yang belum kamu kejar?`

## Judul YouTube Shorts
```
Penyesalan paling lama bukan soal kesalahan. Ada mimpi yang belum kamu kejar? (riset psikologi) #shorts
```

## Waktu upload
Malam 19.00–21.00 WIB, paling pas Minggu malam atau Senin (momen "mulai minggu baru"). Balas komentar di jam pertama dengan "apa langkah paling kecil yang bisa kamu mulai minggu ini?" supaya diskusinya hidup.

## Produksi
- **Folder:** `video-engine/ep42_mimpi-lama/` (dibangun dari EP41; adegan versi 2 "studio jam pasir" menggantikan versi 1 lab hologram).
- **Render:**
  - Render ulang dengan `./build.sh`; suara sudah ada di `vo/`.
  - Buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`, lalu `tighten.py 0.17`).
  - **Penting:** `vo_full.py` menyimpan anchor ke `vo/lines.json`. Kalau `ANCHORS` di `vo.py` diubah setelah suara dibuat, ubah juga anchor di `vo/lines.json`.
  - `DUR` 42, jeda antarbaris 0,30 dtk, encode CRF 26.
- **Lagu orisinal:** `audio.py` di folder ini (variasi EP22: 100 BPM, `TR = 2`).
- **Versi tanpa musik:**
  1. `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`
  2. Mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm).
- **Helper baru versi 2:**
  - `hourglass3d()` — jam pasir kaca: tutup & tiang emas, pasir atas/bawah + aliran, bintang mimpi, `rot` dibalik, `frost`, angka tahun.
  - `mirror()` — pantulan di lantai studio.
  - `q14_card()` — kartu emas 3D nomor 14 yang dibalik.
  - `card_ring()` — cincin 36 kartu 3D.
  - `glass_block()` — balok kaca 3D alasan.
  - `regret_tunnel()` — terowongan kartu penyesalan.
  - Dipakai juga: `studio()` dari EP35 v2, `pie3d()` dari EP25.
- **Helper versi 1 (masih ada di file):**
  - `ideal_self()` — siluet hologram emas di lantai pada kedalaman z: langkah, bintang di dada.
  - `light_bridge()` — jembatan cahaya perspektif dengan anak tangga bergerak menjauh/mendekat.
  - `dream_capsule()` — kapsul kaca + bintang mimpi; `dim`, `frost` (kaca buram), `lid`.
  - `sticky()` — catatan tempel NANTI.
  - `excuse_slab()` — lempeng kaca 3D yang terbang lalu menghantam.
  - `holo_scale()` — timbangan hologram yang berayun teredam.
  - `duty_icon()` / `duty_card()` — kartu KEWAJIBAN retak lalu disapu cahaya & dicentang.
  - `star5()`.
- **Dipakai juga:** helper lab hologram EP39 v2–EP41 (`holo_bg()`, `holo_bust()`, `holo_text()`, `helix_cards()`, `holo_crowd()` dengan parameter `t0`), `research_card()`, `extrude()`, `ui_panel()`.
