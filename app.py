import os
from flask_migrate import Migrate
from src import create_app, db
from src.controllers import register_controllers
from flask_cors import CORS


app = create_app(os.environ.get('FLASK_ENV', 'dev'))
migrate = Migrate(app, db)
register_controllers(app)
CORS(app)

if __name__ == '__main__':
   app.run(host='0.0.0.0')
