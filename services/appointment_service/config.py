import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("MONGO_DB_NAME", "meditrack")
    NOTIFICATION_SERVICE_URL = "http://34.173.55.177:8005"
    PATIENT_SERVICE_URL = "http://35.239.125.65:8001"