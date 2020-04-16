import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

db = SQLQlchemy()
migrate = Migrate()
login = LoginManager()

# from app.auth import bp as auth_bp
# app.register_blueprint(auth_bp, url_prefix='/auth')

def create_app():
  #  TODO : could pass environment as variable here
  app = Flask(__name__)
  environment_configuration = os.environ['CONFIGURATION_SETUP']
  app.config.from_object(environment_configuration)
  db.init_app(app)
  migrate.init_app(app, db)
  login.init_app(app)

  #  TODO : Blueprint registration ?
  # if not app.debug and not app.testing:
  #  TODO : Logging setup
  return app

from app import routes, models
