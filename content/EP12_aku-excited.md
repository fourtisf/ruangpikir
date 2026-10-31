# EP 12 — Mau tampil, kok deg-degan?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep12-aku-excited.mp4` (±53 detik, 1080×1920, ±4,1 MB), halaman web `ruangpikir.id/episode/aku-excited/`.
Seri: Kenapa Kamu Gitu? · Topik: memaknai ulang kecemasan sebelum tampil sebagai excited (anxiety reappraisal).
Format: **trik psikologi praktis** seperti EP03 "Panggil namamu, kok jadi tenang?" (episode paling viral, ±5.100 views): situasi tegang yang umum + satu kalimat yang bisa langsung dicoba + tokoh kapsul di panggung.

## Riset
- **Sumber utama:** Brooks, A. W. (2014). Get excited: Reappraising pre-performance anxiety as excitement. *Journal of Experimental Psychology: General, 143*(3), 1144–1158.
  - Beberapa eksperimen (karaoke, pidato di depan umum, tes matematika). Peserta yang memaknai kecemasannya sebagai excited (mis. mengucapkan "I am excited") merasa lebih excited dan tampil lebih baik dibanding yang disuruh menenangkan diri ("I am calm"/"try to remain calm").
  - Di eksperimen pidato, yang bilang "I am excited" dinilai lebih meyakinkan, kompeten, dan percaya diri.
  - Rasionalnya: cemas dan excited sama-sama keadaan "bergairah tinggi" (jantung berdebar, napas cepat), jadi lebih mudah berpindah ke excited daripada ke tenang.
- **Jujur soal batasnya:** rasa cemas yang dilaporkan peserta tidak hilang; yang berubah penampilan dan rasa excited. Angka persentase dari liputan media tidak dipakai.

## Judul di layar
```
Mau tampil, [kok deg-degan]?
```

## Hook (detik 0–3)
- Suara: **"Mau presentasi, tapi deg-degan? Jangan bilang tenang. Bilang ini."** Situasi yang dialami hampir semua orang + larangan yang membalik saran umum + open loop ("bilang ini" baru dijawab di detik ±33).
- Visual sejak frame pertama: tokoh kapsul gemetar dan berkeringat di bawah lampu sorot panggung (tirai beludru, mic), mata penonton mengawasi dari gelap, jantung berdenyut "118 BPM" + garis detak; gelembung "tenang... tenang..." dicoret, lalu gelembung emas "? ? ?".

