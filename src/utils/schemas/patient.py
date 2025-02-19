from marshmallow import Schema, fields
from .user import user_detail_schema
from .treatment import treatment_schema_list


class PatientDetailSchema(Schema):
    id_patient = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    profession = fields.Str()
    observations = fields.Str()
    birthdate = fields.Str()
    identification = fields.Str()
    email = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    active_treatments = fields.Integer()
    user = fields.Nested(user_detail_schema)
    country = fields.Str()
    gender = fields.Str()
    race = fields.Str()
    complexity = fields.Str()
    weight = fields.Float()
    height = fields.Float()
    allergies = fields.Str()
    move = fields.Str()
    medication = fields.Str()
    treatments = fields.List(fields.Nested(treatment_schema_list))


class PatientCreateSchema(Schema):
    id_user = fields.UUID()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    email = fields.Str()
    birthdate = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    identification = fields.Str()
    profession = fields.Str()
    observations = fields.Str()
    country = fields.Str()
    gender = fields.Str()
    race = fields.Str()
    complexity = fields.Str()
    weight = fields.Float()
    height = fields.Float()
    allergies = fields.Str()
    medication = fields.Str()


class PatientListSchema(Schema):
    id_patient = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    active_treatments = fields.Integer()


class PatientUpdateSchema(Schema):
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    profession = fields.Str()
    observations = fields.Str()
    birthdate = fields.Str()
    identification = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    country = fields.Str()
    gender = fields.Str()
    race = fields.Str()
    complexity = fields.Str()
    weight = fields.Float()
    height = fields.Float()
    allergies = fields.Str()
    medication = fields.Str()


patient_schema_detail = PatientDetailSchema()
patient_schema_list = PatientListSchema()
patient_schema_update = PatientUpdateSchema()
patient_schema_create = PatientCreateSchema()