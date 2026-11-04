import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vo')
# anchor = waktu animasi (DUR 42). Tahun ditulis dengan huruf supaya dibaca benar oleh TTS; "Susan Spreker" = ejaan fonetik Susan Sprecher.
TEXTS = [
    'Mau dia terbuka sama kamu? Coba ini: cerita duluan.',
    'Kita sering nunggu orang lain buka diri duluan. Akhirnya, dua-duanya diem.',
    'Tahun dua ribu tiga belas, psikolog Susan Spreker meneliti dua orang asing yang ngobrol lewat video call.',
    'Ada yang ceritanya gantian, bolak-balik. Ada yang satu cerita terus, yang lain cuma dengerin.',
    'Hasilnya? Yang gantian cerita, lebih saling suka.',
    'Bahkan setelah tukar peran, yang satu arah tetap nggak bisa ngejar.',
    'Soalnya cerita duluan itu kayak bilang: aku percaya sama kamu. Dan orang cenderung membalas.',
    'Mulai dari hal kecil, terus tanya balik. Cerita apa yang pernah bikin kamu langsung akrab? Tulis di komentar!',
    'Follow Ruang Pikir, biar makin kenal isi kepalamu.',
]
ANCHORS = [0.15, 3.05, 7.27, 13.25, 18.55, 21.34, 25.15, 30.39, 36.6]
LINES = list(zip(ANCHORS, TEXTS))
