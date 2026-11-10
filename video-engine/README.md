# Mesin video Ruang Pikir

Video dibuat 100% dengan kode: ilustrasi digambar dengan **skia-python**, suara dari **Gemini TTS** (voice `Achird`), musik + SFX disintesis dengan **numpy/scipy**, lalu digabung dengan **ffmpeg**. Tidak ada biaya per video selain kuota TTS.

Output: MP4 1080×1920 (HD), 30 fps, H.264 (preset slow, CRF 24, `-tune animation`, `aq-mode=3` supaya gradasi gelap tidak belang) + AAC 128k, loudness −14 LUFS. Ukuran ±4–5 MB per 50 detik (sebelumnya ±9 MB; hasil uji SSIM 0,998 terhadap versi CRF 17, tanpa beda kasat mata). Jangan pakai HEVC/H.265: lebih kecil, tapi tidak diputar di sebagian browser. Render 45–55 detik ±5–7 menit di 2 vCPU.

## Instalasi
```bash
pip install -r requirements.txt      # skia-python, numpy, scipy, requests, pillow
# + ffmpeg di PATH
export GEMINI_API_KEY=...            # hanya kalau mau generate suara baru
# atau simpan sekali di file .env di folder repo (salin dari .env.example; .env tidak ikut git),
# dibaca otomatis oleh gemini_tts.py: GEMINI_API_KEY=...  GEMINI_TTS_MODEL=gemini-3.8-flash-tts
# + skia butuh libEGL di Linux: apt install libegl1 libgl1
```

## Render ulang episode yang ada (tanpa API key)
```bash
./ep01_spotlight/build.sh            # -> ep01_spotlight/ruang-pikir-ep01.mp4
./ep02_stroop/build.sh               # -> ep02_stroop/ruang-pikir-ep02.mp4
./ep03_panggil-nama/build.sh         # -> ep03_panggil-nama/ruang-pikir-ep03.mp4
./ep04_pura-pura-gapapa/build.sh     # -> ep04_pura-pura-gapapa/ruang-pikir-ep04.mp4
./ep05_cermin-foto/build.sh          # -> ep05_cermin-foto/ruang-pikir-ep05.mp4
./ep06_liking-gap/build.sh           # -> ep06_liking-gap/ruang-pikir-ep06.mp4
./ep07_omongan-orang/build.sh        # -> ep07_omongan-orang/ruang-pikir-ep07.mp4
./ep08_nunda-kerjaan/build.sh        # -> ep08_nunda-kerjaan/ruang-pikir-ep08.mp4
./ep09_kok-minder/build.sh           # -> ep09_kok-minder/ruang-pikir-ep09.mp4
./ep10_sebut-perasaan/build.sh       # -> ep10_sebut-perasaan/ruang-pikir-ep10.mp4 (format 30 detik)
./ep11_momen-memalukan/build.sh      # -> ep11_momen-memalukan/ruang-pikir-ep11.mp4
./ep12_aku-excited/build.sh          # -> ep12_aku-excited/ruang-pikir-ep12.mp4
./ep13_paksa-melek/build.sh          # -> ep13_paksa-melek/ruang-pikir-ep13.mp4
./ep14_terus-gimana/build.sh         # -> ep14_terus-gimana/ruang-pikir-ep14.mp4
./ep15_chat-duluan/build.sh          # -> ep15_chat-duluan/ruang-pikir-ep15.mp4
./ep16_takut-blank/build.sh          # -> ep16_takut-blank/ruang-pikir-ep16.mp4
./ep17_cepat-akrab/build.sh          # -> ep17_cepat-akrab/ruang-pikir-ep17.mp4
./ep18_makasih-banyak/build.sh       # -> ep18_makasih-banyak/ruang-pikir-ep18.mp4
./ep19_minta-tolong/build.sh         # -> ep19_minta-tolong/ruang-pikir-ep19.mp4
./ep20_cerita-duluan/build.sh        # -> ep20_cerita-duluan/ruang-pikir-ep20.mp4
./ep21_deep-talk/build.sh            # -> ep21_deep-talk/ruang-pikir-ep21.mp4
./ep22_puji-aja/build.sh             # -> ep22_puji-aja/ruang-pikir-ep22.mp4
./ep23_baterai-sosial/build.sh       # -> ep23_baterai-sosial/ruang-pikir-ep23.mp4
./ep24_minta-maaf/build.sh           # -> ep24_minta-maaf/ruang-pikir-ep24.mp4
./ep25_kerja-kelompok/build.sh       # -> ep25_kerja-kelompok/ruang-pikir-ep25.mp4
./ep26_makasih-nunggu/build.sh       # -> ep26_makasih-nunggu/ruang-pikir-ep26.mp4
./ep27_wajar-kok/build.sh            # -> ep27_wajar-kok/ruang-pikir-ep27.mp4
./ep28_ada-saran/build.sh            # -> ep28_ada-saran/ruang-pikir-ep28.mp4
./ep29_nelpon-ortu/build.sh          # -> ep29_nelpon-ortu/ruang-pikir-ep29.mp4
./ep30_jauh-dari-ortu/build.sh       # -> ep30_jauh-dari-ortu/ruang-pikir-ep30.mp4
./ep31_suara-ibu/build.sh            # -> ep31_suara-ibu/ruang-pikir-ep31.mp4
./ep32_move-on/build.sh              # -> ep32_move-on/ruang-pikir-ep32.mp4
./ep33_tulis-besok/build.sh          # -> ep33_tulis-besok/ruang-pikir-ep33.mp4
./ep34_napas-aneh/build.sh           # -> ep34_napas-aneh/ruang-pikir-ep34.mp4
./ep35_digantungin/build.sh          # -> ep35_digantungin/ruang-pikir-ep35.mp4
```
Suara sudah tersimpan di `vo/`. Tambah `--voice` untuk membuat ulang suaranya.

