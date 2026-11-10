# EP 35 — Dia cuek, kok makin kepikiran?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep35-digantungin.mp4` (±53 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/digantungin/`.
**Visual versi 2 (premium):** dirombak setelah ALFA bilang v1 "visualnya jelek": studio lampu sorot + lantai pantul, ponsel DM 3D melayang, bandul hati kaca berisi cairan di ujung rantai, carousel profil 3D, tiga bandul hati kondisi, orbit kartu pikiran, kartu dibuka dengan sinar. Suara, naskah, dan timing sama dengan v1.
Format: topik gebetan (paling banyak dikirim ke teman) + kalimat/pertanyaan disensor lalu dibuka (rumus EP24).

## Riset
- **Sumber:** Whitchurch, E. R., Wilson, T. D., & Gilbert, D. T. (2011). "He loves me, he loves me not . . .": Uncertainty can increase romantic attraction. *Psychological Science, 22*(2), 172–175. (University of Virginia & Harvard.)
  - **47 mahasiswi** melihat profil Facebook **4 mahasiswa laki-laki** yang katanya sudah melihat profil mereka dan menilai seberapa suka.
  - Kondisi: diberi tahu cowok-cowok itu **sangat menyukai** mereka, menyukai **biasa saja**, atau **tidak diberi kepastian** (bisa suka banget, bisa biasa).
  - Hasil: peserta yang **tidak diberi kepastian paling tertarik**, bahkan lebih tertarik daripada yang diberi tahu "disukai banget". Mereka juga **paling sering memikirkan** cowok-cowok itu, dan ada bukti awal bahwa seringnya memikirkan inilah yang menjelaskan naiknya rasa tertarik.
- **Jujur soal batasnya:** studi kecil, peserta perempuan, hanya ketertarikan awal pada orang asing (bukan hubungan yang sudah berjalan); beberapa ulasan menyarankan membacanya sebagai temuan awal. Pertanyaan "Aku suka dia, atau cuma penasaran?" adalah saran refleksi dari temuan ini, bukan intervensi yang diuji. Nama cowok (Raka, Dimas, Bima, Arya), chat, angka "47x hari ini", dan batang di video ilustratif. Tidak ada data Francesca Gino.

## Judul di layar
```
Dia cuek, kok [makin kepikiran?]
```

