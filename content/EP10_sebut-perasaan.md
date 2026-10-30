# EP 10 — Lagi emosi, kok bisa reda? (format 30 detik)

Status: **sudah diproduksi** — `videos/ruang-pikir-ep10-sebut-perasaan.mp4` (±29 detik, 1080×1920, ±2,6 MB), halaman web `ruangpikir.id/episode/sebut-perasaan/`.
Seri: Kenapa Kamu Gitu? · Topik: affect labeling (memberi nama emosi meredam alarm emosi di otak). Episode pertama format **30 detik**.

## Riset
- **Sumber utama:** Lieberman, M. D., Eisenberger, N. I., Crockett, M. J., Tom, S. M., Pfeifer, J. H., & Way, B. M. (2007). Putting feelings into words: Affect labeling disrupts amygdala activity in response to affective stimuli. *Psychological Science, 18*(5), 421–428.
  - fMRI: peserta melihat wajah marah/takut. Saat memberi label emosi (memilih kata yang paling cocok, mis. "marah"), respons amigdala dan area limbik lain lebih rendah dibanding cara memproses lain (memberi label gender, mencocokkan emosi tanpa kata). Prefrontal ventrolateral kanan (RVLPFC) justru lebih aktif dan berbanding terbalik dengan amigdala.
- **Pendukung (perasaan sendiri):** Kircanski, K., Lieberman, M. D., & Craske, M. G. (2012). Feelings into words: Contributions of language to exposure therapy. *Psychological Science, 23*(10), 1086–1091.
  - 88 orang yang takut laba-laba, 4 kelompok. Yang mengucapkan perasaannya saat terapi paparan menunjukkan respons kulit (reaksi tubuh) lebih rendah seminggu kemudian dibanding kelompok memaknai ulang, distraksi, atau paparan saja.
- **Jujur soal batasnya:** di Lieberman 2007 yang diberi label adalah emosi di wajah orang lain; untuk perasaan sendiri dukungannya dari Kircanski 2012. Di Kircanski, rasa takut yang dilaporkan tidak berubah, yang turun reaksi tubuh. Karena itu naskah memakai "alarm emosi di otak ikut turun" dan "lebih tenang", bukan "emosinya hilang". Bukan pengganti bantuan profesional.

## Judul di layar
```
Lagi emosi, [kok bisa reda]?
```

## Hook (detik 0–3)
- Suara: **"Emosi meledak? Cara meredamnya cuma butuh satu kalimat."** Pertanyaan relatable + janji jawaban yang sangat sederhana (open loop: kalimatnya baru dibuka di detik 19).
- Visual sejak frame pertama: bola magma emosi **meledak** (gelombang kejut, sinar, retak, layar bergetar, gelombang panas, latar memerah); lalu muncul kolom ketik kaca kosong "satu kalimat..." dengan kursor berkedip + "?" yang berdenyut di kata "satu kalimat".

## Gaya visual (beda dari EP04–EP09)
"Energi emosi": bola magma (inti bergradasi, urat cahaya berputar, korona api, retak bercahaya) yang **mendingin** jadi bola mint tenang; latar ikut memerah saat emosi panas (`heat_at`). Pemindai MRI 3D mengelilingi kepala, otak dengan amigdala merah (alarm) vs prefrontal mint (rem) + meteran, label kertas "MARAH" yang ditempel, kolom ketik kaca, panci bergetar menahan uap (dipendam) vs toples kaca berlabel "kesal" (diberi nama). Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py; format 30 detik: anchor = waktu video, DUR 29.07 di base.py)
```python
LINES = [
    (0.15, "Emosi meledak? Cara meredamnya cuma butuh satu kalimat."),
    (4.82, "Tahun dua ribu tujuh, Matthew Lieberman memindai otak orang yang melihat wajah marah."),
    (10.42, "Saat mereka memberi nama emosinya, alarm emosi di otak ikut turun."),
    (15.99, "Jadi kalau lagi kesal, bilang aja: aku lagi kesal."),
    (20.65, "Diberi nama, bukan dipendam."),
    (23.67, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```

