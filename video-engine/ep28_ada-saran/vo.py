import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS. "Jaewon Yun" = ejaan fonetik Jaewon Yoon.
TEXTS = [
    'Mau masukan yang beneran berguna? Jangan tanya: ada feedback? Ganti satu kata ini.',
    'Biasanya jawabannya cuma: bagus kok, udah oke.',
    'Tahun dua ribu sembilan belas, peneliti Harvard Jaewon Yun dan timnya menguji ini.',
    'Ada yang dimintai feedback. Ada yang dimintai saran.',
    'Hasilnya? Yang dimintai saran memberi tiga puluh empat persen lebih banyak hal yang bisa diperbaiki, dan lima puluh enam persen lebih banyak caranya.',
    'Soalnya feedback bikin orang menilai yang udah lewat. Saran bikin orang mikir ke depan.',
    'Di riset lapangan dengan puluhan ribu komentar pun, hasilnya sama.',
    'Jadi habis presentasi atau kirim tugas, coba tanya: ada saran, nggak?',
    'Kirim video ini ke teman yang lagi ngerjain skripsi!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.01, 8.59, 12.76, 15.49, 22.65, 27.14, 30.82, 34.28, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
