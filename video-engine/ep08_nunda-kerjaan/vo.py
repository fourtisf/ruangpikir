import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf, nama Sirois & Pychyl ditulis fonetik (Sirwa, Pitchil) supaya dibaca benar oleh TTS.
TEXTS = [
    'Kamu nunda kerjaan bukan karena malas. Kamu lagi kabur dari rasa nggak enak.',
    'Tugasnya bikin bosan, cemas, atau bingung mulai dari mana. Jadi kamu kabur ke HP.',
    'Tahun dua ribu tiga belas, psikolog Sirwa dan Pitchil menyebutnya: memperbaiki mood sesaat.',
    'Tahun dua ribu satu, peneliti bikin peserta bad mood sebelum latihan tes. Mereka malah sibuk main.',
    'Tapi saat diyakinkan mood-nya nggak bisa berubah, mereka berhenti menunda.',
    'Yang dikejar cuma lega sesaat. Tugasnya tetap ada, dan makin berat.',
    'Tahun dua ribu sepuluh, riset Michael Wohl: mahasiswa yang memaafkan diri setelah menunda, lebih jarang menunda lagi.',
    'Jadi jangan marahin diri. Maafin dulu, lalu mulai dari langkah paling kecil.',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 4.22, 8.57, 13.44, 18.7, 22.66, 26.25, 32.53, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
