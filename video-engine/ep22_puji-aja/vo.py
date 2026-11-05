import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS; "Syuan Jao" = ejaan fonetik Xuan Zhao.
TEXTS = [
    'Pengen muji orang, tapi gengsi? Bilang aja. Dia bakal lebih senang dari yang kamu kira.',
    'Kita sering nahan pujian. Takut dikira lebay, takut suasananya jadi canggung.',
    'Tahun dua ribu dua puluh satu, psikolog Syuan Jao dan Nicholas Epley menguji ini.',
    'Orang-orang disuruh nulis pujian tulus buat temannya, lalu menebak reaksinya.',
    'Hasilnya? Yang dipuji lebih senang dari tebakan si pemuji, dan nggak secanggung yang dibayangkan.',
    'Si pemuji sibuk mikirin kata-katanya pas atau nggak. Padahal yang diingat penerima: kamu peduli.',
    'Jadi pujian sederhana pun udah cukup bikin harinya lebih baik.',
    'Yuk coba sekarang: puji satu orang di kolom komentar, atau tag dia!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.07, 9.43, 14.02, 18.38, 23.87, 29.3, 32.81, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
