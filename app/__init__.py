import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
# app.config.from_object(Config)
environment_configuration = os.environ['CONFIGURATION_SETUP']
app.config.from_object(environment_configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import routes, models
