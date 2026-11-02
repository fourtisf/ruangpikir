# EP 17 — Baru kenal, kok langsung akrab?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep17-cepat-akrab.mp4` (±47 detik, 1080×1920), halaman web `ruangpikir.id/episode/cepat-akrab/`.
Seri: Trik Psikologi · Rumus hook EP14 (episode paling cepat viral): "Mau [hasil]? Coba [satu/dua] [kata/pertanyaan] ini."

## Riset
- **Sumber utama:** Aron, A., Melinat, E., Aron, E. N., Vallone, R. D., & Bator, R. J. (1997). The experimental generation of interpersonal closeness: A procedure and some preliminary findings. *Personality and Social Psychology Bulletin, 23*(4), 363–377.
  - Pasangan mahasiswa yang belum saling kenal bergantian menjawab 36 pertanyaan dalam tiga set yang makin lama makin pribadi, total ±45 menit. Pasangan pembanding saling bertanya 36 pertanyaan ringan (basa-basi). Kelompok 36 pertanyaan merasa lebih dekat.
  - Pertanyaan pertama: "Given the choice of anyone in the world, whom would you want as a dinner guest?"
  - Kuncinya: keterbukaan diri yang meningkat bertahap, berkelanjutan, dan timbal balik (gantian).
- **Jujur soal batasnya:** yang diukur rasa dekat setelah satu sesi di laboratorium, bukan hubungan jangka panjang. Klaim populer "36 pertanyaan bikin jatuh cinta" tidak dipakai di video. Tetap perhatikan kenyamanan lawan bicara.

## Judul di layar
```
Baru kenal, [kok langsung akrab]?
```

## Hook (detik 0–3)
- Suara: **"Mau cepat akrab sama orang baru? Coba satu pertanyaan ini."** Rumus EP14 yang paling cepat viral (722 suka, 165 kirim dalam sehari): keinginan sosial yang umum + janji satu hal kecil yang bisa langsung dicoba. Pertanyaannya langsung dibuka di detik ±4: **"Kalau bisa makan malam bareng siapa aja di dunia, kamu pilih siapa?"**
- Visual sejak frame pertama: dua tokoh kapsul canggung di meja kafe malam, chip "krik...", meter **DEKAT** berkedip hampir nol; di "Coba satu pertanyaan ini" kartu emas 3D bertanda **"?"** jatuh berputar dengan sinar emas (detik ±3), lalu dibalik dan pertanyaannya terbaca.

