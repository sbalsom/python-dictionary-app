from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Word
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.api.words import bp

@bp.route('/words', methods=['GET'])
@token_auth.login_required
def index():
    words = Word.query.all()
    json = Word.as_json_collection(words)
    return jsonify(json)

@bp.route('/words/<int:id>', methods=['GET'])
@token_auth.login_required
def show(id):
    word = Word.query.get_or_404(id)
    json = word.as_json()
    return jsonify(json)

@bp.route('/words', methods=['POST'])
@token_auth.login_required
def create():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('word cannot be blank')
    if Word.query.filter_by(name=data['name']).first():
        return bad_request('word already exists')

    word = Word(data["name"])
    db.session.add(word)
    db.session.commit()
    response = jsonify(word.as_json())
    response.status_code = 201
    response.headers['Location'] = url_for('words.show', id=word.id)
    return response


# @bp.route('/words/<int:id>', methods=['PUT'])
# @token_auth.login_required
# def update(id):
#     pass

# @bp.route('/words/<int:id>', methods=['DELETE'])
# @token_auth.login_required
# def destroy(id):
#     pass
