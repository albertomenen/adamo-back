from flask import jsonify
from src import db
from ..models import Station
from marshmallow import Schema, fields
from sqlalchemy import update


class StationSchema(Schema):
    id_station = fields.UUID()
    id_location = fields.UUID()
    station_name = fields.Str()
    placed = fields.Str()
    installation_date = fields.Date()
    version = fields.Str()


class StationListSchema(Schema):
    id_station = fields.UUID()
    station_name = fields.Str()


schema = StationSchema()
schema_list = StationListSchema()


def save_new_station(data):
    station = Station.query.filter_by(email=data['email']).first()
    if not station:
        try:
            new_station = Station(**data)
        except:
            response_object = {
                'status': 'fail',
                'message': 'Bad parameters',
            }
            return response_object, 409
        save_changes(new_station)
        return jsonify(schema.dump(new_station)), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'station email already exists',
        }
        return response_object, 409


def get_stations():
    return jsonify([schema_list.dump(station) for station in Station.query.all()])


def get_station(id_station):
    return jsonify(schema.dump(Station.query.filter_by(id_station=id_station).first()))


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def update_changes(stmt):
    db.session.execute(stmt)
    db.session.commit()
