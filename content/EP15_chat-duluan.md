# EP 15 — Chat duluan, kok gengsi?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep15-chat-duluan.mp4` (±49 detik, 1080×1920), halaman web `ruangpikir.id/episode/chat-duluan/`.
Seri: Trik Psikologi (format seperti EP03, EP12–EP14) · Topik: kita meremehkan seberapa senang orang saat disapa teman lama.

## Riset
- **Sumber utama:** Liu, P. J., Rim, S., Min, L., & Min, K. E. (2023). The surprise of reaching out: Appreciated more than we think. *Journal of Personality and Social Psychology, 124*(4), 754–771 (terbit online Juli 2022).
  - Serangkaian eksperimen (lebih dari 5.900 peserta, termasuk eksperimen lapangan dengan kenalan sungguhan). Peserta menghubungi seseorang yang sudah lama tidak dikontak (pesan singkat, atau pesan + hadiah kecil) lalu menebak seberapa senang penerimanya; penerimanya juga ditanya.
  - Pengirim konsisten **meremehkan** rasa senang penerima (liputan APA: tebakan pengirim ±5,57 vs penerima ±6,17 pada skala 1–7).
  - Rasa **kaget/tidak terduga** ikut memperbesar rasa senang penerima, dan selisihnya makin besar kalau sapaannya makin tidak terduga atau hubungannya makin renggang.
- **Jujur soal batasnya:** penelitian ini tentang hubungan yang dulu baik lalu renggang, bukan hubungan yang berakhir karena konflik; efeknya diukur jangka pendek. Selisih tebakan vs kenyataan nyata tetapi tidak besar, jadi naskah memakai "lebih senang dari yang dikira", bukan "jauh lebih senang". Tahun di video = 2022 (saat terbit online dan ramai diberitakan); sitasi resmi 2023.

## Judul di layar
```
Chat duluan, [kok gengsi]?
```

## Hook (detik 0–3)
- Suara: **"Tiba-tiba keinget teman lama, tapi gengsi chat duluan? Kirim satu chat ini."** Situasi yang hampir semua orang alami + open loop "satu chat ini" yang baru dijawab di detik ±32 (pola "Bilang ini" EP12 yang menahan penonton sampai akhir). Kata "tiba-tiba" di awal juga jadi callback di kalimat penutup ("hai, tiba-tiba keinget kamu").
- Visual sejak frame pertama: tokoh kapsul gemetar di samping ponsel kaca besar, layar chat "Dimas · terakhir chat 3 tahun lalu", riwayat lama yang redup + pemisah **3 TAHUN KEMUDIAN**; kolom ketik terus **mengetik lalu menghapus** ("hai, apa kabar?" → "eh, masih inget aku?") dengan bunyi ketikan; chip "gengsi..."; di "Kirim satu chat ini" muncul gelembung rahasia emas **"? ? ?"**, tombol kirim berpendar emas, sinar emas, chip "1 chat ini", tokoh berubah tersenyum.

