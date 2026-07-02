
"""
NovaStore API  –  complete solution for all morning and afternoon exercises.
 
Endpoints:
  GET  /products          – list all products             (Förmiddag 2–9)
  GET  /products/<id>     – get one product               (Eftermiddag 1)
  POST /products          – create a product              (Eftermiddag 3, 9)
  PUT  /products/<id>     – update a product              (Eftermiddag 7)
  DELETE /products/<id>   – delete a product              (Eftermiddag 8, 10)
  GET  /health            – health-check                  (Förmiddag 10)
  GET  /crash             – simulate 500 error            (Eftermiddag 5)
"""
 
from flask import Flask, jsonify, request
 
app = Flask(__name__)
 
# ---------------------------------------------------------------------------
# In-memory product store (Förmiddag 7 – add more products)
# ---------------------------------------------------------------------------
products = [
    {
        "id": 1,
        "name": "Laptop Pro 15",
        "price": 12999.00,
        "category": "Electronics",   # Förmiddag 6 – added category
        "stock": 10,                 # Förmiddag Extra 9 – stock field
    },
    {
        "id": 2,
        "name": "Wireless Mouse",
        "price": 349.00,
        "category": "Accessories",
        "stock": 50,
    },
    {
        "id": 3,
        "name": "USB-C Hub",
        "price": 599.00,
        "category": "Accessories",
        "stock": 25,
    },
    {
        "id": 4,
        "name": "Mechanical Keyboard",
        "price": 1299.00,
        "category": "Electronics",
        "stock": 15,
    },
    {
        "id": 5,
        "name": "4K Monitor",
        "price": 4499.00,
        "category": "Electronics",
        "stock": 8,
    },

    {"id": 6, 
     "name": "Webcam HD", 
     "price": 799.00,
     "category": "Accessories", 
     "stock": 35},
]
 

 
next_id = 7  # auto-increment counter
 
 
# ---------------------------------------------------------------------------
# GET / products  –  Förmiddag 2, 3, 4, 5, 6, 7, 8
# ---------------------------------------------------------------------------
@app.route("/products", methods=["GET"])
def get_products():
    """Return all products as JSON with status 200."""
    return jsonify(products), 200
 
 
# ---------------------------------------------------------------------------
# GET /products/<id>  –  Eftermiddag 1 + 2
# ---------------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Return a single product by id.
    Returns 404 Not Found if product does not exist.
    """
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        # Eftermiddag 2 – 404 Not Found
        return jsonify({"error": f"Product with id {product_id} not found"}), 404
    return jsonify(product), 200
 
 
# ---------------------------------------------------------------------------
# POST /Create products  –  Eftermiddag 3, 4, 9
# ---------------------------------------------------------------------------
@app.route("/products", methods=["POST"])
def create_product():
    """
    Create a new product.
    Expects JSON body with at least: name (str), price (positive number).
    Returns 400 Bad Request for invalid input.
    Returns 201 Created on success.
    """
    global next_id
    data = request.get_json(silent=True)
 
    # Eftermiddag 4 – validate input (400 Bad Request)
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
        "id": next_id,
        "name": str(data["name"]).strip(),
        "price": float(data["price"]),
        "category": data.get("category", "Uncategorized"),
        "stock": int(data.get("stock", 0)),
    }
    products.append(new_product)
    next_id += 1
 
    # Eftermiddag Extra 9 – 201 Created
    return jsonify(new_product), 201
 
 
# ---------------------------------------------------------------------------
# PUT /products/<id>  –  Eftermiddag Extra 7
# ---------------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Update an existing product partially or fully.
    Returns 404 if product not found, 400 for invalid data.
    """
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": f"Product with id {product_id} not found"}), 404
 
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
 
    # Validate price if provided
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
# DELETE /products/<id>  –  Eftermiddag Extra 8, 10
# ---------------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a product by id.
    Returns 404 if not found, 204 No Content on success.
    """
    global products
    product = next((p for p in products if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": f"Product with id {product_id} not found"}), 404
 
    products = [p for p in products if p["id"] != product_id]
    # Eftermiddag Extra 10 – 204 No Content (no body)
    return "", 204
 
 
# ---------------------------------------------------------------------------
# GET /health  –  Förmiddag Extra 10
# ---------------------------------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok", "message": "NovaStore API is running"}), 200
 
 
# ---------------------------------------------------------------------------
# GET /crash  –  Eftermiddag 5
# ---------------------------------------------------------------------------
@app.route("/crash", methods=["GET"])
def crash():
    """
    Simulate an unexpected server error.
    Returns 500 Internal Server Error.
    """
    return jsonify({"error": "Internal Server Error", "message": "Something went wrong on the server"}), 500
 
 
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)