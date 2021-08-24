from marshmallow import Schema, fields

from .. import db


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def update_changes(*stmt):
    for s in stmt:
        db.session.execute(s)
    db.session.commit()


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