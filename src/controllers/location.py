from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.location import save_new_location, get_location, get_location_from_group, update_location, \
    delete_location
from ..utils.decorators import manage_location

bp = Blueprint('Location', __name__)
api = Api(bp)


# class LocationSetTimetable(Resource):
#     def put(self, id_group, location_id):
#         id_timetable = request.get_json(force=True).get('id_timetable')
#         return set_location_timetable(id_group, location_id, id_timetable)


# api.add_resource(LocationSetTimetable, '/group/<id_group>/location/<location_id>/set_timetable')


class LocationList(Resource):
    @manage_location
    def get(self, id_group):
        return get_location_from_group(id_group)

    @manage_location
    def post(self, id_group):
        return save_new_location(id_group, request.get_json(force=True))


class Location(Resource):
    @manage_location
    def get(self, id_group, location_id):
        return get_location(id_group, location_id)

    @manage_location
    def put(self, id_group, location_id):
        return update_location(id_group, location_id, request.get_json(force=True))

    @manage_location
    def delete(self, id_group, location_id):
        return delete_location(id_group, location_id)


api.add_resource(LocationList, '/group/<id_group>/location')
api.add_resource(Location, '/group/<id_group>/location/<location_id>')
