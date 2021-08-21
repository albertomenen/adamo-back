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
    ts_creation_date = db.Column(db.DateTime(), nullable=False)
    heating_duration = db.Column(db.REAL(), nullable=False)
    points = db.Column(db.JSON())
    # image_3D_color = db.Column(db.String(150), nullable=False)
    # image_3D_depth = db.Column(db.String(150), nullable=False)
    # image_thermic = db.Column(db.String(150), nullable=False)
    state = db.Column(db.Boolean(), default=True, nullable=False)
    ts_next_session = db.Column(db.REAL(), nullable=False)
    ts_end = db.Column(db.REAL(), nullable=False)
    width = db.Column(db.REAL(), nullable=False)
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
    next_session_station_id = db.Column(UUID(as_uuid=True), ForeignKey('station.id_station'))
    status = db.Column(db.String(12), nullable=False, default='new')
    last_session_date = db.Column(db.DateTime(), default=None)

    next_session_station = relationship('Station')

    def __init__(self, id_patient, medic, name, sessions_number, current_session_number, notes, temperature,
                 ts_creation_date, heating_duration, ts_next_session, ts_end, width, height, ppx, ppy,
                 fx, fy, model, coeff, depth_scale, mode, extrinsics, next_session_station_id, points=None):
        self.id_treatment = uuid.uuid4()
        self.id_patient = id_patient
        self.medic = medic
        self.name = name
        self.sessions_number = sessions_number
        self.current_session_number = current_session_number
        self.notes = notes
        self.temperature = temperature
        self.ts_creation_date = ts_creation_date
        self.heating_duration = heating_duration
        self.points = points
        self.state = 'new'
        self.ts_next_session = ts_next_session
        self.ts_end = ts_end
        self.width = width
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
        self.next_session_station_id = next_session_station_id
        self.last_session_date = None

    def __repr__(self):
        return '<Treatment Name: {} >'.format(self.name)
