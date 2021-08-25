import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Date(db.Model):
    __tablename__ = 'date'

    id_date = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    #id_timetable = db.Column(UUID(as_uuid=True), ForeignKey('timetable.id_timetable'), nullable=False)
    id_medic = db.Column(UUID(as_uuid=True), ForeignKey('user.id_user'), nullable=False)
    id_patient = db.Column(UUID(as_uuid=True), ForeignKey('patient.id_patient'), nullable=False)
    id_station = db.Column(UUID(as_uuid=True), ForeignKey('station.id_station'), nullable=False)
    id_treatment = db.Column(UUID(as_uuid=True), ForeignKey('treatment.id_treatment'), nullable=False)
    day = db.Column(db.Date(), nullable=False)
    from_hour = db.Column(db.Time(), nullable=False)
    to_hour = db.Column(db.Time(), nullable=False)
    presented = db.Column(db.Boolean(), default=False, nullable=False)

    def __init__(self, id_medic, id_patient, day, from_hour, to_hour, id_treatment, id_station):
        self.id_date = uuid.uuid4()
        self.id_medic = id_medic
        self.id_patient = id_patient
        year, month, day = map(int, day.split('-'))
        self.day = datetime.date(year, month, day)
        self.from_hour = from_hour
        self.to_hour = to_hour
        self.id_station = id_station
        self.id_treatment = id_treatment
