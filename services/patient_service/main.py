from flask import Flask
from flask_restx import Api, Resource, fields
from bson import ObjectId
from database import Database
from dataclasses import dataclass
from typing import List

app = Flask(__name__)
api = Api(app, version='1.0', title='Patient Service API',
          description='A simple Patient Service API',
          doc='/',
          prefix='/api')

# Define namespaces
ns = api.namespace('patients', description='Patient operations')

# Define models for Swagger documentation
patient_model = api.model('Patient', {
    'name': fields.String(required=True, description='Patient name'),
    'age': fields.Integer(required=True, description='Patient age'),
    'gender': fields.String(required=True, description='Patient gender'),
    'email': fields.String(required=True, description='Patient email'),
    'medical_history': fields.List(fields.String, description='Medical history'),
    'prescriptions': fields.List(fields.String, description='Prescriptions')
})

patient_response = api.model('PatientResponse', {
    'id': fields.String(description='Patient ID'),
    'name': fields.String(description='Patient name'),
    'age': fields.Integer(description='Patient age'),
    'gender': fields.String(description='Patient gender'),
    'email': fields.String(description='Patient email'),
    'medical_history': fields.List(fields.String, description='Medical history'),
    'prescriptions': fields.List(fields.String, description='Prescriptions')
})

db = Database()

@dataclass
class Patient:
    name: str
    age: int
    gender: str
    email: str
    medical_history: List[str] = None
    prescriptions: List[str] = None

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "email": self.email,
            "medical_history": self.medical_history or [],
            "prescriptions": self.prescriptions or []
        }

def validate_object_id(object_id: str):
    try:
        return ObjectId(object_id)
    except:
        return None

@ns.route('/')
class PatientList(Resource):
    @ns.expect(patient_model)
    @ns.response(201, 'Patient successfully created')
    @ns.response(400, 'Invalid input')
    def post(self):
        """Create a new patient"""
        try:
            patient = Patient(**api.payload)
            result = db.insert_patient(patient.to_dict())
            return {"id": str(result.inserted_id)}, 201
        except Exception as e:
            api.abort(400, str(e))

@ns.route('/<string:patient_id>')
@ns.param('patient_id', 'The patient identifier')
class PatientItem(Resource):
    @ns.response(200, 'Success', patient_response)
    @ns.response(400, 'Invalid ID format')
    @ns.response(404, 'Patient not found')
    def get(self, patient_id):
        """Get a patient by ID"""
        object_id = validate_object_id(patient_id)
        if not object_id:
            api.abort(400, "Invalid ID format")

        patient = db.find_patient(object_id)
        if not patient:
            api.abort(404, "Patient not found")

        patient["id"] = str(patient.pop("_id"))
        return patient

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=True)