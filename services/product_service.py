def get_featured_products(products):
    return [p for p in products.values() if p.is_featured]


def get_trending_products(products):
    return [p for p in products.values() if p.is_trending]


def search_products(products, keyword):
    return [p for p in products.values() if keyword.lower in p.name.lower()]


def filter_by_categories(products, category):
    return [p for p in products.values() if p.category == category]


def sort_by_price(products):
    return sorted(products.values(), key=lambda p: p.price)