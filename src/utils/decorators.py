from functools import wraps
from flask import request
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


def login_in_station(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'login_in_station')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_practice_manager(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_practice_manager')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_mp(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_mp')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_nmp(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_nmp')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_patient(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_patient')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_sys_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_sys_admin')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_dev(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_dev')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def get_patient(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'get_patient')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def list_patient(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'list_patient')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def detail_patient(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'detail_patient')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_treatment(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_treatment')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def run_sesion(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'run_sesion')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def session_adjustment(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'session_adjustment')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def session_stop(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'session_stop')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def user_logout(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'user_logout')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def app_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'app_login')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def app_select_patient(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'app_select_patient')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def app_detail_patient(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'app_detail_patient')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def debug_app_hmi(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'debug_app_hmi')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_station(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_station')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_group(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_group')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_location(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_location')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_devices(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_devices')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated


def manage_roles(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        not_permission = check_role(request, 'manage_roles')
        if not_permission:
            return not_permission
        return f(*args, **kwargs)

    return decorated
