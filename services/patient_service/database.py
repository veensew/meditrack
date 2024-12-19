from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
        self.DB_NAME = os.getenv("MONGO_DB_NAME", "meditrack")
        self.client = MongoClient(self.MONGO_URL)
        self.db = self.client[self.DB_NAME]
        self.patients_collection = self.db["patients"]

    def insert_patient(self, patient_data):
        return self.patients_collection.insert_one(patient_data)

    def find_patient(self, patient_id):
        return self.patients_collection.find_one({"_id": patient_id})