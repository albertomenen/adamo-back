from .common import save_changes, update_changes
from ..models import Device
from flask import jsonify, make_response
from marshmallow import Schema, fields
from sqlalchemy import update, delete


class DeviceSchema(Schema):
    id_device = fields.UUID()
    group_id = fields.UUID()
    mac = fields.Str()
    station_id = fields.UUID()
    serial_number = fields.Str()
    hw_version = fields.Str()
    sw_version = fields.Str()
    device_name = fields.Str()


class DeviceUpdateSchema(Schema):
    hw_version = fields.Str()
    sw_version = fields.Str()
    device_name = fields.Str()
    station_id = fields.UUID()
    group_id = fields.UUID()


class DeviceListSchema(Schema):
    id_device = fields.UUID()
    device_name = fields.Str()


schema = DeviceSchema()
schema_list = DeviceListSchema()
schema_update = DeviceUpdateSchema()


def save_new_device(data):
    device = Device.query.filter_by(mac=data['mac']).first()
    if not device:
        new_device = Device(**data)
        save_changes(new_device)
        return make_response(jsonify(schema.dump(new_device)), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'device mac already exists',
        }
        return response_object, 409


def get_device_from_station(station_id):
    return jsonify(schema.dump(Device.query.filter_by(station_id=station_id).first()))


def get_all_devices():
    return jsonify([schema_list.dump(device) for device in Device.query.all()])


def get_all_free_devices():
    return jsonify([schema_list.dump(device) for device in
                    Device.query.filter_by(station_id=None).all()])


def get_device(id_device):
    return jsonify(schema.dump(Device.query.filter_by(id_device=id_device).first()))


def update_device(id_device, data):
    device = Device.query.filter_by(id_device=id_device).first()
    if device:
        new_values = schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Device).where(Device.id_device == id_device).values(new_values).\
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**schema.dump(device), **new_values})
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
            'message': 'device not found',
        }, 404


def delete_device(id_device):
    device = Device.query.filter_by(id_device=id_device).first()
    if device:
        try:
            stmt = delete(Device).where(Device.id_device == id_device).execution_options(synchronize_session=False)
            update_changes(stmt)
            return {
                'status': 'success',
                'message': 'device deleted',
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