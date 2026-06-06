import os
import json

class Review:
    def __init__(self, user, product_id, rating, comment):
        self.user = user
        self.product_id = product_id
        self.rating = rating
        self.comment = comment

reviews = []

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
REVIEWS_FILE = os.path.join(DATA_DIR, "reviews.json")

def save_reviews():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    data = []
    for r in reviews:
        data.append({
            "user": r.user,
            "product_id": r.product_id,
            "rating": r.rating,
            "comment": r.comment
        })
    with open(REVIEWS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_reviews():
    global reviews
    if not os.path.exists(REVIEWS_FILE):
        reviews = []
        return
    try:
        with open(REVIEWS_FILE, "r") as f:
            data = json.load(f)
        reviews = []
        for rdata in data:
            reviews.append(Review(
                rdata["user"],
                rdata["product_id"],
                rdata["rating"],
                rdata["comment"]
            ))
    except Exception:
        reviews = []

def add_review(user, product_id, rating, comment):
    reviews.append(Review(user, product_id, rating, comment))
    save_reviews()

def get_average_rating(product_id):
    product_reviews = [r.rating for r in reviews if r.product_id == product_id]
    return sum(product_reviews) / len(product_reviews) if product_reviews else 0

# Load reviews automatically when the module is imported
load_reviews()