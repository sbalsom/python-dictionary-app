import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config, DevelopmentConfig
from flask_login import LoginManager
# from . import db

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


config_class = os.environ.get('CONFIG_CLASS')

def create_app(config=DevelopmentConfig):
  print(config_class)
  #  TODO : could pass environment as variable here
  app = Flask(__name__)
  app.config.from_object(config)
  db.init_app(app)
  migrate.init_app(app, db)

  # from app.auth import bp as auth_bp
  # app.register_blueprint(auth_bp, url_prefix='/auth')

  # from app.main import bp as main_bp
  # app.register_blueprint(main_bp)
  login.init_app(app)

  from app.api.users import bp as api_bp
  app.register_blueprint(api_bp, url_prefix='/api')

  from app.api.words import bp as words_bp
  app.register_blueprint(words_bp, url_prefix='/api')

  from app.api.user_words import bp as user_words_bp
  app.register_blueprint(user_words_bp, url_prefix='/api/my')

  from app.api.dictionaries import bp as dictionaries_bp
  app.register_blueprint(dictionaries_bp, url_prefix='/api/my')


  #  TODO : Blueprint registration ?
  # if not app.debug and not app.testing:
  #  TODO : Logging setup
  return app

from app import models
