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

def display_catalog(products):
    print("\n" + "=" * 80)
    print("                      🛍️  CURRENT PRODUCT CATALOG  🛍️")
    print("=" * 80)
    print(f"{'ID':<4} | {'Product Name':<18} | {'Orig Price':<10} | {'Final Price':<11} | {'Stock':<6} | {'Brand':<10} | {'Category'}")
    print("-" * 80)
    for pid, p in products.items():
        final_price_str = f"${p.get_final_price():.2f}"
        orig_price_str = f"${p.price:.2f}"
        
        # Add labels for special attributes
        labels = []
        if p.is_featured:
            labels.append("⭐ Featured")
        if p.is_trending:
            labels.append("🔥 Trending")
        if p.stock <= 3:
            labels.append("⚠️ Low Stock")
        
        label_str = f" ({', '.join(labels)})" if labels else ""
        discount_badge = f" [-{p.discount*100:.0f}%]" if p.discount > 0 else ""
        
        name_with_badge = f"{p.name}{discount_badge}"
        print(f"{p.id:<4} | {name_with_badge:<18} | {orig_price_str:<10} | {final_price_str:<11} | {p.stock:<6} | {p.brand:<10} | {p.category}{label_str}")
    print("=" * 80 + "\n")

def view_cart(cart, products):
    if not cart.items:
        print("\n🛒 Your shopping cart is empty!\n")
        return False
        
    print("\n" + "=" * 60)
    print("                      🛒 YOUR SHOPPING CART")
    print("=" * 60)
    print(f"{'ID':<4} | {'Product Name':<18} | {'Qty':<4} | {'Unit Price':<10} | {'Subtotal'}")
    print("-" * 60)
    for pid, qty in cart.items.items():
        p = products[pid]
        unit_price_str = f"${p.get_final_price():.2f}"
        subtotal = p.get_final_price() * qty
        print(f"{p.id:<4} | {p.name:<18} | {qty:<4} | {unit_price_str:<10} | ${subtotal:.2f}")
    
    print("-" * 60)
    total = cart.calculate_total(products)
    if cart.promo_code:
        print(f"Promo Code Applied: '{cart.promo_code}'")
    print(f"Total Cart Value:  ${total:.2f}")
    print("=" * 60 + "\n")
    return True

