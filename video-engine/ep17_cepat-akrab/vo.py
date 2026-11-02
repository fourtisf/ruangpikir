import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Mau cepat akrab sama orang baru? Coba satu pertanyaan ini.',
    'Kalau bisa makan malam bareng siapa aja di dunia, kamu pilih siapa?',
    'Ini pertanyaan pertama dari tiga puluh enam pertanyaan buatan psikolog Arthur Aron, tahun sembilan belas sembilan puluh tujuh.',
    'Dua orang asing saling bertanya, dari yang ringan sampai yang makin pribadi, selama empat puluh lima menit.',
    'Hasilnya? Mereka merasa lebih dekat, dibanding yang cuma ngobrol basa-basi.',
    'Kuncinya: saling terbuka sedikit demi sedikit, dan gantian.',
    'Basa-basi soal cuaca nggak bikin dekat. Cerita kecil tentang dirimu, iya.',
    'Jadi lain kali kenalan, coba tanya itu. Kamu sendiri, pilih makan malam sama siapa? Tulis di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.32, 6.98, 13.87, 19.71, 23.81, 27.04, 31.03, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
