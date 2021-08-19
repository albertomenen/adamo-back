from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.system import save_new_system, get_systems, get_system

bp = Blueprint('System', __name__)
api = Api(bp)


class SystemList(Resource):
    def get(self):
        return get_systems()

    def post(self):
        return save_new_system(request.json)


class System(Resource):
    def get(self, id_system):
        return get_system(id_system)


api.add_resource(SystemList, '/')
api.add_resource(System, '/<system_id>')
