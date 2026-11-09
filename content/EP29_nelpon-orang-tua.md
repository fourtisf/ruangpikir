# EP 29 — Jarang nelpon orang tua? Coba kalimat ini

Status: **sudah diproduksi** — `videos/ruang-pikir-ep29-nelpon-orang-tua.mp4` (±54 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/nelpon-orang-tua/`.
Seri: **"Kalimat yang tepat"** (EP24 → EP26 → EP27 → EP28 → EP29), topik keluarga/anak rantau.

## Riset
- **Sumber:** Kumar, A., & Epley, N. (2021). It's surprisingly nice to hear you: Misunderstanding the impact of communication media can lead to suboptimal choices of how to connect with others. *Journal of Experimental Psychology: General, 150*(3), 595–607. (Amit Kumar, University of Texas at Austin; Nicholas Epley, University of Chicago. Banyak media memberitakannya September 2020 saat terbit online.)
  - Sekitar **200 orang** diminta menebak bagaimana rasanya menghubungi **teman lama** lewat telepon atau email, lalu diacak untuk benar-benar melakukannya.
  - Mereka mengira telepon akan **lebih canggung**. Kenyataannya **tidak lebih canggung**, dan yang menelepon merasa **lebih dekat** daripada yang mengirim email.
  - Waktu yang dihabiskan **hampir sama** dengan menulis dan membalas email.
  - Eksperimen lain dengan orang asing: berbicara lewat suara membuat orang merasa lebih terhubung daripada lewat teks; video tidak menambah banyak dibanding suara saja.
- **Jujur soal batasnya:** riset dilakukan dengan teman lama dan orang asing, **bukan khusus dengan orang tua**; bagian "apalagi ke orang yang paling nungguin kabarmu" adalah ajakan, bukan hasil riset. Kalimat "Nggak ada apa-apa, cuma kangen denger suara Ibu" adalah saran pembuka obrolan, bukan kalimat yang diuji. Chat, "3 minggu lalu", dan tampilan batang di video ilustratif (tanpa angka riset). Tidak ada data Francesca Gino.

## Judul di layar
```
Jarang nelpon orang tua? [Coba kalimat ini]
```

## Hook (detik 0–3)
- Suara: **"Jarang nelpon orang tua? Jangan cuma bales: iya, udah. Coba telepon, terus bilang kalimat ini."**
- Visual sejak frame pertama: ponsel chat dengan **Ibu** ("Nak, udah makan?", "Kapan pulang?"), kartu **TERAKHIR TELEPON: 3 minggu lalu**, balasan **"iya"** / **"udah"** muncul tepat saat diucapkan lalu **dicoret**, layar berganti **Memanggil Ibu...** dengan tombol hijau berdenyut → kartu emas **KALIMAT YANG DITUNGGU** buram + gembok (dibuka di detik ±45 video).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Jarang nelpon orang tua? Jangan cuma bales: iya, udah. Coba telepon, terus bilang kalimat ini."),
    (5.97, "Kita sering nunda, karena takut canggung dan bingung mau ngomong apa."),
    (9.51, "Tahun dua ribu dua puluh satu, peneliti Amit Kumar dan Nicholas Epley menguji ini."),
    (13.49, "Dua ratus orang diminta menghubungi teman lama, lewat telepon atau email."),
    (16.91, "Hasilnya? Mereka kira telepon bakal lebih canggung. Ternyata nggak. Malah rasa dekatnya lebih kuat."),
    (21.48, "Soalnya suara membawa perasaan yang nggak kebaca di tulisan. Waktunya pun hampir sama."),
    (25.8, "Kalau ke teman lama aja gitu, apalagi ke orang yang paling nungguin kabarmu."),
    (29.86, "Jadi malam ini, coba telepon dan bilang: nggak ada apa-apa, cuma kangen denger suara Ibu."),
    (34.69, "Kirim video ini ke teman yang lagi merantau!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
Pemotongan otomatis menaruh "Hasilnya?" di akhir baris 4; dipindah manual ke awal baris 5 di jeda energi.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–6.0 | **Hook:** chat Ibu, TERAKHIR TELEPON 3 minggu lalu, "iya"/"udah" dicoret, layar Memanggil Ibu, kartu KALIMAT YANG DITUNGGU buram. |
| 6.0–9.5 | Kartu SENIN / RABU / JUMAT "nanti aja..." + stempel DITUNDA, tokoh berkeringat: "nanti canggung...", "mau ngomong apa ya?" |
| 9.5–13.5 | Kartu ARSIP RISET 2021 · Amit Kumar & Nicholas Epley · UT Austin & University of Chicago + judul paper "It's surprisingly nice to hear you". |
| 13.5–16.9 | Penghitung **200 ORANG** + grid 200 orang yang terbelah ke TELEPON vs EMAIL. |
| 16.9–21.5 | HASILNYA? → SEBERAPA CANGGUNG: telepon DIKIRA tinggi → TERNYATA SAMA dengan email; RASA DEKAT: telepon LEBIH KUAT + hati; tokoh dari cemas jadi senang. |
| 21.5–25.8 | TULISAN "aku baik kok" + ??? vs SUARA (gelombang emas, "nada hangat", "ketawa kecil") → stopwatch: NGETIK EMAIL vs TELEPON = HAMPIR SAMA. |
| 25.8–29.9 | Telepon TEMAN LAMA → LEBIH DEKAT, lalu rumah Ibu di malam hari + bulan, Ibu berkerudung memegang ponsel: "anakku lagi apa ya?" |
| 29.9–34.7 | KOS ↔ RUMAH: ponsel berdering lalu tersambung, gelombang suara emas; kartu dibuka: **"Nggak ada apa-apa, cuma kangen denger suara Ibu."** + Ibu senang, hati beterbangan, "Ibu juga kangen, Nak". |
| 34.7–36.6 | Kartu "COBA MALAM INI · Telepon, bilang kangen." + panel KIRIM KE (teman kos, sahabat, kakak, teman rantau) + pesawat kertas + TERKIRIM. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Jarang nelpon orang tua? Coba kalimat ini
```
Alternatif: `Jangan cuma bales "iya, udah"` atau `Anak rantau wajib nonton`

## Caption Instagram
```
Jarang nelpon orang tua? Jangan cuma bales "iya, udah" 🙏 Coba telepon, terus bilang kalimat ini.

Kita sering nunda karena takut canggung dan bingung mau ngomong apa 😶

Tahun 2021, peneliti Amit Kumar dan Nicholas Epley menguji ini. 200 orang diminta menghubungi teman lama, lewat telepon atau email.

Hasilnya? Mereka kira telepon bakal lebih canggung. Ternyata nggak. Malah rasa dekatnya lebih kuat 📞

Soalnya suara membawa perasaan yang nggak kebaca di tulisan. Waktunya pun hampir sama.

Kalau ke teman lama aja gitu, apalagi ke orang yang paling nungguin kabarmu 🏠

Jadi malam ini, coba telepon dan bilang: "Nggak ada apa-apa, cuma kangen denger suara Ibu." 🤍
(Ganti jadi Bapak, Mama, Ayah, atau siapa pun yang kamu panggil di rumah.)

📩 Kirim ke teman yang lagi merantau!
💬 Terakhir kamu nelpon orang tua kapan? 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Kumar & Epley (2021), Journal of Experimental Psychology: General.

#psikologi #faktapsikologi #anakrantau #orangtua #keluarga #ruangpikir
```

## Caption TikTok
```
Jarang nelpon orang tua? Jangan cuma bales "iya, udah" 🙏

Riset Kumar & Epley (2021): telepon nggak secanggung yang kita kira, dan bikin lebih dekat daripada tulisan. Malam ini coba bilang: "Nggak ada apa-apa, cuma kangen denger suara Ibu." 🤍

Kirim ke teman yang lagi merantau 📩

#psikologi #anakrantau #orangtua #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Habis nonton ini aku langsung nelpon Ibu, padahal biasanya cuma chat 🥹 Kamu terakhir nelpon orang tua kapan? Tulis "udah" kalau malam ini kamu nelpon 👇
```

## Story promosi
```
Chat dari Ibu cuma kamu bales "iya, udah"? 🥲
Ada riset soal telepon vs chat. Coba kalimat ini malam ini.
Tonton video barunya 👇
```
Stiker polling: `Terakhir nelpon orang tua... minggu ini / udah lama banget`

## Judul YouTube Shorts
```
Jarang nelpon orang tua? Coba bilang kalimat ini malam ini #shorts
```

## Waktu upload
Malam 19.00–21.00 WIB (jam anak kos/rantau santai dan jam orang tua masih bangun), paling pas Jumat–Minggu. Alternatif: menjelang libur panjang/mudik.

## Produksi
Folder `video-engine/ep29_nelpon-ortu/` (dibangun dari EP28): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`; cek tiap baris dengan transkripsi, pemotongan otomatis bisa menaruh kata pembuka di baris sebelumnya). Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 90 BPM, `TR = -2`). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper baru: `chat_phone2()`, `ibu()`, `house()`, `moon()`, `mini_phone()`, `handset()`, `envelope_icon()`, `stopwatch()`, `msg()`, `secret_card2()`, `ghost_bar()`; plus `hero()`, `research_card()`, `race_bar()`, `extrude()`, `stamp()`, `thought()`, `say()`, `waves()`, `avatar()`, `plane_icon()`.
