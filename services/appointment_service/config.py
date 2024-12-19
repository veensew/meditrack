import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("MONGO_DB_NAME", "meditrack")
    NOTIFICATION_SERVICE_URL = "http://34.134.191.201:8004/api"
    PATIENT_SERVICE_URL = "http://34.60.80.153:8001/api"