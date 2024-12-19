from flask import Flask,jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from models import Doctor, Appointment
from database import MongoDB
from services import get_patient_details, send_appointment_notification
from bson.objectid import ObjectId
from bson.errors import InvalidId
import asyncio
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

# Initialize Flask-RestX
api = Api(app, version='1.0',
          title='Health Service API',
          description='Combined Health Service API for Doctors and Appointments',
          doc='/',
          prefix='/api')

# Create namespaces
doctors_ns = api.namespace('doctors', description='Doctor operations')
appointments_ns = api.namespace('appointments', description='Appointment operations')

# Define models for Swagger documentation
doctor_model = api.model('Doctor', {
    'name': fields.String(required=True, description='Doctor name'),
    'specialty': fields.String(required=True, description='Doctor specialty'),
    'available_slots': fields.List(fields.String, description='Available time slots')
})

slots_update_model = api.model('SlotsUpdate', {
    'available_slots': fields.List(fields.String, required=True, description='Updated available time slots')
})

appointment_model = api.model('Appointment', {
    'patient_id': fields.String(required=True, description='Patient ID'),
    'doctor_id': fields.String(required=True, description='Doctor ID'),
    'date': fields.String(required=True, description='Appointment date'),
    'time': fields.String(required=True, description='Appointment time'),
    'symptoms': fields.List(fields.String, description='List of symptoms')
})

db = MongoDB()

def validate_object_id(id_str):
    try:
        return ObjectId(id_str)
    except InvalidId:
        return None

# Doctor endpoints
@doctors_ns.route('/')
class DoctorList(Resource):
    @doctors_ns.expect(doctor_model)
    @doctors_ns.response(201, 'Doctor successfully created')
    @doctors_ns.response(400, 'Invalid input')
    def post(self):
        """Create a new doctor"""
        try:
            doctor = Doctor(**api.payload)
            result = db.add_doctor(doctor.to_dict())
            return {"id": str(result.inserted_id)}, 201
        except Exception as e:
            api.abort(400, str(e))

@doctors_ns.route('/<string:doctor_id>')
@doctors_ns.param('doctor_id', 'The doctor identifier')
class DoctorItem(Resource):
    @doctors_ns.response(200, 'Success')
    @doctors_ns.response(400, 'Invalid ID format')
    @doctors_ns.response(404, 'Doctor not found')
    def get(self, doctor_id):
        """Get a doctor by ID"""
        object_id = validate_object_id(doctor_id)
        if not object_id:
            api.abort(400, "Invalid doctor ID")

        doctor = db.get_doctor(doctor_id)
        if not doctor:
            api.abort(404, "Doctor not found")

        doctor['id'] = str(doctor.pop('_id'))
        return doctor

    @doctors_ns.expect(slots_update_model)
    @doctors_ns.response(200, 'Slots successfully updated')
    @doctors_ns.response(400, 'Invalid ID format')
    @doctors_ns.response(404, 'Doctor not found')
    def put(self, doctor_id):
        """Update doctor's available slots"""
        if not validate_object_id(doctor_id):
            api.abort(400, "Invalid doctor ID")

        result = db.update_doctor_slots(doctor_id, api.payload['available_slots'])

        if result.matched_count == 0:
            api.abort(404, "Doctor not found")

        return {"detail": "Slots updated"}

# Appointment endpoints
@appointments_ns.route('/')
class AppointmentResource(Resource):
    @appointments_ns.expect(appointment_model)
    @appointments_ns.response(201, 'Appointment successfully created')
    @appointments_ns.response(400, 'Invalid input')
    def post(self):
        """Schedule a new appointment"""
        try:
            data = api.payload
            appointment = Appointment(**data)

            # Validate doctor exists
            doctor = db.get_doctor(appointment.doctor_id)
            if not doctor:
                api.abort(404, "Doctor not found")

            # Create event loop for async operations
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Get patient details
            try:
                patient = loop.run_until_complete(get_patient_details(appointment.patient_id))
            except Exception as e:
                loop.close()
                api.abort(404, "Patient not found")

            # Save appointment
            result = db.create_appointment(appointment.to_dict())

            # Send notification asynchronously
            loop.run_until_complete(
                send_appointment_notification(
                    patient.get("email", ""),
                    doctor.get("name", ""),
                    appointment.date,
                    appointment.time
                )
            )

            loop.close()

            return {"id": str(result.inserted_id)}, 201
        except Exception as e:
            return {"error": str(e)}, 400

@app.route('/health', methods=['GET'])
def health_check():
    try:
        service_status = "healthy"

        if service_status == "healthy":
            return jsonify({"status": "healthy"}), 200
        else:
            return jsonify({"status": "unhealthy"}), 500

    except Exception as e:
        # If any error occurs, return unhealthy status
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8003, debug=True)