from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.user import save_new_user, get_users, get_user, update_user, delete_user

bp = Blueprint('user', __name__)
api = Api(bp)


class UserList(Resource):
    def get(self):
        return get_users()

    def post(self):
        return save_new_user(request.json)


class User(Resource):
    def get(self, id_user):
        return get_user(id_user)

    def put(self, id_user):
        return update_user(id_user, request.json)

    def delete(self, id_user):
        return delete_user(id_user)


api.add_resource(UserList, '/')
api.add_resource(User, '/<id_user>')
