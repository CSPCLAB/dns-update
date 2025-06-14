#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GODADDY_API_KEY')
api_secret = os.getenv('GODADDY_API_SECRET')
certbot_domain = os.getenv('CERTBOT_DOMAIN')
validation_value = os.getenv('CERTBOT_VALIDATION')
zone_domain = "cspc.me"

if not all([api_key, api_secret, certbot_domain, validation_value]):
    print("Missing environment variables")
    exit(1)

def get_record_name(certbot_domain, zone_domain):
    if certbot_domain == zone_domain:
        return "_acme-challenge"
    elif certbot_domain.endswith("." + zone_domain):
        sub = certbot_domain[:-(len(zone_domain) + 1)]
        return f"_acme-challenge.{sub}"
    else:
        raise ValueError("CERTBOT_DOMAIN doesn't match ZONE_DOMAIN")

record_name = get_record_name(certbot_domain, zone_domain)
url = f"https://api.godaddy.com/v1/domains/{zone_domain}/records/TXT/{record_name}"
headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "Content-Type": "application/json"
}

# 기존 값 조회
get_resp = requests.get(url, headers=headers)
if get_resp.status_code != 200:
    print("Failed to fetch existing TXT records during cleanup.")
    exit(0)  # 오류로 종료하면 인증 실패 처리됨, 여기선 무시

existing_values = [r["data"] for r in get_resp.json()]
remaining_values = [val for val in existing_values if val != validation_value]

# TXT 레코드 갱신
payload = [{"data": val, "ttl": 600} for val in remaining_values]
put_resp = requests.put(url, headers=headers, json=payload)
if put_resp.status_code != 200:
    print("Failed to cleanup TXT record")
    print(put_resp.text)
