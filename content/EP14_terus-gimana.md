# EP 14 — Banyak nanya, kok malah disukai?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep14-terus-gimana.mp4` (±47 detik, 1080×1920, ±4,0 MB), halaman web `ruangpikir.id/episode/terus-gimana/`.
Seri: Trik Psikologi (format seperti EP03, EP12, EP13) · Topik: pertanyaan lanjutan membuat kita lebih disukai.

## Riset
- **Sumber utama:** Huang, K., Yeomans, M., Brooks, A. W., Minson, J., & Gino, F. (2017). It doesn't hurt to ask: Question-asking increases liking. *Journal of Personality and Social Psychology, 113*(3), 430–452.
  - Obrolan langsung antara orang yang baru kenal: peserta yang diminta lebih banyak bertanya, terutama **pertanyaan lanjutan** (menanggapi cerita lawan bicara), lebih disukai lawan bicaranya.
  - Data speed dating: yang lebih banyak bertanya lebih sering disetujui untuk kencan kedua.
  - Mekanisme: penanya terlihat lebih **responsif** (mendengarkan, memahami, peduli).
  - Orang tidak menyangka bertanya bisa membuat mereka lebih disukai.
- **Jujur soal batasnya:** pertanyaan lanjutan yang tulus (menanggapi cerita), bukan interogasi. Jumlah sampel dari liputan media tidak dipakai.

## Judul di layar
```
Banyak nanya, [kok malah disukai]?
```

## Hook (detik 0–3)
- Suara: **"Mau makin disukai pas ngobrol? Coba dua kata ini: terus gimana?"** Masalah sosial yang dialami banyak orang + trik yang sangat sederhana (dua kata) langsung di detik 2–3.
- Visual sejak frame pertama: dua tokoh kapsul ngobrol di meja kafe malam (lampu gantung hangat, kopi mengepul); yang satu bercerita "aku baru balik dari Jogja", yang lain gemetar "eh... mau ngomong apa ya"; meter NYAMBUNG rendah. Di "terus gimana?" gelembung emas menghantam, lawan bicara berbinar, hati beterbangan, meter NYAMBUNG penuh.

## Gaya visual
Tokoh kapsul premium (`hero()`) di "kafe malam": lampu gantung dengan sorot cahaya hangat, siluet kota, meja kopi, meter NYAMBUNG + hati, panel obrolan kaca (sedikit nanya vs banyak nanya, pertanyaan berwarna emas), speed dating (timer, "hmm..." vs "ketemu lagi!"), busur pertanyaan "?" yang mengalir antar tokoh + telinga "didengar & dipahami", "yang dikira" (nanya = kepo) dicoret vs "kenyataannya" (nanya = disukai), teks 3D "TERUS GIMANA?", kolom komentar. Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Mau makin disukai pas ngobrol? Coba dua kata ini: terus gimana?"),
    (3.9, "Kebanyakan kita sibuk mikirin mau ngomong apa, biar kelihatan menarik."),
    (8.06, "Tahun dua ribu tujuh belas, psikolog Karen Huang dari Harvard meneliti obrolan orang yang baru kenal."),
    (14.06, "Yang lebih banyak bertanya, terutama pertanyaan lanjutan, ternyata lebih disukai."),
    (18.88, "Bahkan di speed dating, mereka lebih sering diajak ketemu lagi."),
    (22.63, "Soalnya, pertanyaan lanjutan bikin lawan bicara merasa didengar dan dipahami."),
    (27.21, "Lucunya, kebanyakan orang nggak nyangka bertanya bisa bikin disukai."),
    (31.25, "Jadi lain kali ngobrol, cukup tanya: terus gimana? Tulis pertanyaan andalanmu di komentar!"),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–3.9 | **Hook:** kafe malam, dua tokoh ngobrol; "aku baru balik dari Jogja" vs "eh... mau ngomong apa ya"; gelembung emas "terus gimana?" → lawan bicara berbinar, hati, meter NYAMBUNG penuh. |
