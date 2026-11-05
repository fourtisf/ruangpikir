# EP 22 — Pengen muji, kok gengsi?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep22-puji-aja.mp4` (±50 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/puji-aja/`.
Seri: Psikologi Ngobrol (format EP14/EP17/EP19–EP21).

## Riset
- **Sumber:** Zhao, X., & Epley, N. (2021). Insufficiently complimentary?: Underestimating the positive impact of compliments creates a barrier to expressing them. *Journal of Personality and Social Psychology, 121*(2), 239–256.
  - Sembilan eksperimen: peserta menulis/menyampaikan pujian tulus untuk teman atau kenalan, lalu menebak perasaan penerima; penerima ditanya langsung.
  - Pemberi pujian konsisten **meremehkan** seberapa senang penerima dan **melebih-lebihkan** seberapa canggung penerima.
  - Pemberi sibuk memikirkan susunan kata ("pas nggak?"), sedangkan penerima lebih memperhatikan kehangatan/ketulusannya.
- **Jujur soal batasnya:** video tidak memakai angka persen; batang hanya "dikira vs kenyataan". Pujian yang dimaksud adalah pujian tulus, bukan rayuan. Tidak ada data Francesca Gino.

## Judul di layar
```
Pengen muji, [kok gengsi]?
```

## Hook (detik 0–3)
- Suara: **"Pengen muji orang, tapi gengsi? Bilang aja. Dia bakal lebih senang dari yang kamu kira."** Perasaan yang sangat Indonesia ("gengsi") + perintah singkat + klaim yang bikin lega.
- Visual sejak frame pertama: kafe malam, tokoh kapsul gemetar ("gengsi ah..."), di meja ada **toples kaca bertutup emas** berisi gelembung pujian bercahaya "bajumu bagus!" yang bergetar ingin keluar; hati kaca SENANG temannya hampir kosong. Di "Bilang aja" (detik ±2,4) tutup toples terlempar, gelembung emas terbang ke teman, teman berbinar, hati kaca terisi ±90% + hati beterbangan.
- **Lagu:** lo-fi pop ceria orisinal mulai dari frame pertama (tanpa fade panjang), langsung memberi energi.

## Lagu (orisinal, bebas hak cipta)
Dibuat di `video-engine/ep22_puji-aja/audio.py` (`music()`): 96 BPM, e-piano Fmaj7–G6–Em7–Am7 dengan ketukan sinkop, bass hangat, kick/clap/hi-hat swing, melodi utama pentatonik yang catchy (berulang tiap 4 bar), chime tiap awal frasa. Volume musik dinaikkan (lebih menonjol dari episode lain) tapi tetap otomatis turun saat narasi bicara. Dicek dengan pendengar AI: "lo-fi ceria, melodi catchy, tanpa bunyi sumbang/klik, 8,5/10 untuk latar video".
- Kalau mau memakai **lagu trending TikTok/IG**, pakai file **`videos/ruang-pikir-ep22-puji-aja-tanpa-musik.mp4`** (narasi + efek suara saja, tanpa lagu orisinal, −14,5 LUFS) supaya dua lagu tidak bertabrakan. Tambahkan lagunya lewat fitur musik di aplikasi: volume **suara asli 100%**, **lagu ±10–15%**. Jangan menempelkan lagu berhak cipta ke file video.
- Lagu yang sedang naik di TikTok Indonesia per 3 Nov 2026 (Katadata, data Endless/Tokchart): "Negoro Angin" (Wahyu DTX), "onty onty" (Zia Devita), "Stop The Wedding!" (Ashe). Cek dulu nuansanya cocok dengan video yang hangat dan positif; kalau ragu, pilih dari tab rekomendasi musik TikTok yang ditandai sedang tren dan bernuansa ceria/akustik.
- Versi tanpa musik dibuat ulang dengan: `cd video-engine/ep22_puji-aja && python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14).

## Gaya visual
"Toples pujian emas": toples kaca + tutup emas yang terlempar, gelembung pujian terbang dengan jejak kilau, hati kaca berisi cairan (SENANG), chip DITAHAN + "dikira lebay", "nanti canggung", "dia mikir aneh?", kartu ARSIP RISET 2021 + "9 eksperimen", kartu kaca PUJIAN TULUS yang diketik, gelembung "dia bakal senang nggak ya?", batang dikira vs kenyataan (SENANG naik, CANGGUNG turun), kaca pembesar di atas pilihan kata vs "kamu peduli", kartu pujian sederhana + matahari hangat "HARINYA LEBIH BAIK", teks 3D "PUJI 1 ORANG" + komentar @tag. Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Pengen muji orang, tapi gengsi? Bilang aja. Dia bakal lebih senang dari yang kamu kira."),
    (5.07, "Kita sering nahan pujian. Takut dikira lebay, takut suasananya jadi canggung."),
    (9.43, "Tahun dua ribu dua puluh satu, psikolog Syuan Jao dan Nicholas Epley menguji ini."),
    (14.02, "Orang-orang disuruh nulis pujian tulus buat temannya, lalu menebak reaksinya."),
    (18.38, "Hasilnya? Yang dipuji lebih senang dari tebakan si pemuji, dan nggak secanggung yang dibayangkan."),
    (23.87, "Si pemuji sibuk mikirin kata-katanya pas atau nggak. Padahal yang diingat penerima: kamu peduli."),
    (29.3, "Jadi pujian sederhana pun udah cukup bikin harinya lebih baik."),
    (32.81, "Yuk coba sekarang: puji satu orang di kolom komentar, atau tag dia!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Syuan Jao" = ejaan fonetik Xuan Zhao untuk TTS (caption tetap "Xuan Zhao").

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–5.1 | **Hook:** "gengsi ah...", toples pujian bergetar → tutup terlempar, "bajumu bagus!" terbang ke teman, hati SENANG ±90%. |
| 5.1–9.4 | Tokoh cemas + toples "kamu keren!" yang DITAHAN; chip "dikira lebay", "nanti canggung", "dia mikir aneh?". |
| 9.4–14.0 | Kartu ARSIP RISET 2021 · Zhao & Epley · JPSP + "9 eksperimen". |
| 14.0–18.4 | Kartu PUJIAN TULUS diketik: "Kamu selalu bikin suasana jadi hangat." + TEBAKAN PEMUJI "dia bakal senang nggak ya?". |
| 18.4–23.9 | Batang SENANG (dikira rendah → kenyataan tinggi) + hati, CANGGUNG (dikira tinggi → kenyataan rendah). |
| 23.9–29.3 | "PEMUJI: KATA-KATANYA PAS?" (kaca pembesar di atas pilihan kata) vs "PENERIMA INGAT: kamu peduli" + hati kaca. |
| 29.3–32.8 | Kartu "senyummu manis", "kerjaanmu rapi", "makasih udah dengerin" + matahari hangat "HARINYA LEBIH BAIK". |
| 32.8–36.6 | Teks 3D "PUJI 1 ORANG" + komentar "@rina kamu baik banget", "@dimas makasih udah ada", "ketawamu nular @sari", "@bunda kamu kuat" + "@ TAG DIA". |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow (lagu mengalun penuh). |

## Teks cover Reels
```
Pengen muji? Bilang aja
```
Alternatif: `Gengsi muji orang? Tonton ini` atau `Pujianmu lebih berarti dari yang kamu kira`

## Caption Instagram
```
Pengen muji orang, tapi gengsi? Bilang aja 🫶 Dia bakal lebih senang dari yang kamu kira.

