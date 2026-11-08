import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun & angka ditulis dengan huruf supaya dibaca benar oleh TTS. "Juliana Syroder" = ejaan fonetik Juliana Schroeder.
TEXTS = [
    'Kamu ngerasa paling banyak kerja di kelompok? Faktanya, hampir semua anggota ngerasa gitu juga.',
    'Yang satu ngaku ngerjain setengah, yang lain juga. Kok bisa?',
    'Tahun dua ribu enam belas, Juliana Syroder dan Nicholas Epley menguji ini ke hampir tujuh ratus mahasiswa.',
    'Hasilnya? Kalau klaim semua anggota dijumlah, totalnya selalu lebih dari seratus persen.',
    'Makin besar kelompoknya, makin parah. Tim delapan orang bisa tembus seratus empat puluh persen!',
    'Bukan karena bohong. Kerjaan sendiri kelihatan jelas, kerjaan orang lain sering nggak kelihatan.',
    'Caranya: sebelum ngomel, sebutin dulu yang lain ngerjain apa aja. Klaim berlebihnya bakal turun.',
    'Kirim video ini ke grup kelompokmu, biar nggak saling ngerasa paling capek!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.13, 8.48, 13.56, 18.13, 22.95, 28.06, 33.51, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
