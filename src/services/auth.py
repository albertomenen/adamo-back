from flask import make_response
from .. import db
from ..models import User, Patient
from ..services.blacklist import save_token
from ..services.user import UserSchema
from ..services.patient import PatientListSchema
from flask import jsonify


class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.id_user)
                if auth_token:
                    patients = db.session.query(Patient).join(User).filter(User.id_group == user.id_group).all()
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': str(auth_token),
                        'user': UserSchema().dump(user),
                        'patients': [PatientListSchema().dump(patient) for patient in patients]
                    }
                    return make_response(jsonify(response_object), 200)
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e)
            }
            return response_object, 500

    @staticmethod
    def logout_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id_user=resp['sub']).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id_user,
                        'role': user.role
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
