import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (dihitung ulang setelah suara jadi; ubah juga vo/lines.json). Angka & tahun ditulis dengan huruf.
TEXTS = [
    'Lihat story teman nongkrong tanpa kamu? Mungkin mereka bukan nggak mau ngajak.',
    'Tahun dua ribu dua puluh lima, Julian Givi dan timnya neliti orang yang pengen ikut, tapi nggak berani minta.',
    'Hasilnya? Kita ngira sengaja nggak diajak, dan bakal ganggu kalau minta ikut.',
    'Padahal yang punya rencana, justru pengen diminta. Sering kali, mereka cuma nggak kepikiran ngajak.',
    'Jadi jangan cuma diem terus overthinking. Coba bilang satu kalimat ini.',
    'Eh, aku boleh ikut nggak?',
    'Tapi ini buat acara santai sama orang yang udah kenal ya, bukan kondangan.',
    'Kirim ke temanmu yang suka nunggu diajak, terus tulis di komentar: kamu tim nunggu diajak, atau tim minta ikut?',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.39, 10.0, 14.15, 19.94, 25.45, 26.78, 31.21, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
