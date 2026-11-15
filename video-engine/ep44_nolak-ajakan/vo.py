import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (dihitung ulang setelah suara jadi; ubah juga vo/lines.json). Angka & tahun ditulis dengan huruf.
TEXTS = [
    'Nggak enak nolak ajakan teman? Riset bilang, kamu terlalu khawatir.',
    'Tahun dua ribu dua puluh tiga, peneliti Julian Givi dan Colleen Kirk nguji ini lewat beberapa eksperimen.',
    'Hasilnya? Orang yang nolak ngira temannya bakal marah, kecewa, dan nggak ngajak lagi.',
    'Padahal yang ngajak, lebih santai dari yang kita bayangin.',
    'Tapi jangan jawab "liat nanti ya". Riset lanjutan mereka nemuin, jawaban "mungkin" malah terasa kurang dihargai, dibanding "nggak" yang jelas.',
    'Jadi kalau mau nolak, coba pakai kalimat ini.',
    'Makasih banget udah ngajak! Kali ini aku nggak bisa, lain kali ya.',
    'Kirim ke temanmu yang paling nggak enakan, terus tulis di komentar: kamu paling susah nolak apa?',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.36, 9.46, 14.26, 17.45, 25.28, 28.56, 32.06, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
