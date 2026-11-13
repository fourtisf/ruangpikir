# EP 41 — Tahu masa depan, kok malah nyesel? (Bola kristal)

Status: **sudah diproduksi** — `videos/ruang-pikir-ep41-bola-kristal.mp4` (±51 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/bola-kristal/`.
Format: **seri 36 pertanyaan** (lanjutan EP39 yang viral & EP40): satu pertanyaan + jawab di komentar + plot twist riset. Gaya **"lab hologram"**.

## Riset
- **Pertanyaan:** Aron, A., Melinat, E., Aron, E. N., Vallone, R. D., & Bator, R. J. (1997). *PSPB, 23*(4), 363–377.
  - Pertanyaan nomor 13 (awal set II): *"If a crystal ball could tell you the truth about yourself, your life, the future or anything else, what would you want to know?"*
- **Plot twist:** Gigerenzer, G., & Garcia-Retamero, R. (2017). Cassandra's regret: The psychology of not wanting to know. *Psychological Review, 124*(2), 179–196. (Max Planck Institute for Human Development.)
  - >2.000 orang dewasa di Jerman dan Spanyol.
  - **86–90%** tidak mau tahu kejadian buruk di masa depan (mis. kapan/kenapa meninggal, apakah pernikahan akan berakhir).
  - **40–77%** juga tidak mau tahu kejadian baik (mis. hasil pertandingan, hadiah Natal).
  - Hanya **±1%** yang konsisten ingin tahu semuanya.
  - Penjelasan peneliti: **antisipasi rasa menyesal** + menjaga kejutan/rasa penasaran untuk hal yang menyenangkan.
  - Satu-satunya pengecualian: jenis kelamin bayi (lebih banyak yang mau tahu).
- **Jujur soal batasnya:**
  - Data dari survei (pertanyaan hipotetis), bukan perilaku nyata.
  - Peserta dari Jerman & Spanyol.
  - "Hampir 9 dari 10" merujuk ke kejadian buruk; "1%" merujuk ke yang konsisten mau tahu semua kejadian.
  - Contoh "jodohku siapa? aku sukses nggak?" ilustratif.
- **Ilustratif:** kerumunan hologram, grid 100 orang (1 menyala = 1%), 10 siluet. Tidak ada data Francesca Gino.

## Judul di layar
```
Tahu masa depan, kok [malah nyesel?]
```

## Hook (detik 0–3)
- Suara: **"Satu pertanyaan ini bikin semua orang mikir lama."**
- Visual sejak frame pertama:
  - siluet hologram dengan cincin berputar di kepala (MIKIR...), lalu muncul siluet lain;
  - **bola kristal hologram raksasa** naik di sorot cahaya, dengan kabut cahaya warna-warni berputar di dalamnya;
  - **SATU KEBENARAN** + label **DIRIMU · HIDUPMU · MASA DEPANMU** mengorbit bola, lalu "?" muncul di dalam bola dengan kilatan.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Satu pertanyaan ini bikin semua orang mikir lama."),
    (3.19, "Kalau ada bola kristal yang bisa kasih tahu satu kebenaran, tentang dirimu, hidupmu, atau masa depanmu, kamu mau tahu apa?"),
    (9.87, "Ini pertanyaan nomor tiga belas, dari tiga puluh enam pertanyaan psikolog Arthur Aron."),
    (14.11, "Mungkin kamu langsung kepikiran: jodohku siapa? Aku bakal sukses nggak?"),
    (17.93, "Tapi tahun dua ribu tujuh belas, Gerd Gigerenser dan timnya nanya lebih dari dua ribu orang."),
    (22.4, "Hasilnya? Hampir sembilan dari sepuluh nggak mau tahu kabar buruk masa depannya. Yang selalu pengen tahu, cuma satu persen."),
    (28.07, "Soalnya kita takut menyesal setelah tahu, dan pengen hidup tetap ada kejutannya."),
    (32.29, "Kamu sendiri, mau tahu apa? Atau mending nggak usah? Tulis di komentar, terus kirim ke temanmu!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
- "Gigerenser" = ejaan fonetik Gigerenzer.
- Suara menambahkan "eh … ya" secara alami ("eh, jodohku siapa ya?"), jadi caption ikut disesuaikan.
- Baris 7 awalnya "takut nyesel", tapi terdengar seperti "takutnya sel", jadi diganti "takut menyesal".

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–9.9 | **Hook + pertanyaan:** siluet hologram MIKIR... → bola kristal raksasa naik + SATU KEBENARAN → label DIRIMU / HIDUPMU / MASA DEPANMU mengorbit → "?" di dalam bola. |
| 9.9–14.1 | Menara spiral 36 kartu di sorot emas, kartu **13** ungu keluar dengan sinar + PSIKOLOG ARTHUR ARON · 1997. |
| 14.1–17.9 | Bola kristal di tengah + kartu pertanyaan masa depan mengorbit ("jodohku siapa?", "aku sukses nggak?", "kapan nikah?", "umurku sampai berapa?", "kerjaanku nanti apa?") → teks 3D JODOHKU SIAPA? lalu AKU SUKSES NGGAK?. |
| 17.9–22.4 | Kartu ARSIP RISET 2017 · Gigerenzer & Garcia-Retamero · Max Planck Institute · Psychological Review → teks 3D **2.000+ ORANG** + kerumunan hologram dalam perspektif + JERMAN · SPANYOL. |
| 22.4–28.1 | HASILNYA? → **9 DARI 10**: 10 siluet, 9 menutup mata dan berubah merah muda (NGGAK MAU TAHU KABAR BURUK) → YANG SELALU PENGEN TAHU: grid 100 ikon orang, satu menyala emas → **CUMA 1%**. |
| 28.1–32.3 | Bola kristal ditutup tirai cahaya (TAKUT MENYESAL) → bergeser ke kiri, kotak kejutan emas muncul dan tutupnya meloncat (PENGEN ADA KEJUTAN). |
| 32.3–36.6 | Layar terbelah KAMU PILIH MANA?: MAU TAHU (bola kristal) vs NGGAK USAH (kotak kejutan) + kolom komentar mengetik "aku mau tahu " + KIRIM KE TEMANMU. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Bola kristal bisa kasih tahu 1 hal. Kamu mau tahu apa?
```
Alternatif: `Tahu masa depan, kok malah nyesel?` · `9 dari 10 orang nggak mau tahu ini`

## Caption Instagram
```
Satu pertanyaan ini bikin semua orang mikir lama 👇

"Kalau ada bola kristal yang bisa kasih tahu SATU kebenaran, tentang dirimu, hidupmu, atau masa depanmu, kamu mau tahu apa?" 🔮

Ini pertanyaan nomor 13 dari 36 pertanyaan psikolog Arthur Aron.

Mungkin kamu langsung kepikiran: jodohku siapa? Aku bakal sukses nggak? 😆

Tapi tahun 2017, Gerd Gigerenzer dan timnya nanya lebih dari 2.000 orang. Hasilnya? Hampir 9 dari 10 nggak mau tahu kabar buruk masa depannya. Yang selalu pengen tahu, cuma 1% 😳

Soalnya kita takut menyesal setelah tahu, dan pengen hidup tetap ada kejutannya ✨

💬 Kamu sendiri mau tahu apa? Atau mending nggak usah? Tulis di komentar!
📩 Kirim ke temanmu, tanya dia mau tahu apa
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Aron dkk. (1997), PSPB; Gigerenzer & Garcia-Retamero (2017), Psychological Review.

#psikologi #faktapsikologi #pertanyaan #masadepan #deeptalk #ruangpikir
```

## Caption TikTok
```
Bola kristal bisa kasih tahu SATU kebenaran tentang hidupmu. Kamu mau tahu apa? 🔮

Plot twist: riset 2017 (2.000+ orang), hampir 9 dari 10 nggak mau tahu kabar buruk masa depannya. Cuma 1% yang selalu pengen tahu 😳

Kamu tim mau tahu atau nggak usah? 👇

#psikologi #pertanyaan #masadepan #deeptalk #ruangpikir
```

## Komentar pertama (pin)
```
Aku mau tahu… nanti aku bahagia nggak 🥹 Kalau kamu? Mau tahu apa, atau tim "nggak usah, biar jadi kejutan"? 👇
```

## Story promosi
```
Bola kristal bisa kasih tahu 1 hal tentang masa depanmu. Kamu mau tahu apa? 🔮
Plot twist: kebanyakan orang malah nggak mau tahu.
Tonton video barunya 👇
```
Stiker polling: `Mau tahu 🔮 / Nggak usah 🎁`

## Judul YouTube Shorts
```
Bola kristal bisa kasih tahu 1 hal tentang masa depanmu. Kamu mau tahu apa? (riset psikologi) #shorts
```

## Waktu upload
Malam 19.00–21.00 WIB, paling pas Jumat–Minggu. Balas komentar di jam pertama dengan "kenapa itu?" atau "kalau ternyata jawabannya nggak enak?" supaya diskusinya hidup.

## Produksi
- **Folder:** `video-engine/ep41_bola-kristal/` (dibangun dari EP40).
- **Render:**
  - Render ulang dengan `./build.sh`; suara sudah ada di `vo/`.
  - Buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`).
  - `DUR` 42, jeda antarbaris 0.35 dtk, encode CRF 26.
- **Lagu orisinal:** `audio.py` di folder ini (variasi EP22: 90 BPM, `TR = 3`).
- **Versi tanpa musik:**
  1. `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`
  2. Mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14).
- **Helper baru:**
  - `crystal_ball()` — bola kristal: alas emas, kabut cahaya berputar, `veil` tirai menutup, `q` tanda tanya.
  - `gift_box()` — kotak kejutan dengan pita; `hop` mengangkat tutup.
  - `holo_crowd()` — kerumunan ikon orang dalam perspektif.
  - `person_grid()` — grid 10×10, satu menyala = 1%.
- **Dipakai juga:** helper lab hologram EP39 v2 & EP40, `thought_ring()`, `eye_icon()`, `research_card()`, `extrude()`.
- **Catatan transkripsi:** kuota model flash habis (429) dan model lain sibuk (503). Pakai `gemini-3.5-flash-lite` untuk satu file gabungan; kalau ada frasa yang terdengar ambigu (mis. "takut nyesel"), ganti kalimatnya supaya jelas.
