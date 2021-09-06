from marshmallow import Schema, fields


class PatientListSchema(Schema):
    email = fields.Str()
    phone = fields.Str()
    name = fields.Str()
    last_name = fields.Str()


class TreatmentSchema(Schema):
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
    # points = fields.List(fields.Nested(Points()))
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

    # sessions = fields.List(fields.Nested(SessionSchema()))


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


schema = TreatmentSchema()
schema_list = TreatmentListSchema()
schema_update = TreatmentUpdateSchema()