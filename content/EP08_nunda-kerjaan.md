# EP 08 — Deadline besok, kok masih nunda?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep08-nunda-kerjaan.mp4` (±53 detik, 1080×1920, ±4,4 MB), halaman web `ruangpikir.id/episode/nunda-bukan-malas/`.
Seri: Kenapa Kamu Gitu? · Topik: prokrastinasi sebagai cara memperbaiki mood sesaat (bukan malas) + memaafkan diri.

## Riset
- **Sumber utama 1:** Sirois, F., & Pychyl, T. (2013). Procrastination and the priority of short-term mood regulation: Consequences for future self. *Social and Personality Psychology Compass, 7*(2), 115–127.
  - Artikel tinjauan: menunda adalah bentuk memperbaiki mood jangka pendek (kabur dari rasa tidak enak yang ditimbulkan tugas); biayanya ditanggung "diri di masa depan".
- **Sumber utama 2 (eksperimen):** Tice, D. M., Bratslavsky, E., & Baumeister, R. F. (2001). Emotional distress regulation takes precedence over impulse control: If you feel bad, do it! *Journal of Personality and Social Psychology, 80*(1), 53–67.
  - 3 eksperimen. Di Eksperimen 3, peserta yang sedang bad mood lebih banyak menunda dengan kegiatan iseng (*frivolous procrastination*), tapi kecenderungan itu **hilang** saat mereka percaya mood-nya "dibekukan" (tidak bisa berubah). Artinya menunda dilakukan demi merasa lebih baik.
  - Detail prosedur (latihan untuk tes, ada permainan di ruangan) baru dicek dari sumber sekunder; naskah sengaja tidak menyebut angka menit.
- **Sumber utama 3:** Wohl, M. J. A., Pychyl, T. A., & Bennett, S. H. (2010). I forgive myself, now I can study: How self-forgiveness for procrastinating can reduce future procrastination. *Personality and Individual Differences, 48*(7), 803–808.
  - 119 mahasiswa tahun pertama, diukur sebelum dua ujian tengah semester. Yang lebih memaafkan dirinya karena menunda belajar untuk ujian pertama, lebih sedikit menunda untuk ujian berikutnya (lewat berkurangnya perasaan negatif).
- **Jujur soal batasnya:** studi Wohl bersifat korelasi (bukan uji acak), jadi disampaikan sebagai temuan, bukan bukti pasti. Bukan diagnosis; menunda sesekali itu wajar. Kalau sangat mengganggu hidup terus-menerus, sarankan cerita ke orang terpercaya/psikolog (ada di website).

## Judul di layar
```
Deadline besok, [kok masih nunda]?
```

## Hook (detik 0–3)
- Suara: "Kamu nunda kerjaan bukan karena malas. Kamu lagi kabur dari rasa nggak enak." (klaim yang membantah anggapan umum + janji penjelasan).
- Visual: frame pertama laptop 3D dengan dokumen kosong "TUGAS_FINAL.docx" dan chip merah "Deadline: besok 08.00"; kata 3D raksasa **MALAS** menghantam layar (goyang + cincin benturan), lalu dicoret dan **pecah berkeping-keping** tepat di "bukan karena malas"; makhluk asap "rasa nggak enak" muncul dari laptop, ponsel meluncur masuk dengan panah "kabur".

## Gaya visual (beda dari EP04–EP07)
"Meja belajar malam": objek 3D lembut dalam perspektif (laptop, ponsel feed, stik game, balok es, balok TUGAS isometrik, tangga), cahaya lampu meja hangat dari kiri atas + pendar ungu malam, teks 3D yang pecah, makhluk asap bermata "rasa nggak enak", bola mood dengan wajah. Tetap tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Kamu nunda kerjaan bukan karena malas. Kamu lagi kabur dari rasa nggak enak."),
    (4.22, "Tugasnya bikin bosan, cemas, atau bingung mulai dari mana. Jadi kamu kabur ke HP."),
    (8.57, "Tahun dua ribu tiga belas, psikolog Sirwa dan Pitchil menyebutnya: memperbaiki mood sesaat."),
    (13.44, "Tahun dua ribu satu, peneliti bikin peserta bad mood sebelum latihan tes. Mereka malah sibuk main."),
    (18.7, "Tapi saat diyakinkan mood-nya nggak bisa berubah, mereka berhenti menunda."),
    (22.66, "Yang dikejar cuma lega sesaat. Tugasnya tetap ada, dan makin berat."),
    (26.25, "Tahun dua ribu sepuluh, riset Michael Wohl: mahasiswa yang memaafkan diri setelah menunda, lebih jarang menunda lagi."),
    (32.53, "Jadi jangan marahin diri. Maafin dulu, lalu mulai dari langkah paling kecil."),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Sirwa dan Pitchil" = ejaan fonetik Sirois & Pychyl supaya dibaca benar oleh TTS (caption tetap "Sirois & Pychyl"). Caption per frasa ada di `PHRASES` di `video-engine/ep08_nunda-kerjaan/episode.py`.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–4.2 | **Hook:** laptop 3D + deadline merah; "MALAS" menghantam, dicoret, pecah; makhluk asap "rasa nggak enak" keluar dari laptop; ponsel masuk + panah "kabur". |
