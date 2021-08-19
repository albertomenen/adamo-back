from flask import jsonify, make_response
from marshmallow import Schema, fields
from .common import update_changes, save_changes
from ..models import User, Patient
from .role import RoleSchema
from sqlalchemy import update


class UserSchema(Schema):
    id_user = fields.UUID()
    id_group = fields.UUID()
    user_name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    name = fields.Str()
    last_name = fields.Str()
    role = fields.Nested(RoleSchema())


class UserListSchema(Schema):
    id_user = fields.UUID()
    user_name = fields.Str()
    email = fields.Email()
    name = fields.Str()
    last_name = fields.Str()
    id_group = fields.UUID()


class UserUpdate(Schema):
    id_group = fields.UUID()
    user_name = fields.Str()
    phone = fields.Str()
    state = fields.Boolean()
    name = fields.Str()
    last_name = fields.Str()
    role_id = fields.UUID()


schema = UserSchema()
schema_list = UserListSchema()
schema_update = UserUpdate()


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        try:
            new_user = User(**data)
        except:
            return {
                       'status': 'fail',
                       'message': 'Wrong user parameters',
                   }, 409
        save_changes(new_user)
        return make_response(jsonify(schema.dump(new_user)), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'user email already exists',
        }
        return response_object, 409


def update_user(user_id, data):
    user = User.query.filter_by(id_user=user_id).filter_by(state=True).first()
    if user:
        new_values = schema_update.dump(data)
        if new_values:
            try:
                stmt = update(User).where(User.id_user == user_id).values(new_values). \
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**schema.dump(user), **new_values})
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


def delete_user(user_id):
    user = User.query.filter_by(id_user=user_id).filter_by(state=True).first()
    if user:
        try:
            stmt_user = update(User).where(User.id_user == user_id).values(state=False). \
                            execution_options(synchronize_session=False)
            stmt_patient = update(Patient).where(Patient.id_user == user_id).values(state=False). \
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


def get_users():
    return jsonify([schema_list.dump(user) for user in User.query.filter_by(state=True).all()])


def get_user(id_user):
    return jsonify(schema.dump(User.query.filter_by(id_user=id_user).filter_by(state=True).first()))
