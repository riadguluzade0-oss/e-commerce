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