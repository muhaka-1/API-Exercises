from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    products = [
        {"id": 1, "name": "Laptop", "price": 12990, "stock": 5},
        {"id": 2, "name": "Monitor", "price": 2990, "stock": 10},
    ]

    @app.get("/products")
    def get_products():
        return jsonify(products)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
