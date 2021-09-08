import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Treatment(db.Model):
    __tablename__ = 'treatment'

    id_treatment = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_patient = db.Column(UUID(as_uuid=True), ForeignKey('palias.id_palias'), nullable=False)
    medic = db.Column(UUID(as_uuid=True), ForeignKey('user.id_user'), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    sessions_number = db.Column(db.SmallInteger(), nullable=False)
    current_session_number = db.Column(db.SmallInteger(), nullable=False)
    notes = db.Column(db.String(4000))
    temperature = db.Column(db.SmallInteger(), nullable=False)
    ts_creation_date = db.Column(db.DateTime())
    heating_duration = db.Column(db.REAL(), nullable=False)
    points = db.Column(db.JSON())
    pressure = db.Column(db.REAL())
    image_3D = db.Column(db.String(150))
    image_thermic = db.Column(db.String(150))
    image_thermic_bin = db.Column(db.String(150))
    image_thermic_width = db.Column(db.Integer())
    image_thermic_height = db.Column(db.Integer())
    image_thermic_depht = db.Column(db.Integer())
    state = db.Column(db.String(12), nullable=False, default='new')
    weight = db.Column(db.REAL())
    height = db.Column(db.REAL(), nullable=False)
    ppx = db.Column(db.REAL(), nullable=False)
    ppy = db.Column(db.REAL(), nullable=False)
    fx = db.Column(db.REAL(), nullable=False)
    fy = db.Column(db.REAL(), nullable=False)
    model = db.Column(db.String(40), nullable=False)
    coeff = db.Column(db.String(100), nullable=False)
    depth_scale = db.Column(db.REAL(), nullable=False)
    mode = db.Column(db.String(45), nullable=False)
    extrinsics = db.Column(db.String(200), nullable=False)
    last_session_date = db.Column(db.Date(), default=None)
    next_session_date = db.Column(db.Date(), default=None)
    injury = db.Column(db.String(100))
    injury_kind = db.Column(db.String(100))
    injury_cause = db.Column(db.String(100))
    move = db.Column(db.String(10))

    sessions = relationship('Session')

    def __init__(self, id_patient, move, medic, name, temperature, heating_duration,
                 weight, height, ppx, ppy, fx, fy, model, coeff, depth_scale, mode, extrinsics,
                 sessions_number, notes=None, points=None, injury=None,
                 injury_kind=None, injury_cause=None, pressure=None, image_thermic_width=None,
                 image_thermic_height=None, image_thermic_depht=None):
        self.pressure = pressure
        self.move = move
        self.id_treatment = uuid.uuid4()
        self.id_patient = id_patient
        self.medic = medic
        self.name = name
        self.sessions_number = sessions_number
        self.current_session_number = 0
        self.notes = notes
        self.temperature = temperature
        self.ts_creation_date = datetime.datetime.now()
        self.heating_duration = heating_duration
        self.points = points
        self.state = 'new'
        self.weight = weight
        self.height = height
        self.ppx = ppx
        self.ppy = ppy
        self.fx = fx
        self.fy = fy
        self.model = model
        self.coeff = coeff
        self.depth_scale = depth_scale
        self.mode = mode
        self.extrinsics = extrinsics
        self.last_session_date = None
        self.injury_cause = injury_cause
        self.injury = injury
        self.injury_kind = injury_kind
        self.image_thermic_width = image_thermic_width
        self.image_thermic_height = image_thermic_height
        self.image_thermic_depht = image_thermic_depht

    def __repr__(self):
        return '<Treatment Name: {} >'.format(self.name)
