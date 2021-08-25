from .system import bp as system_api
from .auth import bp as auth_api
from .role import bp as role_api
from .user import bp as user_api
from .location import bp as location_api
from .group import bp as group_api
from .patient import bp as patient_api
from .station import bp as station_api
from .device import bp as device_api
from .treatment import bp as treatment_api
from .session import bp as session_api
from .date import bp as date_api
#from .timetable import bp as timetable_api


def register_controllers(app):
    app.register_blueprint(auth_api)
    app.register_blueprint(system_api, url_prefix='/system')
    app.register_blueprint(role_api, url_prefix='/role')
    app.register_blueprint(user_api)
    app.register_blueprint(location_api)
    app.register_blueprint(group_api, url_prefix='/group')
    app.register_blueprint(patient_api)
    app.register_blueprint(station_api)
    app.register_blueprint(device_api, url_prefix='/device')
    app.register_blueprint(treatment_api)
    app.register_blueprint(session_api)
    app.register_blueprint(date_api)
#    app.register_blueprint(timetable_api)
