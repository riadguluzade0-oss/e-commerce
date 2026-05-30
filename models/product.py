class Product:
    def __init__(self, id, name, price, stock, category, brand):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
        self.brand = brand
        self.featured = False
        self.trending = False
        self.discount = 0
    
    def get_final_price(self):
        return self.price * (1 - self.discount)

    def reduce_stock(self, quantity):
        if self.stock < quantity:
            raise ValueError(f"Not enough stock for {self.name}. Current stock: {self.stock}")
        self.stock -= quantity
        if self.stock <= 3:
            from utils.notifications import send_notification
            send_notification(f"⚠️ LOW STOCK WARNING: '{self.name}' stock is low ({self.stock} remaining)!")



def apply_discount(product, discount_rate):
    """
    Applies a discount rate (e.g., 0.15 for 15%) to a product.
    """
    product.discount = discount_rate