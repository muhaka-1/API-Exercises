NovaStore API – Complete Solution Guide

Project Structure

novastore/
├── docker-compose.yml
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
└── client/
    ├── Dockerfile
    ├── requirements.txt
    └── client.py


Förmiddag – Konsumera ett API


Uppgift 1 – Starta lösningen

bashdocker compose up --build

This builds the api and client Docker images and starts the API container on port 5001.


Uppgift 2 – Öppna API:et i webbläsaren

Navigate to:

http://localhost:5001/products

You will see a JSON response (not HTML). JSON is a lightweight data format that clients read programmatically, whereas HTML is rendered visually by browsers.


Uppgift 3 – Skriv ut JSON-svaret i klienten

In client.py:

pythonresponse = requests.get(f"{BASE_URL}/products")
print(response.text)   # raw JSON string

Run with:

bashdocker compose run --rm client


Uppgift 4 – Skriv ut statuskoden

pythonresponse = requests.get(f"{BASE_URL}/products")
print(f"Status code: {response.status_code}")

200 OK means the server received the request and returned data successfully. The client can branch logic on the status code (e.g., only parse body if status == 200).


Uppgift 5 – Extrahera id, name och price

pythonproducts = response.json()          # parse JSON → Python list
for p in products:
    print(p["id"], p["name"], p["price"])


Uppgift 6 – Lägg till fältet category i API-svaret

In app.py, add "category" to each product dict:

python{"id": 1, "name": "Laptop Pro 15", "price": 12999.00, "category": "Electronics", ...}

The client continues to work because JSON is additive – new fields are ignored unless the client reads them.


Uppgift 7 & Extra 8 – Lägg till fler produkter

Simply add more dicts to the products list in app.py. The client loop handles any number automatically:

pythonfor p in products:
    print(p["name"])


Extra Uppgift 9 – Verifiera att stock skrivs ut

Add "stock" to each product in the API, then in the client:

pythonprint(f"{p['name']}: {p.get('stock', 'N/A')} in stock")


Extra Uppgift 10 – /health endpoint

In app.py:

python@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "NovaStore API is running"}), 200


Eftermiddag – Bygg ett robust API


Uppgift 1 – GET /products/{id}

python@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": f"Product with id {product_id} not found"}), 404
    return jsonify(product), 200


<int:product_id> – Flask converts the URL segment to an integer automatically.
next(..., None) – returns the first match or None if nothing found.



Uppgift 2 – 404 Not Found

When GET /products/999 is called and no product has id 999:

pythonreturn jsonify({"error": "Product with id 999 not found"}), 404

404 signals to the client that the resource simply does not exist (not a server bug).


Uppgift 3 – POST /products

python@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(silent=True)
    # ... validation ...
    products.append(new_product)
    return jsonify(new_product), 201

Send from the client or curl:

bashcurl -X POST http://localhost:5001/products \
     -H "Content-Type: application/json" \
     -d '{"name":"Headset","price":799}'


Uppgift 4 – 400 Bad Request (validation)

The API checks:


name missing or empty → 400
price missing → 400
price is not a number → 400
price is negative → 400


pythonif "price" not in data:
    errors.append("'price' is required")
elif data["price"] < 0:
    errors.append("'price' must not be negative")

if errors:
    return jsonify({"error": "Validation failed", "details": errors}), 400

Why stop at the API? Invalid data that reaches the database can corrupt it, cause crashes, or violate constraints. The API acts as a gatekeeper.


Uppgift 5 – GET /crash → 500 Internal Server Error

python@app.route("/crash", methods=["GET"])
def crash():
    return jsonify({"error": "Internal Server Error"}), 500

500 means the fault is on the server side (developer's bug), not the client's.


Extra Uppgift 6 – POST syncs with GET /products

Because products is a shared in-memory list, items added via POST are immediately visible via GET /products. No extra work needed – the list is the same object.


Extra Uppgift 7 – PUT /products/{id}

python@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json(silent=True)
    if "price" in data:
        product["price"] = data["price"]
    if "name" in data:
        product["name"] = data["name"]
    return jsonify(product), 200


Extra Uppgift 8 & 9 – DELETE /products/{id} → 204 No Content

python@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    global products
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Not found"}), 404
    products = [p for p in products if p["id"] != product_id]
    return "", 204   # 204 = success, but no body


