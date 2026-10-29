# EP 07 — Omongan orang, kok kepikiran terus?

Status: **sudah diproduksi (v2: visual baru + hook lebih kuat)** — `videos/ruang-pikir-ep07-omongan-orang.mp4` (±50 detik, 1080×1920, ±5,6 MB), halaman web `ruangpikir.id/episode/omongan-orang/`.
Seri: Kenapa Kamu Gitu? · Topik: sociometer (harga diri sebagai alat ukur penerimaan sosial) + kita melebih-lebihkan penilaian orang setelah salah.

## Riset
- **Sumber utama 1:** Leary, M. R., Tambor, E. S., Terdal, S. K., & Downs, D. L. (1995). Self-esteem as an interpersonal monitor: The sociometer hypothesis. *Journal of Personality and Social Psychology, 68*(3), 518–530.
  - 5 studi. Harga diri peserta ikut naik turun mengikuti seberapa diterima atau ditolak yang mereka rasakan; ditolak karena alasan pribadi menurunkan harga diri.
  - Teori: harga diri adalah "sociometer", alat ukur internal yang memantau penerimaan sosial. Latar evolusinya: bagi manusia purba, dikucilkan kelompok berbahaya.
- **Sumber utama 2:** Savitsky, K., Epley, N., & Gilovich, T. (2001). Do others judge us as harshly as we think? Overestimating the impact of our failures, shortcomings, and mishaps. *Journal of Personality and Social Psychology, 81*(1), 44–56.
  - 4 studi. Setelah gagal atau malu di depan orang (misalnya gagal mengerjakan anagram sambil ditonton), orang menebak dirinya akan dinilai jauh lebih buruk daripada penilaian pengamat yang sebenarnya.
  - Penjelasan: kita terlalu fokus pada kesalahan sendiri; pengamat melihat konteks yang lebih luas.
- **Pendukung:** Eisenberger, N. I., Lieberman, M. D., & Williams, K. D. (2003). Does rejection hurt? An fMRI study of social exclusion. *Science, 302*(5643), 290–292. Saat dikucilkan dalam permainan lempar bola di komputer (Cyberball), area otak yang juga terlibat dalam rasa sakit fisik (korteks cingulate anterior) lebih aktif. Jumlah peserta tidak disebut di video.
- **Jujur soal batasnya:** "mirip rasa sakit" artinya area otaknya tumpang tindih, bukan rasa sakit yang sama; riset lanjutan masih memperdebatkan seberapa mirip. Peduli pendapat orang itu normal dan berguna; video tidak menyuruh "cuek total", hanya mengingatkan bahwa alarmnya sering berlebihan. Bukan diagnosis kecemasan sosial.

## Judul di layar
```
Omongan orang, [kok kepikiran terus]?
```

## Hook (detik 0–3)
- Suara membuka dengan kalimat yang langsung relatable + janji jawaban (open loop): "Satu komentar kecil bisa kepikiran seharian. Itu bukan karena kamu lemah."
- Visual yang langsung dikenali: frame pertama ponsel miring 3D bergetar di gelap, notifikasi "kamu kok gitu sih?" jatuh dari atas; notifikasinya lepas dan terbang ke kamera, lalu jadi 6 kartu komentar yang berputar makin cepat mengelilingi kepala, dengan penghitung "diputar ulang di kepala: 1x → 99x".
- Di "Itu bukan karena kamu lemah": putaran berhenti mendadak (kilat cincin), kartu-kartu jatuh, dan di dalam kepala menyala alat ukur misterius + tanda "?", lalu kamera masuk ke kepala (penonton penasaran "alat apa itu?").

## Gaya visual (beda dari EP04–EP06)
"Dunia 3D + UI medsos": ponsel dan kartu kaca miring dalam perspektif 3D, notifikasi & kartu komentar, komentar yang berputar mengelilingi kepala (urut kedalaman), teks 3D bertumpuk ("1995", "SOCIOMETER", "BIP!"), alat ukur fisik berbingkai logam, alarm asap sebagai metafora "kelewat sensitif", kartu riset yang berputar masuk dan dibalik, siluet orang padat dengan cahaya tepi. Tetap tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Satu komentar kecil bisa kepikiran seharian. Itu bukan karena kamu lemah."),
    (4.19, "Di kepalamu ada alat ukur yang terus menilai: kamu disukai, atau nggak."),
    (8.11, "Tahun sembilan belas sembilan puluh lima, psikolog Mark Leary menyebutnya sociometer."),
    (12.82, "Harga dirimu naik turun, ikut seberapa kamu merasa diterima."),
    (16.13, "Dulu, dikucilkan itu bahaya. Jadi ditolak sedikit, otak bereaksi mirip rasa sakit."),
    (20.67, "Masalahnya, alat ukur ini kelewat sensitif."),
    (23.05, "Tahun dua ribu satu, Savitsky dan timnya menemukan: kalau kita salah di depan orang, mereka nggak menilai seburuk yang kita kira."),
    (30.18, "Kita yang terlalu fokus ke kesalahan sendiri."),
    (32.67, "Jadi kalau omongan orang kepikiran lagi, ingat: alat ukurmu suka lebay."),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
