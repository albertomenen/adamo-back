from marshmallow import Schema, fields


class SystemCreateSchema(Schema):
    system_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()
    email = fields.Email()


class SystemDetailSchema(Schema):
    id_system = fields.UUID()
    system_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()
    email = fields.Email()


class SystemUpdateSchema(Schema):
    system_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()


class SystemListSchema(Schema):
    id_system = fields.UUID()
    system_name = fields.Str()
    email = fields.Email()


system_schema_create = SystemCreateSchema()
system_schema_update = SystemUpdateSchema()
system_schema_list = SystemListSchema()
system_schema_detail = SystemDetailSchema()
