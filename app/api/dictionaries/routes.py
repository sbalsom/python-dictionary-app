from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Dictionary
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.api.dictionaries import bp

@bp.route('/dictionaries', methods=['GET'])
@token_auth.login_required
def index():
    dictionaries = g.current_user.dictionaries.all()
    return jsonify(Dictionary.as_json_collection(dictionaries))

@bp.route('/dictionaries/<int:id>', methods=['GET'])
@token_auth.login_required
def show(id):
    dictionary = Dictionary.query.get_or_404(id)
    if dictionary in g.current_user.dictionaries:
        return jsonify(dictionary.as_json())
    else:
      abort(403)


@bp.route('/dictionaries', methods=['POST'])
@token_auth.login_required
def create():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('dictionary name cannot be blank')
    if  Dictionary.query.filter_by(name=data['name'], user_id=g.current_user.id).first():
        return bad_request('you already have a dictionary with that name')
    # TODO : use a constructor
    dictionary = Dictionary(name=data['name'], user_id=g.current_user.id)
    db.session.add(dictionary)
    db.session.commit()
    response = jsonify(dictionary.as_json())
    response.status_code = 201
    response.headers['Location'] = url_for('dictionaries.show', id=dictionary.id)
    return response

@bp.route('/dictionaries/<int:id>', methods=['PUT'])
@token_auth.login_required
def update(id):
    pass

@bp.route('/dictionaries/<int:id>', methods=['DELETE'])
@token_auth.login_required
def destroy(id):
    pass
