class Product:
    def __init__(self, id, name, price, description, stock, category, brand,
                 is_featured=False, is_trending=False, discount=0):
        
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock
        self.category = category
        self.brand = brand

        self.is_featured = is_featured
        self.is_trending = is_trending
        self.discount = discount

        self.reviews = []

    def average_rating(self):
        if len(self.reviews) == 0:
            return 0
        total = 0
        for r in self.reviews:
            total += r.rating
        return total / len(self.reviews)

    def __repr__(self):
        return f"{self.name} - ${self.price}"