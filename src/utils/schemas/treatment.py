from marshmallow import Schema, fields
from .point import point_schema
from .session import session_schema_list


class TreatmentCreateSchema(Schema):
    id_patient = fields.UUID()
    medic = fields.UUID()
    name = fields.Str()
    sessions_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    heating_duration = fields.Integer()
    points = fields.List(fields.Nested(point_schema))
    weight = fields.Float()
    height = fields.Float()
    ppx = fields.Float()
    ppy = fields.Float()
    fx = fields.Float()
    fy = fields.Float()
    model = fields.Str()
    coeff = fields.Str()
    depth_scale = fields.Float()
    mode = fields.Str()
    move = fields.Str()
    extrinsics = fields.Str()
    injury = fields.Str()
    injury_cause = fields.Str()
    injury_kind = fields.Str()


class TreatmentDetailSchema(Schema):
    id_treatment = fields.UUID()
    id_patient = fields.UUID()
    medic = fields.UUID()
    name = fields.Str()
    sessions_number = fields.Integer()
    current_session_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    ts_creation_date = fields.Date()
    heating_duration = fields.Integer()
    points = fields.List(fields.Nested(point_schema))
    ts_next_session = fields.Float()
    ts_end = fields.Float()
    weight = fields.Float()
    height = fields.Float()
    ppx = fields.Float()
    ppy = fields.Float()
    fx = fields.Float()
    fy = fields.Float()
    model = fields.Str()
    coeff = fields.Str()
    depth_scale = fields.Float()
    mode = fields.Str()
    move = fields.Str()
    extrinsics = fields.Str()
    next_session_station_id = fields.UUID()
    last_session_date = fields.Date()
    next_session_date = fields.Date()
    state = fields.Str()
    injury = fields.Str()
    injury_cause = fields.Str()
    injury_kind = fields.Str()

    sessions = fields.List(fields.Nested(session_schema_list))


class TreatmentUpdateSchema(Schema):
    name = fields.Str()
    current_session_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    heating_duration = fields.Float()
    next_session_date = fields.Date()
    last_session_date = fields.Date()
    state = fields.Str()


class TreatmentListSchema(Schema):
    next_session_date = fields.Date()
    id_treatment = fields.UUID()
    name = fields.Str()
    state = fields.Str()
    sessions_number = fields.Integer()
    current_session_number = fields.Integer()
    mode = fields.Str()
    last_session_date = fields.Date()


treatment_schema_create = TreatmentCreateSchema()
treatment_schema_detail = TreatmentDetailSchema()
treatment_schema_list = TreatmentListSchema()
treatment_schema_update = TreatmentUpdateSchema()
