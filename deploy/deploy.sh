#!/usr/bin/env bash
# Update ruangpikir.id dari GitHub. Setelah dijalankan sekali, tersedia sebagai perintah `ruangpikir-deploy`:
#   ruangpikir-deploy                versi terbaru branch utama di GitHub
#   ruangpikir-deploy <branch>       versi terbaru branch tertentu
#   ruangpikir-deploy <commit>       kembali ke versi lama (rollback), mis. ruangpikir-deploy a2b52f4
#   ruangpikir-deploy --force ...    timpa file yang diedit langsung di VPS
# Dari komputer sendiri: ssh root@IP-VPS ruangpikir-deploy
set -euo pipefail

DOMAIN=ruangpikir.id
CMD=/usr/local/bin/ruangpikir-deploy
CACHE_CONF=/etc/nginx/conf.d/ruangpikir-cache.conf
SELF=$(readlink -f "${BASH_SOURCE[0]}")
REPO=$(cd "$(dirname "$SELF")/.." && pwd)

# HTML ruangpikir.id selalu dicek ulang oleh browser, jadi pengunjung langsung dapat versi baru tanpa Ctrl+Shift+R
cache_conf() {
  cat <<'NGINX'
# Dipasang oleh ruangpikir-deploy.
map "$host:$sent_http_content_type" $ruangpikir_cache {
    ~^(www\.)?ruangpikir\.id:text/html  "no-cache";
    default                             "";
}
add_header Cache-Control $ruangpikir_cache;
NGINX
}

ensure_setup() {
  if [ "$(readlink -f "$CMD" 2>/dev/null)" != "$SELF" ]; then
    ln -sf "$SELF" "$CMD"; echo "Perintah 'ruangpikir-deploy' terpasang."
  fi
  if [ -d /etc/nginx/conf.d ] && ! cache_conf | cmp -s - "$CACHE_CONF"; then
    cache_conf > "$CACHE_CONF"
    if nginx -t 2>/dev/null; then systemctl reload nginx
    else rm -f "$CACHE_CONF"; echo "Peringatan: pengaturan cache nginx ditolak, dilewati."; fi
  fi
}

main() {
  local force=0 ref="" before after
  for a in "$@"; do
    case "$a" in
      --force) force=1 ;;
      -h|--help) sed -n '2,7p' "$SELF" | sed 's/^# \{0,1\}//'; return 0 ;;
      *) ref=$a ;;
    esac
  done
  [ "$(id -u)" = 0 ] || { echo "Jalankan sebagai root."; return 1; }
  cd "$REPO"
  ensure_setup

  if [ "$force" = 0 ] && [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "Ada file yang diubah langsung di VPS (akan hilang kalau di-deploy):"
    git status --short --untracked-files=no
    echo "Kalau memang mau ditimpa: ruangpikir-deploy --force"; return 1
  fi

  before=$(git rev-parse --short HEAD)
  git fetch --prune --quiet origin
  git remote set-head origin --auto >/dev/null
  [ -n "$ref" ] || ref=$(git symbolic-ref --short refs/remotes/origin/HEAD | sed 's#^origin/##')

  if git show-ref --verify --quiet "refs/remotes/origin/$ref"; then
    git checkout --quiet --force -B "$ref" --track "origin/$ref"
  elif git rev-parse --verify --quiet "$ref^{commit}" >/dev/null; then
    git checkout --quiet --force --detach "$ref"
  else
    echo "Branch atau commit '$ref' tidak ditemukan di GitHub."; return 1
  fi

  after=$(git rev-parse --short HEAD)
  if [ ! -f website/index.html ]; then
    echo "Versi $after tidak punya website/index.html. Dibatalkan, kembali ke $before."
    git checkout --quiet --force --detach "$before"; return 1
  fi

  if [ "$before" = "$after" ]; then
    echo "Sudah versi terbaru: $after $(git log -1 --format=%s)"
  else
    echo "Live sekarang: $after $(git log -1 --format=%s)"
    if git merge-base --is-ancestor "$before" "$after"; then
      echo "Perubahan baru:"; git log --format='  - %s' "$before..$after"
    fi
    echo "Kalau ada masalah, kembali ke versi sebelumnya: ruangpikir-deploy $before"
  fi

  for u in "https://$DOMAIN" "https://www.$DOMAIN"; do
    echo "$u -> $(curl -s -o /dev/null -m 15 -w '%{http_code}' "$u" || true)   (200 = OK)"
  done
}

# fungsi dibaca utuh dulu, jadi aman walaupun file ini ikut berubah saat git checkout
main "$@"; exit $?
