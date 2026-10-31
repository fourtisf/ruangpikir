import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Mau makin disukai pas ngobrol? Coba dua kata ini: terus gimana?',
    'Kebanyakan kita sibuk mikirin mau ngomong apa, biar kelihatan menarik.',
    'Tahun dua ribu tujuh belas, psikolog Karen Huang dari Harvard meneliti obrolan orang yang baru kenal.',
    'Yang lebih banyak bertanya, terutama pertanyaan lanjutan, ternyata lebih disukai.',
    'Bahkan di speed dating, mereka lebih sering diajak ketemu lagi.',
    'Soalnya, pertanyaan lanjutan bikin lawan bicara merasa didengar dan dipahami.',
    'Lucunya, kebanyakan orang nggak nyangka bertanya bisa bikin disukai.',
    'Jadi lain kali ngobrol, cukup tanya: terus gimana? Tulis pertanyaan andalanmu di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.9, 8.06, 14.06, 18.88, 22.63, 27.21, 31.25, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
