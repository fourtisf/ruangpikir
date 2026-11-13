import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi. Angka & tahun ditulis dengan huruf supaya dibaca benar oleh TTS.
TEXTS = [
    'Penyesalan yang paling lama nempel, ternyata bukan soal kesalahan.',
    'Coba jawab ini: ada mimpi yang udah lama pengen kamu lakuin? Kenapa belum?',
    'Ini pertanyaan nomor empat belas, dari tiga puluh enam pertanyaan psikolog Arthur Aron.',
    'Mungkin jawabanmu: nanti aja, belum waktunya, atau takut gagal.',
    'Tapi tahun dua ribu delapan belas, Thomas Gilovich dan timnya nanya ratusan orang soal penyesalan mereka.',
    'Hasilnya? Tujuh puluh dua persen penyesalan itu soal diri impian yang nggak dikejar. Soal kewajiban yang gagal, cuma dua puluh delapan persen.',
    'Soalnya kewajiban yang gagal biasanya cepat kita beresin. Tapi mimpi? Sering cuma kita tunda.',
    'Kamu sendiri, mimpi apa yang belum kamu kejar? Tulis di komentar, terus kirim ke temanmu yang lagi nunda mimpinya!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.74, 7.27, 11.19, 15.35, 20.23, 26.79, 31.52, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
