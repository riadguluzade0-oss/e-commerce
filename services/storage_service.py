import json
import os
import sqlite3

from models.order import Order
from models.product import Product
from models.user import User

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DATABASE_FILE = os.path.join(DATA_DIR, "ecommerce.db")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def get_connection():
    ensure_data_dir()
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                stock INTEGER NOT NULL DEFAULT 0,
                category TEXT NOT NULL DEFAULT '',
                brand TEXT NOT NULL DEFAULT '',
                is_featured INTEGER NOT NULL DEFAULT 0,
                is_trending INTEGER NOT NULL DEFAULT 0,
                discount REAL NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_favorites (
                username TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                PRIMARY KEY (username, product_id),
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_wishlist (
                username TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                PRIMARY KEY (username, product_id),
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_username TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL,
                delivery_status TEXT NOT NULL DEFAULT 'pending'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                PRIMARY KEY (order_id, product_id),
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT NOT NULL DEFAULT ''
            )
        """)


def _read_json_file(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _table_is_empty(table_name):
    ensure_database()
    with get_connection() as conn:
        row = conn.execute(f"SELECT COUNT(*) AS count FROM {table_name}").fetchone()
    return row["count"] == 0


def _default_products():
    products = {
        1: Product(1, "Nike shoes", 120, 10, "Shoes", "Nike"),
        2: Product(2, "Adidas Hoodie", 80, 5, "Clothes", "Adidas"),
        3: Product(3, "Puma T-Shirt", 40, 20, "Clothes", "Puma"),
    }
    products[1].is_featured = True
    products[2].is_trending = True
    return products


def _products_from_json():
    data = _read_json_file(PRODUCTS_FILE, {})
    if not isinstance(data, dict):
        return {}

    products = {}
    for pid_str, pdata in data.items():
        pid = int(pid_str)
        product = Product(
            id=pdata["id"],
            name=pdata["name"],
            price=pdata["price"],
            description=pdata.get("description", ""),
            stock=pdata["stock"],
            category=pdata["category"],
            brand=pdata["brand"],
        )
        product.is_featured = pdata.get("is_featured", False)
        product.is_trending = pdata.get("is_trending", False)
        product.discount = pdata.get("discount", 0.0)
        products[pid] = product
    return products


def save_products(products):
    ensure_database()
    with get_connection() as conn:
        conn.execute("DELETE FROM products")
        conn.executemany(
            """
            INSERT INTO products (
                id, name, price, description, stock, category, brand,
                is_featured, is_trending, discount
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    product.id,
                    product.name,
                    product.price,
                    getattr(product, "description", ""),
                    product.stock,
                    product.category,
                    product.brand,
                    int(getattr(product, "is_featured", False)),
                    int(getattr(product, "is_trending", False)),
                    getattr(product, "discount", 0.0),
                )
                for product in products.values()
            ],
        )


def load_products():
    ensure_database()
    if _table_is_empty("products"):
        products = _products_from_json() or _default_products()
        save_products(products)
        return products

    products = {}
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM products ORDER BY id").fetchall()

    for row in rows:
        product = Product(
            id=row["id"],
            name=row["name"],
            price=row["price"],
            description=row["description"],
            stock=row["stock"],
            category=row["category"],
            brand=row["brand"],
        )
        product.is_featured = bool(row["is_featured"])
        product.is_trending = bool(row["is_trending"])
        product.discount = row["discount"]
        products[product.id] = product
    return products


def _users_from_json():
    data = _read_json_file(USERS_FILE, {})
    if not isinstance(data, dict):
        return {}

    users = {}
    for username, udata in data.items():
        user = User(
            username=udata["username"],
            email=udata["email"],
            password=udata["password"],
        )
        user.favorites = udata.get("favorites", [])
        user.wishlist = udata.get("wishlist", [])
        users[username] = user
    return users


def save_users(users):
    ensure_database()
    with get_connection() as conn:
        conn.execute("DELETE FROM user_favorites")
        conn.execute("DELETE FROM user_wishlist")
        conn.execute("DELETE FROM users")
        for user in users.values():
            conn.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (user.username, user.email, user.password),
            )
            conn.executemany(
                "INSERT OR IGNORE INTO user_favorites (username, product_id) VALUES (?, ?)",
                [(user.username, product_id) for product_id in getattr(user, "favorites", [])],
            )
            conn.executemany(
                "INSERT OR IGNORE INTO user_wishlist (username, product_id) VALUES (?, ?)",
                [(user.username, product_id) for product_id in getattr(user, "wishlist", [])],
            )


