import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (dihitung ulang setelah suara jadi; ubah juga vo/lines.json). Angka & tahun ditulis dengan huruf.
TEXTS = [
    'Anak sulung pasti galak, bungsu pasti manja? Riset dua puluh ribu orang bilang: itu mitos.',
    'Tapi tahun dua ribu lima belas, Julia Rohrer dan timnya ngecek data lebih dari dua puluh ribu orang, di Amerika, Inggris, dan Jerman.',
    'Hasilnya? Urutan lahir nggak ngaruh ke kepribadian. Nggak bikin kamu lebih supel, lebih rajin, lebih ramah, atau lebih gampang cemas.',
    'Riset lain dengan tiga ratus tujuh puluh tujuh ribu siswa juga sama: bedanya hampir nol.',
    'Satu-satunya beda: anak pertama unggul sekitar satu poin IQ. Itu pun nyaris nggak kerasa.',
    'Jadi kalau kamu dicap galak atau manja, itu bukan karena nomor urut lahirmu.',
    'Kamu anak ke berapa? Tulis di komentar, terus tag kakak atau adikmu!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.64, 12.74, 19.6, 24.16, 29.27, 33.57, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
