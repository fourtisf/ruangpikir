# EP 49 — Mau negur, kok jadi berantem?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep49-negur-tanpa-berantem.mp4` (±53 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/negur-tanpa-berantem/`.
Format: seri **"kalimat yang tepat"** dengan rumus EP24 (±20K views): konflik hubungan sehari-hari + "jangan cuma …, coba kalimat ini" + kalimat disensor lalu dibuka + "kirim ke orang yang …". Dipilih ALFA (18 Nov 2026) dengan permintaan **visual premium + hook kuat**.
Gaya: premium **"duel kalimat"**: dua tokoh berhadapan di studio, blok kata kaca 3D yang dilempar, perisai kaca defensif yang retak, benang cahaya yang menegang merah dan bergetar, waktu membeku ("rewind") ke kalimat pertama.

## Riset
- **Sumber:** Rogers, S. L., Howieson, J., & Neame, C. (2018). I understand you feel that way, but I feel this way: The benefits of I-language and communicating perspective during conflict. *PeerJ, 6*, e4831. https://doi.org/10.7717/peerj.4831
  - Peserta membaca **skenario konflik bayangan** (contoh di makalah: pasangan capek pulang kerja, sementara kamu membereskan rumah sendirian).
  - Peserta menilai kalimat pembuka yang divariasikan: bahasa "aku" vs "kamu", dan sudut pandang yang disampaikan (tidak ada / sudut pandang sendiri / sudut pandang orang lain / dua-duanya).
  - Bahasa "aku" dan menyampaikan sudut pandang sama-sama **menurunkan kesan menyerang** (hostility) dan kemungkinan penerima jadi defensif.
  - Kalimat yang dinilai **paling baik** untuk membuka obrolan konflik: bahasa "aku" + sudut pandang dua pihak, mis. "I understand why you might feel that way, but I feel this way…".
- **Jujur soal batasnya:**
  - Ini penilaian atas kalimat dalam skenario bayangan, **bukan** pengukuran pertengkaran sungguhan atau hubungan jangka panjang.
  - Jumlah peserta tidak dicantumkan karena teks lengkapnya tidak bisa diakses dari sesi ini; angka tidak dipakai di video.
  - Alat ukur TERASA MENYERANG di video **ilustratif** (tanpa angka).
  - Kalimat "Aku ngerti kenapa kamu ngerasa gitu. Tapi aku ngerasanya gini." adalah terjemahan bebas dari contoh kalimat terbaik di makalah, bukan kalimat bahasa Indonesia yang diuji.
- Tidak ada data Francesca Gino.

## Judul di layar
```
Mau negur, kok [jadi berantem?]
```

## Hook (detik 0–3)
- Suara: **"Kamu negur pasangan, ujung-ujungnya malah berantem? Mungkin yang salah kalimat pertamamu."**
- Visual sejak frame pertama:
  - blok kata kaca merah **"KAMU TUH..."** sudah melayang dan menghantam perisai kaca yang baru naik (retak + percikan + guncangan kamera);
  - benang cahaya di antara dua tokoh menegang merah dan bergetar;
  - dibalas **"KAMU JUGA!"** + stempel **BERANTEM**;
  - waktu membeku, layar meredup, blok pertama ditarik ke tengah, disorot bingkai emas → **KALIMAT PERTAMA**.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Kamu negur pasangan, ujung-ujungnya malah berantem? Mungkin yang salah kalimat pertamamu."),
    (4.97, "Tahun dua ribu delapan belas, Shane Rogers dan timnya nguji kalimat pembuka pas lagi konflik."),
    (9.27, "Misalnya: pasanganmu capek pulang kerja, dan kamu beresin rumah sendirian. Kamu pengen negur."),
    (13.9, "Hasilnya? Kalimat yang dibuka pakai kamu, terasa lebih menyerang, dan bikin orang defensif."),
    (18.47, "Yang paling nggak menyerang: pakai aku, dan sebut perasaan dua-duanya. Perasaanmu, dan perasaan dia."),
    (23.51, "Jadi jangan cuma bilang, kamu tuh. Coba kalimat ini."),
    (29.09, "Aku ngerti kenapa kamu ngerasa gitu. Tapi aku ngerasanya gini."),
    (32.6, "Kirim ke orang yang sering salah paham sama kamu. Biar ngobrolnya nggak jadi berantem."),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
