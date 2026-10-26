#!/usr/bin/env bash
# Pasang ruangpikir.id di VPS Ubuntu: nginx + HTTPS gratis (Let's Encrypt).
# Jalankan sebagai root dari repo yang sudah di-clone, misalnya:
#   bash /var/www/ruangpikir/deploy/setup-vps.sh
# Aman dijalankan ulang.
set -euo pipefail

DOMAIN=ruangpikir.id
WEBROOT=$(cd "$(dirname "$0")/../website" && pwd)
CONF=/etc/nginx/sites-available/ruangpikir

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

# 4. Situs nginx (HTTP dulu; certbot menambahkan HTTPS + redirect di langkah 6)
cat > "$CONF" <<NGINX
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN www.$DOMAIN;
    root $WEBROOT;
    index index.html;
    location / { try_files \$uri \$uri/ =404; }
}
NGINX
ln -sf "$CONF" /etc/nginx/sites-enabled/ruangpikir
nginx -t
systemctl enable --now nginx
systemctl reload nginx

# 5. Firewall (hanya kalau ufw aktif)
if command -v ufw >/dev/null && ufw status | grep -q 'Status: active'; then
  ufw allow 'Nginx Full'
fi

# 6. Sertifikat HTTPS untuk apex + www, redirect http -> https. Perpanjangan otomatis via certbot.timer.
certbot --nginx -n --agree-tos --register-unsafely-without-email --redirect \
  -d "$DOMAIN" -d "www.$DOMAIN"

# 7. Cek hasil: https harus 200, http harus 301 (dialihkan ke https). 000 = tidak bisa tersambung.
for u in "https://$DOMAIN" "https://www.$DOMAIN" "http://$DOMAIN"; do
  echo "$u -> $(curl -s -o /dev/null -m 15 -w '%{http_code}' "$u" || true)"
done
echo "Selesai. Buka https://$DOMAIN"
