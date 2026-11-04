# EP 20 — Cerita duluan, kok jadi akrab?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep20-cerita-duluan.mp4` (±46 detik, 1080×1920), halaman web `ruangpikir.id/episode/cerita-duluan/`.
Seri: Psikologi Ngobrol (format EP14/EP17/EP19 yang paling banyak ditonton) · lanjutan langsung EP17 ("saling terbuka sedikit demi sedikit, dan gantian").

## Riset
- **Sumber:** Sprecher, S., Treger, S., Wondra, J. D., Hilaire, N., & Wallpe, K. (2013). Taking turns: Reciprocal self-disclosure promotes liking in initial interactions. *Journal of Experimental Social Psychology, 49*(5), 860–866.
  - Pasangan orang asing (mahasiswa) mengobrol lewat video call (Skype, ±12 menit per obrolan, dua obrolan). Kondisi **bergantian**: saling bercerita bolak-balik. Kondisi **satu arah**: satu bercerita, yang lain mendengarkan, lalu perannya ditukar di obrolan kedua.
  - Pasangan yang bergantian lebih saling suka; pasangan satu arah tetap tidak bisa menyamai meskipun sudah bertukar peran.
  - Penjelasan: keterbukaan yang dibalas terasa sebagai kepercayaan; orang cenderung membalas keterbukaan (norma timbal balik).
- **Jujur soal batasnya:** sampel mahasiswa, obrolan singkat lewat video call. Klaim tambahan (merasa lebih dekat, lebih mirip) hanya ditemukan di ringkasan sekunder, jadi video cuma memakai "lebih saling suka". Tidak ada data Francesca Gino.

## Judul di layar
```
Cerita duluan, [kok jadi akrab]?
```

## Hook (detik 0–3)
- Suara: **"Mau dia terbuka sama kamu? Coba ini: cerita duluan."** Rumus "Mau [hasil]? Coba ini: [jawaban]" yang langsung memberi jawaban (seperti EP14).
- Visual sejak frame pertama: kafe malam, dua tokoh kapsul canggung ("...") dengan **kotak cerita emas bergembok** di meja masing-masing, meter SALING SUKA hampir nol; di "Coba ini" kotak kiri berpendar, gemboknya terbuka, tutupnya terbuka ke belakang dengan **pancaran cahaya emas** dan bola cerita naik + gelembung "aku dulu takut gelap"; lalu gembok kotak pink milik temannya ikut terbuka dan kotaknya membuka (detik ±3,3–4), meter melonjak.

