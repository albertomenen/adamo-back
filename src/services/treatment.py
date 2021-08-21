from flask import jsonify
from src import db
from .common import save_changes, update_changes
from ..models import Treatment, User, Patient, PAlias
from marshmallow import Schema, fields
from sqlalchemy import update


class Points(Schema):
    duration = fields.Float()
    gradual = fields.Boolean()
    x = fields.Float()
    y = fields.Float()
    z = fields.Float()
    rx = fields.Float()
    ry = fields.Float()
    rz = fields.Float()
    height = fields.Float()
    pressure = fields.Float()


class TreatmentSchema(Schema):
    id_treatment = fields.UUID()
    medic = fields.UUID()
    name = fields.Str()
    sessions_number = fields.Integer()
    current_session_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    ts_creation_date = fields.Date()
    heating_duration = fields.Integer()
    points = fields.List(fields.Nested(Points))
    ts_next_session = fields.Float()
    ts_end = fields.Float()
    width = fields.Float()
    height = fields.Float()
    ppx = fields.Float()
    ppy = fields.Float()
    fx = fields.Float()
    fy = fields.Float()
    model = fields.Str()
    coeff = fields.Str()
    depth_scale = fields.Float()
    mode = fields.Str()
    extrinsics = fields.Str()
    next_session_station_id = fields.UUID()
    last_session_date = fields.Str()
    state = fields.Str()


class TreatmentUpdateSchema(Schema):
    name = fields.Str()
    current_session_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    heating_duration = fields.Integer()
    state = fields.Str()
    next_session_station_id = fields.UUID()
    last_session_date = fields.Str()


class TreatmentListSchema(Schema):
    id_treatment = fields.UUID()
    medic_name = fields.Str()
    name = fields.Str()
    state = fields.Str()
    sessions_number = fields.Integer()
    current_session_number = fields.Integer()


schema = TreatmentSchema()
schema_list = TreatmentListSchema()
schema_update = TreatmentUpdateSchema()


def save_new_treatment(id_group, patient_id, data):
    palias = db.session.query(PAlias).join(Patient).join(User)\
        .filter(PAlias.patient == patient_id)\
        .filter(Patient.id_patient == patient_id)\
        .filter(User.id_user == Patient.id_user)\
        .filter(User.id_group == id_group).filter(User.state == True).first()
    if palias:
        try:
            data['id_patient'] = palias.id_palias
            new_treatment = Treatment(**data)
            save_changes(new_treatment)
        except:
            response_object = {
                'status': 'fail',
                'message': 'Bad parameters',
            }
            return response_object, 409
        return jsonify(schema.dump(new_treatment)), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Patient doesn\'t exists',
        }
        return response_object, 409


def get_treatments():
    return jsonify([schema_list.dump(treatment) for treatment in Treatment.query.all()])


def get_query_treatment(id_group, id_patient, id_treatment):
    return db.session.query(Treatment).join(PAlias).join(Patient).join(User) \
        .filter(Treatment.id_treatment == id_treatment) \
        .filter(Treatment.id_patient == PAlias.id_palias) \
        .filter(PAlias.patient == id_patient) \
        .filter(Patient.id_patient == id_patient) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.id_group == id_group).filter(User.state == True).first()

def get_treatments_by_patient(id_group, patient_id):
    treatments = db.session.query(Treatment).join(PAlias).join(Patient).join(User) \
        .filter(Treatment.id_patient == PAlias.id_palias) \
        .filter(PAlias.patient == patient_id) \
        .filter(Patient.id_patient == patient_id) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.id_group == id_group).filter(User.state == True).all()
    return jsonify([schema_list.dump(treatment) for treatment in treatments])


def get_treatment(id_group, id_patient, id_treatment):
    treatment = get_query_treatment(id_group, id_patient, id_treatment)
    return jsonify(schema.dump(treatment))


def update_treatment(id_group, id_patient, id_treatment, data):
    treatment = get_query_treatment(id_group, id_patient, id_treatment)
    if treatment:
        new_values = schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Patient).where(Patient.id_patient == id_patient).values(new_values). \
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**schema.dump(treatment), **new_values})
            except:
                return {
                           'status': 'fail',
                           'message': 'Update failed',
                       }, 401
        else:
            return {
                       'status': 'fail',
                       'message': 'Nothin to update',
                   }, 401

    else:
        return {
                   'status': 'fail',
                   'message': 'treatment not found',
               }, 404