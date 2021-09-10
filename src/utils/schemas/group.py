from marshmallow import Schema, fields
from .location import location_schema_list


class GroupCreateSchema(Schema):
    group_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()
    email = fields.Email()


class GroupDetailSchema(Schema):
    id_group = fields.UUID()
    group_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()
    email = fields.Email()
    logo = fields.Str()
    locations = fields.List(fields.Nested(location_schema_list))


class GroupListSchema(Schema):
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    email = fields.Str()
    id_group = fields.UUID()
    group_name = fields.Str()
    locations = fields.List(fields.Nested(location_schema_list))


class GroupUpdateSchema(Schema):
    group_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()


class GroupName(Schema):
    id_group = fields.UUID()
    group_name = fields.Str()

group_name = GroupName()
group_schema_create = GroupCreateSchema()
group_schema_detail = GroupDetailSchema()
group_schema_list = GroupListSchema()
group_schema_update = GroupUpdateSchema()
