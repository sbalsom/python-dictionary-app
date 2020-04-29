from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Word
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.api.words import bp
from app.api.words.word import WordMethods

@bp.route('/words', methods=['GET'])
@token_auth.login_required
def index():
    words = Word.query.all()
    """
    is there a way that the class Word can inherit
    from WordMethods and then this method could
    be called on word or Word
    """
    json = WordMethods.as_json_collection(WordMethods, words)
    return jsonify(json)

@bp.route('/words/<int:id>', methods=['GET'])
@token_auth.login_required
def show(id):
    word = Word.query.get_or_404(id)
    json = WordMethods.as_json(word)
    return jsonify(json)

@bp.route('/words', methods=['POST'])
@token_auth.login_required
def create():
    """
    How to refactor this one .....
    from_json needs to be called on word ...
    so maybe in this case we use inheritance ...
    """
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('word cannot be blank')
    if Word.query.filter_by(name=data['name']).first():
        return bad_request('word already exists')
    word = Word()
    word.from_json(data)
    db.session.add(word)
    db.session.commit()
    response = jsonify(WordMethods.as_json(word))
    response.status_code = 201
    response.headers['Location'] = url_for('words.show', id=word.id)
    return response



@bp.route('/words/<int:id>', methods=['PUT'])
@token_auth.login_required
def update(id):
    pass

@bp.route('/words/<int:id>', methods=['DELETE'])
@token_auth.login_required
def destroy(id):
    pass
