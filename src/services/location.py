from .common import save_changes, update_changes
from .. import pagination
from ..models import Location, Group, Station, Device
from flask import jsonify, make_response
from sqlalchemy import update
from ..utils.schemas.location import location_schema_list, location_schema_update, location_schema_detail, location_schema_create


def save_new_location(id_group, data):
    location = Location.query.filter_by(email=data['email']).first()
    group = Group.query.filter_by(id_group=id_group).first()
    if not location:
        if not group:
            return {
                       'status': 'fail',
                       'message': 'Group doesn\'t exists',
                   }, 401
        try:
            data['id_group'] = id_group
            new_location = Location(**location_schema_create.dump(data))
            save_changes(new_location)
        except:
            return {
                       'status': 'fail',
                       'message': 'Wrong parameters',
                   }, 401
        return make_response(jsonify(location_schema_detail.dump(new_location)), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'location email already exists',
        }
        return response_object, 409


def get_location_from_group(group_id):
    locations = Location.query.filter_by(id_group=group_id).filter_by(state=True).all()
    return pagination.paginate(locations, location_schema_list, True)


def get_all_locations():
    return pagination.paginate(Location.query.all(), location_schema_list, True)


def get_location(id_group, id_location):
    return jsonify(location_schema_detail.dump(Location.query.filter_by(id_location=id_location)
                               .filter_by(id_group=id_group).filter_by(state=True).first()))


def update_location(id_group, id_location, data):
    location = Location.query.filter_by(id_location=id_location).filter_by(id_group=id_group)\
        .filter_by(state=True).first()
    if location:
        new_values = location_schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Location).where(Location.id_location == id_location).values(new_values).\
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**location_schema_detail.dump(location), **new_values})
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
            'message': 'location not found',
        }, 404


def delete_location(id_group, id_location):
    location = Location.query.filter_by(id_location=id_location).filter_by(id_group=id_group)\
        .filter_by(state=True).first()
    if location:
        try:
            stmt_location = update(Location).where(Location.id_location == id_location).values(state=False). \
                execution_options(synchronize_session=False)
            stmt_station = update(Station).where(Station.id_location == id_location).values(state=False)\
                .execution_options(synchronize_session=False)
            stmt_device = update(Device).where(Device.station_id == Station.id_station) \
                .where(Station.id_location == id_location).values(station_id=None). \
                execution_options(synchronize_session=False)
            update_changes(stmt_location, stmt_station, stmt_device)
            return {
                'status': 'success',
                'message': 'location deleted',
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

