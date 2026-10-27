# EP 03 — Panggil namamu, kok jadi tenang?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep03-panggil-nama.mp4` (±49 detik, 1080×1920), halaman web `ruangpikir.id/episode/panggil-namamu/`.
Seri: Kenapa Kamu Gitu? · Topik: distanced self-talk / self-distancing.

## Riset
- **Sumber utama:** Kross, E., Bruehlman-Senecal, E., Park, J., Burson, A., Dougherty, A., Shablack, H., Bremner, R., Moser, J., & Ayduk, O. (2014). Self-talk as a regulatory mechanism: How you do it matters. *Journal of Personality and Social Psychology, 106*(2), 304–324.
- 7 studi, 585 peserta. Di studi pidato, peserta menyiapkan pidato dadakan sambil bicara ke diri sendiri pakai "aku" atau pakai nama sendiri/"kamu".
- Yang pakai nama: dinilai **tampil lebih baik** oleh penilai, **terlihat lebih tenang**, dan **lebih jarang memikirkan ulang** kejadian itu sesudahnya.
- **Jujur soal batasnya:** cemasnya tidak hilang. Yang berubah adalah seberapa besar cemas itu mengganggu penampilan dan pikiran sesudahnya. Jadi naskah tidak boleh bilang "langsung tenang" atau "cemasnya hilang".

