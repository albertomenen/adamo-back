from src import db, pagination
from .common import update_changes, save_changes
from ..models import Role, User
from flask import jsonify, make_response
from marshmallow import Schema, fields
from sqlalchemy import update, delete


class RoleSchema(Schema):
    id_role = fields.UUID()
    role_name = fields.Str()
    role_code = fields.Str()
    login_in_station = fields.Boolean()
    manage_practice_manager = fields.Boolean()
    manage_mp = fields.Boolean()
    manage_nmp = fields.Boolean()
    manage_patient = fields.Boolean()
    manage_sysadmin = fields.Boolean()
    manage_dev = fields.Boolean()
    get_patient = fields.Boolean()
    list_patient = fields.Boolean()
    detail_patient = fields.Boolean()
    manage_treatment = fields.Boolean()
    run_sesion = fields.Boolean()
    user_logout = fields.Boolean()
    app_login = fields.Boolean()
    app_select_patient = fields.Boolean()
    app_detail_patient = fields.Boolean()
    debug_app_hmi = fields.Boolean()
    manage_station = fields.Boolean()
    manage_group = fields.Boolean()
    manage_practice = fields.Boolean()


class RoleUpdateSchema(Schema):
    role_name = fields.Str()
    role_code = fields.Str()
    login_in_station = fields.Boolean()
    manage_practice_manager = fields.Boolean()
    manage_mp = fields.Boolean()
    manage_nmp = fields.Boolean()
    manage_patient = fields.Boolean()
    manage_sysadmin = fields.Boolean()
    manage_dev = fields.Boolean()
    get_patient = fields.Boolean()
    list_patient = fields.Boolean()
    detail_patient = fields.Boolean()
    manage_treatment = fields.Boolean()
    run_sesion = fields.Boolean()
    user_logout = fields.Boolean()
    app_login = fields.Boolean()
    app_select_patient = fields.Boolean()
    app_detail_patient = fields.Boolean()
    debug_app_hmi = fields.Boolean()
    manage_station = fields.Boolean()
    manage_group = fields.Boolean()
    manage_practice = fields.Boolean()


schema = RoleSchema()
schema_update = RoleUpdateSchema()


def save_new_role(data):
    role = Role.query.filter_by(role_code=data['role_code']).first()
    if not role:
        try:
            new_role = Role(**data)
        except:
            return {
                'status': 'fail',
                'message': 'Wrong parameters passed',
            }
        save_changes(new_role)
        return make_response(jsonify(schema.dump(new_role)), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'role code already exists',
        }
        return response_object, 409


def get_role_from_user(user_id):
    try:
        role = db.session.query(Role).join(User).filter(User.id_user == user_id).first()
        if role:
            return jsonify(schema.dump(role))
        else:
            return make_response('Not found', 404)
    except:
        return make_response('Bad id', 401)


def get_all_roles():
    return pagination.paginate(Role.query.all(), schema, True)


def get_role(id_role):
    try:
        role = Role.query.filter_by(id_role=id_role).first()
        if role:
            return jsonify(schema.dump(role))
        else:
            return make_response('Not found', 404)
    except:
        return make_response('Bad id', 401)


def update_role(id_role, data):
    role = Role.query.filter_by(id_role=id_role).first()
    if role:
        new_values = schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Role).where(Role.id_role == id_role).values(new_values).\
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**schema.dump(role), **new_values})
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
            'message': 'user not found',
        }, 404


def delete_role(role_id):
    role = Role.query.filter_by(id_role=role_id).first()
    users = User.query.filter_by(role_id=role_id).filter_by(state=True).first()
    if role:
        if not users:
            try:
                stmt = delete(Role).where(Role.id_role == role_id).execution_options(synchronize_session=False)
                update_changes(stmt)
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
                    'message': 'Can\'t delete a role in use'
                }, 401
    else:
        return {
            'status': 'fail',
            'message': 'user not found',
        }, 404