## Gaya visual
"Ponsel chat + dua tokoh kapsul berjauhan": ponsel kaca dengan layar chat (riwayat redup, kolom ketik + kursor, tombol kirim, centang biru, balasan), dua jendela kota malam (KAMU vs TEMAN LAMA) dengan pesan yang terbang di lintasan neon, "yang dikira: oh... hai." vs "kenyataannya: EH! apa kabar?! kangen!", notifikasi kejutan + seruan "!" + meter KAGET & SENANG, dinding kaca **GENGSI** yang retak lalu pecah + stempel **SALAH TEBAK**, kolom komentar inisial. Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Tiba-tiba keinget teman lama, tapi gengsi chat duluan? Kirim satu chat ini."),
    (4.38, "Kita sering mikir: nanti ganggu, nanti dikira aneh, udah kelamaan nggak ngobrol."),
    (8.9, "Tahun dua ribu dua puluh dua, psikolog Pegi Liu menguji ini ke lebih dari lima ribu sembilan ratus orang."),
    (14.82, "Peserta diminta menyapa teman yang udah lama nggak dikontak, cukup lewat pesan singkat."),
    (19.73, "Hasilnya? Yang disapa ternyata lebih senang dari yang dikira pengirimnya."),
    (23.85, "Apalagi kalau chatnya nggak disangka-sangka. Makin kaget, makin senang."),
    (27.85, "Jadi rasa takut ganggu itu, seringnya cuma salah tebak."),
    (30.96, "Kirim aja: hai, tiba-tiba keinget kamu. Siapa yang muncul di kepalamu? Tulis inisialnya di komentar!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Pegi Liu" = ejaan fonetik Peggy Liu untuk TTS (caption tetap "Peggy Liu").

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–4.4 | **Hook:** ponsel chat "Dimas · terakhir chat 3 tahun lalu", mengetik lalu menghapus, chip "gengsi..." → gelembung rahasia emas "? ? ?" + tombol kirim emas + "1 chat ini". |
| 4.4–8.9 | YANG KITA PIKIRIN: tokoh gemetar memegang ponsel; chip "nanti ganggu", "nanti dikira aneh", "udah kelamaan", "dia masih inget aku?". |
| 8.9–14.8 | Kartu ARSIP RISET 2022 · Liu, Rim, Min & Min · JPSP; angka 5.900+ berputar naik + avatar. |
| 14.8–19.7 | Dua jendela kota: KAMU vs TEMAN LAMA, "terakhir ngobrol: 3 tahun lalu"; pesan "hai, apa kabar?" terbang di lintasan neon → notifikasi "Pesan baru". |
| 19.7–23.9 | KENYATAANNYA: teman lama berbinar "EH! apa kabar?! kangen!" + hati; YANG DIKIRA: "oh... hai.". |
| 23.9–27.9 | Notifikasi kejutan di layar kunci, seruan "!", meter KAGET lalu SENANG penuh. |
| 27.9–31.0 | Dinding kaca GENGSI ("takut ganggu") retak lalu pecah berhamburan, stempel SALAH TEBAK, garis hati menyambung dua tokoh. |
| 31.0–36.6 | Ponsel: mengetik "hai, tiba-tiba keinget kamu" → kirim → centang biru → balasan "EH!! kangen bgt!"; komentar "inisial R", "D, udah 3 tahun", "A. aku chat sekarang!", "kamu tau siapa". |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Siapa yang barusan kamu inget?
```
Alternatif: `Gengsi chat duluan? Tonton ini` atau `Chat dia, dia bakal senang`

## Caption Instagram
```
Tiba-tiba keinget teman lama, tapi gengsi chat duluan? 🥲

"Nanti ganggu." "Nanti dikira aneh." "Udah kelamaan nggak ngobrol." Akhirnya chatnya dihapus lagi.

Padahal riset bilang kita salah tebak. Psikolog Peggy Liu dan timnya menguji ini ke lebih dari 5.900 orang: peserta diminta menyapa teman yang udah lama nggak dikontak, cukup lewat pesan singkat. Hasilnya? Yang disapa ternyata lebih senang dari yang dikira pengirimnya.

Dan makin nggak disangka chatnya, makin senang yang nerima 💌

Jadi kirim aja: "hai, tiba-tiba keinget kamu. Apa kabar?" 🤍

💬 Siapa yang barusan muncul di kepalamu? Tulis inisialnya di komentar 👇
📩 Atau langsung kirim video ini ke dia.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Liu, Rim, Min & Min (2022/2023), Journal of Personality and Social Psychology.

#psikologi #faktapsikologi #pertemanan #temanlama #overthinking #ruangpikir
```

## Caption TikTok
```
Gengsi chat duluan ke teman lama? Kamu salah tebak 🥲

Riset Liu dkk. (5.900+ orang): yang disapa ternyata lebih senang dari yang dikira pengirimnya. Makin nggak disangka, makin senang.

Siapa yang muncul di kepalamu? Tulis inisialnya 👇

#psikologi #pertemanan #temanlama #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Aku duluan: inisial D, udah 3 tahun nggak chat. Habis upload ini aku kirim "hai, tiba-tiba keinget kamu" 🥲 Giliranmu, inisial siapa? 👇
```

## Story promosi
```
Tiba-tiba keinget teman lama? 🥲
Jangan dihapus lagi chatnya.
Tonton video barunya 👇
```

## Judul YouTube Shorts
```
Gengsi chat teman lama duluan? Ini kata riset psikologi #shorts
```

## Produksi
Folder `video-engine/ep15_chat-duluan/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`; kalimat pertama dibuka "Tiba-tiba ..." supaya kata pertama jelas). Encode CRF 26. Helper baru: `chat_phone()` (ponsel kaca dengan layar chat: riwayat, `gap` pemisah waktu, `typed` + kursor, `mystery` gelembung emas, `sent`/`tick`/`reply`), `typed_at()` (mengetik lalu menghapus), `msg_bubble()`, `ticks()`, `window()` (jendela kota malam), `meter()`, `burst()` (seruan kaget), `glass_wall()` (dinding kaca yang retak lalu pecah); plus helper EP12/EP14 (`hero()`, `say()`, `phone(btitle=...)`, `notif()`, `stamp()`, `crack()`, `research_card()`, `comment()`).
