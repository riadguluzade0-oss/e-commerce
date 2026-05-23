from models.product import Product
from models.user import User
from models.cart import Cart
from models.order import Order


from services.product_service import get_featured_products, search_products
from services.review_service import add_review, get_average_rating
from utils.notifications import send_notification

products = {
    1: Product(1, "Nike shoes", 120, 10, "Shoes", "NIke"),
    2: Product(2, "Adidas Hoodie", 80, 5, "Clothes", "Adidas"),
    3: Product(3, "Puma T-Shirt", 40, 20, "Clothes", "Puma"),
}

products[1].is_featured = True
products[2].is_trending = True


user = User("holland", "holland@mail.com", "12345678")
cart = Cart()

cart.add_item(products[1], 2)
cart.add_item(products[2], 1)

print("Cart total:", cart.calculate_total(products))


order = Order(user, cart.items, cart.calculate_total(products))

if order.process_payment():
    for product_id, qyt in cart.item.items():
        products[product_id].stock -= qyt

    send_notification("Order confirmed!")
    print("Order completed!")
else:
    print("Payment failed")



add_review(user, 1, 5, "Great product!")
print("Rating:", get_average_rating(1))