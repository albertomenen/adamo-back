import json

from flask import request, Blueprint
from flask_restful import Resource, Api
from ..utils.decorators import manage_patient, detail_patient, list_patient, manage_group
from ..services.patient import save_new_patient, get_patient, delete_patient, update_patient, \
    get_patients_by_group, get_patients

bp = Blueprint('Patient', __name__)
api = Api(bp)


class PatientList(Resource):
    @list_patient
    def get(self, group_id):
        filters = json.loads(request.args.get('filters')) if request.args.get('filters') else []
        return get_patients_by_group(group_id, filters)

    @manage_patient
    def post(self, group_id):
        return save_new_patient(group_id, request.get_json(force=True))


class Patient(Resource):
    @detail_patient
    def get(self, patient_id, group_id):
        return get_patient(group_id, patient_id)

    @manage_patient
    def put(self, patient_id, group_id):
        return update_patient(group_id, patient_id, request.get_json(force=True))

    @manage_patient
    def delete(self, patient_id, group_id):
        return delete_patient(group_id, patient_id)


class PatientManager(Resource):
    @list_patient
    def get(self):
        return get_patients(request)


api.add_resource(PatientList, '/group/<group_id>/patient')
api.add_resource(Patient, '/group/<group_id>/patient/<patient_id>')
api.add_resource(PatientManager, '/patient')
