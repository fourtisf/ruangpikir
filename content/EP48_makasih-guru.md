# EP 48 — Makasih ke guru, kok canggung? (Spesial Hari Guru, 25 November)

Status: **sudah diproduksi** — `videos/ruang-pikir-ep48-makasih-guru.mp4` (±46 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/makasih-guru/`.
Format: seri **"kalimat yang tepat"** (rumus EP24: kalimat disensor lalu dibuka di tengah video) + momen **Hari Guru Nasional 25 November**. Dipilih ALFA dari usulan ide 17 Nov 2026.
Ajakan: "Tulis di komentar: guru siapa yang paling kamu ingat?" + kirim pesan ke guru.
**Upload: 24 November malam atau 25 November pagi** (ikut tagar #HariGuruNasional).
Gaya: premium **"kelas malam + surat cahaya"**: papan tulis kapur yang menulis sendiri, jendela cahaya bulan, tokoh Bu Guru berkerudung, surat tulisan tangan, pesawat kertas bercahaya.

## Riset
- **Sumber:** Kumar, A., & Epley, N. (2018). Undervaluing gratitude: Expressers misunderstand the consequences of showing appreciation. *Psychological Science, 29*(9), 1423–1435. https://doi.org/10.1177/0956797618772506
  - Peserta menulis surat terima kasih untuk orang yang berjasa dalam hidup mereka, lalu menebak reaksi penerimanya. Penerima kemudian melaporkan reaksi sebenarnya.
  - Penulis **melebih-lebihkan rasa canggung** penerima dan **meremehkan seberapa senang** (positif) penerima.
  - Penulis juga meremehkan penilaian penerima tentang kehangatan dan terutama **kompetensi** mereka, yaitu seberapa pas kata-katanya.
  - Eksperimen terakhir: kekhawatiran soal kompetensi (kata-kata) adalah salah satu penghalang orang mengungkapkan terima kasih, padahal penerima lebih merasakan ketulusannya.
- **Jujur soal batasnya:**
  - Penerima di riset ini orang-orang yang berjasa dalam hidup peserta, **tidak khusus guru**. Video tidak mengklaim penerimanya guru.
  - Tidak semua penerima bisa dihubungi peneliti; ada kemungkinan yang kurang terkesan tidak ikut menjawab.
  - Klaim "penerima lebih terkejut" tidak dipakai karena laporan media berbeda-beda soal ini.
  - Alat ukur CANGGUNG dan hati SENANG di video **ilustratif** (tanpa angka).
  - Kalimat "Bu, makasih ya. Sampai sekarang, aku masih ingat pelajaran dari Ibu." adalah **saran praktis**, bukan kalimat yang diuji di riset. Ini dicatat di web.
- Tidak ada data Francesca Gino.

## Judul di layar
```
Makasih ke guru, kok [canggung?]
```

## Hook (detik 0–3)
- Suara: **"Ada guru yang masih kamu ingat sampai sekarang? Mungkin dia nggak pernah tahu."**
- Visual sejak frame pertama:
  - kelas malam, kapur menulis sendiri **"Makasih, Bu Guru"** di papan tulis;
  - tokoh Bu Guru (DULU, disorot lampu hangat) dan tokoh kamu (SEKARANG) memegang ponsel;
  - gelembung chat "Bu, makasih ya..." diketik lalu dihapus → **NGGAK JADI DIKIRIM**.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Ada guru yang masih kamu ingat sampai sekarang? Mungkin dia nggak pernah tahu."),
    (3.91, "Tahun dua ribu delapan belas, Amit Kumar dan Nicholas Epley minta orang nulis surat makasih."),
    (9.41, "Penulisnya ngira, penerimanya bakal canggung, dan nggak sesenang itu."),
    (13.57, "Hasilnya? Penerimanya jauh lebih senang dari dugaan, dan canggungnya jauh lebih kecil."),
    (18.94, "Kita juga takut kata-katanya aneh. Padahal yang kerasa, tulusnya."),
    (23.43, "Jadi jangan cuma dibatin. Kirim satu pesan ini ke gurumu."),
    (28.12, "Bu, makasih ya. Sampai sekarang, aku masih ingat pelajaran dari Ibu."),
    (32.62, "Selamat Hari Guru! Tulis di komentar: guru siapa yang paling kamu ingat?"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
- Transkripsi persis dan instruksi gaya tidak ikut terbaca.
- Ada jeda dramatis ±0,7 dtk sebelum kalimat yang dibuka.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–3.9 | **Hook:** papan tulis "Makasih, Bu Guru" tertulis kapur, Bu Guru (DULU) + tokoh (SEKARANG) dengan ponsel, gelembung "Bu, makasih ya..." dihapus → **NGGAK JADI DIKIRIM**. |
| 3.9–9.4 | Kartu ARSIP RISET 2018 · Amit Kumar & Nicholas Epley · Psychological Science · 4 EKSPERIMEN → surat tulisan tangan "Untuk Bu Guru," yang tertulis pulpen emas + chip SURAT MAKASIH. |
| 9.4–13.6 | **DIKIRA PENULIS:** alat ukur CANGGUNG naik tinggi, hati kaca SENANG cuma terisi sedikit, tokoh penulis berkeringat memegang surat. |
| 13.6–18.9 | HASILNYA? → **KENYATAAN:** hati SENANG terisi hampir penuh (garis putus-putus DIKIRA jauh di bawah), Bu Guru membaca surat sambil berpendar, jarum CANGGUNG turun → **JAUH LEBIH KECIL**. |
| 18.9–23.4 | Surat besar dengan coretan & garis merah + kaca pembesar (**KATA-KATANYA ANEH?**) → coretan hilang, surat berpendar, hati muncul → **TULUSNYA**. |
| 23.4–32.6 | Pikiran "(dalam hati) makasih, Bu..." dicoret + stempel **JANGAN CUMA DIBATIN** → kartu emas PESAN UNTUK GURUMU buram + gembok → jeda → dibuka dengan sinar: **"Bu, makasih ya. Sampai sekarang, aku masih ingat pelajaran dari Ibu."** → pesawat kertas bercahaya terbang ke Bu Guru yang berpendar + **TERKIRIM** ✓. |
| 32.6–36.6 | Papan tulis **SELAMAT HARI GURU**, Bu Guru & tokoh terhubung benang cahaya + kolom komentar mengetik "Bu Rina, wali kelas 5 SD!" + GURU SIAPA YANG PALING KAMU INGAT?. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Guru favoritmu mungkin nggak pernah tahu
```
Alternatif: `Selamat Hari Guru! Kirim 1 pesan ini` · `Makasih ke guru, kok canggung?`

## Caption Instagram
```
Ada guru yang masih kamu ingat sampai sekarang? Mungkin dia nggak pernah tahu 🥹

Tahun 2018, Amit Kumar dan Nicholas Epley minta orang nulis surat makasih. Penulisnya ngira, penerimanya bakal canggung, dan nggak sesenang itu.

Hasilnya? Penerimanya jauh lebih senang dari dugaan, dan canggungnya jauh lebih kecil. Kita juga takut kata-katanya aneh. Padahal yang kerasa, tulusnya 💛

Jadi jangan cuma dibatin. Kirim satu pesan ini ke gurumu:
"Bu, makasih ya. Sampai sekarang, aku masih ingat pelajaran dari Ibu." 📩
(Ganti "Bu" jadi "Pak" kalau gurumu bapak-bapak 😊)

Selamat Hari Guru! 🍎
💬 Tulis di komentar: guru siapa yang paling kamu ingat?
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Kumar & Epley (2018), Psychological Science. Kalimatnya saran praktis, bukan kalimat yang diuji di riset.

#HariGuruNasional #HariGuru #psikologi #faktapsikologi #terimakasihguru #ruangpikir
```

## Caption TikTok
```
Guru favoritmu mungkin nggak pernah tahu 🥹

Riset 2018: kita ngira ucapan makasih bakal canggung. Padahal penerimanya jauh lebih senang dari dugaan.

Kirim ini ke gurumu: "Bu, makasih ya. Sampai sekarang, aku masih ingat pelajaran dari Ibu." 📩

Selamat Hari Guru! Guru siapa yang paling kamu ingat? 👇

#HariGuruNasional #HariGuru #psikologi #terimakasihguru #ruangpikir
```

## Komentar pertama (pin)
```
Aku paling ingat wali kelas SD yang sabar banget ngajarin aku baca 🥹 Kamu? Tulis nama & pelajarannya di bawah, siapa tahu gurumu baca 👇
```

## Story promosi
```
Selamat Hari Guru! 🍎
Ada guru yang masih kamu ingat sampai sekarang?
Mungkin dia nggak pernah tahu. Tonton video barunya 👇
```
Stiker pertanyaan: `Guru yang paling kamu ingat siapa?` (jawabannya bisa dibagikan ulang ke story).

## Judul YouTube Shorts
```
Selamat Hari Guru! Kirim 1 pesan ini ke guru favoritmu (riset psikologi) #shorts
```

## Waktu upload
**Senin 24 November jam 19.00–21.00 WIB** (supaya sudah naik saat 25 November ramai), atau **Selasa 25 November jam 06.00–08.00 WIB**. Di jam pertama, balas komentar dengan "udah kamu kirim ke beliau belum?" supaya penonton benar-benar mengirim pesan.

## Produksi
- **Folder:** `video-engine/ep48_makasih-guru/` (dibangun dari EP47).
- **Render:**
  - Render ulang dengan `./build.sh`; suara sudah ada di `vo/` (9 baris di `lines.json`).
  - Buat ulang suara dengan `./build.sh --voice`, lalu cek durasi (target ≤ 55 dtk) dan ubah anchor di `vo/lines.json`.
  - `DUR` 42, jeda antarbaris 0,35 dtk, encode CRF 26.
- **Lagu orisinal:** `audio.py` di folder ini (variasi EP22: 92 BPM, `TR = 3`, hangat).
- **Versi tanpa musik:**
  1. `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`
  2. Mux ke video yang sudah ada (loudnorm ±−14 LUFS).
- **Helper baru:**
  - `classroom_bg()` — kelas malam: jendela cahaya bulan + papan tulis kapur berbingkai kayu.
  - `chalk_text()` — tulisan kapur yang tertulis dari kiri ke kanan + batang kapur di ujungnya.
  - `hand_line()` + `letter3d()` — surat tulisan tangan krem: baris tertulis bertahap + pulpen emas; `squig` = coretan & garis merah.
  - `light_plane()` — pesawat kertas bercahaya dengan pita cahaya.
  - `meters()` — alat ukur CANGGUNG + hati SENANG + garis DIKIRA.
- **Dipakai juga:** `ibu()` (EP29) sebagai Bu Guru, `hero()`, `mini_phone()`, `spot()`, `awk_gauge()`, `glass_heart()`, `research_card()`, `secret_card2()`, `thought()`, `cross()`, `stamp()`, `magnifier()`, `heart_shape()`, `check_mark()`, `bond()`, `sparks()`, `rays()`, `plane_icon()`, `ui_panel()`, `studio()`, `extrude()`.
