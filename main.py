import sys
from models.product import Product, apply_discount
from models.user import User
from models.cart import Cart
from models.order import Order

from services.product_service import get_featured_products, search_products
from services.review_service import add_review, get_average_rating
from services.storage_service import (
    load_products,
    save_products,
    load_users,
    save_users,
    load_orders,
    save_orders
)
from services.analytics_service import print_analytics_dashboard
from utils.notifications import send_notification

def main():
    print("=" * 60)
    print("        🚀 E-COMMERCE ENGINE DEMONSTRATION 🚀        ")
    print("=" * 60)

    # --- TASK 14: Data Storage ---
    # Load products, users, and orders from JSON files
    print("\n--- [Task 14] Loading Data from JSON Storage ---")
    products = load_products()
    users = load_users()
    orders = load_orders(users)
    
    print(f"Loaded {len(products)} products, {len(users)} users, and {len(orders)} historical orders.")

    # Show catalog
    print("\n--- Current Product Catalog ---")
    for pid, p in products.items():
        print(f"ID: {p.id} | {p.name:<15} | Price: ${p.price:<6} | Stock: {p.stock:<4} | Category: {p.category:<8} | Discount: {p.discount*100}%")

    # --- TASK 11: Discounts ---
    print("\n--- [Task 11] Applying Promotions & Discounts ---")
    # Apply a 15% discount to Puma T-Shirt (Product 3)
    puma_tshirt = products[3]
    print(f"Original price of '{puma_tshirt.name}': ${puma_tshirt.price:.2f}")
    apply_discount(puma_tshirt, 0.15)
    print(f"Applied 15% discount!")
    print(f"Discounted price of '{puma_tshirt.name}': ${puma_tshirt.get_final_price():.2f}")

    # Set up user and cart
    user = users.get("holland")
    if not user:
        user = User("holland", "holland@mail.com", "12345678")
        users["holland"] = user
    
    cart = Cart()
    cart.add_item(products[1], 2)
    cart.add_item(products[2], 1)

    print("Cart total:", cart.calculate_total(products))

    order = Order(user, cart.items, cart.calculate_total(products))

    if order.process_payment():
        for product_id, qyt in cart.items.items():
            products[product_id].stock -= qyt

        send_notification("Order confirmed!")
        print("Order completed!")
    else:
        print("Payment failed")

    add_review(user, 1, 5, "Great product!")
    print("Rating:", get_average_rating(1))

    p1 = Product(1, "iPhone", 1200, "Phone", 10, "Electronics", "Apple", True, True, 10)
    print(p1)

if __name__ == "__main__":
    main()