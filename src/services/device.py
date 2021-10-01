from .common import save_changes, update_changes
from .. import pagination
from ..models import Device
from flask import jsonify, make_response
from sqlalchemy import update, delete

from ..utils.filter import filtering
from ..utils.schemas.device import device_schema_list, device_schema_detail, device_schema_update, device_schema_create


def save_new_device(data):
    device = Device.query.filter_by(mac=data['mac']).first()
    if not device:
        new_device = Device(**device_schema_create.dump(data))
        save_changes(new_device)
        return make_response(jsonify(device_schema_detail.dump(new_device)), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'device mac already exists',
        }
        return response_object, 409


def get_device_from_station(station_id):
    return jsonify(device_schema_detail.dump(Device.query.filter_by(station_id=station_id).first()))


def get_all_devices(filters):
    devices = Device.query.all()
    devices = filtering(devices, filters)
    return pagination.paginate(devices, device_schema_list, True)


def get_all_free_devices():
    free_devices = Device.query.filter_by(station_id=None).all()
    return pagination.paginate(free_devices, device_schema_list, True)


def get_device(id_device):
    return jsonify(device_schema_detail.dump(Device.query.filter_by(id_device=id_device).first()))


def update_device(id_device, data):
    device = Device.query.filter_by(id_device=id_device).first()
    if device:
        new_values = device_schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Device).where(Device.id_device == id_device).values(new_values).\
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**device_schema_detail.dump(device), **new_values})
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