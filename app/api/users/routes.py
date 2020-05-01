from flask import jsonify, request, url_for, g, abort
from app import db
from app.models import User
from app.api.users import bp
from app.api.errors import bad_request

@bp.route('/users', methods=['GET'])
def index():
    users = User.query.all()
    return jsonify(User.as_json_collection(users))

@bp.route('/users/<int:id>', methods=['GET'])
def show(id):
    return jsonify(User.query.get_or_404(id).as_json())

@bp.route('/users', methods=['POST'])
def create():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User(data['email'], data['username'], data['password'], new_user=True)
    # user.from_json(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.as_json())
    response.status_code = 201
    response.headers['Location'] = url_for('users.show', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['PUT'])
def update(id):
    if g.current_user.id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_json(data, new_user=False)
    db.session.commit()
    return jsonify(user.as_json())


@bp.route('/users/<int:id>', methods=['DELETE'])
def destroy(id):
    pass


@bp.route('/users/<int:id>/followers', methods=['GET'])
def followers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.paginated_collection(user.followers, page, per_page,
                                   'users.followers', id=id)
    return jsonify(data)

@bp.route('/users/<int:id>/followed', methods=['GET'])
def followed(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.paginated_collection(user.followed, page, per_page,
                                   'users.followed', id=id)
    return jsonify(data)
