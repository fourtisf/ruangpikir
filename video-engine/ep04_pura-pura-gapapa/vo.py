import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    "Pernah bilang \"aku gapapa\", padahal lagi nggak baik-baik aja?",
    "Senyum di luar, tapi di dalam rasanya mau meledak.",
    "Ternyata, nahan emosi bikin tubuhmu makin tegang.",
    "Tahun sembilan belas sembilan puluh tujuh, James Gross dan timnya mengujinya.",
    "Peserta nonton film sedih. Separuhnya disuruh menahan ekspresi wajah.",
    "Hasilnya? Wajahnya memang datar, tapi rasa sedihnya tetap ada.",
    "Malah, jantung dan pembuluh darahnya kerja lebih keras.",
    "Setahun kemudian, Gross menemukan cara yang lebih sehat: memaknai ulang situasinya.",
    "Misalnya, \"dia bukan benci aku, dia lagi capek\". Perasaannya reda, tubuh nggak ikut tegang.",
    "Kamu nggak harus selalu kuat. Cerita ke orang yang kamu percaya, ya.",
    "Follow Ruang Pikir, biar makin kenal isi kepalamu.",
]
ANCHORS = [0.15, 3.48, 6.22, 8.91, 13.13, 16.91, 20.31, 23.32, 27.87, 32.85, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
