# EP 38 — Habis berantem, kok susah baikan?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep38-boleh-peluk.mp4` (±50 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/boleh-peluk/`.
Format: rumus EP24 (konflik hubungan sehari-hari + "Jangan cuma [kebiasaan umum]. Coba satu hal kecil ini" + kalimat disensor lalu dibuka + "kirim ke orang yang mau kamu …"). Visual **UI/UX premium** (permintaan ALFA): panel kaca gaya aplikasi, saklar, segmented control, ring progres, grafik garis, dialog izin.

## Riset
- **Sumber:** Murphy, M. L. M., Janicki-Deverts, D., & Cohen, S. (2018). Receiving a hug is associated with the attenuation of negative mood that occurs on days with interpersonal conflict. *PLOS ONE, 13*(10), e0203522. (Carnegie Mellon University.)
  - **404 orang dewasa sehat** diwawancarai lewat telepon **setiap malam selama 14 hari berturut-turut** tentang:
    - konflik dengan orang lain hari itu;
    - apakah mereka dipeluk;
    - perasaan positif dan negatif.
  - Di hari yang ada konfliknya, yang **dipeluk** mengalami penurunan perasaan positif dan kenaikan perasaan negatif yang **lebih kecil**.
  - Pelukan juga terkait dengan kenaikan perasaan negatif **keesokan harinya** yang lebih kecil (tidak untuk perasaan positif keesokan harinya).
  - Tidak ada beda antara perempuan dan laki-laki.
- **Jujur soal batasnya:**
  - Studi ini **korelasional**: belum membuktikan pelukan yang menyebabkan mood lebih baik.
  - Murphy bilang risetnya masih tahap awal.
  - Pelukan yang tidak diinginkan belum tentu membantu, makanya kalimatnya "Boleh peluk nggak?"
  - "Peneliti menduga pelukan jadi tanda dukungan" adalah dugaan penulis, bukan hasil yang diukur.
- **Ilustratif:** ring mood, grafik garis, timer, dan isi kartu survei. Tidak ada data Francesca Gino.

## Judul di layar
```
Habis berantem, kok [susah baikan?]
```

