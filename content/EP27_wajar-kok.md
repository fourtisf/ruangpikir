# EP 27 — Teman curhat, jangan bilang ini

Status: **sudah diproduksi** — `videos/ruang-pikir-ep27-wajar-kok.mp4` (±54 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/wajar-kok/`.
Seri: **"Kalimat yang tepat"** (lanjutan EP24 minta maaf & EP26 makasih udah nunggu): kafe malam, dua tokoh kapsul, kalimat jawaban disensor dulu lalu dibuka, ajakan "kirim ke…".

## Riset
- **Sumber:** Shenk, C. E., & Fruzzetti, A. E. (2011). The impact of validating and invalidating responses on emotional reactivity. *Journal of Social and Clinical Psychology, 30*(2), 163–183.
  - Mahasiswa mengerjakan tugas hitungan yang dibuat menegangkan, lalu menerima tanggapan yang **memvalidasi** atau **meremehkan (invalidasi)** perasaan mereka.
  - Kelompok yang diremehkan: emosi negatif, detak jantung, dan aktivitas keringat kulit **naik** seiring waktu.
  - Kelompok yang divalidasi: emosi negatif tidak naik dan **detak jantung turun**; keringat kulit naik lebih landai.
- **Jujur soal batasnya:** satu eksperimen laboratorium dengan mahasiswa (rata-rata kelompok, bukan aturan untuk semua orang). Kalimat "gitu doang kok sedih" / "udah, lupain aja" adalah contoh sehari-hari, bukan kalimat persis di eksperimen. Monitor detak jantung di video ilustratif tanpa angka. Tidak ada data Francesca Gino.

## Judul di layar
```
Teman curhat, [jangan bilang ini]
```

## Hook (detik 0–3)
- Suara: **"Teman curhat, jangan bilang: gitu doang kok sedih. Coba ganti pakai kalimat ini."**
- Visual sejak frame pertama: kafe malam, tokoh kapsul menangis "aku capek banget...", di atasnya **monitor kaca PERASAAN DIA** dengan garis detak jantung hijau. Temannya menjawab **"gitu doang kok sedih"** → garis detak **melonjak merah** + alarm + panah naik → gelembung itu **dicoret** → muncul kartu emas **KALIMAT PENGGANTI** yang buram + bergembok (dibuka di detik ±40 video).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Teman curhat, jangan bilang: gitu doang kok sedih. Coba ganti pakai kalimat ini."),
    (4.62, "Kita kira itu nenangin, atau bilang: udah, lupain aja. Padahal bisa bikin perasaannya makin nggak enak."),
    (9.98, "Tahun dua ribu sebelas, psikolog Chad Syenk dan Alan Frusetti menguji ini."),
    (14.09, "Peserta diberi soal hitungan yang bikin stres, lalu ditanggapi dengan dua cara."),
    (17.75, "Hasilnya? Yang perasaannya diremehkan, emosinya makin buruk dan detak jantungnya naik. Yang divalidasi, detak jantungnya justru turun."),
    (24.59, "Validasi itu bukan berarti setuju. Cuma bilang, perasaanmu masuk akal."),
    (28.95, "Jadi lain kali teman curhat, coba bilang: wajar kamu ngerasa gitu. Baru dengerin lagi."),
    (33.95, "Kirim video ini ke teman yang paling sering kamu curhatin!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Chad Syenk dan Alan Frusetti" = ejaan fonetik untuk TTS (caption tetap "Chad Shenk dan Alan Fruzzetti"). Suara pertama terlalu lambat (78 dtk, banyak jeda) sehingga dibuat ulang.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–4.6 | **Hook:** curhat "aku capek banget...", monitor PERASAAN DIA hijau → "gitu doang kok sedih" → merah + alarm, dicoret, kartu KALIMAT PENGGANTI buram. |
| 4.6–10.0 | Teman mengira "aku nenangin nih", gelembung "gitu doang", "udah, lupain aja", "semangat dong!" → hati LEGA terkuras 50% → 12% + MAKIN NGGAK ENAK. |
| 10.0–14.1 | Kartu ARSIP RISET 2011 · Shenk & Fruzzetti · JSCP. |
| 14.1–17.8 | Lembar SOAL HITUNGAN + timer melingkar, tokoh berkeringat → dua cabang DIREMEHKAN / DIVALIDASI. |
| 17.8–24.6 | HASILNYA? → monitor DIREMEHKAN (detak cepat merah, EMOSI ↑ DETAK ↑) vs DIVALIDASI (detak melambat hijau, DETAK ↓). |
| 24.6–29.0 | VALIDASI ≠ SETUJU → kartu ✓ "perasaanmu masuk akal". |
| 29.0–34.0 | Kartu dibuka: **"Wajar kamu ngerasa gitu."**, tokoh yang curhat berhenti menangis + telinga BARU DENGERIN LAGI. |
| 34.0–36.6 | Kartu "COBA SEKARANG" + panel KIRIM KE (sahabat, pacar, kakak, teman kos) + pesawat kertas + TERKIRIM. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Teman curhat? Jangan bilang ini
```
Alternatif: `Stop bilang "gitu doang kok sedih"` atau `1 kalimat buat teman yang lagi curhat`

## Caption Instagram
```
Teman curhat, jangan bilang "gitu doang kok sedih" 🙅 Coba ganti pakai kalimat ini.

Kita kira itu nenangin, atau bilang "udah, lupain aja". Padahal bisa bikin perasaannya makin nggak enak 😶

Tahun 2011, psikolog Chad Shenk dan Alan Fruzzetti menguji ini. Peserta diberi soal hitungan yang bikin stres, lalu ditanggapi dengan dua cara.

Hasilnya? Yang perasaannya diremehkan, emosinya makin buruk dan detak jantungnya naik 📈 Yang divalidasi, detak jantungnya justru turun 📉

Validasi itu bukan berarti setuju. Cuma bilang: perasaanmu masuk akal 🤍

Jadi lain kali teman curhat, coba bilang: "Wajar kamu ngerasa gitu." Baru dengerin lagi.

📩 Kirim ke teman yang paling sering kamu curhatin!
💬 Kalimat apa yang paling bikin kamu lega pas lagi curhat? 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Shenk & Fruzzetti (2011), Journal of Social and Clinical Psychology.

#psikologi #faktapsikologi #curhat #pertemanan #kesehatanmental #ruangpikir
```

## Caption TikTok
```
Teman curhat? Jangan bilang "gitu doang kok sedih" 🙅

Riset Shenk & Fruzzetti (2011): yang diremehkan, detak jantungnya naik. Yang divalidasi, justru turun. Coba bilang: "Wajar kamu ngerasa gitu." 🤍

Kirim ke teman curhatmu 📩

#psikologi #curhat #pertemanan #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Kalimat yang paling bikin aku lega pas curhat: "wajar kok, aku dengerin" 🤍 Kalau kamu? Kalimat apa yang paling bikin kamu lega? 👇
```

## Story promosi
```
Pernah curhat terus dibilang "gitu doang"? 😶
Ada riset soal ini. Coba ganti pakai kalimat ini.
Tonton video barunya 👇
```
Stiker polling: `Pas curhat, kamu paling butuh... didengerin / dikasih solusi`

## Judul YouTube Shorts
```
Teman curhat? Jangan bilang "gitu doang", bilang ini kata riset psikologi #shorts
```

## Waktu upload
Malam 20.00–22.00 WIB (jam orang curhat/chat-an), 2–3 hari setelah EP26.

## Produksi
Folder `video-engine/ep27_wajar-kok/` (dibangun dari EP26): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`; cek tempo — kalau total > 60 dtk buat ulang). Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 94 BPM, `TR = -1`). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper baru: `monitor()`, `worksheet()`; plus `secret_card()`, `glass_heart()`, `research_card()`, `ear()`, `tear()`, `heart_big()`, `ecg_path()`, `cafe_bg()`, `hero()`, `say()`, `thought()`, `avatar()`, `plane_icon()`.
