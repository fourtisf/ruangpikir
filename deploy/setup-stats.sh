#!/usr/bin/env bash
# Pasang statistik pengunjung ruangpikir.id: GoAccess + laporan tiap 10 menit di https://ruangpikir.id/statistik/
# Dipanggil oleh setup-vps.sh. Aman dijalankan ulang.
#   bash setup-stats.sh                   pasang (password dibuat sekali, ditampilkan di layar)
#   bash setup-stats.sh --reset-password  buat password baru
set -euo pipefail

REPO=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
HTPASSWD=/etc/nginx/ruangpikir-stats.htpasswd
[ "$(id -u)" = 0 ] || { echo "Jalankan sebagai root."; exit 1; }

command -v goaccess >/dev/null || { DEBIAN_FRONTEND=noninteractive apt-get install -y -q goaccess >/dev/null; }
mkdir -p /var/log/ruangpikir /var/lib/ruangpikir-stats

# simpan log 90 hari (di folder sendiri supaya tidak bentrok dengan /etc/logrotate.d/nginx)
cat > /etc/logrotate.d/ruangpikir <<'EOF'
/var/log/ruangpikir/*.log {
    daily
    rotate 90
    missingok
    notifempty
    compress
    delaycompress
    sharedscripts
    postrotate
        [ -s /run/nginx.pid ] && kill -USR1 "$(cat /run/nginx.pid)" || true
    endscript
}
EOF

cat > /etc/systemd/system/ruangpikir-stats.service <<EOF
[Unit]
Description=Laporan statistik ruangpikir.id

[Service]
Type=oneshot
ExecStart=/usr/bin/env bash $REPO/deploy/stats-report.sh
EOF
cat > /etc/systemd/system/ruangpikir-stats.timer <<'EOF'
[Unit]
Description=Perbarui statistik ruangpikir.id tiap 10 menit

[Timer]
OnBootSec=2min
OnUnitActiveSec=10min

[Install]
WantedBy=timers.target
EOF
systemctl daemon-reload
systemctl enable --now ruangpikir-stats.timer >/dev/null

if [ ! -s "$HTPASSWD" ] || [ "${1:-}" = "--reset-password" ]; then
  pw=$(openssl rand -base64 18 | tr -dc 'A-Za-z0-9' | cut -c1-14)
  printf 'admin:%s\n' "$(openssl passwd -apr1 "$pw")" > "$HTPASSWD"
  chown root:www-data "$HTPASSWD"; chmod 640 "$HTPASSWD"
  echo "Login statistik https://ruangpikir.id/statistik/  ->  username: admin   password: $pw"
  echo "(Simpan password ini sekarang; tidak ditampilkan lagi. Ganti: bash $REPO/deploy/setup-stats.sh --reset-password)"
fi
bash "$REPO/deploy/stats-report.sh" || true
