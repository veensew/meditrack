from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Doctor:
    name: str
    specialty: str
    available_slots: Optional[List[str]] = None

    def to_dict(self):
        return {
            "name": self.name,
            "specialty": self.specialty,
            "available_slots": self.available_slots or []
        }

@dataclass
class Appointment:
    patient_id: str
    doctor_id: str
    date: str
    time: str
    symptoms: List[str]

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.date,
            "time": self.time,
            "symptoms": self.symptoms
        }