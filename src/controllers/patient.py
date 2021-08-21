from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.patient import save_new_patient, get_patient, get_patients, delete_patient, update_patient, \
    get_patients_by_group

bp = Blueprint('Patient', __name__)
api = Api(bp)


class PatientList(Resource):
    def get(self, group_id):
        return get_patients_by_group(group_id)

    def post(self, group_id):
        return save_new_patient(group_id, request.json)


class Patient(Resource):
    def get(self, patient_id, group_id):
        return get_patient(group_id, patient_id)

    def put(self, patient_id, group_id):
        return update_patient(group_id, patient_id, request.json)

    def delete(self, patient_id, group_id):
        return delete_patient(group_id, patient_id)


api.add_resource(PatientList, '/group/<group_id>/patient')
api.add_resource(Patient, '/group/<group_id>/patient/<patient_id>')
