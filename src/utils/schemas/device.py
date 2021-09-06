from marshmallow import Schema, fields


class DeviceCreateSchema(Schema):
    group_id = fields.UUID()
    mac = fields.Str()
    station_id = fields.UUID()
    serial_number = fields.Str()
    hw_version = fields.Str()
    sw_version = fields.Str()
    device_name = fields.Str()


class DeviceDetailSchema(Schema):
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


device_schema_create = DeviceCreateSchema()
device_schema_detail = DeviceDetailSchema()
device_schema_list = DeviceListSchema()
device_schema_update = DeviceUpdateSchema()
