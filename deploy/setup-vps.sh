#!/usr/bin/env bash
# Pasang ruangpikir.id di VPS Ubuntu: nginx + HTTPS gratis (Let's Encrypt).
# Jalankan sebagai root dari repo yang sudah di-clone, misalnya:
#   bash /var/www/ruangpikir/deploy/setup-vps.sh
# Aman dijalankan ulang.
set -euo pipefail

DOMAIN=ruangpikir.id
WEBROOT=$(cd "$(dirname "$0")/../website" && pwd)
REPO=$(dirname "$WEBROOT")
CONF=/etc/nginx/sites-available/ruangpikir
LE=/etc/letsencrypt

[ "$(id -u)" = 0 ] || { echo "Jalankan sebagai root."; exit 1; }
[ -f "$WEBROOT/index.html" ] || { echo "Tidak ada $WEBROOT/index.html"; exit 1; }

# 1. Port 80/443 harus kosong (atau sudah dipakai nginx)
busy=$(ss -Htlnp 'sport = :80 or sport = :443' | grep -v nginx || true)
if [ -n "$busy" ]; then
  echo "Port 80/443 sedang dipakai program lain:"; echo "$busy"
  echo "Hentikan program itu dulu, lalu jalankan ulang script ini."; exit 1
fi

# 2. DNS harus sudah mengarah ke VPS ini, kalau belum Let's Encrypt pasti gagal
my_ips=$(hostname -I | tr ' ' '\n')
for d in "$DOMAIN" "www.$DOMAIN"; do
  ip4=$(getent ahostsv4 "$d" | awk 'NR==1 {print $1}' || true)
  if [ -z "$ip4" ] || ! grep -qxF "$ip4" <<<"$my_ips"; then
    echo "DNS $d -> ${ip4:-(belum ada)}, bukan IP VPS ini ($(hostname -I))."
    echo "Cek A record di hPanel, tunggu ±5-30 menit, lalu jalankan ulang."; exit 1
  fi
done
echo "DNS OK."

# 3. Paket
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q nginx certbot python3-certbot-nginx

# 4. Situs nginx. Lokasi, log, halaman 404, dan statistik ada di deploy/nginx-site.conf (ikut repo).
mkdir -p /var/log/ruangpikir
SITE_BODY="    root $WEBROOT;
    index index.html;
    include $REPO/deploy/nginx-site.conf;"
if [ -f "$LE/live/$DOMAIN/fullchain.pem" ] && [ -f "$LE/options-ssl-nginx.conf" ] && [ -f "$LE/ssl-dhparams.pem" ]; then
  # sertifikat sudah ada (setup ulang): tulis konfigurasi HTTPS lengkap, tidak perlu certbot lagi
  cat > "$CONF" <<NGINX
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN www.$DOMAIN;
    location ^~ /.well-known/acme-challenge/ { root $WEBROOT; }   # perpanjangan sertifikat
    location / { return 301 https://\$host\$request_uri; }
}
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name $DOMAIN www.$DOMAIN;
    ssl_certificate $LE/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key $LE/live/$DOMAIN/privkey.pem;
    include $LE/options-ssl-nginx.conf;
    ssl_dhparam $LE/ssl-dhparams.pem;
$SITE_BODY
}
NGINX
  NEED_CERT=0
else
  # pemasangan pertama: HTTP dulu, certbot menambahkan HTTPS + redirect di langkah 6
  cat > "$CONF" <<NGINX
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN www.$DOMAIN;
$SITE_BODY
}
NGINX
  NEED_CERT=1
fi
ln -sf "$CONF" /etc/nginx/sites-enabled/ruangpikir
nginx -t
systemctl enable --now nginx
systemctl reload nginx

# 5. Firewall (hanya kalau ufw aktif)
if command -v ufw >/dev/null && ufw status | grep -q 'Status: active'; then
  ufw allow 'Nginx Full'
fi

# 6. Sertifikat HTTPS untuk apex + www, redirect http -> https. Perpanjangan otomatis via certbot.timer.
if [ "$NEED_CERT" = 1 ]; then
  certbot --nginx -n --agree-tos --register-unsafely-without-email --redirect \
    -d "$DOMAIN" -d "www.$DOMAIN"
fi

# 7. Statistik pengunjung (password ditampilkan sekali saat pertama dipasang)
bash "$REPO/deploy/setup-stats.sh"

# 8. Pasang perintah `ruangpikir-deploy` + pengaturan cache, lalu cek situs
bash "$(dirname "$0")/deploy.sh"
echo "Selesai. Buka https://$DOMAIN — untuk update berikutnya cukup: ruangpikir-deploy"
