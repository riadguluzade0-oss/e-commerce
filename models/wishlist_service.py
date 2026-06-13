def add_to_wishlist(user, product):
    if product not in user.wishlist:
        user.wishlist.append(product)
        print("Added to wishlist!")
    else:
        print("Already in wishlist.")


def show_wishlist(user):
    print("Wishlist:")
    for p in user.wishlist:
        print(p)

def handle_buy_or_wishlist(user, product):
    print(f"You selected: {product.name}")

    choice = input("Add to wishlist? (y/n): ")

    if choice.lower() == "y":
        add_to_wishlist(user, product)
    else:
        print("Continuing...")
