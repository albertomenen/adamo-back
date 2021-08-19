from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.group import save_new_group, get_group, get_groups, update_group, delete_group

bp = Blueprint('Group', __name__)
api = Api(bp)


class GroupList(Resource):
    def get(self):
        return get_groups()

    def post(self):
        return save_new_group(request.json)


class Group(Resource):
    def get(self, group_id):
        return get_group(group_id)

    def put(self, group_id):
        return update_group(group_id, request.json)

    def delete(self, group_id):
        return delete_group(group_id)


api.add_resource(GroupList, '/')
api.add_resource(Group, '/<group_id>')
