from flask import jsonify, make_response
from src import db
from .common import update_changes, save_changes
from .user import UserSchema, UserCreateSchema
from ..models import Patient, User, PAlias, Role
from marshmallow import Schema, fields
from sqlalchemy import update


class PatientSchema(Schema):
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
    user = fields.Nested(UserSchema())


class PatientCreateSchema(Schema):
    id_user = fields.UUID()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    email = fields.Str()
    birthdate = fields.Date()
    name = fields.Str()
    last_name = fields.Str()
    identification = fields.Str()
    profession = fields.Str()
    observations = fields.Str()


class PatientListSchema(Schema):
    id_patient = fields.Str()
    email = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    active_treatments = fields.Integer()
    id_user = fields.UUID()


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


schema = PatientSchema()
schema_list = PatientListSchema()
schema_update = PatientUpdateSchema()
schema_create = PatientCreateSchema()
user_create_schema = UserCreateSchema()


def save_new_patient(data):
    patient = Patient.query.filter_by(email=data['email']).first()
    if not patient:
        try:
            new_user = User(**user_create_schema.dump(data))
            new_user.role_id = Role.query.filter_by(role_code='patient').first().id_role
            new_patient = Patient(**schema_create.dump(data))
            new_patient.id_user = new_user.id_user
            new_palias = PAlias(patient=new_patient.id_patient)
            save_changes(new_user)
            save_changes(new_patient)
            save_changes(new_palias)
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e),
            }
            return response_object, 409
        return make_response(jsonify(schema.dump(new_patient)), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'patient email already exists',
        }
        return response_object, 409


def get_patients():
    patient_list = db.session.query(Patient).join(User)\
        .filter(User.id_user == Patient.id_user)\
        .filter(User.state == True).all()
    return jsonify([schema_list.dump(patient) for patient in patient_list])


def get_patients_by_group(id_group):
    patient_list = db.session.query(Patient).join(User)\
        .filter(User.id_user == Patient.id_user)\
        .filter(User.state == True)\
        .filter(User.id_group == id_group).all()
    return jsonify([schema_list.dump(patient) for patient in patient_list])


def get_patient(id_patient):
    patient = db.session.query(Patient).join(User)\
        .filter(Patient.id_patient == id_patient)\
        .filter(User.id_user == Patient.id_user)\
        .filter(User.state == True).first()
    return jsonify(schema.dump(patient))


def update_patient(patient_id, data):
    patient = db.session.query(Patient).join(User)\
        .filter(Patient.id_patient == patient_id)\
        .filter(User.id_user == Patient.id_user)\
        .filter(User.state == True).first()
    if patient:
        new_values = schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Patient).where(Patient.id_patient == patient_id).values(new_values). \
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**schema.dump(patient), **new_values})
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
                   'message': 'user not found',
               }, 404


def delete_patient(patient_id):
    patient = db.session.query(Patient).join(User)\
        .filter(Patient.id_patient == patient_id)\
        .filter(User.id_user == Patient.id_user)\
        .filter(User.state == True).first()
    if patient:
        try:
            stmt_user = update(User).where(User.id_user == patient.id_user).values(state=False). \
                            execution_options(synchronize_session=False)
            stmt_patient = update(Patient).where(Patient.id_patient == patient_id).values(state=False). \
                execution_options(synchronize_session=False)
            update_changes(stmt_user, stmt_patient)

            return {
                       'status': 'success',
                       'message': 'user deleted',
                   }, 203
        except Exception as e:
            return {
                       'status': 'fail',
                       'message': str(e),
                   }, 401
    else:
        return {
                   'status': 'fail',
                   'message': 'user not found',
               }, 404

