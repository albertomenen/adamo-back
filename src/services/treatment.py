from flask import jsonify, make_response
from src import db, pagination
from .common import save_changes, update_changes, Points
from ..models import Treatment, User, Patient, PAlias
from marshmallow import Schema, fields
from sqlalchemy import update


class SessionListSchema(Schema):
    id_session = fields.UUID()
    medic = fields.Str()
    session_number = fields.Integer()
    ts_creation_date = fields.Str()


class PatientListSchema(Schema):
    id_patient = fields.UUID()
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
    points = fields.List(fields.Nested(Points()))
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
    extrinsics = fields.Str()
    next_session_station_id = fields.UUID()
    last_session_date = fields.Str()
    state = fields.Str()
    injury = fields.Str()
    injury_cause = fields.Str()
    injury_kind = fields.Str()

    sessions = fields.List(fields.Nested(SessionListSchema()))


class TreatmentUpdateSchema(Schema):
    name = fields.Str()
    current_session_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    heating_duration = fields.Float()
    next_session_station_id = fields.UUID()
    last_session_date = fields.Str()
    state = fields.Str()


class TreatmentListSchema(Schema):
    id_treatment = fields.UUID()
    name = fields.Str()
    state = fields.Str()
    sessions_number = fields.Integer()
    current_session_number = fields.Integer()
    mode = fields.Str()
    last_session_date = fields.Str()


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
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e),
            }
            return response_object, 409
        return make_response(jsonify(schema.dump(new_treatment)), 201)
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

    return pagination.paginate(treatments, schema_list, True)


def get_treatment(id_group, id_patient, id_treatment):
    treatment = schema.dump(get_query_treatment(id_group, id_patient, id_treatment))
    patient = db.session.query(Patient).join(PAlias)\
        .filter(Patient.id_patient == PAlias.patient).filter(PAlias.id_palias == treatment['id_patient']).first()
    treatment['patient'] = PatientListSchema().dump(patient)
    return jsonify(treatment)


def update_treatment(id_group, id_patient, id_treatment, data):
    treatment = get_query_treatment(id_group, id_patient, id_treatment)
    if treatment:
        new_values = schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Treatment).where(Treatment.id_treatment == id_treatment).values(new_values). \
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**schema.dump(treatment), **new_values})
            except Exception as e:
                return {
                           'status': 'fail',
                           'message': str(e),
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