from marshmallow import Schema, fields
from .location import location_name


class StationCreateSchema(Schema):
    id_location = fields.UUID()
    location = fields.Nested(location_name)
    station_name = fields.Str()
    placed = fields.Str()
    installation_date = fields.Str()


class StationUpdateSchema(Schema):
    station_name = fields.Str()
    version = fields.Str()


class StationDetailSchema(Schema):
    id_station = fields.UUID()
    id_location = fields.UUID()
    location = fields.Nested(location_name)
    station_name = fields.Str()
    placed = fields.Str()
    installation_date = fields.Str()


class StationListSchema(Schema):
    id_station = fields.UUID()
    station_name = fields.Str()
    placed = fields.Str()
    installation_date = fields.Str()
    location = fields.Nested(location_name)


station_schema_create = StationCreateSchema()
station_schema_update = StationUpdateSchema()
station_schema_detail = StationDetailSchema()
station_schema_list = StationListSchema()
