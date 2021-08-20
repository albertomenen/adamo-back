from flask import jsonify, make_response
from marshmallow import Schema, fields
from .common import update_changes, save_changes
from .. import db
from ..models import User, Patient, Role, Group
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


class UserCreateSchema(Schema):
    id_group = fields.UUID()
    user_name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    password = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    role_id = fields.UUID()


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
schema_create = UserCreateSchema()


def save_new_user(role_code, data, id_group=None):
    user = User.query.filter_by(email=data['email']).first()
    role = Role.query.filter_by(role_code=role_code).first()
    if not user:
        if role:
            try:
                new_user = User(**schema_create.dump(data))
                new_user.id_role = role.id_role
                new_user.id_group = id_group
                save_changes(new_user)
            except:
                return {
                           'status': 'fail',
                           'message': 'Wrong user parameters',
                       }, 409
            return make_response(jsonify(schema.dump(new_user)), 201)
        else:
            return {
                       'status': 'fail',
                       'message': 'role not exists',
                   }, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'user email already exists',
        }
        return response_object, 409


def get_users_role(role_code, id_group=None):
    users = db.session.query(User).join(Role)\
        .filter(Role.role_code == role_code) \
        .filter(User.role_id == Role.id_role)\
        .filter(User.group_id == id_group)\
        .filter(User.state == True).all()
    return jsonify([schema_list.dump(user) for user in users])


def get_user_role(role_code, user_id, id_group=None):
    user = db.session.query(User).join(Role) \
        .filter(Role.role_code == role_code) \
        .filter(User.role_id == Role.id_role) \
        .filter(User.group_id == id_group)\
        .filter(User.state == True) \
        .filter(User.id_user == user_id).first()
    return jsonify(schema.dump(user))


def update_user(role_code, user_id, data, id_group=None):
    user = db.session.query(User).join(Role) \
        .filter(Role.role_code == role_code) \
        .filter(User.role_id == Role.id_role) \
        .filter(User.id_user == user_id) \
        .filter(User.group_id == id_group)\
        .filter(User.state == True).first()
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


def delete_user(role_code, user_id, id_group=None):
    user = db.session.query(User).join(Role) \
        .filter(Role.role_code == role_code) \
        .filter(User.role_id == Role.id_role) \
        .filter(User.id_user == user_id) \
        .filter(User.group_id == id_group)\
        .filter(User.state == True).first()
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
