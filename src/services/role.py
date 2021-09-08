from src import db, pagination
from .common import update_changes, save_changes
from ..models import Role, User
from flask import jsonify, make_response
from sqlalchemy import update, delete
from ..utils.schemas.role import role_schema_detail, role_schema_update



def save_new_role(data):
    role = Role.query.filter_by(role_code=data['role_code']).first()
    if not role:
        try:
            new_role = Role(**role_schema_update.dump(data))
        except:
            return {
                'status': 'fail',
                'message': 'Wrong parameters passed',
            }
        save_changes(new_role)
        return make_response(jsonify(role_schema_detail.dump(new_role)), 201)
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
            return jsonify(role_schema_detail.dump(role))
        else:
            return make_response('Not found', 404)
    except:
        return make_response('Bad id', 401)


def get_all_roles():
    return pagination.paginate(Role.query.all(), role_schema_detail, True)


def get_role(id_role):
    try:
        role = Role.query.filter_by(id_role=id_role).first()
        if role:
            return jsonify(role_schema_detail.dump(role))
        else:
            return make_response('Not found', 404)
    except:
        return make_response('Bad id', 401)


def update_role(id_role, data):
    role = Role.query.filter_by(id_role=id_role).first()
    if role:
        new_values = role_schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Role).where(Role.id_role == id_role).values(new_values).\
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**role_schema_update.dump(role), **new_values})
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

