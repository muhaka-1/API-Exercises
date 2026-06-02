import unittest

from app import app


class ProductsApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_products_returns_200_and_list(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        for product in data:
            self.assertIn("id", product)
            self.assertIn("name", product)
            self.assertIn("price", product)
            self.assertIn("stock", product)


if __name__ == "__main__":
    unittest.main()
