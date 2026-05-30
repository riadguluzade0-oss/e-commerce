class Cart:
    def __init__(self):
        self.items = {}
        self.promo_code = None

    def add_item(self, product, quantity):
        if quantity <= 0:
            print("❌ Quantity must be greater than zero.")
            return False
            
        current_in_cart = self.items.get(product.id, 0)
        new_total_quantity = current_in_cart + quantity
        
        if product.stock == 0:
            print(f"❌ '{product.name}' is out of stock.")
            return False
            
        if product.stock < new_total_quantity:
            print(f"❌ Cannot add {quantity} of '{product.name}'. Total in cart ({new_total_quantity}) would exceed available stock ({product.stock}).")
            return False
        
        self.items[product.id] = new_total_quantity
        return True

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]

    def update_quantity(self, product_id, quantity):
        if quantity <= 0:
            self.remove_item(product_id)
        else:
            self.items[product_id] = quantity

    def apply_promo_code(self, promo_code):
        valid_promos = {
            "SAVE10": 0.10,
            "SUPER50": 0.50
        }
        if promo_code in valid_promos:
            self.promo_code = promo_code
            print(f"Promo code '{promo_code}' applied successfully!")
            return True
        else:
            print(f"❌ Invalid promo code '{promo_code}'")
            return False

    def calculate_total(self, products):
        total = 0
        for product_id, qty in self.items.items():
            product = products[product_id]
            total += product.get_final_price() * qty
        
        if self.promo_code == "SAVE10":
            total *= 0.90
        elif self.promo_code == "SUPER50":
            total *= 0.50
            
        return total