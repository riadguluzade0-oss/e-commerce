class Product:
    def __init__(self, id, name, price, description="", stock=0, category="", brand="",
                 is_featured=False, is_trending=False, discount=0, **kwargs):
        self.id = id
        self.name = name
        self.price = price
        
        # Detect if called with 6 positional arguments (old style) lacking description
        # e.g., Product(1, "Nike shoes", 120, 10, "Shoes", "Nike")
        if isinstance(description, int) and brand == "" and category != "":
            self.stock = description
            self.category = stock
            self.brand = category
            self.description = ""
        else:
            self.description = description
            self.stock = stock
            self.category = category
            self.brand = brand

        self.is_featured = is_featured or kwargs.get("is_featured", False)
        self.is_trending = is_trending or kwargs.get("is_trending", False)
        self.discount = discount or kwargs.get("discount", 0)
        self.reviews = []
    
    def get_final_price(self):
        discount_fraction = self.discount / 100.0 if self.discount > 1 else self.discount
        return self.price * (1 - discount_fraction)

    def reduce_stock(self, quantity):
        if self.stock < quantity:
            raise ValueError(f"Not enough stock for {self.name}. Current stock: {self.stock}")
        self.stock -= quantity
        if self.stock <= 3:
            from utils.notifications import send_notification
            send_notification(f"⚠️ LOW STOCK WARNING: '{self.name}' stock is low ({self.stock} remaining)!")

    def average_rating(self):
        if len(self.reviews) == 0:
            return 0
        total = 0
        for r in self.reviews:
            total += r.rating
        return total / len(self.reviews)

    def __repr__(self):
        return f"{self.name} - ${self.price}"


def apply_discount(product, discount_rate):
    """
    Applies a discount rate (e.g., 0.15 for 15%) to a product.
    """
    product.discount = discount_rate

