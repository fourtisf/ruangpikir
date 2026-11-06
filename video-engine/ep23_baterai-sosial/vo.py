import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Habis nongkrong seru, kok langsung capek banget? Tenang, kamu nggak aneh.',
    'Ketawa, ngobrol, foto-foto. Seru! Tapi sampai rumah, rasanya pengen rebahan seharian.',
    'Tahun dua ribu tujuh belas, psikolog Sointu Leikas dari Helsinki melacak ini, lima kali sehari selama dua belas hari.',
    'Saat lagi aktif bersosialisasi, mood mereka naik, dan nggak kerasa capek.',
    'Tapi sekitar tiga jam kemudian, rasa lelahnya baru datang.',
    'Makin banyak orang yang ditemui, makin terasa capeknya. Bahkan buat yang ekstrovert.',
    'Jadi capek habis nongkrong itu wajar. Bukan berarti kamu nggak suka temanmu.',
    'Kasih waktu buat ngecas sendiri dulu. Baterai sosialmu habis setelah berapa jam? Tulis di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.15, 8.81, 15.22, 19.22, 22.4, 27.01, 31.17, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