## Gaya visual
"Kafe malam + kartu pertanyaan 3D" (dibangun dari EP14): kartu emas 3D (muka pertanyaan, belakang "?"), kipas 36 kartu bernomor dengan warna ringan→pribadi + angka 3D "36", kartu yang bolak-balik di antara dua tokoh + bar RINGAN→PRIBADI + timer 45:00, BASA-BASI vs 36 PERTANYAAN dengan meter DEKAT, lapisan diri (cangkang kaca) yang terbuka gantian + "GANTIAN", gelembung "hujan ya hari ini?" dicoret vs "aku dulu takut naik eskalator" emas, teks 3D "KAMU PILIH SIAPA?" + kolom komentar. Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Mau cepat akrab sama orang baru? Coba satu pertanyaan ini."),
    (3.32, "Kalau bisa makan malam bareng siapa aja di dunia, kamu pilih siapa?"),
    (6.98, "Ini pertanyaan pertama dari tiga puluh enam pertanyaan buatan psikolog Arthur Aron, tahun sembilan belas sembilan puluh tujuh."),
    (13.87, "Dua orang asing saling bertanya, dari yang ringan sampai yang makin pribadi, selama empat puluh lima menit."),
    (19.71, "Hasilnya? Mereka merasa lebih dekat, dibanding yang cuma ngobrol basa-basi."),
    (23.81, "Kuncinya: saling terbuka sedikit demi sedikit, dan gantian."),
    (27.04, "Basa-basi soal cuaca nggak bikin dekat. Cerita kecil tentang dirimu, iya."),
    (31.03, "Jadi lain kali kenalan, coba tanya itu. Kamu sendiri, pilih makan malam sama siapa? Tulis di komentar!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–3.3 | **Hook:** kafe malam, dua tokoh canggung, "krik...", meter DEKAT ±0 → kartu emas "?" jatuh berputar + sinar. |
| 3.3–7.0 | Kartu dibalik dan membesar: "PERTANYAAN 01 / 36 — Kalau bisa makan malam bareng siapa aja di dunia, kamu pilih siapa?"; "kamu pilih siapa?" menyala emas; meter DEKAT naik. |
| 7.0–13.9 | Kipas 36 kartu bernomor (ringan→pribadi), angka 3D "36 PERTANYAAN" → kartu ARSIP RISET 1997 · Arthur Aron dkk. · PSPB. |
| 13.9–19.7 | Kartu bolak-balik di antara dua tokoh, warnanya makin hangat; bar RINGAN→PRIBADI; timer 45:00. |
| 19.7–23.8 | BASA-BASI ("kuliah di mana?", "hujan ya?", "udah makan?") vs 36 PERTANYAAN ("kamu pilih siapa?", "momen paling syukur?", "mimpi terbesarmu?"); meter DEKAT + hati. |
| 23.8–27.0 | Lapisan diri (cangkang kaca) terbuka sedikit demi sedikit, gantian kiri-kanan; chip "GANTIAN". |
| 27.0–31.0 | "hujan ya hari ini?" dicoret ("nggak bikin dekat") vs "aku dulu takut naik eskalator" emas + ✓ + hati. |
| 31.0–36.6 | Kafe: kartu pertanyaan, teks 3D "KAMU PILIH SIAPA?", komentar "almarhum kakekku", "BJ Habibie", "aku 10 tahun lagi", "Raisa dong"; meter DEKAT penuh. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
1 pertanyaan biar cepat akrab
```
Alternatif: `Ganti basa-basi dengan ini` atau `Tanya ini ke orang baru`

## Caption Instagram
```
Mau cepat akrab sama orang baru? Coba satu pertanyaan ini 👇

"Kalau bisa makan malam bareng siapa aja di dunia, kamu pilih siapa?" 🍽️

Ini pertanyaan pertama dari 36 pertanyaan buatan psikolog Arthur Aron (1997). Dua orang asing saling bertanya, dari yang ringan sampai yang makin pribadi, selama 45 menit. Hasilnya? Mereka merasa lebih dekat dibanding yang cuma ngobrol basa-basi.

Kuncinya: saling terbuka sedikit demi sedikit, dan gantian. Basa-basi soal cuaca nggak bikin dekat. Cerita kecil tentang dirimu, iya 🤍

💬 Kamu sendiri, pilih makan malam sama siapa? Tulis di komentar 👇
📩 Kirim ke teman yang suka bingung mau ngobrol apa.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Aron dkk. (1997), Personality and Social Psychology Bulletin.

#psikologi #faktapsikologi #ngobrol #pdkt #komunikasi #ruangpikir
```

## Caption TikTok
```
Mau cepat akrab sama orang baru? Tanya ini: "Kalau bisa makan malam bareng siapa aja di dunia, kamu pilih siapa?" 🍽️

Pertanyaan pertama dari 36 pertanyaan riset Arthur Aron (1997). Saling terbuka sedikit demi sedikit & gantian bikin lebih dekat daripada basa-basi.

Kamu pilih siapa? 👇

#psikologi #ngobrol #pdkt #komunikasi #ruangpikir
```

## Komentar pertama (pin)
```
Aku duluan: makan malam sama aku 10 tahun lagi, mau nanya "akhirnya berhasil nggak?" 😅 Kamu pilih siapa? 👇
```

## Story promosi
```
Kenalan sama orang baru, cuma basa-basi terus? 😶
Coba tanya ini.
Tonton video barunya 👇
```

## Judul YouTube Shorts
```
1 pertanyaan biar cepat akrab sama orang baru (riset psikologi) #shorts
```

## Produksi
Folder `video-engine/ep17_cepat-akrab/` (dibangun dari EP14): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`). Encode CRF 26. Helper baru: `q_card()` (kartu pertanyaan 3D: muka teks, belakang "?" emas, `back_only` saat jatuh berputar, `hl` menyalakan baris terakhir), `wrap()`, `wob()` (goyangan kartu yang sama di dua adegan supaya crossfade mulus), `mini_card()`, `depth_col()`, `shells()`; plus helper EP14 (`cafe_bg()`, `table()`, `conn_meter(label=...)`, `two_chat(lx, rx)`), `research_card(tag='PSPB')`.
