import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
# from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
# from . import db

db = SQLAlchemy()
migrate = Migrate()

# config_class = os.environ.get('CONFIG_CLASS')

def create_app(config=Config):
    # print(config_class)
    #  TODO : could pass environment as variable here
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.api.users import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.api.words import bp as words_bp
    app.register_blueprint(words_bp, url_prefix='/api')

    from app.api.user_words import bp as user_words_bp
    app.register_blueprint(user_words_bp, url_prefix='/api/my')

    from app.api.dictionaries import bp as dictionaries_bp
    app.register_blueprint(dictionaries_bp, url_prefix='/api/my')

    if not app.debug and not app.testing:

        if app.config['LOG_TO_STDOUT']:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(logging.INFO)
                app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/dictionary.log', maxBytes=10240,
                                               backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Dictionary Initialization')
    return app

from app import models
