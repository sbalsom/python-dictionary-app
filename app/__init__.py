import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config, DevelopmentConfig
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()



def create_app(config=DevelopmentConfig):
  #  TODO : could pass environment as variable here
  app = Flask(__name__)
  app.config.from_object(config)
  db.init_app(app)
  migrate.init_app(app, db)
  login.init_app(app)

  from app.auth import bp as auth_bp
  app.register_blueprint(auth_bp, url_prefix='/auth')

  # from app.main import bp as main_bp
  # app.register_blueprint(main_bp)

  from app.api import bp as api_bp
  app.register_blueprint(api_bp, url_prefix='/api')
  #  TODO : Blueprint registration ?
  # if not app.debug and not app.testing:
  #  TODO : Logging setup
  return app

from app import routes, models
