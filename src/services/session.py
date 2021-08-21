import datetime

from flask import jsonify, make_response
from src import db
from .common import save_changes
from .device import DeviceListSchema
from .treatment import Points, TreatmentListSchema, update_treatment
from ..models import Session, Treatment, PAlias, Patient, User, Station, Location
from ..services.station import StationListSchema, StationSchema
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
        if treatment.current_session_number == treatment.sessions_number:
            return {
                'status': 'fail',
                'message': 'Treatment finished, cannot add more sessions',
            }, 401
        station = StationSchema().dump(db.session.query(Station).join(Location) \
                                       .filter(Station.id_station == data['station_id']) \
                                       .filter(Station.id_location == Location.id_location) \
                                       .filter(Location.id_group == id_group).first())
        if station and station['device']:
            data['device_id'] = station['device'][0]['id_device']
        else:
            return {
                'status': 'fail',
                'message': 'Device not assigned',
            }, 401
        try:
            data['session_number'] = treatment.current_session_number + 1
            data['treatment_id'] = id_treatment
            new_session = Session(**data)
            save_changes(new_session)

            new_data_treatment = {
                'last_session_date': datetime.datetime.utcnow(),
                'state': 'started' if treatment.current_session_number < treatment.sessions_number - 1 else 'finished',
                'current_session_number': treatment.current_session_number + 1
            }
            update_treatment(id_group, patient_id, id_treatment, new_data_treatment)
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e),
            }
            return response_object, 409
        return make_response(jsonify(schema.dump(new_session)), 201)
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
    return schema.dump(db.session.query(Session).join(Treatment).join(PAlias).join(Patient).join(User) \
        .filter(Session.id_session == id_session) \
        .filter(Session.treatment_id == id_treatment) \
        .filter(Treatment.id_treatment == id_treatment) \
        .filter(Treatment.id_patient == PAlias.id_palias) \
        .filter(PAlias.patient == id_patient) \
        .filter(Patient.id_patient == id_patient) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.id_group == id_group).filter(User.state == True).first())


def get_sessions_treatment(id_group, patient_id, id_treatment):
    treatments = db.session.query(Session).join(Treatment).join(PAlias).join(Patient).join(User) \
        .filter(Session.treatment_id == id_treatment) \
        .filter(Treatment.id_patient == PAlias.id_palias) \
        .filter(PAlias.patient == patient_id) \
        .filter(Patient.id_patient == patient_id) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.id_group == id_group).filter(User.state == True).all()
    return jsonify([schema_list.dump(treatment) for treatment in treatments])
