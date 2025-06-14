#!/bin/bash

# 현재 시각 출력
echo "Script started at: $(date '+%Y-%m-%d %H:%M:%S')"

# 현재 디렉토리를 workdir로 설정 (절대 경로)
workdir="$(pwd)"
echo "Working directory: $workdir"

# Certbot 갱신
echo "Renewing certificates..."
certbot certonly \
  --manual \
  --preferred-challenges dns \
  --manual-auth-hook "$workdir/godaddy-dns-update.py" \
  --manual-cleanup-hook "$workdir/godaddy-dns-cleanup.py" \
  --non-interactive \
  --force-renewal \
  -d '*.cspc.me' -d cspc.me

# 종료 시각 출력
echo "Script ended at: $(date '+%Y-%m-%d %H:%M:%S')"