## Struktur satu episode
| File | Fungsi |
|---|---|
| `vo.py` | Naskah: daftar `(anchor_detik, kalimat)`. Anchor = waktu animasi saat kalimat mulai |
| `vo/lines.json` | Hasil TTS: file wav per kalimat + durasinya |
| `rp.py` (EP01) / `base.py` (EP02+) | Mesin + komponen gambar + layout + time-warp + CLI |
| `stroop.py` (EP02) / `episode.py` (EP03+) | Episode: mengisi `GROUPS`, `CAPS`, judul, fungsi scene `g0..g5`, `build_sfx()` |
| `audio.py` | Musik lo-fi sintetis, kamus `SFX`, mixing + ducking musik di bawah suara |
| `gemini_tts.py` | Panggil Gemini TTS, simpan wav 44.1 kHz, mode `script` memotong per kalimat |
| `vo_rest.py`, `countdown.py`, `tighten_countdown.py` | Alat suara EP02 (lihat "Jebakan suara") |
| `voice.sh`, `vo_full.py` (EP03+) | Suara resep EP01: `gemini-3.1-flash-tts-preview` + instruksi gaya EP01, 1 request. EP04: dipotong dengan `split_lines` (jeda panjang + durasi sebanding panjang kalimat); `--split-only` memotong ulang `vo/full.wav` tanpa request baru |
| `tighten.py` (EP04) | Pendekkan jeda > 0,3 dtk di dalam kalimat (kecepatan bicara tetap) supaya durasi ≤ 55 dtk |
| `logo*.py`, `premium.py`, `v3.py` | Gambar logo kepala + pintu untuk outro (`logo_rp.c4`) |
| `fonts/` | Plus Jakarta Sans + JetBrains Mono (OFL) |

