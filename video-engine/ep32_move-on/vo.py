import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Susah move on? Otakmu lagi kayak orang ketagihan. Jangan stalking, coba satu trik ini.',
    'Tahun dua ribu sepuluh, Helen Fisher memindai otak orang yang baru diputusin.',
    'Pas lihat foto mantannya, area otak yang aktif mirip otak orang yang lagi kecanduan.',
    'Riset lain nemuin, yang sering kepoin medsos mantan, lebih kangen dan lebih susah pulih.',
    'Terus caranya? Tahun dua ribu delapan belas, Sandra Langeslag menguji beberapa cara.',
    'Hasilnya? Yang bikin rasa cinta turun: ingat-ingat kebiasaan dia yang nyebelin.',
    'Memang awalnya bikin sedih. Jadi habis itu, alihkan ke hal yang bikin kamu senang.',
    'Kirim video ini ke teman yang masih stalking mantannya!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.63, 10.08, 14.66, 19.88, 24.12, 28.72, 33.98, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
