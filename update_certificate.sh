#!/bin/bash

# 현재 시각 출력
echo "Script started at: $(date '+%Y-%m-%d %H:%M:%S')"

# 인자 체크
if [ -z "$1" ]; then
  echo "Usage: $0 <workdir>"
  exit 1
fi

# Set workdir
workdir="$1"
cd "$workdir" || { echo "Failed to change directory to $workdir"; exit 1; }

# 웹서버 OFF
echo "Stopping Apache2 service..."
service apache2 stop

# Certbot 갱신
echo "Renewing certificates..."
certbot renew --non-interactive --quiet --manual-auth-hook "$workdir/godaddy-dns-update.py" --manual-cleanup-hook 'rm -f /tmp/CERTBOT_VALIDATION'

# 웹서버 ON
echo "Starting Apache2 service..."
service apache2 start

# 종료 시각 출력
echo "Script ended at: $(date '+%Y-%m-%d %H:%M:%S')"

