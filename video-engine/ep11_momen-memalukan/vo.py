import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf, nama ditulis fonetik (Mekgo = McGaugh, Dorte Bernsen = Dorthe Berntsen, Liri = Leary) supaya dibaca benar oleh TTS.
TEXTS = [
    'Kamu pasti masih ingat momen paling memalukanmu. Otakmu memang sengaja menyimpannya.',
    'Apalagi pas mau tidur, tiba-tiba muncul lagi, bikin pengen teriak ke bantal.',
    'Tahun dua ribu empat, James Mekgo menjelaskan: saat emosi memuncak, amigdala bikin ingatan tersimpan lebih kuat.',
    'Kenapa munculnya pas mau tidur? Ingatan tak diundang paling sering datang saat pikiran lagi santai, kata Dorte Bernsen.',
    'Padahal orang lain jauh lebih jarang memperhatikan kita dari yang kita kira.',
    'Jadi kalau muncul lagi, bilang ke diri sendiri: semua orang pernah malu, dan itu manusiawi.',
    'Riset Mark Liri: baik ke diri sendiri bikin kita menerima kesalahan, tanpa tenggelam dalam malu.',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.8, 9.0, 15.31, 22.0, 26.2, 31.23, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
