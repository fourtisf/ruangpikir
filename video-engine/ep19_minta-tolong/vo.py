import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS; "Jeker dan Lendi" / "Yu Niya" = ejaan fonetik Jecker & Landy / Yu Niiya.
TEXTS = [
    'Mau disukai sama orang? Coba minta tolong hal kecil ke dia.',
    'Kedengarannya kebalik, ya? Soalnya kita sering sungkan, takut ngerepotin.',
    'Tahun sembilan belas enam puluh sembilan, psikolog Jeker dan Lendi menguji ini.',
    'Peserta yang baru menang uang, diminta mengembalikannya, sebagai bantuan pribadi buat si peneliti.',
    'Hasilnya? Yang dimintai tolong, malah lebih suka sama penelitinya.',
    'Tahun dua ribu enam belas, Yu Niya di Jepang juga menemukan: minta tolong secara langsung bikin orang lebih suka.',
    'Soalnya dimintai tolong itu rasanya dipercaya, kayak diajak akrab.',
    'Asal kecil ya, kayak pinjem pulpen atau minta rekomendasi lagu. Kamu biasanya minta tolong apa? Tulis di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.37, 7.35, 11.66, 17.01, 20.61, 26.78, 30.38, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
