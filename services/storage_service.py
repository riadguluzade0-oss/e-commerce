import os
import json
from models.product import Product
from models.user import User
from models.order import Order

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_products(products):
    ensure_data_dir()
    data = {}
    for pid, product in products.items():
        data[str(pid)] = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "category": product.category,
            "brand": product.brand,
            "is_featured": getattr(product, "is_featured", False),
            "is_trending": getattr(product, "is_trending", False),
            "discount": getattr(product, "discount", 0.0)
        }
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_products():
    ensure_data_dir()
    if not os.path.exists(PRODUCTS_FILE):
        # Default seeding
        default_products = {
            1: Product(1, "Nike shoes", 120, 10, "Shoes", "Nike"),
            2: Product(2, "Adidas Hoodie", 80, 5, "Clothes", "Adidas"),
            3: Product(3, "Puma T-Shirt", 40, 20, "Clothes", "Puma"),
        }
        default_products[1].is_featured = True
        default_products[2].is_trending = True
        save_products(default_products)
        return default_products

    with open(PRODUCTS_FILE, "r") as f:
        data = json.load(f)
    
    products = {}
    for pid_str, pdata in data.items():
        pid = int(pid_str)
        product = Product(
            id=pdata["id"],
            name=pdata["name"],
            price=pdata["price"],
            stock=pdata["stock"],
            category=pdata["category"],
            brand=pdata["brand"]
        )
        product.is_featured = pdata.get("is_featured", False)
        product.is_trending = pdata.get("is_trending", False)
        product.discount = pdata.get("discount", 0.0)
        products[pid] = product
    return products

def save_users(users):
    ensure_data_dir()
    data = {}
    for username, user in users.items():
        data[username] = {
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "favorites": getattr(user, "favorites", [])
        }
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_users():
    ensure_data_dir()
    if not os.path.exists(USERS_FILE):
        # Default seeding
        default_users = {
            "holland": User("holland", "holland@mail.com", "12345678")
        }
        save_users(default_users)
        return default_users

    with open(USERS_FILE, "r") as f:
        data = json.load(f)
    
    users = {}
    for username, udata in data.items():
        user = User(
            username=udata["username"],
            email=udata["email"],
            password=udata["password"]
        )
        user.favorites = udata.get("favorites", [])
        users[username] = user
    return users

def save_orders(orders):
    ensure_data_dir()
    data = []
    for order in orders:
        data.append({
            "id": order.id,
            "user_username": order.user.username,
            "items": order.items,
            "total": order.total,
            "status": order.status,
            "delivery_status": getattr(order, "delivery_status", "pending")
        })
    with open(ORDERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_orders(users):
    ensure_data_dir()
    if not os.path.exists(ORDERS_FILE):
        return []

    with open(ORDERS_FILE, "r") as f:
        data = json.load(f)
    
    orders = []
    for odata in data:
        user = users.get(odata["user_username"])
        if not user:
            # Fallback user if not found in db
            user = User(odata["user_username"], f"{odata['user_username']}@mail.com", "")
        
        order = Order(user, odata["items"], odata["total"])
        order.id = odata["id"]
        order.status = odata["status"]
        order.delivery_status = odata.get("delivery_status", "pending")
        orders.append(order)
    return orders
