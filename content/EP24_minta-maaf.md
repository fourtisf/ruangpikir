# EP 24 — Minta maaf, kok nggak dimaafin?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep24-minta-maaf.mp4` (±55 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/minta-maaf/`.
Seri: Psikologi Ngobrol (format EP14 "coba dua kata ini": dua tokoh kapsul di kafe malam + kalimat konkret yang tampil besar).

## Riset
- **Sumber:** Lewicki, R. J., Polin, B., & Lount, R. B., Jr. (2016). An exploration of the structure of effective apologies. *Negotiation and Conflict Management Research, 9*(2), 177–196.
  - Dua studi, total **755 peserta**, menilai permintaan maaf yang berisi 1 sampai 6 unsur: menyatakan penyesalan, menjelaskan apa yang terjadi, **mengakui tanggung jawab**, berjanji tidak mengulang, **menawarkan perbaikan**, dan **meminta dimaafkan**.
  - Paling berpengaruh: mengakui tanggung jawab; kedua: menawarkan perbaikan; tiga unsur berikutnya kurang lebih setara; **paling lemah: meminta dimaafkan**.
  - Makin banyak unsur, makin baik permintaan maaf dinilai. Kalau hanya bisa satu kalimat, menurut penelitinya, akui tanggung jawab.
- **Jujur soal batasnya:** peserta membaca permintaan maaf tertulis dalam skenario (konteks kerja), bukan pertengkaran sungguhan; nada suara dan bahasa tubuh tidak diuji. Batang peringkat di video ilustratif, tanpa angka. Tidak ada data Francesca Gino.

## Judul di layar
```
Minta maaf, [kok nggak dimaafin]?
```

## Hook (detik 0–4)
- Suara: **"Udah minta maaf, kok nggak dimaafin? Jangan cuma bilang, maafin aku ya. Coba dua kalimat ini."** Masalah yang dialami hampir semua orang + larangan yang mengejutkan + janji jawaban konkret.
- Visual sejak frame pertama: kafe malam, dua tokoh kapsul, **hati kaca pink yang langsung retak dan terbelah dua** (kilat + bunyi kaca). Gelembung "maafin aku ya" melayang ke hati lalu mental, temannya diam "...", chip **BELUM DIMAAFIN**, lalu gelembung itu dicoret.
- **Kunci retensi:** di detik ±5 muncul **dua kartu emas "KALIMAT 1" dan "KALIMAT 2" yang tulisannya disensor buram + bergembok**. Penonton harus menonton sampai detik ±27 dan ±31 untuk melihat isinya.
- **Lagu:** variasi lagu EP22 yang lebih hangat (orisinal), mulai dari frame pertama.

## Lagu (orisinal, bebas hak cipta)
Dibuat di `video-engine/ep24_minta-maaf/audio.py` (`music()`, turunan EP22): 92 BPM, `TR = -2` (turun 2 semitone, lebih hangat), e-piano Fmaj7–G6–Em7–Am7, bass, kick/clap/hi-hat swing, melodi pentatonik, chime; volume musik otomatis turun saat narasi.
- Kalau mau memakai **lagu trending TikTok/IG**, pakai **`videos/ruang-pikir-ep24-minta-maaf-tanpa-musik.mp4`** (narasi + efek suara saja) supaya dua lagu tidak bertabrakan. Tambahkan lagunya lewat fitur musik di aplikasi: **suara asli 100%**, **lagu ±10–15%**. Pilih lagu yang hangat/akustik (nuansa baikan). Jangan menempelkan lagu berhak cipta ke file video.

