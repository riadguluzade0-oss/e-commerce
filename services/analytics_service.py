def calculate_analytics(orders, products):
    """
    Calculates total sales and the most popular product across successful orders.
    Successful orders are those with status 'paid' or 'completed'.
    """
    total_sales = 0
    product_sales_qty = {}

    for order in orders:
        if order.status in ["paid", "completed"]:
            total_sales += order.total
            for pid_str, qty in order.items.items():
                pid = int(pid_str)
                product_sales_qty[pid] = product_sales_qty.get(pid, 0) + qty

    most_popular_product_name = "None"
    max_qty = 0
    if product_sales_qty:
        most_popular_pid = max(product_sales_qty, key=product_sales_qty.get)
        max_qty = product_sales_qty[most_popular_pid]
        product = products.get(most_popular_pid)
        if product:
            most_popular_product_name = product.name
        else:
            most_popular_product_name = f"Product ID {most_popular_pid}"

    return {
        "total_sales": total_sales,
        "most_popular_product": most_popular_product_name,
        "units_sold": max_qty
    }

def print_analytics_dashboard(orders, products):
    analytics = calculate_analytics(orders, products)
    print("\n" + "=" * 40)
    print("        📊 ANALYTICS DASHBOARD        ")
    print("=" * 40)
    print(f"Total Sales:            ${analytics['total_sales']:.2f}")
    print(f"Most Popular Product:   {analytics['most_popular_product']}")
    print(f"Units Sold (Popular):   {analytics['units_sold']}")
    print("=" * 40 + "\n")
