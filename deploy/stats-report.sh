#!/usr/bin/env bash
# Rangkum log kunjungan ruangpikir.id (maks. 90 hari) jadi laporan HTML di /statistik/.
# Dijalankan otomatis tiap 10 menit oleh ruangpikir-stats.timer (dipasang deploy/setup-stats.sh).
set -euo pipefail

OUT=/var/lib/ruangpikir-stats
shopt -s nullglob
logs=(/var/log/ruangpikir/access.log*)
[ ${#logs[@]} -gt 0 ] || exit 0

zcat -f "${logs[@]}" | goaccess - --log-format=COMBINED --anonymize-ip --ignore-crawlers --no-progress \
  --html-report-title="Statistik ruangpikir.id" -o "$OUT/report.tmp.html"
mv "$OUT/report.tmp.html" "$OUT/index.html"
