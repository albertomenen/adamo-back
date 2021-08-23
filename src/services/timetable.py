from flask import jsonify, make_response
from src import db
from .common import save_changes
from marshmallow import Schema, fields
from sqlalchemy import update
import datetime
import calendar


class Interval(Schema):
    from_hour = fields.Str()
    to_hour = fields.Str()


class TimetableSchema(Schema):
    id_timetable = fields.UUID()
    name = fields.Str()
    from_date = fields.Date()
    to_date = fields.Date()
    monday = fields.List(fields.Nested(Interval()))
    tuesday = fields.List(fields.Nested(Interval()))
    wednesday = fields.List(fields.Nested(Interval()))
    thursday = fields.List(fields.Nested(Interval()))
    friday = fields.List(fields.Nested(Interval()))
    saturday = fields.List(fields.Nested(Interval()))
    sunday = fields.List(fields.Nested(Interval()))



class TimetableListSchema(Schema):
    id_timetable = fields.UUID()
    from_date = fields.Date()
    to_date = fields.Date()
    name = fields.Str()


schema = TimetableSchema()
schema_list = TimetableListSchema()


def save_new_timetable(id_group, data):
    try:
        data['id_group'] = id_group
        new_timetable = Timetable(**data)
        save_changes(new_timetable)
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e),
        }
        return response_object, 409
    return make_response(jsonify(schema.dump(new_timetable)), 201)


def get_timetables(id_group):
    timetables = Timetable.query.filter_by(id_group=id_group).all()
    return jsonify([schema_list.dump(timetable) for timetable in timetables])


def get_timetable(id_group, id_timetable):
    timetable = Timetable.query.filter_by(id_timetable=id_timetable).filter_by(id_group=id_group).first()
    return jsonify(schema.dump(timetable))


def get_timetable_by_date(timetables, date):
    best_timetable, priority = None, -1
    for timetable in timetables:
        if timetable.from_date <= date <= timetable.to_date and timetable.priority > priority:
            best_timetable = timetable
            priority = timetable.priority
    return schema.dump(best_timetable)


def get_timetable_intersection(timetable_1, timetable_2):
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        pass  # TODO


def get_week_timetable_from_medic(id_location, id_medic, first_day):
    year, month, day = first_day.split('-')
    first_day = datetime.date(int(year), int(month), int(day))
    end_day = first_day + datetime.timedelta(days=6)
    # location_timetables = Timetable.query.filter(Timetable.locations.any(id_location=id_location)).all()
    medic_timetables = Timetable.query.filter(Timetable.users.any(id_user=id_medic)).all()
    timetable_result = {}
    for i in range(7):
        actual_date = first_day + datetime.timedelta(days=i)
        weekday = calendar.day_name[actual_date.weekday()].lower()
        # location_timetable = get_timetable_by_date(location_timetables, actual_date)
        medic_timetable = get_timetable_by_date(medic_timetables, actual_date)
        timetable_result[weekday] = get_timetable_by_date(medic_timetables, actual_date)[weekday]
        # timetable[weekday] = get_timetable_intersection(location_timetable, medic_timetable)
    return timetable_result
