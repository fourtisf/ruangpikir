import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Jarang nelpon orang tua? Jangan cuma bales: iya, udah. Coba telepon, terus bilang kalimat ini.',
    'Kita sering nunda, karena takut canggung dan bingung mau ngomong apa.',
    'Tahun dua ribu dua puluh satu, peneliti Amit Kumar dan Nicholas Epley menguji ini.',
    'Dua ratus orang diminta menghubungi teman lama, lewat telepon atau email.',
    'Hasilnya? Mereka kira telepon bakal lebih canggung. Ternyata nggak. Malah rasa dekatnya lebih kuat.',
    'Soalnya suara membawa perasaan yang nggak kebaca di tulisan. Waktunya pun hampir sama.',
    'Kalau ke teman lama aja gitu, apalagi ke orang yang paling nungguin kabarmu.',
    'Jadi malam ini, coba telepon dan bilang: nggak ada apa-apa, cuma kangen denger suara Ibu.',
    'Kirim video ini ke teman yang lagi merantau!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.97, 9.51, 13.49, 16.91, 21.48, 25.8, 29.86, 34.69, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
