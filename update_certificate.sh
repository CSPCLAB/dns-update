#!/bin/bash

# 현재 시각 출력
echo "Script started at: $(date '+%Y-%m-%d %H:%M:%S')"

# 현재 디렉토리를 workdir로 설정
workdir="$PWD"
echo "Working directory: $workdir"

# 웹서버 OFF
echo "Stopping Nginx service..."
service nginx stop

# Certbot 갱신
echo "Renewing certificates..."
certbot renew --non-interactive --quiet --manual-auth-hook "$workdir/godaddy-dns-update.py" --manual-cleanup-hook 'rm -f /tmp/CERTBOT_VALIDATION'

# 웹서버 ON
echo "Starting Nginx service..."
service nginx start

# 종료 시각 출력
echo "Script ended at: $(date '+%Y-%m-%d %H:%M:%S')"

