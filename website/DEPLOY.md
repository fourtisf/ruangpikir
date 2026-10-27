# Deploy ruangpikir.id

Yang di-deploy: **seluruh folder `website/`** (beranda, halaman episode, gambar, sitemap, 404) plus video dari `videos/` (lewat symlink `website/videos`). Font dimuat dari Google Fonts, dan logo 3D di hero memakai three.js dari `cdn.jsdelivr.net` (kalau browser tidak mendukung WebGL2 atau CDN gagal, logo SVG biasa yang tampil).

Bagian yang dibuat otomatis dari `website/episodes.json` (kartu episode, halaman episode, sitemap, gambar preview) dibangun dengan `python3 tools/build_site.py`. Jalankan setelah menambah episode, lalu commit hasilnya.

Yang dipakai sekarang: **Opsi C (VPS)**. Opsi A/B di bawah hanya cadangan; kalau dipakai, upload isi folder `website/` (ganti symlink `videos` dengan folder video aslinya). Halaman 404 khusus dan statistik hanya ada di Opsi C.

## Opsi A — Pakai hosting Hostinger (kalau punya paket hosting)

1. hPanel → **Websites** → **Add website** → pilih "Empty / custom PHP-HTML website" → pilih domain **ruangpikir.id**.
2. Buka **File Manager** website tersebut → masuk folder `public_html`.
3. Hapus `default.php` / `index.php` bawaan kalau ada, lalu **upload isi folder `website/`**.
4. hPanel → **Security → SSL** → pasang SSL gratis (Let's Encrypt) untuk `ruangpikir.id` dan `www.ruangpikir.id`.
5. Pastikan domain memakai nameserver Hostinger (hPanel → Domain → DNS/Nameserver → "Use Hostinger nameservers").
6. Tunggu propagasi DNS (biasanya 15 menit – beberapa jam), lalu buka `https://ruangpikir.id`.

## Opsi C — VPS sendiri (yang dipakai sekarang)

DNS di hPanel: A record `@` → IP VPS, CNAME `www` → `ruangpikir.id`. Lalu SSH ke VPS sebagai root:

```bash
apt-get update && apt-get install -y git
[ -d /var/www/ruangpikir ] || git clone https://github.com/fourtisf/ruangpikir.git /var/www/ruangpikir
bash /var/www/ruangpikir/deploy/setup-vps.sh
```

Script `deploy/setup-vps.sh` mengecek DNS, memasang nginx yang melayani folder `website/`, memasang HTTPS Let's Encrypt (apex + www, http dialihkan ke https, perpanjangan otomatis), lalu memasang perintah `ruangpikir-deploy`. Aman dijalankan ulang.

### Update website: `ruangpikir-deploy`

Setelah ada perubahan di GitHub, cukup satu perintah di VPS:
```bash
ruangpikir-deploy                 # versi terbaru dari GitHub
ruangpikir-deploy a2b52f4         # kembali ke versi lama (rollback); kode versinya ditampilkan tiap deploy
ruangpikir-deploy nama-branch     # coba versi dari branch lain
ruangpikir-deploy --help
```
Atau langsung dari komputer sendiri (PowerShell / Terminal), tanpa masuk SSH dulu:
```bash
ssh root@31.97.111.49 ruangpikir-deploy
```
Perintah ini menolak jalan kalau ada file yang diedit langsung di VPS (supaya tidak hilang tanpa sengaja); pakai `--force` untuk menimpanya. Pengunjung langsung dapat versi baru tanpa perlu Ctrl+Shift+R (HTML diset `Cache-Control: no-cache`).

VPS yang dipasang sebelum perintah ini ada: jalankan sekali `git -C /var/www/ruangpikir pull && bash /var/www/ruangpikir/deploy/deploy.sh`.

Pengaturan nginx situs ada di `deploy/nginx-site.conf` (ikut repo). Kalau file itu berubah, `ruangpikir-deploy` mengecek dengan `nginx -t` lalu reload; kalau ditolak, deploy dibatalkan dan situs tetap di versi lama.

### API key Gemini di VPS (hanya untuk membuat suara video, website tidak butuh)

Jalankan **satu baris** ini, lalu tempel key saat diminta (tidak terlihat dan tidak masuk riwayat terminal):
```bash
read -rsp "Tempel GEMINI_API_KEY lalu Enter: " k && echo && printf 'GEMINI_API_KEY=%s\nGEMINI_TTS_MODEL=gemini-3.8-flash-tts\n' "$k" > /var/www/ruangpikir/.env && chmod 600 /var/www/ruangpikir/.env && unset k && echo "Tersimpan di /var/www/ruangpikir/.env"
```
File `.env` tidak ikut git, tidak bisa dibuka lewat website (nginx hanya melayani folder `website/`), dan tetap ada setiap `ruangpikir-deploy`.

### Statistik pengunjung: https://ruangpikir.id/statistik/

Tanpa cookie dan tanpa layanan pihak ketiga: nginx mencatat kunjungan ke `/var/log/ruangpikir/access.log` (disimpan 90 hari, IP disamarkan di laporan), lalu GoAccess merangkumnya tiap 10 menit. Username `admin`; password ditampilkan sekali saat `setup-vps.sh` pertama memasang statistik. Lupa password: `bash /var/www/ruangpikir/deploy/setup-stats.sh --reset-password`.

Yang terlihat di laporan: jumlah pengunjung & halaman, asal kunjungan (Instagram, TikTok, Google, …), perangkat, dan kejadian dari website di bagian *Requested Files* sebagai `/e/<nama>`:
`tes-mulai`, `tes-selesai`, `bagikan-hasil`, `putar-<episode>`, `klik-instagram`, `klik-tiktok`, `klik-dm-instagram`.

Tips: aplikasi Instagram/TikTok sering tidak mengirim asal kunjungan. Supaya jelas, pakai link bio `ruangpikir.id/?dari=ig` dan `ruangpikir.id/?dari=tiktok`; angkanya muncul terpisah di laporan.

## Opsi B — Hanya punya domain (tanpa paket hosting): hosting gratis

### Cloudflare Pages
1. Buat project Pages → **Upload assets** → upload folder berisi `index.html`.
2. Project → **Custom domains** → tambahkan `ruangpikir.id` dan `www.ruangpikir.id`.
3. Ikuti instruksi DNS dari Cloudflare: paling mudah pindahkan nameserver domain di hPanel (Domain → DNS/Nameserver → Change nameservers) ke dua nameserver Cloudflare yang diberikan.

### Netlify (alternatif)
1. Buka app.netlify.com/drop → seret folder berisi `index.html`.
2. Site settings → **Domain management** → Add custom domain `ruangpikir.id`.
3. Di hPanel → DNS records: tambahkan record sesuai instruksi Netlify (A record apex ke load balancer Netlify, CNAME `www` ke `<nama-site>.netlify.app`), atau pakai Netlify DNS.

### Lewat CLI (untuk Claude Code)
```bash
# Netlify
npx netlify-cli deploy --dir=website --prod
# atau Vercel
npx vercel deploy website --prod
```
Lalu sambungkan domain di dashboard provider dan atur DNS di Hostinger seperti di atas.

## Setelah live — checklist
- [ ] `https://ruangpikir.id` terbuka, ada gembok HTTPS
- [ ] `https://www.ruangpikir.id` juga terbuka (redirect ke apex boleh)
- [ ] Di HP: hero, game "Mulai tes" → 16 soal → hasil skor & waktu reaksi muncul
- [ ] Tombol "Follow" membuka instagram.com/ruangpikir2026
- [ ] Taruh `ruangpikir.id` di link bio Instagram

## Mengubah isi
- Link sosial media: cari `const SOCIAL = {` di bagian bawah `index.html`.
- Episode baru: tambahkan kartu `<a class="ep">…</a>` di section `#episode` (gambar bisa base64 atau file terpisah).
