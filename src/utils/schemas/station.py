from marshmallow import Schema, fields
# from .device import device_schema_list
from .location import location_name


class StationCreateSchema(Schema):
    id_location = fields.UUID()
    location = fields.Nested(location_name)
    station_name = fields.Str()
    placed = fields.Str()
    installation_date = fields.Str()
    version = fields.Str()
    # device = fields.List(fields.Nested(device_schema_list))


class StationUpdateSchema(Schema):
    station_name = fields.Str()
    version = fields.Str()
    # device = fields.List(fields.Nested(device_schema_list))


class StationDetailSchema(Schema):
    id_station = fields.UUID()
    id_location = fields.UUID()
    location = fields.Nested(location_name)
    station_name = fields.Str()
    placed = fields.Str()
    installation_date = fields.Str()
    version = fields.Str()
    # device = fields.List(fields.Nested(device_schema_list))


class StationListSchema(Schema):
    id_station = fields.UUID()
    station_name = fields.Str()
    location = fields.Nested(location_name)


station_schema_create = StationCreateSchema()
station_schema_update = StationUpdateSchema()
station_schema_detail = StationDetailSchema()
station_schema_list = StationListSchema()
