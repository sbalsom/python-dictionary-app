from app.models import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity
)
from werkzeug.security import safe_str_cmp
from app.api.auth import bp
from flask import jsonify, request


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        identity = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        tokens = {
            'access_token': create_access_token(identity=identity, fresh=True),
            'refresh_token': create_refresh_token(identity=identity)
        }
        return jsonify(tokens), 200
    return jsonify('Wrong username or password'), 401

@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    token = {
        'access_token': create_access_token(identity=identity)
    }
    return jsonify(token), 200
