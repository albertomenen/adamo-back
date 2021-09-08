from flask import jsonify, make_response
from .common import save_changes, update_changes
from .treatment import get_query_treatment, update_treatment
from ..models import Date
from sqlalchemy import update, delete
from ..utils.schemas.date import date_schema_list, date_schema_detail, date_schema_update, date_schema_create


def save_new_date(id_group, id_patient, id_treatment, data):
    treatment = get_query_treatment(id_group, id_patient, id_treatment)
    if treatment:
        try:
            data['id_patient'] = id_patient
            data['id_treatment'] = id_treatment
            new_date = Date(**date_schema_create.dump(data))
            save_changes(new_date)
            update_treatment(id_group, id_patient, id_treatment, {'next_session_date': new_date.day})
            return make_response(jsonify(date_schema_detail.dump(new_date)), 201)
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
    return jsonify([date_schema_list.dump(date) for date in dates])


def get_date(id_station, id_date):
    date = Date.query.filter_by(id_date=id_date).filter_by(id_station=id_station).first()
    return jsonify(date_schema_detail.dump(date))


def update_date(id_station, id_date, data):
    date = Date.query.filter_by(id_date=id_date).filter_by(id_station=id_station).first()
    if date:
        new_values = date_schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Date).where(Date.id_date == id_date).values(new_values).\
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**date_schema_detail.dump(date), **new_values})
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