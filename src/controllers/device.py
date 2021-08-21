from flask import request, Blueprint
from flask_restful import Resource, Api
from ..services.device import get_device, get_all_free_devices, save_new_device, update_device, delete_device, get_all_devices

bp = Blueprint('Device', __name__)
api = Api(bp)


class DeviceList(Resource):
    def get(self):
        return get_all_devices()

    def post(self):
        return save_new_device(request.json)


class DeviceFreeList(Resource):
    def get(self):
        return get_all_free_devices()


class Device(Resource):
    def get(self, device_id):
        return get_device(device_id)

    def put(self, device_id):
        return update_device(device_id, request.json)

    def delete(self, device_id):
        return delete_device(device_id)


api.add_resource(DeviceList, '/')
api.add_resource(DeviceFreeList, '/free')
api.add_resource(Device, '/<device_id>')
