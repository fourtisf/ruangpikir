# EP 23 — Habis nongkrong, kok capek?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep23-baterai-sosial.mp4` (±50 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/baterai-sosial/`.
Seri: perasaan "kok aku gini?" + riset yang bikin lega (format EP04/EP11), dengan tokoh kapsul + kafe malam dari seri Psikologi Ngobrol.

## Riset
- **Sumber:** Leikas, S., & Ilmarinen, V.-J. (2017). Happy now, tired later? Extraverted and conscientious behavior are related to immediate mood gains, but to later fatigue. *Journal of Personality, 85*(5), 603–615.
  - Studi pengalaman (experience sampling): **48 peserta** di Helsinki mencatat perilaku, suasana hati, dan rasa lelah **lima kali sehari selama dua belas hari**.
  - Saat sedang berperilaku ekstrover (aktif bersosialisasi), suasana hati naik dan rasa lelah justru lebih rendah; **sekitar tiga jam kemudian** rasa lelah meningkat.
  - Kelelahan lebih terasa saat bersama lebih banyak orang, dan pola ini tidak bergantung pada skor ekstraversi (jadi bukan cuma introvert).
- **Jujur soal batasnya:** efeknya kecil, sampelnya kecil (48 orang, Finlandia), dan penelitinya sendiri menyarankan replikasi. Video tidak memakai angka persen selain baterai ilustratif, dan menyebut "bahkan buat yang ekstrovert" (sesuai temuan bahwa efeknya tidak bergantung pada kepribadian). "Baterai sosial" adalah istilah populer, bukan istilah teknis dari studi. Tidak ada data Francesca Gino.

## Judul di layar
```
Habis nongkrong, [kok capek]?
```

## Hook (detik 0–3)
- Suara: **"Habis nongkrong seru, kok langsung capek banget? Tenang, kamu nggak aneh."** Pengalaman yang dialami hampir semua orang + kalimat yang langsung bikin lega.
- Visual sejak frame pertama: tokoh kapsul ceria di tengah teman-temannya, **baterai kaca 3D** di atas kepala langsung terkuras 100% → 5% (warna hijau → kuning → merah, kedip), chip merah **"BATERAI SOSIAL LEMAH"**, tokoh lemas berkeringat; di "Tenang" (detik ±3) tokoh jadi tenang, cincin mint, chip **"WAJAR KOK"**.
- **Lagu:** variasi lagu EP22 (orisinal), naik 2 nada dan lebih cepat (100 BPM), mulai dari frame pertama.

## Lagu (orisinal, bebas hak cipta)
Dibuat di `video-engine/ep23_baterai-sosial/audio.py` (`music()`, turunan EP22): 100 BPM, `TR = 2` (naik 2 semitone), e-piano Fmaj7–G6–Em7–Am7 sinkop, bass, kick/clap/hi-hat swing, melodi pentatonik catchy, chime; volume musik otomatis turun saat narasi.
- Kalau mau memakai **lagu trending TikTok/IG**, pakai **`videos/ruang-pikir-ep23-baterai-sosial-tanpa-musik.mp4`** (narasi + efek suara saja) supaya dua lagu tidak bertabrakan. Tambahkan lagunya lewat fitur musik di aplikasi: **suara asli 100%**, **lagu ±10–15%**. Pilih lagu yang santai/ceria (nuansa "pulang nongkrong, rebahan"). Jangan menempelkan lagu berhak cipta ke file video.

