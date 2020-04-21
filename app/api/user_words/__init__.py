from flask import Blueprint

bp = Blueprint('user_words', __name__)

from app.api.user_words import routes
from app.api import errors, tokens
