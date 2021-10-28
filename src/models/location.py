from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Location(db.Model):
    __tablename__ = 'location'

    id_location = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_group = db.Column(UUID(as_uuid=True), ForeignKey('group.id_group'))
    location_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Boolean(), default=True, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, location_name, id_group, address, city, town, phone, contact_name, email):
        self.id_location = uuid.uuid4()
        self.location_name = location_name
        self.id_group = id_group
        self.address = address
        self.city = city
        self.town = town
        self.phone = phone
        self.contact_name = contact_name
        self.state = True
        self.email = email

    def __repr__(self):
        return '<Location Name: {} | email: {} >'.format(self.location_name, self.email)
