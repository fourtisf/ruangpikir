import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Mau presentasi, tapi deg-degan? Jangan bilang tenang. Bilang ini.',
    'Soalnya di badan, cemas sama excited itu mirip banget: jantung berdebar, napas cepat.',
    'Tahun dua ribu empat belas, psikolog Alison Wood Brooks menguji trik sederhana.',
    'Sebelum karaoke, pidato, atau tes matematika, peserta disuruh bilang satu kalimat.',
    'Ada yang bilang: aku tenang. Ada yang bilang: aku excited.',
    'Hasilnya? Yang bilang aku excited tampil lebih baik, dan lebih percaya diri.',
    'Rasa cemasnya nggak hilang. Tapi energinya dibelokkan jadi semangat.',
    'Jadi sebelum tampil, bilang: aku excited! Tulis di komentar, kamu mau tampil di mana?',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.81, 9.09, 14.0, 19.09, 22.69, 27.41, 31.32, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
