import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (dihitung ulang setelah suara jadi; ubah juga vo/lines.json). Angka & tahun ditulis dengan huruf.
TEXTS = [
    'Makin akrab sama teman, gara-gara sama-sama nggak suka orang yang sama? Ternyata ada risetnya.',
    'Tahun dua ribu enam, Jennifer Bosson dan timnya nanya mahasiswa soal awal kenal sahabatnya.',
    'Hasilnya? Yang lebih banyak diingat: sama-sama nggak suka orang lain.',
    'Di eksperimen, orang asing yang sama-sama agak nggak suka seseorang, malah terasa kayak udah kenal lama.',
    'Lucunya, kita nggak sadar. Kita ngira, sama-sama suka yang bikin dekat.',
    'Tapi nggak harus ngomongin orang. Coba ganti musuh bersamanya jadi ini.',
    'Macet, tugas numpuk, atau hujan pas mau pulang.',
    'Kirim ke partner ghibah-mu, terus tulis di komentar: selain orang, musuh bersama kalian apa?',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.14, 10.05, 14.02, 18.99, 23.47, 28.39, 31.41, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
