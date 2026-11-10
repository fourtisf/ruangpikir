import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS. "Witchurch" = ejaan fonetik Whitchurch.
TEXTS = [
    'Dia cuek, kok kamu makin kepikiran? Mungkin kamu bukan lagi jatuh cinta. Kamu lagi digantungin.',
    'Tahun dua ribu sebelas, peneliti Erin Witchurch dan timnya menguji ini.',
    'Mahasiswi melihat profil empat cowok, yang katanya udah lihat profil mereka juga.',
    'Ada yang dibilang: cowok-cowok itu suka banget sama kamu. Ada yang: biasa aja. Dan ada yang: nggak jelas.',
    'Hasilnya? Yang paling tertarik justru yang nggak jelas. Bahkan lebih dari yang disukai banget.',
    'Soalnya ketidakpastian bikin kita mikirin dia terus. Dan makin sering dipikirin, makin kerasa suka.',
    'Jadi sebelum baper, tanya diri sendiri: aku suka dia, atau cuma penasaran?',
    'Kirim video ini ke teman yang lagi digantungin!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 6.22, 9.74, 13.65, 19.55, 24.14, 29.52, 34.12, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
