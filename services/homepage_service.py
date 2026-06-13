def get_featured_products(products):
    if isinstance(products, dict):
        products = products.values()

    result = []
    for p in products:
        if p.is_featured:
            result.append(p)
    return result


def get_trending_products(products):
    if isinstance(products, dict):
        products = products.values()

    result = []
    for p in products:
        if p.is_trending:
            result.append(p)
    return result
