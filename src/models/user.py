from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .blacklist import BlacklistToken
from .. import db, flask_bcrypt
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..config import key
import jwt
import datetime


class User(db.Model):
    __tablename__ = 'user'

    id_user = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_group = db.Column(UUID(as_uuid=True), ForeignKey('group.id_group'))
    user_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    state = db.Column(db.Boolean(), default=True, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey('role.id_role'))

    role = relationship("Role")

    def __init__(self, user_name, role_id, phone, email, password, name, last_name, id_group=None):
        self.id_user = uuid.uuid4()
        self.user_name = user_name
        self.role_id = role_id
        self.id_group = id_group
        self.name = name
        self.last_name = last_name
        self.phone = phone
        self.state = True
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def encode_auth_token(id_user):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': str(id_user)
            }
            return jwt.encode(payload, key, algorithm='HS256')
        except:
            return "Not possible to encode auth token"

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, key, algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return '<User Name: {} | email: {} >'.format(self.user_name, self.email)
