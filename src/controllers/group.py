from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.group import save_new_group, get_group, get_groups, update_group, delete_group
from ..utils.decorators import manage_group

bp = Blueprint('Group', __name__)
api = Api(bp)


class GroupList(Resource):
    @manage_group
    def get(self):
        return get_groups()

    @manage_group
    def post(self):
        return save_new_group(request.get_json(force=True))


class Group(Resource):
    @manage_group
    def get(self, group_id):
        return get_group(group_id)

    @manage_group
    def put(self, group_id):
        return update_group(group_id, request.get_json(force=True))

    @manage_group
    def delete(self, group_id):
        return delete_group(group_id)


api.add_resource(GroupList)
api.add_resource(Group, '/<group_id>')
