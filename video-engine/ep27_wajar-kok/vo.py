import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS. "Chad Syenk dan Alan Frusetti" = ejaan fonetik Chad Shenk & Alan Fruzzetti.
TEXTS = [
    'Teman curhat, jangan bilang: gitu doang kok sedih. Coba ganti pakai kalimat ini.',
    'Kita kira itu nenangin, atau bilang: udah, lupain aja. Padahal bisa bikin perasaannya makin nggak enak.',
    'Tahun dua ribu sebelas, psikolog Chad Syenk dan Alan Frusetti menguji ini.',
    'Peserta diberi soal hitungan yang bikin stres, lalu ditanggapi dengan dua cara.',
    'Hasilnya? Yang perasaannya diremehkan, emosinya makin buruk dan detak jantungnya naik. Yang divalidasi, detak jantungnya justru turun.',
    'Validasi itu bukan berarti setuju. Cuma bilang, perasaanmu masuk akal.',
    'Jadi lain kali teman curhat, coba bilang: wajar kamu ngerasa gitu. Baru dengerin lagi.',
    'Kirim video ini ke teman yang paling sering kamu curhatin!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.62, 9.98, 14.09, 17.75, 24.59, 28.95, 33.95, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
