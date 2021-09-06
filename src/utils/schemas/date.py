from marshmallow import Schema, fields


class DateCreateSchema(Schema):
    id_medic = fields.UUID()
    id_patient = fields.UUID()
    id_treatment = fields.UUID()
    id_station = fields.UUID()
    day = fields.Str()
    from_hour = fields.Str()
    to_hour = fields.Str()


class DateDetailSchema(Schema):
    id_date = fields.UUID()
    id_medic = fields.UUID()
    id_patient = fields.UUID()
    id_station = fields.UUID()
    id_treatment = fields.UUID()
    day = fields.Str()
    from_hour = fields.Str()
    to_hour = fields.Str()
    presented = fields.Boolean()


class DateListSchema(Schema):
    id_date = fields.UUID()
    day = fields.Str()
    from_hour = fields.Str()
    to_hour = fields.Str()
    id_patient = fields.UUID()
    id_treatment = fields.UUID()
    id_station = fields.UUID()
    id_medic = fields.UUID()


class DateUpdateSchema(Schema):
    day = fields.Str()
    from_hour = fields.Str()
    to_hour = fields.Str()
    id_station = fields.UUID()
    id_medic = fields.UUID()


date_schema_create = DateCreateSchema()
date_schema_detail = DateDetailSchema()
date_schema_list = DateListSchema()
date_schema_update = DateUpdateSchema()
