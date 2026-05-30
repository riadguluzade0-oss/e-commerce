def get_featured_products(products):
    result = []
    for p in products:
        if p.is_featured:
            result.append(p)
    return result


def get_trending_products(products):
    result = []
    for p in products:
        if p.is_trending:
            result.append(p)
    return result