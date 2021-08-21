from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.user import save_new_user, get_users_role, get_user_role, update_user, delete_user, get_users
from ..utils.decorators import manage_sysadmin, manage_dev, manage_practice_manager, manage_mp, manage_nmp

bp = Blueprint('User', __name__)
api = Api(bp)


class SysAdminList(Resource):
    @manage_sysadmin
    def get(self):
        return get_users_role('sys_admin')

    @manage_sysadmin
    def post(self):
        return save_new_user('sys_admin', request.json)


class SysAdmin(Resource):
    @manage_sysadmin
    def get(self, id_user):
        return get_user_role('sys_admin', id_user)

    @manage_sysadmin
    def put(self, id_user):
        return update_user('sys_admin', id_user, request.json)

    @manage_sysadmin
    def delete(self, id_user):
        return delete_user('sys_admin', id_user)


api.add_resource(SysAdminList, '/system_admin')
api.add_resource(SysAdmin, '/system_admin/<id_user>')


class DeveloperList(Resource):
    @manage_dev
    def get(self):
        return get_users_role('dev')

    @manage_dev
    def post(self):
        return save_new_user('dev', request.json)


class Developer(Resource):
    @manage_dev
    def get(self, id_user):
        return get_user_role('dev', id_user)

    @manage_dev
    def put(self, id_user):
        return update_user('dev', id_user, request.json)

    @manage_dev
    def delete(self, id_user):
        return delete_user('dev', id_user)


api.add_resource(DeveloperList, '/developer')
api.add_resource(Developer, '/developer/<id_user>')


class PacticeManagerList(Resource):
    @manage_practice_manager
    def get(self, id_group):
        return get_users_role('practice_manager', id_group)

    @manage_practice_manager
    def post(self, id_group):
        return save_new_user('practice_manager', request.json, id_group)


class PacticeManager(Resource):
    @manage_practice_manager
    def get(self, id_user, id_group):
        return get_user_role('practice_manager', id_user, id_group)

    @manage_practice_manager
    def put(self, id_user, id_group):
        return update_user('practice_manager', id_user, request.json, id_group)

    @manage_practice_manager
    def delete(self, id_user, id_group):
        return delete_user('practice_manager', id_user, id_group)


api.add_resource(PacticeManagerList, '/group/<id_group>/practice_manager')
api.add_resource(PacticeManager, '/group/<id_group>/practice_manager/<id_user>')


class MPList(Resource):
    @manage_mp
    def get(self, id_group):
        return get_users_role('mp', id_group)

    @manage_mp
    def post(self, id_group):
        return save_new_user('mp', request.json, id_group)


class MP(Resource):
    @manage_mp
    def get(self, id_user, id_group):
        return get_user_role('mp', id_user, id_group)

    @manage_mp
    def put(self, id_user, id_group):
        return update_user('mp', id_user, request.json, id_group)

    @manage_mp
    def delete(self, id_user, id_group):
        return delete_user('mp', id_user, id_group)


api.add_resource(MPList, '/group/<id_group>/mp')
api.add_resource(MP, '/group/<id_group>/mp/<id_user>')


class NMPList(Resource):
    @manage_nmp
    def get(self, id_group):
        return get_users_role('nmp', id_group)

    @manage_nmp
    def post(self, id_group):
        return save_new_user('nmp', request.json, id_group)


class NMP(Resource):
    @manage_nmp
    def get(self, id_user, id_group):
        return get_user_role('nmp', id_user, id_group)

    @manage_nmp
    def put(self, id_user, id_group):
        return update_user('nmp', id_user, request.json, id_group)

    @manage_nmp
    def delete(self, id_user, id_group):
        return delete_user('nmp', id_user, id_group)


api.add_resource(NMPList, '/group/<id_group>/nmp')
api.add_resource(NMP, '/group/<id_group>/nmp/<id_user>')

