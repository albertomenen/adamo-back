from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Role(db.Model):
    __tablename__ = 'role'

    id_role = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_name = db.Column(db.String(50), nullable=False)
    role_code = db.Column(db.String(20))
    login_in_station = db.Column(db.Boolean)
    manage_practice_manager = db.Column(db.Boolean)
    manage_mp = db.Column(db.Boolean())
    manage_nmp = db.Column(db.Boolean())
    manage_patient = db.Column(db.Boolean())
    manage_sysadmin = db.Column(db.Boolean())
    manage_dev = db.Column(db.Boolean())
    get_patient = db.Column(db.Boolean())
    list_patient = db.Column(db.Boolean())
    detail_patient = db.Column(db.Boolean())
    manage_treatment = db.Column(db.Boolean())
    run_sesion = db.Column(db.Boolean())
    session_adjustment = db.Column(db.Boolean())
    session_stop = db.Column(db.Boolean())
    user_logout = db.Column(db.Boolean())
    app_login = db.Column(db.Boolean())
    app_select_patient = db.Column(db.Boolean())
    app_detail_patient = db.Column(db.Boolean())
    debug_app_hmi = db.Column(db.Boolean())
    manage_station = db.Column(db.Boolean())
    manage_group = db.Column(db.Boolean())
    manage_location = db.Column(db.Boolean())
    manage_devices = db.Column(db.Boolean())
    manage_roles = db.Column(db.Boolean())
    manage_dates = db.Column(db.Boolean())

    def __init__(self, role_name, role_code, login_in_station=False, manage_practice_manager=False, manage_mp=False,
                 manage_nmp=False, manage_patient=False, manage_sysadmin=False, manage_dev=False, get_patient=False,
                 list_patient=False, detail_patient=False, manage_treatment=False, run_sesion=False,
                 user_logout=False, app_login=False, app_select_patient=False, session_adjustment=False,
                 app_detail_patient=False, debug_app_hmi=False, manage_station=False, manage_group=False,
                 manage_location=False, session_stop=False, manage_devices=False, manage_roles=False,
                 manage_dates=False):
        self.id_role = uuid.uuid4()
        self.role_name = role_name
        self.role_code = role_code
        self.login_in_station = login_in_station
        self.manage_practice_manager = manage_practice_manager
        self.manage_mp = manage_mp
        self.manage_nmp = manage_nmp
        self.manage_patient = manage_patient
        self.manage_sysadmin = manage_sysadmin
        self.manage_dev = manage_dev
        self.get_patient = get_patient
        self.list_patient = list_patient
        self.detail_patient = detail_patient
        self.manage_treatment = manage_treatment
        self.run_sesion = run_sesion
        self.user_logout = user_logout
        self.app_login = app_login
        self.app_select_patient = app_select_patient
        self.app_detail_patient = app_detail_patient
        self.debug_app_hmi = debug_app_hmi
        self.manage_station = manage_station
        self.manage_group = manage_group
        self.manage_location = manage_location
        self.session_adjustment = session_adjustment
        self.session_stop = session_stop
        self.manage_devices = manage_devices
        self.manage_roles = manage_roles
        self.manage_dates = manage_dates

    def __repr__(self):
        return '<Role Name: {} >'.format(self.role_name)
