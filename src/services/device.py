from .. import db
from .station import StationListSchema
from ..models import Device, Station
from flask import jsonify
from marshmallow import Schema, fields
from sqlalchemy import update


class DeviceSchema(Schema):
    id_device = fields.UUID()
    mac = fields.Str()
    serial_number = fields.Str()
    hw_version = fields.Str()
    sw_version = fields.Str()
    device_name = fields.Str()
    station = fields.Nested(StationListSchema())


class DeviceListSchema(Schema):
    id_device = fields.UUID()
    device_name = fields.Str()


schema = DeviceSchema()
schema_list = DeviceListSchema()


def save_new_device(data):
    device = Device.query.filter_by(email=data['email']).first()
    if not device:
        new_device = Device(**data)
        save_changes(new_device)
        return jsonify(schema.dump(new_device)), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'device email already exists',
        }
        return response_object, 409


def get_device_from_station(station_id):
    return jsonify(schema.dump(db.session.query(Device).join(Station).filter(Station.id_station == station_id).first()))


def get_all_devices():
    return jsonify([schema_list.dump(device) for device in Device.query.all()])


def get_device(id_device):
    return jsonify(schema.dump(Device.query.filter_by(id_device=id_device).first()))


def save_changes(data):
    db.session.add(data)
    db.session.commit()
