import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS. "Roy Lewiki" = ejaan fonetik Roy Lewicki.
TEXTS = [
    'Udah minta maaf, kok nggak dimaafin? Jangan cuma bilang, maafin aku ya. Coba dua kalimat ini.',
    'Kita sering minta maaf buru-buru, biar cepat selesai. Tapi dia masih diam, dan suasananya tetap dingin.',
    'Tahun dua ribu enam belas, Roy Lewiki dan timnya menguji enam unsur permintaan maaf ke lebih dari tujuh ratus orang.',
    'Hasilnya? Unsur paling ampuh: mengakui kesalahan. Bilang: itu salahku.',
    'Nomor dua: tawarkan perbaikan. Bilang: aku perbaiki, ya.',
    'Yang paling lemah justru minta dimaafkan, alias, maafin aku ya.',
    'Makin lengkap permintaan maafnya, makin dihargai. Tapi kalau cuma sempat dua kalimat, pakai yang ini.',
    'Itu salahku. Aku perbaiki, ya. Kirim video ini ke orang yang mau kamu mintain maaf!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.94, 10.07, 16.26, 21.08, 24.37, 27.99, 32.58, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
