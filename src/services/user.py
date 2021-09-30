import os

from flask import jsonify, make_response
from .common import update_changes, save_changes
from .. import db, pagination, flask_bcrypt
from ..models import User, Patient, Role, Location, CodeUser
from sqlalchemy import update, delete
from ..utils.schemas.user import user_update_schema, user_create_schema, user_detail_schema, user_list_schema
from ..utils.messages import Messages


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
                new_user = User(**user_create_schema.dump(data))
                user_code = CodeUser(new_user.id_user)
                save_changes(new_user)
                save_changes(user_code)
                url = os.environ.get('WEB_URL') + '/{}'.format(user_code.id_code_user)

                print(url)
                Messages.send_email(Messages.SendUrl, new_user.email, url)
            except Exception as e:
                return {
                           'status': 'fail',
                           'message': str(e),
                       }, 409
            return make_response(jsonify(user_detail_schema.dump(new_user)), 201)
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
    return pagination.paginate(users, user_list_schema, True)


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
    return jsonify(user_detail_schema.dump(user))


def check_user_code(user_code):
    code = CodeUser.query.filter(CodeUser.id_code_user == user_code).first()
    if code:
        return {
                           'status': 'Ok',
                           'message': 'Exists',
                       }, 200
    else:
        return {
            'status': 'fail',
            'message': 'Doesnt exist',
        }, 404


def change_password(email):
    user = User.query.filter(User.email == email).first()
    if not user:
        return {
            'status': 'Ok'
        }, 200
    user_code = CodeUser(user.id_user)
    save_changes(user_code)
    url = os.environ.get('WEB_URL') + '/{}'.format(user_code.id_code_user)
    try:
        Messages.send_email(Messages.ChangePassword, email, url)
        return {
            'status': 'Ok'
        }, 200
    except Exception as e:
        return {
            'status': 'fail',
            'msg': str(e)
        }, 400


def prueba_email():
    return Messages.send_email(Messages.SendUrl, 'alfonsocuestaalcantara@gmail.com', 'http://google.com')


def set_password(user_code, password):
    code = CodeUser.query.filter(CodeUser.id_code_user == user_code).first()
    user = User.query.filter(User.id_user == code.id_user).first()
    user.password = flask_bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        save_changes(user)
        stmt = delete(CodeUser).where(CodeUser.id_user == code.id_user).execution_options(synchronize_session=False)
        update_changes(stmt)
        Messages.send_email(Messages.ConfirmationEmail, user.email, user.email)
        return {
                           'status': 'Ok',
                           'message': 'Password updated',
                       }, 200
    except Exception as e:
        return {
                   'status': 'fail',
                   'message': str(e)
               }, 401


def update_user(role_code, user_id, data, id_group=None, id_location=None):
    user = get_user_query(role_code, user_id, id_group, id_location)
    if user:
        new_values = user_update_schema.dump(data)
        if new_values:
            try:
                stmt = update(User).where(User.id_user == user_id).values(new_values). \
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**user_detail_schema.dump(user), **new_values})
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
    users = db.session.query(User).join(Role).filter(Role.role_code != 'patient').filter(Role.role_code != 'master').filter(User.state == True).all()
    return pagination.paginate(users, user_list_schema, True)


def get_user(id_user):
    return jsonify(user_detail_schema.dump(User.query.filter_by(id_user=id_user).filter_by(state=True).first()))
