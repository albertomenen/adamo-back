from flask import jsonify, make_response
from src import db
from .common import save_changes
from ..models import Date, Location, Group
from marshmallow import Schema, fields
from sqlalchemy import update


class DateSchema(Schema):
    id_date = fields.UUID()
    id_timetable = fields.UUID()
    id_medic = fields.UUID()
    id_patient = fields.UUID()
    id_station = fields.UUID()
    id_location = fields.UUID()
    day = fields.Str()
    from_hour = fields.Str()
    to_hour = fields.Str()
    presented = fields.Boolean()


class DateListSchema(Schema):
    id_date = fields.UUID()
    day = fields.Str()
    from_hour = fields.Str()
    to_hour = fields.Str()
    id_patient = fields.UUID()
    id_station = fields.UUID()


schema = DateSchema()
schema_list = DateListSchema()


def save_new_date(id_group, id_location, id_station, data):
    location = Location.query.filter_by(id_location=id_location).filter_by(id_group=id_group).first()
    if location and location.id_timetable:
        id_timetable = location.id_timetable
    else:
        return {
            'status': 'fail',
            'message': 'Not timetable assigned',
        }
    try:
        data['id_location'] = id_location
        data['id_station'] = id_station
        data['id_timetable'] = id_timetable
        new_date = Date(**data)
        save_changes(new_date)
    except:
        response_object = {
            'status': 'fail',
            'message': 'Bad parameters',
        }
        return response_object, 409
    return make_response(jsonify(schema.dump(new_date)), 201)


def check_date_solap():
    pass  # TODO comprobar que esta dentro del horario y que no se sale del horario


def get_dates_medic(id_medic, from_date, to_date):
    dates = Date.query.filter(Date.day >= from_date)\
        .filter(Date.day <= to_date)\
        .filter(Date.id_medic == id_medic).all()
    return [schema_list.dump(date) for date in dates]


def get_free_station(day, from_hour, to_hour):
    pass


def get_free_medic(day, from_hour, to_hour):
    pass


def get_dates_station(id_station, from_date, to_date):
    dates = Date.query.filter(Date.day >= from_date)\
        .filter(Date.day <= to_date)\
        .filter(Date.id_station == id_station).all()
    return [schema_list.dump(date) for date in dates]


def get_dates(id_group, id_location, from_date, to_date):
    dates = Date.query.filter(Date.day >= from_date) \
        .filter(Date.day <= to_date) \
        .filter(Date.id_location == id_location).all()


def get_date(id_location, id_date):
    date = Date.query.filter_by(id_date=id_date).filter_by(id_location=id_location).first()
    return jsonify(schema.dump(date))
