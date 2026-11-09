import os
import requests
import hmac
import hashlib

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

if not API_KEY or not WEBHOOK_SECRET:
    raise ValueError("Missing API_KEY or WEBHOOK_SECRET in .env")


retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])

adapter = HTTPAdapter(max_retries=retry_strategy)


session = requests.Session()
session.mount("https://", adapter)

url = "https://jsonplaceholder.typicode.com/users"

response = session.get(url, timeout=10)
response.raise_for_status()

users = response.json()

print("FIRST 5 USERS")

for user in users[:5]:
    print(
        f"{user.get('id', 'Not Available')} - "
        f"{user.get('name', 'Not Available')} - "
        f"{user.get('email', 'Not Available')}"
    )

first_user = users[0]

address = first_user.get("address", {})
geo = address.get("geo", {})
company = first_user.get("company", {})


city = address.get("city", "Not Available")
latitude = geo.get("lat", "Not Available")
zip_code = address.get("zipcode", "Not Available")
company_name = company.get("name", "Not Available")

print("\nFIRST USER DETAILS")

print(f"City: {city}")
print(f"Latitude: {latitude}")
print(f"Zip: {zip_code}")
print(f"Company: {company_name}")


def verify_signature(payload, signature, secret):
    expected_signature = hmac.new(
        secret.encode("utf-8"), payload, hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)


payload = b'{"event": "payment_success", "amount": 1000}'

valid_signature = hmac.new(
    WEBHOOK_SECRET.encode("utf-8"), payload, hashlib.sha256
).hexdigest()

tampered_payload = b'{"event": "payment_success", "amount": 5000}'

wrong_secret = "wrong_secret"

print("\nWEBHOOK SIGNATURE TESTS")

print("Valid:", verify_signature(payload, valid_signature, WEBHOOK_SECRET))
print("Tampered:", verify_signature(tampered_payload, valid_signature, WEBHOOK_SECRET))

print("Wrong secret:", verify_signature(payload, valid_signature, wrong_secret))
session.close()