- Transkripsi persis dan instruksi gaya tidak ikut terbaca.
- Versi pertama diawali "Negur pasangan…", tapi kata pembukanya kurang jelas dan durasinya cuma ±40 dtk. Diganti "Kamu negur pasangan…" dan isinya ditambah sedikit, lalu `tighten.py 0.16` supaya ≤ 55 dtk.
- Ada jeda dramatis ±0,7 dtk sebelum kalimat yang dibuka.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–5.0 | **Hook:** blok "KAMU TUH..." menghantam perisai kaca (retak, percikan, guncangan), benang tegang merah bergetar, balasan "KAMU JUGA!" + **BERANTEM** → waktu membeku, blok pertama disorot **KALIMAT PERTAMA**. |
| 5.0–9.3 | Kartu ARSIP RISET 2018 · Shane Rogers dkk. · PeerJ · SKENARIO KONFLIK → carousel 4 blok **KALIMAT PEMBUKA** ("Kamu harus bantu!", "Aku butuh bantuan.", "Kamu nggak pernah...", "Aku ngerti kamu capek...") mengorbit tokoh. |
| 9.3–13.9 | MISALNYA: tokoh di sofa + baterai hampir habis + jam 21:30 (**CAPEK PULANG KERJA**) vs tokoh menyapu dengan keranjang cucian (**SENDIRIAN**) → gelembung "..." + benang mulai tegang. |
| 13.9–18.5 | HASILNYA? → blok "KAMU..." dilempar & menghantam, benang tegang merah, alat ukur **TERASA MENYERANG** naik, perisai kaca **DEFENSIF** naik. |
| 18.5–23.5 | Blok emas "AKU..." melayang, perisai turun, benang kendur jadi emas, alat ukur turun; bola **PERASAANMU** (emas) + **PERASAAN DIA** (merah muda) bertemu jadi hati → **DUA-DUANYA**. |
| 23.5–32.6 | Blok "KAMU TUH..." dicap **JANGAN** lalu pecah → kartu emas KALIMAT PEMBUKA buram + gembok → jeda → dibuka dengan sinar: **"Aku ngerti kenapa kamu ngerasa gitu. Tapi aku ngerasanya gini."**, dua tokoh di bawahnya mendekat, perisai hilang, benang kendur emas. |
| 32.6–36.6 | **KIRIM KE DIA**: panel kirim kaca (Pacar / Sahabat / Kakak / Teman kos) + ketukan jari + centang → pesawat kertas bercahaya → dua tokoh berpelukan → **NGGAK JADI BERANTEM**. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Negur malah berantem? Ganti kalimat pertamamu
```
Alternatif: `Jangan bilang "kamu tuh..." pas negur` · `1 kalimat biar negur nggak jadi berantem`

## Caption Instagram
```
Kamu negur pasangan, ujung-ujungnya malah berantem? Mungkin yang salah kalimat pertamamu 😶

Tahun 2018, Shane Rogers dan timnya nguji kalimat pembuka pas lagi konflik. Misalnya: pasanganmu capek pulang kerja, dan kamu beresin rumah sendirian.

Hasilnya? Kalimat yang dibuka pakai "kamu" terasa lebih menyerang, dan bikin orang defensif 🛡️

Yang paling nggak menyerang: pakai "aku", dan sebut perasaan dua-duanya. Perasaanmu, dan perasaan dia 💛

Jadi jangan cuma bilang "kamu tuh…". Coba kalimat ini:
"Aku ngerti kenapa kamu ngerasa gitu. Tapi aku ngerasanya gini." 🤝

📩 Kirim ke orang yang sering salah paham sama kamu
💬 Kamu sering kelepasan bilang "kamu tuh…" nggak? Jujur di komentar
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Rogers, Howieson & Neame (2018), PeerJ. Risetnya memakai skenario konflik bayangan.

#psikologi #faktapsikologi #hubungan #pasangan #komunikasi #ruangpikir
```

## Caption TikTok
```
Negur pasangan malah berantem? Mungkin yang salah kalimat pertamamu 😶

Riset 2018: kalimat yang dibuka pakai "kamu" terasa lebih menyerang. Yang paling aman: pakai "aku" + sebut perasaan dua-duanya.

Coba: "Aku ngerti kenapa kamu ngerasa gitu. Tapi aku ngerasanya gini." 🤝

Kirim ke orang yang sering salah paham sama kamu 👇

#psikologi #hubungan #pasangan #komunikasi #ruangpikir
```

## Komentar pertama (pin)
```
Jujur aku sering kelepasan "kamu tuh selalu…" terus jadi panjang 😭 Kamu tim mana: langsung "kamu tuh…" atau udah bisa "aku ngerasa…"? 👇
```

## Story promosi
```
Negur malah jadi berantem? 😶
Mungkin yang salah kalimat pertamamu.
Tonton video barunya 👇
```
Stiker polling: `Pernah negur malah jadi berantem? Sering 🙋 / Jarang 🙅`

## Judul YouTube Shorts
```
Negur pasangan malah berantem? Ganti kalimat pertamamu (riset psikologi) #shorts
```

## Waktu upload
Kamis atau Jumat malam, 19.00–21.00 WIB, saat banyak orang lagi santai bareng pasangan atau teman kos. Di jam pertama, balas komentar dengan "biasanya kalimat apa yang bikin kalian langsung panas?" supaya diskusinya hidup.

## Produksi
- **Folder:** `video-engine/ep49_negur/` (dibangun dari EP48).
- **Render:**
  - Render ulang dengan `./build.sh`; suara sudah ada di `vo/` (9 baris di `lines.json`, sudah `tighten.py 0.16`).
  - Buat ulang suara dengan `./build.sh --voice`, lalu cek durasi (target ≤ 55 dtk) dan ubah anchor di `vo/lines.json`.
  - `DUR` 42, jeda antarbaris 0,35 dtk, encode CRF 26.
- **Lagu orisinal:** `audio.py` di folder ini (variasi EP22: 98 BPM, `TR = 1`).
- **Versi tanpa musik:**
  1. `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`
  2. Mux ke video yang sudah ada (loudnorm ±−14 LUFS).
- **Helper baru:**
  - `tension_line()` — benang cahaya: kendur emas berpendar ↔ tegang lurus merah yang bergetar + garis tegangan.
  - `glass_shield()` — perisai kaca melengkung yang naik dari lantai, bisa retak, label DEFENSIF.
  - `word_block()` — blok kaca berisi kata 3D yang dilempar.
  - `fly()` — lintasan parabola benda yang dilempar.
  - `duel()` — dua tokoh berhadapan + benang + perisai.
  - `sofa()`, `broom()`, `basket()`.
- **Dipakai juga:** `hero()`, `studio()`, `research_card()`, `battery3d()`, `dclock()`, `awk_gauge()`, `sphere()`, `heart_shape()`, `secret_card2()`, `stamp()`, `sparks()`, `rays()`, `brackets()`, `ui_panel()`, `avatar()`, `tap()`, `check_mark()`, `light_plane()` (EP48), `hug_pair()` (EP38), `extrude()`.
