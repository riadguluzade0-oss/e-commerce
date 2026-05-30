import random


class Order:
    def __init__(self, user, items, total):
        self.id = random.randint(1000,9999)
        self.user = user
        self.items = items
        self.total = total
        self.status = "pending"
        self.delivery_status = "pending"

    def process_payment(self):
        success = random.choice([True, False])

        if success:
            self.status = 'paid'
            print('Payment successful')
        else:
            self.status = 'failed'
            print('Payment failed')

        return success

    def update_delivery_status(self, new_status):
        valid_statuses = ["pending", "shipped", "delivered"]
        if new_status not in valid_statuses:
            print(f"❌ Invalid delivery status: {new_status}")
            return False
        
        self.delivery_status = new_status
        from utils.notifications import send_notification
        send_notification(f"Order #{self.id} delivery status updated to: {new_status}")
        
        # If order reaches delivered, mark overall order status as completed
        if new_status == "delivered":
            self.status = "completed"
            send_notification(f"Order #{self.id} has been successfully completed!")
        
        return True