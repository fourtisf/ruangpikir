# EP 07 — Omongan orang, kok kepikiran terus?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep07-omongan-orang.mp4` (±55 detik, 1080×1920, ±5,4 MB), halaman web `ruangpikir.id/episode/omongan-orang/`.
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
- Suara membuka dengan klaim: "Di kepalamu ada alat ukur yang terus menilai: orang lain suka kamu, atau nggak."
- Visual: siluet kepala tergambar, di dalamnya alat ukur "SOCIOMETER" menyala dengan jarum yang langsung berayun liar sejak frame pertama, garis pindai lewat, notifikasi "+1 suka", "dilihat", "komentar baru" bermunculan, lalu kamera masuk ke alat ukur; jarum ke SUKA (sinar mint) lalu jatuh ke NGGAK (alarm merah + goyang).

## Gaya visual (beda dari EP04–EP06)
"HUD / alat ukur": dasbor instrumen futuristik. Alat ukur jarum (`gauge()`: busur 240° coral → ungu → mint, cincin HUD berputar, angka mono), jam 24 jam, kartu "ARSIP RISET", slider SENSITIVITAS, sudut bingkai HUD, teks mono (JetBrains Mono), sapuan radar samar di latar. Tetap tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Di kepalamu ada alat ukur yang terus menilai: orang lain suka kamu, atau nggak."),
    (4.43, "Makanya satu komentar kecil, bisa kepikiran seharian."),
    (7.3, "Tahun sembilan belas sembilan puluh lima, psikolog Mark Leary menyebutnya sociometer."),
    (11.9, "Harga dirimu naik turun, ikut seberapa kamu merasa diterima."),
    (15.15, "Dulu, dikucilkan kelompok itu bahaya. Makanya ditolak sedikit, otak bereaksi mirip rasa sakit."),
    (20.24, "Masalahnya, alat ukur ini sering kelewat sensitif."),
    (22.95, "Tahun dua ribu satu, Savitsky dan timnya menemukan: kalau kita salah di depan orang, mereka nggak menilai seburuk yang kita kira."),
    (29.94, "Kita yang terlalu fokus ke kesalahan sendiri."),
    (32.38, "Jadi kalau omongan orang kepikiran lagi, ingat: alat ukurmu memang suka lebay."),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
Caption per frasa ada di `PHRASES` di `video-engine/ep07_omongan-orang/episode.py`.

## Adegan
| Waktu | Visual |
|---|---|
| 0–4.4 | **Hook:** kepala garis + alat ukur SOCIOMETER, jarum liar, notifikasi, kamera masuk; jarum ke SUKA lalu jatuh ke NGGAK (alarm). |
| 4.4–7.3 | Kartu komentar "kamu kok gitu sih?" menghantam, jarum alat ukur kecil jatuh; jam 24 jam berputar sehari penuh, komentar yang sama terulang di jam 10.12, 14.36, 19.06, 23.48. |
| 7.3–11.9 | Kartu ARSIP RISET 1995 · Mark Leary dkk. · JPSP; kata "SOCIOMETER" menghantam layar, dipecah jadi "sosial" + "alat ukur". |
| 11.9–15.2 | Tabung HARGA DIRI di tengah, 6 orang tersambung garis; saat mereka menerima (mint, centang) tabung naik ke 92%, saat ada yang menjauh (coral, silang) tabung turun. |
| 15.2–17.3 | ZAMAN DULU: kelompok di sekitar api unggun, satu orang terlempar keluar lingkaran KELOMPOK, tanda BAHAYA. |
| 17.3–20.2 | Komentar "kamu nggak usah ikut ya" menghantam kepala; titik sakit coral berdenyut + gelombang; label "SINYAL MIRIP RASA SAKIT" · Eisenberger dkk. (2003). |
| 20.2–23 | Alat ukur tenang, notifikasi "cuma dibaca" → jarum langsung jatuh ke 0%, alarm; slider SENSITIVITAS meluncur ke MAKS. |
| 23–26 | Kartu ARSIP RISET 2001 · Savitsky, Epley & Gilovich · JPSP. |
| 26–27.8 | Huruf anagram "HALSA" gagal (merah, goyang, silang, GAGAL) di depan penonton. |
| 27.8–29.9 | Dua alat ukur: KITA KIRA (jarum ke PARAH) vs KENYATAAN (jarum hampir di tengah, BIASA). |
| 29.9–32.4 | Kertas dengan satu kesalahan kecil; bingkai fokus mengunci, kaca pembesar memperbesar silangnya ×10, "FOKUS: KESALAHAN"; orang lain sibuk dengan pikirannya sendiri ("laper", "tugas numpuk", "chat doi"). |
| 32.4–36.6 | Komentar-komentar beterbangan, jarum gelisah + alarm; slider sensitivitas diturunkan, jarum tenang, stempel **LEBAY** menghantam alat ukur. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Kenapa omongan orang kepikiran terus?
```

## Caption Instagram
```
Satu komentar kecil, kok bisa kepikiran seharian? 🫠

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
Kenapa omongan orang kepikiran terus? 🫠

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
Folder `video-engine/ep07_omongan-orang/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py`; take ini memakai `tighten.py 0.25` supaya durasi ≤ 55 dtk). Encode CRF 26 (bukan 24) karena animasi HUD padat: CRF 24 menghasilkan 6,7 MB, CRF 26 ±5,4 MB dengan SSIM 0,996. Helper gaya HUD: `gauge()` (alat ukur jarum + angka), `mono()` (teks mono HUD), `brackets()` (sudut bingkai), `scanline()`, `warn_tri()`, `comment()` (kartu komentar dengan avatar), `mini_person()`, `cross()`, `clock24()`, `flame()` (api unggun), `stamp()` (stempel yang dihantamkan), `tile()` (huruf anagram), `file_card()` (kartu arsip riset), `slider()` (slider sensitivitas).
