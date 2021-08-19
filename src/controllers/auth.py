from flask import request, Blueprint, jsonify
from flask_restful import Resource, Api
from ..services.auth import Auth

bp = Blueprint('auth', __name__)
api = Api(bp)


class UserLogin(Resource):
    def post(self):
        return Auth.login_user(data=request.json)


class LogoutAPI(Resource):
    def post(self):
        return Auth.logout_user(request)


api.add_resource(UserLogin, '/login')
api.add_resource(LogoutAPI, '/logout')
