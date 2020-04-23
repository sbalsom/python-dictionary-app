import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  # todo: fetch all values from environment and get rid of child classes
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = os.environ.get('ENV')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    DEBUG = os.environ.get('DEBUG')
    TESTING = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

class ProductionConfig(Config):
    pass

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ENV = 'testing'
    FLASK_ENV = 'testing'
