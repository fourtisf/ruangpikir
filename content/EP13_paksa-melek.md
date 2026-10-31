# EP 13 — Paksa melek, kok malah ngantuk?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep13-paksa-melek.mp4` (±52 detik, 1080×1920, ±4,2 MB), halaman web `ruangpikir.id/episode/paksa-melek/`.
Seri: Trik Psikologi (format seperti EP03 & EP12) · Topik: paradoxical intention untuk susah tidur.

## Riset
- **Kenapa makin dipaksa makin susah:** Ansfield, M. E., Wegner, D. M., & Bowser, R. (1996). Ironic effects of sleep urgency. *Behaviour Research and Therapy, 34*(7), 523–531.
  - Peserta disuruh tidur secepat mungkin atau tidur kapan saja, dengan beban pikiran tinggi (musik mars Sousa) atau rendah (musik santai). Saat beban pikiran tinggi, yang disuruh tidur secepatnya **lebih lama** terlelap (ironic process). Saat beban rendah, efeknya justru kebalikannya. Karena itu naskah menyebut "saat pikirannya sibuk".
- **Trik utama:** Broomfield, N. M., & Espie, C. A. (2003). Initial insomnia and paradoxical intention. *Behavioural and Cognitive Psychotherapy, 31*(3), 313–324.
  - 34 orang dengan susah memulai tidur, 14 malam paradoxical intention (berbaring dengan mata terbuka, berusaha tetap bangun) vs kontrol. Usaha memaksa tidur dan kecemasan soal performa tidur **turun secara signifikan**; waktu terlelap yang dilaporkan sendiri **cenderung** lebih singkat; aktigrafi (alat ukur gerak) tidak menunjukkan beda signifikan.
- **Jujur soal batasnya:** sampel kecil; efek pada waktu terlelap objektif tidak terbukti, jadi naskah memakai "cenderung merasa lebih cepat terlelap". Bukan pengganti penanganan insomnia kronis; di website ada saran ke dokter/psikolog kalau berlangsung terus.

## Judul di layar
```
Paksa melek, [kok malah ngantuk]?
```

## Hook (detik 0–3)
- Suara: **"Nggak bisa tidur? Coba trik aneh ini: paksa dirimu tetap melek."** Masalah universal + trik yang terdengar terbalik (bikin penasaran dan pengen coba).
- Visual sejak frame pertama: kamar gelap jam 02:13 (jam digital merah berkedip), tokoh kapsul berbaring dengan mata melotot; gelembung pikiran berisi domba yang terus melompati pagar dengan penghitung "domba ke-1.247" yang naik terus; lalu ikon mata + teks 3D **TETAP MELEK** menghantam layar.