Pola untuk episode baru adalah pola **EP04** (salin `ep04_pura-pura-gapapa/`, tanpa `vo/` dan `preview/`): `base.py` dipakai sebagai library, `episode.py` menimpa `b.GROUPS`, `b.CAPS`, `b.draw_title`, `b.DRAWERS`, lalu punya `build_sfx()` dan CLI sendiri. EP03 juga menimpa `b.draw_bg` (aurora + bokeh) dan `b.draw_groups` (ilustrasi memudar lembut sebelum zona caption, plus peringatan kalau `save()`/`restore()` tidak seimbang).

## Pipeline
```
vo.py ──TTS──> vo/lNN.wav + lines.json
           └─> episode.py timeline  (time-warp + jadwal SFX + posisi suara)
                 ├─> audio.py       (musik + SFX + suara, ducking)  -> audio.wav
                 └─> episode.py video (render frame skia -> ffmpeg)  -> raw.mp4
ffmpeg mux + loudnorm -14 LUFS -> final.mp4
```

**Time-warp:** animasi ditulis dalam "waktu animasi" (DUR = 42 dtk). Kalau sebuah kalimat lebih panjang dari jendelanya (anchor ke anchor berikutnya), jendela itu otomatis diperlambat supaya suara dan animasi tetap sinkron. Durasi akhir mengikuti panjang suara.

## Layout (wajib dipatuhi)
| Zona | y (px) | Isi |
|---|---|---|
| Tag (+ progress bar di EP01–02; sejak EP03 tanpa progress bar) | 404 | `GROUPS[i][2]`, contoh `RISET · 2000` |
| Judul | 482 | `draw_title`, format "X, [kok bisa]?" (bagian dalam `[...]` berwarna aksen) |
| Ilustrasi | 560 – 1200 | semua gambar scene |
| Caption baris 1 / 2 | 1252 / 1340 | `CAPS`, kata dalam `[...]` diberi highlight |
| Watermark | 1440 | "RUANG PIKIR" |
Bawah 1500 dibiarkan kosong (tertutup UI Instagram/TikTok).

**Gaya sinematik (EP04, gaya standar sekarang):** judul y 232 hanya di adegan pertama; tanpa tag & progress bar; ilustrasi y 260–1220 (memudar lembut di tepi); caption per frasa di tengah y 1332 (1–2 baris, 56 px, tanpa kotak); watermark 1440. Adegan didefinisikan di `b.GROUPS` (9 adegan pendek), caption di `PHRASES` [(waktu, teks)] yang disinkronkan ke jeda suara.

