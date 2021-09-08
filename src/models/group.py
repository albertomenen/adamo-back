from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship


class Group(db.Model):
    __tablename__ = 'group'

    id_group = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Boolean(), default=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    locations = relationship("Location")

    def __init__(self, group_name, address, city, town, phone, contact_name, email):
        self.id_group = uuid.uuid4()
        self.group_name = group_name
        self.address = address
        self.city = city
        self.town = town
        self.phone = phone
        self.contact_name = contact_name
        self.state = True
        self.email = email

    def __repr__(self):
        return '<Group Name: {} | email: {} >'.format(self.group_name, self.email)
