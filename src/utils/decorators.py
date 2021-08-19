from functools import wraps
from flask import request
from ..models import User
from ..services.auth import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def check_role(request_data, role_to_check):
    data, status = Auth.get_logged_in_user(request_data)
    token = data.get('data')

    if not token:
        return data, status

    role = token.get('role')
    if not role or not role.__dict__.get(role_to_check):
        response_object = {
            'status': 'fail',
            'message': 'not permission'
        }
        return response_object, 401


def manage_practice_manager(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_practice_manager')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_sysadmin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_sysadmin')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated
