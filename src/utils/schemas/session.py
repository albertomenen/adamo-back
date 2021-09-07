from marshmallow import Schema, fields
from .point import point_schema


class SessionDetailSchema(Schema):
    id_session = fields.UUID()
    medic = fields.Str()
    session_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    ts_creation_date = fields.Str()
    heating_duration = fields.Float()
    points = fields.List(fields.Nested(point_schema))
    pressure = fields.Float()
    device_id = fields.UUID()
    station_id = fields.UUID()


class SessionListSchema(Schema):
    id_session = fields.UUID()
    medic = fields.Str()
    session_number = fields.Integer()
    ts_creation_date = fields.Str()


class SessionCreateSchema(Schema):
    medic = fields.Str()
    session_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    heating_duration = fields.Float()
    points = fields.List(fields.Nested(point_schema))
    pressure = fields.Float()
    device_id = fields.UUID()
    station_id = fields.UUID()
    treatment_id = fields.UUID()


session_schema_detail = SessionDetailSchema()
session_schema_list = SessionListSchema()
session_schema_create = SessionCreateSchema()
