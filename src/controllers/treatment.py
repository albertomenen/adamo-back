from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.treatment import get_treatment, get_treatments_by_patient, update_treatment, save_new_treatment
from ..utils.decorators import detail_patient, manage_treatment

bp = Blueprint('Treatment', __name__)
api = Api(bp)


class TreatmentList(Resource):
    @detail_patient
    def get(self, group_id, patient_id):
        return get_treatments_by_patient(group_id, patient_id)

    @manage_treatment
    def post(self, group_id, patient_id):
        return save_new_treatment(group_id, patient_id, request.json)


class Treatment(Resource):
    @detail_patient
    def get(self, patient_id, group_id, treatment_id):
        return get_treatment(group_id, patient_id, treatment_id)

    @manage_treatment
    def put(self, patient_id, group_id, treatment_id):
        return update_treatment(group_id, patient_id, treatment_id, request.json)


api.add_resource(TreatmentList, '/group/<group_id>/patient/<patient_id>/treatment')
api.add_resource(Treatment, '/group/<group_id>/patient/<patient_id>/treatment/<treatment_id>')
