from marshmallow import Schema, fields
from .role import role_schema_detail


class UserDetailSchema(Schema):
    id_user = fields.UUID()
    id_group = fields.UUID()
    id_location = fields.UUID()
    user_name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    name = fields.Str()
    country = fields.Str()
    last_name = fields.Str()
    role = fields.Nested(role_schema_detail)


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
    phone = fields.Str()
    last_name = fields.Str()
    id_group = fields.UUID()
    id_location = fields.Str()
    role = fields.Nested(role_schema_detail)


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


user_detail_schema = UserDetailSchema()
user_list_schema = UserListSchema()
user_update_schema = UserUpdate()
user_create_schema = UserCreateSchema()