| 4.2–8.6 | Bola mood "bosan" (abu, z), "cemas" (merah, keringat), "bingung" (biru, ?) keluar dari laptop; ponsel 3D dengan feed yang di-scroll cepat, penghitung "scroll: 5 menit → 2 jam 20 menit". |
| 8.6–13.4 | Kartu ARSIP RISET berputar masuk: "2013" · Sirois & Pychyl; dibalik → "MOOD REPAIR" = memperbaiki mood sesaat. |
| 13.4–18.7 | EKSPERIMEN 2001: bola mood sedih + hujan, lembar LATIHAN TES vs stik game; stik menyala, "main: 14 menit", "latihan: 0 menit". |
| 18.7–22.7 | Balok es membeku menutup bola mood ("MOOD DIBEKUKAN"); stik dicoret, soal-soal dicentang, "latihan dikerjakan". |
| 22.7–26.3 | Meter LEGA naik sesaat lalu habis; balok TUGAS isometrik membesar, memerah, lantai melengkung dan retak, "deadline makin dekat". |
| 26.3–32.5 | Kartu ARSIP RISET 2010 · Michael Wohl dkk.; lalu MARAHIN DIRI ("dasar pemalas!") vs MAAFIN DIRI ("nggak apa-apa"); batang "nunda di ujian berikutnya": panjang vs "lebih jarang". |
| 32.5–36.6 | "DASAR MALAS!" dicoret dan pecah; gelembung "nggak apa-apa, maafin dulu" + hati; tangga 3D: anak tangga pertama "buka file" menyala, bola mood melompat naik dan tersenyum. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Kamu bukan malas
```

## Caption Instagram
```
Kamu nunda kerjaan bukan karena malas. Kamu lagi kabur dari rasa nggak enak 🫠

Tugas yang bikin bosan, cemas, atau bingung mulai dari mana memunculkan perasaan nggak enak. Buka HP "sebentar" bikin lega seketika. Tahun 2013, psikolog Fuschia Sirois dan Timothy Pychyl menyebut ini memperbaiki mood sesaat.

Buktinya? Di eksperimen Tice, Bratslavsky & Baumeister (2001), peserta yang lagi bad mood lebih banyak menunda. Tapi saat mereka diyakinkan mood-nya "dibekukan" dan nggak bisa berubah, mereka berhenti menunda. Yang dikejar ternyata rasa lega, bukan malas-malasan.

Masalahnya, lega itu cuma sesaat. Tugasnya tetap ada, dan makin berat.

Terus gimana? Riset Michael Wohl dkk. (2010) pada mahasiswa: yang memaafkan dirinya setelah menunda belajar, lebih jarang menunda di ujian berikutnya. Jadi jangan marahin diri. Maafin dulu, lalu mulai dari langkah paling kecil: buka file, tulis satu kalimat 🤍

📌 Simpan buat dibaca lagi pas lagi nunda.
📩 Kirim ke teman yang deadline-nya besok tapi masih scroll.
💬 Tugas apa yang lagi kamu tunda sekarang? Ngaku di komentar 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Sirois & Pychyl (2013), Social and Personality Psychology Compass; Tice, Bratslavsky & Baumeister (2001), Journal of Personality and Social Psychology; Wohl, Pychyl & Bennett (2010), Personality and Individual Differences.

#psikologi #faktapsikologi #prokrastinasi #produktif #mahasiswa #ruangpikir
```

## Caption TikTok
```
Kamu nunda kerjaan bukan karena malas 🫠

Menunda itu cara otak kabur dari rasa nggak enak, alias memperbaiki mood sesaat (Sirois & Pychyl, 2013). Peserta yang bad mood berhenti menunda saat yakin mood-nya nggak bisa diubah (Tice dkk., 2001). Dan yang memaafkan diri lebih jarang menunda lagi (Wohl dkk., 2010).

Kirim ke teman yang deadline besok tapi masih scroll 🤍

#psikologi #prokrastinasi #faktapsikologi #mahasiswa #ruangpikir
```

## Komentar pertama (pin)
```
Langkah paling kecil versi kamu apa? Contoh: buka file aja dulu, tulis 1 kalimat, atau pasang timer 5 menit. Tulis punyamu 👇
```

## Story promosi
```
Deadline besok tapi masih scroll? 🫠
Ternyata itu bukan karena kamu malas.
Tonton video barunya 👇
```

## Produksi
Folder `video-engine/ep08_nunda-kerjaan/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`; cek transkripsi nama "Sirwa dan Pitchil"). Encode CRF 26. Helper gaya meja belajar: `laptop()` + `doc_screen()`, `phone2()` + `feed_screen()`, `blob()` (makhluk asap bermata), `shatter_text()` (teks 3D pecah), `mood_ball()`, `controller()`, `test_sheet()`, `ice()` (balok es membeku), `block3d()` (balok isometrik berlabel), `stairs()`; plus `plane`/`extrude()`/`research_card()` dari EP07 (kartu yang memudar saat `t_out`).
