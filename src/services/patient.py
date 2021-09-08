from flask import jsonify, make_response
from src import db, pagination
from .common import update_changes, save_changes
from ..models import Patient, User, PAlias, Role, Group, Treatment
from ..utils.schemas.treatment import treatment_schema_list
from ..utils.schemas.user import user_create_schema, user_update_schema
from ..utils.schemas.patient import patient_schema_list, patient_schema_update, patient_schema_create, patient_schema_detail
from sqlalchemy import update
from ..utils.filter import filtering


def save_new_patient(id_group, data):
    patient = Patient.query.filter_by(email=data['email']).first()
    group = Group.query.filter_by(id_group=id_group).first()
    if not patient:
        if not group:
            return {
                       'status': 'fail',
                       'message': 'Group doesn\'t exists',
                   }, 401
        try:
            data['id_group'] = id_group
            data['role_id'] = Role.query.filter_by(role_code='patient').first().id_role
            new_user = User(**user_create_schema.dump(data))
            data['id_user'] = new_user.id_user
            new_patient = Patient(**patient_schema_create.dump(data))
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
        return make_response(jsonify(patient_schema_detail.dump(new_patient)), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'patient email already exists',
        }
        return response_object, 409


def get_patients():
    patient_list = db.session.query(Patient).join(User) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.state == True).all()
    return pagination.paginate(patient_list, patient_schema_list, True)


def get_patients_by_group(id_group, filters=()):
    patient_list = db.session.query(Patient).join(User) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.state == True) \
        .filter(User.id_group == id_group).all()
    patient_list = filtering(patient_list, filters)
    return pagination.paginate(patient_list, patient_schema_list, True)


def get_patient(id_group, id_patient):
    patient = db.session.query(Patient).join(User) \
        .filter(Patient.id_patient == id_patient) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.state == True) \
        .filter(User.id_group == id_group).first()
    patient = patient_schema_detail.dump(patient)
    treatments = db.session.query(Treatment).join(PAlias) \
        .filter(Treatment.id_patient == PAlias.id_palias).filter(PAlias.patient == id_patient).all()
    patient['treatments'] = [treatment_schema_list().dump(treatment) for treatment in treatments]
    return jsonify(patient)


def update_patient(id_group, patient_id, data):
    patient = db.session.query(Patient).join(User) \
        .filter(Patient.id_patient == patient_id) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.state == True) \
        .filter(User.id_group == id_group).first()
    if patient:
        new_values = patient_schema_update.dump(data)
        new_values_user = user_update_schema.dump(data)
        if new_values:
            try:
                stmt = update(Patient).where(Patient.id_patient == patient_id).values(new_values). \
                    execution_options(synchronize_session=False)
                stmt_user = update(User).where(Patient.id_patient == patient_id).where(Patient.id_user == User.id_user) \
                    .values(new_values_user).execution_options(synchronize_session=False)
                update_changes(stmt, stmt_user)
                return jsonify({**patient_schema_detail.dump(patient), **new_values})
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


def delete_patient(id_group, patient_id):
    patient = db.session.query(Patient).join(User) \
        .filter(Patient.id_patient == patient_id) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.state == True) \
        .filter(User.id_group == id_group).first()
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
