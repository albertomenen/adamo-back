from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Patient(db.Model):
    __tablename__ = 'patient'

    id_patient = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user = db.Column(UUID(as_uuid=True), ForeignKey('user.id_user'), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    profession = db.Column(db.String(150))
    observations = db.Column(db.String(4000))
    birthdate = db.Column(db.Date(), nullable=False)
    identification = db.Column(db.String(9), nullable=False)
    state = db.Column(db.Boolean(), default=True, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    active_treatments = db.Column(db.Integer(), nullable=False, default=0)

    country = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    race = db.Column(db.String(20))
    complexity = db.Column(db.String(100))
    weight = db.Column(db.REAL())
    height = db.Column(db.REAL())
    allergies = db.Column(db.String(500))
    medication = db.Column(db.String(500))

    user = relationship('User')

    def __init__(self, id_user, address, city, town, phone, email, birthdate, name, last_name, identification, country,
                 gender, race, complexity, width, height, allergies, medication, profession=None, observations=None):
        self.id_patient = uuid.uuid4()
        self.id_user = id_user
        self.address = address
        self.city = city
        self.town = town
        self.phone = phone
        self.state = True
        self.email = email
        self.birthdate = birthdate
        self.identification = identification
        self.profession = profession
        self.observations = observations
        self.name = name
        self.last_name = last_name
        self.active_treatments = 0
        self.country = country
        self.gender = gender
        self.race = race
        self.complexity = complexity
        self.width = width
        self.height = height
        self.allergies = allergies
        self.medication = medication

    def __repr__(self):
        return '<Patient Name: {} {} | email: {} >'.format(self.name, self.last_name, self.email)


class PAlias(db.Model):
    __tablename__ = 'palias'

    id_palias = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient = db.Column(UUID(as_uuid=True), ForeignKey('patient.id_patient'), nullable=True)

    treatment = relationship('Treatment')

    def __init__(self, patient):
        self.id_alias = uuid.uuid4()
        self.patient = patient