Kita sering nahan pujian. Takut dikira lebay, takut suasananya jadi canggung 😶

Tahun 2021, psikolog Xuan Zhao dan Nicholas Epley menguji ini. Orang-orang disuruh nulis pujian tulus buat temannya, lalu menebak reaksinya. Hasilnya? Yang dipuji lebih senang dari tebakan si pemuji, dan nggak secanggung yang dibayangkan.

Si pemuji sibuk mikirin kata-katanya pas atau nggak. Padahal yang diingat penerima: kamu peduli 🤍

Jadi pujian sederhana pun udah cukup bikin harinya lebih baik.

💬 Yuk coba sekarang: puji satu orang di kolom komentar, atau tag dia! 👇
📩 Kirim video ini ke orang yang mau kamu puji.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Zhao & Epley (2021), Journal of Personality and Social Psychology.

#psikologi #faktapsikologi #pujian #pertemanan #selflove #ruangpikir
```

## Caption TikTok
```
Pengen muji tapi gengsi? Bilang aja 🫶

Riset Zhao & Epley (2021): yang dipuji lebih senang dari tebakan si pemuji, dan nggak secanggung yang dibayangkan. Yang diingat: kamu peduli.

Puji satu orang di komentar, atau tag dia 👇

#psikologi #pujian #pertemanan #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Aku duluan: makasih buat kamu yang udah nonton sampai sini, kamu keren udah mau belajar hal baru 🫶 Sekarang giliranmu, puji/tag satu orang 👇
```

## Story promosi
```
Pengen muji orang tapi gengsi? 😶
Bilang aja. Dia bakal lebih senang dari yang kamu kira.
Tonton video barunya 👇
```

## Judul YouTube Shorts
```
Pengen muji tapi gengsi? Ini kata riset psikologi #shorts
```

## Produksi
Folder `video-engine/ep22_puji-aja/` (dibangun dari EP21): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`). Encode CRF 26. **Lagu orisinal** ada di `audio.py` folder ini (`music()` 96 BPM: `epiano()`, `lead()`, `bassline()`, `clap()`, `chime()`; `m_gain` 0.85 dengan ducking 0.58 saat narasi). Helper baru: `jar()` (toples pujian), `magnifier()`, `praise_card()`; plus helper EP14–EP21 (`cafe_bg()`, `two_chat()`, `glass_heart()`, `compare_bars()`, `thought()`, `say()`, `extrude()`, `comment()`, `research_card()`).