## Gaya visual
Penerus format tokoh kapsul (EP01/EP03/EP12) di "kamar malam": tokoh kapsul berbaring di kasur (`sleeper()`: mata melotot → kelopak berat → terpejam, headphone), jendela bulan, domba lucu + pagar, jam digital kaca, lampu alarm merah berputar ("OTAK: SIAGA!"), dua kasur eksperimen, kartu 3D TIDUR! yang dibalik jadi MELEK!, lencana TANTANGAN: TETAP MELEK, meteran tekanan & cemas yang turun. Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Nggak bisa tidur? Coba trik aneh ini: paksa dirimu tetap melek."),
    (3.56, "Soalnya, makin dipaksa tidur, otak malah makin siaga."),
    (6.43, "Tahun sembilan belas sembilan puluh enam, psikolog Daniel Wegner menguji ini."),
    (10.6, "Peserta yang disuruh tidur secepat mungkin saat pikirannya sibuk, malah lebih lama terlelap."),
    (15.59, "Nah, trik kebalikannya namanya paradoxical intention."),
    (18.46, "Tahun dua ribu tiga, Colin Espie dan timnya meminta orang yang susah tidur berbaring dengan mata terbuka, dan berusaha tetap bangun."),
    (25.61, "Hasilnya? Tekanan harus tidur hilang, cemasnya turun, dan mereka cenderung merasa lebih cepat terlelap."),
    (31.18, "Jadi malam ini, jangan paksa tidur. Tantang dirimu tetap melek, terus ceritain hasilnya di komentar!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–3.6 | **Hook:** kamar 02:13, tokoh melotot, domba melompati pagar + "domba ke-1.247" naik terus → mata + "TETAP MELEK". |
| 3.6–6.4 | Pikiran "HARUS TIDUR!", "tinggal 4 jam lagi", "besok kerja!", "kok belum ngantuk?!"; jam berlari 02:13 → 03:38; lampu alarm merah berputar, "OTAK: SIAGA!". |
| 6.4–10.6 | Kartu ARSIP RISET 1996 · Ansfield, Wegner & Bowser · Behaviour Research and Therapy. |
| 10.6–15.6 | Dua kasur: "tidur kapan aja" (terlelap, z z z, batang waktu pendek) vs "TIDUR SECEPATNYA!" + headphone musik mars (melotot, batang waktu panjang, "lebih lama"). |
| 15.6–18.5 | Kartu 3D "TIDUR!" berputar dan dibalik jadi "MELEK!" + "PARADOXICAL INTENTION (niat yang dibalik)". |
| 18.5–25.6 | Kartu ARSIP RISET 2003 · Broomfield & Espie; tokoh berbaring mata terbuka + lencana "TANTANGAN: TETAP MELEK"; kelopak mata makin berat. |
| 25.6–31.2 | Meteran TEKANAN HARUS TIDUR & CEMAS SOAL TIDUR turun; tokoh terlelap tersenyum, "terasa lebih cepat terlelap". |
| 31.2–36.6 | "paksa tidur" dicoret → "TETAP MELEK"; tokoh & domba tidur; komentar "aku coba malam ini", "beneran ngantuk wkwk", "berhasil!". |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Susah tidur? Coba paksa melek
```

## Caption Instagram
```
Nggak bisa tidur? Coba trik aneh ini: paksa dirimu tetap melek 👀

Makin dipaksa tidur, otak malah makin siaga. Tahun 1996, psikolog Daniel Wegner dan timnya menemukan: orang yang disuruh tidur secepat mungkin saat pikirannya lagi sibuk, malah lebih lama terlelap.

Trik kebalikannya namanya paradoxical intention. Tahun 2003, Broomfield & Espie meminta orang yang susah tidur berbaring dengan mata terbuka dan berusaha tetap bangun. Hasilnya: tekanan "harus tidur" hilang, cemasnya turun, dan mereka cenderung merasa lebih cepat terlelap 😴

Jadi malam ini: jangan paksa tidur. Tantang dirimu tetap melek.

💬 Coba malam ini, terus ceritain hasilnya di komentar 👇
📩 Kirim ke teman yang suka begadang padahal pengen tidur.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Ansfield, Wegner & Bowser (1996), Behaviour Research and Therapy; Broomfield & Espie (2003), Behavioural and Cognitive Psychotherapy. Kalau susah tidur terus-menerus, konsultasi ke dokter/psikolog ya 🤍

#psikologi #faktapsikologi #susahtidur #insomnia #overthinking #ruangpikir
```

## Caption TikTok
```
Susah tidur? Jangan paksa tidur. Paksa melek 👀

Makin dipaksa tidur, otak makin siaga (Ansfield, Wegner & Bowser, 1996). Trik paradoxical intention: berbaring dengan mata terbuka & berusaha tetap bangun bikin tekanan & cemas turun (Broomfield & Espie, 2003).

Coba malam ini, ceritain hasilnya 👇

#psikologi #susahtidur #insomnia #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Tantangan malam ini: matikan lampu, berbaring santai, buka mata, dan berusaha tetap melek. Besok balik ke sini: berhasil atau malah ketiduran? 😴👇
```

## Story promosi
```
Udah ngitung domba sampai ribuan? 🐑
Coba trik aneh ini: paksa dirimu tetap melek.
Tonton video barunya 👇
```

## Produksi
Folder `video-engine/ep13_paksa-melek/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`). Encode CRF 26. Helper: `sleeper()` (tokoh kapsul berbaring: `eye` melotot→terpejam, `headphones`, `glow`), `sheep()`, `fence()`, `dclock()` (jam digital kaca), `siren()` (lampu alarm berputar), `eye_icon()`, `cloud_bubble()` (gelembung pikiran awan, ekor segitiga), `night_room()`, plus `research_card()`, `plane`/`facing()` (kartu dibalik), `extrude()`, `comment()`.
