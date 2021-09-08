from marshmallow import Schema, fields


class LocationCreateSchema(Schema):
    location_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()
    email = fields.Email()
    state = fields.Boolean()
    id_group = fields.UUID()


class LocationDetailSchema(Schema):
    id_location = fields.UUID()
    location_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()
    email = fields.Email()
    state = fields.Boolean()
    id_group = fields.UUID()


class LocationListSchema(Schema):
    id_location = fields.UUID()
    location_name = fields.Str()
    address = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()
    email = fields.Str()
    city = fields.Str()
    town = fields.Str()



class LocationUpdateSchema(Schema):
    location_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    town = fields.Str()
    phone = fields.Str()
    contact_name = fields.Str()


location_schema_create = LocationCreateSchema()
location_schema_detail = LocationDetailSchema()
location_schema_list = LocationListSchema()
location_schema_update = LocationUpdateSchema()
