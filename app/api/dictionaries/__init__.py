from flask import Blueprint

bp = Blueprint('dictionaries', __name__)

from app.api.dictionaries import routes
# from app.api import errors, tokens
