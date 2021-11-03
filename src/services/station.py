from flask import jsonify, make_response
from src import db, pagination
from .common import save_changes, update_changes
from ..models import Station, Location, Group, Device
from sqlalchemy import update
from ..utils.schemas.station import station_schema_detail, station_schema_list, station_schema_update, station_schema_create


def save_new_station(id_group, id_location, data):
    location = Location.query.filter_by(id_location=id_location).filter_by(id_group=id_group).first()
    if not location:
        return {
                   'status': 'fail',
                   'message': 'Location doesn\'t exists',
               }, 401
    try:
        data['id_location'] = location.id_location
        new_station = Station(**station_schema_create.dump(data))
        save_changes(new_station)
    except:
        response_object = {
            'status': 'fail',
            'message': 'Bad parameters',
        }
        return response_object, 409
    return make_response(jsonify(station_schema_detail.dump(new_station)), 201)


def get_stations(id_group, id_location):
    stations = db.session.query(Station).join(Location)\
        .filter(Location.id_group == id_group)\
        .filter(Station.id_location == id_location)\
        .filter(Station.state == True).all()
    return pagination.paginate(stations, station_schema_list, True)


def get_station(id_group, id_location, id_station):
    station = db.session.query(Station).join(Location).join(Device) \
        .filter(Location.id_group == id_group) \
        .filter(Station.id_location == id_location)\
        .filter(Station.id_station == id_station)\
        .filter(Station.state == True).first()
    return jsonify(station_schema_detail.dump(station))


def update_station(id_group, id_location, id_station, data):
    station = db.session.query(Station).join(Group) \
        .filter(Location.id_group == id_group) \
        .filter(Station.id_location == id_location)\
        .filter(Station.id_station == id_station)\
        .filter(Station.state == True).first()
    if station:
        new_values = station_schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Station).where(Station.id_station == id_station).values(new_values).\
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**station_schema_detail.dump(station), **new_values})
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
            'message': 'user not found',
        }, 404


def delete_station(id_group, id_location, id_station):
    station = db.session.query(Station).join(Location) \
        .filter(Location.id_group == id_group) \
        .filter(Station.id_location == id_location) \
        .filter(Station.id_station == id_station) \
        .filter(Station.state == True).first()
    if station:
        try:
            stmt_station = update(Station).where(Station.id_location == id_location).values(state=False)\
                .execution_options(synchronize_session=False)
            stmt_device = update(Device).where(Device.station_id == Station.id_station) \
                .where(Station.id_location == id_location).values(station_id=None). \
                execution_options(synchronize_session=False)
            update_changes(stmt_station, stmt_device)
            return {
                'status': 'success',
                'message': 'station deleted',
            }, 203
        except Exception as e:
            return {
                'status': 'fail',
                'message': str(e),
            }, 401
    else:
        return {
            'status': 'fail',
            'message': 'user not found',
        }, 404