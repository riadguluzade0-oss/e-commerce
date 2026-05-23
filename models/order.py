import random


class Order:
    def __init__(self, user, items, total):
        self.id = random.randint(1000,9999)
        self.user = user
        self.items = items
        self.total = total
        self.status = "pending"

    def process_payment(self):
        success = random.choice([True, False])

        if success:
            self.status = 'paid'
            print('Payment successful')
        else:
            self.status = 'failed'
            print('Payment failed')

        return success