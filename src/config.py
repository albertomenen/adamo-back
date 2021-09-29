import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./config/.{}.env'.format(os.environ.get('FLASK_ENV', 'dev')))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    S3_Credentials = {
        'ACCESS_KEY': os.environ.get('S3_ACCESS_KEY'),
        'SECRET_KEY': os.environ.get('S3_SECRET_KEY'),
        'BUCKET': os.environ.get('S3_BUCKET')
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(os.environ.get('POSTGRES_USER'),
                                                                   os.environ.get('POSTGRES_PASSWORD'),
                                                                   os.environ.get('POSTGRES_HOST'),
                                                                   os.environ.get('POSTGRES_PORT'),
                                                                   os.environ.get('POSTGRES_DB'))


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
    staging=StagingConfig
)

key = Config.SECRET_KEY
S3_Credentials = Config.S3_Credentials
