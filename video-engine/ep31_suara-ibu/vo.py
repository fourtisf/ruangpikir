import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Waktu kecil, suara Ibu paling bikin tenang. Pas remaja, kok jadi nyebelin? Ternyata otakmu yang pindah channel.',
    'Tahun dua ribu dua puluh dua, peneliti Stanford Daniel Abrams dan timnya memindai otak anak dan remaja.',
    'Mereka diperdengarkan suara ibunya sendiri, dan suara orang asing.',
    'Hasilnya? Di otak anak, suara Ibu bikin pusat rasa senang paling menyala.',
    'Tapi mulai sekitar umur tiga belas, kebalikannya. Suara orang baru yang bikin otak lebih menyala.',
    'Itu bukan tanda nggak sayang. Itu tanda otakmu lagi latihan mandiri, belajar dengerin dunia di luar rumah.',
    'Jadi kalau dulu kamu sering cuek ke Ibu, sekarang kamu tahu alasannya.',
    'Kirim video ini ke Ibumu, biar dia tahu kamu nggak pernah berhenti sayang.',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 6.89, 11.97, 15.1, 19.36, 23.93, 29.24, 33.16, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
