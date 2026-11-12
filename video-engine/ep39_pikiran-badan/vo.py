import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS. "Spreker" = ejaan fonetik Sprecher.
TEXTS = [
    'Mau obrolan nggak garing? Coba satu pertanyaan ini.',
    'Kalau bisa hidup sampai sembilan puluh tahun, kamu pilih punya pikiran, atau badan umur tiga puluh?',
    'Ini salah satu dari tiga puluh enam pertanyaan buatan psikolog Arthur Aron.',
    'Pertanyaannya makin lama makin pribadi, dan dijawab gantian oleh dua orang asing.',
    'Tahun dua ribu dua puluh satu, Susan Spreker menguji ulang. Mereka jadi lebih dekat, dibanding yang cuma basa-basi.',
    'Soalnya pertanyaan kayak gini bikin kita cerita soal diri sendiri, bukan soal cuaca.',
    'Jadi kalau obrolan mulai garing, lempar pertanyaan ini, terus jawab gantian.',
    'Kamu pilih mana: pikiran atau badan? Tulis di komentar, terus kirim ke temanmu!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.45, 8.93, 12.67, 16.81, 22.68, 27.62, 32.04, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
