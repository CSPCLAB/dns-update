#!/usr/local/bin/python3.8
import requests
import os
import dns.resolver
import time
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

# GoDaddy API 인증 정보
api_key = os.environ['GODADDY_API_KEY']
api_secret = os.environ['GODADDY_API_SECRET']

print(api_key)
# 인증서를 갱신하려는 도메인 설정
domain = os.environ['DOMAIN']
record_name = '_acme-challenge'
record_type = 'TXT'
record_data = os.environ['CERTBOT_VALIDATION']  # Certbot에서 제공하는 검증 문자열
record_ttl = 600  # TTL 값 설정



def wait_for_dns_propagation(record_name, expected_data, timeout=1800, interval=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            answers = dns.resolver.resolve(record_name, 'TXT')
            for rdata in answers:
                if expected_data in rdata.to_text():
                    return True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass
        time.sleep(interval)
    return False



# GoDaddy API 엔드포인트
url = f'https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/{record_name}'

# API 헤더 설정
headers = {
    'Authorization': f'sso-key {api_key}:{api_secret}',
    'Content-Type': 'application/json'
}

# TXT 레코드 업데이트를 위한 데이터
data = [{
    'data': record_data,
    'ttl': record_ttl
}]

# API 요청을 통해 DNS 레코드 업데이트
response = requests.put(url, headers=headers, json=data)

print(response.text)
if response.status_code == 200:
    if wait_for_dns_propagation(f'{record_name}.{domain}', record_data):
        print("DNS record propagated.")
    else:
        print("Timeout: DNS record not propagated within the expected time.")
else:
    print("Failed to update DNS record")

