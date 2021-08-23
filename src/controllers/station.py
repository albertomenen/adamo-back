from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.station import save_new_station, get_station, update_station, delete_station, get_stations
from ..utils.decorators import manage_station

bp = Blueprint('Station', __name__)
api = Api(bp)


class StationList(Resource):
    @manage_station
    def get(self, id_group, location_id):
        return get_stations(id_group, location_id)

    @manage_station
    def post(self, id_group, location_id):
        return save_new_station(id_group, location_id, request.get_json(force=True))


class Station(Resource):
    @manage_station
    def get(self, id_group, location_id, id_station):
        return get_station(id_group, location_id, id_station)

    @manage_station
    def put(self, id_group, location_id, id_station):
        return update_station(id_group, location_id, id_station, request.get_json(force=True))

    @manage_station
    def delete(self, id_group, location_id, id_station):
        return delete_station(id_group, location_id, id_station)


api.add_resource(StationList, '/group/<id_group>/location/<location_id>/station')
api.add_resource(Station, '/group/<id_group>/location/<location_id>/station/<id_station>')