Caption per frasa ada di `PHRASES` di `video-engine/ep07_omongan-orang/episode.py`.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–4.2 | **Hook:** ponsel 3D bergetar + notifikasi "kamu kok gitu sih?" → notifikasi terbang ke kamera → 6 kartu komentar berputar makin cepat mengelilingi kepala, penghitung "diputar ulang di kepala: 99x" → putaran berhenti, kartu jatuh, alat ukur + "?" menyala di dalam kepala, kamera masuk. |
| 4.2–8.1 | Alat ukur fisik (bingkai logam, kubah kaca) miring 3D: jarum liar, menimbang, ke SUKA (hati mint beterbangan + sinar), lalu jatuh ke NGGAK (kaca retak, kilat merah, goyang). |
| 8.1–12.8 | Kartu ARSIP RISET berputar masuk: "1995" teks 3D · Mark Leary dkk. · JPSP; kartu dibalik → "SOCIOMETER" = sosial + alat ukur. |
| 12.8–16.1 | Tabung kaca HARGA DIRI berisi cairan bercahaya, 8 avatar berputar mengelilingi: menerima (cincin mint + hati) → tabung naik; tiga menjauh (abu, silang) → tabung turun; satu kembali. |
| 16.1–17.9 | ZAMAN DULU: siluet orang duduk di sekitar api unggun; satu orang terlempar ke kegelapan, tanda BAHAYA. |
| 17.9–20.7 | Komentar "kamu nggak diajak ya" menghantam otak (berdenyut coral) → dua otak: DITOLAK ≈ SAKIT FISIK, "area otak yang sama ikut aktif" · Eisenberger dkk. (2003). |
| 20.7–23.1 | Alarm asap bertuliskan SOCIOMETER di plafon; pemicunya cuma notifikasi kecil "dibaca" → alarm meraung: lampu merah berputar, gelombang suara, "BIP!" teks 3D. |
| 23.1–26.1 | Kartu ARSIP RISET 2001 · Savitsky, Epley & Gilovich · JPSP. |
| 26.1–30.2 | Panggung + lampu sorot: huruf anagram "HALSA" gagal (GAGAL); KITA KIRA "mereka pasti ilfeel banget" (gemetar) vs KENYATAAN penonton: "susah sih soalnya", "biasa aja", "wajar kok"; gelembung kita mengecil. |
| 30.2–32.7 | Kertas dengan satu kesalahan kecil; bingkai fokus mengunci, kaca pembesar logam memperbesar silangnya, "FOKUS: KESALAHAN SENDIRI"; orang lain sibuk dengan pikirannya ("laper", "tugas numpuk", "chat doi"). |
| 32.7–36.6 | Callback hook: kartu komentar kembali berputar mengelilingi kepala yang memerah; kenop SENSITIVITAS diputar ke MIN → putaran hilang, alat ukur jadi tenang (mint), stempel **LEBAY**. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Itu bukan karena kamu lemah
```

## Caption Instagram
```
Satu komentar kecil bisa kepikiran seharian. Dan itu bukan karena kamu lemah 🫠

Tahun 1995, psikolog Mark Leary dan timnya menjelaskan: di kepala kita ada semacam "alat ukur" yang terus memantau seberapa kita diterima orang lain. Namanya sociometer. Harga diri kita ikut naik turun mengikuti alat ukur itu.

Kenapa sesensitif itu? Dulu, dikucilkan kelompok itu berbahaya. Makanya sampai sekarang, ditolak sedikit saja, otak bereaksi mirip rasa sakit (Eisenberger dkk., 2003).

Tapi alat ukur ini sering lebay. Tahun 2001, Savitsky, Epley & Gilovich menemukan: setelah kita salah di depan orang, kita menebak akan dinilai jauh lebih buruk daripada kenyataannya. Kita yang terlalu fokus ke kesalahan sendiri, orang lain nggak sekeras itu menilai 🤍

Jadi wajar kok mikirin pendapat orang. Cuma ingat: alarmnya suka kelewat sensitif.

📩 Kirim ke teman yang suka kepikiran omongan orang.
💬 Komentar orang yang paling lama kamu pikirin apa? Tulis di bawah 👇
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Leary dkk. (1995) & Savitsky, Epley & Gilovich (2001), Journal of Personality and Social Psychology; Eisenberger dkk. (2003), Science.

#psikologi #faktapsikologi #overthinking #insecure #kesehatanmental #ruangpikir
```

## Caption TikTok
```
Satu komentar kecil bisa kepikiran seharian, dan itu bukan karena kamu lemah 🫠

Di kepalamu ada "alat ukur" penerimaan sosial, namanya sociometer (Leary dkk., 1995). Masalahnya, alat ukur ini suka lebay: setelah kita salah, orang lain menilai kita jauh lebih santai dari yang kita kira (Savitsky dkk., 2001).

Kirim ke teman yang suka kepikiran omongan orang 🤍

#psikologi #overthinking #faktapsikologi #insecure #ruangpikir
```

## Komentar pertama (pin)
```
Fakta kecil: setelah salah di depan orang, kita yakin dinilai parah, padahal penontonnya menilai kita jauh lebih biasa aja. Komentar siapa yang paling lama nyangkut di kepalamu? 👇
```

## Story promosi
```
Satu komentar kecil bisa kepikiran seharian? 🫠
Ternyata ada "alat ukur" di kepalamu, dan dia suka lebay.
Tonton video barunya 👇
```

## Produksi
Folder `video-engine/ep07_omongan-orang/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`). Encode CRF 26 (bukan 24) karena animasinya padat (SSIM 0,996, ±5,6 MB). Versi pertama (gaya HUD / alat ukur, hook "Di kepalamu ada alat ukur...") ada di riwayat git (commit d549af3). Helper gaya 3D: `plane_m()`/`plane` (bidang 3D miring lewat `Matrix.setPolyToPoly`), `P3()`, `extrude()`, `phone()`, `notif()`, `head_solid()`, `orbit()`, `gauge_phys()`, `crack()`, `research_card()` (bisa dibalik), `avatar()`, `tube()`, `sitter()`/`stander()`/`bust()`, `brain()`, `smoke_alarm()`, `knob()`, `thought()`, `stamp()`.
