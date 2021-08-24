from flask import jsonify, make_response
from marshmallow import Schema, fields
from .common import update_changes, save_changes
from .timetable import TimetableSchema, TimetableListSchema
from .. import db, pagination
from ..models import User, Patient, Role, Group, Location
from .role import RoleSchema
from sqlalchemy import update


class UserDetailSchema(Schema):
    id_user = fields.UUID()
    id_group = fields.UUID()
    id_location = fields.UUID()
    user_name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    name = fields.Str()
    last_name = fields.Str()
    country = fields.Str()
    role = fields.Nested(RoleSchema())


class UserTimetableSchema(Schema):
    id_user = fields.UUID()
    timetables = fields.List(fields.Nested(TimetableListSchema()))


class UserSchema(Schema):
    id_user = fields.UUID()
    id_group = fields.UUID()
    id_location = fields.UUID()
    user_name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    name = fields.Str()
    country = fields.Str()
    last_name = fields.Str()


class UserCreateSchema(Schema):
    id_group = fields.UUID()
    id_location = fields.UUID()
    user_name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    password = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    country = fields.Str()
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
    id_location = fields.UUID()
    user_name = fields.Str()
    phone = fields.Str()
    state = fields.Boolean()
    name = fields.Str()
    last_name = fields.Str()
    country = fields.Str()
    role_id = fields.UUID()


schema = UserSchema()
schema_detail = UserDetailSchema()
schema_list = UserListSchema()
schema_update = UserUpdate()
schema_create = UserCreateSchema()
schema_timetable = UserTimetableSchema()


def save_new_user(role_code, data, id_group=None, id_location=None):
    user = User.query.filter_by(email=data['email']).first()
    role = Role.query.filter_by(role_code=role_code).first()
    if not user:
        if id_location and not Location.query.filter_by(id_location=id_location).filter_by(id_group=id_group).first():
            return {
                       'status': 'fail',
                       'message': 'Location not foundd',
                   }, 404
        if role:
            try:
                data['role_id'] = role.id_role
                data['id_group'] = id_group
                data['id_location'] = id_location
                new_user = User(**schema_create.dump(data))
                save_changes(new_user)
            except Exception as e:
                return {
                           'status': 'fail',
                           'message': str(e),
                       }, 409
            return make_response(jsonify(schema_detail.dump(new_user)), 201)
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


def get_users_role(role_code, id_group=None, id_location=None):
    users = db.session.query(User).join(Role) \
        .filter(Role.role_code == role_code) \
        .filter(User.role_id == Role.id_role) \
        .filter(User.id_location == id_location) \
        .filter(User.id_group == id_group) \
        .filter(User.state == True).all()
    return pagination.paginate(users, schema_list, True)


def get_user_query(role_code, user_id, id_group=None, id_location=None):
    return db.session.query(User).join(Role) \
        .filter(Role.role_code == role_code) \
        .filter(User.role_id == Role.id_role) \
        .filter(User.id_group == id_group) \
        .filter(User.id_location == id_location) \
        .filter(User.state == True) \
        .filter(User.id_user == user_id).first()


def get_user_role(role_code, user_id, id_group=None, id_location=None):
    user = get_user_query(role_code, user_id, id_group, id_location)
    return jsonify(schema.dump(user))


def update_user(role_code, user_id, data, id_group=None, id_location=None):
    user = get_user_query(role_code, user_id, id_group, id_location)
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


# def set_user_timetable(user_id, id_group, id_location, id_timetable):
#     user = User.query.filter_by(id_group=id_group).filter_by(id_location=id_location).filter_by(id_user=user_id).first()
#     timetable = Timetable.query.filter_by(id_group=id_group).filter_by(id_timetable=id_timetable).first()
#     if user:
#         if timetable:
#             try:
#                 user.timetables.append(timetable)
#                 save_changes(user)
#                 return jsonify(schema_timetable.dump(user))
#             except:
#                 return {
#                            'status': 'fail',
#                            'message': 'Update failed',
#                        }, 401
#         else:
#             return {
#                        'status': 'fail',
#                        'message': 'timetable not found',
#                    }, 401
#
#     else:
#         return {
#                    'status': 'fail',
#                    'message': 'user not found',
#                }, 404


def delete_user(role_code, user_id, id_group=None, id_location=None):
    user = get_user_query(role_code, user_id, id_group, id_location)
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
    return pagination.paginate(User.query.all(), schema_list, True)


def get_user(id_user):
    return jsonify(schema_detail.dump(User.query.filter_by(id_user=id_user).filter_by(state=True).first()))
