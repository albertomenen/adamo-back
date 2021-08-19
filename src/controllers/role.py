from flask import request, Blueprint, make_response
from flask_restful import Resource, Api
from ..services.role import save_new_role, get_role, get_all_roles, delete_role, update_role

bp = Blueprint('role', __name__)
api = Api(bp)


class RoleList(Resource):
    def get(self):
        return get_all_roles()

    def post(self):
        return save_new_role(request.json)


class Role(Resource):
    def get(self, role_id):
        return get_role(role_id)

    def put(self, role_id):
        return update_role(role_id, request.json)

    def delete(self, role_id):
        return delete_role(role_id)


api.add_resource(RoleList, '/')
api.add_resource(Role, '/<role_id>')
