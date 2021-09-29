from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_rest_paginate import Pagination
from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
pagination = Pagination()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    pagination.init_app(app, db)
    mail.init_app(app)
    return app