## Hook (detik 0–3)
- Suara: **"Habis berantem, kalian diem-dieman? Jangan cuma nunggu marahnya reda. Coba satu hal kecil ini."**
- Visual sejak frame pertama:
  - widget kaca gaya *live activity* **Diem-dieman** "belum ada yang ngechat duluan" + timer jam yang berjalan;
  - dua tokoh berjauhan, awan petir di tengah, retakan merah di lantai;
  - loader **NUNGGU MARAH REDA...** berputar lalu dicoret;
  - kartu emas **SATU HAL KECIL** buram + gembok (dibuka di detik ±41 video).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Habis berantem, kalian diem-dieman? Jangan cuma nunggu marahnya reda. Coba satu hal kecil ini."),
    (5.37, "Tahun dua ribu delapan belas, peneliti Michael Murphy dan timnya menelepon empat ratus empat orang, tiap malam."),
    (11.56, "Selama dua minggu, mereka ditanya: hari ini berantem nggak? Dan hari ini dipeluk nggak?"),
    (16.25, "Hasilnya? Di hari ada konflik, yang dipeluk moodnya nggak anjlok separah yang nggak dipeluk."),
    (21.02, "Bahkan besoknya, perasaan negatifnya juga lebih rendah."),
    (24.64, "Peneliti menduga, pelukan jadi tanda dukungan: kita masih aman, kita masih baik-baik aja."),
    (29.92, "Tapi pelukannya harus mau sama mau. Jadi coba tanya dulu: boleh peluk nggak?"),
    (34.45, "Kirim video ini ke orang yang mau kamu peluk!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–5.4 | **Hook:** widget Diem-dieman + timer, dua tokoh berjauhan, awan petir, retakan lantai, loader NUNGGU MARAH REDA... dicoret, kartu SATU HAL KECIL buram. |
| 5.4–11.6 | Kartu ARSIP RISET 2018 · Murphy, Janicki-Deverts & Cohen · Carnegie Mellon University · PLOS ONE. Ponsel 3D dengan panggilan masuk "Tim Peneliti · Survei malam · 21.00" diangkat (ketukan jari + riak), kartu PESERTA 0→404 orang dewasa, kartu TIAP MALAM 21.00 selama 14 hari. |
| 11.6–16.3 | Panel SURVEI MALAM hari 1→14 (ikon petir = konflik, hati = dipeluk). Kartu "Hari ini ada konflik?" dengan segmented YA/TIDAK → YA. Kartu "Hari ini dipeluk?" dengan saklar menyala. Kartu "Mood malam ini?" dengan 5 wajah. |
| 16.3–21.0 | HASILNYA? → dasbor MOOD DI HARI ADA KONFLIK: dua ring progres, NGGAK DIPELUK anjlok (wajah sedih, ANJLOK) vs DIPELUK turun sedikit (TURUN SEDIKIT). |
| 21.0–24.6 | Grafik garis PERASAAN NEGATIF (SEBELUM → KONFLIK → MALAM → BESOK): garis dipeluk lebih rendah sampai besok, BESOKNYA LEBIH RINGAN. |
| 24.6–29.9 | Dua tokoh saling mendekat lalu berpelukan dengan pendar hangat + hati. Panel PENELITI MENDUGA · Sinyal dukungan: ✓ Kita masih aman, ✓ Kita masih baik-baik aja. |
| 29.9–34.5 | Dialog izin gaya sistem "Pelukan? harus mau sama mau" [Nanti dulu | Boleh]. Kartu dibuka dengan sinar: **"Boleh peluk nggak?"**, tombol Boleh diketuk, dua tokoh mulai mendekat. |
| 34.5–36.6 | Kartu SIMPAN KALIMAT INI + KIRIM KE (pacar, sahabat, ibu, ayah) + TERKIRIM, dua tokoh berpelukan. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Habis berantem? Jangan cuma diem-dieman
```
Alternatif: `Satu hal kecil setelah berantem` atau `Boleh peluk nggak? (kata riset)`

## Caption Instagram
```
Habis berantem, kalian diem-dieman? 😶 Jangan cuma nunggu marahnya reda. Coba satu hal kecil ini.

Tahun 2018, peneliti Michael Murphy dan timnya (Carnegie Mellon) menelepon 404 orang, tiap malam. Selama dua minggu, mereka ditanya: hari ini berantem nggak? Dan hari ini dipeluk nggak?

Hasilnya? Di hari ada konflik, yang dipeluk moodnya nggak anjlok separah yang nggak dipeluk. Bahkan besoknya, perasaan negatifnya juga lebih rendah 🫂

Peneliti menduga, pelukan jadi tanda dukungan: kita masih aman, kita masih baik-baik aja.

Tapi pelukannya harus mau sama mau. Jadi coba tanya dulu: "Boleh peluk nggak?" 🤍

📩 Kirim ke orang yang mau kamu peluk
💬 Kamu tim langsung peluk atau tim diem dulu? 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Murphy, Janicki-Deverts & Cohen (2018), PLOS ONE.

#psikologi #faktapsikologi #hubungan #pacaran #berantem #ruangpikir
```

## Caption TikTok
```
Habis berantem, jangan cuma diem-dieman 😶

Riset Carnegie Mellon (2018, 404 orang): di hari ada konflik, yang dipeluk moodnya nggak anjlok separah yang nggak dipeluk, bahkan sampai besoknya. Tapi tanya dulu: "Boleh peluk nggak?" 🫂

Kirim ke orang yang mau kamu peluk 📩

#psikologi #hubungan #pacaran #berantem #ruangpikir
```

## Komentar pertama (pin)
```
Jujur, habis berantem kamu tim "langsung peluk" atau tim "diem dulu 3 hari"? 😭 Tag orang yang mau kamu peluk sekarang 👇
```

## Story promosi
```
Habis berantem, kalian diem-dieman? 😶
Kata riset, coba satu hal kecil ini.
Tonton video barunya 👇
```
Stiker polling: `Habis berantem kamu... langsung peluk 🫂 / diem dulu 😶`

## Judul YouTube Shorts
```
Habis berantem, kok susah baikan? Coba satu hal kecil ini (riset Carnegie Mellon 2018) #shorts
```

## Waktu upload
Malam 19.00–21.00 WIB, paling pas Kamis–Minggu.

## Produksi
- **Folder:** `video-engine/ep38_peluk/` (dibangun dari EP37).
- **Render:**
  - Render ulang dengan `./build.sh`; suara sudah ada di `vo/`.
  - Buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`).
  - `DUR` 42, jeda antarbaris 0.35 dtk, encode CRF 26.
- **Lagu orisinal:** `audio.py` di folder ini (variasi EP22: 92 BPM, `TR = 2`).
- **Versi tanpa musik:**
  1. `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`
  2. Mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14).
- **Helper baru (sistem UI/UX premium):**
  - `ui_panel()` — panel kaca gaya aplikasi: bayangan, kilau, tepi bergradasi.
  - `ui_text()`.
  - `ui_toggle()` — saklar iOS.
  - `ui_seg()` — segmented control.
  - `ui_ring()` — ring progres dengan gradasi melingkar.
  - `mood_face()` — ikon wajah garis.
  - `ui_chart()` — grafik garis halus + area gradasi + grid.
  - `ui_phone()` — ponsel 3D + dynamic island, layar lewat callback.
  - `call_screen()` — layar panggilan masuk.
  - `tap()` — ketukan jari + riak.
  - `ui_dialog()` — dialog izin gaya sistem.
  - `bolt()` — petir.
  - `hug_pair()` — dua tokoh kapsul saling mendekat lalu berpelukan.
- **Dipakai juga:** `studio()`, `rain_cloud()`, `hero()`, `secret_card2()`, `research_card()`, `extrude()`, `check_mark()`, `heart_shape()`, `mini_person()`, `avatar()`, `plane_icon()`.
