from flask import jsonify, make_response
from src import db
from .common import save_changes, update_changes
from .treatment import get_query_treatment, update_treatment
from ..models import Date, Location, Group
from marshmallow import Schema, fields
from sqlalchemy import update, delete


class DateSchema(Schema):
    id_date = fields.UUID()
    id_medic = fields.UUID()
    id_patient = fields.UUID()
    id_station = fields.UUID()
    day = fields.Str()
    from_hour = fields.Str()
    to_hour = fields.Str()
    presented = fields.Boolean()


class DateListSchema(Schema):
    id_date = fields.UUID()
    day = fields.Str()
    from_hour = fields.Str()
    to_hour = fields.Str()
    id_patient = fields.UUID()
    id_station = fields.UUID()
    id_medic = fields.UUID()


class DateUpdateSchema(Schema):
    day = fields.Str()
    from_hour = fields.Str()
    to_hour = fields.Str()
    id_station = fields.UUID()
    id_medic = fields.UUID()


schema = DateSchema()
schema_list = DateListSchema()
schema_update = DateUpdateSchema()


def save_new_date(id_group, id_patient, id_treatment, data):
    treatment = get_query_treatment(id_group, id_patient, id_treatment)
    if treatment:
        try:
            data['id_patient'] = id_patient
            data['id_treatment'] = id_treatment
            new_date = Date(**data)
            save_changes(new_date)
            update_treatment(id_group, id_patient, id_treatment, {'next_session': new_date.id_date})
            return make_response(jsonify(schema.dump(new_date)), 201)
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message':  str(e),
            }
            return response_object, 409
    else:
        return {
                'status': 'fail',
                'message': 'Treatment not found',
            }


def get_dates_medic_station(id_station, from_date, to_date):
    dates = Date.query.filter(Date.day >= from_date) \
        .filter(Date.day <= to_date) \
        .filter(Date.id_station == id_station).all()
    return jsonify([schema_list.dump(date) for date in dates])


def get_date(id_station, id_date):
    date = Date.query.filter_by(id_date=id_date).filter_by(id_station=id_station).first()
    return jsonify(schema.dump(date))


def update_date(id_station, id_date, data):
    date = Date.query.filter_by(id_date=id_date).filter_by(id_station=id_station).first()
    if date:
        new_values = schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Date).where(Date.id_date == id_date).values(new_values).\
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**schema.dump(date), **new_values})
            except Exception as e:
                return {
                           'status': 'fail',
                           'message': str(e),
                       }, 401
        else:
            return {
                'status': 'fail',
                'message': 'Nothin to update',
            }, 401

    else:
        return {
            'status': 'fail',
            'message': 'date not found',
        }, 404


def delete_date(id_station, id_date):
    date = Date.query.filter_by(id_date=id_date).filter_by(id_station=id_station).first()
    if date:
        try:
            stmt = delete(Date).where(Date.id_date == id_date).execution_options(synchronize_session=False)
            update_changes(stmt)
            return {
                'status': 'success',
                'message': 'date deleted',
            }, 203
        except Exception as e:
            return {
                'status': 'fail',
                'message': str(e),
            }, 401
    else:
        return {
            'status': 'fail',
            'message': 'date not found',
        }, 404