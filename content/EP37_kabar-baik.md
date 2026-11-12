# EP 37 — Dikasih kabar baik, kok salah respon?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep37-kabar-baik.mp4` (±50 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/kabar-baik/`.
Format: seri "kalimat yang tepat" + kafe malam dua tokoh (rumus EP14/EP17) + kalimat disensor lalu dibuka (rumus EP24). Visual premium (EP35 v2/EP36): objek 3D besar, gerak fisik.

## Riset
- **Sumber utama:** Gable, S. L., Gonzaga, G. C., & Strachman, A. (2006). Will you be there for me when things go right? Supportive responses to positive event disclosures. *Journal of Personality and Social Psychology, 91*(5), 904–917.
  - Pasangan direkam di lab saat saling bercerita tentang **kejadian baik** dan **kejadian buruk**; respons pasangan dinilai.
  - **Dua bulan kemudian**, respons saat diskusi kabar baik **lebih terkait** dengan kesejahteraan hubungan dan **putus atau tidaknya** hubungan dibanding respons saat diskusi kabar buruk.
- **Studi pendahulu:** Gable, S. L., Reis, H. T., Impett, E. A., & Asher, E. R. (2004). What do you do when things go right? The intrapersonal and interpersonal benefits of sharing positive events. *JPSP, 87*(2), 228–245.
  - Empat cara merespons kabar baik:
    - aktif-membangun: antusias + bertanya;
    - pasif-membangun: datar, "wah, selamat ya";
    - pasif-merusak: mengabaikan / membelokkan ke diri sendiri;
    - aktif-merusak: mencari kekurangannya.
  - Hanya **aktif-membangun** yang terkait dengan hubungan yang lebih dekat dan memuaskan.
- **Jujur soal batasnya:**
  - Studi-studi ini **korelasional**: menunjukkan keterkaitan, bukan bukti sebab-akibat.
  - Pesertanya pasangan/mahasiswa di Amerika.
  - Kalimat "Serius?! Gimana ceritanya?" adalah contoh respons aktif-membangun, bukan kalimat yang diuji persis.
- **Ilustratif:** contoh kalimat respons, meter KEDEKATAN, dan kalender minggu.
- Tidak ada data Francesca Gino.

## Judul di layar
```
Dikasih kabar baik, kok [salah respon?]
```

