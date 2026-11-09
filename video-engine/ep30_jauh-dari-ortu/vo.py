import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Angka ditulis dengan huruf. Ejaan fonetik untuk TTS: "Karstensen" = Carstensen, "Birdit" = Birditt, "Bengtsen" = Bengtson.
TEXTS = [
    'Makin dewasa, kok makin jauh dari orang tua? Ini tiga alasan psikologis yang agak nyakitin.',
    'Pertama: kita ngerasa waktunya masih banyak, jadi sibuk ngejar hal baru.',
    'Tapi di riset Laura Karstensen, begitu anak muda bayangin bakal pindah jauh, mereka milih orang yang paling berarti.',
    'Kedua: nasihat yang nggak diminta. Riset Kira Birdit nemuin, ini salah satu pemicu tegang yang paling bikin masalah.',
    'Ketiga, yang paling nyakitin: orang tua ngerasa lebih dekat ke kamu, daripada kamu ke mereka.',
    'Vern Bengtsen nemuin pola ini berulang, selama dua puluh tahun.',
    'Kalau kamu cuma pulang seminggu setahun, dua puluh tahun ke depan cuma seratus empat puluh hari.',
    'Jadi bukan karena nggak sayang. Mulai dari telepon sebentar, malam ini.',
    'Kirim video ini ke teman yang lagi jauh dari rumah!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.39, 8.78, 14.3, 19.5, 24.05, 27.23, 31.21, 34.56, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
