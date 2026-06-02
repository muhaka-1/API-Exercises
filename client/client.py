import requests
import os

base_url = os.getenv("API_BASE_URL", "http://api:5000")
response = requests.get(f"{base_url}/products", timeout=10)
response.raise_for_status()
print(response.json())
