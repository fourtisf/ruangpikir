import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS. "Gebel" = ejaan fonetik Gable.
TEXTS = [
    'Mau hubunganmu awet? Ternyata yang paling penting bukan cara kamu menghibur pas dia sedih.',
    'Tahun dua ribu enam, peneliti Shelly Gebel dan timnya merekam pasangan yang saling cerita.',
    'Ada cerita sedih, ada kabar baik. Dua bulan kemudian, hubungan mereka dicek lagi.',
    'Hasilnya? Cara merespon kabar baik lebih terkait sama awet atau putusnya hubungan.',
    'Respon datar kayak: wah, selamat ya. Malah cerita diri sendiri. Atau nyari kurangnya. Itu nggak bikin dekat.',
    'Yang bikin makin dekat cuma satu: respon yang antusias, terus nanya lebih lanjut.',
    'Jadi kalau dia cerita kabar baik, coba bilang: serius? Gimana ceritanya?',
    'Kirim video ini ke orang yang selalu antusias dengerin ceritamu!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.37, 9.83, 14.39, 18.56, 24.54, 29.19, 33.38, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
