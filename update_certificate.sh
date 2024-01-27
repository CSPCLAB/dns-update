#!/bin/bash

# 웹서버 OFF
apache2ctl stop

# Certbot 갱신
certbot renew --non-interactive --manual-auth-hook '/root/dns/godaddy-dns-update.py' --manual-cleanup-hook 'rm -f /tmp/CERTBOT_VALIDATION'

# 웹서버 ON
apache2ctl start
