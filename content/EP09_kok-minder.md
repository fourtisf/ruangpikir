# EP 09 — Scroll story, kok jadi minder?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep09-kok-minder.mp4` (±53 detik, 1080×1920, ±5,0 MB), halaman web `ruangpikir.id/episode/scroll-kok-minder/`.
Seri: Kenapa Kamu Gitu? · Topik: meremehkan emosi negatif orang lain ("cuma aku yang hidupnya berantakan").

## Riset
- **Sumber utama:** Jordan, A. H., Monin, B., Dweck, C. S., Lovett, B. J., John, O. P., & Gross, J. J. (2011). Misery has more company than people think: Underestimating the prevalence of others' negative emotions. *Personality and Social Psychology Bulletin, 37*(1), 120–135.
  - 4 studi pada mahasiswa Stanford. Peserta meremehkan seberapa sering teman sebayanya mengalami hal negatif (mis. "bertengkar hebat", "sedih karena kangen orang"), dan melebihkan hal menyenangkan (mis. jalan bareng teman, pergi ke pesta).
  - Salah tebak ini tetap ada saat menilai orang yang dikenal dekat (sahabat, teman sekamar, pacar), sebagian karena emosi negatif lebih sering disembunyikan.
  - Makin rendah tebakan soal emosi negatif orang lain, makin tinggi rasa kesepian dan rumination, dan makin rendah kepuasan hidup (korelasi).
- **Jujur soal batasnya:** hubungan dengan kesepian bersifat korelasi, jadi naskah memakai kata "cenderung". Media sering mengaitkan studi ini dengan Facebook; Facebook hanya inspirasi penelitinya, bukan yang diuji, jadi video tidak mengklaim "medsos bikin kesepian". Angka persen dari liputan media tidak dipakai.

## Judul di layar
```
Scroll story, [kok jadi minder]?
```

## Hook (detik 0–3)
- Suara: **"Kalau kamu ngerasa cuma kamu yang hidupnya berantakan, otakmu lagi salah hitung."** Langsung menyebut perasaan yang dialami banyak orang, lalu membalikkannya dengan klaim mengejutkan + janji penjelasan.
- Visual sejak frame pertama: grid profil 3×3 postingan bahagia (liburan, wisuda, jadian, konser, ngopi, gym, pesta, pantai) meluncur masuk; di tengah satu kartu abu-abu "kamu" dengan wajah sedih yang makin menonjol; chip "yang berantakan: cuma kamu" lalu **glitch merah "SALAH HITUNG"** tepat di kata "salah hitung".

## Gaya visual (beda dari EP04–EP08)
"Di balik postingan": kartu postingan medsos 3D (foto bergradasi + ikon, jumlah suka) yang bisa **dibalik** untuk menampilkan sisi yang nggak diposting ("abis nangis semalam", "takut nggak dapat kerja", "lagi sering berantem"...), grid profil, efek glitch, batang 3D tebakan vs kenyataan, wajah di balik topeng senyum, **gunung es** (yang dipamerkan di atas air vs yang disembunyikan di bawah), sorot lampu ke orang yang sendirian. Tetap tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Kalau kamu ngerasa cuma kamu yang hidupnya berantakan, otakmu lagi salah hitung."),
    (4.5, "Teman liburan, teman wisuda, teman jadian. Kamu? Rebahan sambil overthinking."),
    (8.68, "Tahun dua ribu sebelas, psikolog Alex Jordan di Stanford meneliti ini."),
    (12.48, "Mahasiswa diminta menebak: berapa banyak temannya yang lagi sedih, atau habis bertengkar?"),
    (17.32, "Hasilnya? Soal yang sedih, tebakan mereka terlalu rendah. Soal yang seneng-seneng, terlalu tinggi."),
    (22.64, "Bahkan ke sahabat dan teman sekamar sendiri."),
    (25.03, "Soalnya, rasa sedih biasanya disembunyikan. Yang dipamerkan cuma bagian bahagianya."),
    (29.54, "Dan yang paling salah tebak, cenderung paling kesepian."),
    (32.53, "Jadi kamu nggak sendirian. Coba tanya kabar temanmu hari ini, yang beneran."),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
