from marshmallow import Schema, fields


class Points(Schema):
    duration = fields.Float()
    gradual = fields.Boolean()
    x = fields.Float()
    y = fields.Float()
    z = fields.Float()
    rx = fields.Float()
    ry = fields.Float()
    rz = fields.Float()
    height = fields.Float()
    pressure = fields.Float()
    alias = fields.Str()


point_schema = Points()
