# EP 11 — Momen memalukan, kok keinget terus?

Status: **sudah diproduksi** — `videos/ruang-pikir-ep11-momen-memalukan.mp4` (±48 detik, 1080×1920, ±4,4 MB), halaman web `ruangpikir.id/episode/momen-memalukan/`.
Seri: Kenapa Kamu Gitu? · Topik: ingatan emosional (kenapa momen memalukan awet dan muncul pas mau tidur) + welas asih pada diri sendiri.

## Riset
- **Sumber utama:** McGaugh, J. L. (2004). The amygdala modulates the consolidation of memories of emotionally arousing experiences. *Annual Review of Neuroscience, 27*, 1–28.
  - Tinjauan: saat emosi memuncak, amigdala (bersama hormon stres) memperkuat penyimpanan ingatan; aktivasi amigdala saat kejadian berkaitan erat dengan seberapa kuat kejadian itu diingat kemudian.
- **Kenapa pas mau tidur:** Berntsen, D. (1996). Involuntary autobiographical memories. *Applied Cognitive Psychology, 10*(5), 435–454, dan riset lanjutannya: dari studi buku harian, ingatan yang muncul tanpa diundang paling sering datang saat kegiatan ringan/santai yang tidak menuntut perhatian.
- **Orang lain jarang memperhatikan:** Gilovich, Medvec & Savitsky (2000), *JPSP* — spotlight effect (lihat juga EP01).
- **Yang membantu:** Leary, M. R., Tate, E. B., Adams, C. E., Allen, A. B., & Hancock, J. (2007). Self-compassion and reactions to unpleasant self-relevant events. *JPSP, 92*(5), 887–904. Studi 5: sudut pandang welas asih pada diri sendiri (termasuk "orang lain juga mengalami hal serupa") membuat peserta bisa mengakui perannya dalam kejadian buruk tanpa kewalahan oleh emosi negatif.
- **Jujur soal batasnya:** riset Leary kebanyakan memakai kejadian ringan di laboratorium. Video tidak mengklaim "orang lain pasti sudah lupa" (tidak diteliti langsung), hanya bahwa mereka jauh lebih jarang memperhatikan. Contoh momen memalukan di video fiktif/umum.

## Judul di layar
```
Momen memalukan, [kok keinget terus]?
```

## Hook (detik 0–3)
- Suara: **"Kamu pasti masih ingat momen paling memalukanmu. Otakmu memang sengaja menyimpannya."** Langsung memanggil ingatan pribadi penonton + klaim mengejutkan ("sengaja").
- Visual sejak frame pertama: kamar gelap jam tidur, orang berbaring yang matanya mendadak melotot dan pipinya memerah; polaroid **'salah manggil guru "mama"'** menghantam langit-langit (kilat pink + goyang), lalu polaroid lain bermunculan ("dadah ke orang yang bukan dadah ke aku", "kepleset di depan gebetan", "salah kirim chat ke grup keluarga") + label "DISIMPAN OTAK".

## Gaya visual (beda dari EP04–EP10)
"Kamar jam 2 pagi + arsip ingatan": kamar gelap dengan jendela bulan dan sinar bulan, orang berbaring di kasur (mata melotot → terpejam), polaroid momen memalukan dengan wajah meringis (pipi merah, keringat), lemari arsip ingatan (laci PENTING/BIASA/LUPA) + stempel **PENTING**, meteran EMOSI, siang sibuk (pikiran mengalir) vs malam santai (ingatan naik dari laci), sorot lampu panggung, jaringan "semua orang pernah malu", hati hangat yang mengubah wajah meringis jadi senyum. Tanpa titik/bokeh dan tanpa progress bar.

## Naskah suara (vo.py, anchor = waktu animasi, DUR 42)
```python
LINES = [
    (0.15, "Kamu pasti masih ingat momen paling memalukanmu. Otakmu memang sengaja menyimpannya."),
    (4.8, "Apalagi pas mau tidur, tiba-tiba muncul lagi, bikin pengen teriak ke bantal."),
    (9.0, "Tahun dua ribu empat, James Mekgo menjelaskan: saat emosi memuncak, amigdala bikin ingatan tersimpan lebih kuat."),
    (15.31, "Kenapa munculnya pas mau tidur? Ingatan tak diundang paling sering datang saat pikiran lagi santai, kata Dorte Bernsen."),
    (22.0, "Padahal orang lain jauh lebih jarang memperhatikan kita dari yang kita kira."),
    (26.2, "Jadi kalau muncul lagi, bilang ke diri sendiri: semua orang pernah malu, dan itu manusiawi."),
    (31.23, "Riset Mark Liri: baik ke diri sendiri bikin kita menerima kesalahan, tanpa tenggelam dalam malu."),
    (36.6, "Follow Ruang Pikir, biar makin kenal isi kepalamu."),
]
```
"Mekgo", "Dorte Bernsen", "Liri" = ejaan fonetik McGaugh, Dorthe Berntsen, Leary untuk TTS (caption tetap ejaan asli).

