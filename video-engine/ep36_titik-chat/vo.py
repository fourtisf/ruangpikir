import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Kamu suka bales chat pakai titik? Hati-hati. Kata riset, balasan kayak gitu bisa kedengeran nggak tulus.',
    'Tahun dua ribu enam belas, peneliti Celia Klin dan timnya menguji ini.',
    'Seratus dua puluh enam mahasiswa membaca chat yang dibalas satu kata. Ada yang pakai titik, ada yang nggak.',
    'Hasilnya? Yang pakai titik dinilai kurang tulus. Anehnya, kalau ditulis tangan, nggak ada bedanya.',
    'Soalnya di chat, kita nggak bisa dengar nada suara atau lihat muka. Jadi tanda baca yang ngegantiin.',
    'Dan titik di balasan singkat kerasa kayak nutup obrolan. Kesannya ketus, padahal kamu nggak marah.',
    'Jadi kalau balasnya cuma satu kata, coba trik kecil ini: hapus titiknya.',
    'Kirim video ini ke teman yang suka bales pakai titik!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.88, 9.4, 14.36, 20.28, 25.53, 30.53, 34.26, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
