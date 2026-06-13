class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.favorites = []
        self.wishlist = []

    def check_password(self, password):
        return self.password == password

    def add_favorite(self, product_id):
        if product_id not in self.favorites:
            self.favorites.append(product_id)

    def add_to_wishlist(self, product_id):
        if product_id not in self.wishlist:
            self.wishlist.append(product_id)

    def __repr__(self):
        return f"User(username={self.username!r}, email={self.email!r})"
