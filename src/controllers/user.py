from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.user import save_new_user, get_users_role, get_user_role, update_user, delete_user

bp = Blueprint('user', __name__)
api = Api(bp)


class SysAdminList(Resource):
    def get(self):
        return get_users_role('sys_admin')

    def post(self):
        return save_new_user('sys_admin', request.json)


class SysAdmin(Resource):
    def get(self, id_user):
        return get_user_role('sys_admin', id_user)

    def put(self, id_user):
        return update_user('sys_admin', id_user, request.json)

    def delete(self, id_user):
        return delete_user('sys_admin', id_user)


api.add_resource(SysAdminList, '/system_admin')
api.add_resource(SysAdmin, '/system_admin/<id_user>')


class DeveloperList(Resource):
    def get(self):
        return get_users_role('dev')

    def post(self):
        return save_new_user('dev', request.json)


class Developer(Resource):
    def get(self, id_user):
        return get_user_role('dev', id_user)

    def put(self, id_user):
        return update_user('dev', id_user, request.json)

    def delete(self, id_user):
        return delete_user('dev', id_user)


api.add_resource(DeveloperList, '/developer')
api.add_resource(Developer, '/developer/<id_user>')


class PacticeManagerList(Resource):
    def get(self, id_group):
        return get_users_role('practice_manager', id_group)

    def post(self, id_group):
        return save_new_user('practice_manager', request.json, id_group)


class PacticeManager(Resource):
    def get(self, id_user, id_group):
        return get_user_role('practice_manager', id_user, id_group)

    def put(self, id_user, id_group):
        return update_user('practice_manager', id_user, request.json, id_group)

    def delete(self, id_user, id_group):
        return delete_user('practice_manager', id_user, id_group)


api.add_resource(PacticeManagerList, '/group/<id_group>/practice_manager')
api.add_resource(PacticeManager, '/group/<id_group>/practice_manager/<id_user>')


class MPList(Resource):
    def get(self, id_group):
        return get_users_role('mp', id_group)

    def post(self, id_group):
        return save_new_user('mp', request.json, id_group)


class MP(Resource):
    def get(self, id_user, id_group):
        return get_user_role('mp', id_user, id_group)

    def put(self, id_user, id_group):
        return update_user('mp', id_user, request.json, id_group)

    def delete(self, id_user, id_group):
        return delete_user('mp', id_user, id_group)


api.add_resource(MPList, '/group/<id_group>/mp')
api.add_resource(MP, '/group/<id_group>/mp/<id_user>')


class NMPList(Resource):
    def get(self, id_group):
        return get_users_role('nmp', id_group)

    def post(self, id_group):
        return save_new_user('nmp', request.json, id_group)


class NMP(Resource):
    def get(self, id_user, id_group):
        return get_user_role('nmp', id_user, id_group)

    def put(self, id_user, id_group):
        return update_user('nmp', id_user, request.json, id_group)

    def delete(self, id_user, id_group):
        return delete_user('nmp', id_user, id_group)


api.add_resource(NMPList, '/group/<id_group>/nmp')
api.add_resource(NMP, '/group/<id_group>/nmp/<id_user>')
