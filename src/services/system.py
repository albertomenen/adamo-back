from flask import jsonify, make_response
from src import db, pagination
from .common import save_changes
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
            save_changes(new_system)
        except:
            response_object = {
                'status': 'fail',
                'message': 'Bad parameters',
            }
            return response_object, 409
        return make_response(jsonify(schema.dump(new_system)), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'System email already exists',
        }
        return response_object, 409


def get_systems():
    return pagination.paginate(System.query.all(), schema_list, True)


def get_system(id_system):
    return jsonify(schema.dump(System.query.filter_by(id_system=id_system).first()))

