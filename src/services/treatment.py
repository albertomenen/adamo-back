from flask import jsonify
from src import db
from .common import save_changes
from ..models import Treatment, User, Patient, PAlias
from marshmallow import Schema, fields
from sqlalchemy import update


class TreatmentSchema(Schema):
    id_treatment = fields.UUID()
    medic_name = fields.Str()
    name = fields.Str()
    sessions_number = fields.Integer()
    current_session_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    ts_creation_date = fields.Date()
    heating_duration = fields.Integer()
    points = fields.Str()
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


class TreatmentListSchema(Schema):
    id_treatment = fields.UUID()
    medic_name = fields.Str()
    name = fields.Str()
    sessions_number = fields.Integer()
    current_session_number = fields.Integer()


schema = TreatmentSchema()
schema_list = TreatmentListSchema()


def save_new_treatment(patient_id, data):
    palias = db.session.query(PAlias).join(Patient).filter(Patient.id_patient == patient_id).first()
    if palias:
        try:
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


def get_treatments_by_patient(patient_id):
    db.session.quey(Treatment).join(PAlias).join(Patient).filter(Patient.id_patient == patient_id) \
        .filter(Treatment.id_palias == PAlias.id_palias).all()
    return jsonify([schema_list.dump(treatment) for treatment in Treatment.query.all()])


def get_treatment(id_treatment):
    return jsonify(schema.dump(Treatment.query.filter_by(id_treatment=id_treatment).first()))
