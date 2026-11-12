import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Habis berantem, kalian diem-dieman? Jangan cuma nunggu marahnya reda. Coba satu hal kecil ini.',
    'Tahun dua ribu delapan belas, peneliti Michael Murphy dan timnya menelepon empat ratus empat orang, tiap malam.',
    'Selama dua minggu, mereka ditanya: hari ini berantem nggak? Dan hari ini dipeluk nggak?',
    'Hasilnya? Di hari ada konflik, yang dipeluk moodnya nggak anjlok separah yang nggak dipeluk.',
    'Bahkan besoknya, perasaan negatifnya juga lebih rendah.',
    'Peneliti menduga, pelukan jadi tanda dukungan: kita masih aman, kita masih baik-baik aja.',
    'Tapi pelukannya harus mau sama mau. Jadi coba tanya dulu: boleh peluk nggak?',
    'Kirim video ini ke orang yang mau kamu peluk!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 5.37, 11.56, 16.25, 21.02, 24.64, 29.92, 34.45, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