## Hook (detik 0–3)
- Suara: **"Dia cuek, kok kamu makin kepikiran? Mungkin kamu bukan lagi jatuh cinta. Kamu lagi digantungin."**
- Visual sejak frame pertama: ponsel DM **"dia"**: "lagi apa?", "udah makan belum?" → dibalas **"oke"**, gelembung **mengetik...** muncul lalu hilang tanpa pesan, status online ↔ "terakhir dilihat baru saja", meter **KEPIKIRAN** naik (5x → 47x hari ini), tokoh cemas → hati **JATUH CINTA?** dicoret → hati dengan tanda tanya **tergantung di tali dan berayun** (**DIGANTUNGIN**) → kartu emas **TANYA DIRI SENDIRI** buram + gembok (dibuka di detik ±40 video).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Dia cuek, kok kamu makin kepikiran? Mungkin kamu bukan lagi jatuh cinta. Kamu lagi digantungin."),
    (6.22, "Tahun dua ribu sebelas, peneliti Erin Witchurch dan timnya menguji ini."),
    (9.74, "Mahasiswi melihat profil empat cowok, yang katanya udah lihat profil mereka juga."),
    (13.65, "Ada yang dibilang: cowok-cowok itu suka banget sama kamu. Ada yang: biasa aja. Dan ada yang: nggak jelas."),
    (19.55, "Hasilnya? Yang paling tertarik justru yang nggak jelas. Bahkan lebih dari yang disukai banget."),
    (24.14, "Soalnya ketidakpastian bikin kita mikirin dia terus. Dan makin sering dipikirin, makin kerasa suka."),
    (29.52, "Jadi sebelum baper, tanya diri sendiri: aku suka dia, atau cuma penasaran?"),
    (34.12, "Kirim video ini ke teman yang lagi digantungin!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Witchurch" = ejaan fonetik Whitchurch untuk TTS (caption tetap ejaan asli).

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–6.2 | **Hook (v2):** studio lampu sorot, tokoh berbaring gelisah, ponsel DM 3D melayang: "lagi apa?" → "oke", "mengetik..." muncul lalu hilang; kotak kaca KEPIKIRAN 1x → 47x; bandul hati kaca turun berayun (JATUH CINTA? → teks 3D **DIGANTUNGIN**), kartu TANYA DIRI SENDIRI terbang miring 3D, buram + gembok. |
| 6.2–9.7 | Kartu ARSIP RISET 2011 · Whitchurch, Wilson & Gilbert · Univ. of Virginia · Harvard · Psychological Science → teks 3D **47 MAHASISWI** + 47 hati berdenyut. |
| 9.7–13.7 | Carousel 3D 4 kartu profil cowok berputar di bawah sorot lampu + mata + KATANYA UDAH LIHAT PROFILMU. |
| 13.7–19.6 | MEREKA DIBILANG "DIA ITU...": tiga bandul hati kaca di palang: SUKA BANGET (emas, penuh), BIASA AJA (biru, setengah), NGGAK JELAS (merah muda, "?", cairan naik-turun, berayun). |
| 19.6–24.1 | HASILNYA? → SEBERAPA TERTARIK?: hati NGGAK JELAS terisi penuh + mahkota + sinar, dua hati lain meredup, LEBIH DARI YANG DISUKAI BANGET. |
| 24.1–29.5 | Rantai NGGAK PASTI → KEPIKIRAN → MAKIN SUKA, kepala dengan kartu pikiran yang mengorbit ("dia suka nggak ya?", "kok cuma 'oke'?", "tadi dia lihat story-ku"), bandul RASA SUKA terisi. |
| 29.5–34.1 | Kartu 3D dibuka dengan sinar: **"Aku suka dia, atau cuma penasaran?"** + bandul hati berhenti berayun, tokoh tenang, gelembung SUKA? / PENASARAN?. |
| 34.1–36.6 | Kartu "SEBELUM BAPER, TANYA" + KIRIM KE (bestie, teman kos, sepupu, teman kelas) + TERKIRIM. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Dia cuek, kok makin kepikiran?
```
Alternatif: `Kamu bukan jatuh cinta, kamu digantungin` atau `Dibales "oke" doang tapi kepikiran?`

## Caption Instagram
```
Dia cuek, kok kamu makin kepikiran? 🙃 Mungkin kamu bukan lagi jatuh cinta. Kamu lagi digantungin.

Tahun 2011, peneliti Erin Whitchurch dan timnya menguji ini. Mahasiswi melihat profil 4 cowok, yang katanya udah lihat profil mereka juga.

Ada yang dibilang: cowok-cowok itu suka banget sama kamu. Ada yang: biasa aja. Dan ada yang: nggak jelas.

Hasilnya? Yang paling tertarik justru yang nggak jelas. Bahkan lebih dari yang disukai banget 😳

Soalnya ketidakpastian bikin kita mikirin dia terus. Dan makin sering dipikirin, makin kerasa suka 💭

Jadi sebelum baper, tanya diri sendiri: "Aku suka dia, atau cuma penasaran?" 🤔

📩 Kirim ke teman yang lagi digantungin
💬 Kamu tim "suka beneran" atau "cuma penasaran"? 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Whitchurch, Wilson & Gilbert (2011), Psychological Science.

#psikologi #faktapsikologi #gebetan #digantungin #baper #ruangpikir
```

## Caption TikTok
```
Dia cuek, kok makin kepikiran? 🙃

Riset (Whitchurch dkk. 2011): orang paling tertarik justru pas NGGAK JELAS dia suka balik atau nggak. Sebelum baper, tanya: "Aku suka dia, atau cuma penasaran?" 🤔

Kirim ke teman yang lagi digantungin 📩

#psikologi #gebetan #digantungin #baper #ruangpikir
```

## Komentar pertama (pin)
```
Dibales "oke" doang, tapi kepikiran seharian 😭 Jujur, kamu tim "suka beneran" atau "cuma penasaran"? 👇
```

## Story promosi
```
Dia cuek, tapi kok kamu makin kepikiran? 🙃
Ternyata ada risetnya. Mungkin kamu cuma digantungin.
Tonton video barunya 👇
```
Stiker polling: `Lagi digantungin? Iya 😭 / Nggak dong 😎`

## Judul YouTube Shorts
```
Dia cuek, kok makin kepikiran? Kata riset psikologi, kamu mungkin cuma digantungin #shorts
```

## Waktu upload
Malam 20.00–22.00 WIB (jam chat-an dan galau), paling pas Jumat–Sabtu malam.

## Produksi
Folder `video-engine/ep35_digantungin/` (dibangun dari EP34): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`). `DUR` 42, jeda antarbaris 0.35 dtk. Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 96 BPM, `TR = 1`). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper v2 (premium): `studio()`, `chain()`, `pend_heart()`, `phone3d()`, `carousel()`, `thought_ring()`, `three_hearts()`. Helper v1: `dm_phone()`, `hanging_heart()`, `profile_card()`, `cond_card()`; plus `msg()`, `secret_card2()`, `eye_icon()`, `head_solid()`, `loop_arrow()`, `vbar()`, `crown()`, `race_bar()`, `mini_person()`, `research_card()`, `extrude()`, `thought()`, `cross()`, `avatar()`, `plane_icon()`.
