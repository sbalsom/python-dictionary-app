from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Word
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.api.words import bp


@bp.route('/words', methods=['GET'])
@token_auth.login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Word.paginated_collection(Word.query, page, per_page, 'words.index')
    return jsonify(data)

@bp.route('/words/<int:id>', methods=['GET'])
@token_auth.login_required
def show(id):
    return jsonify(Word.query.get_or_404(id).as_json())

@bp.route('/words', methods=['POST'])
@token_auth.login_required
def create():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('word cannot be blank')
    if Word.query.filter_by(name=data['name']).first():
      # return the word that exists ?
        return bad_request('word already exists')
    word = Word()
    word.from_json(data)
    db.session.add(word)
    db.session.commit()
    response = jsonify(word.as_json())
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
