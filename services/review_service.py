from services.storage_service import add_review_row, load_review_rows


class Review:
    def __init__(self, user, product_id, rating, comment):
        self.user = user
        self.product_id = product_id
        self.rating = rating
        self.comment = comment


reviews = []


def load_reviews():
    global reviews
    reviews = [
        Review(row["user"], row["product_id"], row["rating"], row["comment"])
        for row in load_review_rows()
    ]


def add_review(user, product_id, rating, comment):
    review = Review(user, product_id, rating, comment)
    reviews.append(review)
    add_review_row(user, product_id, rating, comment)


def get_average_rating(product_id):
    product_reviews = [r.rating for r in reviews if r.product_id == product_id]
    return sum(product_reviews) / len(product_reviews) if product_reviews else 0


load_reviews()
