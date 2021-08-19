from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Device(db.Model):
    __tablename__ = 'device'

    id_device = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mac = db.Column(db.String(50), nullable=False, unique=True)
    serial_number = db.Column(db.String(50), nullable=False, unique=True)
    hw_version = db.Column(db.String(12), nullable=False)
    sw_version = db.Column(db.String(12), nullable=False)
    device_name = db.Column(db.String(50), nullable=False)
    station_id = db.Column(UUID(as_uuid=True), ForeignKey('station.id_station'))
    state = db.Column(db.Boolean(), default=True, nullable=False)

    station = relationship("Station")

    def __init__(self, mac, serial_number, hw_version, sw_version, device_name, station_id=None):
        self.id_device = uuid.uuid4()
        self.mac = mac
        self.serial_number = serial_number
        self.hw_version = hw_version
        self.sw_version = sw_version
        self.device_name = device_name
        self.station = station_id
        self.state = True

    def __repr__(self):
        return '<Device Name: {} >'.format(self.device_type)
