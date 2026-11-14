import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (dihitung ulang setelah suara jadi; ubah juga vo/lines.json). Angka & tahun ditulis dengan huruf.
TEXTS = [
    'Love language kamu apa? Plot twist: kata riset, konsep ini nggak terbukti.',
    'Konsep ini dipopulerkan Gary Chapman sejak tahun sembilan belas sembilan puluh dua.',
    'Tapi tahun dua ribu dua puluh empat, psikolog Emily Impett dan timnya ngecek bukti ilmiah soal love language.',
    'Hasilnya? Nggak ada bukti kuat kalau tiap orang cuma punya satu love language. Pasangan yang love language-nya sama, juga nggak terbukti lebih bahagia.',
    'Ternyata, kita butuh semua bentuk sayang. Kayak makanan, cinta butuh menu yang seimbang.',
    'Jadi jangan cuma nebak love language pasanganmu. Coba tanya satu kalimat ini.',
    'Hari ini, kamu lagi butuh apa dari aku?',
    'Kirim ke pasanganmu, terus tulis di komentar: kamu lagi butuh apa?',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.58, 7.98, 12.98, 19.74, 25.07, 30.56, 33.07, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
