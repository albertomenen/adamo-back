from sqlalchemy.orm import relationship
from src import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class System(db.Model):
    __tablename__ = 'system'

    id_system = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    contact_name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, system_name, address, city, town, phone, email, contact_name):
        self.id_system = uuid.uuid4()
        self.system_name = system_name
        self.address = address
        self.city = city
        self.town = town
        self.phone = phone
        self.email = email
        self.contact_name = contact_name
        self.state = True

    def __repr__(self):
        return '<System Name: {} | email: {} >'.format(self.system_name, self.email)
