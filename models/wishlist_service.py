def add_to_wishlist(user, product):
    product_id = getattr(product, "id", product)
    if product_id not in user.wishlist:
        user.wishlist.append(product_id)
        print("Added to wishlist!")
        return True
    else:
        print("Already in wishlist.")
        return False


def show_wishlist(user, products=None):
    print("Wishlist:")
    if not user.wishlist:
        print("Your wishlist is empty.")
        return

    for product_id in user.wishlist:
        product = products.get(product_id) if products else None
        print(product if product else product_id)

def handle_buy_or_wishlist(user, product):
    print(f"You selected: {product.name}")

    choice = input("Add to wishlist? (y/n): ")

    if choice.lower() == "y":
        add_to_wishlist(user, product)
    else:
        print("Continuing...")
