from flask import jsonify
from src import db
from ..models import Session
from ..services.station import StationListSchema
from marshmallow import Schema, fields
from sqlalchemy import update


class SessionSchema(Schema):
    id_session = fields.UUID()
    medic_name = fields.Str()
    session_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    ts_creation_date = fields.Date()
    heating_duration = fields.Integer()
    points = fields.Str()
    station = fields.Nested(StationListSchema())


class SessionListSchema(Schema):
    id_session = fields.UUID()
    medic_name = fields.Str()
    session_number = fields.Integer()


schema = SessionSchema()
schema_list = SessionListSchema()


def save_new_session(data):
    session = Session.query.filter_by(email=data['email']).first()
    if not session:
        try:
            new_session = Session(**data)
        except:
            response_object = {
                'status': 'fail',
                'message': 'Bad parameters',
            }
            return response_object, 409
        save_changes(new_session)
        return jsonify(schema.dump(new_session)), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Session email already exists',
        }
        return response_object, 409


def get_sessions():
    return jsonify([schema_list.dump(session) for session in Session.query.all()])


def get_session(id_session):
    return jsonify(schema.dump(Session.query.filter_by(id_session=id_session).first()))


def save_changes(data):
    db.session.add(data)
    db.session.commit()