## Gaya visual
"Baterai sosial 3D": baterai kaca 3D (`battery3d()`: isi hijau→kuning→merah bersegmen, persen, petir saat dicas, kedip saat lemah), kartu ketawa/ngobrol/foto-foto yang beterbangan lalu berganti kasur "mode rebahan", kartu ARSIP RISET 2017 + kalender 12 hari × 5 titik, kafe malam dengan tiga tokoh + batang MOOD naik / CAPEK tetap rendah ("nggak kerasa capek"), jam besar "+3 JAM" dengan baterai yang terkuras, kerumunan tokoh "N ORANG DITEMUI" + "BAHKAN YANG EKSTROVERT", stempel WAJAR + "ENERGI ≠ SAYANG TEMAN" (baterai vs hati kaca), baterai yang dicas "NGECAS" + teks 3D "BERAPA JAM?" + komentar. Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Habis nongkrong seru, kok langsung capek banget? Tenang, kamu nggak aneh."),
    (4.15, "Ketawa, ngobrol, foto-foto. Seru! Tapi sampai rumah, rasanya pengen rebahan seharian."),
    (8.81, "Tahun dua ribu tujuh belas, psikolog Sointu Leikas dari Helsinki melacak ini, lima kali sehari selama dua belas hari."),
    (15.22, "Saat lagi aktif bersosialisasi, mood mereka naik, dan nggak kerasa capek."),
    (19.22, "Tapi sekitar tiga jam kemudian, rasa lelahnya baru datang."),
    (22.4, "Makin banyak orang yang ditemui, makin terasa capeknya. Bahkan buat yang ekstrovert."),
    (27.01, "Jadi capek habis nongkrong itu wajar. Bukan berarti kamu nggak suka temanmu."),
    (31.17, "Kasih waktu buat ngecas sendiri dulu. Baterai sosialmu habis setelah berapa jam? Tulis di komentar!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–4.2 | **Hook:** tokoh ceria + teman, baterai 3D terkuras 100% → 5%, "BATERAI SOSIAL LEMAH" → tokoh tenang + "WAJAR KOK". |
| 4.2–8.8 | Kartu "ketawa", "ngobrol", "foto-foto" + tokoh excited → sampai rumah: kasur, baterai 8% berkedip, "mode rebahan". |
| 8.8–15.2 | Kartu ARSIP RISET 2017 · Leikas & Ilmarinen · J PERS + kalender 12 hari × 5 catatan "5x SEHARI · 12 HARI". |
| 15.2–19.2 | Kafe malam, tiga tokoh ngobrol; batang MOOD naik, CAPEK tetap rendah, chip "nggak kerasa capek". |
| 19.2–22.4 | Jam besar "+3 JAM", baterai turun 75% → 10%, batang CAPEK naik, tokoh lemas. |
| 22.4–27.0 | Kerumunan tokoh bertambah "N ORANG DITEMUI", tokoh makin capek + "BAHKAN YANG EKSTROVERT". |
| 27.0–31.2 | Stempel WAJAR + baterai ENERGI 12% ≠ hati kaca SAYANG TEMAN penuh. |
| 31.2–36.6 | Baterai dicas (petir) "NGECAS" + teks 3D "BERAPA JAM?" + komentar "2 jam max", "1 jam udah habis", "kuat seharian wkwk", "tergantung orangnya". |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow (lagu mengalun penuh). |

## Teks cover Reels
```
Habis nongkrong, kok capek?
```
Alternatif: `Baterai sosialmu habis? Wajar kok` atau `Capek habis nongkrong bukan berarti nggak suka temanmu`

## Caption Instagram
```
Habis nongkrong seru, kok langsung capek banget? 🪫 Tenang, kamu nggak aneh.

Ketawa, ngobrol, foto-foto. Seru! Tapi sampai rumah, rasanya pengen rebahan seharian 😮‍💨

Tahun 2017, psikolog Sointu Leikas dan Ville-Juhani Ilmarinen dari Helsinki melacak ini: 48 orang mencatat mood dan rasa lelahnya lima kali sehari selama dua belas hari.

Saat lagi aktif bersosialisasi, mood mereka naik dan nggak kerasa capek. Tapi sekitar tiga jam kemudian, rasa lelahnya baru datang. Makin banyak orang yang ditemui, makin terasa capeknya. Bahkan buat yang ekstrovert.

Jadi capek habis nongkrong itu wajar. Bukan berarti kamu nggak suka temanmu 🤍 Kasih waktu buat ngecas sendiri dulu 🔋

💬 Baterai sosialmu habis setelah berapa jam? Tulis di komentar 👇
📩 Kirim ke teman yang selalu langsung rebahan habis nongkrong.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Leikas & Ilmarinen (2017), Journal of Personality. Studinya kecil (48 orang), jadi anggap ini gambaran awal ya.

#psikologi #faktapsikologi #bateraisosial #introvert #nongkrong #ruangpikir
```

## Caption TikTok
```
Habis nongkrong seru, kok langsung capek? 🪫 Kamu nggak aneh.

Riset Leikas & Ilmarinen (2017): saat nongkrong mood naik, tapi ±3 jam kemudian capeknya baru datang. Makin banyak orang, makin capek, bahkan buat yang ekstrovert.

Baterai sosialmu habis setelah berapa jam? 👇

#psikologi #bateraisosial #introvert #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Aku duluan: baterai sosialku habis setelah ±3 jam, habis itu wajib rebahan sambil scroll 😂🔋 Kamu berapa jam? 👇
```

## Story promosi
```
Habis nongkrong, langsung pengen rebahan seharian? 🪫
Tenang, itu wajar. Ada risetnya.
Tonton video barunya 👇
```
Stiker kuis/polling: `Baterai sosialmu habis setelah... 1 jam / 3 jam / seharian kuat`

## Judul YouTube Shorts
```
Habis nongkrong kok capek banget? Ini kata riset psikologi #shorts
```

## Waktu upload
Kamis/Jumat malam 19.00–21.00 WIB, atau Minggu sore (orang baru pulang nongkrong akhir pekan, paling relate).

## Produksi
Folder `video-engine/ep23_baterai-sosial/` (dibangun dari EP22): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`). Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 100 BPM, `TR = 2`). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper baru: `battery3d()`, `bat_col()`, `fun_card()`, `bed()`, `big_clock()`; plus helper EP14–EP22 (`cafe_bg()`, `hero()`, `glass_heart()`, `race_bar()`, `stamp()`, `extrude()`, `comment()`, `research_card()`).
