from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Word
from app.api.errors import bad_request
from app.api.words import bp

from flask_jwt_extended import jwt_required, get_jwt_identity

@bp.route('/words', methods=['GET'])
@jwt_required
def index():
    username = get_jwt_identity()
    words = Word.query.all()
    json = Word.as_json_collection(words)
    return jsonify(json)

@bp.route('/words/<int:id>', methods=['GET'])
@jwt_required
def show(id):
    word = Word.query.get_or_404(id)
    json = word.as_json()
    return jsonify(json)

@bp.route('/words/<int:id>', methods=['DELETE'])
def destroy(id):
    pass
