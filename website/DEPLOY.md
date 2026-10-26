# Deploy ruangpikir.id

File yang di-deploy: **`index.html`** saja (semua gambar, logo, CSS, dan JavaScript sudah ada di dalamnya). Font dimuat dari Google Fonts, dan logo 3D di hero memakai three.js dari `cdn.jsdelivr.net` (kalau browser tidak mendukung WebGL2 atau CDN gagal, logo SVG biasa yang tampil).

## Opsi A — Pakai hosting Hostinger (kalau punya paket hosting)

1. hPanel → **Websites** → **Add website** → pilih "Empty / custom PHP-HTML website" → pilih domain **ruangpikir.id**.
2. Buka **File Manager** website tersebut → masuk folder `public_html`.
3. Hapus `default.php` / `index.php` bawaan kalau ada, lalu **upload `index.html`**.
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
