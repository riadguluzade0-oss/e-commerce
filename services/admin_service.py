PRODUCTS = []

def add_product(product):
    PRODUCTS.append(product)


def edit_product(product_id, **kwargs):
    for p in PRODUCTS:
        if p.id == product_id:
            for key, value in kwargs.items():
                setattr(p, key, value)
            return p
    return None


def delete_product(product_id):
    global PRODUCTS
    PRODUCTS = [p for p in PRODUCTS if p.id != product_id]