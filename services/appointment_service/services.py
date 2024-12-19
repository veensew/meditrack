import httpx
from config import Config
from datetime import datetime

async def get_patient_details(patient_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{Config.PATIENT_SERVICE_URL}/patients/{patient_id}")
        return response.json()

async def send_appointment_notification(patient_email, doctor_name, appointment_date, appointment_time):
    notification_data = {
        "recipient_email": patient_email,
        "subject": "Appointment Confirmation",
        "content": f"""
Dear Patient,

Your appointment has been successfully scheduled with Dr. {doctor_name}
for {appointment_date} at {appointment_time}.

Please arrive 15 minutes before your scheduled time.

Best regards,
Health Center Team
        """.strip(),
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{Config.NOTIFICATION_SERVICE_URL}/notifications/send",
                json=notification_data
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send notification: {str(e)}")