from pymongo import MongoClient
from config import Config

class MongoDB:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URL)
        self.db = self.client[Config.DB_NAME]
        self.notification_collection = self.db.notifications

    def insert_notification(self, notification_data):
        return self.notification_collection.insert_one(notification_data)

    def update_notification_status(self, notification_id, status, sent_at=None):
        update_data = {"status": status}
        if sent_at:
            update_data["sent_at"] = sent_at
        return self.notification_collection.update_one(
            {"id": notification_id},
            {"$set": update_data}
        )

    def get_pending_notifications(self):
        return list(self.notification_collection.find({"status": "pending"}))