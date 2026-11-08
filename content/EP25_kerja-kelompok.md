# EP 25 — Kerja kelompok, kok aku paling capek?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep25-kerja-kelompok.mp4` (±48 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/kerja-kelompok/`.
Seri: perasaan "kok aku gini?" + riset yang bikin lega + trik konkret (format EP14/EP24), dengan 4 tokoh kapsul.

## Riset
- **Sumber utama:** Schroeder, J., Caruso, E. M., & Epley, N. (2016). Many hands make overlooked work: Over-claiming of responsibility increases with group size. *Journal of Experimental Psychology: Applied, 22*(2), 238–246.
  - Empat studi, termasuk **699 mahasiswa MBA** dalam kelompok belajar (kelas negosiasi) dan tim penulis artikel ilmiah; tiap anggota memperkirakan persentase kerjanya sendiri.
  - Jumlah klaim semua anggota **secara konsisten lebih dari 100%** dan makin besar seiring jumlah anggota; di sebagian tim berisi **8 orang atau lebih** totalnya **melewati 140%**, sedangkan kelompok ≤ 4 orang biasanya di bawah 110%.
  - Penyebab: egosentrisme ingatan. Kerja sendiri lebih mudah teringat, kerja orang lain luput. Bukan karena bohong.
- **Trik:** klaim berlebihan berkurang ketika anggota memikirkan dulu kontribusi anggota lain (juga Caruso, Epley & Bazerman, 2006, JPSP). Peneliti juga menyarankan membagi kelompok besar jadi tim kecil dan memperjelas pembagian tugas.
- **Jujur soal batasnya:** angka klaim tokoh di video (50%, 50%, 35%, 30%) adalah contoh ilustrasi; kartu 6 kelompok hanya menulis "> 100%". Tidak ada data Francesca Gino.

## Judul di layar
```
Kerja kelompok, [kok aku paling capek]?
```

## Hook (detik 0–3)
- Suara: **"Kamu ngerasa paling banyak kerja di kelompok? Faktanya, hampir semua anggota ngerasa gitu juga."** Perasaan yang dialami hampir semua pelajar/pekerja + fakta yang membalik dugaan.
- Visual sejak frame pertama: meja kerja kelompok malam, 4 tokoh kapsul + laptop "TUGAS KELOMPOK". Beruntun tiap ±0,35 detik muncul klaim **"aku 50%!", "aku 50%!", "aku 35%!", "aku 30%!"** sementara **penghitung 3D raksasa melonjak 0 → 165%**, berubah merah dan bergetar dengan alarm begitu lewat 100%, chip **LEBIH DARI 100%?!**. Di "hampir semua anggota" keempat tokoh sama-sama berkeringat dengan gelembung "paling capek...".
- **Lagu:** variasi lagu EP22 yang lebih cepat (104 BPM, orisinal), mulai dari frame pertama.

## Lagu (orisinal, bebas hak cipta)
Dibuat di `video-engine/ep25_kerja-kelompok/audio.py` (`music()`, turunan EP22): 104 BPM, `TR = 0`, e-piano Fmaj7–G6–Em7–Am7, bass, kick/clap/hi-hat swing, melodi pentatonik, chime; volume musik otomatis turun saat narasi.
- Kalau mau memakai **lagu trending TikTok/IG**, pakai **`videos/ruang-pikir-ep25-kerja-kelompok-tanpa-musik.mp4`** (narasi + efek suara saja). Tambahkan lagunya lewat fitur musik di aplikasi: **suara asli 100%**, **lagu ±10–15%**. Pilih lagu yang lucu/ceria (nuansa "drama tugas kelompok"). Jangan menempelkan lagu berhak cipta ke file video.

