#!/usr/bin/env python3
import os
import requests
import time
import dns.resolver
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GODADDY_API_KEY')
api_secret = os.getenv('GODADDY_API_SECRET')
certbot_domain = os.getenv('CERTBOT_DOMAIN')
validation_value = os.getenv('CERTBOT_VALIDATION')
zone_domain = "cspc.me"

if not all([api_key, api_secret, certbot_domain, validation_value]):
    print("Missing required environment variables.")
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
fqdn = f"{record_name}.{zone_domain}"
record_type = "TXT"
record_ttl = 600

url = f"https://api.godaddy.com/v1/domains/{zone_domain}/records/{record_type}/{record_name}"
headers = {
    "Authorization": f"sso-key {api_key}:{api_secret}",
    "Content-Type": "application/json"
}

# 1. 기존 값 조회
existing_resp = requests.get(url, headers=headers)
existing_values = []
if existing_resp.status_code == 200:
    existing_values = [r["data"] for r in existing_resp.json()]
else:
    print("Warning: failed to read existing TXT values")

# 2. 현재 값 추가
if validation_value not in existing_values:
    existing_values.append(validation_value)

# 3. 등록
payload = [{"data": val, "ttl": record_ttl} for val in existing_values]
put_resp = requests.put(url, headers=headers, json=payload)
if put_resp.status_code != 200:
    print("Failed to update TXT record")
    print(put_resp.text)
    exit(1)

print(f"TXT record set for {fqdn} → {validation_value}")
print("Waiting for DNS to propagate...")

# 4. 전파 확인
resolver = dns.resolver.Resolver()
resolver.cache = None
resolver.nameservers = ['8.8.8.8', '1.1.1.1']

MAX_WAIT = 180
INTERVAL = 10
elapsed = 0
while elapsed < MAX_WAIT:
    try:
        answers = resolver.resolve(fqdn, 'TXT')
        for rdata in answers:
            txt = rdata.to_text().strip('"')
            if txt == validation_value:
                print(f"TXT record verified in DNS after {elapsed} seconds.")
                exit(0)
    except Exception:
        pass
    time.sleep(INTERVAL)
    elapsed += INTERVAL
    print(f"Still waiting... {elapsed}s")

print("Timeout: DNS record not visible after propagation wait.")
exit(1)
