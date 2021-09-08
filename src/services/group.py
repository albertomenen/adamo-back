from .common import update_changes, save_changes
from .. import pagination
from ..models import Group, User, Location, Station, Device
from flask import jsonify, make_response
from sqlalchemy import update

from ..utils.s3 import upload_to_aws, get_from_aws
from ..utils.schemas.group import group_schema_list, group_schema_update, group_schema_create, group_schema_detail


def save_new_group(data):
    group = Group.query.filter_by(email=data['email']).first()
    if not group:
        try:
            new_group = Group(**group_schema_create.dump(data))
            images_directory = '{}.png'.format(new_group.id_group)
            if 'logo' in data:
                if upload_to_aws(data['logo'], images_directory):
                    new_group.logo = images_directory
                else:
                    raise Exception('Cant upload logo')

            save_changes(new_group)
        except Exception as e:
            return {
                       'status': 'fail',
                       'message': str(e),
                   }, 401
        return make_response(jsonify(group_schema_detail.dump(new_group)), 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'group email already exists',
        }
        return response_object, 409


def get_groups():
    return pagination.paginate(Group.query.all(), group_schema_list, True)


def get_group(id_group):
    group = group_schema_detail.dump(Group.query.filter_by(id_group=id_group).first())
    if group.get('logo'):
        group['logo'] = get_from_aws(group.get('logo'))
    return jsonify(group)


def update_group(id_group, data):
    group = Group.query.filter_by(id_group=id_group).first()
    if group:
        new_values = group_schema_update.dump(data)
        if new_values:
            try:
                stmt = update(Group).where(Group.id_group == id_group).values(new_values). \
                    execution_options(synchronize_session=False)
                update_changes(stmt)
                return jsonify({**group_schema_detail.dump(group), **new_values})
            except Exception as e:
                return {
                           'status': 'fail',
                           'message': str(e),
                       }, 401
        else:
            return {
                       'status': 'fail',
                       'message': 'Nothing to update',
                   }, 401

    else:
        return {
                   'status': 'fail',
                   'message': 'user not found',
               }, 404


def delete_group(group_id):
    group = Group.query.filter_by(id_group=group_id).first()
    users = User.query.filter_by(id_group=group_id).filter_by(state=True).first()
    if group:
        if not users:
            try:
                stmt_user = update(Group).where(Group.id_group == group_id).values(state=False). \
                    execution_options(synchronize_session=False)
                stmt_location = update(Location).where(Location.id_group == group_id).values(state=False). \
                    execution_options(synchronize_session=False)
                stmt_station = update(Station).where(Station.id_location == Location.id_location) \
                    .where(Location.id_group == group_id).values(state=False) \
                    .execution_options(synchronize_session=False)
                stmt_device = update(Device).where(Device.station_id == Station.id_station) \
                    .where(Station.id_location == Location.id_location) \
                    .where(Location.id_group == group_id).values(station_id=None). \
                    execution_options(synchronize_session=False)
                update_changes(stmt_user, stmt_location, stmt_station, stmt_device)
                return {
                           'status': 'success',
                           'message': 'user deleted',
                       }, 203
            except Exception as e:
                return {
                           'status': 'fail',
                           'message': str(e),
                       }, 401
        else:
            return {
                       'status': 'fail',
                       'message': 'Can\'t delete a group in use'
                   }, 401
    else:
        return {
                   'status': 'fail',
                   'message': 'user not found',
               }, 404
