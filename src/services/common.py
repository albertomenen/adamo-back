from marshmallow import Schema, fields

from .. import db


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def update_changes(*stmt):
    for s in stmt:
        db.session.execute(s)
    db.session.commit()


def get_points(points, n, reverse=False):
    result = [points]
    if reverse:
        result.append(points[::-1])
        result *= n // 2
        if n % 2:
            result.append(points)
    else:
        result *= n
    return result