Caption per frasa ada di `PHRASES` di `video-engine/ep09_kok-minder/episode.py`.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–4.5 | **Hook:** grid 3×3 postingan bahagia, kartu "kamu" abu-abu di tengah; chip "yang berantakan: cuma kamu" → glitch merah "SALAH HITUNG". |
| 4.5–8.7 | Kartu story 3D berputar masuk satu per satu sesuai suara: liburan, wisuda, jadian (+ hati); lalu kartu "rebahan" (kamar gelap, cahaya HP, 02.13) + pikiran "kok cuma aku ya", "hidupku gini-gini aja", "ketinggalan semua". |
| 8.7–12.5 | Kartu ARSIP RISET berputar masuk: "2011" · Alex Jordan dkk. · Stanford · PSPB. |
| 12.5–17.3 | 12 avatar mahasiswa + "berapa yang lagi susah?"; beberapa diam-diam sedih (lingkar biru + air mata), dua bertengkar (petir); "TEBAKANMU?". |
| 17.3–22.6 | Batang 3D: YANG SEDIH/BERTENGKAR tebakan rendah vs kenyataan tinggi ("terlalu rendah"); YANG SENENG-SENENG tebakan tinggi vs kenyataan lebih rendah ("terlalu tinggi"). Tanpa angka. |
| 22.6–25 | Kartu SAHABAT & TEMAN SEKAMAR: topeng senyum terangkat, di baliknya wajah sedih, "ternyata lagi susah". |
| 25–29.5 | Gunung es: kamera turun ke bawah air, label "capek", "abis nangis", "takut gagal", "lagi berantem", "kesepian" (YANG DISEMBUNYIKAN); kamera naik ke puncak dengan postingan liburan (YANG DIPAMERKAN). |
| 29.5–32.5 | Orang sendirian di bawah sorot lampu, kartu-kartu bahagia menjauh; "salah tebak ↑ → kesepian ↑". |
| 32.5–36.6 | Callback grid: semua kartu dibalik menampilkan sisi aslinya, garis mint menghubungkan "kamu" ke semuanya; chat "kamu beneran gapapa?" → "jujur, lagi capek banget" + hati. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Bukan cuma kamu yang berantakan
```

## Caption Instagram
```
Kalau kamu ngerasa cuma kamu yang hidupnya berantakan, otakmu lagi salah hitung 🫠

Scroll story: teman liburan, teman wisuda, teman jadian. Kamu? Rebahan sambil overthinking.

Tahun 2011, psikolog Alex Jordan dan timnya di Stanford meminta mahasiswa menebak berapa banyak temannya yang lagi sedih atau habis bertengkar, dan berapa yang lagi seneng-seneng.

Hasilnya: soal yang sedih, tebakan mereka terlalu rendah. Soal yang seneng-seneng, terlalu tinggi. Bahkan saat menebak sahabat dan teman sekamar sendiri.

Kenapa? Karena rasa sedih biasanya disembunyikan. Yang dipamerkan cuma bagian bahagianya. Dan yang paling salah tebak, cenderung paling kesepian.

Jadi kamu nggak sendirian. Banyak orang di sekitarmu juga lagi berjuang, cuma nggak diposting 🤍

📩 Kirim ke teman yang lagi ngerasa ketinggalan.
💬 Tanya kabar satu temanmu hari ini, yang beneran. Udah? Ceritain di komentar 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Jordan, Monin, Dweck, Lovett, John & Gross (2011), Personality and Social Psychology Bulletin.

#psikologi #faktapsikologi #insecure #overthinking #kesehatanmental #ruangpikir
```

## Caption TikTok
```
Ngerasa cuma kamu yang hidupnya berantakan? Otakmu lagi salah hitung 🫠

Riset Jordan dkk. (2011, Stanford): kita meremehkan seberapa sering orang lain lagi sedih, dan melebihkan seberapa sering mereka bahagia. Soalnya rasa sedih disembunyikan, yang dipamerkan cuma bahagianya.

Kirim ke teman yang lagi ngerasa ketinggalan 🤍

#psikologi #insecure #overthinking #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Tantangan kecil: kirim chat "kamu beneran gapapa?" ke satu teman hari ini. Kadang jawabannya bikin kaget. Udah coba? 👇
```

## Story promosi
```
Scroll story terus ngerasa ketinggalan? 🫠
Tenang, otakmu cuma lagi salah hitung.
Tonton video barunya 👇
```

## Produksi
Folder `video-engine/ep09_kok-minder/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`). Encode CRF 26. Helper gaya "di balik postingan": `post_card()` / `card3d()` (kartu postingan 3D; sisi belakang otomatis saat diputar > 90°, teks dari `HONEST`), `scene_art()` (foto bergradasi + ikon: pantai/palem, toga, pasangan, wajah), `you_card()`, `bed_card()`, `glitch_text()`, `bar3d()`, `masked()` (wajah di balik topeng senyum), `berg()` (gunung es + label), plus `avatar()`, `stander()`, `mood_ball()`, `research_card()`.
