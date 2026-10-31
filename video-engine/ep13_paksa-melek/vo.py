import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Nggak bisa tidur? Coba trik aneh ini: paksa dirimu tetap melek.',
    'Soalnya, makin dipaksa tidur, otak malah makin siaga.',
    'Tahun sembilan belas sembilan puluh enam, psikolog Daniel Wegner menguji ini.',
    'Peserta yang disuruh tidur secepat mungkin saat pikirannya sibuk, malah lebih lama terlelap.',
    'Nah, trik kebalikannya namanya paradoxical intention.',
    'Tahun dua ribu tiga, Colin Espie dan timnya meminta orang yang susah tidur berbaring dengan mata terbuka, dan berusaha tetap bangun.',
    'Hasilnya? Tekanan harus tidur hilang, cemasnya turun, dan mereka cenderung merasa lebih cepat terlelap.',
    'Jadi malam ini, jangan paksa tidur. Tantang dirimu tetap melek, terus ceritain hasilnya di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.56, 6.43, 10.6, 15.59, 18.46, 25.61, 31.18, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
