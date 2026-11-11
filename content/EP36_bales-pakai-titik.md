# EP 36 — Bales pakai titik, kok dikira marah?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep36-bales-pakai-titik.mp4` (±52 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/bales-pakai-titik/`.
Format: seri "kalimat yang tepat" (ganti satu hal kecil yang mengubah reaksi orang) + trik disensor lalu dibuka (rumus EP24) + topik chat/ngobrol (paling banyak dikirim ke teman). Visual premium sejak EP35 v2: studio sorot, objek 3D besar di tengah, gerak fisik.

## Riset
- **Sumber utama:** Gunraj, D. N., Drumm-Hewitt, A. M., Dashow, E. M., Upadhyay, S. S. N., & Klin, C. M. (2016). Texting insincerely: The role of the period in text messaging. *Computers in Human Behavior, 55*, 1067–1075. (Binghamton University, lab Celia Klin.)
  - **126 mahasiswa** membaca percakapan singkat: pengirim bertanya, penerima membalas **satu kata** ("Okay", "Sure", "Yeah", "Yup"), **dengan titik** atau **tanpa tanda baca**.
  - Percakapan ditunjukkan sebagai **pesan chat** atau sebagai **catatan tulisan tangan**.
  - Hasil: balasan bertitik dinilai **kurang tulus**, tapi **hanya di chat**. Di tulisan tangan **tidak ada bedanya**.
- **Studi lanjutan:** Houghton, K. J., Upadhyay, S. S. N., & Klin, C. M. (2018). Punctuation in text messages may convey abruptness. Period. *Computers in Human Behavior, 80*. https://doi.org/10.1016/j.chb.2017.10.044 — titik di balasan satu kata terasa **ketus / menutup obrolan** (abruptness, finality).
- **Penjelasan (dari para peneliti):** dalam chat tidak ada nada suara, ekspresi muka, atau jeda, jadi tanda baca ikut membawa "nada".
- **Jujur soal batasnya:**
  - Klin sendiri bilang media melebih-lebihkan: hasil ini **bukan berarti memakai titik itu tidak sopan**.
  - Efeknya terutama pada **balasan yang sangat singkat**. Hubungan antarpengirim dan topik obrolan belum diteliti.
  - Pesertanya mahasiswa Amerika berbahasa Inggris. Contoh kata "oke" di video adalah terjemahan ilustratif.
  - Temuan bahwa tanda seru terasa lebih tulus hanya ada di liputan media, belum terbit sebagai paper, jadi **tidak diklaim** di video.
- **Data ilustratif:** tinggi tabung, persen "KESAN TULUS", nama (Nadia, Raka, Sasa, Dimas), dan isi chat. Tidak ada data Francesca Gino.

## Judul di layar
```
Bales pakai titik, kok [dikira marah?]
```

