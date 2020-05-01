from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import Dictionary, User
from app.api.errors import bad_request
from app.api.dictionaries import bp

@bp.route('/dictionaries', methods=['GET'])
def index():
    g.current_user = User.query.get(3)
    dictionaries = g.current_user.dictionaries.all()
    return jsonify(Dictionary.as_json_collection(dictionaries))

@bp.route('/dictionaries/<int:id>', methods=['GET'])
def show(id):
    g.current_user = User.query.get(3)
    dictionary = Dictionary.query.get_or_404(id)
    if dictionary in g.current_user.dictionaries:
        return jsonify(dictionary.as_json())
    else:
      abort(403)


@bp.route('/dictionaries', methods=['POST'])
def create():
    g.current_user = User.query.get(3)
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
