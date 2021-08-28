import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Session(db.Model):
    __tablename__ = 'session'

    id_session = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medic = db.Column(UUID(as_uuid=True), ForeignKey('user.id_user'), nullable=False)
    heating_duration = db.Column(db.REAL())
    # image_3D_color = db.Column(db.String(50), nullable=False, unique=True)
    # image_thermic = db.Column(db.String(12), nullable=False)
    # image_3D_depth = db.Column(db.String(150), nullable=False)
    points = db.Column(db.JSON())
    points_number = db.Column(db.Integer())
    ts_creation_date = db.Column(db.DateTime())
    temperature = db.Column(db.SmallInteger(), nullable=False)
    session_number = db.Column(db.SmallInteger(), nullable=False)
    notes = db.Column(db.String(4000))
    device_id = db.Column(UUID(as_uuid=True), ForeignKey('device.id_device'), nullable=False)
    station_id = db.Column(UUID(as_uuid=True), ForeignKey('station.id_station'), nullable=False)
    treatment_id = db.Column(UUID(as_uuid=True), ForeignKey('treatment.id_treatment'), nullable=False)
    pressure = db.Column(db.REAL())

    def __init__(self, medic, temperature, session_number, device_id, station_id, treatment_id, pressure=None, heating_duration=None,
                notes=None, points=()):
        if points is None:
            points = []

        self.pressure = pressure
        self.heating_duration = heating_duration
        self.id_session = uuid.uuid4()
        self.medic = medic
        self.points = points
        self.ts_creation_date = datetime.datetime.now()
        self.temperature = temperature
        self.session_number = session_number
        self.notes = notes
        self.device_id = device_id
        self.station_id = station_id
        self.treatment_id = treatment_id
        self.points_number = len(points)

    def __repr__(self):
        return '<Session Number: {} >'.format(self.session_number)
