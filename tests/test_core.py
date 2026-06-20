import os
import tempfile
import unittest
from unittest.mock import patch

from main import register_user
from models.cart import Cart
from models.order import Order
from models.product import Product
from models.user import User
from services.homepage_service import get_featured_products, get_trending_products
from services.search_service import advanced_search
from services.wishlist_service import add_to_wishlist


class CartTests(unittest.TestCase):
    def test_cart_rejects_quantities_over_stock(self):
        product = Product(1, "Shoes", 100, stock=2)
        cart = Cart()

        self.assertTrue(cart.add_item(product, 2))
        self.assertFalse(cart.add_item(product, 1))
        self.assertEqual(cart.items, {1: 2})

    def test_cart_total_uses_product_and_promo_discounts(self):
        product = Product(1, "Shoes", 100, stock=2, discount=0.20)
        cart = Cart()

        cart.add_item(product, 2)
        cart.apply_promo_code("SAVE10")

        self.assertEqual(cart.calculate_total({1: product}), 144)


class ServiceTests(unittest.TestCase):
    def test_search_and_homepage_services_accept_product_dicts(self):
        products = {
            1: Product(1, "Nike Shoes", 120, stock=5, is_featured=True),
            2: Product(2, "Adidas Hoodie", 80, stock=5, is_trending=True),
        }

        self.assertEqual([p.id for p in advanced_search(products, "nike")], [1])
        self.assertEqual([p.id for p in get_featured_products(products)], [1])
        self.assertEqual([p.id for p in get_trending_products(products)], [2])

    def test_wishlist_stores_product_ids_without_duplicates(self):
        user = User("alice", "alice@example.com", "password123")
        product = Product(1, "Nike Shoes", 120)

        self.assertTrue(add_to_wishlist(user, product))
        self.assertFalse(add_to_wishlist(user, product))
        self.assertEqual(user.wishlist, [1])


class StorageTests(unittest.TestCase):
    def test_products_orders_and_reviews_round_trip_with_sqlite(self):
        from services import storage_service

        old_data_dir = storage_service.DATA_DIR
        old_database_file = storage_service.DATABASE_FILE

        with tempfile.TemporaryDirectory() as tmpdir:
            storage_service.DATA_DIR = tmpdir
            storage_service.DATABASE_FILE = os.path.join(tmpdir, "ecommerce.db")
            try:
                product = Product(1, "Nike Shoes", 120, stock=8, category="Shoes", brand="Nike")
                product.is_featured = True
                user = User("alice", "alice@example.com", "password123")
                order = Order(user, {1: 2}, 240)
                order.id = 1234
                order.status = "completed"
                order.delivery_status = "delivered"

                storage_service.save_products({1: product})
                storage_service.save_users({"alice": user})
                storage_service.save_orders([order])
                storage_service.add_review_row("alice", 1, 5, "Great")

                loaded_products = storage_service.load_products()
                loaded_users = storage_service.load_users()
                loaded_orders = storage_service.load_orders(loaded_users)
                loaded_reviews = storage_service.load_review_rows()

                self.assertEqual(loaded_products[1].name, "Nike Shoes")
                self.assertTrue(loaded_products[1].is_featured)
                self.assertEqual(loaded_orders[0].items, {1: 2})
                self.assertEqual(loaded_orders[0].delivery_status, "delivered")
                self.assertEqual(loaded_reviews[0]["comment"], "Great")
            finally:
                storage_service.DATA_DIR = old_data_dir
                storage_service.DATABASE_FILE = old_database_file

    def test_users_round_trip_with_wishlist(self):
        from services import storage_service

        old_data_dir = storage_service.DATA_DIR
        old_database_file = storage_service.DATABASE_FILE

        with tempfile.TemporaryDirectory() as tmpdir:
            storage_service.DATA_DIR = tmpdir
            storage_service.DATABASE_FILE = os.path.join(tmpdir, "ecommerce.db")
            try:
                user = User("alice", "alice@example.com", "password123")
                user.favorites = [2]
                user.wishlist = [1]

                storage_service.save_users({"alice": user})
                loaded = storage_service.load_users()

                self.assertEqual(loaded["alice"].favorites, [2])
                self.assertEqual(loaded["alice"].wishlist, [1])
            finally:
                storage_service.DATA_DIR = old_data_dir
                storage_service.DATABASE_FILE = old_database_file

    def test_register_user_creates_and_persists_new_user(self):
        from services import storage_service

        old_data_dir = storage_service.DATA_DIR
        old_database_file = storage_service.DATABASE_FILE

        with tempfile.TemporaryDirectory() as tmpdir:
            storage_service.DATA_DIR = tmpdir
            storage_service.DATABASE_FILE = os.path.join(tmpdir, "ecommerce.db")
            try:
                users = {}
                answers = ["alice", "alice@example.com", "password123", "password123"]

                with patch("builtins.input", side_effect=answers):
                    user = register_user(users)

                self.assertEqual(user.username, "alice")
                self.assertIn("alice", users)
                self.assertEqual(storage_service.load_users()["alice"].email, "alice@example.com")
            finally:
                storage_service.DATA_DIR = old_data_dir
                storage_service.DATABASE_FILE = old_database_file


if __name__ == "__main__":
    unittest.main()
