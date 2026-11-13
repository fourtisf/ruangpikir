import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Mau tahu apa yang paling berarti buat seseorang? Tanya satu pertanyaan ini.',
    'Rumahmu kebakaran. Semua orang dan hewan peliharaanmu udah aman. Kamu cuma sempat ambil satu barang. Apa?',
    'Ini pertanyaan nomor tiga puluh empat, salah satu yang paling dalam dari tiga puluh enam pertanyaan Arthur Aron.',
    'Jawabannya sering nunjukin apa yang paling berarti buat kita, dan kenapa.',
    'Tapi kita sering takut nanya hal sedalam ini. Takut canggung.',
    'Padahal riset Michael Kardas tahun dua ribu dua puluh dua nemuin: obrolan yang dalam nggak secanggung yang kita kira.',
    'Orang lain ternyata lebih tertarik dengerin cerita kita, daripada yang kita bayangin.',
    'Kamu sendiri, barang apa yang kamu ambil? Tulis di komentar, terus kirim ke temanmu!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.4, 10.16, 15.52, 19.76, 23.15, 28.92, 32.44, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
