import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Kamu nggak jelek di foto. Kamu cuma belum terbiasa.',
    'Di cermin cakep, tapi di kamera belakang, kok beda?',
    'Soalnya wajah kita nggak simetris, dan di cermin, kiri jadi kanan.',
    'Tahun sembilan belas tujuh puluh tujuh, psikolog Theodore Mita mengujinya.',
    'Peserta dikasih dua foto wajahnya: versi asli, dan versi cermin.',
    'Hasilnya? Mereka lebih suka versi cermin. Tapi teman-temannya lebih suka versi asli.',
    'Ini efek paparan: makin sering kita lihat sesuatu, makin kita suka.',
    'Kamu tiap hari lihat versi cermin. Temanmu tiap hari lihat versi asli.',
    'Jadi foto yang kamu benci, bisa jadi versi yang orang lain suka.',
    'Coba balik fotomu sekarang. Mana yang lebih kamu suka? Tulis di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 2.95, 5.75, 9.37, 13.43, 16.95, 21.56, 25.24, 29.08, 32.59, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