## Gaya visual
"Kafe malam + kotak cerita emas": kotak emas/pink bergembok yang terbuka dengan pancaran cahaya, bola cerita bercahaya yang terbang dengan jejak, chip "kamu duluan deh" / "kamu aja duluan" + teks 3D DIEM-DIEMAN + "krik...", kartu ARSIP RISET 2013 + dua bingkai VIDEO CALL · 12 MENIT, baris GANTIAN (bola bolak-balik) vs SATU ARAH (bola satu arah, "cuma dengerin..."), hati kaca SALING SUKA 40% vs 88%, TUKAR PERAN + race bar "nggak bisa ngejar", "aku percaya sama kamu" → MEMBALAS, teks 3D "MULAI DARI HAL KECIL" + "kalau kamu?". Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Mau dia terbuka sama kamu? Coba ini: cerita duluan."),
    (3.05, "Kita sering nunggu orang lain buka diri duluan. Akhirnya, dua-duanya diem."),
    (7.27, "Tahun dua ribu tiga belas, psikolog Susan Spreker meneliti dua orang asing yang ngobrol lewat video call."),
    (13.25, "Ada yang ceritanya gantian, bolak-balik. Ada yang satu cerita terus, yang lain cuma dengerin."),
    (18.55, "Hasilnya? Yang gantian cerita, lebih saling suka."),
    (21.34, "Bahkan setelah tukar peran, yang satu arah tetap nggak bisa ngejar."),
    (25.15, "Soalnya cerita duluan itu kayak bilang: aku percaya sama kamu. Dan orang cenderung membalas."),
    (30.39, "Mulai dari hal kecil, terus tanya balik. Cerita apa yang pernah bikin kamu langsung akrab? Tulis di komentar!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Susan Spreker" = ejaan fonetik Susan Sprecher untuk TTS (caption tetap "Susan Sprecher").

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–3.1 | **Hook:** kafe, "...", kotak emas & pink bergembok → kotak emas terbuka (pancaran cahaya, bola cerita, "aku dulu takut gelap") → gembok kotak pink terbuka, meter SALING SUKA naik. |
| 3.1–7.3 | "kamu duluan deh" / "kamu aja duluan", kotak bergetar → teks 3D DIEM-DIEMAN + "krik...", meter turun. |
| 7.3–13.3 | Kartu ARSIP RISET 2013 · Sprecher dkk. · JESP + dua bingkai video call "VIDEO CALL · 12 MENIT". |
| 13.3–18.6 | Baris GANTIAN: bola cerita bolak-balik; baris SATU ARAH: bola hanya satu arah, "cuma dengerin...". |
| 18.6–21.3 | Hati kaca SALING SUKA: SATU ARAH 40% vs GANTIAN 88%. |
| 21.3–25.2 | TUKAR PERAN (tokoh bertukar tempat + panah melingkar); race bar GANTIAN vs SATU ARAH (setelah tukar peran) yang "nggak bisa ngejar". |
| 25.2–30.4 | Kotak emas terbuka, bola cerita terbang ke teman + "aku percaya sama kamu" → gembok pink terbuka, MEMBALAS, bola kembali; meter naik. |
| 30.4–36.6 | Teks 3D "MULAI DARI HAL KECIL", "aku dulu takut gelap" → "kalau kamu?"; komentar "cerita takut kucing", "pernah salah naik bus", "aib masa kecil wkwk", "cerita soal keluarga". |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Biar dia terbuka, lakukan ini
```
Alternatif: `Cerita duluan, kok jadi akrab?` atau `Jangan nunggu dia cerita duluan`

## Caption Instagram
```
Mau dia terbuka sama kamu? Coba ini: cerita duluan 🔓

Kita sering nunggu orang lain buka diri duluan. "Kamu duluan deh." "Kamu aja duluan." Akhirnya dua-duanya diem 😶

Tahun 2013, psikolog Susan Sprecher meneliti dua orang asing yang ngobrol lewat video call. Ada yang ceritanya gantian, bolak-balik. Ada yang satu cerita terus, yang lain cuma dengerin.

Hasilnya? Yang gantian cerita lebih saling suka. Bahkan setelah tukar peran, yang satu arah tetap nggak bisa ngejar.

Soalnya cerita duluan itu kayak bilang: "aku percaya sama kamu." Dan orang cenderung membalas 🤍

Mulai dari hal kecil, terus tanya balik: "kalau kamu?"

💬 Cerita apa yang pernah bikin kamu langsung akrab sama orang? Tulis di komentar 👇
📩 Kirim ke teman yang suka nunggu dichat duluan.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Sprecher dkk. (2013), Journal of Experimental Social Psychology.

#psikologi #faktapsikologi #ngobrol #pdkt #pertemanan #ruangpikir
```

## Caption TikTok
```
Mau dia terbuka? Cerita duluan, terus tanya balik 🔓

Riset Sprecher dkk. (2013): dua orang asing yang gantian cerita lebih saling suka dibanding yang satu arah, bahkan setelah tukar peran.

Cerita apa yang bikin kamu langsung akrab? 👇

#psikologi #ngobrol #pdkt #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Aku duluan: dulu aku takut gelap sampai SMP, harus tidur lampu nyala 😅 Kalau kamu, cerita apa yang bikin langsung akrab? 👇
```

## Story promosi
```
"Kamu duluan deh." "Kamu aja duluan." 😶
Ternyata kuncinya: cerita duluan.
Tonton video barunya 👇
```

## Judul YouTube Shorts
```
Biar dia terbuka sama kamu, lakukan ini dulu (riset psikologi) #shorts
```

## Produksi
Folder `video-engine/ep20_cerita-duluan/` (dibangun dari EP19): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`). Encode CRF 26. Helper baru: `story_box()` (kotak cerita emas: `open_` tutup ke belakang + pancaran cahaya, `lock` gembok terbuka, `glow`), `padlock()`, `orb()`, `fly_orb()` (bola cerita terbang dengan jejak), `call_frame()` (bingkai video call), `race_bar()`; plus helper EP14–EP19 (`cafe_bg()`, `two_chat()`, `glass_heart()`, `conn_meter(label=...)`, `loop_arrow()`, `say()`, `extrude()`, `comment()`, `research_card(tag=...)`).
