from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.station import save_new_station, get_station, update_station, delete_station, get_stations

bp = Blueprint('Station', __name__)
api = Api(bp)


class StationList(Resource):
    def get(self, id_group, id_location):
        return get_stations(id_group, id_location)

    def post(self, id_group, id_location):
        return save_new_station(id_group, id_location, request.json)


class Station(Resource):
    def get(self, id_group, location_id, id_station):
        return get_station(id_group, location_id, id_station)

    def put(self, id_group, location_id, id_station):
        return update_station(id_group, location_id, id_station, request.json)

    def delete(self, id_group, location_id, id_station):
        return delete_station(id_group, location_id, id_station)


api.add_resource(StationList, '/group/<id_group>/location/<location_id>/station')
api.add_resource(Station, '/group/<id_group>/location/<location_id>/station/<station_id>')