## Komponen siap pakai
Di `base.py`: `person()` (karakter kapsul: mood neutral/worried/happy, sweat, phone, shirt), `spotlight()`, `watcher_eye()`, `scribble()` (pikiran kusut), `pill()`, `sparkle()`, `caption_line()`, `tracked()`, easing `eo/ei/eio/bo/bump`, `prog(t,a,b)`.
Di `stroop.py`: `neon_word()`, `card()`, `ring()`, `brain()`, `eye()`, `stamp()`, contoh grafik batang, gelembung komentar, outro logo.
Di `ep03_panggil-nama/episode.py` dan `ep04_pura-pura-gapapa/episode.py` (gaya premium): `glass()` (kartu kaca), `sheen()` (kilau lewat), `rays()` (sinar berputar), `halo()`, `bubble_path()`/`draw_bubble()` (gelembung bicara), `rich()` (teks dengan kata beraksen), `chip()`, `check_mark()`/`x_mark()` (centang/silang digambar), `ghost()` (sosok bercahaya), `name_badge()`, `mic()`, `stopwatch()`, widget detak jantung (`ecg()`), meter cemas, kemudi, daftar komentar + kolom ketik. EP04 v1 (arsip di riwayat git) menambah `smile_mask()` (topeng senyum + retak), `gauge()` (meter tekanan), `storm()` (badai di dada), detak makin cepat (`accel_phase`/`beat_times`, dipakai juga untuk SFX), `icon()` (wajah/awan/hati/gembok/putar), `tear()`, `meter_row()` (batang hasil dengan penanda pembanding), `flip_card()` (kartu pikiran dibalik). EP04 gaya sinematik: `sphere()` (bola 3D lembut + label), `floor()`/`sag_y()` (lantai yang melengkung karena beban), `face()` (wajah di bola), `pill_bar()` (batang perbandingan berlabel), `head_outline()` (siluet kepala+bahu dari logo), `eye()`, `thought_chip()` (pikiran + coret), `draw_captions()` per kata, `draw_groups()` dengan kamera halus. EP05: `portrait()` (potret asimetris; `mirror`, `flipx` untuk animasi membalik, `glitch` efek kamera), `phone()` (ponsel kaca dengan UI kamera/editor + kilat), `mirror_frame()` (cermin oval berkilau), `polaroid()`, `heart_fly()`, `flip_state()` (bolak-balik cepat untuk hook). EP06 (gaya garis neon + tipografi kinetik): `partial()`, `neon()`, `head_line()`, `text_path()`/`outline_text()`, `slam()`, `waves()`, `loop_arrow()`, `heart_line()`, `thought_bubble_line()`. EP07 (gaya dunia 3D + UI medsos): `plane_m()`/`plane` (gambar di bidang 3D miring lewat `Matrix.setPolyToPoly`, perspektif F=1500 ke pusat 540,760; sisi belakang kartu: cek `facing()` lalu `scale(-1, 1)`), `P3()`, `extrude()` (teks 3D), `phone()` (ponsel kaca + layar kunci + banner), `notif()`, `head_solid()` (kepala padat + cahaya tepi), `orbit()` (kartu komentar berputar urut kedalaman, objek tengah digambar di antara), `gauge()`/`gauge_phys()` (alat ukur jarum + bingkai logam), `crack()`, `research_card()` (kartu riset berputar masuk + bisa dibalik), `avatar()`, `tube()`, `sitter()`/`stander()`/`bust()` (siluet padat), `brain()`, `smoke_alarm()`, `knob()`, `thought()`, `stamp()`. Animasi padat membuat file lebih besar, jadi EP07 di-encode CRF 26 (SSIM 0,996). EP08 (gaya meja belajar malam): `laptop()` + `doc_screen()`, `phone2()` + `feed_screen()`, `blob()` (makhluk asap bermata), `shatter_text()` (teks 3D pecah berkeping), `mood_ball()`, `controller()`, `test_sheet()`, `ice()` (balok es membeku dari bawah), `block3d()` (balok isometrik berlabel), `stairs()`. EP09 (gaya di balik postingan): `post_card()`/`card3d()` (kartu postingan 3D yang otomatis menampilkan sisi belakang saat diputar > 90°), `scene_art()`, `glitch_text()`, `bar3d()`, `masked()` (topeng senyum), `berg()` (gunung es). EP10 (gaya energi emosi, **format 30 detik**): `orb()` (bola magma yang bisa `burst`/retak lalu `cool` jadi mint), `heat_waves()`, `heat_at()` (latar ikut memerah), `input_bar()`, `angry_face()`, `scanner()` (cincin MRI), `brain_lab()` (amigdala vs prefrontal), `pot()`, `jar()`. Untuk video 30 detik: turunkan `DUR` di `base.py` folder episode (outro + 5.4), rapatkan anchor di `vo.py`/`vo/lines.json` ke durasi tiap baris suara (+0,45–0,8 dtk), ganti `41.7` di `draw_captions` dengan `b.DUR - 0.3`, dan mulai outro `gJ` di anchor terakhir. EP11 (gaya kamar jam 2 pagi + arsip ingatan): `bedroom()`, `polaroid()`/`pol3d()` (`heat`, `soft`), `cringe_face()`, `cabinet()`, `chips_flow()`. EP12 (gaya panggung sinematik + tokoh kapsul premium, penerus EP01/EP03): `hero()` (mood worried/excited/calm/happy, `tremble`, `sweat`, `glow`), `stage()` (tirai beludru, lantai mengilap, lampu sorot volumetrik, `warm`), `ecg_path()`, `heart_big()`, `say()`, `mic_stand()`, `note()`, `podium()`, `eyes_ring()`. EP13 (kamar malam + tokoh kapsul berbaring): `sleeper()` (mata melotot → kelopak berat → terpejam, headphone), `sheep()`, `fence()`, `dclock()`, `siren()`, `eye_icon()`, `cloud_bubble()`, `night_room()`. EP14 (kafe malam + dua tokoh kapsul ngobrol): `cafe_bg()`, `table()` (`legs`), `conn_meter()`, `chat_panel()`, `ear()`, `two_chat()`. EP15 (ponsel chat + dua tokoh berjauhan): `chat_phone()` (riwayat, `gap`, `typed` + kursor, `mystery`, `sent`/`tick`/`reply`), `typed_at()`, `msg_bubble()`, `window()`, `meter()`, `burst()`, `glass_wall()` (retak lalu pecah), `phone(btitle=...)`. EP16 (ruang ujian malam + memori kerja): `mem_panel()` (slot + balok jatuh/keluar + bar persen + PENUH!), `block3d()`, `exam_paper()` (`blank` glitch, `ans` jawaban tinta), `note_paper()` (tulisan bertahap, `mystery`), `pen()`, `desk()`, `wall_clock()`, `big_arrow()`, `score_col()`, `dna()`, `research_card(tag=...)`; `DUR` di `base.py` folder ini 41.2 (outro dipendekkan). EP17 (kafe malam + kartu pertanyaan 3D, dibangun dari EP14): `q_card()` (kartu 3D: muka pertanyaan, belakang "?" emas, `back_only`, `hl`), `wrap()`, `wob()`, `mini_card()` (kipas 36 kartu), `depth_col()` (ringan→pribadi), `shells()` (lapisan diri yang terbuka gantian), `research_card(tag=...)`. EP18 (kantor malam + ucapan terima kasih, dibangun dari EP17): `office_bg()` (jendela kota), `carton()` (kardus), `headset()` (di kepala `hero()` yang mengembalikan hx, hy, hr), `phone_icon()` (dering), `envelope()` (amplop gaji), `bar()`. EP19 (kafe malam + hati kaca, dibangun dari EP17): `glass_heart()` (hati kaca 3D berisi cairan bergelombang + gelembung, label persen), `pen()`, `coin()` (koin berputar), `clipboard()`, `favor_card()` (✓ bantuan kecil / ✗ bantuan besar dicoret). EP20 (kafe malam + kotak cerita emas, dibangun dari EP19): `story_box()` (kotak emas: `open_` tutup terbuka ke belakang + pancaran cahaya, `lock` gembok terbuka), `padlock()`, `orb()`, `fly_orb()` (bola cerita terbang dengan jejak), `call_frame()` (bingkai video call), `race_bar()`. EP21 (kolam dangkal → lautan dalam, dibangun dari EP20): `gauge(..., ends=False, read=..., pct=...)` (alat ukur HUD dengan teks bebas, mis. DIKIRA TINGGI → KENYATAAN RENDAH), `sea_bg()` (bawah laut + sorot cahaya, tanpa titik), `water_front()` (air kolam di depan tokoh), `depth_meter()`, `deep_card()`, `float_hero()`, `compare_bars()` (dikira vs kenyataan tanpa angka), `choice_card()`. EP22 (toples pujian emas, dibangun dari EP21): `jar()` (toples kaca: gelembung pujian di dalam, `lid` tutup terlempar, `shake`), `magnifier()`, `praise_card()`. **Lagu orisinal:** `ep22_puji-aja/audio.py` mengganti `music()` dengan lagu lo-fi pop 96 BPM (e-piano Fmaj7–G6–Em7–Am7, bass, kick/clap/hat swing, melodi `lead()` yang catchy, chime tiap 4 bar) dan menaikkan volume musik (`m_gain` 0.85, ducking 0.58 saat ada suara). Salin `audio.py` itu kalau episode lain perlu lagu yang lebih menonjol (EP23 memakai variasinya: `TR = 2` naik 2 semitone, 100 BPM). Versi tanpa musik untuk lagu TikTok/IG: `MUSIC=0 python3 audio.py timeline.json audio_nomusic.wav`, lalu mux ke video. EP23 (baterai sosial): `battery3d()` (baterai kaca 3D: isi hijau→kuning→merah, segmen, persen, `charging` petir, `warn` kedip), `bat_col()`, `fun_card()` (ketawa/ngobrol/foto), `bed()`, `big_clock()`. EP24 (minta maaf): `crack_heart()` (hati kaca: `crack` retak, `split` terbelah dua, `chill` membeku, `gold` disambung emas ala kintsugi), `piece()` + `piece_path()` (keping puzzle kaca 3D yang saling mengunci), `secret_card()` (kartu KALIMAT buram + gembok; buka dengan `reveal`), `thermo()`, `frost()` (kristal es tanpa titik), `plane_icon()`; lagu `TR = -2`, 92 BPM. Teknik hook: tampilkan jawaban yang **disensor** di detik ±4, lalu buka di tengah video supaya penonton bertahan. EP25 (kerja kelompok): `team()` (4 tokoh kapsul di balik meja panjang + `laptop()`), `pie3d()` (diagram lingkaran 3D; total > 100% menumpuk jadi lapisan kedua merah yang bergetar), `counter()` (angka persen 3D putih -> merah/mint), `bar_pct()` (batang persen dengan garis BATAS 100%), `task_card()` (kartu tugas terang dicentang vs gelap buram "?"), `group_phone()` (grup chat KELOMPOK 3); lagu `TR = 0`, 104 BPM. Hook angka: penghitung yang melonjak melewati 100% + alarm di detik pertama. EP26 (makasih udah nunggu, sekuel EP24): tokoh telat berlari masuk + jam berputar, `secret_card(..., 'PENGGANTI', ...)` dibuka saat kalimatnya diucapkan, `group_panel()` (panel kelompok eksperimen A vs B), `svc_icon()` (ikon pesanan/paket/antre), `crown()`, `spot()` (lampu sorot); lagu `TR = 1`, 98 BPM. EP27 (teman curhat): `monitor()` (monitor kaca + `ecg_path()` berjalan; `rate` cepat/lambat, `alarm`, panah naik/turun), `worksheet()` (lembar soal hitungan + timer melingkar); lagu `TR = -1`, 94 BPM. EP28 (ada saran?): `thumb()` (jempol), `idea_card()` (kartu saran konkret ✓), `ask_panel()` (panel kelompok + laptop + jawaban); lagu `TR = 2`, 102 BPM. Catatan suara EP28: TTS membaca lambat (76 dtk mentah), `tighten.py 0.21` memangkas jeda jadi ±40 dtk — selalu cek total setelah tighten. EP29 (jarang nelpon orang tua): `chat_phone2()` (ponsel chat Ibu: gelembung + coretan, label Dibaca, `call` berganti ke layar Memanggil Ibu dengan cincin dering), `ibu()` (tokoh kapsul berkerudung: `hero()` + kerudung dari `skia.Op` union/difference), `house()` (rumah malam, jendela hangat), `moon()`, `mini_phone()` (`ring` bergetar, `call` layar hijau), `handset()`, `envelope_icon()`, `stopwatch()`, `msg()`, `secret_card2()` (kartu kalimat dua baris), `ghost_bar()` (batang putus-putus yang "dikira"); lagu `TR = -2`, 90 BPM. Catatan suara EP29: pemotongan otomatis menaruh "Hasilnya?" di akhir baris sebelumnya; cek tiap baris dengan transkripsi dan pindahkan potongan di jeda energi (lalu perbarui `dur` dan `anchor` di `vo/lines.json`). EP30 (makin jauh dari orang tua, format 3 alasan): `reason_card()` (kartu ALASAN kaca dua baris, disensor + gembok, `c=CORAL` untuk alasan paling nyakitin), `reason_head()`, `grow_kid()`, `hourglass()` (jam pasir kaca + pasir jatuh), `tension_bar()` (meter TEGANG vertikal yang memerah + bergetar), `vbar()` (batang vertikal tanpa angka), kalender minggu (52 × 20 kotak, satu kotak emas per tahun); lagu `TR = -3`, 86 BPM. Kalau suara terlalu panjang: `tighten.py 0.15`, lalu di `base.py` folder episode turunkan `DUR` (outro) dan jeda antarbaris (`need = dur + 0.26`), hitung ulang anchor. EP31 (suara Ibu & otak remaja): `dial()` (kenop radio kaca dua kanal, jarum + getar statis), `voice_arcs()` (busur suara dari mulut), `joy_orb()` (bola pusat rasa senang menyala + sinar; warna `ORB_ROSE`/`ORB_BLUE`/`ORB_DIM`, `mix3()`), `headphones()` (di kepala `hero()`), `mri()` (cincin fMRI + kepala profil + garis pindai), `city()` (kota malam), `brain_panel()` (kepala + bola + dua `vbar()`); lagu `TR = -1`, 94 BPM. Saat memotong header dari episode sebelumnya, cek helper yang masih dipakai (mis. `vbar()` dari EP30). EP32 (susah move on): `ig_phone()` (ponsel profil medsos 'dia': cincin story, angka post/pengikut, grid foto yang digulir dengan `scroll`, `xmark` silang + stempel STOP), `ex_photo()` (polaroid siluet 'dia'), `ex_avatar()`, `broken_heart()` (hati retak lalu terbelah; rotasi tiap belahan berpusat di hati), `way_card()` (kartu CARA 01/02 bisa ditandai CINTA NGGAK TURUN, 03 terkunci memakai `secret_card2()`), `ORB_RED`; `base.py` kembali DUR 42 + jeda 0.35 (suara ±43 dtk); lagu `TR = -1`, 98 BPM. Catatan suara: "kebiasaan nyebelin dia" terdengar "kebiasaannya belia", jadi kalimat diubah ke "kebiasaan dia yang nyebelin"; selalu cek kata kunci dengan transkripsi. EP33 (tulis daftar tugas besok): helper kamar tidur EP13 (`sleeper()`, `night_room()`, `dclock()`, `cloud_bubble()`, `sheep()`, `siren()`, `eye_icon()`) disalin ke folder ini, ditambah `paper()` (kertas bergaris: judul, item centang/kotak, `blur` untuk sensor, `hl` sorot item), `zzz()` (`rise` atur tinggi), `swirl_tasks()` (chip tugas berputar); lagu `TR = -2`, 84 BPM. EP34 (napas aneh / cyclic sighing): `lungs()` (paru-paru kaca + trakea, isi cairan bergelombang sesuai `fill`), `breath_pattern()` + `breath_graph()` (grafik tarik–tarik lagi–buang panjang yang tergambar bertahap + label), `breath_circle()` (lingkaran panduan napas membesar/mengecil + label TARIK/LAGI/BUAAANG); dipakai juga `stage()`, `monitor()`, `vbar()`, `crown()`; lagu `TR = -1`, 88 BPM. EP35 (digantungin): `dm_phone()` (ponsel DM dengan nama/status bebas, gelembung `msg()`, `typing` = gelembung tiga titik "mengetik..."), `hanging_heart()` (hati di ujung tali yang berayun, `swing`, `q` tanda tanya), `profile_card()` (kartu profil kaca + mata `eye_icon()`), `cond_card()` (kartu kondisi hati penuh/biasa/ragu); lagu `TR = 1`, 96 BPM. Catatan transkripsi: transkripsi gabungan sering menggabung atau menggeser baris; cek baris yang meragukan satu per satu. Nama asing yang sulit (mis. Pychyl, McGaugh → "Mekgo") ditulis fonetik di `vo.py` (Pitchil) lalu dicek dengan transkripsi; caption tetap ejaan asli. **Catatan skia-python:** `PathMeasure.getSegment(..., dst, ...)` menimpa `dst`, bukan menambahkan; untuk path dengan beberapa kontur, ambil tiap potongan ke path sementara lalu `addPath`.

