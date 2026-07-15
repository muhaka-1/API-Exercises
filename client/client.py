"""
NovaStore Client
Demonstrates all API endpoints by making HTTP requests and printing the results.
"""

import os
import time
import requests

BASE_URL = os.getenv("API_URL", "http://localhost:5001")


def separator(title: str) -> None:
    """Prints a titled section divider to make terminal output easier to read."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


# ---------------------------------------------------------------------------
# Waits for the API to be reachable before running any requests.
# Retries up to max_retries times with a short delay between attempts.
# This prevents race conditions when the API container is still starting up.
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
# Fetches all products and prints the raw JSON string.
# Shows what a client receives before any parsing is applied.
# ---------------------------------------------------------------------------
def print_raw_json() -> None:
    separator("Raw JSON response from GET /products")
    response = requests.get(f"{BASE_URL}/products")
    print(response.text)


# ---------------------------------------------------------------------------
# Fetches all products and prints the HTTP status code.
# Demonstrates how a client can inspect the status code to understand
# whether the request succeeded before reading the response body.
# ---------------------------------------------------------------------------
def print_status_code() -> None:
    separator("HTTP status code from GET /products")
    response = requests.get(f"{BASE_URL}/products")
    print(f"  Status code: {response.status_code}")
    if response.status_code == 200:
        print("  Meaning: OK – request succeeded, data returned.")


# ---------------------------------------------------------------------------
# Fetches all products and extracts only the id, name, and price fields.
# Shows how to parse a JSON array and read specific keys from each object.
# ---------------------------------------------------------------------------
def extract_fields() -> None:
    separator("Extracted fields: id, name, price")
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    for p in products:
        print(f"  id={p['id']}  name={p['name']}  price={p['price']} kr")


# ---------------------------------------------------------------------------
# Fetches all products and prints each one with its category included.
# Demonstrates that the client automatically benefits from new fields
# added to the API without any breaking changes.
# ---------------------------------------------------------------------------
def print_with_category() -> None:
    separator("Products with category field")
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    for p in products:
        print(f"  [{p['category']}] {p['name']} – {p['price']} kr")


# ---------------------------------------------------------------------------
# Fetches all products and prints the total count plus each product name.
# Shows that the client loop handles any number of products automatically,
# regardless of how many are returned by the API.
# ---------------------------------------------------------------------------
def print_all_products() -> None:
    separator("All products")
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    print(f"  Total products returned: {len(products)}")
    for p in products:
        print(f"  {p['id']}. {p['name']}")


# ---------------------------------------------------------------------------
# Fetches all products and prints the stock level for each one.
# Uses dict.get() with a fallback so the client handles products
# that may not have a stock field without crashing.
# ---------------------------------------------------------------------------
def print_stock_levels() -> None:
    separator("Stock levels")
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    for p in products:
        print(f"  {p['name']}: {p.get('stock', 'N/A')} in stock")


# ---------------------------------------------------------------------------
# Calls the /health endpoint and prints the response.
# Health checks are used by infrastructure tools (load balancers, Docker,
# Kubernetes) to verify the service is alive before routing traffic to it.
# ---------------------------------------------------------------------------
def check_health() -> None:
    separator("Health check – GET /health")
    response = requests.get(f"{BASE_URL}/health")
    print(f"  Status code : {response.status_code}")
    print(f"  Response    : {response.json()}")


# ---------------------------------------------------------------------------
# Fetches a single product by its id using GET /products/<id>.
# Then requests a product that does not exist (id 999) to demonstrate
# that the API returns 404 Not Found for missing resources.
# ---------------------------------------------------------------------------
def get_product_by_id() -> None:
    separator("Single product – GET /products/1")
    r = requests.get(f"{BASE_URL}/products/1")
    print(f"  Status: {r.status_code}")
    print(f"  Body  : {r.json()}")

    separator("Product not found – GET /products/999")
    r = requests.get(f"{BASE_URL}/products/999")
    print(f"  Status: {r.status_code}")
    print(f"  Body  : {r.json()}")


# ---------------------------------------------------------------------------
# Creates a valid product via POST /products and expects 201 Created.
# Then sends three invalid requests to show how the API rejects bad data
# with 400 Bad Request: missing name, missing price, and negative price.
# ---------------------------------------------------------------------------
def post_products() -> None:
    separator("Create a product – POST /products (expects 201)")
    payload = {"name": "Noise-Cancelling Headphones", "price": 2499.00,
               "category": "Audio", "stock": 20}
    r = requests.post(f"{BASE_URL}/products", json=payload)
    print(f"  Status: {r.status_code}  (expected 201)")
    print(f"  Body  : {r.json()}")

    separator("Validation errors – POST /products with bad data (expects 400)")
    r = requests.post(f"{BASE_URL}/products", json={"price": 99})
    print(f"  Missing 'name'  → {r.status_code}: {r.json()}")

    r = requests.post(f"{BASE_URL}/products", json={"name": "Widget"})
    print(f"  Missing 'price' → {r.status_code}: {r.json()}")

    r = requests.post(f"{BASE_URL}/products", json={"name": "Widget", "price": -50})
    print(f"  Negative price  → {r.status_code}: {r.json()}")


# ---------------------------------------------------------------------------
# Calls GET /crash to simulate an unexpected server-side failure.
# Demonstrates the difference between 5xx errors (server fault) and
# 4xx errors (client fault). A 500 means the developer needs to fix something.
# ---------------------------------------------------------------------------
def trigger_crash() -> None:
    separator("Simulated server error – GET /crash (expects 500)")
    r = requests.get(f"{BASE_URL}/crash")
    print(f"  Status: {r.status_code}")
    print(f"  Body  : {r.json()}")


# ---------------------------------------------------------------------------
# Creates a product via POST, then immediately fetches the full product list
# to confirm the new product appears in GET /products.
# Verifies that the two endpoints share the same underlying data store.
# ---------------------------------------------------------------------------
def verify_post_appears_in_list() -> None:
    separator("POST then verify in GET /products")
    payload = {"name": "Smart Speaker", "price": 899.00,
               "category": "Audio", "stock": 30}
    r_post = requests.post(f"{BASE_URL}/products", json=payload)
    created = r_post.json()
    print(f"  Created: {created['name']} (id={created['id']})")

    r_list = requests.get(f"{BASE_URL}/products")
    names = [p["name"] for p in r_list.json()]
    print(f"  Visible in GET /products: {created['name'] in names}")


# ---------------------------------------------------------------------------
# Sends a partial update to product 1 via PUT /products/1.
# Only the price field is changed; all other fields remain the same.
# Confirms the API returns 200 OK with the updated product.
# ---------------------------------------------------------------------------
def update_product() -> None:
    separator("Update a product – PUT /products/1")
    r = requests.put(f"{BASE_URL}/products/1", json={"price": 11499.00})
    print(f"  Status: {r.status_code}")
    print(f"  Body  : {r.json()}")


# ---------------------------------------------------------------------------
# Deletes product 2 via DELETE /products/2 and expects 204 No Content.
# Then fetches the same product to confirm it is gone (expects 404).
# Demonstrates that 204 means success with no response body.
# ---------------------------------------------------------------------------
def delete_product() -> None:
    separator("Delete a product – DELETE /products/2 (expects 204)")
    r = requests.delete(f"{BASE_URL}/products/2")
    print(f"  Status: {r.status_code}  (expected 204, no body)")

    r2 = requests.get(f"{BASE_URL}/products/2")
    print(f"  GET after delete → {r2.status_code}: {r2.json()}")


# ---------------------------------------------------------------------------
# Main entry point – runs all functions in order.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    wait_for_api()

    print_raw_json()
    print_status_code()
    extract_fields()
    print_with_category()
    print_all_products()
    print_stock_levels()
    check_health()

    get_product_by_id()
    post_products()
    trigger_crash()
    verify_post_appears_in_list()
    update_product()
    delete_product()

    print("\n" + "=" * 60)
    print("  All exercises completed!")
    print("=" * 60)