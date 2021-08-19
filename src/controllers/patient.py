from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.patient import save_new_patient, get_patient, get_patients, delete_patient, update_patient, \
    get_patients_by_group

bp = Blueprint('Patient', __name__)
api = Api(bp)


class PatientList(Resource):
    def get(self):
        return get_patients()

    def post(self):
        return save_new_patient(request.json)


class Patient(Resource):
    def get(self, patient_id):
        return get_patient(patient_id)

    def put(self, patient_id):
        return update_patient(patient_id, request.json)

    def delete(self, patient_id):
        return delete_patient(patient_id)


class PatientGroupList(Resource):
    def get(self, group_id):
        return get_patients_by_group(group_id)


api.add_resource(PatientList, '/patient')
api.add_resource(Patient, '/patient/<patient_id>')
api.add_resource(PatientGroupList, '/group/<group_id>/patient')
