import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Dia lebih suka kamu, daripada yang kamu kira.',
    'Tapi habis ngobrol, kita malah mikir: "dia ilfeel nggak, ya?"',
    'Tahun dua ribu delapan belas, psikolog Erica Boothby menelitinya.',
    'Dua orang asing dipasangkan, lalu ngobrol lima menit.',
    'Setelahnya, mereka menebak: seberapa suka lawan bicaranya sama mereka?',
    'Hasilnya? Kebanyakan menebak terlalu rendah.',
    'Lawan bicaranya ternyata lebih suka mereka, daripada yang mereka kira.',
    'Ini namanya liking gap: kita sibuk menilai diri sendiri, sampai nggak lihat sinyal suka dari dia.',
    'Bahkan di antara teman sekamar baru, salah tebak ini bertahan berbulan-bulan.',
    'Jadi, nggak usah diputar ulang di kepala. Kamu lebih disukai dari yang kamu kira.',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 2.62, 5.98, 9.55, 12.46, 16.31, 18.73, 22.58, 27.91, 32.15, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