## Hook (detik 0–3)
- Suara: **"Kamu suka bales chat pakai titik? Hati-hati. Kata riset, balasan kayak gitu bisa kedengeran nggak tulus."**
- Visual sejak frame pertama:
  - ponsel chat 3D: "besok jadi nongkrong?", "aku udah booking!" → dibalas **"oke."** (titiknya menyala koral);
  - titik itu jadi **bola krom hitam raksasa** yang jatuh ke gelembung "oke" besar, lalu gelembungnya **retak dan membeku**;
  - meter **KESAN TULUS** turun dari 92% ke 28%, dan teman cemas berpikir "dia marah ya?";
  - kartu emas **TRIK 1 TANDA** buram + gembok (dibuka di detik ±42 video).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Kamu suka bales chat pakai titik? Hati-hati. Kata riset, balasan kayak gitu bisa kedengeran nggak tulus."),
    (5.88, "Tahun dua ribu enam belas, peneliti Celia Klin dan timnya menguji ini."),
    (9.4, "Seratus dua puluh enam mahasiswa membaca chat yang dibalas satu kata. Ada yang pakai titik, ada yang nggak."),
    (14.36, "Hasilnya? Yang pakai titik dinilai kurang tulus. Anehnya, kalau ditulis tangan, nggak ada bedanya."),
    (20.28, "Soalnya di chat, kita nggak bisa dengar nada suara atau lihat muka. Jadi tanda baca yang ngegantiin."),
    (25.53, "Dan titik di balasan singkat kerasa kayak nutup obrolan. Kesannya ketus, padahal kamu nggak marah."),
    (30.53, "Jadi kalau balasnya cuma satu kata, coba trik kecil ini: hapus titiknya."),
    (34.26, "Kirim video ini ke teman yang suka bales pakai titik!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–5.9 | **Hook:** studio lampu sorot. Ponsel chat 3D, balasan "oke." Bola titik krom raksasa jatuh ke gelembung "oke" besar: retak + membeku + gelombang es. Meter KESAN TULUS turun, teman cemas "dia marah ya?". Kartu TRIK 1 TANDA terbang miring 3D, buram + gembok. |
| 5.9–9.4 | Kartu ARSIP RISET 2016 · Gunraj dkk. & Celia Klin · Binghamton Univ. · Computers in Human Behavior + bola titik "SATU TANDA KECIL". |
| 9.4–14.4 | Teks 3D **126 MAHASISWA** + grid 126 ikon orang. Lalu DIBALAS 1 KATA: dua ponsel 3D miring; gelembung besar berganti oke/iya/sip/boleh, lalu "oke" vs "oke" + bola titik (PAKAI TITIK, koral) dan TANPA TITIK (mint). |
| 14.4–20.3 | HASILNYA? → tabung kaca SEBERAPA TULUS: tanpa titik lebih tinggi, pakai titik KURANG TULUS. Lalu bergeser ke DI CHAT vs DI KERTAS (sobekan kertas tulisan tangan): dua tabung emas sama tinggi, NGGAK ADA BEDANYA. |
| 20.3–25.5 | Ponsel chat 3D di tengah; ikon NADA SUARA dan EKSPRESI MUKA dicoret, lalu tanda baca 3D (bola titik, !, ?, ?!, koma, !!) mengorbit ponsel: TANDA BACA = NADA. |
| 25.5–30.5 | Dua tokoh kapsul. Chat teman mengalir ("haha iya bener", "terus terus?", "seru banget tau!"). Gelembung "oke." dari tokoh kiri: bola titiknya terbang, membesar, jatuh di tengah dan jadi **dinding es OBROLAN DITUTUP**. Sisi teman membeku: "dia marah ya?" + KESANNYA KETUS. Tokoh kiri: "aku biasa aja kok". |
| 30.5–34.3 | Kartu dibuka dengan sinar: **"Balas singkat? Hapus titiknya."** + tombol hapus (backspace) 3D ditekan. Bola titik pecah jadi garis cahaya, es mencair, gelembung "oke" jadi hangat (pendar mint), teman tersenyum: JADI KERASA HANGAT. |
| 34.3–36.6 | Kartu SIMPAN TRIK INI + KIRIM KE (bestie, teman kerja, teman kelas, pacar) + TERKIRIM. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Bales "oke." pakai titik? Hati-hati
```
Alternatif: `Satu titik bikin kamu dikira marah` atau `Tim titik atau tim nggak?`

## Caption Instagram
```
Kamu suka bales chat pakai titik? 😶 Hati-hati. Kata riset, balasan kayak gitu bisa kedengeran nggak tulus.

Tahun 2016, peneliti Celia Klin dan timnya menguji ini. 126 mahasiswa membaca chat yang dibalas satu kata. Ada yang pakai titik, ada yang nggak.

Hasilnya? Yang pakai titik dinilai kurang tulus. Anehnya, kalau ditulis tangan, nggak ada bedanya ✍️

Soalnya di chat, kita nggak bisa dengar nada suara atau lihat muka. Jadi tanda baca yang ngegantiin. Dan titik di balasan singkat kerasa kayak nutup obrolan. Kesannya ketus, padahal kamu nggak marah 🧊

Jadi kalau balasnya cuma satu kata, coba trik kecil ini: hapus titiknya ✨
"oke." → "oke"

📩 Kirim ke teman yang suka bales pakai titik
💬 Kamu tim titik atau tim nggak? 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Gunraj, Klin dkk. (2016); Houghton, Upadhyay & Klin (2018), Computers in Human Behavior.

#psikologi #faktapsikologi #chat #komunikasi #salahpaham #ruangpikir
```

## Caption TikTok
```
Bales "oke." pakai titik, eh dikira marah 😶

Riset (Gunraj, Klin dkk. 2016): balasan satu kata yang pakai titik dinilai kurang tulus, tapi cuma di chat. Ditulis tangan? Nggak ada bedanya. Trik kecil: hapus titiknya ✨

Kirim ke teman yang suka bales pakai titik 📩

#psikologi #chat #salahpaham #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Jujur, kamu pernah dikira marah gara-gara bales "oke." doang? 😭 Tim titik atau tim nggak? 👇
```

## Story promosi
```
Kamu bales "oke." pakai titik?
Kata riset, itu bisa kedengeran nggak tulus 😶
Tonton video barunya 👇
```
Stiker polling: `Kamu tim... titik (.) 😐 / tanpa titik 😊`

## Judul YouTube Shorts
```
Bales chat pakai titik, kok dikira marah? Kata riset psikologi (Klin 2016) #shorts
```

## Waktu upload
Malam 19.00–21.00 WIB (jam ramai chat), paling pas Kamis–Sabtu.

## Produksi
- **Folder:** `video-engine/ep36_titik-chat/` (dibangun dari EP35 v2).
- **Render:**
  - Render ulang dengan `./build.sh`; suara sudah ada di `vo/`.
  - Buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`).
  - `DUR` 42, jeda antarbaris 0.35 dtk, encode CRF 26.
- **Lagu orisinal:** `audio.py` di folder ini (variasi EP22: 100 BPM, `TR = 2`).
- **Versi tanpa musik:**
  1. `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`
  2. Mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14).
- **Helper baru:**
  - `chrome_dot()` — bola titik krom 3D, `cold` = lapisan es.
  - `big_bubble()` — gelembung chat besar + bola titik. Pilihan: `frost_` membeku, `crack` retak, `warm` hangat, `drop` titik jatuh, `burst` pecah, `cursor`; lebar ikut `dot`.
  - `chat_phone3()` / `cphone3d()` — ponsel chat dengan nama bebas, titik di balasan bisa menyala.
  - `tube()` — tabung kaca berisi cairan.
  - `paper_scrap()` — sobekan kertas tulisan tangan.
  - `cue_icon()` — ikon NADA SUARA / EKSPRESI MUKA yang bisa dicoret.
  - `glyph_ring()` — orbit tanda baca 3D.
  - `ice_wall()`, `key_back()` (tombol hapus 3D), `h_meter()`, `sparks()` (ledakan garis, bukan titik), `ice_layer()`.
- **Dipakai juga:** `studio()`, `secret_card2()`, `research_card()`, `extrude()`, `hero()`, `thought()`, `mini_person()`, `avatar()`, `plane_icon()`.
