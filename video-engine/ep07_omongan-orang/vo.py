import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Di kepalamu ada alat ukur yang terus menilai: orang lain suka kamu, atau nggak.',
    'Makanya satu komentar kecil, bisa kepikiran seharian.',
    'Tahun sembilan belas sembilan puluh lima, psikolog Mark Leary menyebutnya sociometer.',
    'Harga dirimu naik turun, ikut seberapa kamu merasa diterima.',
    'Dulu, dikucilkan kelompok itu bahaya. Makanya ditolak sedikit, otak bereaksi mirip rasa sakit.',
    'Masalahnya, alat ukur ini sering kelewat sensitif.',
    'Tahun dua ribu satu, Savitsky dan timnya menemukan: kalau kita salah di depan orang, mereka nggak menilai seburuk yang kita kira.',
    'Kita yang terlalu fokus ke kesalahan sendiri.',
    'Jadi kalau omongan orang kepikiran lagi, ingat: alat ukurmu memang suka lebay.',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.43, 7.3, 11.9, 15.15, 20.24, 22.95, 29.94, 32.38, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
