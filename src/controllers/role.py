from flask import request, Blueprint, make_response
from flask_restful import Resource, Api
from ..services.role import save_new_role, get_role, get_all_roles, delete_role, update_role
from ..utils.decorators import manage_roles

bp = Blueprint('role', __name__)
api = Api(bp)


class RoleList(Resource):
    @manage_roles
    def get(self):
        return get_all_roles()

    @manage_roles
    def post(self):
        return save_new_role(request.get_json(force=True))


class Role(Resource):
    @manage_roles
    def get(self, role_id):
        return get_role(role_id)

    @manage_roles
    def put(self, role_id):
        return update_role(role_id, request.get_json(force=True))

    @manage_roles
    def delete(self, role_id):
        return delete_role(role_id)


api.add_resource(RoleList, '/')
api.add_resource(Role, '/<role_id>')
