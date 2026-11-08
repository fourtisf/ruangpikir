# EP 26 — Telat datang? Jangan minta maaf

Status: **sudah diproduksi** — `videos/ruang-pikir-ep26-makasih-nunggu.mp4` (±51 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/makasih-nunggu/`.
Seri: **"Kalimat yang tepat"** — sekuel EP24 "Minta maaf, kok nggak dimaafin?" (±20K views): kafe malam, dua tokoh kapsul, kalimat jawaban disensor dulu lalu dibuka, ajakan "kirim ke…".

## Riset
- **Sumber:** You, Y., Yang, X., Wang, L., & Deng, X. (2020). When and why saying "thank you" is better than saying "sorry" in redressing service failures: The role of self-esteem. *Journal of Marketing, 84*(2), 133–150.
  - Studi 1a–1e di berbagai situasi layanan yang mengecewakan (mis. keterlambatan): ucapan terima kasih ("terima kasih sudah bersabar") membuat pelanggan **lebih puas** daripada permintaan maaf ("maaf atas keterlambatannya").
  - Studi 2–5: mekanismenya adalah **harga diri** penerima yang naik, karena fokus bergeser dari kesalahan pihak yang telat ke kebaikan orang yang menunggu.
  - Batasan menurut penulis: untuk kegagalan yang berat, perbaikan nyata tetap syarat; keunggulan ucapan terima kasih hilang kalau masalah sudah diantisipasi sebelumnya; efeknya lebih lemah pada orang dengan narsisme rendah.
- **Jujur soal batasnya:** konteksnya layanan pelanggan (bukan janjian antarteman), jadi video menyebut "berbagai layanan yang bikin kecewa" dan menutup dengan catatan "kalau salahnya besar, tetap minta maaf dan perbaiki". Batang PUAS di video ilustratif tanpa angka. Tidak ada data Francesca Gino.

## Judul di layar
```
Telat datang? [Jangan minta maaf]
```

## Hook (detik 0–3)
- Suara: **"Telat datang? Jangan bilang maaf ya. Coba ganti pakai kalimat ini."** Situasi yang semua orang alami + larangan yang membalik kebiasaan + janji kalimat konkret.
- Visual sejak frame pertama: tokoh kapsul **berlari masuk kafe** (garis kecepatan, keringat), **jam di dinding berputar cepat** + chip merah **TELAT 15 MENIT**, temannya menunggu sambil mengetuk-ngetuk. Gelembung "maaf ya..." muncul lalu **dicoret**, kemudian muncul **kartu emas KALIMAT PENGGANTI yang tulisannya buram + gembok** (baru dibuka di detik ±37 video).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Telat datang? Jangan bilang maaf ya. Coba ganti pakai kalimat ini."),
    (4.0, "Biasanya kita langsung bilang: maaf ya, maaf banget, tadi macet."),
    (8.27, "Tahun dua ribu dua puluh, peneliti Yanfen Yo dan timnya menguji ini di berbagai layanan yang bikin kecewa."),
    (13.51, "Ada yang dibilang: maaf ya. Ada yang dibilang: makasih ya, udah sabar."),
    (17.85, "Hasilnya? Yang dibilang makasih justru lebih puas."),
    (21.15, "Soalnya kata maaf bikin fokusnya ke kesalahan kita. Kata makasih bikin fokusnya ke kebaikan dia, jadi dia merasa dihargai."),
    (27.87, "Jadi lain kali telat, bilang: makasih udah nunggu, ya. Tapi kalau salahnya besar, tetap minta maaf dan perbaiki."),
    (33.83, "Kirim video ini ke teman yang paling sering kamu bikin nunggu!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Yanfen Yo" = ejaan fonetik Yanfen You untuk TTS (caption tetap "Yanfen You").

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–4.0 | **Hook:** tokoh berlari masuk kafe, jam berputar + TELAT 15 MENIT, "maaf ya..." dicoret, kartu KALIMAT PENGGANTI buram bergembok. |
| 4.0–8.3 | Gelembung beruntun "maaf ya", "maaf banget", "sorry sorry", "tadi macet..."; teman cuma "oke...", hati SENANG datar 40%. |
| 8.3–13.5 | Kartu ARSIP RISET 2020 · You, Yang, Wang & Deng · J MKT + ikon pesanan telat, paket telat, antre lama. |
| 13.5–17.9 | Panel KELOMPOK A "maaf ya." vs KELOMPOK B "makasih ya, udah sabar." (sama-sama NUNGGU LAMA). |
| 17.9–21.2 | Batang SEBERAPA PUAS?: "MAAF YA" pendek vs "MAKASIH" panjang + mahkota + LEBIH PUAS. |
| 21.2–27.9 | Lampu sorot merah FOKUS: KESALAHANKU vs lampu sorot emas FOKUS: KEBAIKANMU + hati DIHARGAI naik ke 95% + mahkota. |
| 27.9–33.8 | Kartu dibuka: **"Makasih udah nunggu, ya."** + kartu KALAU SALAHNYA BESAR: ✓ tetap minta maaf, ✓ perbaiki. |
| 33.8–36.6 | Kartu "COBA SEKARANG" + panel KIRIM KE (sahabat, pacar, teman kantor, adik) + pesawat kertas + TERKIRIM. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Telat? Jangan minta maaf
```
Alternatif: `Telat datang? Bilang ini, bukan "maaf"` atau `Ganti "maaf ya" pakai kalimat ini`

## Caption Instagram
```
Telat datang? Jangan cuma bilang "maaf ya" 🙅 Coba ganti pakai kalimat ini.

Biasanya kita langsung bilang: "maaf ya, maaf banget, tadi macet" 😅

Tahun 2020, Yanfen You dan timnya menguji ini di berbagai layanan yang bikin kecewa. Ada yang dibilang "maaf ya", ada yang dibilang "makasih ya, udah sabar".

Hasilnya? Yang dibilang makasih justru lebih puas 👑

Soalnya kata maaf bikin fokusnya ke kesalahan kita. Kata makasih bikin fokusnya ke kebaikan dia, jadi dia merasa dihargai 🤍

Jadi lain kali telat, bilang: "Makasih udah nunggu, ya." Tapi kalau salahnya besar, tetap minta maaf dan perbaiki.

📩 Kirim ke teman yang paling sering kamu bikin nunggu!
💬 Kamu tim yang sering telat atau tim yang sering nunggu? 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: You, Yang, Wang & Deng (2020), Journal of Marketing (riset layanan pelanggan).

#psikologi #faktapsikologi #komunikasi #pertemanan #mintamaaf #ruangpikir
```

## Caption TikTok
```
Telat datang? Jangan cuma bilang "maaf ya" 🙅

Riset You dkk. (2020): yang dibilang "makasih udah sabar" lebih puas daripada yang dibilang "maaf". Coba: "Makasih udah nunggu, ya." 🤍

Kirim ke teman yang sering kamu bikin nunggu 📩

#psikologi #komunikasi #pertemanan #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Jujur: kamu tim yang sering telat ⏰ atau tim yang selalu nunggu 🧍? Tag teman yang paling sering bikin kamu nunggu 👇
```

## Story promosi
```
Telat datang, terus bilang "maaf ya"? 😅
Coba ganti pakai kalimat ini. Ada risetnya.
Tonton video barunya 👇
```
Stiker polling: `Kamu tim... sering telat / sering nunggu`

## Judul YouTube Shorts
```
Telat datang? Jangan bilang maaf, bilang ini kata riset psikologi #shorts
```

## Waktu upload
Malam 19.00–21.00 WIB, 2–3 hari setelah EP24 selagi masih naik. Di caption/story sebut "lanjutan video minta maaf" supaya penonton EP24 ikut menonton.

## Produksi
Folder `video-engine/ep26_makasih-nunggu/` (dibangun dari EP25): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`). Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 98 BPM, `TR = 1`). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper baru: `svc_icon()`, `crown()`, `spot()`, `group_panel()`; plus `secret_card()`, `big_clock()`, `glass_heart()`, `race_bar()`, `research_card()`, `cafe_bg()`, `hero()`, `say()`, `avatar()`, `plane_icon()` dari episode sebelumnya.
