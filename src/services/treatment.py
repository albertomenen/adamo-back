from flask import jsonify, make_response
from src import db, pagination
from .common import save_changes, update_changes
from ..models import Treatment, User, Patient, PAlias
from sqlalchemy import update, delete
from ..utils.s3 import upload_to_aws, get_from_aws
from ..utils.schemas.patient import patient_schema_list
from ..utils.schemas.treatment import treatment_schema_list, treatment_schema_create, treatment_schema_update, \
    treatment_schema_detail
from .offset.from_model_to_offset import from_model_to_offset
from .offset.worker_offset import get_offset


def get_points(points, n, reverse=False):
    result = [points]
    if reverse:
        result.append(points[::-1])
        result *= n // 2
        if n % 2 == 1:
            result.append(points)
    else:
        result *= n
    return result


def save_new_treatment(id_group, patient_id, data):
    palias = db.session.query(PAlias).join(Patient).join(User) \
        .filter(PAlias.patient == patient_id) \
        .filter(Patient.id_patient == patient_id) \
        .filter(User.id_user == Patient.id_user) \
        .filter(User.id_group == id_group).filter(User.state == True).first()
    if palias:
        try:
            data['id_patient'] = palias.id_palias
            data['points'] = get_points(data['points'], data.get('cicles', 1), data.get('reverse', False))
            treatment_data = treatment_schema_create.dump(data)
            new_treatment = Treatment(**treatment_schema_create.dump(treatment_data))

            images_directory = '{}/{}/'.format(palias.id_palias, new_treatment.id_treatment)
            for image in ['image_3D_depth', 'image_3D_color', 'image_thermic', 'image_thermic_data']:
                if image in data:
                    if upload_to_aws(data[image], images_directory + image + '.bin'):
                        new_treatment.__dict__[image] = images_directory + image + '.bin'
                    else:
                        raise Exception('Cant upload ' + image + '.bin')

            save_changes(new_treatment)
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e),
            }
            return response_object, 409
        return make_response(jsonify(treatment_schema_detail.dump(new_treatment)), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Patient doesn\'t exists',
        }
        return response_object, 409


def get_treatments():
    return jsonify([treatment_schema_list.dump(treatment) for treatment in Treatment.query.all()])


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

    return pagination.paginate(treatments, treatment_schema_list, True)


def get_patient_from_alias(alias):
    return db.session.query(Patient).join(PAlias) \
        .filter(Patient.id_patient == PAlias.patient).filter(PAlias.id_palias == alias).first()


def get_treatment(id_group, id_patient, id_treatment):
    treatment = treatment_schema_detail.dump(get_query_treatment(id_group, id_patient, id_treatment))
    patient = get_patient_from_alias(treatment['id_patient'])
    treatment['patient'] = patient_schema_list.dump(patient)

    if treatment.get('image_thermic'):
        treatment['image_thermic'] = get_from_aws(treatment.get('image_thermic'))
    return jsonify(treatment)


def update_treatment(id_group, id_patient, id_treatment, data):
    treatment = get_query_treatment(id_group, id_patient, id_treatment)
    if treatment:
        new_values = treatment_schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Treatment).where(Treatment.id_treatment == id_treatment).values(new_values). \
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                if new_values.get('state') == 'started':
                    patient = get_patient_from_alias(treatment.id_patient)
                    stmt = update(Patient).where(Patient.id_patient == id_patient).values(
                        {'active_treatments': patient.active_treatments + 1}). \
                        execution_options(synchronize_session=False)
                    update_changes(stmt)
                elif new_values.get('state') == 'finished':
                    patient = get_patient_from_alias(treatment.id_patient)
                    stmt = update(Patient).where(Patient.id_patient == id_patient).values(
                        {'active_treatments': patient.active_treatments - 1}). \
                        execution_options(synchronize_session=False)
                    update_changes(stmt)
                return jsonify({**treatment_schema_detail.dump(treatment), **new_values})
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


def delete_treatment(id_group, id_patient, id_treatment):
    treatment = get_query_treatment(id_group, id_patient, id_treatment)
    if treatment:
        if treatment.current_session_number == 0:
            try:
                stmt = delete(Treatment).where(Treatment.id_treatment == id_treatment) \
                    .execution_options(synchronize_session=False)
                update_changes(stmt)
                patient = get_patient_from_alias(treatment.id_patient)
                stmt = update(Patient).where(Patient.id_patient == id_patient).values(
                    {'active_treatments': patient.active_treatments - 1}). \
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return {
                           'status': 'success',
                           'message': 'treatment deleted',
                       }, 203
            except Exception as e:
                return {
                           'status': 'fail',
                           'message': str(e),
                       }, 401
        else:
            try:
                stmt = update(Treatment).where(Treatment.id_treatment == id_treatment).values({'state': 'canceled'}). \
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                patient = get_patient_from_alias(treatment.id_patient)
                stmt = update(Patient).where(Patient.id_patient == id_patient).values(
                    {'active_treatments': patient.active_treatments - 1}). \
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return {
                           'status': 'success',
                           'message': 'treatment interrupted',
                       }, 203
            except Exception as e:
                return {
                           'status': 'fail',
                           'message': str(e),
                       }, 401
    else:
        return {
                   'status': 'fail',
                   'message': 'treatment not found',
               }, 404


def get_treatment_offset(id_group, id_patient, id_treatment, new_treatment):
    treatment = get_query_treatment(id_group, id_patient, id_treatment)
    if treatment:
        try:
            data_to_offset = from_model_to_offset(treatment, new_treatment)
            result = get_offset(data_to_offset)
        except Exception as e:
            return {
                       'status': 'fail',
                       'message': str(e),
                   }, 401
        return jsonify(result)
    else:
        return {
                   'status': 'fail',
                   'message': 'Cant find treatment',
               }, 404
