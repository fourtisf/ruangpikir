import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Udah jam satu malam, otak masih mikirin tugas besok? Jangan cuma merem. Tulis ini lima menit.',
    'Tahun dua ribu delapan belas, peneliti Baylor, Michael Scullin, menguji ini di laboratorium tidur.',
    'Lima puluh tujuh orang menulis lima menit sebelum tidur. Setengahnya menulis yang udah dikerjain hari ini. Setengahnya lagi, hal lain.',
    'Hasilnya? Yang menulis daftar tugas buat besok, tidur sembilan menit lebih cepat.',
    'Dan makin rinci daftarnya, makin cepat mereka tidur.',
    'Soalnya otak nggak perlu terus mengulang hal yang takut dilupain. Udah aman di kertas.',
    'Jadi malam ini, ambil kertas, tulis daftar tugas buat besok, baru tidur.',
    'Kirim video ini ke teman yang suka begadang mikirin tugas!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.93, 10.89, 17.02, 21.44, 24.66, 29.37, 33.94, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
