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
        # when authenticated, return a fresh access token and a refresh token
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

@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    token = {
        'access_token': create_access_token(identity=identity)
    }
    return jsonify(token), 200



# username = user.username
#     tokens = {
#         'access_token': create_access_token(identity=username),
#         'refresh_token': create_refresh_token(identity=username)
#     }
#     response = jsonify(tokens)
#     response.status_code = 200
#     response.headers['Location'] = url_for('users.show', id=user.id)
#     return response
