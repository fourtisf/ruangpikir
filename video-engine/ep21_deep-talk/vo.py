import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Takut deep talk sama orang baru? Ternyata, itu nggak secanggung yang kamu kira.',
    'Makanya kita betah di basa-basi: cuaca, kuliah di mana, udah makan belum.',
    'Tahun dua ribu dua puluh dua, psikolog Michael Kardas dan Nicholas Epley menguji ini lewat dua belas eksperimen.',
    'Orang-orang asing disuruh ngobrol dalam, misalnya: hal apa yang paling kamu syukuri?',
    'Hasilnya? Obrolannya nggak secanggung yang dikira, dan lebih bikin dekat.',
    'Bahkan yang awalnya pengen basa-basi, setelah nyoba dua-duanya, malah lebih milih deep talk.',
    'Soalnya kita meremehkan seberapa pengen orang lain ngobrol dalam juga.',
    'Jadi lain kali, coba tanya: apa yang paling kamu syukuri tahun ini? Jawab juga di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.42, 8.37, 14.43, 18.97, 22.92, 27.89, 31.68, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
