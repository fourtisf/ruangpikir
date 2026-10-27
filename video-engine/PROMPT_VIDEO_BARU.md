# Prompt untuk membuat episode baru

Salin blok di bawah ke Claude Code, isi bagian `<<...>>`, lalu kirim. Claude Code akan riset, menulis naskah, membuat suara, menggambar animasi, render, dan menulis caption.

---

```
Buat episode baru Ruang Pikir (@ruangpikir2026, ruangpikir.id) memakai mesin di video-engine/.
Baca dulu CLAUDE.md, brand/BRAND.md, dan video-engine/README.md.

TOPIK: <<contoh: "Foto rame-rame bikin kamu kelihatan lebih cakep" (cheerleader effect)>>
SERI: <<Coba Tes Ini / Kenapa Kamu Gitu? / Psikologi Cinta / Otakmu Lagi Dijebak / Mitos Psikologi>>
NOMOR EPISODE: <<03>>

LANGKAH
1. Riset: cari studi aslinya (peneliti, tahun, jurnal, angka temuan). Jangan mengarang angka. Kalau temuan
   diperdebatkan, katakan dengan jujur di naskah.
2. Naskah 9–11 kalimat (total 40–55 detik), bahasa Indonesia santai, pakai "kamu":
   - 0–3 dtk  HOOK: pertanyaan yang bikin orang merasa "ini aku banget"
   - 3–10     RELATE: situasi sehari-hari
   - 10–30    RISET: siapa, kapan, apa yang ditemukan (+ satu angka mengejutkan kalau ada)
   - 30–38    PENJELASAN: kenapa otak/perilaku kita begitu, satu istilah ilmiahnya
   - 38–46    PUNCHLINE / TIPS: satu kalimat yang nempel atau 1–3 tips
   - akhir    CTA: "Follow Ruang Pikir, ..." atau ajakan komentar
   Judul layar format "X, [kok bisa]?" (maks ±940 px lebar pada 62 px).
3. Buat folder video-engine/ep<<NN>>_<<slug>>/ dengan menyalin ep04_pura-pura-gapapa/ (tanpa vo/ dan preview/),
   tulis ulang scene di episode.py, perbarui build.sh.
4. Isi vo.py (anchor tiap kalimat dalam waktu animasi, DUR 42) dan b.CAPS (anchor sama, 2 baris,
   kata kunci dalam [..]). Caption = ringkasan pendek dari kalimat yang dibacakan.
5. Rancang 6 GROUPS (scene) dengan tag mono: PSIKOLOGI / RISET · TAHUN / ILUSTRASI / TIPS / KOMENTAR / RUANG PIKIR.
   Scene terakhir selalu outro logo (logo_rp.c4) + "RUANG PIKIR" + ruangpikir.id.
6. Gambar setiap scene dengan gaya premium yang sama dengan EP03/EP04:
   - background hitam-ungu malam, debu cahaya, aksen #7F8CFF, glow lembut, aurora + bokeh
   - kartu kaca (glass + sheen), sinar (rays), gelembung bicara, centang/silang digambar sebagai bentuk
   - karakter kapsul (person()), ikon neon, kartu riset (card + stamp), grafik batang untuk angka,
     pill label, sparkle; coral #FF6B57 untuk "salah/kaget", mint #3FD68B untuk "benar/tips"
   - minimal satu momen visual "wow" per video (transformasi, tabrakan, zoom, reveal angka)
   - semua ilustrasi di y 560–1200; jangan menutupi caption
7. Suara: Gemini TTS voice Achird dengan resep EP01 (GEMINI_API_KEY di .env): voice.sh -> vo_full.py
   (gemini-3.1-flash-tts-preview + instruksi gaya EP01, 1 request, dipotong dengan split_lines, lalu tighten.py); cek durasi tiap baris
   dan cek isinya dengan transkripsi (instruksi tidak boleh ikut terbaca); ulangi kalau aneh. Tanpa garis progress bar dan tanpa titik debu.
   Tulis tahun dengan huruf di vo.py (caption tetap angka).
8. SFX: susun build_sfx() yang menempel ke setiap kejadian visual (pop saat muncul, whoosh saat ganti scene,
   ding saat reveal, tick tiap caption).
9. QA: contact sheet ±12 frame, perbaiki tabrakan/overflow, render, cek loudness −14 LUFS.
10. Serahkan: MP4 final di videos/, dan content/EP<<NN>>_<<slug>>.md berisi teks cover (≤6 kata),
    caption IG (hook di baris pertama, cerita riset, CTA komentar + share + ruangpikir.id, sumber, 5–8 hashtag),
    komentar pin, dan teks Story.

ATURAN ISI: bukan diagnosis, tidak melabeli orang nyata, tidak membahas cara menyakiti diri,
topik berat ditutup ajakan bercerita ke psikolog/orang terdekat.
```

---

## Contoh pengisian cepat
- TOPIK: "Cinlok itu ada penjelasan ilmiahnya" (mere exposure effect, Zajonc 1968) · SERI: Psikologi Cinta · EP 03
- TOPIK: "Flash sale, kok bikin panik?" (efek kelangkaan) · SERI: Otakmu Lagi Dijebak · EP 04 (upload 5–9 November)
- TOPIK: "Hitung berapa kali bolanya dioper" (perhatian selektif, Simons & Chabris 1999) · SERI: Coba Tes Ini · EP 05
