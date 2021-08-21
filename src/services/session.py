import datetime

from flask import jsonify
from src import db
from .common import save_changes
from .device import DeviceListSchema
from .treatment import Points, TreatmentListSchema, update_treatment
from ..models import Session, Treatment, PAlias, Patient, User
from ..services.station import StationListSchema
from marshmallow import Schema, fields


class SessionSchema(Schema):
    id_session = fields.UUID()
    medic = fields.Str()
    session_number = fields.Integer()
    notes = fields.Str()
    temperature = fields.Float()
    ts_creation_date = fields.Str()
    heating_duration = fields.Integer()
    points = fields.List(fields.Nested(Points))
    id_device = fields.Nested(DeviceListSchema())
    id_station = fields.Nested(StationListSchema())
    id_treatment = fields.Nested(TreatmentListSchema())


class SessionListSchema(Schema):
    id_session = fields.UUID()
    medic_name = fields.Str()
    session_number = fields.Integer()


schema = SessionSchema()
schema_list = SessionListSchema()


def save_new_session(id_group, patient_id, id_treatment, data):
    treatment = db.session.query(Treatment).join(PAlias).join(Patient).join(User) \
        .filter(Treatment.id_treatment == id_treatment) \
        .filter(PAlias.patient == patient_id) \
        .filter(Patient.id_patient == patient_id) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.id_group == id_group).filter(User.state == True).first()
    if treatment:
        try:
            new_session = Session(**data)
            save_changes(new_session)

            new_data_treatment = {
                'last_session_date': datetime.datetime.utcnow(),
                'state': 'started' if treatment.current_session_number < treatment.sessions_number - 1 else 'finished',
                'current_session_number': treatment.current_session_number + 1
            }
            update_treatment(id_group, patient_id, id_treatment, new_data_treatment)
        except:
            response_object = {
                'status': 'fail',
                'message': 'Bad parameters',
            }
            return response_object, 409
        return jsonify(schema.dump(new_session)), 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'treatment not found',
        }
        return response_object, 409


def get_sessions():
    return jsonify([schema_list.dump(session) for session in Session.query.all()])


def get_session(id_session):
    return jsonify(schema.dump(Session.query.filter_by(id_session=id_session).first()))


def get_session_treatment(id_group, id_patient, id_treatment, id_session):
    return db.session.query(Session).join(Treatment).join(PAlias).join(Patient).join(User) \
        .filter(Session.id_session == id_session) \
        .filter(Session.id_treatment == id_treatment) \
        .filter(Treatment.id_treatment == id_treatment) \
        .filter(Treatment.id_patient == PAlias.id_palias) \
        .filter(PAlias.patient == id_patient) \
        .filter(Patient.id_patient == id_patient) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.id_group == id_group).filter(User.state == True).first()


def get_sessions_treatment(id_group, patient_id, id_treatment):
    treatments = db.session.query(Session).join(Treatment).join(PAlias).join(Patient).join(User) \
        .filter(Session.id_treatment == id_treatment) \
        .filter(Treatment.id_patient == PAlias.id_palias) \
        .filter(PAlias.patient == patient_id) \
        .filter(Patient.id_patient == patient_id) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.id_group == id_group).filter(User.state == True).all()
    return jsonify([schema_list.dump(treatment) for treatment in treatments])
