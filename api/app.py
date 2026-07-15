
"""
NovaStore API  –  A simple REST API for managing products in the NovaStore backend.
 
Endpoints:
  GET  /products          – list all products             
  GET  /products/<id>     – get one product               
  POST /products          – create a product              
  PUT  /products/<id>     – update a product              
  DELETE /products/<id>   – delete a product              
  GET  /health            – health-check                 
  GET  /crash             – simulate 500 error            
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# In-memory product store – acts as the database for this exercise.
# Each product has an id, name, price, category, and stock level.
# ---------------------------------------------------------------------------
products = [
    {"id": 1, "name": "Laptop Pro 15",      "price": 12999.00, "category": "Electronics", "stock": 10},
    {"id": 2, "name": "Wireless Mouse",     "price":   349.00, "category": "Accessories", "stock": 50},
    {"id": 3, "name": "USB-C Hub",          "price":   599.00, "category": "Accessories", "stock": 25},
    {"id": 4, "name": "Mechanical Keyboard","price":  1299.00, "category": "Electronics", "stock": 15},
    {"id": 5, "name": "4K Monitor",         "price":  4499.00, "category": "Electronics", "stock":  8},
    {"id": 6, "name": "Webcam HD",          "price":   799.00, "category": "Accessories", "stock": 35},
]

next_id = 7  # auto-increment counter for new products


# ---------------------------------------------------------------------------
# GET /products
# Returns the full list of products as a JSON array.
# Always responds with 200 OK.
# ---------------------------------------------------------------------------
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products), 200


# ---------------------------------------------------------------------------
# GET /products/<id>
# Looks up a single product by its numeric id.
# Returns 200 OK with the product if found.
# Returns 404 Not Found if no product matches the given id.
# ---------------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": f"Product with id {product_id} not found"}), 404
    return jsonify(product), 200


# ---------------------------------------------------------------------------
# POST /products
# Creates a new product from the JSON body in the request.
# Required fields: name (non-empty string), price (positive number).
# Optional fields: category (defaults to "Uncategorized"), stock (defaults to 0).
# Returns 400 Bad Request if any required field is missing or invalid.
# Returns 201 Created with the new product on success.
# ---------------------------------------------------------------------------
@app.route("/products", methods=["POST"])
def create_product():
    global next_id
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    errors = []
    if "name" not in data or not str(data["name"]).strip():
        errors.append("'name' is required and must not be empty")
    if "price" not in data:
        errors.append("'price' is required")
    elif not isinstance(data["price"], (int, float)):
        errors.append("'price' must be a number")
    elif data["price"] < 0:
        errors.append("'price' must not be negative")

    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    new_product = {
        "id":       next_id,
        "name":     str(data["name"]).strip(),
        "price":    float(data["price"]),
        "category": data.get("category", "Uncategorized"),
        "stock":    int(data.get("stock", 0)),
    }
    products.append(new_product)
    next_id += 1

    return jsonify(new_product), 201


# ---------------------------------------------------------------------------
# PUT /products/<id>
# Partially updates an existing product. Only fields included in the request
# body are changed; omitted fields keep their current values.
# Returns 404 Not Found if the product does not exist.
# Returns 400 Bad Request if any provided value is invalid.
# Returns 200 OK with the updated product on success.
# ---------------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": f"Product with id {product_id} not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    if "price" in data:
        if not isinstance(data["price"], (int, float)):
            return jsonify({"error": "'price' must be a number"}), 400
        if data["price"] < 0:
            return jsonify({"error": "'price' must not be negative"}), 400
        product["price"] = float(data["price"])

    if "name" in data:
        if not str(data["name"]).strip():
            return jsonify({"error": "'name' must not be empty"}), 400
        product["name"] = str(data["name"]).strip()

    if "category" in data:
        product["category"] = data["category"]
    if "stock" in data:
        product["stock"] = int(data["stock"])

    return jsonify(product), 200


# ---------------------------------------------------------------------------
# DELETE /products/<id>
# Removes a product permanently from the in-memory store.
# Returns 404 Not Found if the product does not exist.
# Returns 204 No Content on success (no response body).
# ---------------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    global products
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": f"Product with id {product_id} not found"}), 404

    products = [p for p in products if p["id"] != product_id]
    return "", 204


# ---------------------------------------------------------------------------
# GET /health
# Simple health-check endpoint used to verify the API is running.
# Load balancers and orchestration tools call this before routing traffic.
# Always returns 200 OK with a status message.
# ---------------------------------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "NovaStore API is running"}), 200


# ---------------------------------------------------------------------------
# GET /crash
# Simulates an unhandled server-side error.
# Used to demonstrate how 500 Internal Server Error differs from 4xx errors:
# 5xx means the fault is on the server, not the client.
# ---------------------------------------------------------------------------
@app.route("/crash", methods=["GET"])
def crash():
    return jsonify({"error": "Internal Server Error", "message": "Something went wrong on the server"}), 500


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)