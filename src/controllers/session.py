from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.session import get_session_treatment, get_sessions_treatment, save_new_session
from ..utils.decorators import run_sesion, session_adjustment

bp = Blueprint('Session', __name__)
api = Api(bp)


class SessionList(Resource):
    def get(self, group_id, patient_id, treatment_id):
        return get_sessions_treatment(group_id, patient_id, treatment_id)

    @run_sesion
    def post(self, group_id, patient_id, treatment_id):
        return save_new_session(group_id, patient_id, treatment_id, request.get_json(force=True))


class Session(Resource):
    def get(self, patient_id, group_id, treatment_id, session_id):
        depth_image = bool(request.args.get('depth_image', False))
        return get_session_treatment(group_id, patient_id, treatment_id, session_id, depth_image)


api.add_resource(SessionList, '/group/<group_id>/patient/<patient_id>/treatment/<treatment_id>/session')
api.add_resource(Session, '/group/<group_id>/patient/<patient_id>/treatment/<treatment_id>/session/<session_id>')
