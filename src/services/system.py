from flask import jsonify
from src import db
from ..models import System
from marshmallow import Schema, fields
from sqlalchemy import update


class SystemSchema(Schema):
    id_system = fields.UUID()
    system_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()
    email = fields.Email()


class SystemListSchema(Schema):
    id_system = fields.UUID()
    system_name = fields.Str()
    email = fields.Email()


schema = SystemSchema()
schema_list = SystemListSchema()


def save_new_system(data):
    system = System.query.filter_by(email=data['email']).first()
    if not system:
        try:
            new_system = System(**data)
        except:
            response_object = {
                'status': 'fail',
                'message': 'Bad parameters',
            }
            return response_object, 409
        save_changes(new_system)
        return jsonify(schema.dump(new_system)), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'System email already exists',
        }
        return response_object, 409


def get_systems():
    return jsonify([schema_list.dump(system) for system in System.query.all()])


def get_system(id_system):
    return jsonify(schema.dump(System.query.filter_by(id_system=id_system).first()))


def save_changes(data):
    db.session.add(data)
    db.session.commit()