def main():
    try:
        print("=" * 60)
        print("        🚀 WELCOME TO THE INTERACTIVE E-COMMERCE ENGINE 🚀        ")
        print("=" * 60)

        # Load databases
        products = load_products()
        users = load_users()
        orders = load_orders(users)
        
        print(f"Database successfully loaded: {len(products)} products, {len(users)} users, and {len(orders)} historical orders.")

        # Get user session
        username_input = input("\nEnter your username (Press Enter for guest session 'holland'): ").strip()
        username = username_input if username_input else "holland"
        
        user = users.get(username)
        if not user:
            print(f"👤 Creating new customer profile for '{username}'...")
            user = User(username, f"{username}@mail.com", "12345678")
            users[username] = user
            save_users(users)
        
        print(f"👋 Welcome, {user.username}! Happy shopping!")
        
        cart = Cart()

        while True:
            print("\n" + "—" * 50)
            print("💻 MAIN MENU:")
            print("1. 🛍️  Browse Product Catalog")
            print("2. ➕ Add Product to Cart")
            print("3. 🛒 View Shopping Cart & Apply Promo Code")
            print("4. 💳 Checkout & Process Order")
            print("5. ⭐ Leave a Product Review")
            print("6. 📊 View Store Analytics Dashboard")
            print("7. 🚪 Save and Exit")
            print("—" * 50)
            
            choice = input("Select an option (1-7): ").strip()
            
            if choice == "1":
                display_catalog(products)
                
            elif choice == "2":
                display_catalog(products)
                try:
                    pid_input = input("Enter the Product ID to add: ").strip()
                    if not pid_input:
                        continue
                    pid = int(pid_input)
                    
                    if pid not in products:
                        print("❌ Product ID not found in catalog.")
                        continue
                    
                    qty_input = input(f"How many units of '{products[pid].name}' would you like? ").strip()
                    if not qty_input:
                        continue
                    qty = int(qty_input)
                    
                    # Try adding to cart
                    if cart.add_item(products[pid], qty):
                        print(f"✅ Added {qty}x '{products[pid].name}' to your cart.")
                except ValueError:
                    print("❌ Invalid input. Please enter valid integer values.")
                    
            elif choice == "3":
                if view_cart(cart, products):
                    promo_choice = input("Would you like to apply a promo code? (y/n): ").strip().lower()
                    if promo_choice == "y":
                        code = input("Enter Promo Code (e.g. SAVE10, SUPER50): ").strip()
                        cart.apply_promo_code(code)
                        view_cart(cart, products)
                        
            elif choice == "4":
                if not cart.items:
                    print("❌ Your cart is empty. Add products before checking out!")
                    continue
                    
                view_cart(cart, products)
                checkout_choice = input("Proceed to Payment & Checkout? (y/n): ").strip().lower()
                if checkout_choice != "y":
                    print("Checkout cancelled.")
                    continue
                    
                # Create Order
                total = cart.calculate_total(products)
                order = Order(user, cart.items.copy(), total)
                
                print("\n💳 Processing payment...")
                if order.process_payment():
                    # Success! Deduct stock cleanly
                    for pid, qty in cart.items.items():
                        products[pid].reduce_stock(qty)
                    
                    orders.append(order)
                    
                    # Delivery simulation flow
                    print("\n--- 📦 Delivery Stage Transitions ---")
                    print(f"Initial delivery status: {order.delivery_status}")
                    print("Transitioning to 'shipped'...")
                    order.update_delivery_status("shipped")
                    print("Transitioning to 'delivered'...")
                    order.update_delivery_status("delivered")
                    print(f"Final order status: {order.status} | Final delivery status: {order.delivery_status}")
                    
                    # Persist state
                    print("\n--- 💾 Persisting Updated State to Storage ---")
                    save_products(products)
                    save_users(users)
                    save_orders(orders)
                    print("Data saved successfully to JSON files.")
                    
                    # Confirmation
                    send_notification(f"Order #{order.id} confirmed and successfully processed!")
                    print("\n🎉 Purchase Complete! Thank you for shopping with us!")
                    
                    # Clear cart
                    cart = Cart()
                else:
                    print("❌ Checkout failed due to payment issues. Please try again.")
                    
            elif choice == "5":
                display_catalog(products)
                try:
                    pid_input = input("Enter the Product ID you want to review: ").strip()
                    if not pid_input:
                        continue
                    pid = int(pid_input)
                    
                    if pid not in products:
                        print("❌ Product ID not found in catalog.")
                        continue
                    
                    rating_input = input("Enter rating (1-5 stars): ").strip()
                    if not rating_input:
                        continue
                    rating = int(rating_input)
                    if rating < 1 or rating > 5:
                        print("❌ Rating must be between 1 and 5.")
                        continue
                        
                    comment = input("Write your comment: ").strip()
                    
                    # Add review
                    add_review(user.username, pid, rating, comment)
                    print(f"✅ Thank you! Review added for '{products[pid].name}'.")
                    print(f"New average rating: {get_average_rating(pid):.1f} ⭐")
                except ValueError:
                    print("❌ Invalid input. Rating and Product ID must be integers.")
                    
            elif choice == "6":
                print_analytics_dashboard(orders, products)
                
            elif choice == "7":
                print("\n💾 Saving session details...")
                save_products(products)
                save_users(users)
                save_orders(orders)
                print("👋 Thank you for shopping with us! Goodbye!")
                break
            else:
                print("❌ Invalid option. Please enter a number between 1 and 7.")
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Program interrupted. Saving session and exiting gracefully... Goodbye!")
        try:
            save_products(products)
            save_users(users)
            save_orders(orders)
        except Exception:
            pass

if __name__ == "__main__":
    main()
