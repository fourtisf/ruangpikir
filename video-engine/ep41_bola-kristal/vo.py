import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS. "Gigerenser" = ejaan fonetik Gigerenzer.
TEXTS = [
    'Satu pertanyaan ini bikin semua orang mikir lama.',
    'Kalau ada bola kristal yang bisa kasih tahu satu kebenaran, tentang dirimu, hidupmu, atau masa depanmu, kamu mau tahu apa?',
    'Ini pertanyaan nomor tiga belas, dari tiga puluh enam pertanyaan psikolog Arthur Aron.',
    'Mungkin kamu langsung kepikiran: jodohku siapa? Aku bakal sukses nggak?',
    'Tapi tahun dua ribu tujuh belas, Gerd Gigerenser dan timnya nanya lebih dari dua ribu orang.',
    'Hasilnya? Hampir sembilan dari sepuluh nggak mau tahu kabar buruk masa depannya. Yang selalu pengen tahu, cuma satu persen.',
    'Soalnya kita takut menyesal setelah tahu, dan pengen hidup tetap ada kejutannya.',
    'Kamu sendiri, mau tahu apa? Atau mending nggak usah? Tulis di komentar, terus kirim ke temanmu!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.19, 9.87, 14.11, 17.93, 22.4, 28.07, 32.29, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
