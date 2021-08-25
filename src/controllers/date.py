from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.date import save_new_date, get_dates_medic_station, get_date

bp = Blueprint('Date', __name__)
api = Api(bp)


class DateList(Resource):
    def get(self, id_station):
        return get_dates_medic_station(id_station, request.args.get('from_date'), request.args.get('to_date'))

class DateDetail(Resource):
    def get(self, id_station, id_date):
        return get_date(id_station, id_date)


class DateCreate(Resource):
    def post(self, group_id, patient_id, treatment_id):
        return save_new_date(group_id, patient_id, treatment_id, request.get_json(force=True))


api.add_resource(DateList, '/station/<id_station>/date')
api.add_resource(DateDetail, '/station/<id_station>/date/<id_date>')
api.add_resource(DateCreate, '/group/<group_id>/patient/<patient_id>/treatment/<treatment_id>/date')
