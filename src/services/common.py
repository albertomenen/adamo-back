from marshmallow import Schema, fields

from .. import db


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def update_changes(*stmt):
    for s in stmt:
        db.session.execute(s)
    db.session.commit()
