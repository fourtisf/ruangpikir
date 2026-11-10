# EP 32 — Susah move on? Jangan stalking, coba trik ini

Status: **sudah diproduksi** — `videos/ruang-pikir-ep32-susah-move-on.mp4` (±51 detik, 1080×1920, dengan **lagu instrumental orisinal**), halaman web `ruangpikir.id/episode/susah-move-on/`.
Format: rumus EP24 ("jangan cuma [kebiasaan]. Coba [trik] ini" + jawaban disensor lalu dibuka + "kirim ke …"), topik patah hati/mantan.

## Riset
1. **Otak orang yang baru diputusin** — Fisher, H. E., Brown, L. L., Aron, A., Strong, G., & Mashek, D. (2010). Reward, addiction, and emotion regulation systems associated with rejection in love. *Journal of Neurophysiology, 104*(1), 51–60.
   - fMRI pada **15 orang** (10 perempuan, 5 laki-laki) yang baru diputusin tapi masih sangat cinta. Saat melihat foto orang yang memutuskan mereka, area **dorongan & rasa ketagihan** aktif (ventral tegmental area, ventral striatum/nucleus accumbens, korteks orbitofrontal), area yang juga terlibat pada kecanduan kokain. Penulis menafsirkan penolakan cinta sebagai "bentuk kecanduan".
2. **Stalking medsos mantan** — Marshall, T. C. (2012). Facebook surveillance of former romantic partners: Associations with postbreakup recovery and personal growth. *Cyberpsychology, Behavior, and Social Networking, 15*(10), 521–526.
   - Survei **464 orang** (kebanyakan mahasiswa): makin sering memantau Facebook mantan, makin besar rasa sedih atas putusnya hubungan, perasaan negatif, kerinduan, dan makin kecil pertumbuhan diri. Studi korelasi, bukan bukti sebab-akibat.
3. **Trik yang menurunkan rasa cinta** — Langeslag, S. J. E., & Sanchez, M. E. (2018). Down-regulation of love feelings after a romantic break-up: Self-report and electrophysiological data. *Journal of Experimental Psychology: General, 147*(5), 720–733. (University of Missouri–St. Louis.)
   - **24 orang** (20 perempuan, 4 laki-laki) yang baru putus dan masih sedih. Dibandingkan beberapa strategi: **memikirkan sisi negatif mantan** (mis. kebiasaan yang menyebalkan) **menurunkan rasa cinta** (laporan diri + respons otak/EEG terhadap foto mantan), tapi membuat mood sempat lebih buruk. **Mengalihkan pikiran** tidak menurunkan rasa cinta, tapi membuat mood lebih baik. "Menerima rasa cinta" tidak mengubah rasa cinta.
- **Jujur soal batasnya:** sampel kecil; efek Langeslag diukur sesaat setelah melihat foto, bukan jangka panjang; studi Marshall korelasi. "Mirip otak yang kecanduan" adalah tafsiran peneliti dari pola aktivitas otak, bukan diagnosis. Angka "BUKA PROFIL DIA: 12x", contoh kebiasaan nyebelin ("telat bales chat"…), dan meter di video ilustratif. Video tidak menganjurkan membenci mantan; tujuannya menurunkan rasa terikat lalu mengalihkan energi. Tidak ada data Francesca Gino.

## Judul di layar
```
Udah putus, kok [kepoin dia terus?]
```

