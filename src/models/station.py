import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Station(db.Model):
    __tablename__ = 'station'

    id_station = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_location = db.Column(UUID(as_uuid=True), ForeignKey('location.id_location'))
    station_name = db.Column(db.String(150), nullable=False)
    state = db.Column(db.Boolean(), default=True, nullable=False)
    placed = db.Column(db.String(150))
    installation_date = db.Column(db.Date(), nullable=False)

    # device = relationship("Device")
    location = relationship('Location')

    def __init__(self, id_location, station_name, placed=None, installation_date=datetime.datetime.now()):
        self.id_station = uuid.uuid4()
        self.id_location = id_location
        self.station_name = station_name
        self.state = True
        self.placed = placed
        self.installation_date = installation_date

    def __repr__(self):
        return '<Station Name: {} | email: {} >'.format(self.location_name, self.email)
