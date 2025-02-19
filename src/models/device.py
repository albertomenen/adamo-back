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
    group_id = db.Column(UUID(as_uuid=True), ForeignKey('group.id_group'))
    station_id = db.Column(UUID(as_uuid=True), ForeignKey('station.id_station'))

    group = relationship("Group")
    station = relationship("Station")

    def __init__(self, mac, serial_number, hw_version, sw_version, device_name, station_id=None, group_id=None):
        self.id_device = uuid.uuid4()
        self.mac = mac
        self.serial_number = serial_number
        self.hw_version = hw_version
        self.sw_version = sw_version
        self.device_name = device_name
        self.station_id = station_id
        self.group_id = group_id

    def __repr__(self):
        return '<Device Name: {} >'.format(self.device_type)
