# EP 28 — Minta masukan? Ganti satu kata ini

Status: **sudah diproduksi** — `videos/ruang-pikir-ep28-ada-saran.mp4` (±46 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/ada-saran/`.
Seri: **"Kalimat yang tepat"** (EP24 → EP26 → EP27 → EP28), variasi topik sekolah/kerja.

## Riset
- **Studi awal:** Yoon, J., Blunden, H., Kristal, A., & Whillans, A. (2019). Why asking for advice is more effective than asking for feedback. *Harvard Business Review* (ringkasan 4 eksperimen peneliti Harvard Business School, termasuk eksperimen lapangan di kelas eksekutif).
  - Dibanding yang diminta **feedback**, yang diminta **saran (advice)** menyebutkan **34% lebih banyak hal yang bisa diperbaiki** dan **56% lebih banyak cara memperbaikinya**.
  - Penjelasan: "feedback" diasosiasikan dengan menilai performa yang sudah lewat; "saran" mendorong orang berpikir ke depan.
- **Studi lanjutan:** Blunden, H., Kristal, A., Whillans, A., Yoon, J., Burd, H., Bremner, G., & Yeomans, M. (2025). Eliciting advice instead of feedback improves developmental input. *Management Science*.
  - Eksperimen lapangan pra-registrasi (**27.432 komentar**) + dua studi lab (n = 806): meminta saran menghasilkan masukan yang lebih konkret dan dinilai lebih berguna oleh penilai independen.
- **Jujur soal batasnya:** angka 34%/56% dari studi awal (bukan dari studi lapangan); beberapa ulasan menyebut pemula mungkin lebih butuh semangat daripada kritik detail. Contoh jawaban di video ilustratif. Tidak ada data Francesca Gino.

## Judul di layar
```
Minta masukan? [Ganti satu kata ini]
```

## Hook (detik 0–3)
- Suara: **"Mau masukan yang beneran berguna? Jangan tanya: ada feedback? Ganti satu kata ini."**
- Visual sejak frame pertama: kafe malam, laptop PRESENTASI, tokoh bertanya **"ada feedback?"** → teman menjawab **"bagus kok!"** + jempol 👍 → kartu **MASUKAN KONKRET: 0** (merah) → gelembung dicoret → kartu emas **KALIMAT PENGGANTI** buram + gembok (dibuka di detik ±37 video).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Mau masukan yang beneran berguna? Jangan tanya: ada feedback? Ganti satu kata ini."),
    (5.01, "Biasanya jawabannya cuma: bagus kok, udah oke."),
    (8.59, "Tahun dua ribu sembilan belas, peneliti Harvard Jaewon Yun dan timnya menguji ini."),
    (12.76, "Ada yang dimintai feedback. Ada yang dimintai saran."),
    (15.49, "Hasilnya? Yang dimintai saran memberi tiga puluh empat persen lebih banyak hal yang bisa diperbaiki, dan lima puluh enam persen lebih banyak caranya."),
    (22.65, "Soalnya feedback bikin orang menilai yang udah lewat. Saran bikin orang mikir ke depan."),
    (27.14, "Di riset lapangan dengan puluhan ribu komentar pun, hasilnya sama."),
    (30.82, "Jadi habis presentasi atau kirim tugas, coba tanya: ada saran, nggak?"),
    (34.28, "Kirim video ini ke teman yang lagi ngerjain skripsi!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Jaewon Yun" = ejaan fonetik Jaewon Yoon untuk TTS (caption tetap "Jaewon Yoon").

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–5.0 | **Hook:** laptop PRESENTASI, "ada feedback?" → "bagus kok!" + jempol, MASUKAN KONKRET 0, dicoret, kartu KALIMAT PENGGANTI buram. |
| 5.0–8.6 | Jawaban "bagus kok", "udah oke", "mantap!", "keren" + jempol → chip TAPI APA YANG BISA DIPERBAIKI? |
| 8.6–12.8 | Kartu ARSIP RISET 2019 · Yoon, Blunden, Kristal & Whillans · HBS. |
| 12.8–15.5 | Panel KELOMPOK A "ada feedback?" (bagus kok, udah oke) vs KELOMPOK B "ada saran?" (grafiknya perbesar, teks slide 3 kepanjangan, mulai pakai cerita). |
| 15.5–22.7 | HASILNYA? → batang FEEDBACK vs SARAN: **+34%** hal yang bisa diperbaiki, **+56%** cara memperbaikinya. |
| 22.7–27.1 | Garis waktu: KEMARIN = MENILAI (kaca pembesar + stempel 7/10) vs BESOK = MIKIR KE DEPAN (kartu saran: grafik dibesarin, slide 3 dipotong, tambah contoh). |
| 27.1–30.8 | RISET LAPANGAN · MANAGEMENT SCIENCE 2025: penghitung **27.432 KOMENTAR** + "SARAN" = MASUKAN LEBIH KONKRET. |
| 30.8–34.3 | Kartu dibuka: **"Ada saran, nggak?"** + kartu saran konkret beterbangan, tokoh senang. |
| 34.3–36.6 | Kartu "COBA SEKARANG" + panel KIRIM KE (teman sekelas, rekan kerja, sahabat, adik tingkat) + pesawat kertas + TERKIRIM. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Jangan tanya "ada feedback?"
```
Alternatif: `Ganti 1 kata ini biar dapat masukan berguna` atau `Habis presentasi, tanya ini`

## Caption Instagram
```
Mau masukan yang beneran berguna? Jangan tanya "ada feedback?" 🙅 Ganti satu kata ini.

Biasanya jawabannya cuma: "bagus kok", "udah oke" 👍😅

Tahun 2019, peneliti Harvard Jaewon Yoon dan timnya menguji ini. Ada yang dimintai feedback, ada yang dimintai saran.

Hasilnya? Yang dimintai saran memberi 34% lebih banyak hal yang bisa diperbaiki, dan 56% lebih banyak caranya 📈

Soalnya "feedback" bikin orang menilai yang udah lewat. "Saran" bikin orang mikir ke depan. Di riset lapangan dengan puluhan ribu komentar pun, hasilnya sama.

Jadi habis presentasi atau kirim tugas, coba tanya: "Ada saran, nggak?" 💡

📩 Kirim ke teman yang lagi ngerjain skripsi!
💬 Masukan paling berguna yang pernah kamu dapat apa? 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Yoon, Blunden, Kristal & Whillans (2019, Harvard Business Review); Blunden dkk. (2025, Management Science).

#psikologi #faktapsikologi #presentasi #skripsi #kuliah #ruangpikir
```

## Caption TikTok
```
Habis presentasi jangan tanya "ada feedback?" 🙅

Riset Harvard (2019): yang dimintai "saran" kasih 34% lebih banyak hal yang bisa diperbaiki & 56% lebih banyak caranya. Coba tanya: "Ada saran, nggak?" 💡

Kirim ke teman yang lagi skripsian 📩

#psikologi #presentasi #skripsi #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Masukan paling berguna yang pernah aku dapat: "mulai presentasinya pakai cerita" 💡 Kamu pernah dapat saran apa yang ngubah hasil kerjaanmu? 👇
```

## Story promosi
```
Habis presentasi, cuma dibilang "bagus kok"? 👍😅
Ganti satu kata ini biar dapat masukan yang berguna.
Tonton video barunya 👇
```
Stiker polling: `Kamu lebih sering... nanya "ada feedback?" / nanya "ada saran?"`

## Judul YouTube Shorts
```
Habis presentasi jangan tanya "ada feedback?" Ganti 1 kata ini #shorts
```

## Waktu upload
Minggu–Kamis malam 19.00–21.00 WIB (saat pelajar/mahasiswa ngerjain tugas), atau Senin pagi 06.30–08.00 sebelum kelas/kerja.

## Produksi
Folder `video-engine/ep28_ada-saran/` (dibangun dari EP27): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`; TTS membaca lambat, jadi cek total setelah tighten). Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 102 BPM, `TR = 2`). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper baru: `thumb()`, `idea_card()`, `ask_panel()`; plus `laptop()`, `secret_card()`, `race_bar()`, `extrude()`, `magnifier()`, `stamp()`, `research_card()`, `cafe_bg()`, `hero()`, `say()`, `avatar()`, `plane_icon()`.
