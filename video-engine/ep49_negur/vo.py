import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (dihitung ulang setelah suara jadi; ubah juga vo/lines.json). Angka & tahun ditulis dengan huruf.
TEXTS = [
    'Kamu negur pasangan, ujung-ujungnya malah berantem? Mungkin yang salah kalimat pertamamu.',
    'Tahun dua ribu delapan belas, Shane Rogers dan timnya nguji kalimat pembuka pas lagi konflik.',
    'Misalnya: pasanganmu capek pulang kerja, dan kamu beresin rumah sendirian. Kamu pengen negur.',
    'Hasilnya? Kalimat yang dibuka pakai kamu, terasa lebih menyerang, dan bikin orang defensif.',
    'Yang paling nggak menyerang: pakai aku, dan sebut perasaan dua-duanya. Perasaanmu, dan perasaan dia.',
    'Jadi jangan cuma bilang, kamu tuh. Coba kalimat ini.',
    'Aku ngerti kenapa kamu ngerasa gitu. Tapi aku ngerasanya gini.',
    'Kirim ke orang yang sering salah paham sama kamu. Biar ngobrolnya nggak jadi berantem.',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.97, 9.27, 13.9, 18.47, 23.51, 29.09, 32.6, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
