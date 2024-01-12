import requests
import json

# Your GA4 Measurement ID
MEASUREMENT_ID = 'G-1L1YW7SZFP'  # Replace with your Measurement ID
API_SECRET = '_vs5ggfmTNCe-SSAKOsfmw'  # Optional, based on your setup
hostname = "https://www.thefairycodemother.com"

url = f'https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}'
payload = {
  "client_id": '123456.123456',
  "events": [
    {
      "name": "test_from_codelab",
      "params": {
        "test_param": "test_123"
      }
    }
  ]
}
r = requests.post(url,data=json.dumps(payload),verify=True)
print(r.status_code)
