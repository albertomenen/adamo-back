from flask import request, Blueprint, jsonify
from flask_restful import Resource, Api

from ..services.timetable import get_timetable, get_timetables, save_new_timetable, TimetableSchema, \
    get_week_timetable_from_medic

bp = Blueprint('Timetable', __name__)
api = Api(bp)


class TimetableList(Resource):
    def get(self, id_group):
        return get_timetables(id_group)

    def post(self, id_group):
        return save_new_timetable(id_group, request.get_json(force=True))


class TimetableDetail(Resource):
    def get(self, id_group, id_timetable):
        return get_timetable(id_group, id_timetable)


class Prueba(Resource):
    def get(self):
        return jsonify(get_week_timetable_from_medic(None, "4f66e534-bc18-4027-954d-30477113aaa0", '2021-08-23'))


api.add_resource(Prueba, '/Prueba')

api.add_resource(TimetableList, '/group/<id_group>/timetable')
api.add_resource(TimetableDetail, '/group/<id_group>/timetable/<id_timetable>')
