import json

from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.user import save_new_user, get_users_role, get_user_role, update_user, delete_user, get_users, \
    set_password, check_user_code, change_password, prueba_email
from ..utils.decorators import manage_sys_admin, manage_dev, manage_practice_manager, manage_mp, manage_nmp, \
    manage_treatment, list_patient, token_required

bp = Blueprint('User', __name__)
api = Api(bp)


class Users(Resource):
    @token_required
    def get(self):
        filters = json.loads(request.args.get('filters')) if request.args.get('filters') else []
        return get_users(request, filters)


api.add_resource(Users, '/users')


class HandlePasswordResource(Resource):
    def put(self, k):
        password = request.get_json(force=True).get('password')
        return set_password(k, password)

    def get(self, k):
        return check_user_code(k)


class RecoverPassword(Resource):
    def get(self):
        email = request.args.get('email')
        return change_password(email)


class Prueba(Resource):
    def get(self):
        return prueba_email()

api.add_resource(Prueba, '/prueba')


api.add_resource(HandlePasswordResource, '/user_pass/<k>')
api.add_resource(RecoverPassword, '/recover_pass')


class SysAdminList(Resource):
    @manage_sys_admin
    def get(self):
        return get_users_role('sys_admin')

    @manage_sys_admin
    def post(self):
        return save_new_user('sys_admin', request.get_json(force=True))


class SysAdmin(Resource):
    @manage_sys_admin
    def get(self, id_user):
        return get_user_role('sys_admin', id_user)

    @manage_sys_admin
    def put(self, id_user):
        return update_user('sys_admin', id_user, request.get_json(force=True))

    @manage_sys_admin
    def delete(self, id_user):
        return delete_user('sys_admin', id_user)


api.add_resource(SysAdminList, '/system_admin')
api.add_resource(SysAdmin, '/system_admin/<id_user>')


# class PacticeManagerSetTimetable(Resource):
#     def put(self, id_user, id_group, id_location):
#         id_timetable = request.get_json(force=True).get('id_timetable')
#         return set_user_timetable(id_user, id_group, id_location, id_timetable)
#
#
# api.add_resource(PacticeManagerSetTimetable, '/group/<id_group>/location/<id_location>/medic/<id_user>/set_timetable')


class DeveloperList(Resource):
    @manage_dev
    def get(self):
        return get_users_role('dev')

    @manage_dev
    def post(self):
        return save_new_user('dev', request.get_json(force=True))


class Developer(Resource):
    @manage_dev
    def get(self, id_user):
        return get_user_role('dev', id_user)

    @manage_dev
    def put(self, id_user):
        return update_user('dev', id_user, request.get_json(force=True))

    @manage_dev
    def delete(self, id_user):
        return delete_user('dev', id_user)


api.add_resource(DeveloperList, '/developer')
api.add_resource(Developer, '/developer/<id_user>')


class PacticeManagerList(Resource):
    @manage_practice_manager
    def get(self, id_group, id_location):
        return get_users_role('practice_manager', id_group, id_location)

    @manage_practice_manager
    def post(self, id_group, id_location):
        return save_new_user('practice_manager', request.get_json(force=True), id_group, id_location)


class PacticeManager(Resource):
    @manage_practice_manager
    def get(self, id_user, id_group, id_location):
        return get_user_role('practice_manager', id_user, id_group, id_location)

    @manage_practice_manager
    def put(self, id_user, id_group, id_location):
        return update_user('practice_manager', id_user, request.get_json(force=True), id_group, id_location)

    @manage_practice_manager
    def delete(self, id_user, id_group, id_location):
        return delete_user('practice_manager', id_user, id_group, id_location)


api.add_resource(PacticeManagerList, '/group/<id_group>/location/<id_location>/practice_manager')
api.add_resource(PacticeManager, '/group/<id_group>/location/<id_location>/practice_manager/<id_user>')


class MPList(Resource):
    @list_patient
    def get(self, id_group, id_location):
        return get_users_role('mp', id_group, id_location)

    @manage_mp
    def post(self, id_group, id_location):
        return save_new_user('mp', request.get_json(force=True), id_group, id_location)


class MP(Resource):
    @manage_mp
    def get(self, id_user, id_group, id_location):
        return get_user_role('mp', id_user, id_group, id_location)

    @manage_mp
    def put(self, id_user, id_group, id_location):
        return update_user('mp', id_user, request.get_json(force=True), id_group, id_location)

    @manage_mp
    def delete(self, id_user, id_group, id_location):
        return delete_user('mp', id_user, id_group, id_location)


api.add_resource(MPList, '/group/<id_group>/location/<id_location>/mp')
api.add_resource(MP, '/group/<id_group>/location/<id_location>/mp/<id_user>')


class NMPList(Resource):
    @manage_nmp
    def get(self, id_group, id_location):
        return get_users_role('nmp', id_group, id_location)

    @manage_nmp
    def post(self, id_group, id_location):
        return save_new_user('nmp', request.get_json(force=True), id_group, id_location)


class NMP(Resource):
    @manage_nmp
    def get(self, id_user, id_group, id_location):
        return get_user_role('nmp', id_user, id_group, id_location)

    @manage_nmp
    def put(self, id_user, id_group, id_location):
        return update_user('nmp', id_user, request.get_json(force=True), id_group, id_location)

    @manage_nmp
    def delete(self, id_user, id_group, id_location):
        return delete_user('nmp', id_user, id_group, id_location)


api.add_resource(NMPList, '/group/<id_group>/location/<id_location>/nmp')
api.add_resource(NMP, '/group/<id_group>/location/<id_location>/nmp/<id_user>')
