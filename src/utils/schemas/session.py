from marshmallow import Schema, fields
from .point import point_schema


class SessionDetailSchema(Schema):
    id_session = fields.UUID()
    medic = fields.Str()
    session_number = fields.Integer()
    notes = fields.Str()
    ts_creation_date = fields.Str()
    device_id = fields.UUID()
    station_id = fields.UUID()
    image_thermic = fields.Str()
    image_3D_color = fields.Str()


class SessionListSchema(Schema):
    id_session = fields.UUID()
    medic = fields.Str()
    session_number = fields.Integer()
    ts_creation_date = fields.Str()


class SessionCreateSchema(Schema):
    medic = fields.Str()
    session_number = fields.Integer()
    notes = fields.Str()
    device_id = fields.UUID()
    station_id = fields.UUID()
    treatment_id = fields.UUID()
    image_thermic_width = fields.Str()
    image_thermic_height = fields.Str()
    image_thermic_depth = fields.Str()


session_schema_detail = SessionDetailSchema()
session_schema_list = SessionListSchema()
session_schema_create = SessionCreateSchema()
