class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, product, quantity):
        if product.stock < quantity:
            print("❌ Not enough stock")
            return
        
        if product.id in self.items:
            self.items[product.id] += quantity
        else:
            self.items[product.id] = quantity

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]

    def update_quantity(self, product_id, quantity):
        if quantity <= 0:
            self.remove_item(product_id)
        else:
            self.items[product_id] = quantity

    def calculate_total(self, products):
        total = 0
        for product_id, qty in self.items.items():
            product = products[product_id]
            total += product.get_final_price() * qty
        return total