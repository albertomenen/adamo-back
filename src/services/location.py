from .common import save_changes, update_changes
from ..models import Location, Group, Station, Device
from flask import jsonify
from marshmallow import Schema, fields
from sqlalchemy import update


class LocationSchema(Schema):
    id_location = fields.UUID()
    location_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()
    email = fields.Email()


class LocationListSchema(Schema):
    id_location = fields.UUID()
    location_name = fields.Str()


class LocationUpdateSchema(Schema):
    location_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()


schema = LocationSchema()
schema_list = LocationListSchema()
schema_update = LocationUpdateSchema()


def save_new_location(id_group, data):
    location = Location.query.filter_by(email=data['email']).first()
    group = Group.query.filter_by(id_group=id_group).first()
    if not location:
        if not group:
            return {
                       'status': 'fail',
                       'message': 'Group doesn\'t exists',
                   }, 401
        try:
            new_location = Location(**data)
            save_changes(new_location)
        except:
            return {
                       'status': 'fail',
                       'message': 'Wrong parameters',
                   }, 401
        return jsonify(schema.dump(new_location)), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'location email already exists',
        }
        return response_object, 409


def get_location_from_group(group_id):
    return jsonify([schema_list.dump(location) for location in Location.query.filter_by(id_group=group_id).all()])


def get_all_locations():
    return jsonify([schema_list.dump(location) for location in Location.query.all()])


def get_location(id_group, id_location):
    return jsonify(schema.dump(Location.query.filter_by(id_location=id_location).filter_by(id_group=id_group).first()))


def update_location(id_group, id_location, data):
    location = Location.query.filter_by(id_location=id_location).filter_by(id_group=id_group).first()
    if location:
        new_values = schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Location).where(Location.id_location == id_location).values(new_values).\
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**schema.dump(location), **new_values})
            except Exception as e:
                return {
                           'status': 'fail',
                           'message': str(e),
                       }, 401
        else:
            return {
                'status': 'fail',
                'message': 'Nothin to update',
            }, 401

    else:
        return {
            'status': 'fail',
            'message': 'user not found',
        }, 404


def delete_location(id_group, id_location):
    location = Location.query.filter_by(id_location=id_location).filter_by(id_group=id_group).first()
    if location:
        try:
            stmt_patient = update(Location).where(Location.id_location == id_location).values(state=False). \
                execution_options(synchronize_session=False)
            stmt_station = update(Station).where(Station.id_location == id_location).values(state=False)\
                .execution_options(synchronize_session=False)
            stmt_device = update(Device).where(Device.station_id == Station.id_station) \
                .where(Station.id_location == id_location).values(station_id=None). \
                execution_options(synchronize_session=False)
            update_changes(stmt_patient, stmt_station, stmt_device)
            return {
                'status': 'success',
                'message': 'location deleted',
            }, 203
        except Exception as e:
            return {
                'status': 'fail',
                'message': str(e),
            }, 401
    else:
        return {
            'status': 'fail',
            'message': 'user not found',
        }, 404