## Adegan
| Waktu | Visual |
|---|---|
| 0–4.8 | **Hook:** bola magma emosi meledak (gelombang kejut, retak, goyang, gelombang panas); kolom ketik "satu kalimat..." + "?". |
| 4.8–10.4 | Kepala dalam cincin pemindai MRI (garis pindai lewat), amigdala memerah; kartu WAJAH MARAH / WAJAH TAKUT berganti; chip "Lieberman dkk. · 2007 · Psychological Science". |
| 10.4–16 | Otak besar: label kertas "MARAH" ditempel → amigdala meredup, prefrontal menyala mint; meteran AMIGDALA (alarm emosi) turun, REM EMOSI (prefrontal) naik. |
| 16–20.7 | Bola emosi panas lagi; kolom ketik mengetik "aku lagi kesal" → kirim → kalimatnya terbang masuk ke bola → bola mendingin jadi mint, riak cahaya, "lebih tenang". |
| 20.7–23.7 | DIBERI NAMA (toples kaca + label "kesal", tenang) vs DIPENDAM (panci bergetar, uap, lalu dicoret); catatan Kircanski dkk. (2012). |
| 23.7–29 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
1 kalimat buat redam emosi
```

## Caption Instagram
```
Emosi meledak? Cara meredamnya cuma butuh satu kalimat 🫠

Tahun 2007, psikolog Matthew Lieberman memindai otak orang yang melihat wajah marah. Saat mereka memberi nama emosinya ("marah"), amigdala, alarm emosi di otak, ikut turun. Bagian otak yang jadi "rem" emosi malah menyala.

Riset lanjutan (Kircanski dkk., 2012) juga menemukan: orang yang mengucapkan perasaannya sendiri, tubuhnya lebih tenang menghadapi hal yang ditakuti.

Jadi kalau lagi kesal, coba bilang (atau tulis): "aku lagi kesal." Bukan dipendam, bukan diledakkan, tapi diberi nama 🤍

📌 Simpan buat dipakai pas lagi emosi.
💬 Perasaan apa yang paling susah kamu sebut? Tulis di komentar 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Lieberman dkk. (2007) & Kircanski, Lieberman & Craske (2012), Psychological Science.

#psikologi #faktapsikologi #emosi #kesehatanmental #selfcare #ruangpikir
```

## Caption TikTok
```
Emosi meledak? Coba satu kalimat ini: "aku lagi kesal" 🫠

Riset Lieberman dkk. (2007): memberi nama emosi bikin alarm emosi di otak (amigdala) ikut turun. Diberi nama, bukan dipendam.

Simpan buat nanti 🤍

#psikologi #emosi #faktapsikologi #selfcare #ruangpikir
```

## Komentar pertama (pin)
```
Coba sekarang: lengkapi kalimat "aku lagi merasa ___" di komentar. Nggak usah dijelasin, cukup diberi nama 👇
```

## Story promosi
```
Lagi emosi? 🫠
Cara meredamnya cuma butuh satu kalimat.
Tonton video barunya (30 detik) 👇
```

## Produksi
Folder `video-engine/ep10_sebut-perasaan/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`). **Format 30 detik:** `DUR` di `base.py` folder ini = 29.07 (outro 23.67 + 5.4), anchor di `vo.py`/`vo/lines.json` dirapatkan ke durasi tiap baris suara (jeda 0,45–0,8 dtk), jadi waktu animasi = waktu video; `draw_captions` memakai `b.DUR - 0.3`, outro `gJ` mulai di 23.67. Encode CRF 26. Helper gaya energi emosi: `orb()` (bola magma/tenang, `cool`, `burst`, `crack_`), `heat_waves()`, `heat_at()` (latar memerah), `input_bar()` (kolom ketik), `angry_face()`, `scanner()` (cincin MRI dua belahan), `brain_lab()` (amigdala vs prefrontal), `pot()`, `jar()`.
