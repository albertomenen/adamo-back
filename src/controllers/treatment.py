from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.treatment import get_treatment, get_treatments_by_patient, update_treatment, save_new_treatment, \
    delete_treatment, get_treatment_offset
from ..utils.decorators import detail_patient, manage_treatment, run_sesion

bp = Blueprint('Treatment', __name__)
api = Api(bp)


class TreatmentList(Resource):
    @detail_patient
    def get(self, group_id, patient_id):
        return get_treatments_by_patient(group_id, patient_id)

    @manage_treatment
    def post(self, group_id, patient_id):
        return save_new_treatment(group_id, patient_id, request.get_json(force=True))


class Treatment(Resource):
    @detail_patient
    def get(self, patient_id, group_id, treatment_id):
        return get_treatment(group_id, patient_id, treatment_id)

    @manage_treatment
    def put(self, patient_id, group_id, treatment_id):
        return update_treatment(group_id, patient_id, treatment_id, request.get_json(force=True))

    @manage_treatment
    def delete(self, patient_id, group_id, treatment_id):
        return delete_treatment(group_id, patient_id, treatment_id)


class TreatmentOffset(Resource):
    @run_sesion
    def get(self, group_id, patient_id, treatment_id):
        return get_treatment_offset(group_id, patient_id, treatment_id, request.get_json(force=True))


api.add_resource(TreatmentList, '/group/<group_id>/patient/<patient_id>/treatment')
api.add_resource(Treatment, '/group/<group_id>/patient/<patient_id>/treatment/<treatment_id>')
api.add_resource(TreatmentOffset, '/group/<group_id>/patient/<patient_id>/treatment/<treatment_id>/offset')
