import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Mau dibantu lagi? Tambahin dua kata ini: makasih banyak.',
    'Kedengarannya sepele. Tapi habis dibantu, kita sering cuma bales: oke.',
    'Psikolog Adam Grant menguji ini di sebuah kampus, tahun dua ribu sepuluh.',
    'Petugas penggalang dana, yang kerjanya sering ditolak, sebagian didatangi atasannya, cuma buat bilang: makasih banyak atas kerja kerasnya.',
    'Hasilnya? Minggu itu, mereka menelepon sekitar lima puluh persen lebih banyak.',
    'Padahal gajinya sama, dan nggak ada bonus.',
    'Soalnya ucapan terima kasih bikin orang merasa dihargai, dan pengen bantu lagi.',
    'Jadi habis dibantu, jangan cuma bilang oke. Bilang: makasih banyak! Kamu mau makasih ke siapa? Tulis di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.3, 7.23, 11.33, 19.08, 23.46, 25.82, 30.25, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
