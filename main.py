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

    # --- TASK 16: Inventory Checks ---
    print("\n--- [Task 16] Strict Stock Checks ---")
    # Attempting to add 25 Puma T-Shirts to Cart (Stock is 20)
    print(f"Attempting to add 25 '{puma_tshirt.name}' to cart (Stock: {puma_tshirt.stock})...")
    cart.add_item(puma_tshirt, 25)
    
    # Adding items within stock limits
    print(f"\nAdding items within stock limits...")
    cart.add_item(products[1], 2) # Nike shoes (Stock: 10)
    cart.add_item(products[2], 3) # Adidas Hoodie (Stock: 5 -> will trigger low stock alert upon purchase!)
    
    print(f"Current cart items (Product ID: Quantity): {cart.items}")

    # --- TASK 11 (Optional): Promo Code System ---
    print("\n--- [Task 11] Cart Promo Code System ---")
    total_before = cart.calculate_total(products)
    print(f"Cart total before promo code: ${total_before:.2f}")
    
    # Apply valid promo code "SAVE10" (10% off)
    cart.apply_promo_code("SAVE10")
    total_after = cart.calculate_total(products)
    print(f"Cart total after 'SAVE10' promo code: ${total_after:.2f}")

    # --- TASK 10: Payment & Order Creation ---
    print("\n--- [Task 10 & 16] Checkout, Payment & Inventory Reduction ---")
    order = Order(user, cart.items, total_after)
    
    # Validate stock before checking out
    can_checkout = True
    for pid_str, qty in cart.items.items():
        pid = int(pid_str)
        if products[pid].stock < qty:
            print(f"❌ Checkout failed: '{products[pid].name}' stock has changed and is now insufficient.")
            can_checkout = False
            break

    if can_checkout:
        # Override process_payment success for deterministic demo flow
        print("Processing payment...")
        order.status = 'paid'
        print(f"Payment successful! Order #{order.id} status is now: {order.status}")
        
        # Deduct stock & trigger low-stock alerts if applicable
        for pid_str, qty in cart.items.items():
            pid = int(pid_str)
            products[pid].reduce_stock(qty)
            
        send_notification("Order confirmed!")
        orders.append(order)
    else:
        print("Order could not be processed due to stock constraints.")

    # --- TASK 10: Delivery Stage Transitions ---
    print("\n--- [Task 10] Delivery Stage Transitions ---")
    print(f"Initial delivery status: {order.delivery_status}")
    
    # Move through delivery stages
    print("Transitioning to 'shipped'...")
    order.update_delivery_status("shipped")
    
    print("Transitioning to 'delivered'...")
    order.update_delivery_status("delivered")
    
    print(f"Final order status: {order.status} | Final delivery status: {order.delivery_status}")

    # --- TASK 14: Data Persistence Save ---
    print("\n--- [Task 14] Persisting Updated State to Storage ---")
    save_products(products)
    save_users(users)
    save_orders(orders)
    print("Data saved successfully to JSON files.")

    # --- TASK 13: Analytics Dashboard ---
    print("\n--- [Task 13] Running Analytics Dashboard ---")
    print_analytics_dashboard(orders, products)

    # Review functionality
    print("\n--- Leaving a Review ---")
    add_review(user, 1, 5, "Great product!")
    print("Nike shoes average rating:", get_average_rating(1))
    
    print("\n" + "=" * 60)
    print("        🎉 DEMONSTRATION COMPLETE SUCCESSFULLY! 🎉        ")
    print("=" * 60)

if __name__ == "__main__":
    main()