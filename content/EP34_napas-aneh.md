# EP 34 — Lagi panik, kok susah tenang? Coba napas aneh ini

Status: **sudah diproduksi** — `videos/ruang-pikir-ep34-napas-aneh.mp4` (±52 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/napas-aneh/`.
Format: trik psikologi praktis untuk situasi tegang (rumus EP03/EP12) + trik disensor lalu dibuka (rumus EP24).

## Riset
- **Sumber:** Balban, M. Y., Neri, E., Kogon, M. M., Weed, L., Nouriani, B., Jo, B., Holl, G., Zeitzer, J. M., Spiegel, D., & Huberman, A. D. (2023). Brief structured respiration practices enhance mood and reduce physiological arousal. *Cell Reports Medicine, 4*(1), 100895. (Stanford Medicine.)
  - Uji coba acak: sekitar **108–114 orang dewasa sehat** (kebanyakan mahasiswa) latihan **5 menit sehari selama 28 hari**, dibagi 4 kelompok: **cyclic sighing**, **box breathing** (napas kotak), **cyclic hyperventilation** (hiperventilasi terkontrol), dan **mindfulness meditation**.
  - Semua latihan menaikkan mood positif dan menurunkan kecemasan, tapi **latihan napas lebih baik daripada meditasi** dalam menaikkan mood, dan **cyclic sighing paling besar efeknya**. Kelompok cyclic sighing juga punya **laju napas istirahat yang lebih lambat**.
  - Cara cyclic sighing: tarik napas lewat hidung, tambah tarik sekali lagi untuk mengisi penuh paru-paru, lalu buang pelan lewat mulut, kira-kira dua kali lebih panjang dari tarikannya.
- **Jujur soal batasnya:** satu studi dengan sampel kecil dan peserta sehat (pakar lain, mis. Sara Lazar, menyebutnya perlu diuji pada usia kerja dan pasien). Efek utama diukur pada latihan rutin 5 menit/hari, bukan klaim "langsung sembuh dari panik". Penjelasan "buang napas panjang ngasih sinyal ke tubuh buat melambat" adalah mekanisme umum yang disebut peneliti (sistem saraf parasimpatis), bukan hasil yang diukur langsung di studi ini. Batang di video ilustratif tanpa angka. Bukan pengganti penanganan gangguan panik. Tidak ada data Francesca Gino.

## Judul di layar
```
Lagi panik, kok [susah tenang?]
```

## Hook (detik 0–3)
- Suara: **"Lagi panik atau deg-degan? Jangan cuma tarik napas dalam. Coba napas aneh ini."**
- Visual sejak frame pertama: panggung dengan lampu sorot, tokoh kapsul gemetar dan berkeringat, monitor **DETAK JANTUNG** merah yang cepat + alarm, chip **DEG-DEGAN** → gelembung "tarik napas dalam..." dicoret → kartu emas **NAPAS ANEH** buram + gembok (dibuka di detik ±27 video).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Lagi panik atau deg-degan? Jangan cuma tarik napas dalam. Coba napas aneh ini."),
    (4.68, "Tahun dua ribu dua puluh tiga, tim Stanford, termasuk Andrew Huberman, menguji ini."),
    (8.91, "Sekitar seratus orang latihan lima menit sehari, selama sebulan. Ada yang meditasi, ada yang latihan napas."),
    (14.73, "Hasilnya? Yang paling bikin mood naik dan napas lebih tenang, satu cara napas ini. Bahkan ngalahin meditasi."),
    (20.86, "Caranya: tarik napas lewat hidung, tambah tarik sekali lagi, terus buang pelan lewat mulut, lebih panjang."),
    (27.09, "Soalnya buang napas yang panjang ngasih sinyal ke tubuh buat melambat."),
    (31.03, "Coba sekarang: tarik dua kali, buang panjang. Ulangi lima menit."),
    (34.45, "Kirim ke teman yang besok mau presentasi!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–4.7 | **Hook:** panggung, tokoh gemetar, monitor detak merah + DEG-DEGAN, "tarik napas dalam..." dicoret, kartu NAPAS ANEH buram. |
| 4.7–8.9 | Kartu ARSIP RISET 2023 · Balban, Spiegel & Huberman · Stanford Medicine · Cell Reports Medicine + TERMASUK ANDREW HUBERMAN → paru-paru kaca bernapas · UJI COBA ACAK · 28 HARI. |
| 8.9–14.7 | ±100 ORANG · 5 MENIT SEHARI · 28 HARI: grid orang terbelah ke 4 kelompok MEDITASI, NAPAS KOTAK, HIPERVENTILASI, ??? (gembok). |
| 14.7–20.9 | HASILNYA? → batang MOOD NAIK: ??? paling tinggi → jadi NAPAS ANEH + mahkota, NAPAS JADI LEBIH TENANG, NGALAHIN MEDITASI (batang meditasi meredup). |
| 20.9–27.1 | Kartu dibuka: **"Tarik 2x, buang panjang."** (cyclic sighing) + paru-paru terisi 70% (1 · TARIK lewat hidung), penuh (2 · TARIK LAGI), lalu kosong pelan (3 · BUANG PANJANG lewat mulut) + grafik pola napas TARIK – TARIK LAGI – BUANG PANJAAANG. |
| 27.1–31.0 | Monitor detak jantung melambat dari merah ke hijau, SINYAL: MELAMBAT, paru-paru mengempis, tokoh jadi tenang. |
| 31.0–34.5 | Lingkaran panduan napas TARIK → LAGI → BUAAANG, stopwatch + ULANGI 5 MENIT. |
| 34.5–36.6 | Kartu "NAPAS ANEH · 5 MENIT" + KIRIM KE (teman presentasi, sahabat, teman kelas, adik) + TERKIRIM. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Lagi panik? Coba napas aneh ini
```
Alternatif: `Jangan cuma tarik napas dalam` atau `Trik napas 5 menit (riset Stanford)`

## Caption Instagram
```
Lagi panik atau deg-degan? 😰 Jangan cuma tarik napas dalam. Coba napas aneh ini.

Tahun 2023, tim Stanford, termasuk Andrew Huberman, menguji ini. Sekitar 100 orang latihan 5 menit sehari, selama sebulan. Ada yang meditasi, ada yang latihan napas.

Hasilnya? Yang paling bikin mood naik dan napas lebih tenang, satu cara napas ini. Bahkan ngalahin meditasi 🫁

Caranya:
1️⃣ Tarik napas lewat hidung
2️⃣ Tambah tarik sekali lagi
3️⃣ Buang pelan lewat mulut, lebih panjang

Soalnya buang napas yang panjang ngasih sinyal ke tubuh buat melambat 💚

Coba sekarang: tarik 2x, buang panjang. Ulangi 5 menit.

📩 Kirim ke teman yang besok mau presentasi
💬 Kamu paling sering deg-degan pas apa? 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Balban, Spiegel, Huberman dkk. (2023), Cell Reports Medicine.

#psikologi #faktapsikologi #cemas #presentasi #napas #ruangpikir
```

## Caption TikTok
```
Lagi panik? Jangan cuma tarik napas dalam 😰

Riset Stanford (2023): "tarik 2x lewat hidung, buang panjang lewat mulut" 5 menit sehari bikin mood naik, bahkan ngalahin meditasi 🫁💚

Kirim ke teman yang besok presentasi 📩

#psikologi #cemas #presentasi #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Aku coba 5 kali sebelum presentasi: tarik, tarik lagi, buaaang... beneran lebih tenang 😮‍💨 Kamu paling sering deg-degan pas apa? Presentasi, ujian, atau ketemu gebetan? 👇
```

## Story promosi
```
Deg-degan sebelum presentasi atau ujian? 😰
Kata riset Stanford, coba napas aneh ini 5 menit.
Tonton video barunya 👇
```
Stiker polling: `Kamu paling sering deg-degan pas... presentasi 🎤 / ujian 📝`

## Judul YouTube Shorts
```
Lagi panik? Coba napas aneh ini, kata riset Stanford (cyclic sighing) #shorts
```

## Waktu upload
Minggu–Kamis malam 19.00–21.00 WIB (malam sebelum ujian/presentasi), atau pagi 06.00–07.30 sebelum sekolah/kerja.

## Produksi
Folder `video-engine/ep34_napas-aneh/` (dibangun dari EP33): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`). `DUR` 42, jeda antarbaris 0.35 dtk. Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 88 BPM, `TR = -1`). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper baru: `lungs()`, `breath_pattern()`, `breath_graph()`, `breath_circle()`; plus `stage()`, `monitor()`, `vbar()`, `crown()`, `secret_card2()`, `stopwatch()`, `mini_person()`, `padlock()`, `research_card()`, `extrude()`, `say()`, `avatar()`, `plane_icon()`.