## Hook (detik 0–3)
- Suara: **"Susah move on? Otakmu lagi kayak orang ketagihan. Jangan stalking, coba satu trik ini."**
- Visual sejak frame pertama: ponsel profil medsos **"dia"** yang terus digulir sendiri + chip **BUKA PROFIL DIA: 2x → 12x**, tokoh kapsul cemas, bola otak merah berdenyut **MODE KETAGIHAN** → ponsel disilang merah + stempel **STOP** → kartu emas **TRIK MOVE ON** buram + gembok (dibuka di detik ±33 video).

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Susah move on? Otakmu lagi kayak orang ketagihan. Jangan stalking, coba satu trik ini."),
    (5.63, "Tahun dua ribu sepuluh, Helen Fisher memindai otak orang yang baru diputusin."),
    (10.08, "Pas lihat foto mantannya, area otak yang aktif mirip otak orang yang lagi kecanduan."),
    (14.66, "Riset lain nemuin, yang sering kepoin medsos mantan, lebih kangen dan lebih susah pulih."),
    (19.88, "Terus caranya? Tahun dua ribu delapan belas, Sandra Langeslag menguji beberapa cara."),
    (24.12, "Hasilnya? Yang bikin rasa cinta turun: ingat-ingat kebiasaan dia yang nyebelin."),
    (28.72, "Memang awalnya bikin sedih. Jadi habis itu, alihkan ke hal yang bikin kamu senang."),
    (33.98, "Kirim video ini ke teman yang masih stalking mantannya!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
Versi pertama "kebiasaan nyebelin dia" terdengar seperti "kebiasaannya belia", jadi kalimat diubah dan suara dibuat ulang.

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–5.6 | **Hook:** ponsel profil "dia" digulir, BUKA PROFIL DIA 12x, MODE KETAGIHAN, silang STOP, kartu TRIK MOVE ON buram. |
| 5.6–10.1 | Kartu ARSIP RISET 2010 · Helen Fisher & tim · Rutgers · Journal of Neurophysiology → pemindai fMRI + hati retak · 15 ORANG · BARU DIPUTUSIN. |
| 10.1–14.7 | Polaroid "dia" → garis ke kepala profil, bola merah AREA RASA KETAGIHAN menyala, chip MIRIP OTAK YANG KECANDUAN. |
| 14.7–19.9 | MARSHALL 2012 · 464 ORANG: ponsel digulir makin cepat, batang KANGEN & SUSAH PULIH naik, tokoh menangis. |
| 19.9–24.1 | CARANYA? → kartu riset 2018 Sandra Langeslag & Sanchez → kartu CARA 01 "Alihkan pikiran", CARA 02 "Terima perasaannya", CARA 03 terkunci. |
| 24.1–28.7 | HASILNYA? → cara 01/02 "CINTA NGGAK TURUN", kartu CARA 03 dibuka: **"Ingat kebiasaan dia yang nyebelin."** + chip telat bales chat / suka ngilang / nggak pernah minta maaf, batang RASA CINTA turun + hati retak. |
| 28.7–34.0 | MOOD KAMU turun ("AWALNYA SEDIH, ITU WAJAR") → LALU ALIHKAN: main sama teman, olahraga, dengerin musik, nonton film → mood naik, tokoh senang. |
| 34.0–36.6 | Kartu "TRIK MOVE ON" + KIRIM KE (bestie, teman kos, sepupu, teman kelas) + TERKIRIM. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Susah move on? Jangan stalking
```
Alternatif: `Udah putus, kok kepoin dia terus?` atau `1 trik move on (kata riset)`

## Caption Instagram
```
Susah move on? 💔 Otakmu lagi kayak orang ketagihan. Jangan stalking, coba satu trik ini.

Tahun 2010, Helen Fisher memindai otak orang yang baru diputusin. Pas lihat foto mantannya, area otak yang aktif mirip otak orang yang lagi kecanduan 🧠

Riset lain nemuin, yang sering kepoin medsos mantan, lebih kangen dan lebih susah pulih 📱

Terus caranya? Tahun 2018, Sandra Langeslag menguji beberapa cara.
Hasilnya? Yang bikin rasa cinta turun: ingat-ingat kebiasaan dia yang nyebelin 😤

Memang awalnya bikin sedih. Jadi habis itu, alihkan ke hal yang bikin kamu senang: main sama teman, olahraga, musik 🎧

📩 Kirim ke teman yang masih stalking mantannya
💬 Kebiasaan nyebelin mantan yang bikin kamu sadar? 👇 (jangan sebut nama ya 🤫)
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Fisher dkk. (2010), Journal of Neurophysiology; Marshall (2012), Cyberpsychology, Behavior, and Social Networking; Langeslag & Sanchez (2018), Journal of Experimental Psychology: General.

#psikologi #faktapsikologi #moveon #patahhati #mantan #ruangpikir
```

## Caption TikTok
```
Susah move on? Jangan stalking 💔📱

Riset (Langeslag 2018): yang bikin rasa cinta turun = ingat-ingat kebiasaan dia yang nyebelin. Habis itu alihkan ke hal yang bikin kamu senang 🎧

Kirim ke teman yang masih stalking mantannya 📩

#psikologi #moveon #patahhati #mantan #ruangpikir
```

## Komentar pertama (pin)
```
Yang paling bikin sadar: dia selalu telat bales chat, tapi online terus 😤 Kebiasaan nyebelin apa yang bikin kamu akhirnya move on? 👇 (tanpa sebut nama ya 🤫)
```

## Story promosi
```
Udah putus tapi masih kepoin profilnya? 📱💔
Kata riset, otakmu lagi kayak orang ketagihan. Ini triknya.
Tonton video barunya 👇
```
Stiker polling: `Jujur, kamu pernah stalking mantan? Pernah 🙈 / Nggak pernah 😇`

## Judul YouTube Shorts
```
Susah move on? Jangan stalking, coba 1 trik ini kata riset psikologi #shorts
```

## Waktu upload
Malam 20.00–22.00 WIB (jam galau dan scroll medsos), paling pas Sabtu malam atau Minggu malam.

## Produksi
Folder `video-engine/ep32_move-on/` (dibangun dari EP31): render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.21`). `base.py` folder ini kembali `DUR` 42 dan jeda antarbaris 0.35 dtk (suara ±43 dtk). Encode CRF 26. **Lagu orisinal** di `audio.py` folder ini (variasi EP22: 98 BPM, `TR = -1`). Versi tanpa musik: `python3 episode.py timeline timeline.json && MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video yang sudah ada (`-map 0:v -map 1:a -c:v copy` + loudnorm −14). Helper baru: `ig_phone()`, `ex_photo()`, `ex_avatar()`, `broken_heart()`, `way_card()`, `ORB_RED`; plus `joy_orb()`, `mri()` (EP31), `secret_card2()` (EP29), `vbar()` (EP30), `head_solid()`, `research_card()`, `race_bar()`, `idea_card()`, `tear()`, `stamp()`, `cross()`, `avatar()`, `plane_icon()`.
