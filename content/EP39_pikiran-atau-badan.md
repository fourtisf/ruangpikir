# EP 39 — Obrolan garing, kok jadi seru? (Pikiran atau badan umur 30?)

Status: **sudah diproduksi** — `videos/ruang-pikir-ep39-pikiran-atau-badan.mp4` (±47 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/pikiran-atau-badan/`.
Format: **format EP17** (episode viral 20,9K: satu pertanyaan konkret + penonton menjawab di komentar), dengan pertanyaan pilihan A/B supaya komentar lebih ramai. Visual **UI premium** seperti EP38: kartu emas 3D, tombol kuis, panel energi obrolan, kolom komentar.

## Riset
- **Sumber utama:** Aron, A., Melinat, E., Aron, E. N., Vallone, R. D., & Bator, R. J. (1997). The experimental generation of interpersonal closeness. *Personality and Social Psychology Bulletin, 23*(4), 363–377.
  - Pertanyaan nomor 6 dari 36: *"If you were able to live to the age of 90 and retain either the mind or body of a 30-year-old for the last 60 years of your life, which would you want?"*
  - Dua orang asing bergantian menjawab pertanyaan yang makin pribadi. Mereka merasa lebih dekat dibanding yang berbasa-basi.
- **Uji ulang:** Sprecher, S. (2021). Closeness and other affiliative outcomes generated from the Fast Friends procedure. *Journal of Social and Personal Relationships* (doi 10.1177/0265407521996055).
  - Pasangan orang asing diacak ke tugas 36 pertanyaan, tugas basa-basi, atau kenalan bebas.
  - Tugas 36 pertanyaan menghasilkan rasa dekat dan hasil positif lain yang lebih besar, **terutama dibanding basa-basi**.
- **Pendukung (untuk caption/web):** Leckfor, Wood, Slatcher & Orehek (2025). "Not such fast friends." *JSPR, 42*(11), 3272–3294.
  - 286 pasang orang asing.
  - Obrolan pribadi lebih bikin terhubung daripada basa-basi.
  - Ngobrol langsung lebih kuat daripada lewat chat, karena lewat chat orang lebih sedikit bercerita tentang diri sendiri.
- **Jujur soal batasnya:**
  - Yang diukur adalah rasa dekat setelah satu sesi ngobrol, bukan persahabatan jangka panjang.
  - Klaim populer "36 pertanyaan bikin jatuh cinta" **tidak** dipakai.
  - Kalimat soal pertanyaan disederhanakan ("pikiran atau badan umur 30").
- **Ilustratif:** persen energi obrolan, ring rasa dekat, dan isi chat. Tidak ada data Francesca Gino.

## Judul di layar
```
Obrolan garing, kok [jadi seru?]
```

## Hook (detik 0–3)
- Suara: **"Mau obrolan nggak garing? Coba satu pertanyaan ini."** (rumus EP14/EP17)
- Visual sejak frame pertama:
  - kafe malam, dua tokoh kapsul canggung + panel **ENERGI OBROLAN 10% · GARING** dengan garis datar;
  - kartu emas 3D **"?"** jatuh berputar dengan sinar, lalu dibalik (detik ±4): **"Kalau bisa hidup sampai 90 tahun, kamu pilih punya PIKIRAN atau BADAN umur 30?"**;
  - slider **UMUR 30 → 90**, lalu tombol kuis **PIKIRAN** (ikon otak) dan **BADAN** (ikon dumbel).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Mau obrolan nggak garing? Coba satu pertanyaan ini."),
    (3.45, "Kalau bisa hidup sampai sembilan puluh tahun, kamu pilih punya pikiran, atau badan umur tiga puluh?"),
    (8.93, "Ini salah satu dari tiga puluh enam pertanyaan buatan psikolog Arthur Aron."),
    (12.67, "Pertanyaannya makin lama makin pribadi, dan dijawab gantian oleh dua orang asing."),
    (16.81, "Tahun dua ribu dua puluh satu, Susan Spreker menguji ulang. Mereka jadi lebih dekat, dibanding yang cuma basa-basi."),
    (22.68, "Soalnya pertanyaan kayak gini bikin kita cerita soal diri sendiri, bukan soal cuaca."),
    (27.62, "Jadi kalau obrolan mulai garing, lempar pertanyaan ini, terus jawab gantian."),
    (32.04, "Kamu pilih mana: pikiran atau badan? Tulis di komentar, terus kirim ke temanmu!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Spreker" = ejaan fonetik Sprecher untuk TTS (caption tetap ejaan asli).

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–8.9 | **Hook + pertanyaan:** panel ENERGI OBROLAN garing → kartu emas 3D "?" jatuh berputar → dibalik jadi pertanyaan 06/36 → slider UMUR 30→90 → tombol PIKIRAN / BADAN. |
| 8.9–12.7 | Teks 3D **36 PERTANYAAN** + 36 kartu mini bernomor berputar 3D (warna ringan → pribadi), kartu **06** maju + PSIKOLOG ARTHUR ARON · 1997. |
| 12.7–16.8 | Slider RINGAN → PRIBADI, kartu dilempar bolak-balik di antara dua tokoh (nomornya makin besar), segmented GILIRAN KAMU / GILIRAN DIA, DUA ORANG ASING. |
| 16.8–22.7 | Kartu ARSIP RISET 2021 · Susan Sprecher · Journal of Social and Personal Relationships, lalu dasbor RASA DEKAT SETELAH NGOBROL: ring BASA-BASI vs 36 PERTANYAAN (mahkota, LEBIH DEKAT). |
| 22.7–27.6 | Dua panel chat: BASA-BASI ("panas ya hari ini", "udah makan?") vs CERITA DIRI ("aku pilih badan", "kenapa?", "pengen naik gunung", "sampai tua!") + bar JADI KENAL; awan cuaca dicoret. |
| 27.6–32.0 | Kafe: kartu 06 dilempar ke meja, "pikiran dong!" / "badan! biar bisa jalan-jalan", benang kedekatan menyala, ENERGI OBROLAN naik ke 92% · SERU. |
| 32.0–36.6 | Kartu polling "Kamu pilih mana?" + tombol PIKIRAN / BADAN, kolom komentar mengetik "aku pilih ", tombol kirim, KIRIM KE TEMANMU. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Umur 90: kamu pilih PIKIRAN atau BADAN umur 30?
```
Alternatif: `Pertanyaan biar obrolan nggak garing` atau `Jawab di komentar: pikiran atau badan?`

## Caption Instagram
```
Mau obrolan nggak garing? Coba satu pertanyaan ini 👇

"Kalau bisa hidup sampai 90 tahun, kamu pilih punya PIKIRAN atau BADAN umur 30?" 🧠💪

Ini salah satu dari 36 pertanyaan buatan psikolog Arthur Aron. Pertanyaannya makin lama makin pribadi, dan dijawab gantian oleh dua orang asing.

Tahun 2021, Susan Sprecher menguji ulang: mereka jadi lebih dekat, dibanding yang cuma basa-basi ✨

Soalnya pertanyaan kayak gini bikin kita cerita soal diri sendiri, bukan soal cuaca. Bonus: riset 2025 nemuin ngobrol langsung lebih bikin dekat daripada lewat chat.

Jadi kalau obrolan mulai garing, lempar pertanyaan ini, terus jawab gantian.

💬 Kamu pilih mana: PIKIRAN atau BADAN? Tulis di komentar!
📩 Kirim ke temanmu, tanya dia pilih apa
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Aron dkk. (1997), PSPB; Sprecher (2021), JSPR; Leckfor dkk. (2025), JSPR.

#psikologi #faktapsikologi #ngobrol #pertanyaan #pdkt #ruangpikir
```

## Caption TikTok
```
Umur 90 tahun, kamu pilih punya PIKIRAN atau BADAN umur 30? 🧠💪

Ini pertanyaan dari 36 pertanyaan psikolog Arthur Aron. Diuji ulang tahun 2021: bikin orang asing lebih dekat dibanding basa-basi ✨

Jawab di komentar 👇 terus kirim ke temanmu!

#psikologi #ngobrol #pertanyaan #pdkt #ruangpikir
```

## Komentar pertama (pin)
```
Aku tim BADAN biar bisa jalan-jalan sampai tua 😆 Kamu tim PIKIRAN 🧠 atau BADAN 💪? Jawab + kasih alasannya 👇
```

## Story promosi
```
Umur 90, kamu pilih punya pikiran atau badan umur 30? 🤔
Pertanyaan dari psikolog ini bikin obrolan langsung seru.
Tonton video barunya 👇
```
Stiker polling: `PIKIRAN 🧠 / BADAN 💪`

## Judul YouTube Shorts
```
Umur 90: pilih pikiran atau badan umur 30? Pertanyaan psikolog biar obrolan nggak garing #shorts
```

## Waktu upload
Malam 19.00–21.00 WIB, paling pas Jumat–Minggu (waktu nongkrong). Balas komentar di jam pertama dengan pertanyaan balik ("kenapa pilih itu?") supaya komentarnya makin ramai.

## Produksi
- **Folder:** `video-engine/ep39_pikiran-badan/` (dibangun dari EP38).
- **Render:**
  - Render ulang dengan `./build.sh`; suara sudah ada di `vo/`.
  - Buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`).
  - `DUR` 42, jeda antarbaris 0.35 dtk, encode CRF 26.
- **Lagu orisinal:** `audio.py` di folder ini (variasi EP22: 108 BPM, `TR = 0`).
- **Versi tanpa musik:**
  1. `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`
  2. Mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14).
- **Helper baru:**
  - `q_card3d()` — kartu pertanyaan emas 3D: belakang "?", muka pertanyaan; `flip` membalik.
  - `brain_icon()`, `dumbbell_icon()`.
  - `choice_btn()` — tombol kuis premium.
  - `mini_q()` — kartu mini bernomor.
  - `card_col()` — warna ringan → pribadi.
  - `age_slider()` — slider umur 30→90.
  - `energy_panel()` — ENERGI OBROLAN garing → seru.
- **Dipakai juga:** semua helper UI EP38 (`ui_panel()`, `ui_ring()`, `ui_seg()`, `ui_text()`), plus `cafe_bg()`, `table()`, `bond()`, `hero()`, `say()`, `msg()`, `research_card()`, `extrude()`, `crown()`, `rain_cloud()`, `plane_icon()`, `avatar()`.
- **Catatan:** kelompok adegan di episode ini cuma 8 (A–G + J); `b.DRAWERS` disesuaikan.
