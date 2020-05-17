from flask import jsonify, request, url_for, g, abort
from app import db
from app.api.errors import bad_request
from app.api.user_words import bp
from app.models import User, Word, Dictionary, UserWord, Translation
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


@bp.route('/words', methods=['GET'])
@jwt_required
def index():
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity['username']).first()
    g.current_user = user
    words = g.current_user.words
    return jsonify(UserWord.as_json_collection(words))

@bp.route('/words/<int:id>', methods=['GET'])
@jwt_required
def show(id):
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity['username']).first()
    g.current_user = user
    data = request.get_json()
    w_id = data["word_id"]
    d_id = data["dictionary_id"]
    u_id = g.current_user.id
    user_word = UserWord.query.get_or_404([u_id, w_id, d_id])
    return jsonify(user_word.as_json())

@bp.route('/words', methods=['POST'])
@jwt_required
def create():
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity['username']).first()
    g.current_user = user
    data = request.get_json() or {}
    dictionary = Dictionary.query.get(data['dictionary_id'])
    if dictionary in g.current_user.dictionaries:
        dictionary_id = dictionary.id
    else:
        abort(403)
    if 'name' not in data:
        return bad_request('word cannot be blank')
    if Word.query.filter_by(name=data['name']).first():
        word = Word.query.filter_by(name=data['name']).first()
    else:
        word = Word(data["name"], created_by=g.current_user.username)
        db.session.add(word)
        db.session.commit()
    user_word = UserWord(word.id, dictionary_id, g.current_user.id)
    db.session.add(user_word)
    try:
        db.session.commit()
    except IntegrityError:
        return bad_request('word already is in your dictionary')
    if 'description' in data:
        user_word.description = data['description']
        db.session.add(user_word)
        db.session.commit()
    if 'translations' in data:
        for t in data['translations']:
            trns = Translation(word.id, dictionary.id, t)
            db.session.add(trns)
            db.session.commit()
    response = jsonify(word.as_json())
    response.status_code = 201
    response.headers['Location'] = url_for('words.show', id=word.id)
    return response

@bp.route('/words/<int:id>', methods=['PUT'])
def update(id):
    pass

@bp.route('/words/<int:id>', methods=['DELETE'])
def destroy(id):
    pass
