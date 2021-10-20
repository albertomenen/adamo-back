import datetime

from sqlalchemy import ForeignKey

from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Session(db.Model):
    __tablename__ = 'session'

    id_session = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medic = db.Column(UUID(as_uuid=True), ForeignKey('user.id_user'), nullable=False)
    points = db.Column(db.JSON())

    image_3D_depth = db.Column(db.String(150))
    image_3D_color = db.Column(db.String(150))
    image_thermic = db.Column(db.String(150))
    image_thermic_data = db.Column(db.String(150))
    image_thermic_width = db.Column(db.Integer())
    image_thermic_height = db.Column(db.Integer())
    image_thermic_depth = db.Column(db.Integer())

    ts_creation_date = db.Column(db.DateTime())
    session_number = db.Column(db.SmallInteger(), nullable=False)
    notes = db.Column(db.String(4000))
    device_id = db.Column(UUID(as_uuid=True), ForeignKey('device.id_device'), nullable=False)
    station_id = db.Column(UUID(as_uuid=True), ForeignKey('station.id_station'), nullable=False)
    treatment_id = db.Column(UUID(as_uuid=True), ForeignKey('treatment.id_treatment'), nullable=False)

    def __init__(self, medic, session_number, device_id, station_id, treatment_id,
                 notes=None, image_thermic_width=None, image_thermic_height=None,
                 image_thermic_depth=None, points=None):

        self.id_session = uuid.uuid4()
        self.medic = medic
        self.ts_creation_date = datetime.datetime.now()
        self.session_number = session_number
        self.notes = notes
        self.device_id = device_id
        self.station_id = station_id
        self.treatment_id = treatment_id
        self.image_thermic_width = image_thermic_width
        self.image_thermic_height = image_thermic_height
        self.image_thermic_depth = image_thermic_depth
        self.points = points

    def __repr__(self):
        return '<Session Number: {} >'.format(self.session_number)