## Hook (detik 0–3)
- Suara: **"Mau hubunganmu awet? Ternyata yang paling penting bukan cara kamu menghibur pas dia sedih."**
- Visual sejak frame pertama:
  - kafe malam: dua tokoh kapsul di meja, dihubungkan **benang cahaya emas** yang berdenyut;
  - **awan hujan** + payung (menghibur pas sedih), lalu **dicoret**;
  - **bola KABAR BAIK emas** muncul bersinar;
  - kartu emas **KALIMAT YANG TEPAT** buram + gembok (dibuka di detik ±38 video).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Mau hubunganmu awet? Ternyata yang paling penting bukan cara kamu menghibur pas dia sedih."),
    (5.37, "Tahun dua ribu enam, peneliti Shelly Gebel dan timnya merekam pasangan yang saling cerita."),
    (9.83, "Ada cerita sedih, ada kabar baik. Dua bulan kemudian, hubungan mereka dicek lagi."),
    (14.39, "Hasilnya? Cara merespon kabar baik lebih terkait sama awet atau putusnya hubungan."),
    (18.56, "Respon datar kayak: wah, selamat ya. Malah cerita diri sendiri. Atau nyari kurangnya. Itu nggak bikin dekat."),
    (24.54, "Yang bikin makin dekat cuma satu: respon yang antusias, terus nanya lebih lanjut."),
    (29.19, "Jadi kalau dia cerita kabar baik, coba bilang: serius? Gimana ceritanya?"),
    (33.38, "Kirim video ini ke orang yang selalu antusias dengerin ceritamu!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Gebel" = ejaan fonetik Gable untuk TTS (caption tetap ejaan asli). Baris 4 awalnya "Respon pas kabar baik", tapi "pas kabar" terdengar seperti "pasca" di transkripsi, jadi diganti "Cara merespon kabar baik".

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–5.4 | **Hook:** kafe malam, dua tokoh di meja + benang cahaya kedekatan. Awan hujan + payung, lalu dicoret. Bola KABAR BAIK emas + percikan cahaya. Kartu KALIMAT YANG TEPAT terbang miring 3D, buram + gembok. |
| 5.4–9.8 | Kartu ARSIP RISET 2006 · Gable, Gonzaga & Strachman · Journal of Personality and Social Psychology. Lalu bingkai kamera **REC** merekam pasangan yang bergantian cerita; bola sedih & bola kabar baik muncul di atas kepala. |
| 9.8–14.4 | Bola CERITA SEDIH (hujan di dalamnya) vs bola KABAR BAIK + dua tokoh pencerita. Kalender kaca MINGGU KE 1→8 + **2 BULAN**, lalu AWET? / PUTUS?. |
| 14.4–18.6 | HASILNYA? → **timbangan 3D**: piring RESPON KABAR BAIK lebih berat (turun, mahkota) vs RESPON PAS SEDIH + LEBIH TERKAIT: AWET / PUTUS. |
| 18.6–24.5 | RESPON YANG SALAH: tiga bola emas. "wah, selamat ya." → redup (DATAR). "eh, aku juga dong!" → tertutup bola abu-abu AKU (CERITA DIRI SENDIRI). "nanti capek lho" → retak (NYARI KURANGNYA). Semua dicoret: NGGAK BIKIN DEKAT. |
| 24.5–29.2 | Bola emas di tengah membesar + percikan: ANTUSIAS. Tanda tanya 3D mengorbit: NANYA LAGI. Meter KEDEKATAN 30%→95%, benang antara dua tokoh menebal. |
| 29.2–33.4 | Kartu dibuka dengan sinar: **"Serius?! Gimana ceritanya?"**. Tokoh kiri bilang "Serius?!", tokoh kanan mulai cerita "jadi gini lho...", bola dan benang makin terang. |
| 33.4–36.6 | Kartu SIMPAN KALIMAT INI + KIRIM KE (pacar, bestie, sahabat, ibu) + TERKIRIM. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Dikasih kabar baik, jangan cuma bilang "selamat ya"
```
Alternatif: `Cara cek hubunganmu bakal awet` atau `Respon ini bikin makin dekat`

## Caption Instagram
```
Mau hubunganmu awet? Ternyata yang paling penting bukan cara kamu menghibur pas dia sedih 👀

Tahun 2006, peneliti Shelly Gable dan timnya merekam pasangan yang saling cerita. Ada cerita sedih, ada kabar baik. Dua bulan kemudian, hubungan mereka dicek lagi.

Hasilnya? Cara merespon kabar baik lebih terkait sama awet atau putusnya hubungan ✨

Respon yang nggak bikin dekat:
😐 Datar: "wah, selamat ya."
🙋 Malah cerita diri sendiri: "eh, aku juga dong!"
🙄 Nyari kurangnya: "nanti capek lho"

Yang bikin makin dekat cuma satu: respon yang antusias, terus nanya lebih lanjut.

Jadi kalau dia cerita kabar baik, coba bilang: "Serius?! Gimana ceritanya?" 🥹

📩 Kirim ke orang yang selalu antusias dengerin ceritamu
💬 Kamu biasanya respon yang mana? Jujur 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Gable, Gonzaga & Strachman (2006); Gable, Reis, Impett & Asher (2004), Journal of Personality and Social Psychology.

#psikologi #faktapsikologi #hubungan #pacaran #sahabat #ruangpikir
```

## Caption TikTok
```
Dikasih kabar baik, jangan cuma bilang "wah, selamat ya" 😐

Riset Gable dkk. (2006): cara merespon kabar baik lebih terkait sama awet atau putusnya hubungan dibanding cara menghibur pas sedih. Coba: "Serius?! Gimana ceritanya?" ✨

Kirim ke orang yang selalu antusias dengerin ceritamu 📩

#psikologi #hubungan #pacaran #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Jujur, kamu tim "wah, selamat ya" atau tim "Serius?! Gimana ceritanya?" 😆 Tag orang yang paling antusias dengerin kabar baikmu 👇
```

## Story promosi
```
Pasanganmu cerita kabar baik, kamu bales apa? 👀
Kata riset, itu lebih terkait sama awet-nggaknya hubungan daripada pas dia sedih.
Tonton video barunya 👇
```
Stiker polling: `Kamu biasanya... "wah, selamat ya" 😐 / "Serius?! Gimana?" 🤩`

## Judul YouTube Shorts
```
Dikasih kabar baik, kok salah respon? Kata riset, ini kalimat yang bikin hubungan makin dekat #shorts
```

## Waktu upload
Malam 19.00–21.00 WIB, paling pas Jumat–Minggu (waktu pacaran & nongkrong).

## Produksi
- **Folder:** `video-engine/ep37_kabar-baik/` (dibangun dari EP36).
- **Render:**
  - Render ulang dengan `./build.sh`; suara sudah ada di `vo/`.
  - Buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`).
  - `DUR` 42, jeda antarbaris 0.35 dtk, encode CRF 26.
- **Lagu orisinal:** `audio.py` di folder ini (variasi EP22: 106 BPM, `TR = -1`).
- **Versi tanpa musik:**
  1. `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`
  2. Mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14).
- **Helper baru:**
  - `news_orb()` — bola kabar baik emas. `lit` 0 = redup abu-abu, `crack` retak.
  - `rain_orb()` — bola cerita sedih.
  - `rain_cloud()` — awan + garis hujan.
  - `umbrella()`.
  - `bond()` — benang cahaya kedekatan dengan denyut cahaya garis.
  - `rec_frame()` — bingkai kamera REC.
  - `calendar3d()` — kalender minggu yang dibalik.
  - `scale3d()` — timbangan 3D dengan rantai & piring.
  - `star4()` — kilau bintang 4 sudut.
- **Dipakai juga:** `cafe_bg()`, `table()`, `hero()`, `say()`, `secret_card2()`, `research_card()`, `extrude()`, `h_meter()`, `sparks()`, `chain()`, `crown()`, `avatar()`, `plane_icon()`.
