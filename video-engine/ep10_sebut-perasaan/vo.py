import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (EP10 format 30 detik: anchor dirapatkan ke durasi suara, outro di 23.67, DUR 29.07). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Emosi meledak? Cara meredamnya cuma butuh satu kalimat.',
    'Tahun dua ribu tujuh, Matthew Lieberman memindai otak orang yang melihat wajah marah.',
    'Saat mereka memberi nama emosinya, alarm emosi di otak ikut turun.',
    'Jadi kalau lagi kesal, bilang aja: aku lagi kesal.',
    'Diberi nama, bukan dipendam.',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.82, 10.42, 15.99, 20.65, 23.67]
LINES = list(zip(ANCHORS, TEXTS))
