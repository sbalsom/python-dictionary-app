from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Dictionary, User
from app.api.errors import bad_request
from app.api.dictionaries import bp
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

@bp.route('/dictionaries', methods=['GET'])
@jwt_required
def index():
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity['username']).first()
    g.current_user = user
    dictionaries = g.current_user.dictionaries.all()
    return jsonify(Dictionary.as_json_collection(dictionaries))

@bp.route('/dictionaries/<int:id>', methods=['GET'])
@jwt_required
def show(id):
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity['username']).first()
    g.current_user = user
    dictionary = Dictionary.query.get_or_404(id)
    if dictionary in g.current_user.dictionaries:
        return jsonify(dictionary.as_json())
    else:
      abort(403)


@bp.route('/dictionaries', methods=['POST'])
@jwt_required
def create():
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity['username']).first()
    g.current_user = user
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('dictionary name cannot be blank')
    if  Dictionary.query.filter_by(name=data['name'], user_id=g.current_user.id).first():
        return bad_request('you already have a dictionary with that name')
    dictionary = Dictionary(data['name'], g.current_user.id)
    db.session.add(dictionary)
    db.session.commit()
    response = jsonify(dictionary.as_json())
    response.status_code = 201
    response.headers['Location'] = url_for('dictionaries.show', id=dictionary.id)
    return response

@bp.route('/dictionaries/<int:id>', methods=['PUT'])
def update(id):
    pass

@bp.route('/dictionaries/<int:id>', methods=['DELETE'])
def destroy(id):
    pass