## Gaya visual
"Panggung sinematik + tokoh kapsul premium" (penerus gaya EP01/EP03 yang paling banyak ditonton): tokoh kapsul mengilap dengan ekspresi (cemas, excited, tenang), panggung tirai beludru + lampu sorot volumetrik + lantai mengilap, mata penonton yang bisa berubah jadi hati, jantung 3D + garis detak, kartu kaca CEMAS = EXCITED, karaoke/pidato/tes matematika, gelembung "aku tenang" (biru) vs "aku excited!" (emas), batang tampil & pede, panah energi yang dibelokkan jadi petir SEMANGAT, teks 3D "AKU EXCITED!", kolom komentar. Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Mau presentasi, tapi deg-degan? Jangan bilang tenang. Bilang ini."),
    (3.81, "Soalnya di badan, cemas sama excited itu mirip banget: jantung berdebar, napas cepat."),
    (9.09, "Tahun dua ribu empat belas, psikolog Alison Wood Brooks menguji trik sederhana."),
    (14.0, "Sebelum karaoke, pidato, atau tes matematika, peserta disuruh bilang satu kalimat."),
    (19.09, "Ada yang bilang: aku tenang. Ada yang bilang: aku excited."),
    (22.69, "Hasilnya? Yang bilang aku excited tampil lebih baik, dan lebih percaya diri."),
    (27.41, "Rasa cemasnya nggak hilang. Tapi energinya dibelokkan jadi semangat."),
    (31.32, "Jadi sebelum tampil, bilang: aku excited! Tulis di komentar, kamu mau tampil di mana?"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–3.8 | **Hook:** panggung, tokoh gemetar + keringat, mata penonton, jantung 118 BPM + garis detak; "tenang... tenang..." dicoret → "? ? ?". |
| 3.8–9.1 | Kartu kaca CEMAS (tokoh cemas, merah) = EXCITED (tokoh excited, emas); jantung + garis detak yang sama di keduanya; "MIRIP BANGET DI BADAN". |
| 9.1–14 | Kartu ARSIP RISET 2014 · Alison Wood Brooks · Journal of Experimental Psychology: General. |
| 14–19.1 | Kartu KARAOKE (mic + not), PIDATO (podium), TES MATEMATIKA; gelembung "aku ...." — SATU KALIMAT. |
| 19.1–22.7 | Dua tokoh di dua lampu sorot: "aku tenang" (biru) vs "aku excited!" (emas, bercahaya). |
| 22.7–27.4 | Batang tampil & pede: "aku excited" lebih tinggi + kilau, "lebih baik & lebih pede". |
| 27.4–31.3 | Jantung tetap berdebar ("masih deg-degan"), panah energi merah dibelokkan jadi emas → petir SEMANGAT. |
| 31.3–36.6 | Kembali ke panggung: lampu jadi keemasan, tokoh tersenyum, "AKU EXCITED!" teks 3D menghantam, mata penonton jadi hati, komentar "presentasi kantor", "sidang skripsi", "interview kerja", "nyanyi di nikahan". |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Jangan bilang "tenang", bilang ini
```

## Caption Instagram
```
Mau presentasi tapi deg-degan? Jangan bilang "tenang". Bilang ini 👇

Di badan, cemas sama excited itu mirip banget: jantung berdebar, napas cepat. Bedanya cuma cara kita memaknainya.

Tahun 2014, psikolog Alison Wood Brooks menguji trik sederhana. Sebelum karaoke, pidato, atau tes matematika, peserta disuruh bilang satu kalimat: "aku tenang" atau "aku excited".

Hasilnya? Yang bilang "aku excited" tampil lebih baik dan lebih percaya diri. Rasa cemasnya nggak hilang, tapi energinya dibelokkan jadi semangat ⚡

Jadi sebelum tampil, bilang: "aku excited!" 🤍

💬 Kamu mau tampil di mana? Tulis di komentar (presentasi, sidang, interview, nyanyi?) 👇
📩 Kirim ke teman yang besok mau presentasi.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Brooks (2014), Journal of Experimental Psychology: General.

#psikologi #faktapsikologi #presentasi #percayadiri #publicspeaking #ruangpikir
```

## Caption TikTok
```
Deg-degan mau presentasi? Jangan bilang "tenang", bilang "aku excited!" ⚡

Riset Brooks (2014): yang bilang "aku excited" sebelum karaoke, pidato, dan tes matematika tampil lebih baik dan lebih pede. Cemasnya nggak hilang, energinya dibelokkan jadi semangat.

Kamu mau tampil di mana? 👇

#psikologi #presentasi #percayadiri #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Coba sekarang: ucapkan "aku excited!" tiga kali sebelum tampil berikutnya. Terus balik ke sini, ceritain hasilnya 👇
```

## Story promosi
```
Besok presentasi? 😬
Jangan bilang "tenang". Bilang ini.
Tonton video barunya 👇
```

## Produksi
Folder `video-engine/ep12_aku-excited/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`; take pertama "Deg-degan mau presentasi" terdengar tidak jelas di awal, jadi kalimat dibuka dengan "Mau presentasi, tapi deg-degan?"; selalu cek pemotongan per kalimat dengan transkripsi). Encode CRF 26. Helper: `hero()` (tokoh kapsul premium, mood worried/excited/calm/happy, `tremble`, `sweat`, `glow`), `stage()` (tirai, lantai, lampu sorot, `warm`), `ecg_path()`, `heart_big()`, `say()` (gelembung ucapan + coretan), `mic_stand()`, `note()`, `podium()`, `eyes_ring()` (mata penonton → hati), plus `research_card()`, `extrude()`, `comment()`.