## Adegan
| Waktu animasi | Visual |
|---|---|
| 0–4.8 | **Hook:** kamar gelap, mata melotot, polaroid 'salah manggil guru "mama"' menghantam langit-langit + polaroid lain; "DISIMPAN OTAK". |
| 4.8–9 | Polaroid terus bermunculan; bantal ditarik menutup wajah, "AAAAA!" (teredam bantal). |
| 9–15.3 | Kartu ARSIP RISET 2004 · James McGaugh; meteran EMOSI memuncak, polaroid dicap **PENTING** lalu masuk laci arsip yang menyala merah; "amigdala: simpan kuat-kuat!". |
| 15.3–22 | Siang 14.00: pikiran sibuk mengalir (kerjaan, chat grup, macet...); malam 23.47: semua hilang, laci PENTING terbuka dan polaroid naik — "pikiran lagi santai"; chip Dorthe Berntsen. |
| 22–26.2 | Sorot lampu panggung ke kamu + polaroid raksasa ("YANG KAMU KIRA") yang mengecil; penonton memikirkan "laper", "deadline", "drakor"; chip spotlight effect. |
| 26.2–31.2 | Polaroid muncul lagi lalu mengecil; 8 avatar masing-masing punya polaroid memalukannya sendiri, tersambung garis mint ke "kamu" — SEMUA ORANG PERNAH MALU. |
| 31.2–36.6 | Kembali ke kamar: hati hangat menyentuh polaroid, wajah meringis berubah jadi senyum, pipi tak lagi merah, mata terpejam, "z z z"; chip Mark Leary dkk. (2007). |
| 36.6–42 | Outro logo + RUANG PIKIR + ruangpikir.id + tombol Follow. |

## Teks cover Reels
```
Kenapa momen malu keinget terus?
```

## Caption Instagram
```
Kamu pasti masih ingat momen paling memalukanmu. Dan otakmu memang sengaja menyimpannya 🫠

Saat emosi memuncak (malu banget, deg-degan, panik), amigdala dan hormon stres bikin ingatan itu tersimpan jauh lebih kuat (McGaugh, 2004). Makanya momen 5 tahun lalu masih terasa jelas.

Kenapa munculnya pas mau tidur? Riset Dorthe Berntsen: ingatan tak diundang paling sering datang saat pikiran lagi santai dan nggak sibuk. Kayak pas rebahan di kasur.

Padahal, orang lain jauh lebih jarang memperhatikan kita dari yang kita kira (Gilovich dkk., 2000).

Jadi kalau muncul lagi, bilang ke diri sendiri: "semua orang pernah malu, dan itu manusiawi." Riset Mark Leary dkk. (2007): bersikap baik ke diri sendiri bikin kita bisa menerima kesalahan tanpa tenggelam dalam rasa malu 🤍

💬 Momen memalukan apa yang masih suka muncul pas mau tidur? Ngaku di komentar, kita senasib 👇
📩 Kirim ke teman yang suka teriak ke bantal.
🧠 Main tes otak gratis di ruangpikir.id (link di bio)

Sumber: McGaugh (2004), Annual Review of Neuroscience; Berntsen (1996), Applied Cognitive Psychology; Gilovich, Medvec & Savitsky (2000) & Leary dkk. (2007), Journal of Personality and Social Psychology.

#psikologi #faktapsikologi #overthinking #cringe #kesehatanmental #ruangpikir
```

## Caption TikTok
```
Momen memalukan 5 tahun lalu masih muncul pas mau tidur? 🫠

Saat malu, amigdala bikin ingatan tersimpan lebih kuat (McGaugh, 2004). Dan ingatan tak diundang paling sering datang saat pikiran lagi santai (Berntsen). Bilang ke diri sendiri: semua orang pernah malu 🤍

Ngaku: momen apa yang masih keinget? 👇

#psikologi #overthinking #cringe #faktapsikologi #ruangpikir
```

## Komentar pertama (pin)
```
Aku duluan: pernah dadah balik ke orang yang ternyata dadah ke orang di belakangku 🫠 Sekarang giliranmu 👇
```

## Story promosi
```
Mau tidur, tiba-tiba keinget momen memalukan? 🫠
Ternyata otakmu sengaja nyimpen itu.
Tonton video barunya 👇
```

## Produksi
Folder `video-engine/ep11_momen-memalukan/`: render ulang dengan `./build.sh` (suara sudah ada di `vo/`), buat ulang suara dengan `./build.sh --voice` (resep EP01 + `tighten.py 0.25`; cek transkripsi nama fonetik). Encode CRF 26. Helper gaya kamar + arsip ingatan: `bedroom()` (jendela bulan, kasur, orang berbaring dengan mata/pipi/bantal), `polaroid()`/`pol3d()` (polaroid momen memalukan, `heat` = cahaya merah, `soft` = berubah tenang), `cringe_face()`, `cabinet()` (lemari arsip PENTING/BIASA/LUPA), `chips_flow()` (pikiran siang yang mengalir), plus `stander()`, `bust()`, `avatar()`, `thought()`, `stamp()`, `research_card()`.
