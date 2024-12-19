from pymongo import MongoClient
from config import Config
from bson import ObjectId

class MongoDB:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URL)
        self.db = self.client[Config.DB_NAME]
        self.doctors = self.db.doctors
        self.appointments = self.db.appointments

    # Doctor operations
    def add_doctor(self, doctor_data):
        return self.doctors.insert_one(doctor_data)

    def get_doctor(self, doctor_id):
        return self.doctors.find_one({"_id": ObjectId(doctor_id)})

    def update_doctor_slots(self, doctor_id, slots):
        return self.doctors.update_one(
            {"_id": ObjectId(doctor_id)},
            {"$set": {"available_slots": slots}}
        )

    # Appointment operations
    def create_appointment(self, appointment_data):
        return self.appointments.insert_one(appointment_data)

    def get_appointment(self, appointment_id):
        return self.appointments.find_one({"_id": ObjectId(appointment_id)})