## Gaya visual
"Meja kerja kelompok + diagram lingkaran 3D yang meluap": meja panjang kayu dengan 4 tokoh kapsul berwarna (emas, pink, mint, biru) + laptop bercahaya; penghitung persen 3D; **diagram lingkaran 3D** yang diisi klaim tiap anggota, kelebihannya menumpuk jadi **lapisan kedua merah yang melayang dan bergetar** ("TOTAL 165%", tanda tanya 3D); kartu ARSIP RISET 2016 + 56 ikon mahasiswa; 6 kartu KELOMPOK yang semuanya "> 100%" + stempel **SELALU > 100%**; batang **4 ORANG (<110%)** vs **8+ ORANG (140%+)** melewati garis BATAS 100%; lampu sorot: "KERJAANKU: JELAS" (kartu tugas terang dicentang) vs "KERJAAN MEREKA: ???" (kartu gelap buram) + stempel BUKAN BOHONG; "CARANYA" + gelembung "kalian ngapain aja sih?!" dicoret → kartu **SEBUTIN DULU** (Rina · desain slide, Dimas · cari data, Sari · ngetik laporan, Aku · presentasi ✓) → diagram kembali **TOTAL 100% · LEBIH ADIL**; ponsel grup chat **KELOMPOK 3** + pesawat kertas "KIRIM KE GRUP". Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Kamu ngerasa paling banyak kerja di kelompok? Faktanya, hampir semua anggota ngerasa gitu juga."),
    (5.13, "Yang satu ngaku ngerjain setengah, yang lain juga. Kok bisa?"),
    (8.48, "Tahun dua ribu enam belas, Juliana Syroder dan Nicholas Epley menguji ini ke hampir tujuh ratus mahasiswa."),
    (13.56, "Hasilnya? Kalau klaim semua anggota dijumlah, totalnya selalu lebih dari seratus persen."),
    (18.13, "Makin besar kelompoknya, makin parah. Tim delapan orang bisa tembus seratus empat puluh persen!"),
    (22.95, "Bukan karena bohong. Kerjaan sendiri kelihatan jelas, kerjaan orang lain sering nggak kelihatan."),
    (28.06, "Caranya: sebelum ngomel, sebutin dulu yang lain ngerjain apa aja. Klaim berlebihnya bakal turun."),
    (33.51, "Kirim video ini ke grup kelompokmu, biar nggak saling ngerasa paling capek!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Juliana Syroder" = ejaan fonetik Juliana Schroeder untuk TTS (caption tetap "Juliana Schroeder"). Kata pembuka sengaja "Kamu ngerasa" dan "Caranya" (bukan "Ngerasa"/"Triknya") karena lebih jelas terdengar di transkripsi.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–5.1 | **Hook:** meja kerja kelompok, klaim "aku 50%!" ×4, penghitung melonjak 165% + alarm, LEBIH DARI 100%?!, semua tokoh "paling capek...". |
| 5.1–8.5 | Diagram lingkaran 3D: SETENGAH! + AKU JUGA SETENGAH! → klaim lain menumpuk jadi lapisan merah, TOTAL 165%, tanda tanya 3D. |
| 8.5–13.6 | Kartu ARSIP RISET 2016 · Schroeder, Caruso & Epley · JEP: Applied + 56 ikon mahasiswa + chip 699 MAHASISWA · KELOMPOK BELAJAR. |
| 13.6–18.1 | 6 kartu KELOMPOK dengan diagram yang meluap "> 100%" + stempel SELALU > 100%. |
| 18.1–22.9 | Batang 4 ORANG (<110%) → MAKIN PARAH → 8+ ORANG (140%+) melewati BATAS 100% + angka 3D 140%+. |
| 22.9–28.1 | Stempel BUKAN BOHONG → lampu sorot "KERJAANKU: JELAS" (bikin slide, cari data, begadang revisi ✓) vs "KERJAAN MEREKA: ???" (buram). |
| 28.1–33.5 | CARANYA + "kalian ngapain aja sih?!" dicoret → kartu SEBUTIN DULU → diagram kembali TOTAL 100% · LEBIH ADIL. |
| 33.5–36.6 | Ponsel grup chat KELOMPOK 3: video terkirim + "wkwk ini kita banget", "oke aku list kerjaan masing2 ya", "jangan2 aku yg suka ngilang". |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Kerja kelompok, kok aku paling capek?
```
Alternatif: `Semua anggota ngerasa paling capek` atau `Total kerja kelompokmu 165%?!`

## Caption Instagram
```
Kamu ngerasa paling banyak kerja di kelompok? 😮‍💨 Faktanya, hampir semua anggota ngerasa gitu juga.

Yang satu ngaku ngerjain setengah, yang lain juga. Kok bisa? 🤔

Tahun 2016, Juliana Schroeder, Eugene Caruso, dan Nicholas Epley menguji ini, salah satunya ke 699 mahasiswa dalam kelompok belajar.

Hasilnya? Kalau klaim semua anggota dijumlah, totalnya selalu lebih dari 100%. Makin besar kelompoknya, makin parah: di tim 8 orang bisa tembus 140%! 📈

Bukan karena bohong. Kerjaan sendiri kelihatan jelas, kerjaan orang lain sering nggak kelihatan 👀

Caranya: sebelum ngomel, sebutin dulu yang lain ngerjain apa aja. Klaim berlebihnya bakal turun ✅

📩 Kirim video ini ke grup kelompokmu, biar nggak saling ngerasa paling capek!
💬 Di kelompokmu, kamu tipe yang mana: si paling kerja, si penyelamat deadline, atau si ngilang? 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Schroeder, Caruso & Epley (2016), Journal of Experimental Psychology: Applied.

#psikologi #faktapsikologi #kerjakelompok #tugaskelompok #mahasiswa #ruangpikir
```

## Caption TikTok
```
Ngerasa paling banyak kerja di kelompok? Semua anggota juga ngerasa gitu 😮‍💨

Riset Schroeder dkk. (2016): klaim semua anggota dijumlah selalu > 100%, tim 8 orang bisa 140%! Caranya: sebutin dulu kerjaan yang lain.

Kirim ke grup kelompokmu 📩

#psikologi #kerjakelompok #tugaskelompok #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Jujur aja: di kelompokmu kamu tipe yang mana? 1) si paling kerja 2) si penyelamat deadline 3) si "aku bagian doa" 😆 Jawab pakai angka 👇
```

## Story promosi
```
Kerja kelompok, kok aku terus yang capek? 😮‍💨
Ternyata semua anggota ngerasa gitu. Ada risetnya.
Tonton video barunya 👇
```
Stiker polling: `Di kelompokmu kamu tipe... si paling kerja / si ngilang`

## Judul YouTube Shorts
```
Kerja kelompok kok aku paling capek? Ini kata riset psikologi #shorts
```

## Waktu upload
Minggu malam 19.00–21.00 WIB (sebelum minggu kuliah/kerja mulai, saat banyak yang lagi ngerjain tugas kelompok) atau Senin–Kamis 18.00–20.00 WIB.

## Produksi
Folder `video-engine/ep25_kerja-kelompok/` (dibangun dari EP24): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`). Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 104 BPM, `TR = 0`). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper baru: `pie3d()`, `laptop()`, `team()`, `task_card()`, `counter()`, `bar_pct()`, `group_phone()`; plus helper EP14–EP24 (`cafe_bg()`, `hero()`, `say()`, `thought()`, `stamp()`, `extrude()`, `research_card()`, `mini_person()`, `avatar()`, `check_mark()`, `plane_icon()`).
