from flask import Blueprint

bp = Blueprint('words', __name__)

from app.api.words import routes
from app.api import errors, tokens
