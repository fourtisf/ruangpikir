import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS. "Huberman" dibaca biasa.
TEXTS = [
    'Lagi panik atau deg-degan? Jangan cuma tarik napas dalam. Coba napas aneh ini.',
    'Tahun dua ribu dua puluh tiga, tim Stanford, termasuk Andrew Huberman, menguji ini.',
    'Sekitar seratus orang latihan lima menit sehari, selama sebulan. Ada yang meditasi, ada yang latihan napas.',
    'Hasilnya? Yang paling bikin mood naik dan napas lebih tenang, satu cara napas ini. Bahkan ngalahin meditasi.',
    'Caranya: tarik napas lewat hidung, tambah tarik sekali lagi, terus buang pelan lewat mulut, lebih panjang.',
    'Soalnya buang napas yang panjang ngasih sinyal ke tubuh buat melambat.',
    'Coba sekarang: tarik dua kali, buang panjang. Ulangi lima menit.',
    'Kirim ke teman yang besok mau presentasi!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.68, 8.91, 14.73, 20.86, 27.09, 31.03, 34.45, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
