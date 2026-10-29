import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Kalau kamu ngerasa cuma kamu yang hidupnya berantakan, otakmu lagi salah hitung.',
    'Teman liburan, teman wisuda, teman jadian. Kamu? Rebahan sambil overthinking.',
    'Tahun dua ribu sebelas, psikolog Alex Jordan di Stanford meneliti ini.',
    'Mahasiswa diminta menebak: berapa banyak temannya yang lagi sedih, atau habis bertengkar?',
    'Hasilnya? Soal yang sedih, tebakan mereka terlalu rendah. Soal yang seneng-seneng, terlalu tinggi.',
    'Bahkan ke sahabat dan teman sekamar sendiri.',
    'Soalnya, rasa sedih biasanya disembunyikan. Yang dipamerkan cuma bagian bahagianya.',
    'Dan yang paling salah tebak, cenderung paling kesepian.',
    'Jadi kamu nggak sendirian. Coba tanya kabar temanmu hari ini, yang beneran.',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.5, 8.68, 12.48, 17.32, 22.64, 25.03, 29.54, 32.53, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
