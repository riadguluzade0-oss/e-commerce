def advanced_search(products, keyword=None):
    result = []

    for p in products:
        if keyword is None or keyword.lower() in p.name.lower():
            result.append(p)

    return result