## Judul di layar
```
Panggil namamu, [kok jadi tenang]?
```

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Mau presentasi, terus deg-degan parah?"),
    (2.62, "Coba trik ini: semangati diri pakai namamu."),
    (5.38, "Bukan, 'aku pasti bisa'. Tapi, 'Dina, kamu pasti bisa.'"),
    (8.82, "Tahun 2014, psikolog Ethan Kross menguji trik ini."),
    (11.98, "Peserta siapin pidato dadakan. Ada yang ngomong ke diri pakai 'aku', ada yang pakai nama."),
    (17.39, "Yang pakai nama tampil lebih baik, dan nggak kepikiran terus sesudahnya."),
    (21.81, "Soalnya, namamu bikin kamu ngelihat diri sendiri dari luar."),
    (25.49, "Kayak lagi nyemangatin teman. Ini namanya, self-distancing."),
    (29.17, "Cemasnya nggak langsung hilang, tapi kamu lebih pegang kendali."),
    (33.08, "Tulis di komentar: kalimat semangat pakai namamu sendiri!"),
    (36.64, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Dina" hanya contoh nama (fiktif).

## Caption layar (b.CAPS, anchor sama, kata kunci dalam [..])
```python
CAPS = [
    (0.15, "Mau presentasi, terus", "[deg-degan parah]?"),
    (2.62, "Coba semangati diri", "pakai [namamu sendiri]"),
    (5.38, "Bukan \"aku bisa\", tapi", "\"[Dina], kamu bisa\""),
    (8.82, "Tahun 2014, psikolog", "[Ethan Kross] mengujinya"),
    (11.98, "Peserta siapin", "[pidato dadakan]"),
    (17.39, "Yang pakai nama", "tampil [lebih baik]"),
    (21.81, "Namamu bikin kamu lihat", "diri sendiri [dari luar]"),
    (25.49, "Ini namanya", "[self-distancing]"),
    (29.17, "Cemas tetap ada, tapi", "kamu [pegang kendali]"),
    (33.08, "Tulis di komentar", "pakai [namamu sendiri]!"),
    (36.64, "Follow [Ruang Pikir]", "biar makin kenal isi kepalamu"),
]
```

## Adegan (GROUPS) — semua ilustrasi di y 560–1200
| Waktu | Tag | Visual | SFX |
|---|---|---|---|
| 0–5.4 | PSIKOLOGI | Karakter kapsul (mood worried + sweat) di depan mic, barisan mata penonton (`watcher_eye`), garis detak jantung coral yang makin cepat. Lalu muncul pill "pakai namamu". | heart (berulang, makin cepat), whoosh, pop |
| 5.4–8.8 | COBA INI | Dua gelembung bicara. "Aku pasti bisa" redup lalu **retak dan mengecil (coral)**; "Dina, kamu pasti bisa" muncul membesar dengan glow ungu + tanda centang digambar sebagai bentuk. *Momen wow.* | crack, ding, sparkle |
| 8.8–21.8 | RISET · 2014 | Kartu riset "Ethan Kross · 2014 · 7 studi" + stamp "SELF-TALK". Lalu layar terbagi: kiri karakter "aku" (keringat, coretan kusut), kanan karakter "nama" (tenang). Dua batang "Penampilan": kanan lebih tinggi. **Tanpa angka**, cukup label "lebih baik". | card, stamp, whoosh, rise, ding |
| 21.8–33.1 | ILUSTRASI | Kamera mundur (zoom out): karakter terlihat dari luar dalam bingkai, lalu siluet "diri dari luar" bercahaya menepuk pundaknya seperti teman. Pill "self-distancing". Lalu meter cemas: jarum tetap bergerak, tapi muncul ikon kemudi/kendali mint. | zoom, shine, tick, plip |
| 33.1–36.6 | KOMENTAR | Gelembung komentar bermunculan: "Dina, kamu pasti bisa", "Raka, tarik napas dulu", "kamu udah latihan, kamu siap". | plop × 3 |
| 36.6–42 | RUANG PIKIR | Outro logo (`logo_rp.c4`) + "RUANG PIKIR" + ruangpikir.id | shine |

## Teks cover Reels
```
Sebelum presentasi, sebut namamu
```

## Caption
```
Deg-degan sebelum presentasi? Coba semangati dirimu pakai NAMAMU sendiri, bukan "aku" 🧠

Tahun 2014, psikolog Ethan Kross dan timnya di University of Michigan menguji ini lewat 7 studi dengan 585 peserta. Salah satunya: peserta harus menyiapkan pidato dadakan.

Yang bicara ke diri sendiri pakai nama ("Dina, kamu bisa") dinilai tampil lebih baik, dan lebih jarang kepikiran terus sesudahnya, dibanding yang pakai "aku".

Kenapa? Menyebut nama bikin kita melihat diri sendiri dari luar, seperti sedang menyemangati teman. Namanya self-distancing.

Cemasnya memang nggak langsung hilang, tapi kamu jadi lebih pegang kendali 🙂

💬 Tulis kalimat semangat buat dirimu, pakai namamu sendiri.
📩 Kirim ke teman yang besok mau presentasi atau wawancara.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Kross, E., dkk. (2014), Journal of Personality and Social Psychology.

#psikologi #faktapsikologi #selftalk #kesehatanmental #presentasi #selfgrowth #ruangpikir
```

## Caption TikTok
```
Besok presentasi? Coba semangati diri pakai NAMAMU, bukan "aku" 🧠

Riset Ethan Kross dkk. (2014), 7 studi dengan 585 peserta: yang menyemangati diri pakai nama sendiri tampil lebih baik saat pidato dadakan, dan lebih jarang kepikiran terus sesudahnya.

Tulis kalimat semangat pakai namamu di komentar 👇

#psikologi #selftalk #presentasi #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Contoh: "Dina, tarik napas. Kamu udah latihan, kamu siap." Sekarang giliranmu, pakai namamu sendiri 👇
```

## Story promosi
```
Besok presentasi? 😬
Coba trik pakai namamu sendiri.
Tonton video barunya 👇
```

## Produksi
Folder `video-engine/ep03_panggil-nama/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice`. Di `vo.py` tahun ditulis dengan huruf ("dua ribu empat belas") supaya dibaca benar oleh TTS; caption tetap memakai angka. Suara memakai resep EP01 (`vo_full.py`: `gemini-3.1-flash-tts-preview` + instruksi gaya EP01), sesuai suara acuan pilihan ALFA. Tanpa garis progress bar dan titik debu.