## Gaya visual
"Hati kaca retak + kintsugi emas": hati kaca berisi cairan yang retak, terbelah, lalu membeku biru saat suasana dingin (termometer SUASANA turun ke DINGIN, kristal es di sudut layar); gelembung "maaf ya / sorry... / maaf maaf" yang ditumpuk buru-buru; kartu ARSIP RISET 2016; **6 keping puzzle kaca 3D** (unsur maaf + contoh kalimat) yang saling mengunci; keping berputar dalam lingkaran 3D lalu **AKUI SALAH** maju jadi #1 dengan sinar emas; kartu KALIMAT 1 yang gemboknya terbuka: **"Itu salahku."**; NOMOR 2 + keping TAWARKAN PERBAIKAN; saat "Aku perbaiki, ya." kedua belahan hati menyatu dan retakannya **diisi emas (kintsugi)**; batang peringkat dengan MINTA DIMAAFKAN "PALING LEMAH" + gelembung "maafin aku ya" yang kempes; puzzle lengkap = DIHARGAI penuh; tinggal 2 keping "PAKAI YANG INI"; kartu "COBA SEKARANG" diketik + panel **KIRIM KE** dengan pesawat kertas dan "TERKIRIM". Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Udah minta maaf, kok nggak dimaafin? Jangan cuma bilang, maafin aku ya. Coba dua kalimat ini."),
    (4.94, "Kita sering minta maaf buru-buru, biar cepat selesai. Tapi dia masih diam, dan suasananya tetap dingin."),
    (10.07, "Tahun dua ribu enam belas, Roy Lewiki dan timnya menguji enam unsur permintaan maaf ke lebih dari tujuh ratus orang."),
    (16.26, "Hasilnya? Unsur paling ampuh: mengakui kesalahan. Bilang: itu salahku."),
    (21.08, "Nomor dua: tawarkan perbaikan. Bilang: aku perbaiki, ya."),
    (24.37, "Yang paling lemah justru minta dimaafkan, alias, maafin aku ya."),
    (27.99, "Makin lengkap permintaan maafnya, makin dihargai. Tapi kalau cuma sempat dua kalimat, pakai yang ini."),
    (32.58, "Itu salahku. Aku perbaiki, ya. Kirim video ini ke orang yang mau kamu mintain maaf!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Roy Lewiki" = ejaan fonetik Roy Lewicki untuk TTS (caption tetap "Roy Lewicki"). Suara dirapatkan dengan `tighten.py 0.21` supaya video ≤ 55 detik.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–4.9 | **Hook:** kafe, hati kaca retak & terbelah, "maafin aku ya" mental + dicoret, "...", BELUM DIMAAFIN, dua kartu KALIMAT 1 & 2 buram bergembok. |
| 4.9–10.1 | Gelembung maaf beruntun + BURU-BURU, teman diam "...", termometer SUASANA → DINGIN, hati membeku, kristal es. |
| 10.1–16.3 | Kartu ARSIP RISET 2016 · Lewicki, Polin & Lount · NCMR, chip 6 UNSUR MAAF + 755 PESERTA, 6 keping puzzle keluar dari kartu. |
| 16.3–21.1 | Keping berputar 3D → AKUI SALAH #1 "PALING AMPUH" + sinar emas → kartu KALIMAT 1 terbuka: "Itu salahku." |
| 21.1–24.4 | NOMOR 2 → keping TAWARKAN PERBAIKAN #2, "Aku perbaiki, ya." → hati menyatu + kintsugi emas, teman tersenyum. |
| 24.4–28.0 | Batang SEBERAPA AMPUH? → MINTA DIMAAFKAN "PALING LEMAH", gelembung "maafin aku ya" kempes. |
| 28.0–32.6 | Puzzle 6 keping mengunci, meteran DIHARGAI penuh → "CUMA SEMPAT 2 KALIMAT?" → dua keping emas/mint "PAKAI YANG INI". |
| 32.6–36.6 | Kartu "COBA SEKARANG" diketik: "Itu salahku. / Aku perbaiki, ya." + panel KIRIM KE (sahabat, pasangan, kakak, teman kantor) + TERKIRIM, hati kintsugi bersinar. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Minta maaf, kok nggak dimaafin?
```
Alternatif: `Jangan cuma bilang "maafin aku ya"` atau `2 kalimat biar maafmu diterima`

## Caption Instagram
```
Udah minta maaf, kok nggak dimaafin? 💔 Jangan cuma bilang "maafin aku ya". Coba dua kalimat ini.

Kita sering minta maaf buru-buru, biar cepat selesai. Tapi dia masih diam, dan suasananya tetap dingin 🥶

Tahun 2016, Roy Lewicki dan timnya dari Ohio State University menguji 6 unsur permintaan maaf ke 755 orang.

Hasilnya?
1️⃣ Paling ampuh: mengakui kesalahan → "Itu salahku."
2️⃣ Nomor dua: tawarkan perbaikan → "Aku perbaiki, ya."
Yang paling lemah justru minta dimaafkan, alias "maafin aku ya" 😶

Makin lengkap permintaan maafnya, makin dihargai. Tapi kalau cuma sempat dua kalimat, pakai yang ini 🤍

📩 Kirim video ini ke orang yang mau kamu mintain maaf.
💬 Kamu paling susah minta maaf ke siapa? Cerita di komentar 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Lewicki, Polin & Lount (2016), Negotiation and Conflict Management Research. Yang diuji permintaan maaf tertulis, jadi tetap ucapkan dengan tulus ya.

#psikologi #faktapsikologi #mintamaaf #hubungan #pertemanan #ruangpikir
```

## Caption TikTok
```
Udah minta maaf, kok nggak dimaafin? 💔 Jangan cuma bilang "maafin aku ya".

Riset Lewicki dkk. (2016, 755 orang): paling ampuh "Itu salahku." + "Aku perbaiki, ya." Yang paling lemah justru minta dimaafkan.

Kirim ke orang yang mau kamu mintain maaf 📩

#psikologi #mintamaaf #hubungan #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Template biar gampang: "Itu salahku. Aku perbaiki, ya." 🤍 Kamu paling susah minta maaf ke siapa? Sahabat, pasangan, atau orang tua? 👇
```

## Story promosi
```
Udah minta maaf, tapi masih didiemin? 💔
Coba dua kalimat ini. Ada risetnya.
Tonton video barunya 👇
```
Stiker polling: `Paling susah minta maaf ke... sahabat / pasangan / orang tua`

## Judul YouTube Shorts
```
Minta maaf tapi nggak dimaafin? Coba 2 kalimat ini kata riset psikologi #shorts
```

## Waktu upload
Malam 19.00–21.00 WIB (jam orang chat-an dan baikan), paling bagus Jumat/Sabtu malam.

## Produksi
Folder `video-engine/ep24_minta-maaf/` (dibangun dari EP23): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01, lalu `python3 tighten.py 0.21`). Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 92 BPM, `TR = -2`). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper baru: `crack_heart()`, `piece()`/`piece_path()`, `secret_card()`, `thermo()`, `frost()`, `plane_icon()`; plus helper EP14–EP23 (`cafe_bg()`, `table()`, `hero()`, `say()`, `thought()`, `race_bar()`, `extrude()`, `research_card()`, `ring_pos()`, `rays()`, `padlock()`, `avatar()`).
