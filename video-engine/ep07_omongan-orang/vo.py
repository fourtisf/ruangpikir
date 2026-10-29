import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Satu komentar kecil bisa kepikiran seharian. Itu bukan karena kamu lemah.',
    'Di kepalamu ada alat ukur yang terus menilai: kamu disukai, atau nggak.',
    'Tahun sembilan belas sembilan puluh lima, psikolog Mark Leary menyebutnya sociometer.',
    'Harga dirimu naik turun, ikut seberapa kamu merasa diterima.',
    'Dulu, dikucilkan itu bahaya. Jadi ditolak sedikit, otak bereaksi mirip rasa sakit.',
    'Masalahnya, alat ukur ini kelewat sensitif.',
    'Tahun dua ribu satu, Savitsky dan timnya menemukan: kalau kita salah di depan orang, mereka nggak menilai seburuk yang kita kira.',
    'Kita yang terlalu fokus ke kesalahan sendiri.',
    'Jadi kalau omongan orang kepikiran lagi, ingat: alat ukurmu suka lebay.',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.19, 8.11, 12.82, 16.13, 20.67, 23.05, 30.18, 32.67, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