Aturan gerak: elemen muncul dengan `bo()` (back-out pop) 0.3–0.5 dtk; antar scene crossfade 0.35 dtk + zoom 5%; tidak ada elemen penting yang muncul < 0.3 dtk sebelum dibacakan.

## SFX tersedia (`audio.SFX`)
whoosh, swish, zoom, plop, pop, tick, chop, crack, fizz, fizz_soft, rise, sting, blink, plip, zap, zap2, ding, ding_soft, card, boing, shine, clunk, heart, stamp, beep, go, buzzer, clock.

## Jebakan suara (penting)
- **Suara resmi = resep EP01** (dipilih ALFA, 27 Okt 2026, acuan video "Jam 2 pagi, kok overthinking?"): `gemini-3.1-flash-tts-preview` + `STYLE` EP01 + "Beri jeda sekitar satu detik di antara setiap baris.", semua kalimat 1 request, `split_by_pauses`. Ciri terukur: nada median ±185 Hz, ±16 karakter/detik, ekspresif. Diukur dengan MFCC, audio final EP03 berjarak 0,32 dari video acuan (EP01 0,29; EP02 0,51).
- EP02 memakai `gemini-3.8-flash-tts` (nada ±150 Hz, lebih kalem); suaranya terdengar seperti orang lain. Model ini sekarang **membacakan prefix gaya** (prefix EP02, versi Inggris, format "DIRECTOR'S NOTES / TRANSCRIPT" semuanya ikut terbaca, dicek 27 Okt 2026). Jangan dipakai lagi.
- `gemini-3.1-flash-tts-preview` dengan prefix pendek EP02 nadanya jadi terlalu tinggi (±216 Hz); pakai `STYLE` panjang EP01. `gemini-2.5-flash-preview-tts` memotong kalimat terakhir.
- Mempercepat/memperlambat suara (time-stretch) membuat suara terdengar seperti orang lain; jangan dipakai.
- Prompt gaya yang panjang kadang **ikut dibacakan** oleh model. Pakai prefix gaya pendek (mis. "Ucapkan dengan santai, ramah, dan antusias seperti kreator TikTok:") atau tanpa prefix, dan **cek durasi**: tolak hasil yang > 2× perkiraan (±14 karakter/detik).
- Kalimat dengan jeda internal (hitung mundur) jangan digabung dalam satu request: buat terpisah (`countdown.py`), lalu rapatkan jedanya (`tighten_countdown.py`).
- Banyak kalimat dalam satu request lalu dipotong (`vo_rest.py`) lebih hemat kuota dan suaranya lebih konsisten. Dengan instruksi "beri jeda sekitar satu detik" (resep EP01), jeda di dalam kalimat ("Hasilnya?", "Misalnya,") bisa sama panjang dengan jeda antarkalimat, jadi pakai `split_lines` EP04 dan tetap cek dengan transkripsi. Model kadang menambah "Hmm" di awal: cek transkripsi baris pertama dan buang kalau ada.
- Kuota gratis: ±3 request/menit per model + batas harian. Kena 429 → tunggu, atau ganti `GEMINI_TTS_MODEL`.

## QA sebelum diserahkan
1. `python3 episode.py preview t1 t2 ...` untuk ±12 titik waktu, lalu susun jadi contact sheet dan periksa.
2. Tidak ada tumpang tindih teks; ilustrasi tidak masuk zona caption.
3. Glyph khusus (★ ✓ Ψ) tidak tersedia di font. Gambar sebagai bentuk, jangan sebagai teks.
4. Setelah render: `ffmpeg -i final.mp4 -af ebur128 -f null -` → Integrated sekitar −14 LUFS.
5. Tonton bagian awal: hook harus terbaca dalam 2 detik pertama.
