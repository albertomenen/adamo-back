import os
from flask_migrate import Migrate
from src import create_app, db
from src import models
from src.controllers import register_controllers


app = create_app(os.environ.get('FLASK_ENV', 'dev'))
migrate = Migrate(app, db)
register_controllers(app)


# from src.models import Role
# ro = Role(**{'role_code': 'cosa', 'role_name': 'cosa'})
# app.logger.info(ro)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
