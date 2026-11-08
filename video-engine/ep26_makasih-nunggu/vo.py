import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS. "Yanfen Yo" = ejaan fonetik Yanfen You.
TEXTS = [
    'Telat datang? Jangan bilang maaf ya. Coba ganti pakai kalimat ini.',
    'Biasanya kita langsung bilang: maaf ya, maaf banget, tadi macet.',
    'Tahun dua ribu dua puluh, peneliti Yanfen Yo dan timnya menguji ini di berbagai layanan yang bikin kecewa.',
    'Ada yang dibilang: maaf ya. Ada yang dibilang: makasih ya, udah sabar.',
    'Hasilnya? Yang dibilang makasih justru lebih puas.',
    'Soalnya kata maaf bikin fokusnya ke kesalahan kita. Kata makasih bikin fokusnya ke kebaikan dia, jadi dia merasa dihargai.',
    'Jadi lain kali telat, bilang: makasih udah nunggu, ya. Tapi kalau salahnya besar, tetap minta maaf dan perbaiki.',
    'Kirim video ini ke teman yang paling sering kamu bikin nunggu!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.0, 8.27, 13.51, 17.85, 21.15, 27.87, 33.83, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
