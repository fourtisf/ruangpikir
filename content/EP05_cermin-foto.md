# EP 05 — Cakep di cermin, kok jelek di foto?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep05-cermin-foto.mp4` (±54 detik, 1080×1920, ±5,4 MB), halaman web `ruangpikir.id/episode/cermin-vs-foto/`.
Seri: Kenapa Kamu Gitu? · Topik: efek paparan (mere exposure) pada wajah sendiri.

## Riset
- **Sumber utama:** Mita, T. H., Dermer, M., & Knight, J. (1977). Reversed facial images and the mere-exposure hypothesis. *Journal of Personality and Social Psychology, 35*(8), 597–601.
  - Peserta dan teman/pasangannya diperlihatkan dua foto wajah peserta: versi asli dan versi cermin (dibalik kiri-kanan).
  - Peserta lebih memilih **versi cermin** wajahnya sendiri; teman/pasangannya lebih memilih **versi asli**.
  - Penjelasan: **efek paparan** (Zajonc, 1968), makin sering kita melihat sesuatu, makin kita menyukainya. Kita paling sering melihat wajah sendiri di cermin; orang lain melihat versi aslinya.
- **Jujur soal batasnya:** studi lama dengan sampel kecil (laporan sekunder menyebut 33 mahasiswi; angka ini tidak dipakai di video). Video tidak mengklaim "kamu pasti cakep", hanya bahwa rasa "jelek di foto" sebagian besar soal belum terbiasa.

## Judul di layar
```
Cakep di cermin, [kok jelek di foto]?
```

## Hook (detik 0–3)
- Suara langsung membuka dengan klaim mengejutkan: "Kamu nggak jelek di foto. Kamu cuma belum terbiasa."
- Visual: ponsel kamera, **jepretan + kilat** di 0,2 dtk, lalu wajah **bolak-balik cermin ↔ foto makin cepat** dengan label CERMIN/FOTO dan efek glitch kamera.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Kamu nggak jelek di foto. Kamu cuma belum terbiasa."),
    (2.95, "Di cermin cakep, tapi di kamera belakang, kok beda?"),
    (5.75, "Soalnya wajah kita nggak simetris, dan di cermin, kiri jadi kanan."),
    (9.37, "Tahun sembilan belas tujuh puluh tujuh, psikolog Theodore Mita mengujinya."),
    (13.43, "Peserta dikasih dua foto wajahnya: versi asli, dan versi cermin."),
    (16.95, "Hasilnya? Mereka lebih suka versi cermin. Tapi teman-temannya lebih suka versi asli."),
    (21.56, "Ini efek paparan: makin sering kita lihat sesuatu, makin kita suka."),
    (25.24, "Kamu tiap hari lihat versi cermin. Temanmu tiap hari lihat versi asli."),
    (29.08, "Jadi foto yang kamu benci, bisa jadi versi yang orang lain suka."),
    (32.59, "Coba balik fotomu sekarang. Mana yang lebih kamu suka? Tulis di komentar!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
Caption per frasa ada di `PHRASES` di `video-engine/ep05_cermin-foto/episode.py`.

## Adegan (gaya sinematik)
| Waktu | Visual |
|---|---|
| 0–3 | **Hook:** ponsel kamera, jepretan + kilat, wajah bolak-balik CERMIN ↔ FOTO makin cepat (glitch di versi foto). |
| 3–5.8 | Cermin oval berkilau (wajah tersenyum, centang) vs ponsel kamera belakang (wajah datar) + tanda tanya. |
| 5.8–9.4 | Potret besar + garis simetri; penanda poni, alis, tahi lalat, anting; potret dibalik → semua pindah sisi ("kiri jadi kanan"). |
| 9.4–13.4 | Kartu RISET 1977 · Mita, Dermer & Knight. |
| 13.4–21.6 | Dua foto polaroid ASLI vs CERMIN; "kamu" mengirim hati ke CERMIN, teman-teman mengirim hati ke ASLI. |
| 21.6–25.2 | "efek paparan": 12 thumbnail wajah bermunculan, lalu hati besar bersinar. |
| 25.2–29.1 | Panel KAMU (cermin, tiap hari versi cermin) vs TEMANMU (foto, tiap hari versi asli). |
| 29.1–32.6 | "Foto yang kamu benci" → hati dan komentar "cakep kok!", "natural banget", "suka yang ini". |
| 32.6–36.6 | Ponsel editor, tombol "Balik" ditekan, wajah dibalik bolak-balik; versi cermin vs versi asli; kolom komentar mengetik "aku pilih versi asli!". |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Kamu nggak jelek di foto
```

## Caption Instagram
```
Di cermin cakep, di kamera belakang kok beda? 😭 Tenang, kamu nggak jelek di foto, kamu cuma belum terbiasa.

Wajah kita nggak simetris. Di cermin, kiri jadi kanan, dan versi itulah yang kamu lihat setiap hari.

Tahun 1977, psikolog Theodore Mita dan timnya memperlihatkan dua foto wajah peserta: versi asli dan versi cermin. Hasilnya: peserta lebih suka versi cermin wajahnya sendiri, sementara teman-temannya justru lebih suka versi asli.

Ini namanya efek paparan: makin sering kita melihat sesuatu, makin kita menyukainya. Jadi foto yang kamu benci, bisa jadi versi yang paling sering dilihat (dan disukai) orang lain 🙂

🔁 Coba balik fotomu sekarang. Mana yang lebih kamu suka: versi cermin atau versi asli? Tulis di komentar!
📩 Kirim ke teman yang selalu minta foto diulang.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Mita, Dermer & Knight (1977), Journal of Personality and Social Psychology.

#psikologi #faktapsikologi #selfie #foto #percayadiri #ruangpikir
```

## Caption TikTok
```
Kamu nggak jelek di foto, kamu cuma belum terbiasa 😭

Riset Mita dkk. (1977): orang lebih suka versi cermin wajahnya sendiri, tapi temannya lebih suka versi asli. Efek paparan: yang sering dilihat, itu yang disukai.

Balik fotomu sekarang: cermin atau asli? Tulis di komentar 👇

#psikologi #faktapsikologi #selfie #percayadiri #ruangpikir
```

## Komentar pertama (pin)
```
Tes cepat: buka kamera depan, foto, lalu balik (flip) hasilnya. Versi mana yang kamu suka? Tulis "cermin" atau "asli" 👇
```

## Story promosi
```
Kenapa kamu cakep di cermin, tapi beda di foto? 🤳
Jawabannya bukan karena kamu jelek.
Tonton video barunya 👇
```

## Produksi
Folder `video-engine/ep05_cermin-foto/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py`). Potret asimetris digambar oleh `portrait()` di `episode.py` (parameter `mirror` membalik kiri-kanan, `flipx` untuk animasi membalik, `glitch` untuk efek kamera).
