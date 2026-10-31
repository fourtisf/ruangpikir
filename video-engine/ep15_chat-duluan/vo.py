import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS; "Pegi Liu" = ejaan fonetik Peggy Liu.
TEXTS = [
    'Tiba-tiba keinget teman lama, tapi gengsi chat duluan? Kirim satu chat ini.',
    'Kita sering mikir: nanti ganggu, nanti dikira aneh, udah kelamaan nggak ngobrol.',
    'Tahun dua ribu dua puluh dua, psikolog Pegi Liu menguji ini ke lebih dari lima ribu sembilan ratus orang.',
    'Peserta diminta menyapa teman yang udah lama nggak dikontak, cukup lewat pesan singkat.',
    'Hasilnya? Yang disapa ternyata lebih senang dari yang dikira pengirimnya.',
    'Apalagi kalau chatnya nggak disangka-sangka. Makin kaget, makin senang.',
    'Jadi rasa takut ganggu itu, seringnya cuma salah tebak.',
    'Kirim aja: hai, tiba-tiba keinget kamu. Siapa yang muncul di kepalamu? Tulis inisialnya di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.38, 8.9, 14.82, 19.73, 23.85, 27.85, 30.96, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