def load_users():
    ensure_database()
    if _table_is_empty("users"):
        users = _users_from_json() or {
            "holland": User("holland", "holland@mail.com", "12345678")
        }
        save_users(users)
        return users

    users = {}
    with get_connection() as conn:
        user_rows = conn.execute("SELECT * FROM users ORDER BY username").fetchall()
        favorite_rows = conn.execute(
            "SELECT username, product_id FROM user_favorites ORDER BY username, product_id"
        ).fetchall()
        wishlist_rows = conn.execute(
            "SELECT username, product_id FROM user_wishlist ORDER BY username, product_id"
        ).fetchall()

    for row in user_rows:
        users[row["username"]] = User(row["username"], row["email"], row["password"])

    for row in favorite_rows:
        if row["username"] in users:
            users[row["username"]].favorites.append(row["product_id"])

    for row in wishlist_rows:
        if row["username"] in users:
            users[row["username"]].wishlist.append(row["product_id"])

    return users


def _orders_from_json(users):
    data = _read_json_file(ORDERS_FILE, [])
    if not isinstance(data, list):
        return []

    orders = []
    for odata in data:
        username = odata["user_username"]
        user = users.get(username) or User(username, f"{username}@mail.com", "")
        order = Order(user, odata["items"], odata["total"])
        order.id = odata["id"]
        order.status = odata["status"]
        order.delivery_status = odata.get("delivery_status", "pending")
        orders.append(order)
    return orders


def save_orders(orders):
    ensure_database()
    with get_connection() as conn:
        conn.execute("DELETE FROM order_items")
        conn.execute("DELETE FROM orders")
        for order in orders:
            conn.execute(
                """
                INSERT INTO orders (id, user_username, total, status, delivery_status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    order.id,
                    order.user.username,
                    order.total,
                    order.status,
                    getattr(order, "delivery_status", "pending"),
                ),
            )
            conn.executemany(
                "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                [
                    (order.id, int(product_id), quantity)
                    for product_id, quantity in order.items.items()
                ],
            )


def load_orders(users):
    ensure_database()
    if _table_is_empty("orders"):
        orders = _orders_from_json(users)
        if orders:
            save_orders(orders)
        return orders

    orders = []
    with get_connection() as conn:
        order_rows = conn.execute("SELECT * FROM orders ORDER BY id").fetchall()
        item_rows = conn.execute(
            "SELECT order_id, product_id, quantity FROM order_items ORDER BY order_id, product_id"
        ).fetchall()

    items_by_order_id = {}
    for row in item_rows:
        items_by_order_id.setdefault(row["order_id"], {})[row["product_id"]] = row["quantity"]

    for row in order_rows:
        username = row["user_username"]
        user = users.get(username) or User(username, f"{username}@mail.com", "")
        order = Order(user, items_by_order_id.get(row["id"], {}), row["total"])
        order.id = row["id"]
        order.status = row["status"]
        order.delivery_status = row["delivery_status"]
        orders.append(order)
    return orders


def _reviews_from_json():
    data = _read_json_file(REVIEWS_FILE, [])
    if not isinstance(data, list):
        return []
    return [
        {
            "user": row["user"],
            "product_id": row["product_id"],
            "rating": row["rating"],
            "comment": row["comment"],
        }
        for row in data
    ]


def save_reviews(reviews):
    ensure_database()
    with get_connection() as conn:
        conn.execute("DELETE FROM reviews")
        conn.executemany(
            "INSERT INTO reviews (username, product_id, rating, comment) VALUES (?, ?, ?, ?)",
            [(r.user, r.product_id, r.rating, r.comment) for r in reviews],
        )


def load_review_rows():
    ensure_database()
    if _table_is_empty("reviews"):
        rows = _reviews_from_json()
        if rows:
            with get_connection() as conn:
                conn.executemany(
                    "INSERT INTO reviews (username, product_id, rating, comment) VALUES (?, ?, ?, ?)",
                    [
                        (row["user"], row["product_id"], row["rating"], row["comment"])
                        for row in rows
                    ],
                )
        return rows

    with get_connection() as conn:
        rows = conn.execute(
            "SELECT username, product_id, rating, comment FROM reviews ORDER BY id"
        ).fetchall()
    return [
        {
            "user": row["username"],
            "product_id": row["product_id"],
            "rating": row["rating"],
            "comment": row["comment"],
        }
        for row in rows
    ]


def add_review_row(user, product_id, rating, comment):
    ensure_database()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO reviews (username, product_id, rating, comment) VALUES (?, ?, ?, ?)",
            (user, product_id, rating, comment),
        )
