import datetime
from sqlalchemy import ForeignKey
from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

user_timetable = db.Table('user_timetable',
                          db.Column('id_user', UUID(as_uuid=True), db.ForeignKey('user.id_user'), primary_key=True),
                          db.Column('id_timetable', UUID(as_uuid=True), db.ForeignKey('timetable.id_timetable'),
                                    primary_key=True)
                          )

location_timetable = db.Table('location_timetable',
                              db.Column('id_location', UUID(as_uuid=True), db.ForeignKey('location.id_location'),
                                        primary_key=True),
                              db.Column('id_timetable', UUID(as_uuid=True), db.ForeignKey('timetable.id_timetable'),
                                        primary_key=True)
                              )


class Timetable(db.Model):
    __tablename__ = 'timetable'

    id_timetable = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), nullable=False, unique=True)
    id_group = db.Column(UUID(as_uuid=True), ForeignKey('group.id_group'))
    from_date = db.Column(db.Date(), nullable=False)
    to_date = db.Column(db.Date(), nullable=False)
    monday = db.Column(db.JSON())
    tuesday = db.Column(db.JSON())
    wednesday = db.Column(db.JSON())
    thursday = db.Column(db.JSON())
    friday = db.Column(db.JSON())
    saturday = db.Column(db.JSON())
    sunday = db.Column(db.JSON())
    priority = db.Column(db.Integer(), nullable=False, default=0)

    def __init__(self, id_group, name, from_date, to_date, monday, tuesday, wednesday, thursday, friday, saturday, sunday,
                 priority=0):
        self.id_timetable = uuid.uuid4()
        self.id_group = id_group
        self.name = name
        self.from_date = from_date
        self.to_date = to_date
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday
        self.priority = priority

    def __repr__(self):
        return '<Timetable Name: {} >'.format(self.name)
