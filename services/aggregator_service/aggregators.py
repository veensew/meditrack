from datetime import datetime
from bson import ObjectId
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DataAggregators:
    def __init__(self, mongo_db):
        self.mongo_db = mongo_db

    def aggregate_doctor_appointments(self) -> List[Dict]:
        pipeline = [
            {
                "$group": {
                    "_id": "$doctor_id",
                    "appointment_count": {"$sum": 1}
                }
            }
        ]

        try:
            appointments_result = list(self.mongo_db.appointments.aggregate(pipeline))
            aggregated_data = []

            for appointment in appointments_result:
                doctor_id = appointment["_id"]
                doctor = self.mongo_db.doctors.find_one({"_id": ObjectId(doctor_id)})

                aggregated_data.append({
                    "doctor_id": str(doctor_id),
                    "doctor_name": doctor.get("name", "Unknown") if doctor else "Unknown",
                    "specialty": doctor.get("specialty", "Unknown") if doctor else "Unknown",
                    "appointment_count": appointment["appointment_count"]
                })

            return aggregated_data
        except Exception as e:
            logger.error(f"Doctor appointments aggregation failed: {str(e)}")
            raise

    def aggregate_appointment_frequency(self) -> List[Dict]:
        pipeline = [
            {
                "$group": {
                    "_id": "$date",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]

        try:
            result = list(self.mongo_db.appointments.aggregate(pipeline))
            return [
                {
                    "date": r["_id"],
                    "appointment_count": r["count"]
                }
                for r in result
            ]
        except Exception as e:
            logger.error(f"Appointment frequency aggregation failed: {str(e)}")
            raise

    def aggregate_symptoms_by_specialty(self) -> List[Dict]:
        pipeline = [
            {
                "$addFields": {
                    "doctor_object_id": {"$toObjectId": "$doctor_id"}
                }
            },
            {
                "$lookup": {
                    "from": "doctors",
                    "localField": "doctor_object_id",
                    "foreignField": "_id",
                    "as": "doctor_info"
                }
            },
            {"$unwind": "$doctor_info"},
            {"$unwind": "$symptoms"},
            {
                "$group": {
                    "_id": {
                        "specialty": "$doctor_info.specialty",
                        "symptom": "$symptoms"
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}},
            {
                "$project": {
                    "_id": 0,
                    "specialty": "$_id.specialty",
                    "symptom": "$_id.symptom",
                    "occurrence_count": "$count"
                }
            }
        ]

        try:
            return list(self.mongo_db.appointments.aggregate(pipeline))
        except Exception as e:
            logger.error(f"Symptoms by specialty aggregation failed: {str(e)}")
            raise