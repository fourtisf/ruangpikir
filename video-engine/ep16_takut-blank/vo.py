import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS; "Sian Bailok" = ejaan fonetik Sian Beilock.
TEXTS = [
    'Besok ujian, tapi takut blank? Sepuluh menit sebelum mulai, tulis ini.',
    'Soalnya pas cemas, pikiran kayak nanti salah, nanti nilainya jelek, ikut makan tempat di memori kerja otakmu.',
    'Tahun dua ribu sebelas, psikolog Gerardo Ramirez dan Sian Bailok menguji ini.',
    'Sebelum ujian yang menegangkan, sebagian mahasiswa cuma duduk diam, sebagian lagi menulis semua kekhawatirannya selama sepuluh menit.',
    'Hasilnya? Yang cuma diam, nilainya anjlok. Yang menulis, nilainya justru naik.',
    'Di ujian biologi anak SMA, efeknya paling terasa buat yang gampang cemas.',
    'Soalnya kekhawatiran yang udah pindah ke kertas, nggak lagi menuh-menuhin kepala.',
    'Jadi sebelum ujian, tulis semua takutmu sepuluh menit. Kamu ujian apa minggu ini? Tulis di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.69, 9.2, 13.09, 19.82, 23.76, 27.45, 31.54, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