| 3.9–8.1 | Tokoh gemetar dikelilingi pikiran "harus lucu", "jangan garing!", "harus kelihatan pinter", "tadi aku aneh nggak?" + "mau ngomong apa?". |
| 8.1–14.1 | Kartu ARSIP RISET 2017 · Huang, Yeomans, Brooks, Minson & Gino · JPSP; "obrolan orang yang baru kenal". |
| 14.1–18.9 | Panel obrolan SEDIKIT NANYA vs BANYAK NANYA (pertanyaan emas: "lagi ngapain?", "lari di mana?", "terus gimana rasanya?"); batang "disukai lawan bicara"; chip "pertanyaan lanjutan". |
| 18.9–22.6 | SPEED DATING: dua meja, timer; "sedikit nanya" → "hmm...", "banyak nanya" → "ketemu lagi!" + hati. |
| 22.6–27.2 | Busur pertanyaan "?" mengalir dari penanya ke lawan bicara yang berbinar; telinga + "didengar", "dipahami". |
| 27.2–31.3 | "YANG DIKIRA: nanya terus = kepo, ganggu" dicoret → "KENYATAANNYA: nanya = disukai". |
| 31.3–36.6 | Kafe lagi: teks 3D "TERUS GIMANA?", komentar "kok bisa?", "terus rasanya gimana?", "abis itu ngapain?", "ceritain dong!"; meter NYAMBUNG penuh. |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
2 kata biar makin disukai
```

## Caption Instagram
```
Mau makin disukai pas ngobrol? Coba dua kata ini: "terus gimana?" 💬

Kebanyakan kita sibuk mikirin mau ngomong apa biar kelihatan menarik. Padahal riset Harvard bilang kuncinya justru di bertanya.

Tahun 2017, psikolog Karen Huang dan timnya meneliti obrolan orang yang baru kenal. Yang lebih banyak bertanya, terutama pertanyaan lanjutan ("terus gimana?", "kok bisa?"), ternyata lebih disukai. Bahkan di speed dating, mereka lebih sering diajak ketemu lagi 💕

Soalnya pertanyaan lanjutan bikin lawan bicara merasa didengar dan dipahami. Lucunya, kebanyakan orang nggak nyangka bertanya bisa bikin disukai.

Jadi lain kali ngobrol, nggak usah maksa jadi yang paling seru. Dengerin, terus tanya: "terus gimana?" 🤍

💬 Tulis pertanyaan lanjutan andalanmu di komentar 👇
📩 Kirim ke teman yang suka bingung mau ngomong apa.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: Huang, Yeomans, Brooks, Minson & Gino (2017), Journal of Personality and Social Psychology.

#psikologi #faktapsikologi #komunikasi #pdkt #percayadiri #ruangpikir
```

## Caption TikTok
```
Mau makin disukai pas ngobrol? Tanya "terus gimana?" 💬

Riset Harvard (Huang dkk., 2017): yang banyak nanya, terutama pertanyaan lanjutan, lebih disukai dan lebih sering diajak ketemu lagi di speed dating. Lawan bicara merasa didengar.

Pertanyaan andalanmu apa? 👇

#psikologi #komunikasi #pdkt #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Pertanyaan lanjutan favoritku: "terus kamu ngerasa gimana?" Sekarang giliranmu, tulis punyamu 👇
```

## Story promosi
```
Bingung mau ngomong apa pas ngobrol? 😅
Coba dua kata ini: "terus gimana?"
Tonton video barunya 👇
```

## Produksi
Folder `video-engine/ep14_terus-gimana/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`). Encode CRF 26. Helper baru: `cafe_bg()` (lampu gantung hangat + siluet kota), `table()` (meja kopi, `legs`), `conn_meter()` (meter NYAMBUNG + hati), `chat_panel()` (panel obrolan kaca, pertanyaan emas), `ear()`, `two_chat()`; plus helper EP12 (`hero()`, `say()`, dll).
