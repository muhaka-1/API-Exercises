 
import os
import json
import time
import requests
 
BASE_URL = os.getenv("API_URL", "http://localhost:5001")
 
 
def separator(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)
 
# ---------------------------------------------------------------------------
# Wait for API to be ready (useful in docker compose startup race)
# ---------------------------------------------------------------------------
def wait_for_api(max_retries: int = 10, delay: float = 1.5) -> None:
    print("Waiting for API to be ready...")
    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(f"{BASE_URL}/health", timeout=3)
            if r.status_code == 200:
                print(f"  API ready after {attempt} attempt(s).")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(delay)
    print("  WARNING: Could not reach API – continuing anyway.")
 
 
# ---------------------------------------------------------------------------
# Consume an API Task 3 – print raw JSON response
# ---------------------------------------------------------------------------
def print_raw_json() -> None:
    separator("Raw JSON response from /products")
    response = requests.get(f"{BASE_URL}/products")
    print(response.text)
 
 
# ---------------------------------------------------------------------------
# Consume an API Task 4 – print status code
# ---------------------------------------------------------------------------
def print_status_code() -> None:
    separator("HTTP Status Code")
    response = requests.get(f"{BASE_URL}/products")
    print(f"  Status code: {response.status_code}")
    if response.status_code == 200:
        print("  Meaning: OK – request succeeded, data returned.")
 
 
# ---------------------------------------------------------------------------
# Consume an API Task 5 – extract id, name, price
# ---------------------------------------------------------------------------
def extract_fields() -> None:
    separator("Extracted fields: id, name, price")
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    for p in products:
        print(f"  id={p['id']}  name={p['name']}  price={p['price']} kr")
 
 
# ---------------------------------------------------------------------------
# Consume an API Task 6 – category field now in response
# ---------------------------------------------------------------------------
def category() -> None:
    separator("Extracted fields: id, name, price, category")
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    for p in products:
        print(f"  [{p['category']}] {p['name']} – {p['price']} kr")
 
 
# ---------------------------------------------------------------------------
# Consume an API Task 7 & Extra 8 – observe more products
# ---------------------------------------------------------------------------
def add_more_products() -> None:
    separator("All products (more data)")
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    print(f"  Total products returned: {len(products)}")
    for p in products:
        print(f"  {p['id']}. {p['name']}")
 
 
# ---------------------------------------------------------------------------
# Consume an API Task 9 – print stock
# ---------------------------------------------------------------------------
def get_stock() -> None:
    separator("Stock levels")
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    for p in products:
        print(f"  {p['name']}: {p.get('stock', 'N/A')} in stock")
 
 
# ---------------------------------------------------------------------------
# Consume an API Task 10 – /health endpoint
# ---------------------------------------------------------------------------
def get_health() -> None:
    separator("/health endpoint")
    response = requests.get(f"{BASE_URL}/health")
    print(f"  Status code : {response.status_code}")
    print(f"  Response    : {response.json()}")
 
 
# ---------------------------------------------------------------------------
#  Build a robust API 
# ---------------------------------------------------------------------------


#  Task 1 – Implement GET /products/{id} + 404

def get_product_by_id() -> None:
    separator("GET /products/1 (single product)")
    r = requests.get(f"{BASE_URL}/products/1")
    print(f"  Status: {r.status_code}")
    print(f"  Body  : {r.json()}")
 
#  Task 2 - Implement 404 Not Found

    separator("GET /products/999 (404 Not Found)")
    r = requests.get(f"{BASE_URL}/products/999")
    print(f"  Status: {r.status_code}")
    print(f"  Body  : {r.json()}")
 

#  Task 3, 4, 9 – POST/createproducts, 400 Bad Request, return 201 Created, 

def post_products() -> None:
    separator("POST /products (201 Created)")
    payload = {"name": "Noise-Cancelling Headphones", "price": 2499.00,
                "category": "Audio", "stock": 20}
    r = requests.post(f"{BASE_URL}/products", json=payload)
    print(f"  Status: {r.status_code}  (expected 201)")
    print(f"  Body  : {r.json()}")
 
    separator("POST with invalid data (400 Bad Request)")
 
    # Missing name
    r = requests.post(f"{BASE_URL}/products", json={"price": 99})
    print(f"  Missing 'name'  → {r.status_code}: {r.json()}")
 
    # Missing price
    r = requests.post(f"{BASE_URL}/products", json={"name": "Widget"})
    print(f"  Missing 'price' → {r.status_code}: {r.json()}")
 
    # Negative price
    r = requests.post(f"{BASE_URL}/products", json={"name": "Widget", "price": -50})
    print(f"  Negative price  → {r.status_code}: {r.json()}")
 
 
# ---------------------------------------------------------------------------
# Task 5 – GET /crash (500)
# ---------------------------------------------------------------------------
def get_crash() -> None:
    separator("GET /crash (500 Internal Server Error)")
    r = requests.get(f"{BASE_URL}/crash")
    print(f"  Status: {r.status_code}")
    print(f"  Body  : {r.json()}")
 
 
# ---------------------------------------------------------------------------
# Task 6 – verify POST product shows in GET /products
# ---------------------------------------------------------------------------
def verify_post_appears_in_list() -> None:
    separator("POST a product then verify in GET /products")
    # Create
    payload = {"name": "Smart Speaker", "price": 899.00, "category": "Audio", "stock": 30}
    r_post = requests.post(f"{BASE_URL}/products", json=payload)
    created = r_post.json()
    print(f"  Created: {created['name']} (id={created['id']})")
 
    # List
    r_list = requests.get(f"{BASE_URL}/products")
    names = [p["name"] for p in r_list.json()]
    found = created["name"] in names
    print(f"  Visible in GET /products: {found}")
 
 
# ---------------------------------------------------------------------------
#Task Extra 7 – PUT /products/{id}
# ---------------------------------------------------------------------------
def put_products() -> None:
    separator(" PUT /products/1 (update price)")
    r = requests.put(f"{BASE_URL}/products/1", json={"price": 11499.00})
    print(f"  Status: {r.status_code}")
    print(f"  Body  : {r.json()}")
 
 
# ---------------------------------------------------------------------------
# Task Extra 8 & 10 – DELETE /products/{id} → 204 No Content
# ---------------------------------------------------------------------------
def delete_products() -> None:
    separator("Task Extra 8 & 10 – DELETE /products/2 (204 No Content)")
    r = requests.delete(f"{BASE_URL}/products/2")
    print(f"  Status: {r.status_code}  (expected 204, no body)")
 
    # Confirm deletion
    r2 = requests.get(f"{BASE_URL}/products/2")
    print(f"  GET after delete → {r2.status_code}: {r2.json()}")
 
 
# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    wait_for_api()
 
    # ── Förmiddag ──
    print_raw_json()
    print_status_code()
    extract_fields()
    category()
    add_more_products()
    get_stock()
    get_health()
 
    # ── Eftermiddag ──
    get_product_by_id()
    post_products()
    get_crash()
    verify_post_appears_in_list()
    put_products()
    delete_products()
 
    print("\n" + "=" * 60)
    print("  All exercises completed!")
    print("=" * 60)